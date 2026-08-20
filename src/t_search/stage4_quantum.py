"""Finite quantum clock and constrained-state utilities for Stage 4.

Stage 4A defines finite clock/system kinematics. Stage 4B adds the noninteracting
Page--Wootters-style total constraint and the canonical matched-energy physical
subspace. Conditional clock reductions remain deferred to Stage 4C.
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


@dataclass(frozen=True)
class ConstrainedQuantumModel:
    """Stage 4B canonical constrained global quantum fixture."""

    dimension: int
    h_clock: np.ndarray
    h_system: np.ndarray
    h_total: np.ndarray
    physical_basis: np.ndarray

    @property
    def kinematic_dimension(self) -> int:
        return self.dimension * self.dimension

    @property
    def physical_dimension(self) -> int:
        return self.physical_basis.shape[1]


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


def _validate_state_vector(state: np.ndarray, dimension: int) -> np.ndarray:
    d = _validate_dimension(dimension)
    vector = np.asarray(state, dtype=np.complex128)
    expected = d * d
    if vector.shape != (expected,):
        raise ValueError(f"global state must have shape ({expected},)")
    if not np.all(np.isfinite(vector)):
        raise ValueError("global state amplitudes must be finite")
    return vector


def _validate_coefficients(coefficients: np.ndarray, dimension: int) -> np.ndarray:
    d = _validate_dimension(dimension)
    vector = np.asarray(coefficients, dtype=np.complex128)
    if vector.shape != (d,):
        raise ValueError(f"coefficients must have shape ({d},)")
    if not np.all(np.isfinite(vector)):
        raise ValueError("coefficients must be finite")
    if np.linalg.norm(vector) <= DEFAULT_ATOL:
        raise ValueError("coefficients must define a nonzero state")
    return vector


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


def tensor_basis_state(
    clock_index: int,
    system_index: int,
    dimension: int = DEFAULT_DIMENSION,
) -> np.ndarray:
    """Return |clock_index>_C tensor |system_index>_S."""

    d = _validate_dimension(dimension)
    if isinstance(clock_index, bool) or not isinstance(clock_index, Integral):
        raise ValueError("clock basis index must be an integer")
    if isinstance(system_index, bool) or not isinstance(system_index, Integral):
        raise ValueError("system basis index must be an integer")
    c = int(clock_index)
    s = int(system_index)
    if not 0 <= c < d or not 0 <= s < d:
        raise ValueError(f"basis indices must be between 0 and {d - 1}")
    return np.kron(standard_basis(d)[:, c], standard_basis(d)[:, s])


def total_constraint_operator(dimension: int = DEFAULT_DIMENSION) -> np.ndarray:
    """Return H_tot = H_C tensor I + I tensor H_S."""

    d = _validate_dimension(dimension)
    identity = np.eye(d, dtype=np.complex128)
    return np.kron(clock_hamiltonian(d), identity) + np.kron(
        identity, system_hamiltonian(d)
    )


def matched_energy_basis(dimension: int = DEFAULT_DIMENSION) -> np.ndarray:
    """Return analytic columns |n>_C|n>_S spanning the zero-constraint subspace."""

    d = _validate_dimension(dimension)
    return np.column_stack(tuple(tensor_basis_state(n, n, d) for n in range(d)))


def constraint_kernel_basis(
    dimension: int = DEFAULT_DIMENSION,
    *,
    atol: float = DEFAULT_ATOL,
) -> np.ndarray:
    """Numerically extract an orthonormal basis for ker(H_tot)."""

    h_total = total_constraint_operator(dimension)
    eigenvalues, eigenvectors = np.linalg.eigh(h_total)
    mask = np.abs(eigenvalues) <= atol
    return eigenvectors[:, mask]


def physical_subspace_projector(dimension: int = DEFAULT_DIMENSION) -> np.ndarray:
    """Return the analytic matched-energy physical-subspace projector."""

    basis = matched_energy_basis(dimension)
    return basis @ basis.conj().T


def constraint_kernel_projector(
    dimension: int = DEFAULT_DIMENSION,
    *,
    atol: float = DEFAULT_ATOL,
) -> np.ndarray:
    """Return the numerical zero-eigenspace projector of H_tot."""

    basis = constraint_kernel_basis(dimension, atol=atol)
    return basis @ basis.conj().T


def physical_subspace_dimension(dimension: int = DEFAULT_DIMENSION) -> int:
    """Return dim ker(H_tot) for the canonical matched spectra."""

    return constraint_kernel_basis(dimension).shape[1]


def physical_state_from_coefficients(
    coefficients: np.ndarray,
    dimension: int = DEFAULT_DIMENSION,
    *,
    normalize: bool = False,
) -> np.ndarray:
    """Build sum_n c_n |n>_C|n>_S from a coefficient vector.

    Coefficients are preserved by default. Set ``normalize=True`` to normalize a
    nonzero vector before embedding it in the physical subspace.
    """

    d = _validate_dimension(dimension)
    coeffs = _validate_coefficients(coefficients, d).copy()
    if normalize:
        coeffs /= np.linalg.norm(coeffs)
    return matched_energy_basis(d) @ coeffs


def equal_amplitude_physical_state(
    dimension: int = DEFAULT_DIMENSION,
) -> np.ndarray:
    """Return the normalized equal-amplitude Stage 4B baseline physical state."""

    d = _validate_dimension(dimension)
    return physical_state_from_coefficients(
        np.ones(d, dtype=np.complex128) / np.sqrt(d), d
    )


def constraint_residual(
    state: np.ndarray,
    dimension: int = DEFAULT_DIMENSION,
) -> float:
    """Return ||H_tot |state>||_2."""

    d = _validate_dimension(dimension)
    vector = _validate_state_vector(state, d)
    return float(np.linalg.norm(total_constraint_operator(d) @ vector))


def is_physical_state(
    state: np.ndarray,
    dimension: int = DEFAULT_DIMENSION,
    *,
    atol: float = DEFAULT_ATOL,
) -> bool:
    """Check the Stage 4B zero-constraint condition."""

    return constraint_residual(state, dimension) <= atol


def evolve_under_constraint(
    state: np.ndarray,
    parameter: float,
    dimension: int = DEFAULT_DIMENSION,
) -> np.ndarray:
    """Apply exp(-i H_tot parameter) to a global kinematic state."""

    d = _validate_dimension(dimension)
    vector = _validate_state_vector(state, d)
    return unitary_from_hermitian(total_constraint_operator(d), parameter) @ vector


def stationarity_residual(
    state: np.ndarray,
    parameter: float,
    dimension: int = DEFAULT_DIMENSION,
) -> float:
    """Return ||exp(-i H_tot tau)|state> - |state>||_2."""

    d = _validate_dimension(dimension)
    vector = _validate_state_vector(state, d)
    evolved = evolve_under_constraint(vector, parameter, d)
    return float(np.linalg.norm(evolved - vector))


def canonical_stage4b_model(
    dimension: int = DEFAULT_DIMENSION,
) -> ConstrainedQuantumModel:
    """Construct the Stage 4B constrained global quantum fixture."""

    d = _validate_dimension(dimension)
    return ConstrainedQuantumModel(
        dimension=d,
        h_clock=clock_hamiltonian(d),
        h_system=system_hamiltonian(d),
        h_total=total_constraint_operator(d),
        physical_basis=matched_energy_basis(d),
    )
