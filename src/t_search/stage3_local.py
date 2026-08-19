"""Stage 3E: explicit record-bearing local views and Stage 2 product integration.

The Stage 3 projection deliberately exposes only the local system/record pair
``(X_k,M_k)`` and a declared record readout/diagnostic interface.  The environment
bit ``N_k``, complete trajectory, opposite-side microstates, and boundary variables
are not silently included.

Stage 2 Potentiality is reintroduced only through typed product adapters.  This is
an explicit product construction between two toy-model layers, not a claim that the
Stage 2 branching substrate and Stage 3 bit dynamics are one physical system.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .stage2 import EventId, Prefix
from .stage2_epistemic import EpistemicLocalView, EpistemicPotentiality
from .stage2_ontic import OnticLocalView, OnticPotentiality
from .stage3 import (
    Microstate,
    Trajectory,
    TrajectoryEnsemble,
    UpdateMap,
    all_microstates,
    canonical_forward_ensemble,
    is_bijective,
    u_rec,
    u_scr,
)
from .stage3_asymmetry import Orientation, assess_record_orientation, AsymmetricRecordModel
from .stage3_diagnostics import accessibility_profile, record_profile


@dataclass(frozen=True)
class Stage3RecordBlock:
    """Explicit block-like Stage 3 object for the record-only experiment.

    ``B_3=(Z_space,U_1,U_2,Omega,mu)`` is represented by the complete state
    space, the two declared microscopic updates, and the exact trajectory
    ensemble.  The global mathematical object is not treated as a physically
    accessible God's-eye observer.
    """

    state_space: tuple[Microstate, ...]
    first_update: UpdateMap
    second_update: UpdateMap
    ensemble: TrajectoryEnsemble

    def __post_init__(self) -> None:
        if set(self.state_space) != set(all_microstates()):
            raise ValueError("state_space must contain exactly the complete eight microstates")
        if not is_bijective(self.first_update) or not is_bijective(self.second_update):
            raise ValueError("Stage 3E block updates must be bijective")
        for trajectory in self.ensemble.trajectories:
            z0, z1, z2 = trajectory
            if z1 != self.first_update(z0) or z2 != self.second_update(z1):
                raise ValueError("trajectory is incompatible with the declared block updates")


@dataclass(frozen=True)
class LocalActuality:
    """Declared locally accessible Stage 3 actuality ``(X_k,M_k)``.

    The environment/ancilla bit ``N_k`` is intentionally omitted so that global
    and local descriptions are not trivially identical.
    """

    x: int
    m: int

    def __post_init__(self) -> None:
        if self.x not in (0, 1) or self.m not in (0, 1):
            raise ValueError("local actuality components must be bits")


@dataclass(frozen=True)
class RecordReadout:
    """Locally declared record/register interface at one neutral position."""

    register_component: Literal["m"]
    register_value: int
    target_component: Literal["x"]
    information_profile: tuple[tuple[int, float], ...]
    accessibility_profile: tuple[tuple[int, float], ...]
    orientation: Orientation | None


@dataclass(frozen=True)
class RecordLocalView:
    """Reduced Stage 3 view ``G_k^rec=(Records_k,Actuality_k)``."""

    position: int
    records: RecordReadout
    actuality: LocalActuality


@dataclass(frozen=True)
class CompositeActuality:
    """Explicit product actuality for Stage 3 record + Stage 2 modal layers."""

    record_position: int
    record_actuality: LocalActuality
    modal_actuality: Prefix


@dataclass(frozen=True)
class EpistemicCompleteLocalView:
    """``G=(Records,Actuality,EPot)`` product view with no hidden ``h*`` field."""

    records: RecordReadout
    actuality: CompositeActuality
    potentiality: EpistemicPotentiality
    next_probabilities: tuple[tuple[EventId, float], ...]


@dataclass(frozen=True)
class OnticCompleteLocalView:
    """``G=(Records,Actuality,OPot)`` product view with no selected future."""

    records: RecordReadout
    actuality: CompositeActuality
    potentiality: OnticPotentiality
    next_probabilities: tuple[tuple[EventId, float], ...]


@dataclass(frozen=True)
class ProjectionInformationClassification:
    """Stage 3E information classification for the declared local interface."""

    locally_accessible: tuple[str, ...]
    globally_hidden: tuple[str, ...]
    ambiguous_from_single_view: tuple[str, ...]
    reconstructible_from_view_family: tuple[str, ...]
    lost_without_weighted_global_structure: tuple[str, ...]


def canonical_record_block() -> Stage3RecordBlock:
    """Return the protocol-frozen forward block-like record object."""

    return Stage3RecordBlock(
        state_space=all_microstates(),
        first_update=u_rec,
        second_update=u_scr,
        ensemble=canonical_forward_ensemble(),
    )


def _validate_position(position: int) -> None:
    if position not in (0, 1, 2):
        raise ValueError("position must be one of 0, 1, 2")


def _validate_member(block: Stage3RecordBlock, trajectory: Trajectory) -> None:
    if trajectory not in block.ensemble.trajectories:
        raise ValueError("trajectory must belong to the declared block ensemble")


def _orientation_at_position(
    block: Stage3RecordBlock,
    position: int,
) -> Orientation | None:
    """Return the Stage 3C orientation only where a two-sided window exists."""

    if position != 1:
        return None
    assessment = assess_record_orientation(
        AsymmetricRecordModel(ensemble=block.ensemble, current_position=1, delta=1)
    )
    return assessment.orientation


def project_record_view(
    block: Stage3RecordBlock,
    trajectory: Trajectory,
    *,
    position: int = 1,
) -> RecordLocalView:
    """Project one global trajectory instance to the declared local record view.

    The projection exposes only ``X_k`` and ``M_k`` from the actual microstate.
    Ensemble-level record/accessibility profiles are included because the Stage 3
    experiment interface explicitly grants those diagnostics.  The actual ``N_k``
    and opposite-side microstates remain outside the returned object.
    """

    _validate_position(position)
    _validate_member(block, trajectory)
    state = trajectory[position]
    info = record_profile(block.ensemble, current_position=position)
    access = accessibility_profile(block.ensemble, current_position=position)

    return RecordLocalView(
        position=position,
        records=RecordReadout(
            register_component="m",
            register_value=state.m,
            target_component="x",
            information_profile=tuple(sorted(info.items())),
            accessibility_profile=tuple(sorted(access.items())),
            orientation=_orientation_at_position(block, position),
        ),
        actuality=LocalActuality(x=state.x, m=state.m),
    )


def compatible_global_histories(
    block: Stage3RecordBlock,
    views: tuple[RecordLocalView, ...],
) -> tuple[Trajectory, ...]:
    """Return complete trajectories compatible with all supplied local views.

    Compatibility is based on the declared local Actuality/readout interface, not
    on hidden global fields.  A single canonical central view remains ambiguous
    because the environment bit is omitted; a suitable family of views can remove
    that ambiguity.
    """

    if not views:
        raise ValueError("at least one local view is required")
    positions = [view.position for view in views]
    if len(set(positions)) != len(positions):
        raise ValueError("local view positions must be unique")

    for view in views:
        _validate_position(view.position)
        if view.records.register_value != view.actuality.m:
            raise ValueError("record readout must agree with local actuality")

    compatible: list[Trajectory] = []
    for trajectory in block.ensemble.trajectories:
        matches = True
        for view in views:
            state = trajectory[view.position]
            if state.x != view.actuality.x or state.m != view.actuality.m:
                matches = False
                break
        if matches:
            compatible.append(trajectory)
    return tuple(compatible)


def reconstruct_global_history(
    block: Stage3RecordBlock,
    views: tuple[RecordLocalView, ...],
) -> Trajectory:
    """Return the unique compatible trajectory or reject ambiguity/loss."""

    compatible = compatible_global_histories(block, views)
    if not compatible:
        raise ValueError("local views are incompatible with every global trajectory")
    if len(compatible) != 1:
        raise ValueError("local views do not uniquely reconstruct a global trajectory")
    return compatible[0]


def combine_with_epistemic_potentiality(
    record_view: RecordLocalView,
    modal_view: EpistemicLocalView,
) -> EpistemicCompleteLocalView:
    """Attach the record layer to an already-projected epistemic Stage 2 view."""

    return EpistemicCompleteLocalView(
        records=record_view.records,
        actuality=CompositeActuality(
            record_position=record_view.position,
            record_actuality=record_view.actuality,
            modal_actuality=modal_view.actuality,
        ),
        potentiality=modal_view.potentiality,
        next_probabilities=modal_view.next_probabilities,
    )


def combine_with_ontic_potentiality(
    record_view: RecordLocalView,
    modal_view: OnticLocalView,
) -> OnticCompleteLocalView:
    """Attach the same record layer to an already-projected ontic Stage 2 view."""

    return OnticCompleteLocalView(
        records=record_view.records,
        actuality=CompositeActuality(
            record_position=record_view.position,
            record_actuality=record_view.actuality,
            modal_actuality=modal_view.actuality,
        ),
        potentiality=modal_view.potentiality,
        next_probabilities=modal_view.next_probabilities,
    )


def canonical_projection_classification() -> ProjectionInformationClassification:
    """Return the Stage 3E classification for the canonical ``(X,M)`` interface."""

    return ProjectionInformationClassification(
        locally_accessible=(
            "current neutral position",
            "current X_k value",
            "current M_k record-register value",
            "declared ensemble-level record/accessibility diagnostics",
        ),
        globally_hidden=(
            "current N_k environment bit",
            "actual opposite-side microstates",
            "complete actual trajectory",
            "initial boundary variables as privileged labels",
        ),
        ambiguous_from_single_view=(
            "complete actual trajectory",
            "current N_k environment bit",
            "opposite-side actual microstates",
        ),
        reconstructible_from_view_family=(
            "complete actual trajectory from compatible multi-position local views",
            "hidden N value when changes in X across positions are jointly available",
        ),
        lost_without_weighted_global_structure=(
            "full probability weights over complete trajectories",
            "global trajectory correlations not encoded by one unweighted local instance",
        ),
    )
