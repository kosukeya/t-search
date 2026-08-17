"""Stage 1A: minimal classical global/local reconstruction.

The modeled temporal/causal structure lives only in the directed edges of ``Block``.
Python execution order has no temporal meaning inside the toy model.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

import networkx as nx

EventId = str
Edge = tuple[EventId, EventId]


@dataclass(frozen=True)
class Block:
    """A Stage-1 block-like structure B_1 = (E, C)."""

    events: frozenset[EventId]
    direct_edges: frozenset[Edge]


@dataclass(frozen=True)
class LocalView:
    """A one-hop local structural view V_e."""

    event_id: EventId
    predecessors: frozenset[EventId]
    successors: frozenset[EventId]


@dataclass(frozen=True)
class ViewConsistency:
    """Diagnostics comparing incoming and outgoing edge reports."""

    consistent: bool
    outgoing_edges: frozenset[Edge]
    incoming_edges: frozenset[Edge]
    missing_from_incoming: frozenset[Edge]
    missing_from_outgoing: frozenset[Edge]
    unknown_references: frozenset[EventId]


@dataclass(frozen=True)
class ComparisonResult:
    """Diagnostics used by the Stage 1A round-trip experiment."""

    labeled_equal: bool
    unlabeled_isomorphic: bool
    reachability_equal: bool


def _as_graph(block: Block) -> nx.DiGraph:
    graph = nx.DiGraph()
    graph.add_nodes_from(block.events)
    graph.add_edges_from(block.direct_edges)
    return graph


def make_block(events: Iterable[EventId], direct_edges: Iterable[Edge]) -> Block:
    """Create and validate a finite DAG block.

    Validation follows ``docs/stage1_protocol.md``: every edge endpoint must be an
    event, self-loops are forbidden, and Stage 1 blocks must be acyclic.
    """

    event_set = frozenset(events)
    edge_set = frozenset(tuple(edge) for edge in direct_edges)

    unknown = {
        endpoint
        for source, target in edge_set
        for endpoint in (source, target)
        if endpoint not in event_set
    }
    if unknown:
        raise ValueError(f"edge endpoints are not events: {sorted(unknown)}")

    self_loops = {(source, target) for source, target in edge_set if source == target}
    if self_loops:
        raise ValueError(f"self-loops are forbidden: {sorted(self_loops)}")

    block = Block(event_set, edge_set)
    if not nx.is_directed_acyclic_graph(_as_graph(block)):
        raise ValueError("Stage 1 block must be a directed acyclic graph")

    return block


def canonical_block() -> Block:
    """Return the canonical six-event Stage 1A graph from the protocol."""

    return make_block(
        events={"a", "b", "c", "d", "e", "f"},
        direct_edges={
            ("a", "b"),
            ("a", "c"),
            ("b", "d"),
            ("c", "d"),
            ("d", "e"),
            ("d", "f"),
        },
    )


def project_local_view(block: Block, event: EventId) -> LocalView:
    """Project B_1 onto the one-hop structural view V_e."""

    if event not in block.events:
        raise KeyError(f"unknown event: {event}")

    predecessors = frozenset(source for source, target in block.direct_edges if target == event)
    successors = frozenset(target for source, target in block.direct_edges if source == event)
    return LocalView(event, predecessors, successors)


def project_all_views(block: Block) -> tuple[LocalView, ...]:
    """Project one view per event.

    Sorting is only for deterministic program output. It does not represent modeled
    temporal order.
    """

    return tuple(project_local_view(block, event) for event in sorted(block.events))


def check_view_consistency(views: Iterable[LocalView]) -> ViewConsistency:
    """Compare independently reported incoming and outgoing direct edges."""

    materialized = tuple(views)
    ids = [view.event_id for view in materialized]
    if len(ids) != len(set(ids)):
        raise ValueError("local view family contains duplicate event IDs")

    event_ids = frozenset(ids)
    referenced_ids = frozenset(
        ref
        for view in materialized
        for ref in (*view.predecessors, *view.successors)
    )
    unknown = referenced_ids - event_ids

    outgoing = frozenset(
        (view.event_id, successor)
        for view in materialized
        for successor in view.successors
    )
    incoming = frozenset(
        (predecessor, view.event_id)
        for view in materialized
        for predecessor in view.predecessors
    )

    missing_from_incoming = outgoing - incoming
    missing_from_outgoing = incoming - outgoing
    consistent = not unknown and not missing_from_incoming and not missing_from_outgoing

    return ViewConsistency(
        consistent=consistent,
        outgoing_edges=outgoing,
        incoming_edges=incoming,
        missing_from_incoming=missing_from_incoming,
        missing_from_outgoing=missing_from_outgoing,
        unknown_references=unknown,
    )


def glue_views(views: Iterable[LocalView]) -> Block:
    """Glue a mutually consistent Stage 1A view family into B_1_hat."""

    materialized = tuple(views)
    if not materialized:
        raise ValueError("cannot glue an empty view family")

    consistency = check_view_consistency(materialized)
    if not consistency.consistent:
        raise ValueError(
            "inconsistent local views: "
            f"unknown_references={sorted(consistency.unknown_references)}, "
            f"missing_from_incoming={sorted(consistency.missing_from_incoming)}, "
            f"missing_from_outgoing={sorted(consistency.missing_from_outgoing)}"
        )

    event_ids = frozenset(view.event_id for view in materialized)
    return make_block(event_ids, consistency.outgoing_edges)


def transitive_closure(block: Block) -> frozenset[Edge]:
    """Return the non-reflexive reachability relation prec = TC(C)."""

    closure = nx.transitive_closure(_as_graph(block), reflexive=False)
    return frozenset((source, target) for source, target in closure.edges() if source != target)


def compare_blocks(original: Block, reconstructed: Block) -> ComparisonResult:
    """Compare labeled adjacency, unlabeled isomorphism, and reachability separately."""

    labeled_equal = (
        original.events == reconstructed.events
        and original.direct_edges == reconstructed.direct_edges
    )
    unlabeled_isomorphic = nx.is_isomorphic(_as_graph(original), _as_graph(reconstructed))
    reachability_equal = transitive_closure(original) == transitive_closure(reconstructed)

    return ComparisonResult(
        labeled_equal=labeled_equal,
        unlabeled_isomorphic=unlabeled_isomorphic,
        reachability_equal=reachability_equal,
    )


def views_by_id(views: Iterable[LocalView]) -> Mapping[EventId, LocalView]:
    """Convenience helper for deterministic inspection and tests."""

    return {view.event_id: view for view in views}
