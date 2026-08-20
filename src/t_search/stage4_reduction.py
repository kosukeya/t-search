"""Reduction-map reversibility utilities for Stage 4D.

Stage 4D compares two different maps that share the same clock bra:

* the kinematic projection P_j^kin=(<t_j| tensor I), defined on the full
  d^2-dimensional kinematic Hilbert space and therefore many-to-one; and
* the normalized physical reduction R_j=sqrt(d) P_j^kin restricted to the
  d-dimensional zero-constraint physical subspace.

For the ideal matched-energy model, R_j is represented by a unitary d x d
matrix in the orthonormal physical basis {|n>_C|n>_S}.  The explicit lift E_j
reconstructs a physical global state from one clock-relative system vector.
"""

from __future__ import annotations

from numbers import Integral

import numpy as np

from .stage4_conditional import physical_reduction
from .stage4_quantum import (
    DEFAULT_ATOL,
    DEFAULT_DIMENSION,
    clock_reading_times,
    clock_state,
    is_physical_state,
    matched_energy_basis,
)


def _validate_dimension(dimension: int) -> int:
    if isinstance(dimension, bool) or not isinstance(dimension, Integral):
        raise ValueError("dimension must be an integer")
    d = int(dimension)
    if d < 2:
        raise ValueError("dimension must be at least two")
    return d


def _validate_clock_index(index: int, dimension: int) -> int:
    d = _validate_dimension(dimension)
    if isinstance(index, bool) or not isinstance(index, Integral):
        raise ValueError("clock index must be an integer")
    j = int(index)
    if not 0 <= j < d:
        raise ValueError(f"clock index must be between 0 and {d - 1}")
    return j


def _validate_system_state(state: np.ndarray, dimension: int) -> np.ndarray:
    d = _validate_dimension(dimension)
    vector = np.asarray(state, dtype=np.complex128)
    if vector.shape != (d,):
        raise ValueError(f"system state must have shape ({d},)")
    if not np.all(np.isfinite(vector)):
        raise ValueError("system state amplitudes must be finite")
    return vector


def _validate_global_state(state: np.ndarray, dimension: int) -> np.ndarray:
    d = _validate_dimension(dimension)
    vector = np.asarray(state, dtype=np.complex128)
    if vector.shape != (d * d,):
        raise ValueError(f"global state must have shape ({d * d},)")
    if not np.all(np.isfinite(vector)):
        raise ValueError("global state amplitudes must be finite")
    return vector


def kinematic_projection_matrix(
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
) -> np.ndarray:
    """Return P_j^kin=(<t_j| tensor I_S) as a d x d^2 matrix."""

    d = _validate_dimension(dimension)
    j = _validate_clock_index(index, d)
    clock_bra = clock_state(j, d, origin=origin).conj().reshape(1, d)
    return np.kron(clock_bra, np.eye(d, dtype=np.complex128))


def kinematic_projection_rank(
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
    atol: float = DEFAULT_ATOL,
) -> int:
    """Return rank(P_j^kin) using the declared numerical tolerance."""

    matrix = kinematic_projection_matrix(index, dimension, origin=origin)
    return int(np.linalg.matrix_rank(matrix, tol=atol))


def kinematic_projection_nullity(
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
    atol: float = DEFAULT_ATOL,
) -> int:
    """Return dim ker(P_j^kin) by rank-nullity."""

    d = _validate_dimension(dimension)
    return d * d - kinematic_projection_rank(
        index, d, origin=origin, atol=atol
    )


def physical_reduction_matrix(
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
) -> np.ndarray:
    """Return R_j in physical-basis coefficient coordinates.

    The domain coordinates are coefficients in the orthonormal matched-energy
    basis.  The codomain coordinates are the standard system-energy basis.
    """

    d = _validate_dimension(dimension)
    j = _validate_clock_index(index, d)
    return (
        np.sqrt(d)
        * kinematic_projection_matrix(j, d, origin=origin)
        @ matched_energy_basis(d)
    )


def reconstruction_matrix(
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
) -> np.ndarray:
    """Return E_j: H_S -> H_phys embedded in H_kin."""

    d = _validate_dimension(dimension)
    j = _validate_clock_index(index, d)
    time = clock_reading_times(d, origin=origin)[j]
    phases = np.exp(1j * np.arange(d, dtype=float) * time)
    return matched_energy_basis(d) @ np.diag(phases.astype(np.complex128))


def reconstruct_physical_state(
    system_state: np.ndarray,
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
) -> np.ndarray:
    """Apply E_j to one system vector, yielding a constrained global state."""

    d = _validate_dimension(dimension)
    vector = _validate_system_state(system_state, d)
    return reconstruction_matrix(index, d, origin=origin) @ vector


def system_roundtrip_residual(
    system_state: np.ndarray,
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
    atol: float = DEFAULT_ATOL,
) -> float:
    """Return ||R_j E_j |phi> - |phi>||."""

    d = _validate_dimension(dimension)
    vector = _validate_system_state(system_state, d)
    reconstructed = reconstruct_physical_state(vector, index, d, origin=origin)
    reduced = physical_reduction(
        reconstructed, index, d, origin=origin, atol=atol
    )
    return float(np.linalg.norm(reduced - vector))


def physical_roundtrip_residual(
    global_state: np.ndarray,
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
    atol: float = DEFAULT_ATOL,
) -> float:
    """Return ||E_j R_j |Psi_phys> - |Psi_phys>|| for a physical state."""

    d = _validate_dimension(dimension)
    vector = _validate_global_state(global_state, d)
    if not is_physical_state(vector, d, atol=atol):
        raise ValueError("state must satisfy the Stage 4 zero-constraint condition")
    reduced = physical_reduction(vector, index, d, origin=origin, atol=atol)
    reconstructed = reconstruct_physical_state(reduced, index, d, origin=origin)
    return float(np.linalg.norm(reconstructed - vector))


def lift_after_kinematic_projection_operator(
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
) -> np.ndarray:
    """Return E_j sqrt(d) P_j^kin on the full kinematic space.

    This operator is identity only after restriction to H_phys.  On H_kin it has
    rank d and must not be interpreted as a global inverse of P_j^kin.
    """

    d = _validate_dimension(dimension)
    j = _validate_clock_index(index, d)
    return (
        reconstruction_matrix(j, d, origin=origin)
        @ (np.sqrt(d) * kinematic_projection_matrix(j, d, origin=origin))
    )
