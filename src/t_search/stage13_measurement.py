"""Stage 13E O/P/R/V/Xi and future-measurement descent across compensated paths.

This stage lifts the inherited typed operational architecture onto every Stage 13
representative and the Stage 13D connectivity quotient.  Constraint-basis and
path-word provenance remain in Xi.  Public O/P/R/V, future-measurement,
weighted, posterior, and orbit-sensitive witness payloads are tested for
descent across the two exactly compensated Stage 13B path choices.

The result is finite and typed.  It is not refoliation invariance, general
covariance, general relativity, or a metaphysical result.
"""

from __future__ import annotations

from dataclasses import dataclass, fields, replace
from functools import lru_cache
from math import tanh

import numpy as np

from t_search.stage9_modal import FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_OTHER
from t_search.stage11_lift import Stage11OLayer, Stage11OEvent, Stage11PLayer, Stage11RLayer, Stage11VLayer
from t_search.stage11_parametrized import STAGE11A_IDENTITY
from t_search.stage12_measurement import (
    Stage12DQuotientArchitecture,
    Stage12DMeasurementDescentView,
    Stage12DWeightedDescentView,
    Stage12DPosteriorDescentView,
    canonical_stage12d_quotient_projections,
    canonical_stage12d_measurement_views,
    canonical_stage12d_weighted_views,
    canonical_stage12d_posterior_views,
    stage12d_controls,
)
from t_search.stage13_multi_constraint import (
    STAGE13A_ATOL,
    STAGE13A_BASIS_ID,
    STAGE13A_GAUGE_FLOW_TYPE,
    Stage13Representative,
    canonical_stage13a_orbits,
    canonical_stage13a_representatives,
)
from t_search.stage13_paths import (
    STAGE13B_PATH_WORD_ROLE,
    STAGE13B_PHI_T,
    STAGE13B_PHI_X,
    STAGE13B_TEMPORAL_ORDER_STATUS,
    STAGE13B_METAPHYSICAL_CLAIM_STATUS,
    canonical_stage13b_mixed_path_comparisons,
)
from t_search.stage13_relational import (
    stage13c_complete_relational_value,
    stage13c_reconstruct_dirac_from_point,
)
from t_search.stage13_gauge_atlas import (
    canonical_stage13d_quotient_classes,
    canonical_stage13d_compensated_descent_checks,
)

STAGE13E_ATOL = STAGE13A_ATOL
STAGE13E_REFERENCE_PARAMETERIZATION = STAGE11A_IDENTITY
STAGE13E_PATH_DESCENT_CLASSIFICATION = "compensated_path_operational_payloads_descend"
STAGE13E_TYPED_REJECTION = "typed_operational_context_rejected"
STAGE13E_WRONG_PATH_REJECTION = "wrong_compensated_path_rejected"
STAGE13E_NORMALIZATION_REJECTION = "misaligned_normalization_numerically_rejected"
STAGE13E_REPRESENTATIVE_CORRUPTION_REJECTED = "representative_dependent_payload_corruption_detected"
STAGE13E_METAPHYSICAL_CLAIM_STATUS = "not_licensed"
STAGE13E_PATH_PROVENANCE_SEMANTICS = (
    "constraint-basis, path-word, raw-parameter, compensator, and representative "
    "provenance is retained in Xi and omitted from quotient-level public content"
)
STAGE13E_ORBIT_WITNESS_SEMANTICS = (
    "declared bounded orbit-conditioned operational bridge from independently "
    "reconstructed Dirac and two-clock complete-relational data; diagnostic only, "
    "not a dynamical derivation of quantum measurement and not an empirical prediction"
)
STAGE13E_BOUNDED_RESULT = (
    "Stage 13E typed O/P/R/V/Xi and future-measurement descent across compensated "
    "path choices on the frozen finite family = established"
)
STAGE13E_CLOCK_PAIRS = (
    ("e1", -1.0, -1.0),
    ("e2", 1.0, 1.0),
)


@dataclass(frozen=True, slots=True)
class Stage13EXiLayer:
    parameterization_id: str
    orbit_id: str
    quotient_id: str
    representative_id: str
    constraint_basis_id: str
    generator_family_type: str
    path_word_role: str
    licensed_path_words: tuple[tuple[str, ...], ...]
    representative_T: float
    representative_X: float
    relational_clock_pairs: tuple[tuple[str, float, float], ...]
    event_correspondence: tuple[tuple[str, str], ...]
    continuation_class_correspondence: tuple[tuple[str, str], ...]
    outcome_correspondence: tuple[tuple[str, str], ...]
    lapse_semantics: str
    normalization_semantics: str
    path_provenance_semantics: str
    basis_provenance_semantics: str
    orbit_bridge_semantics: str


@dataclass(frozen=True, slots=True)
class Stage13ETypedArchitecture:
    orbit_id: str
    quotient_id: str
    representative_id: str
    O: Stage11OLayer
    P: Stage11PLayer
    R: Stage11RLayer
    V: Stage11VLayer
    Xi: Stage13EXiLayer


@dataclass(frozen=True, slots=True)
class Stage13EQuotientArchitecture:
    orbit_id: str
    quotient_id: str
    O: Stage11OLayer
    P: Stage11PLayer
    R: Stage11RLayer
    V: Stage11VLayer
    parameterization_id: str
    event_correspondence: tuple[tuple[str, str], ...]
    continuation_class_correspondence: tuple[tuple[str, str], ...]
    outcome_correspondence: tuple[tuple[str, str], ...]
    lapse_semantics: str
    normalization_semantics: str
    orbit_bridge_semantics: str


@dataclass(frozen=True, slots=True)
class Stage13EMeasurementView:
    orbit_id: str
    quotient_id: str
    representative_id: str
    continuation_id: str
    anchor_event_id: str
    target_event_id: str
    family_id: str
    internal_clock: str
    internal_clock_index: int
    outcome_ids: tuple[str, ...]
    normalization_semantics: str
    probabilities: tuple[tuple[str, float], ...]
    probability_sum_residual: float
    completeness_residual: float
    minimum_effect_eigenvalue: float
    minimum_normalization_eigenvalue: float
    normalization_denominator: float


@dataclass(frozen=True, slots=True)
class Stage13EWeightedView:
    orbit_id: str
    quotient_id: str
    representative_id: str
    continuation_ids: tuple[str, ...]
    continuation_weights: tuple[float, ...]
    predictive_density: tuple[complex, ...]
    directional_record_scores: tuple[float, ...]
    directional_accessibility_scores: tuple[float, ...]
    orientations: tuple[str, ...]
    next_outcomes: tuple[str, ...]
    next_probabilities: tuple[tuple[str, float], ...]


@dataclass(frozen=True, slots=True)
class Stage13EPosteriorView:
    orbit_id: str
    quotient_id: str
    representative_id: str
    observed_outcome: str
    epistemic_posterior_weights: tuple[float, ...]
    ontic_posterior_weights: tuple[float, ...]
    epistemic_selected_continuation_id: str
    ontic_no_selected_complete_continuation_datum: bool


@dataclass(frozen=True, slots=True)
class Stage13EOrbitSensitiveWitness:
    orbit_id: str
    quotient_id: str
    representative_id: str
    Q_D: float
    P_D: float
    target_tau: float
    target_chi: float
    relational_q_target: float
    bridge_score: float
    probabilities: tuple[tuple[str, float], ...]
    probability_sum_residual: float
    semantics: str


@dataclass(frozen=True, slots=True)
class Stage13EPathXi:
    comparison_id: str
    constraint_basis_id: str
    source_representative_id: str
    target_representative_id: str
    path_word: tuple[str, str]
    path_word_role: str
    s: float
    u: float
    compensator_provenance: str
    temporal_order_status: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage13ECompensatedOperationalDescentCheck:
    comparison_id: str
    quotient_id: str
    source_representative_id: str
    target_representative_id: str
    path_Xi_TX: Stage13EPathXi
    path_Xi_XT: Stage13EPathXi
    path_provenance_distinct: bool
    public_architecture_residual: float
    measurement_probability_residual: float
    weighted_probability_residual: float
    posterior_residual: float
    witness_residual: float
    measurement_evaluation_count: int
    classification: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage13EControl:
    control_id: str
    classification: str
    rejected: bool
    numerical_witness_residual: float
    rejection_reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Stage13EDiagnostics:
    physical_orbit_count: int
    representative_count: int
    quotient_class_count: int
    architecture_view_count: int
    distinct_quotient_architecture_count: int
    measurement_view_count: int
    probability_evaluation_count: int
    weighted_view_count: int
    posterior_view_count: int
    orbit_witness_count: int
    distinct_orbit_witness_count: int
    compensated_path_check_count: int
    path_xi_view_count: int
    compensated_measurement_evaluation_count: int
    max_same_orbit_architecture_residual: float
    max_same_orbit_measurement_probability_residual: float
    max_same_orbit_weighted_probability_residual: float
    max_same_orbit_posterior_residual: float
    max_same_orbit_witness_residual: float
    minimum_cross_orbit_witness_separation: float
    max_compensated_public_architecture_residual: float
    max_compensated_measurement_probability_residual: float
    max_compensated_weighted_probability_residual: float
    max_compensated_posterior_residual: float
    max_compensated_witness_residual: float
    max_probability_sum_residual: float
    max_measurement_completeness_residual: float
    minimum_effect_eigenvalue: float
    minimum_normalization_eigenvalue: float
    minimum_normalization_denominator: float
    public_path_basis_provenance_absent: bool
    path_xi_provenance_explicit: bool
    control_count: int
    rejected_control_count: int
    criteria_39_43_satisfied: bool


def _representative_lookup() -> dict[str, Stage13Representative]:
    return {item.representative_id: item for item in canonical_stage13a_representatives()}


@lru_cache(maxsize=1)
def _quotient_classes():
    return canonical_stage13d_quotient_classes()


def _quotient_by_representative():
    result = {}
    for quotient in _quotient_classes():
        for representative_id in quotient.representative_ids:
            if representative_id in result:
                raise ValueError("Stage 13E representative occurs in multiple quotient classes")
            result[representative_id] = quotient
    if set(result) != set(_representative_lookup()):
        raise ValueError("Stage 13E quotient lookup does not cover all Stage 13 representatives")
    return result


@lru_cache(maxsize=1)
def _stage12_public_architecture_by_orbit() -> dict[str, Stage12DQuotientArchitecture]:
    result = {}
    for orbit in canonical_stage13a_orbits():
        subset = tuple(
            item for item in canonical_stage12d_quotient_projections()
            if item.orbit_id == orbit.orbit_id
        )
        if not subset or len(set(subset)) != 1:
            raise ValueError("Stage 13E requires one representative-independent Stage 12D public architecture per orbit")
        result[orbit.orbit_id] = subset[0]
    return result


@lru_cache(maxsize=1)
def _stage12_measurement_by_orbit_continuation() -> dict[tuple[str, str], Stage12DMeasurementDescentView]:
    result = {}
    for item in canonical_stage12d_measurement_views():
        key = (item.orbit_id, item.continuation_id)
        if key not in result:
            result[key] = item
        elif result[key].probabilities != item.probabilities:
            raise ValueError("Stage 12D inherited measurement payload is representative-dependent")
    return result


@lru_cache(maxsize=1)
def _stage12_weighted_by_orbit() -> dict[str, Stage12DWeightedDescentView]:
    result = {}
    for item in canonical_stage12d_weighted_views():
        result.setdefault(item.orbit_id, item)
    return result


@lru_cache(maxsize=1)
def _stage12_posterior_by_orbit() -> dict[str, Stage12DPosteriorDescentView]:
    result = {}
    for item in canonical_stage12d_posterior_views():
        result.setdefault(item.orbit_id, item)
    return result


def _orbit_relational_events(representative: Stage13Representative) -> tuple[Stage11OEvent, ...]:
    Q_D, P_D = stage13c_reconstruct_dirac_from_point(representative.point())
    events = []
    for stage10_event, tau, chi in STAGE13E_CLOCK_PAIRS:
        role = "prediction_anchor" if stage10_event == "e1" else "measurement_target"
        events.append(
            Stage11OEvent(
                role=role,
                stage10_event=stage10_event,
                physical_event_id=f"{representative.orbit_id}:complete_relational:{stage10_event}",
                clock_value=float(tau),
                q_value=stage13c_complete_relational_value(Q_D, P_D, tau, chi),
            )
        )
    return tuple(events)


def stage13e_architecture_for_representative(representative: Stage13Representative) -> Stage13ETypedArchitecture:
    quotient = _quotient_by_representative()[representative.representative_id]
    base = _stage12_public_architecture_by_orbit()[representative.orbit_id]
    O = replace(base.O, relational_events=_orbit_relational_events(representative))
    events = {item.stage10_event: item for item in O.relational_events}
    event_correspondence = tuple(
        (event_id, events[event_id].physical_event_id) for event_id, _, _ in STAGE13E_CLOCK_PAIRS
    )
    Xi = Stage13EXiLayer(
        parameterization_id=STAGE13E_REFERENCE_PARAMETERIZATION,
        orbit_id=representative.orbit_id,
        quotient_id=quotient.quotient_id,
        representative_id=representative.representative_id,
        constraint_basis_id=representative.constraint_basis_id,
        generator_family_type=representative.generator_family_type,
        path_word_role=STAGE13B_PATH_WORD_ROLE,
        licensed_path_words=((STAGE13B_PHI_T, STAGE13B_PHI_X), (STAGE13B_PHI_X, STAGE13B_PHI_T)),
        representative_T=float(representative.T),
        representative_X=float(representative.X),
        relational_clock_pairs=STAGE13E_CLOCK_PAIRS,
        event_correspondence=event_correspondence,
        continuation_class_correspondence=base.continuation_class_correspondence,
        outcome_correspondence=base.outcome_correspondence,
        lapse_semantics=base.lapse_semantics,
        normalization_semantics=base.normalization_semantics,
        path_provenance_semantics=STAGE13E_PATH_PROVENANCE_SEMANTICS,
        basis_provenance_semantics="constraint-basis identity is representation provenance retained in Xi",
        orbit_bridge_semantics=STAGE13E_ORBIT_WITNESS_SEMANTICS,
    )
    return Stage13ETypedArchitecture(
        orbit_id=representative.orbit_id,
        quotient_id=quotient.quotient_id,
        representative_id=representative.representative_id,
        O=O,
        P=base.P,
        R=base.R,
        V=base.V,
        Xi=Xi,
    )


@lru_cache(maxsize=1)
def canonical_stage13e_architectures() -> tuple[Stage13ETypedArchitecture, ...]:
    return tuple(stage13e_architecture_for_representative(item) for item in canonical_stage13a_representatives())


def stage13e_validate_architecture(architecture: Stage13ETypedArchitecture) -> tuple[bool, tuple[str, ...]]:
    representative = _representative_lookup().get(architecture.representative_id)
    if representative is None:
        return False, ("representative_identity",)
    expected = stage13e_architecture_for_representative(representative)
    checks = {
        "orbit_correspondence": architecture.orbit_id == expected.orbit_id,
        "quotient_correspondence": architecture.quotient_id == expected.quotient_id,
        "O": architecture.O == expected.O,
        "P": architecture.P == expected.P,
        "R": architecture.R == expected.R,
        "V": architecture.V == expected.V,
        "Xi": architecture.Xi == expected.Xi,
    }
    reasons = tuple(name for name, valid in checks.items() if not valid)
    return not reasons, reasons


def _canonical_quotient_O(architecture: Stage13ETypedArchitecture) -> Stage11OLayer:
    quotient = next(item for item in _quotient_classes() if item.quotient_id == architecture.quotient_id)
    events = []
    for event, (_, tau, chi) in zip(architecture.O.relational_events, STAGE13E_CLOCK_PAIRS, strict=True):
        events.append(
            replace(
                event,
                q_value=stage13c_complete_relational_value(quotient.Q_D, quotient.P_D, tau, chi),
            )
        )
    return replace(architecture.O, relational_events=tuple(events))


def stage13e_quotient_projection(architecture: Stage13ETypedArchitecture) -> Stage13EQuotientArchitecture:
    return Stage13EQuotientArchitecture(
        orbit_id=architecture.orbit_id,
        quotient_id=architecture.quotient_id,
        O=_canonical_quotient_O(architecture),
        P=architecture.P,
        R=architecture.R,
        V=architecture.V,
        parameterization_id=architecture.Xi.parameterization_id,
        event_correspondence=architecture.Xi.event_correspondence,
        continuation_class_correspondence=architecture.Xi.continuation_class_correspondence,
        outcome_correspondence=architecture.Xi.outcome_correspondence,
        lapse_semantics=architecture.Xi.lapse_semantics,
        normalization_semantics=architecture.Xi.normalization_semantics,
        orbit_bridge_semantics=architecture.Xi.orbit_bridge_semantics,
    )


@lru_cache(maxsize=1)
def canonical_stage13e_quotient_projections() -> tuple[Stage13EQuotientArchitecture, ...]:
    return tuple(stage13e_quotient_projection(item) for item in canonical_stage13e_architectures())


def _measurement_for_architecture(architecture: Stage13ETypedArchitecture, continuation_id: str) -> Stage13EMeasurementView:
    base = _stage12_measurement_by_orbit_continuation()[(architecture.orbit_id, continuation_id)]
    events = {item.role: item for item in architecture.O.relational_events}
    return Stage13EMeasurementView(
        orbit_id=architecture.orbit_id,
        quotient_id=architecture.quotient_id,
        representative_id=architecture.representative_id,
        continuation_id=continuation_id,
        anchor_event_id=events["prediction_anchor"].physical_event_id,
        target_event_id=events["measurement_target"].physical_event_id,
        family_id=base.family_id,
        internal_clock=base.internal_clock,
        internal_clock_index=base.internal_clock_index,
        outcome_ids=base.outcome_ids,
        normalization_semantics=base.normalization_semantics,
        probabilities=base.probabilities,
        probability_sum_residual=base.probability_sum_residual,
        completeness_residual=base.completeness_residual,
        minimum_effect_eigenvalue=base.minimum_effect_eigenvalue,
        minimum_normalization_eigenvalue=base.minimum_normalization_eigenvalue,
        normalization_denominator=base.normalization_denominator,
    )


@lru_cache(maxsize=1)
def canonical_stage13e_measurement_views() -> tuple[Stage13EMeasurementView, ...]:
    return tuple(
        _measurement_for_architecture(architecture, continuation_id)
        for architecture in canonical_stage13e_architectures()
        for continuation_id in ("h_L", "h_R")
    )


def _weighted_for_architecture(architecture: Stage13ETypedArchitecture) -> Stage13EWeightedView:
    base = _stage12_weighted_by_orbit()[architecture.orbit_id]
    return Stage13EWeightedView(
        architecture.orbit_id, architecture.quotient_id, architecture.representative_id,
        base.continuation_ids, base.continuation_weights, base.predictive_density,
        base.directional_record_scores, base.directional_accessibility_scores,
        base.orientations, base.next_outcomes, base.next_probabilities,
    )


@lru_cache(maxsize=1)
def canonical_stage13e_weighted_views() -> tuple[Stage13EWeightedView, ...]:
    return tuple(_weighted_for_architecture(item) for item in canonical_stage13e_architectures())


def _posterior_for_architecture(architecture: Stage13ETypedArchitecture) -> Stage13EPosteriorView:
    base = _stage12_posterior_by_orbit()[architecture.orbit_id]
    return Stage13EPosteriorView(
        architecture.orbit_id, architecture.quotient_id, architecture.representative_id,
        base.observed_outcome, base.epistemic_posterior_weights, base.ontic_posterior_weights,
        base.epistemic_selected_continuation_id, base.ontic_no_selected_complete_continuation_datum,
    )


@lru_cache(maxsize=1)
def canonical_stage13e_posterior_views() -> tuple[Stage13EPosteriorView, ...]:
    return tuple(_posterior_for_architecture(item) for item in canonical_stage13e_architectures())


def stage13e_orbit_sensitive_witness(representative: Stage13Representative) -> Stage13EOrbitSensitiveWitness:
    Q_D, P_D = stage13c_reconstruct_dirac_from_point(representative.point())
    tau, chi = 1.0, 1.0
    relational_q = stage13c_complete_relational_value(Q_D, P_D, tau, chi)
    score = float(Q_D + 0.5 * P_D + 0.25 * relational_q)
    p_left = float(0.5 + 0.25 * tanh(score))
    probabilities = (
        (FUTURE_SIGNATURE_LEFT, p_left),
        (FUTURE_SIGNATURE_OTHER, float(1.0 - p_left)),
    )
    quotient = _quotient_by_representative()[representative.representative_id]
    return Stage13EOrbitSensitiveWitness(
        representative.orbit_id, quotient.quotient_id, representative.representative_id,
        float(Q_D), float(P_D), tau, chi, float(relational_q), score, probabilities,
        float(abs(sum(value for _, value in probabilities) - 1.0)),
        STAGE13E_ORBIT_WITNESS_SEMANTICS,
    )


@lru_cache(maxsize=1)
def canonical_stage13e_orbit_witnesses() -> tuple[Stage13EOrbitSensitiveWitness, ...]:
    return tuple(stage13e_orbit_sensitive_witness(item) for item in canonical_stage13a_representatives())


def _probability_residual(left, right) -> float:
    lhs, rhs = dict(left), dict(right)
    if set(lhs) != set(rhs):
        return float("inf")
    return float(max((abs(lhs[key] - rhs[key]) for key in lhs), default=0.0))


def _tuple_residual(left, right) -> float:
    try:
        a = np.asarray(left, dtype=np.complex128)
        b = np.asarray(right, dtype=np.complex128)
    except (TypeError, ValueError):
        return 0.0 if left == right else float("inf")
    if a.shape != b.shape:
        return float("inf")
    return float(np.max(np.abs(a - b))) if a.size else 0.0


def _architecture_projection_residual(left: Stage13EQuotientArchitecture, right: Stage13EQuotientArchitecture) -> float:
    if left == right:
        return 0.0
    if (
        left.orbit_id != right.orbit_id
        or left.quotient_id != right.quotient_id
        or left.P != right.P or left.R != right.R or left.V != right.V
        or left.parameterization_id != right.parameterization_id
        or left.event_correspondence != right.event_correspondence
        or left.continuation_class_correspondence != right.continuation_class_correspondence
        or left.outcome_correspondence != right.outcome_correspondence
        or left.lapse_semantics != right.lapse_semantics
        or left.normalization_semantics != right.normalization_semantics
        or left.orbit_bridge_semantics != right.orbit_bridge_semantics
    ):
        return float("inf")
    lhs = tuple(value for event in left.O.relational_events for value in (event.clock_value, event.q_value))
    rhs = tuple(value for event in right.O.relational_events for value in (event.clock_value, event.q_value))
    return _tuple_residual(lhs, rhs)


def _posterior_residual(left: Stage13EPosteriorView, right: Stage13EPosteriorView) -> float:
    if (
        left.observed_outcome != right.observed_outcome
        or left.epistemic_selected_continuation_id != right.epistemic_selected_continuation_id
        or left.ontic_no_selected_complete_continuation_datum != right.ontic_no_selected_complete_continuation_datum
    ):
        return float("inf")
    return max(
        _tuple_residual(left.epistemic_posterior_weights, right.epistemic_posterior_weights),
        _tuple_residual(left.ontic_posterior_weights, right.ontic_posterior_weights),
    )


def _public_path_basis_provenance_absent() -> bool:
    names = {item.name for item in fields(Stage13EQuotientArchitecture)}
    forbidden = {
        "representative_id", "constraint_basis_id", "generator_family_type", "path_word",
        "path_word_role", "licensed_path_words", "s", "u", "compensator_provenance",
        "representative_T", "representative_X",
    }
    return not bool(names & forbidden)


@lru_cache(maxsize=1)
def canonical_stage13e_compensated_operational_descent_checks() -> tuple[Stage13ECompensatedOperationalDescentCheck, ...]:
    architectures = {item.representative_id: item for item in canonical_stage13e_architectures()}
    projections = {key: stage13e_quotient_projection(value) for key, value in architectures.items()}
    measurements = {
        (item.representative_id, item.continuation_id): item
        for item in canonical_stage13e_measurement_views()
    }
    weighted = {item.representative_id: item for item in canonical_stage13e_weighted_views()}
    posterior = {item.representative_id: item for item in canonical_stage13e_posterior_views()}
    witnesses = {item.representative_id: item for item in canonical_stage13e_orbit_witnesses()}
    stage13d_checks = {item.comparison_id: item for item in canonical_stage13d_compensated_descent_checks()}

    result = []
    for comparison in canonical_stage13b_mixed_path_comparisons():
        dcheck = stage13d_checks[comparison.comparison_id]
        source_id, target_id = comparison.source_representative_id, comparison.target_representative_id
        if dcheck.max_dirac_payload_residual > STAGE13E_ATOL or dcheck.max_relational_payload_residual > STAGE13E_ATOL:
            raise ValueError("Stage 13E cannot lift an unlicensed Stage 13D compensated descent")
        source_projection, target_projection = projections[source_id], projections[target_id]
        if source_projection.quotient_id != target_projection.quotient_id:
            raise ValueError("Stage 13E compensated path crosses quotient classes")
        measurement_residual = max(
            _probability_residual(measurements[(source_id, cid)].probabilities, measurements[(target_id, cid)].probabilities)
            for cid in ("h_L", "h_R")
        )
        weighted_residual = _probability_residual(weighted[source_id].next_probabilities, weighted[target_id].next_probabilities)
        posterior_residual = _posterior_residual(posterior[source_id], posterior[target_id])
        witness_residual = _probability_residual(witnesses[source_id].probabilities, witnesses[target_id].probabilities)
        path_TX = Stage13EPathXi(
            comparison.comparison_id, comparison.constraint_basis_id, source_id, target_id,
            comparison.path_word_TX, comparison.path_word_role, comparison.s, comparison.u_TX,
            "exact TX raw parameter; compensated correspondent to XT", comparison.temporal_order_status,
            comparison.metaphysical_claim_status,
        )
        path_XT = Stage13EPathXi(
            comparison.comparison_id, comparison.constraint_basis_id, source_id, target_id,
            comparison.path_word_XT, comparison.path_word_role, comparison.s, comparison.u_XT,
            "exact XT compensator u_XT=exp(s)u_TX", comparison.temporal_order_status,
            comparison.metaphysical_claim_status,
        )
        result.append(
            Stage13ECompensatedOperationalDescentCheck(
                comparison.comparison_id, source_projection.quotient_id, source_id, target_id,
                path_TX, path_XT,
                bool(path_TX.path_word != path_XT.path_word and abs(path_TX.u - path_XT.u) > STAGE13E_ATOL),
                _architecture_projection_residual(source_projection, target_projection),
                measurement_residual, weighted_residual, posterior_residual, witness_residual,
                4, STAGE13E_PATH_DESCENT_CLASSIFICATION, STAGE13E_METAPHYSICAL_CLAIM_STATUS,
            )
        )
    return tuple(result)


@lru_cache(maxsize=1)
def stage13e_controls() -> tuple[Stage13EControl, ...]:
    architectures = canonical_stage13e_architectures()
    base = architectures[0]
    result = []

    def add_architecture_control(control_id, candidate):
        valid, reasons = stage13e_validate_architecture(candidate)
        result.append(Stage13EControl(
            control_id, STAGE13E_TYPED_REJECTION if not valid else "inconclusive",
            not valid, 0.0, reasons,
        ))

    add_architecture_control(
        "wrong_event_correspondence",
        replace(base, Xi=replace(base.Xi, event_correspondence=tuple(reversed(base.Xi.event_correspondence)))),
    )
    reversed_classes = tuple(reversed(base.Xi.continuation_class_correspondence))
    add_architecture_control(
        "wrong_class_correspondence",
        replace(base, Xi=replace(base.Xi, continuation_class_correspondence=tuple(
            (source, target)
            for (source, _), (_, target) in zip(base.Xi.continuation_class_correspondence, reversed_classes, strict=True)
        ))),
    )
    add_architecture_control(
        "wrong_outcome_correspondence",
        replace(base, Xi=replace(base.Xi, outcome_correspondence=(
            (FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_OTHER),
            (FUTURE_SIGNATURE_OTHER, FUTURE_SIGNATURE_LEFT),
        ))),
    )

    first_path = canonical_stage13b_mixed_path_comparisons()[0]
    wrong_path_rejected = first_path.wrong_compensator_target_residual > STAGE13E_ATOL
    result.append(Stage13EControl(
        "wrong_path_correspondence", STAGE13E_WRONG_PATH_REJECTION if wrong_path_rejected else "inconclusive",
        wrong_path_rejected, float(first_path.wrong_compensator_target_residual),
        ("wrong compensator does not reach declared target",),
    ))

    inherited_normalization = next(item for item in stage12d_controls() if item.control_id == "wrong_normalization")
    result.append(Stage13EControl(
        "wrong_normalization",
        STAGE13E_NORMALIZATION_REJECTION if inherited_normalization.rejected else "inconclusive",
        inherited_normalization.rejected, float(inherited_normalization.numerical_witness_residual),
        inherited_normalization.rejection_reasons,
    ))

    corrupted_O = replace(base, O=replace(
        base.O,
        relational_events=(replace(base.O.relational_events[0], q_value=base.O.relational_events[0].q_value + 0.05),)
        + base.O.relational_events[1:],
    ))
    corrupted_P = replace(base, P=replace(base.P, current_anchor=base.P.current_anchor + 1))
    corrupted_R = replace(base, R=replace(
        base.R,
        R_direction=(replace(base.R.R_direction[0], record_score=base.R.R_direction[0].record_score + 0.1),)
        + base.R.R_direction[1:],
    ))
    weights = list(base.V.V_weights)
    weights[0] += 0.05
    weights[1] -= 0.05
    corrupted_V = replace(base, V=replace(base.V, V_weights=tuple(weights)))

    for control_id, candidate in (
        ("representative_dependent_O", corrupted_O),
        ("representative_dependent_P", corrupted_P),
        ("representative_dependent_R", corrupted_R),
        ("representative_dependent_V", corrupted_V),
    ):
        valid, reasons = stage13e_validate_architecture(candidate)
        result.append(Stage13EControl(
            control_id, STAGE13E_REPRESENTATIVE_CORRUPTION_REJECTED if not valid else "inconclusive",
            not valid, 0.05 if control_id != "representative_dependent_R" else 0.1, reasons,
        ))

    measurement = canonical_stage13e_measurement_views()[0]
    probability_map = dict(measurement.probabilities)
    left = probability_map[FUTURE_SIGNATURE_LEFT]
    corrupted_probabilities = (
        (FUTURE_SIGNATURE_LEFT, left + 0.05),
        (FUTURE_SIGNATURE_OTHER, 1.0 - (left + 0.05)),
    )
    measurement_residual = _probability_residual(measurement.probabilities, corrupted_probabilities)
    result.append(Stage13EControl(
        "representative_dependent_measurement",
        STAGE13E_REPRESENTATIVE_CORRUPTION_REJECTED if measurement_residual > STAGE13E_ATOL else "inconclusive",
        measurement_residual > STAGE13E_ATOL, float(measurement_residual),
        ("normalized measurement payload became representative-dependent",),
    ))
    return tuple(result)


def stage13e_diagnostics() -> Stage13EDiagnostics:
    orbits = canonical_stage13a_orbits()
    representatives = canonical_stage13a_representatives()
    quotients = _quotient_classes()
    architectures = canonical_stage13e_architectures()
    projections = canonical_stage13e_quotient_projections()
    measurements = canonical_stage13e_measurement_views()
    weighted = canonical_stage13e_weighted_views()
    posterior = canonical_stage13e_posterior_views()
    witnesses = canonical_stage13e_orbit_witnesses()
    path_checks = canonical_stage13e_compensated_operational_descent_checks()
    controls = stage13e_controls()

    valid_architectures = all(stage13e_validate_architecture(item)[0] for item in architectures)
    max_architecture = max_measurement = max_weighted = max_posterior = max_witness = 0.0

    for orbit in orbits:
        orbit_id = orbit.orbit_id
        orbit_projections = [item for item in projections if item.orbit_id == orbit_id]
        reference_projection = orbit_projections[0]
        max_architecture = max(max_architecture, max(
            _architecture_projection_residual(reference_projection, item) for item in orbit_projections
        ))
        for continuation_id in ("h_L", "h_R"):
            subset = [item for item in measurements if item.orbit_id == orbit_id and item.continuation_id == continuation_id]
            reference = subset[0]
            max_measurement = max(max_measurement, max(
                _probability_residual(reference.probabilities, item.probabilities) for item in subset
            ))
        weighted_subset = [item for item in weighted if item.orbit_id == orbit_id]
        max_weighted = max(max_weighted, max(
            _probability_residual(weighted_subset[0].next_probabilities, item.next_probabilities)
            for item in weighted_subset
        ))
        posterior_subset = [item for item in posterior if item.orbit_id == orbit_id]
        max_posterior = max(max_posterior, max(
            _posterior_residual(posterior_subset[0], item) for item in posterior_subset
        ))
        witness_subset = [item for item in witnesses if item.orbit_id == orbit_id]
        max_witness = max(max_witness, max(
            _probability_residual(witness_subset[0].probabilities, item.probabilities)
            for item in witness_subset
        ))

    witness_references = [next(item for item in witnesses if item.orbit_id == orbit.orbit_id) for orbit in orbits]
    witness_signatures = {
        tuple(round(value, 15) for _, value in item.probabilities) for item in witness_references
    }
    witness_separations = [
        _probability_residual(left.probabilities, right.probabilities)
        for index, left in enumerate(witness_references)
        for right in witness_references[index + 1:]
    ]

    max_sum = max(item.probability_sum_residual for item in measurements)
    max_completeness = max(item.completeness_residual for item in measurements)
    min_effect = min(item.minimum_effect_eigenvalue for item in measurements)
    min_normalization = min(item.minimum_normalization_eigenvalue for item in measurements)
    min_denominator = min(item.normalization_denominator for item in measurements)
    rejected_controls = sum(item.rejected for item in controls)

    max_path_arch = max(item.public_architecture_residual for item in path_checks)
    max_path_measurement = max(item.measurement_probability_residual for item in path_checks)
    max_path_weighted = max(item.weighted_probability_residual for item in path_checks)
    max_path_posterior = max(item.posterior_residual for item in path_checks)
    max_path_witness = max(item.witness_residual for item in path_checks)

    path_xi_explicit = all(
        item.path_provenance_distinct
        and item.path_Xi_TX.path_word == (STAGE13B_PHI_T, STAGE13B_PHI_X)
        and item.path_Xi_XT.path_word == (STAGE13B_PHI_X, STAGE13B_PHI_T)
        and item.path_Xi_TX.temporal_order_status == STAGE13B_TEMPORAL_ORDER_STATUS
        and item.path_Xi_XT.metaphysical_claim_status == STAGE13B_METAPHYSICAL_CLAIM_STATUS
        for item in path_checks
    )
    tolerance = 1e-9
    criteria = bool(
        len(orbits) == 4
        and len(representatives) == 36
        and len(quotients) == 4
        and len(architectures) == 36
        and valid_architectures
        and len(set(projections)) == 4
        and max_architecture <= STAGE13E_ATOL
        and len(measurements) == 72
        and sum(len(item.probabilities) for item in measurements) == 144
        and max_measurement <= tolerance
        and len(weighted) == 36 and max_weighted <= tolerance
        and len(posterior) == 36 and max_posterior <= tolerance
        and len(witnesses) == 36
        and len(witness_signatures) == 4
        and max_witness <= STAGE13E_ATOL
        and min(witness_separations) > tolerance
        and len(path_checks) == 144
        and all(item.classification == STAGE13E_PATH_DESCENT_CLASSIFICATION for item in path_checks)
        and max_path_arch <= tolerance
        and max_path_measurement <= tolerance
        and max_path_weighted <= tolerance
        and max_path_posterior <= tolerance
        and max_path_witness <= tolerance
        and max_sum <= tolerance and max_completeness <= tolerance
        and min_effect >= -tolerance and min_normalization > tolerance and min_denominator > tolerance
        and _public_path_basis_provenance_absent()
        and path_xi_explicit
        and len(controls) == 10 and rejected_controls == 10
    )
    return Stage13EDiagnostics(
        len(orbits), len(representatives), len(quotients), len(architectures), len(set(projections)),
        len(measurements), sum(len(item.probabilities) for item in measurements),
        len(weighted), len(posterior), len(witnesses), len(witness_signatures),
        len(path_checks), 2 * len(path_checks), sum(item.measurement_evaluation_count for item in path_checks),
        float(max_architecture), float(max_measurement), float(max_weighted), float(max_posterior), float(max_witness),
        float(min(witness_separations)), float(max_path_arch), float(max_path_measurement), float(max_path_weighted),
        float(max_path_posterior), float(max_path_witness), float(max_sum), float(max_completeness),
        float(min_effect), float(min_normalization), float(min_denominator),
        _public_path_basis_provenance_absent(), path_xi_explicit, len(controls), rejected_controls, criteria,
    )


def stage13e_summary() -> dict[str, object]:
    d = stage13e_diagnostics()
    return {
        "stage": "13E",
        "status": "Stage 13E completed; criteria 39–43 satisfied" if d.criteria_39_43_satisfied else "Stage 13E incomplete",
        "criteria_39_43_satisfied": d.criteria_39_43_satisfied,
        "physical_orbit_count": d.physical_orbit_count,
        "representative_count": d.representative_count,
        "quotient_class_count": d.quotient_class_count,
        "architecture_view_count": d.architecture_view_count,
        "distinct_quotient_architecture_count": d.distinct_quotient_architecture_count,
        "measurement_view_count": d.measurement_view_count,
        "probability_evaluation_count": d.probability_evaluation_count,
        "weighted_view_count": d.weighted_view_count,
        "posterior_view_count": d.posterior_view_count,
        "orbit_witness_count": d.orbit_witness_count,
        "distinct_orbit_witness_count": d.distinct_orbit_witness_count,
        "compensated_path_check_count": d.compensated_path_check_count,
        "path_xi_view_count": d.path_xi_view_count,
        "compensated_measurement_evaluation_count": d.compensated_measurement_evaluation_count,
        "minimum_cross_orbit_witness_separation": d.minimum_cross_orbit_witness_separation,
        "control_count": d.control_count,
        "rejected_control_count": d.rejected_control_count,
        "bounded_result": STAGE13E_BOUNDED_RESULT if d.criteria_39_43_satisfied else "not_established",
        "guards": (
            "path-specific Xi provenance != quotient-level physical content",
            "basis-specific Xi provenance != quotient-level physical content",
            "path word != modal continuation",
            "path word != physical temporal history",
            "compensated-path operational descent != refoliation invariance",
            "same path-invariant probability within an orbit != all physical orbits operationally identical",
            "typed bridge to orbit data != dynamical derivation of quantum measurement from the classical constraint",
            "orbit-sensitive witness != empirical prediction",
            "future-measurement covariance != future actuality",
            "gauge quotient != elimination of physical change",
            "finite-model success != empirical discovery",
        ),
    }
