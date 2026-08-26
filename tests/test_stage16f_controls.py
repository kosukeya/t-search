from t_search.stage16_controls import (
    STAGE16F_ANOMALY,
    STAGE16F_BOUNDED_RESULT,
    STAGE16F_CROSS_ORBIT,
    STAGE16F_CYCLE_OPENING,
    STAGE16F_DISCONNECTED,
    STAGE16F_GLOBAL_SEED,
    STAGE16F_GUARDS,
    STAGE16F_INCOMPLETE_RELATIONAL,
    STAGE16F_INVERSE_NONLOCAL,
    STAGE16F_NUMERICAL_ONLY,
    STAGE16F_OPPOSITE_SITE,
    STAGE16F_REQUIRED_VOCABULARY,
    STAGE16F_SINGULAR,
    STAGE16F_SMEARING,
    STAGE16F_STRUCTURE_REMOVED,
    STAGE16F_SUPPORT_EXPANSION,
    STAGE16F_THREE_CYCLE,
    STAGE16F_TYPED,
    STAGE16F_WRONG_COMPENSATOR,
    canonical_stage16f_controls,
    stage16f_diagnostics,
    stage16f_summary,
)


def _by_id():
    return {x.control_id: x for x in canonical_stage16f_controls()}


def test_stage16f_full_frozen_control_inventory_rejects_and_covers_vocabulary():
    controls = canonical_stage16f_controls()
    assert len(controls) == 20
    assert all(x.rejected for x in controls)
    assert set(STAGE16F_REQUIRED_VOCABULARY) <= {x.classification for x in controls}


def test_stage16f_topology_controls_exhibit_closed_vs_open_locality_pressure():
    by = _by_id()
    opening = by["wrap_edge_opening_depth2_peeling"]
    projection = by["three_site_projection_recovers_stage15_pattern"]
    c3 = by["three_cycle_radius1_is_global"]
    disconnected = by["disconnected_0_to_3_false_path"]
    assert opening.classification == STAGE16F_CYCLE_OPENING and opening.rejected
    assert "depth=2" in opening.detail
    assert projection.classification == STAGE16F_CYCLE_OPENING and projection.rejected
    assert projection.max_signal == 1.0
    assert c3.classification == STAGE16F_THREE_CYCLE and c3.violation_count == 3
    assert disconnected.classification == STAGE16F_DISCONNECTED and disconnected.rejected


def test_stage16f_locality_and_singular_controls_reject_false_l1_labels():
    by = _by_id()
    assert by["opposite_generator_support_expansion"].classification == STAGE16F_SUPPORT_EXPANSION
    assert by["opposite_site_coefficient_dependency"].classification == STAGE16F_OPPOSITE_SITE
    assert by["forward_local_inverse_dense_cycle_map"].classification == STAGE16F_INVERSE_NONLOCAL
    assert by["forward_local_inverse_dense_cycle_map"].violation_count == 4
    assert by["known_global_seed_not_silently_L1"].classification == STAGE16F_GLOBAL_SEED
    assert by["known_global_seed_not_silently_L1"].violation_count == 4
    assert by["kappa1_all_ones_singular_cycle_frame"].classification == STAGE16F_SINGULAR
    assert by["kappa1_all_ones_singular_cycle_frame"].max_signal <= 1e-12


def test_stage16f_algebra_path_and_numerical_only_controls_reject():
    by = _by_id()
    assert by["kappa_zero_structure_function_removal"].classification == STAGE16F_STRUCTURE_REMOVED
    assert by["wrong_smearing_reverse_sign"].classification == STAGE16F_SMEARING
    assert by["wrong_smearing_reverse_sign"].violation_count > 0
    assert by["jacobi_violating_epsilon_T2_anomaly"].classification == STAGE16F_ANOMALY
    assert by["jacobi_violating_epsilon_T2_anomaly"].violation_count == by["jacobi_violating_epsilon_T2_anomaly"].witness_count == 324
    assert by["missing_or_wrong_sign_local_compensator"].classification == STAGE16F_WRONG_COMPENSATOR
    assert by["missing_or_wrong_sign_local_compensator"].violation_count == 2592
    assert by["single_zero_clock_sample_claims_strong_commutation"].classification == STAGE16F_NUMERICAL_ONLY
    assert by["single_zero_clock_sample_claims_strong_commutation"].max_signal > 1e-10


def test_stage16f_quotient_relational_and_typed_corruptions_reject():
    controls = canonical_stage16f_controls()
    by = _by_id()
    cross = by["cross_orbit_path_false_positive"]
    assert cross.classification == STAGE16F_CROSS_ORBIT
    assert cross.witness_count == cross.violation_count == 78732
    incomplete = by["single_clock_omission_four_clock_relational"]
    assert incomplete.classification == STAGE16F_INCOMPLETE_RELATIONAL
    assert incomplete.witness_count == incomplete.violation_count == 16
    typed = [x for x in controls if x.classification == STAGE16F_TYPED]
    assert len(typed) == 4
    assert all(x.rejected and x.violation_count == 1 for x in typed)


def test_stage16f_diagnostics_close_only_criteria_45_47_and_preserve_guards():
    d = stage16f_diagnostics()
    assert d.control_count == 20
    assert d.rejected_control_count == 20
    assert d.required_vocabulary_count == 16
    assert d.required_vocabulary_covered
    assert d.cycle_opening_exhibited_depth == 2
    assert d.three_site_projection_one_step_l1
    assert d.typed_corruption_control_count == d.typed_corruption_detected_count == 4
    assert d.all_controls_rejected
    assert d.criteria_45_47_satisfied
    summary = stage16f_summary()
    assert summary["criteria_45_47_satisfied"]
    assert summary["bounded_result"] == STAGE16F_BOUNDED_RESULT
    guards = set(STAGE16F_GUARDS)
    for expected in (
        "cycle opening changes graph topology != proof that topology is ontic",
        "three-cycle L1 label != nontrivial locality evidence",
        "incomplete relational rejection != ontological becoming",
        "typed corruption detection != ontological equivalence",
        "repository validation != new scientific evidence",
    ):
        assert expected in guards
