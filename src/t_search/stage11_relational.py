"""Stage 11B relational observables and relational derivatives.

Stage 11A established a shared sampled constraint orbit represented in four
admissible external parameterizations. Stage 11B now asks which quantities are
relationally invariant on that orbit. Comparisons use explicit physical-event
correspondence and the internal clock T; equal raw external parameter values are
retained only as a false-matching control.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .stage11_parametrized import (
    STAGE11A_ATOL,
    STAGE11A_AFFINE,
    STAGE11A_CUBIC,
    STAGE11A_HYPERBOLIC,
    STAGE11A_IDENTITY,
    Stage11ParametrizedTrajectory,
    canonical_stage11a_positive_family,
    stage11a_event_correspondence,
)

STAGE11B_ANCHOR_INDEX = 6
STAGE11B_TARGET_INDEX = 10
STAGE11B_RAW_MATCH_INVALID = "invalid_equal_raw_parameter_event_rule"


@dataclass(frozen=True, slots=True)
class Stage11RelationalObservation:
    parameterization_id: str
    event_id: str
    parameter_value: float
    clock_value: float
    q_value: float


@dataclass(frozen=True, slots=True)
class Stage11RelationalObservationPair:
    event_id: str
    source: Stage11RelationalObservation
    target: Stage11RelationalObservation


@dataclass(frozen=True, slots=True)
class Stage11TypedRelationalEventRole:
    parameterization_id: str
    role: str
    event_id: str
    parameter_value: float
    clock_value: float
    q_value: float


@dataclass(frozen=True, slots=True)
class Stage11RawParameterMatchWitness:
    source_parameterization_id: str
    target_parameterization_id: str
    raw_parameter_value: float
    source_event_id: str
    target_event_id: str
    source_clock_value: float
    target_clock_value: float
    same_physical_event: bool


@dataclass(frozen=True, slots=True)
class Stage11RawParameterMatchControl:
    source_parameterization_id: str
    target_parameterization_id: str
    equal_raw_parameter_overlap_count: int
    false_event_identity_count: int
    coincident_same_event_count: int
    classification: str
    raw_parameter_matching_rejected: bool


@dataclass(frozen=True, slots=True)
class Stage11BDiagnostics:
    positive_parameterization_count: int
    event_count: int
    relational_observable_evaluation_count: int
    relational_derivative_evaluation_count: int
    max_relational_observable_residual: float
    max_relational_derivative_residual: float
    max_momentum_relational_derivative_residual: float
    reference_relational_derivative: float
    nonlinear_raw_rate_difference_count: int
    max_nonlinear_raw_rate_difference: float
    anchor_target_view_count: int
    anchor_event_id: str
    target_event_id: str
    raw_equal_parameter_overlap_count: int
    raw_equal_parameter_false_identity_count: int
    raw_equal_parameter_coincident_same_event_count: int
    raw_parameter_matching_classification: str
    raw_parameter_matching_rejected: bool
    criteria_17_23_satisfied: bool


def _event_index(trajectory: Stage11ParametrizedTrajectory, event_id: str) -> int:
    try:
        return trajectory.event_ids.index(event_id)
    except ValueError as exc:
        raise ValueError(f"unknown Stage 11B physical event {event_id!r}") from exc


def stage11b_relational_observable_at_event(
    trajectory: Stage11ParametrizedTrajectory,
    event_id: str,
) -> Stage11RelationalObservation:
    """Return q at one explicitly typed physical event."""

    index = _event_index(trajectory, event_id)
    return Stage11RelationalObservation(
        parameterization_id=trajectory.parameterization_id,
        event_id=event_id,
        parameter_value=float(trajectory.parameter_labels[index]),
        clock_value=float(trajectory.clock_values[index]),
        q_value=float(trajectory.q_values[index]),
    )


def stage11b_relational_observable(
    trajectory: Stage11ParametrizedTrajectory,
    clock_value: float,
    *,
    atol: float = STAGE11A_ATOL,
) -> Stage11RelationalObservation:
    """Construct the sampled relational observable q(T=tau).

    Stage 11B deliberately requires a unique internal-clock reading on the
    tested domain. Raw external parameter values are not consulted when finding
    the physical event.
    """

    matches = np.flatnonzero(
        np.isclose(trajectory.clock_values, float(clock_value), atol=atol, rtol=0.0)
    )
    if matches.size != 1:
        raise ValueError(
            "Stage 11B q(T=tau) requires exactly one physical event with the requested internal-clock reading"
        )
    return stage11b_relational_observable_at_event(
        trajectory, trajectory.event_ids[int(matches[0])]
    )


def stage11b_corresponded_relational_observables(
    source: Stage11ParametrizedTrajectory,
    target: Stage11ParametrizedTrajectory,
) -> tuple[Stage11RelationalObservationPair, ...]:
    """Compare q(T=tau) only after explicit Stage 11A event correspondence."""

    pairs: list[Stage11RelationalObservationPair] = []
    for correspondence in stage11a_event_correspondence(source, target):
        source_observation = stage11b_relational_observable(
            source, correspondence.clock_value
        )
        target_observation = stage11b_relational_observable(
            target, correspondence.clock_value
        )
        if (
            source_observation.event_id != correspondence.event_id
            or target_observation.event_id != correspondence.event_id
        ):
            raise ValueError(
                "Stage 11B relational comparison drifted from explicit physical-event correspondence"
            )
        pairs.append(
            Stage11RelationalObservationPair(
                event_id=correspondence.event_id,
                source=source_observation,
                target=target_observation,
            )
        )
    return tuple(pairs)


def stage11b_relational_derivatives(
    trajectory: Stage11ParametrizedTrajectory,
    *,
    atol: float = STAGE11A_ATOL,
) -> np.ndarray:
    """Return dq/dT=(dq/dlambda)/(dT/dlambda) on every sampled event."""

    lapse = np.asarray(trajectory.lapse_values, dtype=float)
    if np.any(lapse <= atol):
        raise ValueError("Stage 11B relational derivative requires positive nonzero lapse")
    return np.asarray(trajectory.raw_q_rates, dtype=float) / lapse


def canonical_stage11b_anchor_target_views() -> tuple[Stage11TypedRelationalEventRole, ...]:
    """Keep anchor/target event roles explicit across all positive charts."""

    views: list[Stage11TypedRelationalEventRole] = []
    for trajectory in canonical_stage11a_positive_family():
        for role, index in (
            ("prediction_anchor", STAGE11B_ANCHOR_INDEX),
            ("measurement_target", STAGE11B_TARGET_INDEX),
        ):
            views.append(
                Stage11TypedRelationalEventRole(
                    parameterization_id=trajectory.parameterization_id,
                    role=role,
                    event_id=trajectory.event_ids[index],
                    parameter_value=float(trajectory.parameter_labels[index]),
                    clock_value=float(trajectory.clock_values[index]),
                    q_value=float(trajectory.q_values[index]),
                )
            )
    return tuple(views)


def stage11b_raw_equal_parameter_matches(
    source: Stage11ParametrizedTrajectory,
    target: Stage11ParametrizedTrajectory,
    *,
    atol: float = STAGE11A_ATOL,
) -> tuple[Stage11RawParameterMatchWitness, ...]:
    """Enumerate equal-raw-parameter coincidences without treating them as events."""

    witnesses: list[Stage11RawParameterMatchWitness] = []
    for source_index, source_value in enumerate(source.parameter_labels):
        for target_index, target_value in enumerate(target.parameter_labels):
            if not np.isclose(source_value, target_value, atol=atol, rtol=0.0):
                continue
            source_event = source.event_ids[source_index]
            target_event = target.event_ids[target_index]
            witnesses.append(
                Stage11RawParameterMatchWitness(
                    source_parameterization_id=source.parameterization_id,
                    target_parameterization_id=target.parameterization_id,
                    raw_parameter_value=float(source_value),
                    source_event_id=source_event,
                    target_event_id=target_event,
                    source_clock_value=float(source.clock_values[source_index]),
                    target_clock_value=float(target.clock_values[target_index]),
                    same_physical_event=source_event == target_event,
                )
            )
    return tuple(witnesses)


def stage11b_raw_parameter_match_control() -> Stage11RawParameterMatchControl:
    """Classify equal raw lambda as an invalid event-identification rule."""

    family = {
        item.parameterization_id: item for item in canonical_stage11a_positive_family()
    }
    source = family[STAGE11A_IDENTITY]
    target = family[STAGE11A_AFFINE]
    witnesses = stage11b_raw_equal_parameter_matches(source, target)
    false_count = sum(not item.same_physical_event for item in witnesses)
    same_count = sum(item.same_physical_event for item in witnesses)
    rejected = len(witnesses) > 0 and false_count > 0
    return Stage11RawParameterMatchControl(
        source_parameterization_id=source.parameterization_id,
        target_parameterization_id=target.parameterization_id,
        equal_raw_parameter_overlap_count=len(witnesses),
        false_event_identity_count=false_count,
        coincident_same_event_count=same_count,
        classification=(STAGE11B_RAW_MATCH_INVALID if rejected else "inconclusive"),
        raw_parameter_matching_rejected=rejected,
    )


def stage11b_diagnostics() -> Stage11BDiagnostics:
    family = canonical_stage11a_positive_family()
    reference = next(
        item for item in family if item.parameterization_id == STAGE11A_IDENTITY
    )
    reference_derivatives = stage11b_relational_derivatives(reference)

    max_observable_residual = 0.0
    max_derivative_residual = 0.0
    max_momentum_residual = 0.0
    observable_evaluations = 0
    derivative_evaluations = 0
    nonlinear_raw_rate_difference_count = 0
    max_nonlinear_raw_rate_difference = 0.0

    for trajectory in family:
        pairs = stage11b_corresponded_relational_observables(reference, trajectory)
        observable_evaluations += len(pairs)
        for pair in pairs:
            max_observable_residual = max(
                max_observable_residual,
                abs(pair.source.q_value - pair.target.q_value),
            )

        derivatives = stage11b_relational_derivatives(trajectory)
        derivative_evaluations += derivatives.size
        max_derivative_residual = max(
            max_derivative_residual,
            float(np.max(np.abs(derivatives - reference_derivatives))),
        )
        max_momentum_residual = max(
            max_momentum_residual,
            float(np.max(np.abs(derivatives - trajectory.p_values))),
        )

        if trajectory.parameterization_id in (STAGE11A_CUBIC, STAGE11A_HYPERBOLIC):
            raw_difference = np.abs(trajectory.raw_q_rates - reference.raw_q_rates)
            nonlinear_raw_rate_difference_count += int(
                np.count_nonzero(raw_difference > STAGE11A_ATOL)
            )
            max_nonlinear_raw_rate_difference = max(
                max_nonlinear_raw_rate_difference,
                float(np.max(raw_difference)),
            )

    anchor_target_views = canonical_stage11b_anchor_target_views()
    anchor_ids = {
        item.event_id for item in anchor_target_views if item.role == "prediction_anchor"
    }
    target_ids = {
        item.event_id for item in anchor_target_views if item.role == "measurement_target"
    }
    typed_anchor_target = (
        len(anchor_ids) == 1
        and len(target_ids) == 1
        and next(iter(anchor_ids)) != next(iter(target_ids))
        and len(anchor_target_views) == 2 * len(family)
    )

    raw_control = stage11b_raw_parameter_match_control()
    criteria = (
        observable_evaluations == len(family) * len(reference.event_ids)
        and max_observable_residual <= STAGE11A_ATOL
        and derivative_evaluations == len(family) * len(reference.event_ids)
        and max_derivative_residual <= STAGE11A_ATOL
        and max_momentum_residual <= STAGE11A_ATOL
        and nonlinear_raw_rate_difference_count > 0
        and max_nonlinear_raw_rate_difference > STAGE11A_ATOL
        and typed_anchor_target
        and raw_control.raw_parameter_matching_rejected
        and raw_control.classification == STAGE11B_RAW_MATCH_INVALID
    )

    return Stage11BDiagnostics(
        positive_parameterization_count=len(family),
        event_count=len(reference.event_ids),
        relational_observable_evaluation_count=observable_evaluations,
        relational_derivative_evaluation_count=derivative_evaluations,
        max_relational_observable_residual=max_observable_residual,
        max_relational_derivative_residual=max_derivative_residual,
        max_momentum_relational_derivative_residual=max_momentum_residual,
        reference_relational_derivative=float(reference_derivatives[0]),
        nonlinear_raw_rate_difference_count=nonlinear_raw_rate_difference_count,
        max_nonlinear_raw_rate_difference=max_nonlinear_raw_rate_difference,
        anchor_target_view_count=len(anchor_target_views),
        anchor_event_id=next(iter(anchor_ids)),
        target_event_id=next(iter(target_ids)),
        raw_equal_parameter_overlap_count=raw_control.equal_raw_parameter_overlap_count,
        raw_equal_parameter_false_identity_count=raw_control.false_event_identity_count,
        raw_equal_parameter_coincident_same_event_count=raw_control.coincident_same_event_count,
        raw_parameter_matching_classification=raw_control.classification,
        raw_parameter_matching_rejected=raw_control.raw_parameter_matching_rejected,
        criteria_17_23_satisfied=criteria,
    )


def stage11b_summary() -> dict[str, object]:
    diagnostics = stage11b_diagnostics()
    return {
        "status": (
            "Stage 11B completed; criteria 17–23 satisfied"
            if diagnostics.criteria_17_23_satisfied
            else "Stage 11B incomplete"
        ),
        "relational_observable": "q(T=tau)",
        "relational_derivative": "dq/dT=(dq/dlambda)/(dT/dlambda)",
        "positive_parameterizations": diagnostics.positive_parameterization_count,
        "event_count": diagnostics.event_count,
        "relational_observable_evaluations": diagnostics.relational_observable_evaluation_count,
        "relational_derivative_evaluations": diagnostics.relational_derivative_evaluation_count,
        "max_relational_observable_residual": diagnostics.max_relational_observable_residual,
        "max_relational_derivative_residual": diagnostics.max_relational_derivative_residual,
        "reference_dq_dT": diagnostics.reference_relational_derivative,
        "nonlinear_raw_rate_difference_count": diagnostics.nonlinear_raw_rate_difference_count,
        "max_nonlinear_raw_rate_difference": diagnostics.max_nonlinear_raw_rate_difference,
        "anchor_event_id": diagnostics.anchor_event_id,
        "target_event_id": diagnostics.target_event_id,
        "raw_equal_parameter_overlap_count": diagnostics.raw_equal_parameter_overlap_count,
        "raw_equal_parameter_false_identity_count": diagnostics.raw_equal_parameter_false_identity_count,
        "raw_equal_parameter_coincident_same_event_count": diagnostics.raw_equal_parameter_coincident_same_event_count,
        "raw_parameter_matching_classification": diagnostics.raw_parameter_matching_classification,
        "bounded_result": "Stage 11B relational observable/derivative covariance on the frozen positive family = established",
        "guard": "relational covariance on one finite orbit != general covariance",
    }
