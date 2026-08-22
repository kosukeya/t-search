"""Stage 9C typed modal models and directional operational underdetermination.

Stage 9A/9B established a constrained continuation family with two physically
inequivalent extensions and a continuation-independent directional record
profile.  Stage 9C keeps that physical carrier fixed and assigns two distinct
modal roles:

    M_E^QR = (QRCarrier, D, h*, q_E)

with one globally selected complete continuation hidden from the public
interface, and

    M_O^QR(D) = (QRCarrier, D, QExt(D), K)

with no selected complete continuation datum.

The public O_QR projection contains current physical data, current record
content, a directional-record interface verified to agree across every carrier
continuation before weighting, and a future-signature prediction.  It never
reads the epistemic hidden selector.

Operational equality in this finite declared interface is an underdetermination
result.  It is not evidence that nature is ontically open, fixed, or becoming.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from math import isclose, isfinite
from typing import Sequence

import numpy as np

from .stage5_clock_change import DEFAULT_ATOL
from .stage7_history import UPPER_EVENT
from .stage7_record import TARGET_LABEL, TARGET_POSITION, target_memory_joint_distribution
from .stage8_continuations import QuantumContinuation
from .stage9_substrate import (
    CANONICAL_ANCHOR,
    assess_stage9_direction,
    reduced_stage9_state,
    stage9_continuation_equivalent,
    stage9_extension_set,
)

FUTURE_SIGNATURE_LEFT = "future_signature_left"
FUTURE_SIGNATURE_OTHER = "future_signature_other"


@dataclass(frozen=True, slots=True)
class Stage9DirectionalCarrier:
    current_anchor: int
    continuations: tuple[QuantumContinuation, ...]


@dataclass(frozen=True, slots=True)
class Stage9EpistemicModel:
    """M_E^QR=(QRCarrier,D,h*,q_E)."""

    carrier: Stage9DirectionalCarrier
    selected_continuation: QuantumContinuation
    belief_weights: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class Stage9OnticExtensionModel:
    """M_O^QR(D)=(QRCarrier,D,QExt(D),K), with no selector field."""

    carrier: Stage9DirectionalCarrier
    extension_weights: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class DirectionalRecordInterface:
    lower_information: float
    upper_information: float
    lower_accuracy: float
    upper_accuracy: float
    record_score: float
    accessibility_score: float
    orientation: str


@dataclass(frozen=True, slots=True)
class Stage9FutureSignatureMeasurement:
    outcome_names: tuple[str, str]
    effects: tuple[np.ndarray, np.ndarray]
    completeness_residual: float
    minimum_effect_eigenvalue: float
    branch_overlap_squared: float


@dataclass(frozen=True, slots=True)
class Stage9QROperationalView:
    """Ontology-neutral Stage 9C public interface O_QR."""

    current_anchor: int
    current_density_matrix: tuple[complex, ...]
    current_record_joint: tuple[float, ...]
    current_record_information: float
    directional_record: DirectionalRecordInterface | None
    next_outcomes: tuple[str, ...]
    next_probabilities: tuple[tuple[str, float], ...]
    observed_outcome: str | None = None


@dataclass(frozen=True, slots=True)
class Stage9QROperationalComparison:
    equal: bool
    current_anchor_equal: bool
    density_equal: bool
    record_joint_equal: bool
    record_information_equal: bool
    directional_record_equal: bool
    next_outcomes_equal: bool
    next_probabilities_equal: bool
    observed_outcome_equal: bool


@dataclass(frozen=True, slots=True)
class Stage9PrivilegedModalDiagnostic:
    semantic_type: str
    selected_continuation_id: str | None
    selected_complete_continuation_present: bool


@dataclass(frozen=True, slots=True)
class Stage9OnticSelectorAudit:
    field_names: tuple[str, ...]
    forbidden_selector_fields: tuple[str, ...]
    direct_continuation_fields: tuple[str, ...]
    arbitrary_instance_dict_present: bool
    all_qext_members_represented: bool
    full_weight_support: bool
    no_selected_complete_continuation_datum: bool


@dataclass(frozen=True, slots=True)
class Stage9Evidence:
    """Externally supplied evidence.  No branch is sampled internally."""

    outcome: str


@dataclass(frozen=True, slots=True)
class UpdatedStage9EpistemicState:
    source_carrier: Stage9DirectionalCarrier
    current_anchor: int
    observed_outcome: str
    selected_continuation: QuantumContinuation
    posterior_weights: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class UpdatedStage9OnticState:
    source_carrier: Stage9DirectionalCarrier
    current_anchor: int
    observed_outcome: str
    posterior_weights: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class Stage9CUpdateComparison:
    evidence: Stage9Evidence
    before_comparison: Stage9QROperationalComparison
    after_comparison: Stage9QROperationalComparison
    epistemic_selected_before: str
    epistemic_selected_after: str
    epistemic_selected_preserved: bool
    epistemic_posterior_weights: tuple[float, ...]
    ontic_posterior_weights: tuple[float, ...]
    ontic_no_selected_complete_continuation_datum: bool


@dataclass(frozen=True, slots=True)
class Stage9CModalDiagnostics:
    qext_size: int
    shared_carrier_identity: bool
    matched_operational_equal: bool
    selected_swap_operational_equal: bool
    privileged_structures_distinct: bool
    hidden_selected_absent_from_operational_schema: bool
    directional_interface_present: bool
    directional_interface_shared_across_continuations: bool
    directional_record_score: float
    directional_accessibility_score: float
    canonical_next_probabilities: tuple[tuple[str, float], ...]
    weight_mismatch_changes_prediction: bool
    mismatched_next_probabilities: tuple[tuple[str, float], ...]
    weight_mismatch_preserves_current_directional_data: bool
    ontic_no_selected_complete_continuation_datum: bool
    ontic_full_weight_support: bool
    update_before_equal: bool
    update_after_equal: bool
    update_anchor_advanced: bool
    epistemic_selected_preserved: bool
    posterior_weights_match: bool
    updated_ontic_no_selected_complete_continuation_datum: bool
    measurement_completeness_residual: float
    measurement_minimum_effect_eigenvalue: float
    future_branch_overlap_squared: float


Stage9CModel = Stage9EpistemicModel | Stage9OnticExtensionModel
UpdatedStage9CModel = UpdatedStage9EpistemicState | UpdatedStage9OnticState
AnyStage9CModel = Stage9CModel | UpdatedStage9CModel


def canonical_stage9_directional_carrier() -> Stage9DirectionalCarrier:
    continuations = stage9_extension_set(CANONICAL_ANCHOR)
    if len(continuations) < 2:
        raise ValueError("Stage 9C carrier requires nontrivial QExt")
    ids = tuple(item.continuation_id for item in continuations)
    if len(set(ids)) != len(ids):
        raise ValueError("Stage 9C continuation ids must be unique")
    return Stage9DirectionalCarrier(CANONICAL_ANCHOR, continuations)


def continuation_by_id(
    carrier: Stage9DirectionalCarrier, continuation_id: str
) -> QuantumContinuation:
    matches = [item for item in carrier.continuations if item.continuation_id == continuation_id]
    if len(matches) != 1:
        raise ValueError(f"unknown or ambiguous Stage 9C continuation id {continuation_id!r}")
    return matches[0]


def _equivalent_index(
    carrier: Stage9DirectionalCarrier,
    continuation: QuantumContinuation,
    *,
    atol: float = DEFAULT_ATOL,
) -> int:
    matches = [
        index
        for index, representative in enumerate(carrier.continuations)
        if stage9_continuation_equivalent(representative, continuation, atol=atol)
    ]
    if len(matches) != 1:
        raise ValueError("selected continuation must belong to exactly one Stage 9C class")
    return matches[0]


def _validate_weights(
    carrier: Stage9DirectionalCarrier,
    weights: Sequence[float],
    *,
    name: str,
) -> tuple[float, ...]:
    frozen = tuple(float(weight) for weight in weights)
    if len(frozen) != len(carrier.continuations):
        raise ValueError(f"{name} must provide one weight per continuation class")
    if any(not isfinite(weight) or weight < 0.0 for weight in frozen):
        raise ValueError(f"{name} must be finite and non-negative")
    total = sum(frozen)
    if not isclose(total, 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError(f"{name} must sum to 1; got {total}")
    return frozen


def matched_uniform_weights(carrier: Stage9DirectionalCarrier) -> tuple[float, ...]:
    count = len(carrier.continuations)
    return tuple(1.0 / count for _ in carrier.continuations)


def make_stage9_epistemic_model(
    carrier: Stage9DirectionalCarrier,
    selected_continuation: QuantumContinuation,
    belief_weights: Sequence[float],
    *,
    atol: float = DEFAULT_ATOL,
) -> Stage9EpistemicModel:
    weights = _validate_weights(carrier, belief_weights, name="q_E")
    selected_index = _equivalent_index(carrier, selected_continuation, atol=atol)
    if weights[selected_index] <= 0.0:
        raise ValueError("selected continuation must retain positive epistemic support")
    return Stage9EpistemicModel(
        carrier,
        carrier.continuations[selected_index],
        weights,
    )


def make_stage9_ontic_model(
    carrier: Stage9DirectionalCarrier,
    extension_weights: Sequence[float],
) -> Stage9OnticExtensionModel:
    return Stage9OnticExtensionModel(
        carrier,
        _validate_weights(carrier, extension_weights, name="K"),
    )


def canonical_stage9c_models(
    *, selected_id: str = "h_L"
) -> tuple[Stage9EpistemicModel, Stage9OnticExtensionModel]:
    carrier = canonical_stage9_directional_carrier()
    weights = matched_uniform_weights(carrier)
    epistemic = make_stage9_epistemic_model(
        carrier, continuation_by_id(carrier, selected_id), weights
    )
    ontic = make_stage9_ontic_model(carrier, weights)
    return epistemic, ontic


def selected_stage9_continuation(model: Stage9EpistemicModel) -> QuantumContinuation:
    """Privileged test-only diagnostic, outside O_QR."""

    return model.selected_continuation


def _model_weights(model: Stage9CModel) -> tuple[float, ...]:
    if isinstance(model, Stage9EpistemicModel):
        return model.belief_weights
    if isinstance(model, Stage9OnticExtensionModel):
        return model.extension_weights
    raise TypeError("unsupported Stage 9C model")


def ontic_selector_audit(model: Stage9OnticExtensionModel) -> Stage9OnticSelectorAudit:
    names = tuple(field.name for field in fields(model))
    forbidden_tokens = (
        "selected",
        "selector",
        "seed",
        "precomputed",
        "latent_branch",
    )
    forbidden = tuple(
        name for name in names if any(token in name.lower() for token in forbidden_tokens)
    )
    direct = tuple(
        name for name in names if isinstance(getattr(model, name), QuantumContinuation)
    )
    arbitrary_dict = hasattr(model, "__dict__")
    all_represented = len(model.carrier.continuations) == len(stage9_extension_set(CANONICAL_ANCHOR))
    full_support = all(weight > 0.0 for weight in model.extension_weights)
    no_selector = bool(
        not forbidden
        and not direct
        and not arbitrary_dict
        and all_represented
        and not hasattr(model, "selected_continuation")
        and not hasattr(model, "selector")
        and not hasattr(model, "seed")
    )
    return Stage9OnticSelectorAudit(
        field_names=names,
        forbidden_selector_fields=forbidden,
        direct_continuation_fields=direct,
        arbitrary_instance_dict_present=arbitrary_dict,
        all_qext_members_represented=all_represented,
        full_weight_support=full_support,
        no_selected_complete_continuation_datum=no_selector,
    )


def privileged_stage9_modal_diagnostic(model: Stage9CModel) -> Stage9PrivilegedModalDiagnostic:
    if isinstance(model, Stage9EpistemicModel):
        return Stage9PrivilegedModalDiagnostic(
            "epistemic-selected-continuation",
            model.selected_continuation.continuation_id,
            True,
        )
    if isinstance(model, Stage9OnticExtensionModel):
        return Stage9PrivilegedModalDiagnostic(
            "ontic-extension-no-selected-continuation",
            None,
            False,
        )
    raise TypeError("unsupported Stage 9C model")


def _normalized_state(vector: np.ndarray) -> np.ndarray:
    state = np.asarray(vector, dtype=np.complex128)
    norm = float(np.linalg.norm(state))
    if norm <= DEFAULT_ATOL:
        raise ValueError("Stage 9C state must have nonzero norm")
    return state / norm


def canonical_stage9_future_signature_measurement(
    carrier: Stage9DirectionalCarrier,
    *,
    atol: float = DEFAULT_ATOL,
) -> Stage9FutureSignatureMeasurement:
    if len(carrier.continuations) != 2:
        raise ValueError("canonical Stage 9C measurement requires exactly two continuations")
    left = _normalized_state(reduced_stage9_state(carrier.continuations[0], UPPER_EVENT))
    right = _normalized_state(reduced_stage9_state(carrier.continuations[1], UPPER_EVENT))
    overlap_squared = float(abs(np.vdot(left, right)) ** 2)
    if overlap_squared >= 1.0 - atol:
        raise ValueError("Stage 9C future continuation rays must be operationally distinguishable")
    p_left = np.outer(left, left.conj())
    identity = np.eye(left.size, dtype=np.complex128)
    p_other = identity - p_left
    effects = (p_left, p_other)
    completeness = float(np.linalg.norm(sum(effects) - identity))
    minimum_eigenvalue = min(
        float(np.min(np.linalg.eigvalsh((effect + effect.conj().T) / 2.0)))
        for effect in effects
    )
    if completeness > atol or minimum_eigenvalue < -atol:
        raise ValueError("Stage 9C future-signature effects are not a valid measurement")
    return Stage9FutureSignatureMeasurement(
        (FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_OTHER),
        effects,
        completeness,
        minimum_eigenvalue,
        overlap_squared,
    )


def continuation_future_signature_probabilities(
    carrier: Stage9DirectionalCarrier,
    continuation: QuantumContinuation,
    *,
    atol: float = DEFAULT_ATOL,
) -> tuple[tuple[str, float], ...]:
    _equivalent_index(carrier, continuation, atol=atol)
    measurement = canonical_stage9_future_signature_measurement(carrier, atol=atol)
    state = _normalized_state(reduced_stage9_state(continuation, UPPER_EVENT))
    result: list[tuple[str, float]] = []
    for name, effect in zip(measurement.outcome_names, measurement.effects, strict=True):
        probability = float(np.real(np.vdot(state, effect @ state)))
        if probability < -atol or probability > 1.0 + atol:
            raise ValueError("Stage 9C Born probability outside [0,1]")
        result.append((name, min(1.0, max(0.0, probability))))
    if not isclose(sum(value for _, value in result), 1.0, rel_tol=0.0, abs_tol=10 * atol):
        raise ValueError("Stage 9C Born probabilities must sum to one")
    return tuple(result)


def _predict_next_probabilities(
    model: Stage9CModel,
    *,
    atol: float = DEFAULT_ATOL,
) -> tuple[tuple[str, float], ...]:
    likelihoods = tuple(
        dict(continuation_future_signature_probabilities(model.carrier, item, atol=atol))
        for item in model.carrier.continuations
    )
    weights = _model_weights(model)
    names = canonical_stage9_future_signature_measurement(model.carrier, atol=atol).outcome_names
    prediction = tuple(
        (
            name,
            float(
                sum(
                    weight * likelihood[name]
                    for weight, likelihood in zip(weights, likelihoods, strict=True)
                )
            ),
        )
        for name in names
    )
    if not isclose(sum(value for _, value in prediction), 1.0, rel_tol=0.0, abs_tol=10 * atol):
        raise ValueError("Stage 9C predicted probabilities must sum to one")
    return prediction


def _density_from_ensemble(states: Sequence[np.ndarray], weights: Sequence[float]) -> np.ndarray:
    if not states or len(states) != len(weights):
        raise ValueError("Stage 9C ensemble must be nonempty and aligned")
    density = np.zeros((states[0].size, states[0].size), dtype=np.complex128)
    for weight, state in zip(weights, states, strict=True):
        normalized = _normalized_state(state)
        density += float(weight) * np.outer(normalized, normalized.conj())
    trace = float(np.real(np.trace(density)))
    if trace <= DEFAULT_ATOL:
        raise ValueError("Stage 9C ensemble density must have positive trace")
    return density / trace


def _record_joint_from_ensemble(states: Sequence[np.ndarray], weights: Sequence[float]) -> np.ndarray:
    joint = np.zeros((2, 2), dtype=float)
    for weight, state in zip(weights, states, strict=True):
        joint += float(weight) * target_memory_joint_distribution(
            _normalized_state(state), position=TARGET_POSITION, label=TARGET_LABEL
        )
    total = float(np.sum(joint))
    if total <= DEFAULT_ATOL:
        raise ValueError("Stage 9C record joint has zero mass")
    return joint / total


def _mutual_information(joint: np.ndarray) -> float:
    probabilities = np.asarray(joint, dtype=float)
    probabilities = probabilities / np.sum(probabilities)
    px = np.sum(probabilities, axis=1, keepdims=True)
    pm = np.sum(probabilities, axis=0, keepdims=True)
    independent = px @ pm
    mask = probabilities > 0.0
    return float(
        np.sum(probabilities[mask] * np.log2(probabilities[mask] / independent[mask]))
    )


def _shared_directional_record_interface(
    carrier: Stage9DirectionalCarrier,
    *,
    atol: float = DEFAULT_ATOL,
) -> DirectionalRecordInterface:
    assessments = tuple(assess_stage9_direction(item) for item in carrier.continuations)
    reference = assessments[0]
    numeric_fields = (
        "lower_information",
        "upper_information",
        "lower_accuracy",
        "upper_accuracy",
        "record_score",
        "accessibility_score",
    )
    for item in assessments[1:]:
        if item.orientation != reference.orientation:
            raise ValueError("Stage 9C carrier continuations disagree on record orientation")
        for name in numeric_fields:
            if not isclose(
                float(getattr(item, name)),
                float(getattr(reference, name)),
                rel_tol=0.0,
                abs_tol=atol,
            ):
                raise ValueError("Stage 9C carrier continuations disagree on directional interface")
    return DirectionalRecordInterface(
        lower_information=reference.lower_information,
        upper_information=reference.upper_information,
        lower_accuracy=reference.lower_accuracy,
        upper_accuracy=reference.upper_accuracy,
        record_score=reference.record_score,
        accessibility_score=reference.accessibility_score,
        orientation=reference.orientation,
    )


def _current_ensemble(model: AnyStage9CModel) -> tuple[tuple[np.ndarray, ...], tuple[float, ...]]:
    if isinstance(model, (Stage9EpistemicModel, Stage9OnticExtensionModel)):
        states = tuple(
            reduced_stage9_state(item, model.carrier.current_anchor)
            for item in model.carrier.continuations
        )
        reference = states[0]
        for state in states[1:]:
            if np.linalg.norm(state - reference) > DEFAULT_ATOL:
                raise ValueError("Stage 9C carrier does not share one current Actuality")
        return (reference,), (1.0,)
    if isinstance(model, (UpdatedStage9EpistemicState, UpdatedStage9OnticState)):
        states = tuple(
            reduced_stage9_state(item, model.current_anchor)
            for item in model.source_carrier.continuations
        )
        return states, model.posterior_weights
    raise TypeError("unsupported Stage 9C state")


def stage9_qr_operational_view(
    model: AnyStage9CModel,
    *,
    atol: float = DEFAULT_ATOL,
) -> Stage9QROperationalView:
    states, weights = _current_ensemble(model)
    density = _density_from_ensemble(states, weights)
    joint = _record_joint_from_ensemble(states, weights)
    information = _mutual_information(joint)

    if isinstance(model, (Stage9EpistemicModel, Stage9OnticExtensionModel)):
        current_anchor = model.carrier.current_anchor
        directional = _shared_directional_record_interface(model.carrier, atol=atol)
        next_probabilities = _predict_next_probabilities(model, atol=atol)
        next_outcomes = tuple(name for name, _ in next_probabilities)
        observed = None
    else:
        current_anchor = model.current_anchor
        directional = None
        next_probabilities = ()
        next_outcomes = ()
        observed = model.observed_outcome

    return Stage9QROperationalView(
        current_anchor=current_anchor,
        current_density_matrix=tuple(complex(value) for value in density.reshape(-1)),
        current_record_joint=tuple(float(value) for value in joint.reshape(-1)),
        current_record_information=float(information),
        directional_record=directional,
        next_outcomes=next_outcomes,
        next_probabilities=next_probabilities,
        observed_outcome=observed,
    )


def _arrays_close(left: Sequence[complex | float], right: Sequence[complex | float], *, atol: float) -> bool:
    return len(left) == len(right) and bool(
        np.allclose(np.asarray(left), np.asarray(right), atol=atol, rtol=0.0)
    )


def _directional_close(
    left: DirectionalRecordInterface | None,
    right: DirectionalRecordInterface | None,
    *,
    atol: float,
) -> bool:
    if left is None or right is None:
        return left is right
    if left.orientation != right.orientation:
        return False
    return all(
        isclose(float(a), float(b), rel_tol=0.0, abs_tol=atol)
        for a, b in (
            (left.lower_information, right.lower_information),
            (left.upper_information, right.upper_information),
            (left.lower_accuracy, right.lower_accuracy),
            (left.upper_accuracy, right.upper_accuracy),
            (left.record_score, right.record_score),
            (left.accessibility_score, right.accessibility_score),
        )
    )


def compare_stage9_qr_views(
    left: Stage9QROperationalView,
    right: Stage9QROperationalView,
    *,
    atol: float = DEFAULT_ATOL,
) -> Stage9QROperationalComparison:
    left_prob = dict(left.next_probabilities)
    right_prob = dict(right.next_probabilities)
    probability_equal = bool(
        set(left_prob) == set(right_prob)
        and all(
            isclose(left_prob[name], right_prob[name], rel_tol=0.0, abs_tol=atol)
            for name in left_prob
        )
    )
    checks = dict(
        current_anchor_equal=left.current_anchor == right.current_anchor,
        density_equal=_arrays_close(left.current_density_matrix, right.current_density_matrix, atol=atol),
        record_joint_equal=_arrays_close(left.current_record_joint, right.current_record_joint, atol=atol),
        record_information_equal=isclose(
            left.current_record_information, right.current_record_information, rel_tol=0.0, abs_tol=atol
        ),
        directional_record_equal=_directional_close(left.directional_record, right.directional_record, atol=atol),
        next_outcomes_equal=left.next_outcomes == right.next_outcomes,
        next_probabilities_equal=probability_equal,
        observed_outcome_equal=left.observed_outcome == right.observed_outcome,
    )
    return Stage9QROperationalComparison(equal=all(checks.values()), **checks)


def _outcome_likelihoods(
    carrier: Stage9DirectionalCarrier,
    evidence: Stage9Evidence,
    *,
    atol: float = DEFAULT_ATOL,
) -> tuple[float, ...]:
    measurement = canonical_stage9_future_signature_measurement(carrier, atol=atol)
    if evidence.outcome not in measurement.outcome_names:
        raise ValueError("Stage 9C evidence outcome is outside the declared Next_QR set")
    return tuple(
        dict(continuation_future_signature_probabilities(carrier, item, atol=atol))[evidence.outcome]
        for item in carrier.continuations
    )


def _bayes_condition(
    prior: Sequence[float], likelihoods: Sequence[float], *, atol: float = DEFAULT_ATOL
) -> tuple[float, ...]:
    raw = tuple(
        float(weight) * float(likelihood)
        for weight, likelihood in zip(prior, likelihoods, strict=True)
    )
    total = sum(raw)
    if total <= atol:
        raise ValueError("Stage 9C evidence has zero predictive support")
    return tuple(value / total for value in raw)


def update_stage9_epistemic_model(
    model: Stage9EpistemicModel,
    evidence: Stage9Evidence,
    *,
    atol: float = DEFAULT_ATOL,
) -> UpdatedStage9EpistemicState:
    likelihoods = _outcome_likelihoods(model.carrier, evidence, atol=atol)
    selected_index = _equivalent_index(model.carrier, model.selected_continuation, atol=atol)
    if likelihoods[selected_index] <= atol:
        raise ValueError("Stage 9C evidence contradicts the hidden selected continuation")
    return UpdatedStage9EpistemicState(
        source_carrier=model.carrier,
        current_anchor=UPPER_EVENT,
        observed_outcome=evidence.outcome,
        selected_continuation=model.selected_continuation,
        posterior_weights=_bayes_condition(model.belief_weights, likelihoods, atol=atol),
    )


def update_stage9_ontic_model(
    model: Stage9OnticExtensionModel,
    evidence: Stage9Evidence,
    *,
    atol: float = DEFAULT_ATOL,
) -> UpdatedStage9OnticState:
    likelihoods = _outcome_likelihoods(model.carrier, evidence, atol=atol)
    return UpdatedStage9OnticState(
        source_carrier=model.carrier,
        current_anchor=UPPER_EVENT,
        observed_outcome=evidence.outcome,
        posterior_weights=_bayes_condition(model.extension_weights, likelihoods, atol=atol),
    )


def updated_ontic_selector_audit(model: UpdatedStage9OnticState) -> bool:
    names = tuple(field.name for field in fields(model))
    forbidden_tokens = ("selected", "selector", "seed", "precomputed", "latent_branch")
    return bool(
        not any(any(token in name.lower() for token in forbidden_tokens) for name in names)
        and not any(isinstance(getattr(model, name), QuantumContinuation) for name in names)
        and not hasattr(model, "__dict__")
        and not hasattr(model, "selected_continuation")
    )


def compare_common_stage9_evidence(
    epistemic: Stage9EpistemicModel,
    ontic: Stage9OnticExtensionModel,
    evidence: Stage9Evidence,
    *,
    atol: float = DEFAULT_ATOL,
) -> Stage9CUpdateComparison:
    if epistemic.carrier is not ontic.carrier:
        raise ValueError("Stage 9C common update requires the exact same carrier object")
    before = compare_stage9_qr_views(
        stage9_qr_operational_view(epistemic, atol=atol),
        stage9_qr_operational_view(ontic, atol=atol),
        atol=atol,
    )
    selected_before = epistemic.selected_continuation
    updated_e = update_stage9_epistemic_model(epistemic, evidence, atol=atol)
    updated_o = update_stage9_ontic_model(ontic, evidence, atol=atol)
    after = compare_stage9_qr_views(
        stage9_qr_operational_view(updated_e, atol=atol),
        stage9_qr_operational_view(updated_o, atol=atol),
        atol=atol,
    )
    return Stage9CUpdateComparison(
        evidence=evidence,
        before_comparison=before,
        after_comparison=after,
        epistemic_selected_before=selected_before.continuation_id,
        epistemic_selected_after=updated_e.selected_continuation.continuation_id,
        epistemic_selected_preserved=stage9_continuation_equivalent(
            selected_before, updated_e.selected_continuation, atol=atol
        ),
        epistemic_posterior_weights=updated_e.posterior_weights,
        ontic_posterior_weights=updated_o.posterior_weights,
        ontic_no_selected_complete_continuation_datum=updated_ontic_selector_audit(updated_o),
    )


def stage9c_modal_diagnostics(*, atol: float = DEFAULT_ATOL) -> Stage9CModalDiagnostics:
    epistemic, ontic = canonical_stage9c_models(selected_id="h_L")
    carrier = epistemic.carrier
    weights = matched_uniform_weights(carrier)
    epistemic_right = make_stage9_epistemic_model(
        carrier, continuation_by_id(carrier, "h_R"), weights, atol=atol
    )

    view_e = stage9_qr_operational_view(epistemic, atol=atol)
    view_o = stage9_qr_operational_view(ontic, atol=atol)
    view_right = stage9_qr_operational_view(epistemic_right, atol=atol)
    matched = compare_stage9_qr_views(view_e, view_o, atol=atol)
    selected_swap = compare_stage9_qr_views(view_e, view_right, atol=atol)

    mismatch = make_stage9_ontic_model(carrier, (0.75, 0.25))
    mismatch_view = stage9_qr_operational_view(mismatch, atol=atol)
    mismatch_comparison = compare_stage9_qr_views(view_e, mismatch_view, atol=atol)

    privileged_distinct = (
        privileged_stage9_modal_diagnostic(epistemic)
        != privileged_stage9_modal_diagnostic(ontic)
    )
    schema_names = {field.name for field in fields(Stage9QROperationalView)}
    hidden_absent = all(
        forbidden not in schema_names
        for forbidden in (
            "selected_continuation",
            "selected_history",
            "selector",
            "model_type",
            "belief_weights",
            "extension_weights",
        )
    )
    audit = ontic_selector_audit(ontic)
    directional = view_e.directional_record
    if directional is None:
        raise ValueError("Stage 9C canonical pre-update interface must expose R_direction")

    evidence = Stage9Evidence(FUTURE_SIGNATURE_LEFT)
    update = compare_common_stage9_evidence(epistemic, ontic, evidence, atol=atol)
    measurement = canonical_stage9_future_signature_measurement(carrier, atol=atol)
    posterior_match = bool(
        np.allclose(
            np.asarray(update.epistemic_posterior_weights),
            np.asarray(update.ontic_posterior_weights),
            atol=atol,
            rtol=0.0,
        )
    )

    assessments = tuple(assess_stage9_direction(item) for item in carrier.continuations)
    direction_shared = all(
        item.orientation == assessments[0].orientation
        and isclose(item.record_score, assessments[0].record_score, rel_tol=0.0, abs_tol=atol)
        and isclose(
            item.accessibility_score,
            assessments[0].accessibility_score,
            rel_tol=0.0,
            abs_tol=atol,
        )
        for item in assessments[1:]
    )

    return Stage9CModalDiagnostics(
        qext_size=len(carrier.continuations),
        shared_carrier_identity=epistemic.carrier is ontic.carrier,
        matched_operational_equal=matched.equal,
        selected_swap_operational_equal=selected_swap.equal,
        privileged_structures_distinct=privileged_distinct,
        hidden_selected_absent_from_operational_schema=hidden_absent,
        directional_interface_present=directional.orientation != "none",
        directional_interface_shared_across_continuations=direction_shared,
        directional_record_score=directional.record_score,
        directional_accessibility_score=directional.accessibility_score,
        canonical_next_probabilities=view_e.next_probabilities,
        weight_mismatch_changes_prediction=bool(
            mismatch_comparison.current_anchor_equal
            and mismatch_comparison.density_equal
            and mismatch_comparison.record_joint_equal
            and mismatch_comparison.record_information_equal
            and mismatch_comparison.directional_record_equal
            and mismatch_comparison.next_outcomes_equal
            and not mismatch_comparison.next_probabilities_equal
            and not mismatch_comparison.equal
        ),
        mismatched_next_probabilities=mismatch_view.next_probabilities,
        weight_mismatch_preserves_current_directional_data=bool(
            mismatch_comparison.current_anchor_equal
            and mismatch_comparison.density_equal
            and mismatch_comparison.record_joint_equal
            and mismatch_comparison.record_information_equal
            and mismatch_comparison.directional_record_equal
        ),
        ontic_no_selected_complete_continuation_datum=audit.no_selected_complete_continuation_datum,
        ontic_full_weight_support=audit.full_weight_support,
        update_before_equal=update.before_comparison.equal,
        update_after_equal=update.after_comparison.equal,
        update_anchor_advanced=UPPER_EVENT > carrier.current_anchor,
        epistemic_selected_preserved=update.epistemic_selected_preserved,
        posterior_weights_match=posterior_match,
        updated_ontic_no_selected_complete_continuation_datum=(
            update.ontic_no_selected_complete_continuation_datum
        ),
        measurement_completeness_residual=measurement.completeness_residual,
        measurement_minimum_effect_eigenvalue=measurement.minimum_effect_eigenvalue,
        future_branch_overlap_squared=measurement.branch_overlap_squared,
    )


def stage9c_summary() -> dict[str, object]:
    diagnostics = stage9c_modal_diagnostics()
    return {
        "stage": "9C",
        "status": "typed modal models operationally underdetermined on directional carrier",
        "interface": (
            "O_QR=(current density,R_content,R_direction/R_access,Next_QR,"
            "future-signature probabilities,observed evidence)"
        ),
        "diagnostics": asdict(diagnostics),
        "exit_criteria_satisfied": tuple(range(24, 31)),
        "next": "Stage 9D — continuation-aware clock transport",
        "guards": (
            "operational directional equality != modal/ontological identity",
            "directional record arrow != ontological future openness",
            "directional record arrow != ontological becoming",
            "hidden h* diagnostic != operational access to h*",
            "matched numerical q_E and K != matched probability semantics",
            "explicit evidence update != ontological becoming",
            "weight sensitivity != selected-continuation observability",
            "control of V_weights != determination of V_semantics",
        ),
    }
