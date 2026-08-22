"""Stage 9F ablation / reconstruction / accessibility matrix.

Stage 9F pressure-tests the positive P/O/R_direction/V compatibility established
in Stage 9E.  Ingredients are neutralized one at a time while the retained
constrained structure is re-derived rather than assumed.

The status vocabulary is functional, not metaphysical:

- preserved: the role remains directly represented;
- reconstructible: an explicit ingredient is removed but rebuilt from retained
  declared structure by an executable witness;
- inaccessible: the global role remains represented while the declared local
  interface does not expose it;
- lost: the represented role is deliberately removed;
- underdetermined: the retained structure admits multiple incompatible values
  or semantic completions;
- not_established: retained typing is insufficient to license the role.

These statuses do not imply metaphysical fundamentality or irreducibility.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from enum import Enum
from functools import lru_cache
from itertools import permutations, product
from typing import Any, Callable

import numpy as np

from .stage5_clock_change import DEFAULT_ATOL, SUBSYSTEMS
from .stage7_history import (
    CURRENT_EVENT,
    LOWER_EVENT,
    UPPER_EVENT,
    clock_reading_projector,
)
from .stage7_record import (
    TARGET_LABEL,
    TARGET_POSITION,
    controlled_record_write_ambient_operator,
    target_memory_joint_distribution,
)
from .stage7_spectator import (
    spectator_physical_basis,
    spectator_support_basis,
    spectator_total_constraint_operator,
)
from .stage8_continuations import (
    QuantumContinuation,
    canonical_continuation_left,
    canonical_continuation_right,
)
from .stage9_controls import (
    assess_stage9b_control_admissibility,
    assess_stage9b_control_direction,
    canonical_stage9b_control_physical_state,
    reduced_stage9b_control_state,
    stage9b_control_clock_reduction_matrix,
    stage9b_control_retains_nontrivial_v,
)
from .stage9_modal import (
    Stage9DirectionalCarrier,
    make_stage9_epistemic_model,
    make_stage9_ontic_model,
    privileged_stage9_modal_diagnostic,
    stage9c_modal_diagnostics,
)
from .stage9_substrate import (
    _decoder_accuracy,
    _joint_from_current_coordinates,
    _mutual_information,
    _target_support_projector,
    assess_stage9_direction,
    canonical_stage9_physical_state,
    reduced_stage9_state,
    stage9_branch_action_operator,
    stage9_clock_reduction_matrix,
    stage9_clock_reduction_operator,
    stage9_extension_set,
)
from .stage9_transport import (
    stage9_clock_change_support_matrix,
    stage9d_transport_diagnostics,
)


ROLE_IDS: tuple[str, ...] = (
    "R_content",
    "R_direction",
    "R_access",
    "V_extension_multiplicity",
    "V_selected_vs_unselected_semantics",
    "V_weights",
    "P_perspective_transport",
    "event_class_correspondence",
    "P_RV_typed_identification",
    "O_V_extension_relation",
)

ABLATION_IDS: tuple[str, ...] = (
    "record_write_neutralized",
    "scrambler_neutralized",
    "qext_collapsed_singleton",
    "modal_semantics_removed",
    "weights_unfixed",
    "local_record_access_hidden",
    "explicit_perspective_edges_removed",
    "event_class_correspondence_removed",
)


class RoleStatus(str, Enum):
    PRESERVED = "preserved"
    RECONSTRUCTIBLE = "reconstructible"
    INACCESSIBLE = "inaccessible"
    LOST = "lost"
    UNDERDETERMINED = "underdetermined"
    NOT_ESTABLISHED = "not_established"


@dataclass(frozen=True, slots=True)
class RoleEvidence:
    role: str
    direct_available: bool = False
    reconstruction_available: bool = False
    globally_represented: bool | None = None
    locally_accessible: bool | None = None
    decisive_loss: bool = False
    underdetermined: bool = False
    measurements: tuple[tuple[str, Any], ...] = ()
    note: str = ""

    @property
    def status(self) -> RoleStatus:
        if self.direct_available:
            return RoleStatus.PRESERVED
        if self.reconstruction_available:
            return RoleStatus.RECONSTRUCTIBLE
        if self.globally_represented is True and self.locally_accessible is False:
            return RoleStatus.INACCESSIBLE
        if self.decisive_loss:
            return RoleStatus.LOST
        if self.underdetermined:
            return RoleStatus.UNDERDETERMINED
        return RoleStatus.NOT_ESTABLISHED

    def as_dict(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "status": self.status.value,
            "direct_available": self.direct_available,
            "reconstruction_available": self.reconstruction_available,
            "globally_represented": self.globally_represented,
            "locally_accessible": self.locally_accessible,
            "decisive_loss": self.decisive_loss,
            "underdetermined": self.underdetermined,
            "measurements": dict(self.measurements),
            "note": self.note,
        }


@dataclass(frozen=True, slots=True)
class AblationCase:
    ingredient: str
    neutralization: str
    probes: tuple[RoleEvidence, ...]

    def __post_init__(self) -> None:
        if self.ingredient not in ABLATION_IDS:
            raise ValueError(f"unknown Stage 9F ablation: {self.ingredient!r}")
        if tuple(probe.role for probe in self.probes) != ROLE_IDS:
            raise ValueError("Stage 9F probes must follow the frozen role order")

    def status(self, role: str) -> RoleStatus:
        return next(probe.status for probe in self.probes if probe.role == role)

    def as_dict(self) -> dict[str, Any]:
        return {
            "ingredient": self.ingredient,
            "neutralization": self.neutralization,
            "probes": [probe.as_dict() for probe in self.probes],
        }


@dataclass(frozen=True, slots=True)
class TransportReconstructionDiagnostics:
    continuation_count: int
    comparisons: int
    minimum_chart_rank: int
    max_state_transport_residual: float
    max_inverse_residual: float
    max_metric_covariance_residual: float
    max_reference_map_residual: float | None
    valid: bool
    reconstructible_from_node_coordinates: bool


@dataclass(frozen=True, slots=True)
class DirectionalMechanismDiagnostics:
    record_write_current_information: tuple[tuple[str, float], ...]
    record_write_record_scores: tuple[tuple[str, float], ...]
    record_write_accessibility_scores: tuple[tuple[str, float], ...]
    record_write_v_nontrivial: bool
    record_write_valid_constrained_carriers: bool
    record_write_transport: TransportReconstructionDiagnostics
    no_scramble_current_information: tuple[tuple[str, float], ...]
    no_scramble_record_scores: tuple[tuple[str, float], ...]
    no_scramble_accessibility_scores: tuple[tuple[str, float], ...]
    no_scramble_v_nontrivial: bool
    no_scramble_valid_constrained_carriers: bool
    no_scramble_transport: TransportReconstructionDiagnostics
    no_scramble_direction_lost_while_current_record_retained: bool


@dataclass(frozen=True, slots=True)
class SingletonDiagnostics:
    qext_size: int
    current_record_information: float
    record_score: float
    accessibility_score: float
    record_defined: bool
    semantic_types_distinct: bool
    ontic_has_no_selected_continuation_field: bool
    singleton_weight: float
    singleton_weight_reconstructible_from_normalization: bool
    future_extension_present: bool
    transport: TransportReconstructionDiagnostics


@dataclass(frozen=True, slots=True)
class SemanticWeightDiagnostics:
    matched_public_views_equal: bool
    privileged_modal_structures_distinct: bool
    modal_semantics_reconstructible_from_public_carrier: bool
    uniform_weights: tuple[float, ...]
    alternative_weights: tuple[float, ...]
    prediction_changes_with_weights: bool
    weight_change_preserves_directional_data: bool
    weights_reconstructible_from_carrier: bool


@dataclass(frozen=True, slots=True)
class HiddenAccessView:
    current_anchor: int
    continuation_ids: tuple[str, ...]
    continuation_weights: tuple[float, ...]
    current_record_information: float
    record_score: float
    orientation: str


@dataclass(frozen=True, slots=True)
class AccessibilityDiagnostics:
    global_record_information: float
    global_record_score: float
    global_accessibility_score: float
    global_orientation: str
    hidden_view_field_names: tuple[str, ...]
    local_accessibility_field_exposed: bool
    v_extension_count_retained: int
    weights_retained: tuple[float, ...]
    global_direction_preserved: bool
    local_access_inaccessible: bool


@dataclass(frozen=True, slots=True)
class CorrespondenceDiagnostics:
    local_p_atlas_retained: bool
    local_p_comparisons: int
    event_class_correspondence_declared: bool
    typed_cross_perspective_rv_identification_established: bool
    wrong_class_control_rejected: bool
    wrong_event_control_rejected: bool


@dataclass(frozen=True, slots=True)
class MismatchDiagnostic:
    mismatch: str
    affected_role: str
    detected: bool
    measurements: tuple[tuple[str, Any], ...]
    note: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "mismatch": self.mismatch,
            "affected_role": self.affected_role,
            "detected": self.detected,
            "measurements": dict(self.measurements),
            "note": self.note,
        }


@dataclass(frozen=True, slots=True)
class Stage9FDiagnostics:
    directional_mechanism: DirectionalMechanismDiagnostics
    singleton_qext: SingletonDiagnostics
    semantic_weights: SemanticWeightDiagnostics
    accessibility: AccessibilityDiagnostics
    edge_reconstruction: TransportReconstructionDiagnostics
    correspondence: CorrespondenceDiagnostics
    wrong_observable: MismatchDiagnostic


def _preserved(
    role: str,
    measurements: tuple[tuple[str, Any], ...] = (),
    note: str = "",
) -> RoleEvidence:
    return RoleEvidence(
        role=role,
        direct_available=True,
        globally_represented=True,
        locally_accessible=True if role == "R_access" else None,
        measurements=measurements,
        note=note or "role remains directly represented after neutralization",
    )


def _reconstructible(
    role: str,
    measurements: tuple[tuple[str, Any], ...],
    note: str,
) -> RoleEvidence:
    return RoleEvidence(
        role=role,
        reconstruction_available=True,
        globally_represented=True,
        measurements=measurements,
        note=note,
    )


def _inaccessible(
    role: str,
    measurements: tuple[tuple[str, Any], ...],
    note: str,
) -> RoleEvidence:
    return RoleEvidence(
        role=role,
        globally_represented=True,
        locally_accessible=False,
        measurements=measurements,
        note=note,
    )


def _lost(
    role: str,
    measurements: tuple[tuple[str, Any], ...],
    note: str,
) -> RoleEvidence:
    return RoleEvidence(
        role=role,
        globally_represented=False,
        decisive_loss=True,
        measurements=measurements,
        note=note,
    )


def _underdetermined(
    role: str,
    measurements: tuple[tuple[str, Any], ...],
    note: str,
) -> RoleEvidence:
    return RoleEvidence(
        role=role,
        globally_represented=True,
        underdetermined=True,
        measurements=measurements,
        note=note,
    )


def _not_established(
    role: str,
    measurements: tuple[tuple[str, Any], ...],
    note: str,
) -> RoleEvidence:
    return RoleEvidence(role=role, measurements=measurements, note=note)


def _normalized(vector: np.ndarray) -> np.ndarray:
    state = np.asarray(vector, dtype=np.complex128)
    norm = float(np.linalg.norm(state))
    if norm <= DEFAULT_ATOL:
        raise ValueError("Stage 9F state must have nonzero norm")
    return state / norm


def _current_record_information(state: np.ndarray) -> float:
    joint = target_memory_joint_distribution(
        _normalized(state),
        position=TARGET_POSITION,
        label=TARGET_LABEL,
    )
    return _mutual_information(joint)


def _unitarity_residual(operator: np.ndarray) -> float:
    identity = np.eye(operator.shape[0], dtype=np.complex128)
    return float(np.linalg.norm(operator.conj().T @ operator - identity))


ReductionMatrixFn = Callable[[QuantumContinuation, str, int], np.ndarray]
PhysicalStateFn = Callable[[QuantumContinuation], np.ndarray]


def _qr_coordinates(
    continuation: QuantumContinuation,
    clock: str,
    index: int,
    reduction_matrix_fn: ReductionMatrixFn,
) -> tuple[np.ndarray, np.ndarray]:
    reduction = reduction_matrix_fn(continuation, clock, index)
    q, r = np.linalg.qr(reduction, mode="reduced")
    if reduction.shape != (18, 14) or np.linalg.matrix_rank(r, tol=DEFAULT_ATOL) != 14:
        raise ValueError("Stage 9F ablated clock chart is not rank 14")
    return q, r


def _transport_diagnostics(
    continuations: tuple[QuantumContinuation, ...],
    reduction_matrix_fn: ReductionMatrixFn,
    physical_state_fn: PhysicalStateFn,
    *,
    compare_to_canonical_edges: bool = False,
    atol: float = DEFAULT_ATOL,
) -> TransportReconstructionDiagnostics:
    comparisons = 0
    minimum_rank = 14
    max_state = 0.0
    max_inverse = 0.0
    max_metric = 0.0
    max_reference = 0.0

    for continuation in continuations:
        state = physical_state_fn(continuation)
        node_data: dict[tuple[str, int], tuple[np.ndarray, np.ndarray, np.ndarray]] = {}
        for clock in SUBSYSTEMS:
            for index in range(3):
                q, coordinates = _qr_coordinates(
                    continuation, clock, index, reduction_matrix_fn
                )
                minimum_rank = min(
                    minimum_rank,
                    int(np.linalg.matrix_rank(coordinates, tol=atol)),
                )
                reduced = stage9_clock_reduction_operator(clock, index) @ state
                state_coordinates = q.conj().T @ reduced
                inverse = np.linalg.inv(coordinates)
                metric = inverse.conj().T @ inverse
                node_data[(clock, index)] = (coordinates, state_coordinates, metric)

        for source_clock, target_clock in permutations(SUBSYSTEMS, 2):
            for source_index, target_index in product(range(3), repeat=2):
                source_c, source_state, source_metric = node_data[
                    (source_clock, source_index)
                ]
                target_c, target_state, target_metric = node_data[
                    (target_clock, target_index)
                ]
                transform = target_c @ np.linalg.inv(source_c)
                reverse = source_c @ np.linalg.inv(target_c)
                max_state = max(
                    max_state,
                    float(np.linalg.norm(transform @ source_state - target_state)),
                )
                max_inverse = max(
                    max_inverse,
                    float(np.linalg.norm(reverse @ transform - np.eye(14))),
                )
                max_metric = max(
                    max_metric,
                    float(
                        np.linalg.norm(
                            transform.conj().T @ target_metric @ transform
                            - source_metric
                        )
                    ),
                )
                if compare_to_canonical_edges:
                    reference = stage9_clock_change_support_matrix(
                        continuation,
                        target_clock,
                        target_index,
                        source_clock,
                        source_index,
                    )
                    max_reference = max(
                        max_reference,
                        float(np.linalg.norm(transform - reference)),
                    )
                comparisons += 1

    expected = 54 * len(continuations)
    valid = bool(
        comparisons == expected
        and minimum_rank == 14
        and max_state <= 10 * atol
        and max_inverse <= 100 * atol
        and max_metric <= 100 * atol
    )
    reconstructible = bool(
        valid and (not compare_to_canonical_edges or max_reference <= 100 * atol)
    )
    return TransportReconstructionDiagnostics(
        continuation_count=len(continuations),
        comparisons=comparisons,
        minimum_chart_rank=minimum_rank,
        max_state_transport_residual=max_state,
        max_inverse_residual=max_inverse,
        max_metric_covariance_residual=max_metric,
        max_reference_map_residual=(
            max_reference if compare_to_canonical_edges else None
        ),
        valid=valid,
        reconstructible_from_node_coordinates=reconstructible,
    )


def _canonical_reduction_matrix(
    continuation: QuantumContinuation, clock: str, index: int
) -> np.ndarray:
    return stage9_clock_reduction_matrix(continuation, clock, index)


def _canonical_physical_state(continuation: QuantumContinuation) -> np.ndarray:
    return canonical_stage9_physical_state(continuation)


def _no_record_reduction_matrix(
    continuation: QuantumContinuation, clock: str, index: int
) -> np.ndarray:
    return stage9b_control_clock_reduction_matrix(
        continuation, "no-record", clock, index
    )


def _no_record_physical_state(continuation: QuantumContinuation) -> np.ndarray:
    return canonical_stage9b_control_physical_state(continuation, "no-record")


def _no_scramble_schedule(
    continuation: QuantumContinuation,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    identity = np.eye(18, dtype=np.complex128)
    record = controlled_record_write_ambient_operator()
    branch = stage9_branch_action_operator(continuation)
    return identity, record, branch @ record


def _no_scramble_dressing(continuation: QuantumContinuation) -> np.ndarray:
    dressing = np.zeros((54, 54), dtype=np.complex128)
    for index, rest in enumerate(_no_scramble_schedule(continuation)):
        dressing += np.kron(clock_reading_projector(index), rest)
    return dressing


def _no_scramble_physical_basis(continuation: QuantumContinuation) -> np.ndarray:
    return _no_scramble_dressing(continuation) @ spectator_physical_basis()


def _no_scramble_reduction_matrix(
    continuation: QuantumContinuation, clock: str, index: int
) -> np.ndarray:
    return (
        stage9_clock_reduction_operator(clock, index)
        @ _no_scramble_physical_basis(continuation)
    )


def _no_scramble_a_reconstruction(
    continuation: QuantumContinuation, index: int
) -> np.ndarray:
    support = spectator_support_basis("A")
    physical = _no_scramble_physical_basis(continuation)
    coordinates = (
        support.conj().T
        @ _no_scramble_reduction_matrix(continuation, "A", index)
    )
    if coordinates.shape != (14, 14) or np.linalg.matrix_rank(
        coordinates, tol=DEFAULT_ATOL
    ) != 14:
        raise ValueError("Stage 9F no-scramble A chart is not invertible")
    return physical @ np.linalg.inv(coordinates) @ support.conj().T


def _no_scramble_physical_state(continuation: QuantumContinuation) -> np.ndarray:
    current = reduced_stage9_state(continuation, CURRENT_EVENT)
    state = _no_scramble_a_reconstruction(
        continuation, CURRENT_EVENT
    ) @ current
    return _normalized(state)


def _no_scramble_reduced_state(
    continuation: QuantumContinuation, event_index: int
) -> np.ndarray:
    return (
        stage9_clock_reduction_operator("A", event_index)
        @ _no_scramble_physical_state(continuation)
    )


def _no_scramble_a_transition(
    continuation: QuantumContinuation,
    target_index: int,
    source_index: int,
) -> np.ndarray:
    support = spectator_support_basis("A")
    transition = (
        stage9_clock_reduction_operator("A", target_index)
        @ _no_scramble_a_reconstruction(continuation, source_index)
    )
    return support.conj().T @ transition @ support


def _no_scramble_event_joint(
    continuation: QuantumContinuation, event_index: int
) -> np.ndarray:
    if event_index not in (LOWER_EVENT, UPPER_EVENT):
        raise ValueError("Stage 9F no-scramble compares e0 and e2 only")
    current = _no_scramble_reduced_state(continuation, CURRENT_EVENT)
    support = spectator_support_basis("A")
    current_coordinates = support.conj().T @ current
    transition = _no_scramble_a_transition(
        continuation, CURRENT_EVENT, event_index
    )
    target_at_current = (
        transition
        @ _target_support_projector()
        @ transition.conj().T
    )
    return _joint_from_current_coordinates(
        current_coordinates, target_at_current
    )


def _no_scramble_direction(
    continuation: QuantumContinuation,
) -> tuple[float, float, float, str]:
    lower = _no_scramble_event_joint(continuation, LOWER_EVENT)
    upper = _no_scramble_event_joint(continuation, UPPER_EVENT)
    lower_information = _mutual_information(lower)
    upper_information = _mutual_information(upper)
    lower_accuracy = _decoder_accuracy(lower)
    upper_accuracy = _decoder_accuracy(upper)
    score = lower_information - upper_information
    access = lower_accuracy - upper_accuracy
    orientation = (
        "none"
        if abs(score) <= 1e-10 and abs(access) <= 1e-10
        else "lower-index"
        if score > 0.0 or access > 0.0
        else "upper-index"
    )
    return lower_information, score, access, orientation


def _no_scramble_admissible(
    continuation: QuantumContinuation, *, atol: float = DEFAULT_ATOL
) -> bool:
    schedule = _no_scramble_schedule(continuation)
    schedule_residual = max(_unitarity_residual(operator) for operator in schedule)
    dressing = _no_scramble_dressing(continuation)
    dressing_residual = _unitarity_residual(dressing)
    constraint = dressing @ spectator_total_constraint_operator() @ dressing.conj().T
    hermiticity = float(np.linalg.norm(constraint - constraint.conj().T))
    physical = _no_scramble_physical_basis(continuation)
    constraint_residual = float(np.linalg.norm(constraint @ physical))
    ranks = tuple(
        int(
            np.linalg.matrix_rank(
                _no_scramble_reduction_matrix(continuation, clock, index),
                tol=atol,
            )
        )
        for clock in SUBSYSTEMS
        for index in range(3)
    )
    return bool(
        schedule_residual <= atol
        and dressing_residual <= atol
        and hermiticity <= atol
        and constraint_residual <= 10 * atol
        and physical.shape[1] == 14
        and min(ranks) == 14
    )


def _no_scramble_v_nontrivial(*, atol: float = DEFAULT_ATOL) -> bool:
    left = canonical_continuation_left()
    right = canonical_continuation_right()
    return bool(
        np.linalg.norm(
            _no_scramble_schedule(left)[UPPER_EVENT]
            - _no_scramble_schedule(right)[UPPER_EVENT]
        )
        > atol
    )


@lru_cache(maxsize=1)
def directional_mechanism_diagnostics() -> DirectionalMechanismDiagnostics:
    continuations = (
        canonical_continuation_left(),
        canonical_continuation_right(),
    )

    no_record_assessments = tuple(
        assess_stage9b_control_direction(item, "no-record")
        for item in continuations
    )
    no_record_current = tuple(
        (
            item.continuation_id,
            _current_record_information(
                reduced_stage9b_control_state(
                    item, "no-record", CURRENT_EVENT
                )
            ),
        )
        for item in continuations
    )
    no_record_transport = _transport_diagnostics(
        continuations,
        _no_record_reduction_matrix,
        _no_record_physical_state,
    )

    no_scramble_assessments = tuple(
        (item, _no_scramble_direction(item)) for item in continuations
    )
    no_scramble_current = tuple(
        (
            item.continuation_id,
            _current_record_information(
                _no_scramble_reduced_state(item, CURRENT_EVENT)
            ),
        )
        for item in continuations
    )
    no_scramble_transport = _transport_diagnostics(
        continuations,
        _no_scramble_reduction_matrix,
        _no_scramble_physical_state,
    )

    no_scramble_record_retained = all(
        information > 1.0 - 1e-9 for _, information in no_scramble_current
    )
    no_scramble_direction_lost = all(
        abs(values[1]) <= 1e-9 and abs(values[2]) <= 1e-9
        for _, values in no_scramble_assessments
    )

    return DirectionalMechanismDiagnostics(
        record_write_current_information=no_record_current,
        record_write_record_scores=tuple(
            (item.continuation_id, assessment.record_score)
            for item, assessment in zip(
                continuations, no_record_assessments, strict=True
            )
        ),
        record_write_accessibility_scores=tuple(
            (item.continuation_id, assessment.accessibility_score)
            for item, assessment in zip(
                continuations, no_record_assessments, strict=True
            )
        ),
        record_write_v_nontrivial=stage9b_control_retains_nontrivial_v(
            "no-record"
        ),
        record_write_valid_constrained_carriers=all(
            assess_stage9b_control_admissibility(
                item, "no-record"
            ).valid_constrained_carrier
            for item in continuations
        ),
        record_write_transport=no_record_transport,
        no_scramble_current_information=no_scramble_current,
        no_scramble_record_scores=tuple(
            (item.continuation_id, values[1])
            for item, values in no_scramble_assessments
        ),
        no_scramble_accessibility_scores=tuple(
            (item.continuation_id, values[2])
            for item, values in no_scramble_assessments
        ),
        no_scramble_v_nontrivial=_no_scramble_v_nontrivial(),
        no_scramble_valid_constrained_carriers=all(
            _no_scramble_admissible(item) for item in continuations
        ),
        no_scramble_transport=no_scramble_transport,
        no_scramble_direction_lost_while_current_record_retained=bool(
            no_scramble_record_retained and no_scramble_direction_lost
        ),
    )


@lru_cache(maxsize=1)
def singleton_qext_diagnostics() -> SingletonDiagnostics:
    left = canonical_continuation_left()
    carrier = Stage9DirectionalCarrier(CURRENT_EVENT, (left,))
    epistemic = make_stage9_epistemic_model(carrier, left, (1.0,))
    ontic = make_stage9_ontic_model(carrier, (1.0,))
    assessment = assess_stage9_direction(left)
    current_information = _current_record_information(
        reduced_stage9_state(left, CURRENT_EVENT)
    )
    semantic_types_distinct = bool(
        privileged_stage9_modal_diagnostic(epistemic)
        != privileged_stage9_modal_diagnostic(ontic)
    )
    ontic_fields = {field.name for field in fields(ontic)}
    transport = _transport_diagnostics(
        (left,),
        _canonical_reduction_matrix,
        _canonical_physical_state,
    )
    future_present = (
        float(np.linalg.norm(reduced_stage9_state(left, UPPER_EVENT)))
        > DEFAULT_ATOL
    )
    return SingletonDiagnostics(
        qext_size=len(carrier.continuations),
        current_record_information=current_information,
        record_score=assessment.record_score,
        accessibility_score=assessment.accessibility_score,
        record_defined=assessment.record_defined,
        semantic_types_distinct=semantic_types_distinct,
        ontic_has_no_selected_continuation_field=(
            "selected_continuation" not in ontic_fields
            and not hasattr(ontic, "selected_continuation")
        ),
        singleton_weight=ontic.extension_weights[0],
        singleton_weight_reconstructible_from_normalization=(
            ontic.extension_weights == (1.0,)
        ),
        future_extension_present=future_present,
        transport=transport,
    )


@lru_cache(maxsize=1)
def _stage9c():
    return stage9c_modal_diagnostics()


@lru_cache(maxsize=1)
def _stage9d():
    return stage9d_transport_diagnostics()


@lru_cache(maxsize=1)
def semantic_weight_diagnostics() -> SemanticWeightDiagnostics:
    diagnostics = _stage9c()
    return SemanticWeightDiagnostics(
        matched_public_views_equal=diagnostics.matched_operational_equal,
        privileged_modal_structures_distinct=(
            diagnostics.privileged_structures_distinct
        ),
        modal_semantics_reconstructible_from_public_carrier=False,
        uniform_weights=(0.5, 0.5),
        alternative_weights=(0.75, 0.25),
        prediction_changes_with_weights=(
            diagnostics.weight_mismatch_changes_prediction
        ),
        weight_change_preserves_directional_data=(
            diagnostics.weight_mismatch_preserves_current_directional_data
        ),
        weights_reconstructible_from_carrier=False,
    )


@lru_cache(maxsize=1)
def accessibility_diagnostics() -> AccessibilityDiagnostics:
    continuations = stage9_extension_set(CURRENT_EVENT)
    assessment = assess_stage9_direction(continuations[0])
    current_information = _current_record_information(
        reduced_stage9_state(continuations[0], CURRENT_EVENT)
    )
    hidden = HiddenAccessView(
        current_anchor=CURRENT_EVENT,
        continuation_ids=tuple(
            continuation.continuation_id for continuation in continuations
        ),
        continuation_weights=(0.5, 0.5),
        current_record_information=current_information,
        record_score=assessment.record_score,
        orientation=assessment.orientation,
    )
    names = tuple(field.name for field in fields(hidden))
    exposed = "accessibility_score" in names
    return AccessibilityDiagnostics(
        global_record_information=current_information,
        global_record_score=assessment.record_score,
        global_accessibility_score=assessment.accessibility_score,
        global_orientation=assessment.orientation,
        hidden_view_field_names=names,
        local_accessibility_field_exposed=exposed,
        v_extension_count_retained=len(continuations),
        weights_retained=hidden.continuation_weights,
        global_direction_preserved=bool(
            assessment.record_defined
            and assessment.record_score > DEFAULT_ATOL
            and assessment.accessibility_score > DEFAULT_ATOL
        ),
        local_access_inaccessible=not exposed,
    )


@lru_cache(maxsize=1)
def perspective_edge_reconstruction_diagnostics() -> TransportReconstructionDiagnostics:
    continuations = stage9_extension_set(CURRENT_EVENT)
    return _transport_diagnostics(
        continuations,
        _canonical_reduction_matrix,
        _canonical_physical_state,
        compare_to_canonical_edges=True,
    )


@lru_cache(maxsize=1)
def correspondence_diagnostics() -> CorrespondenceDiagnostics:
    reconstruction = perspective_edge_reconstruction_diagnostics()
    d = _stage9d()
    return CorrespondenceDiagnostics(
        local_p_atlas_retained=reconstruction.valid,
        local_p_comparisons=reconstruction.comparisons,
        event_class_correspondence_declared=False,
        typed_cross_perspective_rv_identification_established=False,
        wrong_class_control_rejected=d.wrong_class_correspondence_rejected,
        wrong_event_control_rejected=d.wrong_event_correspondence_rejected,
    )


@lru_cache(maxsize=1)
def wrong_observable_diagnostic() -> MismatchDiagnostic:
    d = _stage9d()
    return MismatchDiagnostic(
        mismatch="wrong_record_observable_coordinates",
        affected_role="P_RV_typed_identification",
        detected=d.bare_observable_rejected,
        measurements=(
            ("bare_observable_residual", d.bare_observable_residual),
            ("typed_observable_transport_residual", d.max_observable_transport_residual),
        ),
        note=(
            "bare source-chart matrix reuse is rejected; covariance/algebraic "
            "transport does not supply semantic observable typing"
        ),
    )


def _baseline_probes() -> dict[str, RoleEvidence]:
    c = _stage9c()
    d = _stage9d()
    left = canonical_continuation_left()
    assessment = assess_stage9_direction(left)
    current_information = _current_record_information(
        reduced_stage9_state(left, CURRENT_EVENT)
    )
    return {
        "R_content": _preserved(
            "R_content",
            (("current_information", current_information),),
        ),
        "R_direction": _preserved(
            "R_direction",
            (("record_score", assessment.record_score),),
        ),
        "R_access": _preserved(
            "R_access",
            (("accessibility_score", assessment.accessibility_score),),
        ),
        "V_extension_multiplicity": _preserved(
            "V_extension_multiplicity",
            (("qext_size", c.qext_size),),
        ),
        "V_selected_vs_unselected_semantics": _preserved(
            "V_selected_vs_unselected_semantics",
            (("privileged_structures_distinct", c.privileged_structures_distinct),),
        ),
        "V_weights": _preserved(
            "V_weights",
            (("weights", (0.5, 0.5)),),
        ),
        "P_perspective_transport": _preserved(
            "P_perspective_transport",
            (("state_transports", d.distinct_clock_state_transports),),
        ),
        "event_class_correspondence": _preserved(
            "event_class_correspondence",
            (("correct_correspondence_valid", d.correct_class_correspondence_valid),),
        ),
        "P_RV_typed_identification": _preserved(
            "P_RV_typed_identification",
            (
                ("directional_record_covariance", d.directional_record_covariance),
                ("class_weight_covariance", d.class_weight_transport_covariance),
            ),
        ),
        "O_V_extension_relation": _preserved(
            "O_V_extension_relation",
            (("current_anchor", CURRENT_EVENT), ("qext_size", c.qext_size)),
        ),
    }


@lru_cache(maxsize=1)
def stage9f_ablation_matrix() -> tuple[AblationCase, ...]:
    baseline = _baseline_probes()
    directional = directional_mechanism_diagnostics()
    singleton = singleton_qext_diagnostics()
    semantic = semantic_weight_diagnostics()
    access = accessibility_diagnostics()
    reconstruction = perspective_edge_reconstruction_diagnostics()
    correspondence = correspondence_diagnostics()

    record_write = AblationCase(
        ingredient="record_write_neutralized",
        neutralization=(
            "remove U_rec while retaining the common scrambler and the h_L/h_R "
            "future branch action; re-derive constrained carriers and clock charts"
        ),
        probes=(
            _lost(
                "R_content",
                directional.record_write_current_information,
                "target-memory current record information vanishes",
            ),
            _lost(
                "R_direction",
                directional.record_write_record_scores,
                "without record content the directional record score vanishes",
            ),
            _lost(
                "R_access",
                directional.record_write_accessibility_scores,
                "there is no target-specific record left for the local interface to access",
            ),
            _preserved(
                "V_extension_multiplicity",
                (
                    ("nontrivial_v", directional.record_write_v_nontrivial),
                    ("qext_size", 2),
                ),
                "the h_L/h_R future distinction remains physically nontrivial",
            ),
            baseline["V_selected_vs_unselected_semantics"],
            baseline["V_weights"],
            _preserved(
                "P_perspective_transport",
                (
                    (
                        "comparisons",
                        directional.record_write_transport.comparisons,
                    ),
                    (
                        "valid",
                        directional.record_write_transport.valid,
                    ),
                ),
                "the no-record constrained completions retain rank-14 clock transport",
            ),
            baseline["event_class_correspondence"],
            _not_established(
                "P_RV_typed_identification",
                (("directional_record_present", False),),
                "typed P transport remains, but there is no directional R to identify across charts",
            ),
            baseline["O_V_extension_relation"],
        ),
    )

    scrambler = AblationCase(
        ingredient="scrambler_neutralized",
        neutralization=(
            "retain U_rec at e1 but remove U_scr from e2; keep the h_L/h_R "
            "future branch action and re-derive constrained carriers"
        ),
        probes=(
            _preserved(
                "R_content",
                directional.no_scramble_current_information,
                "the current target-memory record remains one bit",
            ),
            _lost(
                "R_direction",
                directional.no_scramble_record_scores,
                "without the future scrambler lower/upper record information is symmetric",
            ),
            _preserved(
                "R_access",
                (
                    ("current_record_accessible", True),
                    (
                        "directional_accessibility_scores",
                        directional.no_scramble_accessibility_scores,
                    ),
                ),
                "record content remains locally available even though access asymmetry vanishes",
            ),
            _preserved(
                "V_extension_multiplicity",
                (
                    ("nontrivial_v", directional.no_scramble_v_nontrivial),
                    ("qext_size", 2),
                ),
                "the branch distinction survives removal of the directional scrambler",
            ),
            baseline["V_selected_vs_unselected_semantics"],
            baseline["V_weights"],
            _preserved(
                "P_perspective_transport",
                (
                    ("comparisons", directional.no_scramble_transport.comparisons),
                    ("valid", directional.no_scramble_transport.valid),
                ),
                "the re-derived no-scramble clock atlas remains valid",
            ),
            baseline["event_class_correspondence"],
            _not_established(
                "P_RV_typed_identification",
                (("directional_record_present", False),),
                "P/V typing remains but directional-R covariance has no nonzero role to transport",
            ),
            baseline["O_V_extension_relation"],
        ),
    )

    singleton_case = AblationCase(
        ingredient="qext_collapsed_singleton",
        neutralization="retain only one admissible continuation class h_L",
        probes=(
            _preserved(
                "R_content",
                (("current_information", singleton.current_record_information),),
            ),
            _preserved(
                "R_direction",
                (("record_score", singleton.record_score),),
                "nonzero directional R survives collapse of V multiplicity",
            ),
            _preserved(
                "R_access",
                (("accessibility_score", singleton.accessibility_score),),
            ),
            _lost(
                "V_extension_multiplicity",
                (("qext_size", singleton.qext_size),),
                "multi-continuation Potentiality is removed by construction",
            ),
            _preserved(
                "V_selected_vs_unselected_semantics",
                (
                    ("semantic_types_distinct", singleton.semantic_types_distinct),
                    (
                        "ontic_has_no_selector_field",
                        singleton.ontic_has_no_selected_continuation_field,
                    ),
                ),
                "formal selected-vs-unselected typing remains distinct on singleton support",
            ),
            _reconstructible(
                "V_weights",
                (("singleton_weight", singleton.singleton_weight),),
                "normalization uniquely fixes the sole continuation weight to one",
            ),
            _preserved(
                "P_perspective_transport",
                (
                    ("comparisons", singleton.transport.comparisons),
                    ("valid", singleton.transport.valid),
                ),
                "the remaining continuation retains its re-derived clock atlas",
            ),
            _preserved(
                "event_class_correspondence",
                (("singleton_identity_correspondence", True),),
            ),
            _preserved(
                "P_RV_typed_identification",
                (("directional_record_defined", singleton.record_defined),),
                "typed record transport is still meaningful for the remaining class",
            ),
            _preserved(
                "O_V_extension_relation",
                (("future_extension_present", singleton.future_extension_present),),
                "one admissible continuation still extends the current anchor",
            ),
        ),
    )

    semantics_removed = AblationCase(
        ingredient="modal_semantics_removed",
        neutralization=(
            "retain physical carrier, directional records, continuation classes, and "
            "weights but erase selected-vs-unselected model typing"
        ),
        probes=(
            baseline["R_content"],
            baseline["R_direction"],
            baseline["R_access"],
            baseline["V_extension_multiplicity"],
            _lost(
                "V_selected_vs_unselected_semantics",
                (
                    (
                        "same_public_view_supports_distinct_privileged_structures",
                        semantic.privileged_modal_structures_distinct
                        and semantic.matched_public_views_equal,
                    ),
                ),
                "the erased semantic role is not uniquely reconstructed from public P/O/R/V carrier data",
            ),
            baseline["V_weights"],
            baseline["P_perspective_transport"],
            baseline["event_class_correspondence"],
            baseline["P_RV_typed_identification"],
            baseline["O_V_extension_relation"],
        ),
    )

    weights_unfixed = AblationCase(
        ingredient="weights_unfixed",
        neutralization=(
            "retain carrier and modal typing but omit a declared q_E/K weight assignment"
        ),
        probes=(
            baseline["R_content"],
            baseline["R_direction"],
            baseline["R_access"],
            baseline["V_extension_multiplicity"],
            baseline["V_selected_vs_unselected_semantics"],
            _underdetermined(
                "V_weights",
                (
                    ("uniform", semantic.uniform_weights),
                    ("alternative", semantic.alternative_weights),
                    (
                        "prediction_changes",
                        semantic.prediction_changes_with_weights,
                    ),
                ),
                "the same carrier admits distinct normalized weights with different predictions",
            ),
            baseline["P_perspective_transport"],
            baseline["event_class_correspondence"],
            baseline["P_RV_typed_identification"],
            baseline["O_V_extension_relation"],
        ),
    )

    access_hidden = AblationCase(
        ingredient="local_record_access_hidden",
        neutralization=(
            "retain global record content/direction and V data but remove R_access from "
            "the declared local public interface"
        ),
        probes=(
            _preserved(
                "R_content",
                (("global_information", access.global_record_information),),
                "global record content remains represented",
            ),
            _preserved(
                "R_direction",
                (("global_record_score", access.global_record_score),),
                "global directional relation remains represented",
            ),
            _inaccessible(
                "R_access",
                (
                    ("global_accessibility_score", access.global_accessibility_score),
                    (
                        "interface_exposes_accessibility",
                        access.local_accessibility_field_exposed,
                    ),
                ),
                "the global accessible record relation is retained but hidden from the declared local interface",
            ),
            baseline["V_extension_multiplicity"],
            baseline["V_selected_vs_unselected_semantics"],
            baseline["V_weights"],
            baseline["P_perspective_transport"],
            baseline["event_class_correspondence"],
            baseline["P_RV_typed_identification"],
            baseline["O_V_extension_relation"],
        ),
    )

    edges_removed = AblationCase(
        ingredient="explicit_perspective_edges_removed",
        neutralization=(
            "remove stored/explicit cross-clock edge matrices while retaining each "
            "continuation's per-node QR coordinate matrices"
        ),
        probes=(
            baseline["R_content"],
            baseline["R_direction"],
            baseline["R_access"],
            baseline["V_extension_multiplicity"],
            baseline["V_selected_vs_unselected_semantics"],
            baseline["V_weights"],
            _reconstructible(
                "P_perspective_transport",
                (
                    ("comparisons", reconstruction.comparisons),
                    (
                        "max_reference_map_residual",
                        reconstruction.max_reference_map_residual,
                    ),
                ),
                "S^h_{Y<-X}=C_{h,Y} C_{h,X}^{-1} reconstructs all canonical tested edges",
            ),
            baseline["event_class_correspondence"],
            baseline["P_RV_typed_identification"],
            baseline["O_V_extension_relation"],
        ),
    )

    chi_removed = AblationCase(
        ingredient="event_class_correspondence_removed",
        neutralization=(
            "retain all local continuation clock charts and physical edge reconstruction "
            "but remove declared event/class correspondence chi"
        ),
        probes=(
            baseline["R_content"],
            baseline["R_direction"],
            baseline["R_access"],
            baseline["V_extension_multiplicity"],
            baseline["V_selected_vs_unselected_semantics"],
            baseline["V_weights"],
            _preserved(
                "P_perspective_transport",
                (
                    ("comparisons", correspondence.local_p_comparisons),
                    ("atlas_retained", correspondence.local_p_atlas_retained),
                ),
                "bare physical clock transport remains executable locally",
            ),
            _lost(
                "event_class_correspondence",
                (("correspondence_declared", False),),
                "the cross-perspective event/class typing resource is removed by construction",
            ),
            _not_established(
                "P_RV_typed_identification",
                (
                    (
                        "typed_identification_established",
                        correspondence.typed_cross_perspective_rv_identification_established,
                    ),
                    (
                        "wrong_class_control_rejected",
                        correspondence.wrong_class_control_rejected,
                    ),
                    (
                        "wrong_event_control_rejected",
                        correspondence.wrong_event_control_rejected,
                    ),
                ),
                "without chi, local matrices do not license a typed claim about corresponding events/classes",
            ),
            baseline["O_V_extension_relation"],
        ),
    )

    return (
        record_write,
        scrambler,
        singleton_case,
        semantics_removed,
        weights_unfixed,
        access_hidden,
        edges_removed,
        chi_removed,
    )


def stage9f_status_table() -> dict[str, dict[str, str]]:
    return {
        case.ingredient: {
            role: case.status(role).value for role in ROLE_IDS
        }
        for case in stage9f_ablation_matrix()
    }


@lru_cache(maxsize=1)
def stage9f_diagnostics() -> Stage9FDiagnostics:
    return Stage9FDiagnostics(
        directional_mechanism=directional_mechanism_diagnostics(),
        singleton_qext=singleton_qext_diagnostics(),
        semantic_weights=semantic_weight_diagnostics(),
        accessibility=accessibility_diagnostics(),
        edge_reconstruction=perspective_edge_reconstruction_diagnostics(),
        correspondence=correspondence_diagnostics(),
        wrong_observable=wrong_observable_diagnostic(),
    )


def stage9f_summary() -> dict[str, object]:
    diagnostics = stage9f_diagnostics()
    return {
        "stage": "9F",
        "status": (
            "ablation / reconstruction / accessibility matrix completed over "
            "directional R and quantum Potentiality roles"
        ),
        "status_vocabulary": tuple(status.value for status in RoleStatus),
        "roles": ROLE_IDS,
        "ablations": [
            case.as_dict() for case in stage9f_ablation_matrix()
        ],
        "status_table": stage9f_status_table(),
        "diagnostics": asdict(diagnostics),
        "mismatches": [diagnostics.wrong_observable.as_dict()],
        "exit_criteria_satisfied": tuple(range(43, 48)),
        "criterion_assessment": {
            "43": (
                "record-write and scrambler ablations separate R_content, "
                "R_direction, R_access, and nontrivial V"
            ),
            "44": (
                "singleton-QExt ablation removes V multiplicity while retaining "
                "directional R and makes the sole weight reconstructible"
            ),
            "45": (
                "erased modal semantics are lost/not uniquely reconstructed and "
                "unfixed nontrivial weights are underdetermined"
            ),
            "46": (
                "global R_content/R_direction and V remain represented while "
                "declared local R_access becomes inaccessible"
            ),
            "47": (
                "explicit P edges are reconstructible from node coordinates; "
                "removing event/class chi makes typed P-R-V identification "
                "not_established; wrong observable coordinates are rejected"
            ),
        },
        "next": "Stage 9G — synthesis and evidence-selected next gate",
        "guards": (
            "lost != metaphysically irreducible",
            "reconstructible != universally redundant",
            "underdetermined != ontically open",
            "inaccessible != globally absent",
            "not_established != false",
            "record content != directional record arrow",
            "directional R without V multiplicity != universal R-V independence theorem",
            "V without directional R != universal R-V independence theorem",
            "singleton support != absence of a formal selected-vs-unselected type distinction",
            "P edge reconstruction != P=R or P=V",
            "local P transport without chi != typed event/class identification",
            "covariance of a wrongly typed observable != semantic correctness",
            "directional record arrow != ontological future openness",
            "directional record arrow != ontological becoming",
            "full Stage 9C future-measurement covariance remains not_established",
        ),
    }
