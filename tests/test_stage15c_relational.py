import math

from t_search.stage15_local import STAGE15A_ATOL, canonical_stage15a_off_surface_probes
from t_search.stage15_relational import (
    STAGE15C_OMITTED_CLOCK_CLASSIFICATION,
    STAGE15C_RAW_Q_CLASSIFICATION,
    canonical_stage15c_complete_relational_evaluations,
    canonical_stage15c_dirac_estimates,
    canonical_stage15c_local_path_relational_comparisons,
    canonical_stage15c_omitted_clock_evaluations,
    canonical_stage15c_raw_Q_evaluations,
    canonical_stage15c_smeared_path_relational_comparisons,
    stage15c_complete_relational_spreads,
    stage15c_cross_orbit_arrow_audit,
    stage15c_diagnostics,
    stage15c_dirac_bracket_residuals,
    stage15c_omitted_clock_group_spreads,
    stage15c_orbit_dirac_summaries,
    stage15c_orbit_pair_discriminations,
    stage15c_quotient_classes,
    stage15c_raw_Q_spreads,
)


def test_stage15c_reconstructs_dirac_pair_and_strongly_commutes_on_and_off_surface():
    estimates = canonical_stage15c_dirac_estimates()
    summaries = stage15c_orbit_dirac_summaries()
    assert len(estimates) == 108
    assert len(summaries) == 4
    assert all(item.representative_count == 27 for item in summaries)
    assert max(item.Q_declared_residual for item in estimates) <= STAGE15A_ATOL
    assert max(item.P_declared_residual for item in estimates) <= STAGE15A_ATOL
    assert max(item.Q_D_spread for item in summaries) <= STAGE15A_ATOL
    assert max(item.P_D_spread for item in summaries) <= STAGE15A_ATOL
    assert max(
        max((*item.bracket_Q_residuals, *item.bracket_P_residuals))
        for item in estimates
    ) <= STAGE15A_ATOL

    off_surface = canonical_stage15a_off_surface_probes()
    assert len(off_surface) == 108
    assert max(
        max(stage15c_dirac_bracket_residuals(point)) for point in off_surface
    ) <= STAGE15A_ATOL


def test_stage15c_full_dirac_pair_separates_all_six_sampled_physical_orbit_pairs():
    pairs = stage15c_orbit_pair_discriminations()
    assert len(pairs) == 6
    assert all(item.physically_distinct for item in pairs)
    assert min(item.full_pair_separation for item in pairs) >= 0.5 - STAGE15A_ATOL
    assert sum(item.same_P_different_Q for item in pairs) == 1
    assert sum(item.same_Q_different_P for item in pairs) == 1


def test_stage15c_complete_three_clock_relational_observable_descends_and_changes():
    evaluations = canonical_stage15c_complete_relational_evaluations()
    assert len(evaluations) == 2916
    assert len({(item.tau0, item.tau1, item.tau2) for item in evaluations}) == 27
    assert max(item.target_residual for item in evaluations) <= STAGE15A_ATOL
    spreads = stage15c_complete_relational_spreads()
    assert len(spreads) == 4
    assert all(math.isclose(spread, 3.5, abs_tol=STAGE15A_ATOL) for _, spread in spreads)


def test_stage15c_local_compensated_paths_descend_to_same_complete_relational_values():
    comparisons = canonical_stage15c_local_path_relational_comparisons()
    assert len(comparisons) == 23328
    assert len({item.pair_id for item in comparisons}) == 864
    assert max(item.endpoint_order_residual for item in comparisons) <= STAGE15A_ATOL
    assert max(
        max(
            item.relational_order_residual,
            item.path_012_target_residual,
            item.path_102_target_residual,
        )
        for item in comparisons
    ) <= STAGE15A_ATOL


def test_stage15c_smeared_predicted_compensation_descends_to_complete_relational_values():
    comparisons = canonical_stage15c_smeared_path_relational_comparisons()
    assert len(comparisons) == 14580
    assert len({(item.representative_id, item.case_id) for item in comparisons}) == 540
    assert max(item.endpoint_residual for item in comparisons) <= STAGE15A_ATOL
    assert max(
        max(
            item.relational_order_residual,
            item.nm_target_residual,
            item.compensated_target_residual,
        )
        for item in comparisons
    ) <= STAGE15A_ATOL


def test_stage15c_omitting_any_one_clock_condition_leaves_explicit_gauge_dependence():
    evaluations = canonical_stage15c_omitted_clock_evaluations()
    spreads = stage15c_omitted_clock_group_spreads()
    assert len(evaluations) == 324
    assert len(spreads) == 108
    assert all(item.classification == STAGE15C_OMITTED_CLOCK_CLASSIFICATION for item in evaluations)
    assert all(spread > STAGE15A_ATOL for _, _, _, spread in spreads)

    expected = {0: 2.0, 1: 1.0, 2: 0.5}
    for omitted, target in expected.items():
        assert all(
            math.isclose(spread, target, abs_tol=STAGE15A_ATOL)
            for _, index, _, spread in spreads
            if index == omitted
        )


def test_stage15c_raw_Q_coordinate_does_not_descend_to_the_sampled_quotient():
    evaluations = canonical_stage15c_raw_Q_evaluations()
    spreads = stage15c_raw_Q_spreads()
    assert len(evaluations) == 108
    assert len(spreads) == 4
    assert all(item.classification == STAGE15C_RAW_Q_CLASSIFICATION for item in evaluations)
    assert all(math.isclose(spread, 3.5, abs_tol=STAGE15A_ATOL) for _, spread in spreads)


def test_stage15c_sampled_quotient_is_exactly_four_classes_of_27_and_rejects_cross_orbit_paths():
    classes = stage15c_quotient_classes()
    licensed, rejected = stage15c_cross_orbit_arrow_audit()
    assert len(classes) == 4
    assert all(len(item.member_representative_ids) == 27 for item in classes)
    assert all(len(item.member_orbit_ids) == 1 for item in classes)
    assert licensed == 0
    assert rejected == 8748


def test_stage15c_diagnostics_close_only_criteria_25_through_31():
    diagnostics = stage15c_diagnostics()
    assert diagnostics.representative_count == 108
    assert diagnostics.dirac_estimate_count == 108
    assert diagnostics.strong_commutation_probe_count == 216
    assert diagnostics.orbit_summary_count == 4
    assert diagnostics.distinct_orbit_pair_count == 6
    assert diagnostics.physically_distinct_pair_count == 6
    assert diagnostics.complete_relational_evaluation_count == 2916
    assert diagnostics.local_compensated_pair_count == 864
    assert diagnostics.local_relational_comparison_count == 23328
    assert diagnostics.smeared_ordering_count == 540
    assert diagnostics.smeared_relational_comparison_count == 14580
    assert diagnostics.omitted_clock_evaluation_count == 324
    assert diagnostics.omitted_clock_group_count == 108
    assert diagnostics.omitted_clock_incomplete_group_count == 108
    assert diagnostics.raw_Q_evaluation_count == 108
    assert diagnostics.raw_Q_group_count == 4
    assert diagnostics.raw_Q_nondescending_group_count == 4
    assert diagnostics.quotient_class_count == 4
    assert diagnostics.min_quotient_class_size == 27
    assert diagnostics.max_quotient_class_size == 27
    assert diagnostics.cross_orbit_licensed_arrow_count == 0
    assert diagnostics.cross_orbit_rejected_count == 8748
    assert diagnostics.same_P_different_Q_control_count == 1
    assert diagnostics.same_Q_different_P_control_count == 1
    assert diagnostics.max_dirac_bracket_residual <= STAGE15A_ATOL
    assert diagnostics.min_distinct_orbit_full_pair_separation >= 0.5 - STAGE15A_ATOL
    assert diagnostics.max_complete_relational_target_residual <= STAGE15A_ATOL
    assert diagnostics.max_local_endpoint_order_residual <= STAGE15A_ATOL
    assert diagnostics.max_local_relational_residual <= STAGE15A_ATOL
    assert diagnostics.max_smeared_endpoint_residual <= STAGE15A_ATOL
    assert diagnostics.max_smeared_relational_residual <= STAGE15A_ATOL
    assert all(
        math.isclose(observed, expected, abs_tol=STAGE15A_ATOL)
        for observed, expected in zip(
            diagnostics.omitted_clock_spreads, (2.0, 1.0, 0.5), strict=True
        )
    )
    assert math.isclose(diagnostics.min_raw_Q_spread, 3.5, abs_tol=STAGE15A_ATOL)
    assert math.isclose(diagnostics.max_raw_Q_spread, 3.5, abs_tol=STAGE15A_ATOL)
    assert diagnostics.strong_dirac_commutation_established
    assert diagnostics.nontrivial_complete_relational_change
    assert diagnostics.local_path_relational_descent_established
    assert diagnostics.smeared_path_relational_descent_established
    assert diagnostics.omitted_clock_incompleteness_explicit
    assert diagnostics.raw_coordinate_non_descent_explicit
    assert diagnostics.quotient_exactly_four_by_twenty_seven
    assert diagnostics.metaphysical_boundary_explicit
    assert diagnostics.criteria_25_31_satisfied
