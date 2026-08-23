from t_search.stage12_ablation import (
    STAGE12F_CROSS_ORBIT_GAUGE_REJECTED,
    STAGE12F_EQUAL_LABEL_REJECTED,
    STAGE12F_GUARDS,
    STAGE12F_NOT_LICENSED,
    STAGE12F_ORBIT_CORRESPONDENCE_CORRUPTED,
    STAGE12F_ORBIT_IDENTITY_RECONSTRUCTIBLE,
    STAGE12F_REPRESENTATIVE_CORRUPTION,
    STAGE12F_SINGLE_INVARIANT_REJECTED,
    STAGE12F_TEMPORAL_SUCCESSION_REJECTED,
    canonical_stage12f_ablations,
    canonical_stage12f_false_positive_controls,
    stage12f_diagnostics,
    stage12f_summary,
)


def _controls_by_id():
    return {item.control_id: item for item in canonical_stage12f_false_positive_controls()}


def test_stage12f_orbit_identity_and_correspondence_ablations_separate_typing_from_numerics() -> None:
    ablations = canonical_stage12f_ablations()
    assert len(ablations) == 2
    assert {item.classification for item in ablations} == {
        STAGE12F_ORBIT_IDENTITY_RECONSTRUCTIBLE,
        STAGE12F_ORBIT_CORRESPONDENCE_CORRUPTED,
    }
    assert all(item.numerical_payload_status == "reconstructible" for item in ablations)
    assert all(item.typed_identification_status == "lost" for item in ablations)
    assert all(item.covariance_status == "not_established" for item in ablations)
    assert all(item.metaphysical_claim_status == STAGE12F_NOT_LICENSED for item in ablations)


def test_stage12f_single_invariant_and_equal_label_false_matches_are_rejected() -> None:
    controls = _controls_by_id()
    assert controls["same_P_D_only"].classification == STAGE12F_SINGLE_INVARIANT_REJECTED
    assert controls["same_Q_D_only"].classification == STAGE12F_SINGLE_INVARIANT_REJECTED
    for control_id, expected_count in (
        ("equal_T_cross_orbit", 30),
        ("equal_q_cross_orbit", 2),
        ("equal_raw_lambda_cross_orbit", 312),
    ):
        item = controls[control_id]
        assert item.classification == STAGE12F_EQUAL_LABEL_REJECTED
        assert item.rejected
        assert item.witness_count == expected_count


def test_stage12f_wrong_gauge_cross_orbit_and_invariant_corruptions_are_rejected() -> None:
    controls = _controls_by_id()
    assert controls["forced_cross_orbit_Phi"].classification == STAGE12F_CROSS_ORBIT_GAUGE_REJECTED
    assert controls["forced_cross_orbit_Phi"].rejected
    for control_id in ("wrong_Q_D_path", "wrong_P_D_path"):
        assert controls[control_id].classification == "numerically_refuted"
        assert controls[control_id].rejected
        assert controls[control_id].residual > 0.0


def test_stage12f_detects_representative_dependent_O_P_R_V_and_measurement_corruption() -> None:
    controls = _controls_by_id()
    ids = {
        "representative_dependent_O_corruption",
        "representative_dependent_P_corruption",
        "representative_dependent_R_corruption",
        "representative_dependent_V_corruption",
        "representative_dependent_measurement_corruption",
    }
    assert all(controls[control_id].classification == STAGE12F_REPRESENTATIVE_CORRUPTION for control_id in ids)
    assert all(controls[control_id].rejected for control_id in ids)
    assert all(controls[control_id].residual > 0.0 for control_id in ids)
    assert abs(controls["representative_dependent_measurement_corruption"].residual - 0.05) <= 1e-12


def test_stage12f_consolidates_context_transport_and_orbit_insensitive_controls() -> None:
    controls = _controls_by_id()
    for control_id in (
        "wrong_orbit_correspondence",
        "wrong_event_correspondence",
        "wrong_class_correspondence",
        "wrong_outcome_correspondence",
        "wrong_normalization",
        "orbit_insensitive_measurement_clone",
        "mixed_orbit_phi",
        "clock_label_as_parameterization",
        "parameterization_label_as_clock",
        "gauge_type_relabelled_as_reparameterization",
        "constraint_orbit_as_modal_continuation",
        "orientation_reversal",
        "noninjective_square",
    ):
        assert controls[control_id].rejected
    assert controls["orbit_insensitive_measurement_clone"].classification == "false_positive_rejected"


def test_stage12f_rejects_cross_orbit_temporal_succession_overread() -> None:
    control = _controls_by_id()["different_physical_orbit_as_temporal_succession"]
    assert control.classification == STAGE12F_TEMPORAL_SUCCESSION_REJECTED
    assert control.rejected
    assert control.metaphysical_claim_status == STAGE12F_NOT_LICENSED


def test_stage12f_full_matrix_closes_criteria_44_through_47() -> None:
    d = stage12f_diagnostics()
    assert d.ablation_count == 2
    assert d.reconstructible_ablation_count == 2
    assert d.typed_lost_ablation_count == 2
    assert d.false_positive_control_count == 27
    assert d.rejected_false_positive_control_count == 27
    assert d.single_invariant_control_count == 2
    assert d.equal_label_control_count == 3
    assert d.wrong_gauge_control_count == 3
    assert d.representative_corruption_control_count == 5
    assert d.representative_corruption_detected_count == 5
    assert d.orbit_insensitive_trivialization_rejected
    assert d.orientation_reversal_rejected
    assert d.noninjective_relabeling_rejected
    assert d.temporal_succession_false_positive_rejected
    assert d.all_metaphysical_claims_not_licensed
    assert d.metaphysical_promotion_avoided
    assert d.criteria_44_47_satisfied


def test_stage12f_summary_keeps_interpretation_guards_and_stage12g_boundary() -> None:
    summary = stage12f_summary()
    assert summary["status"] == "Stage 12F completed; criteria 44–47 satisfied"
    assert summary["bounded_result"].endswith("= established")
    assert summary["next"] == "Stage 12G — executable synthesis and evidence-selected next gate"
    assert tuple(summary["guards"]) == STAGE12F_GUARDS
    for phrase in (
        "numerical reconstructibility != typed operational identification",
        "reconstructible != universally redundant",
        "lost != metaphysically irreducible",
        "wrong-gauge failure != ontological becoming",
        "cross-orbit mismatch != temporal succession or ontological becoming",
        "false-positive rejection != proof of eternalism",
        "not_established != false",
    ):
        assert phrase in summary["guards"]
