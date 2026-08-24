import math

from t_search.stage13_multi_constraint import STAGE13A_ATOL, canonical_stage13a_orbits
from t_search.stage13_relational import (
    STAGE13C_COMPLETE_RELATIONAL_ROLE,
    STAGE13C_DIRAC_ROLE,
    STAGE13C_METAPHYSICAL_CLAIM_STATUS,
    STAGE13C_ONE_CLOCK_CLASSIFICATION,
    STAGE13C_PATH_COVARIANCE,
    canonical_stage13c_compensated_relational_comparisons,
    canonical_stage13c_complete_relational_evaluations,
    canonical_stage13c_dirac_estimates,
    canonical_stage13c_one_clock_evaluations,
    stage13c_diagnostics,
    stage13c_one_clock_group_spreads,
    stage13c_orbit_dirac_summaries,
    stage13c_orbit_pair_discriminations,
)


def test_stage13c_reconstructs_dirac_pair_from_all_36_representatives() -> None:
    estimates = canonical_stage13c_dirac_estimates()
    assert len(estimates) == 36
    assert all(item.role == STAGE13C_DIRAC_ROLE for item in estimates)
    assert max(item.Q_declared_residual for item in estimates) <= STAGE13A_ATOL
    assert max(item.P_declared_residual for item in estimates) <= STAGE13A_ATOL


def test_stage13c_dirac_pair_commutes_with_both_positive_constraints() -> None:
    estimates = canonical_stage13c_dirac_estimates()
    residual = max(
        max(
            item.bracket_Q_KT_residual,
            item.bracket_Q_KX_residual,
            item.bracket_P_KT_residual,
            item.bracket_P_KX_residual,
        )
        for item in estimates
    )
    assert residual <= STAGE13A_ATOL


def test_stage13c_same_orbit_representatives_agree_in_full_dirac_pair() -> None:
    summaries = stage13c_orbit_dirac_summaries()
    assert len(summaries) == 4
    assert all(item.representative_count == 9 for item in summaries)
    assert max(item.Q_D_spread for item in summaries) <= STAGE13A_ATOL
    assert max(item.P_D_spread for item in summaries) <= STAGE13A_ATOL


def test_stage13c_all_six_physical_orbit_pairs_remain_distinct() -> None:
    pairs = stage13c_orbit_pair_discriminations()
    assert len(pairs) == 6
    assert all(item.physically_distinct for item in pairs)
    assert math.isclose(min(item.full_pair_separation for item in pairs), 0.5, abs_tol=1e-12)


def test_stage13c_same_p_different_q_and_same_q_different_p_controls_remain_explicit() -> None:
    pairs = stage13c_orbit_pair_discriminations()
    assert sum(item.same_P_different_Q for item in pairs) == 1
    assert sum(item.same_Q_different_P for item in pairs) == 1


def test_stage13c_two_clock_complete_observable_is_representative_independent() -> None:
    evaluations = canonical_stage13c_complete_relational_evaluations()
    assert len(evaluations) == 324
    assert all(item.role == STAGE13C_COMPLETE_RELATIONAL_ROLE for item in evaluations)
    assert max(item.target_residual for item in evaluations) <= STAGE13A_ATOL

    for orbit in canonical_stage13a_orbits():
        for tau in (-1.0, 0.0, 1.0):
            for chi in (-1.0, 0.0, 1.0):
                values = [
                    item.q_complete
                    for item in evaluations
                    if item.orbit_id == orbit.orbit_id and item.tau == tau and item.chi == chi
                ]
                assert len(values) == 9
                assert max(values) - min(values) <= STAGE13A_ATOL


def test_stage13c_complete_observable_agrees_across_all_compensated_path_choices() -> None:
    comparisons = canonical_stage13c_compensated_relational_comparisons()
    assert len(comparisons) == 1296
    assert all(item.classification == STAGE13C_PATH_COVARIANCE for item in comparisons)
    residual = max(
        max(item.TX_XT_residual, item.TX_target_residual, item.XT_target_residual)
        for item in comparisons
    )
    assert residual <= STAGE13A_ATOL


def test_stage13c_one_clock_expression_is_explicitly_incomplete() -> None:
    evaluations = canonical_stage13c_one_clock_evaluations()
    spreads = stage13c_one_clock_group_spreads()
    assert len(evaluations) == 36
    assert len(spreads) == 12
    assert all(item.classification == STAGE13C_ONE_CLOCK_CLASSIFICATION for item in evaluations)
    assert all(spread > STAGE13A_ATOL for _, _, spread in spreads)
    assert all(math.isclose(spread, 1.0, abs_tol=1e-12) for _, _, spread in spreads)


def test_stage13c_relational_change_does_not_license_metaphysical_claims() -> None:
    estimates = canonical_stage13c_dirac_estimates()
    complete = canonical_stage13c_complete_relational_evaluations()
    compensated = canonical_stage13c_compensated_relational_comparisons()
    one_clock = canonical_stage13c_one_clock_evaluations()
    assert all(
        item.metaphysical_claim_status == STAGE13C_METAPHYSICAL_CLAIM_STATUS
        for item in (*estimates, *complete, *compensated, *one_clock)
    )


def test_stage13c_diagnostics_close_criteria_24_31_only() -> None:
    diagnostics = stage13c_diagnostics()
    assert diagnostics.representative_count == 36
    assert diagnostics.dirac_estimate_count == 36
    assert diagnostics.orbit_summary_count == 4
    assert diagnostics.distinct_orbit_pair_count == 6
    assert diagnostics.physically_distinct_pair_count == 6
    assert diagnostics.complete_relational_evaluation_count == 324
    assert diagnostics.compensated_path_relational_comparison_count == 1296
    assert diagnostics.one_clock_evaluation_count == 36
    assert diagnostics.one_clock_group_count == 12
    assert diagnostics.one_clock_incomplete_group_count == 12
    assert diagnostics.same_P_different_Q_control_count == 1
    assert diagnostics.same_Q_different_P_control_count == 1
    assert math.isclose(diagnostics.min_distinct_orbit_full_pair_separation, 0.5, abs_tol=1e-12)
    assert math.isclose(diagnostics.min_one_clock_spread, 1.0, abs_tol=1e-12)
    assert math.isclose(diagnostics.max_one_clock_spread, 1.0, abs_tol=1e-12)
    assert diagnostics.nontrivial_complete_relational_change
    assert diagnostics.one_clock_incompleteness_explicit
    assert diagnostics.metaphysical_boundary_explicit
    assert diagnostics.criteria_24_31_satisfied
