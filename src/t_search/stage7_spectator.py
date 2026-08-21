"""Stage 7A spectator-memory constrained baseline.

Stage 7A adds a two-dimensional memory factor to the Stage 5 constrained
three-clock model without any record-writing interaction.  The purpose is to
verify, rather than merely assume, that the inherited constrained perspective
structure extends by an identity action on memory.

The spectator construction is deliberately a strict no-record control:
``memory present != record present``.  A positive record witness is not inferred
from the existence of the memory tensor factor or from arbitrary pre-existing
correlations.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import permutations, product
from typing import Iterable

import numpy as np

from .stage5_clock_change import (
    DEFAULT_ATOL,
    DEFAULT_DIMENSION,
    DEFAULT_RATES,
    SUBSYSTEMS,
    analytic_physical_basis,
    centered_energy_labels,
    physical_state_from_coefficients,
    total_constraint_operator,
)
from .stage5_clock_transforms import genuine_clock_change_operator
from .stage5_reductions import (
    clock_reconstruction_operator,
    clock_relative_support_basis,
    clock_relative_support_projector,
    kinematic_clock_projection_operator,
    physical_clock_reduction_operator,
    same_clock_transition_operator,
)

MEMORY_DIMENSION = 2


@dataclass(frozen=True)
class SpectatorClockChangeDiagnostics:
    comparisons: int
    max_state_residual: float
    max_born_residual: float
    max_inverse_residual: float


@dataclass(frozen=True)
class SpectatorCompositionDiagnostics:
    comparisons: int
    max_composition_residual: float


@dataclass(frozen=True)
class SpectatorRecordDiagnostics:
    comparisons: int
    max_target_memory_mutual_information: float
    positive_record_witness: bool
    record_coupling_present: bool


def memory_identity() -> np.ndarray:
    return np.eye(MEMORY_DIMENSION, dtype=np.complex128)


def spectator_kinematic_dimension(dimension: int = DEFAULT_DIMENSION) -> int:
    d = len(centered_energy_labels(dimension))
    return d**3 * MEMORY_DIMENSION


def spectator_total_constraint_operator(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Return H_tot^(7A)=H_tot^(5) tensor I_M for H_M=0."""

    return np.kron(total_constraint_operator(dimension, rates=rates), memory_identity())


def spectator_physical_basis(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Return an orthonormal basis for H_phys^(5) tensor H_M."""

    return np.kron(analytic_physical_basis(dimension, rates=rates), memory_identity())


def spectator_physical_projector(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    basis = spectator_physical_basis(dimension, rates=rates)
    return basis @ basis.conj().T


def spectator_physical_dimension(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> int:
    return spectator_physical_basis(dimension, rates=rates).shape[1]


def spectator_constraint_residual(
    state: np.ndarray,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> float:
    vector = np.asarray(state, dtype=np.complex128)
    expected = spectator_kinematic_dimension(dimension)
    if vector.shape != (expected,):
        raise ValueError(f"spectator global state must have shape ({expected},)")
    if not np.all(np.isfinite(vector)):
        raise ValueError("spectator global state amplitudes must be finite")
    return float(np.linalg.norm(spectator_total_constraint_operator(dimension, rates=rates) @ vector))


def spectator_support_basis(
    clock: str,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    return np.kron(clock_relative_support_basis(clock, dimension, rates=rates), memory_identity())


def spectator_support_projector(
    clock: str,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    basis = spectator_support_basis(clock, dimension, rates=rates)
    return basis @ basis.conj().T


def spectator_support_dimension(
    clock: str,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> int:
    return spectator_support_basis(clock, dimension, rates=rates).shape[1]


def spectator_kinematic_clock_projection_operator(
    clock: str,
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    return np.kron(
        kinematic_clock_projection_operator(clock, index, dimension, rates=rates),
        memory_identity(),
    )


def spectator_reduction_operator(
    clock: str,
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    return np.kron(
        physical_clock_reduction_operator(clock, index, dimension, rates=rates),
        memory_identity(),
    )


def spectator_reconstruction_operator(
    clock: str,
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    return np.kron(
        clock_reconstruction_operator(clock, index, dimension, rates=rates),
        memory_identity(),
    )


def spectator_same_clock_transition_operator(
    clock: str,
    target_index: int,
    source_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    return np.kron(
        same_clock_transition_operator(
            clock, target_index, source_index, dimension, rates=rates
        ),
        memory_identity(),
    )


def spectator_clock_change_operator(
    target_clock: str,
    target_index: int,
    source_clock: str,
    source_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    return np.kron(
        genuine_clock_change_operator(
            target_clock,
            target_index,
            source_clock,
            source_index,
            dimension,
            rates=rates,
        ),
        memory_identity(),
    )


def spectator_physical_reduction(
    state: np.ndarray,
    clock: str,
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    atol: float = DEFAULT_ATOL,
) -> np.ndarray:
    vector = np.asarray(state, dtype=np.complex128)
    if spectator_constraint_residual(vector, dimension, rates=rates) > atol:
        raise ValueError("state must satisfy the declared Stage 7A spectator constraint")
    return spectator_reduction_operator(clock, index, dimension, rates=rates) @ vector


def spectator_clock_probability(
    state: np.ndarray,
    clock: str,
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    atol: float = DEFAULT_ATOL,
) -> float:
    vector = np.asarray(state, dtype=np.complex128)
    if spectator_constraint_residual(vector, dimension, rates=rates) > atol:
        raise ValueError("state must satisfy the declared Stage 7A spectator constraint")
    if not np.isclose(np.linalg.norm(vector), 1.0, atol=atol, rtol=0.0):
        raise ValueError("spectator clock probability requires a normalized state")
    conditioned = spectator_kinematic_clock_projection_operator(
        clock, index, dimension, rates=rates
    ) @ vector
    return float(np.vdot(conditioned, conditioned).real)


def canonical_memory_state() -> np.ndarray:
    """Return a nontrivial normalized qubit state independent of all clock data."""

    return np.array(
        [np.sqrt(0.65), np.exp(0.43j) * np.sqrt(0.35)], dtype=np.complex128
    )


def canonical_stage7a_state(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Return a normalized product |Psi_5> tensor |mu> spectator state."""

    physical_dimension = analytic_physical_basis(dimension, rates=rates).shape[1]
    indices = np.arange(1, physical_dimension + 1, dtype=float)
    coefficients = indices + 1j * ((-1.0) ** indices) * (indices + 0.5)
    stage5_state = physical_state_from_coefficients(
        coefficients,
        dimension,
        rates=rates,
        normalize=True,
    )
    return np.kron(stage5_state, canonical_memory_state())


def _canonical_support_projector(
    clock: str,
    dimension: int,
    *,
    rates: Iterable[float],
) -> np.ndarray:
    support = spectator_support_basis(clock, dimension, rates=rates)
    n = support.shape[1]
    indices = np.arange(1, n + 1, dtype=float)
    coefficients = indices + 1j * (n + 1.0 - indices)
    coefficients = coefficients / np.linalg.norm(coefficients)
    vector = support @ coefficients
    return np.outer(vector, vector.conj())


def spectator_clock_change_diagnostics(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> SpectatorClockChangeDiagnostics:
    """Exhaustively test direct-state, Born, and inverse covariance for Stage 7A."""

    d = len(centered_energy_labels(dimension))
    state = canonical_stage7a_state(dimension, rates=rates)
    comparisons = 0
    max_state = 0.0
    max_born = 0.0
    max_inverse = 0.0

    for source_clock in SUBSYSTEMS:
        for target_clock in SUBSYSTEMS:
            if source_clock == target_clock:
                continue
            source_projector = _canonical_support_projector(
                source_clock, dimension, rates=rates
            )
            for source_index in range(d):
                source_state = spectator_physical_reduction(
                    state, source_clock, source_index, dimension, rates=rates
                )
                source_probability = float(
                    np.vdot(source_state, source_projector @ source_state).real
                )
                for target_index in range(d):
                    transform = spectator_clock_change_operator(
                        target_clock,
                        target_index,
                        source_clock,
                        source_index,
                        dimension,
                        rates=rates,
                    )
                    direct_target = spectator_physical_reduction(
                        state, target_clock, target_index, dimension, rates=rates
                    )
                    transformed_target = transform @ source_state
                    max_state = max(
                        max_state, float(np.linalg.norm(transformed_target - direct_target))
                    )

                    target_projector = transform @ source_projector @ transform.conj().T
                    target_probability = float(
                        np.vdot(direct_target, target_projector @ direct_target).real
                    )
                    max_born = max(max_born, abs(source_probability - target_probability))

                    reverse = spectator_clock_change_operator(
                        source_clock,
                        source_index,
                        target_clock,
                        target_index,
                        dimension,
                        rates=rates,
                    )
                    source_support = spectator_support_projector(
                        source_clock, dimension, rates=rates
                    )
                    max_inverse = max(
                        max_inverse,
                        float(np.linalg.norm(reverse @ transform - source_support)),
                    )
                    comparisons += 1

    return SpectatorClockChangeDiagnostics(
        comparisons=comparisons,
        max_state_residual=max_state,
        max_born_residual=max_born,
        max_inverse_residual=max_inverse,
    )


def spectator_composition_diagnostics(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> SpectatorCompositionDiagnostics:
    """Exhaustively test three-clock composition with memory left untouched."""

    d = len(centered_energy_labels(dimension))
    comparisons = 0
    maximum = 0.0
    for source_clock, middle_clock, target_clock in permutations(SUBSYSTEMS, 3):
        for source_index, middle_index, target_index in product(range(d), repeat=3):
            first = spectator_clock_change_operator(
                middle_clock,
                middle_index,
                source_clock,
                source_index,
                dimension,
                rates=rates,
            )
            second = spectator_clock_change_operator(
                target_clock,
                target_index,
                middle_clock,
                middle_index,
                dimension,
                rates=rates,
            )
            direct = spectator_clock_change_operator(
                target_clock,
                target_index,
                source_clock,
                source_index,
                dimension,
                rates=rates,
            )
            maximum = max(maximum, float(np.linalg.norm(second @ first - direct)))
            comparisons += 1
    return SpectatorCompositionDiagnostics(
        comparisons=comparisons,
        max_composition_residual=maximum,
    )


def _classical_mutual_information(joint: np.ndarray) -> float:
    probabilities = np.asarray(joint, dtype=float)
    total = float(np.sum(probabilities))
    if total <= 0.0:
        raise ValueError("joint distribution must have positive total probability")
    probabilities = probabilities / total
    p_target = np.sum(probabilities, axis=1, keepdims=True)
    p_memory = np.sum(probabilities, axis=0, keepdims=True)
    product_distribution = p_target @ p_memory
    mask = probabilities > 0.0
    return float(
        np.sum(
            probabilities[mask]
            * np.log2(probabilities[mask] / product_distribution[mask])
        )
    )


def spectator_no_record_diagnostics(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    atol: float = DEFAULT_ATOL,
) -> SpectatorRecordDiagnostics:
    """Scan explicit rest-energy targets against computational memory readout.

    The canonical state is a product between the Stage 5 physical state and the
    memory qubit, and every Stage 7A perspective map acts as identity on memory.
    Target-memory mutual information should therefore vanish for each of the two
    rest-energy targets in every clock perspective and reading.
    """

    d = len(centered_energy_labels(dimension))
    state = canonical_stage7a_state(dimension, rates=rates)
    comparisons = 0
    maximum = 0.0
    for clock in SUBSYSTEMS:
        for index in range(d):
            reduced = spectator_physical_reduction(
                state, clock, index, dimension, rates=rates, atol=atol
            )
            amplitudes = reduced.reshape(d, d, MEMORY_DIMENSION)
            probabilities = np.abs(amplitudes) ** 2
            for target_position in (0, 1):
                if target_position == 0:
                    joint = np.sum(probabilities, axis=1)
                else:
                    joint = np.sum(probabilities, axis=0)
                information = _classical_mutual_information(joint)
                maximum = max(maximum, abs(information))
                comparisons += 1

    return SpectatorRecordDiagnostics(
        comparisons=comparisons,
        max_target_memory_mutual_information=maximum,
        positive_record_witness=bool(maximum > atol),
        record_coupling_present=False,
    )


def stage7a_summary(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> dict[str, object]:
    clock_change = spectator_clock_change_diagnostics(dimension, rates=rates)
    composition = spectator_composition_diagnostics(dimension, rates=rates)
    record = spectator_no_record_diagnostics(dimension, rates=rates)
    d = len(centered_energy_labels(dimension))
    return {
        "dimension": d,
        "memory_dimension": MEMORY_DIMENSION,
        "kinematic_dimension": spectator_kinematic_dimension(dimension),
        "physical_dimension": spectator_physical_dimension(dimension, rates=rates),
        "support_dimensions": {
            clock: spectator_support_dimension(clock, dimension, rates=rates)
            for clock in SUBSYSTEMS
        },
        "clock_change": asdict(clock_change),
        "composition": asdict(composition),
        "record_control": asdict(record),
        "guards": [
            "memory present != record present",
            "entanglement != record",
            "spectator identity extension != record formation",
        ],
    }
