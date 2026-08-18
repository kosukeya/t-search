"""Stage 2C: ontic-extension model over the neutral Stage 2 substrate.

The model represents current Actuality plus every admissible complete extension and
associated weights. It deliberately contains no selected complete future or hidden
future selector. This is a formal modeling choice, not evidence of ontic openness in
physical reality.
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

ExtensionWeights = tuple[tuple[History, float], ...]


@dataclass(frozen=True)
class OnticPotentiality:
    """Typed carrier for all admissible complete extensions of current Actuality."""

    histories: tuple[History, ...]


@dataclass(frozen=True)
class OnticLocalView:
    """Stage 2C local view G_O(D), with no selected-history datum."""

    actuality: Prefix
    potentiality: OnticPotentiality
    next_probabilities: tuple[tuple[EventId, float], ...]


@dataclass(frozen=True)
class OnticExtensionModel:
    """M_O(D) = (D, Ext_T(D), K), with no selected complete future."""

    substrate: BranchingStructure
    actuality: Prefix
    potentiality: OnticPotentiality
    extension_weights: ExtensionWeights


def make_ontic_extension_model(
    substrate: BranchingStructure,
    actuality: Prefix,
    extension_weights: Mapping[History, float],
) -> OnticExtensionModel:
    """Create a validated ontic-extension state.

    ``extension_weights`` must cover exactly ``Ext_T(actuality)``. The weights are
    normalized over complete live extensions so their marginal gives immediate-next
    probabilities. No member is designated as the already-selected actual future.
    """

    current = validate_prefix(substrate, actuality)
    live = tuple(extensions(substrate, current))
    live_set = set(live)
    materialized = {
        tuple(history): float(weight)
        for history, weight in extension_weights.items()
    }

    if set(materialized) != live_set:
        raise ValueError(
            "extension weights must specify exactly all admissible complete extensions"
        )

    if any(
        not isfinite(weight) or weight < 0.0
        for weight in materialized.values()
    ):
        raise ValueError("extension weights must be finite and non-negative")

    total = sum(materialized.values())
    if not isclose(total, 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError(f"extension weights must sum to 1; got {total}")

    frozen_weights = tuple((history, materialized[history]) for history in live)
    return OnticExtensionModel(
        substrate=substrate,
        actuality=current,
        potentiality=OnticPotentiality(live),
        extension_weights=frozen_weights,
    )


def canonical_ontic_model(
    *,
    actuality: Prefix = ("p", "n"),
) -> OnticExtensionModel:
    """Return the Stage 2C baseline with uniform weight over live extensions."""

    substrate = canonical_stage2_substrate()
    current = validate_prefix(substrate, actuality)
    live = extensions(substrate, current)
    uniform = 1.0 / len(live)
    return make_ontic_extension_model(
        substrate,
        current,
        {history: uniform for history in live},
    )


def extension_distribution(model: OnticExtensionModel) -> dict[History, float]:
    """Materialize K over current complete admissible extensions."""

    return dict(model.extension_weights)


def ontic_next_probabilities(
    model: OnticExtensionModel,
) -> tuple[tuple[EventId, float], ...]:
    """Marginalize extension weights to the immediate next event."""

    current = validate_prefix(model.substrate, model.actuality)
    index = len(current)
    totals: dict[EventId, float] = {}

    for history, weight in model.extension_weights:
        if index >= len(history):
            continue
        event = history[index]
        totals[event] = totals.get(event, 0.0) + weight

    return tuple(sorted(totals.items()))


def project_ontic_view(model: OnticExtensionModel) -> OnticLocalView:
    """Project M_O(D) to its current modal local view."""

    return OnticLocalView(
        actuality=model.actuality,
        potentiality=model.potentiality,
        next_probabilities=ontic_next_probabilities(model),
    )


def update_ontic_model(
    model: OnticExtensionModel,
    observed_next: EventId,
) -> OnticExtensionModel:
    """Extend Actuality by an explicit observation and prune incompatible futures.

    The update never creates a selected complete future. It only lengthens the
    actual prefix, restricts ``Ext_T(D)``, and renormalizes surviving weights.
    """

    updated_actuality = extend_prefix(
        model.substrate,
        model.actuality,
        observed_next,
    )
    raw = extension_distribution(model)
    survivors = {
        history: weight
        for history, weight in raw.items()
        if is_prefix(updated_actuality, history)
    }
    total = sum(survivors.values())
    if total <= 0.0:
        raise ValueError("observation has zero ontic transition weight")

    normalized = {
        history: weight / total
        for history, weight in survivors.items()
    }
    return make_ontic_extension_model(
        model.substrate,
        updated_actuality,
        normalized,
    )
