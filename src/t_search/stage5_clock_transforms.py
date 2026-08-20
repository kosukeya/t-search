"""Stage 5C genuine physical clock-change maps.

The maps in this module connect *distinct* clock-relative support spaces through
the common constrained physical Hilbert space:

    S_{Y<-X}(k,j) = R_Y(k) E_X(j) : K_X -> K_Y.

Although every ambient rest tensor product has dimension d^2, their tensor-factor
meanings differ with the clock choice.  The implementation therefore never
identifies two rest spaces directly; the common physical space is the bridge.
Three-clock composition is intentionally deferred to Stage 5D.
"""

from __future__ import annotations

from typing import Iterable

import numpy as np

from .stage5_clock_change import DEFAULT_ATOL, DEFAULT_DIMENSION, DEFAULT_RATES
from .stage5_reductions import (
    clock_reconstruction_operator,
    clock_relative_support_basis,
    clock_relative_support_projector,
    physical_clock_reduction_operator,
    rest_subsystems,
)


def _validate_distinct_clocks(source_clock: str, target_clock: str) -> tuple[str, str]:
    # rest_subsystems performs the declared A/B/C validation.
    rest_subsystems(source_clock)
    rest_subsystems(target_clock)
    if source_clock == target_clock:
        raise ValueError("genuine clock change requires distinct source and target clocks")
    return source_clock, target_clock


def genuine_clock_change_operator(
    target_clock: str,
    target_index: int,
    source_clock: str,
    source_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Return S_{Y<-X}(k,j)=R_Y(k)E_X(j) on ambient rest coordinates.

    The matrix has shape (d^2,d^2), but it is a partial isometry whose physical
    domain is K_X and physical codomain is K_Y.  It is not asserted to be a
    unitary on the unrestricted ambient rest tensor-product spaces.
    """

    source, target = _validate_distinct_clocks(source_clock, target_clock)
    reduction_target = physical_clock_reduction_operator(
        target, target_index, dimension, rates=rates
    )
    reconstruction_source = clock_reconstruction_operator(
        source, source_index, dimension, rates=rates
    )
    return reduction_target @ reconstruction_source


def genuine_clock_change_support_matrix(
    target_clock: str,
    target_index: int,
    source_clock: str,
    source_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Represent S_{Y<-X}(k,j) in orthonormal K_X/K_Y coordinates."""

    source, target = _validate_distinct_clocks(source_clock, target_clock)
    source_basis = clock_relative_support_basis(source, dimension, rates=rates)
    target_basis = clock_relative_support_basis(target, dimension, rates=rates)
    operator = genuine_clock_change_operator(
        target,
        target_index,
        source,
        source_index,
        dimension,
        rates=rates,
    )
    return target_basis.conj().T @ operator @ source_basis


def apply_genuine_clock_change(
    source_state: np.ndarray,
    target_clock: str,
    target_index: int,
    source_clock: str,
    source_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    atol: float = DEFAULT_ATOL,
) -> np.ndarray:
    """Transform one state known to lie in K_X into the target support K_Y."""

    source, target = _validate_distinct_clocks(source_clock, target_clock)
    source_basis = clock_relative_support_basis(source, dimension, rates=rates)
    expected = source_basis.shape[0]
    vector = np.asarray(source_state, dtype=np.complex128)
    if vector.shape != (expected,):
        raise ValueError(f"source rest state must have shape ({expected},)")
    if not np.all(np.isfinite(vector)):
        raise ValueError("source rest state amplitudes must be finite")

    source_projector = clock_relative_support_projector(source, dimension, rates=rates)
    if np.linalg.norm((np.eye(expected) - source_projector) @ vector) > atol:
        raise ValueError("source rest state must lie in the declared source-clock support")

    operator = genuine_clock_change_operator(
        target,
        target_index,
        source,
        source_index,
        dimension,
        rates=rates,
    )
    transformed = operator @ vector

    # This is an internal construction invariant, not an additional physical
    # assumption: R_Y E_X must land in the declared target support.
    target_projector = clock_relative_support_projector(target, dimension, rates=rates)
    if np.linalg.norm((np.eye(expected) - target_projector) @ transformed) > atol:
        raise RuntimeError("clock-change construction failed to land in target support")
    return transformed
