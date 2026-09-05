"""Bounded R1 audit of existing Stage 7 maps; not a timed-intervention pilot.

Run from the repository root: python experiments/r1_intervention_preflight.py
Requires the repository's installed dependencies. JSON goes to stdout.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from t_search.stage7_history import (
    canonical_physical_history_state,
    history_constraint_operator,
    history_physical_basis,
    history_reduction_coordinates,
)
from t_search.stage7_record_transport import (
    history_clock_reduction_coordinates,
    history_support_metric,
    physical_memory_projector,
)

ATOL = 1e-10
BASELINE = "af0ff7adab6a2751849239e0fbd464c678406218"


def norm(a: np.ndarray) -> float:
    return float(np.linalg.norm(a))


def audit() -> dict:
    eye = np.eye(14)
    i2 = np.eye(2)
    x = np.array([[0, 1], [1, 0]])
    y = np.array([[0, -1j], [1j, 0]])
    z = np.diag([1, -1])
    raw = {"I": i2, "X": x, "Y": y, "Z": z,
           "P0": (i2 + z) / 2, "P1": (i2 - z) / 2}
    leakage = {}
    for kind in ("forward", "no-record"):
        j = history_physical_basis(kind)
        p = j @ j.conj().T
        assert norm(j.conj().T @ j - eye) < ATOL
        assert norm(history_constraint_operator(kind) @ j) < ATOL
        leakage[kind] = {
            name: float(np.linalg.norm((np.eye(54) - p) @
                        np.kron(np.eye(27), k) @ j, 2))
            for name, k in raw.items()
        }
    assert leakage["forward"]["P0"] > 0.4
    assert leakage["forward"]["P1"] > 0.4
    assert leakage["forward"]["X"] < ATOL
    assert max(leakage["no-record"].values()) < ATOL

    j = history_physical_basis("forward")
    v = j.conj().T @ canonical_physical_history_state()
    rho = np.outer(v, v.conj())
    compressed = [j.conj().T @ np.kron(np.eye(27), raw[f"P{m}"]) @ j
                  for m in (0, 1)]
    deficit = eye - sum(k.conj().T @ k for k in compressed)
    survival = float(np.trace((eye - deficit) @ rho).real)
    assert np.linalg.eigvalsh(deficit).min() > -ATOL
    assert survival < 1 - ATOL  # Projection is postselection, not a TP repair.
    assert abs(survival - 7 / 9) < ATOL
    assert abs(np.linalg.eigvalsh(deficit).max() - 4 / 9) < ATOL

    ks = [physical_memory_projector(m) for m in (0, 1)]
    completeness = norm(sum(k.conj().T @ k for k in ks) - eye)
    assert completeness < ATOL
    for k in ks:
        assert norm(k - k.conj().T) < ATOL
        assert norm(k @ k - k) < ATOL
    sigma = sum(k @ rho @ k.conj().T for k in ks)
    r0 = history_reduction_coordinates("forward", 0)
    assert norm(r0.conj().T @ r0 - eye) < ATOL
    before_delta = r0 @ (sigma - rho) @ r0.conj().T
    before_distance = float(np.abs(np.linalg.eigvalsh(before_delta)).sum() / 2)
    assert abs(before_distance - 0.5) < ATOL

    charts = []
    max_branch_residual = 0.0
    for clock in ("A", "C"):
        for event in (0, 1, 2):
            r = history_clock_reduction_coordinates("forward", clock, event)
            ri = np.linalg.inv(r)
            g = history_support_metric("forward", clock, event)
            transported = [r @ k @ ri for k in ks]
            metric_error = norm(r.conj().T @ g @ r - eye)
            tp_error = norm(sum(k.conj().T @ g @ k for k in transported) - g)
            # All 196 matrix units span the input operator space: a linear
            # covariance check, not a sample-based proof of physical locality.
            for a in range(14):
                for b in range(14):
                    e = np.zeros((14, 14), dtype=complex)
                    e[a, b] = 1
                    d = r @ e @ r.conj().T
                    for k, kt in zip(ks, transported):
                        err = norm(kt @ d @ kt.conj().T -
                                   r @ k @ e @ k.conj().T @ r.conj().T)
                        max_branch_residual = max(max_branch_residual, err)
            d = r @ rho @ r.conj().T
            probabilities = [float(np.trace(g @ kt @ d @ kt.conj().T).real)
                             for kt in transported]
            assert metric_error < ATOL and tp_error < ATOL
            assert max(abs(p - 0.5) for p in probabilities) < ATOL
            charts.append({"clock": clock, "reading": event,
                           "metric_residual": metric_error,
                           "metric_tp_residual": tp_error,
                           "reduction_min_singular_value": float(np.linalg.svd(r, compute_uv=False).min()),
                           "branch_probabilities": probabilities})
    assert max_branch_residual < ATOL
    # Restrict provenance to modules this audit actually uses, not the whole repo.
    used = ["stage3", "stage3_asymmetry", "stage3_diagnostics", "stage5_clock_change",
            "stage5_clock_transforms", "stage5_reductions", "stage7_spectator",
            "stage7_record", "stage7_history", "stage7_record_transport"]
    hashes = {f"src/t_search/{name}.py": hashlib.sha256(
        (ROOT / f"src/t_search/{name}.py").read_bytes()).hexdigest() for name in used}
    return {"baseline_commit": BASELINE, "numpy_version": np.__version__,
            "atol": ATOL, "audit_kind": "fixed_constraint_feasibility",
            "pilot_gate": "blocked", "new_scientific_claim": False,
            "dimensions": {"kinematic": 54, "physical": 14},
            "bare_memory_operator_leakage_spectral_norm": leakage,
            "compressed_readout": {"canonical_survival_probability": survival,
                "max_failure_probability": float(np.linalg.eigvalsh(deficit).max())},
            "lifted_readout": {"tp_residual": completeness,
                "nonselective_earlier_full_state_trace_distance": before_distance,
                "max_matrix_unit_covariance_residual": max_branch_residual},
            "charts": charts, "source_sha256": hashes}


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, ensure_ascii=False, allow_nan=False))
