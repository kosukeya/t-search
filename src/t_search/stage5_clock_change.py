"""Stage 5 change-of-clock utilities.

Stage 5A implements only the symmetric three-subsystem constrained substrate:
three finite odd-dimensional subsystems, the zero-sum constraint, its analytic
physical basis, numerical kernel diagnostics, and one finite DFT clock basis per
subsystem. Physical reductions and cross-clock perspective changes begin in
Stage 5B/C and are intentionally absent here.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import product
from numbers import Integral, Real
from typing import Iterable

import numpy as np

DEFAULT_DIMENSION = 3
DEFAULT_ATOL = 1e-10
SUBSYSTEMS = ("A", "B", "C")
DEFAULT_RATES = (1.0, 1.0, 1.0)


@dataclass(frozen=True)
class Stage5AConstrainedModel:
    """Symmetric three-subsystem Stage 5A baseline fixture."""

    dimension: int
    rates: tuple[float, float, float]
    energy_labels: np.ndarray
    h_a: np.ndarray
    h_b: np.ndarray
    h_c: np.ndarray
    h_total: np.ndarray
    physical_basis: np.ndarray
    clock_bases: dict[str, np.ndarray]

    @property
    def kinematic_dimension(self) -> int:
        return self.dimension**3

    @property
    def physical_dimension(self) -> int:
        return self.physical_basis.shape[1]


def _validate_dimension(dimension: int) -> int:
    if isinstance(dimension, bool) or not isinstance(dimension, Integral):
        raise ValueError("dimension must be an odd integer")
    d = int(dimension)
    if d < 3 or d % 2 == 0:
        raise ValueError("dimension must be an odd integer at least three")
    return d


def _validate_rate(rate: float) -> float:
    if isinstance(rate, bool) or not isinstance(rate, Real):
        raise ValueError("clock rate must be a finite positive real number")
    value = float(rate)
    if not np.isfinite(value) or value <= 0.0:
        raise ValueError("clock rate must be a finite positive real number")
    return value


def _validate_rates(rates: Iterable[float]) -> tuple[float, float, float]:
    values = tuple(_validate_rate(rate) for rate in rates)
    if len(values) != 3:
        raise ValueError("rates must contain exactly three values")
    return values


def _validate_subsystem(subsystem: str) -> str:
    if subsystem not in SUBSYSTEMS:
        raise ValueError("subsystem must be one of 'A', 'B', or 'C'")
    return subsystem


def _validate_clock_index(index: int, dimension: int) -> int:
    d = _validate_dimension(dimension)
    if isinstance(index, bool) or not isinstance(index, Integral):
        raise ValueError("clock index must be an integer")
    j = int(index)
    if not 0 <= j < d:
        raise ValueError(f"clock index must be between 0 and {d - 1}")
    return j


def centered_energy_labels(dimension: int = DEFAULT_DIMENSION) -> np.ndarray:
    """Return symmetric integer energy labels -q,...,+q for odd d=2q+1."""

    d = _validate_dimension(dimension)
    q = (d - 1) // 2
    return np.arange(-q, q + 1, dtype=int)


def kinematic_dimension(dimension: int = DEFAULT_DIMENSION) -> int:
    """Return dim(H_A tensor H_B tensor H_C)=d^3."""

    d = _validate_dimension(dimension)
    return d**3


def subsystem_hamiltonian(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rate: float = 1.0,
) -> np.ndarray:
    """Return H_X with eigenvalues lambda*m in the centered energy basis."""

    labels = centered_energy_labels(dimension).astype(float)
    lam = _validate_rate(rate)
    return np.diag(lam * labels).astype(np.complex128)


def total_constraint_operator(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Return H_tot=H_A+H_B+H_C on the three-subsystem tensor product."""

    d = _validate_dimension(dimension)
    rate_a, rate_b, rate_c = _validate_rates(rates)
    identity = np.eye(d, dtype=np.complex128)
    h_a = subsystem_hamiltonian(d, rate=rate_a)
    h_b = subsystem_hamiltonian(d, rate=rate_b)
    h_c = subsystem_hamiltonian(d, rate=rate_c)
    return (
        np.kron(np.kron(h_a, identity), identity)
        + np.kron(np.kron(identity, h_b), identity)
        + np.kron(np.kron(identity, identity), h_c)
    )


def label_to_index(label: int, dimension: int = DEFAULT_DIMENSION) -> int:
    """Return the tensor-basis index corresponding to one centered energy label."""

    labels = centered_energy_labels(dimension)
    matches = np.flatnonzero(labels == label)
    if matches.size != 1:
        raise ValueError("energy label is outside the declared basis")
    return int(matches[0])


def tensor_basis_state(
    a: int,
    b: int,
    c: int,
    dimension: int = DEFAULT_DIMENSION,
) -> np.ndarray:
    """Return |a,b,c> using physical energy labels rather than raw indices."""

    d = _validate_dimension(dimension)
    ia = label_to_index(a, d)
    ib = label_to_index(b, d)
    ic = label_to_index(c, d)
    vector = np.zeros(d**3, dtype=np.complex128)
    vector[(ia * d + ib) * d + ic] = 1.0
    return vector


def constraint_compatible_triples(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    atol: float = DEFAULT_ATOL,
) -> tuple[tuple[int, int, int], ...]:
    """Return energy-label triples satisfying lambda_A*a+lambda_B*b+lambda_C*c=0."""

    labels = tuple(int(value) for value in centered_energy_labels(dimension))
    rate_a, rate_b, rate_c = _validate_rates(rates)
    allowed: list[tuple[int, int, int]] = []
    for a, b, c in product(labels, repeat=3):
        total = rate_a * a + rate_b * b + rate_c * c
        if abs(total) <= atol:
            allowed.append((a, b, c))
    return tuple(allowed)


def analytic_physical_basis(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Return the exact constraint-compatible product basis as matrix columns."""

    d = _validate_dimension(dimension)
    triples = constraint_compatible_triples(d, rates=rates)
    return np.column_stack(tuple(tensor_basis_state(*triple, d) for triple in triples))


def numerical_constraint_kernel_basis(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    atol: float = DEFAULT_ATOL,
) -> np.ndarray:
    """Return a numerical orthonormal basis for ker(H_tot)."""

    h_total = total_constraint_operator(dimension, rates=rates)
    eigenvalues, eigenvectors = np.linalg.eigh(h_total)
    mask = np.abs(eigenvalues) <= atol
    return eigenvectors[:, mask]


def physical_subspace_projector(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    basis = analytic_physical_basis(dimension, rates=rates)
    return basis @ basis.conj().T


def numerical_kernel_projector(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    atol: float = DEFAULT_ATOL,
) -> np.ndarray:
    basis = numerical_constraint_kernel_basis(dimension, rates=rates, atol=atol)
    return basis @ basis.conj().T


def physical_subspace_dimension(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> int:
    return len(constraint_compatible_triples(dimension, rates=rates))


def physical_state_from_coefficients(
    coefficients: np.ndarray,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    normalize: bool = False,
) -> np.ndarray:
    """Embed physical-basis coefficients into the full kinematic space."""

    basis = analytic_physical_basis(dimension, rates=rates)
    vector = np.asarray(coefficients, dtype=np.complex128)
    expected = basis.shape[1]
    if vector.shape != (expected,):
        raise ValueError(f"coefficients must have shape ({expected},)")
    if not np.all(np.isfinite(vector)):
        raise ValueError("coefficients must be finite")
    norm = np.linalg.norm(vector)
    if norm <= DEFAULT_ATOL:
        raise ValueError("coefficients must define a nonzero state")
    if normalize:
        vector = vector / norm
    return basis @ vector


def constraint_residual(
    state: np.ndarray,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> float:
    d = _validate_dimension(dimension)
    vector = np.asarray(state, dtype=np.complex128)
    expected = d**3
    if vector.shape != (expected,):
        raise ValueError(f"global state must have shape ({expected},)")
    if not np.all(np.isfinite(vector)):
        raise ValueError("global state amplitudes must be finite")
    return float(np.linalg.norm(total_constraint_operator(d, rates=rates) @ vector))


def clock_step(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rate: float = 1.0,
) -> float:
    d = _validate_dimension(dimension)
    lam = _validate_rate(rate)
    return 2.0 * np.pi / (d * lam)


def clock_reading_times(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rate: float = 1.0,
) -> np.ndarray:
    d = _validate_dimension(dimension)
    return clock_step(d, rate=rate) * np.arange(d, dtype=float)


def clock_state(
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rate: float = 1.0,
) -> np.ndarray:
    """Return one finite DFT clock-reading state for a positive Hamiltonian."""

    d = _validate_dimension(dimension)
    j = _validate_clock_index(index, d)
    lam = _validate_rate(rate)
    labels = centered_energy_labels(d).astype(float)
    time = j * clock_step(d, rate=lam)
    return np.exp(-1j * lam * labels * time) / np.sqrt(d)


def clock_basis_matrix(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rate: float = 1.0,
) -> np.ndarray:
    d = _validate_dimension(dimension)
    lam = _validate_rate(rate)
    return np.column_stack(tuple(clock_state(j, d, rate=lam) for j in range(d)))


def clock_translation_unitary(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rate: float = 1.0,
    steps: int = 1,
) -> np.ndarray:
    """Return exp(-i H_X steps*Delta_X) for one subsystem clock."""

    d = _validate_dimension(dimension)
    lam = _validate_rate(rate)
    if isinstance(steps, bool) or not isinstance(steps, Integral):
        raise ValueError("steps must be an integer")
    h = subsystem_hamiltonian(d, rate=lam)
    parameter = int(steps) * clock_step(d, rate=lam)
    phases = np.exp(-1j * np.diag(h).real * parameter)
    return np.diag(phases).astype(np.complex128)


def canonical_stage5a_model(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> Stage5AConstrainedModel:
    """Construct the declared Stage 5A substrate without reduced perspectives."""

    d = _validate_dimension(dimension)
    rate_a, rate_b, rate_c = _validate_rates(rates)
    h_a = subsystem_hamiltonian(d, rate=rate_a)
    h_b = subsystem_hamiltonian(d, rate=rate_b)
    h_c = subsystem_hamiltonian(d, rate=rate_c)
    return Stage5AConstrainedModel(
        dimension=d,
        rates=(rate_a, rate_b, rate_c),
        energy_labels=centered_energy_labels(d),
        h_a=h_a,
        h_b=h_b,
        h_c=h_c,
        h_total=total_constraint_operator(d, rates=(rate_a, rate_b, rate_c)),
        physical_basis=analytic_physical_basis(d, rates=(rate_a, rate_b, rate_c)),
        clock_bases={
            "A": clock_basis_matrix(d, rate=rate_a),
            "B": clock_basis_matrix(d, rate=rate_b),
            "C": clock_basis_matrix(d, rate=rate_c),
        },
    )
