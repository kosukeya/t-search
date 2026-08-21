import numpy as np
import pytest

from t_search.stage7_history import CURRENT_EVENT, LOWER_EVENT, UPPER_EVENT
from t_search.stage8_continuations import (
    QuantumContinuation,
    assess_continuation_admissibility,
    canonical_continuation_left,
    canonical_continuation_right,
    continuation_constraint_operator,
    continuation_equivalent,
    continuation_future_operator,
    continuation_physical_basis,
    continuation_schedule_rest_operators,
    deduplicate_continuations,
    future_pair_phase_ambient_operator,
    future_pair_phase_support_matrix,
    quantum_extension_set,
    reduced_continuation_state,
    renamed_continuation,
    stage8a_substrate_diagnostics,
    stage8a_summary,
)

ATOL = 1e-10


def test_stage8a_qext_contains_two_nontrivial_canonical_continuations():
    qext = quantum_extension_set()
    assert len(qext) == 2
    assert tuple(item.continuation_id for item in qext) == ("h_L", "h_R")
    assert qext[0].future_action != qext[1].future_action


def test_stage8a_canonical_continuations_share_current_prefix_schedule():
    left = canonical_continuation_left()
    right = canonical_continuation_right()
    left_schedule = continuation_schedule_rest_operators(left)
    right_schedule = continuation_schedule_rest_operators(right)

    assert np.allclose(left_schedule[LOWER_EVENT], right_schedule[LOWER_EVENT], atol=ATOL, rtol=0.0)
    assert np.allclose(left_schedule[CURRENT_EVENT], right_schedule[CURRENT_EVENT], atol=ATOL, rtol=0.0)
    assert not np.allclose(left_schedule[UPPER_EVENT], right_schedule[UPPER_EVENT], atol=ATOL, rtol=0.0)


def test_stage8a_current_actuality_states_are_equal_through_e1():
    left = canonical_continuation_left()
    right = canonical_continuation_right()
    for event in (LOWER_EVENT, CURRENT_EVENT):
        assert np.allclose(
            reduced_continuation_state(left, event),
            reduced_continuation_state(right, event),
            atol=ATOL,
            rtol=0.0,
        )


def test_stage8a_future_states_are_physically_inequivalent():
    diagnostics = stage8a_substrate_diagnostics()
    assert diagnostics.physically_inequivalent is True
    assert np.isclose(diagnostics.future_operator_residual, 4.0, atol=ATOL, rtol=0.0)
    assert np.isclose(diagnostics.future_state_overlap_squared, 0.0, atol=ATOL, rtol=0.0)
    assert np.isclose(diagnostics.future_state_distance, np.sqrt(2.0), atol=ATOL, rtol=0.0)
    assert diagnostics.future_probe_difference > ATOL


def test_stage8a_future_difference_is_memory_and_record_target_neutral():
    diagnostics = stage8a_substrate_diagnostics()
    assert diagnostics.memory_neutral_future is True
    assert diagnostics.record_target_neutral_future is True
    assert diagnostics.common_current_record_information_residual <= ATOL
    assert np.isclose(diagnostics.current_record_information, 1.0, atol=ATOL, rtol=0.0)


def test_stage8a_pair_phase_is_reversible_unitary_and_nontrivial():
    support_phase = future_pair_phase_support_matrix()
    ambient_phase = future_pair_phase_ambient_operator()
    assert np.allclose(
        support_phase.conj().T @ support_phase,
        np.eye(support_phase.shape[0]),
        atol=ATOL,
        rtol=0.0,
    )
    assert np.allclose(support_phase @ support_phase, np.eye(support_phase.shape[0]), atol=ATOL, rtol=0.0)
    assert np.allclose(
        ambient_phase.conj().T @ ambient_phase,
        np.eye(ambient_phase.shape[0]),
        atol=ATOL,
        rtol=0.0,
    )
    assert not np.allclose(ambient_phase, np.eye(ambient_phase.shape[0]), atol=ATOL, rtol=0.0)


def test_stage8a_each_continuation_defines_a_valid_modified_constraint():
    for continuation in quantum_extension_set():
        assessment = assess_continuation_admissibility(continuation)
        assert assessment.admissible is True
        assert assessment.current_prefix_compatible is True
        assert assessment.schedule_unitarity_residual <= ATOL
        assert assessment.dressing_unitarity_residual <= ATOL
        assert assessment.constraint_hermiticity_residual <= ATOL
        assert assessment.physical_constraint_residual <= ATOL
        assert assessment.physical_dimension == 14
        assert assessment.minimum_clock_reduction_rank == 14

        constraint = continuation_constraint_operator(continuation)
        physical = continuation_physical_basis(continuation)
        assert constraint.shape == (54, 54)
        assert physical.shape == (54, 14)
        assert np.linalg.norm(constraint @ physical) <= 10 * ATOL


def test_stage8a_all_nine_clock_readings_remain_injective_for_each_continuation():
    diagnostics = stage8a_substrate_diagnostics()
    assert diagnostics.minimum_clock_reduction_rank == 14
    assert diagnostics.maximum_constraint_residual <= ATOL


def test_stage8a_pure_renaming_does_not_create_new_physical_continuation():
    left = canonical_continuation_left()
    right = canonical_continuation_right()
    renamed = renamed_continuation(left, "cosmetic-label")

    assert renamed.continuation_id != left.continuation_id
    assert continuation_equivalent(left, renamed) is True
    deduplicated = deduplicate_continuations((left, right, renamed))
    assert len(deduplicated) == 2
    assert stage8a_substrate_diagnostics().deduplicated_size_with_rename == 2


def test_stage8a_distinct_future_actions_are_not_equivalent():
    left = canonical_continuation_left()
    right = canonical_continuation_right()
    assert continuation_equivalent(left, right) is False
    assert np.linalg.norm(
        continuation_future_operator(left) - continuation_future_operator(right)
    ) > ATOL


def test_stage8a_current_incompatible_continuation_is_rejected_from_qext():
    invalid = QuantumContinuation(
        continuation_id="invalid-current",
        future_action="identity",
        current_action="identity",
    )
    assessment = assess_continuation_admissibility(invalid)
    assert assessment.current_prefix_compatible is False
    assert assessment.admissible is False
    with pytest.raises(ValueError, match="not physically admissible/current-compatible"):
        quantum_extension_set(
            candidates=(canonical_continuation_left(), canonical_continuation_right(), invalid)
        )
    assert stage8a_substrate_diagnostics().invalid_current_prefix_rejected is True


def test_stage8a_terminal_current_has_no_further_canonical_extensions():
    assert quantum_extension_set(UPPER_EVENT) == ()
    assert stage8a_substrate_diagnostics().terminal_qext_size == 0
    with pytest.raises(ValueError, match="declared only at e1 or terminal e2"):
        quantum_extension_set(LOWER_EVENT)


def test_stage8a_summary_preserves_modal_interpretation_boundary():
    summary = stage8a_summary()
    assert summary["current_anchor"] == "e1"
    assert summary["qext"] == ("h_L", "h_R")
    assert summary["diagnostics"]["physically_inequivalent"] is True
    assert "QExt represented != ontically real futures by definition" in summary["guards"]
    assert "future physical inequivalence != modal semantics by itself" in summary["guards"]
