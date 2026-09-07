"""R3b: 7 fixed channels, 28 settings; data-only bounds vs reference truth."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import platform
import runpy
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
C = runpy.run_path(str(ROOT/"experiments/r2c_retention_recovery.py"))
B = C["B"]
CERT = runpy.run_path(str(ROOT/"src/t_search/r3_certificate.py"))
certify = CERT["certify"]
ATOL = 1e-10
BASELINE = "2c6cd594f46dbb657bb2e2bd5c3aae3122d65782"
ASSUMPTIONS = {k: True for k in CERT["ASSUMPTION_KEYS"]}
CASE_IDS = (*B["CONDITIONS"], "phase_flip", "replace_plus", "pauli_A", "pauli_B")


def probes():
    return {"z0": np.array([1, 0], complex), "z1": np.array([0, 1], complex),
            "x_plus": np.array([1, 1], complex)/np.sqrt(2),
            "x_minus": np.array([1, -1], complex)/np.sqrt(2)}


def channel(case_id):
    if case_id in B["CONDITIONS"]:
        return C["composite_kraus"](case_id, "Q")
    ident = np.eye(2, dtype=complex)
    x = np.array([[0, 1], [1, 0]], complex)
    y = np.array([[0, -1j], [1j, 0]], complex)
    z = np.diag([1., -1.]).astype(complex)
    if case_id == "phase_flip":
        return [z]
    if case_id == "replace_plus":
        return [np.outer(probes()["x_plus"], b) for b in ident]
    weights = {"pauli_A": (.5, .25, 0., .25), "pauli_B": (.75, 0., .25, 0.)}
    if case_id not in weights:
        raise ValueError("Unknown fixed case")
    return [np.sqrt(p)*k for p, k in zip(weights[case_id], (ident, x, y, z))]


def measure(kraus):
    """Keep both outcomes and every Kraus branch, including zero weights."""
    vectors = probes()
    correct, settings = {}, []
    for name, vector in vectors.items():
        basis = ("z0", "z1") if name.startswith("z") else ("x_plus", "x_minus")
        branches = [[float(abs(np.vdot(vectors[out], k @ vector))**2) for out in basis]
                    for k in kraus]
        totals = [sum(row[j] for row in branches) for j in (0, 1)]
        correct[name] = totals[basis.index(name)]
        state = C["apply_kraus"](np.outer(vector, vector.conj()), kraus)
        settings.append({"input": name, "outcome_labels": list(basis),
            "outcome_probabilities": totals, "kraus_branch_probabilities": branches,
            "normalization_error": abs(sum(totals)-1),
            "output_state": B["sparse_state"](state),
            "output_diagnostics": B["state_diagnostics"](state)})
    return correct, settings


def reference_truth(kraus):
    """Independent input: channel only, never a certificate or measured data."""
    choi = C["reference_output"](kraus)
    fidelity = float(np.trace(C["bell_state"]() @ choi).real)
    return {"entanglement_fidelity": fidelity, "reference_output": B["sparse_state"](choi),
            "state_diagnostics": B["state_diagnostics"](choi),
            "tp_residual_fro": C["tp_residual"](kraus),
            "reference_marginal_residual_fro": float(np.linalg.norm(B["marginal"](choi, (0,))-np.eye(2)/2))}


def analytic(case_id):
    values = {"no_record": (1, 1, 1, 1, 1), "records_E_off": (1, 1, 1, 1, 1),
        "records_E_on": (1, .5, .5, .5, .5), "phase_flip": (1, 0, 0, 0, 0),
        "replace_plus": (.5, .5, 0, .5, .25),
        "pauli_A": (.75, .75, .5, .75, .5), "pauli_B": (.75, .75, .5, .75, .75)}
    return dict(zip(("F_Z", "F_X", "lower_bound", "upper_bound", "entanglement_fidelity"), values[case_id]))


def run_experiment():
    rows = []
    for case_id in CASE_IDS:
        kraus = channel(case_id)  # built once per condition, not per probe
        probabilities, settings = measure(kraus)
        # Only the four probabilities and the declared assumptions cross this boundary.
        certificate_input = {"probabilities": probabilities, "assumptions": dict(ASSUMPTIONS)}
        certificate = certify(**certificate_input)
        truth = reference_truth(kraus)
        expected = analytic(case_id)  # not available to the certifier
        error = max(abs((truth if k == "entanglement_fidelity" else certificate)[k]-v)
                    for k, v in expected.items())
        violation = max(0., certificate["lower_bound"]-truth["entanglement_fidelity"],
                        truth["entanglement_fidelity"]-certificate["upper_bound"])
        rows.append({"case_id": case_id,
            "kind": "R2 Q-access recovery" if case_id in B["CONDITIONS"] else "logical-channel control",
            "certificate_input": certificate_input, "certificate": certificate,
            "measurements": settings, "reference_truth": truth, "analytic": expected,
            "analytic_max_error": error, "interval_violation": violation})
    paths = ("src/t_search/r3_certificate.py", "experiments/r3b_recovery_certificate.py",
             "tests/test_r3b_recovery_certificate.py", "experiments/r2_shared_records.py",
             "experiments/r2c_retention_recovery.py")
    return {"specification": "r3a-v1", "interpretation": "known-bound reproduction",
        "provenance": {"baseline_commit": BASELINE, "python": platform.python_version(),
            "numpy": np.__version__, "source_sha256": {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}},
        "absolute_tolerance": ATOL, "relative_tolerance": 0,
        "cp_basis": "Explicit Kraus channels; baseline reuses R2c encoding, Q restriction and decoder",
        "cases": rows, "summary": {"case_count": len(rows), "setting_count": sum(len(r["measurements"]) for r in rows),
            "max_analytic_error": max(r["analytic_max_error"] for r in rows),
            "max_interval_violation": max(r["interval_violation"] for r in rows),
            "certified_case_count": sum(r["certificate"]["non_measure_prepare_certified"] for r in rows)},
        "limits": ["Declared trusted preparation/measurement, dimensions, common CPTP process and wiring",
            "Born probabilities, not finite-sample confidence bounds or SPAM-corrected data",
            "Numerical margin withholds borderline claims; it is not statistical confidence",
            "Implemented-channel bound, not optimal recovery, a unique gate, or quantum capacity",
            "No alternative decoder implementation, GST, noise sweep or clock-device construction",
            "Original pilot_gate blocked; Stage 17 remains unstarted; no further experiment selected"]}


if __name__ == "__main__":
    result = run_experiment()
    (ROOT/"results/r3b_recovery_certificate.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False)+"\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2))
