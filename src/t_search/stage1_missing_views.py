"""Stage 1B B3: reconstruction with missing local views.

This module implements the semantics fixed in
``docs/stage1b_missing_views_protocol.md``.

The surviving inputs are full Stage 1A ``LocalView`` objects. B3 changes only
coverage: one or more complete views are removed before reconstruction.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product
from typing import Iterable, Literal

import networkx as nx

from .stage1 import Block, Edge, EventId, LocalView, make_block

MissingViewPolicy = Literal["strict", "latent"]


@dataclass(frozen=True)
class MissingViewReconstruction:
    """Diagnostics and reconstructed block for a B3 missing-view run."""

    policy: MissingViewPolicy
    block: Block
    view_owners: frozenset[EventId]
    referenced_events: frozenset[EventId]
    latent_events: frozenset[EventId]
    dangling_references: frozenset[EventId]
    singly_reported_edges: frozenset[Edge]
    doubly_reported_edges: frozenset[Edge]


def _edge_reports(
    views: Iterable[LocalView],
) -> tuple[
    tuple[LocalView, ...],
    frozenset[EventId],
    frozenset[EventId],
    frozenset[Edge],
    frozenset[Edge],
]:
    materialized = tuple(views)
    if not materialized:
        raise ValueError("cannot reconstruct from an empty missing-view family")

    ids = [view.event_id for view in materialized]
    if len(ids) != len(set(ids)):
        raise ValueError("missing-view family contains duplicate event IDs")

    owners = frozenset(ids)
    referenced = frozenset(
        ref
        for view in materialized
        for ref in (*view.predecessors, *view.successors)
    )
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

    owner_outgoing = frozenset(
        edge for edge in outgoing if edge[0] in owners and edge[1] in owners
    )
    owner_incoming = frozenset(
        edge for edge in incoming if edge[0] in owners and edge[1] in owners
    )
    if owner_outgoing != owner_incoming:
        raise ValueError(
            "surviving owner-owner reports are inconsistent: "
            f"outgoing_only={sorted(owner_outgoing - owner_incoming)}, "
            f"incoming_only={sorted(owner_incoming - owner_outgoing)}"
        )

    return materialized, owners, referenced, outgoing, incoming


def reconstruct_missing_views(
    views: Iterable[LocalView],
    *,
    policy: MissingViewPolicy,
) -> MissingViewReconstruction:
    """Reconstruct under either the strict-owner or referenced-latent policy."""

    _, owners, referenced, outgoing, incoming = _edge_reports(views)
    singly_reported = outgoing ^ incoming
    doubly_reported = outgoing & incoming

    if policy == "strict":
        events = owners
        edges = frozenset(
            edge
            for edge in (outgoing | incoming)
            if edge[0] in owners and edge[1] in owners
        )
        latent = frozenset()
        dangling = referenced - owners
    elif policy == "latent":
        events = owners | referenced
        edges = outgoing | incoming
        latent = events - owners
        dangling = frozenset()
    else:
        raise ValueError(f"unknown missing-view policy: {policy!r}")

    return MissingViewReconstruction(
        policy=policy,
        block=make_block(events, edges),
        view_owners=owners,
        referenced_events=referenced,
        latent_events=latent,
        dangling_references=dangling,
        singly_reported_edges=singly_reported,
        doubly_reported_edges=doubly_reported,
    )


def enumerate_latent_edge_completions(
    reconstruction: MissingViewReconstruction,
) -> tuple[Block, ...]:
    """Enumerate DAG completions for unreported relations among latent events.

    The candidate event universe is deliberately closed to the IDs already present
    as view owners or references. For each unordered latent pair that is not fixed
    by surviving edge evidence, consider no edge, left->right, or right->left.
    Only acyclic candidates are returned.
    """

    if reconstruction.policy != "latent":
        raise ValueError("candidate completion requires the latent reconstruction policy")

    base = reconstruction.block
    latent = sorted(reconstruction.latent_events)
    unresolved_pairs = [
        (left, right)
        for left, right in combinations(latent, 2)
        if (left, right) not in base.direct_edges
        and (right, left) not in base.direct_edges
    ]

    candidates: list[Block] = []
    for choices in product((0, 1, 2), repeat=len(unresolved_pairs)):
        edges = set(base.direct_edges)
        for (left, right), choice in zip(unresolved_pairs, choices):
            if choice == 1:
                edges.add((left, right))
            elif choice == 2:
                edges.add((right, left))

        graph = nx.DiGraph()
        graph.add_nodes_from(base.events)
        graph.add_edges_from(edges)
        if nx.is_directed_acyclic_graph(graph):
            candidates.append(make_block(base.events, edges))

    return tuple(candidates)
