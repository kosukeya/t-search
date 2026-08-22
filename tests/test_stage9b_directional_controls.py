import numpy as np
import pytest

from t_search.stage7_history import CURRENT_EVENT, LOWER_EVENT, UPPER_EVENT
from t_search.stage8_continuations import (
    canonical_continuation_left,
    canonical_continuation_right,
)
from t_search.stage9_controls import (
    ALL_CONTROLS,
    PURE_CONTROLS,
    assess_stage9b_control_admissibility,
    assess_stage9b_control_direction,
    reduced_stage9b_control_state,
    stage9b_common_reversal_is_interaction_reversal,
    stage9b_control_diagnostics,
    stage9b_control_retains_nontrivial_v,
    stage9b_control_schedule_rest_operators,
    stage9b_summary,
)
from t_search.stage9_substrate import reduced_stage9_state

ATOL = 1e-10


def _continuations():
    return canonical_continuation_left(), canonical_continuation_right()


def test_stage9b_forward_control_reproduces_stage9a_positive_direction():
    for continuation in _continuations():
        assessment = assess_stage9b_control_direction(continuation, "forward")
        assert assessment.record_defined is True
        assert assessment.orientation == "lower-index"
        assert np.isclose(assessment.record_score, 1.0, atol=ATOL, rtol=0.0)
        assert np.isclose(assessment.accessibility_score, 0.5, atol=ATOL, rtol=0.0)
        assert assessment.branch_weight_used is False
        assert assessment.v_extension_nontrivial is True


def test_stage9b_reversed_control_flips_both_directional_diagnostics():
    for continuation in _continuations():
        forward = assess_stage9b_control_direction(continuation, "forward")
        reversed_item = assess_stage9b_control_direction(continuation, "reversed")
        assert reversed_item.record_defined is True
        assert reversed_item.orientation == "upper-index"
        assert np.isclose(reversed_item.record_score, -1.0, atol=ATOL, rtol=0.0)
        assert np.isclose(
            reversed_item.accessibility_score, -0.5, atol=ATOL, rtol=0.0
        )
        assert np.isclose(
            reversed_item.record_score,
            -forward.record_score,
            atol=ATOL,
            rtol=0.0,
        )
        assert np.isclose(
            reversed_item.accessibility_score,
            -forward.accessibility_score,
            atol=ATOL,
            rtol=0.0,
        )


def test_stage9b_reversal_is_modeled_interaction_reversal_not_index_iteration():
    assert stage9b_common_reversal_is_interaction_reversal() is True

    left = canonical_continuation_left()
    forward = stage9b_control_schedule_rest_operators(left, "forward")
    reversed_schedule = stage9b_control_schedule_rest_operators(left, "reversed")
    for index in (LOWER_EVENT, CURRENT_EVENT, UPPER_EVENT):
        assert np.allclose(
            reversed_schedule[index],
            forward[UPPER_EVENT - index],
            atol=ATOL,
            rtol=0.0,
        )


def test_stage9b_forward_and_reversed_share_the_declared_current_actuality():
    for continuation in _continuations():
        forward_current = reduced_stage9b_control_state(
            continuation, "forward", CURRENT_EVENT
        )
        reversed_current = reduced_stage9b_control_state(
            continuation, "reversed", CURRENT_EVENT
        )
        stage9a_current = reduced_stage9_state(continuation, CURRENT_EVENT)
        assert np.allclose(forward_current, stage9a_current, atol=ATOL, rtol=0.0)
        assert np.allclose(reversed_current, stage9a_current, atol=ATOL, rtol=0.0)


def test_stage9b_balanced_control_cancels_direction_without_collapsing_v():
    for continuation in _continuations():
        assessment = assess_stage9b_control_direction(continuation, "balanced")
        assert assessment.record_defined is False
        assert assessment.orientation == "none"
        assert abs(assessment.record_score) <= ATOL
        assert abs(assessment.accessibility_score) <= ATOL
        assert assessment.branch_weight_used is False
        assert assessment.v_extension_nontrivial is True


def test_stage9b_no_record_control_removes_direction_without_collapsing_v():
    for continuation in _continuations():
        assessment = assess_stage9b_control_direction(continuation, "no-record")
        assert assessment.record_defined is False
        assert assessment.orientation == "none"
        assert abs(assessment.record_score) <= ATOL
        assert abs(assessment.accessibility_score) <= ATOL
        assert assessment.branch_weight_used is False
        assert assessment.v_extension_nontrivial is True


def test_stage9b_all_controls_retain_physically_nontrivial_extension_pair():
    assert all(stage9b_control_retains_nontrivial_v(control) for control in ALL_CONTROLS)

    left = canonical_continuation_left()
    right = canonical_continuation_right()
    for control in PURE_CONTROLS:
        left_upper = stage9b_control_schedule_rest_operators(left, control)[UPPER_EVENT]
        right_upper = stage9b_control_schedule_rest_operators(right, control)[UPPER_EVENT]
        assert np.linalg.norm(left_upper - right_upper) > ATOL


def test_stage9b_each_pure_control_is_a_valid_constrained_multiclock_carrier():
    for continuation in _continuations():
        for control in PURE_CONTROLS:
            assessment = assess_stage9b_control_admissibility(continuation, control)
            assert assessment.valid_constrained_carrier is True
            assert assessment.schedule_unitarity_residual <= ATOL
            assert assessment.dressing_unitarity_residual <= ATOL
            assert assessment.constraint_hermiticity_residual <= ATOL
            assert assessment.physical_constraint_residual <= 10 * ATOL
            assert assessment.physical_dimension == 14
            assert assessment.minimum_clock_reduction_rank == 14


def test_stage9b_control_diagnostics_summarize_expected_signs_and_residuals():
    diagnostics = stage9b_control_diagnostics()
    assert all(np.isclose(score, 1.0, atol=ATOL, rtol=0.0) for _, score in diagnostics.forward_scores)
    assert all(np.isclose(score, -1.0, atol=ATOL, rtol=0.0) for _, score in diagnostics.reversed_scores)
    assert diagnostics.reversal_record_residual <= ATOL
    assert diagnostics.reversal_accessibility_residual <= ATOL
    assert diagnostics.balanced_record_residual <= ATOL
    assert diagnostics.balanced_accessibility_residual <= ATOL
    assert diagnostics.no_record_record_residual <= ATOL
    assert diagnostics.no_record_accessibility_residual <= ATOL
    assert diagnostics.common_reversal_is_interaction_reversal is True
    assert diagnostics.all_controls_retain_nontrivial_v is True
    assert diagnostics.all_pure_controls_valid_constrained_carriers is True
    assert diagnostics.minimum_clock_reduction_rank == 14
    assert diagnostics.maximum_constraint_residual <= 10 * ATOL


def test_stage9b_balanced_has_no_single_pure_schedule_or_state():
    continuation = canonical_continuation_left()
    with pytest.raises(ValueError, match="balanced is a mixture"):
        stage9b_control_schedule_rest_operators(continuation, "balanced")
    with pytest.raises(ValueError, match="balanced admissibility"):
        assess_stage9b_control_admissibility(continuation, "balanced")


def test_stage9b_summary_keeps_control_and_interpretation_typing_explicit():
    summary = stage9b_summary()
    assert summary["current_anchor"] == "e1"
    assert summary["controls"] == ALL_CONTROLS
    assert summary["diagnostics"]["common_reversal_is_interaction_reversal"] is True
    assert summary["diagnostics"]["all_controls_retain_nontrivial_v"] is True
    assert "reversed diagnostic sign != reversed Python iteration" in summary["guards"]
    assert "balanced mixture != pure constrained history" in summary["guards"]
    assert "directional record arrow != ontological future openness" in summary["guards"]
    assert "control of R_direction != control of V_semantics" in summary["guards"]
