"""Stage 6D horizontal/vertical compatibility utilities.

Stage 6C represented physical-clock perspective changes as horizontal maps in a
partial atlas.  Stage 6D adds a separately typed vertical conditioning structure
and asks whether the two structures are compatible under an explicit event
correspondence ``chi``.

Horizontal maps remain Stage 5/6C support-space perspective transformations.
Vertical maps are induced from one common reversible conditioning family on the
constrained physical-support coordinates and then represented separately in each
clock perspective.  Commuting squares therefore test compatibility between two
arrow types; they do not identify a perspective change with temporal succession.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, permutations, product
from typing import Any, Iterable

import numpy as np

from .stage5_clock_change import DEFAULT_ATOL, DEFAULT_DIMENSION, DEFAULT_RATES, SUBSYSTEMS
from .stage5_reductions import support_coordinate_reduction_matrix
from .stage6_partial_atlas import (
    PerspectiveNode,
    build_partial_clock_atlas,
    indirect_paths,
)

VERTICAL_GENERATOR_SCALE = 0.37


@dataclass(frozen=True, order=True)
class Event:
    """One explicitly declared vertical event label and order coordinate."""

    label: str
    coordinate: float

    def as_dict(self) -> dict[str, Any]:
        return {"label": self.label, "coordinate": self.coordinate}


CANONICAL_EVENTS: tuple[Event, ...] = (
    Event("e0", 0.0),
    Event("e1", 1.0),
    Event("e2", 3.0),
)


@dataclass(frozen=True)
class EventCorrespondence:
    """Explicit event correspondence between two perspective domains.

    The mapping is declared independently of clock-reading equality.  The
    ``orientation`` field states the expected order rule and is used only by the
    order-covariance diagnostic; it does not change horizontal map direction.
    """

    source: PerspectiveNode
    target: PerspectiveNode
    mapping: tuple[tuple[str, str], ...]
    orientation: str = "preserving"

    def __post_init__(self) -> None:
        if self.orientation not in {"preserving", "reversing"}:
            raise ValueError("event correspondence orientation must be preserving or reversing")
        source_labels = [source for source, _target in self.mapping]
        if len(set(source_labels)) != len(source_labels):
            raise ValueError("event correspondence contains duplicate source labels")

    def target_label(self, source_label: str) -> str:
        matches = [target for source, target in self.mapping if source == source_label]
        if not matches:
            raise KeyError(f"event correspondence has no image for {source_label!r}")
        if len(matches) != 1:
            raise RuntimeError("duplicate event correspondence escaped validation")
        return matches[0]

    def as_dict(self) -> dict[str, Any]:
        return {
            "source": self.source.label,
            "target": self.target.label,
            "mapping": {source: target for source, target in self.mapping},
            "orientation": self.orientation,
        }


@dataclass(frozen=True)
class CompatibilityDiagnostics:
    """Compatibility diagnostics for one source/target perspective pair."""

    source: PerspectiveNode
    target: PerspectiveNode
    path_count: int
    event_relation_count: int
    square_count: int
    max_horizontal_bridge_residual: float
    max_square_residual: float
    order_violation_count: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "source": self.source.label,
            "target": self.target.label,
            "path_count": self.path_count,
            "event_relation_count": self.event_relation_count,
            "square_count": self.square_count,
            "max_horizontal_bridge_residual": self.max_horizontal_bridge_residual,
            "max_square_residual": self.max_square_residual,
            "order_violation_count": self.order_violation_count,
        }


@dataclass(frozen=True)
class CompatibilityFamilyScan:
    """Exhaustive Stage 6D scan over the canonical qutrit perspective family."""

    endpoint_case_count: int
    indirect_path_count: int
    event_relation_count: int
    square_count: int
    max_horizontal_bridge_residual: float
    max_square_residual: float
    order_violation_count: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "endpoint_case_count": self.endpoint_case_count,
            "indirect_path_count": self.indirect_path_count,
            "event_relation_count": self.event_relation_count,
            "square_count": self.square_count,
            "max_horizontal_bridge_residual": self.max_horizontal_bridge_residual,
            "max_square_residual": self.max_square_residual,
            "order_violation_count": self.order_violation_count,
        }


@dataclass(frozen=True)
class MismatchControlDiagnostics:
    """Deliberately wrong event-correspondence control for one canonical path."""

    source: PerspectiveNode
    target: PerspectiveNode
    path: tuple[str, ...]
    topology_unchanged: bool
    canonical_max_square_residual: float
    mismatch_max_square_residual: float
    mismatch_failed_square_count: int
    canonical_order_violation_count: int
    mismatch_order_violation_count: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "source": self.source.label,
            "target": self.target.label,
            "path": list(self.path),
            "topology_unchanged": self.topology_unchanged,
            "canonical_max_square_residual": self.canonical_max_square_residual,
            "mismatch_max_square_residual": self.mismatch_max_square_residual,
            "mismatch_failed_square_count": self.mismatch_failed_square_count,
            "canonical_order_violation_count": self.canonical_order_violation_count,
            "mismatch_order_violation_count": self.mismatch_order_violation_count,
        }


def _event_lookup(events: Iterable[Event]) -> dict[str, Event]:
    event_tuple = tuple(events)
    labels = [event.label for event in event_tuple]
    if len(set(labels)) != len(labels):
        raise ValueError("event family contains duplicate labels")
    return {event.label: event for event in event_tuple}


def ordered_event_relations(
    events: Iterable[Event] = CANONICAL_EVENTS,
) -> tuple[tuple[Event, Event], ...]:
    """Return all strictly forward declared event relations by coordinate."""

    event_tuple = tuple(events)
    _event_lookup(event_tuple)
    return tuple(
        (source, target)
        for source, target in combinations(event_tuple, 2)
        if source.coordinate < target.coordinate
    )


def identity_event_correspondence(
    source: PerspectiveNode,
    target: PerspectiveNode,
    events: Iterable[Event] = CANONICAL_EVENTS,
) -> EventCorrespondence:
    """Return an explicit orientation-preserving label correspondence."""

    event_tuple = tuple(events)
    _event_lookup(event_tuple)
    return EventCorrespondence(
        source=source,
        target=target,
        mapping=tuple((event.label, event.label) for event in event_tuple),
        orientation="preserving",
    )


def mismatched_event_correspondence(
    source: PerspectiveNode,
    target: PerspectiveNode,
) -> EventCorrespondence:
    """Return the frozen Stage 6D mismatch control.

    The event labels ``e1`` and ``e2`` are swapped while the correspondence is
    still *declared* orientation-preserving.  This is intentionally inconsistent
    with the canonical event order and should break both order covariance and
    the affected commuting squares.
    """

    return EventCorrespondence(
        source=source,
        target=target,
        mapping=(("e0", "e0"), ("e1", "e2"), ("e2", "e1")),
        orientation="preserving",
    )


def common_vertical_conditioning_matrix(
    source_event: Event,
    target_event: Event,
    support_dimension: int,
) -> np.ndarray:
    """Return the common reversible vertical conditioning map on H_phys support.

    This is a deliberately simple finite-dimensional conditioning family.  The
    unequal canonical event spacings make the mismatch control discriminating.
    Its role is vertical succession/conditioning in the toy model, not a claim
    of a fundamental Hamiltonian of time.
    """

    if support_dimension < 1:
        raise ValueError("support dimension must be positive")
    centered = np.arange(support_dimension, dtype=float) - (support_dimension - 1) / 2.0
    delta = float(target_event.coordinate - source_event.coordinate)
    phases = np.exp(-1j * VERTICAL_GENERATOR_SCALE * centered * delta)
    return np.diag(phases.astype(np.complex128))


def perspective_vertical_map(
    perspective: PerspectiveNode,
    source_event: Event,
    target_event: Event,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Represent the common vertical map in one clock-perspective support."""

    rate_tuple = tuple(rates)
    reduction = support_coordinate_reduction_matrix(
        perspective.clock,
        perspective.index,
        dimension,
        rates=rate_tuple,
    )
    common = common_vertical_conditioning_matrix(
        source_event,
        target_event,
        reduction.shape[1],
    )
    return reduction @ common @ reduction.conj().T


def horizontal_bridge_reference(
    source: PerspectiveNode,
    target: PerspectiveNode,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Return R_target R_source^dagger in support coordinates.

    This common-physical-space bridge is used only as a diagnostic reference.
    Stage 6D horizontal maps themselves are composed from Stage 6C atlas edges.
    """

    rate_tuple = tuple(rates)
    source_reduction = support_coordinate_reduction_matrix(
        source.clock,
        source.index,
        dimension,
        rates=rate_tuple,
    )
    target_reduction = support_coordinate_reduction_matrix(
        target.clock,
        target.index,
        dimension,
        rates=rate_tuple,
    )
    return target_reduction @ source_reduction.conj().T


def mapped_event(
    correspondence: EventCorrespondence,
    source_event: Event,
    target_events: Iterable[Event] = CANONICAL_EVENTS,
) -> Event:
    """Apply explicit ``chi`` to one event label."""

    lookup = _event_lookup(target_events)
    label = correspondence.target_label(source_event.label)
    if label not in lookup:
        raise KeyError(f"mapped event {label!r} is absent from target event family")
    return lookup[label]


def order_covariant(
    correspondence: EventCorrespondence,
    source_event: Event,
    target_event: Event,
    target_events: Iterable[Event] = CANONICAL_EVENTS,
) -> bool:
    """Check the declared order rule under explicit event correspondence."""

    if source_event.coordinate >= target_event.coordinate:
        raise ValueError("order covariance diagnostic requires a strictly forward source relation")
    mapped_source = mapped_event(correspondence, source_event, target_events)
    mapped_target = mapped_event(correspondence, target_event, target_events)
    if correspondence.orientation == "preserving":
        return mapped_source.coordinate < mapped_target.coordinate
    return mapped_source.coordinate > mapped_target.coordinate


def compatibility_square_residual(
    horizontal_map: np.ndarray,
    source_vertical: np.ndarray,
    target_vertical: np.ndarray,
) -> float:
    """Return ||M D_source - D_target M||_F."""

    horizontal = np.asarray(horizontal_map, dtype=np.complex128)
    d_source = np.asarray(source_vertical, dtype=np.complex128)
    d_target = np.asarray(target_vertical, dtype=np.complex128)
    return float(np.linalg.norm(horizontal @ d_source - d_target @ horizontal))


def square_residual_for_correspondence(
    horizontal_map: np.ndarray,
    source: PerspectiveNode,
    target: PerspectiveNode,
    source_event: Event,
    target_event: Event,
    correspondence: EventCorrespondence,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    target_events: Iterable[Event] = CANONICAL_EVENTS,
) -> float:
    """Evaluate one horizontal/vertical compatibility square."""

    if correspondence.source != source or correspondence.target != target:
        raise ValueError("event correspondence endpoints do not match square perspectives")
    rate_tuple = tuple(rates)
    mapped_source = mapped_event(correspondence, source_event, target_events)
    mapped_target = mapped_event(correspondence, target_event, target_events)
    source_vertical = perspective_vertical_map(
        source,
        source_event,
        target_event,
        dimension,
        rates=rate_tuple,
    )
    target_vertical = perspective_vertical_map(
        target,
        mapped_source,
        mapped_target,
        dimension,
        rates=rate_tuple,
    )
    return compatibility_square_residual(horizontal_map, source_vertical, target_vertical)


def compatibility_diagnostics(
    source: PerspectiveNode,
    target: PerspectiveNode,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    tolerance: float = DEFAULT_ATOL,
    events: Iterable[Event] = CANONICAL_EVENTS,
) -> CompatibilityDiagnostics:
    """Evaluate all Stage 6C two-hop paths for one perspective endpoint pair."""

    rate_tuple = tuple(rates)
    event_tuple = tuple(events)
    relations = ordered_event_relations(event_tuple)
    atlas = build_partial_clock_atlas(
        source,
        target,
        dimension,
        rates=rate_tuple,
        tolerance=tolerance,
    )
    paths = indirect_paths(atlas, source, target)
    if not paths:
        raise RuntimeError("Stage 6D requires at least one horizontal reconstruction path")
    correspondence = identity_event_correspondence(source, target, event_tuple)
    bridge = horizontal_bridge_reference(source, target, dimension, rates=rate_tuple)

    bridge_residuals: list[float] = []
    square_residuals: list[float] = []
    for path in paths:
        horizontal = atlas.compose_path(path)
        bridge_residuals.append(float(np.linalg.norm(horizontal - bridge)))
        for source_event, target_event in relations:
            square_residuals.append(
                square_residual_for_correspondence(
                    horizontal,
                    source,
                    target,
                    source_event,
                    target_event,
                    correspondence,
                    dimension,
                    rates=rate_tuple,
                    target_events=event_tuple,
                )
            )

    order_violations = sum(
        not order_covariant(correspondence, source_event, target_event, event_tuple)
        for source_event, target_event in relations
    )
    return CompatibilityDiagnostics(
        source=source,
        target=target,
        path_count=len(paths),
        event_relation_count=len(relations),
        square_count=len(paths) * len(relations),
        max_horizontal_bridge_residual=max(bridge_residuals),
        max_square_residual=max(square_residuals),
        order_violation_count=order_violations,
    )


def canonical_stage6d_diagnostics() -> CompatibilityDiagnostics:
    """Return the canonical C0 -> B2 Stage 6D compatibility case."""

    return compatibility_diagnostics(PerspectiveNode("C", 0), PerspectiveNode("B", 2))


def scan_horizontal_vertical_compatibility(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    tolerance: float = DEFAULT_ATOL,
    events: Iterable[Event] = CANONICAL_EVENTS,
) -> CompatibilityFamilyScan:
    """Exhaustively scan all ordered distinct-clock endpoint/readout pairs."""

    rate_tuple = tuple(rates)
    event_tuple = tuple(events)
    endpoint_diagnostics: list[CompatibilityDiagnostics] = []
    for source_clock, target_clock in permutations(SUBSYSTEMS, 2):
        for source_index, target_index in product(range(dimension), repeat=2):
            endpoint_diagnostics.append(
                compatibility_diagnostics(
                    PerspectiveNode(source_clock, source_index),
                    PerspectiveNode(target_clock, target_index),
                    dimension,
                    rates=rate_tuple,
                    tolerance=tolerance,
                    events=event_tuple,
                )
            )

    return CompatibilityFamilyScan(
        endpoint_case_count=len(endpoint_diagnostics),
        indirect_path_count=sum(item.path_count for item in endpoint_diagnostics),
        event_relation_count=sum(item.event_relation_count for item in endpoint_diagnostics),
        square_count=sum(item.square_count for item in endpoint_diagnostics),
        max_horizontal_bridge_residual=max(
            item.max_horizontal_bridge_residual for item in endpoint_diagnostics
        ),
        max_square_residual=max(item.max_square_residual for item in endpoint_diagnostics),
        order_violation_count=sum(item.order_violation_count for item in endpoint_diagnostics),
    )


def mismatch_control_diagnostics(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    tolerance: float = DEFAULT_ATOL,
) -> MismatchControlDiagnostics:
    """Apply the deliberately wrong ``chi`` while leaving atlas topology fixed."""

    source = PerspectiveNode("C", 0)
    target = PerspectiveNode("B", 2)
    rate_tuple = tuple(rates)
    atlas = build_partial_clock_atlas(
        source,
        target,
        dimension,
        rates=rate_tuple,
        tolerance=tolerance,
    )
    paths = indirect_paths(atlas, source, target)
    selected = next(path for path in paths if path[1].index == 1)
    horizontal = atlas.compose_path(selected)
    relations = ordered_event_relations(CANONICAL_EVENTS)

    canonical = identity_event_correspondence(source, target, CANONICAL_EVENTS)
    mismatch = mismatched_event_correspondence(source, target)
    canonical_residuals = tuple(
        square_residual_for_correspondence(
            horizontal,
            source,
            target,
            source_event,
            target_event,
            canonical,
            dimension,
            rates=rate_tuple,
        )
        for source_event, target_event in relations
    )
    mismatch_residuals = tuple(
        square_residual_for_correspondence(
            horizontal,
            source,
            target,
            source_event,
            target_event,
            mismatch,
            dimension,
            rates=rate_tuple,
        )
        for source_event, target_event in relations
    )

    canonical_order_violations = sum(
        not order_covariant(canonical, source_event, target_event)
        for source_event, target_event in relations
    )
    mismatch_order_violations = sum(
        not order_covariant(mismatch, source_event, target_event)
        for source_event, target_event in relations
    )

    return MismatchControlDiagnostics(
        source=source,
        target=target,
        path=tuple(node.label for node in selected),
        topology_unchanged=(
            atlas.has_perspective(target)
            and not atlas.has_direct_map(source, target)
            and len(paths) == dimension
        ),
        canonical_max_square_residual=max(canonical_residuals),
        mismatch_max_square_residual=max(mismatch_residuals),
        mismatch_failed_square_count=sum(residual > tolerance for residual in mismatch_residuals),
        canonical_order_violation_count=canonical_order_violations,
        mismatch_order_violation_count=mismatch_order_violations,
    )


def stage6d_rows() -> dict[str, Any]:
    """Return JSON-friendly canonical, exhaustive, and mismatch diagnostics."""

    return {
        "canonical": canonical_stage6d_diagnostics().as_dict(),
        "family_scan": scan_horizontal_vertical_compatibility().as_dict(),
        "mismatch_control": mismatch_control_diagnostics().as_dict(),
        "guards": {
            "horizontal_vertical_identity_claimed": False,
            "clock_coordinate_defines_event_correspondence": False,
            "perspective_change_is_temporal_succession": False,
        },
    }
