"""Stage 15F locality-breaking, anomaly, and false-positive controls.

This stage is destructive by design.  It does not add a new positive carrier.
Instead it perturbs one frozen Stage 15 assumption at a time and checks that
the corresponding positive claim is no longer silently accepted.

The controls cover structure-function removal, graph/site disconnection,
locality-breaking and singular basis maps, smearing/Jacobi corruption,
cross-orbit false paths, incomplete relational observables, typed O/P/R/V
corruption, and the known distance-2 seed reconstruction.

Passing a negative control means that the declared validator rejects the
corrupted construction.  It is not evidence for general relativity,
refoliation invariance, causal locality, or any metaphysical conclusion.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from functools import lru_cache

import numpy as np

from .stage15_basis import (
    STAGE15D_KNOWN_SEED_ID,
    STAGE15D_L1_WITNESS_ID,
    STAGE15D_LFINITE,
    STAGE15D_NONLOCAL,
    Stage15DBasisCandidate,
    canonical_stage15d_candidates,
    stage15d_locality_audit,
    stage15d_matrix_and_derivatives,
)
from .stage15_local import (
    STAGE15A_ATOL,
    STAGE15A_GENERATOR_SUPPORTS,
    STAGE15A_SMEARING_PAIRS,
    canonical_stage15a_off_surface_probes,
    canonical_stage15a_representatives,
    stage15a_constraint_gradients,
    stage15a_jacobi_residual,
    stage15a_poisson_pair,
    stage15a_smeared_direct,
)
from .stage15_measurement import (
    canonical_stage15e_architectures,
    stage15e_architecture_for_representative,
    stage15e_quotient_projection,
    stage15e_validate_architecture,
)
from .stage15_relational import (
    stage15c_cross_orbit_arrow_audit,
    stage15c_omitted_clock_group_spreads,
)

STAGE15F_STRUCTURE_REMOVED = "structure_function_removed_control_rejected"
STAGE15F_DISCONNECTED = "disconnected_site_false_positive_rejected"
STAGE15F_SUPPORT_EXPANSION = "support_expansion_detected"
STAGE15F_DISTANCE2 = "distance2_basis_nonlocal_detected"
STAGE15F_SINGULAR = "singular_basis_map_rejected"
STAGE15F_SMEARING = "smearing_antisymmetry_corruption_detected"
STAGE15F_ANOMALY = "constraint_algebra_anomaly_detected"
STAGE15F_CROSS_ORBIT = "cross_orbit_false_positive_rejected"
STAGE15F_INCOMPLETE_RELATIONAL = "relational_observable_incomplete"
STAGE15F_REP_PAYLOAD = "representative_dependent_payload_corruption_detected"
STAGE15F_PATH_PAYLOAD = "path_dependent_payload_corruption_detected"
STAGE15F_BASIS_PAYLOAD = "basis_dependent_payload_corruption_detected"

STAGE15F_REQUIRED_VOCABULARY = (
    STAGE15F_STRUCTURE_REMOVED,
    STAGE15F_DISCONNECTED,
    STAGE15F_SUPPORT_EXPANSION,
    STAGE15F_DISTANCE2,
    STAGE15F_SINGULAR,
    STAGE15F_SMEARING,
    STAGE15F_ANOMALY,
    STAGE15F_CROSS_ORBIT,
    STAGE15F_INCOMPLETE_RELATIONAL,
    STAGE15F_REP_PAYLOAD,
)

STAGE15F_GUARDS = (
    "negative-control rejection != proof of continuum correctness",
    "graph disconnection control != relativistic causal disconnection",
    "locality-breaking detection != physical causal locality",
    "constraint-algebra anomaly detection != quantum anomaly theorem",
    "cross-orbit rejection != ontological superselection",
    "incomplete relational rejection != ontological becoming",
    "typed corruption detection != ontological equivalence",
    "local Abelianization surviving controls != physical triviality",
    "known seed non-L1 classification != universal nonlocality of Abelianization",
    "spatially indexed constraint precursor != general relativity",
    "repository validation != new scientific evidence",
)

STAGE15F_BOUNDED_RESULT = (
    "Stage 15F frozen locality-breaking, anomaly, false-positive, relational, "
    "and typed-payload controls on the Stage 15 finite carrier = all declared "
    "controls rejected as intended"
)


@dataclass(frozen=True, slots=True)
class Stage15FControlResult:
    control_id: str
    classification: str
    rejected: bool
    witness_count: int
    violation_count: int
    max_signal: float
    detail: str


@dataclass(frozen=True, slots=True)
class Stage15FDiagnostics:
    control_count: int
    rejected_control_count: int
    required_vocabulary_count: int
    required_vocabulary_covered: bool
    structure_baseline_nonzero_count: int
    structure_removed_nonzero_count: int
    deleted_middle_generator_min_rank: int
    disconnected_path_rejected: bool
    locality_basis_control_count: int
    locality_basis_rejected_count: int
    smearing_corruption_probe_count: int
    smearing_corruption_detected_count: int
    max_smearing_antisymmetry_signal: float
    jacobi_anomaly_probe_count: int
    jacobi_anomaly_detected_count: int
    max_jacobi_anomaly_signal: float
    cross_orbit_rejected_count: int
    incomplete_relational_group_count: int
    incomplete_relational_rejected_count: int
    typed_corruption_control_count: int
    typed_corruption_detected_count: int
    known_seed_one_step_l1: bool
    known_seed_lfinite_depth: int | None
    all_controls_rejected: bool
    criteria_44_47_satisfied: bool


def _poisson_from_gradients(df: np.ndarray, dg: np.ndarray) -> float:
    return float(
        sum(
            df[q_index] * dg[p_index] - df[p_index] * dg[q_index]
            for q_index, p_index in ((0, 1), (2, 3), (4, 5), (6, 7))
        )
    )


def _fs(*values: int) -> frozenset[int]:
    return frozenset(values)


def _identity_columns() -> tuple[frozenset[int], frozenset[int], frozenset[int]]:
    return (_fs(0), _fs(1), _fs(2))


def _original_supports() -> tuple[frozenset[int], frozenset[int], frozenset[int]]:
    return tuple(STAGE15A_GENERATOR_SUPPORTS[index] for index in range(3))


def _structure_function_removed_control() -> Stage15FControlResult:
    probes = canonical_stage15a_off_surface_probes()
    baseline_nonzero = sum(
        abs(stage15a_poisson_pair(point, 0, 1)) > STAGE15A_ATOL for point in probes
    )
    corrupted_nonzero = 0
    max_corrupted = 0.0
    for point in probes:
        gradients = stage15a_constraint_gradients(point, kappa=0.0)
        bracket = abs(_poisson_from_gradients(gradients[0], gradients[1]))
        max_corrupted = max(max_corrupted, bracket)
        corrupted_nonzero += bracket > STAGE15A_ATOL
    rejected = baseline_nonzero > 0 and corrupted_nonzero == 0
    return Stage15FControlResult(
        "kappa_zero_structure_function_removal",
        STAGE15F_STRUCTURE_REMOVED,
        bool(rejected),
        len(probes),
        int(baseline_nonzero),
        float(max_corrupted),
        f"baseline_nonzero={baseline_nonzero}; kappa0_nonzero={corrupted_nonzero}",
    )


def _site_deletion_rank_control() -> Stage15FControlResult:
    ranks = []
    for representative in canonical_stage15a_representatives():
        gradients = stage15a_constraint_gradients(representative.point())
        ranks.append(int(np.linalg.matrix_rank(gradients[[0, 2], :])))
    minimum = min(ranks)
    return Stage15FControlResult(
        "delete_middle_site_generator_rank",
        STAGE15F_DISCONNECTED,
        minimum < 3,
        len(ranks),
        sum(rank < 3 for rank in ranks),
        float(minimum),
        "removing the middle labelled generator leaves only two independent tested directions",
    )


def _connected_after_site_deletion(deleted_site: int, source: int, target: int) -> bool:
    vertices = {0, 1, 2} - {deleted_site}
    if source not in vertices or target not in vertices:
        return False
    edges = {(0, 1), (1, 2)}
    adjacency = {vertex: set() for vertex in vertices}
    for left, right in edges:
        if left in vertices and right in vertices:
            adjacency[left].add(right)
            adjacency[right].add(left)
    frontier = [source]
    seen = {source}
    while frontier:
        current = frontier.pop()
        if current == target:
            return True
        for neighbour in adjacency[current]:
            if neighbour not in seen:
                seen.add(neighbour)
                frontier.append(neighbour)
    return False


def _disconnected_false_path_control() -> Stage15FControlResult:
    connected = _connected_after_site_deletion(1, 0, 2)
    return Stage15FControlResult(
        "deleted_site_0_to_2_false_path",
        STAGE15F_DISCONNECTED,
        not connected,
        1,
        int(not connected),
        1.0 if not connected else 0.0,
        "after deleting site 1, sites 0 and 2 have no graph path and cannot be licensed as a nearest-neighbour route",
    )


def _support_expansion_control() -> Stage15FControlResult:
    candidate = next(
        item
        for item in canonical_stage15d_candidates()
        if item.candidate_id == "head_shear_support_expansion_control"
    )
    audit = stage15d_locality_audit(candidate)
    rejected = audit.locality_class == STAGE15D_NONLOCAL and not audit.one_step_l1
    return Stage15FControlResult(
        "support_expanding_generator",
        STAGE15F_SUPPORT_EXPANSION,
        bool(rejected),
        1,
        int(rejected),
        1.0 if rejected else 0.0,
        ";".join(audit.failure_reasons),
    )


def _distance2_coefficient_candidate() -> Stage15DBasisCandidate:
    columns = _identity_columns()
    supports = _original_supports()
    return Stage15DBasisCandidate(
        candidate_id="distance2_coefficient_dependency_control",
        family_id="stage15f_locality_corruption",
        transform_kind="stage15f_distance2_metadata",
        parameter=None,
        diagonal=None,
        forward_columns=columns,
        inverse_columns=columns,
        forward_coefficient_sites=(_fs(2), _fs(), _fs()),
        inverse_coefficient_sites=(_fs(2), _fs(), _fs()),
        forward_simplified_supports=supports,
        inverse_simplified_supports=supports,
    )


def _distance2_coefficient_control() -> Stage15FControlResult:
    audit = stage15d_locality_audit(_distance2_coefficient_candidate())
    rejected = audit.locality_class == STAGE15D_NONLOCAL and not audit.one_step_l1
    return Stage15FControlResult(
        "distance2_coefficient_in_alleged_L1",
        STAGE15F_DISTANCE2,
        bool(rejected),
        1,
        int(rejected),
        1.0 if rejected else 0.0,
        ";".join(audit.failure_reasons),
    )


def _singular_basis_candidate() -> Stage15DBasisCandidate:
    columns = _identity_columns()
    supports = _original_supports()
    empty = (_fs(), _fs(), _fs())
    return Stage15DBasisCandidate(
        candidate_id="singular_diagonal_basis_control",
        family_id="stage15f_singular_control",
        transform_kind="diag",
        parameter=None,
        diagonal=(1.0, 0.0, 1.0),
        forward_columns=columns,
        inverse_columns=columns,
        forward_coefficient_sites=empty,
        inverse_coefficient_sites=empty,
        forward_simplified_supports=supports,
        inverse_simplified_supports=supports,
    )


def _singular_basis_control() -> Stage15FControlResult:
    candidate = _singular_basis_candidate()
    determinants = []
    for representative in canonical_stage15a_representatives():
        matrix, _ = stage15d_matrix_and_derivatives(candidate, representative.point())
        determinants.append(abs(float(np.linalg.det(matrix))))
    minimum = min(determinants)
    singular_count = sum(value <= STAGE15A_ATOL for value in determinants)
    return Stage15FControlResult(
        "singular_noninvertible_basis",
        STAGE15F_SINGULAR,
        singular_count == len(determinants),
        len(determinants),
        int(singular_count),
        float(minimum),
        "the map is L0-shaped in support bookkeeping but determinant zero, so invertibility rejects it",
    )


def _smearing_wrong_sign_control() -> Stage15FControlResult:
    residuals = []
    for point in canonical_stage15a_off_surface_probes():
        for N, M in STAGE15A_SMEARING_PAIRS:
            direct_nm = stage15a_smeared_direct(point, N, M)
            corrupted_reverse = direct_nm
            residuals.append(abs(direct_nm + corrupted_reverse))
    detected = sum(value > STAGE15A_ATOL for value in residuals)
    return Stage15FControlResult(
        "wrong_smearing_antisymmetry_sign",
        STAGE15F_SMEARING,
        detected > 0,
        len(residuals),
        int(detected),
        float(max(residuals, default=0.0)),
        "reversed smearing bracket is deliberately assigned the same sign",
    )


def _jacobi_anomaly_control() -> Stage15FControlResult:
    epsilon = 0.125
    anomaly_gradient = np.zeros(8, dtype=float)
    anomaly_gradient[6] = epsilon
    residuals = []
    for point in canonical_stage15a_off_surface_probes():
        c2_gradient = stage15a_constraint_gradients(point)[2]
        corrupted = stage15a_jacobi_residual(point) + _poisson_from_gradients(
            anomaly_gradient, c2_gradient
        )
        residuals.append(abs(corrupted))
    detected = sum(value > STAGE15A_ATOL for value in residuals)
    return Stage15FControlResult(
        "jacobi_violating_epsilon_T2_anomaly",
        STAGE15F_ANOMALY,
        detected == len(residuals) and detected > 0,
        len(residuals),
        int(detected),
        float(max(residuals, default=0.0)),
        "adds epsilon*T2 to the {C0,C1} bracket; nesting with C2 leaves a nonzero Jacobi residual",
    )


def _cross_orbit_control() -> Stage15FControlResult:
    licensed, rejected = stage15c_cross_orbit_arrow_audit()
    return Stage15FControlResult(
        "cross_orbit_local_path_false_positive",
        STAGE15F_CROSS_ORBIT,
        licensed == 0 and rejected > 0,
        licensed + rejected,
        rejected,
        float(licensed),
        f"licensed={licensed}; rejected={rejected}",
    )


def _incomplete_relational_control() -> Stage15FControlResult:
    groups = stage15c_omitted_clock_group_spreads()
    rejected = sum(spread > STAGE15A_ATOL for *_prefix, spread in groups)
    return Stage15FControlResult(
        "one_clock_omitted_relational_expression",
        STAGE15F_INCOMPLETE_RELATIONAL,
        rejected == len(groups) and rejected > 0,
        len(groups),
        rejected,
        float(max(spread for *_prefix, spread in groups)),
        "every fixed-two-clock group retains dependence on the omitted raw clock",
    )


def _typed_corruption_controls() -> tuple[Stage15FControlResult, ...]:
    representatives = canonical_stage15a_representatives()
    base = canonical_stage15e_architectures()[0]
    baseline_projection = stage15e_quotient_projection(base)

    event = base.O.relational_events[0]
    corrupted_O = replace(
        base,
        O=replace(
            base.O,
            relational_events=(
                replace(event, q_value=float(event.q_value + 0.01)),
                *base.O.relational_events[1:],
            ),
        ),
    )

    corrupted_P = replace(
        base,
        P=replace(base.P, qext_ids=tuple(reversed(base.P.qext_ids))),
    )

    basis_architecture = stage15e_architecture_for_representative(
        representatives[0], candidate_id=STAGE15D_L1_WITNESS_ID
    )
    direction0 = basis_architecture.R.R_direction[0]
    corrupted_R = replace(
        basis_architecture,
        R=replace(
            basis_architecture.R,
            R_direction=(
                replace(direction0, record_score=float(direction0.record_score + 0.01)),
                *basis_architecture.R.R_direction[1:],
            ),
        ),
    )

    weights = list(base.V.V_weights)
    weights[0] += 0.01
    weights[1] -= 0.01
    corrupted_V = replace(base, V=replace(base.V, V_weights=tuple(weights)))

    controls = (
        (
            "representative_dependent_O_corruption",
            STAGE15F_REP_PAYLOAD,
            corrupted_O,
            baseline_projection,
        ),
        (
            "path_dependent_P_corruption",
            STAGE15F_PATH_PAYLOAD,
            corrupted_P,
            baseline_projection,
        ),
        (
            "basis_dependent_R_corruption",
            STAGE15F_BASIS_PAYLOAD,
            corrupted_R,
            stage15e_quotient_projection(basis_architecture),
        ),
        (
            "representative_dependent_V_corruption",
            STAGE15F_REP_PAYLOAD,
            corrupted_V,
            baseline_projection,
        ),
    )

    results = []
    for control_id, classification, corrupted, expected_projection in controls:
        valid, _ = stage15e_validate_architecture(corrupted)
        projection_changed = stage15e_quotient_projection(corrupted) != expected_projection
        detected = (not valid) and projection_changed
        results.append(
            Stage15FControlResult(
                control_id,
                classification,
                bool(detected),
                1,
                int(detected),
                1.0 if detected else 0.0,
                "illicit provenance-conditioned mutation changes quotient-level public content and fails architecture validation",
            )
        )
    return tuple(results)


def _known_seed_non_l1_control() -> Stage15FControlResult:
    candidate = next(
        item
        for item in canonical_stage15d_candidates()
        if item.candidate_id == STAGE15D_KNOWN_SEED_ID
    )
    audit = stage15d_locality_audit(candidate)
    rejected_as_l1 = (
        not audit.one_step_l1
        and audit.locality_class == STAGE15D_LFINITE
        and audit.lfinite_depth == 2
    )
    return Stage15FControlResult(
        "known_distance2_seed_not_silently_L1",
        STAGE15F_DISTANCE2,
        bool(rejected_as_l1),
        1,
        int(rejected_as_l1),
        float(audit.lfinite_depth or 0),
        "known seed reconstruction remains Lfinite depth 2 rather than one-step L1",
    )


@lru_cache(maxsize=1)
def canonical_stage15f_controls() -> tuple[Stage15FControlResult, ...]:
    return (
        _structure_function_removed_control(),
        _site_deletion_rank_control(),
        _disconnected_false_path_control(),
        _support_expansion_control(),
        _distance2_coefficient_control(),
        _singular_basis_control(),
        _smearing_wrong_sign_control(),
        _jacobi_anomaly_control(),
        _cross_orbit_control(),
        _incomplete_relational_control(),
        *_typed_corruption_controls(),
        _known_seed_non_l1_control(),
    )


@lru_cache(maxsize=1)
def stage15f_diagnostics() -> Stage15FDiagnostics:
    controls = canonical_stage15f_controls()
    by_id = {item.control_id: item for item in controls}

    structure = by_id["kappa_zero_structure_function_removal"]
    baseline_nonzero = int(structure.detail.split(";")[0].split("=")[1])
    removed_nonzero = int(structure.detail.split(";")[1].split("=")[1])

    deletion = by_id["delete_middle_site_generator_rank"]
    disconnected = by_id["deleted_site_0_to_2_false_path"]

    locality_ids = {
        "support_expanding_generator",
        "distance2_coefficient_in_alleged_L1",
        "singular_noninvertible_basis",
        "known_distance2_seed_not_silently_L1",
    }
    locality_controls = [item for item in controls if item.control_id in locality_ids]

    smearing = by_id["wrong_smearing_antisymmetry_sign"]
    jacobi = by_id["jacobi_violating_epsilon_T2_anomaly"]
    cross = by_id["cross_orbit_local_path_false_positive"]
    incomplete = by_id["one_clock_omitted_relational_expression"]

    typed_ids = {
        "representative_dependent_O_corruption",
        "path_dependent_P_corruption",
        "basis_dependent_R_corruption",
        "representative_dependent_V_corruption",
    }
    typed = [item for item in controls if item.control_id in typed_ids]

    seed_candidate = next(
        item
        for item in canonical_stage15d_candidates()
        if item.candidate_id == STAGE15D_KNOWN_SEED_ID
    )
    seed_audit = stage15d_locality_audit(seed_candidate)

    classifications = {item.classification for item in controls}
    vocabulary_covered = set(STAGE15F_REQUIRED_VOCABULARY) <= classifications
    all_rejected = all(item.rejected for item in controls)

    criteria = (
        len(controls) == 15
        and all_rejected
        and vocabulary_covered
        and baseline_nonzero > 0
        and removed_nonzero == 0
        and int(deletion.max_signal) == 2
        and disconnected.rejected
        and len(locality_controls) == 4
        and all(item.rejected for item in locality_controls)
        and smearing.violation_count > 0
        and jacobi.violation_count == jacobi.witness_count == 108
        and cross.violation_count == 8748
        and incomplete.violation_count == incomplete.witness_count == 108
        and len(typed) == 4
        and all(item.rejected for item in typed)
        and not seed_audit.one_step_l1
        and seed_audit.lfinite_depth == 2
    )

    return Stage15FDiagnostics(
        control_count=len(controls),
        rejected_control_count=sum(item.rejected for item in controls),
        required_vocabulary_count=len(STAGE15F_REQUIRED_VOCABULARY),
        required_vocabulary_covered=bool(vocabulary_covered),
        structure_baseline_nonzero_count=baseline_nonzero,
        structure_removed_nonzero_count=removed_nonzero,
        deleted_middle_generator_min_rank=int(deletion.max_signal),
        disconnected_path_rejected=disconnected.rejected,
        locality_basis_control_count=len(locality_controls),
        locality_basis_rejected_count=sum(item.rejected for item in locality_controls),
        smearing_corruption_probe_count=smearing.witness_count,
        smearing_corruption_detected_count=smearing.violation_count,
        max_smearing_antisymmetry_signal=smearing.max_signal,
        jacobi_anomaly_probe_count=jacobi.witness_count,
        jacobi_anomaly_detected_count=jacobi.violation_count,
        max_jacobi_anomaly_signal=jacobi.max_signal,
        cross_orbit_rejected_count=cross.violation_count,
        incomplete_relational_group_count=incomplete.witness_count,
        incomplete_relational_rejected_count=incomplete.violation_count,
        typed_corruption_control_count=len(typed),
        typed_corruption_detected_count=sum(item.rejected for item in typed),
        known_seed_one_step_l1=seed_audit.one_step_l1,
        known_seed_lfinite_depth=seed_audit.lfinite_depth,
        all_controls_rejected=bool(all_rejected),
        criteria_44_47_satisfied=bool(criteria),
    )


def stage15f_summary() -> dict[str, object]:
    diagnostics = stage15f_diagnostics()
    return {
        "control_count": diagnostics.control_count,
        "rejected_control_count": diagnostics.rejected_control_count,
        "required_vocabulary_covered": diagnostics.required_vocabulary_covered,
        "criteria_44_47_satisfied": diagnostics.criteria_44_47_satisfied,
        "bounded_result": STAGE15F_BOUNDED_RESULT,
        "guards": STAGE15F_GUARDS,
    }
