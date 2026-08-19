"""Stage 3F: controlled local-access degradation without changing the global block.

The global Stage 3 trajectory ensemble remains fixed.  Accessibility is changed only
through an explicit observation channel over the declared local interface.  This
keeps separate:

- information present in the global microstate/trajectory ensemble;
- information available through one local observation channel.

The canonical record readout can be passed through an exact binary-symmetric
channel (BSC).  Current ``X`` can independently be exposed or masked.  Readout
noise is an interface model, not a microscopic irreversible update and not a claim
that inaccessible information is ontologically absent.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from math import log2
from typing import Callable, Hashable

from .stage3 import Trajectory
from .stage3_local import Stage3RecordBlock


@dataclass(frozen=True)
class LocalAccessPolicy:
    """Declared observation interface at one neutral trajectory position.

    ``record_error_probability`` is restricted to ``[0,1/2]`` because Stage 3F
    studies monotone degradation of a binary readout rather than an invertibly
    relabeled channel with error probability greater than one half.
    """

    expose_x: bool = True
    expose_m: bool = True
    record_error_probability: Fraction = Fraction(0, 1)

    def __post_init__(self) -> None:
        epsilon = Fraction(self.record_error_probability)
        if epsilon < 0 or epsilon > Fraction(1, 2):
            raise ValueError("record_error_probability must lie in [0, 1/2]")
        if not self.expose_m and epsilon != 0:
            raise ValueError("record noise is undefined when the record readout is hidden")
        object.__setattr__(self, "record_error_probability", epsilon)


@dataclass(frozen=True)
class LocalObservationSample:
    """One exact weighted branch of the local observation channel."""

    trajectory: Trajectory
    observed_x: int | None
    observed_m: int | None
    weight: Fraction

    def __post_init__(self) -> None:
        if self.observed_x not in (None, 0, 1):
            raise ValueError("observed_x must be a bit or None")
        if self.observed_m not in (None, 0, 1):
            raise ValueError("observed_m must be a bit or None")
        if self.weight <= 0:
            raise ValueError("observation sample weights must be strictly positive")


@dataclass(frozen=True)
class LocalObservationEnsemble:
    """Exact distribution induced by a local access policy over a fixed block."""

    position: int
    policy: LocalAccessPolicy
    samples: tuple[LocalObservationSample, ...]

    def __post_init__(self) -> None:
        if self.position not in (0, 1, 2):
            raise ValueError("position must be one of 0, 1, 2")
        if not self.samples:
            raise ValueError("observation ensemble must contain at least one sample")
        total = sum((sample.weight for sample in self.samples), Fraction(0, 1))
        if total != Fraction(1, 1):
            raise ValueError(f"observation sample weights must sum to one; got {total}")


ObservationOutcome = tuple[int | None, int | None]
SampleVariable = Callable[[LocalObservationSample], Hashable]


def make_local_observation_ensemble(
    block: Stage3RecordBlock,
    policy: LocalAccessPolicy,
    *,
    position: int = 1,
) -> LocalObservationEnsemble:
    """Apply an exact local observation channel without modifying ``block``.

    When ``M`` is exposed, the true register bit is passed through a BSC with
    error probability ``epsilon``.  ``X`` is either copied exactly or masked.
    The trajectory prior remains the exact weight from the global block.
    """

    if position not in (0, 1, 2):
        raise ValueError("position must be one of 0, 1, 2")

    epsilon = policy.record_error_probability
    samples: list[LocalObservationSample] = []

    for trajectory, prior in block.ensemble.weighted_trajectories:
        state = trajectory[position]
        observed_x = state.x if policy.expose_x else None

        if not policy.expose_m:
            samples.append(
                LocalObservationSample(
                    trajectory=trajectory,
                    observed_x=observed_x,
                    observed_m=None,
                    weight=prior,
                )
            )
            continue

        correct_weight = prior * (Fraction(1, 1) - epsilon)
        error_weight = prior * epsilon
        if correct_weight > 0:
            samples.append(
                LocalObservationSample(
                    trajectory=trajectory,
                    observed_x=observed_x,
                    observed_m=state.m,
                    weight=correct_weight,
                )
            )
        if error_weight > 0:
            samples.append(
                LocalObservationSample(
                    trajectory=trajectory,
                    observed_x=observed_x,
                    observed_m=1 - state.m,
                    weight=error_weight,
                )
            )

    return LocalObservationEnsemble(position=position, policy=policy, samples=tuple(samples))


def _distribution(
    ensemble: LocalObservationEnsemble,
    variable: SampleVariable,
) -> dict[Hashable, Fraction]:
    distribution: dict[Hashable, Fraction] = defaultdict(Fraction)
    for sample in ensemble.samples:
        distribution[variable(sample)] += sample.weight
    return dict(sorted(distribution.items(), key=lambda item: repr(item[0])))


def _joint_distribution(
    ensemble: LocalObservationEnsemble,
    first: SampleVariable,
    second: SampleVariable,
) -> dict[tuple[Hashable, Hashable], Fraction]:
    distribution: dict[tuple[Hashable, Hashable], Fraction] = defaultdict(Fraction)
    for sample in ensemble.samples:
        distribution[(first(sample), second(sample))] += sample.weight
    return dict(sorted(distribution.items(), key=lambda item: repr(item[0])))


def _mutual_information(
    ensemble: LocalObservationEnsemble,
    first: SampleVariable,
    second: SampleVariable,
) -> float:
    joint = _joint_distribution(ensemble, first, second)
    first_marginal: dict[Hashable, Fraction] = defaultdict(Fraction)
    second_marginal: dict[Hashable, Fraction] = defaultdict(Fraction)
    for (first_value, second_value), probability in joint.items():
        first_marginal[first_value] += probability
        second_marginal[second_value] += probability

    information = 0.0
    for (first_value, second_value), probability in joint.items():
        denominator = first_marginal[first_value] * second_marginal[second_value]
        information += float(probability) * log2(float(probability / denominator))
    return information


def _bayes_accuracy(
    ensemble: LocalObservationEnsemble,
    predictor: SampleVariable,
    target: SampleVariable,
) -> float:
    joint = _joint_distribution(ensemble, predictor, target)
    grouped: dict[Hashable, list[Fraction]] = defaultdict(list)
    for (predictor_value, _), probability in joint.items():
        grouped[predictor_value].append(probability)
    return float(sum((max(probabilities) for probabilities in grouped.values()), Fraction(0, 1)))


def _target_x(position: int) -> SampleVariable:
    if position not in (0, 1, 2):
        raise ValueError("target position must be one of 0, 1, 2")

    def target(sample: LocalObservationSample) -> int:
        return sample.trajectory[position].x

    return target


def _full_local_predictor(sample: LocalObservationSample) -> ObservationOutcome:
    return (sample.observed_x, sample.observed_m)


def _record_predictor(sample: LocalObservationSample) -> int:
    if sample.observed_m is None:
        raise ValueError("record readout is hidden under this access policy")
    return sample.observed_m


def local_observation_mutual_information(
    ensemble: LocalObservationEnsemble,
    *,
    target_position: int,
) -> float:
    """Return information in the entire exposed local observation about ``X_j``."""

    return _mutual_information(ensemble, _full_local_predictor, _target_x(target_position))


def local_observation_decoding_accuracy(
    ensemble: LocalObservationEnsemble,
    *,
    target_position: int,
) -> float:
    """Return optimal decoding accuracy from all exposed local fields."""

    return _bayes_accuracy(ensemble, _full_local_predictor, _target_x(target_position))


def record_readout_mutual_information(
    ensemble: LocalObservationEnsemble,
    *,
    target_position: int,
) -> float:
    """Return information carried specifically by the exposed record readout."""

    if not ensemble.policy.expose_m:
        raise ValueError("record readout is hidden under this access policy")
    return _mutual_information(ensemble, _record_predictor, _target_x(target_position))


def record_readout_decoding_accuracy(
    ensemble: LocalObservationEnsemble,
    *,
    target_position: int,
) -> float:
    """Return optimal target decoding accuracy from the record readout alone."""

    if not ensemble.policy.expose_m:
        raise ValueError("record readout is hidden under this access policy")
    return _bayes_accuracy(ensemble, _record_predictor, _target_x(target_position))


def record_readout_profile(
    ensemble: LocalObservationEnsemble,
) -> dict[int, float]:
    """Information profile of the accessible/noisy record readout across positions."""

    return {
        position: record_readout_mutual_information(ensemble, target_position=position)
        for position in (0, 1, 2)
    }


def record_readout_accessibility_profile(
    ensemble: LocalObservationEnsemble,
) -> dict[int, float]:
    """Bayes-decoding profile of the accessible/noisy record readout."""

    return {
        position: record_readout_decoding_accuracy(ensemble, target_position=position)
        for position in (0, 1, 2)
    }


def record_readout_arrow_score(
    ensemble: LocalObservationEnsemble,
    *,
    delta: int = 1,
) -> float:
    """Signed accessible-record information contrast around the current position."""

    lower = ensemble.position - delta
    upper = ensemble.position + delta
    if delta <= 0 or lower not in (0, 1, 2) or upper not in (0, 1, 2):
        raise ValueError("both comparison positions must exist and delta must be positive")
    profile = record_readout_profile(ensemble)
    return profile[lower] - profile[upper]


def record_readout_accessibility_arrow_score(
    ensemble: LocalObservationEnsemble,
    *,
    delta: int = 1,
) -> float:
    """Signed accessible-record decoder contrast around the current position."""

    lower = ensemble.position - delta
    upper = ensemble.position + delta
    if delta <= 0 or lower not in (0, 1, 2) or upper not in (0, 1, 2):
        raise ValueError("both comparison positions must exist and delta must be positive")
    profile = record_readout_accessibility_profile(ensemble)
    return profile[lower] - profile[upper]


def outcome_distribution(
    ensemble: LocalObservationEnsemble,
) -> dict[ObservationOutcome, Fraction]:
    """Return the exact distribution over exposed local outcomes."""

    return _distribution(ensemble, _full_local_predictor)  # type: ignore[return-value]


def posterior_histories_given_outcome(
    ensemble: LocalObservationEnsemble,
    outcome: ObservationOutcome,
) -> tuple[tuple[Trajectory, Fraction], ...]:
    """Return exact posterior weights over global histories for one local outcome.

    A history is considered compatible when the declared observation channel gives
    the outcome positive probability.  This is epistemic/interface compatibility,
    not ontic possibility.
    """

    raw: dict[Trajectory, Fraction] = defaultdict(Fraction)
    for sample in ensemble.samples:
        if _full_local_predictor(sample) == outcome:
            raw[sample.trajectory] += sample.weight

    total = sum(raw.values(), Fraction(0, 1))
    if total <= 0:
        raise ValueError("outcome has zero probability under the declared access channel")

    return tuple(
        (trajectory, weight / total)
        for trajectory, weight in sorted(raw.items(), key=lambda item: repr(item[0]))
    )


def compatible_history_count(
    ensemble: LocalObservationEnsemble,
    outcome: ObservationOutcome,
) -> int:
    """Count positive-posterior global histories for one observed outcome."""

    return len(posterior_histories_given_outcome(ensemble, outcome))
