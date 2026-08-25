import math

import pytest

from t_search.stage14_paths import (
    STAGE14B_PATH_12D,
    STAGE14B_PATH_21D,
    canonical_stage14b_cross_orbit_rejections,
    canonical_stage14b_mixed_pairs,
    canonical_stage14b_path_results,
    stage14b_apply_path,
    stage14b_diagnostics,
    stage14b_make_mixed_pair,
)
from t_search.stage14_structure_function import (
    STAGE14A_ATOL,
    canonical_stage14a_orbits,
    canonical_stage14a_representatives_for_orbit,
)


def test_stage14b_constructs_exact_frozen_864_pair_family():
    pairs = canonical_stage14b_mixed_pairs()
    assert len(pairs) == 864
    assert len({pair.pair_id for pair in pairs}) == 864
    assert all(pair.source.orbit_id == pair.target.orbit_id for pair in pairs)
    assert all(abs(pair.s) > STAGE14A_ATOL for pair in pairs)
    assert all(abs(pair.u) > STAGE14A_ATOL for pair in pairs)
    assert all(abs(pair.source.X - pair.target.X) > STAGE14A_ATOL for pair in pairs)


def test_stage14b_two_ordered_path_implementations_match_exact_raw_formulas():
    results = canonical_stage14b_path_results()
    assert len(results) == 1728
    assert {result.path_word for result in results} == {STAGE14B_PATH_12D, STAGE14B_PATH_21D}
    assert max(result.raw_formula_residual for result in results) <= STAGE14A_ATOL


def test_stage14b_exact_third_direction_compensation_closes_every_positive_pair():
    results = canonical_stage14b_path_results()
    assert max(result.final_endpoint_residual for result in results) <= STAGE14A_ATOL
    assert max(result.final_dirac_residual for result in results) <= STAGE14A_ATOL


def test_stage14b_compensator_identity_has_nontrivial_and_zero_difference_subfamilies():
    pairs = canonical_stage14b_mixed_pairs()
    nontrivial = [pair for pair in pairs if abs(pair.source.X) > STAGE14A_ATOL]
    zero_x = [pair for pair in pairs if abs(pair.source.X) <= STAGE14A_ATOL]
    assert len(nontrivial) == 576
    assert len(zero_x) == 288
    for pair in pairs:
        assert math.isclose(
            pair.compensator_difference,
            pair.expected_compensator_difference,
            rel_tol=0.0,
            abs_tol=STAGE14A_ATOL,
        )
    assert all(abs(pair.compensator_difference) > STAGE14A_ATOL for pair in nontrivial)
    assert all(abs(pair.compensator_difference) <= STAGE14A_ATOL for pair in zero_x)


def test_stage14b_wrong_missing_and_stage13_style_compensators_are_detected():
    diagnostics = stage14b_diagnostics()
    assert diagnostics.wrong_sign_rejected_count == 1728
    assert diagnostics.wrong_half_value_rejected_count == 1728
    assert diagnostics.missing_compensator_rejected_count == 1728
    assert diagnostics.stage13_style_rejected_nontrivial_count == 576
    assert diagnostics.stage13_style_zero_difference_compatible_count == 288
    assert diagnostics.wrong_controls_detected


def test_stage14b_cross_orbit_pairs_are_never_licensed():
    assert canonical_stage14b_cross_orbit_rejections() == 8748
    orbits = canonical_stage14a_orbits()
    source = canonical_stage14a_representatives_for_orbit(orbits[0])[0]
    target = canonical_stage14a_representatives_for_orbit(orbits[1])[-1]
    with pytest.raises(ValueError, match="distinct physical orbits"):
        stage14b_make_mixed_pair(source, target)


def test_stage14b_one_explicit_pair_requires_different_compensators_but_closes_both_orders():
    pairs = canonical_stage14b_mixed_pairs()
    pair = next(pair for pair in pairs if pair.source.X != 0.0)
    assert abs(pair.v_21D - pair.v_12D) > STAGE14A_ATOL
    result_12 = stage14b_apply_path(pair, STAGE14B_PATH_12D)
    result_21 = stage14b_apply_path(pair, STAGE14B_PATH_21D)
    assert result_12.final_endpoint_residual <= STAGE14A_ATOL
    assert result_21.final_endpoint_residual <= STAGE14A_ATOL


def test_stage14b_diagnostics_close_only_criteria_18_through_24():
    diagnostics = stage14b_diagnostics()
    assert diagnostics.mixed_pair_count == 864
    assert diagnostics.path_result_count == 1728
    assert diagnostics.nontrivial_X0_pair_count == 576
    assert diagnostics.zero_X0_pair_count == 288
    assert diagnostics.nonzero_compensator_difference_count == 576
    assert diagnostics.zero_compensator_difference_count == 288
    assert diagnostics.all_positive_pairs_closed
    assert diagnostics.nontrivial_path_order_detected
    assert diagnostics.zero_difference_subfamily_exact
    assert diagnostics.cross_orbit_false_positive_rejected
    assert diagnostics.criteria_18_24_satisfied
