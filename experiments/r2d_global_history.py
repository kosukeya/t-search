"""R2d: the frozen R2b circuit as an open four-event constraint history.

The event register is a representation, not an added accessible physical clock.
Noise/readout dilations and alternative clocks are outside this construction.
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
ATOL = B["ATOL"]
EVENTS = tuple(range(4))
BASELINE = "04eed933cdfff3b4bd88088e5ffddadef40acc52"


def steps(condition):
    if condition not in B["CONDITIONS"]:
        raise ValueError("Unknown condition")
    identity = np.eye(16, dtype=complex)
    return [B["cnot"](k) if (condition != "no_record" and
            (k != 3 or condition == "records_E_on")) else identity.copy()
            for k in (1, 2, 3)]


def cumulative(condition):
    values = [np.eye(16, dtype=complex)]
    for u in steps(condition):
        values.append(u @ values[-1])
    return values


def construction(condition):
    """P enforces propagation; the separate boundary fixes ancillas to 000."""
    values = cumulative(condition)
    w = np.vstack(values)/2  # all possible 16-dimensional initial states
    jmap = w[:, [0, 8]]  # only ready ancillas, arbitrary S
    propagation = np.zeros((48, 64), complex)
    for j, u in enumerate(steps(condition)):
        propagation[16*j:16*(j+1), 16*j:16*(j+1)] = -u/np.sqrt(2)
        propagation[16*j:16*(j+1), 16*(j+1):16*(j+2)] = np.eye(16)/np.sqrt(2)
    ready = np.zeros((16, 16), complex)
    ready[0, 0] = ready[8, 8] = 1
    boundary = np.zeros((16, 64), complex)
    boundary[:, :16] = np.eye(16)-ready
    hprop = propagation.conj().T @ propagation
    hready = hprop + boundary.conj().T @ boundary
    return {"V": values, "W": w, "J": jmap, "P": propagation,
            "boundary": boundary, "H_prop": hprop, "H_ready": hready}


def history_state(rho, condition):
    rho = B["validate_state"](rho, 2)
    jmap = construction(condition)["J"]
    return jmap @ rho @ jmap.conj().T


def event_block(operator, event):
    if event not in EVENTS:
        raise ValueError("Event must be 0, 1, 2 or 3")
    return operator[16*event:16*(event+1), 16*event:16*(event+1)]


def conditioned_operator(operator, event):
    """Linear reduction on the history image, whose event weight is 1/4.

    This scaled block map is not claimed TP on arbitrary 64-dimensional states.
    """
    return 4*event_block(operator, event)


def joint_instrument_kraus(event, readout):
    if event not in EVENTS:
        raise ValueError("Unknown event")
    operators = []
    for outcome, projector in B["readout_kraus"](readout):
        k = np.zeros((16, 64), complex)
        k[:, 16*event:16*(event+1)] = projector
        operators.append((outcome, k))
    return operators


def calibration(condition, event):
    joint = np.zeros((2, 2, 2))
    for b in (0, 1):
        omega = history_state(np.diag([1-b, b]), condition)
        for (x, y), k in joint_instrument_kraus(event, (1, 2)):
            joint[b, x, y] = 2*float(np.trace(k @ omega @ k.conj().T).real)
    errors = [float(sum(joint[b, x, y] for b, x, y in itertools.product((0, 1), repeat=3)
                        if (x, y)[k] != b)) for k in (0, 1)]
    agreement = float(sum(joint[b, x, x] for b, x in itertools.product((0, 1), repeat=2)))
    written = [condition != "no_record" and event >= k for k in (1, 2)]
    expected_errors = [0. if yes else .5 for yes in written]
    expected_agreement = .5 if sum(written) == 1 else 1.
    return {"condition": condition, "event": event, "joint_axes": ["B", "F1", "F2"],
            "joint_probabilities_given_event": joint.tolist(), "errors": errors,
            "agreement": agreement, "analytic_errors": expected_errors,
            "analytic_agreement": expected_agreement,
            "analytic_max_error": max([abs(a-b) for a, b in zip(errors, expected_errors)]+
                                      [abs(agreement-expected_agreement)])}


def case(condition, name, rho, model):
    jmap = model["J"]
    omega = jmap @ rho @ jmap.conj().T
    events = []
    for j in EVENTS:
        state = conditioned_operator(omega, j)
        e = model["V"][j][:, [0, 8]]
        readouts = []
        for readout in B["READOUTS"]:
            branches = [(outcome, k @ omega @ k.conj().T)
                        for outcome, k in joint_instrument_kraus(j, readout)]
            conditional_post = 4*sum((x for _, x in branches), np.zeros((16, 16), complex))
            written_read = condition != "no_record" and any(k <= j for k in readout)
            amplitude = float(abs(rho[0, 1])) if written_read else 0.
            expected = {"S": 0., "Q": 0. if condition == "records_E_on" and j == 3 else amplitude,
                        "G": amplitude}
            measured = {scope: B["distance"](B["marginal"](state, keep),
                        B["marginal"](conditional_post, keep)) for scope, keep in B["SCOPES"].items()}
            direct = dict(B["instrument"](state, readout))
            readouts.append({"readout": list(readout),
                "branches": [{"outcome": list(outcome),
                    "joint_probability_event_outcome": float(np.trace(branch).real),
                    "probability_given_event": 4*float(np.trace(branch).real),
                    "conditional_branch_vs_circuit_residual_fro": float(np.linalg.norm(4*branch-direct[outcome]))}
                    for outcome, branch in branches],
                "disturbance": measured, "analytic_disturbance": expected,
                "analytic_max_error": max(abs(measured[s]-expected[s]) for s in measured)})
        events.append({"event": j, "probability": float(np.trace(event_block(omega, j)).real),
            "conditional_state": B["sparse_state"](state),
            "state_diagnostics": B["state_diagnostics"](state),
            "conditional_vs_circuit_residual_fro": float(np.linalg.norm(state-e @ rho @ e.conj().T)),
            "readouts": readouts})
    # Same diagonal slices alone do not imply a coherent constraint history.
    dephased = np.zeros_like(omega)
    for j in EVENTS:
        dephased[16*j:16*(j+1), 16*j:16*(j+1)] = event_block(omega, j)
    return {"condition": condition, "input": name, "history_state": B["sparse_state"](omega),
        "history_diagnostics": B["state_diagnostics"](omega),
        "history_constraint_residual_fro": float(np.linalg.norm(model["H_ready"] @ omega)),
        "event_dephased_propagation_energy": float(np.trace(model["H_prop"] @ dephased).real),
        "events": events}


def model_diagnostics(condition, model):
    jmap, w = model["J"], model["W"]
    ep = np.linalg.eigvalsh(model["H_prop"])
    er = np.linalg.eigvalsh(model["H_ready"])
    kraus = [k for j in EVENTS for _, k in joint_instrument_kraus(j, (1, 2))]
    return {"condition": condition, "history_dimension": 64,
        "propagation_kernel_dimension": int(sum(abs(ep) < ATOL)),
        "ready_kernel_dimension": int(sum(abs(er) < ATOL)),
        "propagation_spectrum": ep.tolist(), "ready_spectrum": er.tolist(),
        "J_isometry_residual_fro": float(np.linalg.norm(jmap.conj().T @ jmap-np.eye(2))),
        "W_isometry_residual_fro": float(np.linalg.norm(w.conj().T @ w-np.eye(16))),
        "propagation_residual_fro": float(np.linalg.norm(model["P"] @ w)),
        "ready_boundary_residual_fro": float(np.linalg.norm(model["boundary"] @ jmap)),
        "H_ready_J_residual_fro": float(np.linalg.norm(model["H_ready"] @ jmap)),
        "terminal_encoding_residual_fro": float(np.linalg.norm(2*jmap[48:, :]-B["encoding"](condition))),
        "joint_event_readout_tp_residual_fro": float(np.linalg.norm(sum(k.conj().T @ k for k in kraus)-np.eye(64)))}


def run_experiment():
    models = {c: construction(c) for c in B["CONDITIONS"]}
    diagnostics = [model_diagnostics(c, models[c]) for c in models]
    cases = [case(c, name, rho, models[c]) for c in models for name, rho in B["inputs"]().items()]
    calibrations = [calibration(c, j) for c in models for j in EVENTS]
    paths = ("experiments/r2_shared_records.py", "experiments/r2d_global_history.py",
             "tests/test_r2d_global_history.py")
    return {"specification": "R2 plan: open four-event baseline history; r2a-v1 section 8",
        "interpretation": "known-result reproduction and finite-model connection",
        "provenance": {"baseline_commit": BASELINE, "python": platform.python_version(),
            "numpy": np.__version__, "source_sha256": {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}},
        "absolute_tolerance": ATOL, "relative_tolerance": 0,
        "factor_order": ["event (dimension 4)", "S", "F1", "F2", "E"],
        "boundary": "open edges 0->1, 1->2, 2->3; ready ancillas at event 0; no final return",
        "models": diagnostics, "calibrations": calibrations, "cases": cases,
        "summary": {"condition_count": 3, "history_case_count": len(cases),
            "conditional_state_count": sum(len(x["events"]) for x in cases),
            "readout_comparison_count": sum(len(e["readouts"]) for x in cases for e in x["events"]),
            "calibration_count": len(calibrations),
            "max_calibration_analytic_error": max(x["analytic_max_error"] for x in calibrations),
            "max_disturbance_analytic_error": max(r["analytic_max_error"] for x in cases for e in x["events"] for r in e["readouts"])},
        "limits": ["Event conditioning is a representation map, not a physically licensed clock device",
            "Only the closed baseline circuit is embedded; noise/readout dilations are not constructed",
            "Same diagonal event states do not suffice for propagation constraints",
            "No decoherent-histories theorem, thermodynamic arrow, or ontological conclusion",
            "R2 synthesis only; original pilot_gate blocked and Stage 17 unstarted"]}


if __name__ == "__main__":
    report = run_experiment()
    (ROOT/"results/r2d_global_history.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False)+"\n", encoding="utf-8")
    print(json.dumps(report["summary"], indent=2))
