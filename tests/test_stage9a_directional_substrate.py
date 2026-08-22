import numpy as np
import pytest

from t_search.stage7_history import (
    CURRENT_EVENT,
    LOWER_EVENT,
    UPPER_EVENT,
    pair_scrambler_ambient_operator,
)
from t_search.stage7_record import controlled_record_write_ambient_operator
from t_search.stage8_continuations import (
    QuantumContinuation,
    canonical_continuation_left,
    canonical_continuation_right,
    future_pair_phase_ambient_operator,
    renamed_continuation,
)
from t_search.stage9_substrate import (
    assess_stage9_admissibility,
    assess_stage9_direction,
    canonical_stage9_physical_state,
    deduplicate_stage9_continuations,
    reduced_stage9_state,
    stage9_branch_action_operator,
    stage9_constraint_operator,
    stage9_continuation_equivalent,
    stage9_extension_set,
    stage9_physical_basis,
    stage9_schedule_rest_operators,
    stage9a_substrate_diagnostics,
    stage9a_summary,
)

ATOL = 1e-10


def test_stage9a_qext_has_two_physically_distinct_canonical_continuations():
    qext = stage9_extension_set()
    assert len(qext) == 2
    assert tuple(item.continuation_id for item in qext) == ("h_L", "h_R")
    assert qext[0].future_action != qext[1].future_action
    assert stage9a_substrate_diagnostics().physically_inequivalent is True


def test_stage9a_continuations_share_e0_and_e1_schedule_but_fork_at_e2():
    left = canonical_continuation_left()
    right = canonical_continuation_right()
    left_schedule = stage9_schedule_rest_operators(left)
    right_schedule = stage9_schedule_rest_operators(right)

    assert np.allclose(
        left_schedule[LOWER_EVENT], right_schedule[LOWER_EVENT], atol=ATOL, rtol=0.0
    )
    assert np.allclose(
        left_schedule[CURRENT_EVENT], right_schedule[CURRENT_EVENT], atol=ATOL, rtol=0.0
    )
    assert not np.allclose(
        left_schedule[UPPER_EVENT], right_schedule[UPPER_EVENT], atol=ATOL, rtol=0.0
    )


def test_stage9a_canonical_schedule_is_common_record_then_common_scramble_plus_branch_action():
    left = canonical_continuation_left()
    right = canonical_continuation_right()
    record = controlled_record_write_ambient_operator()
    scramble = pair_scrambler_ambient_operator()
    phase = future_pair_phase_ambient_operator()

    left_schedule = stage9_schedule_rest_operators(left)
    right_schedule = stage9_schedule_rest_operators(right)

    assert np.allclose(left_schedule[CURRENT_EVENT], record, atol=ATOL, rtol=0.0)
    assert np.allclose(
        left_schedule[UPPER_EVENT], scramble @ record, atol=ATOL, rtol=0.0
    )
    assert np.allclose(
        right_schedule[UPPER_EVENT], phase @ scramble @ record, atol=ATOL, rtol=0.0
    )


def test_stage9a_current_actuality_is_shared_through_e1():
    left = canonical_continuation_left()
    right = canonical_continuation_right()
    for event in (LOWER_EVENT, CURRENT_EVENT):
        assert np.allclose(
            reduced_stage9_state(left, event),
            reduced_stage9_state(right, event),
            atol=ATOL,
            rtol=0.0,
        )
    diagnostics = stage9a_substrate_diagnostics()
    assert diagnostics.common_e0_state_residual <= ATOL
    assert diagnostics.common_e1_state_residual <= ATOL


def test_stage9a_each_continuation_has_same_nonzero_direction_before_weighting():
    qext = stage9_extension_set()
    assessments = tuple(assess_stage9_direction(item) for item in qext)
    assert all(item.record_defined for item in assessments)
    assert all(item.orientation == "lower-index" for item in assessments)
    assert all(item.record_score > 0.9 for item in assessments)
    assert all(item.accessibility_score > 0.4 for item in assessments)
    assert np.isclose(assessments[0].record_score, assessments[1].record_score, atol=ATOL, rtol=0.0)
    assert np.isclose(
        assessments[0].accessibility_score,
        assessments[1].accessibility_score,
        atol=ATOL,
        rtol=0.0,
    )
    assert stage9a_substrate_diagnostics().coherent_direction is True


def test_stage9a_branch_action_is_separate_from_memory_record_channel():
    diagnostics = stage9a_substrate_diagnostics()
    assert diagnostics.branch_action_memory_neutral is True
    assert diagnostics.branch_action_record_target_neutral is True
    assert diagnostics.continuation_identity_separated_from_record_channel is True

    left = canonical_continuation_left()
    right = canonical_continuation_right()
    assert not np.allclose(
        stage9_branch_action_operator(left),
        stage9_branch_action_operator(right),
        atol=ATOL,
        rtol=0.0,
    )


def test_stage9a_each_continuation_defines_valid_constrained_multi_clock_carrier():
    for continuation in stage9_extension_set():
        assessment = assess_stage9_admissibility(continuation)
        assert assessment.admissible is True
        assert assessment.current_prefix_compatible is True
        assert assessment.schedule_unitarity_residual <= ATOL
        assert assessment.dressing_unitarity_residual <= ATOL
        assert assessment.constraint_hermiticity_residual <= ATOL
        assert assessment.physical_constraint_residual <= ATOL
        assert assessment.physical_dimension == 14
        assert assessment.minimum_clock_reduction_rank == 14

        physical = stage9_physical_basis(continuation)
        constraint = stage9_constraint_operator(continuation)
        assert physical.shape == (54, 14)
        assert constraint.shape == (54, 54)
        assert np.linalg.norm(constraint @ physical) <= 10 * ATOL
        state = canonical_stage9_physical_state(continuation)
        assert np.isclose(np.linalg.norm(state), 1.0, atol=ATOL, rtol=0.0)


def test_stage9a_future_continuations_are_not_only_different_labels():
    diagnostics = stage9a_substrate_diagnostics()
    assert diagnostics.future_operator_residual > ATOL
    assert diagnostics.physically_inequivalent is True
    assert (
        diagnostics.future_state_overlap_squared < 1.0 - ATOL
        or diagnostics.future_probe_difference > ATOL
    )

    left = canonical_continuation_left()
    right = canonical_continuation_right()
    assert stage9_continuation_equivalent(left, right) is False


def test_stage9a_pure_renaming_does_not_create_third_continuation():
    left = canonical_continuation_left()
    right = canonical_continuation_right()
    renamed = renamed_continuation(left, "cosmetic-stage9-label")
    assert stage9_continuation_equivalent(left, renamed) is True
    deduplicated = deduplicate_stage9_continuations((left, right, renamed))
    assert len(deduplicated) == 2
    diagnostics = stage9a_substrate_diagnostics()
    assert diagnostics.renamed_equivalent is True
    assert diagnostics.deduplicated_size_with_rename == 2


def test_stage9a_current_incompatible_candidate_is_rejected():
    invalid = QuantumContinuation(
        continuation_id="invalid-stage9-current",
        future_action="identity",
        current_action="identity",
    )
    assessment = assess_stage9_admissibility(invalid)
    assert assessment.current_prefix_compatible is False
    assert assessment.admissible is False
    with pytest.raises(ValueError, match="not Stage 9A admissible/current-compatible"):
        stage9_extension_set(
            candidates=(
                canonical_continuation_left(),
                canonical_continuation_right(),
                invalid,
            )
        )
    assert stage9a_substrate_diagnostics().invalid_current_prefix_rejected is True


def test_stage9a_terminal_qext_is_empty_and_e0_is_not_declared_current():
    assert stage9_extension_set(UPPER_EVENT) == ()
    assert stage9a_substrate_diagnostics().terminal_qext_size == 0
    with pytest.raises(ValueError, match="declared only at e1 or terminal e2"):
        stage9_extension_set(LOWER_EVENT)


def test_stage9a_summary_keeps_interpretation_guards_explicit():
    summary = stage9a_summary()
    assert summary["current_anchor"] == "e1"
    assert summary["qext"] == ("h_L", "h_R")
    assert summary["schedule"]["h_L_e2"] == "U_scr U_rec"
    assert summary["schedule"]["h_R_e2"] == "Z_C U_scr U_rec"
    assert summary["diagnostics"]["coherent_direction"] is True
    assert summary["diagnostics"]["continuation_identity_separated_from_record_channel"] is True
    assert "directional record arrow != ontological future openness" in summary["guards"]
    assert "continuation identity != record-direction identity" in summary["guards"]
