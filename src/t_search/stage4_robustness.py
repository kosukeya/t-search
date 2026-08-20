"""Cross-checks and robustness helpers for Stage 4G.

Stage 4G does not add a new quantum mechanism.  It reuses the Stage 4A--F
construction to test whether the surviving relations remain stable under
bookkeeping relabeling, global phase, coefficient-family changes, clock-origin
changes, and modest finite-dimension changes.

The helpers in this module deliberately distinguish covariance of a chosen
representation from a change of the physical clock subsystem.  The latter is
reserved for Stage 5.
"""

from __future__ import annotations

from dataclasses import dataclass
from numbers import Integral, Real

import numpy as np

from .stage4_conditional import clock_probability_profile, physical_reduction
from .stage4_controls import (
    born_consistency_residual,
    density_matrix,
    plus01_projector,
    ray_fidelity,
)
from .stage4_quantum import (
    DEFAULT_ATOL,
    DEFAULT_DIMENSION,
    constraint_residual,
    is_physical_state,
)
from .stage4_reduction import physical_roundtrip_residual
from .stage4_transition import (
    relational_transition_matrix,
    transition_composition_residual,
    transition_expected_residual,
)


def _validate_dimension(dimension: int) -> int:
    if isinstance(dimension, bool) or not isinstance(dimension, Integral):
        raise ValueError("dimension must be an integer")
    d = int(dimension)
    if d < 2:
        raise ValueError("dimension must be at least two")
    return d


def _validate_phase(phase: float) -> float:
    if isinstance(phase, bool) or not isinstance(phase, Real):
        raise ValueError("phase must be a finite real number")
    value = float(phase)
    if not np.isfinite(value):
        raise ValueError("phase must be a finite real number")
    return value


def _validate_global_state(state: np.ndarray, dimension: int) -> np.ndarray:
    d = _validate_dimension(dimension)
    vector = np.asarray(state, dtype=np.complex128)
    if vector.shape != (d * d,):
        raise ValueError(f"global state must have shape ({d * d},)")
    if not np.all(np.isfinite(vector)):
        raise ValueError("global state amplitudes must be finite")
    return vector


@dataclass(frozen=True)
class ClockLabeling:
    """Pure bookkeeping labels attached bijectively to neutral clock indices."""

    labels: tuple[str, ...]

    def __post_init__(self) -> None:
        if len(self.labels) < 2:
            raise ValueError("at least two clock labels are required")
        if any(not isinstance(label, str) or not label for label in self.labels):
            raise ValueError("clock labels must be nonempty strings")
        if len(set(self.labels)) != len(self.labels):
            raise ValueError("clock labels must be unique")

    @property
    def dimension(self) -> int:
        return len(self.labels)

    def index_of(self, label: str) -> int:
        try:
            return self.labels.index(label)
        except ValueError as exc:
            raise ValueError(f"unknown clock label: {label!r}") from exc


def relabeled_transition_matrix(
    labeling: ClockLabeling,
    source_label: str,
    target_label: str,
    *,
    origin: float = 0.0,
) -> np.ndarray:
    """Return the native transition after a pure rename of clock indices."""

    source = labeling.index_of(source_label)
    target = labeling.index_of(target_label)
    return relational_transition_matrix(
        source, target, labeling.dimension, origin=origin
    )


def relabeled_composition_residual(
    labeling: ClockLabeling,
    source_label: str,
    middle_label: str,
    target_label: str,
    *,
    origin: float = 0.0,
) -> float:
    """Check composition using renamed bookkeeping labels only."""

    source = labeling.index_of(source_label)
    middle = labeling.index_of(middle_label)
    target = labeling.index_of(target_label)
    return transition_composition_residual(
        source, middle, target, labeling.dimension, origin=origin
    )


def global_phase_shift(
    state: np.ndarray,
    phase: float,
    dimension: int = DEFAULT_DIMENSION,
) -> np.ndarray:
    """Multiply one global vector by a physically irrelevant common phase."""

    d = _validate_dimension(dimension)
    vector = _validate_global_state(state, d)
    theta = _validate_phase(phase)
    return np.exp(1j * theta) * vector


def global_phase_local_density_residual(
    state: np.ndarray,
    clock_index: int,
    phase: float,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
    atol: float = DEFAULT_ATOL,
) -> float:
    """Compare local density matrices before/after one global phase shift."""

    d = _validate_dimension(dimension)
    vector = _validate_global_state(state, d)
    shifted = global_phase_shift(vector, phase, d)
    psi = physical_reduction(vector, clock_index, d, origin=origin, atol=atol)
    psi_shifted = physical_reduction(
        shifted, clock_index, d, origin=origin, atol=atol
    )
    return float(np.linalg.norm(density_matrix(psi, d) - density_matrix(psi_shifted, d)))


def ray_change_deficit_profile(
    state: np.ndarray,
    dimension: int = DEFAULT_DIMENSION,
    *,
    reference_index: int = 0,
    origin: float = 0.0,
    atol: float = DEFAULT_ATOL,
) -> np.ndarray:
    """Return 1-fidelity relative to one reference clock reading."""

    d = _validate_dimension(dimension)
    vector = _validate_global_state(state, d)
    if not is_physical_state(vector, d, atol=atol):
        raise ValueError("state must satisfy the Stage 4 zero-constraint condition")
    if not 0 <= reference_index < d:
        raise ValueError(f"reference index must be between 0 and {d - 1}")
    reference = physical_reduction(
        vector, reference_index, d, origin=origin, atol=atol
    )
    deficits = []
    for j in range(d):
        local = physical_reduction(vector, j, d, origin=origin, atol=atol)
        deficits.append(1.0 - ray_fidelity(reference, local, d))
    return np.asarray(deficits, dtype=float)


@dataclass(frozen=True)
class Stage4RobustnessSummary:
    """Maximum residuals for one physical state under the declared interface."""

    dimension: int
    origin: float
    constraint_residual: float
    max_clock_probability_residual: float
    max_roundtrip_residual: float
    max_transition_expected_residual: float
    max_transition_composition_residual: float
    max_born_consistency_residual: float

    @property
    def max_structural_residual(self) -> float:
        return max(
            self.constraint_residual,
            self.max_clock_probability_residual,
            self.max_roundtrip_residual,
            self.max_transition_expected_residual,
            self.max_transition_composition_residual,
            self.max_born_consistency_residual,
        )


def summarize_physical_state_robustness(
    state: np.ndarray,
    dimension: int = DEFAULT_DIMENSION,
    *,
    origin: float = 0.0,
    atol: float = DEFAULT_ATOL,
) -> Stage4RobustnessSummary:
    """Run the principal Stage 4 identities as one cross-check suite."""

    d = _validate_dimension(dimension)
    vector = _validate_global_state(state, d)
    if not is_physical_state(vector, d, atol=atol):
        raise ValueError("state must satisfy the Stage 4 zero-constraint condition")

    probability_profile = clock_probability_profile(vector, d, origin=origin)
    target_probability = 1.0 / d
    probability_residual = float(
        np.max(np.abs(probability_profile - target_probability))
    )

    roundtrip_residual = max(
        physical_roundtrip_residual(vector, j, d, origin=origin, atol=atol)
        for j in range(d)
    )

    transition_expected = max(
        transition_expected_residual(source, target, d, origin=origin)
        for source in range(d)
        for target in range(d)
    )

    transition_composition = max(
        transition_composition_residual(source, middle, target, d, origin=origin)
        for source in range(d)
        for middle in range(d)
        for target in range(d)
    )

    projector = plus01_projector(d)
    born_residual = max(
        born_consistency_residual(
            vector, j, projector, d, origin=origin, atol=atol
        )
        for j in range(d)
    )

    return Stage4RobustnessSummary(
        dimension=d,
        origin=float(origin),
        constraint_residual=constraint_residual(vector, d),
        max_clock_probability_residual=probability_residual,
        max_roundtrip_residual=float(roundtrip_residual),
        max_transition_expected_residual=float(transition_expected),
        max_transition_composition_residual=float(transition_composition),
        max_born_consistency_residual=float(born_residual),
    )
