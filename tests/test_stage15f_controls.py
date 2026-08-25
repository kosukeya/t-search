from t_search.stage15_controls import (
    STAGE15F_ANOMALY,
    STAGE15F_BASIS_PAYLOAD,
    STAGE15F_BOUNDED_RESULT,
    STAGE15F_CROSS_ORBIT,
    STAGE15F_DISTANCE2,
    STAGE15F_DISCONNECTED,
    STAGE15F_GUARDS,
    STAGE15F_INCOMPLETE_RELATIONAL,
    STAGE15F_PATH_PAYLOAD,
    STAGE15F_REP_PAYLOAD,
    STAGE15F_REQUIRED_VOCABULARY,
    STAGE15F_SINGULAR,
    STAGE15F_SMEARING,
    STAGE15F_STRUCTURE_REMOVED,
    STAGE15F_SUPPORT_EXPANSION,
    canonical_stage15f_controls,
    stage15f_diagnostics,
    stage15f_summary,
)


def _by_id():
    return {item.control_id: item for item in canonical_stage15f_controls()}


def test_stage15f_criterion_44_frozen_control_inventory_is_complete_and_all_controls_reject():
    controls = canonical_stage15f_controls()
    assert len(controls) == 15
    assert all(item.rejected for item in controls)
    classifications = {item.classification for item in controls}
    assert set(STAGE15F_REQUIRED_VOCABULARY) <= classifications

    required_ids = {
        "kappa_zero_structure_function_removal",
        "delete_middle_site_generator_rank",
        "deleted_site_0_to_2_false_path",
        "support_expanding_generator",
        "distance2_coefficient_in_alleged_L1",
        "singular_noninvertible_basis",
        "wrong_smearing_antisymmetry_sign",
        "jacobi_violating_epsilon_T2_anomaly",
        "cross_orbit_local_path_false_positive",
        "one_clock_omitted_relational_expression",
        "representative_dependent_O_corruption",
        "path_dependent_P_corruption",
        "basis_dependent_R_corruption",
        "representative_dependent_V_corruption",
        "known_distance2_seed_not_silently_L1",
    }
    assert {item.control_id for item in controls} == required_ids


def test_stage15f_criterion_45_locality_and_basis_false_positives_are_rejected_without_redefining_L1():
    controls = _by_id()

    support = controls["support_expanding_generator"]
    assert support.classification == STAGE15F_SUPPORT_EXPANSION
    assert support.rejected

    distance2 = controls["distance2_coefficient_in_alleged_L1"]
    assert distance2.classification == STAGE15F_DISTANCE2
    assert distance2.rejected
    assert "L1_rule_failed" in distance2.detail

    singular = controls["singular_noninvertible_basis"]
    assert singular.classification == STAGE15F_SINGULAR
    assert singular.rejected
    assert singular.witness_count == singular.violation_count == 108
    assert singular.max_signal == 0.0

    seed = controls["known_distance2_seed_not_silently_L1"]
    assert seed.classification == STAGE15F_DISTANCE2
    assert seed.rejected
    assert seed.max_signal == 2.0


def test_stage15f_criterion_46_structure_graph_smearing_jacobi_and_cross_orbit_controls_are_discriminating():
    controls = _by_id()

    structure = controls["kappa_zero_structure_function_removal"]
    assert structure.classification == STAGE15F_STRUCTURE_REMOVED
    assert structure.rejected
    assert "baseline_nonzero=72" in structure.detail
    assert "kappa0_nonzero=0" in structure.detail

    deletion = controls["delete_middle_site_generator_rank"]
    assert deletion.classification == STAGE15F_DISCONNECTED
    assert deletion.rejected
    assert deletion.max_signal == 2.0

    disconnected = controls["deleted_site_0_to_2_false_path"]
    assert disconnected.classification == STAGE15F_DISCONNECTED
    assert disconnected.rejected

    smearing = controls["wrong_smearing_antisymmetry_sign"]
    assert smearing.classification == STAGE15F_SMEARING
    assert smearing.rejected
    assert smearing.witness_count == 648
    assert smearing.violation_count == 360
    assert smearing.max_signal > 0.0

    jacobi = controls["jacobi_violating_epsilon_T2_anomaly"]
    assert jacobi.classification == STAGE15F_ANOMALY
    assert jacobi.rejected
    assert jacobi.witness_count == jacobi.violation_count == 108
    assert abs(jacobi.max_signal - 0.125) <= 1e-12

    cross = controls["cross_orbit_local_path_false_positive"]
    assert cross.classification == STAGE15F_CROSS_ORBIT
    assert cross.rejected
    assert cross.witness_count == cross.violation_count == 8748
    assert cross.max_signal == 0.0


def test_stage15f_criterion_47_incomplete_relational_and_all_typed_public_corruptions_are_detected():
    controls = _by_id()

    incomplete = controls["one_clock_omitted_relational_expression"]
    assert incomplete.classification == STAGE15F_INCOMPLETE_RELATIONAL
    assert incomplete.rejected
    assert incomplete.witness_count == incomplete.violation_count == 108
    assert abs(incomplete.max_signal - 2.0) <= 1e-12

    typed_ids = {
        "representative_dependent_O_corruption": STAGE15F_REP_PAYLOAD,
        "path_dependent_P_corruption": STAGE15F_PATH_PAYLOAD,
        "basis_dependent_R_corruption": STAGE15F_BASIS_PAYLOAD,
        "representative_dependent_V_corruption": STAGE15F_REP_PAYLOAD,
    }
    for control_id, classification in typed_ids.items():
        item = controls[control_id]
        assert item.classification == classification
        assert item.rejected
        assert item.witness_count == item.violation_count == 1


def test_stage15f_diagnostics_close_only_criteria_44_through_47():
    diagnostics = stage15f_diagnostics()
    assert diagnostics.control_count == 15
    assert diagnostics.rejected_control_count == 15
    assert diagnostics.required_vocabulary_count == 10
    assert diagnostics.required_vocabulary_covered
    assert diagnostics.structure_baseline_nonzero_count == 72
    assert diagnostics.structure_removed_nonzero_count == 0
    assert diagnostics.deleted_middle_generator_min_rank == 2
    assert diagnostics.disconnected_path_rejected
    assert diagnostics.locality_basis_control_count == 4
    assert diagnostics.locality_basis_rejected_count == 4
    assert diagnostics.smearing_corruption_probe_count == 648
    assert diagnostics.smearing_corruption_detected_count == 360
    assert diagnostics.max_smearing_antisymmetry_signal > 0.0
    assert diagnostics.jacobi_anomaly_probe_count == 108
    assert diagnostics.jacobi_anomaly_detected_count == 108
    assert abs(diagnostics.max_jacobi_anomaly_signal - 0.125) <= 1e-12
    assert diagnostics.cross_orbit_rejected_count == 8748
    assert diagnostics.incomplete_relational_group_count == 108
    assert diagnostics.incomplete_relational_rejected_count == 108
    assert diagnostics.typed_corruption_control_count == 4
    assert diagnostics.typed_corruption_detected_count == 4
    assert not diagnostics.known_seed_one_step_l1
    assert diagnostics.known_seed_lfinite_depth == 2
    assert diagnostics.all_controls_rejected
    assert diagnostics.criteria_44_47_satisfied


def test_stage15f_summary_preserves_control_and_interpretation_boundaries():
    summary = stage15f_summary()
    assert summary["control_count"] == 15
    assert summary["rejected_control_count"] == 15
    assert summary["required_vocabulary_covered"]
    assert summary["criteria_44_47_satisfied"]
    assert summary["bounded_result"] == STAGE15F_BOUNDED_RESULT
    guards = set(summary["guards"])
    for phrase in (
        "negative-control rejection != proof of continuum correctness",
        "graph disconnection control != relativistic causal disconnection",
        "locality-breaking detection != physical causal locality",
        "constraint-algebra anomaly detection != quantum anomaly theorem",
        "cross-orbit rejection != ontological superselection",
        "incomplete relational rejection != ontological becoming",
        "typed corruption detection != ontological equivalence",
        "local Abelianization surviving controls != physical triviality",
        "known seed non-L1 classification != universal nonlocality of Abelianization",
        "spatially indexed constraint precursor != general relativity",
        "repository validation != new scientific evidence",
    ):
        assert phrase in guards
