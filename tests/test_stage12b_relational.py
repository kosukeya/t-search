import numpy as np

from t_search.stage12_multi_orbit import (
    STAGE12A_ATOL,
    STAGE12A_OMEGA_ALPHA,
    STAGE12A_OMEGA_BETA,
    STAGE12A_OMEGA_GAMMA,
    canonical_stage12a_orbits,
    canonical_stage12a_representatives_for_orbit,
)
from t_search.stage12_relational import (
    STAGE12B_DIFFERENT_ORBIT,
    STAGE12B_FALSE_POSITIVE_REJECTED,
    STAGE12B_TAU_VALUES,
    canonical_stage12b_derivative_evaluations,
    canonical_stage12b_dirac_estimates,
    canonical_stage12b_external_dirac_estimates,
    canonical_stage12b_orbit_comparisons,
    canonical_stage12b_relational_evaluations,
    stage12b_compare_orbits,
    stage12b_diagnostics,
    stage12b_dirac_from_representative,
    stage12b_false_match_control,
)


def _orbits_by_id():
    return {orbit.orbit_id: orbit for orbit in canonical_stage12a_orbits()}


def test_stage12b_dirac_invariants_are_independently_recomputed_from_phase_space() -> None:
    estimates = canonical_stage12b_dirac_estimates()
    assert len(estimates) == 20
    assert all(item.provenance.startswith("independently recomputed") for item in estimates)
    assert max(item.stored_Q_D_residual for item in estimates) <= STAGE12A_ATOL
    assert max(item.stored_P_D_residual for item in estimates) <= STAGE12A_ATOL
    assert max(item.constraint_residual for item in estimates) <= STAGE12A_ATOL

    for orbit in canonical_stage12a_orbits():
        representatives = canonical_stage12a_representatives_for_orbit(orbit)
        for representative in representatives:
            estimate = stage12b_dirac_from_representative(representative)
            assert np.isclose(estimate.Q_D, representative.q - representative.p * representative.T)
            assert np.isclose(estimate.P_D, representative.p)
            assert np.isclose(estimate.Q_D, orbit.Q_D, atol=STAGE12A_ATOL, rtol=0.0)
            assert np.isclose(estimate.P_D, orbit.P_D, atol=STAGE12A_ATOL, rtol=0.0)


def test_stage12b_same_orbit_representatives_agree_in_both_dirac_invariants() -> None:
    estimates = canonical_stage12b_dirac_estimates()
    for orbit in canonical_stage12a_orbits():
        subset = [item for item in estimates if item.orbit_id == orbit.orbit_id]
        assert len(subset) == 5
        assert max(abs(item.Q_D - orbit.Q_D) for item in subset) <= STAGE12A_ATOL
        assert max(abs(item.P_D - orbit.P_D) for item in subset) <= STAGE12A_ATOL


def test_stage12b_external_parameterizations_recover_the_same_dirac_pair() -> None:
    estimates = canonical_stage12b_external_dirac_estimates()
    orbit_by_id = _orbits_by_id()
    assert len(estimates) == 16
    for item in estimates:
        orbit = orbit_by_id[item.orbit_id]
        assert item.max_Q_D_spread <= STAGE12A_ATOL
        assert item.max_P_D_spread <= STAGE12A_ATOL
        assert np.isclose(item.Q_D, orbit.Q_D, atol=STAGE12A_ATOL, rtol=0.0)
        assert np.isclose(item.P_D, orbit.P_D, atol=STAGE12A_ATOL, rtol=0.0)


def test_stage12b_all_canonical_distinct_orbits_are_not_gauge_collapsed() -> None:
    comparisons = canonical_stage12b_orbit_comparisons()
    assert len(comparisons) == 6
    assert all(not item.full_dirac_pair_equal for item in comparisons)
    assert all(item.classification == STAGE12B_DIFFERENT_ORBIT for item in comparisons)


def test_stage12b_same_P_and_same_Q_single_invariant_controls_are_rejected() -> None:
    orbit_by_id = _orbits_by_id()
    alpha_beta = stage12b_compare_orbits(
        orbit_by_id[STAGE12A_OMEGA_ALPHA], orbit_by_id[STAGE12A_OMEGA_BETA]
    )
    assert alpha_beta.P_D_equal
    assert not alpha_beta.Q_D_equal
    assert not alpha_beta.full_dirac_pair_equal
    assert alpha_beta.single_invariant_match == "P_D_only"
    assert alpha_beta.classification == STAGE12B_DIFFERENT_ORBIT

    alpha_gamma = stage12b_compare_orbits(
        orbit_by_id[STAGE12A_OMEGA_ALPHA], orbit_by_id[STAGE12A_OMEGA_GAMMA]
    )
    assert alpha_gamma.Q_D_equal
    assert not alpha_gamma.P_D_equal
    assert not alpha_gamma.full_dirac_pair_equal
    assert alpha_gamma.single_invariant_match == "Q_D_only"
    assert alpha_gamma.classification == STAGE12B_DIFFERENT_ORBIT


def test_stage12b_relational_q_is_reconstructed_from_every_representative_and_external_chart() -> None:
    evaluations = canonical_stage12b_relational_evaluations()
    assert STAGE12B_TAU_VALUES == (-1.25, -0.25, 0.75, 1.50)
    assert len(evaluations) == 144
    assert {item.source_kind for item in evaluations} == {
        "gauge_representative",
        "external_parameterization",
    }
    assert {item.orbit_id for item in evaluations} == {
        orbit.orbit_id for orbit in canonical_stage12a_orbits()
    }
    assert max(item.residual for item in evaluations) <= STAGE12A_ATOL

    # Nontrivial relational change is present on every physical orbit.
    for orbit in canonical_stage12a_orbits():
        values = [
            item.reconstructed_q
            for item in evaluations
            if item.orbit_id == orbit.orbit_id
            and item.source_kind == "gauge_representative"
            and item.source_id.endswith("rep_00")
        ]
        assert len(values) == len(STAGE12B_TAU_VALUES)
        assert len({round(value, 12) for value in values}) == len(values)


def test_stage12b_relational_derivative_equals_P_D_across_representatives_and_parameterizations() -> None:
    evaluations = canonical_stage12b_derivative_evaluations()
    assert len(evaluations) == 232
    assert {item.source_kind for item in evaluations} == {
        "gauge_representative_pair",
        "external_parameterization_interval",
    }
    assert max(item.residual for item in evaluations) <= STAGE12A_ATOL
    for item in evaluations:
        assert np.isclose(item.dq_dT, item.expected_P_D, atol=STAGE12A_ATOL, rtol=0.0)


def test_stage12b_equal_label_and_equal_single_variable_false_matches_are_rejected() -> None:
    control = stage12b_false_match_control()
    assert control.same_P_different_Q_rejected
    assert control.same_Q_different_P_rejected
    assert control.equal_T_cross_orbit_match_count == 30
    assert control.equal_q_cross_orbit_match_count == 2
    assert control.equal_raw_lambda_cross_orbit_match_count == 312
    assert control.all_equal_single_variable_matches_rejected
    assert control.classification == STAGE12B_FALSE_POSITIVE_REJECTED


def test_stage12b_diagnostics_close_criteria_17_through_23() -> None:
    diagnostics = stage12b_diagnostics()
    assert diagnostics.representative_dirac_estimate_count == 20
    assert diagnostics.external_dirac_estimate_count == 16
    assert diagnostics.physical_orbit_comparison_count == 6
    assert diagnostics.relational_evaluation_count == 144
    assert diagnostics.derivative_evaluation_count == 232
    assert diagnostics.max_independent_stored_Q_D_residual <= STAGE12A_ATOL
    assert diagnostics.max_independent_stored_P_D_residual <= STAGE12A_ATOL
    assert diagnostics.max_same_orbit_Q_D_residual <= STAGE12A_ATOL
    assert diagnostics.max_same_orbit_P_D_residual <= STAGE12A_ATOL
    assert diagnostics.max_external_Q_D_spread <= STAGE12A_ATOL
    assert diagnostics.max_external_P_D_spread <= STAGE12A_ATOL
    assert diagnostics.max_relational_q_residual <= STAGE12A_ATOL
    assert diagnostics.max_relational_derivative_residual <= STAGE12A_ATOL
    assert diagnostics.distinct_orbits_not_collapsed
    assert diagnostics.same_P_different_Q_control_passed
    assert diagnostics.same_Q_different_P_control_passed
    assert diagnostics.equal_T_cross_orbit_match_count == 30
    assert diagnostics.equal_q_cross_orbit_match_count == 2
    assert diagnostics.equal_raw_lambda_cross_orbit_match_count == 312
    assert diagnostics.false_match_controls_rejected
    assert diagnostics.criteria_17_23_satisfied
