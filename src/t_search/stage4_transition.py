"""Clock-relative transition structure for Stage 4E.

Stage 4E composes the Stage 4D physical reduction/reconstruction maps into
local-to-local transformations

    T_{k<-j} = R_k E_j.

For the ideal matched-energy Page--Wootters-style model these transitions are
unitary and equal to exp[-i H_S (t_k-t_j)].  The module deliberately describes
this as a clock-relative transition structure, not as a fundamental invariant
of time.
"""

from __future__ import annotations

from numbers import Integral

import numpy as np

from .stage4_conditional import physical_reduction, system_evolution_unitary
from .stage4_quantum import DEFAULT_ATOL, DEFAULT_DIMENSION, clock_reading_times
from .stage4_reduction import kinematic_projection_matrix, reconstruction_matrix


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


def _validate_system_state(state: np.ndarray, dimension: int) -> np.ndarray:
    d = _validate_dimension(dimension)
    vector = np.asarray(state, dtype=np.complex128)
    if vector.shape != (d,):
        raise ValueError(f"system state must have shape ({d},)")
    if not np.all(np.isfinite(vector)):
        raise ValueError("system state amplitudes must be finite")
    return vector


def relational_transition_matrix(
    source_index: int,
    target_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
) -> np.ndarray:
    """Return T_{target<-source}=R_target E_source on H_S.

    The implementation composes the full embedded reconstruction E_source with
    the normalized physical clock projection R_target.  This keeps the
    construction tied explicitly to the global/clock-relative maps rather than
    assuming the Schrödinger propagator in advance.
    """

    d = _validate_dimension(dimension)
    source = _validate_clock_index(source_index, d)
    target = _validate_clock_index(target_index, d)
    return (
        np.sqrt(d)
        * kinematic_projection_matrix(target, d, origin=origin)
        @ reconstruction_matrix(source, d, origin=origin)
    )


def expected_system_transition_matrix(
    source_index: int,
    target_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
) -> np.ndarray:
    """Return exp[-i H_S (t_target-t_source)] independently of R/E maps."""

    d = _validate_dimension(dimension)
    source = _validate_clock_index(source_index, d)
    target = _validate_clock_index(target_index, d)
    times = clock_reading_times(d, origin=origin)
    return system_evolution_unitary(times[target] - times[source], d)


def transition_expected_residual(
    source_index: int,
    target_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
) -> float:
    """Return ||T_{target<-source}-exp[-i H_S Delta t]||_F."""

    actual = relational_transition_matrix(
        source_index, target_index, dimension, origin=origin
    )
    expected = expected_system_transition_matrix(
        source_index, target_index, dimension, origin=origin
    )
    return float(np.linalg.norm(actual - expected))


def transition_identity_residual(
    index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
) -> float:
    """Return ||T_{j<-j}-I||_F."""

    d = _validate_dimension(dimension)
    j = _validate_clock_index(index, d)
    transition = relational_transition_matrix(j, j, d, origin=origin)
    return float(np.linalg.norm(transition - np.eye(d, dtype=np.complex128)))


def transition_inverse_residual(
    source_index: int,
    target_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
) -> float:
    """Return ||T_{source<-target} T_{target<-source}-I||_F."""

    d = _validate_dimension(dimension)
    source = _validate_clock_index(source_index, d)
    target = _validate_clock_index(target_index, d)
    forward = relational_transition_matrix(source, target, d, origin=origin)
    backward = relational_transition_matrix(target, source, d, origin=origin)
    return float(
        np.linalg.norm(backward @ forward - np.eye(d, dtype=np.complex128))
    )


def transition_composition_residual(
    source_index: int,
    middle_index: int,
    target_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
) -> float:
    """Return ||T_{target<-middle} T_{middle<-source}-T_{target<-source}||_F."""

    d = _validate_dimension(dimension)
    source = _validate_clock_index(source_index, d)
    middle = _validate_clock_index(middle_index, d)
    target = _validate_clock_index(target_index, d)
    first = relational_transition_matrix(source, middle, d, origin=origin)
    second = relational_transition_matrix(middle, target, d, origin=origin)
    direct = relational_transition_matrix(source, target, d, origin=origin)
    return float(np.linalg.norm(second @ first - direct))


def transition_unitarity_residual(
    source_index: int,
    target_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
) -> float:
    """Return ||T^dagger T-I||_F."""

    d = _validate_dimension(dimension)
    transition = relational_transition_matrix(
        source_index, target_index, d, origin=origin
    )
    return float(
        np.linalg.norm(
            transition.conj().T @ transition - np.eye(d, dtype=np.complex128)
        )
    )


def propagate_relative_state(
    state: np.ndarray,
    source_index: int,
    target_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
) -> np.ndarray:
    """Apply T_{target<-source} to one clock-relative system vector."""

    d = _validate_dimension(dimension)
    vector = _validate_system_state(state, d)
    return relational_transition_matrix(
        source_index, target_index, d, origin=origin
    ) @ vector


def physical_reduction_transition_residual(
    global_state: np.ndarray,
    source_index: int,
    target_index: int,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
    atol: float = DEFAULT_ATOL,
) -> float:
    """Compare T_{target<-source} R_source|Psi> with R_target|Psi>."""

    d = _validate_dimension(dimension)
    source = _validate_clock_index(source_index, d)
    target = _validate_clock_index(target_index, d)
    psi_source = physical_reduction(
        global_state, source, d, origin=origin, atol=atol
    )
    psi_target = physical_reduction(
        global_state, target, d, origin=origin, atol=atol
    )
    propagated = propagate_relative_state(
        psi_source, source, target, d, origin=origin
    )
    return float(np.linalg.norm(propagated - psi_target))


def origin_covariance_residual(
    source_index: int,
    target_index: int,
    shifted_origin: float,
    dimension: int = DEFAULT_DIMENSION,
    *,
    reference_origin: float = 0.0,
) -> float:
    """Return ||T^(shifted)_{target<-source}-T^(reference)_{target<-source}||_F."""

    d = _validate_dimension(dimension)
    reference = relational_transition_matrix(
        source_index, target_index, d, origin=reference_origin
    )
    shifted = relational_transition_matrix(
        source_index, target_index, d, origin=shifted_origin
    )
    return float(np.linalg.norm(shifted - reference))
