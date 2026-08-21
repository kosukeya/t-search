"""Stage 6C partial perspective-atlas utilities.

Stage 5 established pairwise and three-clock consistency for genuine physical
clock changes.  Stage 6C removes the assumption that every requested direct
perspective edge is primitive.  A sparse atlas stores only declared direct
maps, reconstructs missing source-to-target maps by path composition, compares
alternative paths, and detects deliberately introduced path/loop failures.

All maps here remain Stage 5 support-space perspective maps.  A nonzero loop
residual in a perturbed atlas is an algebraic consistency failure only; it is
not interpreted as physical curvature or gravitational holonomy.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, permutations, product
from typing import Any, Iterable

import numpy as np

from .stage5_clock_change import DEFAULT_ATOL, DEFAULT_DIMENSION, DEFAULT_RATES, SUBSYSTEMS
from .stage5_clock_transforms import genuine_clock_change_support_matrix
from .stage5_reductions import rest_subsystems


class UnknownPerspectiveError(KeyError):
    """Raised when a requested perspective is not part of the declared atlas."""


class DirectMapUnavailableError(KeyError):
    """Raised when both perspectives exist but no primitive direct edge exists."""


@dataclass(frozen=True, order=True)
class PerspectiveNode:
    """One physical-clock perspective at one declared clock reading."""

    clock: str
    index: int

    @property
    def label(self) -> str:
        return f"{self.clock}{self.index}"

    def as_dict(self) -> dict[str, Any]:
        return {"clock": self.clock, "index": self.index, "label": self.label}


@dataclass(frozen=True)
class AtlasEdge:
    """One declared primitive horizontal perspective map."""

    source: PerspectiveNode
    target: PerspectiveNode
    matrix: np.ndarray

    def as_dict(self) -> dict[str, Any]:
        return {
            "source": self.source.label,
            "target": self.target.label,
            "shape": list(self.matrix.shape),
        }


@dataclass(frozen=True)
class PartialPerspectiveAtlas:
    """Sparse directed atlas of declared perspective maps."""

    perspectives: tuple[PerspectiveNode, ...]
    edges: tuple[AtlasEdge, ...]
    tolerance: float = DEFAULT_ATOL

    def __post_init__(self) -> None:
        if len(set(self.perspectives)) != len(self.perspectives):
            raise ValueError("partial atlas contains duplicate perspectives")
        if not self.perspectives:
            raise ValueError("partial atlas must contain at least one perspective")

        perspective_set = set(self.perspectives)
        edge_pairs: set[tuple[PerspectiveNode, PerspectiveNode]] = set()
        for edge in self.edges:
            if edge.source not in perspective_set or edge.target not in perspective_set:
                raise ValueError("atlas edge endpoint is not a declared perspective")
            pair = (edge.source, edge.target)
            if pair in edge_pairs:
                raise ValueError("partial atlas contains duplicate directed edges")
            edge_pairs.add(pair)
            matrix = np.asarray(edge.matrix)
            if matrix.ndim != 2:
                raise ValueError("atlas edge matrix must be two-dimensional")
            if not np.all(np.isfinite(matrix)):
                raise ValueError("atlas edge matrix must be finite")

    def has_perspective(self, node: PerspectiveNode) -> bool:
        return node in self.perspectives

    def has_direct_map(self, source: PerspectiveNode, target: PerspectiveNode) -> bool:
        if source not in self.perspectives or target not in self.perspectives:
            return False
        return any(edge.source == source and edge.target == target for edge in self.edges)

    def direct_map(self, source: PerspectiveNode, target: PerspectiveNode) -> np.ndarray:
        if source not in self.perspectives:
            raise UnknownPerspectiveError(f"unknown source perspective {source.label}")
        if target not in self.perspectives:
            raise UnknownPerspectiveError(f"unknown target perspective {target.label}")
        matches = [
            edge.matrix
            for edge in self.edges
            if edge.source == source and edge.target == target
        ]
        if not matches:
            raise DirectMapUnavailableError(
                f"no primitive direct map {source.label}->{target.label}"
            )
        if len(matches) != 1:
            raise RuntimeError("duplicate direct atlas maps escaped construction validation")
        return np.asarray(matches[0], dtype=np.complex128)

    def outgoing(self, source: PerspectiveNode) -> tuple[PerspectiveNode, ...]:
        if source not in self.perspectives:
            raise UnknownPerspectiveError(f"unknown perspective {source.label}")
        return tuple(edge.target for edge in self.edges if edge.source == source)

    def compose_path(self, path: Iterable[PerspectiveNode]) -> np.ndarray:
        nodes = tuple(path)
        if len(nodes) < 2:
            raise ValueError("map composition requires a path with at least one edge")
        for node in nodes:
            if node not in self.perspectives:
                raise UnknownPerspectiveError(f"unknown perspective {node.label}")

        result = self.direct_map(nodes[0], nodes[1])
        for source, target in zip(nodes[1:-1], nodes[2:]):
            result = self.direct_map(source, target) @ result
        return result

    def simple_paths(
        self,
        source: PerspectiveNode,
        target: PerspectiveNode,
        *,
        max_hops: int,
    ) -> tuple[tuple[PerspectiveNode, ...], ...]:
        """Enumerate simple directed source-to-target paths up to ``max_hops``."""

        if max_hops < 1:
            raise ValueError("max_hops must be at least one")
        if source not in self.perspectives:
            raise UnknownPerspectiveError(f"unknown source perspective {source.label}")
        if target not in self.perspectives:
            raise UnknownPerspectiveError(f"unknown target perspective {target.label}")

        found: list[tuple[PerspectiveNode, ...]] = []

        def visit(path: tuple[PerspectiveNode, ...]) -> None:
            current = path[-1]
            hops = len(path) - 1
            if current == target:
                found.append(path)
                return
            if hops >= max_hops:
                return
            for nxt in self.outgoing(current):
                if nxt in path:
                    continue
                visit(path + (nxt,))

        visit((source,))
        return tuple(found)

    def path_residual(
        self,
        first: Iterable[PerspectiveNode],
        second: Iterable[PerspectiveNode],
    ) -> float:
        first_path = tuple(first)
        second_path = tuple(second)
        if first_path[0] != second_path[0] or first_path[-1] != second_path[-1]:
            raise ValueError("path comparison requires common source and target")
        return float(
            np.linalg.norm(self.compose_path(first_path) - self.compose_path(second_path))
        )

    def loop_residual(self, loop: Iterable[PerspectiveNode]) -> float:
        nodes = tuple(loop)
        if len(nodes) < 3 or nodes[0] != nodes[-1]:
            raise ValueError("loop must contain at least two edges and close at its source")
        matrix = self.compose_path(nodes)
        if matrix.shape[0] != matrix.shape[1]:
            raise ValueError("closed-loop support matrix must be square")
        return float(np.linalg.norm(matrix - np.eye(matrix.shape[0], dtype=np.complex128)))

    def as_dict(self) -> dict[str, Any]:
        return {
            "perspectives": [node.as_dict() for node in self.perspectives],
            "edges": [edge.as_dict() for edge in self.edges],
            "tolerance": self.tolerance,
        }


@dataclass(frozen=True)
class PartialAtlasDiagnostics:
    """Diagnostics for one deliberately missing direct source-to-target edge."""

    source: PerspectiveNode
    target: PerspectiveNode
    target_present: bool
    direct_edge_present: bool
    path_count: int
    max_indirect_direct_residual: float
    max_pairwise_path_residual: float
    max_loop_residual: float

    def as_dict(self) -> dict[str, Any]:
        return {
            "source": self.source.label,
            "target": self.target.label,
            "target_present": self.target_present,
            "direct_edge_present": self.direct_edge_present,
            "path_count": self.path_count,
            "max_indirect_direct_residual": self.max_indirect_direct_residual,
            "max_pairwise_path_residual": self.max_pairwise_path_residual,
            "max_loop_residual": self.max_loop_residual,
        }


@dataclass(frozen=True)
class PartialAtlasFamilyScan:
    """Exhaustive canonical Stage 6C scan over ordered clock/readout endpoints."""

    endpoint_case_count: int
    indirect_path_count: int
    closed_loop_count: int
    missing_direct_edge_count: int
    present_target_count: int
    max_indirect_direct_residual: float
    max_pairwise_path_residual: float
    max_loop_residual: float

    def as_dict(self) -> dict[str, Any]:
        return {
            "endpoint_case_count": self.endpoint_case_count,
            "indirect_path_count": self.indirect_path_count,
            "closed_loop_count": self.closed_loop_count,
            "missing_direct_edge_count": self.missing_direct_edge_count,
            "present_target_count": self.present_target_count,
            "max_indirect_direct_residual": self.max_indirect_direct_residual,
            "max_pairwise_path_residual": self.max_pairwise_path_residual,
            "max_loop_residual": self.max_loop_residual,
        }


def _validate_node(node: PerspectiveNode, dimension: int) -> None:
    rest_subsystems(node.clock)
    if not isinstance(node.index, int) or isinstance(node.index, bool):
        raise TypeError("perspective index must be an integer")
    if not 0 <= node.index < dimension:
        raise ValueError("perspective index is outside the declared clock dimension")


def _intermediate_clock(source_clock: str, target_clock: str) -> str:
    rest_subsystems(source_clock)
    rest_subsystems(target_clock)
    if source_clock == target_clock:
        raise ValueError("partial cross-clock atlas requires distinct endpoint clocks")
    return next(clock for clock in SUBSYSTEMS if clock not in {source_clock, target_clock})


def _edge(
    source: PerspectiveNode,
    target: PerspectiveNode,
    dimension: int,
    *,
    rates: Iterable[float],
) -> AtlasEdge:
    matrix = genuine_clock_change_support_matrix(
        target.clock,
        target.index,
        source.clock,
        source.index,
        dimension,
        rates=rates,
    )
    return AtlasEdge(source=source, target=target, matrix=matrix)


def build_partial_clock_atlas(
    source: PerspectiveNode,
    target: PerspectiveNode,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    tolerance: float = DEFAULT_ATOL,
) -> PartialPerspectiveAtlas:
    """Build a sparse atlas with no primitive ``source -> target`` edge.

    All readings of the third physical clock are retained as intermediate
    perspectives.  The sparse graph contains three classes of edges:

    ``source -> intermediate(k) -> target`` for every ``k``;
    ``target -> source`` as a return edge for closed-loop diagnostics.

    Thus the target perspective exists and the missing direct map can be
    reconstructed along multiple distinct available paths.
    """

    if dimension < 2:
        raise ValueError("dimension must be at least two")
    _validate_node(source, dimension)
    _validate_node(target, dimension)
    intermediate_clock = _intermediate_clock(source.clock, target.clock)
    intermediate_nodes = tuple(
        PerspectiveNode(intermediate_clock, index) for index in range(dimension)
    )
    perspectives = (source, *intermediate_nodes, target)

    edges: list[AtlasEdge] = []
    for intermediate in intermediate_nodes:
        edges.append(_edge(source, intermediate, dimension, rates=rates))
        edges.append(_edge(intermediate, target, dimension, rates=rates))
    edges.append(_edge(target, source, dimension, rates=rates))

    atlas = PartialPerspectiveAtlas(
        perspectives=perspectives,
        edges=tuple(edges),
        tolerance=tolerance,
    )
    if atlas.has_direct_map(source, target):
        raise RuntimeError("partial-atlas construction accidentally retained direct edge")
    return atlas


def indirect_paths(
    atlas: PartialPerspectiveAtlas,
    source: PerspectiveNode,
    target: PerspectiveNode,
) -> tuple[tuple[PerspectiveNode, ...], ...]:
    """Return the declared two-hop reconstruction paths between endpoints."""

    return tuple(
        path
        for path in atlas.simple_paths(source, target, max_hops=2)
        if len(path) == 3
    )


def external_direct_reference(
    source: PerspectiveNode,
    target: PerspectiveNode,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Return the Stage 5 primitive map as an external reconstruction reference.

    The returned matrix is deliberately *not* inserted as an atlas edge.
    """

    _validate_node(source, dimension)
    _validate_node(target, dimension)
    if source.clock == target.clock:
        raise ValueError("external direct reference requires distinct endpoint clocks")
    return genuine_clock_change_support_matrix(
        target.clock,
        target.index,
        source.clock,
        source.index,
        dimension,
        rates=rates,
    )


def diagnose_partial_atlas(
    atlas: PartialPerspectiveAtlas,
    source: PerspectiveNode,
    target: PerspectiveNode,
    direct_reference: np.ndarray,
) -> PartialAtlasDiagnostics:
    paths = indirect_paths(atlas, source, target)
    if not paths:
        raise ValueError("partial atlas contains no two-hop reconstruction path")

    composed = [atlas.compose_path(path) for path in paths]
    reference = np.asarray(direct_reference, dtype=np.complex128)
    indirect_direct = [float(np.linalg.norm(matrix - reference)) for matrix in composed]
    pairwise = [
        float(np.linalg.norm(first - second))
        for first, second in combinations(composed, 2)
    ]
    loops = [atlas.loop_residual(path + (source,)) for path in paths]

    return PartialAtlasDiagnostics(
        source=source,
        target=target,
        target_present=atlas.has_perspective(target),
        direct_edge_present=atlas.has_direct_map(source, target),
        path_count=len(paths),
        max_indirect_direct_residual=max(indirect_direct),
        max_pairwise_path_residual=max(pairwise, default=0.0),
        max_loop_residual=max(loops),
    )


def canonical_partial_clock_atlas() -> tuple[
    PartialPerspectiveAtlas,
    PerspectiveNode,
    PerspectiveNode,
]:
    """Return the decisive sparse ``C0 -> B2`` atlas via all A readings."""

    source = PerspectiveNode("C", 0)
    target = PerspectiveNode("B", 2)
    return build_partial_clock_atlas(source, target, 3), source, target


def scan_partial_clock_atlas_family(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    tolerance: float = DEFAULT_ATOL,
) -> PartialAtlasFamilyScan:
    """Scan every ordered distinct-clock endpoint and all endpoint readings."""

    diagnostics: list[PartialAtlasDiagnostics] = []
    indirect_path_count = 0
    closed_loop_count = 0

    for source_clock, target_clock in permutations(SUBSYSTEMS, 2):
        for source_index, target_index in product(range(dimension), repeat=2):
            source = PerspectiveNode(source_clock, source_index)
            target = PerspectiveNode(target_clock, target_index)
            atlas = build_partial_clock_atlas(
                source,
                target,
                dimension,
                rates=rates,
                tolerance=tolerance,
            )
            reference = external_direct_reference(
                source,
                target,
                dimension,
                rates=rates,
            )
            diagnostic = diagnose_partial_atlas(atlas, source, target, reference)
            diagnostics.append(diagnostic)
            indirect_path_count += diagnostic.path_count
            closed_loop_count += diagnostic.path_count

    return PartialAtlasFamilyScan(
        endpoint_case_count=len(diagnostics),
        indirect_path_count=indirect_path_count,
        closed_loop_count=closed_loop_count,
        missing_direct_edge_count=sum(not item.direct_edge_present for item in diagnostics),
        present_target_count=sum(item.target_present for item in diagnostics),
        max_indirect_direct_residual=max(
            item.max_indirect_direct_residual for item in diagnostics
        ),
        max_pairwise_path_residual=max(
            item.max_pairwise_path_residual for item in diagnostics
        ),
        max_loop_residual=max(item.max_loop_residual for item in diagnostics),
    )


def perturb_direct_edge(
    atlas: PartialPerspectiveAtlas,
    source: PerspectiveNode,
    target: PerspectiveNode,
    *,
    epsilon: float = 1e-4,
    row: int = 0,
    column: int = 0,
) -> PartialPerspectiveAtlas:
    """Return a copy with one declared edge deliberately perturbed."""

    if epsilon == 0.0:
        raise ValueError("perturbation epsilon must be nonzero")
    matrix = atlas.direct_map(source, target)
    if not (0 <= row < matrix.shape[0] and 0 <= column < matrix.shape[1]):
        raise IndexError("perturbation coordinate is outside edge-matrix shape")

    replacement = np.array(matrix, dtype=np.complex128, copy=True)
    replacement[row, column] += epsilon
    edges = tuple(
        AtlasEdge(edge.source, edge.target, replacement)
        if edge.source == source and edge.target == target
        else edge
        for edge in atlas.edges
    )
    return PartialPerspectiveAtlas(
        perspectives=atlas.perspectives,
        edges=edges,
        tolerance=atlas.tolerance,
    )


def stage6c_summary_rows() -> dict[str, Any]:
    """Return JSON-friendly canonical and exhaustive Stage 6C diagnostics."""

    atlas, source, target = canonical_partial_clock_atlas()
    reference = external_direct_reference(source, target, 3)
    canonical = diagnose_partial_atlas(atlas, source, target, reference)

    perturbed_source = source
    perturbed_target = PerspectiveNode("A", 1)
    perturbed = perturb_direct_edge(
        atlas,
        perturbed_source,
        perturbed_target,
        epsilon=1e-4,
    )
    perturbed_diagnostics = diagnose_partial_atlas(
        perturbed,
        source,
        target,
        reference,
    )

    return {
        "canonical_atlas": atlas.as_dict(),
        "canonical_diagnostics": canonical.as_dict(),
        "family_scan": scan_partial_clock_atlas_family().as_dict(),
        "perturbed_edge": {
            "source": perturbed_source.label,
            "target": perturbed_target.label,
            "epsilon": 1e-4,
        },
        "perturbed_diagnostics": perturbed_diagnostics.as_dict(),
    }
