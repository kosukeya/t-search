"""R2c: one-shot record noise and pre-readout unknown-state recovery.

Uses the frozen R2b model unchanged. These are separate experiments: recovery
starts before noise/readout. No numerical optimization of recovery is claimed.
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
PROBABILITIES = (0., .1, .25, .5)
SCOPES = ("Q", "G")
BASELINE = "3580f00ebea83c06b8a66562e4a21224e7424eaf"


def apply_kraus(operator, kraus):
    """Linear action on any operator; all branches are summed without repair."""
    size = kraus[0].shape[0]
    return sum((k @ operator @ k.conj().T for k in kraus), np.zeros((size, size), complex))


def tp_residual(kraus):
    size = kraus[0].shape[1]
    return float(np.linalg.norm(sum(k.conj().T @ k for k in kraus)-np.eye(size)))


def noise_kraus(p):
    if not np.isfinite(p) or p < 0 or p > 1:
        raise ValueError("Noise probability must lie in [0,1]")
    ident = np.eye(2)
    flip = np.array([[0, 1], [1, 0]])
    return [np.sqrt((p if i else 1-p)*(p if j else 1-p))*
            np.kron(np.kron(np.kron(ident, flip if i else ident), flip if j else ident), ident)
            for i, j in itertools.product((0, 1), repeat=2)]


def retention(condition, p):
    kraus = noise_kraus(p)
    joint = np.zeros((2, 2, 2))
    states = []
    for b in (0, 1):
        before = B["encode"](np.diag([1-b, b]), condition)
        after = apply_kraus(before, kraus)
        states.append({"input_label": b, "after_noise": B["sparse_state"](after),
                       "state_diagnostics": B["state_diagnostics"](after)})
        for (x, y), branch in B["instrument"](after, (1, 2)):
            joint[b, x, y] = float(np.trace(branch).real)/2
    errors = [float(sum(joint[b, x, y] for b, x, y in itertools.product((0, 1), repeat=3)
                        if (x, y)[k] != b)) for k in (0, 1)]
    agreement = float(sum(joint[b, x, x] for b, x in itertools.product((0, 1), repeat=2)))
    both_correct = float(sum(joint[b, b, b] for b in (0, 1)))
    a = (1-p)**2+p**2
    expected = {"errors": [.5, .5] if condition == "no_record" else [p, p],
                "agreement": a, "both_correct": a/2 if condition == "no_record" else (1-p)**2}
    deviations = [abs(errors[k]-expected["errors"][k]) for k in (0, 1)]
    deviations += [abs(agreement-expected["agreement"]), abs(both_correct-expected["both_correct"])]
    return {"condition": condition, "p": p, "joint_axes": ["B", "F1", "F2"],
            "joint_probabilities": joint.tolist(), "errors": errors, "agreement": agreement,
            "both_correct": both_correct, "analytic": expected,
            "analytic_max_error": max(deviations), "normalization_error": float(abs(joint.sum()-1)),
            "noise_tp_residual_fro": tp_residual(kraus), "states": states}


def encoding_kraus(condition, scope):
    """Channel S -> accessible X; Q traces E, G retains E."""
    if scope not in SCOPES:
        raise ValueError("Scope must be Q or G")
    v = B["encoding"](condition)
    if scope == "G":
        return [v]
    # V axes are [SF1F2, E, input S]. No selection of E's outcome.
    return [v.reshape(8, 2, 2)[:, e, :] for e in (0, 1)]


def decoder_unitary(condition, scope):
    if scope not in SCOPES or condition not in B["CONDITIONS"]:
        raise ValueError("Unknown condition or scope")
    if scope == "G":
        return B["circuit"](condition).conj().T
    if condition == "no_record":
        return np.eye(8, dtype=complex)
    # C1/C2 do not act on E; this E=0 restriction represents the same Q unitary,
    # not a postselection of the E-on encoded state (E was already traced out).
    indices = np.arange(0, 16, 2)
    return B["circuit"]("records_E_off").conj().T[np.ix_(indices, indices)]


def decoder_kraus(condition, scope):
    """Apply declared inverse on X then trace all output record registers."""
    u = decoder_unitary(condition, scope)
    dimension = u.shape[0]
    return [u.reshape(2, dimension//2, dimension)[:, a, :] for a in range(dimension//2)]


def composite_kraus(condition, scope):
    return [r @ n for r in decoder_kraus(condition, scope) for n in encoding_kraus(condition, scope)]


def bell_state():
    phi = np.array([1, 0, 0, 1], dtype=complex)/np.sqrt(2)
    return np.outer(phi, phi.conj())


def reference_output(kraus):
    """R is never acted on; the input is the normalized Bell reference state."""
    return apply_kraus(bell_state(), [np.kron(np.eye(2), k) for k in kraus])


def recovery(condition, scope):
    enc = encoding_kraus(condition, scope)
    dec = decoder_kraus(condition, scope)
    comp = composite_kraus(condition, scope)
    accessible = reference_output(enc)
    recovered = apply_kraus(accessible, [np.kron(np.eye(2), k) for k in dec])
    choi = reference_output(comp)
    fidelity = float(np.trace(bell_state() @ recovered).real)  # squared convention
    dephases = condition == "records_E_on" and scope == "Q"
    upper = .5 if dephases else 1.
    plus = B["inputs"]()["plus"]
    minus = np.array([[.5, -.5], [-.5, .5]], complex)
    phase_collision = B["distance"](apply_kraus(plus, enc), apply_kraus(minus, enc))
    return {"condition": condition, "scope": scope,
        "access_factors": ["S", "F1", "F2"]+(["E"] if scope == "G" else []),
        "start": "encoded state before any record noise or readout",
        "reference_factors": ["R", "S_prime"],
        "accessible_reference_state": B["sparse_state"](accessible),
        "recovered_reference_state": B["sparse_state"](recovered),
        "achieved_entanglement_fidelity": fidelity,
        "analytic_upper_bound": upper, "upper_bound_gap": upper-fidelity,
        "upper_bound_reason": "R2a section 8: cq reference state implies Fe <= 1/2" if dephases else
            "Fe <= 1 for density states; the declared inverse attains it",
        "channel_type": "Z_dephasing" if dephases else "identity",
        "encoding_tp_residual_fro": tp_residual(enc),
        "decoder_tp_residual_fro": tp_residual(dec),
        "composite_tp_residual_fro": tp_residual(comp),
        "decoder_unitarity_residual_fro": float(np.linalg.norm(
            decoder_unitary(condition, scope).conj().T @ decoder_unitary(condition, scope)-
            np.eye(decoder_unitary(condition, scope).shape[0]))),
        "two_step_vs_composite_residual_fro": float(np.linalg.norm(recovered-choi)),
        "reference_marginal_residual_fro": float(np.linalg.norm(B["marginal"](recovered, (0,))-np.eye(2)/2)),
        "accessible_state_diagnostics": B["state_diagnostics"](accessible),
        "recovered_state_diagnostics": B["state_diagnostics"](recovered),
        "composite_choi_state_diagnostics": B["state_diagnostics"](choi),
        "phase_pair_input_distance": B["distance"](plus, minus),
        "phase_pair_accessible_distance": phase_collision}


def run_experiment():
    retained = [retention(c, p) for c in B["CONDITIONS"] for p in PROBABILITIES]
    recovered = [recovery(c, x) for c in B["CONDITIONS"] for x in SCOPES]
    paths = ("experiments/r2_shared_records.py", "experiments/r2c_retention_recovery.py",
             "tests/test_r2c_retention_recovery.py")
    return {"specification": "r2a-v1 section 8", "interpretation": "known-result reproduction",
        "absolute_tolerance": ATOL, "relative_tolerance": 0,
        "provenance": {"baseline_commit": BASELINE, "python": platform.python_version(),
            "numpy": np.__version__, "source_sha256": {
                p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}},
        "factor_order_retention": ["S", "F1", "F2", "E"],
        "factor_order_reference_encoding": ["R", "S", "F1", "F2", "E"],
        "noise": "Independent bit flips on F1 and F2, once before Z readout",
        "recovery": "Deterministic CPTP decoder; no noise, readout, postselection or input description",
        "cp_basis": "Explicit Kraus operators, isometric encoding, unitary decoder and partial trace",
        "retention_cases": retained, "recovery_cases": recovered,
        "summary": {"retention_case_count": len(retained), "recovery_case_count": len(recovered),
            "max_retention_analytic_error": max(r["analytic_max_error"] for r in retained),
            "max_recovery_bound_gap_absolute": max(abs(r["upper_bound_gap"]) for r in recovered)},
        "limits": ["One-shot noise is not a lifetime or a thermodynamic arrow",
            "Q and G are different resource classes, not equivalent internal observers",
            "Q includes S and both records; recovery is not an Fi-only readout",
            "No global-history extension or ontological actualization claim",
            "R2d unstarted; original pilot_gate remains blocked"]}


if __name__ == "__main__":
    report = run_experiment()
    (ROOT/"results/r2c_retention_recovery.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False)+"\n")
    print(json.dumps(report["summary"], indent=2))
