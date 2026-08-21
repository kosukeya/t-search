import numpy as np

from t_search.stage7_history import (
    CURRENT_EVENT,
    LOWER_EVENT,
    UPPER_EVENT,
    assess_relational_record,
    balanced_forward_reverse_assessment,
    canonical_history_model,
    canonical_physical_history_state,
    event_target_joint_distribution,
    history_constraint_operator,
    history_constraint_residual,
    history_dressing_operator,
    history_physical_basis,
    history_physical_projector,
    history_reconstruction_operator,
    history_reduction_operator,
    history_transition_support_matrix,
    pair_scrambler_support_matrix,
    schedule_rest_operators,
    stage7c_constraint_diagnostics,
    stage7c_control_assessments,
    stage7c_summary,
    uncertain_memory_control_assessment,
)
from t_search.stage7_spectator import (
    spectator_support_basis,
    spectator_support_projector,
    spectator_total_constraint_operator,
)

ATOL = 1e-10


def test_stage7c_history_typing_and_internal_anchor_are_explicit():
    forward = canonical_history_model("forward")
    reversed_model = canonical_history_model("reversed")
    assert forward.event_labels == ("e0", "e1", "e2")
    assert forward.orientation_convention == "lower-minus-upper around current event e1"
    assert "A-clock reading projectors" in forward.interaction_anchor
    assert reversed_model.kind == "reversed"
    assert (LOWER_EVENT, CURRENT_EVENT, UPPER_EVENT) == (0, 1, 2)


def test_stage7c_pair_scrambler_is_reversible_unitary():
    u = pair_scrambler_support_matrix()
    identity = np.eye(u.shape[0])
    assert u.shape == (14, 14)
    assert np.allclose(u.conj().T @ u, identity, atol=ATOL, rtol=0.0)
    assert np.allclose(u @ u, identity, atol=ATOL, rtol=0.0)


def test_stage7c_forward_schedule_has_record_then_scramble_cumulative_structure():
    v0, v1, v2 = schedule_rest_operators("forward")
    assert np.allclose(v0, np.eye(18), atol=ATOL, rtol=0.0)
    assert not np.allclose(v1, v0, atol=ATOL, rtol=0.0)
    assert not np.allclose(v2, v1, atol=ATOL, rtol=0.0)
    for operator in (v0, v1, v2):
        assert np.allclose(
            operator.conj().T @ operator,
            np.eye(operator.shape[0]),
            atol=ATOL,
            rtol=0.0,
        )


def test_stage7c_dressing_is_clock_conditioned_and_unitary():
    dressing = history_dressing_operator("forward")
    assert dressing.shape == (54, 54)
    assert np.allclose(
        dressing.conj().T @ dressing,
        np.eye(54),
        atol=ATOL,
        rtol=0.0,
    )

    # The three cumulative operators are genuinely distinguished by the
    # internal A-clock reading anchor, not by Python application order alone.
    v0, v1, v2 = schedule_rest_operators("forward")
    assert not np.allclose(v0, v1, atol=ATOL, rtol=0.0)
    assert not np.allclose(v1, v2, atol=ATOL, rtol=0.0)


def test_stage7c_modified_constraint_is_hermitian_distinct_and_has_rederived_kernel():
    diagnostics = stage7c_constraint_diagnostics("forward")
    assert diagnostics["kinematic_dimension"] == 54
    assert diagnostics["physical_dimension"] == 14
    assert diagnostics["modified_constraint_differs_from_spectator"] is True
    assert diagnostics["dressing_unitarity_residual"] <= ATOL
    assert diagnostics["constraint_hermiticity_residual"] <= ATOL
    assert diagnostics["physical_kernel_residual"] <= ATOL
    assert diagnostics["analytic_numerical_projector_residual"] <= ATOL
    assert diagnostics["rederived_reduction_isometry_residual"] <= ATOL
    assert diagnostics["rederived_roundtrip_residual"] <= ATOL

    h_hist = history_constraint_operator("forward")
    assert not np.allclose(h_hist, spectator_total_constraint_operator(), atol=ATOL, rtol=0.0)


def test_stage7c_rederived_reductions_reconstructions_round_trip_all_events():
    physical_projector = history_physical_projector("forward")
    support_projector = spectator_support_projector("A")
    for index in (0, 1, 2):
        reduction = history_reduction_operator(index)
        reconstruction = history_reconstruction_operator("forward", index)
        assert np.allclose(
            reduction @ reconstruction,
            support_projector,
            atol=ATOL,
            rtol=0.0,
        )
        assert np.allclose(
            reconstruction @ reduction @ physical_projector,
            physical_projector,
            atol=ATOL,
            rtol=0.0,
        )


def test_stage7c_rederived_transitions_match_direct_conditioning_of_one_physical_history():
    state = canonical_physical_history_state("forward")
    support = spectator_support_basis("A")
    for source in (0, 1, 2):
        source_state = history_reduction_operator(source) @ state
        source_coordinates = support.conj().T @ source_state
        for target in (0, 1, 2):
            direct_target = history_reduction_operator(target) @ state
            direct_coordinates = support.conj().T @ direct_target
            transition = history_transition_support_matrix("forward", target, source)
            assert np.allclose(
                transition @ source_coordinates,
                direct_coordinates,
                atol=ATOL,
                rtol=0.0,
            )


def test_stage7c_forward_history_defines_lower_index_record_orientation():
    assessment = assess_relational_record("forward")
    assert assessment.internally_anchored is True
    assert assessment.directional_score_defined is True
    assert assessment.constraint_residual <= ATOL
    assert np.isclose(assessment.lower_information, 1.0, atol=ATOL, rtol=0.0)
    assert assessment.upper_information <= ATOL
    assert np.isclose(assessment.lower_accuracy, 1.0, atol=ATOL, rtol=0.0)
    assert np.isclose(assessment.upper_accuracy, 0.5, atol=ATOL, rtol=0.0)
    assert np.isclose(assessment.record_score, 1.0, atol=ATOL, rtol=0.0)
    assert np.isclose(assessment.accessibility_score, 0.5, atol=ATOL, rtol=0.0)
    assert assessment.orientation == "lower-index"
    assert assessment.record_defined is True


def test_stage7c_explicit_reversed_history_reverses_orientation_not_just_sign_label():
    forward = assess_relational_record("forward")
    reversed_assessment = assess_relational_record("reversed")
    assert reversed_assessment.internally_anchored is True
    assert reversed_assessment.record_defined is True
    assert reversed_assessment.orientation == "upper-index"
    assert reversed_assessment.lower_information <= ATOL
    assert np.isclose(reversed_assessment.upper_information, 1.0, atol=ATOL, rtol=0.0)
    assert np.isclose(
        reversed_assessment.record_score,
        -forward.record_score,
        atol=ATOL,
        rtol=0.0,
    )
    assert np.isclose(
        reversed_assessment.accessibility_score,
        -forward.accessibility_score,
        atol=ATOL,
        rtol=0.0,
    )
    # The reversed control is a genuinely different internally anchored
    # schedule/constraint, not the forward result with its sign renamed.
    assert not np.allclose(
        history_constraint_operator("reversed"),
        history_constraint_operator("forward"),
        atol=ATOL,
        rtol=0.0,
    )


def test_stage7c_balanced_forward_reverse_metaensemble_cancels_directional_scores():
    balanced = balanced_forward_reverse_assessment()
    assert np.isclose(
        balanced.lower_information,
        balanced.upper_information,
        atol=ATOL,
        rtol=0.0,
    )
    assert np.isclose(
        balanced.lower_accuracy,
        balanced.upper_accuracy,
        atol=ATOL,
        rtol=0.0,
    )
    assert abs(balanced.record_score) <= ATOL
    assert abs(balanced.accessibility_score) <= ATOL
    assert balanced.orientation == "none"
    assert balanced.record_defined is False


def test_stage7c_no_record_control_retains_order_and_scramble_but_no_orientation():
    no_record = assess_relational_record("no-record")
    assert no_record.internally_anchored is True
    assert no_record.directional_score_defined is True
    assert no_record.constraint_residual <= ATOL
    assert no_record.lower_information <= ATOL
    assert no_record.upper_information <= ATOL
    assert abs(no_record.record_score) <= ATOL
    assert abs(no_record.accessibility_score) <= ATOL
    assert no_record.orientation == "none"
    assert no_record.record_defined is False
    assert not np.allclose(
        history_constraint_operator("no-record"),
        spectator_total_constraint_operator(),
        atol=ATOL,
        rtol=0.0,
    )


def test_stage7c_maximally_uncertain_memory_control_erases_record_orientation():
    uncertain = uncertain_memory_control_assessment()
    assert uncertain.internally_anchored is True
    assert uncertain.lower_information <= ATOL
    assert uncertain.upper_information <= ATOL
    assert abs(uncertain.record_score) <= ATOL
    assert abs(uncertain.accessibility_score) <= ATOL
    assert uncertain.orientation == "none"
    assert uncertain.record_defined is False


def test_stage7c_all_canonical_physical_histories_satisfy_their_own_modified_constraint():
    for kind in ("forward", "reversed", "no-record"):
        state = canonical_physical_history_state(kind)
        basis = history_physical_basis(kind)
        assert np.isclose(np.linalg.norm(state), 1.0, atol=ATOL, rtol=0.0)
        assert history_constraint_residual(state, kind) <= ATOL
        assert np.linalg.norm(
            (np.eye(54) - basis @ basis.conj().T) @ state
        ) <= ATOL


def test_stage7c_control_summary_requires_all_predeclared_orientation_controls():
    controls = stage7c_control_assessments()
    assert controls.forward.record_defined is True
    assert controls.reversed.record_defined is True
    assert controls.forward_reverse_sign_reversal is True
    assert controls.balanced_cancels is True
    assert controls.no_record_cancels is True
    assert controls.uncertain_memory_cancels is True

    summary = stage7c_summary()
    assert summary["event_order"] == ["e0", "e1", "e2"]
    assert summary["current_event"] == "e1"
    assert "simulation/intervention order != modeled temporal order" in summary["guards"]
    assert "record-defined orientation != ontological becoming" in summary["guards"]
