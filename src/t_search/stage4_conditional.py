"""Clock conditioning and finite Page--Wootters reductions for Stage 4C.

This module starts from the Stage 4A/B clock kinematics and constrained physical
subspace.  Formal clock conditioning is kept separate from the normalized
physical reduction: an arbitrary kinematic vector can be conditioned on a clock
reading, but only a zero-constraint vector is accepted as a Page--Wootters
physical reduction in this checkpoint.
"""

from __future__ import annotations

from numbers import Integral

import numpy as np

from .stage4_quantum import (
    DEFAULT_ATOL,
    DEFAULT_DIMENSION,
    clock_reading_times,
    clock_state,
    clock_step,
    is_physical_state,
    system_hamiltonian,
    unitary_from_hermitian,
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


def condition_on_clock(
    state: np.ndarray,
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
) -> np.ndarray:
    """Return (<t_j|_C tensor I_S)|state> for any kinematic vector."""

    d = _validate_dimension(dimension)
    j = _validate_clock_index(index, d)
    vector = _validate_global_state(state, d)
    amplitudes = vector.reshape(d, d)
    clock_bra = clock_state(j, d, origin=origin).conj()
    return clock_bra @ amplitudes


def clock_outcome_probability(
    state: np.ndarray,
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
) -> float:
    """Return ||(<t_j| tensor I)|state>||^2."""

    conditional = condition_on_clock(state, index, dimension, origin=origin)
    return float(np.vdot(conditional, conditional).real)


def clock_probability_profile(
    state: np.ndarray,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
) -> np.ndarray:
    """Return clock-outcome probabilities for the complete DFT clock basis."""

    d = _validate_dimension(dimension)
    return np.array(
        [
            clock_outcome_probability(state, j, d, origin=origin)
            for j in range(d)
        ],
        dtype=float,
    )


def physical_reduction(
    state: np.ndarray,
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
    atol: float = DEFAULT_ATOL,
) -> np.ndarray:
    """Apply R_j=sqrt(d)(<t_j| tensor I) to a constrained physical state."""

    d = _validate_dimension(dimension)
    vector = _validate_global_state(state, d)
    if not is_physical_state(vector, d, atol=atol):
        raise ValueError("state must satisfy the Stage 4 zero-constraint condition")
    return np.sqrt(d) * condition_on_clock(vector, index, d, origin=origin)


def normalized_physical_conditional_state(
    state: np.ndarray,
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
    atol: float = DEFAULT_ATOL,
) -> np.ndarray:
    """Return the unit-norm conditional ray representative for a physical state."""

    reduced = physical_reduction(
        state,
        index,
        dimension,
        origin=origin,
        atol=atol,
    )
    norm = float(np.linalg.norm(reduced))
    if norm <= atol:
        raise ValueError("conditional state has zero norm")
    return reduced / norm


def system_evolution_unitary(
    parameter: float,
    dimension: int = DEFAULT_DIMENSION,
) -> np.ndarray:
    """Return exp(-i H_S parameter)."""

    d = _validate_dimension(dimension)
    return unitary_from_hermitian(system_hamiltonian(d), parameter)


def conditional_schrodinger_residual(
    state: np.ndarray,
    target_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    reference_index: int = 0,
    origin: float = 0.0,
    atol: float = DEFAULT_ATOL,
) -> float:
    """Compare two physical reductions with the expected relative system unitary."""

    d = _validate_dimension(dimension)
    target = _validate_clock_index(target_index, d)
    reference = _validate_clock_index(reference_index, d)
    times = clock_reading_times(d, origin=origin)
    psi_reference = physical_reduction(
        state, reference, d, origin=origin, atol=atol
    )
    psi_target = physical_reduction(state, target, d, origin=origin, atol=atol)
    expected = system_evolution_unitary(times[target] - times[reference], d) @ psi_reference
    return float(np.linalg.norm(psi_target - expected))


def one_step_conditional_residuals(
    state: np.ndarray,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
    atol: float = DEFAULT_ATOL,
) -> np.ndarray:
    """Return residuals for psi_{j+1}=U_S(Delta)psi_j, including wrap-around."""

    d = _validate_dimension(dimension)
    step_unitary = system_evolution_unitary(clock_step(d), d)
    residuals: list[float] = []
    for j in range(d):
        next_j = (j + 1) % d
        psi_j = physical_reduction(state, j, d, origin=origin, atol=atol)
        psi_next = physical_reduction(state, next_j, d, origin=origin, atol=atol)
        residuals.append(float(np.linalg.norm(step_unitary @ psi_j - psi_next)))
    return np.array(residuals, dtype=float)


def full_period_system_residual(
    state: np.ndarray,
    dimension: int = DEFAULT_DIMENSION,
    *,
    index: int = 0,
    origin: float = 0.0,
    atol: float = DEFAULT_ATOL,
) -> float:
    """Return ||exp(-i H_S 2pi)psi_j-psi_j|| for one physical reduction."""

    d = _validate_dimension(dimension)
    j = _validate_clock_index(index, d)
    psi = physical_reduction(state, j, d, origin=origin, atol=atol)
    evolved = system_evolution_unitary(d * clock_step(d), d) @ psi
    return float(np.linalg.norm(evolved - psi))
