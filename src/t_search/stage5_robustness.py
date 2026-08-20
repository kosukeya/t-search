"""Stage 5G robustness diagnostics for physical clock changes.

The helpers in this module deliberately reuse the Stage 5A--5F public
construction while varying finite dimension, clock-rate scales, physical-state
coefficients, global phase, and subsystem bookkeeping.  They are diagnostics
for the declared toy family, not claims of quantum general covariance.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations, product
from typing import Iterable, Sequence

import numpy as np

from .stage5_clock_change import (
    DEFAULT_ATOL,
    DEFAULT_DIMENSION,
    DEFAULT_RATES,
    SUBSYSTEMS,
    analytic_physical_basis,
    centered_energy_labels,
    clock_reading_times,
    constraint_residual,
    physical_state_from_coefficients,
)
from .stage5_reductions import (
    clock_reconstruction_operator,
    clock_relative_support_basis,
    clock_relative_support_dimension,
    expected_same_clock_transition_operator,
    physical_clock_probability,
    physical_clock_reduction,
    physical_clock_reduction_operator,
)


@dataclass(frozen=True)
class Stage5RobustnessSummary:
    dimension: int
    rates: tuple[float, float, float]
    physical_dimension: int
    support_dimensions: tuple[int, int, int]
    max_constraint_residual: float
    max_clock_probability_residual: float
    max_reduction_isometry_residual: float
    max_physical_roundtrip_residual: float
    max_same_clock_dynamics_residual: float
    max_clock_change_unitarity_residual: float
    max_direct_route_residual: float
    max_composition_residual: float
    max_born_covariance_residual: float


def deterministic_physical_coefficients(
    physical_dimension: int,
    *,
    family: str = "generic",
) -> np.ndarray:
    """Return one deterministic nonzero complex coefficient family."""

    if isinstance(physical_dimension, bool) or not isinstance(physical_dimension, int):
        raise ValueError("physical_dimension must be an integer")
    if physical_dimension < 1:
        raise ValueError("physical_dimension must be positive")

    n = physical_dimension
    index = np.arange(1, n + 1, dtype=float)
    if family == "generic":
        values = (1.0 + 0.17 * index) + 1j * (0.31 * np.cos(index) - 0.11 * index)
    elif family == "alternating":
        signs = np.where(np.arange(n) % 2 == 0, 1.0, -1.0)
        values = signs * (0.7 + 0.09 * index) + 1j * (0.23 * np.sin(index))
    elif family == "sparse":
        values = np.zeros(n, dtype=np.complex128)
        values[0] = 1.0 + 0.25j
        if n > 1:
            values[-1] = -0.45 + 0.8j
    else:
        raise ValueError("family must be 'generic', 'alternating', or 'sparse'")

    values = np.asarray(values, dtype=np.complex128)
    norm = np.linalg.norm(values)
    if norm <= DEFAULT_ATOL:
        raise RuntimeError("deterministic coefficient family unexpectedly vanished")
    return values / norm


def _validated_rates(rates: Iterable[float]) -> tuple[float, float, float]:
    values = tuple(float(value) for value in rates)
    if len(values) != 3 or not all(np.isfinite(value) and value > 0.0 for value in values):
        raise ValueError("rates must contain exactly three finite positive values")
    return values


def stage5_joint_robustness_summary(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    coefficient_family: str = "generic",
) -> Stage5RobustnessSummary:
    """Evaluate the main Stage 5 structural/operational identities together.

    The full discrete reading sets are used for the declared finite model,
    including all ordered distinct-clock composition routes.
    """

    d = len(centered_energy_labels(dimension))
    validated_rates = _validated_rates(rates)
    physical_basis = analytic_physical_basis(d, rates=validated_rates)
    physical_dimension = physical_basis.shape[1]
    coefficients = deterministic_physical_coefficients(
        physical_dimension, family=coefficient_family
    )
    state = physical_state_from_coefficients(
        coefficients, d, rates=validated_rates, normalize=False
    )

    support_bases = {
        clock: clock_relative_support_basis(clock, d, rates=validated_rates)
        for clock in SUBSYSTEMS
    }
    support_dimensions = tuple(
        clock_relative_support_dimension(clock, d, rates=validated_rates)
        for clock in SUBSYSTEMS
    )
    if any(value != physical_dimension for value in support_dimensions):
        raise RuntimeError("declared robustness family lost physical/support dimension matching")

    reductions = {
        (clock, j): physical_clock_reduction_operator(
            clock, j, d, rates=validated_rates
        )
        for clock in SUBSYSTEMS
        for j in range(d)
    }
    reconstructions = {
        (clock, j): clock_reconstruction_operator(
            clock, j, d, rates=validated_rates
        )
        for clock in SUBSYSTEMS
        for j in range(d)
    }

    identity_phys = np.eye(physical_dimension, dtype=np.complex128)
    max_constraint = constraint_residual(state, d, rates=validated_rates)
    max_probability = 0.0
    max_isometry = 0.0
    max_roundtrip = 0.0
    max_same_clock = 0.0

    for clock in SUBSYSTEMS:
        support = support_bases[clock]
        identity_support = np.eye(physical_dimension, dtype=np.complex128)
        for j in range(d):
            probability = physical_clock_probability(
                state, clock, j, d, rates=validated_rates
            )
            max_probability = max(max_probability, abs(probability - 1.0 / d))

            coordinate_reduction = support.conj().T @ reductions[(clock, j)] @ physical_basis
            max_isometry = max(
                max_isometry,
                float(np.linalg.norm(coordinate_reduction.conj().T @ coordinate_reduction - identity_phys)),
                float(np.linalg.norm(coordinate_reduction @ coordinate_reduction.conj().T - identity_support)),
            )
            coordinate_reconstruction = physical_basis.conj().T @ reconstructions[(clock, j)] @ support
            max_roundtrip = max(
                max_roundtrip,
                float(np.linalg.norm(coordinate_reconstruction @ coordinate_reduction - identity_phys)),
                float(np.linalg.norm(coordinate_reduction @ coordinate_reconstruction - identity_support)),
            )

        for j, k in product(range(d), repeat=2):
            transition = reductions[(clock, k)] @ reconstructions[(clock, j)]
            expected = expected_same_clock_transition_operator(
                clock, k, j, d, rates=validated_rates
            )
            max_same_clock = max(
                max_same_clock, float(np.linalg.norm(transition - expected))
            )

    clock_change: dict[tuple[str, int, str, int], np.ndarray] = {}
    max_clock_change_unitarity = 0.0
    max_direct_route = 0.0
    max_born = 0.0

    for source_clock in SUBSYSTEMS:
        source_support = support_bases[source_clock]
        # Nontrivial rank-one source projector, guaranteed to live in K_X.
        source_vector = source_support[:, 0].copy()
        if physical_dimension > 1:
            source_vector = source_vector + (0.4 + 0.3j) * source_support[:, -1]
        source_vector = source_vector / np.linalg.norm(source_vector)
        source_projector = np.outer(source_vector, source_vector.conj())

        for target_clock in SUBSYSTEMS:
            if target_clock == source_clock:
                continue
            target_support = support_bases[target_clock]
            identity_support = np.eye(physical_dimension, dtype=np.complex128)
            for j, k in product(range(d), repeat=2):
                transform = reductions[(target_clock, k)] @ reconstructions[(source_clock, j)]
                clock_change[(target_clock, k, source_clock, j)] = transform
                coordinate_transform = target_support.conj().T @ transform @ source_support
                max_clock_change_unitarity = max(
                    max_clock_change_unitarity,
                    float(np.linalg.norm(coordinate_transform.conj().T @ coordinate_transform - identity_support)),
                    float(np.linalg.norm(coordinate_transform @ coordinate_transform.conj().T - identity_support)),
                )

                source_state = reductions[(source_clock, j)] @ state
                target_direct = reductions[(target_clock, k)] @ state
                target_via_source = transform @ source_state
                max_direct_route = max(
                    max_direct_route,
                    float(np.linalg.norm(target_via_source - target_direct)),
                )

                transformed_projector = transform @ source_projector @ transform.conj().T
                source_probability = float(np.vdot(source_state, source_projector @ source_state).real)
                target_probability = float(
                    np.vdot(target_direct, transformed_projector @ target_direct).real
                )
                max_born = max(max_born, abs(source_probability - target_probability))

    max_composition = 0.0
    for source_clock, middle_clock, target_clock in permutations(SUBSYSTEMS, 3):
        for j, k, ell in product(range(d), repeat=3):
            first = clock_change[(middle_clock, k, source_clock, j)]
            second = clock_change[(target_clock, ell, middle_clock, k)]
            direct = clock_change[(target_clock, ell, source_clock, j)]
            max_composition = max(
                max_composition,
                float(np.linalg.norm(second @ first - direct)),
            )

    return Stage5RobustnessSummary(
        dimension=d,
        rates=validated_rates,
        physical_dimension=physical_dimension,
        support_dimensions=support_dimensions,
        max_constraint_residual=float(max_constraint),
        max_clock_probability_residual=float(max_probability),
        max_reduction_isometry_residual=float(max_isometry),
        max_physical_roundtrip_residual=float(max_roundtrip),
        max_same_clock_dynamics_residual=float(max_same_clock),
        max_clock_change_unitarity_residual=float(max_clock_change_unitarity),
        max_direct_route_residual=float(max_direct_route),
        max_composition_residual=float(max_composition),
        max_born_covariance_residual=float(max_born),
    )


def global_phase_density_residuals(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    phase: float = 0.731,
) -> tuple[float, float]:
    """Return max reduced-density and clock-probability changes under global phase."""

    d = len(centered_energy_labels(dimension))
    validated_rates = _validated_rates(rates)
    physical_dimension = analytic_physical_basis(d, rates=validated_rates).shape[1]
    coefficients = deterministic_physical_coefficients(physical_dimension, family="generic")
    state = physical_state_from_coefficients(coefficients, d, rates=validated_rates)
    phased = np.exp(1j * float(phase)) * state

    max_density = 0.0
    max_probability = 0.0
    for clock in SUBSYSTEMS:
        for j in range(d):
            reduced = physical_clock_reduction(state, clock, j, d, rates=validated_rates)
            reduced_phased = physical_clock_reduction(
                phased, clock, j, d, rates=validated_rates
            )
            rho = np.outer(reduced, reduced.conj())
            rho_phased = np.outer(reduced_phased, reduced_phased.conj())
            max_density = max(max_density, float(np.linalg.norm(rho_phased - rho)))
            p = physical_clock_probability(state, clock, j, d, rates=validated_rates)
            p_phased = physical_clock_probability(
                phased, clock, j, d, rates=validated_rates
            )
            max_probability = max(max_probability, abs(p_phased - p))
    return max_density, max_probability


def subsystem_permutations() -> tuple[tuple[str, str, str], ...]:
    """Return all old-name -> new-name permutations in A/B/C order."""

    return tuple(permutations(SUBSYSTEMS, 3))


def _validate_permutation(permutation: Sequence[str]) -> tuple[str, str, str]:
    values = tuple(permutation)
    if len(values) != 3 or set(values) != set(SUBSYSTEMS):
        raise ValueError("permutation must contain A, B, C exactly once")
    return values  # type: ignore[return-value]


def global_subsystem_permutation_operator(
    permutation: Sequence[str],
    dimension: int = DEFAULT_DIMENSION,
) -> np.ndarray:
    """Return U_pi sending old subsystem X to new subsystem pi(X)."""

    values = _validate_permutation(permutation)
    d = len(centered_energy_labels(dimension))
    name_to_position = {name: position for position, name in enumerate(SUBSYSTEMS)}
    mapping = dict(zip(SUBSYSTEMS, values))
    operator = np.zeros((d**3, d**3), dtype=np.complex128)
    for old_indices in product(range(d), repeat=3):
        new_indices = [0, 0, 0]
        for old_position, old_name in enumerate(SUBSYSTEMS):
            new_name = mapping[old_name]
            new_indices[name_to_position[new_name]] = old_indices[old_position]
        old_flat = (old_indices[0] * d + old_indices[1]) * d + old_indices[2]
        new_flat = (new_indices[0] * d + new_indices[1]) * d + new_indices[2]
        operator[new_flat, old_flat] = 1.0
    return operator


def rest_subsystem_permutation_operator(
    source_clock: str,
    permutation: Sequence[str],
    dimension: int = DEFAULT_DIMENSION,
) -> tuple[str, np.ndarray]:
    """Return the induced rest-coordinate permutation and target clock name."""

    values = _validate_permutation(permutation)
    if source_clock not in SUBSYSTEMS:
        raise ValueError("source_clock must be A, B, or C")
    d = len(centered_energy_labels(dimension))
    mapping = dict(zip(SUBSYSTEMS, values))
    target_clock = mapping[source_clock]
    source_rest = tuple(name for name in SUBSYSTEMS if name != source_clock)
    target_rest = tuple(name for name in SUBSYSTEMS if name != target_clock)

    operator = np.zeros((d**2, d**2), dtype=np.complex128)
    for old_indices in product(range(d), repeat=2):
        carried = {
            mapping[source_rest[position]]: old_indices[position]
            for position in range(2)
        }
        new_indices = (carried[target_rest[0]], carried[target_rest[1]])
        old_flat = old_indices[0] * d + old_indices[1]
        new_flat = new_indices[0] * d + new_indices[1]
        operator[new_flat, old_flat] = 1.0
    return target_clock, operator
