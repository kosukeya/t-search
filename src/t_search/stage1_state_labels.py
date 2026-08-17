"""Stage 1B B5: keep event identity separate from state equality."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from .stage1 import (
    Block,
    LocalView,
    check_view_consistency,
    make_block,
)

StateValue = str
StateAssignment = frozenset[tuple[str, StateValue]]


@dataclass(frozen=True)
class StateLabeledWorld:
    block: Block
    state_assignment: StateAssignment

    def states(self) -> Mapping[str, StateValue]:
        return dict(self.state_assignment)


@dataclass(frozen=True)
class StateLabeledView:
    event_id: str
    state_value: StateValue
    predecessors: frozenset[str]
    successors: frozenset[str]


@dataclass(frozen=True)
class StateReconstruction:
    world: StateLabeledWorld
    collision_groups: Mapping[StateValue, frozenset[str]]


def make_state_labeled_world(
    block: Block,
    assignment: Mapping[str, StateValue],
) -> StateLabeledWorld:
    """Attach a total event->state map to a Stage-1 block.

    State values need not be unique. Event IDs remain the identity keys.
    """

    keys = frozenset(assignment)
    missing = block.events - keys
    unknown = keys - block.events
    if missing:
        raise ValueError(f"state assignment missing events: {sorted(missing)}")
    if unknown:
        raise ValueError(f"state assignment contains unknown events: {sorted(unknown)}")

    state_assignment = frozenset((event, assignment[event]) for event in block.events)
    return StateLabeledWorld(block, state_assignment)


def canonical_state_labeled_world(block: Block) -> StateLabeledWorld:
    """Attach the canonical B5 collision: b != c but s(b) = s(c) = X."""

    return make_state_labeled_world(
        block,
        {
            "a": "A",
            "b": "X",
            "c": "X",
            "d": "D",
            "e": "E",
            "f": "F",
        },
    )


def state_collision_groups(
    assignment: Mapping[str, StateValue] | StateAssignment,
) -> dict[StateValue, frozenset[str]]:
    """Return only state values that are shared by multiple events."""

    mapping = dict(assignment)
    groups: dict[StateValue, set[str]] = {}
    for event, state in mapping.items():
        groups.setdefault(state, set()).add(event)
    return {
        state: frozenset(events)
        for state, events in groups.items()
        if len(events) > 1
    }


def project_state_labeled_view(world: StateLabeledWorld, event: str) -> StateLabeledView:
    """Project one ID-preserving one-hop view with an attached owner state."""

    if event not in world.block.events:
        raise KeyError(f"unknown event: {event}")
    states = world.states()
    predecessors = frozenset(
        source for source, target in world.block.direct_edges if target == event
    )
    successors = frozenset(
        target for source, target in world.block.direct_edges if source == event
    )
    return StateLabeledView(event, states[event], predecessors, successors)


def project_all_state_labeled_views(world: StateLabeledWorld) -> tuple[StateLabeledView, ...]:
    """Project one state-labeled view per event."""

    return tuple(
        project_state_labeled_view(world, event)
        for event in sorted(world.block.events)
    )


def glue_state_labeled_views(views: Iterable[StateLabeledView]) -> StateReconstruction:
    """Reconstruct by event ID; equal state values are deliberately allowed."""

    materialized = tuple(views)
    if not materialized:
        raise ValueError("cannot glue an empty state-labeled view family")

    ids = [view.event_id for view in materialized]
    if len(ids) != len(set(ids)):
        raise ValueError("state-labeled view family contains duplicate event IDs")

    structural_views = tuple(
        LocalView(view.event_id, view.predecessors, view.successors)
        for view in materialized
    )
    consistency = check_view_consistency(structural_views)
    if not consistency.consistent:
        raise ValueError(
            "inconsistent state-labeled local views: "
            f"unknown_references={sorted(consistency.unknown_references)}, "
            f"missing_from_incoming={sorted(consistency.missing_from_incoming)}, "
            f"missing_from_outgoing={sorted(consistency.missing_from_outgoing)}"
        )

    event_ids = frozenset(ids)
    block = make_block(event_ids, consistency.outgoing_edges)
    assignment = {view.event_id: view.state_value for view in materialized}
    world = make_state_labeled_world(block, assignment)
    return StateReconstruction(world, state_collision_groups(assignment))


def collapse_world_by_state(world: StateLabeledWorld) -> Block:
    """Deliberately incorrect control: treat state values as node identities."""

    states = world.states()
    collapsed_events = frozenset(states.values())
    collapsed_edges = frozenset(
        (states[source], states[target])
        for source, target in world.block.direct_edges
        if states[source] != states[target]
    )
    return make_block(collapsed_events, collapsed_edges)
