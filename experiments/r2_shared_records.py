"""R2b fixed-basis shared records (r2a-v1). Run this script with Python/NumPy."""
from __future__ import annotations
import hashlib
import itertools
import json
from pathlib import Path
import platform
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
ATOL = 1e-10
CONDITIONS = ("no_record", "records_E_off", "records_E_on")
READOUTS = ((1,), (2,), (1, 2))
SCOPES = {"S": (0,), "Q": (0, 1, 2), "G": (0, 1, 2, 3)}
BASELINE = "e1d71795eb18385b24753d3b0e4eb207be35679e"


def state_diagnostics(rho):
    return {"trace_error": float(abs(np.trace(rho)-1)),
            "hermitian_residual_fro": float(np.linalg.norm(rho-rho.conj().T)),
            "minimum_eigenvalue": float(np.linalg.eigvalsh(rho).min())}


def validate_state(rho, dimension):
    rho = np.asarray(rho, dtype=complex)
    if rho.shape != (dimension, dimension) or not np.isfinite(rho).all():
        raise ValueError("Invalid density matrix shape or entries")
    d = state_diagnostics(rho)
    if (d["trace_error"] > ATOL or d["hermitian_residual_fro"] > ATOL
            or d["minimum_eigenvalue"] < -ATOL):
        raise ValueError("Input must be Hermitian, positive, and trace one")
    return rho


def inputs():
    def pure(v):
        v = np.asarray(v, dtype=complex)
        return np.outer(v, v.conj())
    return {"zero": pure([1, 0]), "one": pure([0, 1]),
            "plus": pure(np.array([1, 1])/np.sqrt(2)),
            "plus_i": pure(np.array([1, 1j])/np.sqrt(2)),
            "maximally_mixed": np.eye(2)/2,
            "asymmetric_mixed": np.array([[1/3, (1+1j)/6], [(1-1j)/6, 2/3]])}


def cnot(target):
    """S is most significant; targets 1,2,3 are F1,F2,E."""
    if target not in (1, 2, 3):
        raise ValueError("Target must be F1, F2, or E")
    u = np.zeros((16, 16), complex)
    for col in range(16):
        row = col ^ (1 << (3-target)) if col & 8 else col
        u[row, col] = 1
    return u


def circuit(condition):
    if condition not in CONDITIONS:
        raise ValueError("Unknown condition")
    u = np.eye(16, dtype=complex)
    if condition != "no_record":
        u = cnot(2) @ cnot(1)
    if condition == "records_E_on":
        u = cnot(3) @ u
    return u


def encoding(condition):
    return circuit(condition)[:, [0, 8]]  # ancillas prepared as 000


def encode(rho, condition):
    rho = validate_state(rho, 2)
    v = encoding(condition)
    return v @ rho @ v.conj().T


def marginal(matrix, keep):
    """Partial trace in original qubit order; also accepts general operators."""
    n = matrix.shape[0].bit_length()-1
    if matrix.shape != (2**n, 2**n):
        raise ValueError("Expected square qubit operator")
    keep = tuple(keep)
    if tuple(sorted(set(keep))) != keep or any(k < 0 or k >= n for k in keep):
        raise ValueError("Keep indices must be unique, ordered, and in range")
    tensor = matrix.reshape((2,)*(2*n))
    active = n
    for k in reversed(range(n)):
        if k not in keep:
            tensor = np.trace(tensor, axis1=k, axis2=k+active)
            active -= 1
    return tensor.reshape(2**len(keep), 2**len(keep))


def readout_kraus(readout):
    if tuple(readout) not in READOUTS:
        raise ValueError("Readout must be F1, F2, or F1+F2")
    return [(outcome, np.diag([
        all(((i >> (3-k)) & 1) == b for k, b in zip(readout, outcome))
        for i in range(16)]).astype(complex))
        for outcome in itertools.product((0, 1), repeat=len(readout))]


def instrument(rho, readout):
    """Retain unnormalized branches for every outcome, including zero."""
    return [(outcome, p @ rho @ p.conj().T) for outcome, p in readout_kraus(readout)]


def nonselective(rho, readout):
    return sum((b for _, b in instrument(rho, readout)), np.zeros_like(rho))


def distance(left, right):
    return float(np.linalg.svd(left-right, compute_uv=False).sum()/2)


def sparse_state(rho):
    """Only exact zeros omitted: no threshold, clipping, or normalization."""
    rows, cols = np.nonzero(rho)
    return {"dimension": rho.shape[0], "entries":
        [[int(i), int(j), float(rho[i, j].real), float(rho[i, j].imag)]
         for i, j in zip(rows, cols)]}


def fixed_z_sbs(rho):
    """S-Z structure: all other qubits are fragments (Q: F1,F2; G: F1,F2,E).

    One-positive-branch satisfaction is vacuous, not an information certificate.
    This is not a search over bases or a distance to the nearest SBS.
    """
    n = rho.shape[0].bit_length()-1
    d = 2**(n-1)
    diagonal = np.zeros_like(rho)
    conditional, factor_errors, weights = [], [], []
    for b in (0, 1):
        block = rho[b*d:(b+1)*d, b*d:(b+1)*d]
        diagonal[b*d:(b+1)*d, b*d:(b+1)*d] = block
        weight = float(np.trace(block).real)
        if weight < 0:
            raise ValueError("Negative branch weight; no clipping permitted")
        weights.append(weight)
        if weight == 0:
            conditional.append(None)
            factor_errors.append(None)
            continue
        state = block/weight
        factors = [marginal(state, (k,)) for k in range(n-1)]
        product = np.ones((1, 1), complex)
        for factor in factors:
            product = np.kron(product, factor)
        conditional.append(factors)
        factor_errors.append(float(np.linalg.norm(state-product)))
    overlaps = None
    if all(x is not None for x in conditional):
        overlaps = [float(np.linalg.norm(x @ y)) for x, y in zip(*conditional)]
    off_diagonal = float(np.linalg.norm(rho-diagonal))
    residuals = [off_diagonal]+[e for e in factor_errors if e is not None]+(overlaps or [])
    return {"basis": "Z_S", "fragment_count": n-1, "branch_weights": weights,
        "off_block_residual_fro": off_diagonal,
        "conditional_product_residuals_fro": factor_errors,
        "support_product_residuals_fro": overlaps,
        "support_check_note": "two positive branches" if overlaps is not None else
            "vacuous: one positive branch; not a device-information certificate",
        "fixed_z_structure_satisfied": all(e <= ATOL for e in residuals)}


def calibration(condition):
    joint = np.zeros((2, 2, 2))
    for b in (0, 1):
        for (x, y), branch in instrument(encode(np.diag([1-b, b]), condition), (1, 2)):
            joint[b, x, y] = float(np.trace(branch).real)/2
    errors = [sum(joint[b, x, y] for b, x, y in itertools.product((0, 1), repeat=3)
                  if (x, y)[k] != b) for k in (0, 1)]
    agreement = sum(joint[b, x, x] for b, x in itertools.product((0, 1), repeat=2))
    expected = .5 if condition == "no_record" else 0.
    return {"joint_axes": ["B", "F1", "F2"], "joint_probabilities": joint.tolist(),
        "errors": [float(x) for x in errors], "agreement": float(agreement),
        "both_correct": float(sum(joint[b, b, b] for b in (0, 1))),
        "analytic_max_error": float(max(abs(x-expected) for x in errors)),
        "normalization_error": float(abs(joint.sum()-1))}


def run_experiment():
    cases, validations = [], []
    max_error = 0.
    for condition in CONDITIONS:
        u, v = circuit(condition), encoding(condition)
        validations.append({"condition": condition,
            "unitarity_residual_fro": float(np.linalg.norm(u.conj().T @ u-np.eye(16))),
            "isometry_residual_fro": float(np.linalg.norm(v.conj().T @ v-np.eye(2)))})
        for name, rho in inputs().items():
            omega = encode(rho, condition)
            before = {s: marginal(omega, k) for s, k in SCOPES.items()}
            readouts = []
            for readout in READOUTS:
                branches = instrument(omega, readout)
                post = sum((b for _, b in branches), np.zeros_like(omega))
                branch_reports = []
                recomposed = np.zeros_like(omega)
                for outcome, branch in branches:
                    probability = float(np.trace(branch).real)
                    if probability < 0:
                        raise ValueError("Negative branch probability")
                    conditional = None if probability == 0 else branch/probability
                    if conditional is not None:
                        recomposed += probability*conditional
                    branch_reports.append({"outcome": list(outcome), "probability": probability,
                        "conditional_state": None if conditional is None else sparse_state(conditional),
                        "undefined_reason": "zero probability" if conditional is None else None,
                        "state_diagnostics": None if conditional is None else state_diagnostics(conditional)})
                disturbances = {}
                for scope, keep in SCOPES.items():
                    measured = distance(before[scope], marginal(post, keep))
                    expected = 0. if (condition == "no_record" or scope == "S" or
                        (condition == "records_E_on" and scope == "Q")) else float(abs(rho[0, 1]))
                    error = abs(measured-expected)
                    max_error = max(max_error, error)
                    disturbances[scope] = {"trace_distance": measured, "analytic": expected,
                                          "absolute_error": error}
                readouts.append({"fragments": list(readout), "branches": branch_reports,
                    "disturbance": disturbances, "nonselective_state": sparse_state(post),
                    "post_state_diagnostics": state_diagnostics(post),
                    "probability_sum_error": abs(sum(b["probability"] for b in branch_reports)-1),
                    "recomposition_residual_fro": float(np.linalg.norm(recomposed-post)),
                    "repeat_nonselective_residual_fro": float(np.linalg.norm(nonselective(post, readout)-post))})
            cases.append({"condition": condition, "input": name, "input_state": sparse_state(rho),
                "before_state_diagnostics": {s: state_diagnostics(x) for s, x in before.items()},
                "before_states": {s: sparse_state(x) for s, x in before.items()},
                "fixed_z_sbs": {s: fixed_z_sbs(before[s]) for s in ("Q", "G")},
                "readout_order_residual_fro": float(np.linalg.norm(
                    nonselective(nonselective(omega, (1,)), (2,))-
                    nonselective(nonselective(omega, (2,)), (1,)))), "readouts": readouts})
    apparatus = []
    for readout in READOUTS:
        ops = [p for _, p in readout_kraus(readout)]
        apparatus.append({"fragments": list(readout),
            "tp_completeness_residual_fro": float(np.linalg.norm(sum(p.conj().T @ p for p in ops)-np.eye(16))),
            "projector_residual_fro": float(max(np.linalg.norm(p @ p-p) for p in ops)),
            "branch_effect_complement_minimum_eigenvalue": float(min(
                np.linalg.eigvalsh(np.eye(16)-p.conj().T @ p).min() for p in ops))})
    sources = ("experiments/r2_shared_records.py", "tests/test_r2_shared_records.py")
    return {"specification": "r2a-v1", "interpretation": "known-result reproduction",
        "factor_order": ["S", "F1", "F2", "E"], "absolute_tolerance": ATOL,
        "relative_tolerance": 0, "provenance": {"baseline_commit": BASELINE,
            "python": platform.python_version(), "numpy": np.__version__,
            "source_sha256": {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sources}},
        "cp_basis": "Explicit Kraus maps; isometric encoding; partial traces.",
        "conditioning_policy": "All outcomes retained; exactly zero probability gives null state.",
        "encoding_validation": validations, "instrument_validation": apparatus,
        "calibration": {c: calibration(c) for c in CONDITIONS}, "cases": cases,
        "summary": {"case_count": len(cases), "readout_comparisons": len(cases)*len(READOUTS),
                    "maximum_disturbance_analytic_error": max_error},
        "limits": ["Fixed Z basis, preparation and gate order",
            "Joint-state diagnostics are not accessible through Fi-only readout",
            "R2c noise/recovery and R2d history experiments unstarted",
            "No ontological actualization claim; original pilot_gate remains blocked"]}


if __name__ == "__main__":
    report = run_experiment()
    path = ROOT/"results/r2_shared_records.json"
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False, allow_nan=False)+"\n")
    print(json.dumps(report["summary"], indent=2))
