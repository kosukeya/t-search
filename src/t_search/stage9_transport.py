"""Stage 9D continuation-aware clock transport for directional quantum Potentiality.

Each Stage 9 continuation defines its own constrained physical basis, so every
A/B/C clock chart and cross-clock map is re-derived separately for h_L and h_R.
Directional record semantics are anchored at the declared A/e1 current event,
lifted to physical coordinates, and then represented in each local chart.

This module keeps three resources explicit and separate:

1. physical clock transport for each continuation;
2. relational-event and continuation-class correspondence;
3. semantic typing of record-target and memory observables.

A matrix that happens to transform covariantly is not thereby the right
observable for the declared continuation/event/register semantics.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from itertools import permutations, product
from typing import Literal

import numpy as np

from .stage3_asymmetry import orientation_from_scores
from .stage5_clock_change import DEFAULT_ATOL, SUBSYSTEMS
from .stage7_history import CURRENT_EVENT, LOWER_EVENT, UPPER_EVENT
from .stage7_record import canonical_target_pair_projector
from .stage7_spectator import MEMORY_DIMENSION, memory_identity, spectator_support_basis
from .stage8_continuations import QuantumContinuation
from .stage9_modal import (
    Stage9EpistemicModel,
    Stage9OnticExtensionModel,
    Stage9DirectionalCarrier,
    canonical_stage9c_models,
    continuation_by_id,
    make_stage9_epistemic_model,
    matched_uniform_weights,
)
from .stage9_substrate import (
    canonical_stage9_physical_state,
    stage9_a_transition_support_matrix,
    stage9_clock_reduction_matrix,
    stage9_clock_reduction_operator,
    stage9_continuation_equivalent,
    stage9_extension_set,
    stage9_physical_basis,
)

Stage9DModel = Stage9EpistemicModel | Stage9OnticExtensionModel
EventChiKind = Literal["preserving", "reversing", "misdeclared-preserving"]
ClassChiKind = Literal["preserving", "swapped-classes", "misdeclared-terminal-preserving"]


@dataclass(frozen=True, slots=True)
class Stage9EventCorrespondence:
    name: EventChiKind
    source_events: tuple[str, str, str]
    target_events: tuple[str, str, str]
    orientation_sign: int
    declared_orientation: str


@dataclass(frozen=True, slots=True)
class Stage9ClassCorrespondence:
    name: ClassChiKind
    source_current_event: int
    target_current_event: int
    class_map: tuple[tuple[str, str], ...]


@dataclass(frozen=True, slots=True)
class Stage9ClassCorrespondenceAudit:
    bijective: bool
    current_event_preserved: bool
    physical_classes_preserved: bool
    source_qext_size: int
    target_qext_size: int
    valid: bool


@dataclass(frozen=True, slots=True)
class Stage9TypedRecordObservable:
    continuation_id: str
    clock: str
    clock_index: int
    event_anchor: str
    relational_target: str
    register_semantics: str
    coordinate_basis: str
    matrix: np.ndarray


@dataclass(frozen=True, slots=True)
class Stage9PerspectiveRecordAssessment:
    continuation_id: str
    clock: str
    clock_index: int
    chi: str
    lower_information: float
    upper_information: float
    lower_accuracy: float
    upper_accuracy: float
    record_score: float
    accessibility_score: float
    orientation: str
    record_defined: bool
    metric_norm: float


@dataclass(frozen=True, slots=True)
class Stage9PerspectiveQRView:
    current_event: int
    clock: str
    clock_index: int
    continuation_ids: tuple[str, ...]
    continuation_weights: tuple[float, ...]
    predictive_density: tuple[complex, ...]
    directional_record_scores: tuple[float, ...]
    directional_accessibility_scores: tuple[float, ...]
    orientations: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Stage9DTransportDiagnostics:
    qext_size: int
    perspective_nodes_per_continuation: int
    total_perspective_nodes: int
    minimum_chart_rank: int
    distinct_clock_state_transports: int
    three_clock_compositions: int
    max_state_transport_residual: float
    max_inverse_residual: float
    max_metric_covariance_residual: float
    max_composition_residual: float
    max_observable_transport_residual: float
    max_metric_self_adjoint_residual: float
    max_projector_residual: float
    max_record_memory_commutator_residual: float
    max_preserving_record_score_residual: float
    max_preserving_accessibility_residual: float
    max_reversing_record_sign_residual: float
    max_reversing_accessibility_sign_residual: float
    max_weight_transport_residual: float
    matched_modal_views_all_nodes: bool
    selected_swap_modal_views_all_nodes: bool
    hidden_selected_absent_from_view_schema: bool
    correct_class_correspondence_valid: bool
    wrong_class_correspondence_rejected: bool
    terminal_current_correspondence_rejected: bool
    wrong_event_correspondence_rejected: bool
    wrong_continuation_map_residual: float
    wrong_continuation_map_rejected: bool
    max_cross_continuation_map_difference: float
    one_rederived_map_suffices_for_all_continuations: bool
    bare_observable_residual: float
    bare_observable_rejected: bool
    observable_typing_fields_present: bool
    continuation_level_transport_covariance: bool
    directional_record_covariance: bool
    class_weight_transport_covariance: bool
    full_stage9c_future_measurement_covariance_established: bool


def _validate_clock(clock: str) -> str:
    if clock not in SUBSYSTEMS:
        raise ValueError("clock must be one of A, B, or C")
    return clock


def _validate_index(index: int) -> int:
    if isinstance(index, bool) or not isinstance(index, int) or index not in (0, 1, 2):
        raise ValueError("clock index must be 0, 1, or 2")
    return index


def stage9_clock_support_qr(
    continuation: QuantumContinuation, clock: str, index: int
) -> tuple[np.ndarray, np.ndarray]:
    _validate_clock(clock)
    _validate_index(index)
    reduction = stage9_clock_reduction_matrix(continuation, clock, index)
    q, r = np.linalg.qr(reduction, mode="reduced")
    if reduction.shape != (18, 14) or np.linalg.matrix_rank(r, tol=DEFAULT_ATOL) != 14:
        raise ValueError("Stage 9D clock reading is not an injective perspective")
    return q, r


def stage9_clock_support_basis(
    continuation: QuantumContinuation, clock: str, index: int
) -> np.ndarray:
    return stage9_clock_support_qr(continuation, clock, index)[0]


def stage9_clock_coordinates(
    continuation: QuantumContinuation, clock: str, index: int
) -> np.ndarray:
    return stage9_clock_support_qr(continuation, clock, index)[1]


def stage9_support_metric(
    continuation: QuantumContinuation, clock: str, index: int
) -> np.ndarray:
    coordinates = stage9_clock_coordinates(continuation, clock, index)
    inverse = np.linalg.inv(coordinates)
    return inverse.conj().T @ inverse


def stage9_clock_change_support_matrix(
    continuation: QuantumContinuation,
    target_clock: str,
    target_index: int,
    source_clock: str,
    source_index: int,
) -> np.ndarray:
    _validate_clock(source_clock)
    _validate_clock(target_clock)
    _validate_index(source_index)
    _validate_index(target_index)
    if source_clock == target_clock:
        raise ValueError("Stage 9D genuine clock change requires distinct clocks")
    source = stage9_clock_coordinates(continuation, source_clock, source_index)
    target = stage9_clock_coordinates(continuation, target_clock, target_index)
    return target @ np.linalg.inv(source)


def stage9_reduced_support_coordinates(
    continuation: QuantumContinuation, clock: str, index: int
) -> np.ndarray:
    physical = canonical_stage9_physical_state(continuation)
    support = stage9_clock_support_basis(continuation, clock, index)
    reduced = stage9_clock_reduction_operator(clock, index) @ physical
    return support.conj().T @ reduced


def stage9_reduced_ambient_state(
    continuation: QuantumContinuation, clock: str, index: int
) -> np.ndarray:
    return stage9_clock_reduction_operator(clock, index) @ canonical_stage9_physical_state(
        continuation
    )


def _normalized_density(state: np.ndarray) -> np.ndarray:
    vector = np.asarray(state, dtype=np.complex128)
    norm = float(np.linalg.norm(vector))
    if norm <= DEFAULT_ATOL:
        raise ValueError("Stage 9D reduced state has zero norm")
    vector = vector / norm
    return np.outer(vector, vector.conj())


def event_correspondence(kind: EventChiKind = "preserving") -> Stage9EventCorrespondence:
    if kind == "preserving":
        return Stage9EventCorrespondence(
            kind, ("e0", "e1", "e2"), ("e0", "e1", "e2"), 1, "preserving"
        )
    if kind == "reversing":
        return Stage9EventCorrespondence(
            kind, ("e0", "e1", "e2"), ("e2", "e1", "e0"), -1, "reversing"
        )
    if kind == "misdeclared-preserving":
        return Stage9EventCorrespondence(
            kind, ("e0", "e1", "e2"), ("e2", "e1", "e0"), 1, "preserving"
        )
    raise ValueError("unknown Stage 9D event correspondence")


def class_correspondence(
    carrier: Stage9DirectionalCarrier,
    kind: ClassChiKind = "preserving",
) -> Stage9ClassCorrespondence:
    ids = tuple(item.continuation_id for item in carrier.continuations)
    if kind == "preserving":
        mapping = tuple((item, item) for item in ids)
        return Stage9ClassCorrespondence(kind, carrier.current_anchor, carrier.current_anchor, mapping)
    if kind == "swapped-classes":
        if len(ids) != 2:
            raise ValueError("swapped-class control requires exactly two continuations")
        return Stage9ClassCorrespondence(
            kind,
            carrier.current_anchor,
            carrier.current_anchor,
            ((ids[0], ids[1]), (ids[1], ids[0])),
        )
    if kind == "misdeclared-terminal-preserving":
        return Stage9ClassCorrespondence(
            kind,
            carrier.current_anchor,
            UPPER_EVENT,
            tuple((item, item) for item in ids),
        )
    raise ValueError("unknown Stage 9D class correspondence")


def audit_class_correspondence(
    carrier: Stage9DirectionalCarrier,
    correspondence: Stage9ClassCorrespondence,
    *,
    atol: float = DEFAULT_ATOL,
) -> Stage9ClassCorrespondenceAudit:
    source_ids = tuple(item.continuation_id for item in carrier.continuations)
    mapped_sources = tuple(pair[0] for pair in correspondence.class_map)
    mapped_targets = tuple(pair[1] for pair in correspondence.class_map)
    bijective = bool(
        len(mapped_sources) == len(source_ids)
        and set(mapped_sources) == set(source_ids)
        and len(set(mapped_targets)) == len(mapped_targets)
    )
    try:
        target_qext = stage9_extension_set(correspondence.target_current_event)
    except ValueError:
        target_qext = ()
    target_ids = tuple(item.continuation_id for item in target_qext)
    current_preserved = correspondence.target_current_event == carrier.current_anchor
    classes_preserved = False
    if bijective and current_preserved and set(mapped_targets) == set(target_ids):
        classes_preserved = all(
            stage9_continuation_equivalent(
                continuation_by_id(carrier, source_id),
                next(item for item in target_qext if item.continuation_id == target_id),
                atol=atol,
            )
            for source_id, target_id in correspondence.class_map
        )
    return Stage9ClassCorrespondenceAudit(
        bijective,
        current_preserved,
        classes_preserved,
        len(source_ids),
        len(target_qext),
        bool(bijective and current_preserved and classes_preserved),
    )


def _fixed_a_coordinates(continuation: QuantumContinuation) -> np.ndarray:
    support = spectator_support_basis("A")
    coordinates = support.conj().T @ stage9_clock_reduction_matrix(
        continuation, "A", CURRENT_EVENT
    )
    if coordinates.shape != (14, 14) or np.linalg.matrix_rank(
        coordinates, tol=DEFAULT_ATOL
    ) != 14:
        raise ValueError("Stage 9D A/e1 semantic coordinates are not invertible")
    return coordinates


def _target_support_projector() -> np.ndarray:
    return np.kron(canonical_target_pair_projector(), memory_identity())


def _memory_support_projector(bit: int) -> np.ndarray:
    if bit not in (0, 1):
        raise ValueError("memory bit must be 0 or 1")
    pair_dimension = canonical_target_pair_projector().shape[0]
    memory = np.zeros((MEMORY_DIMENSION, MEMORY_DIMENSION), dtype=np.complex128)
    memory[bit, bit] = 1.0
    return np.kron(np.eye(pair_dimension, dtype=np.complex128), memory)


def physical_event_target_operator(
    continuation: QuantumContinuation, event_index: int
) -> np.ndarray:
    if event_index not in (LOWER_EVENT, UPPER_EVENT):
        raise ValueError("record target event must be e0 or e2")
    target = _target_support_projector()
    transition = stage9_a_transition_support_matrix(
        continuation, CURRENT_EVENT, event_index
    )
    fixed = transition @ target @ transition.conj().T
    coordinates = _fixed_a_coordinates(continuation)
    return np.linalg.inv(coordinates) @ fixed @ coordinates


def physical_memory_projector(
    continuation: QuantumContinuation, bit: int
) -> np.ndarray:
    coordinates = _fixed_a_coordinates(continuation)
    return np.linalg.inv(coordinates) @ _memory_support_projector(bit) @ coordinates


def represent_physical_operator(
    continuation: QuantumContinuation,
    operator: np.ndarray,
    clock: str,
    index: int,
) -> np.ndarray:
    physical = np.asarray(operator, dtype=np.complex128)
    if physical.shape != (14, 14):
        raise ValueError("Stage 9D physical-coordinate operator must have shape (14,14)")
    coordinates = stage9_clock_coordinates(continuation, clock, index)
    return coordinates @ physical @ np.linalg.inv(coordinates)


def typed_event_target_observable(
    continuation: QuantumContinuation,
    clock: str,
    index: int,
    event_index: int,
) -> Stage9TypedRecordObservable:
    label = "e0" if event_index == LOWER_EVENT else "e2"
    matrix = represent_physical_operator(
        continuation,
        physical_event_target_operator(continuation, event_index),
        clock,
        index,
    )
    return Stage9TypedRecordObservable(
        continuation.continuation_id,
        clock,
        index,
        "e1",
        label,
        "record-target projector",
        "continuation-specific QR support coordinates",
        matrix,
    )


def typed_memory_observable(
    continuation: QuantumContinuation, clock: str, index: int, bit: int
) -> Stage9TypedRecordObservable:
    matrix = represent_physical_operator(
        continuation, physical_memory_projector(continuation, bit), clock, index
    )
    return Stage9TypedRecordObservable(
        continuation.continuation_id,
        clock,
        index,
        "e1",
        "memory",
        f"memory bit {bit}",
        "continuation-specific QR support coordinates",
        matrix,
    )


def metric_self_adjoint_residual(operator: np.ndarray, metric: np.ndarray) -> float:
    return float(np.linalg.norm(metric @ operator - operator.conj().T @ metric))


def _metric_joint_distribution(
    state_coordinates: np.ndarray,
    metric: np.ndarray,
    target_projector: np.ndarray,
    memory_projectors: tuple[np.ndarray, np.ndarray],
) -> tuple[np.ndarray, float, float, float]:
    identity = np.eye(target_projector.shape[0], dtype=np.complex128)
    denominator = np.vdot(state_coordinates, metric @ state_coordinates)
    if abs(denominator.imag) > 1e-9 or denominator.real <= DEFAULT_ATOL:
        raise RuntimeError("invalid Stage 9D induced-metric norm")
    joint = np.zeros((2, 2), dtype=float)
    max_self_adjoint = metric_self_adjoint_residual(target_projector, metric)
    max_projector = float(np.linalg.norm(target_projector @ target_projector - target_projector))
    max_commutator = 0.0
    for target_bit, target in (
        (1, target_projector),
        (0, identity - target_projector),
    ):
        for memory_bit, memory in enumerate(memory_projectors):
            max_self_adjoint = max(
                max_self_adjoint, metric_self_adjoint_residual(memory, metric)
            )
            max_projector = max(
                max_projector, float(np.linalg.norm(memory @ memory - memory))
            )
            max_commutator = max(
                max_commutator, float(np.linalg.norm(target @ memory - memory @ target))
            )
            value = np.vdot(
                state_coordinates, metric @ target @ memory @ state_coordinates
            ) / denominator
            if abs(value.imag) > 1e-9:
                raise RuntimeError("record probability acquired an imaginary part")
            joint[target_bit, memory_bit] = float(value.real)
    joint[np.abs(joint) <= DEFAULT_ATOL] = 0.0
    if np.min(joint) < -DEFAULT_ATOL:
        raise RuntimeError("record joint distribution acquired negative probability")
    joint = np.clip(joint, 0.0, None)
    joint = joint / np.sum(joint)
    return joint, max_self_adjoint, max_projector, max_commutator


def _mutual_information(joint: np.ndarray) -> float:
    probabilities = np.asarray(joint, dtype=float)
    px = np.sum(probabilities, axis=1, keepdims=True)
    pm = np.sum(probabilities, axis=0, keepdims=True)
    independent = px @ pm
    mask = probabilities > DEFAULT_ATOL
    if not np.any(mask):
        return 0.0
    return float(
        np.sum(probabilities[mask] * np.log2(probabilities[mask] / independent[mask]))
    )


def _decoder_accuracy(joint: np.ndarray) -> float:
    return float(sum(np.max(joint[:, memory_bit]) for memory_bit in (0, 1)))


def perspective_record_joint_distribution(
    continuation: QuantumContinuation,
    clock: str,
    index: int,
    event_index: int,
) -> tuple[np.ndarray, float, float, float]:
    state_coordinates = stage9_reduced_support_coordinates(continuation, clock, index)
    metric = stage9_support_metric(continuation, clock, index)
    target = typed_event_target_observable(
        continuation, clock, index, event_index
    ).matrix
    memory = tuple(
        typed_memory_observable(continuation, clock, index, bit).matrix
        for bit in (0, 1)
    )
    return _metric_joint_distribution(
        state_coordinates, metric, target, memory  # type: ignore[arg-type]
    )


def perspective_record_assessment(
    continuation: QuantumContinuation,
    clock: str,
    index: int,
    *,
    chi: EventChiKind = "preserving",
    tolerance: float = 1e-10,
) -> Stage9PerspectiveRecordAssessment:
    correspondence = event_correspondence(chi)
    lower_event = LOWER_EVENT if correspondence.target_events[0] == "e0" else UPPER_EVENT
    upper_event = UPPER_EVENT if correspondence.target_events[2] == "e2" else LOWER_EVENT
    lower_joint, _, _, _ = perspective_record_joint_distribution(
        continuation, clock, index, lower_event
    )
    upper_joint, _, _, _ = perspective_record_joint_distribution(
        continuation, clock, index, upper_event
    )
    lower_information = _mutual_information(lower_joint)
    upper_information = _mutual_information(upper_joint)
    lower_accuracy = _decoder_accuracy(lower_joint)
    upper_accuracy = _decoder_accuracy(upper_joint)
    record_score = lower_information - upper_information
    accessibility_score = lower_accuracy - upper_accuracy
    orientation = orientation_from_scores(
        record_score, accessibility_score, tolerance=tolerance
    )
    state_coordinates = stage9_reduced_support_coordinates(continuation, clock, index)
    metric = stage9_support_metric(continuation, clock, index)
    metric_norm = float(np.vdot(state_coordinates, metric @ state_coordinates).real)
    selected_information = (
        lower_information
        if orientation == "lower-index"
        else upper_information if orientation == "upper-index" else 0.0
    )
    return Stage9PerspectiveRecordAssessment(
        continuation.continuation_id,
        clock,
        index,
        correspondence.name,
        lower_information,
        upper_information,
        lower_accuracy,
        upper_accuracy,
        record_score,
        accessibility_score,
        orientation,
        bool(orientation != "none" and selected_information > tolerance),
        metric_norm,
    )


def _model_weights(model: Stage9DModel) -> tuple[float, ...]:
    if isinstance(model, Stage9EpistemicModel):
        return model.belief_weights
    if isinstance(model, Stage9OnticExtensionModel):
        return model.extension_weights
    raise TypeError("unsupported Stage 9D model")


def perspective_qr_view(
    model: Stage9DModel,
    clock: str,
    index: int,
    *,
    correspondence: Stage9ClassCorrespondence | None = None,
    atol: float = DEFAULT_ATOL,
) -> Stage9PerspectiveQRView:
    chi = correspondence or class_correspondence(model.carrier, "preserving")
    audit = audit_class_correspondence(model.carrier, chi, atol=atol)
    if not audit.valid:
        raise ValueError("class correspondence does not preserve Stage 9 QExt classes")
    weights = _model_weights(model)
    density = np.zeros((18, 18), dtype=np.complex128)
    scores: list[float] = []
    access: list[float] = []
    orientations: list[str] = []
    for weight, continuation in zip(weights, model.carrier.continuations, strict=True):
        density += float(weight) * _normalized_density(
            stage9_reduced_ambient_state(continuation, clock, index)
        )
        assessment = perspective_record_assessment(
            continuation, clock, index, chi="preserving"
        )
        scores.append(assessment.record_score)
        access.append(assessment.accessibility_score)
        orientations.append(assessment.orientation)
    density = density / np.trace(density)
    return Stage9PerspectiveQRView(
        chi.target_current_event,
        clock,
        index,
        tuple(target for _, target in chi.class_map),
        tuple(float(value) for value in weights),
        tuple(complex(value) for value in density.reshape(-1)),
        tuple(scores),
        tuple(access),
        tuple(orientations),
    )


def _views_close(
    left: Stage9PerspectiveQRView,
    right: Stage9PerspectiveQRView,
    *,
    atol: float = DEFAULT_ATOL,
) -> bool:
    if (
        left.current_event != right.current_event
        or left.clock != right.clock
        or left.clock_index != right.clock_index
        or left.continuation_ids != right.continuation_ids
        or left.orientations != right.orientations
    ):
        return False
    return bool(
        np.allclose(left.continuation_weights, right.continuation_weights, atol=atol, rtol=0.0)
        and np.allclose(left.predictive_density, right.predictive_density, atol=atol, rtol=0.0)
        and np.allclose(left.directional_record_scores, right.directional_record_scores, atol=atol, rtol=0.0)
        and np.allclose(left.directional_accessibility_scores, right.directional_accessibility_scores, atol=atol, rtol=0.0)
    )


def _wrong_continuation_map_residual(*, atol: float = DEFAULT_ATOL) -> float:
    left, right = stage9_extension_set(CURRENT_EVENT)
    residuals: list[float] = []
    for target_clock in ("B", "C"):
        for source_index, target_index in product(range(3), repeat=2):
            wrong_map = stage9_clock_change_support_matrix(
                left, target_clock, target_index, "A", source_index
            )
            source = stage9_reduced_support_coordinates(right, "A", source_index)
            target = stage9_reduced_support_coordinates(right, target_clock, target_index)
            residuals.append(float(np.linalg.norm(wrong_map @ source - target)))
    value = max(residuals)
    return 0.0 if value <= atol else value


def stage9d_transport_diagnostics(
    *, atol: float = DEFAULT_ATOL
) -> Stage9DTransportDiagnostics:
    epistemic, ontic = canonical_stage9c_models(selected_id="h_L")
    carrier = epistemic.carrier
    continuations = carrier.continuations

    minimum_rank = 14
    max_state = 0.0
    max_inverse = 0.0
    max_metric = 0.0
    max_observable = 0.0
    state_comparisons = 0
    map_differences: list[float] = []

    for continuation in continuations:
        for clock in SUBSYSTEMS:
            for index in range(3):
                minimum_rank = min(
                    minimum_rank,
                    int(
                        np.linalg.matrix_rank(
                            stage9_clock_reduction_matrix(continuation, clock, index),
                            tol=atol,
                        )
                    ),
                )
        physical_operators = (
            physical_event_target_operator(continuation, LOWER_EVENT),
            physical_event_target_operator(continuation, UPPER_EVENT),
            physical_memory_projector(continuation, 0),
            physical_memory_projector(continuation, 1),
        )
        for source_clock, target_clock in permutations(SUBSYSTEMS, 2):
            for source_index, target_index in product(range(3), repeat=2):
                transform = stage9_clock_change_support_matrix(
                    continuation,
                    target_clock,
                    target_index,
                    source_clock,
                    source_index,
                )
                reverse = stage9_clock_change_support_matrix(
                    continuation,
                    source_clock,
                    source_index,
                    target_clock,
                    target_index,
                )
                source_state = stage9_reduced_support_coordinates(
                    continuation, source_clock, source_index
                )
                target_state = stage9_reduced_support_coordinates(
                    continuation, target_clock, target_index
                )
                source_metric = stage9_support_metric(
                    continuation, source_clock, source_index
                )
                target_metric = stage9_support_metric(
                    continuation, target_clock, target_index
                )
                max_state = max(
                    max_state, float(np.linalg.norm(transform @ source_state - target_state))
                )
                max_inverse = max(
                    max_inverse,
                    float(np.linalg.norm(reverse @ transform - np.eye(14))),
                )
                max_metric = max(
                    max_metric,
                    float(
                        np.linalg.norm(
                            transform.conj().T @ target_metric @ transform - source_metric
                        )
                    ),
                )
                inverse_transform = np.linalg.inv(transform)
                for physical_operator in physical_operators:
                    source_operator = represent_physical_operator(
                        continuation, physical_operator, source_clock, source_index
                    )
                    target_operator = represent_physical_operator(
                        continuation, physical_operator, target_clock, target_index
                    )
                    max_observable = max(
                        max_observable,
                        float(
                            np.linalg.norm(
                                transform @ source_operator @ inverse_transform - target_operator
                            )
                        ),
                    )
                state_comparisons += 1

    left, right = continuations
    for source_clock, target_clock in permutations(SUBSYSTEMS, 2):
        for source_index, target_index in product(range(3), repeat=2):
            left_map = stage9_clock_change_support_matrix(
                left, target_clock, target_index, source_clock, source_index
            )
            right_map = stage9_clock_change_support_matrix(
                right, target_clock, target_index, source_clock, source_index
            )
            map_differences.append(float(np.linalg.norm(left_map - right_map)))

    max_composition = 0.0
    composition_count = 0
    for continuation in continuations:
        for source_clock, middle_clock, target_clock in permutations(SUBSYSTEMS, 3):
            for source_index, middle_index, target_index in product(range(3), repeat=3):
                first = stage9_clock_change_support_matrix(
                    continuation,
                    middle_clock,
                    middle_index,
                    source_clock,
                    source_index,
                )
                second = stage9_clock_change_support_matrix(
                    continuation,
                    target_clock,
                    target_index,
                    middle_clock,
                    middle_index,
                )
                direct = stage9_clock_change_support_matrix(
                    continuation,
                    target_clock,
                    target_index,
                    source_clock,
                    source_index,
                )
                max_composition = max(
                    max_composition, float(np.linalg.norm(second @ first - direct))
                )
                composition_count += 1

    max_preserving_record = 0.0
    max_preserving_access = 0.0
    max_reversing_record = 0.0
    max_reversing_access = 0.0
    max_self_adjoint = 0.0
    max_projector = 0.0
    max_commutator = 0.0
    wrong_event_residual = 0.0
    for continuation in continuations:
        reference = perspective_record_assessment(
            continuation, "A", CURRENT_EVENT, chi="preserving"
        )
        for clock in SUBSYSTEMS:
            for index in range(3):
                preserving = perspective_record_assessment(
                    continuation, clock, index, chi="preserving"
                )
                reversing = perspective_record_assessment(
                    continuation, clock, index, chi="reversing"
                )
                wrong = perspective_record_assessment(
                    continuation, clock, index, chi="misdeclared-preserving"
                )
                max_preserving_record = max(
                    max_preserving_record,
                    abs(preserving.record_score - reference.record_score),
                )
                max_preserving_access = max(
                    max_preserving_access,
                    abs(preserving.accessibility_score - reference.accessibility_score),
                )
                max_reversing_record = max(
                    max_reversing_record,
                    abs(reversing.record_score + reference.record_score),
                )
                max_reversing_access = max(
                    max_reversing_access,
                    abs(reversing.accessibility_score + reference.accessibility_score),
                )
                wrong_event_residual = max(
                    wrong_event_residual,
                    abs(wrong.record_score - reference.record_score),
                    abs(wrong.accessibility_score - reference.accessibility_score),
                )
                for event in (LOWER_EVENT, UPPER_EVENT):
                    _, self_adj, projector, commutator = perspective_record_joint_distribution(
                        continuation, clock, index, event
                    )
                    max_self_adjoint = max(max_self_adjoint, self_adj)
                    max_projector = max(max_projector, projector)
                    max_commutator = max(max_commutator, commutator)

    preserving_class = class_correspondence(carrier, "preserving")
    preserving_audit = audit_class_correspondence(carrier, preserving_class, atol=atol)
    wrong_class = audit_class_correspondence(
        carrier, class_correspondence(carrier, "swapped-classes"), atol=atol
    )
    terminal = audit_class_correspondence(
        carrier,
        class_correspondence(carrier, "misdeclared-terminal-preserving"),
        atol=atol,
    )

    weights = matched_uniform_weights(carrier)
    swapped_epistemic = make_stage9_epistemic_model(
        carrier, continuation_by_id(carrier, "h_R"), weights, atol=atol
    )
    matched_all = True
    selected_swap_all = True
    max_weight_residual = 0.0
    for clock in SUBSYSTEMS:
        for index in range(3):
            e_view = perspective_qr_view(
                epistemic, clock, index, correspondence=preserving_class, atol=atol
            )
            o_view = perspective_qr_view(
                ontic, clock, index, correspondence=preserving_class, atol=atol
            )
            s_view = perspective_qr_view(
                swapped_epistemic, clock, index, correspondence=preserving_class, atol=atol
            )
            matched_all = matched_all and _views_close(e_view, o_view, atol=atol)
            selected_swap_all = selected_swap_all and _views_close(e_view, s_view, atol=atol)
            max_weight_residual = max(
                max_weight_residual,
                max(
                    abs(a - b)
                    for a, b in zip(
                        e_view.continuation_weights,
                        o_view.continuation_weights,
                        strict=True,
                    )
                ),
            )

    schema = {field.name for field in fields(Stage9PerspectiveQRView)}
    hidden_absent = all(
        forbidden not in schema
        for forbidden in (
            "selected_continuation",
            "selected_history",
            "selector",
            "model_type",
        )
    )

    wrong_map = _wrong_continuation_map_residual(atol=atol)
    max_map_difference = max(map_differences)
    one_map = max_map_difference <= atol

    bare_residual = 0.0
    for continuation in continuations:
        physical_lower = physical_event_target_operator(continuation, LOWER_EVENT)
        for source_clock, target_clock in permutations(SUBSYSTEMS, 2):
            for source_index, target_index in product(range(3), repeat=2):
                source_operator = represent_physical_operator(
                    continuation, physical_lower, source_clock, source_index
                )
                target_operator = represent_physical_operator(
                    continuation, physical_lower, target_clock, target_index
                )
                bare_residual = max(
                    bare_residual, float(np.linalg.norm(source_operator - target_operator))
                )

    typed_fields = {field.name for field in fields(Stage9TypedRecordObservable)}
    typing_present = all(
        name in typed_fields
        for name in (
            "continuation_id",
            "clock",
            "clock_index",
            "event_anchor",
            "relational_target",
            "register_semantics",
            "coordinate_basis",
            "matrix",
        )
    )

    tolerance = 1e-9
    continuation_covariance = bool(
        minimum_rank == 14
        and state_comparisons == 108
        and composition_count == 324
        and max_state <= tolerance
        and max_inverse <= tolerance
        and max_metric <= tolerance
        and max_composition <= tolerance
        and max_observable <= tolerance
    )
    record_covariance = bool(
        max_preserving_record <= tolerance
        and max_preserving_access <= tolerance
        and max_reversing_record <= tolerance
        and max_reversing_access <= tolerance
        and max_self_adjoint <= tolerance
        and max_projector <= tolerance
        and max_commutator <= tolerance
        and wrong_event_residual > tolerance
        and typing_present
    )
    class_weight_covariance = bool(
        preserving_audit.valid
        and matched_all
        and selected_swap_all
        and max_weight_residual <= tolerance
    )

    # Stage 9D transports continuation-specific states, record observables,
    # classes, and weights.  It does not construct a single declared transport
    # for the cross-continuation Stage 9C future-signature measurement family.
    full_future_measurement_covariance = False

    return Stage9DTransportDiagnostics(
        len(continuations),
        9,
        9 * len(continuations),
        minimum_rank,
        state_comparisons,
        composition_count,
        max_state,
        max_inverse,
        max_metric,
        max_composition,
        max_observable,
        max_self_adjoint,
        max_projector,
        max_commutator,
        max_preserving_record,
        max_preserving_access,
        max_reversing_record,
        max_reversing_access,
        max_weight_residual,
        matched_all,
        selected_swap_all,
        hidden_absent,
        preserving_audit.valid,
        not wrong_class.valid,
        not terminal.valid,
        wrong_event_residual > tolerance,
        wrong_map,
        wrong_map > tolerance,
        max_map_difference,
        one_map,
        bare_residual,
        bare_residual > tolerance,
        typing_present,
        continuation_covariance,
        record_covariance,
        class_weight_covariance,
        full_future_measurement_covariance,
    )


def stage9d_summary() -> dict[str, object]:
    diagnostics = stage9d_transport_diagnostics()
    return {
        "stage": "9D",
        "transport": "continuation-aware directional P-R-V atlas",
        "diagnostics": asdict(diagnostics),
        "criteria": {
            "31": "18 continuation-specific A/B/C charts are re-derived and remain rank 14",
            "32": "108 genuine distinct-clock state/inverse/metric transports and 324 three-clock compositions are covariant",
            "33": "typed directional record observables preserve record/accessibility scores and transform with explicit event correspondence",
            "34": "continuation classes, weights, matched modal views, and hidden-selector swap invariance survive all local charts",
            "35": "wrong class/event/continuation-map and bare-observable controls are rejected",
            "36": "Stage 9C future-signature measurement-family covariance remains separately not established rather than inferred from state/record/class transport",
        },
        "guards": [
            "equal numeric clock readings != event identity",
            "covariance of a wrongly typed observable != semantic correctness",
            "continuation-aware transport != one universal h-independent map",
            "branch-specific perspective map != hidden branch selection",
            "directional record covariance != P=R",
            "P-R_direction-V covariance != ontic openness",
            "class/weight covariance != V_semantics identity",
            "full Stage 9C future-measurement covariance remains not_established",
            "finite clock covariance != general covariance",
        ],
        "next": "Stage 9E — P/O/R_direction/V compatibility matrix",
    }
