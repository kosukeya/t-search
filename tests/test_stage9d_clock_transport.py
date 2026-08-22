import numpy as np
import pytest

from t_search.stage5_clock_change import SUBSYSTEMS
from t_search.stage7_history import CURRENT_EVENT, LOWER_EVENT, UPPER_EVENT
from t_search.stage9_modal import canonical_stage9c_models
from t_search.stage9_substrate import stage9_extension_set
from t_search.stage9_transport import (
    audit_class_correspondence,
    class_correspondence,
    event_correspondence,
    perspective_qr_view,
    perspective_record_assessment,
    physical_event_target_operator,
    represent_physical_operator,
    stage9_clock_change_support_matrix,
    stage9_clock_coordinates,
    stage9_clock_support_qr,
    stage9_reduced_support_coordinates,
    stage9_support_metric,
    stage9d_summary,
    stage9d_transport_diagnostics,
    typed_event_target_observable,
)

ATOL = 1e-9


def test_stage9d_rederives_eighteen_rank14_continuation_specific_charts():
    diagnostics = stage9d_transport_diagnostics()
    assert diagnostics.qext_size == 2
    assert diagnostics.perspective_nodes_per_continuation == 9
    assert diagnostics.total_perspective_nodes == 18
    assert diagnostics.minimum_chart_rank == 14
    for continuation in stage9_extension_set(CURRENT_EVENT):
        for clock in SUBSYSTEMS:
            for index in range(3):
                q, r = stage9_clock_support_qr(continuation, clock, index)
                assert q.shape == (18, 14)
                assert r.shape == (14, 14)
                assert np.linalg.matrix_rank(r, tol=ATOL) == 14
                assert stage9_clock_coordinates(continuation, clock, index).shape == (14, 14)


def test_stage9d_genuine_state_inverse_metric_and_composition_covariance():
    diagnostics = stage9d_transport_diagnostics()
    assert diagnostics.distinct_clock_state_transports == 108
    assert diagnostics.three_clock_compositions == 324
    assert diagnostics.max_state_transport_residual <= ATOL
    assert diagnostics.max_inverse_residual <= ATOL
    assert diagnostics.max_metric_covariance_residual <= ATOL
    assert diagnostics.max_composition_residual <= ATOL
    assert diagnostics.continuation_level_transport_covariance is True


def test_stage9d_record_observables_are_typed_and_transport_covariantly():
    diagnostics = stage9d_transport_diagnostics()
    assert diagnostics.observable_typing_fields_present is True
    assert diagnostics.max_observable_transport_residual <= ATOL
    assert diagnostics.max_metric_self_adjoint_residual <= ATOL
    assert diagnostics.max_projector_residual <= ATOL
    assert diagnostics.max_record_memory_commutator_residual <= ATOL
    assert diagnostics.directional_record_covariance is True

    continuation = stage9_extension_set(CURRENT_EVENT)[0]
    typed = typed_event_target_observable(
        continuation, "B", 0, LOWER_EVENT
    )
    assert typed.continuation_id == continuation.continuation_id
    assert typed.clock == "B"
    assert typed.clock_index == 0
    assert typed.event_anchor == "e1"
    assert typed.relational_target == "e0"
    assert typed.register_semantics == "record-target projector"
    assert "continuation-specific" in typed.coordinate_basis


def test_stage9d_directional_scores_are_perspective_covariant_for_each_continuation():
    diagnostics = stage9d_transport_diagnostics()
    assert diagnostics.max_preserving_record_score_residual <= ATOL
    assert diagnostics.max_preserving_accessibility_residual <= ATOL
    assert diagnostics.max_reversing_record_sign_residual <= ATOL
    assert diagnostics.max_reversing_accessibility_sign_residual <= ATOL

    for continuation in stage9_extension_set(CURRENT_EVENT):
        for clock in SUBSYSTEMS:
            for index in range(3):
                preserving = perspective_record_assessment(
                    continuation, clock, index, chi="preserving"
                )
                reversing = perspective_record_assessment(
                    continuation, clock, index, chi="reversing"
                )
                assert np.isclose(preserving.record_score, 1.0, atol=ATOL, rtol=0.0)
                assert np.isclose(
                    preserving.accessibility_score, 0.5, atol=ATOL, rtol=0.0
                )
                assert preserving.orientation == "lower-index"
                assert preserving.record_defined is True
                assert np.isclose(reversing.record_score, -1.0, atol=ATOL, rtol=0.0)
                assert np.isclose(
                    reversing.accessibility_score, -0.5, atol=ATOL, rtol=0.0
                )
                assert reversing.orientation == "upper-index"


def test_stage9d_event_correspondence_not_numeric_clock_reading_defines_orientation():
    preserving = event_correspondence("preserving")
    reversing = event_correspondence("reversing")
    wrong = event_correspondence("misdeclared-preserving")
    assert preserving.target_events == ("e0", "e1", "e2")
    assert reversing.target_events == ("e2", "e1", "e0")
    assert reversing.orientation_sign == -1
    assert wrong.target_events == reversing.target_events
    assert wrong.orientation_sign == 1
    assert stage9d_transport_diagnostics().wrong_event_correspondence_rejected is True


def test_stage9d_class_correspondence_preserves_only_physical_qext_classes():
    epistemic, _ = canonical_stage9c_models()
    carrier = epistemic.carrier
    correct = audit_class_correspondence(
        carrier, class_correspondence(carrier, "preserving")
    )
    swapped = audit_class_correspondence(
        carrier, class_correspondence(carrier, "swapped-classes")
    )
    terminal = audit_class_correspondence(
        carrier, class_correspondence(carrier, "misdeclared-terminal-preserving")
    )
    assert correct.valid is True
    assert correct.bijective is True
    assert correct.current_event_preserved is True
    assert correct.physical_classes_preserved is True
    assert swapped.valid is False
    assert terminal.valid is False


def test_stage9d_modal_views_remain_matched_and_hidden_selector_swap_invariant_all_nodes():
    diagnostics = stage9d_transport_diagnostics()
    assert diagnostics.matched_modal_views_all_nodes is True
    assert diagnostics.selected_swap_modal_views_all_nodes is True
    assert diagnostics.max_weight_transport_residual <= ATOL
    assert diagnostics.hidden_selected_absent_from_view_schema is True
    assert diagnostics.class_weight_transport_covariance is True

    epistemic, ontic = canonical_stage9c_models()
    for clock in SUBSYSTEMS:
        for index in range(3):
            e_view = perspective_qr_view(epistemic, clock, index)
            o_view = perspective_qr_view(ontic, clock, index)
            assert e_view.continuation_ids == ("h_L", "h_R")
            assert e_view.continuation_weights == o_view.continuation_weights
            assert np.allclose(
                e_view.predictive_density,
                o_view.predictive_density,
                atol=ATOL,
                rtol=0.0,
            )
            assert np.allclose(
                e_view.directional_record_scores,
                (1.0, 1.0),
                atol=ATOL,
                rtol=0.0,
            )


def test_stage9d_wrong_continuation_map_and_bare_observable_are_rejected():
    diagnostics = stage9d_transport_diagnostics()
    assert diagnostics.max_cross_continuation_map_difference > ATOL
    assert diagnostics.one_rederived_map_suffices_for_all_continuations is False
    assert diagnostics.wrong_continuation_map_residual > ATOL
    assert diagnostics.wrong_continuation_map_rejected is True
    assert diagnostics.bare_observable_residual > ATOL
    assert diagnostics.bare_observable_rejected is True


def test_stage9d_direct_transport_example_matches_target_state_and_metric():
    continuation = stage9_extension_set(CURRENT_EVENT)[0]
    source = stage9_reduced_support_coordinates(continuation, "A", CURRENT_EVENT)
    target = stage9_reduced_support_coordinates(continuation, "B", 0)
    transform = stage9_clock_change_support_matrix(
        continuation, "B", 0, "A", CURRENT_EVENT
    )
    assert np.allclose(transform @ source, target, atol=ATOL, rtol=0.0)
    source_metric = stage9_support_metric(continuation, "A", CURRENT_EVENT)
    target_metric = stage9_support_metric(continuation, "B", 0)
    assert np.allclose(
        transform.conj().T @ target_metric @ transform,
        source_metric,
        atol=ATOL,
        rtol=0.0,
    )


def test_stage9d_correct_observable_transport_differs_from_bare_matrix_reuse():
    continuation = stage9_extension_set(CURRENT_EVENT)[0]
    physical = physical_event_target_operator(continuation, LOWER_EVENT)
    source_operator = represent_physical_operator(
        continuation, physical, "A", CURRENT_EVENT
    )
    target_operator = represent_physical_operator(continuation, physical, "B", 0)
    transform = stage9_clock_change_support_matrix(
        continuation, "B", 0, "A", CURRENT_EVENT
    )
    transported = transform @ source_operator @ np.linalg.inv(transform)
    assert np.allclose(transported, target_operator, atol=ATOL, rtol=0.0)
    assert not np.allclose(source_operator, target_operator, atol=ATOL, rtol=0.0)


def test_stage9d_does_not_overclaim_future_measurement_or_general_covariance():
    diagnostics = stage9d_transport_diagnostics()
    assert diagnostics.full_stage9c_future_measurement_covariance_established is False
    summary = stage9d_summary()
    assert "full Stage 9C future-measurement covariance remains not_established" in summary["guards"]
    assert "finite clock covariance != general covariance" in summary["guards"]
    assert summary["next"] == "Stage 9E — P/O/R_direction/V compatibility matrix"


def test_stage9d_perspective_view_rejects_wrong_class_correspondence():
    epistemic, _ = canonical_stage9c_models()
    with pytest.raises(ValueError, match="does not preserve Stage 9 QExt classes"):
        perspective_qr_view(
            epistemic,
            "A",
            CURRENT_EVENT,
            correspondence=class_correspondence(epistemic.carrier, "swapped-classes"),
        )
