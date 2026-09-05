"""Finite readout design audit: one CNOT on a closed three-event history.

The strict family is off/single. 'compensated' is an explicitly over-budget
diagnostic, with a second CNOT at the closing edge. No projection repairs a
failed preparation. This is a discrete propagation constraint, not an additive
continuous-time interaction Hamiltonian. Run this file to emit JSON.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from t_search.stage5_clock_change import clock_state
from t_search.stage7_history import (
    canonical_source_support_coordinates,
    history_constraint_operator,
    history_physical_basis,
    history_transition_support_matrix,
)
from t_search.stage7_record import canonical_target_pair_projector
from t_search.stage7_spectator import (
    spectator_kinematic_clock_projection_operator,
    spectator_support_basis,
)

ATOL = 1e-10
BASELINE = "4b46b54cf180c627c3a972a6b4a434afa0180ad1"


def norm(a):
    return float(np.linalg.norm(a))


def nullspace(a):
    _, sv, vh = np.linalg.svd(a, full_matrices=True)
    rank = int(np.sum(sv > ATOL))
    return vh.conj().T[:, rank:]


def components():
    cnot = np.eye(4, dtype=complex)
    cnot[2:, 2:] = np.array([[0, 1], [1, 0]])
    support = np.kron(spectator_support_basis("A"), np.eye(2))
    ready = np.kron(np.eye(14), np.array([[1], [0]]))
    t = [np.kron(history_transition_support_matrix("forward", j, k), np.eye(2))
         for j, k in ((1, 0), (2, 1), (0, 2))]
    return support, ready, t, np.kron(np.eye(7), cnot), np.kron(np.eye(9), cnot)


def construct(mode):
    if mode not in ("off", "single", "compensated"):
        raise ValueError("unknown design")
    support, ready, t, d, d_ambient = components()
    links = [u.copy() for u in t]
    if mode != "off":
        links[0] = d @ t[0]  # Record formation first, then copying M to N.
    if mode == "compensated":
        links[2] = t[2] @ d.conj().T  # Extra interaction, not a free reset.
    fibers = [np.eye(28), links[0], links[1] @ links[0]]
    loop = links[2] @ fibers[2]
    seeds = nullspace(loop - np.eye(28))
    ready_seeds = nullspace((loop - np.eye(28)) @ ready)
    history = sum(np.kron(clock_state(j, 3).reshape(3, 1), support @ f @ seeds)
                  for j, f in enumerate(fibers)) / np.sqrt(3)
    # Penalize disallowed BC support explicitly; never enlarge the old support.
    h = np.kron(np.eye(3), np.eye(36) - support @ support.conj().T)
    for j, u in enumerate(links):
        k = (j + 1) % 3
        edge = (np.kron(clock_state(k, 3).conj().reshape(1, 3), support.conj().T)
                - np.kron(clock_state(j, 3).conj().reshape(1, 3), u @ support.conj().T))
        h = h + edge.conj().T @ edge / 2
    return {"mode": mode, "support": support, "ready": ready,
            "t": t, "d": d, "d_ambient": d_ambient,
            "links": links, "fibers": fibers, "loop": loop,
            "seeds": seeds, "ready_seeds": ready_seeds,
            "history": history, "constraint": h}


def reduction(clock, reading):
    return np.sqrt(3) * np.kron(
        spectator_kinematic_clock_projection_operator(clock, reading), np.eye(2))


def chart(history, clock, reading):
    q, r = np.linalg.qr(reduction(clock, reading) @ history, mode="reduced")
    sv = np.linalg.svd(r, compute_uv=False)
    assert sv.min() > ATOL
    ri = np.linalg.inv(r)
    return q, r, ri.conj().T @ ri, float(sv.min())


def pointer_effect(bit):
    return np.kron(np.eye(14), np.diag([int(bit == 0), int(bit == 1)]))


def model_audit(model):
    s, e, q = model["support"], model["ready"], model["seeds"]
    j, h, f = model["history"], model["constraint"], model["fibers"]
    rdim = q.shape[1]
    ev = np.linalg.eigvalsh(h)
    assert ev.min() > -ATOL
    assert int(np.sum(abs(ev) < ATOL)) == rdim
    assert norm(h @ j) < ATOL and norm(j.conj().T @ j - np.eye(rdim)) < ATOL
    assert all(norm(u.conj().T @ u - np.eye(28)) < ATOL for u in model["links"])
    # Outcome effects refer to A/e2, even when represented in a C chart.
    effects = [q.conj().T @ f[2].conj().T @ pointer_effect(b) @ f[2] @ q for b in (0, 1)]
    assert norm(sum(effects) - np.eye(rdim)) < ATOL
    # Compression onto Fix(loop) can make pointer effects unsharp (single).
    # Positive square roots give a mathematical instrument on solution space;
    # this does not establish a physical final detector within the closed cycle.
    physical_kraus = []
    for ef in effects:
        assert norm(ef.conj().T - ef) < ATOL
        vals, vecs = np.linalg.eigh(ef)
        assert vals.min() > -ATOL and vals.max() < 1 + ATOL
        physical_kraus.append((vecs * np.sqrt(np.maximum(vals, 0))) @ vecs.conj().T)
    charts = []
    for clock in ("A", "C"):
        for reading in range(3):
            basis, r, g, min_sv = chart(j, clock, reading)
            ri = np.linalg.inv(r)
            kraus = [r @ k @ ri for k in physical_kraus]
            metric_error = norm(r.conj().T @ g @ r - np.eye(rdim))
            tp_error = norm(sum(k.conj().T @ g @ k for k in kraus) - g)
            # Operator identities certify all input states, rather than a few probes.
            probability_error = max(norm(r.conj().T @ k.conj().T @ g @ k @ r - ef)
                                    for k, ef in zip(kraus, effects))
            reconstruction_error = norm(j @ ri @ basis.conj().T @ reduction(clock, reading) @ j - j)
            assert max(metric_error, tp_error, probability_error, reconstruction_error) < ATOL
            charts.append({"clock": clock, "reading": reading, "rank": rdim,
                           "min_singular_value": min_sv,
                           "metric_error": metric_error, "tp_error": tp_error,
                           "all_state_probability_error": probability_error,
                           "reconstruction_error": reconstruction_error})

    v = canonical_source_support_coordinates()
    seed = e @ v
    defect = norm((model["loop"] - np.eye(28)) @ seed)
    output = {"physical_dimension": rdim,
              "ready_input_dimension": model["ready_seeds"].shape[1],
              "canonical_loop_defect": defect,
              "constraint_residual": norm(h @ j),
              "pointer_effect_projectivity_errors": [norm(ef @ ef - ef) for ef in effects],
              "canonical_probabilities": None, "charts": charts}
    if defect < ATOL:
        coeff = q.conj().T @ seed
        state = j @ coeff
        expected = [float(np.vdot(coeff, ef @ coeff).real) for ef in effects]
        represented = []
        raw_c = []
        for clock in ("A", "C"):
            for reading in range(3):
                _, r, g, _ = chart(j, clock, reading)
                y = r @ coeff
                ps = [float(np.vdot(y, g @ r @ ef @ np.linalg.inv(r) @ y).real)
                      for ef in effects]
                assert max(abs(a - b) for a, b in zip(ps, expected)) < ATOL
                represented.append({"clock": clock, "reading": reading, "p_N_at_A_e2": ps})
                if clock == "C":
                    raw = reduction(clock, reading) @ state
                    p1 = float(np.vdot(raw, np.kron(np.eye(18), np.diag([0, 1])) @ raw).real
                               / np.vdot(raw, raw).real)
                    raw_c.append(p1)
        bproj = np.kron(canonical_target_pair_projector(), np.eye(4))
        final = f[2] @ seed
        joint = [[float(np.vdot(final, bp @ pointer_effect(n) @ final).real) for n in (0, 1)]
                 for bp in (np.eye(28) - bproj, bproj)]
        output["canonical_probabilities"] = {
            "pointer_at_A_e2": expected, "final_B_by_N": joint,
            "same_A_e2_event_in_charts": represented,
            "different_question_bare_N_given_C_reading": raw_c}
    else:
        # Deliberately do not project or renormalize the inadmissible seed.
        allowed = e @ model["ready_seeds"]
        n1 = allowed.conj().T @ f[2].conj().T @ pointer_effect(1) @ f[2] @ allowed
        output["allowed_ready_inputs_N1_effect_norm"] = norm(n1)
        assert norm(n1) < ATOL
    return output


def audit():
    models = {name: construct(name) for name in ("off", "single", "compensated")}
    off, single, comp = (models[name] for name in ("off", "single", "compensated"))
    e, t, d = off["ready"], off["t"], off["d"]
    assert norm(t[2] @ t[1] @ t[0] - np.eye(28)) < ATOL
    assert norm(d @ t[1] - t[1] @ d) < ATOL
    assert norm(single["loop"] - t[0].conj().T @ d @ t[0]) < ATOL
    expected_dims = {"off": (28, 14), "single": (21, 7), "compensated": (28, 14)}
    results = {name: model_audit(m) for name, m in models.items()}
    for name, (physical, ready) in expected_dims.items():
        assert results[name]["physical_dimension"] == physical
        assert results[name]["ready_input_dimension"] == ready
    assert abs(results["single"]["canonical_loop_defect"] - 1) < ATOL
    assert results["single"]["canonical_probabilities"] is None
    for name, expected in (("off", [1, 0]), ("compensated", [.5, .5])):
        assert np.allclose(results[name]["canonical_probabilities"]["pointer_at_A_e2"], expected, atol=ATOL, rtol=0)
    cp = results["compensated"]["canonical_probabilities"]
    assert np.allclose(cp["final_B_by_N"], np.full((2, 2), .25), atol=ATOL, rtol=0)
    assert np.allclose(cp["different_question_bare_N_given_C_reading"], [3 / 14, 3 / 7, 3 / 8], atol=ATOL, rtol=0)

    # Check equivalence of kernels only; the propagation and Stage 7 Hamiltonians
    # have different nonzero spectra. Compare also the tempting dressed extension.
    old_j = np.kron(history_physical_basis("forward"), np.eye(2))
    old_p = old_j @ old_j.conj().T
    w = sum(np.kron(np.outer(clock_state(k, 3), clock_state(k, 3).conj()),
                    np.eye(36) if k == 0 else comp["d_ambient"]) for k in range(3))
    hd = w @ np.kron(history_constraint_operator("forward"), np.eye(2)) @ w.conj().T
    kernel_errors = {
        "off_vs_stage7": norm(off["history"] @ off["history"].conj().T - old_p),
        "compensated_vs_dressing": norm(comp["history"] @ comp["history"].conj().T - w @ old_p @ w.conj().T),
        "dressed_constraint_on_compensated_basis": norm(hd @ comp["history"])}
    assert max(kernel_errors.values()) < ATOL

    # The common A/e0 preparation is exact in off and compensated for all inputs.
    def ready_history(m):
        return m["history"] @ m["seeds"].conj().T @ m["ready"]
    prep_error = norm(reduction("A", 0) @ (ready_history(off) - ready_history(comp)))
    assert prep_error < ATOL
    # Coherent readout is a TP Stinespring isometry before final pointer readout.
    f2 = comp["fibers"][2] @ e
    ks = [np.kron(np.eye(14), np.eye(2)[b:b+1]) @ f2 for b in (0, 1)]
    tp_error = norm(sum(k.conj().T @ k for k in ks) - np.eye(14))
    assert tp_error < ATOL
    plain_t10 = history_transition_support_matrix("forward", 1, 0)
    plain_t21 = history_transition_support_matrix("forward", 2, 1)
    expected_ks = [plain_t21 @ np.kron(np.eye(7), np.diag([int(b == 0), int(b == 1)]))
                   @ plain_t10 for b in (0, 1)]
    dilation_error = max(norm(k - expected) for k, expected in zip(ks, expected_ks))
    assert dilation_error < ATOL
    # All-input obstruction: with no further N coupling, N=1 at e2 has the
    # same effect as M=1 immediately before the single copying operation.
    n1_at_end = e.conj().T @ single["fibers"][2].conj().T @ pointer_effect(1) @ single["fibers"][2] @ e
    m1_at_copy = plain_t10.conj().T @ np.kron(np.eye(7), np.diag([0, 1])) @ plain_t10
    persistence_error = norm(n1_at_end - m1_at_copy)
    assert persistence_error < ATOL
    paths = ["src/t_search/stage7_history.py", "src/t_search/stage7_record.py",
             "src/t_search/stage7_spectator.py", "src/t_search/stage5_clock_change.py",
             "src/t_search/stage5_reductions.py", "src/t_search/stage5_clock_transforms.py"]
    hashes = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths}
    return {"baseline_commit": BASELINE, "numpy_version": np.__version__, "atol": ATOL,
            "status": "completed_strict_candidate_rejected",
            "pilot_gate": "blocked", "new_scientific_claim": False,
            "strict_budget": {"pointer_qubits": 1, "pointer_ready_state": "0",
                              "CNOTs_per_cycle": 1, "periodic_events": 3},
            "kinematic_dimension": 108, "models": results,
            "kernel_comparison_errors": kernel_errors,
            "off_compensated_common_preparation_error": prep_error,
            "compensated_final_instrument_tp_error": tp_error,
            "compensated_readout_dilation_error": dilation_error,
            "single_pointer_persistence_effect_error": persistence_error,
            "compensated_CNOTs_per_cycle": 2, "compensated_within_budget": False,
            "source_sha256": hashes}


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, ensure_ascii=False, allow_nan=False))
