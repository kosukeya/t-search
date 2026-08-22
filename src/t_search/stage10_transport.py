"""Stage 10C continuation-aware A/B/C measurement transport.

Stage 10B selected a continuation-specific physical quadratic-form object
(F_{h,o}, N_h) that exactly reproduces the Stage 9C future-signature
likelihoods at the A/e2 reference node.  Stage 10C represents that same
physical object in every canonical A/B/C QR-support chart and verifies that
representation transport agrees with direct reconstruction.

For a continuation h with support-coordinate matrix C_{h,X,j}, a physical
quadratic form H_h is represented in chart (X,j) as

    H^X_h = C_{h,X,j}^{-dagger} H_h C_{h,X,j}^{-1}.

For a genuine Stage 9D clock map

    S^h_{Y<-X} = C_{h,Y,k} C_{h,X,j}^{-1},

quadratic forms therefore transport dually:

    H^Y_h = S^{-dagger} H^X_h S^{-1}.

Stage 10C applies this rule to the operational normalization form and every
future-signature effect form.  It establishes representation covariance,
completeness, positivity/Hermiticity, route composition, and typing over the
finite atlas.  It intentionally leaves full per-continuation probability
covariance to Stage 10D.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations, product
from typing import Literal

import numpy as np

from .stage5_clock_change import DEFAULT_ATOL, SUBSYSTEMS
from .stage7_history import CURRENT_EVENT, UPPER_EVENT
from .stage8_continuations import QuantumContinuation
from .stage9_modal import canonical_stage9_directional_carrier
from .stage9_transport import (
    audit_class_correspondence,
    class_correspondence,
    event_correspondence,
    stage9_clock_change_support_matrix,
    stage9_clock_coordinates,
)
from .stage10_lift import (
    Stage10ContinuationMeasurementLift,
    canonical_stage10b_lifts,
    lift_stage10_reference_measurement,
)

OutcomeChiKind = Literal["preserving", "swapped"]

STAGE10C_CHART_BASIS = "continuation-specific QR support coordinates"
STAGE10C_REPRESENTATION = "dual chart representation of Stage 10B physical effect/normalization forms"


@dataclass(frozen=True, slots=True)
class Stage10ChartEffect:
    continuation_id: str
    clock: str
    clock_index: int
    prediction_anchor: int
    target_event: int
    outcome_id: str
    outcome_semantics: str
    outcome_provenance: str
    coordinate_basis: str
    matrix: np.ndarray


@dataclass(frozen=True, slots=True)
class Stage10ChartMeasurement:
    family_id: str
    continuation_id: str
    clock: str
    clock_index: int
    prediction_anchor: int
    target_event: int
    representation: str
    coordinate_basis: str
    normalization_semantics: str
    normalization_form: np.ndarray
    class_correspondence: tuple[str, str]
    event_correspondence: tuple[tuple[str, str], ...]
    outcome_correspondence: tuple[tuple[str, str], ...]
    effects: tuple[Stage10ChartEffect, ...]


@dataclass(frozen=True, slots=True)
class Stage10MeasurementCorrespondenceAudit:
    event_roles_preserved: bool
    class_correspondence_valid: bool
    outcome_correspondence_bijective: bool
    outcome_semantics_preserved: bool
    valid: bool


@dataclass(frozen=True, slots=True)
class Stage10CTransportDiagnostics:
    qext_size: int
    charts_per_continuation: int
    total_charts: int
    genuine_measurement_transports: int
    three_clock_measurement_compositions: int
    max_direct_transport_normalization_residual: float
    max_direct_transport_effect_residual: float
    max_composition_normalization_residual: float
    max_composition_effect_residual: float
    max_completeness_residual: float
    max_hermiticity_residual: float
    minimum_effect_eigenvalue: float
    minimum_normalization_eigenvalue: float
    max_reference_support_normalization_residual: float
    max_reference_support_effect_residual: float
    all_chart_typing_valid: bool
    preserving_correspondence_valid: bool
    wrong_event_correspondence_rejected: bool
    wrong_class_correspondence_rejected: bool
    bare_effect_residual: float
    bare_effect_rejected: bool
    full_per_continuation_probability_covariance_established: bool


def _validate_clock(clock: str) -> str:
    if clock not in SUBSYSTEMS:
        raise ValueError("Stage 10C clock must be A, B, or C")
    return clock


def _validate_index(index: int) -> int:
    if isinstance(index, bool) or not isinstance(index, int) or index not in (0, 1, 2):
        raise ValueError("Stage 10C clock index must be 0, 1, or 2")
    return index


def _inverse_congruence(form: np.ndarray, coordinates: np.ndarray) -> np.ndarray:
    inverse = np.linalg.inv(coordinates)
    return inverse.conj().T @ np.asarray(form, dtype=np.complex128) @ inverse


def _dual_transport(form: np.ndarray, transform: np.ndarray) -> np.ndarray:
    inverse = np.linalg.inv(transform)
    return inverse.conj().T @ np.asarray(form, dtype=np.complex128) @ inverse


def _preserving_event_pairs() -> tuple[tuple[str, str], ...]:
    return (("e1", "e1"), ("e2", "e2"))


def _outcome_pairs(kind: OutcomeChiKind = "preserving") -> tuple[tuple[str, str], ...]:
    names = ("future_signature_left", "future_signature_other")
    if kind == "preserving":
        return tuple((name, name) for name in names)
    if kind == "swapped":
        return ((names[0], names[1]), (names[1], names[0]))
    raise ValueError("unknown Stage 10C outcome correspondence")


def direct_stage10_chart_measurement(
    continuation: QuantumContinuation,
    clock: str,
    index: int,
    *,
    lift: Stage10ContinuationMeasurementLift | None = None,
) -> Stage10ChartMeasurement:
    """Represent one Stage 10B physical measurement object in a local chart."""

    _validate_clock(clock)
    _validate_index(index)
    selected = lift or lift_stage10_reference_measurement(continuation)
    if selected.continuation_id != continuation.continuation_id:
        raise ValueError("Stage 10C lift belongs to a different continuation")
    coordinates = stage9_clock_coordinates(continuation, clock, index)
    normalization = _inverse_congruence(
        selected.physical_normalization_form, coordinates
    )
    effects = tuple(
        Stage10ChartEffect(
            continuation_id=continuation.continuation_id,
            clock=clock,
            clock_index=index,
            prediction_anchor=selected.prediction_anchor,
            target_event=selected.target_event,
            outcome_id=effect.outcome_id,
            outcome_semantics=effect.outcome_semantics,
            outcome_provenance=effect.outcome_provenance,
            coordinate_basis=STAGE10C_CHART_BASIS,
            matrix=_inverse_congruence(effect.physical_effect_form, coordinates),
        )
        for effect in selected.effects
    )
    return Stage10ChartMeasurement(
        family_id=selected.family_id,
        continuation_id=continuation.continuation_id,
        clock=clock,
        clock_index=index,
        prediction_anchor=selected.prediction_anchor,
        target_event=selected.target_event,
        representation=STAGE10C_REPRESENTATION,
        coordinate_basis=STAGE10C_CHART_BASIS,
        normalization_semantics=selected.normalization_semantics,
        normalization_form=normalization,
        class_correspondence=(continuation.continuation_id, continuation.continuation_id),
        event_correspondence=_preserving_event_pairs(),
        outcome_correspondence=_outcome_pairs("preserving"),
        effects=effects,
    )


def canonical_stage10c_charts() -> tuple[Stage10ChartMeasurement, ...]:
    carrier = canonical_stage9_directional_carrier()
    lifts = {item.continuation_id: item for item in canonical_stage10b_lifts()}
    return tuple(
        direct_stage10_chart_measurement(
            continuation,
            clock,
            index,
            lift=lifts[continuation.continuation_id],
        )
        for continuation in carrier.continuations
        for clock in SUBSYSTEMS
        for index in range(3)
    )


def transport_stage10_chart_measurement(
    source: Stage10ChartMeasurement,
    continuation: QuantumContinuation,
    target_clock: str,
    target_index: int,
) -> Stage10ChartMeasurement:
    """Dual-transport a typed measurement through one genuine clock change."""

    _validate_clock(target_clock)
    _validate_index(target_index)
    if source.continuation_id != continuation.continuation_id:
        raise ValueError("Stage 10C source chart belongs to a different continuation")
    if source.clock == target_clock:
        raise ValueError("Stage 10C transport requires a genuine distinct-clock change")
    transform = stage9_clock_change_support_matrix(
        continuation,
        target_clock,
        target_index,
        source.clock,
        source.clock_index,
    )
    effects = tuple(
        Stage10ChartEffect(
            continuation_id=effect.continuation_id,
            clock=target_clock,
            clock_index=target_index,
            prediction_anchor=effect.prediction_anchor,
            target_event=effect.target_event,
            outcome_id=effect.outcome_id,
            outcome_semantics=effect.outcome_semantics,
            outcome_provenance=effect.outcome_provenance,
            coordinate_basis=STAGE10C_CHART_BASIS,
            matrix=_dual_transport(effect.matrix, transform),
        )
        for effect in source.effects
    )
    return Stage10ChartMeasurement(
        family_id=source.family_id,
        continuation_id=source.continuation_id,
        clock=target_clock,
        clock_index=target_index,
        prediction_anchor=source.prediction_anchor,
        target_event=source.target_event,
        representation=source.representation,
        coordinate_basis=source.coordinate_basis,
        normalization_semantics=source.normalization_semantics,
        normalization_form=_dual_transport(source.normalization_form, transform),
        class_correspondence=source.class_correspondence,
        event_correspondence=source.event_correspondence,
        outcome_correspondence=source.outcome_correspondence,
        effects=effects,
    )


def audit_measurement_correspondence(
    *,
    event_kind: str = "preserving",
    class_kind: str = "preserving",
    outcome_kind: OutcomeChiKind = "preserving",
    atol: float = DEFAULT_ATOL,
) -> Stage10MeasurementCorrespondenceAudit:
    carrier = canonical_stage9_directional_carrier()
    event = event_correspondence(event_kind)  # type: ignore[arg-type]
    klass = class_correspondence(carrier, class_kind)  # type: ignore[arg-type]
    class_audit = audit_class_correspondence(carrier, klass, atol=atol)
    outcomes = _outcome_pairs(outcome_kind)
    event_roles_preserved = bool(
        event.declared_orientation == "preserving"
        and event.target_events[1] == "e1"
        and event.target_events[2] == "e2"
    )
    sources = tuple(source for source, _ in outcomes)
    targets = tuple(target for _, target in outcomes)
    outcome_bijective = bool(
        len(set(sources)) == len(sources)
        and len(set(targets)) == len(targets)
        and set(sources) == {"future_signature_left", "future_signature_other"}
        and set(targets) == set(sources)
    )
    outcome_semantics_preserved = all(source == target for source, target in outcomes)
    valid = bool(
        event_roles_preserved
        and class_audit.valid
        and outcome_bijective
        and outcome_semantics_preserved
    )
    return Stage10MeasurementCorrespondenceAudit(
        event_roles_preserved=event_roles_preserved,
        class_correspondence_valid=class_audit.valid,
        outcome_correspondence_bijective=outcome_bijective,
        outcome_semantics_preserved=outcome_semantics_preserved,
        valid=valid,
    )


def _chart_typing_valid(chart: Stage10ChartMeasurement) -> bool:
    expected_outcomes = ("future_signature_left", "future_signature_other")
    return bool(
        chart.prediction_anchor == CURRENT_EVENT
        and chart.target_event == UPPER_EVENT
        and chart.class_correspondence
        == (chart.continuation_id, chart.continuation_id)
        and chart.event_correspondence == _preserving_event_pairs()
        and chart.outcome_correspondence == _outcome_pairs("preserving")
        and tuple(effect.outcome_id for effect in chart.effects) == expected_outcomes
        and all(effect.continuation_id == chart.continuation_id for effect in chart.effects)
        and all(effect.clock == chart.clock for effect in chart.effects)
        and all(effect.clock_index == chart.clock_index for effect in chart.effects)
    )


def stage10c_transport_diagnostics(
    *, atol: float = DEFAULT_ATOL
) -> Stage10CTransportDiagnostics:
    carrier = canonical_stage9_directional_carrier()
    lifts = {item.continuation_id: item for item in canonical_stage10b_lifts()}

    charts: dict[tuple[str, str, int], Stage10ChartMeasurement] = {}
    max_completeness = 0.0
    max_hermiticity = 0.0
    min_effect = float("inf")
    min_normalization = float("inf")
    max_reference_normalization = 0.0
    max_reference_effect = 0.0
    all_typing = True

    for continuation in carrier.continuations:
        lift = lifts[continuation.continuation_id]
        for clock in SUBSYSTEMS:
            for index in range(3):
                chart = direct_stage10_chart_measurement(
                    continuation, clock, index, lift=lift
                )
                charts[(continuation.continuation_id, clock, index)] = chart
                all_typing = bool(all_typing and _chart_typing_valid(chart))
                effect_sum = sum(
                    (effect.matrix for effect in chart.effects),
                    start=np.zeros_like(chart.normalization_form),
                )
                max_completeness = max(
                    max_completeness,
                    float(np.linalg.norm(effect_sum - chart.normalization_form)),
                )
                max_hermiticity = max(
                    max_hermiticity,
                    float(np.linalg.norm(
                        chart.normalization_form - chart.normalization_form.conj().T
                    )),
                )
                normalized_hermitian = (
                    chart.normalization_form + chart.normalization_form.conj().T
                ) / 2.0
                min_normalization = min(
                    min_normalization,
                    float(np.min(np.linalg.eigvalsh(normalized_hermitian))),
                )
                for effect in chart.effects:
                    max_hermiticity = max(
                        max_hermiticity,
                        float(np.linalg.norm(effect.matrix - effect.matrix.conj().T)),
                    )
                    hermitian = (effect.matrix + effect.matrix.conj().T) / 2.0
                    min_effect = min(
                        min_effect,
                        float(np.min(np.linalg.eigvalsh(hermitian))),
                    )

        reference = charts[(continuation.continuation_id, "A", UPPER_EVENT)]
        max_reference_normalization = max(
            max_reference_normalization,
            float(np.linalg.norm(
                reference.normalization_form - lift.support_normalization_matrix
            )),
        )
        for chart_effect, lifted_effect in zip(
            reference.effects, lift.effects, strict=True
        ):
            max_reference_effect = max(
                max_reference_effect,
                float(np.linalg.norm(
                    chart_effect.matrix - lifted_effect.support_effect_matrix
                )),
            )

    max_direct_normalization = 0.0
    max_direct_effect = 0.0
    transport_count = 0
    bare_residual = 0.0
    for continuation in carrier.continuations:
        for source_clock, target_clock in permutations(SUBSYSTEMS, 2):
            for source_index, target_index in product(range(3), repeat=2):
                source = charts[
                    (continuation.continuation_id, source_clock, source_index)
                ]
                direct_target = charts[
                    (continuation.continuation_id, target_clock, target_index)
                ]
                transported = transport_stage10_chart_measurement(
                    source, continuation, target_clock, target_index
                )
                max_direct_normalization = max(
                    max_direct_normalization,
                    float(np.linalg.norm(
                        transported.normalization_form - direct_target.normalization_form
                    )),
                )
                for transported_effect, direct_effect, source_effect in zip(
                    transported.effects,
                    direct_target.effects,
                    source.effects,
                    strict=True,
                ):
                    max_direct_effect = max(
                        max_direct_effect,
                        float(np.linalg.norm(
                            transported_effect.matrix - direct_effect.matrix
                        )),
                    )
                    bare_residual = max(
                        bare_residual,
                        float(np.linalg.norm(
                            source_effect.matrix - direct_effect.matrix
                        )),
                    )
                transport_count += 1

    max_composition_normalization = 0.0
    max_composition_effect = 0.0
    composition_count = 0
    for continuation in carrier.continuations:
        for source_clock, middle_clock, target_clock in permutations(SUBSYSTEMS, 3):
            for source_index, middle_index, target_index in product(range(3), repeat=3):
                source = charts[
                    (continuation.continuation_id, source_clock, source_index)
                ]
                middle = transport_stage10_chart_measurement(
                    source, continuation, middle_clock, middle_index
                )
                composed = transport_stage10_chart_measurement(
                    middle, continuation, target_clock, target_index
                )
                direct = transport_stage10_chart_measurement(
                    source, continuation, target_clock, target_index
                )
                max_composition_normalization = max(
                    max_composition_normalization,
                    float(np.linalg.norm(
                        composed.normalization_form - direct.normalization_form
                    )),
                )
                for composed_effect, direct_effect in zip(
                    composed.effects, direct.effects, strict=True
                ):
                    max_composition_effect = max(
                        max_composition_effect,
                        float(np.linalg.norm(
                            composed_effect.matrix - direct_effect.matrix
                        )),
                    )
                composition_count += 1

    preserving = audit_measurement_correspondence(
        event_kind="preserving", class_kind="preserving", outcome_kind="preserving"
    )
    wrong_event = audit_measurement_correspondence(
        event_kind="misdeclared-preserving",
        class_kind="preserving",
        outcome_kind="preserving",
    )
    wrong_class = audit_measurement_correspondence(
        event_kind="preserving",
        class_kind="swapped-classes",
        outcome_kind="preserving",
    )

    return Stage10CTransportDiagnostics(
        qext_size=len(carrier.continuations),
        charts_per_continuation=len(SUBSYSTEMS) * 3,
        total_charts=len(charts),
        genuine_measurement_transports=transport_count,
        three_clock_measurement_compositions=composition_count,
        max_direct_transport_normalization_residual=max_direct_normalization,
        max_direct_transport_effect_residual=max_direct_effect,
        max_composition_normalization_residual=max_composition_normalization,
        max_composition_effect_residual=max_composition_effect,
        max_completeness_residual=max_completeness,
        max_hermiticity_residual=max_hermiticity,
        minimum_effect_eigenvalue=min_effect,
        minimum_normalization_eigenvalue=min_normalization,
        max_reference_support_normalization_residual=max_reference_normalization,
        max_reference_support_effect_residual=max_reference_effect,
        all_chart_typing_valid=all_typing,
        preserving_correspondence_valid=preserving.valid,
        wrong_event_correspondence_rejected=not wrong_event.valid,
        wrong_class_correspondence_rejected=not wrong_class.valid,
        bare_effect_residual=bare_residual,
        bare_effect_rejected=bare_residual > 10 * atol,
        full_per_continuation_probability_covariance_established=False,
    )


def stage10c_summary(*, atol: float = DEFAULT_ATOL) -> dict[str, object]:
    diagnostics = stage10c_transport_diagnostics(atol=atol)
    return {
        "qext_size": diagnostics.qext_size,
        "total_charts": diagnostics.total_charts,
        "genuine_measurement_transports": diagnostics.genuine_measurement_transports,
        "three_clock_measurement_compositions": diagnostics.three_clock_measurement_compositions,
        "max_direct_transport_normalization_residual": diagnostics.max_direct_transport_normalization_residual,
        "max_direct_transport_effect_residual": diagnostics.max_direct_transport_effect_residual,
        "max_composition_normalization_residual": diagnostics.max_composition_normalization_residual,
        "max_composition_effect_residual": diagnostics.max_composition_effect_residual,
        "max_completeness_residual": diagnostics.max_completeness_residual,
        "max_hermiticity_residual": diagnostics.max_hermiticity_residual,
        "minimum_effect_eigenvalue": diagnostics.minimum_effect_eigenvalue,
        "minimum_normalization_eigenvalue": diagnostics.minimum_normalization_eigenvalue,
        "all_chart_typing_valid": diagnostics.all_chart_typing_valid,
        "preserving_correspondence_valid": diagnostics.preserving_correspondence_valid,
        "wrong_event_correspondence_rejected": diagnostics.wrong_event_correspondence_rejected,
        "wrong_class_correspondence_rejected": diagnostics.wrong_class_correspondence_rejected,
        "bare_effect_residual": diagnostics.bare_effect_residual,
        "bare_effect_rejected": diagnostics.bare_effect_rejected,
        "full_per_continuation_probability_covariance_established": diagnostics.full_per_continuation_probability_covariance_established,
    }
