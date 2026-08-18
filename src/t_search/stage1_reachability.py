"""Stage 1B B4: reconstruction from reachability-only local views.

B4 discards direct one-hop adjacency and retains only the non-reflexive
reachability relation. Python execution order has no temporal meaning in the model.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import networkx as nx

from .stage1 import Block, Edge, EventId, make_block, transitive_closure


@dataclass(frozen=True)
class ReachabilityLocalView:
    """R_e = (id_e, Anc(e), Desc(e))."""

    event_id: EventId
    ancestors: frozenset[EventId]
    descendants: frozenset[EventId]


@dataclass(frozen=True)
class ReachabilityConsistency:
    """Diagnostics for a complete family of reachability-only views."""

    consistent: bool
    descendant_relation: frozenset[Edge]
    ancestor_relation: frozenset[Edge]
    unknown_references: frozenset[EventId]
    self_references: frozenset[Edge]
    missing_from_ancestors: frozenset[Edge]
    missing_from_descendants: frozenset[Edge]
    acyclic: bool
    transitive: bool


def project_reachability_view(block: Block, event: EventId) -> ReachabilityLocalView:
    """Project a block onto one event's complete ancestor/descendant sets."""
    if event not in block.events:
        raise KeyError(f"unknown event: {event}")

    relation = transitive_closure(block)
    ancestors = frozenset(source for source, target in relation if target == event)
    descendants = frozenset(target for source, target in relation if source == event)
    return ReachabilityLocalView(event, ancestors, descendants)


def project_all_reachability_views(block: Block) -> tuple[ReachabilityLocalView, ...]:
    """Project one reachability-only view per event."""
    return tuple(project_reachability_view(block, event) for event in sorted(block.events))


def _is_transitive_relation(relation: frozenset[Edge]) -> bool:
    """Check transitivity directly, independent of graph-library convenience APIs."""
    pairs = set(relation)
    for left, middle in pairs:
        for candidate_middle, right in pairs:
            if middle == candidate_middle and left != right and (left, right) not in pairs:
                return False
    return True


def check_reachability_consistency(
    views: Iterable[ReachabilityLocalView],
) -> ReachabilityConsistency:
    """Validate dual ancestor/descendant reports and strict partial-order structure."""
    materialized = tuple(views)
    if not materialized:
        raise ValueError("cannot validate an empty reachability-view family")

    ids = [view.event_id for view in materialized]
    if len(ids) != len(set(ids)):
        raise ValueError("reachability-view family contains duplicate event IDs")

    event_ids = frozenset(ids)
    referenced_ids = frozenset(
        reference
        for view in materialized
        for reference in (*view.ancestors, *view.descendants)
    )
    unknown = referenced_ids - event_ids

    descendant_relation = frozenset(
        (view.event_id, descendant)
        for view in materialized
        for descendant in view.descendants
    )
    ancestor_relation = frozenset(
        (ancestor, view.event_id)
        for view in materialized
        for ancestor in view.ancestors
    )

    reported_relation = descendant_relation | ancestor_relation
    self_references = frozenset(
        (source, target)
        for source, target in reported_relation
        if source == target
    )
    missing_from_ancestors = descendant_relation - ancestor_relation
    missing_from_descendants = ancestor_relation - descendant_relation

    graph = nx.DiGraph()
    graph.add_nodes_from(event_ids)
    graph.add_edges_from(reported_relation)

    acyclic = not unknown and not self_references and nx.is_directed_acyclic_graph(graph)
    transitive = not unknown and not self_references and _is_transitive_relation(
        reported_relation
    )
    consistent = (
        not unknown
        and not self_references
        and not missing_from_ancestors
        and not missing_from_descendants
        and acyclic
        and transitive
    )

    return ReachabilityConsistency(
        consistent=consistent,
        descendant_relation=descendant_relation,
        ancestor_relation=ancestor_relation,
        unknown_references=unknown,
        self_references=self_references,
        missing_from_ancestors=missing_from_ancestors,
        missing_from_descendants=missing_from_descendants,
        acyclic=acyclic,
        transitive=transitive,
    )


def reconstruct_cover_from_reachability(
    views: Iterable[ReachabilityLocalView],
) -> Block:
    """Reconstruct the unique transitive reduction of a finite partial order.

    Exact recovery of the original direct-edge set requires that the original edge
    set was already the cover/minimal generating relation. If the original encoding
    contained transitive shortcut edges, those shortcuts are intentionally not
    recoverable from reachability alone.
    """
    materialized = tuple(views)
    consistency = check_reachability_consistency(materialized)
    if not consistency.consistent:
        raise ValueError(
            "inconsistent reachability views: "
            f"unknown_references={sorted(consistency.unknown_references)}, "
            f"self_references={sorted(consistency.self_references)}, "
            f"missing_from_ancestors={sorted(consistency.missing_from_ancestors)}, "
            f"missing_from_descendants={sorted(consistency.missing_from_descendants)}, "
            f"acyclic={consistency.acyclic}, transitive={consistency.transitive}"
        )

    event_ids = frozenset(view.event_id for view in materialized)
    relation_graph = nx.DiGraph()
    relation_graph.add_nodes_from(event_ids)
    relation_graph.add_edges_from(consistency.descendant_relation)

    reduction = nx.transitive_reduction(relation_graph)
    return make_block(event_ids, frozenset(reduction.edges()))
