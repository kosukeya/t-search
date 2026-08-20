"""Finite clock kinematics for Stage 4A.

Stage 4A intentionally stops before Page--Wootters constraints or conditional
system dynamics.  This module only defines the finite clock/system Hilbert-space
kinematics, energy Hamiltonians, DFT clock-reading basis, and cyclic clock
translation used by later Stage 4 checkpoints.
"""

from __future__ import annotations

from dataclasses import dataclass
from numbers import Integral, Real

import numpy as np

DEFAULT_DIMENSION = 4
DEFAULT_ATOL = 1e-10


@dataclass(frozen=True)
class FiniteClockKinematics:
    """Declared Stage 4A finite clock/system kinematics."""

    dimension: int
    h_clock: np.ndarray
    h_system: np.ndarray
    clock_times: np.ndarray
    clock_basis: np.ndarray

    @property
    def clock_dimension(self) -> int:
        return self.dimension

    @property
    def system_dimension(self) -> int:
        return self.dimension

    @property
    def kinematic_dimension(self) -> int:
        return self.dimension * self.dimension

    @property
    def step(self) -> float:
        return clock_step(self.dimension)


def _validate_dimension(dimension: int) -> int:
    if isinstance(dimension, bool) or not isinstance(dimension, Integral):
        raise ValueError("dimension must be an integer")
    d = int(dimension)
    if d < 2:
        raise ValueError("dimension must be at least two")
    return d


def _validate_origin(origin: float) -> float:
    if isinstance(origin, bool) or not isinstance(origin, Real):
        raise ValueError("origin must be a finite real number")
    value = float(origin)
    if not np.isfinite(value):
        raise ValueError("origin must be a finite real number")
    return value


def standard_basis(dimension: int) -> np.ndarray:
    """Return the canonical orthonormal energy basis as matrix columns."""

    d = _validate_dimension(dimension)
    return np.eye(d, dtype=np.complex128)


def system_hamiltonian(dimension: int = DEFAULT_DIMENSION) -> np.ndarray:
    """Return H_S with spectrum 0,1,...,d-1 in the energy basis."""

    d = _validate_dimension(dimension)
    return np.diag(np.arange(d, dtype=float)).astype(np.complex128)


def clock_hamiltonian(dimension: int = DEFAULT_DIMENSION) -> np.ndarray:
    """Return H_C with spectrum 0,-1,...,-(d-1) in the energy basis."""

    return -system_hamiltonian(dimension)


def kinematic_dimension(
    clock_dimension: int = DEFAULT_DIMENSION,
    system_dimension: int = DEFAULT_DIMENSION,
) -> int:
    """Return dim(H_C tensor H_S) without constructing the tensor space."""

    d_clock = _validate_dimension(clock_dimension)
    d_system = _validate_dimension(system_dimension)
    return d_clock * d_system


def clock_step(dimension: int = DEFAULT_DIMENSION) -> float:
    """Return the discrete clock spacing Delta = 2*pi/d."""

    d = _validate_dimension(dimension)
    return 2.0 * np.pi / d


def clock_reading_times(
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
) -> np.ndarray:
    """Return t_j = origin + 2*pi*j/d for j=0,...,d-1."""

    d = _validate_dimension(dimension)
    alpha = _validate_origin(origin)
    return alpha + clock_step(d) * np.arange(d, dtype=float)


def clock_state_at_time(time: float, dimension: int = DEFAULT_DIMENSION) -> np.ndarray:
    """Return the ideal DFT clock vector at an arbitrary real reading time."""

    if isinstance(time, bool) or not isinstance(time, Real):
        raise ValueError("time must be a finite real number")
    value = float(time)
    if not np.isfinite(value):
        raise ValueError("time must be a finite real number")
    d = _validate_dimension(dimension)
    n = np.arange(d, dtype=float)
    return np.exp(1j * n * value) / np.sqrt(d)


def clock_state(
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
) -> np.ndarray:
    """Return |t_j> for one canonical clock-reading label j."""

    d = _validate_dimension(dimension)
    if isinstance(index, bool) or not isinstance(index, Integral):
        raise ValueError("clock index must be an integer")
    j = int(index)
    if not 0 <= j < d:
        raise ValueError(f"clock index must be between 0 and {d - 1}")
    alpha = _validate_origin(origin)
    return clock_state_at_time(alpha + j * clock_step(d), d)


def clock_basis_matrix(
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
) -> np.ndarray:
    """Return the DFT clock-reading basis as matrix columns."""

    d = _validate_dimension(dimension)
    alpha = _validate_origin(origin)
    return np.column_stack(tuple(clock_state(j, d, origin=alpha) for j in range(d)))


def clock_gram_matrix(
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
) -> np.ndarray:
    """Return the clock-basis Gram matrix."""

    basis = clock_basis_matrix(dimension, origin=origin)
    return basis.conj().T @ basis


def is_clock_basis_orthonormal(
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
    atol: float = DEFAULT_ATOL,
) -> bool:
    """Check DFT-clock orthonormality within the declared tolerance."""

    d = _validate_dimension(dimension)
    return bool(
        np.allclose(
            clock_gram_matrix(d, origin=origin),
            np.eye(d, dtype=np.complex128),
            atol=atol,
            rtol=0.0,
        )
    )


def unitary_from_hermitian(hamiltonian: np.ndarray, parameter: float) -> np.ndarray:
    """Return exp(-i H parameter) for a finite Hermitian matrix."""

    matrix = np.asarray(hamiltonian, dtype=np.complex128)
    if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
        raise ValueError("hamiltonian must be a square matrix")
    if not np.allclose(matrix, matrix.conj().T, atol=DEFAULT_ATOL, rtol=0.0):
        raise ValueError("hamiltonian must be Hermitian")
    if isinstance(parameter, bool) or not isinstance(parameter, Real):
        raise ValueError("parameter must be a finite real number")
    tau = float(parameter)
    if not np.isfinite(tau):
        raise ValueError("parameter must be a finite real number")

    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    phases = np.exp(-1j * eigenvalues * tau)
    return (eigenvectors * phases) @ eigenvectors.conj().T


def clock_translation_unitary(
    dimension: int = DEFAULT_DIMENSION,
    *,
    steps: int = 1,
) -> np.ndarray:
    """Return exp(-i H_C steps*Delta)."""

    d = _validate_dimension(dimension)
    if isinstance(steps, bool) or not isinstance(steps, Integral):
        raise ValueError("steps must be an integer")
    return unitary_from_hermitian(clock_hamiltonian(d), int(steps) * clock_step(d))


def translate_clock_state(
    state: np.ndarray,
    dimension: int = DEFAULT_DIMENSION,
    *,
    steps: int = 1,
) -> np.ndarray:
    """Apply the declared clock translation to one clock-state vector."""

    d = _validate_dimension(dimension)
    vector = np.asarray(state, dtype=np.complex128)
    if vector.shape != (d,):
        raise ValueError(f"clock state must have shape ({d},)")
    return clock_translation_unitary(d, steps=steps) @ vector


def cyclic_clock_index(index: int, dimension: int = DEFAULT_DIMENSION) -> int:
    """Return an integer clock label reduced modulo d."""

    d = _validate_dimension(dimension)
    if isinstance(index, bool) or not isinstance(index, Integral):
        raise ValueError("clock index must be an integer")
    return int(index) % d


def canonical_stage4a_kinematics(
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
) -> FiniteClockKinematics:
    """Construct the Stage 4A clock/system kinematic fixture."""

    d = _validate_dimension(dimension)
    alpha = _validate_origin(origin)
    return FiniteClockKinematics(
        dimension=d,
        h_clock=clock_hamiltonian(d),
        h_system=system_hamiltonian(d),
        clock_times=clock_reading_times(d, origin=alpha),
        clock_basis=clock_basis_matrix(d, origin=alpha),
    )
