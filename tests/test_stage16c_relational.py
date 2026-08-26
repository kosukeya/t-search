from t_search.stage16_relational import *


def test_stage16c_strong_dirac_pair_and_exact_quotient():
    d=stage16c_diagnostics()
    assert d.strong_commutation_point_count==648
    assert d.strong_commutation_bracket_count==5184
    assert d.max_dirac_bracket_residual<=STAGE16C_ATOL
    assert d.strong_dirac_invariance_established
    assert d.quotient_class_count==4
    assert d.min_class_size==d.max_class_size==81
    assert d.quotient_exactly_four_by_eighty_one


def test_stage16c_orbit_discrimination_and_cross_orbit_rejection():
    d=stage16c_diagnostics()
    assert d.orbit_pair_count==6
    assert d.physically_distinct_orbit_pair_count==6
    assert d.min_orbit_pair_separation==0.5
    assert d.cross_orbit_ordered_pair_count==78732
    assert d.cross_orbit_rejected_count==78732
    assert d.orbit_discrimination_established


def test_stage16c_presented_generator_atlas_connects_every_orbit():
    d=stage16c_diagnostics(); spokes=canonical_stage16c_reachability_spokes()
    assert len(spokes)==320
    assert d.reachability_spoke_success_count==320
    assert d.derived_same_orbit_ordered_pair_count==26244
    assert d.max_reachability_parameter<2.0
    assert d.max_reachability_residual<=STAGE16C_ATOL
    assert d.max_reachability_inverse_residual<=STAGE16C_ATOL
    assert d.same_orbit_reachability_established


def test_stage16c_complete_four_clock_relational_observable_is_exhaustive_and_nontrivial():
    d=stage16c_diagnostics()
    assert d.complete_relational_evaluation_count==26244
    assert d.max_complete_target_residual<=STAGE16C_ATOL
    assert d.min_complete_relational_spread==5.0
    assert d.max_complete_relational_spread==5.0
    assert d.complete_relational_established
    assert d.nontrivial_relational_change_established


def test_stage16c_local_and_smeared_compensated_path_descent():
    d=stage16c_diagnostics()
    assert d.local_path_count==2592
    assert d.local_relational_comparison_count==209952
    assert d.smeared_path_count==2592
    assert d.smeared_relational_comparison_count==209952
    assert d.max_local_dirac_residual<=STAGE16C_ATOL
    assert d.max_local_relational_residual<=STAGE16C_ATOL
    assert d.max_smeared_dirac_residual<=STAGE16C_ATOL
    assert d.max_smeared_relational_residual<=STAGE16C_ATOL
    assert d.local_path_descent_established
    assert d.smeared_path_descent_established


def test_stage16c_omitted_clock_and_raw_q_controls_are_rejected():
    d=stage16c_diagnostics()
    assert d.omitted_clock_evaluation_count==1296
    assert d.omitted_clock_group_count==16
    assert d.omitted_clock_incomplete_group_count==16
    assert all(abs(a-b)<=STAGE16C_ATOL for a,b in zip(d.omitted_clock_spreads,(2.0,1.0,0.5,1.5),strict=True))
    assert d.raw_q_evaluation_count==324
    assert d.raw_q_group_count==4
    assert d.raw_q_nondescending_group_count==4
    assert d.min_raw_q_spread==d.max_raw_q_spread==5.0
    assert d.omitted_clock_controls_rejected
    assert d.raw_q_control_rejected


def test_stage16c_criteria_25_31_and_guards():
    d=stage16c_diagnostics()
    assert d.criteria_25_31_satisfied
    for guard in (
        "complete relational observable != ontological becoming by definition",
        "Dirac-invariant data + relational change != proof of eternalism",
        "same-orbit reachability != ontological identity",
        "quotient class != ontological world",
        "compensated path descent != refoliation invariance",
        "repository validation != new scientific evidence",
    ):
        assert guard in STAGE16C_GUARDS
