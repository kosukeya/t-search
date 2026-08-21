"""Stage 8C operational underdetermination and explicit quantum update.

Stage 8B placed two type-distinct modal models on the same executable
continuation carrier. Stage 8C freezes an ontology-neutral operational
interface and applies one explicit piece of future evidence to both models.

A fixed future-signature projective measurement is built from the two
physically orthogonal Stage 8A e2 reduced states. Each continuation supplies a
Born likelihood, while q_E or K enters only as an outer mixture weight. The
hidden epistemic selected continuation h* is never read by the operational
projection.

The update receives explicit evidence and never samples a branch internally.
The epistemic update preserves h* and conditions q_E. The ontic-extension
update conditions K and advances to terminal e2 without adding a hidden
selected-continuation field.

Operational equality under this declared finite interface is underdetermination,
not modal or ontological identity.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from math import isclose
from typing import Sequence

import numpy as np

from .stage5_clock_change import DEFAULT_ATOL
from .stage7_history import UPPER_EVENT
from .stage7_record import (
    TARGET_LABEL,
    TARGET_POSITION,
    target_memory_joint_distribution,
)
from .stage8_continuations import (
    QuantumContinuation,
    continuation_equivalent,
    quantum_extension_set,
    reduced_continuation_state,
)
from .stage8_modal import (
    EpistemicQuantumModel,
    OnticQuantumExtensionModel,
    QuantumContinuationCarrier,
    canonical_stage8b_models,
    continuation_by_id,
    make_epistemic_quantum_model,
    make_ontic_quantum_extension_model,
    matched_uniform_weights,
    selected_quantum_continuation,
)

FUTURE_SIGNATURE_0 = "future_signature_0"
FUTURE_SIGNATURE_1 = "future_signature_1"
FUTURE_SIGNATURE_REMAINDER = "future_signature_remainder"


@dataclass(frozen=True, slots=True)
class FutureSignatureMeasurement:
    outcome_names: tuple[str, str, str]
    effects: tuple[np.ndarray, np.ndarray, np.ndarray]
    completeness_residual: float
    orthogonality_residual: float
    minimum_effect_eigenvalue: float


@dataclass(frozen=True, slots=True)
class QuantumOperationalView:
    """Full Stage 8C ontology-neutral interface O_Q."""

    current_anchor: int
    current_density_matrix: tuple[complex, ...]
    current_record_joint: tuple[float, ...]
    current_record_information: float
    next_outcomes: tuple[str, ...]
    next_probabilities: tuple[tuple[str, float], ...]
    observed_outcome: str | None = None


@dataclass(frozen=True, slots=True)
class QuantumOperationalComparison:
    equal: bool
    current_anchor_equal: bool
    density_equal: bool
    record_joint_equal: bool
    record_information_equal: bool
    next_outcomes_equal: bool
    next_probabilities_equal: bool
    observed_outcome_equal: bool


@dataclass(frozen=True, slots=True)
class PrivilegedQuantumModalDiagnostic:
    semantic_type: str
    selected_continuation_id: str | None
    selected_complete_continuation_present: bool


@dataclass(frozen=True, slots=True)
class QuantumEvidence:
    """Explicit externally supplied evidence; this object performs no sampling."""

    outcome: str


@dataclass(frozen=True, slots=True)
class UpdatedEpistemicQuantumState:
    source_carrier: QuantumContinuationCarrier
    current_anchor: int
    observed_outcome: str
    selected_continuation: QuantumContinuation
    posterior_weights: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class UpdatedOnticQuantumState:
    """Evidence-conditioned ontic state with no selected-future field."""

    source_carrier: QuantumContinuationCarrier
    current_anchor: int
    observed_outcome: str
    posterior_weights: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class UpdatedOnticSelectorAudit:
    field_names: tuple[str, ...]
    forbidden_selector_fields: tuple[str, ...]
    direct_continuation_fields: tuple[str, ...]
    arbitrary_instance_dict_present: bool
    no_selected_complete_continuation_datum: bool


@dataclass(frozen=True, slots=True)
class Stage8CUpdateComparison:
    evidence: QuantumEvidence
    epistemic_before: QuantumOperationalView
    ontic_before: QuantumOperationalView
    before_comparison: QuantumOperationalComparison
    epistemic_after: QuantumOperationalView
    ontic_after: QuantumOperationalView
    after_comparison: QuantumOperationalComparison
    epistemic_selected_before: str
    epistemic_selected_after: str
    epistemic_selected_preserved: bool
    epistemic_posterior_weights: tuple[float, ...]
    ontic_posterior_weights: tuple[float, ...]
    ontic_remaining_qext_size: int
    ontic_no_selected_complete_continuation_datum: bool


@dataclass(frozen=True, slots=True)
class Stage8COperationalDiagnostics:
    qext_size: int
    matched_operational_equal: bool
    selected_swap_operational_equal: bool
    privileged_structures_distinct: bool
    hidden_selected_absent_from_operational_schema: bool
    canonical_next_probabilities: tuple[tuple[str, float], ...]
    weight_mismatch_changes_prediction: bool
    mismatched_next_probabilities: tuple[tuple[str, float], ...]
    update_before_equal: bool
    update_after_equal: bool
    update_anchor_advanced: bool
    update_outcome_equal: bool
    epistemic_selected_preserved: bool
    epistemic_posterior_weights: tuple[float, ...]
    ontic_posterior_weights: tuple[float, ...]
    ontic_posterior_pruned: bool
    ontic_remaining_qext_size: int
    ontic_no_selected_complete_continuation_datum: bool
    same_density_with_distinct_modal_structure: bool
    same_born_prediction_with_distinct_modal_structure: bool
    current_state_has_multiple_coherent_amplitudes: bool
    superposition_does_not_select_modal_semantics: bool
    state_and_born_data_do_not_select_modal_semantics: bool
    measurement_completeness_residual: float
    measurement_orthogonality_residual: float
    minimum_effect_eigenvalue: float


Stage8CModel = EpistemicQuantumModel | OnticQuantumExtensionModel
UpdatedStage8CModel = UpdatedEpistemicQuantumState | UpdatedOnticQuantumState
AnyStage8CModel = Stage8CModel | UpdatedStage8CModel


def _normalized_state(vector: np.ndarray) -> np.ndarray:
    state = np.asarray(vector, dtype=np.complex128)
    norm = float(np.linalg.norm(state))
    if norm <= DEFAULT_ATOL:
        raise ValueError("quantum state must have nonzero norm")
    return state / norm


def canonical_future_signature_measurement(
    carrier: QuantumContinuationCarrier,
    *,
    atol: float = DEFAULT_ATOL,
) -> FutureSignatureMeasurement:
    """Project onto the two canonical physical e2 rays plus their complement."""

    if len(carrier.continuations) != 2:
        raise ValueError("canonical Stage 8C measurement requires exactly two QExt members")
    states = tuple(
        _normalized_state(reduced_continuation_state(item, UPPER_EVENT))
        for item in carrier.continuations
    )
    if abs(np.vdot(states[0], states[1])) > atol:
        raise ValueError("canonical Stage 8C future states must be orthogonal")

    p0 = np.outer(states[0], states[0].conj())
    p1 = np.outer(states[1], states[1].conj())
    identity = np.eye(states[0].size, dtype=np.complex128)
    remainder = identity - p0 - p1
    effects = (p0, p1, remainder)
    completeness = float(np.linalg.norm(sum(effects) - identity))
    orthogonality = float(np.linalg.norm(p0 @ p1))
    minimum_eigenvalue = min(
        float(np.min(np.linalg.eigvalsh((effect + effect.conj().T) / 2.0)))
        for effect in effects
    )
    if completeness > atol or orthogonality > atol or minimum_eigenvalue < -atol:
        raise ValueError("future-signature effects do not define the declared measurement")
    return FutureSignatureMeasurement(
        outcome_names=(
            FUTURE_SIGNATURE_0,
            FUTURE_SIGNATURE_1,
            FUTURE_SIGNATURE_REMAINDER,
        ),
        effects=effects,
        completeness_residual=completeness,
        orthogonality_residual=orthogonality,
        minimum_effect_eigenvalue=minimum_eigenvalue,
    )


def continuation_future_signature_probabilities(
    carrier: QuantumContinuationCarrier,
    continuation: QuantumContinuation,
    *,
    atol: float = DEFAULT_ATOL,
) -> tuple[tuple[str, float], ...]:
    if not any(
        continuation_equivalent(continuation, member, atol=atol)
        for member in carrier.continuations
    ):
        raise ValueError("continuation must belong to the declared Stage 8C carrier")
    measurement = canonical_future_signature_measurement(carrier, atol=atol)
    state = _normalized_state(reduced_continuation_state(continuation, UPPER_EVENT))
    probabilities: list[tuple[str, float]] = []
    for name, effect in zip(measurement.outcome_names, measurement.effects, strict=True):
        value = float(np.real(np.vdot(state, effect @ state)))
        if value < -atol or value > 1.0 + atol:
            raise ValueError("Born probability lies outside [0,1]")
        probabilities.append((name, min(1.0, max(0.0, value))))
    total = sum(value for _, value in probabilities)
    if not isclose(total, 1.0, rel_tol=0.0, abs_tol=10 * atol):
        raise ValueError("future-signature Born probabilities must sum to one")
    return tuple(probabilities)


def _active_next_outcomes(
    carrier: QuantumContinuationCarrier,
    *,
    atol: float = DEFAULT_ATOL,
) -> tuple[str, ...]:
    distributions = tuple(
        dict(continuation_future_signature_probabilities(carrier, item, atol=atol))
        for item in carrier.continuations
    )
    names = canonical_future_signature_measurement(carrier, atol=atol).outcome_names
    return tuple(
        name for name in names if any(dist[name] > atol for dist in distributions)
    )


def _model_weights(model: Stage8CModel) -> tuple[float, ...]:
    if isinstance(model, EpistemicQuantumModel):
        return model.belief_weights
    if isinstance(model, OnticQuantumExtensionModel):
        return model.extension_weights
    raise TypeError("unsupported pre-update Stage 8C model")


def _predict_next_probabilities(
    model: Stage8CModel,
    *,
    atol: float = DEFAULT_ATOL,
) -> tuple[tuple[str, float], ...]:
    active = _active_next_outcomes(model.carrier, atol=atol)
    likelihoods = tuple(
        dict(continuation_future_signature_probabilities(model.carrier, item, atol=atol))
        for item in model.carrier.continuations
    )
    weights = _model_weights(model)
    prediction = tuple(
        (
            outcome,
            float(
                sum(
                    weight * likelihood[outcome]
                    for weight, likelihood in zip(weights, likelihoods, strict=True)
                )
            ),
        )
        for outcome in active
    )
    if not isclose(sum(p for _, p in prediction), 1.0, rel_tol=0.0, abs_tol=10 * atol):
        raise ValueError("active future-outcome probabilities must sum to one")
    return prediction


def _density_from_ensemble(
    states: Sequence[np.ndarray], weights: Sequence[float]
) -> np.ndarray:
    if len(states) != len(weights) or not states:
        raise ValueError("ensemble states and weights must be nonempty and aligned")
    density = np.zeros((states[0].size, states[0].size), dtype=np.complex128)
    for weight, state in zip(weights, states, strict=True):
        normalized = _normalized_state(state)
        density += float(weight) * np.outer(normalized, normalized.conj())
    trace = float(np.real(np.trace(density)))
    if trace <= DEFAULT_ATOL:
        raise ValueError("ensemble density must have positive trace")
    return density / trace


def _record_joint_from_ensemble(
    states: Sequence[np.ndarray], weights: Sequence[float]
) -> np.ndarray:
    """Use the explicitly frozen Stage 7 target Q, never an unspecified record."""

    joint = np.zeros((2, 2), dtype=float)
    for weight, state in zip(weights, states, strict=True):
        joint += float(weight) * target_memory_joint_distribution(
            _normalized_state(state),
            position=TARGET_POSITION,
            label=TARGET_LABEL,
        )
    total = float(np.sum(joint))
    if total <= DEFAULT_ATOL:
        raise ValueError("record joint distribution must have positive mass")
    return joint / total


def _classical_mutual_information(joint: np.ndarray) -> float:
    probabilities = np.asarray(joint, dtype=float)
    probabilities = probabilities / np.sum(probabilities)
    px = np.sum(probabilities, axis=1, keepdims=True)
    pm = np.sum(probabilities, axis=0, keepdims=True)
    independent = px @ pm
    mask = probabilities > 0.0
    return float(
        np.sum(probabilities[mask] * np.log2(probabilities[mask] / independent[mask]))
    )


def _current_ensemble(
    model: AnyStage8CModel,
) -> tuple[tuple[np.ndarray, ...], tuple[float, ...]]:
    """Return current physical ensemble without consulting epistemic h*."""

    if isinstance(model, (EpistemicQuantumModel, OnticQuantumExtensionModel)):
        states = tuple(
            reduced_continuation_state(item, model.carrier.current_anchor)
            for item in model.carrier.continuations
        )
        reference = states[0]
        for state in states[1:]:
            if np.linalg.norm(state - reference) > DEFAULT_ATOL:
                raise ValueError("carrier does not share one current Actuality")
        return (reference,), (1.0,)

    if isinstance(model, (UpdatedEpistemicQuantumState, UpdatedOnticQuantumState)):
        states = tuple(
            reduced_continuation_state(item, model.current_anchor)
            for item in model.source_carrier.continuations
        )
        return states, model.posterior_weights
    raise TypeError("unsupported Stage 8C model type")


def quantum_operational_view(
    model: AnyStage8CModel,
    *,
    atol: float = DEFAULT_ATOL,
) -> QuantumOperationalView:
    states, current_weights = _current_ensemble(model)
    density = _density_from_ensemble(states, current_weights)
    joint = _record_joint_from_ensemble(states, current_weights)
    record_information = _classical_mutual_information(joint)

    if isinstance(model, (EpistemicQuantumModel, OnticQuantumExtensionModel)):
        next_probabilities = _predict_next_probabilities(model, atol=atol)
        next_outcomes = tuple(outcome for outcome, _ in next_probabilities)
        current_anchor = model.carrier.current_anchor
        observed = None
    else:
        next_outcomes = ()
        next_probabilities = ()
        current_anchor = model.current_anchor
        observed = model.observed_outcome

    return QuantumOperationalView(
        current_anchor=current_anchor,
        current_density_matrix=tuple(complex(value) for value in density.reshape(-1)),
        current_record_joint=tuple(float(value) for value in joint.reshape(-1)),
        current_record_information=float(record_information),
        next_outcomes=next_outcomes,
        next_probabilities=next_probabilities,
        observed_outcome=observed,
    )


def _arrays_close(
    left: Sequence[complex | float],
    right: Sequence[complex | float],
    *,
    atol: float,
) -> bool:
    return len(left) == len(right) and bool(
        np.allclose(np.asarray(left), np.asarray(right), atol=atol, rtol=0.0)
    )


def compare_quantum_operational_views(
    left: QuantumOperationalView,
    right: QuantumOperationalView,
    *,
    atol: float = DEFAULT_ATOL,
) -> QuantumOperationalComparison:
    left_prob = dict(left.next_probabilities)
    right_prob = dict(right.next_probabilities)
    probabilities_equal = bool(
        set(left_prob) == set(right_prob)
        and all(
            isclose(left_prob[name], right_prob[name], rel_tol=0.0, abs_tol=atol)
            for name in left_prob
        )
    )
    current_anchor_equal = left.current_anchor == right.current_anchor
    density_equal = _arrays_close(
        left.current_density_matrix, right.current_density_matrix, atol=atol
    )
    record_joint_equal = _arrays_close(
        left.current_record_joint, right.current_record_joint, atol=atol
    )
    record_information_equal = isclose(
        left.current_record_information,
        right.current_record_information,
        rel_tol=0.0,
        abs_tol=atol,
    )
    next_outcomes_equal = left.next_outcomes == right.next_outcomes
    observed_outcome_equal = left.observed_outcome == right.observed_outcome
    equal = bool(
        current_anchor_equal
        and density_equal
        and record_joint_equal
        and record_information_equal
        and next_outcomes_equal
        and probabilities_equal
        and observed_outcome_equal
    )
    return QuantumOperationalComparison(
        equal=equal,
        current_anchor_equal=current_anchor_equal,
        density_equal=density_equal,
        record_joint_equal=record_joint_equal,
        record_information_equal=record_information_equal,
        next_outcomes_equal=next_outcomes_equal,
        next_probabilities_equal=probabilities_equal,
        observed_outcome_equal=observed_outcome_equal,
    )


def privileged_quantum_modal_diagnostic(
    model: Stage8CModel,
) -> PrivilegedQuantumModalDiagnostic:
    """Test-only structural diagnostic; deliberately outside O_Q."""

    if isinstance(model, EpistemicQuantumModel):
        return PrivilegedQuantumModalDiagnostic(
            semantic_type="epistemic-selected-continuation",
            selected_continuation_id=selected_quantum_continuation(model).continuation_id,
            selected_complete_continuation_present=True,
        )
    if isinstance(model, OnticQuantumExtensionModel):
        return PrivilegedQuantumModalDiagnostic(
            semantic_type="ontic-extension-no-selected-continuation",
            selected_continuation_id=None,
            selected_complete_continuation_present=False,
        )
    raise TypeError("unsupported Stage 8C model type")


def _outcome_likelihoods(
    carrier: QuantumContinuationCarrier,
    evidence: QuantumEvidence,
    *,
    atol: float = DEFAULT_ATOL,
) -> tuple[float, ...]:
    active = _active_next_outcomes(carrier, atol=atol)
    if evidence.outcome not in active:
        raise ValueError("evidence outcome is not in the declared current Next_Q set")
    return tuple(
        dict(continuation_future_signature_probabilities(carrier, item, atol=atol))[
            evidence.outcome
        ]
        for item in carrier.continuations
    )


def _bayes_condition(
    prior: Sequence[float],
    likelihoods: Sequence[float],
    *,
    atol: float = DEFAULT_ATOL,
) -> tuple[float, ...]:
    raw = tuple(
        float(weight) * float(likelihood)
        for weight, likelihood in zip(prior, likelihoods, strict=True)
    )
    total = sum(raw)
    if total <= atol:
        raise ValueError("explicit evidence has zero predictive support")
    return tuple(value / total for value in raw)


def update_epistemic_quantum_model(
    model: EpistemicQuantumModel,
    evidence: QuantumEvidence,
    *,
    atol: float = DEFAULT_ATOL,
) -> UpdatedEpistemicQuantumState:
    """Condition q_E on explicit evidence while preserving pre-existing h*."""

    likelihoods = _outcome_likelihoods(model.carrier, evidence, atol=atol)
    selected = selected_quantum_continuation(model)
    selected_index = next(
        index
        for index, item in enumerate(model.carrier.continuations)
        if continuation_equivalent(item, selected, atol=atol)
    )
    if likelihoods[selected_index] <= atol:
        raise ValueError("explicit evidence contradicts the hidden selected continuation")
    posterior = _bayes_condition(model.belief_weights, likelihoods, atol=atol)
    return UpdatedEpistemicQuantumState(
        source_carrier=model.carrier,
        current_anchor=UPPER_EVENT,
        observed_outcome=evidence.outcome,
        selected_continuation=selected,
        posterior_weights=posterior,
    )


def update_ontic_quantum_model(
    model: OnticQuantumExtensionModel,
    evidence: QuantumEvidence,
    *,
    atol: float = DEFAULT_ATOL,
) -> UpdatedOnticQuantumState:
    """Condition K on explicit evidence without adding a selected-future field."""

    likelihoods = _outcome_likelihoods(model.carrier, evidence, atol=atol)
    posterior = _bayes_condition(model.extension_weights, likelihoods, atol=atol)
    return UpdatedOnticQuantumState(
        source_carrier=model.carrier,
        current_anchor=UPPER_EVENT,
        observed_outcome=evidence.outcome,
        posterior_weights=posterior,
    )


def updated_ontic_selector_audit(
    model: UpdatedOnticQuantumState,
) -> UpdatedOnticSelectorAudit:
    names = tuple(field.name for field in fields(model))
    forbidden_tokens = ("selected", "selector", "seed", "precomputed", "latent_branch")
    forbidden = tuple(
        name
        for name in names
        if any(token in name.lower() for token in forbidden_tokens)
    )
    direct = tuple(
        name for name in names if isinstance(getattr(model, name), QuantumContinuation)
    )
    arbitrary_dict = hasattr(model, "__dict__")
    no_selector = bool(
        not forbidden
        and not direct
        and not arbitrary_dict
        and not hasattr(model, "selected_continuation")
        and not hasattr(model, "selector")
        and not hasattr(model, "seed")
    )
    return UpdatedOnticSelectorAudit(
        field_names=names,
        forbidden_selector_fields=forbidden,
        direct_continuation_fields=direct,
        arbitrary_instance_dict_present=arbitrary_dict,
        no_selected_complete_continuation_datum=no_selector,
    )


def updated_ontic_remaining_qext(
    model: UpdatedOnticQuantumState,
) -> tuple[QuantumContinuation, ...]:
    if model.current_anchor != UPPER_EVENT:
        raise ValueError("Stage 8C updated ontic state must be anchored at terminal e2")
    return quantum_extension_set(UPPER_EVENT)


def compare_common_quantum_evidence(
    epistemic_model: EpistemicQuantumModel,
    ontic_model: OnticQuantumExtensionModel,
    evidence: QuantumEvidence,
    *,
    atol: float = DEFAULT_ATOL,
) -> Stage8CUpdateComparison:
    if epistemic_model.carrier is not ontic_model.carrier:
        raise ValueError("Stage 8C common update requires the same continuation carrier object")

    epistemic_before = quantum_operational_view(epistemic_model, atol=atol)
    ontic_before = quantum_operational_view(ontic_model, atol=atol)
    before = compare_quantum_operational_views(epistemic_before, ontic_before, atol=atol)

    selected_before = selected_quantum_continuation(epistemic_model)
    updated_epistemic = update_epistemic_quantum_model(
        epistemic_model, evidence, atol=atol
    )
    updated_ontic = update_ontic_quantum_model(ontic_model, evidence, atol=atol)
    selected_after = updated_epistemic.selected_continuation

    epistemic_after = quantum_operational_view(updated_epistemic, atol=atol)
    ontic_after = quantum_operational_view(updated_ontic, atol=atol)
    after = compare_quantum_operational_views(epistemic_after, ontic_after, atol=atol)
    audit = updated_ontic_selector_audit(updated_ontic)

    return Stage8CUpdateComparison(
        evidence=evidence,
        epistemic_before=epistemic_before,
        ontic_before=ontic_before,
        before_comparison=before,
        epistemic_after=epistemic_after,
        ontic_after=ontic_after,
        after_comparison=after,
        epistemic_selected_before=selected_before.continuation_id,
        epistemic_selected_after=selected_after.continuation_id,
        epistemic_selected_preserved=continuation_equivalent(
            selected_before, selected_after, atol=atol
        ),
        epistemic_posterior_weights=updated_epistemic.posterior_weights,
        ontic_posterior_weights=updated_ontic.posterior_weights,
        ontic_remaining_qext_size=len(updated_ontic_remaining_qext(updated_ontic)),
        ontic_no_selected_complete_continuation_datum=(
            audit.no_selected_complete_continuation_datum
        ),
    )


def stage8c_operational_diagnostics(
    *,
    atol: float = DEFAULT_ATOL,
) -> Stage8COperationalDiagnostics:
    epistemic, ontic = canonical_stage8b_models(selected_id="h_L")
    carrier = epistemic.carrier
    baseline_e = quantum_operational_view(epistemic, atol=atol)
    baseline_o = quantum_operational_view(ontic, atol=atol)
    baseline = compare_quantum_operational_views(baseline_e, baseline_o, atol=atol)

    weights = matched_uniform_weights(carrier)
    swapped = make_epistemic_quantum_model(
        carrier, continuation_by_id(carrier, "h_R"), weights, atol=atol
    )
    selected_swap_equal = compare_quantum_operational_views(
        baseline_e, quantum_operational_view(swapped, atol=atol), atol=atol
    ).equal

    mismatch = make_ontic_quantum_extension_model(carrier, (0.75, 0.25))
    mismatch_view = quantum_operational_view(mismatch, atol=atol)
    mismatch_comparison = compare_quantum_operational_views(
        baseline_e, mismatch_view, atol=atol
    )

    privileged_distinct = bool(
        privileged_quantum_modal_diagnostic(epistemic)
        != privileged_quantum_modal_diagnostic(ontic)
    )
    schema_names = {field.name for field in fields(QuantumOperationalView)}
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

    evidence = QuantumEvidence(FUTURE_SIGNATURE_0)
    update = compare_common_quantum_evidence(epistemic, ontic, evidence, atol=atol)
    measurement = canonical_future_signature_measurement(carrier, atol=atol)
    current_state = _normalized_state(
        reduced_continuation_state(carrier.continuations[0], carrier.current_anchor)
    )
    multiple_amplitudes = int(np.count_nonzero(np.abs(current_state) > atol)) > 1
    same_density_distinct = bool(baseline.density_equal and privileged_distinct)
    same_born_distinct = bool(baseline.next_probabilities_equal and privileged_distinct)
    state_born_control = bool(same_density_distinct and same_born_distinct and baseline.equal)
    superposition_control = bool(multiple_amplitudes and baseline.equal and privileged_distinct)
    ontic_pruned = bool(
        sum(weight > atol for weight in ontic.extension_weights)
        > sum(weight > atol for weight in update.ontic_posterior_weights)
    )

    return Stage8COperationalDiagnostics(
        qext_size=len(carrier.continuations),
        matched_operational_equal=baseline.equal,
        selected_swap_operational_equal=selected_swap_equal,
        privileged_structures_distinct=privileged_distinct,
        hidden_selected_absent_from_operational_schema=hidden_absent,
        canonical_next_probabilities=baseline_e.next_probabilities,
        weight_mismatch_changes_prediction=bool(
            mismatch_comparison.current_anchor_equal
            and mismatch_comparison.density_equal
            and mismatch_comparison.record_joint_equal
            and mismatch_comparison.next_outcomes_equal
            and not mismatch_comparison.next_probabilities_equal
            and not mismatch_comparison.equal
        ),
        mismatched_next_probabilities=mismatch_view.next_probabilities,
        update_before_equal=update.before_comparison.equal,
        update_after_equal=update.after_comparison.equal,
        update_anchor_advanced=bool(
            update.epistemic_before.current_anchor < update.epistemic_after.current_anchor
            and update.epistemic_after.current_anchor == UPPER_EVENT
            and update.ontic_after.current_anchor == UPPER_EVENT
        ),
        update_outcome_equal=bool(
            update.epistemic_after.observed_outcome
            == update.ontic_after.observed_outcome
            == evidence.outcome
        ),
        epistemic_selected_preserved=update.epistemic_selected_preserved,
        epistemic_posterior_weights=update.epistemic_posterior_weights,
        ontic_posterior_weights=update.ontic_posterior_weights,
        ontic_posterior_pruned=ontic_pruned,
        ontic_remaining_qext_size=update.ontic_remaining_qext_size,
        ontic_no_selected_complete_continuation_datum=(
            update.ontic_no_selected_complete_continuation_datum
        ),
        same_density_with_distinct_modal_structure=same_density_distinct,
        same_born_prediction_with_distinct_modal_structure=same_born_distinct,
        current_state_has_multiple_coherent_amplitudes=multiple_amplitudes,
        superposition_does_not_select_modal_semantics=superposition_control,
        state_and_born_data_do_not_select_modal_semantics=state_born_control,
        measurement_completeness_residual=measurement.completeness_residual,
        measurement_orthogonality_residual=measurement.orthogonality_residual,
        minimum_effect_eigenvalue=measurement.minimum_effect_eigenvalue,
    )


def stage8c_summary() -> dict[str, object]:
    diagnostics = stage8c_operational_diagnostics()
    return {
        "stage": "8C",
        "interface": "O_Q=(current density, R_now, Next_Q, Born-mixture prediction)",
        "diagnostics": asdict(diagnostics),
        "exit_criteria_satisfied": tuple(range(22, 30)),
        "guards": [
            "operational quantum equality != modal/ontological identity",
            "matched numerical q_E and K != matched probability semantics",
            "explicit evidence update != ontological becoming",
            "random sampling != ontic actualization evidence",
            "superposition != ontic Potentiality by definition",
            "same density/Born data != unique modal semantics in this family",
            "evidence-conditioned singleton support != pre-existing hidden selector",
        ],
        "next": "Stage 8D — genuine clock-change modal transport",
    }
