"""Stage 10D per-continuation Born-probability covariance.

Stage 10C established that the typed future-signature measurement *forms* are
covariant over the continuation-specific A/B/C clock atlas.  Stage 10D now
checks the operational probabilities themselves before any continuation-weight
aggregation.

For a local chart state z and the Stage 10C effect/normalization forms,

    p(o|h,X,j) = z^dagger F^X_{h,o} z / (z^dagger N^X_h z).

The canonical continuation states must reproduce the unchanged Stage 9C
future-signature likelihoods at all 18 charts.  A deterministic family of
additional constrained physical-coordinate probes is also transported through
the atlas.  Those probes are used to rule out accidental equality on the two
canonical states and to make wrong-normalization controls discriminating.

This stage establishes the typed *per-continuation* measurement-family
covariance.  Continuation-weight aggregation, epistemic/ontic public views,
and evidence-update covariance remain Stage 10E work.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Literal

import numpy as np

from .stage5_clock_change import DEFAULT_ATOL, SUBSYSTEMS
from .stage7_history import UPPER_EVENT
from .stage8_continuations import QuantumContinuation
from .stage9_modal import (
    FUTURE_SIGNATURE_LEFT,
    FUTURE_SIGNATURE_OTHER,
    canonical_stage9_directional_carrier,
    continuation_future_signature_probabilities,
)
from .stage9_substrate import stage9_physical_basis
from .stage9_transport import (
    stage9_clock_coordinates,
    stage9_reduced_support_coordinates,
    stage9_support_metric,
)
from .stage10_lift import (
    Stage10ContinuationMeasurementLift,
    canonical_stage10b_lifts,
)
from .stage10_transport import (
    Stage10ChartMeasurement,
    audit_measurement_correspondence,
    canonical_stage10c_charts,
)

MeasurementCovarianceStatus = Literal[
    "established", "partial", "refuted", "not_established"
]

STAGE10D_PROBE_FAMILY = (
    "14 physical-coordinate basis probes + adjacent real/phase superpositions + dense complex probe"
)


@dataclass(frozen=True, slots=True)
class Stage10DProbe:
    probe_id: str
    physical_coordinates: np.ndarray


@dataclass(frozen=True, slots=True)
class Stage10DProbabilityDiagnostics:
    continuation_count: int
    charts_per_continuation: int
    canonical_probability_evaluations: int
    max_pairwise_canonical_probability_residual: float
    max_stage9c_reference_probability_residual: float
    max_canonical_probability_sum_residual: float
    minimum_canonical_probability: float
    maximum_canonical_probability: float
    minimum_canonical_denominator: float
    per_continuation_before_weighting: bool
    branch_weight_aggregation_performed: bool
    swapped_outcome_semantics_rejected: bool
    swapped_outcome_numeric_residual: float
    probe_family_size: int
    probe_states_in_physical_span: bool
    probe_probability_evaluations: int
    max_probe_chart_covariance_residual: float
    max_probe_probability_sum_residual: float
    minimum_probe_probability: float
    maximum_probe_probability: float
    minimum_probe_denominator: float
    wrong_identity_normalization_probability_residual: float
    wrong_identity_normalization_sum_residual: float
    wrong_physical_metric_probability_residual: float
    wrong_physical_metric_sum_residual: float
    wrong_identity_normalization_rejected: bool
    wrong_physical_metric_rejected: bool
    accidental_canonical_equality_ruled_out: bool
    completeness_probability_covariance: bool
    positivity_probability_covariance: bool
    per_continuation_probability_covariance: bool
    stage9c_reference_likelihood_covariance: bool
    measurement_covariance_status: MeasurementCovarianceStatus
    weighted_modal_update_covariance_established: bool


def stage10d_probe_family() -> tuple[Stage10DProbe, ...]:
    """Return deterministic nonzero coordinates in the 14D physical space.

    Every vector is a valid constrained input because it is interpreted as
    coordinates in the continuation-specific Stage 9 physical basis.  The
    family deliberately includes phase-sensitive superpositions so that a
    control cannot pass merely because basis-state diagonal matrix elements
    happen to agree.
    """

    dim = 14
    probes: list[Stage10DProbe] = []
    eye = np.eye(dim, dtype=np.complex128)
    for index in range(dim):
        probes.append(Stage10DProbe(f"basis_{index}", eye[:, index].copy()))

    for index in range(dim - 1):
        real = (eye[:, index] + eye[:, index + 1]) / np.sqrt(2.0)
        phase = (eye[:, index] + 1j * eye[:, index + 1]) / np.sqrt(2.0)
        probes.append(Stage10DProbe(f"real_pair_{index}_{index+1}", real))
        probes.append(Stage10DProbe(f"phase_pair_{index}_{index+1}", phase))

    dense = np.arange(1, dim + 1, dtype=np.float64) + 1j * np.arange(
        dim, 0, -1, dtype=np.float64
    )
    dense = dense / np.linalg.norm(dense)
    probes.append(Stage10DProbe("dense_complex", dense.astype(np.complex128)))
    return tuple(probes)


def _chart_lookup() -> dict[tuple[str, str, int], Stage10ChartMeasurement]:
    return {
        (chart.continuation_id, chart.clock, chart.clock_index): chart
        for chart in canonical_stage10c_charts()
    }


def _lift_lookup() -> dict[str, Stage10ContinuationMeasurementLift]:
    return {lift.continuation_id: lift for lift in canonical_stage10b_lifts()}


def _validate_real_denominator(value: complex, *, atol: float) -> float:
    if abs(float(value.imag)) > 10 * atol:
        raise ValueError("Stage 10D normalization denominator acquired imaginary part")
    denominator = float(value.real)
    if denominator <= atol:
        raise ValueError("Stage 10D normalization denominator is non-positive")
    return denominator


def _effect_probabilities(
    state: np.ndarray,
    chart: Stage10ChartMeasurement,
    normalization: np.ndarray,
    *,
    atol: float,
) -> tuple[tuple[str, float], ...]:
    vector = np.asarray(state, dtype=np.complex128)
    denominator = _validate_real_denominator(
        np.vdot(vector, normalization @ vector), atol=atol
    )
    values: list[tuple[str, float]] = []
    for effect in chart.effects:
        numerator = np.vdot(vector, effect.matrix @ vector)
        if abs(float(numerator.imag)) > 10 * atol:
            raise ValueError("Stage 10D effect expectation acquired imaginary part")
        values.append((effect.outcome_id, float(numerator.real) / denominator))
    return tuple(values)


def stage10d_chart_probabilities(
    continuation: QuantumContinuation,
    chart: Stage10ChartMeasurement,
    *,
    physical_coordinates: np.ndarray | None = None,
    normalization: np.ndarray | None = None,
    atol: float = DEFAULT_ATOL,
) -> tuple[tuple[str, float], ...]:
    """Evaluate one typed Stage 10C chart on a canonical or probe state."""

    if chart.continuation_id != continuation.continuation_id:
        raise ValueError("Stage 10D chart belongs to a different continuation")
    if physical_coordinates is None:
        state = stage9_reduced_support_coordinates(
            continuation, chart.clock, chart.clock_index
        )
    else:
        coordinates = np.asarray(physical_coordinates, dtype=np.complex128)
        if coordinates.shape != (14,) or float(np.linalg.norm(coordinates)) <= atol:
            raise ValueError("Stage 10D probe coordinates must be a nonzero 14-vector")
        state = stage9_clock_coordinates(
            continuation, chart.clock, chart.clock_index
        ) @ coordinates
    selected_normalization = (
        chart.normalization_form if normalization is None else normalization
    )
    return _effect_probabilities(
        state, chart, selected_normalization, atol=atol
    )


def stage10d_physical_probe_probabilities(
    lift: Stage10ContinuationMeasurementLift,
    coordinates: np.ndarray,
    *,
    atol: float = DEFAULT_ATOL,
) -> tuple[tuple[str, float], ...]:
    vector = np.asarray(coordinates, dtype=np.complex128)
    if vector.shape != (14,) or float(np.linalg.norm(vector)) <= atol:
        raise ValueError("Stage 10D physical probe must be a nonzero 14-vector")
    denominator = _validate_real_denominator(
        np.vdot(vector, lift.physical_normalization_form @ vector), atol=atol
    )
    values: list[tuple[str, float]] = []
    for effect in lift.effects:
        numerator = np.vdot(vector, effect.physical_effect_form @ vector)
        if abs(float(numerator.imag)) > 10 * atol:
            raise ValueError("Stage 10D physical effect expectation acquired imaginary part")
        values.append((effect.outcome_id, float(numerator.real) / denominator))
    return tuple(values)


def _dict(values: tuple[tuple[str, float], ...]) -> dict[str, float]:
    return dict(values)


def _probability_residual(
    left: tuple[tuple[str, float], ...],
    right: tuple[tuple[str, float], ...],
) -> float:
    lhs = _dict(left)
    rhs = _dict(right)
    if set(lhs) != set(rhs):
        return float("inf")
    return max(abs(lhs[name] - rhs[name]) for name in lhs)


def _sum_residual(values: tuple[tuple[str, float], ...]) -> float:
    return abs(sum(value for _, value in values) - 1.0)


def _bounds(values: tuple[tuple[str, float], ...]) -> tuple[float, float]:
    numbers = tuple(value for _, value in values)
    return min(numbers), max(numbers)


def _normalization_denominator(
    state: np.ndarray, normalization: np.ndarray, *, atol: float
) -> float:
    return _validate_real_denominator(
        np.vdot(state, normalization @ state), atol=atol
    )


def _wrong_normalization_assessment(
    continuation: QuantumContinuation,
    chart: Stage10ChartMeasurement,
    probe: Stage10DProbe,
    correct: tuple[tuple[str, float], ...],
    *,
    atol: float,
) -> tuple[float, float, float, float]:
    coordinates = stage9_clock_coordinates(
        continuation, chart.clock, chart.clock_index
    )
    state = coordinates @ probe.physical_coordinates
    identity = np.eye(state.size, dtype=np.complex128)
    physical_metric = stage9_support_metric(
        continuation, chart.clock, chart.clock_index
    )

    identity_probabilities = _effect_probabilities(
        state, chart, identity, atol=atol
    )
    metric_probabilities = _effect_probabilities(
        state, chart, physical_metric, atol=atol
    )
    return (
        _probability_residual(correct, identity_probabilities),
        _sum_residual(identity_probabilities),
        _probability_residual(correct, metric_probabilities),
        _sum_residual(metric_probabilities),
    )


def stage10d_probability_diagnostics(
    *, atol: float = DEFAULT_ATOL
) -> Stage10DProbabilityDiagnostics:
    carrier = canonical_stage9_directional_carrier()
    charts = _chart_lookup()
    lifts = _lift_lookup()

    max_pairwise = 0.0
    max_reference = 0.0
    max_canonical_sum = 0.0
    min_canonical_probability = float("inf")
    max_canonical_probability = -float("inf")
    min_canonical_denominator = float("inf")
    canonical_evaluations = 0
    swapped_numeric_residual = 0.0

    for continuation in carrier.continuations:
        reference = continuation_future_signature_probabilities(
            carrier, continuation, atol=atol
        )
        node_probabilities: list[tuple[tuple[str, float], ...]] = []
        for clock in SUBSYSTEMS:
            for index in range(3):
                chart = charts[(continuation.continuation_id, clock, index)]
                values = stage10d_chart_probabilities(
                    continuation, chart, atol=atol
                )
                node_probabilities.append(values)
                canonical_evaluations += len(values)
                max_reference = max(
                    max_reference, _probability_residual(values, reference)
                )
                max_canonical_sum = max(max_canonical_sum, _sum_residual(values))
                low, high = _bounds(values)
                min_canonical_probability = min(min_canonical_probability, low)
                max_canonical_probability = max(max_canonical_probability, high)
                state = stage9_reduced_support_coordinates(
                    continuation, clock, index
                )
                min_canonical_denominator = min(
                    min_canonical_denominator,
                    _normalization_denominator(
                        state, chart.normalization_form, atol=atol
                    ),
                )
                table = _dict(values)
                swapped_numeric_residual = max(
                    swapped_numeric_residual,
                    abs(
                        table[FUTURE_SIGNATURE_LEFT]
                        - table[FUTURE_SIGNATURE_OTHER]
                    ),
                )
        for left, right in combinations(node_probabilities, 2):
            max_pairwise = max(max_pairwise, _probability_residual(left, right))

    swapped_audit = audit_measurement_correspondence(
        event_kind="preserving",
        class_kind="preserving",
        outcome_kind="swapped",
        atol=atol,
    )

    probes = stage10d_probe_family()
    probe_states_in_physical_span = True
    probe_evaluations = 0
    max_probe_covariance = 0.0
    max_probe_sum = 0.0
    min_probe_probability = float("inf")
    max_probe_probability = -float("inf")
    min_probe_denominator = float("inf")
    wrong_identity_probability = 0.0
    wrong_identity_sum = 0.0
    wrong_metric_probability = 0.0
    wrong_metric_sum = 0.0

    for continuation in carrier.continuations:
        basis = stage9_physical_basis(continuation)
        probe_states_in_physical_span = bool(
            probe_states_in_physical_span
            and basis.shape[1] == 14
            and np.linalg.matrix_rank(basis, tol=atol) == 14
        )
        lift = lifts[continuation.continuation_id]
        for probe in probes:
            ambient = basis @ probe.physical_coordinates
            probe_states_in_physical_span = bool(
                probe_states_in_physical_span
                and ambient.ndim == 1
                and float(np.linalg.norm(ambient)) > atol
            )
            physical_reference = stage10d_physical_probe_probabilities(
                lift, probe.physical_coordinates, atol=atol
            )
            for clock in SUBSYSTEMS:
                for index in range(3):
                    chart = charts[(continuation.continuation_id, clock, index)]
                    values = stage10d_chart_probabilities(
                        continuation,
                        chart,
                        physical_coordinates=probe.physical_coordinates,
                        atol=atol,
                    )
                    probe_evaluations += len(values)
                    max_probe_covariance = max(
                        max_probe_covariance,
                        _probability_residual(values, physical_reference),
                    )
                    max_probe_sum = max(max_probe_sum, _sum_residual(values))
                    low, high = _bounds(values)
                    min_probe_probability = min(min_probe_probability, low)
                    max_probe_probability = max(max_probe_probability, high)
                    state = stage9_clock_coordinates(
                        continuation, clock, index
                    ) @ probe.physical_coordinates
                    min_probe_denominator = min(
                        min_probe_denominator,
                        _normalization_denominator(
                            state, chart.normalization_form, atol=atol
                        ),
                    )
                    (
                        identity_probability_residual,
                        identity_sum_residual,
                        metric_probability_residual,
                        metric_sum_residual,
                    ) = _wrong_normalization_assessment(
                        continuation, chart, probe, values, atol=atol
                    )
                    wrong_identity_probability = max(
                        wrong_identity_probability, identity_probability_residual
                    )
                    wrong_identity_sum = max(
                        wrong_identity_sum, identity_sum_residual
                    )
                    wrong_metric_probability = max(
                        wrong_metric_probability, metric_probability_residual
                    )
                    wrong_metric_sum = max(wrong_metric_sum, metric_sum_residual)

    canonical_covariant = bool(max_pairwise <= 10 * atol)
    reference_covariant = bool(max_reference <= 10 * atol)
    canonical_complete = bool(max_canonical_sum <= 10 * atol)
    probe_complete = bool(max_probe_sum <= 10 * atol)
    positivity = bool(
        min_canonical_probability >= -10 * atol
        and max_canonical_probability <= 1.0 + 10 * atol
        and min_probe_probability >= -10 * atol
        and max_probe_probability <= 1.0 + 10 * atol
        and min_canonical_denominator > atol
        and min_probe_denominator > atol
    )
    wrong_identity_rejected = bool(
        wrong_identity_probability > 10 * atol or wrong_identity_sum > 10 * atol
    )
    wrong_metric_rejected = bool(
        wrong_metric_probability > 10 * atol or wrong_metric_sum > 10 * atol
    )
    probe_covariant = bool(max_probe_covariance <= 10 * atol)
    accidental_ruled_out = bool(
        len(probes) > 1
        and probe_states_in_physical_span
        and probe_covariant
        and wrong_identity_rejected
        and wrong_metric_rejected
    )
    swapped_rejected = bool(
        not swapped_audit.valid and swapped_numeric_residual > 10 * atol
    )
    per_continuation_covariant = bool(
        canonical_covariant
        and reference_covariant
        and probe_covariant
        and canonical_complete
        and probe_complete
        and positivity
        and swapped_rejected
        and accidental_ruled_out
    )
    status: MeasurementCovarianceStatus = (
        "established" if per_continuation_covariant else "partial"
    )

    return Stage10DProbabilityDiagnostics(
        continuation_count=len(carrier.continuations),
        charts_per_continuation=len(SUBSYSTEMS) * 3,
        canonical_probability_evaluations=canonical_evaluations,
        max_pairwise_canonical_probability_residual=max_pairwise,
        max_stage9c_reference_probability_residual=max_reference,
        max_canonical_probability_sum_residual=max_canonical_sum,
        minimum_canonical_probability=min_canonical_probability,
        maximum_canonical_probability=max_canonical_probability,
        minimum_canonical_denominator=min_canonical_denominator,
        per_continuation_before_weighting=True,
        branch_weight_aggregation_performed=False,
        swapped_outcome_semantics_rejected=swapped_rejected,
        swapped_outcome_numeric_residual=swapped_numeric_residual,
        probe_family_size=len(probes),
        probe_states_in_physical_span=probe_states_in_physical_span,
        probe_probability_evaluations=probe_evaluations,
        max_probe_chart_covariance_residual=max_probe_covariance,
        max_probe_probability_sum_residual=max_probe_sum,
        minimum_probe_probability=min_probe_probability,
        maximum_probe_probability=max_probe_probability,
        minimum_probe_denominator=min_probe_denominator,
        wrong_identity_normalization_probability_residual=wrong_identity_probability,
        wrong_identity_normalization_sum_residual=wrong_identity_sum,
        wrong_physical_metric_probability_residual=wrong_metric_probability,
        wrong_physical_metric_sum_residual=wrong_metric_sum,
        wrong_identity_normalization_rejected=wrong_identity_rejected,
        wrong_physical_metric_rejected=wrong_metric_rejected,
        accidental_canonical_equality_ruled_out=accidental_ruled_out,
        completeness_probability_covariance=canonical_complete and probe_complete,
        positivity_probability_covariance=positivity,
        per_continuation_probability_covariance=per_continuation_covariant,
        stage9c_reference_likelihood_covariance=reference_covariant,
        measurement_covariance_status=status,
        weighted_modal_update_covariance_established=False,
    )


def stage10d_summary(*, atol: float = DEFAULT_ATOL) -> dict[str, object]:
    diagnostics = stage10d_probability_diagnostics(atol=atol)
    return {
        "continuation_count": diagnostics.continuation_count,
        "charts_per_continuation": diagnostics.charts_per_continuation,
        "canonical_probability_evaluations": diagnostics.canonical_probability_evaluations,
        "max_pairwise_canonical_probability_residual": diagnostics.max_pairwise_canonical_probability_residual,
        "max_stage9c_reference_probability_residual": diagnostics.max_stage9c_reference_probability_residual,
        "max_canonical_probability_sum_residual": diagnostics.max_canonical_probability_sum_residual,
        "probe_family_size": diagnostics.probe_family_size,
        "probe_probability_evaluations": diagnostics.probe_probability_evaluations,
        "max_probe_chart_covariance_residual": diagnostics.max_probe_chart_covariance_residual,
        "max_probe_probability_sum_residual": diagnostics.max_probe_probability_sum_residual,
        "wrong_identity_normalization_probability_residual": diagnostics.wrong_identity_normalization_probability_residual,
        "wrong_identity_normalization_sum_residual": diagnostics.wrong_identity_normalization_sum_residual,
        "wrong_physical_metric_probability_residual": diagnostics.wrong_physical_metric_probability_residual,
        "wrong_physical_metric_sum_residual": diagnostics.wrong_physical_metric_sum_residual,
        "swapped_outcome_numeric_residual": diagnostics.swapped_outcome_numeric_residual,
        "per_continuation_probability_covariance": diagnostics.per_continuation_probability_covariance,
        "stage9c_reference_likelihood_covariance": diagnostics.stage9c_reference_likelihood_covariance,
        "measurement_covariance_status": diagnostics.measurement_covariance_status,
        "weighted_modal_update_covariance_established": diagnostics.weighted_modal_update_covariance_established,
    }
