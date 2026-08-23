"""Stage 11D future-measurement reparameterization covariance.

Stage 11C established a typed product lift of O/P/R/V/Xi across four
orientation-preserving external parameterizations.  Stage 11D now reuses the
already frozen Stage 10 future-signature measurement family and evaluates the
actual operational probability/update layer on that lift.

To isolate external reparameterization from internal-clock change, Stage 11D
holds the Stage 10 reference internal chart fixed at A/e2.  Stage 11E will test
A/B/C clock-change x reparameterization compatibility.

The physical measurement question is unchanged:

    anchor e1 -> target e2
    QExt(e1) = {h_L, h_R}
    outcomes = {future_signature_left, future_signature_other}

External raw parameter labels and lapse values enter only through the Stage 11
Xi/context typing.  They are not silently substituted for physical event
identity or for the Stage 10 operational normalization form.

A wrong event bridge, wrong lapse/Jacobian semantics, or wrong outcome bridge is
therefore rejected even when ignoring that typing could leave a numerical
probability table unchanged.  A deliberately misaligned normalization also has
an explicit tomography-probe numerical witness.

This establishes only the declared finite product construction.  It is not a
derivation of quantum dynamics from the classical parametrized precursor and
is not general covariance, eternalism, future actuality, or absence of
ontological becoming.
"""

from __future__ import annotations

from dataclasses import dataclass, fields, replace
from math import isclose

import numpy as np

from .stage5_clock_change import DEFAULT_ATOL
from .stage7_history import CURRENT_EVENT, UPPER_EVENT
from .stage9_modal import (
    FUTURE_SIGNATURE_LEFT,
    FUTURE_SIGNATURE_OTHER,
    Stage9CModel,
    Stage9EpistemicModel,
    Stage9Evidence,
    Stage9OnticExtensionModel,
    canonical_stage9c_models,
    continuation_by_id,
    continuation_future_signature_probabilities,
    make_stage9_epistemic_model,
    matched_uniform_weights,
    privileged_stage9_modal_diagnostic,
)
from .stage9_substrate import canonical_stage9_physical_state, stage9_physical_basis
from .stage9_transport import stage9_clock_coordinates
from .stage10_modal import stage10e_posterior_view, stage10e_public_measurement_view
from .stage10_probability import stage10d_chart_probabilities, stage10d_probe_family
from .stage10_reference import STAGE10_REFERENCE_FAMILY_ID
from .stage10_transport import Stage10ChartMeasurement, canonical_stage10c_charts
from .stage11_lift import (
    Stage11TypedArchitecture,
    stage11c_public_architecture,
    stage11c_validate_architecture,
)
from .stage11_parametrized import (
    STAGE11A_ATOL,
    STAGE11A_CUBIC,
    STAGE11A_IDENTITY,
    canonical_stage11a_positive_family,
)

STAGE11D_REFERENCE_CLOCK = "A"
STAGE11D_REFERENCE_CLOCK_INDEX = UPPER_EVENT
STAGE11D_TYPED_REJECTION = "typed_measurement_context_rejected"
STAGE11D_NORMALIZATION_REJECTION = "misaligned_normalization_numerically_rejected"
STAGE11D_COVARIANCE_RESULT = (
    "Stage 11D future-measurement reparameterization covariance on the frozen positive family = established"
)

_EXPECTED_OUTCOMES = (FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_OTHER)
_EXPECTED_STAGE10_EVENTS = (("e1", "e1"), ("e2", "e2"))
_EXPECTED_OUTCOME_CORRESPONDENCE = tuple((item, item) for item in _EXPECTED_OUTCOMES)


@dataclass(frozen=True, slots=True)
class Stage11DContextValidation:
    parameterization_id: str
    continuation_id: str
    architecture_valid: bool
    event_bridge_valid: bool
    lapse_jacobian_semantics_valid: bool
    continuation_correspondence_valid: bool
    outcome_correspondence_valid: bool
    stage10_chart_typing_valid: bool
    valid: bool
    rejection_reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Stage11DMeasurementView:
    parameterization_id: str
    family_id: str
    continuation_id: str
    prediction_anchor: int
    target_event: int
    anchor_physical_event_id: str
    target_physical_event_id: str
    anchor_parameter_value: float
    target_parameter_value: float
    anchor_clock_value: float
    target_clock_value: float
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
class Stage11DWeightedPublicView:
    parameterization_id: str
    anchor_physical_event_id: str
    target_physical_event_id: str
    anchor_parameter_value: float
    target_parameter_value: float
    continuation_ids: tuple[str, ...]
    continuation_weights: tuple[float, ...]
    predictive_density: tuple[complex, ...]
    directional_record_scores: tuple[float, ...]
    directional_accessibility_scores: tuple[float, ...]
    orientations: tuple[str, ...]
    next_outcomes: tuple[str, ...]
    next_probabilities: tuple[tuple[str, float], ...]


@dataclass(frozen=True, slots=True)
class Stage11DPosteriorView:
    parameterization_id: str
    anchor_physical_event_id: str
    target_physical_event_id: str
    observed_outcome: str
    epistemic_posterior_weights: tuple[float, ...]
    ontic_posterior_weights: tuple[float, ...]
    epistemic_selected_continuation_id: str
    ontic_no_selected_complete_continuation_datum: bool


@dataclass(frozen=True, slots=True)
class Stage11DControl:
    control: str
    classification: str
    rejected: bool
    typed_rejection: bool
    numerical_witness_residual: float
    rejection_reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Stage11DDiagnostics:
    parameterization_count: int
    continuation_count: int
    measurement_view_count: int
    probability_evaluation_count: int
    max_per_continuation_reparameterization_probability_residual: float
    max_stage10_reference_probability_residual: float
    max_probability_sum_residual: float
    minimum_probability: float
    maximum_probability: float
    max_completeness_residual: float
    minimum_effect_eigenvalue: float
    minimum_normalization_eigenvalue: float
    minimum_normalization_denominator: float
    anchor_raw_parameter_value_count: int
    target_raw_parameter_value_count: int
    weighted_public_view_count: int
    max_weighted_prediction_reparameterization_residual: float
    matched_epistemic_ontic_public_views_all_parameterizations: bool
    hidden_hstar_swap_public_views_all_parameterizations: bool
    privileged_modal_roles_still_distinct: bool
    public_weighted_schema_selector_free: bool
    posterior_parameterization_count: int
    max_epistemic_posterior_reparameterization_residual: float
    max_ontic_posterior_reparameterization_residual: float
    max_epistemic_ontic_posterior_residual: float
    epistemic_hidden_selection_preserved: bool
    ontic_updated_selector_free_all_parameterizations: bool
    control_count: int
    rejected_control_count: int
    wrong_normalization_matrix_residual: float
    wrong_normalization_probability_residual: float
    criteria_32_38_satisfied: bool


def _chart_lookup() -> dict[tuple[str, str, int], Stage10ChartMeasurement]:
    return {
        (item.continuation_id, item.clock, item.clock_index): item
        for item in canonical_stage10c_charts()
    }


def _reference_chart(continuation_id: str) -> Stage10ChartMeasurement:
    key = (continuation_id, STAGE11D_REFERENCE_CLOCK, STAGE11D_REFERENCE_CLOCK_INDEX)
    try:
        return _chart_lookup()[key]
    except KeyError as exc:
        raise ValueError(f"missing Stage 10 reference chart for {continuation_id!r}") from exc


def _role_event(architecture: Stage11TypedArchitecture, role: str):
    matches = tuple(item for item in architecture.O.relational_events if item.role == role)
    if len(matches) != 1:
        raise ValueError(f"Stage 11D requires exactly one {role!r} relational event")
    return matches[0]


def _expected_architecture(parameterization_id: str) -> Stage11TypedArchitecture:
    _, ontic = canonical_stage9c_models(selected_id="h_L")
    return stage11c_public_architecture(ontic, parameterization_id)


def stage11d_validate_measurement_context(
    architecture: Stage11TypedArchitecture,
    continuation_id: str,
    *,
    atol: float = STAGE11A_ATOL,
) -> Stage11DContextValidation:
    """Validate the typed bridge before any Stage 10 probability is evaluated."""

    expected = _expected_architecture(architecture.Xi.parameterization_id)
    base_validation = stage11c_validate_architecture(architecture, atol=atol)
    anchor = _role_event(architecture, "prediction_anchor")
    target = _role_event(architecture, "measurement_target")
    expected_anchor = _role_event(expected, "prediction_anchor")
    expected_target = _role_event(expected, "measurement_target")

    event_bridge_valid = bool(
        architecture.Xi.event_correspondence == expected.Xi.event_correspondence
        and anchor.stage10_event == "e1"
        and target.stage10_event == "e2"
        and anchor.physical_event_id == expected_anchor.physical_event_id
        and target.physical_event_id == expected_target.physical_event_id
        and anchor.physical_event_id != target.physical_event_id
        and dict(architecture.Xi.event_correspondence).get("e1") == anchor.physical_event_id
        and dict(architecture.Xi.event_correspondence).get("e2") == target.physical_event_id
    )
    lapse_valid = bool(
        architecture.Xi.lapse_semantics == expected.Xi.lapse_semantics
        and isclose(
            architecture.Xi.anchor_lapse,
            expected.Xi.anchor_lapse,
            rel_tol=0.0,
            abs_tol=atol,
        )
        and isclose(
            architecture.Xi.target_lapse,
            expected.Xi.target_lapse,
            rel_tol=0.0,
            abs_tol=atol,
        )
    )
    continuation_valid = bool(
        continuation_id in architecture.P.qext_ids
        and (continuation_id, continuation_id)
        in architecture.Xi.continuation_class_correspondence
    )
    outcome_valid = architecture.Xi.outcome_correspondence == _EXPECTED_OUTCOME_CORRESPONDENCE

    chart = _reference_chart(continuation_id)
    chart_valid = bool(
        chart.family_id == STAGE10_REFERENCE_FAMILY_ID
        and chart.continuation_id == continuation_id
        and chart.clock == STAGE11D_REFERENCE_CLOCK
        and chart.clock_index == STAGE11D_REFERENCE_CLOCK_INDEX
        and chart.prediction_anchor == CURRENT_EVENT
        and chart.target_event == UPPER_EVENT
        and chart.class_correspondence == (continuation_id, continuation_id)
        and chart.event_correspondence == _EXPECTED_STAGE10_EVENTS
        and chart.outcome_correspondence == _EXPECTED_OUTCOME_CORRESPONDENCE
        and tuple(effect.outcome_id for effect in chart.effects) == _EXPECTED_OUTCOMES
    )

    reasons: list[str] = []
    for name, valid in (
        ("stage11c_architecture", base_validation.valid),
        ("event_bridge", event_bridge_valid),
        ("lapse_jacobian", lapse_valid),
        ("continuation_correspondence", continuation_valid),
        ("outcome_correspondence", outcome_valid),
        ("stage10_chart_typing", chart_valid),
    ):
        if not valid:
            reasons.append(name)
    valid = bool(
        base_validation.valid
        and event_bridge_valid
        and lapse_valid
        and continuation_valid
        and outcome_valid
        and chart_valid
    )
    return Stage11DContextValidation(
        parameterization_id=architecture.Xi.parameterization_id,
        continuation_id=continuation_id,
        architecture_valid=base_validation.valid,
        event_bridge_valid=event_bridge_valid,
        lapse_jacobian_semantics_valid=lapse_valid,
        continuation_correspondence_valid=continuation_valid,
        outcome_correspondence_valid=outcome_valid,
        stage10_chart_typing_valid=chart_valid,
        valid=valid,
        rejection_reasons=tuple(reasons),
    )


def _physical_coordinates(continuation, *, atol: float) -> np.ndarray:
    basis = stage9_physical_basis(continuation)
    state = canonical_stage9_physical_state(continuation)
    coordinates, _, rank, _ = np.linalg.lstsq(basis, state, rcond=None)
    if rank != basis.shape[1]:
        raise ValueError("Stage 11D physical basis is not full rank")
    if float(np.linalg.norm(basis @ coordinates - state)) > 10 * atol:
        raise ValueError("Stage 11D physical-coordinate reconstruction failed")
    return np.asarray(coordinates, dtype=np.complex128)


def _normalization_denominator(continuation, chart: Stage10ChartMeasurement, *, atol: float) -> float:
    physical = _physical_coordinates(continuation, atol=atol)
    coordinates = stage9_clock_coordinates(continuation, chart.clock, chart.clock_index)
    state = coordinates @ physical
    value = np.vdot(state, chart.normalization_form @ state)
    if abs(float(value.imag)) > 10 * atol:
        raise ValueError("Stage 11D normalization denominator acquired imaginary part")
    result = float(value.real)
    if result <= atol:
        raise ValueError("Stage 11D normalization denominator is non-positive")
    return result


def _measurement_matrix_diagnostics(chart: Stage10ChartMeasurement) -> tuple[float, float, float]:
    total = np.zeros_like(chart.normalization_form, dtype=np.complex128)
    minimum_effect = float("inf")
    for effect in chart.effects:
        total += effect.matrix
        hermitian = (effect.matrix + effect.matrix.conj().T) / 2.0
        minimum_effect = min(
            minimum_effect,
            float(np.min(np.linalg.eigvalsh(hermitian))),
        )
    normalization = (chart.normalization_form + chart.normalization_form.conj().T) / 2.0
    minimum_normalization = float(np.min(np.linalg.eigvalsh(normalization)))
    completeness = float(np.linalg.norm(total - chart.normalization_form))
    return completeness, minimum_effect, minimum_normalization


def stage11d_measurement_view(
    parameterization_id: str,
    continuation_id: str,
    *,
    atol: float = DEFAULT_ATOL,
) -> Stage11DMeasurementView:
    epistemic, ontic = canonical_stage9c_models(selected_id="h_L")
    del epistemic
    architecture = stage11c_public_architecture(ontic, parameterization_id)
    validation = stage11d_validate_measurement_context(
        architecture, continuation_id, atol=max(atol, STAGE11A_ATOL)
    )
    if not validation.valid:
        raise ValueError(
            "Stage 11D measurement context is not well typed: "
            + ",".join(validation.rejection_reasons)
        )

    continuation = continuation_by_id(ontic.carrier, continuation_id)
    chart = _reference_chart(continuation_id)
    probabilities = stage10d_chart_probabilities(continuation, chart, atol=atol)
    probability_sum_residual = abs(sum(value for _, value in probabilities) - 1.0)
    completeness, minimum_effect, minimum_normalization = _measurement_matrix_diagnostics(chart)
    denominator = _normalization_denominator(continuation, chart, atol=atol)
    anchor = _role_event(architecture, "prediction_anchor")
    target = _role_event(architecture, "measurement_target")

    return Stage11DMeasurementView(
        parameterization_id=parameterization_id,
        family_id=chart.family_id,
        continuation_id=continuation_id,
        prediction_anchor=chart.prediction_anchor,
        target_event=chart.target_event,
        anchor_physical_event_id=anchor.physical_event_id,
        target_physical_event_id=target.physical_event_id,
        anchor_parameter_value=architecture.Xi.anchor_parameter_value,
        target_parameter_value=architecture.Xi.target_parameter_value,
        anchor_clock_value=anchor.clock_value,
        target_clock_value=target.clock_value,
        internal_clock=chart.clock,
        internal_clock_index=chart.clock_index,
        outcome_ids=tuple(name for name, _ in probabilities),
        normalization_semantics=chart.normalization_semantics,
        probabilities=probabilities,
        probability_sum_residual=probability_sum_residual,
        completeness_residual=completeness,
        minimum_effect_eigenvalue=minimum_effect,
        minimum_normalization_eigenvalue=minimum_normalization,
        normalization_denominator=denominator,
    )


def canonical_stage11d_measurement_views() -> tuple[Stage11DMeasurementView, ...]:
    epistemic, _ = canonical_stage9c_models(selected_id="h_L")
    ids = tuple(item.continuation_id for item in epistemic.carrier.continuations)
    return tuple(
        stage11d_measurement_view(trajectory.parameterization_id, continuation_id)
        for trajectory in canonical_stage11a_positive_family()
        for continuation_id in ids
    )


def _probability_residual(
    left: tuple[tuple[str, float], ...],
    right: tuple[tuple[str, float], ...],
) -> float:
    lhs = dict(left)
    rhs = dict(right)
    if set(lhs) != set(rhs):
        return float("inf")
    return max(abs(lhs[name] - rhs[name]) for name in lhs) if lhs else 0.0


def stage11d_weighted_public_view(
    model: Stage9CModel,
    parameterization_id: str,
    *,
    atol: float = DEFAULT_ATOL,
) -> Stage11DWeightedPublicView:
    architecture = stage11c_public_architecture(model, parameterization_id)
    for continuation_id in architecture.P.qext_ids:
        validation = stage11d_validate_measurement_context(
            architecture, continuation_id, atol=max(atol, STAGE11A_ATOL)
        )
        if not validation.valid:
            raise ValueError("Stage 11D weighted view has invalid measurement context")
    base = stage10e_public_measurement_view(
        model, STAGE11D_REFERENCE_CLOCK, STAGE11D_REFERENCE_CLOCK_INDEX, atol=atol
    )
    if base.current_event != CURRENT_EVENT or base.next_outcomes != _EXPECTED_OUTCOMES:
        raise ValueError("Stage 11D Stage 10E public view drifted from the frozen question")
    anchor = _role_event(architecture, "prediction_anchor")
    target = _role_event(architecture, "measurement_target")
    return Stage11DWeightedPublicView(
        parameterization_id=parameterization_id,
        anchor_physical_event_id=anchor.physical_event_id,
        target_physical_event_id=target.physical_event_id,
        anchor_parameter_value=architecture.Xi.anchor_parameter_value,
        target_parameter_value=architecture.Xi.target_parameter_value,
        continuation_ids=base.continuation_ids,
        continuation_weights=base.continuation_weights,
        predictive_density=base.predictive_density,
        directional_record_scores=base.directional_record_scores,
        directional_accessibility_scores=base.directional_accessibility_scores,
        orientations=base.orientations,
        next_outcomes=base.next_outcomes,
        next_probabilities=base.next_probabilities,
    )


def _weighted_payload_close(
    left: Stage11DWeightedPublicView,
    right: Stage11DWeightedPublicView,
    *,
    atol: float,
) -> bool:
    if (
        left.anchor_physical_event_id != right.anchor_physical_event_id
        or left.target_physical_event_id != right.target_physical_event_id
        or left.continuation_ids != right.continuation_ids
        or left.orientations != right.orientations
        or left.next_outcomes != right.next_outcomes
    ):
        return False
    for a, b in (
        (left.continuation_weights, right.continuation_weights),
        (left.predictive_density, right.predictive_density),
        (left.directional_record_scores, right.directional_record_scores),
        (left.directional_accessibility_scores, right.directional_accessibility_scores),
    ):
        if not np.allclose(np.asarray(a), np.asarray(b), atol=atol, rtol=0.0):
            return False
    return _probability_residual(left.next_probabilities, right.next_probabilities) <= atol


def stage11d_posterior_view(
    epistemic: Stage9EpistemicModel,
    ontic: Stage9OnticExtensionModel,
    evidence: Stage9Evidence,
    parameterization_id: str,
    *,
    atol: float = DEFAULT_ATOL,
) -> Stage11DPosteriorView:
    architecture_e = stage11c_public_architecture(epistemic, parameterization_id)
    architecture_o = stage11c_public_architecture(ontic, parameterization_id)
    if architecture_e != architecture_o:
        raise ValueError("Stage 11D matched modal update requires equal public architecture")
    for continuation_id in architecture_o.P.qext_ids:
        if not stage11d_validate_measurement_context(
            architecture_o, continuation_id, atol=max(atol, STAGE11A_ATOL)
        ).valid:
            raise ValueError("Stage 11D posterior context is not well typed")
    base = stage10e_posterior_view(
        epistemic,
        ontic,
        evidence,
        STAGE11D_REFERENCE_CLOCK,
        STAGE11D_REFERENCE_CLOCK_INDEX,
        atol=atol,
    )
    anchor = _role_event(architecture_o, "prediction_anchor")
    target = _role_event(architecture_o, "measurement_target")
    return Stage11DPosteriorView(
        parameterization_id=parameterization_id,
        anchor_physical_event_id=anchor.physical_event_id,
        target_physical_event_id=target.physical_event_id,
        observed_outcome=base.observed_outcome,
        epistemic_posterior_weights=base.epistemic_posterior_weights,
        ontic_posterior_weights=base.ontic_posterior_weights,
        epistemic_selected_continuation_id=base.epistemic_selected_continuation_id,
        ontic_no_selected_complete_continuation_datum=base.ontic_no_selected_complete_continuation_datum,
    )


def _posterior_residual(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    return float(
        np.max(np.abs(np.asarray(left, dtype=float) - np.asarray(right, dtype=float)))
    )


def _wrong_normalization_witness(*, atol: float) -> tuple[float, float]:
    """Return matrix/probability residuals for a deliberately misaligned metric."""

    epistemic, _ = canonical_stage9c_models(selected_id="h_L")
    charts = _chart_lookup()
    probes = stage10d_probe_family()
    max_matrix_residual = 0.0
    max_probability_residual = 0.0
    for continuation in epistemic.carrier.continuations:
        reference = _reference_chart(continuation.continuation_id)
        alternatives = tuple(
            item
            for (cid, _, _), item in charts.items()
            if cid == continuation.continuation_id and item is not reference
        )
        wrong = max(
            alternatives,
            key=lambda item: float(
                np.linalg.norm(item.normalization_form - reference.normalization_form)
            ),
        )
        matrix_residual = float(
            np.linalg.norm(wrong.normalization_form - reference.normalization_form)
        )
        max_matrix_residual = max(max_matrix_residual, matrix_residual)
        for probe in probes:
            correct = stage10d_chart_probabilities(
                continuation,
                reference,
                physical_coordinates=probe.physical_coordinates,
                atol=atol,
            )
            misaligned = stage10d_chart_probabilities(
                continuation,
                reference,
                physical_coordinates=probe.physical_coordinates,
                normalization=wrong.normalization_form,
                atol=atol,
            )
            max_probability_residual = max(
                max_probability_residual,
                _probability_residual(correct, misaligned),
            )
    return max_matrix_residual, max_probability_residual


def stage11d_controls(*, atol: float = DEFAULT_ATOL) -> tuple[Stage11DControl, ...]:
    _, ontic = canonical_stage9c_models(selected_id="h_L")
    base = stage11c_public_architecture(ontic, STAGE11A_CUBIC)
    continuation_id = base.P.qext_ids[0]

    swapped_events = tuple(reversed(base.Xi.event_correspondence))
    # Reversing tuple order alone is not enough; swap the physical-event targets.
    event_map = dict(base.Xi.event_correspondence)
    corrupted_event = replace(
        base,
        Xi=replace(
            base.Xi,
            event_correspondence=(
                ("e1", event_map["e2"]),
                ("e2", event_map["e1"]),
            ),
        ),
    )
    del swapped_events

    identity_architecture = _expected_architecture(STAGE11A_IDENTITY)
    corrupted_jacobian = replace(
        base,
        Xi=replace(
            base.Xi,
            target_lapse=identity_architecture.Xi.target_lapse,
        ),
    )

    corrupted_outcome = replace(
        base,
        Xi=replace(
            base.Xi,
            outcome_correspondence=(
                (FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_OTHER),
                (FUTURE_SIGNATURE_OTHER, FUTURE_SIGNATURE_LEFT),
            ),
        ),
    )

    typed_controls: list[Stage11DControl] = []
    for name, candidate in (
        ("wrong_event_correspondence", corrupted_event),
        ("wrong_lapse_jacobian", corrupted_jacobian),
        ("wrong_outcome_correspondence", corrupted_outcome),
    ):
        validation = stage11d_validate_measurement_context(
            candidate, continuation_id, atol=max(atol, STAGE11A_ATOL)
        )
        typed_controls.append(
            Stage11DControl(
                control=name,
                classification=(STAGE11D_TYPED_REJECTION if not validation.valid else "inconclusive"),
                rejected=not validation.valid,
                typed_rejection=not validation.valid,
                numerical_witness_residual=0.0,
                rejection_reasons=validation.rejection_reasons,
            )
        )

    matrix_residual, probability_residual = _wrong_normalization_witness(atol=atol)
    normalization_rejected = bool(
        matrix_residual > 10 * atol and probability_residual > 10 * atol
    )
    typed_controls.append(
        Stage11DControl(
            control="wrong_normalization",
            classification=(
                STAGE11D_NORMALIZATION_REJECTION if normalization_rejected else "inconclusive"
            ),
            rejected=normalization_rejected,
            typed_rejection=False,
            numerical_witness_residual=probability_residual,
            rejection_reasons=("misaligned_chart_normalization",),
        )
    )
    return tuple(typed_controls)


def _selector_free_weighted_schema() -> bool:
    names = {item.name for item in fields(Stage11DWeightedPublicView)}
    forbidden = {
        "selected_continuation",
        "selected_continuation_id",
        "selector",
        "hidden_selector",
        "modal_type",
        "model_type",
        "belief_weights",
        "extension_weights",
    }
    return not bool(names & forbidden)


def stage11d_diagnostics(*, atol: float = DEFAULT_ATOL) -> Stage11DDiagnostics:
    epistemic, ontic = canonical_stage9c_models(selected_id="h_L")
    carrier = epistemic.carrier
    parameterizations = canonical_stage11a_positive_family()
    continuation_ids = tuple(item.continuation_id for item in carrier.continuations)
    views = canonical_stage11d_measurement_views()

    grouped: dict[str, list[Stage11DMeasurementView]] = {item: [] for item in continuation_ids}
    for view in views:
        grouped[view.continuation_id].append(view)

    max_reparam_probability = 0.0
    max_reference_probability = 0.0
    max_sum = 0.0
    minimum_probability = float("inf")
    maximum_probability = -float("inf")
    max_completeness = 0.0
    minimum_effect = float("inf")
    minimum_normalization = float("inf")
    minimum_denominator = float("inf")
    for continuation_id, items in grouped.items():
        reference_view = next(
            item for item in items if item.parameterization_id == STAGE11A_IDENTITY
        )
        continuation = continuation_by_id(carrier, continuation_id)
        stage10_reference = continuation_future_signature_probabilities(
            carrier, continuation, atol=atol
        )
        for item in items:
            max_reparam_probability = max(
                max_reparam_probability,
                _probability_residual(reference_view.probabilities, item.probabilities),
            )
            max_reference_probability = max(
                max_reference_probability,
                _probability_residual(stage10_reference, item.probabilities),
            )
            max_sum = max(max_sum, item.probability_sum_residual)
            values = tuple(value for _, value in item.probabilities)
            minimum_probability = min(minimum_probability, min(values))
            maximum_probability = max(maximum_probability, max(values))
            max_completeness = max(max_completeness, item.completeness_residual)
            minimum_effect = min(minimum_effect, item.minimum_effect_eigenvalue)
            minimum_normalization = min(
                minimum_normalization, item.minimum_normalization_eigenvalue
            )
            minimum_denominator = min(
                minimum_denominator, item.normalization_denominator
            )

    anchor_raw_count = len({item.anchor_parameter_value for item in views})
    target_raw_count = len({item.target_parameter_value for item in views})

    weighted_e = [
        stage11d_weighted_public_view(epistemic, item.parameterization_id, atol=atol)
        for item in parameterizations
    ]
    weighted_o = [
        stage11d_weighted_public_view(ontic, item.parameterization_id, atol=atol)
        for item in parameterizations
    ]
    uniform = matched_uniform_weights(carrier)
    swapped_epistemic = make_stage9_epistemic_model(
        carrier,
        continuation_by_id(carrier, "h_R"),
        uniform,
        atol=atol,
    )
    weighted_swap = [
        stage11d_weighted_public_view(swapped_epistemic, item.parameterization_id, atol=atol)
        for item in parameterizations
    ]
    weighted_reference = next(
        item for item in weighted_e if item.parameterization_id == STAGE11A_IDENTITY
    )
    max_weighted_reparam = max(
        _probability_residual(weighted_reference.next_probabilities, item.next_probabilities)
        for item in weighted_e
    )
    matched_modal = all(
        _weighted_payload_close(left, right, atol=10 * atol)
        for left, right in zip(weighted_e, weighted_o, strict=True)
    )
    hidden_swap = all(
        _weighted_payload_close(left, right, atol=10 * atol)
        for left, right in zip(weighted_e, weighted_swap, strict=True)
    )
    privileged_e = privileged_stage9_modal_diagnostic(epistemic)
    privileged_o = privileged_stage9_modal_diagnostic(ontic)
    privileged_distinct = bool(
        privileged_e.selected_complete_continuation_present
        and not privileged_o.selected_complete_continuation_present
        and privileged_e.semantic_type != privileged_o.semantic_type
    )

    evidence = Stage9Evidence(FUTURE_SIGNATURE_LEFT)
    posterior_views = [
        stage11d_posterior_view(
            epistemic, ontic, evidence, item.parameterization_id, atol=atol
        )
        for item in parameterizations
    ]
    posterior_reference = next(
        item for item in posterior_views if item.parameterization_id == STAGE11A_IDENTITY
    )
    max_e_posterior = max(
        _posterior_residual(
            posterior_reference.epistemic_posterior_weights,
            item.epistemic_posterior_weights,
        )
        for item in posterior_views
    )
    max_o_posterior = max(
        _posterior_residual(
            posterior_reference.ontic_posterior_weights,
            item.ontic_posterior_weights,
        )
        for item in posterior_views
    )
    max_eo_posterior = max(
        _posterior_residual(
            item.epistemic_posterior_weights, item.ontic_posterior_weights
        )
        for item in posterior_views
    )
    selection_preserved = all(
        item.epistemic_selected_continuation_id
        == epistemic.selected_continuation.continuation_id
        for item in posterior_views
    )
    ontic_selector_free = all(
        item.ontic_no_selected_complete_continuation_datum
        for item in posterior_views
    )

    controls = stage11d_controls(atol=atol)
    matrix_residual, normalization_probability_residual = _wrong_normalization_witness(
        atol=atol
    )
    rejected_controls = sum(item.rejected for item in controls)

    tolerance = 1e-9
    criteria = bool(
        len(parameterizations) == 4
        and len(continuation_ids) == 2
        and len(views) == 8
        and all(item.family_id == STAGE10_REFERENCE_FAMILY_ID for item in views)
        and all(item.prediction_anchor == CURRENT_EVENT for item in views)
        and all(item.target_event == UPPER_EVENT for item in views)
        and all(item.internal_clock == STAGE11D_REFERENCE_CLOCK for item in views)
        and all(item.internal_clock_index == UPPER_EVENT for item in views)
        and all(item.outcome_ids == _EXPECTED_OUTCOMES for item in views)
        and anchor_raw_count > 1
        and target_raw_count > 1
        and len({item.anchor_physical_event_id for item in views}) == 1
        and len({item.target_physical_event_id for item in views}) == 1
        and views[0].anchor_physical_event_id != views[0].target_physical_event_id
        and max_reparam_probability <= tolerance
        and max_reference_probability <= tolerance
        and max_sum <= tolerance
        and minimum_probability >= -tolerance
        and maximum_probability <= 1.0 + tolerance
        and max_completeness <= tolerance
        and minimum_effect >= -tolerance
        and minimum_normalization > tolerance
        and minimum_denominator > tolerance
        and max_weighted_reparam <= tolerance
        and matched_modal
        and hidden_swap
        and privileged_distinct
        and _selector_free_weighted_schema()
        and max_e_posterior <= tolerance
        and max_o_posterior <= tolerance
        and max_eo_posterior <= tolerance
        and selection_preserved
        and ontic_selector_free
        and len(controls) == 4
        and rejected_controls == 4
        and matrix_residual > tolerance
        and normalization_probability_residual > tolerance
    )

    return Stage11DDiagnostics(
        parameterization_count=len(parameterizations),
        continuation_count=len(continuation_ids),
        measurement_view_count=len(views),
        probability_evaluation_count=sum(len(item.probabilities) for item in views),
        max_per_continuation_reparameterization_probability_residual=max_reparam_probability,
        max_stage10_reference_probability_residual=max_reference_probability,
        max_probability_sum_residual=max_sum,
        minimum_probability=minimum_probability,
        maximum_probability=maximum_probability,
        max_completeness_residual=max_completeness,
        minimum_effect_eigenvalue=minimum_effect,
        minimum_normalization_eigenvalue=minimum_normalization,
        minimum_normalization_denominator=minimum_denominator,
        anchor_raw_parameter_value_count=anchor_raw_count,
        target_raw_parameter_value_count=target_raw_count,
        weighted_public_view_count=len(weighted_e) + len(weighted_o),
        max_weighted_prediction_reparameterization_residual=max_weighted_reparam,
        matched_epistemic_ontic_public_views_all_parameterizations=matched_modal,
        hidden_hstar_swap_public_views_all_parameterizations=hidden_swap,
        privileged_modal_roles_still_distinct=privileged_distinct,
        public_weighted_schema_selector_free=_selector_free_weighted_schema(),
        posterior_parameterization_count=len(posterior_views),
        max_epistemic_posterior_reparameterization_residual=max_e_posterior,
        max_ontic_posterior_reparameterization_residual=max_o_posterior,
        max_epistemic_ontic_posterior_residual=max_eo_posterior,
        epistemic_hidden_selection_preserved=selection_preserved,
        ontic_updated_selector_free_all_parameterizations=ontic_selector_free,
        control_count=len(controls),
        rejected_control_count=rejected_controls,
        wrong_normalization_matrix_residual=matrix_residual,
        wrong_normalization_probability_residual=normalization_probability_residual,
        criteria_32_38_satisfied=criteria,
    )


def stage11d_summary(*, atol: float = DEFAULT_ATOL) -> dict[str, object]:
    d = stage11d_diagnostics(atol=atol)
    return {
        "stage": "11D",
        "parameterization_count": d.parameterization_count,
        "continuation_count": d.continuation_count,
        "measurement_view_count": d.measurement_view_count,
        "probability_evaluation_count": d.probability_evaluation_count,
        "max_per_continuation_reparameterization_probability_residual": d.max_per_continuation_reparameterization_probability_residual,
        "max_stage10_reference_probability_residual": d.max_stage10_reference_probability_residual,
        "max_probability_sum_residual": d.max_probability_sum_residual,
        "minimum_probability": d.minimum_probability,
        "maximum_probability": d.maximum_probability,
        "max_completeness_residual": d.max_completeness_residual,
        "minimum_effect_eigenvalue": d.minimum_effect_eigenvalue,
        "minimum_normalization_eigenvalue": d.minimum_normalization_eigenvalue,
        "minimum_normalization_denominator": d.minimum_normalization_denominator,
        "anchor_raw_parameter_value_count": d.anchor_raw_parameter_value_count,
        "target_raw_parameter_value_count": d.target_raw_parameter_value_count,
        "max_weighted_prediction_reparameterization_residual": d.max_weighted_prediction_reparameterization_residual,
        "matched_epistemic_ontic_public_views_all_parameterizations": d.matched_epistemic_ontic_public_views_all_parameterizations,
        "hidden_hstar_swap_public_views_all_parameterizations": d.hidden_hstar_swap_public_views_all_parameterizations,
        "posterior_parameterization_count": d.posterior_parameterization_count,
        "max_epistemic_posterior_reparameterization_residual": d.max_epistemic_posterior_reparameterization_residual,
        "max_ontic_posterior_reparameterization_residual": d.max_ontic_posterior_reparameterization_residual,
        "control_count": d.control_count,
        "rejected_control_count": d.rejected_control_count,
        "wrong_normalization_matrix_residual": d.wrong_normalization_matrix_residual,
        "wrong_normalization_probability_residual": d.wrong_normalization_probability_residual,
        "criteria_32_38_satisfied": d.criteria_32_38_satisfied,
        "bounded_result": STAGE11D_COVARIANCE_RESULT if d.criteria_32_38_satisfied else "not_established",
    }
