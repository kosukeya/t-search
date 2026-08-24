import math

from t_search.stage14_relational import (
    STAGE14C_TWO_CLOCK_CLASSIFICATION,
    canonical_stage14c_compensated_relational_comparisons,
    canonical_stage14c_complete_relational_evaluations,
    canonical_stage14c_dirac_estimates,
    canonical_stage14c_two_clock_evaluations,
    stage14c_complete_relational_spreads,
    stage14c_cross_orbit_arrow_audit,
    stage14c_diagnostics,
    stage14c_orbit_dirac_summaries,
    stage14c_orbit_pair_discriminations,
    stage14c_quotient_classes,
    stage14c_two_clock_group_spreads,
)
from t_search.stage14_structure_function import STAGE14A_ATOL


def test_stage14c_reconstructs_dirac_pair_on_all_108_representatives():
    estimates = canonical_stage14c_dirac_estimates()
    summaries = stage14c_orbit_dirac_summaries()
    assert len(estimates) == 108
    assert len(summaries) == 4
    assert all(item.representative_count == 27 for item in summaries)
    assert max(item.Q_declared_residual for item in estimates) <= STAGE14A_ATOL
    assert max(item.P_declared_residual for item in estimates) <= STAGE14A_ATOL
    assert max(item.Q_D_spread for item in summaries) <= STAGE14A_ATOL
    assert max(item.P_D_spread for item in summaries) <= STAGE14A_ATOL
    assert max(
        max(
            item.bracket_Q_D_residual,
            item.bracket_Q_H1_residual,
            item.bracket_Q_H2_residual,
            item.bracket_P_D_residual,
            item.bracket_P_H1_residual,
            item.bracket_P_H2_residual,
        )
        for item in estimates
    ) <= STAGE14A_ATOL


def test_stage14c_full_dirac_pair_separates_all_six_physical_orbit_pairs():
    pairs = stage14c_orbit_pair_discriminations()
    assert len(pairs) == 6
    assert all(item.physically_distinct for item in pairs)
    assert min(item.full_pair_separation for item in pairs) >= 0.5 - STAGE14A_ATOL
    assert sum(item.same_P_different_Q for item in pairs) == 1
    assert sum(item.same_Q_different_P for item in pairs) == 1


def test_stage14c_three_condition_complete_relational_observable_descends_to_targets():
    evaluations = canonical_stage14c_complete_relational_evaluations()
    assert len(evaluations) == 2916
    assert len({(item.tau1, item.tau2, item.chi) for item in evaluations}) == 27
    assert max(item.target_residual for item in evaluations) <= STAGE14A_ATOL
    spreads = stage14c_complete_relational_spreads()
    assert len(spreads) == 4
    assert min(spread for _, spread in spreads) >= 3.0 - STAGE14A_ATOL
    assert max(spread for _, spread in spreads) >= 5.0 - STAGE14A_ATOL


def test_stage14c_complete_relational_values_are_independent_of_compensated_path_order():
    comparisons = canonical_stage14c_compensated_relational_comparisons()
    assert len(comparisons) == 23328
    assert len({item.pair_id for item in comparisons}) == 864
    assert max(
        max(
            item.path_order_residual,
            item.path_12_target_residual,
            item.path_21_target_residual,
        )
        for item in comparisons
    ) <= STAGE14A_ATOL


def test_stage14c_two_clock_expression_retains_third_direction_gauge_dependence():
    evaluations = canonical_stage14c_two_clock_evaluations()
    spreads = stage14c_two_clock_group_spreads()
    assert len(evaluations) == 108
    assert len(spreads) == 36
    assert all(item.classification == STAGE14C_TWO_CLOCK_CLASSIFICATION for item in evaluations)
    assert all(spread > STAGE14A_ATOL for _, _, _, spread in spreads)
    assert math.isclose(min(spread for _, _, _, spread in spreads), 1.0, abs_tol=STAGE14A_ATOL)
    assert math.isclose(max(spread for _, _, _, spread in spreads), 1.0, abs_tol=STAGE14A_ATOL)


def test_stage14c_sampled_quotient_is_exactly_four_classes_of_27_with_no_cross_orbit_arrows():
    classes = stage14c_quotient_classes()
    licensed, rejected = stage14c_cross_orbit_arrow_audit()
    assert len(classes) == 4
    assert all(len(item.member_representative_ids) == 27 for item in classes)
    assert all(len(item.member_orbit_ids) == 1 for item in classes)
    assert licensed == 0
    assert rejected == 8748


def test_stage14c_diagnostics_close_only_criteria_25_through_31():
    diagnostics = stage14c_diagnostics()
    assert diagnostics.representative_count == 108
    assert diagnostics.dirac_estimate_count == 108
    assert diagnostics.orbit_summary_count == 4
    assert diagnostics.distinct_orbit_pair_count == 6
    assert diagnostics.physically_distinct_pair_count == 6
    assert diagnostics.complete_relational_evaluation_count == 2916
    assert diagnostics.compensated_pair_count == 864
    assert diagnostics.compensated_path_relational_comparison_count == 23328
    assert diagnostics.two_clock_evaluation_count == 108
    assert diagnostics.two_clock_group_count == 36
    assert diagnostics.two_clock_incomplete_group_count == 36
    assert diagnostics.quotient_class_count == 4
    assert diagnostics.min_quotient_class_size == 27
    assert diagnostics.max_quotient_class_size == 27
    assert diagnostics.cross_orbit_licensed_arrow_count == 0
    assert diagnostics.cross_orbit_rejected_count == 8748
    assert diagnostics.same_P_different_Q_control_count == 1
    assert diagnostics.same_Q_different_P_control_count == 1
    assert diagnostics.nontrivial_complete_relational_change
    assert diagnostics.two_clock_incompleteness_explicit
    assert diagnostics.quotient_exactly_four_by_twenty_seven
    assert diagnostics.metaphysical_boundary_explicit
    assert diagnostics.criteria_25_31_satisfied
