"""Stage 3D: reversal, symmetric-mixture, and boundary controls.

These controls test whether the Stage 3C record-defined orientation tracks the
record/boundary structure rather than mere ordered positions or irreversible
microscopic dynamics.  Position labels remain neutral bookkeeping labels.
"""

from __future__ import annotations

from fractions import Fraction
from typing import Iterable

from .stage3 import (
    Microstate,
    TrajectoryEnsemble,
    canonical_forward_ensemble,
    forward_trajectory,
    make_trajectory_ensemble,
    reverse_ensemble,
    u_scr,
)
from .stage3_asymmetry import (
    AsymmetricRecordModel,
    RecordOrientationAssessment,
    assess_record_orientation,
)


def u_identity(state: Microstate) -> Microstate:
    """Identity update used as the reversible no-record first interaction."""

    return state


def mix_ensembles(
    weighted_ensembles: Iterable[tuple[TrajectoryEnsemble, Fraction | int]],
) -> TrajectoryEnsemble:
    """Return an exact convex mixture, merging duplicate complete trajectories.

    Mixture weights must be strictly positive and sum exactly to one.  Because
    forward and reversed ensembles can share trajectories, probabilities are
    accumulated before constructing the validated output ensemble.
    """

    materialized = tuple(
        (ensemble, Fraction(weight)) for ensemble, weight in weighted_ensembles
    )
    if not materialized:
        raise ValueError("at least one ensemble is required")
    weights = [weight for _, weight in materialized]
    if any(weight <= 0 for weight in weights):
        raise ValueError("mixture weights must be strictly positive")
    if sum(weights, Fraction(0, 1)) != Fraction(1, 1):
        raise ValueError("mixture weights must sum exactly to one")

    combined: dict[tuple[Microstate, Microstate, Microstate], Fraction] = {}
    for ensemble, mixture_weight in materialized:
        for trajectory, trajectory_weight in ensemble.weighted_trajectories:
            combined[trajectory] = combined.get(trajectory, Fraction(0, 1)) + (
                mixture_weight * trajectory_weight
            )

    return make_trajectory_ensemble(combined.items())


def canonical_reversed_control_ensemble() -> TrajectoryEnsemble:
    """Return the exact modeled-history reversal of the canonical ensemble."""

    return reverse_ensemble(canonical_forward_ensemble())


def symmetric_forward_reverse_ensemble() -> TrajectoryEnsemble:
    """Return ``1/2 mu_fwd + 1/2 J_*mu_fwd`` with duplicate histories merged."""

    forward = canonical_forward_ensemble()
    reversed_ensemble = reverse_ensemble(forward)
    return mix_ensembles(
        (
            (forward, Fraction(1, 2)),
            (reversed_ensemble, Fraction(1, 2)),
        )
    )


def no_record_forward_ensemble() -> TrajectoryEnsemble:
    """Preserve ordered positions and scrambling while omitting record coupling.

    The first update is the reversible identity ``u_identity`` rather than
    ``U_rec``.  The blank register therefore remains independent of the system
    while the second reversible scrambling update is retained.
    """

    quarter = Fraction(1, 4)
    weighted = []
    for a in (0, 1):
        for b in (0, 1):
            z0 = Microstate(a, 0, b)
            z1 = u_identity(z0)
            z2 = u_scr(z1)
            weighted.append(((z0, z1, z2), quarter))
    return make_trajectory_ensemble(weighted)


def uniform_memory_initial_distribution() -> dict[Microstate, Fraction]:
    """Return independent uniform ``X_0,M_0,N_0`` over all eight microstates."""

    eighth = Fraction(1, 8)
    return {
        Microstate(x, m, n): eighth
        for x in (0, 1)
        for m in (0, 1)
        for n in (0, 1)
    }


def uniform_memory_forward_ensemble() -> TrajectoryEnsemble:
    """Use canonical reversible maps with an independent uniform memory boundary."""

    return make_trajectory_ensemble(
        (forward_trajectory(initial), weight)
        for initial, weight in uniform_memory_initial_distribution().items()
    )


def assess_control_ensemble(ensemble: TrajectoryEnsemble) -> RecordOrientationAssessment:
    """Apply the frozen Stage 3C interpretation criterion to one control ensemble."""

    return assess_record_orientation(AsymmetricRecordModel(ensemble=ensemble))


def stage3d_control_assessments() -> dict[str, RecordOrientationAssessment]:
    """Return canonical and required Stage 3D control assessments.

    ``microscopic_maps_reversible`` in the returned Stage 3C assessment refers
    to the canonical ``U_rec/U_scr`` pair.  The no-record control instead uses
    ``u_identity/U_scr``; its reversibility must be checked against those actual
    control maps separately.
    """

    return {
        "forward": assess_control_ensemble(canonical_forward_ensemble()),
        "reversed": assess_control_ensemble(canonical_reversed_control_ensemble()),
        "symmetric": assess_control_ensemble(symmetric_forward_reverse_ensemble()),
        "no-record": assess_control_ensemble(no_record_forward_ensemble()),
        "uniform-memory": assess_control_ensemble(uniform_memory_forward_ensemble()),
    }
