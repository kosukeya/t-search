"""r4b-v1: record comparison, interference and a fixed history family.

Exact Born probabilities (up to roundoff), no shots or outcome selection.
Intermediate history projectors are not measurements in the actual circuit.
"""
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path
import platform
import runpy

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
B = runpy.run_path(str(ROOT / "experiments/r2_shared_records.py"))
BASELINE = "9e32fac74ddc7cc2e60e5008df49dbf184050cff"
ATOL = 1e-10
CONTEXTS = ("read", "undo", "copy_undo")
OUTCOMES = tuple(itertools.product((1, -1), (0, 1), (0, 1)))
RECORD_OUTCOMES = tuple(itertools.product((0, 1), repeat=2))
HISTORY_LABELS = tuple(itertools.product((0, 1), range(8)))


def tensor(*values):
    out = np.array([[1.]], complex)
    for value in values:
        out = np.kron(out, value)
    return out


def cnot(control, target):
    """Indices 0,1,2,3 denote S,F1,F2,E, most significant first."""
    if control not in range(4) or target not in range(4) or control == target:
        raise ValueError("Distinct control and target indices in range(4) required")
    matrix = np.zeros((16, 16), complex)
    for col in range(16):
        row = col ^ (1 << (3-target)) if col & (1 << (3-control)) else col
        matrix[row, col] = 1
    return matrix


def probes():
    vectors = {"zero": [1, 0], "one": [0, 1],
               "plus": np.array([1, 1])/np.sqrt(2),
               "plus_i": np.array([1, 1j])/np.sqrt(2)}
    return {name: np.outer(v, np.conjugate(v)) for name, v in vectors.items()}


def operations(context, environment):
    if context not in CONTEXTS or environment not in (0, 1):
        raise ValueError("Unknown context or environment condition")
    identity = np.eye(16, dtype=complex)
    return [cnot(0, 1), cnot(1, 3) if environment else identity.copy(),
            cnot(1, 2) if context != "undo" else identity.copy(),
            cnot(0, 1) if context != "read" else identity.copy()]


def model(context, environment):
    ops = operations(context, environment)
    identity = np.eye(2)
    z = [np.diag([1, 0]), np.diag([0, 1])]
    x = {s: np.array([[1, s], [s, 1]])/2 for s in (1, -1)}
    terminal = np.array([tensor(x[s], z[f], z[g], identity)
                         for s, f, g in OUTCOMES])
    pointers = [tensor(identity, z[b], identity, identity) for b in (0, 1)]
    record_readouts = np.array([tensor(identity, z[f], z[g], identity)
                                for f, g in RECORD_OUTCOMES])
    cumulative = [np.eye(16, dtype=complex)]
    for op in ops:
        cumulative.append(op @ cumulative[-1])
    embedding = np.eye(16, dtype=complex)[:, [0, 8]]
    jmap = np.vstack([v @ embedding for v in cumulative])/np.sqrt(5)
    continuation = ops[3] @ ops[2]
    chains = np.array([terminal[o] @ continuation @ pointers[b] @ cumulative[2]
                       for b, o in HISTORY_LABELS])
    return {"operations": ops, "cumulative": cumulative, "embedding": embedding,
            "J": jmap, "terminal": terminal, "pointers": pointers,
            "record_readouts": record_readouts, "chains": chains,
            "continuation": continuation}


def packed(matrix):
    """Store every nonzero complex entry; no tolerance-based sparsification."""
    return {"shape": list(matrix.shape), "entries": [
        [int(i), int(j), float(matrix[i, j].real), float(matrix[i, j].imag)]
        for i, j in zip(*np.nonzero(matrix))]}


def probabilities(projectors, state):
    # Do not clip or renormalize: diagnostics must expose numerical failures.
    return np.einsum("oij,ji->o", projectors, state).real


def analytic_probabilities(rho, context, environment):
    """Closed formulas from r4b-v1, independent of gate matrices."""
    out = []
    for s, f, g in OUTCOMES:
        if context == "undo":
            p = (.5 + s*rho[0, 1].real*(1-environment)) if (f, g) == (0, 0) else 0.
        elif context == "read":
            p = rho[f, f].real/2 if f == g else 0.
        else:
            p = rho[g, g].real/2 if f == 0 else 0.
        out.append(p)
    return np.array(out)


def history_statistics(rho0, states, circuit):
    chains = circuit["chains"]
    d = np.einsum("aij,jk,bik->ab", chains, rho0, chains.conj(), optimize=True)
    off = d - np.diag(np.diag(d))
    dephased = sum(p @ states[2] @ p for p in circuit["pointers"])
    v = circuit["continuation"]
    counterfactual = probabilities(circuit["terminal"], v @ dephased @ v.conj().T)
    # Coarse-graining in one actual context: sum amplitudes, including cross terms.
    coarse = np.array([d[np.ix_([o, o+8], [o, o+8])].sum().real for o in range(8)])
    diagonal = np.diag(d).real.reshape(2, 8).sum(axis=0)
    max_abs = float(np.max(np.abs(off)))
    max_real = float(np.max(np.abs(off.real)))
    return {"decoherence_functional": packed(d),
            "max_offdiagonal_abs": max_abs, "max_offdiagonal_real_abs": max_real,
            "medium_decoherent": max_abs <= ATOL, "weakly_consistent": max_real <= ATOL,
            "coarse_probabilities": coarse.tolist(),
            "diagonal_sum_probabilities": diagonal.tolist(),
            "inserted_measurement_probabilities": counterfactual.tolist(),
            "diagonal_vs_inserted_max_error": float(np.max(np.abs(diagonal-counterfactual))),
            "hermitian_residual_fro": float(np.linalg.norm(d-d.conj().T)),
            "minimum_eigenvalue": float(np.linalg.eigvalsh(d).min()),
            "diagonal_normalization_error": float(abs(np.trace(d)-1))}


def case(context, environment, name, rho, circuit=None):
    rho = B["validate_state"](rho, 2)
    circuit = model(context, environment) if circuit is None else circuit
    rho0 = circuit["embedding"] @ rho @ circuit["embedding"].conj().T
    states = [rho0]
    for op in circuit["operations"]:
        states.append(op @ states[-1] @ op.conj().T)
    observed = probabilities(circuit["terminal"], states[-1])
    expected = analytic_probabilities(rho, context, environment)
    history = history_statistics(rho0, states, circuit)
    inserted = np.array(history["inserted_measurement_probabilities"])
    expected_inserted = analytic_probabilities(np.diag(np.diag(rho)), context, environment)
    history["actual_vs_inserted_total_variation"] = float(np.abs(observed-inserted).sum()/2)
    history["coarse_vs_actual_max_error"] = float(np.max(np.abs(np.array(history["coarse_probabilities"])-observed)))
    sensitive = context == "undo" and environment == 0
    analytic = {"probabilities": expected.tolist(),
                "inserted_measurement_probabilities": expected_inserted.tolist(),
                "max_offdiagonal_abs": float(abs(rho[0, 1])/2) if sensitive else 0.,
                "max_offdiagonal_real_abs": float(abs(rho[0, 1].real)/2) if sensitive else 0.,
                "actual_vs_inserted_total_variation": float(abs(rho[0, 1].real)) if sensitive else 0.}
    errors = [float(np.max(np.abs(observed-expected))),
              float(np.max(np.abs(inserted-expected_inserted)))]
    errors.extend(abs(history[key]-analytic[key]) for key in
                  ("max_offdiagonal_abs", "max_offdiagonal_real_abs", "actual_vs_inserted_total_variation"))
    jmap = circuit["J"]
    omega = jmap @ rho @ jmap.conj().T
    event_rows = []
    for j, state in enumerate(states):
        block = omega[16*j:16*(j+1), 16*j:16*(j+1)]
        event_rows.append({"event": j, "state_G": packed(state),
            "state_Q": packed(B["marginal"](state, (0, 1, 2))),
            "z_record_probabilities": probabilities(circuit["record_readouts"], state).tolist(),
            "state_diagnostics": B["state_diagnostics"](state),
            "history_weight": float(np.trace(block).real),
            "history_reconstruction_residual_fro": float(np.linalg.norm(5*block-state))})
    b = {"zero": 0, "one": 1}.get(name)
    calibration = None if b is None else {
        "prepared_z_value": b,
        "F1_correct": float(sum(observed[o] for o, (_, f, _) in enumerate(OUTCOMES) if f == b)),
        "F2_correct": float(sum(observed[o] for o, (_, _, g) in enumerate(OUTCOMES) if g == b))}
    return {"context": context, "environment": environment, "input": name,
            "input_state": packed(rho), "terminal_event": 4,
            "terminal_probabilities": observed.tolist(),
            "terminal_normalization_error": float(abs(observed.sum()-1)),
            "minimum_probability": float(min(observed.min(), inserted.min())),
            "x_plus_probability": float(observed[:4].sum()),
            "record_agreement": float(sum(observed[o] for o, (_, f, g) in enumerate(OUTCOMES) if f == g)),
            "calibration": calibration, "events": event_rows, "history": history,
            "global_history": {"isometry_residual_fro": float(np.linalg.norm(jmap.conj().T @ jmap-np.eye(2))),
                "propagation_residual_fro": float(np.linalg.norm(np.vstack([
                    jmap[16*(j+1):16*(j+2)]-op @ jmap[16*j:16*(j+1)]
                    for j, op in enumerate(circuit["operations"])]))),
                "normalization_error": float(abs(np.trace(omega)-1))},
            "analytic": analytic, "analytic_max_error": float(max(errors))}


def run_experiment():
    rows = []
    for context, environment in itertools.product(CONTEXTS, (0, 1)):
        circuit = model(context, environment)  # same process for all four inputs
        rows.extend(case(context, environment, name, rho, circuit) for name, rho in probes().items())
    calibrations = []
    for context, environment in itertools.product(CONTEXTS, (0, 1)):
        selected = [r for r in rows if r["context"] == context and r["environment"] == environment and r["calibration"] is not None]
        calibrations.append({"context": context, "environment": environment,
            "equal_z_input_weights": [.5, .5],
            "F1_correct": sum(r["calibration"]["F1_correct"] for r in selected)/2,
            "F2_correct": sum(r["calibration"]["F2_correct"] for r in selected)/2,
            "record_agreement": sum(r["record_agreement"] for r in selected)/2})
    paths = ("experiments/r4b_record_comparison.py", "tests/test_r4b_record_comparison.py",
             "experiments/r2_shared_records.py", "docs/t_search_r4a_comparative_audit.md",
             "docs/t_search_r4_protocol.md")
    diagnostics = [r["analytic_max_error"] for r in rows]
    for r in rows:
        diagnostics.extend([r["terminal_normalization_error"], max(0., -r["minimum_probability"]),
                            r["history"]["coarse_vs_actual_max_error"],
                            r["history"]["diagonal_vs_inserted_max_error"],
                            r["history"]["hermitian_residual_fro"],
                            r["history"]["diagonal_normalization_error"],
                            max(0., -r["history"]["minimum_eigenvalue"])])
        diagnostics.extend(r["global_history"].values())
        for event in r["events"]:
            sd = event["state_diagnostics"]
            diagnostics.extend([event["history_reconstruction_residual_fro"],
                                abs(event["history_weight"]-.2), sd["trace_error"],
                                sd["hermitian_residual_fro"], max(0., -sd["minimum_eigenvalue"])])
    maximum = float(max(diagnostics))
    return {"specification": "r4b-v1", "absolute_tolerance": ATOL, "relative_tolerance": 0,
        "provenance": {"baseline_commit": BASELINE, "python": platform.python_version(),
            "numpy": np.__version__, "source_sha256": {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}},
        "qubit_order": ["S", "F1", "F2", "E"],
        "access": {"terminal_readout": ["S", "F1", "F2"],
                   "environment_write_event": 2, "environment_readout_or_recovery": False},
        "events": ["ready", "after_S_to_F1", "after_environment_step", "after_copy_or_identity", "after_undo_or_identity"],
        "terminal_observables": ["X_S", "Z_F1", "Z_F2"],
        "outcome_labels": [list(o) for o in OUTCOMES],
        "record_outcome_labels": [list(o) for o in RECORD_OUTCOMES],
        "history_labels": [{"F1_z_at_event_2": b, "terminal_outcome_index": o} for b, o in HISTORY_LABELS],
        "probability_semantics": {"terminal": "Actual circuit, no intermediate projection",
            "events": "State predictions, not extra physical readouts",
            "history_diagonal": "Weights; classical history probabilities only when the specified consistency condition holds",
            "inserted_measurement": "Different circuit with nonselective F1-Z measurement at event 2"},
        "cases": rows, "calibration_summary": calibrations,
        "summary": {"case_count": len(rows), "outcomes_per_case": 8, "histories_per_case": 16,
            "events_per_case": 5, "medium_decoherent_count": sum(r["history"]["medium_decoherent"] for r in rows),
            "weakly_consistent_count": sum(r["history"]["weakly_consistent"] for r in rows),
            "max_analytic_error": max(r["analytic_max_error"] for r in rows),
            "max_verification_residual": maximum, "all_checks_within_tolerance": maximum <= ATOL},
        "limits": ["Fixed family and exact model probabilities, not finite-sample guarantees",
            "No hidden realized friend outcome or unrecorded external classical log",
            "CPL, single outcomes, Local Friendliness and ontological becoming are not certified",
            "Five-event register is a mathematical representation, not a physical clock",
            "S interference loss in copy_undo is not optimal Q-access irrecoverability",
            "Original pilot remains blocked and Stage 17 remains frozen"]}


if __name__ == "__main__":
    result = run_experiment()
    if not result["summary"]["all_checks_within_tolerance"]:
        raise RuntimeError("R4b verification failed; result file not overwritten")
    (ROOT / "results/r4b_record_comparison.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False)+"\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2))
