"""Stage 5E operational covariance and perspective-dependent structure.

A genuine clock change transforms reduced observables together with reduced
states.  Reduced operators are support operators: they act on K_X inside the
ambient d^2 rest tensor product and must not be silently identified across
clock choices merely because their ambient matrix shapes coincide.
"""

from __future__ import annotations

from numbers import Real
from typing import Iterable

import numpy as np

from .stage5_clock_change import (
    DEFAULT_ATOL,
    DEFAULT_DIMENSION,
    DEFAULT_RATES,
    centered_energy_labels,
    physical_subspace_projector,
)
from .stage5_clock_transforms import genuine_clock_change_operator
from .stage5_reductions import (
    clock_reconstruction_operator,
    clock_relative_support_projector,
    physical_clock_reduction,
    physical_clock_reduction_operator,
)


def _rest_dimension(dimension: int) -> int:
    return len(centered_energy_labels(dimension)) ** 2


def _global_dimension(dimension: int) -> int:
    return len(centered_energy_labels(dimension)) ** 3


def _validate_rest_state(state: np.ndarray, dimension: int) -> np.ndarray:
    vector = np.asarray(state, dtype=np.complex128)
    expected = _rest_dimension(dimension)
    if vector.shape != (expected,):
        raise ValueError(f"rest state must have shape ({expected},)")
    if not np.all(np.isfinite(vector)):
        raise ValueError("rest state amplitudes must be finite")
    return vector


def _validate_normalized_rest_state(
    state: np.ndarray,
    dimension: int,
    *,
    atol: float,
) -> np.ndarray:
    vector = _validate_rest_state(state, dimension)
    if not np.isclose(np.linalg.norm(vector), 1.0, atol=atol, rtol=0.0):
        raise ValueError("rest state must be normalized")
    return vector


def _validate_rest_operator(operator: np.ndarray, dimension: int) -> np.ndarray:
    matrix = np.asarray(operator, dtype=np.complex128)
    expected = _rest_dimension(dimension)
    if matrix.shape != (expected, expected):
        raise ValueError(f"rest operator must have shape ({expected},{expected})")
    if not np.all(np.isfinite(matrix)):
        raise ValueError("rest operator entries must be finite")
    return matrix


def _validate_physical_operator(operator: np.ndarray, dimension: int) -> np.ndarray:
    matrix = np.asarray(operator, dtype=np.complex128)
    expected = _global_dimension(dimension)
    if matrix.shape != (expected, expected):
        raise ValueError(f"physical operator must have shape ({expected},{expected})")
    if not np.all(np.isfinite(matrix)):
        raise ValueError("physical operator entries must be finite")
    return matrix


def support_operator_residual(
    operator: np.ndarray,
    clock: str,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> float:
    """Return ||O-P_K O P_K|| for one reduced clock perspective."""

    matrix = _validate_rest_operator(operator, dimension)
    projector = clock_relative_support_projector(clock, dimension, rates=rates)
    return float(np.linalg.norm(matrix - projector @ matrix @ projector))


def validate_reduced_observable(
    operator: np.ndarray,
    clock: str,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    atol: float = DEFAULT_ATOL,
) -> np.ndarray:
    """Validate a Hermitian support operator for one clock perspective."""

    matrix = _validate_rest_operator(operator, dimension)
    if np.linalg.norm(matrix - matrix.conj().T) > atol:
        raise ValueError("reduced observable must be Hermitian")
    if support_operator_residual(matrix, clock, dimension, rates=rates) > atol:
        raise ValueError("reduced observable must act within the declared clock support")
    return matrix


def transform_reduced_observable(
    operator: np.ndarray,
    target_clock: str,
    target_index: int,
    source_clock: str,
    source_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    atol: float = DEFAULT_ATOL,
) -> np.ndarray:
    """Return O_Y=S_{Y<-X} O_X S_{Y<-X}^dagger."""

    source_operator = validate_reduced_observable(
        operator,
        source_clock,
        dimension,
        rates=rates,
        atol=atol,
    )
    transform = genuine_clock_change_operator(
        target_clock,
        target_index,
        source_clock,
        source_index,
        dimension,
        rates=rates,
    )
    transformed = transform @ source_operator @ transform.conj().T

    target_projector = clock_relative_support_projector(
        target_clock, dimension, rates=rates
    )
    if np.linalg.norm(transformed - target_projector @ transformed @ target_projector) > atol:
        raise RuntimeError("transformed observable failed to land in target support")
    if np.linalg.norm(transformed - transformed.conj().T) > atol:
        raise RuntimeError("transformed observable failed Hermiticity check")
    return transformed


def lift_reduced_observable_to_physical(
    operator: np.ndarray,
    clock: str,
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    atol: float = DEFAULT_ATOL,
) -> np.ndarray:
    """Lift a reduced support observable into the common constrained space.

    The reduction matrix is defined on the full kinematic space, so the lifted
    operator must be explicitly restricted on both sides to H_phys.  Without
    that domain restriction E_X O_X R_X can have nonzero action on kinematic
    inputs outside the physical subspace even though its image lies in H_phys.
    """

    reduced = validate_reduced_observable(
        operator, clock, dimension, rates=rates, atol=atol
    )
    reconstruction = clock_reconstruction_operator(clock, index, dimension, rates=rates)
    reduction = physical_clock_reduction_operator(clock, index, dimension, rates=rates)
    physical_projector = physical_subspace_projector(dimension, rates=rates)
    lifted = (
        physical_projector
        @ reconstruction
        @ reduced
        @ reduction
        @ physical_projector
    )

    if np.linalg.norm(lifted - physical_projector @ lifted @ physical_projector) > atol:
        raise RuntimeError("lifted observable failed to remain in the physical subspace")
    if np.linalg.norm(lifted - lifted.conj().T) > atol:
        raise RuntimeError("lifted observable failed Hermiticity check")
    return lifted


def reduce_physical_observable_to_clock(
    operator: np.ndarray,
    clock: str,
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    atol: float = DEFAULT_ATOL,
) -> np.ndarray:
    """Reduce one Hermitian physical-subspace operator to clock support K_X."""

    physical = _validate_physical_operator(operator, dimension)
    if np.linalg.norm(physical - physical.conj().T) > atol:
        raise ValueError("physical observable must be Hermitian")
    projector = physical_subspace_projector(dimension, rates=rates)
    if np.linalg.norm(physical - projector @ physical @ projector) > atol:
        raise ValueError("physical observable must act within the declared physical subspace")

    reduction = physical_clock_reduction_operator(clock, index, dimension, rates=rates)
    reconstruction = clock_reconstruction_operator(clock, index, dimension, rates=rates)
    reduced = reduction @ physical @ reconstruction
    return validate_reduced_observable(
        reduced, clock, dimension, rates=rates, atol=atol
    )


def reduced_expectation_value(
    state: np.ndarray,
    observable: np.ndarray,
    dimension: int = DEFAULT_DIMENSION,
    *,
    atol: float = DEFAULT_ATOL,
) -> float:
    """Return <psi|O|psi> for a normalized reduced pure state."""

    vector = _validate_normalized_rest_state(state, dimension, atol=atol)
    matrix = _validate_rest_operator(observable, dimension)
    if np.linalg.norm(matrix - matrix.conj().T) > atol:
        raise ValueError("observable must be Hermitian")
    value = np.vdot(vector, matrix @ vector)
    if abs(value.imag) > atol:
        raise RuntimeError("Hermitian expectation acquired an unexpected imaginary part")
    return float(value.real)


def reduced_born_probability(
    state: np.ndarray,
    projector: np.ndarray,
    dimension: int = DEFAULT_DIMENSION,
    *,
    atol: float = DEFAULT_ATOL,
) -> float:
    """Return the Born probability for a normalized reduced state/projector."""

    matrix = _validate_rest_operator(projector, dimension)
    if np.linalg.norm(matrix - matrix.conj().T) > atol:
        raise ValueError("projector must be Hermitian")
    if np.linalg.norm(matrix @ matrix - matrix) > atol:
        raise ValueError("projector must be idempotent")
    probability = reduced_expectation_value(state, matrix, dimension, atol=atol)
    if probability < -atol or probability > 1.0 + atol:
        raise RuntimeError("Born probability fell outside [0,1] beyond tolerance")
    return float(np.clip(probability, 0.0, 1.0))


def pure_bipartite_entanglement_entropy(
    state: np.ndarray,
    dimension: int = DEFAULT_DIMENSION,
    *,
    base: float = 2.0,
    atol: float = DEFAULT_ATOL,
) -> float:
    """Return the pure-state bipartite entropy for a d x d reduced rest state."""

    vector = _validate_normalized_rest_state(state, dimension, atol=atol)
    if isinstance(base, bool) or not isinstance(base, Real):
        raise ValueError("entropy base must be a finite positive real number other than one")
    base_value = float(base)
    if not np.isfinite(base_value) or base_value <= 0.0 or np.isclose(base_value, 1.0):
        raise ValueError("entropy base must be a finite positive real number other than one")

    d = len(centered_energy_labels(dimension))
    amplitudes = vector.reshape(d, d)
    rho_first = amplitudes @ amplitudes.conj().T
    eigenvalues = np.linalg.eigvalsh(rho_first).real
    eigenvalues[np.abs(eigenvalues) < atol] = 0.0
    if np.min(eigenvalues) < -atol:
        raise RuntimeError("reduced density matrix is not positive semidefinite")
    eigenvalues = np.clip(eigenvalues, 0.0, None)
    total = float(np.sum(eigenvalues))
    if not np.isclose(total, 1.0, atol=atol, rtol=0.0):
        raise RuntimeError("reduced density eigenvalues do not sum to one")
    nonzero = eigenvalues[eigenvalues > atol]
    if nonzero.size == 0:
        return 0.0
    entropy = -np.sum(nonzero * np.log(nonzero)) / np.log(base_value)
    return float(entropy)


def perspective_entanglement_entropy(
    physical_state: np.ndarray,
    clock: str,
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    base: float = 2.0,
    atol: float = DEFAULT_ATOL,
) -> float:
    """Reduce a physical state relative to one clock and compute rest entanglement."""

    reduced = physical_clock_reduction(
        physical_state,
        clock,
        index,
        dimension,
        rates=rates,
        atol=atol,
    )
    return pure_bipartite_entanglement_entropy(
        reduced, dimension, base=base, atol=atol
    )
