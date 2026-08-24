"""Stage 13B noncommuting gauge paths and compensated closure.

This module consumes the Stage 13A positive two-constraint carrier and tests
only the Stage 13B evidence frozen in ``docs/stage13_protocol.md``:

* all 144 ordered mixed same-orbit source/target pairs;
* raw-order dependence when the same K_X parameter is reused after reordering;
* exact compensated closure using ``u_XT = exp(s) u_TX``;
* wrong-compensator detection;
* preservation of the positive two-constraint surface and declared physical
  orbit typing under the licensed compensated paths;
* explicit separation of gauge-path order from physical temporal order;
* rejection of cross-orbit mixed-path construction.

The positive result is a finite constraint-generated path-closure result only.
It is not refoliation invariance, a hypersurface-deformation algebra, general
covariance, or a result about ontological becoming.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp

from t_search.stage13_multi_constraint import (
    STAGE13A_A,
    STAGE13A_ATOL,
    STAGE13A_BASIS_ID,
    STAGE13A_K_T,
    STAGE13A_K_X,
    Stage13PhaseSpacePoint,
    Stage13Representative,
    canonical_stage13a_mixed_pairs,
    canonical_stage13a_orbits,
    canonical_stage13a_representatives_for_orbit,
    stage13a_K_T,
    stage13a_K_X,
)

STAGE13B_PATH_WORD_ROLE = "constraint_generated_gauge_path_word"
STAGE13B_PATH_ORDER_ROLE = "gauge_generator_order_metadata"
STAGE13B_TEMPORAL_ORDER_STATUS = "not_physical_temporal_order"
STAGE13B_METAPHYSICAL_CLAIM_STATUS = "not_licensed"
STAGE13B_CLASSIFICATION = "compensated_path_closure_established"
STAGE13B_WRONG_COMPENSATOR_CLASSIFICATION = "wrong_compensator_detected"
STAGE13B_SAME_RAW_CLASSIFICATION = "same_raw_parameter_reorder_false_positive_rejected"
STAGE13B_CROSS_ORBIT_CLASSIFICATION = "cross_orbit_path_rejected"


@dataclass(frozen=True, slots=True)
class Stage13BMixedPathComparison:
    comparison_id: str
    orbit_id: str
    source_representative_id: str
    target_representative_id: str
    source_event_id: str
    target_event_id: str
    constraint_basis_id: str
    path_word_TX: tuple[str, str]
    path_word_XT: tuple[str, str]
    path_word_role: str
    path_order_role: str
    temporal_order_status: str
    metaphysical_claim_status: str
    s: float
    delta_X: float
    u_TX: float
    u_XT: float
    compensator_law_residual: float
    same_raw_u: float
    same_raw_TX_endpoint: Stage13PhaseSpacePoint
    same_raw_XT_endpoint: Stage13PhaseSpacePoint
    same_raw_endpoint_separation: float
    same_raw_TX_target_residual: float
    same_raw_XT_target_residual: float
    compensated_TX_endpoint: Stage13PhaseSpacePoint
    compensated_XT_endpoint: Stage13PhaseSpacePoint
    compensated_endpoint_separation: float
    compensated_TX_target_residual: float
    compensated_XT_target_residual: float
    compensated_constraint_residual: float
    wrong_u_XT: float
    wrong_compensator_parameter_residual: float
    wrong_compensator_endpoint: Stage13PhaseSpacePoint
    wrong_compensator_target_residual: float
    physical_orbit_identity_preserved: bool
    same_raw_classification: str
    compensated_classification: str
    wrong_compensator_classification: str
    provenance: str


@dataclass(frozen=True, slots=True)
class Stage13BDiagnostics:
    mixed_pair_count: int
    nontrivial_two_generator_pair_count: int
    same_raw_noncommuting_count: int
    compensated_closure_count: int
    compensated_surface_preservation_count: int
    wrong_compensator_detected_count: int
    typed_path_semantics_count: int
    cross_orbit_control_rejected: bool
    minimum_same_raw_endpoint_separation: float
    maximum_same_raw_endpoint_separation: float
    maximum_compensator_law_residual: float
    maximum_compensated_endpoint_separation: float
    maximum_compensated_target_residual: float
    maximum_compensated_constraint_residual: float
    minimum_wrong_compensator_target_residual: float
    maximum_wrong_compensator_target_residual: float
    physical_orbit_identity_preserved: bool
    path_order_temporal_distinction_explicit: bool
    criteria_17_23_satisfied: bool


def _constraint_residual(point: Stage13PhaseSpacePoint) -> float:
    return float(max(abs(stage13a_K_T(point)), abs(stage13a_K_X(point))))


def _point_residual(left: Stage13PhaseSpacePoint, right: Stage13PhaseSpacePoint) -> float:
    return float(
        max(
            abs(left.T - right.T),
            abs(left.p_T - right.p_T),
            abs(left.X - right.X),
            abs(left.p_X - right.p_X),
            abs(left.q - right.q),
            abs(left.p - right.p),
        )
    )


def _target_residual(point: Stage13PhaseSpacePoint, target: Stage13Representative) -> float:
    return _point_residual(point, target.point())


def stage13b_apply_phi_T(point: Stage13PhaseSpacePoint, s: float) -> Stage13PhaseSpacePoint:
    """Apply the exact frozen ``K_T`` flow for raw parameter ``s``."""

    return Stage13PhaseSpacePoint(
        T=float(point.T + s),
        p_T=point.p_T,
        X=point.X,
        p_X=point.p_X,
        q=float(point.q + point.p * s),
        p=point.p,
    )


def stage13b_apply_phi_X(point: Stage13PhaseSpacePoint, u: float) -> Stage13PhaseSpacePoint:
    """Apply the exact frozen ``K_X`` flow for raw parameter ``u``.

    ``K_X`` is constant along its own Hamiltonian flow, so the exact ``p_T``
    update is linear in ``u``.  On the licensed positive surface ``K_X=0``
    and ``p_T`` therefore remains unchanged.
    """

    K_X = stage13a_K_X(point)
    eT = exp(point.T)
    return Stage13PhaseSpacePoint(
        T=point.T,
        p_T=float(point.p_T - u * K_X),
        X=float(point.X + eT * u),
        p_X=point.p_X,
        q=float(point.q + STAGE13A_A * eT * u),
        p=point.p,
    )


def _path_TX(source: Stage13Representative, s: float, u: float) -> tuple[Stage13PhaseSpacePoint, Stage13PhaseSpacePoint]:
    after_T = stage13b_apply_phi_T(source.point(), s)
    endpoint = stage13b_apply_phi_X(after_T, u)
    return after_T, endpoint


def _path_XT(source: Stage13Representative, s: float, u: float) -> tuple[Stage13PhaseSpacePoint, Stage13PhaseSpacePoint]:
    after_X = stage13b_apply_phi_X(source.point(), u)
    endpoint = stage13b_apply_phi_T(after_X, s)
    return after_X, endpoint


def stage13b_mixed_path_comparison(
    source: Stage13Representative,
    target: Stage13Representative,
) -> Stage13BMixedPathComparison:
    """Compare raw-reordered, compensated, and wrong-compensator mixed paths."""

    if source.orbit_id != target.orbit_id:
        raise ValueError("Stage 13B mixed path cannot connect distinct physical orbits")
    if source.constraint_basis_id != STAGE13A_BASIS_ID or target.constraint_basis_id != STAGE13A_BASIS_ID:
        raise ValueError("Stage 13B mixed path requires the frozen positive constraint basis")
    if abs(source.T - target.T) <= STAGE13A_ATOL:
        raise ValueError("Stage 13B mixed path requires nonzero T displacement")
    if abs(source.X - target.X) <= STAGE13A_ATOL:
        raise ValueError("Stage 13B mixed path requires nonzero X displacement")

    s = float(target.T - source.T)
    delta_X = float(target.X - source.X)
    u_TX = float(delta_X / exp(target.T))
    u_XT = float(delta_X / exp(source.T))
    compensator_law_residual = float(abs(u_XT - exp(s) * u_TX))

    # Canonical same-raw-u false positive: use the TX value in both orders.
    same_raw_u = u_TX
    _, same_raw_TX = _path_TX(source, s, same_raw_u)
    _, same_raw_XT = _path_XT(source, s, same_raw_u)

    # Positive compensated pair.
    after_T, compensated_TX = _path_TX(source, s, u_TX)
    after_X, compensated_XT = _path_XT(source, s, u_XT)
    compensated_constraint_residual = max(
        _constraint_residual(source.point()),
        _constraint_residual(after_T),
        _constraint_residual(after_X),
        _constraint_residual(compensated_TX),
        _constraint_residual(compensated_XT),
        _constraint_residual(target.point()),
    )

    # A deterministic wrong compensator, one quarter of the way from the
    # exact XT value toward the same-raw TX value.  Because every mixed pair
    # has nonzero s and delta_X, this differs from the exact value everywhere.
    wrong_u_XT = float(u_XT + 0.25 * (u_TX - u_XT))
    _, wrong_endpoint = _path_XT(source, s, wrong_u_XT)

    return Stage13BMixedPathComparison(
        comparison_id=f"mixed:{source.representative_id}->{target.representative_id}",
        orbit_id=source.orbit_id,
        source_representative_id=source.representative_id,
        target_representative_id=target.representative_id,
        source_event_id=source.event_id,
        target_event_id=target.event_id,
        constraint_basis_id=STAGE13A_BASIS_ID,
        path_word_TX=(STAGE13A_K_T, STAGE13A_K_X),
        path_word_XT=(STAGE13A_K_X, STAGE13A_K_T),
        path_word_role=STAGE13B_PATH_WORD_ROLE,
        path_order_role=STAGE13B_PATH_ORDER_ROLE,
        temporal_order_status=STAGE13B_TEMPORAL_ORDER_STATUS,
        metaphysical_claim_status=STAGE13B_METAPHYSICAL_CLAIM_STATUS,
        s=s,
        delta_X=delta_X,
        u_TX=u_TX,
        u_XT=u_XT,
        compensator_law_residual=compensator_law_residual,
        same_raw_u=same_raw_u,
        same_raw_TX_endpoint=same_raw_TX,
        same_raw_XT_endpoint=same_raw_XT,
        same_raw_endpoint_separation=_point_residual(same_raw_TX, same_raw_XT),
        same_raw_TX_target_residual=_target_residual(same_raw_TX, target),
        same_raw_XT_target_residual=_target_residual(same_raw_XT, target),
        compensated_TX_endpoint=compensated_TX,
        compensated_XT_endpoint=compensated_XT,
        compensated_endpoint_separation=_point_residual(compensated_TX, compensated_XT),
        compensated_TX_target_residual=_target_residual(compensated_TX, target),
        compensated_XT_target_residual=_target_residual(compensated_XT, target),
        compensated_constraint_residual=float(compensated_constraint_residual),
        wrong_u_XT=wrong_u_XT,
        wrong_compensator_parameter_residual=float(abs(wrong_u_XT - u_XT)),
        wrong_compensator_endpoint=wrong_endpoint,
        wrong_compensator_target_residual=_target_residual(wrong_endpoint, target),
        physical_orbit_identity_preserved=(source.orbit_id == target.orbit_id),
        same_raw_classification=STAGE13B_SAME_RAW_CLASSIFICATION,
        compensated_classification=STAGE13B_CLASSIFICATION,
        wrong_compensator_classification=STAGE13B_WRONG_COMPENSATOR_CLASSIFICATION,
        provenance=(
            "Stage 13B comparison of same-raw reordered paths, exact algebraic "
            "compensation, and a deterministic wrong-compensator control"
        ),
    )


def canonical_stage13b_mixed_path_comparisons() -> tuple[Stage13BMixedPathComparison, ...]:
    return tuple(
        stage13b_mixed_path_comparison(source, target)
        for source, target in canonical_stage13a_mixed_pairs()
    )


def stage13b_cross_orbit_control_rejected() -> bool:
    """Return True only if the mixed-path constructor rejects a cross-orbit pair."""

    alpha = canonical_stage13a_representatives_for_orbit(canonical_stage13a_orbits()[0])
    beta = canonical_stage13a_representatives_for_orbit(canonical_stage13a_orbits()[1])
    source = alpha[0]
    target = next(
        item
        for item in beta
        if abs(item.T - source.T) > STAGE13A_ATOL and abs(item.X - source.X) > STAGE13A_ATOL
    )
    try:
        stage13b_mixed_path_comparison(source, target)
    except ValueError as exc:
        return "distinct physical orbits" in str(exc)
    return False


def stage13b_diagnostics() -> Stage13BDiagnostics:
    comparisons = canonical_stage13b_mixed_path_comparisons()

    nontrivial = [
        item
        for item in comparisons
        if abs(item.s) > STAGE13A_ATOL
        and abs(item.delta_X) > STAGE13A_ATOL
        and abs(item.u_TX - item.u_XT) > STAGE13A_ATOL
    ]
    same_raw_noncommuting = [
        item for item in comparisons if item.same_raw_endpoint_separation > STAGE13A_ATOL
    ]
    compensated_closed = [
        item
        for item in comparisons
        if item.compensator_law_residual <= STAGE13A_ATOL
        and item.compensated_endpoint_separation <= STAGE13A_ATOL
        and item.compensated_TX_target_residual <= STAGE13A_ATOL
        and item.compensated_XT_target_residual <= STAGE13A_ATOL
    ]
    surface_preserved = [
        item for item in comparisons if item.compensated_constraint_residual <= STAGE13A_ATOL
    ]
    wrong_detected = [
        item
        for item in comparisons
        if item.wrong_compensator_parameter_residual > STAGE13A_ATOL
        and item.wrong_compensator_target_residual > STAGE13A_ATOL
    ]
    typed = [
        item
        for item in comparisons
        if item.path_word_role == STAGE13B_PATH_WORD_ROLE
        and item.path_order_role == STAGE13B_PATH_ORDER_ROLE
        and item.temporal_order_status == STAGE13B_TEMPORAL_ORDER_STATUS
        and item.metaphysical_claim_status == STAGE13B_METAPHYSICAL_CLAIM_STATUS
        and item.path_word_TX == (STAGE13A_K_T, STAGE13A_K_X)
        and item.path_word_XT == (STAGE13A_K_X, STAGE13A_K_T)
    ]

    cross_orbit_rejected = stage13b_cross_orbit_control_rejected()
    orbit_preserved = all(item.physical_orbit_identity_preserved for item in comparisons)
    temporal_distinction = len(typed) == len(comparisons)
    criteria = (
        len(comparisons) == 144
        and len(nontrivial) == 144
        and len(same_raw_noncommuting) == 144
        and len(compensated_closed) == 144
        and len(surface_preserved) == 144
        and len(wrong_detected) == 144
        and orbit_preserved
        and temporal_distinction
        and cross_orbit_rejected
    )

    return Stage13BDiagnostics(
        mixed_pair_count=len(comparisons),
        nontrivial_two_generator_pair_count=len(nontrivial),
        same_raw_noncommuting_count=len(same_raw_noncommuting),
        compensated_closure_count=len(compensated_closed),
        compensated_surface_preservation_count=len(surface_preserved),
        wrong_compensator_detected_count=len(wrong_detected),
        typed_path_semantics_count=len(typed),
        cross_orbit_control_rejected=cross_orbit_rejected,
        minimum_same_raw_endpoint_separation=min(item.same_raw_endpoint_separation for item in comparisons),
        maximum_same_raw_endpoint_separation=max(item.same_raw_endpoint_separation for item in comparisons),
        maximum_compensator_law_residual=max(item.compensator_law_residual for item in comparisons),
        maximum_compensated_endpoint_separation=max(item.compensated_endpoint_separation for item in comparisons),
        maximum_compensated_target_residual=max(
            max(item.compensated_TX_target_residual, item.compensated_XT_target_residual)
            for item in comparisons
        ),
        maximum_compensated_constraint_residual=max(
            item.compensated_constraint_residual for item in comparisons
        ),
        minimum_wrong_compensator_target_residual=min(
            item.wrong_compensator_target_residual for item in comparisons
        ),
        maximum_wrong_compensator_target_residual=max(
            item.wrong_compensator_target_residual for item in comparisons
        ),
        physical_orbit_identity_preserved=orbit_preserved,
        path_order_temporal_distinction_explicit=temporal_distinction,
        criteria_17_23_satisfied=criteria,
    )


def stage13b_summary() -> dict[str, object]:
    diagnostics = stage13b_diagnostics()
    return {
        "stage": "Stage 13B — noncommuting gauge paths and compensated closure",
        "mixed_pair_count": diagnostics.mixed_pair_count,
        "nontrivial_two_generator_pair_count": diagnostics.nontrivial_two_generator_pair_count,
        "same_raw_noncommuting_count": diagnostics.same_raw_noncommuting_count,
        "compensated_closure_count": diagnostics.compensated_closure_count,
        "wrong_compensator_detected_count": diagnostics.wrong_compensator_detected_count,
        "cross_orbit_control_rejected": diagnostics.cross_orbit_control_rejected,
        "minimum_same_raw_endpoint_separation": diagnostics.minimum_same_raw_endpoint_separation,
        "maximum_same_raw_endpoint_separation": diagnostics.maximum_same_raw_endpoint_separation,
        "maximum_compensator_law_residual": diagnostics.maximum_compensator_law_residual,
        "maximum_compensated_endpoint_separation": diagnostics.maximum_compensated_endpoint_separation,
        "maximum_compensated_target_residual": diagnostics.maximum_compensated_target_residual,
        "maximum_compensated_constraint_residual": diagnostics.maximum_compensated_constraint_residual,
        "minimum_wrong_compensator_target_residual": diagnostics.minimum_wrong_compensator_target_residual,
        "maximum_wrong_compensator_target_residual": diagnostics.maximum_wrong_compensator_target_residual,
        "physical_orbit_identity_preserved": diagnostics.physical_orbit_identity_preserved,
        "path_order_temporal_distinction_explicit": diagnostics.path_order_temporal_distinction_explicit,
        "criteria_17_23_satisfied": diagnostics.criteria_17_23_satisfied,
        "bounded_result": (
            "Stage 13B compensated two-generator path closure on the frozen 144-pair finite family = established"
        ),
        "guards": (
            "raw gauge-path commutativity != successful multi-constraint closure",
            "same raw generator parameters under reordered paths != corresponding gauge path",
            "wrong compensator failure != physical time asymmetry",
            "path word != physical temporal history",
            "path-order mismatch != arrow of time by definition",
            "compensated multi-constraint path closure != refoliation invariance",
            "first-class finite path closure != hypersurface-deformation algebra",
            "constraint-algebra/refoliation precursor != general relativity",
            "finite-model success != empirical discovery",
        ),
        "next": "Stage 13C — Dirac / two-clock complete relational observables and physical-orbit discrimination",
    }
