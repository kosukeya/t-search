"""Stage 11E clock-change x external-reparameterization compatibility.

Stage 11D established future-measurement reparameterization covariance at one
fixed Stage 10 internal chart.  Stage 11E combines the two already-tested
representation changes without promoting either into a new dynamical law:

    G_{rho->sigma}: external parameterization transport,
    C_{X->Y}:       genuine Stage 10 internal-clock transport.

The declared test is the typed product square

    C o G ~= G o C

on the finite family of four positive external parameterizations and all nine
A/B/C clock/readout nodes.  The clock leg reuses the genuine continuation-aware
Stage 10C dual transport; the parameter leg changes only Stage 11 Xi/context
representation metadata while preserving the typed physical event roles.

The stage checks relational O/event payloads, continuation-specific measurement
forms and probabilities, weighted/modal public outputs, and common-evidence
posteriors.  A deliberately mislabeled-but-untransported measurement chart is
used as a noncommuting wrong-path control.

Commutation here is compatibility of the declared finite typed product
construction.  It is not general covariance, an interaction law between the two
representations, a proof of eternalism, or a refutation of ontological becoming.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from functools import lru_cache
from itertools import permutations, product
from math import isclose

import numpy as np

from .stage5_clock_change import DEFAULT_ATOL, SUBSYSTEMS
from .stage9_modal import (
    FUTURE_SIGNATURE_LEFT,
    Stage9CModel,
    Stage9EpistemicModel,
    Stage9Evidence,
    Stage9OnticExtensionModel,
    canonical_stage9c_models,
    continuation_by_id,
    make_stage9_epistemic_model,
    matched_uniform_weights,
)
from .stage9_transport import stage9_clock_change_support_matrix
from .stage10_modal import (
    Stage10EPosteriorView,
    Stage10EPublicMeasurementView,
    stage10e_posterior_view,
    stage10e_public_measurement_view,
)
from .stage10_probability import stage10d_chart_probabilities
from .stage10_transport import (
    Stage10ChartMeasurement,
    canonical_stage10c_charts,
    transport_stage10_chart_measurement,
)
from .stage11_lift import Stage11TypedArchitecture, stage11c_public_architecture
from .stage11_parametrized import (
    STAGE11A_ATOL,
    STAGE11A_POSITIVE_PARAMETERIZATION_IDS,
)

STAGE11E_RESULT = (
    "Stage 11E clock-change x parameterization compatibility on the frozen finite family = established"
)
STAGE11E_WRONG_PATH_CLASSIFICATION = "noncommuting_wrong_clock_path_detected"
STAGE11E_REPARAMETERIZATION_SEMANTICS = (
    "G changes external parameterization/Xi metadata at fixed typed physical events; "
    "it does not act as a Stage 10 internal-clock map"
)
STAGE11E_CLOCK_SEMANTICS = (
    "C is the genuine continuation-aware Stage 10C dual measurement transport; "
    "it does not redefine the external parameterization"
)

ClockNode = tuple[str, int]


@dataclass(frozen=True, slots=True)
class Stage11EReparameterizationTransport:
    source_parameterization_id: str
    target_parameterization_id: str
    anchor_physical_event_id: str
    target_physical_event_id: str
    source_anchor_parameter_value: float
    target_anchor_parameter_value: float
    source_target_parameter_value: float
    target_target_parameter_value: float
    source_anchor_lapse: float
    target_anchor_lapse: float
    source_target_lapse: float
    target_target_lapse: float
    event_correspondence: tuple[tuple[str, str], ...]
    continuation_class_correspondence: tuple[tuple[str, str], ...]
    outcome_correspondence: tuple[tuple[str, str], ...]
    semantics: str
    valid: bool


@dataclass(frozen=True, slots=True)
class Stage11EClockTransport:
    continuation_id: str
    source_clock: str
    source_index: int
    target_clock: str
    target_index: int
    matrix: np.ndarray
    semantics: str
    valid: bool


@dataclass(frozen=True, slots=True)
class Stage11EEventView:
    parameterization_id: str
    internal_clock: str
    internal_clock_index: int
    anchor_physical_event_id: str
    target_physical_event_id: str
    anchor_parameter_value: float
    target_parameter_value: float
    anchor_relational_clock_value: float
    target_relational_clock_value: float
    anchor_q_value: float
    target_q_value: float


@dataclass(frozen=True, slots=True)
class Stage11EMeasurementView:
    parameterization_id: str
    continuation_id: str
    internal_clock: str
    internal_clock_index: int
    anchor_physical_event_id: str
    target_physical_event_id: str
    anchor_parameter_value: float
    target_parameter_value: float
    chart: Stage10ChartMeasurement
    probabilities: tuple[tuple[str, float], ...]


@dataclass(frozen=True, slots=True)
class Stage11EWeightedView:
    parameterization_id: str
    internal_clock: str
    internal_clock_index: int
    anchor_physical_event_id: str
    target_physical_event_id: str
    anchor_parameter_value: float
    target_parameter_value: float
    public_view: Stage10EPublicMeasurementView


@dataclass(frozen=True, slots=True)
class Stage11EPosteriorView:
    parameterization_id: str
    internal_clock: str
    internal_clock_index: int
    anchor_physical_event_id: str
    target_physical_event_id: str
    anchor_parameter_value: float
    target_parameter_value: float
    posterior_view: Stage10EPosteriorView


@dataclass(frozen=True, slots=True)
class Stage11EWrongPathControl:
    classification: str
    detected: bool
    continuation_id: str
    source_parameterization_id: str
    target_parameterization_id: str
    source_clock: str
    source_index: int
    target_clock: str
    target_index: int
    normalization_residual: float
    effect_residual: float
    probability_residual: float


@dataclass(frozen=True, slots=True)
class Stage11EDiagnostics:
    parameterization_count: int
    clock_node_count: int
    reparameterization_transport_count: int
    continuation_count: int
    clock_transport_count: int
    event_square_count: int
    measurement_square_count: int
    weighted_square_count: int
    posterior_square_count: int
    all_reparameterization_transports_valid: bool
    all_clock_transports_valid: bool
    nontrivial_reparameterization_transport_count: int
    nontrivial_clock_transport_count: int
    max_event_path_residual: float
    max_measurement_path_normalization_residual: float
    max_measurement_path_effect_residual: float
    max_measurement_direct_target_normalization_residual: float
    max_measurement_direct_target_effect_residual: float
    max_measurement_probability_path_residual: float
    max_measurement_direct_target_probability_residual: float
    max_weighted_path_residual: float
    max_matched_modal_endpoint_residual: float
    max_hidden_hstar_endpoint_residual: float
    max_epistemic_posterior_path_residual: float
    max_ontic_posterior_path_residual: float
    max_epistemic_ontic_posterior_endpoint_residual: float
    epistemic_hidden_selection_preserved: bool
    ontic_selector_free_all_endpoints: bool
    wrong_path_control_detected: bool
    wrong_path_normalization_residual: float
    wrong_path_effect_residual: float
    wrong_path_probability_residual: float
    criteria_39_43_satisfied: bool


def _clock_nodes() -> tuple[ClockNode, ...]:
    return tuple((clock, index) for clock in SUBSYSTEMS for index in range(3))


def _distinct_clock_edges() -> tuple[tuple[str, int, str, int], ...]:
    return tuple(
        (source_clock, source_index, target_clock, target_index)
        for source_clock in SUBSYSTEMS
        for source_index in range(3)
        for target_clock in SUBSYSTEMS
        if target_clock != source_clock
        for target_index in range(3)
    )


@lru_cache(maxsize=1)
def _models() -> tuple[Stage9EpistemicModel, Stage9OnticExtensionModel, Stage9EpistemicModel]:
    epistemic, ontic = canonical_stage9c_models(selected_id="h_L")
    uniform = matched_uniform_weights(epistemic.carrier)
    swapped = make_stage9_epistemic_model(
        epistemic.carrier,
        continuation_by_id(epistemic.carrier, "h_R"),
        uniform,
        atol=DEFAULT_ATOL,
    )
    return epistemic, ontic, swapped


@lru_cache(maxsize=None)
def _architecture(parameterization_id: str) -> Stage11TypedArchitecture:
    _, ontic, _ = _models()
    return stage11c_public_architecture(ontic, parameterization_id)


def _role_event(architecture: Stage11TypedArchitecture, role: str):
    matches = tuple(item for item in architecture.O.relational_events if item.role == role)
    if len(matches) != 1:
        raise ValueError(f"Stage 11E requires exactly one {role!r} event")
    return matches[0]


@lru_cache(maxsize=1)
def canonical_stage11e_reparameterization_transports() -> tuple[Stage11EReparameterizationTransport, ...]:
    result: list[Stage11EReparameterizationTransport] = []
    for source_id, target_id in permutations(STAGE11A_POSITIVE_PARAMETERIZATION_IDS, 2):
        source = _architecture(source_id)
        target = _architecture(target_id)
        source_anchor = _role_event(source, "prediction_anchor")
        source_target = _role_event(source, "measurement_target")
        target_anchor = _role_event(target, "prediction_anchor")
        target_target = _role_event(target, "measurement_target")
        valid = bool(
            source_anchor.physical_event_id == target_anchor.physical_event_id
            and source_target.physical_event_id == target_target.physical_event_id
            and source.Xi.event_correspondence == target.Xi.event_correspondence
            and source.Xi.continuation_class_correspondence
            == target.Xi.continuation_class_correspondence
            and source.Xi.outcome_correspondence == target.Xi.outcome_correspondence
            and source.Xi.parameterization_id == source_id
            and target.Xi.parameterization_id == target_id
            and source_id != target_id
        )
        result.append(
            Stage11EReparameterizationTransport(
                source_parameterization_id=source_id,
                target_parameterization_id=target_id,
                anchor_physical_event_id=source_anchor.physical_event_id,
                target_physical_event_id=source_target.physical_event_id,
                source_anchor_parameter_value=source.Xi.anchor_parameter_value,
                target_anchor_parameter_value=target.Xi.anchor_parameter_value,
                source_target_parameter_value=source.Xi.target_parameter_value,
                target_target_parameter_value=target.Xi.target_parameter_value,
                source_anchor_lapse=source.Xi.anchor_lapse,
                target_anchor_lapse=target.Xi.anchor_lapse,
                source_target_lapse=source.Xi.target_lapse,
                target_target_lapse=target.Xi.target_lapse,
                event_correspondence=source.Xi.event_correspondence,
                continuation_class_correspondence=source.Xi.continuation_class_correspondence,
                outcome_correspondence=source.Xi.outcome_correspondence,
                semantics=STAGE11E_REPARAMETERIZATION_SEMANTICS,
                valid=valid,
            )
        )
    return tuple(result)


@lru_cache(maxsize=1)
def _chart_lookup() -> dict[tuple[str, str, int], Stage10ChartMeasurement]:
    return {
        (item.continuation_id, item.clock, item.clock_index): item
        for item in canonical_stage10c_charts()
    }


@lru_cache(maxsize=None)
def _clock_transport(
    continuation_id: str,
    source_clock: str,
    source_index: int,
    target_clock: str,
    target_index: int,
) -> Stage11EClockTransport:
    if source_clock == target_clock:
        raise ValueError("Stage 11E clock transport requires distinct clock subsystems")
    epistemic, _, _ = _models()
    continuation = continuation_by_id(epistemic.carrier, continuation_id)
    matrix = stage9_clock_change_support_matrix(
        continuation,
        target_clock,
        target_index,
        source_clock,
        source_index,
    )
    valid = bool(
        matrix.shape == (14, 14)
        and np.linalg.matrix_rank(matrix, tol=DEFAULT_ATOL) == 14
        and np.all(np.isfinite(matrix))
    )
    return Stage11EClockTransport(
        continuation_id=continuation_id,
        source_clock=source_clock,
        source_index=source_index,
        target_clock=target_clock,
        target_index=target_index,
        matrix=matrix,
        semantics=STAGE11E_CLOCK_SEMANTICS,
        valid=valid,
    )


@lru_cache(maxsize=1)
def canonical_stage11e_clock_transports() -> tuple[Stage11EClockTransport, ...]:
    epistemic, _, _ = _models()
    return tuple(
        _clock_transport(
            continuation.continuation_id,
            source_clock,
            source_index,
            target_clock,
            target_index,
        )
        for continuation in epistemic.carrier.continuations
        for source_clock, source_index, target_clock, target_index in _distinct_clock_edges()
    )


def stage11e_event_view(
    parameterization_id: str, clock: str, index: int
) -> Stage11EEventView:
    architecture = _architecture(parameterization_id)
    anchor = _role_event(architecture, "prediction_anchor")
    target = _role_event(architecture, "measurement_target")
    return Stage11EEventView(
        parameterization_id=parameterization_id,
        internal_clock=clock,
        internal_clock_index=index,
        anchor_physical_event_id=anchor.physical_event_id,
        target_physical_event_id=target.physical_event_id,
        anchor_parameter_value=architecture.Xi.anchor_parameter_value,
        target_parameter_value=architecture.Xi.target_parameter_value,
        anchor_relational_clock_value=anchor.clock_value,
        target_relational_clock_value=target.clock_value,
        anchor_q_value=anchor.q_value,
        target_q_value=target.q_value,
    )


def _apply_G_event(view: Stage11EEventView, target_parameterization_id: str) -> Stage11EEventView:
    return stage11e_event_view(
        target_parameterization_id, view.internal_clock, view.internal_clock_index
    )


def _apply_C_event(
    view: Stage11EEventView, target_clock: str, target_index: int
) -> Stage11EEventView:
    return replace(view, internal_clock=target_clock, internal_clock_index=target_index)


def _event_residual(left: Stage11EEventView, right: Stage11EEventView) -> float:
    if (
        left.parameterization_id != right.parameterization_id
        or left.internal_clock != right.internal_clock
        or left.internal_clock_index != right.internal_clock_index
        or left.anchor_physical_event_id != right.anchor_physical_event_id
        or left.target_physical_event_id != right.target_physical_event_id
    ):
        return float("inf")
    values_left = np.asarray(
        (
            left.anchor_parameter_value,
            left.target_parameter_value,
            left.anchor_relational_clock_value,
            left.target_relational_clock_value,
            left.anchor_q_value,
            left.target_q_value,
        ),
        dtype=float,
    )
    values_right = np.asarray(
        (
            right.anchor_parameter_value,
            right.target_parameter_value,
            right.anchor_relational_clock_value,
            right.target_relational_clock_value,
            right.anchor_q_value,
            right.target_q_value,
        ),
        dtype=float,
    )
    return float(np.max(np.abs(values_left - values_right)))


@lru_cache(maxsize=None)
def _transported_chart(
    continuation_id: str,
    source_clock: str,
    source_index: int,
    target_clock: str,
    target_index: int,
) -> Stage10ChartMeasurement:
    epistemic, _, _ = _models()
    continuation = continuation_by_id(epistemic.carrier, continuation_id)
    source = _chart_lookup()[(continuation_id, source_clock, source_index)]
    return transport_stage10_chart_measurement(
        source, continuation, target_clock, target_index
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


def _chart_residual(
    left: Stage10ChartMeasurement,
    right: Stage10ChartMeasurement,
) -> tuple[float, float]:
    if (
        left.family_id != right.family_id
        or left.continuation_id != right.continuation_id
        or left.clock != right.clock
        or left.clock_index != right.clock_index
        or left.prediction_anchor != right.prediction_anchor
        or left.target_event != right.target_event
        or left.class_correspondence != right.class_correspondence
        or left.event_correspondence != right.event_correspondence
        or left.outcome_correspondence != right.outcome_correspondence
    ):
        return float("inf"), float("inf")
    normalization = float(np.linalg.norm(left.normalization_form - right.normalization_form))
    lhs = {item.outcome_id: item for item in left.effects}
    rhs = {item.outcome_id: item for item in right.effects}
    if set(lhs) != set(rhs):
        return normalization, float("inf")
    effect = max(
        float(np.linalg.norm(lhs[name].matrix - rhs[name].matrix))
        for name in lhs
    )
    return normalization, effect


def _measurement_view_from_chart(
    parameterization_id: str,
    continuation_id: str,
    chart: Stage10ChartMeasurement,
) -> Stage11EMeasurementView:
    architecture = _architecture(parameterization_id)
    anchor = _role_event(architecture, "prediction_anchor")
    target = _role_event(architecture, "measurement_target")
    epistemic, _, _ = _models()
    continuation = continuation_by_id(epistemic.carrier, continuation_id)
    probabilities = stage10d_chart_probabilities(continuation, chart, atol=DEFAULT_ATOL)
    return Stage11EMeasurementView(
        parameterization_id=parameterization_id,
        continuation_id=continuation_id,
        internal_clock=chart.clock,
        internal_clock_index=chart.clock_index,
        anchor_physical_event_id=anchor.physical_event_id,
        target_physical_event_id=target.physical_event_id,
        anchor_parameter_value=architecture.Xi.anchor_parameter_value,
        target_parameter_value=architecture.Xi.target_parameter_value,
        chart=chart,
        probabilities=probabilities,
    )


@lru_cache(maxsize=None)
def stage11e_measurement_view(
    parameterization_id: str,
    continuation_id: str,
    clock: str,
    index: int,
) -> Stage11EMeasurementView:
    return _measurement_view_from_chart(
        parameterization_id,
        continuation_id,
        _chart_lookup()[(continuation_id, clock, index)],
    )


def _apply_G_measurement(
    view: Stage11EMeasurementView, target_parameterization_id: str
) -> Stage11EMeasurementView:
    return _measurement_view_from_chart(
        target_parameterization_id, view.continuation_id, view.chart
    )


def _apply_C_measurement(
    view: Stage11EMeasurementView, target_clock: str, target_index: int
) -> Stage11EMeasurementView:
    chart = _transported_chart(
        view.continuation_id,
        view.internal_clock,
        view.internal_clock_index,
        target_clock,
        target_index,
    )
    return _measurement_view_from_chart(
        view.parameterization_id, view.continuation_id, chart
    )


def _weighted_base(model: Stage9CModel, clock: str, index: int) -> Stage10EPublicMeasurementView:
    return stage10e_public_measurement_view(model, clock, index, atol=DEFAULT_ATOL)


def _weighted_payload_residual(
    left: Stage10EPublicMeasurementView,
    right: Stage10EPublicMeasurementView,
) -> float:
    if (
        left.current_event != right.current_event
        or left.clock != right.clock
        or left.clock_index != right.clock_index
        or left.continuation_ids != right.continuation_ids
        or left.orientations != right.orientations
        or left.next_outcomes != right.next_outcomes
    ):
        return float("inf")
    residuals = [
        float(np.max(np.abs(np.asarray(a) - np.asarray(b))))
        for a, b in (
            (left.continuation_weights, right.continuation_weights),
            (left.predictive_density, right.predictive_density),
            (left.directional_record_scores, right.directional_record_scores),
            (
                left.directional_accessibility_scores,
                right.directional_accessibility_scores,
            ),
        )
    ]
    residuals.append(_probability_residual(left.next_probabilities, right.next_probabilities))
    return max(residuals)


def _weighted_model_key(model: Stage9CModel) -> str:
    epistemic, ontic, swapped = _models()
    if model is epistemic:
        return "epistemic"
    if model is ontic:
        return "ontic"
    if model is swapped:
        return "epistemic_swapped"
    raise ValueError("Stage 11E only caches the three canonical matched modal models")


@lru_cache(maxsize=None)
def _weighted_base_cached(model_key: str, clock: str, index: int) -> Stage10EPublicMeasurementView:
    epistemic, ontic, swapped = _models()
    model = {
        "epistemic": epistemic,
        "ontic": ontic,
        "epistemic_swapped": swapped,
    }[model_key]
    return _weighted_base(model, clock, index)


def stage11e_weighted_view(
    model: Stage9CModel, parameterization_id: str, clock: str, index: int
) -> Stage11EWeightedView:
    architecture = stage11c_public_architecture(model, parameterization_id)
    anchor = _role_event(architecture, "prediction_anchor")
    target = _role_event(architecture, "measurement_target")
    base = _weighted_base_cached(_weighted_model_key(model), clock, index)
    return Stage11EWeightedView(
        parameterization_id=parameterization_id,
        internal_clock=clock,
        internal_clock_index=index,
        anchor_physical_event_id=anchor.physical_event_id,
        target_physical_event_id=target.physical_event_id,
        anchor_parameter_value=architecture.Xi.anchor_parameter_value,
        target_parameter_value=architecture.Xi.target_parameter_value,
        public_view=base,
    )


def _apply_G_weighted(
    model: Stage9CModel, view: Stage11EWeightedView, target_parameterization_id: str
) -> Stage11EWeightedView:
    return stage11e_weighted_view(
        model, target_parameterization_id, view.internal_clock, view.internal_clock_index
    )


def _apply_C_weighted(
    model: Stage9CModel, view: Stage11EWeightedView, target_clock: str, target_index: int
) -> Stage11EWeightedView:
    return stage11e_weighted_view(
        model, view.parameterization_id, target_clock, target_index
    )


def _weighted_view_residual(left: Stage11EWeightedView, right: Stage11EWeightedView) -> float:
    if (
        left.parameterization_id != right.parameterization_id
        or left.internal_clock != right.internal_clock
        or left.internal_clock_index != right.internal_clock_index
        or left.anchor_physical_event_id != right.anchor_physical_event_id
        or left.target_physical_event_id != right.target_physical_event_id
    ):
        return float("inf")
    metadata = max(
        abs(left.anchor_parameter_value - right.anchor_parameter_value),
        abs(left.target_parameter_value - right.target_parameter_value),
    )
    return max(metadata, _weighted_payload_residual(left.public_view, right.public_view))


@lru_cache(maxsize=None)
def _posterior_base_cached(clock: str, index: int) -> Stage10EPosteriorView:
    epistemic, ontic, _ = _models()
    return stage10e_posterior_view(
        epistemic,
        ontic,
        Stage9Evidence(FUTURE_SIGNATURE_LEFT),
        clock,
        index,
        atol=DEFAULT_ATOL,
    )


def stage11e_posterior_view(
    parameterization_id: str, clock: str, index: int
) -> Stage11EPosteriorView:
    architecture = _architecture(parameterization_id)
    anchor = _role_event(architecture, "prediction_anchor")
    target = _role_event(architecture, "measurement_target")
    base = _posterior_base_cached(clock, index)
    return Stage11EPosteriorView(
        parameterization_id=parameterization_id,
        internal_clock=clock,
        internal_clock_index=index,
        anchor_physical_event_id=anchor.physical_event_id,
        target_physical_event_id=target.physical_event_id,
        anchor_parameter_value=architecture.Xi.anchor_parameter_value,
        target_parameter_value=architecture.Xi.target_parameter_value,
        posterior_view=base,
    )


def _apply_G_posterior(
    view: Stage11EPosteriorView, target_parameterization_id: str
) -> Stage11EPosteriorView:
    return stage11e_posterior_view(
        target_parameterization_id, view.internal_clock, view.internal_clock_index
    )


def _apply_C_posterior(
    view: Stage11EPosteriorView, target_clock: str, target_index: int
) -> Stage11EPosteriorView:
    return stage11e_posterior_view(
        view.parameterization_id, target_clock, target_index
    )


def _posterior_tuple_residual(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    return float(np.max(np.abs(np.asarray(left, dtype=float) - np.asarray(right, dtype=float))))


def _posterior_view_residual(
    left: Stage11EPosteriorView, right: Stage11EPosteriorView
) -> tuple[float, float]:
    if (
        left.parameterization_id != right.parameterization_id
        or left.internal_clock != right.internal_clock
        or left.internal_clock_index != right.internal_clock_index
        or left.anchor_physical_event_id != right.anchor_physical_event_id
        or left.target_physical_event_id != right.target_physical_event_id
        or left.posterior_view.observed_outcome != right.posterior_view.observed_outcome
        or left.posterior_view.epistemic_selected_continuation_id
        != right.posterior_view.epistemic_selected_continuation_id
        or left.posterior_view.ontic_no_selected_complete_continuation_datum
        != right.posterior_view.ontic_no_selected_complete_continuation_datum
    ):
        return float("inf"), float("inf")
    metadata = max(
        abs(left.anchor_parameter_value - right.anchor_parameter_value),
        abs(left.target_parameter_value - right.target_parameter_value),
    )
    epistemic = max(
        metadata,
        _posterior_tuple_residual(
            left.posterior_view.epistemic_posterior_weights,
            right.posterior_view.epistemic_posterior_weights,
        ),
    )
    ontic = max(
        metadata,
        _posterior_tuple_residual(
            left.posterior_view.ontic_posterior_weights,
            right.posterior_view.ontic_posterior_weights,
        ),
    )
    return epistemic, ontic


def _mislabeled_untransported_chart(
    source: Stage10ChartMeasurement, target_clock: str, target_index: int
) -> Stage10ChartMeasurement:
    return replace(
        source,
        clock=target_clock,
        clock_index=target_index,
        effects=tuple(
            replace(effect, clock=target_clock, clock_index=target_index)
            for effect in source.effects
        ),
    )


def stage11e_wrong_path_control(*, atol: float = DEFAULT_ATOL) -> Stage11EWrongPathControl:
    source_parameterization_id = "cubic"
    target_parameterization_id = "hyperbolic"
    continuation_id = "h_L"
    source_clock, source_index = "A", 0
    target_clock, target_index = "B", 1
    source = _chart_lookup()[(continuation_id, source_clock, source_index)]
    wrong = _mislabeled_untransported_chart(source, target_clock, target_index)
    correct = _chart_lookup()[(continuation_id, target_clock, target_index)]
    normalization_residual, effect_residual = _chart_residual(wrong, correct)
    epistemic, _, _ = _models()
    continuation = continuation_by_id(epistemic.carrier, continuation_id)
    wrong_probabilities = stage10d_chart_probabilities(continuation, wrong, atol=atol)
    correct_probabilities = stage10d_chart_probabilities(continuation, correct, atol=atol)
    probability_residual = _probability_residual(wrong_probabilities, correct_probabilities)
    detected = bool(
        normalization_residual > 10 * atol
        and effect_residual > 10 * atol
        and probability_residual > 10 * atol
    )
    return Stage11EWrongPathControl(
        classification=(
            STAGE11E_WRONG_PATH_CLASSIFICATION if detected else "inconclusive"
        ),
        detected=detected,
        continuation_id=continuation_id,
        source_parameterization_id=source_parameterization_id,
        target_parameterization_id=target_parameterization_id,
        source_clock=source_clock,
        source_index=source_index,
        target_clock=target_clock,
        target_index=target_index,
        normalization_residual=normalization_residual,
        effect_residual=effect_residual,
        probability_residual=probability_residual,
    )


def stage11e_diagnostics(*, atol: float = DEFAULT_ATOL) -> Stage11EDiagnostics:
    epistemic, ontic, swapped = _models()
    parameter_ids = STAGE11A_POSITIVE_PARAMETERIZATION_IDS
    reparam_transports = canonical_stage11e_reparameterization_transports()
    clock_transports = canonical_stage11e_clock_transports()
    continuation_ids = tuple(item.continuation_id for item in epistemic.carrier.continuations)
    clock_edges = _distinct_clock_edges()
    parameter_edges = tuple(permutations(parameter_ids, 2))

    nontrivial_reparam = sum(
        (
            not isclose(
                item.source_anchor_parameter_value,
                item.target_anchor_parameter_value,
                rel_tol=0.0,
                abs_tol=STAGE11A_ATOL,
            )
            or not isclose(
                item.source_target_parameter_value,
                item.target_target_parameter_value,
                rel_tol=0.0,
                abs_tol=STAGE11A_ATOL,
            )
        )
        for item in reparam_transports
    )
    nontrivial_clock = sum(
        float(np.linalg.norm(item.matrix - np.eye(item.matrix.shape[0]))) > 10 * atol
        for item in clock_transports
    )

    max_event_path = 0.0
    event_square_count = 0
    for source_parameterization_id, target_parameterization_id in parameter_edges:
        for source_clock, source_index, target_clock, target_index in clock_edges:
            start = stage11e_event_view(
                source_parameterization_id, source_clock, source_index
            )
            path_gc = _apply_C_event(
                _apply_G_event(start, target_parameterization_id),
                target_clock,
                target_index,
            )
            path_cg = _apply_G_event(
                _apply_C_event(start, target_clock, target_index),
                target_parameterization_id,
            )
            direct = stage11e_event_view(
                target_parameterization_id, target_clock, target_index
            )
            max_event_path = max(
                max_event_path,
                _event_residual(path_gc, path_cg),
                _event_residual(path_gc, direct),
                _event_residual(path_cg, direct),
            )
            event_square_count += 1

    max_path_normalization = 0.0
    max_path_effect = 0.0
    max_direct_normalization = 0.0
    max_direct_effect = 0.0
    max_probability_path = 0.0
    max_probability_direct = 0.0
    measurement_square_count = 0
    for continuation_id in continuation_ids:
        for source_parameterization_id, target_parameterization_id in parameter_edges:
            for source_clock, source_index, target_clock, target_index in clock_edges:
                start = stage11e_measurement_view(
                    source_parameterization_id,
                    continuation_id,
                    source_clock,
                    source_index,
                )
                path_gc = _apply_C_measurement(
                    _apply_G_measurement(start, target_parameterization_id),
                    target_clock,
                    target_index,
                )
                path_cg = _apply_G_measurement(
                    _apply_C_measurement(start, target_clock, target_index),
                    target_parameterization_id,
                )
                direct = stage11e_measurement_view(
                    target_parameterization_id,
                    continuation_id,
                    target_clock,
                    target_index,
                )
                path_norm, path_effect = _chart_residual(path_gc.chart, path_cg.chart)
                direct_norm_a, direct_effect_a = _chart_residual(path_gc.chart, direct.chart)
                direct_norm_b, direct_effect_b = _chart_residual(path_cg.chart, direct.chart)
                max_path_normalization = max(max_path_normalization, path_norm)
                max_path_effect = max(max_path_effect, path_effect)
                max_direct_normalization = max(
                    max_direct_normalization, direct_norm_a, direct_norm_b
                )
                max_direct_effect = max(
                    max_direct_effect, direct_effect_a, direct_effect_b
                )
                max_probability_path = max(
                    max_probability_path,
                    _probability_residual(path_gc.probabilities, path_cg.probabilities),
                )
                max_probability_direct = max(
                    max_probability_direct,
                    _probability_residual(path_gc.probabilities, direct.probabilities),
                    _probability_residual(path_cg.probabilities, direct.probabilities),
                )
                measurement_square_count += 1

    max_weighted_path = 0.0
    max_matched_modal = 0.0
    max_hidden_hstar = 0.0
    weighted_square_count = 0
    max_e_posterior_path = 0.0
    max_o_posterior_path = 0.0
    max_eo_endpoint = 0.0
    selection_preserved = True
    ontic_selector_free = True
    posterior_square_count = 0

    for source_parameterization_id, target_parameterization_id in parameter_edges:
        for source_clock, source_index, target_clock, target_index in clock_edges:
            start_e = stage11e_weighted_view(
                epistemic, source_parameterization_id, source_clock, source_index
            )
            path_e_gc = _apply_C_weighted(
                epistemic,
                _apply_G_weighted(epistemic, start_e, target_parameterization_id),
                target_clock,
                target_index,
            )
            path_e_cg = _apply_G_weighted(
                epistemic,
                _apply_C_weighted(epistemic, start_e, target_clock, target_index),
                target_parameterization_id,
            )
            direct_e = stage11e_weighted_view(
                epistemic, target_parameterization_id, target_clock, target_index
            )
            direct_o = stage11e_weighted_view(
                ontic, target_parameterization_id, target_clock, target_index
            )
            direct_swap = stage11e_weighted_view(
                swapped, target_parameterization_id, target_clock, target_index
            )
            max_weighted_path = max(
                max_weighted_path,
                _weighted_view_residual(path_e_gc, path_e_cg),
                _weighted_view_residual(path_e_gc, direct_e),
                _weighted_view_residual(path_e_cg, direct_e),
            )
            max_matched_modal = max(
                max_matched_modal,
                _weighted_view_residual(direct_e, direct_o),
            )
            max_hidden_hstar = max(
                max_hidden_hstar,
                _weighted_view_residual(direct_e, direct_swap),
            )
            weighted_square_count += 1

            start_p = stage11e_posterior_view(
                source_parameterization_id, source_clock, source_index
            )
            path_p_gc = _apply_C_posterior(
                _apply_G_posterior(start_p, target_parameterization_id),
                target_clock,
                target_index,
            )
            path_p_cg = _apply_G_posterior(
                _apply_C_posterior(start_p, target_clock, target_index),
                target_parameterization_id,
            )
            direct_p = stage11e_posterior_view(
                target_parameterization_id, target_clock, target_index
            )
            e_residual, o_residual = _posterior_view_residual(path_p_gc, path_p_cg)
            e_direct_a, o_direct_a = _posterior_view_residual(path_p_gc, direct_p)
            e_direct_b, o_direct_b = _posterior_view_residual(path_p_cg, direct_p)
            max_e_posterior_path = max(
                max_e_posterior_path, e_residual, e_direct_a, e_direct_b
            )
            max_o_posterior_path = max(
                max_o_posterior_path, o_residual, o_direct_a, o_direct_b
            )
            max_eo_endpoint = max(
                max_eo_endpoint,
                _posterior_tuple_residual(
                    direct_p.posterior_view.epistemic_posterior_weights,
                    direct_p.posterior_view.ontic_posterior_weights,
                ),
            )
            selection_preserved = bool(
                selection_preserved
                and direct_p.posterior_view.epistemic_selected_continuation_id
                == epistemic.selected_continuation.continuation_id
            )
            ontic_selector_free = bool(
                ontic_selector_free
                and direct_p.posterior_view.ontic_no_selected_complete_continuation_datum
            )
            posterior_square_count += 1

    wrong = stage11e_wrong_path_control(atol=atol)
    tolerance = 1e-9
    criteria = bool(
        len(parameter_ids) == 4
        and len(_clock_nodes()) == 9
        and len(reparam_transports) == 12
        and all(item.valid for item in reparam_transports)
        and nontrivial_reparam > 0
        and len(continuation_ids) == 2
        and len(clock_transports) == 108
        and all(item.valid for item in clock_transports)
        and nontrivial_clock > 0
        and event_square_count == 648
        and measurement_square_count == 1296
        and weighted_square_count == 648
        and posterior_square_count == 648
        and max_event_path <= tolerance
        and max_path_normalization <= tolerance
        and max_path_effect <= tolerance
        and max_direct_normalization <= tolerance
        and max_direct_effect <= tolerance
        and max_probability_path <= tolerance
        and max_probability_direct <= tolerance
        and max_weighted_path <= tolerance
        and max_matched_modal <= tolerance
        and max_hidden_hstar <= tolerance
        and max_e_posterior_path <= tolerance
        and max_o_posterior_path <= tolerance
        and max_eo_endpoint <= tolerance
        and selection_preserved
        and ontic_selector_free
        and wrong.detected
    )
    return Stage11EDiagnostics(
        parameterization_count=len(parameter_ids),
        clock_node_count=len(_clock_nodes()),
        reparameterization_transport_count=len(reparam_transports),
        continuation_count=len(continuation_ids),
        clock_transport_count=len(clock_transports),
        event_square_count=event_square_count,
        measurement_square_count=measurement_square_count,
        weighted_square_count=weighted_square_count,
        posterior_square_count=posterior_square_count,
        all_reparameterization_transports_valid=all(item.valid for item in reparam_transports),
        all_clock_transports_valid=all(item.valid for item in clock_transports),
        nontrivial_reparameterization_transport_count=nontrivial_reparam,
        nontrivial_clock_transport_count=nontrivial_clock,
        max_event_path_residual=max_event_path,
        max_measurement_path_normalization_residual=max_path_normalization,
        max_measurement_path_effect_residual=max_path_effect,
        max_measurement_direct_target_normalization_residual=max_direct_normalization,
        max_measurement_direct_target_effect_residual=max_direct_effect,
        max_measurement_probability_path_residual=max_probability_path,
        max_measurement_direct_target_probability_residual=max_probability_direct,
        max_weighted_path_residual=max_weighted_path,
        max_matched_modal_endpoint_residual=max_matched_modal,
        max_hidden_hstar_endpoint_residual=max_hidden_hstar,
        max_epistemic_posterior_path_residual=max_e_posterior_path,
        max_ontic_posterior_path_residual=max_o_posterior_path,
        max_epistemic_ontic_posterior_endpoint_residual=max_eo_endpoint,
        epistemic_hidden_selection_preserved=selection_preserved,
        ontic_selector_free_all_endpoints=ontic_selector_free,
        wrong_path_control_detected=wrong.detected,
        wrong_path_normalization_residual=wrong.normalization_residual,
        wrong_path_effect_residual=wrong.effect_residual,
        wrong_path_probability_residual=wrong.probability_residual,
        criteria_39_43_satisfied=criteria,
    )


def stage11e_summary(*, atol: float = DEFAULT_ATOL) -> dict[str, object]:
    d = stage11e_diagnostics(atol=atol)
    return {
        "stage": "11E",
        "criteria_39_43_satisfied": d.criteria_39_43_satisfied,
        "parameterization_count": d.parameterization_count,
        "clock_node_count": d.clock_node_count,
        "reparameterization_transport_count": d.reparameterization_transport_count,
        "clock_transport_count": d.clock_transport_count,
        "event_square_count": d.event_square_count,
        "measurement_square_count": d.measurement_square_count,
        "weighted_square_count": d.weighted_square_count,
        "posterior_square_count": d.posterior_square_count,
        "max_event_path_residual": d.max_event_path_residual,
        "max_measurement_path_normalization_residual": d.max_measurement_path_normalization_residual,
        "max_measurement_path_effect_residual": d.max_measurement_path_effect_residual,
        "max_measurement_direct_target_normalization_residual": d.max_measurement_direct_target_normalization_residual,
        "max_measurement_direct_target_effect_residual": d.max_measurement_direct_target_effect_residual,
        "max_measurement_probability_path_residual": d.max_measurement_probability_path_residual,
        "max_measurement_direct_target_probability_residual": d.max_measurement_direct_target_probability_residual,
        "max_weighted_path_residual": d.max_weighted_path_residual,
        "max_epistemic_posterior_path_residual": d.max_epistemic_posterior_path_residual,
        "max_ontic_posterior_path_residual": d.max_ontic_posterior_path_residual,
        "wrong_path_control_detected": d.wrong_path_control_detected,
        "wrong_path_normalization_residual": d.wrong_path_normalization_residual,
        "wrong_path_effect_residual": d.wrong_path_effect_residual,
        "wrong_path_probability_residual": d.wrong_path_probability_residual,
        "bounded_result": STAGE11E_RESULT if d.criteria_39_43_satisfied else "not_established",
        "guards": (
            "internal-clock covariance != reparameterization covariance",
            "commuting typed product square != independent interaction law",
            "commuting typed diagram != general covariance",
            "path-independent future probabilities != future actuality",
            "path-independent evidence update != ontological becoming",
            "finite typed parametrized covariance != general covariance",
        ),
    }
