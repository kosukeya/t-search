"""Stage 5D cross-clock composition utilities.

Stage 5C established pairwise genuine clock changes

    S_{Y<-X}(k,j) = R_Y(k) E_X(j) : K_X -> K_Y.

This module tests the first genuinely three-perspective consistency law:

    S_{Z<-Y}(l,k) S_{Y<-X}(k,j) = S_{Z<-X}(l,j)

for three distinct physical clock subsystems.  The maps remain support-space
objects even though their ambient matrix representatives all have shape d^2 x d^2.
"""

from __future__ import annotations

from itertools import permutations
from typing import Iterable

import numpy as np

from .stage5_clock_change import DEFAULT_ATOL, DEFAULT_DIMENSION, DEFAULT_RATES, SUBSYSTEMS
from .stage5_clock_transforms import (
    apply_genuine_clock_change,
    genuine_clock_change_operator,
    genuine_clock_change_support_matrix,
)
from .stage5_reductions import (
    clock_relative_support_basis,
    clock_relative_support_projector,
    rest_subsystems,
)


def _validate_three_distinct_clocks(
    source_clock: str,
    intermediate_clock: str,
    target_clock: str,
) -> tuple[str, str, str]:
    for clock in (source_clock, intermediate_clock, target_clock):
        # Public Stage 5B helper performs the A/B/C validation.
        rest_subsystems(clock)
    if len({source_clock, intermediate_clock, target_clock}) != 3:
        raise ValueError("cross-clock composition requires three distinct clock subsystems")
    return source_clock, intermediate_clock, target_clock


def ordered_distinct_clock_triples() -> tuple[tuple[str, str, str], ...]:
    """Return all six ordered (source, intermediate, target) clock triples."""

    return tuple(permutations(SUBSYSTEMS, 3))


def composed_cross_clock_operator(
    target_clock: str,
    target_index: int,
    intermediate_clock: str,
    intermediate_index: int,
    source_clock: str,
    source_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Return S_{Z<-Y}(l,k) S_{Y<-X}(k,j) in ambient rest coordinates."""

    source, intermediate, target = _validate_three_distinct_clocks(
        source_clock, intermediate_clock, target_clock
    )
    first = genuine_clock_change_operator(
        intermediate,
        intermediate_index,
        source,
        source_index,
        dimension,
        rates=rates,
    )
    second = genuine_clock_change_operator(
        target,
        target_index,
        intermediate,
        intermediate_index,
        dimension,
        rates=rates,
    )
    return second @ first


def direct_cross_clock_operator(
    target_clock: str,
    target_index: int,
    intermediate_clock: str,
    source_clock: str,
    source_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Return the direct S_{Z<-X}(l,j), validating a distinct intermediate clock."""

    source, _intermediate, target = _validate_three_distinct_clocks(
        source_clock, intermediate_clock, target_clock
    )
    return genuine_clock_change_operator(
        target,
        target_index,
        source,
        source_index,
        dimension,
        rates=rates,
    )


def cross_clock_composition_support_matrices(
    target_clock: str,
    target_index: int,
    intermediate_clock: str,
    intermediate_index: int,
    source_clock: str,
    source_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> tuple[np.ndarray, np.ndarray]:
    """Return (composed, direct) maps in orthonormal K_X/K_Z coordinates."""

    source, intermediate, target = _validate_three_distinct_clocks(
        source_clock, intermediate_clock, target_clock
    )
    first = genuine_clock_change_support_matrix(
        intermediate,
        intermediate_index,
        source,
        source_index,
        dimension,
        rates=rates,
    )
    second = genuine_clock_change_support_matrix(
        target,
        target_index,
        intermediate,
        intermediate_index,
        dimension,
        rates=rates,
    )
    direct = genuine_clock_change_support_matrix(
        target,
        target_index,
        source,
        source_index,
        dimension,
        rates=rates,
    )
    return second @ first, direct


def apply_cross_clock_route(
    source_state: np.ndarray,
    target_clock: str,
    target_index: int,
    intermediate_clock: str,
    intermediate_index: int,
    source_clock: str,
    source_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    atol: float = DEFAULT_ATOL,
) -> np.ndarray:
    """Apply X -> Y -> Z while checking both support transitions."""

    source, intermediate, target = _validate_three_distinct_clocks(
        source_clock, intermediate_clock, target_clock
    )
    middle_state = apply_genuine_clock_change(
        source_state,
        intermediate,
        intermediate_index,
        source,
        source_index,
        dimension,
        rates=rates,
        atol=atol,
    )
    return apply_genuine_clock_change(
        middle_state,
        target,
        target_index,
        intermediate,
        intermediate_index,
        dimension,
        rates=rates,
        atol=atol,
    )


def closed_three_clock_loop_operator(
    source_clock: str,
    source_index: int,
    second_clock: str,
    second_index: int,
    third_clock: str,
    third_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Return X -> Y -> Z -> X as an ambient source-rest-space operator."""

    source, second, third = _validate_three_distinct_clocks(
        source_clock, second_clock, third_clock
    )
    xy = genuine_clock_change_operator(
        second, second_index, source, source_index, dimension, rates=rates
    )
    yz = genuine_clock_change_operator(
        third, third_index, second, second_index, dimension, rates=rates
    )
    zx = genuine_clock_change_operator(
        source, source_index, third, third_index, dimension, rates=rates
    )
    return zx @ yz @ xy


def closed_three_clock_loop_support_matrix(
    source_clock: str,
    source_index: int,
    second_clock: str,
    second_index: int,
    third_clock: str,
    third_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Represent X -> Y -> Z -> X on orthonormal K_X coordinates."""

    source, second, third = _validate_three_distinct_clocks(
        source_clock, second_clock, third_clock
    )
    support = clock_relative_support_basis(source, dimension, rates=rates)
    loop = closed_three_clock_loop_operator(
        source,
        source_index,
        second,
        second_index,
        third,
        third_index,
        dimension,
        rates=rates,
    )
    return support.conj().T @ loop @ support


def source_support_projector(
    source_clock: str,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Convenience accessor used by Stage 5D closed-loop diagnostics."""

    return clock_relative_support_projector(source_clock, dimension, rates=rates)
