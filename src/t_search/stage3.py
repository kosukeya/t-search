"""Stage 3A: reversible finite substrate for record experiments.

This module implements only the neutral reversible trajectory machinery needed by
Stage 3. Later stages add record diagnostics and arrow scores. Position indices
remain bookkeeping labels here and are not interpreted as past/future.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import log2
from typing import Callable, Iterable, Mapping

Bit = int
UpdateMap = Callable[["Microstate"], "Microstate"]


@dataclass(frozen=True, order=True)
class Microstate:
    """Complete three-bit microstate ``Z=(X,M,N)``."""

    x: Bit
    m: Bit
    n: Bit

    def __post_init__(self) -> None:
        for name, value in (("x", self.x), ("m", self.m), ("n", self.n)):
            if value not in (0, 1):
                raise ValueError(f"{name} must be a bit, got {value!r}")


Trajectory = tuple[Microstate, Microstate, Microstate]
WeightedTrajectory = tuple[Trajectory, Fraction]


@dataclass(frozen=True)
class TrajectoryEnsemble:
    """Exact finite probability distribution over three-position trajectories."""

    weighted_trajectories: tuple[WeightedTrajectory, ...]

    def __post_init__(self) -> None:
        if not self.weighted_trajectories:
            raise ValueError("trajectory ensemble must be non-empty")

        trajectories = [trajectory for trajectory, _ in self.weighted_trajectories]
        if len(set(trajectories)) != len(trajectories):
            raise ValueError("trajectory ensemble must not contain duplicate trajectories")

        weights = [weight for _, weight in self.weighted_trajectories]
        if any(weight <= 0 for weight in weights):
            raise ValueError("trajectory weights must be strictly positive")
        if sum(weights, Fraction(0, 1)) != Fraction(1, 1):
            raise ValueError("trajectory weights must sum exactly to one")

    @property
    def trajectories(self) -> tuple[Trajectory, ...]:
        return tuple(trajectory for trajectory, _ in self.weighted_trajectories)

    def as_mapping(self) -> dict[Trajectory, Fraction]:
        return dict(self.weighted_trajectories)


def all_microstates() -> tuple[Microstate, ...]:
    """Return the complete eight-state space ``{0,1}^3`` in deterministic order."""

    return tuple(
        Microstate(x, m, n)
        for x in (0, 1)
        for m in (0, 1)
        for n in (0, 1)
    )


def u_rec(state: Microstate) -> Microstate:
    """Reversible recording interaction ``(X,M,N)->(X,M XOR X,N)``."""

    return Microstate(state.x, state.m ^ state.x, state.n)


def u_scr(state: Microstate) -> Microstate:
    """Reversible scrambling interaction ``(X,M,N)->(X XOR N,M,N)``."""

    return Microstate(state.x ^ state.n, state.m, state.n)


def is_bijective(update: UpdateMap) -> bool:
    """Return whether ``update`` is a permutation of the complete microstate space."""

    domain = all_microstates()
    images = tuple(update(state) for state in domain)
    return set(images) == set(domain) and len(set(images)) == len(domain)


def assert_bijective(update: UpdateMap, *, name: str = "update") -> None:
    """Raise when a map claimed as reversible is not bijective on all eight states."""

    if not is_bijective(update):
        raise ValueError(f"{name} is not bijective on the complete microstate space")


def forward_trajectory(initial: Microstate) -> Trajectory:
    """Construct ``z0,z1,z2`` using the protocol-frozen reversible maps."""

    z0 = initial
    z1 = u_rec(z0)
    z2 = u_scr(z1)
    return z0, z1, z2


def is_forward_dynamically_valid(trajectory: Trajectory) -> bool:
    """Check the declared forward map sequence without assigning temporal meaning."""

    z0, z1, z2 = trajectory
    return z1 == u_rec(z0) and z2 == u_scr(z1)


def reverse_trajectory(trajectory: Trajectory) -> Trajectory:
    """Apply the modeled history-reversal map ``J(z0,z1,z2)=(z2,z1,z0)``."""

    z0, z1, z2 = trajectory
    return z2, z1, z0


def is_reverse_dynamically_valid(reversed_trajectory: Trajectory) -> bool:
    """Check reverse motion with inverse maps in reverse order.

    Both canonical updates are self-inverse, so a reversed tuple ``(z2,z1,z0)``
    is valid when ``z1=U_scr^{-1}(z2)`` and ``z0=U_rec^{-1}(z1)``.
    """

    z2, z1, z0 = reversed_trajectory
    return z1 == u_scr(z2) and z0 == u_rec(z1)


def make_trajectory_ensemble(
    weighted_trajectories: Iterable[tuple[Trajectory, Fraction | int]],
) -> TrajectoryEnsemble:
    """Normalize input types and construct an exact validated ensemble."""

    materialized = tuple(
        (trajectory, Fraction(weight)) for trajectory, weight in weighted_trajectories
    )
    return TrajectoryEnsemble(materialized)


def canonical_initial_distribution() -> dict[Microstate, Fraction]:
    """Return the Stage 3 canonical boundary distribution.

    ``X=a`` and ``N=b`` are independent uniform bits while ``M=0``. This is
    only an exact boundary ensemble in Stage 3A; its record interpretation is
    intentionally deferred to Stage 3C.
    """

    quarter = Fraction(1, 4)
    return {
        Microstate(a, 0, b): quarter
        for a in (0, 1)
        for b in (0, 1)
    }


def canonical_forward_ensemble() -> TrajectoryEnsemble:
    """Transport the exact canonical boundary distribution through both maps."""

    return make_trajectory_ensemble(
        (forward_trajectory(initial), weight)
        for initial, weight in canonical_initial_distribution().items()
    )


def reverse_ensemble(ensemble: TrajectoryEnsemble) -> TrajectoryEnsemble:
    """Push an ensemble forward through the modeled history-reversal map ``J``."""

    return make_trajectory_ensemble(
        (reverse_trajectory(trajectory), weight)
        for trajectory, weight in ensemble.weighted_trajectories
    )


def canonical_reversed_ensemble() -> TrajectoryEnsemble:
    """Return ``J_* mu_fwd`` for the canonical exact ensemble."""

    return reverse_ensemble(canonical_forward_ensemble())


def state_marginal(
    ensemble: TrajectoryEnsemble,
    position: int,
) -> dict[Microstate, Fraction]:
    """Return the exact full-microstate distribution at one neutral position."""

    if position not in (0, 1, 2):
        raise ValueError("position must be one of 0, 1, 2")

    marginal: dict[Microstate, Fraction] = {}
    for trajectory, weight in ensemble.weighted_trajectories:
        state = trajectory[position]
        marginal[state] = marginal.get(state, Fraction(0, 1)) + weight
    return dict(sorted(marginal.items()))


def distribution_entropy(distribution: Mapping[object, Fraction]) -> float:
    """Exact-probability Shannon entropy in bits for Stage 3A preservation checks."""

    if not distribution:
        raise ValueError("distribution must be non-empty")
    total = sum(distribution.values(), Fraction(0, 1))
    if total != Fraction(1, 1):
        raise ValueError("distribution probabilities must sum exactly to one")
    if any(probability < 0 for probability in distribution.values()):
        raise ValueError("distribution probabilities must be non-negative")

    return -sum(
        float(probability) * log2(float(probability))
        for probability in distribution.values()
        if probability > 0
    )


def full_state_entropies(ensemble: TrajectoryEnsemble) -> tuple[float, float, float]:
    """Return ``H(Z_0),H(Z_1),H(Z_2)`` for the exact ensemble."""

    return tuple(
        distribution_entropy(state_marginal(ensemble, position))
        for position in (0, 1, 2)
    )  # type: ignore[return-value]
