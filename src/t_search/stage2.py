"""Stage 2A: ontology-neutral finite branching substrate.

This module implements only the shared branching structure used later by the
Stage 2 epistemic-history and ontic-extension models. It deliberately assigns
no epistemic or ontic interpretation to the alternatives.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Hashable, Mapping, Sequence

import networkx as nx

from .stage1 import Edge, EventId

History = tuple[EventId, ...]
Prefix = tuple[EventId, ...]


@dataclass(frozen=True)
class BranchingStructure:
    """A finite rooted outward tree used as the neutral Stage 2 substrate.

    The protocol writes ``T = (E, C, H)``. ``H`` is intentionally derived from
    ``E`` and ``C`` rather than stored independently, avoiding duplicate state
    that could become inconsistent with the edge relation.
    """

    events: frozenset[EventId]
    direct_edges: frozenset[Edge]
    root: EventId

    @property
    def histories(self) -> tuple[History, ...]:
        return maximal_histories(self)


def _as_graph(substrate: BranchingStructure) -> nx.DiGraph:
    graph = nx.DiGraph()
    graph.add_nodes_from(substrate.events)
    graph.add_edges_from(substrate.direct_edges)
    return graph


def make_branching_structure(
    events: Sequence[EventId] | set[EventId] | frozenset[EventId],
    direct_edges: Sequence[Edge] | set[Edge] | frozenset[Edge],
    *,
    root: EventId,
) -> BranchingStructure:
    """Create and validate the Stage 2A rooted finite-tree substrate."""

    event_set = frozenset(events)
    edge_set = frozenset(tuple(edge) for edge in direct_edges)

    if not event_set:
        raise ValueError("branching structure must contain at least one event")
    if root not in event_set:
        raise ValueError(f"root is not an event: {root!r}")

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

    substrate = BranchingStructure(event_set, edge_set, root)
    graph = _as_graph(substrate)
    if not nx.is_directed_acyclic_graph(graph):
        raise ValueError("Stage 2 branching structure must be acyclic")

    if graph.in_degree(root) != 0:
        raise ValueError("root must have in-degree zero")

    reachable = frozenset(nx.descendants(graph, root)) | {root}
    unreachable = event_set - reachable
    if unreachable:
        raise ValueError(f"events are unreachable from root: {sorted(unreachable)}")

    wrong_indegree = {
        event: graph.in_degree(event)
        for event in event_set
        if event != root and graph.in_degree(event) != 1
    }
    if wrong_indegree:
        raise ValueError(
            "baseline branching substrate must be an outward rooted tree; "
            f"non-root in-degrees={wrong_indegree}"
        )

    return substrate


def canonical_stage2_substrate() -> BranchingStructure:
    """Return the asymmetric neutral branching substrate fixed by Stage 2.0."""

    return make_branching_structure(
        events={"p", "n", "l1", "l2", "r1"},
        direct_edges={
            ("p", "n"),
            ("n", "l1"),
            ("l1", "l2"),
            ("n", "r1"),
        },
        root="p",
    )


def maximal_histories(substrate: BranchingStructure) -> tuple[History, ...]:
    """Derive all maximal root-to-leaf histories in deterministic order."""

    graph = _as_graph(substrate)
    leaves = sorted(event for event in substrate.events if graph.out_degree(event) == 0)
    histories = [
        tuple(nx.shortest_path(graph, substrate.root, leaf))
        for leaf in leaves
    ]
    return tuple(sorted(histories))


def is_prefix(prefix: Prefix, history: History) -> bool:
    """Return whether ``prefix`` is a non-empty initial segment of ``history``."""

    return bool(prefix) and len(prefix) <= len(history) and history[: len(prefix)] == prefix


def is_valid_prefix(substrate: BranchingStructure, prefix: Prefix) -> bool:
    """Return whether ``prefix`` is an actual prefix of at least one maximal history."""

    return any(is_prefix(prefix, history) for history in substrate.histories)


def validate_prefix(substrate: BranchingStructure, prefix: Prefix) -> Prefix:
    """Validate and return ``prefix`` for callers that need an explicit guard."""

    materialized = tuple(prefix)
    if not materialized:
        raise ValueError("actual prefix must be non-empty")
    if not is_valid_prefix(substrate, materialized):
        raise ValueError(f"not a valid prefix of the branching substrate: {materialized!r}")
    return materialized


def prefix_tip(prefix: Prefix) -> EventId:
    """Return the current/tip event of a non-empty actual prefix."""

    if not prefix:
        raise ValueError("cannot take the tip of an empty prefix")
    return prefix[-1]


def extensions(substrate: BranchingStructure, prefix: Prefix) -> tuple[History, ...]:
    """Return ``Ext_T(D)``: complete histories extending the current prefix."""

    materialized = validate_prefix(substrate, prefix)
    return tuple(history for history in substrate.histories if is_prefix(materialized, history))


def next_events(substrate: BranchingStructure, prefix: Prefix) -> frozenset[EventId]:
    """Return immediate events that can follow the current prefix."""

    materialized = validate_prefix(substrate, prefix)
    index = len(materialized)
    return frozenset(
        history[index]
        for history in extensions(substrate, materialized)
        if index < len(history)
    )


def extend_prefix(
    substrate: BranchingStructure,
    prefix: Prefix,
    next_event: EventId,
) -> Prefix:
    """Extend a valid actual prefix by one admissible immediate event."""

    materialized = validate_prefix(substrate, prefix)
    allowed = next_events(substrate, materialized)
    if next_event not in allowed:
        raise ValueError(
            f"event {next_event!r} is not an admissible immediate successor; "
            f"allowed={sorted(allowed)}"
        )
    return materialized + (next_event,)


def _history_path_graph(
    history: History,
    *,
    state_labels: Mapping[EventId, Hashable] | None = None,
) -> nx.DiGraph:
    graph = nx.DiGraph()
    for index, event in enumerate(history):
        attrs = {"root": index == 0}
        if state_labels is not None:
            attrs["state"] = state_labels[event]
        graph.add_node(index, **attrs)
        if index:
            graph.add_edge(index - 1, index)
    return graph


def histories_equivalent(
    left: History,
    right: History,
    *,
    left_state_labels: Mapping[EventId, Hashable] | None = None,
    right_state_labels: Mapping[EventId, Hashable] | None = None,
) -> bool:
    """Compare histories up to event renaming, optionally preserving state labels."""

    if (left_state_labels is None) != (right_state_labels is None):
        raise ValueError("provide state-label maps for both histories or neither")

    left_graph = _history_path_graph(left, state_labels=left_state_labels)
    right_graph = _history_path_graph(right, state_labels=right_state_labels)

    if left_state_labels is None:
        node_match = nx.algorithms.isomorphism.categorical_node_match("root", False)
    else:
        node_match = nx.algorithms.isomorphism.categorical_node_match(
            ["root", "state"],
            [False, None],
        )
    return nx.is_isomorphic(left_graph, right_graph, node_match=node_match)


def _continuation_history(history: History, prefix: Prefix) -> History:
    if not is_prefix(prefix, history):
        raise ValueError(f"prefix {prefix!r} does not extend into history {history!r}")
    return (prefix[-1],) + history[len(prefix) :]


def continuations_equivalent(
    left: History,
    right: History,
    prefix: Prefix,
    *,
    state_labels: Mapping[EventId, Hashable] | None = None,
) -> bool:
    """Compare two extensions relative to the same current prefix up to renaming."""

    left_continuation = _continuation_history(left, prefix)
    right_continuation = _continuation_history(right, prefix)
    return histories_equivalent(
        left_continuation,
        right_continuation,
        left_state_labels=state_labels,
        right_state_labels=state_labels,
    )


def extension_equivalence_classes(
    substrate: BranchingStructure,
    prefix: Prefix,
    *,
    state_labels: Mapping[EventId, Hashable] | None = None,
) -> tuple[tuple[History, ...], ...]:
    """Partition ``Ext_T(D)`` into genuinely distinct continuation classes."""

    live = extensions(substrate, prefix)
    classes: list[list[History]] = []
    for history in live:
        for equivalence_class in classes:
            if continuations_equivalent(
                history,
                equivalence_class[0],
                prefix,
                state_labels=state_labels,
            ):
                equivalence_class.append(history)
                break
        else:
            classes.append([history])
    return tuple(tuple(group) for group in classes)


def branching_structures_equivalent(
    left: BranchingStructure,
    right: BranchingStructure,
    *,
    left_state_labels: Mapping[EventId, Hashable] | None = None,
    right_state_labels: Mapping[EventId, Hashable] | None = None,
) -> bool:
    """Compare rooted branching structures up to event renaming."""

    if (left_state_labels is None) != (right_state_labels is None):
        raise ValueError("provide state-label maps for both structures or neither")

    left_graph = _as_graph(left)
    right_graph = _as_graph(right)
    for event in left_graph.nodes:
        left_graph.nodes[event]["root"] = event == left.root
        if left_state_labels is not None:
            left_graph.nodes[event]["state"] = left_state_labels[event]
    for event in right_graph.nodes:
        right_graph.nodes[event]["root"] = event == right.root
        if right_state_labels is not None:
            right_graph.nodes[event]["state"] = right_state_labels[event]

    if left_state_labels is None:
        node_match = nx.algorithms.isomorphism.categorical_node_match("root", False)
    else:
        node_match = nx.algorithms.isomorphism.categorical_node_match(
            ["root", "state"],
            [False, None],
        )
    return nx.is_isomorphic(left_graph, right_graph, node_match=node_match)
