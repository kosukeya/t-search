"""Stage 11F ablation / wrong-gauge / false-positive controls.

Stage 11A-E established a finite typed parametrized-covariance precursor on a
frozen positive family.  Stage 11F asks a different question: what survives
when representation/typing resources are removed or corrupted, and what kind
of conclusion is still licensed?

The central distinctions are:

    numerical reconstructibility != typed operational identification
    reconstructible != universally redundant
    lost != metaphysically irreducible

Ablations are therefore classified separately at the numerical-payload,
typed-identification, and covariance-claim levels.  These finite-model controls
are not claims about metaphysical fundamentality or ontological becoming.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Literal

import numpy as np

from .stage5_clock_change import DEFAULT_ATOL
from .stage9_modal import canonical_stage9c_models
from .stage11_lift import (
    STAGE11C_CORRUPTION_CLASSIFICATION,
    stage11c_corruption_controls,
    stage11c_public_architecture,
    stage11c_validate_architecture,
)
from .stage11_measurement import stage11d_validate_measurement_context
from .stage11_parametrized import (
    STAGE11A_ATOL,
    STAGE11A_CUBIC,
    STAGE11A_IDENTITY,
    STAGE11A_NONINJECTIVE,
    STAGE11A_REVERSE,
    canonical_stage11a_positive_family,
    canonical_stage11a_source_labels,
    stage11a_excluded_parameterizations,
)
from .stage11_relational import (
    STAGE11B_RAW_MATCH_INVALID,
    STAGE11B_TARGET_INDEX,
    stage11b_raw_parameter_match_control,
    stage11b_relational_derivatives,
)

NumericalPayloadStatus = Literal["preserved", "reconstructible", "corrupted"]
TypedIdentificationStatus = Literal["preserved", "lost", "underdetermined"]
CovarianceStatus = Literal["established", "not_established", "refuted"]

STAGE11F_EVENT_RECONSTRUCTIBLE = "event_correspondence_reconstructible_but_typed_identity_lost"
STAGE11F_MISSING_LAPSE_SEMANTICS = "lapse_semantics_missing_typed_claim_not_established"
STAGE11F_WRONG_LAPSE_JACOBIAN = "wrong_lapse_jacobian_numerically_refuted"
STAGE11F_ORIENTATION_REVERSE = "orientation_reversal_outside_positive_family"
STAGE11F_NONINJECTIVE = "noninjective_relabeling_rejected"

STAGE11F_GUARDS = (
    "numerical reconstructibility != typed operational identification",
    "reconstructible != universally redundant",
    "lost != metaphysically irreducible",
    "missing typing != metaphysical absence",
    "wrong-gauge failure != ontological becoming",
    "finite-model ablation != fundamental ontology",
    "not_established != false",
)


@dataclass(frozen=True, slots=True)
class Stage11FAblationClassification:
    ablation: str
    resource: str
    numerical_payload_status: NumericalPayloadStatus
    typed_identification_status: TypedIdentificationStatus
    covariance_status: CovarianceStatus
    classification: str
    witness: str
    residual: float


@dataclass(frozen=True, slots=True)
class Stage11FFalsePositiveControl:
    control: str
    classification: str
    rejected: bool
    witness_count: int
    residual: float
    witness: str


@dataclass(frozen=True, slots=True)
class Stage11FDiagnostics:
    classifications: tuple[Stage11FAblationClassification, ...]
    false_positive_controls: tuple[Stage11FFalsePositiveControl, ...]
    event_correspondence_numerically_reconstructible: bool
    event_correspondence_typed_identity_lost: bool
    missing_lapse_semantics_rejected: bool
    missing_lapse_numeric_derivative_residual: float
    wrong_lapse_jacobian_rejected: bool
    wrong_lapse_value_residual: float
    wrong_lapse_relational_derivative_residual: float
    orientation_reverse_rejected: bool
    orientation_reverse_decreasing_step_count: int
    noninjective_rejected: bool
    noninjective_collision_count: int
    raw_lambda_matching_rejected: bool
    raw_lambda_false_identity_count: int
    parameter_corruption_control_count: int
    parameter_corruption_detected_count: int
    false_positive_control_count: int
    rejected_false_positive_control_count: int
    metaphysical_promotion_avoided: bool
    criteria_44_47_satisfied: bool


def _trajectory(parameterization_id: str):
    matches = tuple(
        item
        for item in canonical_stage11a_positive_family()
        if item.parameterization_id == parameterization_id
    )
    if len(matches) != 1:
        raise ValueError(f"unknown Stage 11F positive parameterization {parameterization_id!r}")
    return matches[0]


def _event_correspondence_ablation() -> tuple[Stage11FAblationClassification, bool, bool]:
    _, ontic = canonical_stage9c_models(selected_id="h_L")
    base = stage11c_public_architecture(ontic, STAGE11A_CUBIC)
    missing = replace(
        base,
        Xi=replace(
            base.Xi,
            event_correspondence=(),
            event_correspondence_semantics="",
        ),
    )
    validation = stage11c_validate_architecture(missing)
    measurement_validation = stage11d_validate_measurement_context(
        missing, base.P.qext_ids[0], atol=STAGE11A_ATOL
    )

    reconstructed = tuple(
        (item.stage10_event, item.physical_event_id) for item in missing.O.relational_events
    )
    reconstructible = reconstructed == base.Xi.event_correspondence
    q_residual = max(
        abs(left.q_value - right.q_value)
        for left, right in zip(missing.O.relational_events, base.O.relational_events, strict=True)
    )
    typed_lost = bool(
        not validation.valid
        and not measurement_validation.valid
        and "Xi" in validation.corrupted_layers
        and "event_bridge" in measurement_validation.rejection_reasons
    )
    classification = Stage11FAblationClassification(
        ablation="remove_parameter_event_correspondence",
        resource="parameter-event correspondence",
        numerical_payload_status="reconstructible" if reconstructible else "corrupted",
        typed_identification_status="lost" if typed_lost else "preserved",
        covariance_status="not_established" if typed_lost else "established",
        classification=(STAGE11F_EVENT_RECONSTRUCTIBLE if reconstructible and typed_lost else "inconclusive"),
        witness=(
            "O retains the e1/e2 physical-event roles and q(T) payload, so the mapping can be reconstructed, "
            "but Xi no longer supplies the declared typed identification"
        ),
        residual=float(q_residual),
    )
    return classification, reconstructible, typed_lost


def _lapse_ablations() -> tuple[
    Stage11FAblationClassification,
    Stage11FAblationClassification,
    bool,
    float,
    bool,
    float,
    float,
]:
    _, ontic = canonical_stage9c_models(selected_id="h_L")
    cubic_architecture = stage11c_public_architecture(ontic, STAGE11A_CUBIC)
    identity_architecture = stage11c_public_architecture(ontic, STAGE11A_IDENTITY)
    continuation_id = cubic_architecture.P.qext_ids[0]
    cubic = _trajectory(STAGE11A_CUBIC)

    missing_semantics = replace(
        cubic_architecture,
        Xi=replace(cubic_architecture.Xi, lapse_semantics=""),
    )
    missing_validation = stage11d_validate_measurement_context(
        missing_semantics, continuation_id, atol=STAGE11A_ATOL
    )
    derivative = stage11b_relational_derivatives(cubic)
    derivative_residual = float(np.max(np.abs(derivative - cubic.p_values)))
    missing_rejected = bool(
        not missing_validation.valid
        and "lapse_jacobian" in missing_validation.rejection_reasons
        and derivative_residual <= STAGE11A_ATOL
    )
    missing_classification = Stage11FAblationClassification(
        ablation="remove_lapse_jacobian_semantics",
        resource="lapse/Jacobian semantics",
        numerical_payload_status="preserved",
        typed_identification_status="underdetermined" if missing_rejected else "preserved",
        covariance_status="not_established" if missing_rejected else "established",
        classification=(STAGE11F_MISSING_LAPSE_SEMANTICS if missing_rejected else "inconclusive"),
        witness=(
            "the stored cubic lapse still reconstructs dq/dT correctly, but the Xi statement that explains "
            "how lapse transforms under reparameterization has been removed"
        ),
        residual=derivative_residual,
    )

    wrong_target_lapse = identity_architecture.Xi.target_lapse
    wrong_architecture = replace(
        cubic_architecture,
        Xi=replace(cubic_architecture.Xi, target_lapse=wrong_target_lapse),
    )
    wrong_validation = stage11d_validate_measurement_context(
        wrong_architecture, continuation_id, atol=STAGE11A_ATOL
    )
    expected_target_lapse = cubic_architecture.Xi.target_lapse
    lapse_value_residual = abs(wrong_target_lapse - expected_target_lapse)
    raw_rate = float(cubic.raw_q_rates[STAGE11B_TARGET_INDEX])
    wrong_relational_derivative = raw_rate / float(wrong_target_lapse)
    expected_derivative = float(cubic.p_values[STAGE11B_TARGET_INDEX])
    wrong_derivative_residual = abs(wrong_relational_derivative - expected_derivative)
    wrong_rejected = bool(
        not wrong_validation.valid
        and "lapse_jacobian" in wrong_validation.rejection_reasons
        and lapse_value_residual > 10 * STAGE11A_ATOL
        and wrong_derivative_residual > 10 * STAGE11A_ATOL
    )
    wrong_classification = Stage11FAblationClassification(
        ablation="wrong_lapse_jacobian_value",
        resource="lapse/Jacobian value",
        numerical_payload_status="corrupted" if wrong_rejected else "preserved",
        typed_identification_status="lost" if wrong_rejected else "preserved",
        covariance_status="refuted" if wrong_rejected else "established",
        classification=(STAGE11F_WRONG_LAPSE_JACOBIAN if wrong_rejected else "inconclusive"),
        witness=(
            "reusing the identity-chart target lapse in the cubic chart violates Xi typing and changes the "
            "reconstructed relational derivative away from p"
        ),
        residual=wrong_derivative_residual,
    )
    return (
        missing_classification,
        wrong_classification,
        missing_rejected,
        derivative_residual,
        wrong_rejected,
        float(lapse_value_residual),
        float(wrong_derivative_residual),
    )


def _false_positive_controls() -> tuple[Stage11FFalsePositiveControl, ...]:
    excluded = {item.parameterization_id: item for item in stage11a_excluded_parameterizations()}
    source = canonical_stage11a_source_labels()

    reverse_labels = -source
    reverse_decreasing = int(np.count_nonzero(np.diff(reverse_labels) < 0.0))
    reverse_spec = excluded[STAGE11A_REVERSE]
    reverse_rejected = bool(
        not reverse_spec.admissible
        and not reverse_spec.orientation_preserving
        and reverse_decreasing == source.size - 1
    )

    square_labels = source**2
    rounded = np.round(square_labels, decimals=12)
    noninjective_collisions = int(square_labels.size - np.unique(rounded).size)
    noninjective_spec = excluded[STAGE11A_NONINJECTIVE]
    noninjective_rejected = bool(
        not noninjective_spec.admissible
        and not noninjective_spec.injective_on_test_domain
        and noninjective_collisions > 0
    )

    raw = stage11b_raw_parameter_match_control()
    corruption = stage11c_corruption_controls()

    controls: list[Stage11FFalsePositiveControl] = [
        Stage11FFalsePositiveControl(
            control="orientation_reversal",
            classification=(STAGE11F_ORIENTATION_REVERSE if reverse_rejected else "inconclusive"),
            rejected=reverse_rejected,
            witness_count=reverse_decreasing,
            residual=float(np.max(np.maximum(0.0, -np.diff(reverse_labels)))) if reverse_labels.size > 1 else 0.0,
            witness="f_rev(lambda)=-lambda reverses every sampled raw-label step and is outside the positive family",
        ),
        Stage11FFalsePositiveControl(
            control="noninjective_square",
            classification=(STAGE11F_NONINJECTIVE if noninjective_rejected else "inconclusive"),
            rejected=noninjective_rejected,
            witness_count=noninjective_collisions,
            residual=float(noninjective_collisions),
            witness="f_noninj(lambda)=lambda^2 identifies distinct signed source labels on the tested domain",
        ),
        Stage11FFalsePositiveControl(
            control="raw_lambda_event_matching",
            classification=raw.classification,
            rejected=raw.raw_parameter_matching_rejected,
            witness_count=raw.false_event_identity_count,
            residual=float(raw.false_event_identity_count),
            witness="equal raw lambda produces explicit false physical-event identifications",
        ),
    ]
    for item in corruption:
        controls.append(
            Stage11FFalsePositiveControl(
                control=f"parameter_dependent_{item.layer}_corruption",
                classification=item.classification,
                rejected=item.detected,
                witness_count=1 if item.detected else 0,
                residual=1.0 if item.detected else 0.0,
                witness=f"Stage 11C validator detects parameter-dependent {item.layer} payload corruption",
            )
        )
    return tuple(controls)


def stage11f_diagnostics(*, atol: float = DEFAULT_ATOL) -> Stage11FDiagnostics:
    del atol  # Stage 11F uses the frozen project tolerances in the component witnesses.
    event_classification, event_reconstructible, event_lost = _event_correspondence_ablation()
    (
        missing_lapse_classification,
        wrong_lapse_classification,
        missing_lapse_rejected,
        missing_lapse_derivative_residual,
        wrong_lapse_rejected,
        wrong_lapse_value_residual,
        wrong_lapse_derivative_residual,
    ) = _lapse_ablations()
    controls = _false_positive_controls()

    by_name = {item.control: item for item in controls}
    orientation = by_name["orientation_reversal"]
    noninjective = by_name["noninjective_square"]
    raw = by_name["raw_lambda_event_matching"]
    corruption_controls = tuple(
        item for item in controls if item.control.startswith("parameter_dependent_")
    )
    rejected_count = sum(item.rejected for item in controls)

    required_guards = {
        "reconstructible != universally redundant",
        "lost != metaphysically irreducible",
        "wrong-gauge failure != ontological becoming",
        "finite-model ablation != fundamental ontology",
        "not_established != false",
    }
    guard_audit = required_guards.issubset(set(STAGE11F_GUARDS))

    criteria_44 = bool(
        event_reconstructible
        and event_lost
        and event_classification.numerical_payload_status == "reconstructible"
        and event_classification.typed_identification_status == "lost"
        and event_classification.covariance_status == "not_established"
    )
    criteria_45 = bool(
        missing_lapse_rejected
        and missing_lapse_derivative_residual <= STAGE11A_ATOL
        and wrong_lapse_rejected
        and wrong_lapse_value_residual > 10 * STAGE11A_ATOL
        and wrong_lapse_derivative_residual > 10 * STAGE11A_ATOL
    )
    criteria_46 = bool(
        len(controls) == 7
        and rejected_count == len(controls)
        and orientation.witness_count > 0
        and noninjective.witness_count > 0
        and raw.classification == STAGE11B_RAW_MATCH_INVALID
        and raw.witness_count > 0
        and len(corruption_controls) == 4
        and all(
            item.classification == STAGE11C_CORRUPTION_CLASSIFICATION
            and item.rejected
            for item in corruption_controls
        )
    )
    criteria_47 = guard_audit

    return Stage11FDiagnostics(
        classifications=(
            event_classification,
            missing_lapse_classification,
            wrong_lapse_classification,
        ),
        false_positive_controls=controls,
        event_correspondence_numerically_reconstructible=event_reconstructible,
        event_correspondence_typed_identity_lost=event_lost,
        missing_lapse_semantics_rejected=missing_lapse_rejected,
        missing_lapse_numeric_derivative_residual=missing_lapse_derivative_residual,
        wrong_lapse_jacobian_rejected=wrong_lapse_rejected,
        wrong_lapse_value_residual=wrong_lapse_value_residual,
        wrong_lapse_relational_derivative_residual=wrong_lapse_derivative_residual,
        orientation_reverse_rejected=orientation.rejected,
        orientation_reverse_decreasing_step_count=orientation.witness_count,
        noninjective_rejected=noninjective.rejected,
        noninjective_collision_count=noninjective.witness_count,
        raw_lambda_matching_rejected=raw.rejected,
        raw_lambda_false_identity_count=raw.witness_count,
        parameter_corruption_control_count=len(corruption_controls),
        parameter_corruption_detected_count=sum(item.rejected for item in corruption_controls),
        false_positive_control_count=len(controls),
        rejected_false_positive_control_count=rejected_count,
        metaphysical_promotion_avoided=guard_audit,
        criteria_44_47_satisfied=bool(criteria_44 and criteria_45 and criteria_46 and criteria_47),
    )


def stage11f_summary(*, atol: float = DEFAULT_ATOL) -> dict[str, object]:
    d = stage11f_diagnostics(atol=atol)
    return {
        "stage": "11F",
        "criteria_44_47_satisfied": d.criteria_44_47_satisfied,
        "classifications": tuple(
            {
                "ablation": item.ablation,
                "resource": item.resource,
                "numerical_payload_status": item.numerical_payload_status,
                "typed_identification_status": item.typed_identification_status,
                "covariance_status": item.covariance_status,
                "classification": item.classification,
                "witness": item.witness,
                "residual": item.residual,
            }
            for item in d.classifications
        ),
        "controls": tuple(
            {
                "control": item.control,
                "classification": item.classification,
                "rejected": item.rejected,
                "witness_count": item.witness_count,
                "residual": item.residual,
            }
            for item in d.false_positive_controls
        ),
        "event_correspondence_reconstructible": d.event_correspondence_numerically_reconstructible,
        "event_typed_identity_lost": d.event_correspondence_typed_identity_lost,
        "missing_lapse_numeric_derivative_residual": d.missing_lapse_numeric_derivative_residual,
        "wrong_lapse_value_residual": d.wrong_lapse_value_residual,
        "wrong_lapse_relational_derivative_residual": d.wrong_lapse_relational_derivative_residual,
        "orientation_reverse_decreasing_step_count": d.orientation_reverse_decreasing_step_count,
        "noninjective_collision_count": d.noninjective_collision_count,
        "raw_lambda_false_identity_count": d.raw_lambda_false_identity_count,
        "parameter_corruption_controls": (
            d.parameter_corruption_detected_count,
            d.parameter_corruption_control_count,
        ),
        "false_positive_controls_rejected": (
            d.rejected_false_positive_control_count,
            d.false_positive_control_count,
        ),
        "guards": STAGE11F_GUARDS,
        "next": "Stage 11G — synthesis and evidence-selected next gate",
    }
