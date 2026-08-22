"""Stage 10D per-continuation Born-probability covariance.

Stage 10C established that the typed future-signature measurement *forms* are
covariant over the continuation-specific A/B/C clock atlas.  Stage 10D checks
the operational probabilities themselves before any continuation-weight
aggregation.

For a local chart state z and the Stage 10C effect/normalization forms,

    p(o|h,X,j) = z^dagger F^X_{h,o} z / (z^dagger N^X_h z).

The canonical continuation states must reproduce the unchanged Stage 9C
future-signature likelihoods at all 18 charts.  A deterministic,
Hermitian-tomography-complete family of additional constrained physical-
coordinate probes is also transported through the atlas.  Those probes rule
out accidental equality on the canonical states and make wrong-normalization
controls discriminating.

A Stage 10D pilot exposed an important finite-model fact: the Stage 9D physical
metric can numerically coincide with the Stage 10 operational normalization
form even though the two remain differently typed resources.  Therefore the
negative metric control is a genuinely *misaligned chart metric*, not the
correct same-chart Stage 9D metric.  Typed distinction does not imply numerical
inequality.

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
from .stage8_continuations import QuantumContinuation
from .stage9_modal import (
    FUTURE_SIGNATURE_LEFT,
    FUTURE_SIGNATURE_OTHER,
    canonical_stage9_directional_carrier,
    continuation_future_signature_probabilities,
)
from .stage9_substrate import (
    canonical_stage9_physical_state,
    stage9_physical_basis,
)
from .stage9_transport import stage9_clock_coordinates
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
    "Hermitian-tomography-complete 196 physical-coordinate probes"
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
    max_operational_physical_metric_form_residual: float
    physical_metric_operational_normalization_numerically_coincident: bool
    wrong_identity_normalization_probability_residual: float
    wrong_identity_normalization_sum_residual: float
    misaligned_metric_form_residual: float
    misaligned_metric_probability_residual: float
    misaligned_metric_sum_residual: float
    wrong_identity_normalization_rejected: bool
    misaligned_metric_rejected: bool
    accidental_canonical_equality_ruled_out: bool
    completeness_probability_covariance: bool
    positivity_probability_covariance: bool
    per_continuation_probability_covariance: bool
    stage9c_reference_likelihood_covariance: bool
    measurement_covariance_status: MeasurementCovarianceStatus
    weighted_modal_update_covariance_established: bool


def stage10d_probe_family() -> tuple[Stage10DProbe, ...]:
    """Return a tomography-complete family for 14D Hermitian quadratic forms.

    For every coordinate basis vector e_i, and every pair i<j, the family
    contains e_i, (e_i+e_j)/sqrt(2), and (e_i+i e_j)/sqrt(2).  Their quadratic
    expectations determine all diagonal, real off-diagonal, and imaginary
    off-diagonal entries of a Hermitian form.  Thus a wrong Hermitian
    normalization cannot hide merely because the two canonical states fail to
    probe a differing matrix component.

    Every probe is a valid constrained input because it is interpreted as
    coordinates in the continuation-specific Stage 9 physical basis.
    """

    dim = 14
    eye = np.eye(dim, dtype=np.complex128)
    probes: list[Stage10DProbe] = [
        Stage10DProbe(f"basis_{index}", eye[:, index].copy())
        for index in range(dim)
    ]
    for left, right in combinations(range(dim), 2):
        real = (eye[:, left] + eye[:, right]) / np.sqrt(2.0)
        phase = (eye[:, left] + 1j * eye[:, right]) / np.sqrt(2.0)
        probes.append(Stage10DProbe(f"real_pair_{left}_{right}", real))
        probes.append(Stage10DProbe(f"phase_pair_{left}_{right}", phase))
    return tuple(probes)


def _chart_lookup() -> dict[tuple[str, str, int], Stage10ChartMeasurement]:
    return {
        (chart.continuation_id, chart.clock, chart.clock_index): chart
        for chart in canonical_stage10c_charts()
    }


def _lift_lookup() -> dict[str, Stage10ContinuationMeasurementLift]:
    return {lift.continuation_id: lift for lift in canonical_stage10b_lifts()}


def _physical_coordinates(
    continuation: QuantumContinuation, *, atol: float
) -> np.ndarray:
    basis = stage9_physical_basis(continuation)
    state = canonical_stage9_physical_state(continuation)
    coordinates, _, rank, _ = np.linalg.lstsq(basis, state, rcond=None)
    if rank != 14:
        raise ValueError("Stage 10D physical basis is not full rank")
    if float(np.linalg.norm(basis @ coordinates - state)) > 10 * atol:
        raise ValueError("Stage 10D canonical physical-coordinate reconstruction failed")
    return np.asarray(coordinates, dtype=np.complex128)


def _support_metric_from_coordinates(coordinates: np.ndarray) -> np.ndarray:
    inverse = np.linalg.inv(coordinates)
    return inverse.conj().T @ inverse


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
    coordinates = stage9_clock_coordinates(
        continuation, chart.clock, chart.clock_index
    )
    physical = (
        _physical_coordinates(continuation, atol=atol)
        if physical_coordinates is None
        else np.asarray(physical_coordinates, dtype=np.complex128)
    )
    if physical.shape != (14,) or float(np.linalg.norm(physical)) <= atol:
        raise ValueError("Stage 10D physical coordinates must be a nonzero 14-vector")
    state = coordinates @ physical
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


def _most_misaligned_metric(
    key: tuple[str, str, int],
    chart_normalization: np.ndarray,
    metrics: dict[tuple[str, str, int], np.ndarray],
) -> tuple[np.ndarray, float]:
    continuation_id, _, _ = key
    candidates = tuple(
        (metric_key, metric)
        for metric_key, metric in metrics.items()
        if metric_key[0] == continuation_id and metric_key != key
    )
    if not candidates:
        raise ValueError("Stage 10D requires at least two charts for metric control")
    metric_key, metric = max(
        candidates,
        key=lambda item: float(np.linalg.norm(item[1] - chart_normalization)),
    )
    del metric_key
    residual = float(np.linalg.norm(metric - chart_normalization))
    return metric, residual


def stage10d_probability_diagnostics(
    *, atol: float = DEFAULT_ATOL
) -> Stage10DProbabilityDiagnostics:
    carrier = canonical_stage9_directional_carrier()
    charts = _chart_lookup()
    lifts = _lift_lookup()

    # Cache the 18 expensive continuation-specific QR coordinate matrices once.
    coordinate_matrices: dict[tuple[str, str, int], np.ndarray] = {}
    physical_metrics: dict[tuple[str, str, int], np.ndarray] = {}
    canonical_physical: dict[str, np.ndarray] = {}
    for continuation in carrier.continuations:
        canonical_physical[continuation.continuation_id] = _physical_coordinates(
            continuation, atol=atol
        )
        for clock in SUBSYSTEMS:
            for index in range(3):
                key = (continuation.continuation_id, clock, index)
                coordinates = stage9_clock_coordinates(continuation, clock, index)
                coordinate_matrices[key] = coordinates
                physical_metrics[key] = _support_metric_from_coordinates(coordinates)

    max_pairwise = 0.0
    max_reference = 0.0
    max_canonical_sum = 0.0
    min_canonical_probability = float("inf")
    max_canonical_probability = -float("inf")
    min_canonical_denominator = float("inf")
    canonical_evaluations = 0
    swapped_numeric_residual = 0.0
    max_operational_metric_form_residual = 0.0

    for continuation in carrier.continuations:
        reference = continuation_future_signature_probabilities(
            carrier, continuation, atol=atol
        )
        node_probabilities: list[tuple[tuple[str, float], ...]] = []
        physical = canonical_physical[continuation.continuation_id]
        for clock in SUBSYSTEMS:
            for index in range(3):
                key = (continuation.continuation_id, clock, index)
                chart = charts[key]
                state = coordinate_matrices[key] @ physical
                values = _effect_probabilities(
                    state, chart, chart.normalization_form, atol=atol
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
                min_canonical_denominator = min(
                    min_canonical_denominator,
                    _normalization_denominator(
                        state, chart.normalization_form, atol=atol
                    ),
                )
                max_operational_metric_form_residual = max(
                    max_operational_metric_form_residual,
                    float(np.linalg.norm(
                        chart.normalization_form - physical_metrics[key]
                    )),
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
    misaligned_metric_form_residual = 0.0
    misaligned_metric_probability = 0.0
    misaligned_metric_sum = 0.0

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
                    key = (continuation.continuation_id, clock, index)
                    chart = charts[key]
                    state = coordinate_matrices[key] @ probe.physical_coordinates
                    values = _effect_probabilities(
                        state, chart, chart.normalization_form, atol=atol
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
                    min_probe_denominator = min(
                        min_probe_denominator,
                        _normalization_denominator(
                            state, chart.normalization_form, atol=atol
                        ),
                    )

                    identity = np.eye(state.size, dtype=np.complex128)
                    identity_probabilities = _effect_probabilities(
                        state, chart, identity, atol=atol
                    )
                    wrong_identity_probability = max(
                        wrong_identity_probability,
                        _probability_residual(values, identity_probabilities),
                    )
                    wrong_identity_sum = max(
                        wrong_identity_sum, _sum_residual(identity_probabilities)
                    )

                    wrong_metric, form_residual = _most_misaligned_metric(
                        key, chart.normalization_form, physical_metrics
                    )
                    misaligned_metric_form_residual = max(
                        misaligned_metric_form_residual, form_residual
                    )
                    wrong_metric_probabilities = _effect_probabilities(
                        state, chart, wrong_metric, atol=atol
                    )
                    misaligned_metric_probability = max(
                        misaligned_metric_probability,
                        _probability_residual(values, wrong_metric_probabilities),
                    )
                    misaligned_metric_sum = max(
                        misaligned_metric_sum,
                        _sum_residual(wrong_metric_probabilities),
                    )

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
    metric_coincident = bool(max_operational_metric_form_residual <= 10 * atol)
    wrong_identity_rejected = bool(
        wrong_identity_probability > 10 * atol or wrong_identity_sum > 10 * atol
    )
    misaligned_metric_rejected = bool(
        misaligned_metric_form_residual > 10 * atol
        and (
            misaligned_metric_probability > 10 * atol
            or misaligned_metric_sum > 10 * atol
        )
    )
    probe_covariant = bool(max_probe_covariance <= 10 * atol)
    accidental_ruled_out = bool(
        len(probes) == 14 + 2 * (14 * 13 // 2)
        and probe_states_in_physical_span
        and probe_covariant
        and wrong_identity_rejected
        and misaligned_metric_rejected
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
        max_operational_physical_metric_form_residual=max_operational_metric_form_residual,
        physical_metric_operational_normalization_numerically_coincident=metric_coincident,
        wrong_identity_normalization_probability_residual=wrong_identity_probability,
        wrong_identity_normalization_sum_residual=wrong_identity_sum,
        misaligned_metric_form_residual=misaligned_metric_form_residual,
        misaligned_metric_probability_residual=misaligned_metric_probability,
        misaligned_metric_sum_residual=misaligned_metric_sum,
        wrong_identity_normalization_rejected=wrong_identity_rejected,
        misaligned_metric_rejected=misaligned_metric_rejected,
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
        "max_operational_physical_metric_form_residual": diagnostics.max_operational_physical_metric_form_residual,
        "physical_metric_operational_normalization_numerically_coincident": diagnostics.physical_metric_operational_normalization_numerically_coincident,
        "wrong_identity_normalization_probability_residual": diagnostics.wrong_identity_normalization_probability_residual,
        "wrong_identity_normalization_sum_residual": diagnostics.wrong_identity_normalization_sum_residual,
        "misaligned_metric_form_residual": diagnostics.misaligned_metric_form_residual,
        "misaligned_metric_probability_residual": diagnostics.misaligned_metric_probability_residual,
        "misaligned_metric_sum_residual": diagnostics.misaligned_metric_sum_residual,
        "swapped_outcome_numeric_residual": diagnostics.swapped_outcome_numeric_residual,
        "per_continuation_probability_covariance": diagnostics.per_continuation_probability_covariance,
        "stage9c_reference_likelihood_covariance": diagnostics.stage9c_reference_likelihood_covariance,
        "measurement_covariance_status": diagnostics.measurement_covariance_status,
        "weighted_modal_update_covariance_established": diagnostics.weighted_modal_update_covariance_established,
    }
