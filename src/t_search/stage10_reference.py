"""Stage 10A typed reference future-measurement family.

Stage 10A does not transport the measurement across clocks yet.  It promotes
Stage 9C's canonical A/e2 future-signature measurement into an explicitly typed
reference object while preserving the original effects and Born likelihoods.

The common numerical effect matrices are wrapped separately for each declared
continuation so that continuation identity is part of the type even at the
reference node.  This is not yet the continuation-specific physical/support
lift required by Stage 10B.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from math import isclose

import numpy as np

from .stage5_clock_change import DEFAULT_ATOL
from .stage7_history import CURRENT_EVENT, UPPER_EVENT
from .stage8_continuations import QuantumContinuation
from .stage9_modal import (
    FUTURE_SIGNATURE_LEFT,
    FUTURE_SIGNATURE_OTHER,
    canonical_stage9_directional_carrier,
    canonical_stage9_future_signature_measurement,
    continuation_future_signature_probabilities,
)
from .stage9_substrate import reduced_stage9_state, stage9_continuation_equivalent

STAGE10_REFERENCE_FAMILY_ID = "stage9c_future_signature"
STAGE10_REFERENCE_CLOCK = "A"
STAGE10_REFERENCE_BASIS = "Stage 9C common A/e2 reduced ambient basis"
STAGE10_REFERENCE_NORMALIZATION = "normalized reduced-state Euclidean Born rule"


@dataclass(frozen=True, slots=True)
class Stage10OutcomeIdentity:
    outcome_id: str
    semantics: str
    provenance: str


@dataclass(frozen=True, slots=True)
class Stage10TypedReferenceEffect:
    family_id: str
    continuation_id: str
    prediction_anchor: int
    target_event: int
    clock: str
    clock_index: int
    outcome_id: str
    outcome_semantics: str
    outcome_provenance: str
    effect_provenance: str
    coordinate_basis: str
    normalization: str
    matrix: np.ndarray


@dataclass(frozen=True, slots=True)
class Stage10ReferenceMeasurementFamily:
    family_id: str
    prediction_anchor: int
    target_event: int
    clock: str
    clock_index: int
    coordinate_basis: str
    normalization: str
    continuation_ids: tuple[str, ...]
    outcomes: tuple[Stage10OutcomeIdentity, ...]
    effects: tuple[Stage10TypedReferenceEffect, ...]


@dataclass(frozen=True, slots=True)
class Stage10ReferenceDiagnostics:
    continuation_count: int
    typed_effect_count: int
    canonical_outcomes_reproduced: bool
    canonical_effects_reproduced: bool
    prediction_anchor_explicit: bool
    target_event_explicit: bool
    anchor_target_distinct: bool
    max_effect_residual: float
    max_completeness_residual: float
    minimum_effect_eigenvalue: float
    future_branch_overlap_squared: float
    operationally_discriminating: bool
    max_stage9_probability_residual: float
    all_reference_probabilities_normalized: bool
    public_schema_fields: tuple[str, ...]
    forbidden_public_fields: tuple[str, ...]
    public_schema_selector_free: bool


def canonical_stage10_outcomes() -> tuple[Stage10OutcomeIdentity, ...]:
    return (
        Stage10OutcomeIdentity(
            FUTURE_SIGNATURE_LEFT,
            "future signature aligned with the canonical h_L e2 reference ray",
            "Stage 9C canonical future_signature_left outcome identity",
        ),
        Stage10OutcomeIdentity(
            FUTURE_SIGNATURE_OTHER,
            "complement of the canonical h_L e2 reference-ray signature",
            "Stage 9C canonical future_signature_other outcome identity",
        ),
    )


def _outcome_by_id(outcome_id: str) -> Stage10OutcomeIdentity:
    matches = [item for item in canonical_stage10_outcomes() if item.outcome_id == outcome_id]
    if len(matches) != 1:
        raise ValueError(f"unknown Stage 10A outcome {outcome_id!r}")
    return matches[0]


def canonical_stage10_reference_measurement_family() -> Stage10ReferenceMeasurementFamily:
    carrier = canonical_stage9_directional_carrier()
    stage9 = canonical_stage9_future_signature_measurement(carrier)
    outcomes = canonical_stage10_outcomes()
    if tuple(item.outcome_id for item in outcomes) != stage9.outcome_names:
        raise RuntimeError("Stage 10A outcome identities drifted from Stage 9C")

    typed_effects: list[Stage10TypedReferenceEffect] = []
    for continuation in carrier.continuations:
        for name, matrix in zip(stage9.outcome_names, stage9.effects, strict=True):
            outcome = _outcome_by_id(name)
            effect_provenance = (
                "projector onto normalized canonical h_L reduced e2 ray"
                if name == FUTURE_SIGNATURE_LEFT
                else "identity minus the canonical h_L reduced-e2 ray projector"
            )
            typed_effects.append(
                Stage10TypedReferenceEffect(
                    family_id=STAGE10_REFERENCE_FAMILY_ID,
                    continuation_id=continuation.continuation_id,
                    prediction_anchor=CURRENT_EVENT,
                    target_event=UPPER_EVENT,
                    clock=STAGE10_REFERENCE_CLOCK,
                    clock_index=UPPER_EVENT,
                    outcome_id=name,
                    outcome_semantics=outcome.semantics,
                    outcome_provenance=outcome.provenance,
                    effect_provenance=effect_provenance,
                    coordinate_basis=STAGE10_REFERENCE_BASIS,
                    normalization=STAGE10_REFERENCE_NORMALIZATION,
                    matrix=np.array(matrix, dtype=np.complex128, copy=True),
                )
            )

    return Stage10ReferenceMeasurementFamily(
        family_id=STAGE10_REFERENCE_FAMILY_ID,
        prediction_anchor=CURRENT_EVENT,
        target_event=UPPER_EVENT,
        clock=STAGE10_REFERENCE_CLOCK,
        clock_index=UPPER_EVENT,
        coordinate_basis=STAGE10_REFERENCE_BASIS,
        normalization=STAGE10_REFERENCE_NORMALIZATION,
        continuation_ids=tuple(item.continuation_id for item in carrier.continuations),
        outcomes=outcomes,
        effects=tuple(typed_effects),
    )


def reference_effects_for_continuation(
    family: Stage10ReferenceMeasurementFamily,
    continuation_id: str,
) -> tuple[Stage10TypedReferenceEffect, ...]:
    if continuation_id not in family.continuation_ids:
        raise ValueError(f"unknown Stage 10A continuation {continuation_id!r}")
    effects = tuple(
        effect for effect in family.effects if effect.continuation_id == continuation_id
    )
    expected = tuple(item.outcome_id for item in family.outcomes)
    if tuple(effect.outcome_id for effect in effects) != expected:
        raise RuntimeError("Stage 10A typed effect ordering is incomplete or ambiguous")
    return effects


def _canonical_equivalent_continuation(continuation: QuantumContinuation) -> QuantumContinuation:
    carrier = canonical_stage9_directional_carrier()
    matches = tuple(
        item
        for item in carrier.continuations
        if stage9_continuation_equivalent(item, continuation, atol=DEFAULT_ATOL)
    )
    if len(matches) != 1:
        raise ValueError("continuation must belong to exactly one canonical Stage 10A class")
    return matches[0]


def _normalized_reference_state(continuation: QuantumContinuation) -> np.ndarray:
    state = np.asarray(reduced_stage9_state(continuation, UPPER_EVENT), dtype=np.complex128)
    norm = float(np.linalg.norm(state))
    if norm <= DEFAULT_ATOL:
        raise ValueError("Stage 10A reference state has zero norm")
    return state / norm


def stage10_reference_probabilities(
    family: Stage10ReferenceMeasurementFamily,
    continuation: QuantumContinuation,
    *,
    atol: float = DEFAULT_ATOL,
) -> tuple[tuple[str, float], ...]:
    canonical = _canonical_equivalent_continuation(continuation)
    effects = reference_effects_for_continuation(family, canonical.continuation_id)
    state = _normalized_reference_state(canonical)
    values: list[tuple[str, float]] = []
    for effect in effects:
        if (
            effect.prediction_anchor != family.prediction_anchor
            or effect.target_event != family.target_event
            or effect.clock != family.clock
            or effect.clock_index != family.clock_index
            or effect.normalization != family.normalization
        ):
            raise ValueError("Stage 10A typed effect is inconsistent with its reference family")
        value = np.vdot(state, effect.matrix @ state)
        if abs(float(value.imag)) > atol:
            raise ValueError("Stage 10A Born probability acquired an imaginary component")
        probability = float(value.real)
        if probability < -atol or probability > 1.0 + atol:
            raise ValueError("Stage 10A Born probability lies outside [0,1]")
        values.append((effect.outcome_id, min(1.0, max(0.0, probability))))
    if not isclose(sum(value for _, value in values), 1.0, rel_tol=0.0, abs_tol=10 * atol):
        raise ValueError("Stage 10A reference probabilities must sum to one")
    return tuple(values)


def stage10_reference_schema_audit(
    family: Stage10ReferenceMeasurementFamily,
) -> tuple[tuple[str, ...], tuple[str, ...], bool]:
    family_fields = tuple(field.name for field in fields(family))
    outcome_fields = tuple(field.name for field in fields(Stage10OutcomeIdentity))
    effect_fields = tuple(field.name for field in fields(Stage10TypedReferenceEffect))
    public_fields = tuple(dict.fromkeys(family_fields + outcome_fields + effect_fields))
    forbidden_exact = {
        "selected_continuation",
        "selected_continuation_id",
        "selector",
        "hidden_selector",
        "model_type",
        "modal_type",
        "semantic_type",
        "privileged_modal_type",
    }
    forbidden = tuple(name for name in public_fields if name in forbidden_exact)
    return public_fields, forbidden, not forbidden


def stage10a_reference_diagnostics(
    *,
    atol: float = DEFAULT_ATOL,
) -> Stage10ReferenceDiagnostics:
    family = canonical_stage10_reference_measurement_family()
    carrier = canonical_stage9_directional_carrier()
    stage9 = canonical_stage9_future_signature_measurement(carrier, atol=atol)
    canonical_outcomes = tuple(item.outcome_id for item in family.outcomes)

    max_effect_residual = 0.0
    max_completeness = 0.0
    minimum_eigenvalue = float("inf")
    max_probability_residual = 0.0
    probability_vectors: list[np.ndarray] = []
    all_normalized = True

    for continuation in carrier.continuations:
        typed = reference_effects_for_continuation(family, continuation.continuation_id)
        matrices = tuple(effect.matrix for effect in typed)
        for matrix, reference in zip(matrices, stage9.effects, strict=True):
            max_effect_residual = max(
                max_effect_residual,
                float(np.linalg.norm(matrix - reference)),
            )
            hermitian = (matrix + matrix.conj().T) / 2.0
            minimum_eigenvalue = min(
                minimum_eigenvalue,
                float(np.min(np.linalg.eigvalsh(hermitian))),
            )
        identity = np.eye(matrices[0].shape[0], dtype=np.complex128)
        max_completeness = max(
            max_completeness,
            float(np.linalg.norm(sum(matrices) - identity)),
        )

        stage10_probabilities = stage10_reference_probabilities(
            family, continuation, atol=atol
        )
        stage9_probabilities = continuation_future_signature_probabilities(
            carrier, continuation, atol=atol
        )
        d10 = dict(stage10_probabilities)
        d9 = dict(stage9_probabilities)
        if set(d10) != set(d9):
            max_probability_residual = float("inf")
        else:
            max_probability_residual = max(
                max_probability_residual,
                max(abs(d10[name] - d9[name]) for name in d10),
            )
        vector = np.asarray([d10[name] for name in canonical_outcomes], dtype=float)
        probability_vectors.append(vector)
        all_normalized = bool(
            all_normalized
            and np.min(vector) >= -atol
            and np.max(vector) <= 1.0 + atol
            and abs(float(np.sum(vector)) - 1.0) <= 10 * atol
        )

    discriminating = bool(
        len(probability_vectors) >= 2
        and any(
            np.linalg.norm(left - right) > atol
            for index, left in enumerate(probability_vectors)
            for right in probability_vectors[index + 1 :]
        )
        and stage9.branch_overlap_squared < 1.0 - atol
    )
    public_fields, forbidden, selector_free = stage10_reference_schema_audit(family)

    return Stage10ReferenceDiagnostics(
        continuation_count=len(carrier.continuations),
        typed_effect_count=len(family.effects),
        canonical_outcomes_reproduced=canonical_outcomes == stage9.outcome_names,
        canonical_effects_reproduced=max_effect_residual <= atol,
        prediction_anchor_explicit=family.prediction_anchor == CURRENT_EVENT,
        target_event_explicit=family.target_event == UPPER_EVENT,
        anchor_target_distinct=family.prediction_anchor != family.target_event,
        max_effect_residual=max_effect_residual,
        max_completeness_residual=max_completeness,
        minimum_effect_eigenvalue=minimum_eigenvalue,
        future_branch_overlap_squared=stage9.branch_overlap_squared,
        operationally_discriminating=discriminating,
        max_stage9_probability_residual=max_probability_residual,
        all_reference_probabilities_normalized=all_normalized,
        public_schema_fields=public_fields,
        forbidden_public_fields=forbidden,
        public_schema_selector_free=selector_free,
    )


def stage10a_summary(*, atol: float = DEFAULT_ATOL) -> dict[str, object]:
    diagnostics = stage10a_reference_diagnostics(atol=atol)
    return {
        "continuation_count": diagnostics.continuation_count,
        "typed_effect_count": diagnostics.typed_effect_count,
        "canonical_outcomes_reproduced": diagnostics.canonical_outcomes_reproduced,
        "canonical_effects_reproduced": diagnostics.canonical_effects_reproduced,
        "anchor_target_distinct": diagnostics.anchor_target_distinct,
        "max_completeness_residual": diagnostics.max_completeness_residual,
        "minimum_effect_eigenvalue": diagnostics.minimum_effect_eigenvalue,
        "future_branch_overlap_squared": diagnostics.future_branch_overlap_squared,
        "operationally_discriminating": diagnostics.operationally_discriminating,
        "max_stage9_probability_residual": diagnostics.max_stage9_probability_residual,
        "public_schema_selector_free": diagnostics.public_schema_selector_free,
    }
