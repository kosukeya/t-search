"""Stage 7D genuine clock-change transport for the Stage 7C record history.

Stage 7C modifies the spectator constraint by an A-clock-conditioned dressing.
The resulting physical space is common to all clock choices, but the inherited
Stage 5/7A ideal support maps are no longer valid interacting maps.  Stage 7D
therefore re-derives, for every clock/readout node (X,j),

    D_X(j) : H_phys^hist -> H_rest(X) tensor H_M,

its 14-dimensional image support, an exact reconstruction on that support, and
cross-clock maps through the common modified physical space.

A central executable result is that B/C reductions remain full-rank but are not
Euclidean isometries.  The reduced support therefore carries the metric induced
from the common physical Hilbert space.  In orthonormal image coordinates y=C c,

    G = C^{-dagger} C^{-1},

so the re-derived clock change S=C_Y C_X^{-1} obeys

    S^dagger G_Y S = G_X

even when S is not Euclidean-unitary.  Physical observables are represented as
O_X=C_X O_phys C_X^{-1}; they are idempotent and G-self-adjoint rather than
necessarily Hermitian in the ambient Euclidean metric.

Record covariance is tested with an explicit event correspondence chi.  Equal
numeric clock readings never identify events.  The orientation-preserving chi
maps e0/e1/e2 to the same relational event labels; the orientation-reversing chi
swaps e0 and e2 while fixing e1.  A falsely declared preserving use of the
reversing chi is an explicit negative control.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import permutations, product
from typing import Literal

import numpy as np

from .stage3_asymmetry import orientation_from_scores
from .stage5_clock_change import DEFAULT_ATOL, SUBSYSTEMS
from .stage7_history import (
    CURRENT_EVENT,
    LOWER_EVENT,
    UPPER_EVENT,
    HistoryKind,
    canonical_physical_history_state,
    history_constraint_residual,
    history_physical_basis,
    history_reduction_coordinates,
    history_transition_support_matrix,
)
from .stage7_record import canonical_target_pair_projector
from .stage7_spectator import (
    MEMORY_DIMENSION,
    memory_identity,
    spectator_clock_change_operator,
    spectator_kinematic_clock_projection_operator,
)

ChiKind = Literal["preserving", "reversing", "misdeclared-preserving"]


@dataclass(frozen=True)
class EventCorrespondence:
    name: ChiKind
    source_events: tuple[str, str, str]
    target_events: tuple[str, str, str]
    orientation_sign: int
    declared_orientation: str


@dataclass(frozen=True)
class PerspectiveRecordAssessment:
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


@dataclass(frozen=True)
class Stage7DReductionDiagnostics:
    nodes: int
    min_rank: int
    max_support_roundtrip_residual: float
    max_physical_roundtrip_residual: float
    max_a_isometry_residual: float
    min_non_a_isometry_residual: float
    max_non_a_isometry_residual: float
    max_condition_number: float
    max_clock_probability_sum_residual: float
    nonuniform_clock_probability_detected: bool


@dataclass(frozen=True)
class Stage7DTransportDiagnostics:
    distinct_clock_comparisons: int
    max_state_transport_residual: float
    max_inverse_residual: float
    max_metric_covariance_residual: float
    max_observable_transport_residual: float
    max_preserving_record_score_residual: float
    max_preserving_accessibility_residual: float
    max_reversing_record_sign_residual: float
    max_reversing_accessibility_sign_residual: float
    max_metric_self_adjoint_residual: float
    max_projector_residual: float
    max_record_memory_commutator_residual: float
    max_euclidean_unitarity_residual: float
    legacy_spectator_map_state_residual: float
    bare_observable_residual: float
    bare_metric_self_adjoint_residual: float
    wrong_chi_record_score_residual: float
    wrong_chi_accessibility_residual: float
    preserving_covariance: bool
    reversing_covariance: bool
    legacy_map_rejected: bool
    bare_observable_rejected: bool
    wrong_chi_rejected: bool


def _validate_clock(clock: str) -> str:
    if clock not in SUBSYSTEMS:
        raise ValueError("clock must be one of A, B, or C")
    return clock


def _validate_index(index: int) -> int:
    if isinstance(index, bool) or not isinstance(index, int) or index not in (0, 1, 2):
        raise ValueError("Stage 7D clock index must be 0, 1, or 2")
    return index


def event_correspondence(kind: ChiKind = "preserving") -> EventCorrespondence:
    if kind == "preserving":
        return EventCorrespondence(
            name=kind,
            source_events=("e0", "e1", "e2"),
            target_events=("e0", "e1", "e2"),
            orientation_sign=1,
            declared_orientation="preserving",
        )
    if kind == "reversing":
        return EventCorrespondence(
            name=kind,
            source_events=("e0", "e1", "e2"),
            target_events=("e2", "e1", "e0"),
            orientation_sign=-1,
            declared_orientation="reversing",
        )
    if kind == "misdeclared-preserving":
        return EventCorrespondence(
            name=kind,
            source_events=("e0", "e1", "e2"),
            target_events=("e2", "e1", "e0"),
            orientation_sign=1,
            declared_orientation="preserving",
        )
    raise ValueError("chi must be preserving, reversing, or misdeclared-preserving")


def history_clock_reduction_operator(clock: str, index: int) -> np.ndarray:
    """Return sqrt(3)<t_j|_X tensor I on the common Stage 7 kinematic carrier.

    This is only the kinematic clock-reading map.  Its physical image/support is
    re-derived from the Stage 7C modified physical basis below.
    """

    x = _validate_clock(clock)
    j = _validate_index(index)
    return np.sqrt(3.0) * spectator_kinematic_clock_projection_operator(x, j)


def history_clock_reduction_matrix(
    kind: HistoryKind,
    clock: str,
    index: int,
) -> np.ndarray:
    """Represent D_X(j) on the orthonormal modified physical basis."""

    return history_clock_reduction_operator(clock, index) @ history_physical_basis(kind)


def _support_qr(kind: HistoryKind, clock: str, index: int) -> tuple[np.ndarray, np.ndarray]:
    reduction = history_clock_reduction_matrix(kind, clock, index)
    q, r = np.linalg.qr(reduction, mode="reduced")
    if np.linalg.matrix_rank(r, tol=DEFAULT_ATOL) != reduction.shape[1]:
        raise ValueError("declared clock reading is not an injective Stage 7D perspective")
    return q, r


def history_clock_support_basis(
    kind: HistoryKind,
    clock: str,
    index: int,
) -> np.ndarray:
    """Return an orthonormal basis for im(D_X(j)|H_phys^hist)."""

    return _support_qr(kind, clock, index)[0]


def history_clock_support_projector(
    kind: HistoryKind,
    clock: str,
    index: int,
) -> np.ndarray:
    basis = history_clock_support_basis(kind, clock, index)
    return basis @ basis.conj().T


def history_clock_reduction_coordinates(
    kind: HistoryKind,
    clock: str,
    index: int,
) -> np.ndarray:
    """Return C_X,j with y_X,j=C_X,j c for physical coefficients c."""

    return _support_qr(kind, clock, index)[1]


def history_clock_reconstruction_operator(
    kind: HistoryKind,
    clock: str,
    index: int,
) -> np.ndarray:
    """Exact inverse from the re-derived image support back to H_phys^hist."""

    support = history_clock_support_basis(kind, clock, index)
    coordinates = history_clock_reduction_coordinates(kind, clock, index)
    physical = history_physical_basis(kind)
    return physical @ np.linalg.inv(coordinates) @ support.conj().T


def history_clock_change_operator(
    kind: HistoryKind,
    target_clock: str,
    target_index: int,
    source_clock: str,
    source_index: int,
) -> np.ndarray:
    """Return the re-derived interacting S_{Y<-X}=D_Y E_X on ambient rest spaces."""

    _validate_clock(source_clock)
    _validate_clock(target_clock)
    _validate_index(source_index)
    _validate_index(target_index)
    if source_clock == target_clock:
        raise ValueError("Stage 7D genuine clock change requires distinct clocks")
    return (
        history_clock_reduction_operator(target_clock, target_index)
        @ history_clock_reconstruction_operator(kind, source_clock, source_index)
    )


def history_clock_change_support_matrix(
    kind: HistoryKind,
    target_clock: str,
    target_index: int,
    source_clock: str,
    source_index: int,
) -> np.ndarray:
    """Represent the interacting clock change in orthonormal image coordinates."""

    source = history_clock_reduction_coordinates(kind, source_clock, source_index)
    target = history_clock_reduction_coordinates(kind, target_clock, target_index)
    return target @ np.linalg.inv(source)


def history_support_metric(
    kind: HistoryKind,
    clock: str,
    index: int,
) -> np.ndarray:
    """Return the physical Hilbert metric induced on orthonormal image coordinates."""

    coordinates = history_clock_reduction_coordinates(kind, clock, index)
    inverse = np.linalg.inv(coordinates)
    return inverse.conj().T @ inverse


def reduced_history_support_coordinates(
    state: np.ndarray,
    kind: HistoryKind,
    clock: str,
    index: int,
    *,
    atol: float = DEFAULT_ATOL,
) -> np.ndarray:
    vector = np.asarray(state, dtype=np.complex128)
    if history_constraint_residual(vector, kind) > atol:
        raise ValueError("state must satisfy the declared Stage 7C modified constraint")
    support = history_clock_support_basis(kind, clock, index)
    reduced = history_clock_reduction_operator(clock, index) @ vector
    return support.conj().T @ reduced


def history_clock_probability(
    state: np.ndarray,
    kind: HistoryKind,
    clock: str,
    index: int,
) -> float:
    """Return ||<t_j|_X Psi||^2; unlike Stage 7A this need not be 1/3."""

    reduced = history_clock_reduction_operator(clock, index) @ np.asarray(
        state, dtype=np.complex128
    )
    return float(np.vdot(reduced, reduced).real / 3.0)


def _fixed_a_target_operator_at_current(event_index: int) -> np.ndarray:
    if event_index not in (LOWER_EVENT, UPPER_EVENT):
        raise ValueError("record target event must be e0 or e2")
    target = np.kron(canonical_target_pair_projector(), memory_identity())
    transition = history_transition_support_matrix("forward", CURRENT_EVENT, event_index)
    return transition @ target @ transition.conj().T


def _fixed_a_memory_projector(bit: int) -> np.ndarray:
    if bit not in (0, 1):
        raise ValueError("memory bit must be 0 or 1")
    pair_dimension = canonical_target_pair_projector().shape[0]
    memory = np.zeros((MEMORY_DIMENSION, MEMORY_DIMENSION), dtype=np.complex128)
    memory[bit, bit] = 1.0
    return np.kron(np.eye(pair_dimension, dtype=np.complex128), memory)


def _physical_operator_from_fixed_a(operator: np.ndarray) -> np.ndarray:
    """Convert the Stage 7C A/e1 support representation to physical coordinates."""

    coordinates = history_reduction_coordinates("forward", CURRENT_EVENT)
    return np.linalg.inv(coordinates) @ operator @ coordinates


def physical_event_target_operator(event_index: int) -> np.ndarray:
    operator = _physical_operator_from_fixed_a(
        _fixed_a_target_operator_at_current(event_index)
    )
    if np.linalg.norm(operator - operator.conj().T) > DEFAULT_ATOL:
        raise RuntimeError("physical target operator failed Hermiticity")
    return operator


def physical_memory_projector(bit: int) -> np.ndarray:
    operator = _physical_operator_from_fixed_a(_fixed_a_memory_projector(bit))
    if np.linalg.norm(operator - operator.conj().T) > DEFAULT_ATOL:
        raise RuntimeError("physical memory operator failed Hermiticity")
    return operator


def represent_physical_operator(
    operator: np.ndarray,
    kind: HistoryKind,
    clock: str,
    index: int,
) -> np.ndarray:
    """Return O_X=C_X O_phys C_X^{-1} on one re-derived support."""

    physical = np.asarray(operator, dtype=np.complex128)
    if physical.shape != (14, 14):
        raise ValueError("Stage 7D physical-coordinate operator must have shape (14,14)")
    coordinates = history_clock_reduction_coordinates(kind, clock, index)
    return coordinates @ physical @ np.linalg.inv(coordinates)


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
    if abs(denominator.imag) > DEFAULT_ATOL or denominator.real <= DEFAULT_ATOL:
        raise RuntimeError("invalid induced-metric norm")

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
                max_self_adjoint,
                metric_self_adjoint_residual(memory, metric),
            )
            max_projector = max(
                max_projector,
                float(np.linalg.norm(memory @ memory - memory)),
            )
            max_commutator = max(
                max_commutator,
                float(np.linalg.norm(target @ memory - memory @ target)),
            )
            value = np.vdot(
                state_coordinates,
                metric @ target @ memory @ state_coordinates,
            ) / denominator
            if abs(value.imag) > 1e-9:
                raise RuntimeError("commuting record readout acquired an imaginary probability")
            joint[target_bit, memory_bit] = float(value.real)

    joint[np.abs(joint) <= DEFAULT_ATOL] = 0.0
    if np.min(joint) < -DEFAULT_ATOL:
        raise RuntimeError("record joint distribution acquired a negative probability")
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
    clock: str,
    index: int,
    event_index: int,
    *,
    state: np.ndarray | None = None,
    kind: HistoryKind = "forward",
) -> tuple[np.ndarray, float, float, float]:
    physical_state = (
        canonical_physical_history_state(kind)
        if state is None
        else np.asarray(state, dtype=np.complex128)
    )
    state_coordinates = reduced_history_support_coordinates(
        physical_state, kind, clock, index
    )
    metric = history_support_metric(kind, clock, index)

    # Stage 7D record transport is anchored to the forward Stage 7C record
    # semantics.  Other HistoryKind values are allowed for map diagnostics but
    # the target/readout physical operators are those declared by that witness.
    target_physical = physical_event_target_operator(event_index)
    target = represent_physical_operator(target_physical, kind, clock, index)
    memory = tuple(
        represent_physical_operator(physical_memory_projector(bit), kind, clock, index)
        for bit in (0, 1)
    )
    return _metric_joint_distribution(
        state_coordinates,
        metric,
        target,
        memory,  # type: ignore[arg-type]
    )


def perspective_record_assessment(
    clock: str,
    index: int,
    *,
    chi: ChiKind = "preserving",
    tolerance: float = 1e-10,
) -> PerspectiveRecordAssessment:
    correspondence = event_correspondence(chi)
    lower_event = LOWER_EVENT if correspondence.target_events[0] == "e0" else UPPER_EVENT
    upper_event = UPPER_EVENT if correspondence.target_events[2] == "e2" else LOWER_EVENT

    lower_joint, _, _, _ = perspective_record_joint_distribution(clock, index, lower_event)
    upper_joint, _, _, _ = perspective_record_joint_distribution(clock, index, upper_event)
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
    state_coordinates = reduced_history_support_coordinates(
        canonical_physical_history_state("forward"), "forward", clock, index
    )
    metric = history_support_metric("forward", clock, index)
    metric_norm = float(np.vdot(state_coordinates, metric @ state_coordinates).real)
    return PerspectiveRecordAssessment(
        clock=clock,
        clock_index=index,
        chi=correspondence.name,
        lower_information=lower_information,
        upper_information=upper_information,
        lower_accuracy=lower_accuracy,
        upper_accuracy=upper_accuracy,
        record_score=record_score,
        accessibility_score=accessibility_score,
        orientation=orientation,
        record_defined=bool(orientation != "none" and selected_information > tolerance),
        metric_norm=metric_norm,
    )


def stage7d_reduction_diagnostics() -> Stage7DReductionDiagnostics:
    physical = history_physical_basis("forward")
    physical_projector = physical @ physical.conj().T
    canonical_state = canonical_physical_history_state("forward")
    min_rank = 14
    max_support_roundtrip = 0.0
    max_physical_roundtrip = 0.0
    max_a_isometry = 0.0
    non_a_isometries: list[float] = []
    max_condition = 0.0
    probability_sum_residual = 0.0
    nonuniform = False

    for clock in SUBSYSTEMS:
        probabilities = []
        for index in (0, 1, 2):
            reduction_matrix = history_clock_reduction_matrix("forward", clock, index)
            rank = int(np.linalg.matrix_rank(reduction_matrix, tol=DEFAULT_ATOL))
            min_rank = min(min_rank, rank)
            gram_residual = float(
                np.linalg.norm(reduction_matrix.conj().T @ reduction_matrix - np.eye(14))
            )
            if clock == "A":
                max_a_isometry = max(max_a_isometry, gram_residual)
            else:
                non_a_isometries.append(gram_residual)

            coordinates = history_clock_reduction_coordinates("forward", clock, index)
            max_condition = max(max_condition, float(np.linalg.cond(coordinates)))
            reduction = history_clock_reduction_operator(clock, index)
            reconstruction = history_clock_reconstruction_operator("forward", clock, index)
            support_projector = history_clock_support_projector("forward", clock, index)
            max_support_roundtrip = max(
                max_support_roundtrip,
                float(np.linalg.norm(reduction @ reconstruction - support_projector)),
            )
            max_physical_roundtrip = max(
                max_physical_roundtrip,
                float(
                    np.linalg.norm(
                        reconstruction @ reduction @ physical_projector - physical_projector
                    )
                ),
            )
            probabilities.append(
                history_clock_probability(canonical_state, "forward", clock, index)
            )
        probability_sum_residual = max(
            probability_sum_residual, abs(sum(probabilities) - 1.0)
        )
        if max(probabilities) - min(probabilities) > DEFAULT_ATOL:
            nonuniform = True

    return Stage7DReductionDiagnostics(
        nodes=9,
        min_rank=min_rank,
        max_support_roundtrip_residual=max_support_roundtrip,
        max_physical_roundtrip_residual=max_physical_roundtrip,
        max_a_isometry_residual=max_a_isometry,
        min_non_a_isometry_residual=min(non_a_isometries),
        max_non_a_isometry_residual=max(non_a_isometries),
        max_condition_number=max_condition,
        max_clock_probability_sum_residual=probability_sum_residual,
        nonuniform_clock_probability_detected=nonuniform,
    )


def _node_operator(clock: str, index: int, physical_operator: np.ndarray) -> np.ndarray:
    return represent_physical_operator(physical_operator, "forward", clock, index)


def stage7d_transport_diagnostics() -> Stage7DTransportDiagnostics:
    state = canonical_physical_history_state("forward")
    source_reference = perspective_record_assessment("A", CURRENT_EVENT, chi="preserving")
    max_state = 0.0
    max_inverse = 0.0
    max_metric = 0.0
    max_observable = 0.0
    max_euclidean_unitarity = 0.0
    comparisons = 0

    physical_operators = (
        physical_event_target_operator(LOWER_EVENT),
        physical_event_target_operator(UPPER_EVENT),
        physical_memory_projector(0),
        physical_memory_projector(1),
    )

    for source_clock in SUBSYSTEMS:
        for target_clock in SUBSYSTEMS:
            if source_clock == target_clock:
                continue
            for source_index, target_index in product(range(3), repeat=2):
                source_coordinates = reduced_history_support_coordinates(
                    state, "forward", source_clock, source_index
                )
                target_coordinates = reduced_history_support_coordinates(
                    state, "forward", target_clock, target_index
                )
                transform = history_clock_change_support_matrix(
                    "forward",
                    target_clock,
                    target_index,
                    source_clock,
                    source_index,
                )
                reverse = history_clock_change_support_matrix(
                    "forward",
                    source_clock,
                    source_index,
                    target_clock,
                    target_index,
                )
                max_state = max(
                    max_state,
                    float(np.linalg.norm(transform @ source_coordinates - target_coordinates)),
                )
                max_inverse = max(
                    max_inverse,
                    float(np.linalg.norm(reverse @ transform - np.eye(14))),
                )
                source_metric = history_support_metric(
                    "forward", source_clock, source_index
                )
                target_metric = history_support_metric(
                    "forward", target_clock, target_index
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
                max_euclidean_unitarity = max(
                    max_euclidean_unitarity,
                    float(np.linalg.norm(transform.conj().T @ transform - np.eye(14))),
                )
                inverse_transform = np.linalg.inv(transform)
                for physical_operator in physical_operators:
                    source_operator = _node_operator(
                        source_clock, source_index, physical_operator
                    )
                    target_operator = _node_operator(
                        target_clock, target_index, physical_operator
                    )
                    max_observable = max(
                        max_observable,
                        float(
                            np.linalg.norm(
                                transform @ source_operator @ inverse_transform
                                - target_operator
                            )
                        ),
                    )
                comparisons += 1

    max_preserving_record = 0.0
    max_preserving_access = 0.0
    max_reversing_record = 0.0
    max_reversing_access = 0.0
    max_self_adjoint = 0.0
    max_projector = 0.0
    max_commutator = 0.0
    for clock in SUBSYSTEMS:
        for index in (0, 1, 2):
            preserving = perspective_record_assessment(clock, index, chi="preserving")
            reversing = perspective_record_assessment(clock, index, chi="reversing")
            max_preserving_record = max(
                max_preserving_record,
                abs(preserving.record_score - source_reference.record_score),
            )
            max_preserving_access = max(
                max_preserving_access,
                abs(preserving.accessibility_score - source_reference.accessibility_score),
            )
            max_reversing_record = max(
                max_reversing_record,
                abs(reversing.record_score + source_reference.record_score),
            )
            max_reversing_access = max(
                max_reversing_access,
                abs(reversing.accessibility_score + source_reference.accessibility_score),
            )
            for event in (LOWER_EVENT, UPPER_EVENT):
                _, self_adj, projector, commutator = perspective_record_joint_distribution(
                    clock, index, event
                )
                max_self_adjoint = max(max_self_adjoint, self_adj)
                max_projector = max(max_projector, projector)
                max_commutator = max(max_commutator, commutator)

    # Explicit negative controls use A/e1 -> B/e0.
    source_clock, source_index = "A", CURRENT_EVENT
    target_clock, target_index = "B", 0
    source_ambient = history_clock_reduction_operator(source_clock, source_index) @ state
    target_ambient = history_clock_reduction_operator(target_clock, target_index) @ state
    legacy = spectator_clock_change_operator(
        target_clock,
        target_index,
        source_clock,
        source_index,
    )
    legacy_residual = float(np.linalg.norm(legacy @ source_ambient - target_ambient))

    source_lower = _node_operator(
        source_clock, source_index, physical_event_target_operator(LOWER_EVENT)
    )
    target_lower = _node_operator(
        target_clock, target_index, physical_event_target_operator(LOWER_EVENT)
    )
    target_metric = history_support_metric("forward", target_clock, target_index)
    bare_residual = float(np.linalg.norm(source_lower - target_lower))
    bare_self_adjoint = metric_self_adjoint_residual(source_lower, target_metric)

    wrong = perspective_record_assessment(
        target_clock, target_index, chi="misdeclared-preserving"
    )
    wrong_record = abs(wrong.record_score - source_reference.record_score)
    wrong_access = abs(
        wrong.accessibility_score - source_reference.accessibility_score
    )

    tolerance = 1e-9
    return Stage7DTransportDiagnostics(
        distinct_clock_comparisons=comparisons,
        max_state_transport_residual=max_state,
        max_inverse_residual=max_inverse,
        max_metric_covariance_residual=max_metric,
        max_observable_transport_residual=max_observable,
        max_preserving_record_score_residual=max_preserving_record,
        max_preserving_accessibility_residual=max_preserving_access,
        max_reversing_record_sign_residual=max_reversing_record,
        max_reversing_accessibility_sign_residual=max_reversing_access,
        max_metric_self_adjoint_residual=max_self_adjoint,
        max_projector_residual=max_projector,
        max_record_memory_commutator_residual=max_commutator,
        max_euclidean_unitarity_residual=max_euclidean_unitarity,
        legacy_spectator_map_state_residual=legacy_residual,
        bare_observable_residual=bare_residual,
        bare_metric_self_adjoint_residual=bare_self_adjoint,
        wrong_chi_record_score_residual=wrong_record,
        wrong_chi_accessibility_residual=wrong_access,
        preserving_covariance=bool(
            max_state <= tolerance
            and max_inverse <= tolerance
            and max_metric <= tolerance
            and max_observable <= tolerance
            and max_preserving_record <= tolerance
            and max_preserving_access <= tolerance
        ),
        reversing_covariance=bool(
            max_reversing_record <= tolerance
            and max_reversing_access <= tolerance
        ),
        legacy_map_rejected=bool(legacy_residual > tolerance),
        bare_observable_rejected=bool(
            bare_residual > tolerance and bare_self_adjoint > tolerance
        ),
        wrong_chi_rejected=bool(
            wrong_record > tolerance and wrong_access > tolerance
        ),
    )


def stage7d_summary() -> dict[str, object]:
    state = canonical_physical_history_state("forward")
    probabilities = {
        clock: [
            history_clock_probability(state, "forward", clock, index)
            for index in (0, 1, 2)
        ]
        for clock in SUBSYSTEMS
    }
    assessments = {
        f"{clock}{index}": asdict(
            perspective_record_assessment(clock, index, chi="preserving")
        )
        for clock in SUBSYSTEMS
        for index in (0, 1, 2)
    }
    return {
        "reduction": asdict(stage7d_reduction_diagnostics()),
        "transport": asdict(stage7d_transport_diagnostics()),
        "clock_probabilities": probabilities,
        "preserving_record_assessments": assessments,
        "chi": {
            "preserving": asdict(event_correspondence("preserving")),
            "reversing": asdict(event_correspondence("reversing")),
            "misdeclared_preserving_control": asdict(
                event_correspondence("misdeclared-preserving")
            ),
        },
        "guards": [
            "equal numeric clock readings != event identity",
            "interacting clock change != inherited spectator clock change",
            "non-Euclidean-unitary map != failed perspective map when the induced physical metric is preserved",
            "G-self-adjoint observable != arbitrary non-Hermitian observable",
            "record covariance != P=R",
            "orientation-reversing chi != physical reversal of the history dynamics",
        ],
    }
