"""Stage 3C: assess record-defined orientation in the canonical ensemble.

Stage 3B already defines the measurement machinery.  This module adds only a
conservative interpretation layer: a record-defined orientation is recognized
when the mutual-information and decoder-accessibility contrasts are both
non-zero and select the same neutral side.  Position indices remain bookkeeping
labels; no side is called physical past or future here.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from .stage3 import (
    TrajectoryEnsemble,
    canonical_forward_ensemble,
    is_bijective,
    u_rec,
    u_scr,
)
from .stage3_diagnostics import (
    accessibility_arrow_score,
    accessibility_profile,
    record_arrow_score,
    record_profile,
)

Orientation = Literal["lower-index", "upper-index", "none"]


@dataclass(frozen=True)
class AsymmetricRecordModel:
    """Record-only Stage 3C model with a neutral current-position interface."""

    ensemble: TrajectoryEnsemble
    current_position: int = 1
    delta: int = 1
    record_component: str = "m"
    target_component: str = "x"


@dataclass(frozen=True)
class RecordOrientationAssessment:
    """Diagnostic evidence for a record-defined orientation.

    ``orientation`` uses only neutral index language.  ``record_defined`` is a
    statement about this declared ensemble and interface, not a claim about a
    fundamental physical arrow of time.
    """

    current_position: int
    delta: int
    lower_position: int
    upper_position: int
    lower_information: float
    upper_information: float
    lower_accuracy: float
    upper_accuracy: float
    record_score: float
    accessibility_score: float
    diagnostics_agree: bool
    orientation: Orientation
    record_defined: bool
    microscopic_maps_reversible: bool


def orientation_from_scores(
    record_score: float,
    accessibility_score: float,
    *,
    tolerance: float = 1e-12,
) -> Orientation:
    """Return the neutral side selected consistently by two signed diagnostics.

    A zero score or disagreement between the two diagnostics returns ``none``.
    This deliberately avoids allowing one diagnostic alone to define the Stage
    3C interpretation.
    """

    if tolerance < 0:
        raise ValueError("tolerance must be non-negative")

    record_zero = abs(record_score) <= tolerance
    accessibility_zero = abs(accessibility_score) <= tolerance
    if record_zero or accessibility_zero:
        return "none"

    if record_score > 0 and accessibility_score > 0:
        return "lower-index"
    if record_score < 0 and accessibility_score < 0:
        return "upper-index"
    return "none"


def assess_record_orientation(
    model: AsymmetricRecordModel,
    *,
    tolerance: float = 1e-12,
) -> RecordOrientationAssessment:
    """Assess whether the declared ensemble supports a record-defined orientation."""

    profile = record_profile(
        model.ensemble,
        current_position=model.current_position,
        record_component=model.record_component,
        target_component=model.target_component,
    )
    access = accessibility_profile(
        model.ensemble,
        current_position=model.current_position,
        record_component=model.record_component,
        target_component=model.target_component,
    )
    record_score = record_arrow_score(
        model.ensemble,
        current_position=model.current_position,
        delta=model.delta,
        record_component=model.record_component,
        target_component=model.target_component,
    )
    accessibility_score = accessibility_arrow_score(
        model.ensemble,
        current_position=model.current_position,
        delta=model.delta,
        record_component=model.record_component,
        target_component=model.target_component,
    )

    lower = model.current_position - model.delta
    upper = model.current_position + model.delta
    orientation = orientation_from_scores(
        record_score,
        accessibility_score,
        tolerance=tolerance,
    )
    diagnostics_agree = orientation != "none"

    if orientation == "lower-index":
        selected_information = profile[lower]
    elif orientation == "upper-index":
        selected_information = profile[upper]
    else:
        selected_information = 0.0

    record_defined = diagnostics_agree and selected_information > tolerance
    reversible = is_bijective(u_rec) and is_bijective(u_scr)

    return RecordOrientationAssessment(
        current_position=model.current_position,
        delta=model.delta,
        lower_position=lower,
        upper_position=upper,
        lower_information=profile[lower],
        upper_information=profile[upper],
        lower_accuracy=access[lower],
        upper_accuracy=access[upper],
        record_score=record_score,
        accessibility_score=accessibility_score,
        diagnostics_agree=diagnostics_agree,
        orientation=orientation,
        record_defined=record_defined,
        microscopic_maps_reversible=reversible,
    )


def canonical_asymmetric_record_model() -> AsymmetricRecordModel:
    """Return the protocol-frozen blank-memory Stage 3C model."""

    return AsymmetricRecordModel(ensemble=canonical_forward_ensemble())


def canonical_record_orientation_assessment() -> RecordOrientationAssessment:
    """Assess the canonical Stage 3C model with the frozen Stage 3B diagnostics."""

    return assess_record_orientation(canonical_asymmetric_record_model())
