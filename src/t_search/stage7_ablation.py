"""Stage 7F ablation / reconstruction / mismatch diagnostics.

Stage 7A--E put explicit quantum records, internally anchored history, genuine
clock perspectives, event correspondence, and local memory accessibility into
one finite constrained construction.  Stage 7F now neutralizes those ingredients
one at a time and classifies the resulting *represented roles*.

The status vocabulary is deliberately functional rather than metaphysical:

- preserved: the role remains directly represented by the retained interface;
- reconstructible: an explicit ingredient is removed but the role is recovered
  from retained declared structure by an executable reconstruction witness;
- inaccessible: the global role remains represented but the declared local
  interface cannot access it;
- lost: the baseline role was represented and the declared ablation removes its
  current representation without a reconstruction witness;
- not_established: the retained structure does not license a verdict.

In particular, ``lost`` does not mean metaphysically irreducible and
``reconstructible`` does not mean universally redundant.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from functools import lru_cache
from itertools import permutations, product
from typing import Any

import numpy as np

from .stage3_asymmetry import orientation_from_scores
from .stage5_clock_change import DEFAULT_ATOL, SUBSYSTEMS
from .stage7_accessibility_atlas import (
    local_accessibility_assessment,
    partial_atlas_path_assessment,
)
from .stage7_history import (
    CURRENT_EVENT,
    LOWER_EVENT,
    UPPER_EVENT,
    assess_relational_record,
    canonical_history_model,
    canonical_physical_history_state,
)
from .stage7_record import (
    TARGET_LABEL,
    TARGET_POSITION,
    apply_record_write,
    canonical_record_source_state,
    stage7b_record_diagnostics,
    target_memory_joint_distribution,
)
from .stage7_record_transport import (
    history_clock_change_support_matrix,
    history_clock_reduction_coordinates,
    perspective_record_assessment,
    perspective_record_joint_distribution,
    reduced_history_support_coordinates,
)

ROLE_IDS: tuple[str, ...] = (
    "target_specific_record",
    "record_defined_direction",
    "local_record_readout",
    "perspective_transport",
    "P_R_covariance",
    "internal_history_anchor",
)

ABLATION_IDS: tuple[str, ...] = (
    "memory_removed",
    "record_coupling_neutralized",
    "history_anchor_removed",
    "explicit_perspective_maps_removed",
    "event_correspondence_removed",
    "local_access_hidden",
    "local_access_maximally_noisy",
)


class RoleStatus(str, Enum):
    PRESERVED = "preserved"
    RECONSTRUCTIBLE = "reconstructible"
    INACCESSIBLE = "inaccessible"
    LOST = "lost"
    NOT_ESTABLISHED = "not_established"


@dataclass(frozen=True)
class RoleEvidence:
    role: str
    direct_available: bool = False
    reconstruction_available: bool = False
    globally_represented: bool | None = None
    locally_accessible: bool | None = None
    decisive_loss: bool = False
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
            "measurements": dict(self.measurements),
            "note": self.note,
        }


@dataclass(frozen=True)
class AblationCase:
    ingredient: str
    neutralization: str
    probes: tuple[RoleEvidence, ...]

    def __post_init__(self) -> None:
        if self.ingredient not in ABLATION_IDS:
            raise ValueError(f"unknown Stage 7F ablation: {self.ingredient!r}")
        if tuple(probe.role for probe in self.probes) != ROLE_IDS:
            raise ValueError("Stage 7F probes must follow the frozen role order")

    def status(self, role: str) -> RoleStatus:
        return next(probe.status for probe in self.probes if probe.role == role)

    def as_dict(self) -> dict[str, Any]:
        return {
            "ingredient": self.ingredient,
            "neutralization": self.neutralization,
            "probes": [probe.as_dict() for probe in self.probes],
        }


@dataclass(frozen=True)
class PerspectiveReconstructionDiagnostics:
    comparisons: int
    max_reference_map_residual: float
    max_state_transport_residual: float
    max_inverse_residual: float
    max_metric_covariance_residual: float
    max_record_score_residual: float
    max_accessibility_residual: float
    reconstructible: bool


@dataclass(frozen=True)
class NoRecordPerspectiveDiagnostics:
    comparisons: int
    min_rank: int
    max_state_transport_residual: float
    max_inverse_residual: float
    max_metric_covariance_residual: float
    record_score: float
    accessibility_score: float
    record_defined: bool
    internally_anchored: bool
    perspective_structure_preserved: bool


@dataclass(frozen=True)
class MemoryRemovalDiagnostics:
    baseline_lower_information: float
    baseline_upper_information: float
    removed_lower_information: float
    removed_upper_information: float
    removed_record_score: float
    removed_accessibility_score: float
    removed_orientation: str
    record_survives_removal: bool


@dataclass(frozen=True)
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


@dataclass(frozen=True)
class RReconstructionDiagnostics:
    perspective_structure_preserved: bool
    history_anchor_preserved: bool
    no_record_record_defined: bool
    no_record_record_score: float
    no_record_accessibility_score: float
    p_and_o_retained_without_r: bool
    reconstruction_witness_found: bool


def _mi(joint: np.ndarray) -> float:
    probabilities = np.asarray(joint, dtype=float)
    total = float(np.sum(probabilities))
    if total <= 0.0:
        raise ValueError("joint distribution must have positive total mass")
    probabilities = probabilities / total
    px = np.sum(probabilities, axis=1, keepdims=True)
    py = np.sum(probabilities, axis=0, keepdims=True)
    independent = px @ py
    mask = probabilities > DEFAULT_ATOL
    if not np.any(mask):
        return 0.0
    return float(np.sum(probabilities[mask] * np.log2(probabilities[mask] / independent[mask])))


def _decoder_accuracy(joint: np.ndarray) -> float:
    probabilities = np.asarray(joint, dtype=float)
    return float(sum(np.max(probabilities[:, output]) for output in range(probabilities.shape[1])))


def _preserved(role: str, measurements: tuple[tuple[str, Any], ...] = (), note: str = "") -> RoleEvidence:
    return RoleEvidence(
        role=role,
        direct_available=True,
        globally_represented=True,
        locally_accessible=True if role == "local_record_readout" else None,
        measurements=measurements,
        note=note or "role remains directly represented after neutralization",
    )


def _reconstructible(role: str, measurements: tuple[tuple[str, Any], ...], note: str) -> RoleEvidence:
    return RoleEvidence(
        role=role,
        reconstruction_available=True,
        globally_represented=True,
        measurements=measurements,
        note=note,
    )


def _lost(role: str, measurements: tuple[tuple[str, Any], ...], note: str) -> RoleEvidence:
    return RoleEvidence(
        role=role,
        globally_represented=False,
        decisive_loss=True,
        measurements=measurements,
        note=note,
    )


def _inaccessible(role: str, measurements: tuple[tuple[str, Any], ...], note: str) -> RoleEvidence:
    return RoleEvidence(
        role=role,
        globally_represented=True,
        locally_accessible=False,
        measurements=measurements,
        note=note,
    )


def _not_established(role: str, measurements: tuple[tuple[str, Any], ...], note: str) -> RoleEvidence:
    return RoleEvidence(role=role, measurements=measurements, note=note)


def _metric_from_coordinates(coordinates: np.ndarray) -> np.ndarray:
    inverse = np.linalg.inv(coordinates)
    return inverse.conj().T @ inverse


def _node_cache(kind: str) -> dict[tuple[str, int], tuple[np.ndarray, np.ndarray, np.ndarray]]:
    state = canonical_physical_history_state(kind)  # type: ignore[arg-type]
    nodes: dict[tuple[str, int], tuple[np.ndarray, np.ndarray, np.ndarray]] = {}
    for clock in SUBSYSTEMS:
        for index in range(3):
            coordinates = history_clock_reduction_coordinates(kind, clock, index)  # type: ignore[arg-type]
            metric = _metric_from_coordinates(coordinates)
            state_coordinates = reduced_history_support_coordinates(
                state, kind, clock, index  # type: ignore[arg-type]
            )
            nodes[(clock, index)] = (coordinates, metric, state_coordinates)
    return nodes


@lru_cache(maxsize=1)
def perspective_reconstruction_diagnostics() -> PerspectiveReconstructionDiagnostics:
    """Remove explicit Stage 7D edge maps and rebuild them from per-node reductions."""

    nodes = _node_cache("forward")
    reference = perspective_record_assessment("A", CURRENT_EVENT, chi="preserving")
    comparisons = 0
    max_reference = 0.0
    max_state = 0.0
    max_inverse = 0.0
    max_metric = 0.0
    max_record = 0.0
    max_access = 0.0

    for source_clock, target_clock in permutations(SUBSYSTEMS, 2):
        for source_index, target_index in product(range(3), repeat=2):
            source_c, source_metric, source_state = nodes[(source_clock, source_index)]
            target_c, target_metric, target_state = nodes[(target_clock, target_index)]
            reconstructed = target_c @ np.linalg.inv(source_c)
            reverse = source_c @ np.linalg.inv(target_c)
            direct_reference = history_clock_change_support_matrix(
                "forward", target_clock, target_index, source_clock, source_index
            )
            max_reference = max(max_reference, float(np.linalg.norm(reconstructed - direct_reference)))
            max_state = max(max_state, float(np.linalg.norm(reconstructed @ source_state - target_state)))
            max_inverse = max(max_inverse, float(np.linalg.norm(reverse @ reconstructed - np.eye(14))))
            max_metric = max(
                max_metric,
                float(np.linalg.norm(reconstructed.conj().T @ target_metric @ reconstructed - source_metric)),
            )
            target_record = perspective_record_assessment(
                target_clock, target_index, chi="preserving"
            )
            max_record = max(max_record, abs(target_record.record_score - reference.record_score))
            max_access = max(
                max_access,
                abs(target_record.accessibility_score - reference.accessibility_score),
            )
            comparisons += 1

    reconstructible = bool(
        comparisons == 54
        and max_reference <= 1e-9
        and max_state <= 1e-9
        and max_inverse <= 1e-9
        and max_metric <= 1e-9
        and max_record <= 1e-9
        and max_access <= 1e-9
    )
    return PerspectiveReconstructionDiagnostics(
        comparisons=comparisons,
        max_reference_map_residual=max_reference,
        max_state_transport_residual=max_state,
        max_inverse_residual=max_inverse,
        max_metric_covariance_residual=max_metric,
        max_record_score_residual=max_record,
        max_accessibility_residual=max_access,
        reconstructible=reconstructible,
    )


@lru_cache(maxsize=1)
def no_record_perspective_diagnostics() -> NoRecordPerspectiveDiagnostics:
    """Retain the internal history anchor and clock perspectives while removing record coupling."""

    nodes = _node_cache("no-record")
    comparisons = 0
    min_rank = 14
    max_state = 0.0
    max_inverse = 0.0
    max_metric = 0.0
    for source_clock, target_clock in permutations(SUBSYSTEMS, 2):
        for source_index, target_index in product(range(3), repeat=2):
            source_c, source_metric, source_state = nodes[(source_clock, source_index)]
            target_c, target_metric, target_state = nodes[(target_clock, target_index)]
            min_rank = min(
                min_rank,
                int(np.linalg.matrix_rank(source_c, tol=DEFAULT_ATOL)),
                int(np.linalg.matrix_rank(target_c, tol=DEFAULT_ATOL)),
            )
            transform = target_c @ np.linalg.inv(source_c)
            reverse = source_c @ np.linalg.inv(target_c)
            max_state = max(max_state, float(np.linalg.norm(transform @ source_state - target_state)))
            max_inverse = max(max_inverse, float(np.linalg.norm(reverse @ transform - np.eye(14))))
            max_metric = max(
                max_metric,
                float(np.linalg.norm(transform.conj().T @ target_metric @ transform - source_metric)),
            )
            comparisons += 1

    record = assess_relational_record("no-record")
    preserved = bool(
        comparisons == 54
        and min_rank == 14
        and max_state <= 1e-9
        and max_inverse <= 1e-9
        and max_metric <= 1e-9
    )
    return NoRecordPerspectiveDiagnostics(
        comparisons=comparisons,
        min_rank=min_rank,
        max_state_transport_residual=max_state,
        max_inverse_residual=max_inverse,
        max_metric_covariance_residual=max_metric,
        record_score=record.record_score,
        accessibility_score=record.accessibility_score,
        record_defined=record.record_defined,
        internally_anchored=record.internally_anchored,
        perspective_structure_preserved=preserved,
    )


@lru_cache(maxsize=1)
def memory_removal_diagnostics() -> MemoryRemovalDiagnostics:
    """Discard the memory carrier from the retained record description.

    This is distinct from Stage 7E hidden access.  Here the memory variable is
    removed from the retained carrier by collapsing the memory outcome itself;
    therefore no global target-memory correlation remains in the ablated model.
    """

    lower, *_ = perspective_record_joint_distribution("A", CURRENT_EVENT, LOWER_EVENT)
    upper, *_ = perspective_record_joint_distribution("A", CURRENT_EVENT, UPPER_EVENT)
    baseline_lower = _mi(lower)
    baseline_upper = _mi(upper)
    removed_lower_joint = np.sum(lower, axis=1, keepdims=True)
    removed_upper_joint = np.sum(upper, axis=1, keepdims=True)
    removed_lower = _mi(removed_lower_joint)
    removed_upper = _mi(removed_upper_joint)
    removed_lower_accuracy = _decoder_accuracy(removed_lower_joint)
    removed_upper_accuracy = _decoder_accuracy(removed_upper_joint)
    record_score = removed_lower - removed_upper
    accessibility_score = removed_lower_accuracy - removed_upper_accuracy
    orientation = orientation_from_scores(record_score, accessibility_score, tolerance=1e-10)
    return MemoryRemovalDiagnostics(
        baseline_lower_information=baseline_lower,
        baseline_upper_information=baseline_upper,
        removed_lower_information=removed_lower,
        removed_upper_information=removed_upper,
        removed_record_score=record_score,
        removed_accessibility_score=accessibility_score,
        removed_orientation=orientation,
        record_survives_removal=bool(
            abs(record_score) > 1e-10 or abs(accessibility_score) > 1e-10
        ),
    )


@lru_cache(maxsize=1)
def baseline_role_evidence() -> tuple[RoleEvidence, ...]:
    record = perspective_record_assessment("A", CURRENT_EVENT, chi="preserving")
    access = local_accessibility_assessment("A", CURRENT_EVENT, "full")
    reconstruction = perspective_reconstruction_diagnostics()
    history = assess_relational_record("forward")
    return (
        _preserved(
            "target_specific_record",
            (("record_score", record.record_score), ("lower_information", record.lower_information)),
        ),
        _preserved(
            "record_defined_direction",
            (("record_score", record.record_score), ("orientation", record.orientation)),
        ),
        _preserved(
            "local_record_readout",
            (("locally_accessible", access.locally_accessible), ("local_record_score", access.local_record_score)),
        ),
        _preserved(
            "perspective_transport",
            (("comparisons", reconstruction.comparisons), ("max_state_residual", reconstruction.max_state_transport_residual)),
        ),
        _preserved(
            "P_R_covariance",
            (("max_record_score_residual", reconstruction.max_record_score_residual),),
        ),
        _preserved(
            "internal_history_anchor",
            (("internally_anchored", history.internally_anchored),),
        ),
    )


def _memory_removed_case() -> AblationCase:
    diagnostic = memory_removal_diagnostics()
    p = perspective_reconstruction_diagnostics()
    return AblationCase(
        ingredient="memory_removed",
        neutralization="discard M from the retained record carrier while retaining the A/B/C clock carrier",
        probes=(
            _lost(
                "target_specific_record",
                (("removed_lower_information", diagnostic.removed_lower_information), ("removed_upper_information", diagnostic.removed_upper_information)),
                "without a retained memory variable there is no target-memory record relation",
            ),
            _lost(
                "record_defined_direction",
                (("record_score", diagnostic.removed_record_score), ("orientation", diagnostic.removed_orientation)),
                "the directional record contrast vanishes after memory removal",
            ),
            _lost(
                "local_record_readout",
                (("accessibility_score", diagnostic.removed_accessibility_score),),
                "there is no memory readout endpoint after M is removed",
            ),
            _preserved(
                "perspective_transport",
                (("reconstructed_map_comparisons", p.comparisons),),
                "the A/B/C physical clock carrier is retained independently of the removed record memory",
            ),
            _not_established(
                "P_R_covariance",
                (("record_survives_removal", diagnostic.record_survives_removal),),
                "P-R covariance has no positive R endpoint after memory removal",
            ),
            _preserved("internal_history_anchor", (("event_labels_retained", True),)),
        ),
    )


def _record_coupling_case() -> AblationCase:
    diagnostic = no_record_perspective_diagnostics()
    return AblationCase(
        ingredient="record_coupling_neutralized",
        neutralization="use the internally anchored no-record history with the record write replaced by identity",
        probes=(
            _lost(
                "target_specific_record",
                (("record_defined", diagnostic.record_defined), ("record_score", diagnostic.record_score)),
                "the no-record construction carries no positive target-specific record witness",
            ),
            _lost(
                "record_defined_direction",
                (("record_score", diagnostic.record_score), ("accessibility_score", diagnostic.accessibility_score)),
                "retaining order and perspectives does not recreate the record-defined direction",
            ),
            _lost(
                "local_record_readout",
                (("record_defined", diagnostic.record_defined),),
                "the readout endpoint exists but contains no record information to access",
            ),
            _preserved(
                "perspective_transport",
                (("comparisons", diagnostic.comparisons), ("max_metric_residual", diagnostic.max_metric_covariance_residual)),
                "the no-record constrained family still admits the tested full-rank multi-clock maps",
            ),
            _not_established(
                "P_R_covariance",
                (("record_defined", diagnostic.record_defined),),
                "with R neutralized, positive P-R covariance is not an applicable surviving role",
            ),
            _preserved(
                "internal_history_anchor",
                (("internally_anchored", diagnostic.internally_anchored),),
                "the no-record control retains the e0<e1<e2 internal anchor",
            ),
        ),
    )


def _history_anchor_case() -> AblationCase:
    record = stage7b_record_diagnostics()
    p = perspective_reconstruction_diagnostics()
    return AblationCase(
        ingredient="history_anchor_removed",
        neutralization="fall back to the Stage 7B reversible target-specific record witness without an internally modeled event history",
        probes=(
            _preserved(
                "target_specific_record",
                (("target_information_after", record.target_information_after), ("positive_witness", record.positive_target_specific_record_witness)),
                "target-specific record correlation survives without directional history semantics",
            ),
            _not_established(
                "record_defined_direction",
                (("directional_score_defined", record.directional_score_defined),),
                "record correlation alone does not define lower-versus-upper temporal orientation",
            ),
            _preserved(
                "local_record_readout",
                (("target_information_after", record.target_information_after),),
                "the computational memory readout still exposes the target-specific record",
            ),
            _preserved(
                "perspective_transport",
                (("clock_carrier_reconstructible", p.reconstructible),),
                "removing the Stage 7C history anchor does not remove the inherited constrained clock carrier",
            ),
            _not_established(
                "P_R_covariance",
                (("directional_score_defined", record.directional_score_defined),),
                "the directional record correspondence required for Stage 7D covariance is absent",
            ),
            _lost(
                "internal_history_anchor",
                (("directional_score_defined", record.directional_score_defined),),
                "Stage 7B explicitly has no internally anchored relational history",
            ),
        ),
    )


def _explicit_map_case() -> AblationCase:
    diagnostic = perspective_reconstruction_diagnostics()
    measurements = (
        ("comparisons", diagnostic.comparisons),
        ("max_reference_map_residual", diagnostic.max_reference_map_residual),
        ("max_state_transport_residual", diagnostic.max_state_transport_residual),
        ("max_metric_covariance_residual", diagnostic.max_metric_covariance_residual),
    )
    return AblationCase(
        ingredient="explicit_perspective_maps_removed",
        neutralization="remove explicit cross-clock edge matrices but retain the common physical carrier and per-node reductions C_X",
        probes=(
            _preserved("target_specific_record"),
            _preserved("record_defined_direction"),
            _preserved("local_record_readout"),
            _reconstructible(
                "perspective_transport",
                measurements,
                "clock-change maps are recovered as C_Y @ inv(C_X)",
            ),
            _reconstructible(
                "P_R_covariance",
                (("max_record_score_residual", diagnostic.max_record_score_residual), ("max_accessibility_residual", diagnostic.max_accessibility_residual)),
                "record covariance is recovered after rebuilding the perspective maps from retained reductions",
            ),
            _preserved("internal_history_anchor"),
        ),
    )


def _chi_removed_case() -> AblationCase:
    record = perspective_record_assessment("A", CURRENT_EVENT, chi="preserving")
    return AblationCase(
        ingredient="event_correspondence_removed",
        neutralization="retain local perspectives and records but withhold cross-perspective event correspondence chi",
        probes=(
            _preserved("target_specific_record", (("local_record_score", record.record_score),)),
            _preserved("record_defined_direction", (("local_orientation", record.orientation),)),
            _preserved("local_record_readout"),
            _preserved("perspective_transport"),
            _not_established(
                "P_R_covariance",
                (("chi_declared", False),),
                "cross-perspective record covariance cannot be interpreted without an event correspondence",
            ),
            _preserved("internal_history_anchor"),
        ),
    )


def _access_case(interface: str) -> AblationCase:
    access = local_accessibility_assessment("B", 0, interface)  # type: ignore[arg-type]
    return AblationCase(
        ingredient=(
            "local_access_hidden" if interface == "hidden" else "local_access_maximally_noisy"
        ),
        neutralization=f"replace full memory readout by the {interface} Stage 7E channel",
        probes=(
            _preserved(
                "target_specific_record",
                (("global_record_score", access.global_record_score), ("globally_represented", access.globally_represented)),
            ),
            _preserved(
                "record_defined_direction",
                (("global_orientation", access.global_orientation),),
            ),
            _inaccessible(
                "local_record_readout",
                (("local_record_score", access.local_record_score), ("local_accessibility_score", access.local_accessibility_score)),
                "the global record remains represented while this declared interface exposes no local record information",
            ),
            _preserved("perspective_transport"),
            _preserved(
                "P_R_covariance",
                (("global_record_score", access.global_record_score),),
                "global record covariance is unchanged because only the local readout channel is replaced",
            ),
            _preserved("internal_history_anchor"),
        ),
    )


@lru_cache(maxsize=1)
def build_stage7f_ablation_matrix() -> tuple[AblationCase, ...]:
    return (
        _memory_removed_case(),
        _record_coupling_case(),
        _history_anchor_case(),
        _explicit_map_case(),
        _chi_removed_case(),
        _access_case("hidden"),
        _access_case("maximally-noisy"),
    )


def _wrong_chi_mismatch() -> MismatchDiagnostic:
    source = perspective_record_assessment("A", CURRENT_EVENT, chi="preserving")
    wrong = perspective_record_assessment("B", 0, chi="misdeclared-preserving")
    record_residual = abs(wrong.record_score - source.record_score)
    access_residual = abs(wrong.accessibility_score - source.accessibility_score)
    return MismatchDiagnostic(
        mismatch="wrong_or_misdeclared_chi",
        affected_role="P_R_covariance",
        detected=bool(record_residual > 1e-3 and access_residual > 1e-3),
        measurements=(
            ("record_score_residual", record_residual),
            ("accessibility_score_residual", access_residual),
            ("source_orientation", source.orientation),
            ("wrong_orientation", wrong.orientation),
        ),
        note="wrong event correspondence breaks the declared covariance comparison without deleting P or R themselves",
    )


def _perturbed_edge_mismatch() -> MismatchDiagnostic:
    affected = partial_atlas_path_assessment(1, perturb_local_edge=True)
    unaffected = [partial_atlas_path_assessment(index) for index in (0, 2)]
    detected = bool(
        affected.map_residual > 1e-3
        and affected.state_residual > 1e-3
        and affected.metric_covariance_residual > 1e-3
        and affected.record_score_residual > 1e-4
        and all(item.consistent for item in unaffected)
    )
    return MismatchDiagnostic(
        mismatch="perturbed_local_perspective_edge",
        affected_role="path_specific_P_R_covariance",
        detected=detected,
        measurements=(
            ("map_residual", affected.map_residual),
            ("state_residual", affected.state_residual),
            ("metric_residual", affected.metric_covariance_residual),
            ("observable_residual", affected.max_observable_residual),
            ("record_score_residual", affected.record_score_residual),
            ("unaffected_paths_consistent", all(item.consistent for item in unaffected)),
        ),
        note="one perturbed primitive edge is localized by map/state/metric/record diagnostics even when the tested projector algebra still transports",
    )


@lru_cache(maxsize=1)
def stage7f_mismatch_matrix() -> tuple[MismatchDiagnostic, ...]:
    return (_wrong_chi_mismatch(), _perturbed_edge_mismatch())


@lru_cache(maxsize=1)
def r_reconstruction_from_p_o_diagnostics() -> RReconstructionDiagnostics:
    no_record = no_record_perspective_diagnostics()
    p_and_o_without_r = bool(
        no_record.perspective_structure_preserved
        and no_record.internally_anchored
        and not no_record.record_defined
        and abs(no_record.record_score) <= 1e-10
        and abs(no_record.accessibility_score) <= 1e-10
    )
    return RReconstructionDiagnostics(
        perspective_structure_preserved=no_record.perspective_structure_preserved,
        history_anchor_preserved=no_record.internally_anchored,
        no_record_record_defined=no_record.record_defined,
        no_record_record_score=no_record.record_score,
        no_record_accessibility_score=no_record.accessibility_score,
        p_and_o_retained_without_r=p_and_o_without_r,
        reconstruction_witness_found=False,
    )


def stage7f_summary() -> dict[str, object]:
    baseline = baseline_role_evidence()
    cases = build_stage7f_ablation_matrix()
    mismatches = stage7f_mismatch_matrix()
    reconstruction = r_reconstruction_from_p_o_diagnostics()
    own_role_status = {
        "memory_record_resource": next(
            case for case in cases if case.ingredient == "memory_removed"
        ).status("target_specific_record").value,
        "record_coupling": next(
            case for case in cases if case.ingredient == "record_coupling_neutralized"
        ).status("record_defined_direction").value,
        "history_anchor": next(
            case for case in cases if case.ingredient == "history_anchor_removed"
        ).status("internal_history_anchor").value,
        "explicit_perspective_maps": next(
            case for case in cases if case.ingredient == "explicit_perspective_maps_removed"
        ).status("perspective_transport").value,
        "event_correspondence_for_P_R": next(
            case for case in cases if case.ingredient == "event_correspondence_removed"
        ).status("P_R_covariance").value,
        "hidden_local_access": next(
            case for case in cases if case.ingredient == "local_access_hidden"
        ).status("local_record_readout").value,
    }
    return {
        "status_vocabulary": [status.value for status in RoleStatus],
        "roles": list(ROLE_IDS),
        "baseline": [probe.as_dict() for probe in baseline],
        "ablations": [case.as_dict() for case in cases],
        "mismatches": [item.as_dict() for item in mismatches],
        "own_role_status_after_neutralization": own_role_status,
        "r_reconstruction_from_p_o": asdict(reconstruction),
        "bounded_interpretation": {
            "P_plus_O_implies_R_in_declared_stage7_family": False,
            "explicit_cross_clock_edge_matrices_are_primitive_in_declared_interface": False,
            "R_metaphysically_irreducible": False,
            "P_universally_redundant": False,
            "inaccessible_means_globally_absent": False,
            "not_established_means_false": False,
        },
        "guards": [
            "lost != metaphysically irreducible",
            "reconstructible != universally redundant",
            "target-specific record correlation != record-defined direction",
            "P + O retained without R != proof that P/O can never generate records in another model",
            "local inaccessibility != global record absence",
            "missing chi != false covariance; it makes the cross-perspective comparison not established",
            "wrong chi mismatch != destruction of P or R",
            "explicit perspective-map reconstruction != elimination of the perspective layer",
            "localized path mismatch != spacetime curvature",
            "not_established != false",
        ],
    }
