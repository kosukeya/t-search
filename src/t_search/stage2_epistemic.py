"""Stage 2B: epistemic-history model over the neutral Stage 2 substrate.

The model contains one complete selected history ``h*`` globally, while local
projection deliberately ignores that hidden selector and derives predictions only
from the current evidence prefix and epistemic belief distribution.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import isclose, isfinite
from typing import Mapping

from .stage2 import (
    BranchingStructure,
    EventId,
    History,
    Prefix,
    canonical_stage2_substrate,
    extend_prefix,
    extensions,
    is_prefix,
    validate_prefix,
)

BeliefWeights = tuple[tuple[History, float], ...]


@dataclass(frozen=True)
class EpistemicPotentiality:
    """Typed set of live hypotheses about the already-selected complete history."""

    histories: tuple[History, ...]


@dataclass(frozen=True)
class EpistemicLocalView:
    """Stage 2B local view G_E(D), intentionally excluding the hidden h*."""

    actuality: Prefix
    potentiality: EpistemicPotentiality
    next_probabilities: tuple[tuple[EventId, float], ...]


@dataclass(frozen=True)
class EpistemicHistoryModel:
    """M_E = (T, h*, q_E)."""

    substrate: BranchingStructure
    selected_history: History
    belief_weights: BeliefWeights


def make_epistemic_history_model(
    substrate: BranchingStructure,
    selected_history: History,
    belief_weights: Mapping[History, float],
) -> EpistemicHistoryModel:
    """Create a validated epistemic-history model.

    The local belief distribution must explicitly cover every complete history in
    the substrate, sum to one, and retain positive support for the selected actual
    history. The final condition ensures that h* belongs to current epistemic
    Potentiality before any discriminating evidence is supplied.
    """

    selected = tuple(selected_history)
    histories = tuple(substrate.histories)
    history_set = set(histories)

    if selected not in history_set:
        raise ValueError(
            "selected_history must be a complete maximal history of the substrate"
        )

    materialized = {
        tuple(history): float(weight)
        for history, weight in belief_weights.items()
    }
    if set(materialized) != history_set:
        raise ValueError(
            "belief distribution must specify exactly all complete histories"
        )

    if any(
        not isfinite(weight) or weight < 0.0
        for weight in materialized.values()
    ):
        raise ValueError("belief weights must be finite and non-negative")

    total = sum(materialized.values())
    if not isclose(total, 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError(f"belief weights must sum to 1; got {total}")

    if materialized[selected] <= 0.0:
        raise ValueError("selected history must have positive epistemic support")

    frozen = tuple((history, materialized[history]) for history in histories)
    return EpistemicHistoryModel(substrate, selected, frozen)


def canonical_epistemic_model(
    *,
    selected_history: History | None = None,
) -> EpistemicHistoryModel:
    """Return the Stage 2B baseline with equal beliefs over h_L and h_R."""

    substrate = canonical_stage2_substrate()
    h_left = ("p", "n", "l1", "l2")
    h_right = ("p", "n", "r1")
    selected = h_left if selected_history is None else tuple(selected_history)
    return make_epistemic_history_model(
        substrate,
        selected,
        {
            h_left: 0.5,
            h_right: 0.5,
        },
    )


def belief_distribution(model: EpistemicHistoryModel) -> dict[History, float]:
    """Materialize q_E as a dictionary for diagnostics and conditioning."""

    return dict(model.belief_weights)


def selected_history(model: EpistemicHistoryModel) -> History:
    """Privileged global diagnostic. This is not a local observable."""

    return model.selected_history


def _conditional_distribution(
    model: EpistemicHistoryModel,
    prefix: Prefix,
) -> dict[History, float]:
    """Condition q_E on a supplied evidence prefix without consulting h*."""

    materialized = validate_prefix(model.substrate, prefix)
    raw = belief_distribution(model)
    live = {
        history: raw[history]
        for history in extensions(model.substrate, materialized)
        if raw[history] > 0.0
    }
    total = sum(live.values())
    if total <= 0.0:
        raise ValueError("current evidence has zero epistemic support")
    return {history: weight / total for history, weight in live.items()}


def epistemic_potentiality(
    model: EpistemicHistoryModel,
    prefix: Prefix,
) -> EpistemicPotentiality:
    """Return EPot(D): live hypotheses with positive conditional support."""

    conditional = _conditional_distribution(model, prefix)
    return EpistemicPotentiality(tuple(conditional))


def epistemic_next_probabilities(
    model: EpistemicHistoryModel,
    prefix: Prefix,
) -> tuple[tuple[EventId, float], ...]:
    """Marginalize conditional history beliefs to immediate-next events."""

    materialized = validate_prefix(model.substrate, prefix)
    conditional = _conditional_distribution(model, materialized)
    index = len(materialized)
    totals: dict[EventId, float] = {}

    for history, weight in conditional.items():
        if index >= len(history):
            continue
        event = history[index]
        totals[event] = totals.get(event, 0.0) + weight

    return tuple(sorted(totals.items()))


def project_epistemic_view(
    model: EpistemicHistoryModel,
    prefix: Prefix,
) -> EpistemicLocalView:
    """Project M_E to G_E(D) without exposing or consulting the hidden h*."""

    materialized = validate_prefix(model.substrate, prefix)
    return EpistemicLocalView(
        actuality=materialized,
        potentiality=epistemic_potentiality(model, materialized),
        next_probabilities=epistemic_next_probabilities(model, materialized),
    )


def actual_next_from_hidden_history(
    model: EpistemicHistoryModel,
    prefix: Prefix,
) -> EventId | None:
    """Privileged diagnostic revealing the next event encoded by h*."""

    materialized = validate_prefix(model.substrate, prefix)
    if not is_prefix(materialized, model.selected_history):
        raise ValueError("prefix is incompatible with the hidden selected history")
    if len(materialized) == len(model.selected_history):
        return None
    return model.selected_history[len(materialized)]


def condition_epistemic_model(
    model: EpistemicHistoryModel,
    prefix: Prefix,
    observed_next: EventId,
) -> tuple[EpistemicHistoryModel, Prefix]:
    """Condition q_E after an explicit observation while leaving h* unchanged.

    The baseline treats this as an actual-run update. An observation inconsistent
    with the already-selected complete history is rejected rather than silently
    replacing h*.
    """

    materialized = validate_prefix(model.substrate, prefix)
    updated_prefix = extend_prefix(model.substrate, materialized, observed_next)

    if not is_prefix(updated_prefix, model.selected_history):
        raise ValueError("observation contradicts the hidden selected history")

    raw = belief_distribution(model)
    survivors = {
        history: raw[history] if is_prefix(updated_prefix, history) else 0.0
        for history in model.substrate.histories
    }
    total = sum(survivors.values())
    if total <= 0.0:
        raise ValueError("observation has zero epistemic support")

    normalized = {
        history: weight / total
        for history, weight in survivors.items()
    }
    updated_model = make_epistemic_history_model(
        model.substrate,
        model.selected_history,
        normalized,
    )
    return updated_model, updated_prefix
