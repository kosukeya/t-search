"""Operational and negative controls for Stage 4F.

This module tests where the ideal finite Page--Wootters-style construction does
and does not support the interpretations used in earlier Stage 4 checkpoints.
It separates:

* global conditional Born probabilities from local Born probabilities;
* formal clock conditioning from physical constrained dynamics;
* vector change from ray/density-matrix change; and
* the ideal DFT time basis from clock-energy-basis conditioning.
"""

from __future__ import annotations

from numbers import Integral

import numpy as np

from .stage4_conditional import (
    condition_on_clock,
    normalized_physical_conditional_state,
    system_evolution_unitary,
)
from .stage4_quantum import (
    DEFAULT_ATOL,
    DEFAULT_DIMENSION,
    clock_reading_times,
    clock_state,
    is_physical_state,
    standard_basis,
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


def _validate_global_state(state: np.ndarray, dimension: int) -> np.ndarray:
    d = _validate_dimension(dimension)
    vector = np.asarray(state, dtype=np.complex128)
    if vector.shape != (d * d,):
        raise ValueError(f"global state must have shape ({d * d},)")
    if not np.all(np.isfinite(vector)):
        raise ValueError("global state amplitudes must be finite")
    return vector


def _validate_system_state(state: np.ndarray, dimension: int) -> np.ndarray:
    d = _validate_dimension(dimension)
    vector = np.asarray(state, dtype=np.complex128)
    if vector.shape != (d,):
        raise ValueError(f"system state must have shape ({d},)")
    if not np.all(np.isfinite(vector)):
        raise ValueError("system state amplitudes must be finite")
    return vector


def _validate_projector(projector: np.ndarray, dimension: int) -> np.ndarray:
    d = _validate_dimension(dimension)
    matrix = np.asarray(projector, dtype=np.complex128)
    if matrix.shape != (d, d):
        raise ValueError(f"projector must have shape ({d}, {d})")
    if not np.all(np.isfinite(matrix)):
        raise ValueError("projector entries must be finite")
    if not np.allclose(matrix, matrix.conj().T, atol=DEFAULT_ATOL, rtol=0.0):
        raise ValueError("projector must be Hermitian")
    if not np.allclose(matrix @ matrix, matrix, atol=DEFAULT_ATOL, rtol=0.0):
        raise ValueError("projector must be idempotent")
    return matrix


def plus01_projector(dimension: int = DEFAULT_DIMENSION) -> np.ndarray:
    """Return |+><+| for |+>=(|0>+|1>)/sqrt(2)."""

    d = _validate_dimension(dimension)
    ket = (standard_basis(d)[:, 0] + standard_basis(d)[:, 1]) / np.sqrt(2.0)
    return np.outer(ket, ket.conj())


def global_conditional_born_probability(
    state: np.ndarray,
    clock_index: int,
    system_projector: np.ndarray,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
    atol: float = DEFAULT_ATOL,
) -> float:
    """Return P(a|t_j) from the global constrained state."""

    d = _validate_dimension(dimension)
    j = _validate_clock_index(clock_index, d)
    vector = _validate_global_state(state, d)
    if not is_physical_state(vector, d, atol=atol):
        raise ValueError("state must satisfy the Stage 4 zero-constraint condition")
    projector = _validate_projector(system_projector, d)
    t = clock_state(j, d, origin=origin)
    clock_projector = np.outer(t, t.conj())
    numerator_operator = np.kron(clock_projector, projector)
    denominator_operator = np.kron(
        clock_projector, np.eye(d, dtype=np.complex128)
    )
    numerator = float(np.vdot(vector, numerator_operator @ vector).real)
    denominator = float(np.vdot(vector, denominator_operator @ vector).real)
    if denominator <= atol:
        raise ValueError("clock outcome has zero conditional-probability denominator")
    return numerator / denominator


def local_born_probability(
    state: np.ndarray,
    clock_index: int,
    system_projector: np.ndarray,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
    atol: float = DEFAULT_ATOL,
) -> float:
    """Return <psi_j|Pi|psi_j> from the normalized physical reduction."""

    d = _validate_dimension(dimension)
    projector = _validate_projector(system_projector, d)
    psi = normalized_physical_conditional_state(
        state, clock_index, d, origin=origin, atol=atol
    )
    return float(np.vdot(psi, projector @ psi).real)


def born_consistency_residual(
    state: np.ndarray,
    clock_index: int,
    system_projector: np.ndarray,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
    atol: float = DEFAULT_ATOL,
) -> float:
    """Return |P_global(a|t_j)-P_local(a|t_j)|."""

    global_probability = global_conditional_born_probability(
        state,
        clock_index,
        system_projector,
        dimension,
        origin=origin,
        atol=atol,
    )
    local_probability = local_born_probability(
        state,
        clock_index,
        system_projector,
        dimension,
        origin=origin,
        atol=atol,
    )
    return abs(global_probability - local_probability)


def normalized_formal_conditional_state(
    state: np.ndarray,
    clock_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
    atol: float = DEFAULT_ATOL,
) -> np.ndarray:
    """Normalize a formal clock conditional without imposing the constraint."""

    d = _validate_dimension(dimension)
    vector = _validate_global_state(state, d)
    conditional = condition_on_clock(vector, clock_index, d, origin=origin)
    norm = float(np.linalg.norm(conditional))
    if norm <= atol:
        raise ValueError("formal conditional state has zero norm")
    return conditional / norm


def formal_conditional_schrodinger_residual(
    state: np.ndarray,
    target_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    reference_index: int = 0,
    origin: float = 0.0,
    atol: float = DEFAULT_ATOL,
) -> float:
    """Test the Schrödinger relation for a formally conditioned kinematic state."""

    d = _validate_dimension(dimension)
    reference = _validate_clock_index(reference_index, d)
    target = _validate_clock_index(target_index, d)
    psi_reference = normalized_formal_conditional_state(
        state, reference, d, origin=origin, atol=atol
    )
    psi_target = normalized_formal_conditional_state(
        state, target, d, origin=origin, atol=atol
    )
    times = clock_reading_times(d, origin=origin)
    expected = system_evolution_unitary(times[target] - times[reference], d) @ psi_reference
    return float(np.linalg.norm(psi_target - expected))


def density_matrix(state: np.ndarray, dimension: int = DEFAULT_DIMENSION) -> np.ndarray:
    """Return |psi><psi| for a normalized or unnormalized nonzero system vector."""

    d = _validate_dimension(dimension)
    vector = _validate_system_state(state, d)
    norm = float(np.linalg.norm(vector))
    if norm <= DEFAULT_ATOL:
        raise ValueError("system state must be nonzero")
    normalized = vector / norm
    return np.outer(normalized, normalized.conj())


def ray_fidelity(
    state_a: np.ndarray,
    state_b: np.ndarray,
    dimension: int = DEFAULT_DIMENSION,
) -> float:
    """Return normalized pure-state fidelity |<a|b>|^2."""

    d = _validate_dimension(dimension)
    a = _validate_system_state(state_a, d)
    b = _validate_system_state(state_b, d)
    norm_a = float(np.linalg.norm(a))
    norm_b = float(np.linalg.norm(b))
    if norm_a <= DEFAULT_ATOL or norm_b <= DEFAULT_ATOL:
        raise ValueError("system states must be nonzero")
    overlap = np.vdot(a / norm_a, b / norm_b)
    return float(abs(overlap) ** 2)


def density_matrix_residual(
    state_a: np.ndarray,
    state_b: np.ndarray,
    dimension: int = DEFAULT_DIMENSION,
) -> float:
    """Return Frobenius distance between the two pure-state density matrices."""

    return float(
        np.linalg.norm(
            density_matrix(state_a, dimension) - density_matrix(state_b, dimension)
        )
    )


def energy_basis_physical_projection_matrix(
    energy_index: int,
    dimension: int = DEFAULT_DIMENSION,
) -> np.ndarray:
    """Return the clock-energy-basis projection on physical coefficient space.

    The domain coordinates are coefficients c_n of sum_n c_n |n>_C|n>_S.
    Conditioning on <m|_C returns c_m |m>_S, represented by |m><m|.
    """

    d = _validate_dimension(dimension)
    m = _validate_clock_index(energy_index, d)
    basis = standard_basis(d)
    ket = basis[:, m]
    return np.outer(ket, ket.conj())


def energy_basis_projection_rank(
    energy_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    atol: float = DEFAULT_ATOL,
) -> int:
    """Return rank of the clock-energy-basis physical projection."""

    matrix = energy_basis_physical_projection_matrix(energy_index, dimension)
    return int(np.linalg.matrix_rank(matrix, tol=atol))


def energy_basis_projection_nullity(
    energy_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    atol: float = DEFAULT_ATOL,
) -> int:
    """Return nullity of the clock-energy-basis physical projection."""

    d = _validate_dimension(dimension)
    return d - energy_basis_projection_rank(energy_index, d, atol=atol)
