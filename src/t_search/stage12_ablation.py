"""Stage 12F ablation / wrong-orbit / false-positive controls.

Stage 12A-E establish a finite typed multi-orbit gauge atlas with relational,
measurement, and C x G x Phi compatibility evidence.  Stage 12F asks what
survives when orbit/correspondence resources are removed or corrupted, and
whether deliberately weak or mistyped matching rules can counterfeit the
positive result.

The central distinctions remain explicit:

    numerical reconstructibility != typed operational identification
    reconstructible != universally redundant
    lost != metaphysically irreducible
    wrong-gauge failure != ontological becoming

All controls are finite-model diagnostics.  No failure or ablation is promoted
to a claim about metaphysical fundamentality, eternalism, or ontological
becoming.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from functools import lru_cache
from typing import Literal

from .stage11_ablation import stage11f_diagnostics
from .stage12_compatibility import stage12e_controls
from .stage12_gauge_atlas import (
    STAGE12C_FALSE_POSITIVE_REJECTED,
    STAGE12C_NUMERICALLY_REFUTED,
    STAGE12C_NUMERICAL_STATUS_RECONSTRUCTIBLE,
    STAGE12C_TYPED_STATUS_LOST,
    canonical_stage12c_wrong_invariant_controls,
    stage12c_gauge_arrow,
    stage12c_modal_separation_control,
    stage12c_orbit_identity_ablation,
)
from .stage12_measurement import (
    STAGE12D_FALSE_POSITIVE_REJECTED,
    canonical_stage12d_architectures,
    canonical_stage12d_measurement_views,
    stage12d_controls,
    stage12d_validate_architecture,
)
from .stage12_multi_orbit import (
    STAGE12A_ATOL,
    canonical_stage12a_orbits,
    canonical_stage12a_representatives,
)
from .stage12_relational import (
    STAGE12B_DIFFERENT_ORBIT,
    STAGE12B_FALSE_POSITIVE_REJECTED,
    stage12b_compare_orbits,
    stage12b_dirac_from_representative,
    stage12b_false_match_control,
)

NumericalPayloadStatus = Literal["preserved", "reconstructible", "corrupted"]
TypedIdentificationStatus = Literal["preserved", "lost", "underdetermined"]
CovarianceStatus = Literal["established", "not_established", "refuted"]

STAGE12F_ORBIT_IDENTITY_RECONSTRUCTIBLE = (
    "orbit_identity_reconstructible_but_typed_correspondence_lost"
)
STAGE12F_ORBIT_CORRESPONDENCE_CORRUPTED = (
    "corrupted_orbit_correspondence_numerically_reconstructible_but_typed_claim_lost"
)
STAGE12F_SINGLE_INVARIANT_REJECTED = "single_invariant_orbit_match_false_positive_rejected"
STAGE12F_EQUAL_LABEL_REJECTED = "equal_label_or_single_variable_match_false_positive_rejected"
STAGE12F_CROSS_ORBIT_GAUGE_REJECTED = "cross_orbit_gauge_false_positive_rejected"
STAGE12F_REPRESENTATIVE_CORRUPTION = "representative_dependent_payload_corruption_detected"
STAGE12F_TEMPORAL_SUCCESSION_REJECTED = "cross_orbit_temporal_succession_false_positive_rejected"
STAGE12F_FALSE_POSITIVE_REJECTED = "false_positive_rejected"
STAGE12F_NOT_LICENSED = "not_licensed"
STAGE12F_RESULT = (
    "Stage 12F typed-resource ablation / wrong-orbit / false-positive controls "
    "on the frozen finite multi-orbit gauge atlas = established"
)

STAGE12F_GUARDS = (
    "numerical reconstructibility != typed operational identification",
    "reconstructible != universally redundant",
    "lost != metaphysically irreducible",
    "missing typing != metaphysical absence",
    "wrong-gauge failure != ontological becoming",
    "cross-orbit mismatch != temporal succession or ontological becoming",
    "finite-model ablation != fundamental ontology",
    "false-positive rejection != proof of eternalism",
    "not_established != false",
)


@dataclass(frozen=True, slots=True)
class Stage12FAblationClassification:
    ablation_id: str
    resource: str
    numerical_payload_status: NumericalPayloadStatus
    typed_identification_status: TypedIdentificationStatus
    covariance_status: CovarianceStatus
    classification: str
    residual: float
    witness: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage12FFalsePositiveControl:
    control_id: str
    category: str
    classification: str
    rejected: bool
    witness_count: int
    residual: float
    witness: str
    evidence_source: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage12FDiagnostics:
    ablation_count: int
    reconstructible_ablation_count: int
    typed_lost_ablation_count: int
    false_positive_control_count: int
    rejected_false_positive_control_count: int
    single_invariant_control_count: int
    equal_label_control_count: int
    wrong_gauge_control_count: int
    representative_corruption_control_count: int
    representative_corruption_detected_count: int
    orbit_insensitive_trivialization_rejected: bool
    orientation_reversal_rejected: bool
    noninjective_relabeling_rejected: bool
    temporal_succession_false_positive_rejected: bool
    all_metaphysical_claims_not_licensed: bool
    metaphysical_promotion_avoided: bool
    criteria_44_47_satisfied: bool


def _representative_lookup():
    return {item.representative_id: item for item in canonical_stage12a_representatives()}


def _canonical_orbit_for_dirac(Q_D: float, P_D: float) -> str | None:
    matches = [
        orbit.orbit_id
        for orbit in canonical_stage12a_orbits()
        if abs(orbit.Q_D - Q_D) <= STAGE12A_ATOL
        and abs(orbit.P_D - P_D) <= STAGE12A_ATOL
    ]
    return matches[0] if len(matches) == 1 else None


@lru_cache(maxsize=1)
def canonical_stage12f_ablations() -> tuple[Stage12FAblationClassification, ...]:
    """Classify removal/corruption of orbit identity separately from numerics."""

    inherited = stage12c_orbit_identity_ablation()
    inherited_ok = bool(
        inherited.typed_status == STAGE12C_TYPED_STATUS_LOST
        and inherited.numerical_status == STAGE12C_NUMERICAL_STATUS_RECONSTRUCTIBLE
        and inherited.reconstructed_class_count == 4
        and inherited.reconstructed_class_sizes == (5, 5, 5, 5)
    )
    removed = Stage12FAblationClassification(
        ablation_id="remove_typed_orbit_identity_correspondence",
        resource="typed physical-orbit identity/correspondence",
        numerical_payload_status="reconstructible" if inherited_ok else "corrupted",
        typed_identification_status="lost" if inherited_ok else "preserved",
        covariance_status="not_established" if inherited_ok else "established",
        classification=(
            STAGE12F_ORBIT_IDENTITY_RECONSTRUCTIBLE if inherited_ok else "inconclusive"
        ),
        residual=0.0 if inherited_ok else 1.0,
        witness=(
            "declared orbit labels are removed while the full independently reconstructed "
            "Dirac pair still recovers four numerical classes of five representatives"
        ),
        metaphysical_claim_status=STAGE12F_NOT_LICENSED,
    )

    architectures = canonical_stage12d_architectures()
    base = architectures[0]
    other = next(item for item in architectures if item.orbit_id != base.orbit_id)
    corrupted = replace(
        base,
        orbit_id=other.orbit_id,
        Xi=replace(base.Xi, orbit_id=other.orbit_id, quotient_id=other.quotient_id),
    )
    validation = stage12d_validate_architecture(corrupted)
    representative = _representative_lookup()[base.representative_id]
    estimate = stage12b_dirac_from_representative(representative)
    reconstructed_orbit = _canonical_orbit_for_dirac(estimate.Q_D, estimate.P_D)
    corrupted_ok = bool(
        not validation.valid
        and reconstructed_orbit == base.orbit_id
        and reconstructed_orbit != corrupted.orbit_id
    )
    correspondence = Stage12FAblationClassification(
        ablation_id="corrupt_orbit_and_quotient_correspondence",
        resource="Xi orbit/quotient correspondence",
        numerical_payload_status="reconstructible" if corrupted_ok else "corrupted",
        typed_identification_status="lost" if corrupted_ok else "preserved",
        covariance_status="not_established" if corrupted_ok else "established",
        classification=(
            STAGE12F_ORBIT_CORRESPONDENCE_CORRUPTED if corrupted_ok else "inconclusive"
        ),
        residual=0.0 if corrupted_ok else 1.0,
        witness=(
            "the representative phase-space payload still reconstructs its original full Dirac pair, "
            "while the deliberately corrupted Xi orbit/quotient claim fails typed validation"
        ),
        metaphysical_claim_status=STAGE12F_NOT_LICENSED,
    )
    return (removed, correspondence)


def _base_false_match_controls() -> list[Stage12FFalsePositiveControl]:
    false_match = stage12b_false_match_control()
    result: list[Stage12FFalsePositiveControl] = []

    result.append(
        Stage12FFalsePositiveControl(
            control_id="same_P_D_only",
            category="single_invariant",
            classification=(
                STAGE12F_SINGLE_INVARIANT_REJECTED
                if false_match.same_P_different_Q_rejected
                else "inconclusive"
            ),
            rejected=false_match.same_P_different_Q_rejected,
            witness_count=1,
            residual=0.75,
            witness="omega_alpha and omega_beta share P_D but have different Q_D",
            evidence_source="Stage 12B full-Dirac-pair control",
            metaphysical_claim_status=STAGE12F_NOT_LICENSED,
        )
    )
    result.append(
        Stage12FFalsePositiveControl(
            control_id="same_Q_D_only",
            category="single_invariant",
            classification=(
                STAGE12F_SINGLE_INVARIANT_REJECTED
                if false_match.same_Q_different_P_rejected
                else "inconclusive"
            ),
            rejected=false_match.same_Q_different_P_rejected,
            witness_count=1,
            residual=0.5,
            witness="omega_alpha and omega_gamma share Q_D but have different P_D",
            evidence_source="Stage 12B full-Dirac-pair control",
            metaphysical_claim_status=STAGE12F_NOT_LICENSED,
        )
    )

    for control_id, count in (
        ("equal_T_cross_orbit", false_match.equal_T_cross_orbit_match_count),
        ("equal_q_cross_orbit", false_match.equal_q_cross_orbit_match_count),
        ("equal_raw_lambda_cross_orbit", false_match.equal_raw_lambda_cross_orbit_match_count),
    ):
        rejected = bool(count > 0 and false_match.all_equal_single_variable_matches_rejected)
        result.append(
            Stage12FFalsePositiveControl(
                control_id=control_id,
                category="equal_label_or_single_variable",
                classification=(STAGE12F_EQUAL_LABEL_REJECTED if rejected else "inconclusive"),
                rejected=rejected,
                witness_count=int(count),
                residual=float(count),
                witness="equal one-dimensional labels/values do not license full physical-orbit identity",
                evidence_source="Stage 12B equal-label controls",
                metaphysical_claim_status=STAGE12F_NOT_LICENSED,
            )
        )
    return result


def _wrong_gauge_controls() -> list[Stage12FFalsePositiveControl]:
    result: list[Stage12FFalsePositiveControl] = []
    wrong_invariants = canonical_stage12c_wrong_invariant_controls()
    for item in wrong_invariants:
        rejected = item.classification == STAGE12C_NUMERICALLY_REFUTED
        result.append(
            Stage12FFalsePositiveControl(
                control_id=item.control_id,
                category="wrong_gauge",
                classification=item.classification,
                rejected=rejected,
                witness_count=1 if rejected else 0,
                residual=float(
                    max(
                        item.Q_D_drift,
                        item.P_D_drift,
                        item.phase_space_residual,
                        item.constraint_residual,
                    )
                ),
                witness=f"purported gauge path corrupts {item.corrupted_field} and fails the invariant/flow check",
                evidence_source="Stage 12C wrong-invariant controls",
                metaphysical_claim_status=STAGE12F_NOT_LICENSED,
            )
        )

    reps = canonical_stage12a_representatives()
    source = next(item for item in reps if item.orbit_id == "omega_alpha")
    target = next(item for item in reps if item.orbit_id == "omega_beta")
    cross_rejected = False
    try:
        stage12c_gauge_arrow(source, target)
    except ValueError:
        cross_rejected = True
    result.append(
        Stage12FFalsePositiveControl(
            control_id="forced_cross_orbit_Phi",
            category="wrong_gauge",
            classification=(STAGE12F_CROSS_ORBIT_GAUGE_REJECTED if cross_rejected else "inconclusive"),
            rejected=cross_rejected,
            witness_count=1 if cross_rejected else 0,
            residual=float(
                max(abs(source.Q_D - target.Q_D), abs(source.P_D - target.P_D))
            ),
            witness="typed Phi construction rejects endpoints belonging to distinct physical orbits",
            evidence_source="Stage 12C gauge-arrow constructor",
            metaphysical_claim_status=STAGE12F_NOT_LICENSED,
        )
    )
    return result


def _representative_corruption_controls() -> list[Stage12FFalsePositiveControl]:
    architectures = canonical_stage12d_architectures()
    base = architectures[0]
    magnitude = 0.125

    corrupted_event = replace(
        base.O.relational_events[0],
        q_value=float(base.O.relational_events[0].q_value + magnitude),
    )
    corrupted_O = replace(
        base,
        O=replace(
            base.O,
            relational_events=(corrupted_event,) + base.O.relational_events[1:],
        ),
    )
    corrupted_P = replace(base, P=replace(base.P, qext_ids=tuple(reversed(base.P.qext_ids))))
    corrupted_direction = replace(
        base.R.R_direction[0],
        record_score=float(base.R.R_direction[0].record_score + magnitude),
    )
    corrupted_R = replace(
        base,
        R=replace(base.R, R_direction=(corrupted_direction,) + base.R.R_direction[1:]),
    )
    corrupted_weights = (float(base.V.V_weights[0] + magnitude),) + base.V.V_weights[1:]
    corrupted_V = replace(base, V=replace(base.V, V_weights=corrupted_weights))

    result: list[Stage12FFalsePositiveControl] = []
    for layer, candidate, residual in (
        ("O", corrupted_O, magnitude),
        ("P", corrupted_P, 1.0),
        ("R", corrupted_R, magnitude),
        ("V", corrupted_V, magnitude),
    ):
        validation = stage12d_validate_architecture(candidate)
        rejected = bool(not validation.valid)
        result.append(
            Stage12FFalsePositiveControl(
                control_id=f"representative_dependent_{layer}_corruption",
                category="representative_dependent_corruption",
                classification=(STAGE12F_REPRESENTATIVE_CORRUPTION if rejected else "inconclusive"),
                rejected=rejected,
                witness_count=1 if rejected else 0,
                residual=float(residual),
                witness=(
                    f"only {base.representative_id} receives corrupted {layer}; the canonical Stage 12D "
                    "representative validator rejects the resulting within-orbit descent mismatch"
                ),
                evidence_source="Stage 12D typed architecture validator",
                metaphysical_claim_status=STAGE12F_NOT_LICENSED,
            )
        )

    measurements = canonical_stage12d_measurement_views()
    base_measurement = next(
        item
        for item in measurements
        if item.representative_id == base.representative_id and item.continuation_id == "h_L"
    )
    same_orbit_peer = next(
        item
        for item in measurements
        if item.orbit_id == base_measurement.orbit_id
        and item.continuation_id == base_measurement.continuation_id
        and item.representative_id != base_measurement.representative_id
    )
    probabilities = dict(base_measurement.probabilities)
    outcome_ids = tuple(probabilities)
    probabilities[outcome_ids[0]] += 0.05
    probabilities[outcome_ids[1]] -= 0.05
    corrupted_probabilities = tuple((outcome, float(probabilities[outcome])) for outcome in outcome_ids)
    peer_probabilities = dict(same_orbit_peer.probabilities)
    residual = max(
        abs(dict(corrupted_probabilities)[outcome] - peer_probabilities[outcome])
        for outcome in outcome_ids
    )
    rejected = residual > STAGE12A_ATOL
    result.append(
        Stage12FFalsePositiveControl(
            control_id="representative_dependent_measurement_corruption",
            category="representative_dependent_corruption",
            classification=(STAGE12F_REPRESENTATIVE_CORRUPTION if rejected else "inconclusive"),
            rejected=rejected,
            witness_count=1 if rejected else 0,
            residual=float(residual),
            witness=(
                "one representative receives a probability perturbation that preserves normalization but "
                "breaks same-orbit measurement descent relative to an unmodified peer"
            ),
            evidence_source="Stage 12D same-orbit measurement descent",
            metaphysical_claim_status=STAGE12F_NOT_LICENSED,
        )
    )
    return result


@lru_cache(maxsize=1)
def canonical_stage12f_false_positive_controls() -> tuple[Stage12FFalsePositiveControl, ...]:
    controls: list[Stage12FFalsePositiveControl] = []
    controls.extend(_base_false_match_controls())
    controls.extend(_wrong_gauge_controls())

    modal = stage12c_modal_separation_control()
    modal_rejected = modal.classification == STAGE12C_FALSE_POSITIVE_REJECTED
    controls.append(
        Stage12FFalsePositiveControl(
            control_id="constraint_orbit_as_modal_continuation",
            category="typed_conflation",
            classification=modal.classification,
            rejected=modal_rejected,
            witness_count=1 if modal_rejected else 0,
            residual=1.0 if modal_rejected else 0.0,
            witness="gauge quotient classes remain disjoint from modal continuation nodes",
            evidence_source="Stage 12C modal-separation control",
            metaphysical_claim_status=STAGE12F_NOT_LICENSED,
        )
    )

    for item in stage12d_controls():
        controls.append(
            Stage12FFalsePositiveControl(
                control_id=item.control_id,
                category=(
                    "orbit_insensitive_trivialization"
                    if item.control_id == "orbit_insensitive_measurement_clone"
                    else "measurement_or_correspondence_context"
                ),
                classification=item.classification,
                rejected=item.rejected,
                witness_count=1 if item.rejected else 0,
                residual=float(item.numerical_witness_residual),
                witness="Stage 12D inherited typed-context / normalization / orbit-sensitivity control",
                evidence_source="Stage 12D controls",
                metaphysical_claim_status=STAGE12F_NOT_LICENSED,
            )
        )

    controls.extend(_representative_corruption_controls())

    for item in stage12e_controls():
        controls.append(
            Stage12FFalsePositiveControl(
                control_id=item.control_id,
                category="mixed_or_untyped_transport",
                classification=item.classification,
                rejected=item.rejected,
                witness_count=1 if item.rejected else 0,
                residual=1.0 if item.rejected else 0.0,
                witness=item.reason,
                evidence_source="Stage 12E invalid-path controls",
                metaphysical_claim_status=STAGE12F_NOT_LICENSED,
            )
        )

    inherited = stage11f_diagnostics()
    inherited_by_id = {item.control: item for item in inherited.false_positive_controls}
    for control_id in ("orientation_reversal", "noninjective_square"):
        item = inherited_by_id[control_id]
        controls.append(
            Stage12FFalsePositiveControl(
                control_id=control_id,
                category="excluded_external_reparameterization",
                classification=item.classification,
                rejected=item.rejected,
                witness_count=item.witness_count,
                residual=float(item.residual),
                witness=item.witness,
                evidence_source="Stage 11F excluded external-parameterization controls",
                metaphysical_claim_status=STAGE12F_NOT_LICENSED,
            )
        )

    alpha, beta = canonical_stage12a_orbits()[:2]
    comparison = stage12b_compare_orbits(alpha, beta)
    succession_rejected = bool(
        comparison.classification == STAGE12B_DIFFERENT_ORBIT
        and not comparison.full_dirac_pair_equal
    )
    controls.append(
        Stage12FFalsePositiveControl(
            control_id="different_physical_orbit_as_temporal_succession",
            category="metaphysical_overread",
            classification=(
                STAGE12F_TEMPORAL_SUCCESSION_REJECTED if succession_rejected else "inconclusive"
            ),
            rejected=succession_rejected,
            witness_count=1 if succession_rejected else 0,
            residual=float(max(abs(alpha.Q_D - beta.Q_D), abs(alpha.P_D - beta.P_D))),
            witness=(
                "different frozen Dirac data identify distinct physical-orbit classes; the model supplies "
                "no licensed Phi arrow or rule that turns that difference into later-time succession"
            ),
            evidence_source="Stage 12B/C physical-orbit discrimination and gauge typing",
            metaphysical_claim_status=STAGE12F_NOT_LICENSED,
        )
    )
    return tuple(controls)


@lru_cache(maxsize=1)
def stage12f_diagnostics() -> Stage12FDiagnostics:
    ablations = canonical_stage12f_ablations()
    controls = canonical_stage12f_false_positive_controls()

    reconstructible = sum(item.numerical_payload_status == "reconstructible" for item in ablations)
    typed_lost = sum(item.typed_identification_status == "lost" for item in ablations)
    rejected = sum(item.rejected for item in controls)
    representative_controls = tuple(
        item for item in controls if item.category == "representative_dependent_corruption"
    )
    single_invariant = tuple(item for item in controls if item.category == "single_invariant")
    equal_label = tuple(
        item for item in controls if item.category == "equal_label_or_single_variable"
    )
    wrong_gauge = tuple(item for item in controls if item.category == "wrong_gauge")

    clone = next(item for item in controls if item.control_id == "orbit_insensitive_measurement_clone")
    orientation = next(item for item in controls if item.control_id == "orientation_reversal")
    noninjective = next(item for item in controls if item.control_id == "noninjective_square")
    succession = next(
        item for item in controls if item.control_id == "different_physical_orbit_as_temporal_succession"
    )

    all_not_licensed = all(
        item.metaphysical_claim_status == STAGE12F_NOT_LICENSED
        for item in (*ablations, *controls)
    )
    required_guards = {
        "reconstructible != universally redundant",
        "lost != metaphysically irreducible",
        "wrong-gauge failure != ontological becoming",
        "cross-orbit mismatch != temporal succession or ontological becoming",
        "finite-model ablation != fundamental ontology",
        "false-positive rejection != proof of eternalism",
        "not_established != false",
    }
    guard_audit = required_guards.issubset(set(STAGE12F_GUARDS))

    criteria_44 = bool(
        len(ablations) == 2
        and reconstructible == 2
        and typed_lost == 2
        and all(item.covariance_status == "not_established" for item in ablations)
    )
    criteria_45 = bool(
        len(single_invariant) == 2
        and all(item.rejected for item in single_invariant)
        and len(equal_label) == 3
        and all(item.rejected and item.witness_count > 0 for item in equal_label)
        and len(wrong_gauge) == 3
        and all(item.rejected for item in wrong_gauge)
    )
    criteria_46 = bool(
        len(representative_controls) == 5
        and all(item.rejected for item in representative_controls)
        and clone.rejected
    )
    criteria_47 = bool(all_not_licensed and guard_audit and succession.rejected)
    all_controls_rejected = rejected == len(controls)

    return Stage12FDiagnostics(
        ablation_count=len(ablations),
        reconstructible_ablation_count=reconstructible,
        typed_lost_ablation_count=typed_lost,
        false_positive_control_count=len(controls),
        rejected_false_positive_control_count=rejected,
        single_invariant_control_count=len(single_invariant),
        equal_label_control_count=len(equal_label),
        wrong_gauge_control_count=len(wrong_gauge),
        representative_corruption_control_count=len(representative_controls),
        representative_corruption_detected_count=sum(item.rejected for item in representative_controls),
        orbit_insensitive_trivialization_rejected=clone.rejected,
        orientation_reversal_rejected=orientation.rejected,
        noninjective_relabeling_rejected=noninjective.rejected,
        temporal_succession_false_positive_rejected=succession.rejected,
        all_metaphysical_claims_not_licensed=all_not_licensed,
        metaphysical_promotion_avoided=guard_audit,
        criteria_44_47_satisfied=bool(
            criteria_44 and criteria_45 and criteria_46 and criteria_47 and all_controls_rejected
        ),
    )


def stage12f_summary() -> dict[str, object]:
    diagnostics = stage12f_diagnostics()
    return {
        "stage": "12F",
        "status": (
            "Stage 12F completed; criteria 44–47 satisfied"
            if diagnostics.criteria_44_47_satisfied
            else "Stage 12F incomplete"
        ),
        "bounded_result": STAGE12F_RESULT,
        "ablations": tuple(
            {
                "ablation_id": item.ablation_id,
                "resource": item.resource,
                "numerical_payload_status": item.numerical_payload_status,
                "typed_identification_status": item.typed_identification_status,
                "covariance_status": item.covariance_status,
                "classification": item.classification,
                "residual": item.residual,
                "metaphysical_claim_status": item.metaphysical_claim_status,
            }
            for item in canonical_stage12f_ablations()
        ),
        "controls": tuple(
            {
                "control_id": item.control_id,
                "category": item.category,
                "classification": item.classification,
                "rejected": item.rejected,
                "witness_count": item.witness_count,
                "residual": item.residual,
                "evidence_source": item.evidence_source,
                "metaphysical_claim_status": item.metaphysical_claim_status,
            }
            for item in canonical_stage12f_false_positive_controls()
        ),
        "diagnostics": {
            "ablation_count": diagnostics.ablation_count,
            "reconstructible_ablation_count": diagnostics.reconstructible_ablation_count,
            "typed_lost_ablation_count": diagnostics.typed_lost_ablation_count,
            "false_positive_controls": (
                diagnostics.rejected_false_positive_control_count,
                diagnostics.false_positive_control_count,
            ),
            "single_invariant_control_count": diagnostics.single_invariant_control_count,
            "equal_label_control_count": diagnostics.equal_label_control_count,
            "wrong_gauge_control_count": diagnostics.wrong_gauge_control_count,
            "representative_corruption_controls": (
                diagnostics.representative_corruption_detected_count,
                diagnostics.representative_corruption_control_count,
            ),
            "orbit_insensitive_trivialization_rejected": diagnostics.orbit_insensitive_trivialization_rejected,
            "orientation_reversal_rejected": diagnostics.orientation_reversal_rejected,
            "noninjective_relabeling_rejected": diagnostics.noninjective_relabeling_rejected,
            "temporal_succession_false_positive_rejected": diagnostics.temporal_succession_false_positive_rejected,
            "all_metaphysical_claims_not_licensed": diagnostics.all_metaphysical_claims_not_licensed,
        },
        "guards": STAGE12F_GUARDS,
        "next": "Stage 12G — executable synthesis and evidence-selected next gate",
    }
