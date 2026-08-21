"""Stage 7B reversible target-specific quantum record witness.

This module deliberately implements a *support-local* reversible record write
before Stage 7C attempts an internally anchored relational history.  The
construction therefore establishes a target-specific correlation witness and a
physical-subspace automorphism, not time-localized record formation or a
record-defined temporal orientation.

Canonical qutrit witness (A-clock perspective):

* target Q: first rest subsystem B has energy label -1;
* wrong target W: second rest subsystem C has energy label +1;
* memory readout: computational Z_M basis;
* record write: controlled X_M on Q.

The canonical source state has equal weight on four support pairs chosen so
that Q and W are independent.  Hence a successful record write gives
I(Q;M)=1 bit while I(W;M)=0, whereas the identity/no-record control leaves
I(Q;M)=0.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

import numpy as np

from .stage5_clock_change import DEFAULT_ATOL, DEFAULT_DIMENSION, DEFAULT_RATES, centered_energy_labels
from .stage5_reductions import clock_relative_support_pairs, rest_subsystems
from .stage7_spectator import (
    MEMORY_DIMENSION,
    memory_identity,
    spectator_constraint_residual,
    spectator_physical_basis,
    spectator_physical_projector,
    spectator_reconstruction_operator,
    spectator_reduction_operator,
    spectator_support_basis,
    spectator_support_projector,
)

CANONICAL_CLOCK = "A"
CANONICAL_CLOCK_INDEX = 0
TARGET_POSITION = 0
TARGET_LABEL = -1
WRONG_TARGET_POSITION = 1
WRONG_TARGET_LABEL = 1


@dataclass(frozen=True)
class Stage7BRecordDiagnostics:
    target_name: str
    wrong_target_name: str
    memory_readout: str
    target_information_before: float
    target_information_after: float
    target_information_no_record: float
    target_information_gain: float
    wrong_target_information_after: float
    support_unitarity_residual: float
    ambient_unitarity_residual: float
    inverse_recovery_residual: float
    physical_automorphism_residual: float
    physical_constraint_residual: float
    positive_target_specific_record_witness: bool
    directional_score_defined: bool


def memory_pauli_z() -> np.ndarray:
    """Return the explicit computational memory readout observable Z_M."""

    return np.diag([1.0, -1.0]).astype(np.complex128)


def _validate_canonical_qutrit(dimension: int, clock: str) -> None:
    d = len(centered_energy_labels(dimension))
    if d != 3 or clock != CANONICAL_CLOCK:
        raise ValueError("canonical Stage 7B witness is declared only for qutrit clock A")
    if rest_subsystems(clock) != ("B", "C"):
        raise RuntimeError("canonical A-clock rest ordering changed unexpectedly")


def _pair_predicate_projector(
    clock: str,
    position: int,
    label: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    pairs = clock_relative_support_pairs(clock, dimension, rates=rates)
    if position not in (0, 1):
        raise ValueError("target position must be 0 or 1 in the rest-pair ordering")
    flags = np.array([1.0 if pair[position] == label else 0.0 for pair in pairs])
    if not np.any(flags) or np.all(flags):
        raise ValueError("target predicate must define a nontrivial binary partition")
    return np.diag(flags).astype(np.complex128)


def canonical_target_pair_projector(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    _validate_canonical_qutrit(dimension, CANONICAL_CLOCK)
    return _pair_predicate_projector(
        CANONICAL_CLOCK, TARGET_POSITION, TARGET_LABEL, dimension, rates=rates
    )


def canonical_wrong_target_pair_projector(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    _validate_canonical_qutrit(dimension, CANONICAL_CLOCK)
    return _pair_predicate_projector(
        CANONICAL_CLOCK,
        WRONG_TARGET_POSITION,
        WRONG_TARGET_LABEL,
        dimension,
        rates=rates,
    )


def controlled_record_write_support_matrix(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Return U_rec=Q⊗X_M+(I-Q)⊗I_M on K_A⊗H_M coordinates."""

    q = canonical_target_pair_projector(dimension, rates=rates)
    identity_pairs = np.eye(q.shape[0], dtype=np.complex128)
    x_memory = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128)
    return np.kron(q, x_memory) + np.kron(identity_pairs - q, memory_identity())


def no_record_support_matrix(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    q = canonical_target_pair_projector(dimension, rates=rates)
    return np.eye(q.shape[0] * MEMORY_DIMENSION, dtype=np.complex128)


def controlled_record_write_ambient_operator(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Extend the support unitary by identity on the orthogonal ambient complement."""

    support = spectator_support_basis(CANONICAL_CLOCK, dimension, rates=rates)
    projector = spectator_support_projector(CANONICAL_CLOCK, dimension, rates=rates)
    u_support = controlled_record_write_support_matrix(dimension, rates=rates)
    identity = np.eye(projector.shape[0], dtype=np.complex128)
    return support @ u_support @ support.conj().T + (identity - projector)


def canonical_record_source_support_coordinates(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Equal superposition with Q and wrong-target W independently balanced."""

    _validate_canonical_qutrit(dimension, CANONICAL_CLOCK)
    pairs = clock_relative_support_pairs(CANONICAL_CLOCK, dimension, rates=rates)
    required = ((-1, 0), (-1, 1), (0, 0), (0, 1))
    indices = []
    for pair in required:
        if pair not in pairs:
            raise RuntimeError(f"required canonical support pair missing: {pair}")
        indices.append(pairs.index(pair))

    coordinates = np.zeros((len(pairs), MEMORY_DIMENSION), dtype=np.complex128)
    amplitude = 1.0 / np.sqrt(len(required))
    for index in indices:
        coordinates[index, 0] = amplitude
    return coordinates.reshape(-1)


def canonical_record_source_state(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    support = spectator_support_basis(CANONICAL_CLOCK, dimension, rates=rates)
    return support @ canonical_record_source_support_coordinates(dimension, rates=rates)


def apply_record_write(
    state: np.ndarray,
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    vector = np.asarray(state, dtype=np.complex128)
    support_projector = spectator_support_projector(CANONICAL_CLOCK, dimension, rates=rates)
    if vector.shape != (support_projector.shape[0],):
        raise ValueError("reduced record state has the wrong ambient shape")
    if np.linalg.norm((np.eye(vector.size) - support_projector) @ vector) > DEFAULT_ATOL:
        raise ValueError("record source state must lie in the declared A-clock support")
    return controlled_record_write_ambient_operator(dimension, rates=rates) @ vector


def _classical_mutual_information(joint: np.ndarray) -> float:
    probabilities = np.asarray(joint, dtype=float)
    total = float(np.sum(probabilities))
    if total <= 0.0:
        raise ValueError("joint distribution must have positive total probability")
    probabilities = probabilities / total
    px = np.sum(probabilities, axis=1, keepdims=True)
    pm = np.sum(probabilities, axis=0, keepdims=True)
    independent = px @ pm
    mask = probabilities > 0.0
    return float(np.sum(probabilities[mask] * np.log2(probabilities[mask] / independent[mask])))


def target_memory_joint_distribution(
    state: np.ndarray,
    *,
    position: int,
    label: int,
    dimension: int = DEFAULT_DIMENSION,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Return p(binary target bit, computational memory bit) on K_A⊗H_M."""

    support = spectator_support_basis(CANONICAL_CLOCK, dimension, rates=rates)
    vector = np.asarray(state, dtype=np.complex128)
    if vector.shape != (support.shape[0],):
        raise ValueError("reduced record state has the wrong ambient shape")
    coordinates = support.conj().T @ vector
    probabilities = np.abs(coordinates.reshape(-1, MEMORY_DIMENSION)) ** 2
    pairs = clock_relative_support_pairs(CANONICAL_CLOCK, dimension, rates=rates)
    joint = np.zeros((2, MEMORY_DIMENSION), dtype=float)
    for pair_index, pair in enumerate(pairs):
        target_bit = int(pair[position] == label)
        joint[target_bit, :] += probabilities[pair_index, :]
    return joint / np.sum(joint)


def target_memory_mutual_information(
    state: np.ndarray,
    *,
    position: int = TARGET_POSITION,
    label: int = TARGET_LABEL,
    dimension: int = DEFAULT_DIMENSION,
    rates: Iterable[float] = DEFAULT_RATES,
) -> float:
    joint = target_memory_joint_distribution(
        state, position=position, label=label, dimension=dimension, rates=rates
    )
    return _classical_mutual_information(joint)


def physical_record_automorphism_operator(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> np.ndarray:
    """Lift the support-local record write to an automorphism of H_phys^(7A)."""

    reduction = spectator_reduction_operator(
        CANONICAL_CLOCK, CANONICAL_CLOCK_INDEX, dimension, rates=rates
    )
    reconstruction = spectator_reconstruction_operator(
        CANONICAL_CLOCK, CANONICAL_CLOCK_INDEX, dimension, rates=rates
    )
    projector = spectator_physical_projector(dimension, rates=rates)
    ambient_write = controlled_record_write_ambient_operator(dimension, rates=rates)
    return projector @ reconstruction @ ambient_write @ reduction @ projector


def stage7b_record_diagnostics(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
    atol: float = DEFAULT_ATOL,
) -> Stage7BRecordDiagnostics:
    initial = canonical_record_source_state(dimension, rates=rates)
    write = controlled_record_write_ambient_operator(dimension, rates=rates)
    recorded = write @ initial
    no_recorded = initial.copy()
    recovered = write @ recorded

    before = target_memory_mutual_information(initial, dimension=dimension, rates=rates)
    after = target_memory_mutual_information(recorded, dimension=dimension, rates=rates)
    no_record = target_memory_mutual_information(no_recorded, dimension=dimension, rates=rates)
    wrong_after = target_memory_mutual_information(
        recorded,
        position=WRONG_TARGET_POSITION,
        label=WRONG_TARGET_LABEL,
        dimension=dimension,
        rates=rates,
    )

    u_support = controlled_record_write_support_matrix(dimension, rates=rates)
    support_unitarity = float(
        np.linalg.norm(u_support.conj().T @ u_support - np.eye(u_support.shape[0]))
    )
    ambient_unitarity = float(np.linalg.norm(write.conj().T @ write - np.eye(write.shape[0])))

    physical_basis = spectator_physical_basis(dimension, rates=rates)
    physical_write = physical_record_automorphism_operator(dimension, rates=rates)
    physical_coordinates = physical_basis.conj().T @ physical_write @ physical_basis
    physical_automorphism = float(
        np.linalg.norm(
            physical_coordinates.conj().T @ physical_coordinates
            - np.eye(physical_coordinates.shape[0])
        )
    )

    reconstruction = spectator_reconstruction_operator(
        CANONICAL_CLOCK, CANONICAL_CLOCK_INDEX, dimension, rates=rates
    )
    physical_initial = reconstruction @ initial
    physical_recorded = physical_write @ physical_initial
    constraint = spectator_constraint_residual(physical_recorded, dimension, rates=rates)
    reduced_recorded = spectator_reduction_operator(
        CANONICAL_CLOCK, CANONICAL_CLOCK_INDEX, dimension, rates=rates
    ) @ physical_recorded
    lift_reduce_residual = float(np.linalg.norm(reduced_recorded - recorded))
    physical_automorphism = max(physical_automorphism, lift_reduce_residual)

    gain = after - before
    positive = bool(
        before <= atol
        and no_record <= atol
        and after > atol
        and wrong_after <= atol
        and support_unitarity <= atol
        and ambient_unitarity <= atol
        and physical_automorphism <= atol
        and constraint <= atol
    )

    return Stage7BRecordDiagnostics(
        target_name="Q: B energy label == -1 in A-clock rest support",
        wrong_target_name="W: C energy label == +1 in A-clock rest support",
        memory_readout="computational Z_M",
        target_information_before=before,
        target_information_after=after,
        target_information_no_record=no_record,
        target_information_gain=gain,
        wrong_target_information_after=wrong_after,
        support_unitarity_residual=support_unitarity,
        ambient_unitarity_residual=ambient_unitarity,
        inverse_recovery_residual=float(np.linalg.norm(recovered - initial)),
        physical_automorphism_residual=physical_automorphism,
        physical_constraint_residual=constraint,
        positive_target_specific_record_witness=positive,
        directional_score_defined=False,
    )


def stage7b_summary(
    dimension: int = DEFAULT_DIMENSION,
    *,
    rates: Iterable[float] = DEFAULT_RATES,
) -> dict[str, object]:
    diagnostics = stage7b_record_diagnostics(dimension, rates=rates)
    return {
        "clock": CANONICAL_CLOCK,
        "clock_index": CANONICAL_CLOCK_INDEX,
        "record": asdict(diagnostics),
        "guards": [
            "target-specific correlation != record-defined temporal orientation",
            "support-local reversible write != time-localized dynamical interaction",
            "physical-subspace automorphism != time-localized interaction",
            "mutual information != directional record by itself",
        ],
    }
