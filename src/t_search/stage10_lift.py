"""Stage 10B continuation-specific measurement lift and normalization choice.

Stage 10A froze the Stage 9C future-signature POVM at the common A/e2
reduced-ambient reference representation.  Stage 10B independently pulls that
same operational question into each continuation's own A/e2 QR-support and
physical coordinates.

The retained transport representation is a reference-induced effect form.  If
R_h is the continuation-specific A/e2 reduction matrix and E_o is a Stage 9C
reference effect, then

    N_h = R_h^dagger R_h
    F_{h,o} = R_h^dagger E_o R_h

on physical coordinates.  Therefore

    p(o|h) = c^dagger F_{h,o} c / (c^dagger N_h c)

is exactly the Stage 9C normalized-reduced-state Born probability, and

    sum_o F_{h,o} = N_h.

At the reference QR-support chart this same construction becomes an ordinary
local POVM with identity normalization.  Because genuine Stage 9D clock maps
are generally non-Euclidean-unitary, Stage 10B does not promote "reset the
normalization to identity in every chart" to a cross-clock rule.  Stage 10C
will instead test dual transport of the reference-induced normalization/effect
forms.

This stage establishes only the continuation-specific reference lift and the
normalization representation choice.  It does not establish cross-clock
measurement covariance.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product

import numpy as np

from .stage5_clock_change import DEFAULT_ATOL
from .stage7_history import CURRENT_EVENT, UPPER_EVENT
from .stage8_continuations import QuantumContinuation
from .stage9_modal import (
    FUTURE_SIGNATURE_LEFT,
    FUTURE_SIGNATURE_OTHER,
    canonical_stage9_directional_carrier,
    continuation_future_signature_probabilities,
)
from .stage9_substrate import (
    canonical_stage9_physical_state,
    stage9_clock_reduction_matrix,
    stage9_physical_basis,
)
from .stage9_transport import (
    stage9_clock_change_support_matrix,
    stage9_clock_coordinates,
    stage9_clock_support_basis,
    stage9_reduced_support_coordinates,
)
from .stage10_reference import (
    STAGE10_REFERENCE_CLOCK,
    STAGE10_REFERENCE_FAMILY_ID,
    Stage10OutcomeIdentity,
    canonical_stage10_reference_measurement_family,
    reference_effects_for_continuation,
)

STAGE10B_SUPPORT_BASIS = "continuation-specific A/e2 QR-support coordinates"
STAGE10B_PHYSICAL_BASIS = "continuation-specific 14D constrained physical coordinates"
STAGE10B_RETAINED_REPRESENTATION = "reference-induced physical-coordinate effect form"
STAGE10B_RETAINED_NORMALIZATION = "Stage 9C reduced-Euclidean norm pulled back to physical coordinates"
STAGE10B_REFERENCE_SUPPORT_NORMALIZATION = "identity on continuation-specific A/e2 QR support"


@dataclass(frozen=True, slots=True)
class Stage10LiftedEffect:
    family_id: str
    continuation_id: str
    prediction_anchor: int
    target_event: int
    reference_clock: str
    reference_clock_index: int
    outcome_id: str
    outcome_semantics: str
    outcome_provenance: str
    effect_provenance: str
    support_coordinate_basis: str
    physical_coordinate_basis: str
    normalization_semantics: str
    support_effect_matrix: np.ndarray
    physical_effect_form: np.ndarray


@dataclass(frozen=True, slots=True)
class Stage10ContinuationMeasurementLift:
    family_id: str
    continuation_id: str
    prediction_anchor: int
    target_event: int
    reference_clock: str
    reference_clock_index: int
    representation: str
    normalization_semantics: str
    support_coordinate_basis: str
    physical_coordinate_basis: str
    support_normalization_matrix: np.ndarray
    physical_normalization_form: np.ndarray
    class_correspondence: tuple[str, str]
    outcome_correspondence: tuple[tuple[str, str], ...]
    outcomes: tuple[Stage10OutcomeIdentity, ...]
    effects: tuple[Stage10LiftedEffect, ...]


@dataclass(frozen=True, slots=True)
class Stage10BNormalizationDecision:
    retained_representation: str
    retained_normalization: str
    reference_support_povm_equivalent: bool
    physical_effect_form_equivalent: bool
    genuine_maps_nonunitary: bool
    local_identity_reset_not_transport_covariant: bool
    max_nonunitarity_residual: float
    max_identity_reset_residual: float
    physical_metric_identified_with_operational_normalization: bool


@dataclass(frozen=True, slots=True)
class Stage10BLiftDiagnostics:
    continuation_count: int
    effects_per_continuation: int
    all_lifts_continuation_specific: bool
    max_support_completeness_residual: float
    max_physical_completeness_residual: float
    minimum_support_effect_eigenvalue: float
    minimum_physical_effect_eigenvalue: float
    minimum_physical_normalization_eigenvalue: float
    max_support_stage9_probability_residual: float
    max_effect_form_stage9_probability_residual: float
    max_support_vs_form_probability_residual: float
    class_correspondences_explicit: bool
    outcome_correspondences_explicit: bool
    wrong_continuation_lift_rejected: bool
    wrong_continuation_form_residual: float
    normalization_decision: Stage10BNormalizationDecision
    full_cross_clock_measurement_covariance_established: bool


def _continuation_by_id(continuation_id: str) -> QuantumContinuation:
    carrier = canonical_stage9_directional_carrier()
    matches = tuple(
        item for item in carrier.continuations if item.continuation_id == continuation_id
    )
    if len(matches) != 1:
        raise ValueError(f"unknown Stage 10B continuation {continuation_id!r}")
    return matches[0]


def _physical_coordinates(continuation: QuantumContinuation) -> np.ndarray:
    basis = stage9_physical_basis(continuation)
    state = canonical_stage9_physical_state(continuation)
    coordinates, _, rank, _ = np.linalg.lstsq(basis, state, rcond=None)
    if rank != 14:
        raise ValueError("Stage 10B physical basis is not full rank")
    residual = float(np.linalg.norm(basis @ coordinates - state))
    if residual > 10 * DEFAULT_ATOL:
        raise ValueError("Stage 10B physical-coordinate reconstruction failed")
    return np.asarray(coordinates, dtype=np.complex128)


def _outcome_correspondence() -> tuple[tuple[str, str], ...]:
    return (
        (FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_LEFT),
        (FUTURE_SIGNATURE_OTHER, FUTURE_SIGNATURE_OTHER),
    )


def lift_stage10_reference_measurement(
    continuation: QuantumContinuation,
    *,
    atol: float = DEFAULT_ATOL,
) -> Stage10ContinuationMeasurementLift:
    """Independently pull the Stage 10A reference family into one continuation."""

    canonical = _continuation_by_id(continuation.continuation_id)
    reference = canonical_stage10_reference_measurement_family()
    typed_reference = reference_effects_for_continuation(
        reference, canonical.continuation_id
    )

    reduction = stage9_clock_reduction_matrix(
        canonical, STAGE10_REFERENCE_CLOCK, UPPER_EVENT
    )
    support = stage9_clock_support_basis(
        canonical, STAGE10_REFERENCE_CLOCK, UPPER_EVENT
    )
    coordinates = stage9_clock_coordinates(
        canonical, STAGE10_REFERENCE_CLOCK, UPPER_EVENT
    )
    if reduction.shape != (18, 14) or support.shape != (18, 14) or coordinates.shape != (14, 14):
        raise ValueError("unexpected Stage 10B reference reduction dimensions")
    if np.linalg.matrix_rank(coordinates, tol=atol) != 14:
        raise ValueError("Stage 10B reference support coordinates are not invertible")

    support_normalization = np.eye(14, dtype=np.complex128)
    physical_normalization = reduction.conj().T @ reduction
    # Equivalent QR expression; this is also a guard that the lift uses the
    # continuation's own support coordinates rather than a universal map.
    qr_normalization = coordinates.conj().T @ coordinates
    if np.linalg.norm(physical_normalization - qr_normalization) > 10 * atol:
        raise RuntimeError("Stage 10B reduction/QR normalization pullbacks disagree")

    lifted: list[Stage10LiftedEffect] = []
    for effect in typed_reference:
        support_effect = support.conj().T @ effect.matrix @ support
        physical_form = reduction.conj().T @ effect.matrix @ reduction
        qr_form = coordinates.conj().T @ support_effect @ coordinates
        if np.linalg.norm(physical_form - qr_form) > 10 * atol:
            raise RuntimeError("Stage 10B ambient and QR effect pullbacks disagree")
        lifted.append(
            Stage10LiftedEffect(
                family_id=effect.family_id,
                continuation_id=canonical.continuation_id,
                prediction_anchor=effect.prediction_anchor,
                target_event=effect.target_event,
                reference_clock=effect.clock,
                reference_clock_index=effect.clock_index,
                outcome_id=effect.outcome_id,
                outcome_semantics=effect.outcome_semantics,
                outcome_provenance=effect.outcome_provenance,
                effect_provenance=(
                    effect.effect_provenance
                    + "; independently pulled back through continuation-specific A/e2 reduction"
                ),
                support_coordinate_basis=STAGE10B_SUPPORT_BASIS,
                physical_coordinate_basis=STAGE10B_PHYSICAL_BASIS,
                normalization_semantics=STAGE10B_RETAINED_NORMALIZATION,
                support_effect_matrix=support_effect,
                physical_effect_form=physical_form,
            )
        )

    return Stage10ContinuationMeasurementLift(
        family_id=STAGE10_REFERENCE_FAMILY_ID,
        continuation_id=canonical.continuation_id,
        prediction_anchor=CURRENT_EVENT,
        target_event=UPPER_EVENT,
        reference_clock=STAGE10_REFERENCE_CLOCK,
        reference_clock_index=UPPER_EVENT,
        representation=STAGE10B_RETAINED_REPRESENTATION,
        normalization_semantics=STAGE10B_RETAINED_NORMALIZATION,
        support_coordinate_basis=STAGE10B_SUPPORT_BASIS,
        physical_coordinate_basis=STAGE10B_PHYSICAL_BASIS,
        support_normalization_matrix=support_normalization,
        physical_normalization_form=physical_normalization,
        class_correspondence=(canonical.continuation_id, canonical.continuation_id),
        outcome_correspondence=_outcome_correspondence(),
        outcomes=reference.outcomes,
        effects=tuple(lifted),
    )


def canonical_stage10b_lifts() -> tuple[Stage10ContinuationMeasurementLift, ...]:
    carrier = canonical_stage9_directional_carrier()
    return tuple(lift_stage10_reference_measurement(item) for item in carrier.continuations)


def stage10b_support_probabilities(
    lift: Stage10ContinuationMeasurementLift,
    continuation: QuantumContinuation,
    *,
    atol: float = DEFAULT_ATOL,
) -> tuple[tuple[str, float], ...]:
    if lift.continuation_id != continuation.continuation_id:
        raise ValueError("Stage 10B lift belongs to a different continuation class")
    state = stage9_reduced_support_coordinates(
        continuation, STAGE10_REFERENCE_CLOCK, UPPER_EVENT
    )
    denominator = np.vdot(state, lift.support_normalization_matrix @ state)
    if abs(float(denominator.imag)) > atol or denominator.real <= atol:
        raise ValueError("invalid Stage 10B support normalization")
    values: list[tuple[str, float]] = []
    for effect in lift.effects:
        value = np.vdot(state, effect.support_effect_matrix @ state) / denominator
        if abs(float(value.imag)) > 10 * atol:
            raise ValueError("Stage 10B support probability acquired imaginary part")
        values.append((effect.outcome_id, float(value.real)))
    return tuple(values)


def stage10b_effect_form_probabilities(
    lift: Stage10ContinuationMeasurementLift,
    continuation: QuantumContinuation,
    *,
    atol: float = DEFAULT_ATOL,
) -> tuple[tuple[str, float], ...]:
    if lift.continuation_id != continuation.continuation_id:
        raise ValueError("Stage 10B lift belongs to a different continuation class")
    coordinates = _physical_coordinates(continuation)
    denominator = np.vdot(
        coordinates, lift.physical_normalization_form @ coordinates
    )
    if abs(float(denominator.imag)) > atol or denominator.real <= atol:
        raise ValueError("invalid Stage 10B physical normalization form")
    values: list[tuple[str, float]] = []
    for effect in lift.effects:
        value = np.vdot(
            coordinates, effect.physical_effect_form @ coordinates
        ) / denominator
        if abs(float(value.imag)) > 10 * atol:
            raise ValueError("Stage 10B effect-form probability acquired imaginary part")
        values.append((effect.outcome_id, float(value.real)))
    return tuple(values)


def _probability_residual(
    left: tuple[tuple[str, float], ...],
    right: tuple[tuple[str, float], ...],
) -> float:
    dl = dict(left)
    dr = dict(right)
    if set(dl) != set(dr):
        return float("inf")
    return max(abs(dl[name] - dr[name]) for name in dl)


def stage10b_normalization_decision(
    *,
    atol: float = DEFAULT_ATOL,
) -> Stage10BNormalizationDecision:
    carrier = canonical_stage9_directional_carrier()
    support_residual = 0.0
    form_residual = 0.0
    max_nonunitarity = 0.0
    max_identity_reset = 0.0

    for continuation in carrier.continuations:
        lift = lift_stage10_reference_measurement(continuation, atol=atol)
        reference = continuation_future_signature_probabilities(
            carrier, continuation, atol=atol
        )
        support_residual = max(
            support_residual,
            _probability_residual(
                stage10b_support_probabilities(lift, continuation, atol=atol), reference
            ),
        )
        form_residual = max(
            form_residual,
            _probability_residual(
                stage10b_effect_form_probabilities(lift, continuation, atol=atol), reference
            ),
        )
        for target_clock in ("B", "C"):
            for target_index in range(3):
                transform = stage9_clock_change_support_matrix(
                    continuation,
                    target_clock,
                    target_index,
                    STAGE10_REFERENCE_CLOCK,
                    UPPER_EVENT,
                )
                identity = np.eye(transform.shape[0], dtype=np.complex128)
                max_nonunitarity = max(
                    max_nonunitarity,
                    float(np.linalg.norm(transform.conj().T @ transform - identity)),
                )
                inverse = np.linalg.inv(transform)
                transported_identity = inverse.conj().T @ identity @ inverse
                max_identity_reset = max(
                    max_identity_reset,
                    float(np.linalg.norm(transported_identity - identity)),
                )

    return Stage10BNormalizationDecision(
        retained_representation=STAGE10B_RETAINED_REPRESENTATION,
        retained_normalization=STAGE10B_RETAINED_NORMALIZATION,
        reference_support_povm_equivalent=support_residual <= 10 * atol,
        physical_effect_form_equivalent=form_residual <= 10 * atol,
        genuine_maps_nonunitary=max_nonunitarity > 10 * atol,
        local_identity_reset_not_transport_covariant=max_identity_reset > 10 * atol,
        max_nonunitarity_residual=max_nonunitarity,
        max_identity_reset_residual=max_identity_reset,
        # Stage 9D's support metric tracks physical-coordinate norm.  Stage 10B's
        # operational normalization instead pulls back the Stage 9C reduced norm.
        # They are deliberately distinct typed resources; no equality is assumed.
        physical_metric_identified_with_operational_normalization=False,
    )


def stage10b_lift_diagnostics(
    *,
    atol: float = DEFAULT_ATOL,
) -> Stage10BLiftDiagnostics:
    carrier = canonical_stage9_directional_carrier()
    lifts = canonical_stage10b_lifts()
    max_support_completeness = 0.0
    max_physical_completeness = 0.0
    min_support_effect = float("inf")
    min_physical_effect = float("inf")
    min_normalization = float("inf")
    max_support_probability = 0.0
    max_form_probability = 0.0
    max_support_vs_form = 0.0

    for continuation, lift in zip(carrier.continuations, lifts, strict=True):
        support_sum = sum(
            (effect.support_effect_matrix for effect in lift.effects),
            start=np.zeros((14, 14), dtype=np.complex128),
        )
        physical_sum = sum(
            (effect.physical_effect_form for effect in lift.effects),
            start=np.zeros((14, 14), dtype=np.complex128),
        )
        max_support_completeness = max(
            max_support_completeness,
            float(np.linalg.norm(support_sum - lift.support_normalization_matrix)),
        )
        max_physical_completeness = max(
            max_physical_completeness,
            float(np.linalg.norm(physical_sum - lift.physical_normalization_form)),
        )
        min_normalization = min(
            min_normalization,
            float(np.min(np.linalg.eigvalsh(
                (lift.physical_normalization_form + lift.physical_normalization_form.conj().T) / 2.0
            ))),
        )
        for effect in lift.effects:
            min_support_effect = min(
                min_support_effect,
                float(np.min(np.linalg.eigvalsh(
                    (effect.support_effect_matrix + effect.support_effect_matrix.conj().T) / 2.0
                ))),
            )
            min_physical_effect = min(
                min_physical_effect,
                float(np.min(np.linalg.eigvalsh(
                    (effect.physical_effect_form + effect.physical_effect_form.conj().T) / 2.0
                ))),
            )

        reference = continuation_future_signature_probabilities(
            carrier, continuation, atol=atol
        )
        support_probabilities = stage10b_support_probabilities(
            lift, continuation, atol=atol
        )
        form_probabilities = stage10b_effect_form_probabilities(
            lift, continuation, atol=atol
        )
        max_support_probability = max(
            max_support_probability,
            _probability_residual(support_probabilities, reference),
        )
        max_form_probability = max(
            max_form_probability,
            _probability_residual(form_probabilities, reference),
        )
        max_support_vs_form = max(
            max_support_vs_form,
            _probability_residual(support_probabilities, form_probabilities),
        )

    wrong_rejected = False
    wrong_form_residual = 0.0
    if len(lifts) >= 2:
        left, right = lifts[:2]
        wrong_form_residual = max(
            float(np.linalg.norm(a.physical_effect_form - b.physical_effect_form))
            for a, b in zip(left.effects, right.effects, strict=True)
        )
        try:
            stage10b_effect_form_probabilities(left, carrier.continuations[1], atol=atol)
        except ValueError:
            wrong_rejected = True

    class_explicit = all(
        lift.class_correspondence == (lift.continuation_id, lift.continuation_id)
        for lift in lifts
    )
    expected_outcomes = _outcome_correspondence()
    outcome_explicit = all(lift.outcome_correspondence == expected_outcomes for lift in lifts)
    all_specific = bool(
        len(lifts) == len(carrier.continuations)
        and len({lift.continuation_id for lift in lifts}) == len(lifts)
        and all(
            all(
                "continuation-specific A/e2 reduction" in effect.effect_provenance
                for effect in lift.effects
            )
            for lift in lifts
        )
    )

    return Stage10BLiftDiagnostics(
        continuation_count=len(lifts),
        effects_per_continuation=len(lifts[0].effects) if lifts else 0,
        all_lifts_continuation_specific=all_specific,
        max_support_completeness_residual=max_support_completeness,
        max_physical_completeness_residual=max_physical_completeness,
        minimum_support_effect_eigenvalue=min_support_effect,
        minimum_physical_effect_eigenvalue=min_physical_effect,
        minimum_physical_normalization_eigenvalue=min_normalization,
        max_support_stage9_probability_residual=max_support_probability,
        max_effect_form_stage9_probability_residual=max_form_probability,
        max_support_vs_form_probability_residual=max_support_vs_form,
        class_correspondences_explicit=class_explicit,
        outcome_correspondences_explicit=outcome_explicit,
        wrong_continuation_lift_rejected=wrong_rejected,
        wrong_continuation_form_residual=wrong_form_residual,
        normalization_decision=stage10b_normalization_decision(atol=atol),
        full_cross_clock_measurement_covariance_established=False,
    )


def stage10b_summary(*, atol: float = DEFAULT_ATOL) -> dict[str, object]:
    diagnostics = stage10b_lift_diagnostics(atol=atol)
    decision = diagnostics.normalization_decision
    return {
        "continuation_count": diagnostics.continuation_count,
        "effects_per_continuation": diagnostics.effects_per_continuation,
        "all_lifts_continuation_specific": diagnostics.all_lifts_continuation_specific,
        "max_support_completeness_residual": diagnostics.max_support_completeness_residual,
        "max_physical_completeness_residual": diagnostics.max_physical_completeness_residual,
        "minimum_physical_normalization_eigenvalue": diagnostics.minimum_physical_normalization_eigenvalue,
        "max_support_stage9_probability_residual": diagnostics.max_support_stage9_probability_residual,
        "max_effect_form_stage9_probability_residual": diagnostics.max_effect_form_stage9_probability_residual,
        "retained_representation": decision.retained_representation,
        "genuine_maps_nonunitary": decision.genuine_maps_nonunitary,
        "local_identity_reset_not_transport_covariant": decision.local_identity_reset_not_transport_covariant,
        "max_nonunitarity_residual": decision.max_nonunitarity_residual,
        "max_identity_reset_residual": decision.max_identity_reset_residual,
        "wrong_continuation_lift_rejected": diagnostics.wrong_continuation_lift_rejected,
        "full_cross_clock_measurement_covariance_established": diagnostics.full_cross_clock_measurement_covariance_established,
    }
