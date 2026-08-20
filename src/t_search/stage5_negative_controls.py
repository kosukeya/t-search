"""Stage 5F negative controls for clock-change covariance.

These utilities deliberately probe cases outside the physical/support assumptions
used in Stages 5B--5E.  They are diagnostics for the boundaries of the finite
construction, not alternative physical clock-change prescriptions.
"""

from __future__ import annotations

from itertools import product
from numbers import Integral
from typing import Iterable

import numpy as np

from .stage5_clock_change import (
    DEFAULT_ATOL,
    DEFAULT_DIMENSION,
    DEFAULT_RATES,
    SUBSYSTEMS,
    analytic_physical_basis,
    centered_energy_labels,
    label_to_index,
)
from .stage5_clock_transforms import genuine_clock_change_operator
from .stage5_reductions import (
    clock_relative_support_projector,
    rest_basis_state,
    rest_pair_for_triple,
    rest_subsystems,
)

_SUBSYSTEM_INDEX = {"A": 0, "B": 1, "C": 2}


def _validate_clock(clock: str) -> str:
    # Reuse the public rest-factor API for the declared A/B/C validation.
    rest_subsystems(clock)
    return clock


def _validate_energy_label(label: int, dimension: int) -> int:
    if isinstance(label, bool) or not isinstance(label, Integral):
        raise ValueError("energy label must be an integer in the declared basis")
    value = int(label)
    label_to_index(value, dimension)
    return value


def energy_basis_conditioning_operator(
    clock: str,
    energy_label: int,
    dimension: int = DEFAULT_DIMENSION,
) -> np.ndarray:
    """Return (<m|_X tensor I_rest) for an energy-basis clock conditioning.

    This intentionally uses the clock energy basis rather than the ideal DFT
    reading basis.  It is a Stage 5F negative-control map, not a physical clock
    reduction used by the Stage 5 construction.
    """

    x = _validate_clock(clock)
    labels = centered_energy_labels(dimension)
    d = len(labels)
    label = _validate_energy_label(energy_label, d)
    clock_position = _SUBSYSTEM_INDEX[x]
    raw_clock_index = label_to_index(label, d)

    projection = np.zeros((d**2, d**3), dtype=np.complex128)
    for raw_indices in product(range(d), repeat=3):
        if raw_indices[clock_position] != raw_clock_index:
            continue
        global_index = (raw_indices[0] * d + raw_indices[1]) * d + raw_indices[2]
        rest_indices = tuple(
            value for position, value in enumerate(raw_indices) if position != clock_position
        )
        rest_index = rest_indices[0] * d + rest_indices[1]
        projection[rest_index, global_index] = 1.0
    return projection


def energy_basis_conditioning_physical_matrix(
    clock: str,
    energy_label: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Restrict energy-basis conditioning to physical coefficient coordinates."""

    projection = energy_basis_conditioning_operator(clock, energy_label, dimension)
    physical_basis = analytic_physical_basis(dimension, rates=rates)
    return projection @ physical_basis


def energy_basis_conditioning_rank(
    clock: str,
    energy_label: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    atol: float = DEFAULT_ATOL,
) -> int:
    """Return the rank of wrong-basis conditioning on H_phys coefficients."""

    matrix = energy_basis_conditioning_physical_matrix(
        clock, energy_label, dimension, rates=rates
    )
    singular_values = np.linalg.svd(matrix, compute_uv=False)
    return int(np.sum(singular_values > atol))


def ambient_clock_change_rank(
    target_clock: str,
    target_index: int,
    source_clock: str,
    source_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    atol: float = DEFAULT_ATOL,
) -> int:
    """Return the rank of the embedded d^2 x d^2 genuine clock-change matrix."""

    operator = genuine_clock_change_operator(
        target_clock,
        target_index,
        source_clock,
        source_index,
        dimension,
        rates=rates,
    )
    singular_values = np.linalg.svd(operator, compute_uv=False)
    return int(np.sum(singular_values > atol))


def ambient_clock_change_unitarity_residuals(
    target_clock: str,
    target_index: int,
    source_clock: str,
    source_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> tuple[float, float]:
    """Return unrestricted-rest residuals against I, expected to be nonzero."""

    operator = genuine_clock_change_operator(
        target_clock,
        target_index,
        source_clock,
        source_index,
        dimension,
        rates=rates,
    )
    identity = np.eye(operator.shape[0], dtype=np.complex128)
    left = float(np.linalg.norm(operator.conj().T @ operator - identity))
    right = float(np.linalg.norm(operator @ operator.conj().T - identity))
    return left, right


def first_off_support_pair(
    clock: str,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> tuple[int, int]:
    """Return a deterministic product-energy pair outside K_X."""

    x = _validate_clock(clock)
    labels = tuple(int(value) for value in centered_energy_labels(dimension))
    projector = clock_relative_support_projector(x, dimension, rates=rates)
    for pair in product(labels, repeat=2):
        basis = rest_basis_state(pair, dimension)
        if np.linalg.norm(projector @ basis) <= DEFAULT_ATOL:
            return pair
    raise RuntimeError("declared rest tensor product has no off-support basis state")


def same_numeric_reading_semantic_witness(
    source_clock: str,
    target_clock: str,
    physical_triple: tuple[int, int, int],
) -> tuple[tuple[str, str], tuple[int, int], tuple[str, str], tuple[int, int]]:
    """Return source/target factor labels for one equal-reading clock change.

    This records the semantic change in the reduced tensor factors.  It does not
    assert that equal numeric clock coordinates correspond to one physical event.
    """

    source = _validate_clock(source_clock)
    target = _validate_clock(target_clock)
    if source == target:
        raise ValueError("semantic witness requires distinct source and target clocks")
    if len(physical_triple) != 3:
        raise ValueError("physical triple must contain exactly three energy labels")
    source_rest = rest_subsystems(source)
    target_rest = rest_subsystems(target)
    source_pair = rest_pair_for_triple(physical_triple, source)
    target_pair = rest_pair_for_triple(physical_triple, target)
    return source_rest, source_pair, target_rest, target_pair
