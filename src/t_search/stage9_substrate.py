"""Stage 9A common directional-record / quantum-Potentiality substrate.

Stage 8A provided two physically inequivalent continuations sharing the current
A-clock actuality through e1, but its e2 schedules retained target-record
information symmetrically and therefore did not carry a directional record
arrow. Stage 7C provided the complementary directional mechanism:

    V_0 = I
    V_1 = U_rec
    V_2 = U_scr U_rec

Stage 9A combines those already-tested ingredients without identifying the
continuation label with record direction.  Both canonical continuations use the
same record write and the same target scrambler.  They differ only through the
Stage 8 C-sector phase action applied after the common scrambling completion:

    h_L: V_2 = U_scr U_rec
    h_R: V_2 = Z_C U_scr U_rec

Z_C is identity on memory and commutes with the B-energy record-target
projector.  Thus the continuation distinction is carried by a future physical
degree of freedom separate from the record-direction channel.

As in Stages 7-8, each continuation defines its own clock-conditioned dressing
W_h and constrained operator H_h = W_h H_0 W_h^dagger.  Physical bases and
clock reductions are derived from that continuation-specific constrained
construction.

This module establishes only the finite Stage 9A substrate.  It does not infer
ontological future openness or ontological becoming from the coexistence of
nontrivial QExt and a directional record diagnostic.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Sequence

import numpy as np

from .stage3_asymmetry import orientation_from_scores
from .stage5_clock_change import DEFAULT_ATOL, SUBSYSTEMS
from .stage7_history import (
    CURRENT_EVENT,
    LOWER_EVENT,
    UPPER_EVENT,
    canonical_source_support_state,
    clock_reading_projector,
    pair_scrambler_ambient_operator,
)
from .stage7_record import canonical_target_pair_projector, controlled_record_write_ambient_operator
from .stage7_spectator import (
    MEMORY_DIMENSION,
    memory_identity,
    spectator_kinematic_clock_projection_operator,
    spectator_physical_basis,
    spectator_support_basis,
    spectator_total_constraint_operator,
)
from .stage8_continuations import (
    QuantumContinuation,
    canonical_continuation_left,
    canonical_continuation_right,
    future_pair_coherence_probe_support_matrix,
    future_pair_phase_ambient_operator,
    renamed_continuation,
)

CANONICAL_ANCHOR = CURRENT_EVENT
TERMINAL_EVENT = UPPER_EVENT


@dataclass(frozen=True)
class Stage9AAdmissibility:
    continuation_id: str
    admissible: bool
    current_prefix_compatible: bool
    schedule_unitarity_residual: float
    dressing_unitarity_residual: float
    constraint_hermiticity_residual: float
    physical_constraint_residual: float
    physical_dimension: int
    minimum_clock_reduction_rank: int
    branch_action_memory_neutral: bool
    branch_action_record_target_neutral: bool


@dataclass(frozen=True)
class Stage9ADirectionalAssessment:
    continuation_id: str
    lower_information: float
    upper_information: float
    lower_accuracy: float
    upper_accuracy: float
    record_score: float
    accessibility_score: float
    orientation: str
    record_defined: bool
    internally_anchored: bool


@dataclass(frozen=True)
class Stage9ASubstrateDiagnostics:
    qext_size: int
    physical_continuations: tuple[str, ...]
    common_e0_state_residual: float
    common_e1_state_residual: float
    current_record_information_residual: float
    per_continuation_record_scores: tuple[tuple[str, float], ...]
    per_continuation_accessibility_scores: tuple[tuple[str, float], ...]
    minimum_record_score: float
    minimum_accessibility_score: float
    coherent_direction: bool
    future_state_overlap_squared: float
    future_state_distance: float
    future_probe_expectation_left: float
    future_probe_expectation_right: float
    future_probe_difference: float
    future_operator_residual: float
    physically_inequivalent: bool
    minimum_clock_reduction_rank: int
    maximum_constraint_residual: float
    branch_action_memory_neutral: bool
    branch_action_record_target_neutral: bool
    continuation_identity_separated_from_record_channel: bool
    renamed_equivalent: bool
    deduplicated_size_with_rename: int
    invalid_current_prefix_rejected: bool
    terminal_qext_size: int


def _ambient_identity() -> np.ndarray:
    return np.eye(18, dtype=np.complex128)


def stage9_branch_action_operator(continuation: QuantumContinuation) -> np.ndarray:
    """Return only the continuation-defining future action, not the arrow channel."""

    if continuation.future_action == "identity":
        return _ambient_identity()
    if continuation.future_action == "c-phase":
        return future_pair_phase_ambient_operator()
    raise ValueError("unknown Stage 9A future action")


def stage9_schedule_rest_operators(
    continuation: QuantumContinuation,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return the canonical Stage 9A cumulative A-clock rest schedules.

    The record write and target scrambler are common to both canonical
    continuations.  The continuation-specific action is applied only after the
    common directional completion.
    """

    identity = _ambient_identity()
    record = controlled_record_write_ambient_operator()
    scramble = pair_scrambler_ambient_operator()
    if continuation.current_action != "record":
        current = identity
        common_future = scramble
    else:
        current = record
        common_future = scramble @ record
    future = stage9_branch_action_operator(continuation) @ common_future
    return identity, current, future


def stage9_dressing_operator(continuation: QuantumContinuation) -> np.ndarray:
    dressing = np.zeros((54, 54), dtype=np.complex128)
    for index, rest_operator in enumerate(stage9_schedule_rest_operators(continuation)):
        dressing += np.kron(clock_reading_projector(index), rest_operator)
    return dressing


def stage9_constraint_operator(continuation: QuantumContinuation) -> np.ndarray:
    dressing = stage9_dressing_operator(continuation)
    baseline = spectator_total_constraint_operator()
    return dressing @ baseline @ dressing.conj().T


def stage9_physical_basis(continuation: QuantumContinuation) -> np.ndarray:
    return stage9_dressing_operator(continuation) @ spectator_physical_basis()


def stage9_clock_reduction_operator(clock: str, index: int) -> np.ndarray:
    if clock not in SUBSYSTEMS:
        raise ValueError("clock must be one of A, B, or C")
    if isinstance(index, bool) or not isinstance(index, int) or index not in (0, 1, 2):
        raise ValueError("clock index must be 0, 1, or 2")
    return np.sqrt(3.0) * spectator_kinematic_clock_projection_operator(clock, index)


def stage9_clock_reduction_matrix(
    continuation: QuantumContinuation,
    clock: str,
    index: int,
) -> np.ndarray:
    return stage9_clock_reduction_operator(clock, index) @ stage9_physical_basis(continuation)


def _clock_support_qr(
    continuation: QuantumContinuation,
    clock: str,
    index: int,
) -> tuple[np.ndarray, np.ndarray]:
    reduction = stage9_clock_reduction_matrix(continuation, clock, index)
    q, r = np.linalg.qr(reduction, mode="reduced")
    if np.linalg.matrix_rank(r, tol=DEFAULT_ATOL) != reduction.shape[1]:
        raise ValueError("Stage 9A clock reading is not an injective perspective")
    return q, r


def stage9_clock_reconstruction_operator(
    continuation: QuantumContinuation,
    clock: str,
    index: int,
) -> np.ndarray:
    support, coordinates = _clock_support_qr(continuation, clock, index)
    physical = stage9_physical_basis(continuation)
    return physical @ np.linalg.inv(coordinates) @ support.conj().T


def canonical_stage9_physical_state(continuation: QuantumContinuation) -> np.ndarray:
    source = canonical_source_support_state()
    reconstruction = stage9_clock_reconstruction_operator(
        continuation, "A", LOWER_EVENT
    )
    state = reconstruction @ source
    norm = np.linalg.norm(state)
    if norm <= DEFAULT_ATOL:
        raise ValueError("Stage 9A reconstruction produced zero physical state")
    return state / norm


def reduced_stage9_state(
    continuation: QuantumContinuation,
    event_index: int,
) -> np.ndarray:
    if event_index not in (LOWER_EVENT, CURRENT_EVENT, UPPER_EVENT):
        raise ValueError("event index must be 0, 1, or 2")
    state = canonical_stage9_physical_state(continuation)
    return stage9_clock_reduction_operator("A", event_index) @ state


def stage9_constraint_residual(continuation: QuantumContinuation) -> float:
    state = canonical_stage9_physical_state(continuation)
    return float(np.linalg.norm(stage9_constraint_operator(continuation) @ state))


def _fixed_a_support_coordinates(
    continuation: QuantumContinuation,
    index: int,
) -> np.ndarray:
    support = spectator_support_basis("A")
    return support.conj().T @ stage9_clock_reduction_matrix(continuation, "A", index)


def stage9_a_reconstruction_operator(
    continuation: QuantumContinuation,
    index: int,
) -> np.ndarray:
    """Reconstruct from the fixed A-rest support used by the record semantics."""

    support = spectator_support_basis("A")
    physical = stage9_physical_basis(continuation)
    coordinates = _fixed_a_support_coordinates(continuation, index)
    if np.linalg.matrix_rank(coordinates, tol=DEFAULT_ATOL) != coordinates.shape[0]:
        raise ValueError("Stage 9A A-clock fixed-support coordinates are not invertible")
    return physical @ np.linalg.inv(coordinates) @ support.conj().T


def stage9_a_transition_support_matrix(
    continuation: QuantumContinuation,
    target_index: int,
    source_index: int,
) -> np.ndarray:
    support = spectator_support_basis("A")
    transition = (
        stage9_clock_reduction_operator("A", target_index)
        @ stage9_a_reconstruction_operator(continuation, source_index)
    )
    return support.conj().T @ transition @ support


def _target_support_projector() -> np.ndarray:
    return np.kron(canonical_target_pair_projector(), memory_identity())


def _memory_support_projector(bit: int) -> np.ndarray:
    if bit not in (0, 1):
        raise ValueError("memory bit must be 0 or 1")
    pair_dimension = canonical_target_pair_projector().shape[0]
    memory = np.zeros((MEMORY_DIMENSION, MEMORY_DIMENSION), dtype=np.complex128)
    memory[bit, bit] = 1.0
    return np.kron(np.eye(pair_dimension, dtype=np.complex128), memory)


def _joint_from_current_coordinates(
    current_coordinates: np.ndarray,
    target_projector_at_current: np.ndarray,
) -> np.ndarray:
    identity = np.eye(target_projector_at_current.shape[0], dtype=np.complex128)
    joint = np.zeros((2, 2), dtype=float)
    commutator_max = 0.0
    for target_bit, target_projector in (
        (1, target_projector_at_current),
        (0, identity - target_projector_at_current),
    ):
        for memory_bit in (0, 1):
            memory_projector = _memory_support_projector(memory_bit)
            commutator_max = max(
                commutator_max,
                float(
                    np.linalg.norm(
                        target_projector @ memory_projector
                        - memory_projector @ target_projector
                    )
                ),
            )
            probability = np.vdot(
                current_coordinates,
                target_projector @ memory_projector @ current_coordinates,
            ).real
            joint[target_bit, memory_bit] = float(probability)
    if commutator_max > DEFAULT_ATOL:
        raise ValueError("Stage 9A target and memory readouts must commute")
    total = float(np.sum(joint))
    if total <= 0.0:
        raise ValueError("Stage 9A joint distribution has zero total probability")
    return joint / total


def _mutual_information(joint: np.ndarray) -> float:
    probabilities = np.asarray(joint, dtype=float)
    px = np.sum(probabilities, axis=1, keepdims=True)
    pm = np.sum(probabilities, axis=0, keepdims=True)
    independent = px @ pm
    mask = probabilities > 0.0
    return float(
        np.sum(
            probabilities[mask]
            * np.log2(probabilities[mask] / independent[mask])
        )
    )


def _decoder_accuracy(joint: np.ndarray) -> float:
    return float(sum(np.max(joint[:, memory_bit]) for memory_bit in (0, 1)))


def stage9_event_target_joint_distribution(
    continuation: QuantumContinuation,
    event_index: int,
) -> np.ndarray:
    if event_index not in (LOWER_EVENT, UPPER_EVENT):
        raise ValueError("Stage 9A compares only lower e0 and upper e2")
    current = reduced_stage9_state(continuation, CURRENT_EVENT)
    support = spectator_support_basis("A")
    current_coordinates = support.conj().T @ current
    transition = stage9_a_transition_support_matrix(
        continuation, CURRENT_EVENT, event_index
    )
    target_at_event = _target_support_projector()
    target_at_current = transition @ target_at_event @ transition.conj().T
    return _joint_from_current_coordinates(current_coordinates, target_at_current)


def assess_stage9_direction(
    continuation: QuantumContinuation,
    *,
    tolerance: float = 1e-10,
) -> Stage9ADirectionalAssessment:
    lower_joint = stage9_event_target_joint_distribution(continuation, LOWER_EVENT)
    upper_joint = stage9_event_target_joint_distribution(continuation, UPPER_EVENT)
    lower_information = _mutual_information(lower_joint)
    upper_information = _mutual_information(upper_joint)
    lower_accuracy = _decoder_accuracy(lower_joint)
    upper_accuracy = _decoder_accuracy(upper_joint)
    record_score = lower_information - upper_information
    accessibility_score = lower_accuracy - upper_accuracy
    orientation = orientation_from_scores(
        record_score, accessibility_score, tolerance=tolerance
    )
    return Stage9ADirectionalAssessment(
        continuation_id=continuation.continuation_id,
        lower_information=lower_information,
        upper_information=upper_information,
        lower_accuracy=lower_accuracy,
        upper_accuracy=upper_accuracy,
        record_score=record_score,
        accessibility_score=accessibility_score,
        orientation=orientation,
        record_defined=bool(orientation != "none"),
        internally_anchored=True,
    )


def _memory_z_ambient() -> np.ndarray:
    support = spectator_support_basis("A")
    pair_dimension = canonical_target_pair_projector().shape[0]
    memory_z = np.diag([1.0, -1.0]).astype(np.complex128)
    support_operator = np.kron(
        np.eye(pair_dimension, dtype=np.complex128), memory_z
    )
    projector = support @ support.conj().T
    identity = _ambient_identity()
    return support @ support_operator @ support.conj().T + (identity - projector)


def _record_target_ambient_projector() -> np.ndarray:
    support = spectator_support_basis("A")
    target_support = _target_support_projector()
    return support @ target_support @ support.conj().T


def _branch_action_memory_neutral(
    continuation: QuantumContinuation,
    *,
    atol: float = DEFAULT_ATOL,
) -> bool:
    branch = stage9_branch_action_operator(continuation)
    memory_z = _memory_z_ambient()
    return bool(np.linalg.norm(branch @ memory_z - memory_z @ branch) <= atol)


def _branch_action_record_target_neutral(
    continuation: QuantumContinuation,
    *,
    atol: float = DEFAULT_ATOL,
) -> bool:
    branch = stage9_branch_action_operator(continuation)
    target = _record_target_ambient_projector()
    return bool(np.linalg.norm(branch @ target - target @ branch) <= atol)


def assess_stage9_admissibility(
    continuation: QuantumContinuation,
    *,
    atol: float = DEFAULT_ATOL,
) -> Stage9AAdmissibility:
    schedule = stage9_schedule_rest_operators(continuation)
    identity = _ambient_identity()
    record = controlled_record_write_ambient_operator()
    prefix_ok = bool(
        continuation.current_anchor == CANONICAL_ANCHOR
        and np.linalg.norm(schedule[LOWER_EVENT] - identity) <= atol
        and np.linalg.norm(schedule[CURRENT_EVENT] - record) <= atol
    )
    schedule_unitarity = max(
        float(np.linalg.norm(op.conj().T @ op - identity)) for op in schedule
    )
    dressing = stage9_dressing_operator(continuation)
    dressing_unitarity = float(
        np.linalg.norm(
            dressing.conj().T @ dressing
            - np.eye(dressing.shape[0], dtype=np.complex128)
        )
    )
    constraint = stage9_constraint_operator(continuation)
    hermiticity = float(np.linalg.norm(constraint - constraint.conj().T))
    physical = stage9_physical_basis(continuation)
    physical_dimension = int(physical.shape[1])
    ranks = [
        int(
            np.linalg.matrix_rank(
                stage9_clock_reduction_matrix(continuation, clock, index),
                tol=atol,
            )
        )
        for clock in SUBSYSTEMS
        for index in (0, 1, 2)
    ]
    try:
        residual = stage9_constraint_residual(continuation)
    except (ValueError, np.linalg.LinAlgError):
        residual = float("inf")
    admissible = bool(
        prefix_ok
        and schedule_unitarity <= atol
        and dressing_unitarity <= atol
        and hermiticity <= atol
        and physical_dimension == 14
        and min(ranks) == 14
        and residual <= atol
    )
    return Stage9AAdmissibility(
        continuation_id=continuation.continuation_id,
        admissible=admissible,
        current_prefix_compatible=prefix_ok,
        schedule_unitarity_residual=schedule_unitarity,
        dressing_unitarity_residual=dressing_unitarity,
        constraint_hermiticity_residual=hermiticity,
        physical_constraint_residual=residual,
        physical_dimension=physical_dimension,
        minimum_clock_reduction_rank=min(ranks),
        branch_action_memory_neutral=_branch_action_memory_neutral(
            continuation, atol=atol
        ),
        branch_action_record_target_neutral=_branch_action_record_target_neutral(
            continuation, atol=atol
        ),
    )


def stage9_continuation_equivalent(
    left: QuantumContinuation,
    right: QuantumContinuation,
    *,
    atol: float = DEFAULT_ATOL,
) -> bool:
    if left.current_anchor != right.current_anchor:
        return False
    left_schedule = stage9_schedule_rest_operators(left)
    right_schedule = stage9_schedule_rest_operators(right)
    return all(
        np.linalg.norm(a - b) <= atol
        for a, b in zip(left_schedule, right_schedule, strict=True)
    )


def deduplicate_stage9_continuations(
    continuations: Sequence[QuantumContinuation],
    *,
    atol: float = DEFAULT_ATOL,
) -> tuple[QuantumContinuation, ...]:
    representatives: list[QuantumContinuation] = []
    for continuation in continuations:
        if not any(
            stage9_continuation_equivalent(continuation, existing, atol=atol)
            for existing in representatives
        ):
            representatives.append(continuation)
    return tuple(representatives)


def stage9_extension_set(
    current_event: int = CANONICAL_ANCHOR,
    *,
    candidates: Iterable[QuantumContinuation] | None = None,
    atol: float = DEFAULT_ATOL,
) -> tuple[QuantumContinuation, ...]:
    if current_event == TERMINAL_EVENT:
        return ()
    if current_event != CANONICAL_ANCHOR:
        raise ValueError("canonical Stage 9A QExt is declared only at e1 or terminal e2")
    proposed = tuple(candidates) if candidates is not None else (
        canonical_continuation_left(),
        canonical_continuation_right(),
    )
    for continuation in proposed:
        assessment = assess_stage9_admissibility(continuation, atol=atol)
        if not assessment.admissible:
            raise ValueError(
                f"continuation {continuation.continuation_id!r} is not Stage 9A admissible/current-compatible"
            )
    return deduplicate_stage9_continuations(proposed, atol=atol)


def _normalized_reduced_state(
    continuation: QuantumContinuation,
    event_index: int,
) -> np.ndarray:
    state = reduced_stage9_state(continuation, event_index)
    norm = np.linalg.norm(state)
    if norm <= DEFAULT_ATOL:
        raise ValueError("Stage 9A reduced state has zero norm")
    return state / norm


def _future_probe_expectation(continuation: QuantumContinuation) -> float:
    support = spectator_support_basis("A")
    future = support.conj().T @ _normalized_reduced_state(
        continuation, UPPER_EVENT
    )
    probe = future_pair_coherence_probe_support_matrix()
    return float(np.vdot(future, probe @ future).real)


def stage9a_substrate_diagnostics(
    *,
    atol: float = DEFAULT_ATOL,
) -> Stage9ASubstrateDiagnostics:
    qext = stage9_extension_set(atol=atol)
    left, right = qext
    left_e0 = _normalized_reduced_state(left, LOWER_EVENT)
    right_e0 = _normalized_reduced_state(right, LOWER_EVENT)
    left_e1 = _normalized_reduced_state(left, CURRENT_EVENT)
    right_e1 = _normalized_reduced_state(right, CURRENT_EVENT)
    left_e2 = _normalized_reduced_state(left, UPPER_EVENT)
    right_e2 = _normalized_reduced_state(right, UPPER_EVENT)

    assessments = tuple(assess_stage9_direction(item) for item in qext)
    record_scores = tuple(
        (item.continuation_id, assessment.record_score)
        for item, assessment in zip(qext, assessments, strict=True)
    )
    accessibility_scores = tuple(
        (item.continuation_id, assessment.accessibility_score)
        for item, assessment in zip(qext, assessments, strict=True)
    )
    orientations = tuple(assessment.orientation for assessment in assessments)
    coherent_direction = bool(
        all(assessment.record_defined for assessment in assessments)
        and len(set(orientations)) == 1
        and orientations[0] != "none"
    )

    overlap_squared = float(abs(np.vdot(left_e2, right_e2)) ** 2)
    phase = np.vdot(left_e2, right_e2)
    if abs(phase) > atol:
        phase = phase / abs(phase)
    else:
        phase = 1.0 + 0.0j
    future_distance = float(np.linalg.norm(left_e2 - phase.conjugate() * right_e2))
    left_probe = _future_probe_expectation(left)
    right_probe = _future_probe_expectation(right)
    future_operator_residual = float(
        np.linalg.norm(
            stage9_schedule_rest_operators(left)[UPPER_EVENT]
            - stage9_schedule_rest_operators(right)[UPPER_EVENT]
        )
    )
    physically_inequivalent = bool(
        overlap_squared < 1.0 - atol
        or abs(left_probe - right_probe) > atol
        or future_operator_residual > atol
    )

    admissibility = tuple(assess_stage9_admissibility(item, atol=atol) for item in qext)
    renamed = renamed_continuation(left, "cosmetic-stage9-label")
    deduplicated = deduplicate_stage9_continuations((left, right, renamed), atol=atol)

    invalid = QuantumContinuation(
        continuation_id="invalid-stage9-current",
        future_action="identity",
        current_action="identity",
    )
    invalid_rejected = False
    try:
        stage9_extension_set(
            candidates=(left, right, invalid),
            atol=atol,
        )
    except ValueError:
        invalid_rejected = True

    return Stage9ASubstrateDiagnostics(
        qext_size=len(qext),
        physical_continuations=tuple(item.continuation_id for item in qext),
        common_e0_state_residual=float(np.linalg.norm(left_e0 - right_e0)),
        common_e1_state_residual=float(np.linalg.norm(left_e1 - right_e1)),
        current_record_information_residual=abs(
            assessments[0].lower_information - assessments[1].lower_information
        ),
        per_continuation_record_scores=record_scores,
        per_continuation_accessibility_scores=accessibility_scores,
        minimum_record_score=min(item.record_score for item in assessments),
        minimum_accessibility_score=min(
            item.accessibility_score for item in assessments
        ),
        coherent_direction=coherent_direction,
        future_state_overlap_squared=overlap_squared,
        future_state_distance=future_distance,
        future_probe_expectation_left=left_probe,
        future_probe_expectation_right=right_probe,
        future_probe_difference=abs(left_probe - right_probe),
        future_operator_residual=future_operator_residual,
        physically_inequivalent=physically_inequivalent,
        minimum_clock_reduction_rank=min(
            item.minimum_clock_reduction_rank for item in admissibility
        ),
        maximum_constraint_residual=max(
            item.physical_constraint_residual for item in admissibility
        ),
        branch_action_memory_neutral=all(
            item.branch_action_memory_neutral for item in admissibility
        ),
        branch_action_record_target_neutral=all(
            item.branch_action_record_target_neutral for item in admissibility
        ),
        continuation_identity_separated_from_record_channel=bool(
            coherent_direction
            and all(item.branch_action_memory_neutral for item in admissibility)
            and all(
                item.branch_action_record_target_neutral for item in admissibility
            )
            and physically_inequivalent
        ),
        renamed_equivalent=stage9_continuation_equivalent(left, renamed, atol=atol),
        deduplicated_size_with_rename=len(deduplicated),
        invalid_current_prefix_rejected=invalid_rejected,
        terminal_qext_size=len(stage9_extension_set(TERMINAL_EVENT, atol=atol)),
    )


def stage9a_summary() -> dict[str, object]:
    qext = stage9_extension_set()
    assessments = tuple(assess_stage9_direction(item) for item in qext)
    diagnostics = stage9a_substrate_diagnostics()
    return {
        "current_anchor": "e1",
        "qext": tuple(item.continuation_id for item in qext),
        "schedule": {
            "common_e0": "I",
            "common_e1": "U_rec",
            "h_L_e2": "U_scr U_rec",
            "h_R_e2": "Z_C U_scr U_rec",
        },
        "direction": tuple(asdict(item) for item in assessments),
        "diagnostics": asdict(diagnostics),
        "guards": (
            "directional record arrow != ontological future openness",
            "directional record arrow != ontological becoming",
            "QExt represented != ontically real futures by definition",
            "continuation identity != record-direction identity",
            "weighted directional score != continuation-independent directional structure",
            "finite constrained-model success != empirical discovery",
        ),
    }
