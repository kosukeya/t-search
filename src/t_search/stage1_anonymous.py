"""Stage 1B B6: anonymous / global-ID-free local-view reconstruction.

The anonymous local data contain no shared event IDs. Generated labels ``v0`` ...
``vN`` are exhaustive-search bookkeeping only and are removed again when candidate
solutions are quotiented by directed graph isomorphism.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Literal

import networkx as nx

from .stage1 import Block, EventId


@dataclass(frozen=True, order=True)
class AnonymousStarView:
    """Minimal anonymous one-hop view: only directed in/out degree survives."""

    in_degree: int
    out_degree: int


@dataclass(frozen=True, order=True)
class RefinedAnonymousView:
    """One-step anonymous refinement using neighbor star-type multisets."""

    center_type: AnonymousStarView
    predecessor_types: tuple[AnonymousStarView, ...]
    successor_types: tuple[AnonymousStarView, ...]


AnonymousMode = Literal["star", "refined"]
AnonymousFamily = tuple[AnonymousStarView, ...] | tuple[RefinedAnonymousView, ...]


@dataclass(frozen=True)
class AnonymousSearchResult:
    """Exhaustive candidate search, deduplicated by directed isomorphism."""

    mode: AnonymousMode
    n_events: int
    scanned_graphs: int
    topological_label_matches: int
    isomorphism_classes: tuple[Block, ...]

    @property
    def n_compatible(self) -> int:
        return len(self.isomorphism_classes)

    @property
    def unique_up_to_isomorphism(self) -> bool:
        return self.n_compatible == 1


def _as_graph(block: Block) -> nx.DiGraph:
    graph = nx.DiGraph()
    graph.add_nodes_from(block.events)
    graph.add_edges_from(block.direct_edges)
    return graph


def project_anonymous_star_family(block: Block) -> tuple[AnonymousStarView, ...]:
    """Return the unordered/multiset-equivalent family A^(0)(B)."""
    graph = _as_graph(block)
    return tuple(
        sorted(
            AnonymousStarView(graph.in_degree(event), graph.out_degree(event))
            for event in graph.nodes()
        )
    )


def project_refined_anonymous_family(block: Block) -> tuple[RefinedAnonymousView, ...]:
    """Return A^(1)(B), using only anonymous star types of immediate neighbors."""
    graph = _as_graph(block)
    star_types = {
        event: AnonymousStarView(graph.in_degree(event), graph.out_degree(event))
        for event in graph.nodes()
    }

    family = []
    for event in graph.nodes():
        family.append(
            RefinedAnonymousView(
                center_type=star_types[event],
                predecessor_types=tuple(
                    sorted(star_types[parent] for parent in graph.predecessors(event))
                ),
                successor_types=tuple(
                    sorted(star_types[child] for child in graph.successors(event))
                ),
            )
        )
    return tuple(sorted(family))


def project_anonymous_family(block: Block, mode: AnonymousMode) -> AnonymousFamily:
    if mode == "star":
        return project_anonymous_star_family(block)
    if mode == "refined":
        return project_refined_anonymous_family(block)
    raise ValueError(f"unknown anonymous mode: {mode}")


def enumerate_topological_dags(n_events: int) -> Iterable[Block]:
    """Enumerate all forward-edge DAGs on one fixed topological ordering.

    Every finite DAG has a topological ordering, so every DAG is isomorphic to at
    least one graph generated here. B6 intentionally caps this exhaustive search at
    six events to keep the search finite and transparent.
    """
    if n_events < 1:
        raise ValueError("n_events must be positive")
    if n_events > 6:
        raise ValueError("B6 exhaustive enumeration is capped at six events")

    events = tuple(f"v{i}" for i in range(n_events))
    possible_edges = tuple(
        (events[i], events[j])
        for i in range(n_events)
        for j in range(i + 1, n_events)
    )

    frozen_events = frozenset(events)
    for mask in range(1 << len(possible_edges)):
        edges = frozenset(
            edge
            for index, edge in enumerate(possible_edges)
            if (mask >> index) & 1
        )
        # All generated edges point forward in the fixed ordering, so acyclicity is
        # guaranteed by construction and no temporal meaning is attached to that order.
        yield Block(events=frozen_events, direct_edges=edges)


def _append_if_new_isomorphism_class(candidate: Block, representatives: list[Block]) -> None:
    candidate_graph = _as_graph(candidate)
    if any(nx.is_isomorphic(candidate_graph, _as_graph(rep)) for rep in representatives):
        return
    representatives.append(candidate)


def find_compatible_anonymous_dags(
    target_family: AnonymousFamily,
    *,
    mode: AnonymousMode,
) -> AnonymousSearchResult:
    """Exhaustively search DAGs whose anonymous local family matches ``target_family``."""
    n_events = len(target_family)
    if n_events < 1:
        raise ValueError("anonymous target family must be non-empty")

    scanned = 0
    raw_matches = 0
    representatives: list[Block] = []

    for candidate in enumerate_topological_dags(n_events):
        scanned += 1
        if project_anonymous_family(candidate, mode) != target_family:
            continue
        raw_matches += 1
        _append_if_new_isomorphism_class(candidate, representatives)

    return AnonymousSearchResult(
        mode=mode,
        n_events=n_events,
        scanned_graphs=scanned,
        topological_label_matches=raw_matches,
        isomorphism_classes=tuple(representatives),
    )


def contains_isomorphic_candidate(target: Block, candidates: Iterable[Block]) -> bool:
    """Return whether one candidate belongs to the target's directed isomorphism class."""
    target_graph = _as_graph(target)
    return any(nx.is_isomorphic(target_graph, _as_graph(candidate)) for candidate in candidates)


def reachability_pair_count(block: Block) -> int:
    """Count non-reflexive reachable ordered pairs for diagnostics."""
    closure = nx.transitive_closure(_as_graph(block))
    return sum(1 for source, target in closure.edges() if source != target)
