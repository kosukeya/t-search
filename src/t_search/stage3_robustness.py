"""Stage 3G: robustness helpers for relabeling, boundary, and balance controls.

This module adds no new temporal ontology.  It stress-tests structures already
isolated in Stages 3A--3F under bookkeeping relabeling, repeated state values,
memory-boundary variation, and forward/reverse mixture balance.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction

from .stage3 import (
    Microstate,
    Trajectory,
    TrajectoryEnsemble,
    canonical_forward_ensemble,
    forward_trajectory,
    make_trajectory_ensemble,
    reverse_ensemble,
)
from .stage3_asymmetry import RecordOrientationAssessment
from .stage3_controls import mix_ensembles
from .stage3_diagnostics import record_profile


@dataclass(frozen=True)
class PositionRenaming:
    """Pure bookkeeping names for the three neutral trajectory positions."""

    labels: tuple[str, str, str]

    def __post_init__(self) -> None:
        if len(self.labels) != 3 or len(set(self.labels)) != 3:
            raise ValueError("position labels must be three unique names")
        if any(not isinstance(label, str) or not label.strip() for label in self.labels):
            raise ValueError("position labels must be non-empty strings")

    def label(self, position: int) -> str:
        if position not in (0, 1, 2):
            raise ValueError("position must be one of 0, 1, 2")
        return self.labels[position]


@dataclass(frozen=True)
class PositionedMicrostate:
    """Keep occurrence/position identity separate from repeated state value."""

    position: int
    state: Microstate

    def __post_init__(self) -> None:
        if self.position not in (0, 1, 2):
            raise ValueError("position must be one of 0, 1, 2")


def position_tagged_trajectory(trajectory: Trajectory) -> tuple[PositionedMicrostate, ...]:
    """Return position-tagged occurrences without collapsing repeated values."""

    return tuple(PositionedMicrostate(position, state) for position, state in enumerate(trajectory))


def relabeled_record_profile(
    ensemble: TrajectoryEnsemble,
    renaming: PositionRenaming,
) -> tuple[tuple[str, float], ...]:
    """Attach arbitrary bookkeeping names to the unchanged record profile."""

    profile = record_profile(ensemble, current_position=1)
    return tuple((renaming.label(position), profile[position]) for position in (0, 1, 2))


def relabeled_selected_side(
    assessment: RecordOrientationAssessment,
    renaming: PositionRenaming,
) -> str | None:
    """Translate a neutral orientation to the corresponding arbitrary label."""

    if assessment.orientation == "lower-index":
        return renaming.label(0)
    if assessment.orientation == "upper-index":
        return renaming.label(2)
    if assessment.orientation is None:
        return None
    raise ValueError(f"unknown orientation: {assessment.orientation!r}")


def _as_unit_fraction(value: Fraction | int) -> Fraction:
    materialized = Fraction(value)
    if materialized < 0 or materialized > 1:
        raise ValueError("probability must lie in [0,1]")
    return materialized


def biased_memory_initial_distribution(
    memory_zero_probability: Fraction | int,
) -> dict[Microstate, Fraction]:
    """Return independent uniform X,N and a tunable binary memory boundary.

    ``P(M_0=0)=p`` and ``P(M_0=1)=1-p``.  Zero-weight states are omitted.
    This varies global preparation rather than local readout quality.
    """

    p_zero = _as_unit_fraction(memory_zero_probability)
    distribution: dict[Microstate, Fraction] = {}
    for x in (0, 1):
        for n in (0, 1):
            for m, memory_weight in ((0, p_zero), (1, 1 - p_zero)):
                weight = Fraction(1, 4) * memory_weight
                if weight > 0:
                    distribution[Microstate(x, m, n)] = weight
    return distribution


def biased_memory_forward_ensemble(
    memory_zero_probability: Fraction | int,
) -> TrajectoryEnsemble:
    """Run canonical reversible maps from a tunable memory-boundary ensemble."""

    initial = biased_memory_initial_distribution(memory_zero_probability)
    return make_trajectory_ensemble(
        (forward_trajectory(state), weight) for state, weight in initial.items()
    )


def forward_reverse_balance_ensemble(
    forward_weight: Fraction | int,
) -> TrajectoryEnsemble:
    """Return ``w*mu_fwd + (1-w)*J_*mu_fwd`` for exact ``0<=w<=1``."""

    weight = _as_unit_fraction(forward_weight)
    forward = canonical_forward_ensemble()
    reversed_ensemble = reverse_ensemble(forward)
    if weight == 1:
        return forward
    if weight == 0:
        return reversed_ensemble
    return mix_ensembles(
        (
            (forward, weight),
            (reversed_ensemble, 1 - weight),
        )
    )
