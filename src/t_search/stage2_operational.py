"""Stage 2D: ontology-neutral operational interface for Stage 2 local views.

The epistemic and ontic models intentionally use different Potentiality types and
internal semantics. This module erases those semantic/type distinctions and keeps
only the observables fixed by the Stage 2 protocol:

    O(G) = (A_now, Next(D), pi(next | D)).

Operational equality under this interface is not ontological equality.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose

from .stage1 import EventId
from .stage2 import History, Prefix, is_prefix
from .stage2_epistemic import EpistemicLocalView
from .stage2_ontic import OnticLocalView


@dataclass(frozen=True)
class OperationalView:
    """Ontology-neutral Stage 2 operational view O(G)."""

    actuality: Prefix
    next_events: tuple[EventId, ...]
    next_probabilities: tuple[tuple[EventId, float], ...]


@dataclass(frozen=True)
class OperationalComparison:
    """Component-wise comparison of two ontology-neutral operational views."""

    equal: bool
    actuality_equal: bool
    next_events_equal: bool
    probabilities_equal: bool


def _next_events_from_histories(
    actuality: Prefix,
    histories: tuple[History, ...],
) -> tuple[EventId, ...]:
    """Derive immediate alternatives from the live Potentiality carrier."""

    index = len(actuality)
    events: set[EventId] = set()
    for history in histories:
        if not is_prefix(actuality, history):
            raise ValueError(
                "Potentiality contains a history incompatible with current Actuality"
            )
        if index < len(history):
            events.add(history[index])
    return tuple(sorted(events))


def _normalize_probability_tuple(
    next_events: tuple[EventId, ...],
    probabilities: tuple[tuple[EventId, float], ...],
) -> tuple[tuple[EventId, float], ...]:
    """Canonicalize and validate the predictive distribution for comparison."""

    materialized = dict(probabilities)
    if set(materialized) != set(next_events):
        raise ValueError(
            "next-probability keys must match the immediate alternatives exactly"
        )
    return tuple((event, float(materialized[event])) for event in next_events)


def operationalize_epistemic_view(view: EpistemicLocalView) -> OperationalView:
    """Erase epistemic Potentiality semantics and retain only O(G_E)."""

    next_events = _next_events_from_histories(
        view.actuality,
        view.potentiality.histories,
    )
    return OperationalView(
        actuality=view.actuality,
        next_events=next_events,
        next_probabilities=_normalize_probability_tuple(
            next_events,
            view.next_probabilities,
        ),
    )


def operationalize_ontic_view(view: OnticLocalView) -> OperationalView:
    """Erase ontic Potentiality semantics and retain only O(G_O)."""

    next_events = _next_events_from_histories(
        view.actuality,
        view.potentiality.histories,
    )
    return OperationalView(
        actuality=view.actuality,
        next_events=next_events,
        next_probabilities=_normalize_probability_tuple(
            next_events,
            view.next_probabilities,
        ),
    )


def compare_operational_views(
    left: OperationalView,
    right: OperationalView,
    *,
    abs_tol: float = 1e-12,
) -> OperationalComparison:
    """Compare operational views without inspecting model types or hidden state."""

    actuality_equal = left.actuality == right.actuality
    next_events_equal = left.next_events == right.next_events

    left_probabilities = dict(left.next_probabilities)
    right_probabilities = dict(right.next_probabilities)
    probabilities_equal = set(left_probabilities) == set(right_probabilities) and all(
        isclose(
            left_probabilities[event],
            right_probabilities[event],
            rel_tol=0.0,
            abs_tol=abs_tol,
        )
        for event in left_probabilities
    )

    equal = actuality_equal and next_events_equal and probabilities_equal
    return OperationalComparison(
        equal=equal,
        actuality_equal=actuality_equal,
        next_events_equal=next_events_equal,
        probabilities_equal=probabilities_equal,
    )
