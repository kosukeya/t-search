"""Stage 7E accessibility and partial-atlas record consistency.

Stage 7D established a record-bearing, induced-metric-preserving interacting
clock atlas.  Stage 7E separates two notions that must not be identified:

    global/reconstructible record structure != local memory accessibility.

The common physical state and record operators are held fixed while only the
declared memory readout interface is changed.  Four interfaces are tested:

- full: exact computational memory readout;
- hidden: both memory values map to one visible output;
- maximally-noisy: a binary-symmetric channel with crossover 1/2;
- coarse: a binary-symmetric channel with crossover 1/4.

The second pressure test removes the canonical direct edge A/e1 -> B/e0 from a
partial interacting perspective atlas.  Three indirect paths via C/e0, C/e1,
and C/e2 remain.  They are compared with the mathematically re-derived direct
map only as an oracle, not as an available atlas edge.  A controlled
perturbation of the single local edge C/e1 -> B/e0 must spoil only the path that
uses that edge.

No local access failure is interpreted as destruction of the globally
represented record, and no path residual is interpreted as spacetime curvature.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal

import numpy as np

from .stage3_asymmetry import orientation_from_scores
from .stage5_clock_change import DEFAULT_ATOL
from .stage7_history import CURRENT_EVENT, LOWER_EVENT, UPPER_EVENT, canonical_physical_history_state
from .stage7_record_transport import (
    history_clock_change_support_matrix,
    history_support_metric,
    perspective_record_assessment,
    perspective_record_joint_distribution,
    physical_event_target_operator,
    physical_memory_projector,
    reduced_history_support_coordinates,
    represent_physical_operator,
)

AccessKind = Literal["full", "hidden", "maximally-noisy", "coarse"]


@dataclass(frozen=True)
class PerspectiveNode:
    clock: str
    index: int

    @property
    def label(self) -> str:
        return f"{self.clock}/e{self.index}"


@dataclass(frozen=True)
class LocalAccessibilityAssessment:
    clock: str
    clock_index: int
    interface: str
    global_lower_information: float
    global_upper_information: float
    global_record_score: float
    global_accessibility_score: float
    global_orientation: str
    globally_represented: bool
    local_lower_information: float
    local_upper_information: float
    local_lower_accuracy: float
    local_upper_accuracy: float
    local_record_score: float
    local_accessibility_score: float
    local_orientation: str
    locally_accessible: bool


@dataclass(frozen=True)
class PartialAtlasPathAssessment:
    source: str
    intermediate: str
    target: str
    direct_edge_available: bool
    perturbed: bool
    map_residual: float
    state_residual: float
    metric_covariance_residual: float
    max_observable_residual: float
    record_score: float
    accessibility_score: float
    record_score_residual: float
    accessibility_score_residual: float
    consistent: bool


@dataclass(frozen=True)
class Stage7EAccessibilityDiagnostics:
    nodes_tested: int
    interfaces_tested: int
    max_full_global_local_record_residual: float
    max_full_global_local_accessibility_residual: float
    max_hidden_local_record_score: float
    max_hidden_local_accessibility_score: float
    max_noisy_local_record_score: float
    max_noisy_local_accessibility_score: float
    min_coarse_record_score: float
    min_coarse_accessibility_score: float
    global_record_survives_hidden: bool
    global_record_survives_noisy: bool
    hidden_is_inaccessible: bool
    noisy_is_inaccessible: bool
    coarse_is_degraded_but_accessible: bool


@dataclass(frozen=True)
class Stage7EAtlasDiagnostics:
    source: str
    target: str
    direct_edge_available: bool
    ideal_indirect_paths: int
    max_ideal_map_residual: float
    max_ideal_state_residual: float
    max_ideal_metric_residual: float
    max_ideal_observable_residual: float
    max_ideal_record_score_residual: float
    max_ideal_accessibility_residual: float
    perturbed_intermediate: str
    perturbed_map_residual: float
    perturbed_state_residual: float
    perturbed_metric_residual: float
    perturbed_observable_residual: float
    perturbed_record_score_residual: float
    perturbed_accessibility_residual: float
    ideal_paths_consistent: bool
    perturbation_detected: bool
    localized_failure: bool


_SOURCE = PerspectiveNode("A", CURRENT_EVENT)
_TARGET = PerspectiveNode("B", 0)
_INTERMEDIATES = tuple(PerspectiveNode("C", index) for index in range(3))
_PERTURBED_INTERMEDIATE = PerspectiveNode("C", 1)


def memory_readout_channel(kind: AccessKind) -> np.ndarray:
    """Return P(accessible_output | physical_memory_bit)."""

    if kind == "full":
        return np.eye(2, dtype=float)
    if kind == "hidden":
        return np.array([[1.0, 0.0], [1.0, 0.0]], dtype=float)
    if kind == "maximally-noisy":
        return np.full((2, 2), 0.5, dtype=float)
    if kind == "coarse":
        return np.array([[0.75, 0.25], [0.25, 0.75]], dtype=float)
    raise ValueError("interface must be full, hidden, maximally-noisy, or coarse")


def apply_memory_interface(joint: np.ndarray, kind: AccessKind) -> np.ndarray:
    probabilities = np.asarray(joint, dtype=float)
    if probabilities.shape != (2, 2):
        raise ValueError("record joint distribution must have shape (2,2)")
    if np.min(probabilities) < -DEFAULT_ATOL:
        raise ValueError("record joint distribution must be nonnegative")
    total = float(np.sum(probabilities))
    if total <= 0.0:
        raise ValueError("record joint distribution has zero mass")
    normalized = probabilities / total
    visible = normalized @ memory_readout_channel(kind)
    visible[np.abs(visible) <= DEFAULT_ATOL] = 0.0
    return visible / np.sum(visible)


def _mutual_information(joint: np.ndarray) -> float:
    probabilities = np.asarray(joint, dtype=float)
    px = np.sum(probabilities, axis=1, keepdims=True)
    pm = np.sum(probabilities, axis=0, keepdims=True)
    independent = px @ pm
    mask = probabilities > DEFAULT_ATOL
    if not np.any(mask):
        return 0.0
    return float(np.sum(probabilities[mask] * np.log2(probabilities[mask] / independent[mask])))


def _decoder_accuracy(joint: np.ndarray) -> float:
    return float(sum(np.max(joint[:, output]) for output in range(joint.shape[1])))


def local_accessibility_assessment(
    clock: str,
    index: int,
    interface: AccessKind,
    *,
    tolerance: float = 1e-10,
) -> LocalAccessibilityAssessment:
    global_assessment = perspective_record_assessment(clock, index, chi="preserving")
    lower_joint, *_ = perspective_record_joint_distribution(clock, index, LOWER_EVENT)
    upper_joint, *_ = perspective_record_joint_distribution(clock, index, UPPER_EVENT)
    lower_visible = apply_memory_interface(lower_joint, interface)
    upper_visible = apply_memory_interface(upper_joint, interface)

    lower_information = _mutual_information(lower_visible)
    upper_information = _mutual_information(upper_visible)
    lower_accuracy = _decoder_accuracy(lower_visible)
    upper_accuracy = _decoder_accuracy(upper_visible)
    record_score = lower_information - upper_information
    accessibility_score = lower_accuracy - upper_accuracy
    orientation = orientation_from_scores(record_score, accessibility_score, tolerance=tolerance)
    selected_information = (
        lower_information
        if orientation == "lower-index"
        else upper_information if orientation == "upper-index" else 0.0
    )
    locally_accessible = bool(orientation != "none" and selected_information > tolerance)

    return LocalAccessibilityAssessment(
        clock=clock,
        clock_index=index,
        interface=interface,
        global_lower_information=global_assessment.lower_information,
        global_upper_information=global_assessment.upper_information,
        global_record_score=global_assessment.record_score,
        global_accessibility_score=global_assessment.accessibility_score,
        global_orientation=global_assessment.orientation,
        globally_represented=global_assessment.record_defined,
        local_lower_information=lower_information,
        local_upper_information=upper_information,
        local_lower_accuracy=lower_accuracy,
        local_upper_accuracy=upper_accuracy,
        local_record_score=record_score,
        local_accessibility_score=accessibility_score,
        local_orientation=orientation,
        locally_accessible=locally_accessible,
    )


def stage7e_accessibility_diagnostics() -> Stage7EAccessibilityDiagnostics:
    kinds: tuple[AccessKind, ...] = ("full", "hidden", "maximally-noisy", "coarse")
    assessments = [
        local_accessibility_assessment(clock, index, kind)
        for clock in ("A", "B", "C")
        for index in range(3)
        for kind in kinds
    ]
    full = [item for item in assessments if item.interface == "full"]
    hidden = [item for item in assessments if item.interface == "hidden"]
    noisy = [item for item in assessments if item.interface == "maximally-noisy"]
    coarse = [item for item in assessments if item.interface == "coarse"]

    return Stage7EAccessibilityDiagnostics(
        nodes_tested=9,
        interfaces_tested=len(kinds),
        max_full_global_local_record_residual=max(
            abs(item.global_record_score - item.local_record_score) for item in full
        ),
        max_full_global_local_accessibility_residual=max(
            abs(item.global_accessibility_score - item.local_accessibility_score)
            for item in full
        ),
        max_hidden_local_record_score=max(abs(item.local_record_score) for item in hidden),
        max_hidden_local_accessibility_score=max(
            abs(item.local_accessibility_score) for item in hidden
        ),
        max_noisy_local_record_score=max(abs(item.local_record_score) for item in noisy),
        max_noisy_local_accessibility_score=max(
            abs(item.local_accessibility_score) for item in noisy
        ),
        min_coarse_record_score=min(item.local_record_score for item in coarse),
        min_coarse_accessibility_score=min(item.local_accessibility_score for item in coarse),
        global_record_survives_hidden=all(item.globally_represented for item in hidden),
        global_record_survives_noisy=all(item.globally_represented for item in noisy),
        hidden_is_inaccessible=all(not item.locally_accessible for item in hidden),
        noisy_is_inaccessible=all(not item.locally_accessible for item in noisy),
        coarse_is_degraded_but_accessible=all(
            item.locally_accessible
            and tolerance_less(item.local_record_score, item.global_record_score)
            and tolerance_less(item.local_accessibility_score, item.global_accessibility_score)
            for item in coarse
        ),
    )


def tolerance_less(left: float, right: float, tolerance: float = 1e-10) -> bool:
    return bool(left > tolerance and left < right - tolerance)


def _edge(target: PerspectiveNode, source: PerspectiveNode) -> np.ndarray:
    if target.clock == source.clock:
        raise ValueError("Stage 7E partial atlas uses genuine distinct-clock edges")
    return history_clock_change_support_matrix(
        "forward", target.clock, target.index, source.clock, source.index
    )


def _canonical_direct_reference() -> np.ndarray:
    """Mathematical oracle for the intentionally omitted A/e1 -> B/e0 edge."""

    return _edge(_TARGET, _SOURCE)


def _correct_target_operator(physical_operator: np.ndarray) -> np.ndarray:
    return represent_physical_operator(
        physical_operator, "forward", _TARGET.clock, _TARGET.index
    )


def _metric_joint_from_coordinates(
    coordinates: np.ndarray,
    target_projector: np.ndarray,
    memory_projectors: tuple[np.ndarray, np.ndarray],
) -> np.ndarray:
    metric = history_support_metric("forward", _TARGET.clock, _TARGET.index)
    identity = np.eye(14, dtype=np.complex128)
    denominator = np.vdot(coordinates, metric @ coordinates)
    if abs(denominator.imag) > 1e-9 or denominator.real <= DEFAULT_ATOL:
        raise RuntimeError("invalid target-chart metric norm")
    joint = np.zeros((2, 2), dtype=float)
    for target_bit, target in ((1, target_projector), (0, identity - target_projector)):
        for memory_bit, memory in enumerate(memory_projectors):
            value = np.vdot(coordinates, metric @ target @ memory @ coordinates) / denominator
            if abs(value.imag) > 1e-8:
                raise RuntimeError("record readout acquired an imaginary probability")
            joint[target_bit, memory_bit] = float(value.real)
    joint[np.abs(joint) <= DEFAULT_ATOL] = 0.0
    if np.min(joint) < -1e-8:
        raise RuntimeError("record readout acquired a negative probability")
    joint = np.clip(joint, 0.0, None)
    return joint / np.sum(joint)


def _record_profile_from_target_coordinates(coordinates: np.ndarray) -> tuple[float, float]:
    lower = _correct_target_operator(physical_event_target_operator(LOWER_EVENT))
    upper = _correct_target_operator(physical_event_target_operator(UPPER_EVENT))
    memory = tuple(
        _correct_target_operator(physical_memory_projector(bit)) for bit in (0, 1)
    )
    lower_joint = _metric_joint_from_coordinates(coordinates, lower, memory)  # type: ignore[arg-type]
    upper_joint = _metric_joint_from_coordinates(coordinates, upper, memory)  # type: ignore[arg-type]
    record_score = _mutual_information(lower_joint) - _mutual_information(upper_joint)
    accessibility_score = _decoder_accuracy(lower_joint) - _decoder_accuracy(upper_joint)
    return record_score, accessibility_score


def _perturb_target_edge(edge: np.ndarray, strength: float = 0.25) -> np.ndarray:
    """Locally scale one correct joint-record sector in the B/e0 target chart."""

    lower = _correct_target_operator(physical_event_target_operator(LOWER_EVENT))
    memory_one = _correct_target_operator(physical_memory_projector(1))
    sector = lower @ memory_one
    perturbation = np.eye(14, dtype=np.complex128) + strength * sector
    return perturbation @ edge


def partial_atlas_path_assessment(
    intermediate_index: int,
    *,
    perturb_local_edge: bool = False,
    tolerance: float = 1e-9,
) -> PartialAtlasPathAssessment:
    if intermediate_index not in (0, 1, 2):
        raise ValueError("intermediate C-clock index must be 0, 1, or 2")
    middle = PerspectiveNode("C", intermediate_index)
    first = _edge(middle, _SOURCE)
    second = _edge(_TARGET, middle)
    if perturb_local_edge:
        if middle != _PERTURBED_INTERMEDIATE:
            raise ValueError("the canonical Stage 7E perturbation is localized to C/e1 -> B/e0")
        second = _perturb_target_edge(second)

    composite = second @ first
    reference = _canonical_direct_reference()
    source_state = reduced_history_support_coordinates(
        canonical_physical_history_state("forward"),
        "forward",
        _SOURCE.clock,
        _SOURCE.index,
    )
    path_state = composite @ source_state
    reference_state = reference @ source_state

    source_metric = history_support_metric("forward", _SOURCE.clock, _SOURCE.index)
    target_metric = history_support_metric("forward", _TARGET.clock, _TARGET.index)
    metric_residual = float(
        np.linalg.norm(composite.conj().T @ target_metric @ composite - source_metric)
    )

    physical_operators = (
        physical_event_target_operator(LOWER_EVENT),
        physical_event_target_operator(UPPER_EVENT),
        physical_memory_projector(0),
        physical_memory_projector(1),
    )
    observable_residual = 0.0
    inverse_composite = np.linalg.inv(composite)
    for physical_operator in physical_operators:
        source_operator = represent_physical_operator(
            physical_operator, "forward", _SOURCE.clock, _SOURCE.index
        )
        correct_target = _correct_target_operator(physical_operator)
        transported = composite @ source_operator @ inverse_composite
        observable_residual = max(
            observable_residual, float(np.linalg.norm(transported - correct_target))
        )

    record_score, accessibility_score = _record_profile_from_target_coordinates(path_state)
    reference_assessment = perspective_record_assessment(
        _TARGET.clock, _TARGET.index, chi="preserving"
    )
    map_residual = float(np.linalg.norm(composite - reference))
    state_residual = float(np.linalg.norm(path_state - reference_state))
    record_residual = abs(record_score - reference_assessment.record_score)
    accessibility_residual = abs(
        accessibility_score - reference_assessment.accessibility_score
    )
    consistent = bool(
        map_residual <= tolerance
        and state_residual <= tolerance
        and metric_residual <= tolerance
        and observable_residual <= tolerance
        and record_residual <= tolerance
        and accessibility_residual <= tolerance
    )
    return PartialAtlasPathAssessment(
        source=_SOURCE.label,
        intermediate=middle.label,
        target=_TARGET.label,
        direct_edge_available=False,
        perturbed=perturb_local_edge,
        map_residual=map_residual,
        state_residual=state_residual,
        metric_covariance_residual=metric_residual,
        max_observable_residual=observable_residual,
        record_score=record_score,
        accessibility_score=accessibility_score,
        record_score_residual=record_residual,
        accessibility_score_residual=accessibility_residual,
        consistent=consistent,
    )


def stage7e_partial_atlas_diagnostics() -> Stage7EAtlasDiagnostics:
    ideal = [partial_atlas_path_assessment(index) for index in range(3)]
    perturbed = partial_atlas_path_assessment(1, perturb_local_edge=True)
    unaffected = [item for item in ideal if item.intermediate != _PERTURBED_INTERMEDIATE.label]
    # The canonical perturbation commutes with the tested record projector algebra,
    # so observable similarity transport can remain exact even though the edge no
    # longer preserves the target metric/state and the resulting record statistic
    # shifts.  Criterion 29 therefore detects the localized inconsistency from the
    # independently failing map/state/metric/statistical witnesses rather than
    # requiring every diagnostic to fail simultaneously.
    perturbation_detected = bool(
        perturbed.map_residual > 1e-3
        and perturbed.state_residual > 1e-3
        and perturbed.metric_covariance_residual > 1e-3
        and perturbed.record_score_residual > 1e-4
    )
    localized = bool(
        perturbation_detected
        and all(item.consistent for item in unaffected)
        and not perturbed.consistent
    )
    return Stage7EAtlasDiagnostics(
        source=_SOURCE.label,
        target=_TARGET.label,
        direct_edge_available=False,
        ideal_indirect_paths=len(ideal),
        max_ideal_map_residual=max(item.map_residual for item in ideal),
        max_ideal_state_residual=max(item.state_residual for item in ideal),
        max_ideal_metric_residual=max(item.metric_covariance_residual for item in ideal),
        max_ideal_observable_residual=max(item.max_observable_residual for item in ideal),
        max_ideal_record_score_residual=max(item.record_score_residual for item in ideal),
        max_ideal_accessibility_residual=max(
            item.accessibility_score_residual for item in ideal
        ),
        perturbed_intermediate=perturbed.intermediate,
        perturbed_map_residual=perturbed.map_residual,
        perturbed_state_residual=perturbed.state_residual,
        perturbed_metric_residual=perturbed.metric_covariance_residual,
        perturbed_observable_residual=perturbed.max_observable_residual,
        perturbed_record_score_residual=perturbed.record_score_residual,
        perturbed_accessibility_residual=perturbed.accessibility_score_residual,
        ideal_paths_consistent=all(item.consistent for item in ideal),
        perturbation_detected=perturbation_detected,
        localized_failure=localized,
    )


def stage7e_summary() -> dict[str, object]:
    return {
        "accessibility": asdict(stage7e_accessibility_diagnostics()),
        "partial_atlas": asdict(stage7e_partial_atlas_diagnostics()),
        "canonical_missing_edge": "A/e1 -> B/e0",
        "indirect_paths": ["A/e1 -> C/e0 -> B/e0", "A/e1 -> C/e1 -> B/e0", "A/e1 -> C/e2 -> B/e0"],
        "perturbed_edge": "C/e1 -> B/e0",
        "guards": [
            "locally inaccessible record != globally absent record",
            "global reconstructibility != local accessibility",
            "indirect reconstructibility != direct local edge availability",
            "partial atlas path consistency != universal frame availability",
            "localized path inconsistency != spacetime curvature",
            "observable-algebra correspondence != full state/metric path consistency",
            "record covariance != P=R",
        ],
    }
