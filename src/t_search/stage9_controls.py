"""Stage 9B directional diagnostics and controls on the Stage 9A carrier.

The controls keep the Stage 9A continuation-defining C-sector branch action
separate from the record-direction mechanism.

Forward uses the Stage 9A schedule

    (I, U_rec, B_h U_scr U_rec).

Reversed reverses the *common record/scramble interaction skeleton* rather than
merely iterating event labels backwards:

    (U_scr U_rec, U_rec, B_h).

For the identity branch this is exactly the modeled-history reversal of the
common directional skeleton (I, U_rec, U_scr U_rec).  The independent branch
action B_h is deliberately retained at e2 so nontrivial V remains a future
continuation distinction.

Balanced is the equal operational mixture of the forward and reversed
constrained histories for one continuation.  No-record neutralizes only the
record write while retaining the scrambler and the same branch action:

    (I, I, B_h U_scr).

All pure control histories are re-embedded in the constrained multi-clock
construction.  Balanced is a mixture of two separately valid constrained
histories, not a claim that their averaged dressing is itself a unitary pure
history.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

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
from .stage7_record import controlled_record_write_ambient_operator
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
from .stage9_substrate import (
    _decoder_accuracy,
    _joint_from_current_coordinates,
    _mutual_information,
    _target_support_projector,
    reduced_stage9_state,
    stage9_branch_action_operator,
    stage9_clock_reduction_operator,
    stage9_schedule_rest_operators,
)

Stage9BControl = Literal["forward", "reversed", "balanced", "no-record"]
PURE_CONTROLS: tuple[Stage9BControl, ...] = ("forward", "reversed", "no-record")
ALL_CONTROLS: tuple[Stage9BControl, ...] = (
    "forward",
    "reversed",
    "balanced",
    "no-record",
)


@dataclass(frozen=True)
class Stage9BControlAssessment:
    continuation_id: str
    control: Stage9BControl
    lower_information: float
    upper_information: float
    lower_accuracy: float
    upper_accuracy: float
    record_score: float
    accessibility_score: float
    orientation: str
    record_defined: bool
    branch_weight_used: bool
    v_extension_nontrivial: bool


@dataclass(frozen=True)
class Stage9BControlAdmissibility:
    continuation_id: str
    control: Stage9BControl
    valid_constrained_carrier: bool
    schedule_unitarity_residual: float
    dressing_unitarity_residual: float
    constraint_hermiticity_residual: float
    physical_constraint_residual: float
    physical_dimension: int
    minimum_clock_reduction_rank: int


@dataclass(frozen=True)
class Stage9BControlDiagnostics:
    forward_scores: tuple[tuple[str, float], ...]
    reversed_scores: tuple[tuple[str, float], ...]
    balanced_scores: tuple[tuple[str, float], ...]
    no_record_scores: tuple[tuple[str, float], ...]
    forward_accessibility_scores: tuple[tuple[str, float], ...]
    reversed_accessibility_scores: tuple[tuple[str, float], ...]
    balanced_accessibility_scores: tuple[tuple[str, float], ...]
    no_record_accessibility_scores: tuple[tuple[str, float], ...]
    reversal_record_residual: float
    reversal_accessibility_residual: float
    balanced_record_residual: float
    balanced_accessibility_residual: float
    no_record_record_residual: float
    no_record_accessibility_residual: float
    common_reversal_is_interaction_reversal: bool
    all_controls_retain_nontrivial_v: bool
    all_pure_controls_valid_constrained_carriers: bool
    minimum_clock_reduction_rank: int
    maximum_constraint_residual: float


def _ambient_identity() -> np.ndarray:
    return np.eye(18, dtype=np.complex128)


def stage9b_control_schedule_rest_operators(
    continuation: QuantumContinuation,
    control: Stage9BControl,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return one pure Stage 9B control schedule.

    ``balanced`` is intentionally excluded because it is an equal mixture of
    two valid constrained histories rather than one pure unitary schedule.
    """

    if control == "balanced":
        raise ValueError("balanced is a mixture of forward and reversed histories")
    if control not in PURE_CONTROLS:
        raise ValueError("unknown Stage 9B control")

    if control == "forward":
        return stage9_schedule_rest_operators(continuation)

    identity = _ambient_identity()
    record = controlled_record_write_ambient_operator()
    scramble = pair_scrambler_ambient_operator()
    branch = stage9_branch_action_operator(continuation)

    if control == "reversed":
        # Reverse only the common R-direction mechanism.  The independent
        # continuation branch action stays future-facing at e2.
        return scramble @ record, record, branch

    # no-record: remove U_rec but preserve the common scrambler and B_h.
    return identity, identity, branch @ scramble


def stage9b_control_dressing_operator(
    continuation: QuantumContinuation,
    control: Stage9BControl,
) -> np.ndarray:
    dressing = np.zeros((54, 54), dtype=np.complex128)
    for index, rest_operator in enumerate(
        stage9b_control_schedule_rest_operators(continuation, control)
    ):
        dressing += np.kron(clock_reading_projector(index), rest_operator)
    return dressing


def stage9b_control_constraint_operator(
    continuation: QuantumContinuation,
    control: Stage9BControl,
) -> np.ndarray:
    dressing = stage9b_control_dressing_operator(continuation, control)
    baseline = spectator_total_constraint_operator()
    return dressing @ baseline @ dressing.conj().T


def stage9b_control_physical_basis(
    continuation: QuantumContinuation,
    control: Stage9BControl,
) -> np.ndarray:
    return stage9b_control_dressing_operator(continuation, control) @ spectator_physical_basis()


def stage9b_control_clock_reduction_matrix(
    continuation: QuantumContinuation,
    control: Stage9BControl,
    clock: str,
    index: int,
) -> np.ndarray:
    return (
        stage9_clock_reduction_operator(clock, index)
        @ stage9b_control_physical_basis(continuation, control)
    )


def _control_fixed_a_support_coordinates(
    continuation: QuantumContinuation,
    control: Stage9BControl,
    index: int,
) -> np.ndarray:
    support = spectator_support_basis("A")
    return support.conj().T @ stage9b_control_clock_reduction_matrix(
        continuation, control, "A", index
    )


def stage9b_control_a_reconstruction_operator(
    continuation: QuantumContinuation,
    control: Stage9BControl,
    index: int,
) -> np.ndarray:
    support = spectator_support_basis("A")
    physical = stage9b_control_physical_basis(continuation, control)
    coordinates = _control_fixed_a_support_coordinates(continuation, control, index)
    if np.linalg.matrix_rank(coordinates, tol=DEFAULT_ATOL) != coordinates.shape[0]:
        raise ValueError("Stage 9B A-clock fixed-support coordinates are not invertible")
    return physical @ np.linalg.inv(coordinates) @ support.conj().T


def _declared_current_support_state(
    continuation: QuantumContinuation,
    control: Stage9BControl,
) -> np.ndarray:
    if control in ("forward", "reversed"):
        # Reversal is anchored on exactly the Stage 9A e1 Actuality.
        return reduced_stage9_state(continuation, CURRENT_EVENT)
    if control == "no-record":
        # Neutralizing U_rec means the declared current memory stays blank.
        return canonical_source_support_state()
    raise ValueError("balanced has no single pure current support state")


def canonical_stage9b_control_physical_state(
    continuation: QuantumContinuation,
    control: Stage9BControl,
) -> np.ndarray:
    if control == "balanced":
        raise ValueError("balanced is a mixture, not one pure physical state")
    current = _declared_current_support_state(continuation, control)
    reconstruction = stage9b_control_a_reconstruction_operator(
        continuation, control, CURRENT_EVENT
    )
    state = reconstruction @ current
    norm = np.linalg.norm(state)
    if norm <= DEFAULT_ATOL:
        raise ValueError("Stage 9B reconstruction produced zero physical state")
    return state / norm


def reduced_stage9b_control_state(
    continuation: QuantumContinuation,
    control: Stage9BControl,
    event_index: int,
) -> np.ndarray:
    if event_index not in (LOWER_EVENT, CURRENT_EVENT, UPPER_EVENT):
        raise ValueError("event index must be 0, 1, or 2")
    state = canonical_stage9b_control_physical_state(continuation, control)
    return stage9_clock_reduction_operator("A", event_index) @ state


def stage9b_control_a_transition_support_matrix(
    continuation: QuantumContinuation,
    control: Stage9BControl,
    target_index: int,
    source_index: int,
) -> np.ndarray:
    support = spectator_support_basis("A")
    transition = (
        stage9_clock_reduction_operator("A", target_index)
        @ stage9b_control_a_reconstruction_operator(
            continuation, control, source_index
        )
    )
    return support.conj().T @ transition @ support


def stage9b_event_target_joint_distribution(
    continuation: QuantumContinuation,
    control: Stage9BControl,
    event_index: int,
) -> np.ndarray:
    if event_index not in (LOWER_EVENT, UPPER_EVENT):
        raise ValueError("Stage 9B compares only lower e0 and upper e2")

    if control == "balanced":
        forward = stage9b_event_target_joint_distribution(
            continuation, "forward", event_index
        )
        reversed_joint = stage9b_event_target_joint_distribution(
            continuation, "reversed", event_index
        )
        return 0.5 * (forward + reversed_joint)

    current = reduced_stage9b_control_state(continuation, control, CURRENT_EVENT)
    support = spectator_support_basis("A")
    current_coordinates = support.conj().T @ current
    transition = stage9b_control_a_transition_support_matrix(
        continuation, control, CURRENT_EVENT, event_index
    )
    target_at_event = _target_support_projector()
    target_at_current = transition @ target_at_event @ transition.conj().T
    return _joint_from_current_coordinates(current_coordinates, target_at_current)


def assess_stage9b_control_direction(
    continuation: QuantumContinuation,
    control: Stage9BControl,
    *,
    tolerance: float = 1e-10,
) -> Stage9BControlAssessment:
    lower_joint = stage9b_event_target_joint_distribution(
        continuation, control, LOWER_EVENT
    )
    upper_joint = stage9b_event_target_joint_distribution(
        continuation, control, UPPER_EVENT
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
    return Stage9BControlAssessment(
        continuation_id=continuation.continuation_id,
        control=control,
        lower_information=lower_information,
        upper_information=upper_information,
        lower_accuracy=lower_accuracy,
        upper_accuracy=upper_accuracy,
        record_score=record_score,
        accessibility_score=accessibility_score,
        orientation=orientation,
        record_defined=bool(orientation != "none"),
        branch_weight_used=False,
        v_extension_nontrivial=stage9b_control_retains_nontrivial_v(control),
    )


def _unitarity_residual(operator: np.ndarray) -> float:
    identity = np.eye(operator.shape[0], dtype=np.complex128)
    return float(np.linalg.norm(operator.conj().T @ operator - identity))


def assess_stage9b_control_admissibility(
    continuation: QuantumContinuation,
    control: Stage9BControl,
    *,
    atol: float = DEFAULT_ATOL,
) -> Stage9BControlAdmissibility:
    if control == "balanced":
        raise ValueError("balanced admissibility is inherited from its pure components")

    schedule = stage9b_control_schedule_rest_operators(continuation, control)
    schedule_residual = max(_unitarity_residual(operator) for operator in schedule)
    dressing = stage9b_control_dressing_operator(continuation, control)
    dressing_residual = _unitarity_residual(dressing)
    constraint = stage9b_control_constraint_operator(continuation, control)
    hermiticity_residual = float(np.linalg.norm(constraint - constraint.conj().T))
    physical = stage9b_control_physical_basis(continuation, control)
    physical_constraint_residual = float(np.linalg.norm(constraint @ physical))
    minimum_rank = min(
        np.linalg.matrix_rank(
            stage9b_control_clock_reduction_matrix(
                continuation, control, clock, index
            ),
            tol=atol,
        )
        for clock in SUBSYSTEMS
        for index in (0, 1, 2)
    )
    dimension = physical.shape[1]
    valid = bool(
        schedule_residual <= atol
        and dressing_residual <= atol
        and hermiticity_residual <= atol
        and physical_constraint_residual <= 10 * atol
        and dimension == 14
        and minimum_rank == 14
    )
    return Stage9BControlAdmissibility(
        continuation_id=continuation.continuation_id,
        control=control,
        valid_constrained_carrier=valid,
        schedule_unitarity_residual=schedule_residual,
        dressing_unitarity_residual=dressing_residual,
        constraint_hermiticity_residual=hermiticity_residual,
        physical_constraint_residual=physical_constraint_residual,
        physical_dimension=dimension,
        minimum_clock_reduction_rank=minimum_rank,
    )


def stage9b_common_reversal_is_interaction_reversal(
    *,
    atol: float = DEFAULT_ATOL,
) -> bool:
    """Audit the common arrow skeleton using the identity continuation.

    For h_L, the forward schedule is (I,R,SR) and the reversed schedule is
    (SR,R,I), so this checks an actual modeled interaction-history reversal
    rather than a diagnostic sign flip or reversed Python iteration.
    """

    left = canonical_continuation_left()
    forward = stage9b_control_schedule_rest_operators(left, "forward")
    reversed_schedule = stage9b_control_schedule_rest_operators(left, "reversed")
    return bool(
        all(
            np.linalg.norm(reversed_schedule[index] - forward[2 - index]) <= atol
            for index in (0, 1, 2)
        )
    )


def stage9b_control_retains_nontrivial_v(
    control: Stage9BControl,
    *,
    atol: float = DEFAULT_ATOL,
) -> bool:
    left = canonical_continuation_left()
    right = canonical_continuation_right()

    if control == "balanced":
        return bool(
            stage9b_control_retains_nontrivial_v("forward", atol=atol)
            and stage9b_control_retains_nontrivial_v("reversed", atol=atol)
        )

    left_upper = stage9b_control_schedule_rest_operators(left, control)[UPPER_EVENT]
    right_upper = stage9b_control_schedule_rest_operators(right, control)[UPPER_EVENT]
    return bool(np.linalg.norm(left_upper - right_upper) > atol)


def stage9b_control_diagnostics() -> Stage9BControlDiagnostics:
    continuations = (
        canonical_continuation_left(),
        canonical_continuation_right(),
    )
    assessments = {
        control: tuple(
            assess_stage9b_control_direction(continuation, control)
            for continuation in continuations
        )
        for control in ALL_CONTROLS
    }

    forward = assessments["forward"]
    reversed_items = assessments["reversed"]
    balanced = assessments["balanced"]
    no_record = assessments["no-record"]

    admissibility = tuple(
        assess_stage9b_control_admissibility(continuation, control)
        for continuation in continuations
        for control in PURE_CONTROLS
    )

    reversal_record_residual = max(
        abs(f.record_score + r.record_score)
        for f, r in zip(forward, reversed_items)
    )
    reversal_accessibility_residual = max(
        abs(f.accessibility_score + r.accessibility_score)
        for f, r in zip(forward, reversed_items)
    )

    return Stage9BControlDiagnostics(
        forward_scores=tuple((item.continuation_id, item.record_score) for item in forward),
        reversed_scores=tuple((item.continuation_id, item.record_score) for item in reversed_items),
        balanced_scores=tuple((item.continuation_id, item.record_score) for item in balanced),
        no_record_scores=tuple((item.continuation_id, item.record_score) for item in no_record),
        forward_accessibility_scores=tuple(
            (item.continuation_id, item.accessibility_score) for item in forward
        ),
        reversed_accessibility_scores=tuple(
            (item.continuation_id, item.accessibility_score) for item in reversed_items
        ),
        balanced_accessibility_scores=tuple(
            (item.continuation_id, item.accessibility_score) for item in balanced
        ),
        no_record_accessibility_scores=tuple(
            (item.continuation_id, item.accessibility_score) for item in no_record
        ),
        reversal_record_residual=float(reversal_record_residual),
        reversal_accessibility_residual=float(reversal_accessibility_residual),
        balanced_record_residual=float(max(abs(item.record_score) for item in balanced)),
        balanced_accessibility_residual=float(
            max(abs(item.accessibility_score) for item in balanced)
        ),
        no_record_record_residual=float(max(abs(item.record_score) for item in no_record)),
        no_record_accessibility_residual=float(
            max(abs(item.accessibility_score) for item in no_record)
        ),
        common_reversal_is_interaction_reversal=stage9b_common_reversal_is_interaction_reversal(),
        all_controls_retain_nontrivial_v=all(
            stage9b_control_retains_nontrivial_v(control) for control in ALL_CONTROLS
        ),
        all_pure_controls_valid_constrained_carriers=all(
            item.valid_constrained_carrier for item in admissibility
        ),
        minimum_clock_reduction_rank=min(
            item.minimum_clock_reduction_rank for item in admissibility
        ),
        maximum_constraint_residual=max(
            item.physical_constraint_residual for item in admissibility
        ),
    )


def stage9b_summary() -> dict[str, object]:
    diagnostics = stage9b_control_diagnostics()
    return {
        "current_anchor": "e1",
        "controls": ALL_CONTROLS,
        "diagnostics": asdict(diagnostics),
        "control_semantics": {
            "forward": "Stage 9A common record then scramble skeleton",
            "reversed": "modeled interaction reversal of common R-direction skeleton; V branch retained at e2",
            "balanced": "equal mixture of forward and reversed constrained histories",
            "no-record": "record write neutralized; scrambler and V branch retained",
        },
        "guards": (
            "reversed diagnostic sign != reversed Python iteration",
            "balanced mixture != pure constrained history",
            "directional record arrow != ontological future openness",
            "directional record arrow != ontological becoming",
            "control of R_direction != control of V_semantics",
            "continuation identity != record-direction identity",
            "Potentiality != quantum randomness by definition",
        ),
    }
