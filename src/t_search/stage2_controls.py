"""Stage 2F controls for renaming, repeated states, and operational comparison.

These helpers do not add new Stage 2 ontology. They test whether conclusions from
Stages 2A-2E depend on bookkeeping event names, collapse repeated state values, or
silently compare different parameterizations.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Hashable, Mapping

from .stage1 import EventId
from .stage2 import BranchingStructure, History, Prefix, make_branching_structure
from .stage2_epistemic import (
    EpistemicHistoryModel,
    belief_distribution,
    make_epistemic_history_model,
)
from .stage2_ontic import (
    OnticExtensionModel,
    extension_distribution,
    make_ontic_extension_model,
)
from .stage2_operational import OperationalView

StateValue = Hashable
EventRenaming = Mapping[EventId, EventId]
StateLabels = Mapping[EventId, StateValue]


def validate_event_renaming(
    substrate: BranchingStructure,
    renaming: EventRenaming,
) -> dict[EventId, EventId]:
    """Require a total injective rename of every event in one substrate."""

    materialized = dict(renaming)
    if set(materialized) != set(substrate.events):
        raise ValueError("renaming must specify exactly every event in the substrate")
    if len(set(materialized.values())) != len(materialized):
        raise ValueError("event renaming must be injective")
    return materialized


def rename_history(history: History, renaming: EventRenaming) -> History:
    """Rename an event history under a supplied total map for its events."""

    try:
        return tuple(renaming[event] for event in history)
    except KeyError as exc:
        raise ValueError(f"renaming is missing event {exc.args[0]!r}") from exc


def rename_prefix(prefix: Prefix, renaming: EventRenaming) -> Prefix:
    """Rename an actual/evidence prefix."""

    return rename_history(prefix, renaming)


def rename_branching_structure(
    substrate: BranchingStructure,
    renaming: EventRenaming,
) -> BranchingStructure:
    """Return an isomorphic rooted branching structure with renamed event IDs."""

    mapping = validate_event_renaming(substrate, renaming)
    return make_branching_structure(
        events={mapping[event] for event in substrate.events},
        direct_edges={
            (mapping[source], mapping[target])
            for source, target in substrate.direct_edges
        },
        root=mapping[substrate.root],
    )


def rename_epistemic_model(
    model: EpistemicHistoryModel,
    renaming: EventRenaming,
) -> EpistemicHistoryModel:
    """Transport an epistemic-history model along a pure event renaming."""

    mapping = validate_event_renaming(model.substrate, renaming)
    renamed_substrate = rename_branching_structure(model.substrate, mapping)
    renamed_selected = rename_history(model.selected_history, mapping)
    renamed_beliefs = {
        rename_history(history, mapping): weight
        for history, weight in belief_distribution(model).items()
    }
    return make_epistemic_history_model(
        renamed_substrate,
        renamed_selected,
        renamed_beliefs,
    )


def rename_ontic_model(
    model: OnticExtensionModel,
    renaming: EventRenaming,
) -> OnticExtensionModel:
    """Transport an ontic-extension state along a pure event renaming."""

    mapping = validate_event_renaming(model.substrate, renaming)
    renamed_substrate = rename_branching_structure(model.substrate, mapping)
    renamed_actuality = rename_prefix(model.actuality, mapping)
    renamed_weights = {
        rename_history(history, mapping): weight
        for history, weight in extension_distribution(model).items()
    }
    return make_ontic_extension_model(
        renamed_substrate,
        renamed_actuality,
        renamed_weights,
    )


def rename_operational_view(
    view: OperationalView,
    renaming: EventRenaming,
) -> OperationalView:
    """Transport an OperationalView under the same bookkeeping renaming."""

    renamed_actuality = rename_prefix(view.actuality, renaming)
    renamed_next = tuple(sorted(renaming[event] for event in view.next_events))
    renamed_probabilities = tuple(
        sorted((renaming[event], probability) for event, probability in view.next_probabilities)
    )
    return OperationalView(
        actuality=renamed_actuality,
        next_events=renamed_next,
        next_probabilities=renamed_probabilities,
    )


def validate_state_labels(
    substrate: BranchingStructure,
    state_labels: StateLabels,
) -> dict[EventId, StateValue]:
    """Require one state/configuration value for each event without using it as ID."""

    materialized = dict(state_labels)
    if set(materialized) != set(substrate.events):
        raise ValueError("state labels must specify exactly every event in the substrate")
    return materialized


def state_collision_groups(
    substrate: BranchingStructure,
    state_labels: StateLabels,
) -> dict[StateValue, frozenset[EventId]]:
    """Return repeated-state groups while preserving distinct event identities."""

    labels = validate_state_labels(substrate, state_labels)
    grouped: dict[StateValue, set[EventId]] = defaultdict(set)
    for event, state in labels.items():
        grouped[state].add(event)
    return {
        state: frozenset(events)
        for state, events in grouped.items()
        if len(events) > 1
    }


def operational_next_state_values(
    view: OperationalView,
    state_labels: StateLabels,
) -> frozenset[StateValue]:
    """Project immediate event alternatives to state values for a collapse control."""

    return frozenset(state_labels[event] for event in view.next_events)
