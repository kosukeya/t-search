import numpy as np
import pytest

from t_search.stage7_history import CURRENT_EVENT, UPPER_EVENT
from t_search.stage8_compatibility import (
    continuation_record_joint_distribution,
    continuation_record_profile,
    stage8e_compatibility_diagnostics,
    stage8e_compatibility_matrix,
    stage8e_summary,
)
from t_search.stage8_continuations import (
    QuantumContinuation,
    assess_continuation_admissibility,
    canonical_continuation_left,
    canonical_continuation_right,
    quantum_extension_set,
)

ATOL = 1e-9


def test_stage8e_p_o_event_effect_family_is_covariant_in_continuation_aware_atlas():
    diagnostics = stage8e_compatibility_diagnostics()
    assert diagnostics.p_o_event_effect_covariance is True
    assert diagnostics.max_p_o_operator_transport_residual <= ATOL
    assert diagnostics.max_p_o_probability_residual <= ATOL
    assert diagnostics.max_event_effect_completeness_residual <= ATOL
    assert diagnostics.max_event_effect_metric_self_adjoint_residual <= ATOL


def test_stage8e_p_r_current_record_statistics_are_covariant_with_corresponding_observables():
    diagnostics = stage8e_compatibility_diagnostics()
    assert diagnostics.p_r_current_record_covariance is True
    assert diagnostics.max_current_record_joint_residual <= ATOL
    assert diagnostics.max_current_record_information_residual <= ATOL


@pytest.mark.parametrize(
    "continuation",
    [canonical_continuation_left(), canonical_continuation_right()],
)
def test_stage8e_canonical_v_classes_keep_one_bit_current_target_record(continuation):
    for clock in ("A", "B", "C"):
        for index in range(3):
            joint, *_ = continuation_record_joint_distribution(
                continuation, clock, index, CURRENT_EVENT
            )
            probabilities = np.asarray(joint)
            assert np.sum(probabilities) == pytest.approx(1.0, abs=ATOL)
            assert np.min(probabilities) >= -ATOL

    profile = continuation_record_profile(continuation)
    assert profile.current_information == pytest.approx(1.0, abs=ATOL)
    assert profile.current_record_present is True


def test_stage8e_wrong_target_and_bare_observable_controls_prevent_fake_p_r_covariance():
    diagnostics = stage8e_compatibility_diagnostics()
    assert diagnostics.max_wrong_target_information <= ATOL
    assert diagnostics.bare_record_metric_self_adjoint_residual > ATOL
    assert diagnostics.bare_record_observable_rejected is True


def test_stage8e_o_v_alternatives_first_differ_only_after_current_anchor():
    diagnostics = stage8e_compatibility_diagnostics()
    assert diagnostics.o_v_first_difference_event == UPPER_EVENT
    assert diagnostics.o_v_first_difference_event > CURRENT_EVENT
    assert diagnostics.o_v_difference_after_current_anchor is True
    assert diagnostics.o_v_invalid_current_prefix_rejected is True
    assert diagnostics.o_v_terminal_qext_empty is True
    assert quantum_extension_set(UPPER_EVENT) == ()


def test_stage8e_current_prefix_control_still_rejects_changed_actuality():
    invalid = QuantumContinuation(
        continuation_id="stage8e-invalid-current",
        future_action="identity",
        current_action="identity",
    )
    assessment = assess_continuation_admissibility(invalid)
    assert assessment.current_prefix_compatible is False
    assert assessment.admissible is False


def test_stage8e_physically_distinct_v_classes_share_the_same_current_record():
    diagnostics = stage8e_compatibility_diagnostics()
    assert diagnostics.current_record_shared_across_v_classes is True
    assert diagnostics.current_record_class_joint_residual <= ATOL
    assert diagnostics.distinct_v_classes_with_same_current_record is True


def test_stage8e_canonical_record_neutral_v_family_has_no_directional_record_arrow():
    left = continuation_record_profile(canonical_continuation_left())
    right = continuation_record_profile(canonical_continuation_right())

    for profile in (left, right):
        assert profile.lower_information == pytest.approx(1.0, abs=ATOL)
        assert profile.current_information == pytest.approx(1.0, abs=ATOL)
        assert profile.upper_information == pytest.approx(1.0, abs=ATOL)
        assert profile.record_score == pytest.approx(0.0, abs=ATOL)
        assert profile.accessibility_score == pytest.approx(0.0, abs=ATOL)
        assert profile.orientation == "none"
        assert profile.current_record_present is True
        assert profile.directional_record_defined is False

    diagnostics = stage8e_compatibility_diagnostics()
    assert diagnostics.baseline_directional_r_absent is True


def test_stage8e_same_order_and_current_state_do_not_force_directional_r():
    diagnostics = stage8e_compatibility_diagnostics()
    assert diagnostics.record_scramble_control_current_state_residual <= ATOL
    assert diagnostics.record_scramble_control_record_score == pytest.approx(1.0, abs=ATOL)
    assert diagnostics.record_scramble_control_directional_r_present is True
    assert diagnostics.order_does_not_force_directional_r is True


def test_stage8e_p_v_class_weight_covariance_survives_integrated_compatibility_check():
    diagnostics = stage8e_compatibility_diagnostics()
    assert diagnostics.p_v_class_weight_covariance is True
    assert diagnostics.matched_public_modal_views_all_nodes is True


def test_stage8e_same_p_o_current_r_carrier_remains_modally_underdetermined():
    diagnostics = stage8e_compatibility_diagnostics()
    assert diagnostics.privileged_modal_structures_distinct is True
    assert diagnostics.same_por_carrier_distinct_v_semantics is True
    assert diagnostics.transported_weight_mismatch_density_residual > ATOL
    assert diagnostics.weight_mismatch_control_detected is True


def test_stage8e_does_not_overclaim_full_directional_porv_or_measurement_covariance():
    diagnostics = stage8e_compatibility_diagnostics()
    assert diagnostics.full_stage8c_measurement_covariance_established is False
    assert diagnostics.full_directional_porv_integration_established is False


def test_stage8e_compatibility_matrix_keeps_positive_underdetermined_and_partial_rows_distinct():
    matrix = {entry.relation: entry.status for entry in stage8e_compatibility_matrix()}
    assert matrix["P-O(event effects)"] == "compatible"
    assert matrix["P-R(current record)"] == "compatible"
    assert matrix["P-V(class/weights)"] == "compatible"
    assert matrix["O-V(extension)"] == "compatible"
    assert matrix["R(current)-V"] == "underdetermined"
    assert matrix["O=>R(direction)"] == "implication_refuted"
    assert matrix["P/O/current-R=>V semantics"] == "underdetermined"
    assert matrix["full P/O/directional-R/V"] == "partial"


def test_stage8e_summary_closes_current_execution_criteria_36_to_41_only():
    summary = stage8e_summary()
    assert tuple(summary["current_execution_criteria"].keys()) == (
        "36",
        "37",
        "38",
        "39",
        "40",
        "41",
    )
    assert summary["next"] == "Stage 8F — ablation / reconstruction / mismatch matrix"
    guards = summary["guards"]
    assert "event-effect covariance != temporal succession" in guards
    assert "current record covariance != directional record arrow" in guards
    assert "order != directional record arrow" in guards
    assert "R-V compatibility != R=V" in guards
    assert "same P/O/current-R public data != modal identity" in guards
    assert "not_established != false" in guards
