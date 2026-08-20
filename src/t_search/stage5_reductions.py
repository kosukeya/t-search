"""Stage 5B per-clock support, reduction, reconstruction, and transition utilities.

These functions build one clock-relative perspective at a time from the common
Stage 5 constrained physical space.  Genuine changes between distinct physical
clock subsystems remain deferred to Stage 5C.
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
    clock_reading_times,
    clock_state,
    constraint_compatible_triples,
    constraint_residual,
    label_to_index,
    subsystem_hamiltonian,
)

_SUBSYSTEM_INDEX = {"A": 0, "B": 1, "C": 2}


def _validate_subsystem(subsystem: str) -> str:
    if subsystem not in SUBSYSTEMS:
        raise ValueError("subsystem must be one of 'A', 'B', or 'C'")
    return subsystem


def _validate_rates(
    dimension: int,
    rates: Iterable[float],
) -> tuple[float, float, float]:
    values = tuple(rates)
    if len(values) != 3:
        raise ValueError("rates must contain exactly three values")
    validated: list[float] = []
    for value in values:
        # Reuse the Stage 5A rate validator through the public Hamiltonian API.
        h = subsystem_hamiltonian(dimension, rate=value)
        # The positive rate is the spacing between neighboring centered levels.
        labels = centered_energy_labels(dimension)
        nonzero = np.flatnonzero(labels != 0)
        if nonzero.size == 0:
            raise ValueError("declared energy basis must contain nonzero labels")
        idx = int(nonzero[0])
        validated.append(float(np.diag(h).real[idx] / labels[idx]))
    return tuple(validated)  # type: ignore[return-value]


def _validate_clock_index(index: int, dimension: int) -> int:
    if isinstance(index, bool) or not isinstance(index, Integral):
        raise ValueError("clock index must be an integer")
    # clock_state performs the dimension and range validation.
    clock_state(int(index), dimension)
    return int(index)


def _validate_global_state(state: np.ndarray, dimension: int) -> np.ndarray:
    d = len(centered_energy_labels(dimension))
    vector = np.asarray(state, dtype=np.complex128)
    expected = d**3
    if vector.shape != (expected,):
        raise ValueError(f"global state must have shape ({expected},)")
    if not np.all(np.isfinite(vector)):
        raise ValueError("global state amplitudes must be finite")
    return vector


def _validate_rest_state(state: np.ndarray, dimension: int) -> np.ndarray:
    d = len(centered_energy_labels(dimension))
    vector = np.asarray(state, dtype=np.complex128)
    expected = d**2
    if vector.shape != (expected,):
        raise ValueError(f"rest state must have shape ({expected},)")
    if not np.all(np.isfinite(vector)):
        raise ValueError("rest state amplitudes must be finite")
    return vector


def rest_subsystems(clock: str) -> tuple[str, str]:
    """Return the non-clock subsystem order used by one reduced perspective."""

    x = _validate_subsystem(clock)
    return tuple(name for name in SUBSYSTEMS if name != x)  # type: ignore[return-value]


def rest_pair_for_triple(
    triple: tuple[int, int, int],
    clock: str,
) -> tuple[int, int]:
    """Remove one clock label from an (A,B,C) energy triple."""

    x = _validate_subsystem(clock)
    index = _SUBSYSTEM_INDEX[x]
    return tuple(value for position, value in enumerate(triple) if position != index)  # type: ignore[return-value]


def rest_basis_state(
    pair: tuple[int, int],
    dimension: int = DEFAULT_DIMENSION,
) -> np.ndarray:
    """Return one product-energy basis vector in a d^2 rest tensor product."""

    d = len(centered_energy_labels(dimension))
    if len(pair) != 2:
        raise ValueError("rest energy label pair must contain exactly two values")
    first = label_to_index(pair[0], d)
    second = label_to_index(pair[1], d)
    vector = np.zeros(d**2, dtype=np.complex128)
    vector[first * d + second] = 1.0
    return vector


def clock_relative_support_pairs(
    clock: str,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> tuple[tuple[int, int], ...]:
    """Return rest-energy pairs compatible with the global zero constraint."""

    x = _validate_subsystem(clock)
    validated_rates = _validate_rates(dimension, rates)
    triples = constraint_compatible_triples(dimension, rates=validated_rates)
    pairs = tuple(rest_pair_for_triple(triple, x) for triple in triples)
    if len(set(pairs)) != len(pairs):
        raise ValueError("constraint does not define a unique clock label for each support pair")
    return pairs


def clock_relative_support_basis(
    clock: str,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Return the orthonormal support K_X as columns inside the d^2 rest space."""

    pairs = clock_relative_support_pairs(clock, dimension, rates=rates)
    return np.column_stack(tuple(rest_basis_state(pair, dimension) for pair in pairs))


def clock_relative_support_projector(
    clock: str,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    basis = clock_relative_support_basis(clock, dimension, rates=rates)
    return basis @ basis.conj().T


def clock_relative_support_dimension(
    clock: str,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> int:
    return len(clock_relative_support_pairs(clock, dimension, rates=rates))


def kinematic_clock_projection_operator(
    clock: str,
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Return P_X,j^kin=(<t_j|_X tensor I_rest) on the full kinematic space."""

    x = _validate_subsystem(clock)
    d = len(centered_energy_labels(dimension))
    j = _validate_clock_index(index, d)
    validated_rates = _validate_rates(d, rates)
    clock_position = _SUBSYSTEM_INDEX[x]
    rate = validated_rates[clock_position]
    reading = clock_state(j, d, rate=rate)

    projection = np.zeros((d**2, d**3), dtype=np.complex128)
    for raw_indices in product(range(d), repeat=3):
        global_index = (raw_indices[0] * d + raw_indices[1]) * d + raw_indices[2]
        clock_index = raw_indices[clock_position]
        rest_indices = tuple(
            value for position, value in enumerate(raw_indices) if position != clock_position
        )
        rest_index = rest_indices[0] * d + rest_indices[1]
        projection[rest_index, global_index] = np.conjugate(reading[clock_index])
    return projection


def formal_clock_conditioning(
    state: np.ndarray,
    clock: str,
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Condition an arbitrary kinematic state without declaring it physical."""

    vector = _validate_global_state(state, dimension)
    return kinematic_clock_projection_operator(
        clock, index, dimension, rates=rates
    ) @ vector


def physical_clock_reduction_operator(
    clock: str,
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Return sqrt(d) P_X,j^kin, intended only on H_phys."""

    d = len(centered_energy_labels(dimension))
    return np.sqrt(d) * kinematic_clock_projection_operator(
        clock, index, d, rates=rates
    )


def physical_clock_reduction(
    state: np.ndarray,
    clock: str,
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    atol: float = DEFAULT_ATOL,
) -> np.ndarray:
    """Reduce one physical global state to its X-clock support K_X."""

    vector = _validate_global_state(state, dimension)
    if constraint_residual(vector, dimension, rates=rates) > atol:
        raise ValueError("state must satisfy the declared Stage 5 constraint")
    return physical_clock_reduction_operator(
        clock, index, dimension, rates=rates
    ) @ vector


def physical_clock_probability(
    state: np.ndarray,
    clock: str,
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    atol: float = DEFAULT_ATOL,
) -> float:
    """Return ||P_X,j^kin |Psi>||^2 for a normalized physical state."""

    vector = _validate_global_state(state, dimension)
    if constraint_residual(vector, dimension, rates=rates) > atol:
        raise ValueError("state must satisfy the declared Stage 5 constraint")
    if not np.isclose(np.linalg.norm(vector), 1.0, atol=atol, rtol=0.0):
        raise ValueError("physical clock probability requires a normalized state")
    conditioned = formal_clock_conditioning(
        vector, clock, index, dimension, rates=rates
    )
    return float(np.vdot(conditioned, conditioned).real)


def support_coordinate_reduction_matrix(
    clock: str,
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Represent R_X(j): H_phys -> K_X in orthonormal support coordinates."""

    physical_basis = analytic_physical_basis(dimension, rates=rates)
    support_basis = clock_relative_support_basis(clock, dimension, rates=rates)
    reduction = physical_clock_reduction_operator(
        clock, index, dimension, rates=rates
    )
    return support_basis.conj().T @ reduction @ physical_basis


def clock_reconstruction_operator(
    clock: str,
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Return E_X(j): ambient rest space -> H_phys, inverse on K_X only."""

    physical_basis = analytic_physical_basis(dimension, rates=rates)
    support_basis = clock_relative_support_basis(clock, dimension, rates=rates)
    reduction_coordinates = support_coordinate_reduction_matrix(
        clock, index, dimension, rates=rates
    )
    return physical_basis @ reduction_coordinates.conj().T @ support_basis.conj().T


def reconstruct_physical_state(
    rest_state: np.ndarray,
    clock: str,
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    atol: float = DEFAULT_ATOL,
) -> np.ndarray:
    """Reconstruct a physical global state from a vector known to lie in K_X."""

    vector = _validate_rest_state(rest_state, dimension)
    projector = clock_relative_support_projector(clock, dimension, rates=rates)
    if np.linalg.norm((np.eye(projector.shape[0]) - projector) @ vector) > atol:
        raise ValueError("rest state must lie in the declared clock-relative support")
    return clock_reconstruction_operator(
        clock, index, dimension, rates=rates
    ) @ vector


def rest_hamiltonian(
    clock: str,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Return the sum of the two non-clock subsystem Hamiltonians."""

    x = _validate_subsystem(clock)
    d = len(centered_energy_labels(dimension))
    validated_rates = _validate_rates(d, rates)
    rate_by_name = dict(zip(SUBSYSTEMS, validated_rates))
    first, second = rest_subsystems(x)
    h_first = subsystem_hamiltonian(d, rate=rate_by_name[first])
    h_second = subsystem_hamiltonian(d, rate=rate_by_name[second])
    identity = np.eye(d, dtype=np.complex128)
    return np.kron(h_first, identity) + np.kron(identity, h_second)


def rest_unitary(
    clock: str,
    parameter: float,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Return exp(-i H_rest^(X) parameter) for the diagonal finite model."""

    if isinstance(parameter, bool) or not np.isscalar(parameter):
        raise ValueError("parameter must be a finite real number")
    tau = float(parameter)
    if not np.isfinite(tau):
        raise ValueError("parameter must be a finite real number")
    h = rest_hamiltonian(clock, dimension, rates=rates)
    return np.diag(np.exp(-1j * np.diag(h).real * tau)).astype(np.complex128)


def same_clock_transition_operator(
    clock: str,
    target_index: int,
    source_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Return T_X(k<-j)=R_X(k)E_X(j) on the ambient rest space."""

    reduction = physical_clock_reduction_operator(
        clock, target_index, dimension, rates=rates
    )
    reconstruction = clock_reconstruction_operator(
        clock, source_index, dimension, rates=rates
    )
    return reduction @ reconstruction


def same_clock_transition_support_matrix(
    clock: str,
    target_index: int,
    source_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Represent T_X(k<-j) as a square matrix on K_X coordinates."""

    support = clock_relative_support_basis(clock, dimension, rates=rates)
    transition = same_clock_transition_operator(
        clock, target_index, source_index, dimension, rates=rates
    )
    return support.conj().T @ transition @ support


def expected_same_clock_transition_operator(
    clock: str,
    target_index: int,
    source_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Return P_K exp[-i H_rest (t_k-t_j)] P_K on the ambient rest space."""

    x = _validate_subsystem(clock)
    d = len(centered_energy_labels(dimension))
    validated_rates = _validate_rates(d, rates)
    rate = validated_rates[_SUBSYSTEM_INDEX[x]]
    j = _validate_clock_index(source_index, d)
    k = _validate_clock_index(target_index, d)
    times = clock_reading_times(d, rate=rate)
    delta = float(times[k] - times[j])
    support_projector = clock_relative_support_projector(x, d, rates=validated_rates)
    evolution = rest_unitary(x, delta, d, rates=validated_rates)
    return support_projector @ evolution @ support_projector
