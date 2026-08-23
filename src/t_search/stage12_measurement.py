"""Stage 12D O/P/R/V/Xi and orbit-sensitive future-measurement descent.

Stage 12D reuses the Stage 10/11 future-measurement family rather than
redesigning it.  External reparameterization is fixed to the Stage 11 identity
chart and the internal measurement chart to Stage 11D's A/e2 reference so this
stage isolates same-orbit constraint-generated gauge-representative descent.
Explicit C x G x Phi compatibility remains Stage 12E.

Representative-level relational O values are reconstructed independently from
phase-space data and are compared with an explicit tolerance.  The quotient
projection is then canonicalized with the Stage 12C quotient-class Dirac data,
so machine-level floating-point noise is not mistaken for a distinct physical
quotient object.

The inherited Stage 10/11 measurement payload is supplemented by a declared,
bounded orbit-sensitive operational witness.  That bridge is diagnostic only:
it is not a dynamical derivation of quantum measurement from the classical
constraint and is not an empirical prediction.
"""

from __future__ import annotations

from dataclasses import dataclass, fields, replace
from functools import lru_cache
from math import tanh

import numpy as np

from .stage5_clock_change import DEFAULT_ATOL
from .stage9_modal import (
    FUTURE_SIGNATURE_LEFT,
    FUTURE_SIGNATURE_OTHER,
    Stage9Evidence,
    canonical_stage9c_models,
)
from .stage11_lift import (
    Stage11OLayer,
    Stage11OEvent,
    Stage11PLayer,
    Stage11RLayer,
    Stage11VLayer,
    stage11c_public_architecture,
)
from .stage11_measurement import (
    STAGE11D_REFERENCE_CLOCK,
    STAGE11D_REFERENCE_CLOCK_INDEX,
    Stage11DMeasurementView,
    Stage11DPosteriorView,
    Stage11DWeightedPublicView,
    stage11d_controls,
    stage11d_measurement_view,
    stage11d_posterior_view,
    stage11d_weighted_public_view,
)
from .stage11_parametrized import STAGE11A_ATOL, STAGE11A_IDENTITY
from .stage11_relational import STAGE11B_ANCHOR_INDEX, STAGE11B_TARGET_INDEX
from .stage12_gauge_atlas import Stage12CQuotientClass, canonical_stage12c_quotient_classes
from .stage12_multi_orbit import (
    Stage12GaugeRepresentative,
    canonical_stage12a_orbits,
    canonical_stage12a_representatives,
)
from .stage12_relational import stage12b_dirac_from_representative

STAGE12D_ATOL = STAGE11A_ATOL
STAGE12D_REFERENCE_PARAMETERIZATION = STAGE11A_IDENTITY
STAGE12D_TYPED_REJECTION = "typed_measurement_context_rejected"
STAGE12D_NORMALIZATION_REJECTION = "misaligned_normalization_numerically_rejected"
STAGE12D_FALSE_POSITIVE_REJECTED = "false_positive_rejected"
STAGE12D_ORBIT_WITNESS_SEMANTICS = (
    "declared bounded orbit-conditioned operational bridge from independently "
    "reconstructed Dirac/relational data; not a dynamical derivation of quantum "
    "measurement from the classical constraint"
)
STAGE12D_GAUGE_PROVENANCE_SEMANTICS = (
    "representative-specific constraint-generated gauge provenance retained in Xi; "
    "quotient projection removes only representative redundancy"
)
STAGE12D_BOUNDED_RESULT = (
    "Stage 12D typed O/P/R/V and orbit-sensitive future-measurement descent "
    "on the frozen finite gauge atlas = established"
)


@dataclass(frozen=True, slots=True)
class Stage12DXiLayer:
    parameterization_id: str
    orbit_id: str
    quotient_id: str
    representative_id: str
    gauge_parameter_s: float
    gauge_provenance_semantics: str
    stage11_anchor_physical_event_id: str
    stage11_target_physical_event_id: str
    event_correspondence: tuple[tuple[str, str], ...]
    continuation_class_correspondence: tuple[tuple[str, str], ...]
    outcome_correspondence: tuple[tuple[str, str], ...]
    lapse_semantics: str
    normalization_semantics: str
    orbit_bridge_semantics: str


@dataclass(frozen=True, slots=True)
class Stage12DTypedArchitecture:
    orbit_id: str
    quotient_id: str
    representative_id: str
    O: Stage11OLayer
    P: Stage11PLayer
    R: Stage11RLayer
    V: Stage11VLayer
    Xi: Stage12DXiLayer


@dataclass(frozen=True, slots=True)
class Stage12DQuotientArchitecture:
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
class Stage12DArchitectureValidation:
    orbit_id: str
    representative_id: str
    orbit_valid: bool
    quotient_valid: bool
    O_valid: bool
    P_valid: bool
    R_valid: bool
    V_valid: bool
    Xi_valid: bool
    valid: bool
    rejection_reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Stage12DMeasurementDescentView:
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
class Stage12DWeightedDescentView:
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
class Stage12DPosteriorDescentView:
    orbit_id: str
    quotient_id: str
    representative_id: str
    observed_outcome: str
    epistemic_posterior_weights: tuple[float, ...]
    ontic_posterior_weights: tuple[float, ...]
    epistemic_selected_continuation_id: str
    ontic_no_selected_complete_continuation_datum: bool


@dataclass(frozen=True, slots=True)
class Stage12DOrbitSensitiveWitness:
    orbit_id: str
    quotient_id: str
    representative_id: str
    Q_D: float
    P_D: float
    target_tau: float
    relational_q_target: float
    bridge_score: float
    probabilities: tuple[tuple[str, float], ...]
    probability_sum_residual: float
    semantics: str


@dataclass(frozen=True, slots=True)
class Stage12DControl:
    control_id: str
    classification: str
    rejected: bool
    numerical_witness_residual: float
    rejection_reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Stage12DDiagnostics:
    physical_orbit_count: int
    representative_count: int
    quotient_class_count: int
    architecture_view_count: int
    distinct_quotient_architecture_count: int
    measurement_view_count: int
    probability_evaluation_count: int
    weighted_public_view_count: int
    posterior_view_count: int
    orbit_witness_count: int
    distinct_orbit_witness_count: int
    max_same_orbit_architecture_residual: float
    max_same_orbit_measurement_probability_residual: float
    max_same_orbit_weighted_probability_residual: float
    max_same_orbit_posterior_residual: float
    max_same_orbit_witness_residual: float
    minimum_cross_orbit_witness_separation: float
    max_probability_sum_residual: float
    max_measurement_completeness_residual: float
    minimum_effect_eigenvalue: float
    minimum_normalization_eigenvalue: float
    minimum_normalization_denominator: float
    matched_epistemic_ontic_public_architecture: bool
    public_schema_selector_free: bool
    control_count: int
    rejected_control_count: int
    criteria_32_38_satisfied: bool


def _representative_lookup() -> dict[str, Stage12GaugeRepresentative]:
    return {item.representative_id: item for item in canonical_stage12a_representatives()}


@lru_cache(maxsize=1)
def _quotient_classes() -> tuple[Stage12CQuotientClass, ...]:
    return canonical_stage12c_quotient_classes()


def _quotient_lookup() -> dict[str, Stage12CQuotientClass]:
    result: dict[str, Stage12CQuotientClass] = {}
    for quotient in _quotient_classes():
        for representative_id in quotient.representative_ids:
            if representative_id in result:
                raise ValueError("Stage 12D representative occurs in multiple quotient classes")
            result[representative_id] = quotient
    if set(result) != set(_representative_lookup()):
        raise ValueError("Stage 12D quotient lookup does not cover the representative carrier")
    return result


@lru_cache(maxsize=1)
def _stage11_reference_architecture():
    _, ontic = canonical_stage9c_models(selected_id="h_L")
    return stage11c_public_architecture(ontic, STAGE12D_REFERENCE_PARAMETERIZATION)


def _stage11_role_event(role: str) -> Stage11OEvent:
    matches = tuple(
        item for item in _stage11_reference_architecture().O.relational_events if item.role == role
    )
    if len(matches) != 1:
        raise ValueError(f"Stage 12D expected exactly one Stage 11 {role!r} event")
    return matches[0]


def _anchor_target_tau() -> tuple[float, float]:
    anchor = _stage11_role_event("prediction_anchor")
    target = _stage11_role_event("measurement_target")
    if STAGE11B_ANCHOR_INDEX >= STAGE11B_TARGET_INDEX:
        raise ValueError("Stage 12D inherited anchor must precede target in the frozen event sample")
    return float(anchor.clock_value), float(target.clock_value)


def _orbit_relational_events(
    representative: Stage12GaugeRepresentative,
) -> tuple[Stage11OEvent, ...]:
    estimate = stage12b_dirac_from_representative(representative)
    anchor_tau, target_tau = _anchor_target_tau()
    return (
        Stage11OEvent(
            role="prediction_anchor",
            stage10_event="e1",
            physical_event_id=f"{representative.orbit_id}:relational:e1",
            clock_value=anchor_tau,
            q_value=float(estimate.Q_D + estimate.P_D * anchor_tau),
        ),
        Stage11OEvent(
            role="measurement_target",
            stage10_event="e2",
            physical_event_id=f"{representative.orbit_id}:relational:e2",
            clock_value=target_tau,
            q_value=float(estimate.Q_D + estimate.P_D * target_tau),
        ),
    )


def stage12d_architecture_for_representative(
    representative: Stage12GaugeRepresentative,
) -> Stage12DTypedArchitecture:
    base = _stage11_reference_architecture()
    quotient = _quotient_lookup()[representative.representative_id]
    relational_events = _orbit_relational_events(representative)
    O = replace(base.O, relational_events=relational_events)
    anchor, target = relational_events
    Xi = Stage12DXiLayer(
        parameterization_id=STAGE12D_REFERENCE_PARAMETERIZATION,
        orbit_id=representative.orbit_id,
        quotient_id=quotient.quotient_id,
        representative_id=representative.representative_id,
        gauge_parameter_s=float(representative.gauge_parameter_s),
        gauge_provenance_semantics=STAGE12D_GAUGE_PROVENANCE_SEMANTICS,
        stage11_anchor_physical_event_id=_stage11_role_event("prediction_anchor").physical_event_id,
        stage11_target_physical_event_id=_stage11_role_event("measurement_target").physical_event_id,
        event_correspondence=(("e1", anchor.physical_event_id), ("e2", target.physical_event_id)),
        continuation_class_correspondence=base.Xi.continuation_class_correspondence,
        outcome_correspondence=base.Xi.outcome_correspondence,
        lapse_semantics=base.Xi.lapse_semantics,
        normalization_semantics=(
            "Stage 10/11 continuation-specific measurement normalization retained; "
            "gauge provenance is not a normalization form"
        ),
        orbit_bridge_semantics=STAGE12D_ORBIT_WITNESS_SEMANTICS,
    )
    return Stage12DTypedArchitecture(
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
def canonical_stage12d_architectures() -> tuple[Stage12DTypedArchitecture, ...]:
    return tuple(
        stage12d_architecture_for_representative(item)
        for item in canonical_stage12a_representatives()
    )


def stage12d_validate_architecture(
    architecture: Stage12DTypedArchitecture,
) -> Stage12DArchitectureValidation:
    representative = _representative_lookup().get(architecture.representative_id)
    if representative is None:
        return Stage12DArchitectureValidation(
            architecture.orbit_id,
            architecture.representative_id,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            ("representative_identity",),
        )
    expected = stage12d_architecture_for_representative(representative)
    checks = {
        "orbit_correspondence": (
            architecture.orbit_id == representative.orbit_id
            and architecture.Xi.orbit_id == representative.orbit_id
        ),
        "quotient_correspondence": (
            architecture.quotient_id == expected.quotient_id
            and architecture.Xi.quotient_id == expected.quotient_id
        ),
        "O": architecture.O == expected.O,
        "P": architecture.P == expected.P,
        "R": architecture.R == expected.R,
        "V": architecture.V == expected.V,
        "Xi": architecture.Xi == expected.Xi,
    }
    reasons = tuple(name for name, valid in checks.items() if not valid)
    return Stage12DArchitectureValidation(
        orbit_id=architecture.orbit_id,
        representative_id=architecture.representative_id,
        orbit_valid=checks["orbit_correspondence"],
        quotient_valid=checks["quotient_correspondence"],
        O_valid=checks["O"],
        P_valid=checks["P"],
        R_valid=checks["R"],
        V_valid=checks["V"],
        Xi_valid=checks["Xi"],
        valid=not reasons,
        rejection_reasons=reasons,
    )


def _canonical_quotient_O(
    architecture: Stage12DTypedArchitecture,
    quotient: Stage12CQuotientClass,
) -> Stage11OLayer:
    """Canonicalize relational O using quotient-level Dirac data.

    Representative O remains an independent phase-space reconstruction.  This
    function is used only after the Stage 12C equivalence class has been built,
    and removes floating-point representative noise at the quotient boundary.
    """

    if tuple(sorted(quotient.inferred_orbit_ids)) != (architecture.orbit_id,):
        raise ValueError("Stage 12D quotient projection cannot mix physical orbits")
    events = tuple(
        replace(
            event,
            q_value=float(quotient.Q_D + quotient.P_D * event.clock_value),
        )
        for event in architecture.O.relational_events
    )
    return replace(architecture.O, relational_events=events)


def stage12d_quotient_projection(
    architecture: Stage12DTypedArchitecture,
) -> Stage12DQuotientArchitecture:
    quotient = next(
        item for item in _quotient_classes() if item.quotient_id == architecture.quotient_id
    )
    return Stage12DQuotientArchitecture(
        orbit_id=architecture.orbit_id,
        quotient_id=architecture.quotient_id,
        O=_canonical_quotient_O(architecture, quotient),
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
def canonical_stage12d_quotient_projections() -> tuple[Stage12DQuotientArchitecture, ...]:
    return tuple(stage12d_quotient_projection(item) for item in canonical_stage12d_architectures())


def _wrap_measurement(
    architecture: Stage12DTypedArchitecture,
    base: Stage11DMeasurementView,
) -> Stage12DMeasurementDescentView:
    events = {item.role: item for item in architecture.O.relational_events}
    return Stage12DMeasurementDescentView(
        orbit_id=architecture.orbit_id,
        quotient_id=architecture.quotient_id,
        representative_id=architecture.representative_id,
        continuation_id=base.continuation_id,
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
def canonical_stage12d_measurement_views() -> tuple[Stage12DMeasurementDescentView, ...]:
    _, ontic = canonical_stage9c_models(selected_id="h_L")
    continuation_ids = tuple(item.continuation_id for item in ontic.carrier.continuations)
    base = {
        continuation_id: stage11d_measurement_view(
            STAGE12D_REFERENCE_PARAMETERIZATION, continuation_id
        )
        for continuation_id in continuation_ids
    }
    return tuple(
        _wrap_measurement(architecture, base[continuation_id])
        for architecture in canonical_stage12d_architectures()
        for continuation_id in continuation_ids
    )


def _wrap_weighted(
    architecture: Stage12DTypedArchitecture,
    base: Stage11DWeightedPublicView,
) -> Stage12DWeightedDescentView:
    return Stage12DWeightedDescentView(
        orbit_id=architecture.orbit_id,
        quotient_id=architecture.quotient_id,
        representative_id=architecture.representative_id,
        continuation_ids=base.continuation_ids,
        continuation_weights=base.continuation_weights,
        predictive_density=base.predictive_density,
        directional_record_scores=base.directional_record_scores,
        directional_accessibility_scores=base.directional_accessibility_scores,
        orientations=base.orientations,
        next_outcomes=base.next_outcomes,
        next_probabilities=base.next_probabilities,
    )


@lru_cache(maxsize=1)
def canonical_stage12d_weighted_views() -> tuple[Stage12DWeightedDescentView, ...]:
    _, ontic = canonical_stage9c_models(selected_id="h_L")
    base = stage11d_weighted_public_view(ontic, STAGE12D_REFERENCE_PARAMETERIZATION)
    return tuple(_wrap_weighted(item, base) for item in canonical_stage12d_architectures())


def _wrap_posterior(
    architecture: Stage12DTypedArchitecture,
    base: Stage11DPosteriorView,
) -> Stage12DPosteriorDescentView:
    return Stage12DPosteriorDescentView(
        orbit_id=architecture.orbit_id,
        quotient_id=architecture.quotient_id,
        representative_id=architecture.representative_id,
        observed_outcome=base.observed_outcome,
        epistemic_posterior_weights=base.epistemic_posterior_weights,
        ontic_posterior_weights=base.ontic_posterior_weights,
        epistemic_selected_continuation_id=base.epistemic_selected_continuation_id,
        ontic_no_selected_complete_continuation_datum=base.ontic_no_selected_complete_continuation_datum,
    )


@lru_cache(maxsize=1)
def canonical_stage12d_posterior_views() -> tuple[Stage12DPosteriorDescentView, ...]:
    epistemic, ontic = canonical_stage9c_models(selected_id="h_L")
    base = stage11d_posterior_view(
        epistemic,
        ontic,
        Stage9Evidence(FUTURE_SIGNATURE_LEFT),
        STAGE12D_REFERENCE_PARAMETERIZATION,
    )
    return tuple(_wrap_posterior(item, base) for item in canonical_stage12d_architectures())


def stage12d_orbit_sensitive_witness(
    representative: Stage12GaugeRepresentative,
) -> Stage12DOrbitSensitiveWitness:
    estimate = stage12b_dirac_from_representative(representative)
    _, target_tau = _anchor_target_tau()
    relational_q = float(estimate.Q_D + estimate.P_D * target_tau)
    score = float(estimate.Q_D + 0.5 * estimate.P_D + 0.25 * relational_q)
    p_left = float(0.5 + 0.25 * tanh(score))
    p_other = float(1.0 - p_left)
    probabilities = (
        (FUTURE_SIGNATURE_LEFT, p_left),
        (FUTURE_SIGNATURE_OTHER, p_other),
    )
    quotient = _quotient_lookup()[representative.representative_id]
    return Stage12DOrbitSensitiveWitness(
        orbit_id=representative.orbit_id,
        quotient_id=quotient.quotient_id,
        representative_id=representative.representative_id,
        Q_D=float(estimate.Q_D),
        P_D=float(estimate.P_D),
        target_tau=target_tau,
        relational_q_target=relational_q,
        bridge_score=score,
        probabilities=probabilities,
        probability_sum_residual=float(abs(p_left + p_other - 1.0)),
        semantics=STAGE12D_ORBIT_WITNESS_SEMANTICS,
    )


@lru_cache(maxsize=1)
def canonical_stage12d_orbit_witnesses() -> tuple[Stage12DOrbitSensitiveWitness, ...]:
    return tuple(
        stage12d_orbit_sensitive_witness(item) for item in canonical_stage12a_representatives()
    )


def _probability_residual(
    left: tuple[tuple[str, float], ...],
    right: tuple[tuple[str, float], ...],
) -> float:
    lhs, rhs = dict(left), dict(right)
    if set(lhs) != set(rhs):
        return float("inf")
    return max((abs(lhs[key] - rhs[key]) for key in lhs), default=0.0)


def _tuple_residual(left: tuple[object, ...], right: tuple[object, ...]) -> float:
    try:
        a = np.asarray(left, dtype=np.complex128)
        b = np.asarray(right, dtype=np.complex128)
    except (TypeError, ValueError):
        return 0.0 if left == right else float("inf")
    if a.shape != b.shape:
        return float("inf")
    return float(np.max(np.abs(a - b))) if a.size else 0.0


def _architecture_projection_residual(
    left: Stage12DQuotientArchitecture,
    right: Stage12DQuotientArchitecture,
) -> float:
    if left == right:
        return 0.0
    if (
        left.orbit_id != right.orbit_id
        or left.quotient_id != right.quotient_id
        or left.P != right.P
        or left.R != right.R
        or left.V != right.V
        or left.event_correspondence != right.event_correspondence
        or left.continuation_class_correspondence != right.continuation_class_correspondence
        or left.outcome_correspondence != right.outcome_correspondence
        or left.parameterization_id != right.parameterization_id
        or left.lapse_semantics != right.lapse_semantics
        or left.normalization_semantics != right.normalization_semantics
        or left.orbit_bridge_semantics != right.orbit_bridge_semantics
    ):
        return float("inf")
    lhs = tuple(
        value
        for event in left.O.relational_events
        for value in (event.clock_value, event.q_value)
    )
    rhs = tuple(
        value
        for event in right.O.relational_events
        for value in (event.clock_value, event.q_value)
    )
    return _tuple_residual(lhs, rhs)


def _public_schema_selector_free() -> bool:
    names: set[str] = set()
    for cls in (
        Stage12DTypedArchitecture,
        Stage12DXiLayer,
        Stage12DQuotientArchitecture,
        Stage12DWeightedDescentView,
    ):
        names.update(item.name for item in fields(cls))
    forbidden = {
        "selected_continuation",
        "selected_continuation_id",
        "hidden_selector",
        "selector",
        "modal_type",
        "model_type",
    }
    return not bool(names & forbidden)


@lru_cache(maxsize=1)
def stage12d_controls() -> tuple[Stage12DControl, ...]:
    architectures = canonical_stage12d_architectures()
    base = architectures[0]
    other_orbit = next(item for item in architectures if item.orbit_id != base.orbit_id)

    wrong_orbit = replace(
        base,
        orbit_id=other_orbit.orbit_id,
        Xi=replace(base.Xi, orbit_id=other_orbit.orbit_id),
    )
    wrong_event = replace(
        base,
        Xi=replace(base.Xi, event_correspondence=tuple(reversed(base.Xi.event_correspondence))),
    )
    reversed_classes = tuple(reversed(base.Xi.continuation_class_correspondence))
    wrong_class = replace(
        base,
        Xi=replace(
            base.Xi,
            continuation_class_correspondence=tuple(
                (source, target)
                for (source, _), (_, target) in zip(
                    base.Xi.continuation_class_correspondence,
                    reversed_classes,
                    strict=True,
                )
            ),
        ),
    )
    wrong_outcome = replace(
        base,
        Xi=replace(
            base.Xi,
            outcome_correspondence=(
                (FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_OTHER),
                (FUTURE_SIGNATURE_OTHER, FUTURE_SIGNATURE_LEFT),
            ),
        ),
    )

    result: list[Stage12DControl] = []
    for control_id, candidate in (
        ("wrong_orbit_correspondence", wrong_orbit),
        ("wrong_event_correspondence", wrong_event),
        ("wrong_class_correspondence", wrong_class),
        ("wrong_outcome_correspondence", wrong_outcome),
    ):
        validation = stage12d_validate_architecture(candidate)
        result.append(
            Stage12DControl(
                control_id=control_id,
                classification=STAGE12D_TYPED_REJECTION if not validation.valid else "inconclusive",
                rejected=not validation.valid,
                numerical_witness_residual=0.0,
                rejection_reasons=validation.rejection_reasons,
            )
        )

    inherited_normalization = next(
        item for item in stage11d_controls() if item.control == "wrong_normalization"
    )
    result.append(
        Stage12DControl(
            control_id="wrong_normalization",
            classification=(
                STAGE12D_NORMALIZATION_REJECTION
                if inherited_normalization.rejected
                else "inconclusive"
            ),
            rejected=inherited_normalization.rejected,
            numerical_witness_residual=float(inherited_normalization.numerical_witness_residual),
            rejection_reasons=inherited_normalization.rejection_reasons,
        )
    )

    witnesses = canonical_stage12d_orbit_witnesses()
    canonical_signatures = {
        tuple(round(value, 15) for _, value in item.probabilities)
        for item in witnesses
        if item.representative_id.endswith("rep_00")
    }
    cloned_signatures = {
        tuple(round(value, 15) for _, value in witnesses[0].probabilities)
        for _ in canonical_stage12a_orbits()
    }
    clone_rejected = len(canonical_signatures) == 4 and len(cloned_signatures) == 1
    result.append(
        Stage12DControl(
            control_id="orbit_insensitive_measurement_clone",
            classification=STAGE12D_FALSE_POSITIVE_REJECTED if clone_rejected else "inconclusive",
            rejected=clone_rejected,
            numerical_witness_residual=float(len(canonical_signatures) - len(cloned_signatures)),
            rejection_reasons=("orbit-sensitive operational witness erased",),
        )
    )
    return tuple(result)


def stage12d_diagnostics(*, atol: float = DEFAULT_ATOL) -> Stage12DDiagnostics:
    orbits = canonical_stage12a_orbits()
    representatives = canonical_stage12a_representatives()
    quotients = _quotient_classes()
    architectures = canonical_stage12d_architectures()
    projections = canonical_stage12d_quotient_projections()
    measurements = canonical_stage12d_measurement_views()
    weighted = canonical_stage12d_weighted_views()
    posterior = canonical_stage12d_posterior_views()
    witnesses = canonical_stage12d_orbit_witnesses()
    controls = stage12d_controls()

    all_architectures_valid = all(stage12d_validate_architecture(item).valid for item in architectures)
    max_architecture = 0.0
    max_measurement = 0.0
    max_weighted = 0.0
    max_posterior = 0.0
    max_witness = 0.0

    for orbit in orbits:
        orbit_projections = [item for item in projections if item.orbit_id == orbit.orbit_id]
        reference_projection = orbit_projections[0]
        max_architecture = max(
            max_architecture,
            max(
                _architecture_projection_residual(reference_projection, item)
                for item in orbit_projections
            ),
        )

        continuation_ids = {
            item.continuation_id for item in measurements if item.orbit_id == orbit.orbit_id
        }
        for continuation_id in continuation_ids:
            subset = [
                item
                for item in measurements
                if item.orbit_id == orbit.orbit_id and item.continuation_id == continuation_id
            ]
            reference = subset[0]
            max_measurement = max(
                max_measurement,
                max(
                    _probability_residual(reference.probabilities, item.probabilities)
                    for item in subset
                ),
            )

        weighted_subset = [item for item in weighted if item.orbit_id == orbit.orbit_id]
        weighted_reference = weighted_subset[0]
        max_weighted = max(
            max_weighted,
            max(
                _probability_residual(weighted_reference.next_probabilities, item.next_probabilities)
                for item in weighted_subset
            ),
        )

        posterior_subset = [item for item in posterior if item.orbit_id == orbit.orbit_id]
        posterior_reference = posterior_subset[0]
        max_posterior = max(
            max_posterior,
            max(
                max(
                    _tuple_residual(
                        posterior_reference.epistemic_posterior_weights,
                        item.epistemic_posterior_weights,
                    ),
                    _tuple_residual(
                        posterior_reference.ontic_posterior_weights,
                        item.ontic_posterior_weights,
                    ),
                )
                for item in posterior_subset
            ),
        )

        witness_subset = [item for item in witnesses if item.orbit_id == orbit.orbit_id]
        witness_reference = witness_subset[0]
        max_witness = max(
            max_witness,
            max(
                _probability_residual(witness_reference.probabilities, item.probabilities)
                for item in witness_subset
            ),
        )

    witness_references = [
        next(item for item in witnesses if item.orbit_id == orbit.orbit_id) for orbit in orbits
    ]
    separations = [
        _probability_residual(left.probabilities, right.probabilities)
        for index, left in enumerate(witness_references)
        for right in witness_references[index + 1 :]
    ]
    minimum_separation = min(separations)
    distinct_witnesses = len(
        {
            tuple(round(value, 15) for _, value in item.probabilities)
            for item in witness_references
        }
    )

    max_sum = max(item.probability_sum_residual for item in measurements)
    max_completeness = max(item.completeness_residual for item in measurements)
    minimum_effect = min(item.minimum_effect_eigenvalue for item in measurements)
    minimum_normalization = min(item.minimum_normalization_eigenvalue for item in measurements)
    minimum_denominator = min(item.normalization_denominator for item in measurements)

    epistemic, ontic = canonical_stage9c_models(selected_id="h_L")
    matched_public = (
        stage11c_public_architecture(epistemic, STAGE12D_REFERENCE_PARAMETERIZATION)
        == stage11c_public_architecture(ontic, STAGE12D_REFERENCE_PARAMETERIZATION)
    )
    rejected_controls = sum(item.rejected for item in controls)
    distinct_quotient_architectures = len(set(projections))
    tolerance = 1.0e-9

    criteria = bool(
        len(orbits) == 4
        and len(representatives) == 20
        and len(quotients) == 4
        and len(architectures) == 20
        and all_architectures_valid
        and distinct_quotient_architectures == 4
        and max_architecture <= STAGE12D_ATOL
        and len(measurements) == 40
        and sum(len(item.probabilities) for item in measurements) == 80
        and max_measurement <= tolerance
        and len(weighted) == 20
        and max_weighted <= tolerance
        and len(posterior) == 20
        and max_posterior <= tolerance
        and len(witnesses) == 20
        and distinct_witnesses == 4
        and max_witness <= STAGE12D_ATOL
        and minimum_separation > tolerance
        and all(item.probability_sum_residual <= tolerance for item in witnesses)
        and max_sum <= tolerance
        and max_completeness <= tolerance
        and minimum_effect >= -tolerance
        and minimum_normalization > tolerance
        and minimum_denominator > tolerance
        and matched_public
        and _public_schema_selector_free()
        and len(controls) == 6
        and rejected_controls == 6
    )

    return Stage12DDiagnostics(
        physical_orbit_count=len(orbits),
        representative_count=len(representatives),
        quotient_class_count=len(quotients),
        architecture_view_count=len(architectures),
        distinct_quotient_architecture_count=distinct_quotient_architectures,
        measurement_view_count=len(measurements),
        probability_evaluation_count=sum(len(item.probabilities) for item in measurements),
        weighted_public_view_count=len(weighted),
        posterior_view_count=len(posterior),
        orbit_witness_count=len(witnesses),
        distinct_orbit_witness_count=distinct_witnesses,
        max_same_orbit_architecture_residual=float(max_architecture),
        max_same_orbit_measurement_probability_residual=float(max_measurement),
        max_same_orbit_weighted_probability_residual=float(max_weighted),
        max_same_orbit_posterior_residual=float(max_posterior),
        max_same_orbit_witness_residual=float(max_witness),
        minimum_cross_orbit_witness_separation=float(minimum_separation),
        max_probability_sum_residual=float(max_sum),
        max_measurement_completeness_residual=float(max_completeness),
        minimum_effect_eigenvalue=float(minimum_effect),
        minimum_normalization_eigenvalue=float(minimum_normalization),
        minimum_normalization_denominator=float(minimum_denominator),
        matched_epistemic_ontic_public_architecture=matched_public,
        public_schema_selector_free=_public_schema_selector_free(),
        control_count=len(controls),
        rejected_control_count=rejected_controls,
        criteria_32_38_satisfied=criteria,
    )


def stage12d_summary(*, atol: float = DEFAULT_ATOL) -> dict[str, object]:
    d = stage12d_diagnostics(atol=atol)
    return {
        "stage": "12D",
        "status": (
            "Stage 12D completed; criteria 32–38 satisfied"
            if d.criteria_32_38_satisfied
            else "Stage 12D incomplete"
        ),
        "criteria_32_38_satisfied": d.criteria_32_38_satisfied,
        "reference_parameterization": STAGE12D_REFERENCE_PARAMETERIZATION,
        "reference_internal_clock": STAGE11D_REFERENCE_CLOCK,
        "reference_internal_clock_index": STAGE11D_REFERENCE_CLOCK_INDEX,
        "physical_orbit_count": d.physical_orbit_count,
        "representative_count": d.representative_count,
        "architecture_view_count": d.architecture_view_count,
        "distinct_quotient_architecture_count": d.distinct_quotient_architecture_count,
        "measurement_view_count": d.measurement_view_count,
        "probability_evaluation_count": d.probability_evaluation_count,
        "weighted_public_view_count": d.weighted_public_view_count,
        "posterior_view_count": d.posterior_view_count,
        "orbit_witness_count": d.orbit_witness_count,
        "distinct_orbit_witness_count": d.distinct_orbit_witness_count,
        "minimum_cross_orbit_witness_separation": d.minimum_cross_orbit_witness_separation,
        "control_count": d.control_count,
        "rejected_control_count": d.rejected_control_count,
        "bounded_result": (
            STAGE12D_BOUNDED_RESULT if d.criteria_32_38_satisfied else "not_established"
        ),
        "guards": (
            "same gauge-invariant probability within an orbit != all physical orbits operationally identical",
            "typed bridge to orbit data != dynamical derivation of quantum measurement from the classical constraint",
            "future-measurement covariance != future actuality",
            "operational quotient descent != modal/ontological identity",
        ),
    }
