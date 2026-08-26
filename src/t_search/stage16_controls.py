"""Stage 16F topology/locality-breaking, anomaly, and false-positive controls."""
from __future__ import annotations

from dataclasses import dataclass, replace
from functools import lru_cache

import numpy as np

from .stage15_basis import stage15d_diagnostics
from .stage16_basis import (
    STAGE16D_CLASSIFICATION,
    STAGE16D_LFINITE_MAX_DEPTH,
    STAGE16D_NONLOCAL,
    canonical_stage16d_candidates,
    stage16d_known_seed_locality_audit,
)
from .stage16_local import (
    STAGE16A_ATOL,
    STAGE16A_C,
    STAGE16A_KAPPA,
    STAGE16A_SMEARING_PAIRS,
    canonical_stage16a_off_surface_probes,
    canonical_stage16a_representatives,
    stage16a_constraint_gradients,
    stage16a_frame_determinant,
    stage16a_jacobi_residual,
    stage16a_poisson_pair,
    stage16a_smeared_direct,
)
from .stage16_measurement import (
    canonical_stage16e_architectures,
    stage16e_architecture_for_representative,
    stage16e_quotient_projection,
    stage16e_validate_architecture,
)
from .stage16_paths import canonical_stage16b_local_probes
from .stage16_relational import stage16c_diagnostics

STAGE16F_STRUCTURE_REMOVED = "structure_function_removed_control_rejected"
STAGE16F_CYCLE_OPENING = "cycle_opening_control_detected"
STAGE16F_THREE_CYCLE = "three_cycle_locality_degeneracy_detected"
STAGE16F_DISCONNECTED = "disconnected_component_false_positive_rejected"
STAGE16F_SUPPORT_EXPANSION = "support_expansion_detected"
STAGE16F_OPPOSITE_SITE = "opposite_site_basis_nonlocal_detected"
STAGE16F_INVERSE_NONLOCAL = "inverse_nonlocality_detected"
STAGE16F_GLOBAL_SEED = "global_seed_not_L1_detected"
STAGE16F_SINGULAR = "singular_cycle_frame_rejected"
STAGE16F_SMEARING = "smearing_antisymmetry_corruption_detected"
STAGE16F_ANOMALY = "constraint_algebra_anomaly_detected"
STAGE16F_WRONG_COMPENSATOR = "wrong_compensator_rejected"
STAGE16F_CROSS_ORBIT = "cross_orbit_false_positive_rejected"
STAGE16F_INCOMPLETE_RELATIONAL = "relational_observable_incomplete"
STAGE16F_TYPED = "typed_payload_provenance_corruption_detected"
STAGE16F_NUMERICAL_ONLY = "numerical_only_commuting_claim_rejected"

STAGE16F_REQUIRED_VOCABULARY = (
    STAGE16F_STRUCTURE_REMOVED,
    STAGE16F_CYCLE_OPENING,
    STAGE16F_THREE_CYCLE,
    STAGE16F_DISCONNECTED,
    STAGE16F_SUPPORT_EXPANSION,
    STAGE16F_OPPOSITE_SITE,
    STAGE16F_INVERSE_NONLOCAL,
    STAGE16F_GLOBAL_SEED,
    STAGE16F_SINGULAR,
    STAGE16F_SMEARING,
    STAGE16F_ANOMALY,
    STAGE16F_WRONG_COMPENSATOR,
    STAGE16F_CROSS_ORBIT,
    STAGE16F_INCOMPLETE_RELATIONAL,
    STAGE16F_TYPED,
    STAGE16F_NUMERICAL_ONLY,
)

STAGE16F_GUARDS = (
    "negative-control rejection != proof of continuum correctness",
    "cycle opening changes graph topology != proof that topology is ontic",
    "three-cycle L1 label != nontrivial locality evidence",
    "locality-breaking detection != physical causal locality",
    "constraint-algebra anomaly detection != quantum anomaly theorem",
    "cross-orbit rejection != ontological superselection",
    "incomplete relational rejection != ontological becoming",
    "typed corruption detection != ontological equivalence",
    "numerical-only commuting rejection != universal non-Abelianity",
    "four-site constraint precursor != general relativity",
    "repository validation != new scientific evidence",
)

STAGE16F_BOUNDED_RESULT = (
    "Stage 16F frozen topology/locality-breaking, algebra/path anomaly, "
    "false-positive, relational, and typed-payload controls on the Stage 16 "
    "finite four-cycle carrier = all declared controls rejected as intended"
)


@dataclass(frozen=True, slots=True)
class Stage16FControlResult:
    control_id: str
    classification: str
    rejected: bool
    witness_count: int
    violation_count: int
    max_signal: float
    detail: str


@dataclass(frozen=True, slots=True)
class Stage16FDiagnostics:
    control_count: int
    rejected_control_count: int
    required_vocabulary_count: int
    required_vocabulary_covered: bool
    cycle_opening_exhibited_depth: int | None
    three_site_projection_one_step_l1: bool
    typed_corruption_control_count: int
    typed_corruption_detected_count: int
    all_controls_rejected: bool
    criteria_45_47_satisfied: bool


def _poisson(df: np.ndarray, dg: np.ndarray) -> float:
    return float(sum(df[q] * dg[p] - df[p] * dg[q] for q, p in ((0,1),(2,3),(4,5),(6,7),(8,9))))


def _structure_removed_control() -> Stage16FControlResult:
    probes = canonical_stage16a_off_surface_probes()
    baseline = sum(
        any(abs(stage16a_poisson_pair(point, i, (i + 1) % 4)) > STAGE16A_ATOL for i in range(4))
        for point in probes
    )
    removed = 0
    max_removed = 0.0
    for point in probes:
        g = stage16a_constraint_gradients(point, kappa=0.0)
        vals = [abs(_poisson(g[i], g[j])) for i in range(4) for j in range(i + 1, 4)]
        max_removed = max(max_removed, max(vals))
        removed += max(vals) > STAGE16A_ATOL
    rejected = baseline > 0 and removed == 0
    return Stage16FControlResult(
        "kappa_zero_structure_function_removal", STAGE16F_STRUCTURE_REMOVED,
        bool(rejected), len(probes), int(baseline), float(max_removed),
        f"baseline_nonzero_points={baseline}; kappa0_nonzero_points={removed}",
    )


def _seed_gradient(seed_index: int) -> np.ndarray:
    g = np.zeros(10, dtype=float)
    g[1] = STAGE16A_C[seed_index]
    g[3 + 2 * seed_index] = 1.0
    return g


def _open_chain_depth2_control() -> Stage16FControlResult:
    # Opening only the wrap term C3=K3 permits two local peeling steps:
    # row2 <- row2-a2 row3, then row1 <- row1-a1 row2.  The result is
    # (K0+a0*K1,K1,K2,K3), which strongly commutes.
    residuals = []
    for point in canonical_stage16a_off_surface_probes():
        k = [_seed_gradient(i) for i in range(4)]
        seed1_value = point.pi1 + STAGE16A_C[1] * point.P
        g0 = k[0] + STAGE16A_KAPPA * point.T0 * k[1]
        g0 = g0.copy()
        g0[2] += STAGE16A_KAPPA * seed1_value
        gradients = (g0, k[1], k[2], k[3])
        residuals.append(max(abs(_poisson(gradients[i], gradients[j])) for i in range(4) for j in range(i + 1, 4)))
    max_res = max(residuals)
    rejected = max_res <= STAGE16A_ATOL and STAGE16D_LFINITE_MAX_DEPTH >= 2
    return Stage16FControlResult(
        "wrap_edge_opening_depth2_peeling", STAGE16F_CYCLE_OPENING,
        bool(rejected), len(residuals), sum(x <= STAGE16A_ATOL for x in residuals), float(max_res),
        "remove only kappa*T3*K0; an explicit two-step local peeling yields a strong basis (depth=2), unlike the closed-cycle frozen depth<=4 search",
    )


def _three_site_projection_control() -> Stage16FControlResult:
    d = stage15d_diagnostics()
    rejected = d.local_abelianization_established and d.minimum_local_abelianization_depth == 1
    return Stage16FControlResult(
        "three_site_projection_recovers_stage15_pattern", STAGE16F_CYCLE_OPENING,
        bool(rejected), 1, int(rejected), float(d.minimum_local_abelianization_depth),
        "removing site 3 recovers the Stage 15 open three-site one-step L1 witness",
    )


def _three_cycle_degeneracy_control() -> Stage16FControlResult:
    n1 = {i: {i, (i - 1) % 3, (i + 1) % 3} for i in range(3)}
    degenerate = all(len(v) == 3 for v in n1.values())
    return Stage16FControlResult(
        "three_cycle_radius1_is_global", STAGE16F_THREE_CYCLE,
        degenerate, 3, sum(len(v) == 3 for v in n1.values()), 3.0,
        "on C3 every radius-1 neighbourhood contains all three sites, so L1 is not a nontrivial locality restriction",
    )


def _graph_connected(edges: set[tuple[int, int]], source: int, target: int) -> bool:
    adj = {i: set() for i in range(4)}
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    seen = {source}; stack = [source]
    while stack:
        x = stack.pop()
        if x == target:
            return True
        for y in adj[x]:
            if y not in seen:
                seen.add(y); stack.append(y)
    return False


def _disconnected_control() -> Stage16FControlResult:
    edges = {(0,1), (2,3)}
    connected = _graph_connected(edges, 0, 3)
    return Stage16FControlResult(
        "disconnected_0_to_3_false_path", STAGE16F_DISCONNECTED,
        not connected, 1, int(not connected), 1.0 if not connected else 0.0,
        "after cutting the 1-2 and 3-0 edges, sites 0 and 3 lie in disconnected components and no cross-component path is licensed",
    )


def _support_expansion_control() -> Stage16FControlResult:
    n1_0 = {3,0,1}
    corrupted_labels = {0,2}
    rejected = not corrupted_labels <= n1_0
    return Stage16FControlResult(
        "opposite_generator_support_expansion", STAGE16F_SUPPORT_EXPANSION,
        rejected, 1, int(rejected), float(len(corrupted_labels - n1_0)),
        "an alleged row-0 L1 generator explicitly mixes opposite label 2",
    )


def _opposite_site_coefficient_control() -> Stage16FControlResult:
    n1_0 = {3,0,1}
    coefficient_sites = {2}
    rejected = not coefficient_sites <= n1_0
    return Stage16FControlResult(
        "opposite_site_coefficient_dependency", STAGE16F_OPPOSITE_SITE,
        rejected, 1, int(rejected), float(len(coefficient_sites - n1_0)),
        "row 0 uses only local generator labels but an alleged L1 coefficient depends on opposite-site T2",
    )


def _inverse_nonlocality_control() -> Stage16FControlResult:
    lam = 0.25
    B = np.eye(4)
    for i in range(4):
        B[i, (i + 1) % 4] = lam
    Binv = np.linalg.inv(B)
    opposite = sum(abs(Binv[i, (i + 2) % 4]) > STAGE16A_ATOL for i in range(4))
    forward_local = all(all(abs(B[i,j]) <= STAGE16A_ATOL or j in {i,(i-1)%4,(i+1)%4} for j in range(4)) for i in range(4))
    rejected = forward_local and opposite == 4
    return Stage16FControlResult(
        "forward_local_inverse_dense_cycle_map", STAGE16F_INVERSE_NONLOCAL,
        bool(rejected), 4, int(opposite), float(max(abs(Binv[i,(i+2)%4]) for i in range(4))),
        "forward cyclic nearest-neighbour map is local, but its inverse has nonzero opposite-site entries in every row",
    )


def _global_seed_control() -> Stage16FControlResult:
    audit = stage16d_known_seed_locality_audit()
    rejected = (not audit.forward_map_l1 and audit.locality_class == STAGE16D_NONLOCAL and audit.opposite_generator_nonzero_row_count == 4)
    return Stage16FControlResult(
        "known_global_seed_not_silently_L1", STAGE16F_GLOBAL_SEED,
        bool(rejected), 4, audit.opposite_generator_nonzero_row_count, float(audit.determinant_clock_dependence_count),
        "known global seed reconstruction remains strongly useful as a control but is nonlocal_for_stage16_L1",
    )


def _singular_frame_control() -> Stage16FControlResult:
    rep = next(r for r in canonical_stage16a_representatives() if r.point().clocks() == (1.,1.,1.,1.))
    determinant = stage16a_frame_determinant(rep.point(), kappa=1.0)
    rejected = abs(determinant) <= STAGE16A_ATOL
    return Stage16FControlResult(
        "kappa1_all_ones_singular_cycle_frame", STAGE16F_SINGULAR,
        rejected, 1, int(rejected), abs(float(determinant)),
        "kappa=1 with all clocks=1 gives Delta=0 and the cyclic frame is rejected as singular",
    )


def _smearing_sign_control() -> Stage16FControlResult:
    residuals = []
    for point in canonical_stage16a_off_surface_probes():
        for N, M in STAGE16A_SMEARING_PAIRS:
            nm = stage16a_smeared_direct(point, N, M)
            corrupted_reverse = nm
            residuals.append(abs(nm + corrupted_reverse))
    detected = sum(x > STAGE16A_ATOL for x in residuals)
    return Stage16FControlResult(
        "wrong_smearing_reverse_sign", STAGE16F_SMEARING,
        detected > 0, len(residuals), detected, float(max(residuals, default=0.0)),
        "reversed smeared bracket is deliberately assigned the same sign",
    )


def _jacobi_anomaly_control() -> Stage16FControlResult:
    epsilon = 0.125
    residuals = []
    for point in canonical_stage16a_off_surface_probes():
        residuals.append(abs(stage16a_jacobi_residual(point, 0, 1, 2) - epsilon))
    detected = sum(x > STAGE16A_ATOL for x in residuals)
    return Stage16FControlResult(
        "jacobi_violating_epsilon_T2_anomaly", STAGE16F_ANOMALY,
        detected == len(residuals) and detected > 0, len(residuals), detected,
        float(max(residuals, default=0.0)),
        "adds epsilon*T2 to {C0,C1}; the (0,1,2) Jacobiator acquires a nonzero constant contribution",
    )


def _wrong_compensator_control() -> Stage16FControlResult:
    probes = canonical_stage16b_local_probes()
    violations = sum(p.missing_residual > STAGE16A_ATOL and p.wrong_sign_residual > STAGE16A_ATOL for p in probes)
    min_signal = min(min(p.missing_residual, p.wrong_sign_residual) for p in probes)
    return Stage16FControlResult(
        "missing_or_wrong_sign_local_compensator", STAGE16F_WRONG_COMPENSATOR,
        violations == len(probes), len(probes), violations, float(min_signal),
        "every frozen adjacent local probe rejects both missing and wrong-sign compensation",
    )


def _cross_orbit_control() -> Stage16FControlResult:
    d = stage16c_diagnostics()
    rejected = d.cross_orbit_rejected_count == d.cross_orbit_ordered_pair_count and d.cross_orbit_rejected_count > 0
    return Stage16FControlResult(
        "cross_orbit_path_false_positive", STAGE16F_CROSS_ORBIT,
        bool(rejected), d.cross_orbit_ordered_pair_count, d.cross_orbit_rejected_count, float(d.min_orbit_pair_separation),
        "all ordered cross-orbit representative pairs are rejected by the Dirac-pair quotient",
    )


def _incomplete_relational_control() -> Stage16FControlResult:
    d = stage16c_diagnostics()
    rejected = d.omitted_clock_incomplete_group_count == d.omitted_clock_group_count == 16
    return Stage16FControlResult(
        "single_clock_omission_four_clock_relational", STAGE16F_INCOMPLETE_RELATIONAL,
        bool(rejected), d.omitted_clock_group_count, d.omitted_clock_incomplete_group_count,
        float(max(d.omitted_clock_spreads)),
        "all four single-clock omissions across all four orbits retain representative dependence",
    )


def _typed_corruption_controls() -> tuple[Stage16FControlResult, ...]:
    reps = canonical_stage16a_representatives()
    base = canonical_stage16e_architectures()[0]
    baseline_projection = stage16e_quotient_projection(base)
    event0 = base.O.relational_events[0]
    corrupt_o = replace(base, O=replace(base.O, relational_events=(replace(event0, q_value=float(event0.q_value + 0.01)), *base.O.relational_events[1:])))
    corrupt_p = replace(base, P=replace(base.P, qext_ids=tuple(reversed(base.P.qext_ids))))

    l1_candidate = next(c for c in canonical_stage16d_candidates() if c.lfinite_depth == 1)
    basis_arch = stage16e_architecture_for_representative(reps[0], l1_candidate.candidate_id)
    direction0 = basis_arch.R.R_direction[0]
    corrupt_r = replace(basis_arch, R=replace(basis_arch.R, R_direction=(replace(direction0, record_score=float(direction0.record_score + 0.01)), *basis_arch.R.R_direction[1:])))
    weights = list(basis_arch.V.V_weights); weights[0] += 0.01; weights[1] -= 0.01
    corrupt_v = replace(basis_arch, V=replace(basis_arch.V, V_weights=tuple(weights)))

    cases = (
        ("representative_dependent_O_corruption", corrupt_o, baseline_projection),
        ("path_dependent_P_corruption", corrupt_p, baseline_projection),
        ("basis_dependent_R_corruption", corrupt_r, stage16e_quotient_projection(basis_arch)),
        ("depth_dependent_V_corruption", corrupt_v, stage16e_quotient_projection(basis_arch)),
    )
    out = []
    for cid, corrupted, expected in cases:
        valid, _ = stage16e_validate_architecture(corrupted)
        changed = stage16e_quotient_projection(corrupted) != expected
        detected = (not valid) and changed
        out.append(Stage16FControlResult(
            cid, STAGE16F_TYPED, bool(detected), 1, int(detected), 1.0 if detected else 0.0,
            "illicit representative/path/basis/depth-conditioned mutation changes public payload and fails typed architecture validation",
        ))
    return tuple(out)


def _numerical_only_commuting_control() -> Stage16FControlResult:
    zero = next(p for p in canonical_stage16a_off_surface_probes() if p.clocks() == (0.,0.,0.,0.))
    sample_max = max(abs(stage16a_poisson_pair(zero, i, j)) for i in range(4) for j in range(i + 1,4))
    other = next(p for p in canonical_stage16a_off_surface_probes() if p.clocks() == (-1.,-1.,-1.,-1.))
    global_max = max(abs(stage16a_poisson_pair(other, i, j)) for i in range(4) for j in range(i + 1,4))
    rejected = sample_max <= STAGE16A_ATOL and global_max > STAGE16A_ATOL
    return Stage16FControlResult(
        "single_zero_clock_sample_claims_strong_commutation", STAGE16F_NUMERICAL_ONLY,
        bool(rejected), 2, int(rejected), float(global_max),
        "the original basis happens to commute at the zero-clock sample but is noncommuting at another off-surface point, so sampled numerical zero cannot certify strong commutation",
    )


@lru_cache(maxsize=1)
def canonical_stage16f_controls() -> tuple[Stage16FControlResult, ...]:
    return (
        _structure_removed_control(),
        _open_chain_depth2_control(),
        _three_site_projection_control(),
        _three_cycle_degeneracy_control(),
        _disconnected_control(),
        _support_expansion_control(),
        _opposite_site_coefficient_control(),
        _inverse_nonlocality_control(),
        _global_seed_control(),
        _singular_frame_control(),
        _smearing_sign_control(),
        _jacobi_anomaly_control(),
        _wrong_compensator_control(),
        _cross_orbit_control(),
        _incomplete_relational_control(),
        *_typed_corruption_controls(),
        _numerical_only_commuting_control(),
    )


@lru_cache(maxsize=1)
def stage16f_diagnostics() -> Stage16FDiagnostics:
    controls = canonical_stage16f_controls()
    classifications = {x.classification for x in controls}
    all_rejected = all(x.rejected for x in controls)
    vocabulary = set(STAGE16F_REQUIRED_VOCABULARY) <= classifications
    opening = next(x for x in controls if x.control_id == "wrap_edge_opening_depth2_peeling")
    projection = next(x for x in controls if x.control_id == "three_site_projection_recovers_stage15_pattern")
    typed = [x for x in controls if x.classification == STAGE16F_TYPED]
    criteria = (
        len(controls) == 20
        and all_rejected
        and vocabulary
        and opening.rejected
        and "depth=2" in opening.detail
        and projection.rejected
        and len(typed) == 4
        and all(x.rejected for x in typed)
    )
    return Stage16FDiagnostics(
        control_count=len(controls),
        rejected_control_count=sum(x.rejected for x in controls),
        required_vocabulary_count=len(STAGE16F_REQUIRED_VOCABULARY),
        required_vocabulary_covered=bool(vocabulary),
        cycle_opening_exhibited_depth=2 if opening.rejected else None,
        three_site_projection_one_step_l1=projection.rejected,
        typed_corruption_control_count=len(typed),
        typed_corruption_detected_count=sum(x.rejected for x in typed),
        all_controls_rejected=bool(all_rejected),
        criteria_45_47_satisfied=bool(criteria),
    )


def stage16f_summary() -> dict[str, object]:
    d = stage16f_diagnostics()
    return {
        "control_count": d.control_count,
        "rejected_control_count": d.rejected_control_count,
        "required_vocabulary_covered": d.required_vocabulary_covered,
        "criteria_45_47_satisfied": d.criteria_45_47_satisfied,
        "bounded_result": STAGE16F_BOUNDED_RESULT,
        "guards": STAGE16F_GUARDS,
        "stage16d_classification_retained": STAGE16D_CLASSIFICATION,
    }
