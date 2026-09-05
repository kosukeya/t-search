"""Separate one-shot record formation from cyclic return in the R1b carrier.

Keep R1b unchanged. Build the two-edge constraint directly, compare kernels
with the cyclic controls, and verify fixed-experiment statistics. This is a
boundary supplement for conceptual synthesis, not an RQ2 novelty pilot.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import runpy

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
R1B = runpy.run_path(str(ROOT / "experiments/r1b_readout_design_audit.py"))
ATOL = 1e-10
BASELINE = "bd02f1a7a0a944c5bd60a395fcdcdaad67304f1d"
norm = R1B["norm"]


def construct_open(copy):
    if copy not in (0, 1):
        raise ValueError("copy must be 0 or 1")
    support, ready, t, d, _ = R1B["components"]()
    links = [(d if copy else np.eye(28)) @ t[0], t[1]]
    fibers = [np.eye(28), links[0], links[1] @ links[0]]
    h = np.kron(np.eye(3), np.eye(36) - support @ support.conj().T)
    for j, u in enumerate(links):
        edge = (np.kron(R1B["clock_state"](j + 1, 3).conj().reshape(1, 3), support.conj().T)
                - np.kron(R1B["clock_state"](j, 3).conj().reshape(1, 3), u @ support.conj().T))
        h = h + edge.conj().T @ edge / 2
    # No closing edge and no monodromy projection: every seed is allowed.
    history = sum(np.kron(R1B["clock_state"](j, 3).reshape(3, 1), support @ f)
                  for j, f in enumerate(fibers)) / np.sqrt(3)
    return {"constraint": h, "history": history, "ready": ready,
            "support": support, "fibers": fibers}


def audit():
    models = {s: construct_open(s) for s in (0, 1)}
    report = {}
    for setting, model in models.items():
        h, j, e = (model[k] for k in ("constraint", "history", "ready"))
        eigenvalues = np.linalg.eigvalsh(h)
        assert eigenvalues.min() > -ATOL
        assert int(np.sum(abs(eigenvalues) < ATOL)) == 28
        assert norm(h @ j) < ATOL and norm(j.conj().T @ j - np.eye(28)) < ATOL
        # The nonzero spectral gap differs from the compensated cyclic model.
        gap = float(eigenvalues[eigenvalues > ATOL].min())
        assert abs(gap - .5) < ATOL
        prep_error = norm(R1B["reduction"]("A", 0) @ j @ e - model["support"] @ e)
        assert prep_error < ATOL
        f2 = model["fibers"][2]
        ks = [np.kron(np.eye(14), np.eye(2)[b:b+1]) @ f2 @ e for b in (0, 1)]
        tp_error = norm(sum(k.conj().T @ k for k in ks) - np.eye(14))
        assert tp_error < ATOL
        v = R1B["canonical_source_support_coordinates"]()
        seed = e @ v
        effects = [f2.conj().T @ R1B["pointer_effect"](b) @ f2 for b in (0, 1)]
        ps = [float(np.vdot(seed, ef @ seed).real) for ef in effects]
        assert np.allclose(ps, [.5, .5] if setting else [1, 0], atol=ATOL, rtol=0)
        charts = []
        for clock in ("A", "C"):
            for reading in range(3):
                basis, r, g, sv = R1B["chart"](j, clock, reading)
                ri = np.linalg.inv(r)
                errors = [norm(r.conj().T @ g @ r - np.eye(28)),
                          norm(j @ ri @ basis.conj().T @ R1B["reduction"](clock, reading) @ j - j)]
                for ef in effects:
                    ox = r @ ef @ ri
                    errors.append(norm(r.conj().T @ g @ ox @ r - ef))
                assert max(errors) < ATOL
                charts.append({"clock": clock, "reading": reading,
                               "rank": 28, "min_singular_value": sv,
                               "max_all_input_identity_error": max(errors)})
        cyclic = R1B["construct"]("compensated" if setting else "off")
        jc, hc = cyclic["history"], cyclic["constraint"]
        cyclic_seed_map = jc @ cyclic["seeds"].conj().T
        projector_error = norm(j @ j.conj().T - jc @ jc.conj().T)
        state_map_error = norm(j - cyclic_seed_map)
        h_difference = norm(h - hc)
        cyclic_eigenvalues = np.linalg.eigvalsh(hc)
        cyclic_gap = float(cyclic_eigenvalues[cyclic_eigenvalues > ATOL].min())
        # The ambient complement penalty has energy 1, so the full gap is 1;
        # the cyclic history-support propagation gap is 3/2.
        assert abs(cyclic_gap - 1) < ATOL
        assert max(projector_error, state_map_error) < ATOL
        assert h_difference > 1
        report[str(setting)] = {
            "copy_interactions_in_interval": setting,
            "physical_dimension": 28, "ready_input_dimension": 14,
            "constraint_residual": norm(h @ j), "preparation_error": prep_error,
            "final_instrument_tp_error": tp_error,
            "canonical_pointer_at_A_e2": ps, "open_full_spectral_gap": gap,
            "cyclic_comparator": "compensated" if setting else "off",
            "cyclic_full_spectral_gap": cyclic_gap,
            "kernel_projector_difference": projector_error,
            "all_seed_history_map_difference": state_map_error,
            "constraint_matrix_difference": h_difference, "charts": charts}

    # The closed single-copy model is a proper subspace of the open one.
    closed_single = R1B["construct"]("single")
    p_open = models[1]["history"] @ models[1]["history"].conj().T
    p_single = closed_single["history"] @ closed_single["history"].conj().T
    subset_error = norm(p_open @ p_single - p_single)
    assert subset_error < ATOL
    assert int(np.linalg.matrix_rank(p_open - p_single, tol=ATOL)) == 7
    common_preparation_error = norm(R1B["reduction"]("A", 0) @ (
        models[0]["history"] @ models[0]["ready"] - models[1]["history"] @ models[1]["ready"]))
    assert common_preparation_error < ATOL
    # The standard open history is genuinely outside the closed-single kernel.
    standard = models[1]["history"] @ models[1]["ready"] @ R1B["canonical_source_support_coordinates"]()
    single_violation = norm(closed_single["constraint"] @ standard)
    assert single_violation > .1
    source_paths = ["experiments/r1b_readout_design_audit.py",
                    "src/t_search/stage7_history.py", "src/t_search/stage7_spectator.py",
                    "src/t_search/stage7_record.py", "src/t_search/stage5_clock_change.py"]
    return {"baseline_commit": BASELINE, "numpy_version": np.__version__, "atol": ATOL,
            "purpose": "clarify_blockness_becoming", "status": "supplement_and_synthesis_completed",
            "original_pilot_gate": "blocked", "new_scientific_claim": False,
            "kinematic_dimension": 108, "open_settings": report,
            "closed_single_subset_error": subset_error,
            "closed_single_excluded_seed_dimensions": 7,
            "open_common_preparation_error": common_preparation_error,
            "open_standard_state_closed_single_constraint_violation": single_violation,
            "source_sha256": {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in source_paths}}


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, ensure_ascii=False, allow_nan=False))
