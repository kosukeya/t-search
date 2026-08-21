"""Stage 8A common quantum-extension substrate.

Stage 8.0 requires QExt(D) to contain executable quantum continuations rather
than branch labels.  This module constructs the smallest canonical family on
the Stage 7 constrained carrier.

The declared current anchor is e1.  Both canonical continuations share

    V_0 = I
    V_1 = U_rec

and therefore have the same A-clock current actuality through e1.  They differ
only at e2:

    h_L: V_2 = U_rec
    h_R: V_2 = Z_C U_rec

where Z_C is a reversible phase on the C=+1 sector of the A-clock rest support
and acts as identity on memory.  Z_C also commutes with the Stage 7 record
target projector (a B-energy predicate), so the baseline future distinction is
not definitionally a memory-record difference.

Each schedule defines a global clock-conditioned dressing W_h and a modified
constraint H_h = W_h H_0 W_h^dagger.  Physical bases and clock reductions are
therefore derived from the continuation-specific constrained construction.

This is a finite executable extension substrate.  It is not a claim that the
represented alternatives are ontically real futures.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable, Literal, Sequence

import numpy as np

from .stage5_clock_change import DEFAULT_ATOL, SUBSYSTEMS
from .stage5_reductions import clock_relative_support_pairs
from .stage7_history import (
    CURRENT_EVENT,
    LOWER_EVENT,
    UPPER_EVENT,
    canonical_source_support_state,
    clock_reading_projector,
)
from .stage7_record import (
    canonical_target_pair_projector,
    controlled_record_write_ambient_operator,
    target_memory_mutual_information,
)
from .stage7_spectator import (
    MEMORY_DIMENSION,
    memory_identity,
    spectator_kinematic_clock_projection_operator,
    spectator_physical_basis,
    spectator_support_basis,
    spectator_total_constraint_operator,
)

FutureAction = Literal["identity", "c-phase"]
CurrentAction = Literal["record", "identity"]

CANONICAL_ANCHOR = CURRENT_EVENT
TERMINAL_EVENT = UPPER_EVENT


@dataclass(frozen=True)
class QuantumContinuation:
    continuation_id: str
    future_action: FutureAction
    current_action: CurrentAction = "record"
    current_anchor: int = CANONICAL_ANCHOR


@dataclass(frozen=True)
class ContinuationAdmissibility:
    continuation_id: str
    admissible: bool
    current_prefix_compatible: bool
    schedule_unitarity_residual: float
    dressing_unitarity_residual: float
    constraint_hermiticity_residual: float
    physical_constraint_residual: float
    physical_dimension: int
    minimum_clock_reduction_rank: int
    memory_neutral_future: bool
    record_target_neutral_future: bool


@dataclass(frozen=True)
class Stage8ASubstrateDiagnostics:
    qext_size: int
    physical_continuations: tuple[str, ...]
    common_e0_state_residual: float
    common_e1_state_residual: float
    common_current_record_information_residual: float
    current_record_information: float
    future_state_overlap_squared: float
    future_state_distance: float
    future_probe_expectation_left: float
    future_probe_expectation_right: float
    future_probe_difference: float
    future_operator_residual: float
    renamed_equivalent: bool
    deduplicated_size_with_rename: int
    minimum_clock_reduction_rank: int
    maximum_constraint_residual: float
    memory_neutral_future: bool
    record_target_neutral_future: bool
    invalid_current_prefix_rejected: bool
    terminal_qext_size: int
    physically_inequivalent: bool


def canonical_continuation_left() -> QuantumContinuation:
    return QuantumContinuation("h_L", "identity")


def canonical_continuation_right() -> QuantumContinuation:
    return QuantumContinuation("h_R", "c-phase")


def renamed_continuation(
    continuation: QuantumContinuation,
    new_id: str,
) -> QuantumContinuation:
    return QuantumContinuation(
        continuation_id=new_id,
        future_action=continuation.future_action,
        current_action=continuation.current_action,
        current_anchor=continuation.current_anchor,
    )


def _ambient_identity() -> np.ndarray:
    return np.eye(18, dtype=np.complex128)


def _memory_z_ambient() -> np.ndarray:
    pairs = clock_relative_support_pairs("A")
    pair_identity = np.eye(len(pairs), dtype=np.complex128)
    memory_z = np.diag([1.0, -1.0]).astype(np.complex128)
    support = spectator_support_basis("A")
    support_op = np.kron(pair_identity, memory_z)
    support_projector = support @ support.conj().T
    identity = _ambient_identity()
    return support @ support_op @ support.conj().T + (identity - support_projector)


def future_pair_phase_support_matrix() -> np.ndarray:
    """Return Z_C on pair support, tensored with identity on memory.

    The pair phase is -1 iff the second A-clock rest subsystem C has energy
    label +1 and +1 otherwise.  It changes future pair coherence without
    touching memory or the B-based record-target truth value.
    """

    pairs = clock_relative_support_pairs("A")
    phases = np.array([-1.0 if pair[1] == 1 else 1.0 for pair in pairs])
    return np.kron(np.diag(phases).astype(np.complex128), memory_identity())


def future_pair_phase_ambient_operator() -> np.ndarray:
    support = spectator_support_basis("A")
    projector = support @ support.conj().T
    phase = future_pair_phase_support_matrix()
    identity = _ambient_identity()
    return support @ phase @ support.conj().T + (identity - projector)


def future_pair_coherence_probe_support_matrix() -> np.ndarray:
    """Hermitian pair-only probe exchanging C=0 and C=+1 at fixed B.

    The probe is deliberately identity on memory.  It is used only as a
    physical inequivalence diagnostic for the canonical continuation pair.
    """

    pairs = clock_relative_support_pairs("A")
    pair_probe = np.zeros((len(pairs), len(pairs)), dtype=np.complex128)
    for b_label in (-1, 0):
        first = (b_label, 0)
        second = (b_label, 1)
        if first in pairs and second in pairs:
            i = pairs.index(first)
            j = pairs.index(second)
            pair_probe[i, j] = 1.0
            pair_probe[j, i] = 1.0
    return np.kron(pair_probe, memory_identity())


def continuation_future_operator(continuation: QuantumContinuation) -> np.ndarray:
    if continuation.future_action == "identity":
        return _ambient_identity()
    if continuation.future_action == "c-phase":
        return future_pair_phase_ambient_operator()
    raise ValueError("unknown Stage 8A future action")


def continuation_schedule_rest_operators(
    continuation: QuantumContinuation,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    identity = _ambient_identity()
    record = controlled_record_write_ambient_operator()
    current = record if continuation.current_action == "record" else identity
    future = continuation_future_operator(continuation) @ current
    return identity, current, future


def continuation_dressing_operator(continuation: QuantumContinuation) -> np.ndarray:
    dressing = np.zeros((54, 54), dtype=np.complex128)
    for index, rest_operator in enumerate(continuation_schedule_rest_operators(continuation)):
        dressing += np.kron(clock_reading_projector(index), rest_operator)
    return dressing


def continuation_constraint_operator(continuation: QuantumContinuation) -> np.ndarray:
    dressing = continuation_dressing_operator(continuation)
    baseline = spectator_total_constraint_operator()
    return dressing @ baseline @ dressing.conj().T


def continuation_physical_basis(continuation: QuantumContinuation) -> np.ndarray:
    return continuation_dressing_operator(continuation) @ spectator_physical_basis()


def continuation_clock_reduction_operator(clock: str, index: int) -> np.ndarray:
    if clock not in SUBSYSTEMS:
        raise ValueError("clock must be one of A, B, or C")
    if isinstance(index, bool) or not isinstance(index, int) or index not in (0, 1, 2):
        raise ValueError("clock index must be 0, 1, or 2")
    return np.sqrt(3.0) * spectator_kinematic_clock_projection_operator(clock, index)


def continuation_clock_reduction_matrix(
    continuation: QuantumContinuation,
    clock: str,
    index: int,
) -> np.ndarray:
    return continuation_clock_reduction_operator(clock, index) @ continuation_physical_basis(continuation)


def _clock_support_qr(
    continuation: QuantumContinuation,
    clock: str,
    index: int,
) -> tuple[np.ndarray, np.ndarray]:
    reduction = continuation_clock_reduction_matrix(continuation, clock, index)
    q, r = np.linalg.qr(reduction, mode="reduced")
    if np.linalg.matrix_rank(r, tol=DEFAULT_ATOL) != reduction.shape[1]:
        raise ValueError("continuation clock reading is not an injective perspective")
    return q, r


def continuation_clock_reconstruction_operator(
    continuation: QuantumContinuation,
    clock: str,
    index: int,
) -> np.ndarray:
    support, coordinates = _clock_support_qr(continuation, clock, index)
    physical = continuation_physical_basis(continuation)
    return physical @ np.linalg.inv(coordinates) @ support.conj().T


def canonical_continuation_physical_state(continuation: QuantumContinuation) -> np.ndarray:
    """Build the continuation history from the common event-e0 boundary state."""

    source = canonical_source_support_state()
    reconstruction = continuation_clock_reconstruction_operator(
        continuation, "A", LOWER_EVENT
    )
    state = reconstruction @ source
    norm = np.linalg.norm(state)
    if norm <= DEFAULT_ATOL:
        raise ValueError("continuation reconstruction produced zero physical state")
    return state / norm


def reduced_continuation_state(
    continuation: QuantumContinuation,
    event_index: int,
) -> np.ndarray:
    if event_index not in (LOWER_EVENT, CURRENT_EVENT, UPPER_EVENT):
        raise ValueError("event index must be 0, 1, or 2")
    state = canonical_continuation_physical_state(continuation)
    return continuation_clock_reduction_operator("A", event_index) @ state


def _support_coordinates(reduced_state: np.ndarray) -> np.ndarray:
    support = spectator_support_basis("A")
    return support.conj().T @ np.asarray(reduced_state, dtype=np.complex128)


def continuation_constraint_residual(continuation: QuantumContinuation) -> float:
    state = canonical_continuation_physical_state(continuation)
    return float(np.linalg.norm(continuation_constraint_operator(continuation) @ state))


def continuation_current_record_information(continuation: QuantumContinuation) -> float:
    current = reduced_continuation_state(continuation, CURRENT_EVENT)
    return target_memory_mutual_information(current)


def continuation_equivalent(
    left: QuantumContinuation,
    right: QuantumContinuation,
    *,
    atol: float = DEFAULT_ATOL,
) -> bool:
    if left.current_anchor != right.current_anchor:
        return False
    left_schedule = continuation_schedule_rest_operators(left)
    right_schedule = continuation_schedule_rest_operators(right)
    return all(
        np.linalg.norm(a - b) <= atol
        for a, b in zip(left_schedule, right_schedule, strict=True)
    )


def deduplicate_continuations(
    continuations: Sequence[QuantumContinuation],
    *,
    atol: float = DEFAULT_ATOL,
) -> tuple[QuantumContinuation, ...]:
    representatives: list[QuantumContinuation] = []
    for continuation in continuations:
        if not any(
            continuation_equivalent(continuation, existing, atol=atol)
            for existing in representatives
        ):
            representatives.append(continuation)
    return tuple(representatives)


def _memory_neutral(operator: np.ndarray, *, atol: float = DEFAULT_ATOL) -> bool:
    return bool(np.linalg.norm(operator @ _memory_z_ambient() - _memory_z_ambient() @ operator) <= atol)


def _record_target_ambient_projector() -> np.ndarray:
    support = spectator_support_basis("A")
    target_support = np.kron(canonical_target_pair_projector(), memory_identity())
    return support @ target_support @ support.conj().T


def _record_target_neutral(operator: np.ndarray, *, atol: float = DEFAULT_ATOL) -> bool:
    target = _record_target_ambient_projector()
    return bool(np.linalg.norm(operator @ target - target @ operator) <= atol)


def assess_continuation_admissibility(
    continuation: QuantumContinuation,
    *,
    atol: float = DEFAULT_ATOL,
) -> ContinuationAdmissibility:
    schedule = continuation_schedule_rest_operators(continuation)
    identity = _ambient_identity()
    record = controlled_record_write_ambient_operator()
    prefix_ok = bool(
        continuation.current_anchor == CANONICAL_ANCHOR
        and np.linalg.norm(schedule[0] - identity) <= atol
        and np.linalg.norm(schedule[1] - record) <= atol
    )
    schedule_unitarity = max(
        float(np.linalg.norm(op.conj().T @ op - identity)) for op in schedule
    )
    dressing = continuation_dressing_operator(continuation)
    dressing_unitarity = float(
        np.linalg.norm(dressing.conj().T @ dressing - np.eye(54, dtype=np.complex128))
    )
    constraint = continuation_constraint_operator(continuation)
    hermiticity = float(np.linalg.norm(constraint - constraint.conj().T))
    physical = continuation_physical_basis(continuation)
    physical_dimension = int(physical.shape[1])
    ranks = [
        int(np.linalg.matrix_rank(continuation_clock_reduction_matrix(continuation, clock, index), tol=atol))
        for clock in SUBSYSTEMS
        for index in (0, 1, 2)
    ]
    future = continuation_future_operator(continuation)
    try:
        residual = continuation_constraint_residual(continuation)
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
    return ContinuationAdmissibility(
        continuation_id=continuation.continuation_id,
        admissible=admissible,
        current_prefix_compatible=prefix_ok,
        schedule_unitarity_residual=schedule_unitarity,
        dressing_unitarity_residual=dressing_unitarity,
        constraint_hermiticity_residual=hermiticity,
        physical_constraint_residual=residual,
        physical_dimension=physical_dimension,
        minimum_clock_reduction_rank=min(ranks),
        memory_neutral_future=_memory_neutral(future, atol=atol),
        record_target_neutral_future=_record_target_neutral(future, atol=atol),
    )


def quantum_extension_set(
    current_event: int = CANONICAL_ANCHOR,
    *,
    candidates: Iterable[QuantumContinuation] | None = None,
    atol: float = DEFAULT_ATOL,
) -> tuple[QuantumContinuation, ...]:
    """Return QExt(D) after physical admissibility and equivalence filtering.

    The declared terminal semantics are QExt(e2)=empty: no continuation beyond
    the terminal event is represented in the canonical three-event family.
    """

    if current_event == TERMINAL_EVENT:
        return ()
    if current_event != CANONICAL_ANCHOR:
        raise ValueError("canonical Stage 8A QExt is declared only at e1 or terminal e2")
    proposed = tuple(candidates) if candidates is not None else (
        canonical_continuation_left(),
        canonical_continuation_right(),
    )
    for continuation in proposed:
        diagnostics = assess_continuation_admissibility(continuation, atol=atol)
        if not diagnostics.admissible:
            raise ValueError(
                f"continuation {continuation.continuation_id!r} is not physically admissible/current-compatible"
            )
    return deduplicate_continuations(proposed, atol=atol)


def _future_probe_expectation(continuation: QuantumContinuation) -> float:
    future = _support_coordinates(reduced_continuation_state(continuation, UPPER_EVENT))
    probe = future_pair_coherence_probe_support_matrix()
    return float(np.vdot(future, probe @ future).real / np.vdot(future, future).real)


def stage8a_substrate_diagnostics(*, atol: float = DEFAULT_ATOL) -> Stage8ASubstrateDiagnostics:
    left = canonical_continuation_left()
    right = canonical_continuation_right()
    qext = quantum_extension_set()

    left_e0 = reduced_continuation_state(left, LOWER_EVENT)
    right_e0 = reduced_continuation_state(right, LOWER_EVENT)
    left_e1 = reduced_continuation_state(left, CURRENT_EVENT)
    right_e1 = reduced_continuation_state(right, CURRENT_EVENT)
    left_e2 = reduced_continuation_state(left, UPPER_EVENT)
    right_e2 = reduced_continuation_state(right, UPPER_EVENT)

    left_future = _support_coordinates(left_e2)
    right_future = _support_coordinates(right_e2)
    left_future = left_future / np.linalg.norm(left_future)
    right_future = right_future / np.linalg.norm(right_future)
    overlap_squared = float(abs(np.vdot(left_future, right_future)) ** 2)
    future_distance = float(np.linalg.norm(left_future - right_future))

    left_info = continuation_current_record_information(left)
    right_info = continuation_current_record_information(right)
    left_probe = _future_probe_expectation(left)
    right_probe = _future_probe_expectation(right)

    renamed = renamed_continuation(left, "h_L_renamed")
    with_rename = deduplicate_continuations((left, right, renamed), atol=atol)

    invalid = QuantumContinuation(
        "invalid-current-prefix",
        "identity",
        current_action="identity",
    )
    invalid_rejected = False
    try:
        quantum_extension_set(candidates=(left, right, invalid), atol=atol)
    except ValueError:
        invalid_rejected = True

    admissibilities = [assess_continuation_admissibility(item, atol=atol) for item in qext]
    future_operator_residual = float(
        np.linalg.norm(continuation_future_operator(left) - continuation_future_operator(right))
    )
    physically_inequivalent = bool(
        len(qext) >= 2
        and future_operator_residual > atol
        and overlap_squared < 1.0 - atol
        and abs(left_probe - right_probe) > atol
    )

    return Stage8ASubstrateDiagnostics(
        qext_size=len(qext),
        physical_continuations=tuple(item.continuation_id for item in qext),
        common_e0_state_residual=float(np.linalg.norm(left_e0 - right_e0)),
        common_e1_state_residual=float(np.linalg.norm(left_e1 - right_e1)),
        common_current_record_information_residual=abs(left_info - right_info),
        current_record_information=0.5 * (left_info + right_info),
        future_state_overlap_squared=overlap_squared,
        future_state_distance=future_distance,
        future_probe_expectation_left=left_probe,
        future_probe_expectation_right=right_probe,
        future_probe_difference=abs(left_probe - right_probe),
        future_operator_residual=future_operator_residual,
        renamed_equivalent=continuation_equivalent(left, renamed, atol=atol),
        deduplicated_size_with_rename=len(with_rename),
        minimum_clock_reduction_rank=min(item.minimum_clock_reduction_rank for item in admissibilities),
        maximum_constraint_residual=max(item.physical_constraint_residual for item in admissibilities),
        memory_neutral_future=all(item.memory_neutral_future for item in admissibilities),
        record_target_neutral_future=all(item.record_target_neutral_future for item in admissibilities),
        invalid_current_prefix_rejected=invalid_rejected,
        terminal_qext_size=len(quantum_extension_set(TERMINAL_EVENT)),
        physically_inequivalent=physically_inequivalent,
    )


def stage8a_summary() -> dict[str, object]:
    diagnostics = stage8a_substrate_diagnostics()
    return {
        "current_anchor": "e1",
        "terminal_event": "e2",
        "qext": tuple(item.continuation_id for item in quantum_extension_set()),
        "diagnostics": asdict(diagnostics),
        "future_difference": "memory-neutral C-sector phase after the shared e1 record state",
        "guards": [
            "QExt represented != ontically real futures by definition",
            "different continuation labels != physically different continuations",
            "future physical inequivalence != modal semantics by itself",
            "record-neutral continuation substrate != R-V independence theorem",
        ],
    }
