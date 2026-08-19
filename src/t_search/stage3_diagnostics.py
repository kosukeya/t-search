"""Stage 3B: exact record and accessibility diagnostics.

This module adds measurement machinery on top of the reversible Stage 3A
trajectory ensemble.  It deliberately does not assign physical past/future
meaning to position indices.  Signed scores compare the two sides of a neutral
current position; interpretation is deferred to later Stage 3 checkpoints.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from math import log2
from typing import Callable, Hashable

from .stage3 import Trajectory, TrajectoryEnsemble, distribution_entropy

Variable = Callable[[Trajectory], Hashable]
ComponentName = str

_VALID_POSITIONS = (0, 1, 2)
_VALID_COMPONENTS = ("x", "m", "n")


def _validate_position(position: int) -> None:
    if position not in _VALID_POSITIONS:
        raise ValueError("position must be one of 0, 1, 2")


def _validate_component(component: ComponentName) -> None:
    if component not in _VALID_COMPONENTS:
        raise ValueError("component must be one of 'x', 'm', 'n'")


def _validate_directional_window(current_position: int, delta: int) -> tuple[int, int]:
    _validate_position(current_position)
    if not isinstance(delta, int) or isinstance(delta, bool) or delta <= 0:
        raise ValueError("delta must be a positive integer")

    lower = current_position - delta
    upper = current_position + delta
    if lower not in _VALID_POSITIONS or upper not in _VALID_POSITIONS:
        raise ValueError("both comparison positions must exist")
    return lower, upper


def component_value(
    trajectory: Trajectory,
    position: int,
    component: ComponentName,
) -> int:
    """Read one bit component from one neutral trajectory position."""

    _validate_position(position)
    _validate_component(component)
    return getattr(trajectory[position], component)


def component_variable(position: int, component: ComponentName) -> Variable:
    """Return an extractor for a declared position/component pair."""

    _validate_position(position)
    _validate_component(component)

    def extract(trajectory: Trajectory) -> Hashable:
        return component_value(trajectory, position, component)

    return extract


def variable_distribution(
    ensemble: TrajectoryEnsemble,
    variable: Variable,
) -> dict[Hashable, Fraction]:
    """Return the exact marginal distribution of a trajectory-derived variable."""

    marginal: dict[Hashable, Fraction] = {}
    for trajectory, weight in ensemble.weighted_trajectories:
        value = variable(trajectory)
        marginal[value] = marginal.get(value, Fraction(0, 1)) + weight
    return dict(sorted(marginal.items(), key=lambda item: repr(item[0])))


def joint_distribution(
    ensemble: TrajectoryEnsemble,
    first: Variable,
    second: Variable,
) -> dict[tuple[Hashable, Hashable], Fraction]:
    """Return the exact joint distribution of two trajectory-derived variables."""

    joint: dict[tuple[Hashable, Hashable], Fraction] = {}
    for trajectory, weight in ensemble.weighted_trajectories:
        key = (first(trajectory), second(trajectory))
        joint[key] = joint.get(key, Fraction(0, 1)) + weight
    return dict(sorted(joint.items(), key=lambda item: repr(item[0])))


def component_distribution(
    ensemble: TrajectoryEnsemble,
    position: int,
    component: ComponentName,
) -> dict[Hashable, Fraction]:
    """Return an exact component marginal at one neutral position."""

    return variable_distribution(ensemble, component_variable(position, component))


def component_joint_distribution(
    ensemble: TrajectoryEnsemble,
    first_position: int,
    first_component: ComponentName,
    second_position: int,
    second_component: ComponentName,
) -> dict[tuple[Hashable, Hashable], Fraction]:
    """Return an exact joint distribution for two position/component values."""

    return joint_distribution(
        ensemble,
        component_variable(first_position, first_component),
        component_variable(second_position, second_component),
    )


def variable_entropy(ensemble: TrajectoryEnsemble, variable: Variable) -> float:
    """Shannon entropy ``H(variable)`` in bits."""

    return distribution_entropy(variable_distribution(ensemble, variable))


def component_entropy(
    ensemble: TrajectoryEnsemble,
    position: int,
    component: ComponentName,
) -> float:
    """Shannon entropy of one declared trajectory component in bits."""

    return variable_entropy(ensemble, component_variable(position, component))


def mutual_information(
    ensemble: TrajectoryEnsemble,
    first: Variable,
    second: Variable,
) -> float:
    """Return exact-ensemble mutual information ``I(first;second)`` in bits."""

    joint = joint_distribution(ensemble, first, second)
    first_marginal: dict[Hashable, Fraction] = defaultdict(Fraction)
    second_marginal: dict[Hashable, Fraction] = defaultdict(Fraction)

    for (first_value, second_value), probability in joint.items():
        first_marginal[first_value] += probability
        second_marginal[second_value] += probability

    information = 0.0
    for (first_value, second_value), probability in joint.items():
        if probability == 0:
            continue
        denominator = first_marginal[first_value] * second_marginal[second_value]
        ratio = float(probability / denominator)
        information += float(probability) * log2(ratio)
    return information


def component_mutual_information(
    ensemble: TrajectoryEnsemble,
    first_position: int,
    first_component: ComponentName,
    second_position: int,
    second_component: ComponentName,
) -> float:
    """Mutual information between two declared trajectory components."""

    return mutual_information(
        ensemble,
        component_variable(first_position, first_component),
        component_variable(second_position, second_component),
    )


def conditional_entropy(
    ensemble: TrajectoryEnsemble,
    target: Variable,
    given: Variable,
) -> float:
    """Return conditional entropy ``H(target|given)`` in bits."""

    joint = joint_distribution(ensemble, target, given)
    given_distribution = variable_distribution(ensemble, given)
    return distribution_entropy(joint) - distribution_entropy(given_distribution)


def component_conditional_entropy(
    ensemble: TrajectoryEnsemble,
    target_position: int,
    target_component: ComponentName,
    given_position: int,
    given_component: ComponentName,
) -> float:
    """Conditional entropy for two declared trajectory components."""

    return conditional_entropy(
        ensemble,
        component_variable(target_position, target_component),
        component_variable(given_position, given_component),
    )


def bayes_optimal_accuracy(
    ensemble: TrajectoryEnsemble,
    predictor: Variable,
    target: Variable,
) -> float:
    """Bayes-optimal decoding accuracy for predicting ``target`` from ``predictor``.

    For each predictor value, the optimal decoder chooses the target value with
    largest joint probability.  Summing those maxima gives the exact accuracy.
    """

    joint = joint_distribution(ensemble, predictor, target)
    grouped: dict[Hashable, list[Fraction]] = defaultdict(list)
    for (predictor_value, _), probability in joint.items():
        grouped[predictor_value].append(probability)
    return float(sum((max(probabilities) for probabilities in grouped.values()), Fraction(0, 1)))


def component_decoding_accuracy(
    ensemble: TrajectoryEnsemble,
    predictor_position: int,
    predictor_component: ComponentName,
    target_position: int,
    target_component: ComponentName,
) -> float:
    """Bayes-optimal accuracy between two declared trajectory components."""

    return bayes_optimal_accuracy(
        ensemble,
        component_variable(predictor_position, predictor_component),
        component_variable(target_position, target_component),
    )


def record_profile(
    ensemble: TrajectoryEnsemble,
    *,
    current_position: int = 1,
    record_component: ComponentName = "m",
    target_component: ComponentName = "x",
) -> dict[int, float]:
    """Return ``Q_R(k,j)=I(R_k;X_j)`` over all neutral positions ``j``."""

    _validate_position(current_position)
    _validate_component(record_component)
    _validate_component(target_component)
    return {
        position: component_mutual_information(
            ensemble,
            current_position,
            record_component,
            position,
            target_component,
        )
        for position in _VALID_POSITIONS
    }


def accessibility_profile(
    ensemble: TrajectoryEnsemble,
    *,
    current_position: int = 1,
    record_component: ComponentName = "m",
    target_component: ComponentName = "x",
) -> dict[int, float]:
    """Return Bayes-optimal target accessibility from the current record register."""

    _validate_position(current_position)
    _validate_component(record_component)
    _validate_component(target_component)
    return {
        position: component_decoding_accuracy(
            ensemble,
            current_position,
            record_component,
            position,
            target_component,
        )
        for position in _VALID_POSITIONS
    }


def record_arrow_score(
    ensemble: TrajectoryEnsemble,
    *,
    current_position: int = 1,
    delta: int = 1,
    record_component: ComponentName = "m",
    target_component: ComponentName = "x",
) -> float:
    """Return the signed information contrast across a neutral current position.

    ``A_R(k,delta)=I(R_k;X_{k-delta})-I(R_k;X_{k+delta})``.
    The sign is a property of this declared orientation convention; Stage 3B
    does not rename either side past or future.
    """

    lower, upper = _validate_directional_window(current_position, delta)
    profile = record_profile(
        ensemble,
        current_position=current_position,
        record_component=record_component,
        target_component=target_component,
    )
    return profile[lower] - profile[upper]


def accessibility_arrow_score(
    ensemble: TrajectoryEnsemble,
    *,
    current_position: int = 1,
    delta: int = 1,
    record_component: ComponentName = "m",
    target_component: ComponentName = "x",
) -> float:
    """Return the signed Bayes-decoding accessibility contrast across ``k``."""

    lower, upper = _validate_directional_window(current_position, delta)
    profile = accessibility_profile(
        ensemble,
        current_position=current_position,
        record_component=record_component,
        target_component=target_component,
    )
    return profile[lower] - profile[upper]
