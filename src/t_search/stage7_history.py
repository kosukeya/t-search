"""Stage 7C relationally anchored record formation and orientation controls.

Stage 7B produced a reversible target-specific record write on one support, but
it did not locate that write at an internally modeled event.  Stage 7C embeds a
three-event schedule directly into a modified constrained model.

For the canonical qutrit A-clock history, define three cumulative rest-memory
unitaries V_j attached to the orthogonal A-clock reading projectors |t_j><t_j|:

forward:
    V_0 = I
    V_1 = U_rec
    V_2 = U_scr U_rec

reversed control:
    V_0 = U_scr U_rec
    V_1 = U_rec
    V_2 = I

no-record control:
    V_0 = I
    V_1 = I
    V_2 = U_scr

The global clock-conditioned dressing is

    W = sum_j |t_j><t_j|_A tensor V_j

and the corresponding modified constraint is

    H_hist = W H_0 W^dagger.

Thus the event anchor is part of the constrained model itself rather than the
order in which Python applies matrices.  Because H_hist is a modified
constraint, the physical basis and A-clock reductions/reconstructions are
re-derived below from H_hist; inherited Stage 5/7A maps are not silently reused
as interacting maps.

The construction is deliberately a finite unitary-equivalent pressure-test
family.  It is not claimed to be a unique autonomous interaction Hamiltonian,
a thermodynamic arrow, or fundamental time reversal.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

import numpy as np

from .stage3_asymmetry import orientation_from_scores
from .stage5_clock_change import (
    DEFAULT_ATOL,
    DEFAULT_DIMENSION,
    DEFAULT_RATES,
    clock_state,
)
from .stage5_reductions import clock_relative_support_pairs
from .stage7_record import (
    CANONICAL_CLOCK,
    canonical_target_pair_projector,
    controlled_record_write_ambient_operator,
)
from .stage7_spectator import (
    MEMORY_DIMENSION,
    memory_identity,
    spectator_kinematic_clock_projection_operator,
    spectator_physical_basis,
    spectator_support_basis,
    spectator_support_projector,
    spectator_total_constraint_operator,
)

HistoryKind = Literal["forward", "reversed", "no-record"]

CURRENT_EVENT = 1
LOWER_EVENT = 0
UPPER_EVENT = 2
_REQUIRED_SOURCE_PAIRS = ((-1, 0), (-1, 1), (0, 0), (0, 1))


@dataclass(frozen=True)
class RelationalHistoryModel:
    kind: HistoryKind
    event_labels: tuple[str, str, str]
    orientation_convention: str
    interaction_anchor: str


@dataclass(frozen=True)
class RelationalRecordAssessment:
    kind: str
    lower_information: float
    upper_information: float
    lower_accuracy: float
    upper_accuracy: float
    record_score: float
    accessibility_score: float
    orientation: str
    record_defined: bool
    directional_score_defined: bool
    internally_anchored: bool
    constraint_residual: float
    lower_joint: tuple[tuple[float, float], tuple[float, float]]
    upper_joint: tuple[tuple[float, float], tuple[float, float]]


@dataclass(frozen=True)
class Stage7CControls:
    forward: RelationalRecordAssessment
    reversed: RelationalRecordAssessment
    balanced_record_score: float
    balanced_accessibility_score: float
    balanced_lower_information: float
    balanced_upper_information: float
    no_record: RelationalRecordAssessment
    uncertain_memory: RelationalRecordAssessment
    forward_reverse_sign_reversal: bool
    balanced_cancels: bool
    no_record_cancels: bool
    uncertain_memory_cancels: bool


def canonical_history_model(kind: HistoryKind = "forward") -> RelationalHistoryModel:
    if kind not in ("forward", "reversed", "no-record"):
        raise ValueError("history kind must be forward, reversed, or no-record")
    return RelationalHistoryModel(
        kind=kind,
        event_labels=("e0", "e1", "e2"),
        orientation_convention="lower-minus-upper around current event e1",
        interaction_anchor="orthogonal A-clock reading projectors inside W and H_hist",
    )


def pair_scrambler_support_matrix() -> np.ndarray:
    """Reversible nuisance-controlled target scrambler X -> X XOR N.

    On the canonical four-pair source subspace, X=1 iff B=-1 and N=1 iff
    C=+1.  Therefore only the N=1 sector is flipped:

        (-1,+1) <-> (0,+1)

    while the N=0 pairs (-1,0) and (0,0) remain fixed.  This makes the final
    target bit X XOR N independent of the original X for the balanced source.
    The remaining support pairs are also left unchanged.
    """

    pairs = clock_relative_support_pairs(CANONICAL_CLOCK)
    permutation = np.eye(len(pairs), dtype=np.complex128)
    first, second = (-1, 1), (0, 1)
    i = pairs.index(first)
    j = pairs.index(second)
    permutation[i, i] = 0.0
    permutation[j, j] = 0.0
    permutation[i, j] = 1.0
    permutation[j, i] = 1.0
    return np.kron(permutation, memory_identity())


def pair_scrambler_ambient_operator() -> np.ndarray:
    support = spectator_support_basis(CANONICAL_CLOCK)
    projector = spectator_support_projector(CANONICAL_CLOCK)
    u_support = pair_scrambler_support_matrix()
    identity = np.eye(projector.shape[0], dtype=np.complex128)
    return support @ u_support @ support.conj().T + (identity - projector)


def schedule_rest_operators(kind: HistoryKind) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    model = canonical_history_model(kind)
    identity = np.eye(18, dtype=np.complex128)
    record = controlled_record_write_ambient_operator()
    scramble = pair_scrambler_ambient_operator()
    if model.kind == "forward":
        return identity, record, scramble @ record
    if model.kind == "reversed":
        return scramble @ record, record, identity
    return identity, identity, scramble


def clock_reading_projector(index: int) -> np.ndarray:
    if index not in (0, 1, 2):
        raise ValueError("Stage 7C clock index must be 0, 1, or 2")
    ket = clock_state(index, 3, rate=1.0)
    return np.outer(ket, ket.conj())


def history_dressing_operator(kind: HistoryKind = "forward") -> np.ndarray:
    """Return W=sum_j |t_j><t_j|_A tensor V_j on A tensor (B,C,M)."""

    operators = schedule_rest_operators(kind)
    dressing = np.zeros((54, 54), dtype=np.complex128)
    for index, rest_operator in enumerate(operators):
        dressing += np.kron(clock_reading_projector(index), rest_operator)
    return dressing


def history_constraint_operator(kind: HistoryKind = "forward") -> np.ndarray:
    """Return the internally anchored modified constraint H_hist=W H_0 W^dagger."""

    dressing = history_dressing_operator(kind)
    baseline = spectator_total_constraint_operator()
    return dressing @ baseline @ dressing.conj().T


def history_physical_basis(kind: HistoryKind = "forward") -> np.ndarray:
    dressing = history_dressing_operator(kind)
    return dressing @ spectator_physical_basis()


def history_physical_projector(kind: HistoryKind = "forward") -> np.ndarray:
    basis = history_physical_basis(kind)
    return basis @ basis.conj().T


def history_constraint_residual(state: np.ndarray, kind: HistoryKind = "forward") -> float:
    vector = np.asarray(state, dtype=np.complex128)
    if vector.shape != (54,):
        raise ValueError("Stage 7C physical state must have shape (54,)")
    return float(np.linalg.norm(history_constraint_operator(kind) @ vector))


def history_reduction_operator(index: int) -> np.ndarray:
    """Kinematic A-clock reduction map; physical validity is schedule-specific."""

    if index not in (0, 1, 2):
        raise ValueError("Stage 7C clock index must be 0, 1, or 2")
    return np.sqrt(3.0) * spectator_kinematic_clock_projection_operator(
        CANONICAL_CLOCK, index
    )


def history_reduction_coordinates(kind: HistoryKind, index: int) -> np.ndarray:
    """Re-derive R_A^hist(j) in fixed A-rest support coordinates."""

    support = spectator_support_basis(CANONICAL_CLOCK)
    physical = history_physical_basis(kind)
    return support.conj().T @ history_reduction_operator(index) @ physical


def history_reconstruction_operator(kind: HistoryKind, index: int) -> np.ndarray:
    """Re-derive E_A^hist(j) from the modified physical basis and reduction."""

    support = spectator_support_basis(CANONICAL_CLOCK)
    physical = history_physical_basis(kind)
    coordinates = history_reduction_coordinates(kind, index)
    return physical @ coordinates.conj().T @ support.conj().T


def history_transition_support_matrix(
    kind: HistoryKind,
    target_index: int,
    source_index: int,
) -> np.ndarray:
    """Return the re-derived same-A-clock relational transition on support coords."""

    support = spectator_support_basis(CANONICAL_CLOCK)
    transition = (
        history_reduction_operator(target_index)
        @ history_reconstruction_operator(kind, source_index)
    )
    return support.conj().T @ transition @ support


def canonical_source_support_coordinates(memory_bit: int = 0) -> np.ndarray:
    if memory_bit not in (0, 1):
        raise ValueError("memory bit must be 0 or 1")
    pairs = clock_relative_support_pairs(CANONICAL_CLOCK)
    coordinates = np.zeros((len(pairs), MEMORY_DIMENSION), dtype=np.complex128)
    amplitude = 1.0 / np.sqrt(len(_REQUIRED_SOURCE_PAIRS))
    for pair in _REQUIRED_SOURCE_PAIRS:
        coordinates[pairs.index(pair), memory_bit] = amplitude
    return coordinates.reshape(-1)


def canonical_source_support_state(memory_bit: int = 0) -> np.ndarray:
    return spectator_support_basis(CANONICAL_CLOCK) @ canonical_source_support_coordinates(memory_bit)


def canonical_physical_history_state(kind: HistoryKind = "forward", *, memory_bit: int = 0) -> np.ndarray:
    """Construct one valid physical history state from its declared event-0 boundary.

    The reversed control starts from the *forward final event state*, then evolves
    under the explicitly reversed cumulative schedule.  This is a modeled
    reversed construction, not a sign relabeling of the forward diagnostic.
    """

    if kind == "reversed":
        forward_state = canonical_physical_history_state("forward", memory_bit=memory_bit)
        forward_final = history_reduction_operator(UPPER_EVENT) @ forward_state
        return history_reconstruction_operator("reversed", LOWER_EVENT) @ forward_final
    source = canonical_source_support_state(memory_bit)
    return history_reconstruction_operator(kind, LOWER_EVENT) @ source


def reduced_history_state(
    state: np.ndarray,
    kind: HistoryKind,
    index: int,
    *,
    atol: float = DEFAULT_ATOL,
) -> np.ndarray:
    vector = np.asarray(state, dtype=np.complex128)
    if history_constraint_residual(vector, kind) > atol:
        raise ValueError("state must satisfy the declared Stage 7C modified constraint")
    return history_reduction_operator(index) @ vector


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
                float(np.linalg.norm(target_projector @ memory_projector - memory_projector @ target_projector)),
            )
            probability = np.vdot(
                current_coordinates,
                target_projector @ memory_projector @ current_coordinates,
            ).real
            joint[target_bit, memory_bit] = float(probability)
    if commutator_max > DEFAULT_ATOL:
        raise ValueError("declared target and memory readouts must commute in Stage 7C")
    total = float(np.sum(joint))
    if total <= 0.0:
        raise ValueError("joint distribution has zero total probability")
    return joint / total


def _mutual_information(joint: np.ndarray) -> float:
    probabilities = np.asarray(joint, dtype=float)
    px = np.sum(probabilities, axis=1, keepdims=True)
    pm = np.sum(probabilities, axis=0, keepdims=True)
    independent = px @ pm
    mask = probabilities > 0.0
    return float(np.sum(probabilities[mask] * np.log2(probabilities[mask] / independent[mask])))


def _decoder_accuracy(joint: np.ndarray) -> float:
    """Bayes-optimal target-bit accuracy from the memory bit."""

    return float(sum(np.max(joint[:, memory_bit]) for memory_bit in (0, 1)))


def event_target_joint_distribution(
    state: np.ndarray,
    kind: HistoryKind,
    event_index: int,
) -> np.ndarray:
    if event_index not in (LOWER_EVENT, UPPER_EVENT):
        raise ValueError("Stage 7C compares only lower event e0 and upper event e2")
    current = reduced_history_state(state, kind, CURRENT_EVENT)
    support = spectator_support_basis(CANONICAL_CLOCK)
    current_coordinates = support.conj().T @ current
    transition = history_transition_support_matrix(kind, CURRENT_EVENT, event_index)
    target_at_event = _target_support_projector()
    target_at_current = transition @ target_at_event @ transition.conj().T
    return _joint_from_current_coordinates(current_coordinates, target_at_current)


def assess_relational_record(
    kind: HistoryKind,
    *,
    state: np.ndarray | None = None,
    tolerance: float = 1e-10,
) -> RelationalRecordAssessment:
    model = canonical_history_model(kind)
    physical = canonical_physical_history_state(kind) if state is None else np.asarray(state, dtype=np.complex128)
    lower_joint = event_target_joint_distribution(physical, kind, LOWER_EVENT)
    upper_joint = event_target_joint_distribution(physical, kind, UPPER_EVENT)
    lower_information = _mutual_information(lower_joint)
    upper_information = _mutual_information(upper_joint)
    lower_accuracy = _decoder_accuracy(lower_joint)
    upper_accuracy = _decoder_accuracy(upper_joint)
    record_score = lower_information - upper_information
    accessibility_score = lower_accuracy - upper_accuracy
    orientation = orientation_from_scores(record_score, accessibility_score, tolerance=tolerance)
    selected_information = (
        lower_information
        if orientation == "lower-index"
        else upper_information if orientation == "upper-index" else 0.0
    )
    return RelationalRecordAssessment(
        kind=model.kind,
        lower_information=lower_information,
        upper_information=upper_information,
        lower_accuracy=lower_accuracy,
        upper_accuracy=upper_accuracy,
        record_score=record_score,
        accessibility_score=accessibility_score,
        orientation=orientation,
        record_defined=bool(orientation != "none" and selected_information > tolerance),
        directional_score_defined=True,
        internally_anchored=True,
        constraint_residual=history_constraint_residual(physical, kind),
        lower_joint=tuple(tuple(float(value) for value in row) for row in lower_joint),  # type: ignore[arg-type]
        upper_joint=tuple(tuple(float(value) for value in row) for row in upper_joint),  # type: ignore[arg-type]
    )


def _assessment_from_mixed_joints(
    kind: str,
    lower_joint: np.ndarray,
    upper_joint: np.ndarray,
    *,
    internally_anchored: bool,
    tolerance: float = 1e-10,
) -> RelationalRecordAssessment:
    lower_information = _mutual_information(lower_joint)
    upper_information = _mutual_information(upper_joint)
    lower_accuracy = _decoder_accuracy(lower_joint)
    upper_accuracy = _decoder_accuracy(upper_joint)
    record_score = lower_information - upper_information
    accessibility_score = lower_accuracy - upper_accuracy
    orientation = orientation_from_scores(record_score, accessibility_score, tolerance=tolerance)
    selected_information = (
        lower_information
        if orientation == "lower-index"
        else upper_information if orientation == "upper-index" else 0.0
    )
    return RelationalRecordAssessment(
        kind=kind,
        lower_information=lower_information,
        upper_information=upper_information,
        lower_accuracy=lower_accuracy,
        upper_accuracy=upper_accuracy,
        record_score=record_score,
        accessibility_score=accessibility_score,
        orientation=orientation,
        record_defined=bool(orientation != "none" and selected_information > tolerance),
        directional_score_defined=True,
        internally_anchored=internally_anchored,
        constraint_residual=0.0,
        lower_joint=tuple(tuple(float(value) for value in row) for row in lower_joint),  # type: ignore[arg-type]
        upper_joint=tuple(tuple(float(value) for value in row) for row in upper_joint),  # type: ignore[arg-type]
    )


def uncertain_memory_control_assessment() -> RelationalRecordAssessment:
    """Maximally mixed memory boundary, represented as a 50/50 physical mixture."""

    lower = np.zeros((2, 2), dtype=float)
    upper = np.zeros((2, 2), dtype=float)
    for memory_bit in (0, 1):
        physical = canonical_physical_history_state("forward", memory_bit=memory_bit)
        lower += 0.5 * event_target_joint_distribution(physical, "forward", LOWER_EVENT)
        upper += 0.5 * event_target_joint_distribution(physical, "forward", UPPER_EVENT)
    return _assessment_from_mixed_joints(
        "uncertain-memory", lower, upper, internally_anchored=True
    )


def balanced_forward_reverse_assessment() -> RelationalRecordAssessment:
    """Equal meta-ensemble of the explicit forward and reversed constrained histories."""

    forward_state = canonical_physical_history_state("forward")
    reversed_state = canonical_physical_history_state("reversed")
    lower = 0.5 * event_target_joint_distribution(forward_state, "forward", LOWER_EVENT)
    lower += 0.5 * event_target_joint_distribution(reversed_state, "reversed", LOWER_EVENT)
    upper = 0.5 * event_target_joint_distribution(forward_state, "forward", UPPER_EVENT)
    upper += 0.5 * event_target_joint_distribution(reversed_state, "reversed", UPPER_EVENT)
    return _assessment_from_mixed_joints(
        "balanced-forward-reverse", lower, upper, internally_anchored=True
    )


def stage7c_constraint_diagnostics(kind: HistoryKind = "forward") -> dict[str, float | int | bool]:
    dressing = history_dressing_operator(kind)
    constraint = history_constraint_operator(kind)
    basis = history_physical_basis(kind)
    eigenvalues, eigenvectors = np.linalg.eigh(constraint)
    kernel = eigenvectors[:, np.abs(eigenvalues) <= DEFAULT_ATOL]
    numerical_projector = kernel @ kernel.conj().T
    analytic_projector = basis @ basis.conj().T
    reduction_residual = 0.0
    roundtrip_residual = 0.0
    support = spectator_support_projector(CANONICAL_CLOCK)
    for index in (0, 1, 2):
        coordinates = history_reduction_coordinates(kind, index)
        reduction_residual = max(
            reduction_residual,
            float(np.linalg.norm(coordinates.conj().T @ coordinates - np.eye(14))),
        )
        reduction = history_reduction_operator(index)
        reconstruction = history_reconstruction_operator(kind, index)
        roundtrip_residual = max(
            roundtrip_residual,
            float(np.linalg.norm(reduction @ reconstruction - support)),
            float(np.linalg.norm(reconstruction @ reduction @ analytic_projector - analytic_projector)),
        )
    return {
        "kinematic_dimension": 54,
        "physical_dimension": basis.shape[1],
        "dressing_unitarity_residual": float(
            np.linalg.norm(dressing.conj().T @ dressing - np.eye(54))
        ),
        "constraint_hermiticity_residual": float(np.linalg.norm(constraint - constraint.conj().T)),
        "physical_kernel_residual": float(np.linalg.norm(constraint @ basis)),
        "analytic_numerical_projector_residual": float(np.linalg.norm(analytic_projector - numerical_projector)),
        "rederived_reduction_isometry_residual": reduction_residual,
        "rederived_roundtrip_residual": roundtrip_residual,
        "modified_constraint_differs_from_spectator": bool(
            np.linalg.norm(constraint - spectator_total_constraint_operator()) > DEFAULT_ATOL
        ),
    }


def stage7c_control_assessments() -> Stage7CControls:
    forward = assess_relational_record("forward")
    reversed_assessment = assess_relational_record("reversed")
    balanced = balanced_forward_reverse_assessment()
    no_record = assess_relational_record("no-record")
    uncertain = uncertain_memory_control_assessment()
    tolerance = 1e-10
    return Stage7CControls(
        forward=forward,
        reversed=reversed_assessment,
        balanced_record_score=balanced.record_score,
        balanced_accessibility_score=balanced.accessibility_score,
        balanced_lower_information=balanced.lower_information,
        balanced_upper_information=balanced.upper_information,
        no_record=no_record,
        uncertain_memory=uncertain,
        forward_reverse_sign_reversal=bool(
            forward.record_defined
            and reversed_assessment.record_defined
            and forward.record_score > tolerance
            and reversed_assessment.record_score < -tolerance
            and abs(forward.record_score + reversed_assessment.record_score) <= tolerance
            and abs(forward.accessibility_score + reversed_assessment.accessibility_score) <= tolerance
        ),
        balanced_cancels=bool(
            abs(balanced.record_score) <= tolerance
            and abs(balanced.accessibility_score) <= tolerance
        ),
        no_record_cancels=bool(
            not no_record.record_defined
            and abs(no_record.record_score) <= tolerance
            and abs(no_record.accessibility_score) <= tolerance
        ),
        uncertain_memory_cancels=bool(
            not uncertain.record_defined
            and abs(uncertain.record_score) <= tolerance
            and abs(uncertain.accessibility_score) <= tolerance
        ),
    )


def stage7c_summary() -> dict[str, object]:
    controls = stage7c_control_assessments()
    return {
        "constraint": stage7c_constraint_diagnostics("forward"),
        "controls": asdict(controls),
        "event_order": ["e0", "e1", "e2"],
        "current_event": "e1",
        "record_score": "A_R=I(M_e1;Q_e0)-I(M_e1;Q_e2)",
        "accessibility_score": "A_acc=Acc(Q_e0|M_e1)-Acc(Q_e2|M_e1)",
        "guards": [
            "simulation/intervention order != modeled temporal order",
            "clock-conditioned conjugated constraint != unique autonomous interaction Hamiltonian",
            "modeled history reversal != fundamental time-reversal symmetry",
            "record-defined orientation != thermodynamic arrow",
            "record-defined orientation != ontological becoming",
            "record-defined orientation != phenomenal passage",
        ],
    }
