from dataclasses import fields

import numpy as np
import pytest

from t_search.stage5_clock_change import SUBSYSTEMS
from t_search.stage7_history import CURRENT_EVENT, UPPER_EVENT
from t_search.stage8_continuations import (
    canonical_continuation_left,
    canonical_continuation_right,
    quantum_extension_set,
)
from t_search.stage8_modal import (
    canonical_stage8b_models,
    continuation_by_id,
    make_epistemic_quantum_model,
    matched_uniform_weights,
)
from t_search.stage8_modal_transport import (
    PerspectiveModalView,
    audit_modal_correspondence,
    continuation_clock_change_support_matrix,
    continuation_clock_coordinates,
    continuation_clock_support_basis,
    continuation_family_density_residual,
    continuation_reduced_support_coordinates,
    continuation_support_metric,
    modal_event_correspondence,
    perspective_modal_view,
    stage8d_summary,
    stage8d_transport_diagnostics,
)

ATOL = 1e-9

# The exhaustive diagnostic traverses 108 state transports and 324 three-clock
# compositions. Compute it once for the module.
DIAGNOSTIC = stage8d_transport_diagnostics()


def test_stage8d_each_continuation_rederives_nine_full_rank_support_charts():
    for continuation in quantum_extension_set():
        for clock in SUBSYSTEMS:
            for index in range(3):
                support = continuation_clock_support_basis(continuation, clock, index)
                coordinates = continuation_clock_coordinates(continuation, clock, index)
                metric = continuation_support_metric(continuation, clock, index)

                assert support.shape == (18, 14)
                assert coordinates.shape == (14, 14)
                assert metric.shape == (14, 14)
                assert np.linalg.matrix_rank(coordinates, tol=1e-10) == 14
                assert np.linalg.norm(support.conj().T @ support - np.eye(14)) <= ATOL
                assert np.min(np.linalg.eigvalsh(metric)) > 0.0


def test_stage8d_rederived_maps_transport_each_continuation_state_exactly():
    diagnostic = DIAGNOSTIC
    assert diagnostic.qext_size == 2
    assert diagnostic.perspective_nodes_per_continuation == 9
    assert diagnostic.distinct_clock_state_transports == 108
    assert diagnostic.max_state_transport_residual <= ATOL
    assert diagnostic.max_inverse_residual <= ATOL
    assert diagnostic.continuation_level_pv_covariance is True


def test_stage8d_rederived_maps_preserve_each_continuations_induced_metric():
    assert DIAGNOSTIC.max_metric_covariance_residual <= ATOL


def test_stage8d_three_clock_composition_holds_separately_for_each_continuation():
    assert DIAGNOSTIC.three_clock_compositions == 324
    assert DIAGNOSTIC.max_composition_residual <= ATOL


def test_stage8d_direct_h_right_a_to_b_transport_uses_h_right_map():
    continuation = canonical_continuation_right()
    transform = continuation_clock_change_support_matrix(
        continuation, "B", 0, "A", CURRENT_EVENT
    )
    source = continuation_reduced_support_coordinates(
        continuation, "A", CURRENT_EVENT
    )
    target = continuation_reduced_support_coordinates(continuation, "B", 0)
    source_metric = continuation_support_metric(continuation, "A", CURRENT_EVENT)
    target_metric = continuation_support_metric(continuation, "B", 0)

    assert np.linalg.norm(transform @ source - target) <= ATOL
    assert np.linalg.norm(transform.conj().T @ target_metric @ transform - source_metric) <= ATOL


def test_stage8d_modal_correspondence_explicitly_preserves_event_and_physical_classes():
    epistemic, _ = canonical_stage8b_models()
    chi = modal_event_correspondence(epistemic.carrier, "preserving")
    audit = audit_modal_correspondence(epistemic.carrier, chi)

    assert chi.source_current_event == CURRENT_EVENT
    assert chi.target_current_event == CURRENT_EVENT
    assert chi.class_map == (("h_L", "h_L"), ("h_R", "h_R"))
    assert audit.bijective is True
    assert audit.current_event_preserved is True
    assert audit.physical_classes_preserved is True
    assert audit.source_qext_size == audit.target_qext_size == 2
    assert audit.valid is True


def test_stage8d_equal_numeric_clock_readings_are_not_used_as_event_identity():
    epistemic, _ = canonical_stage8b_models()
    chi = modal_event_correspondence(epistemic.carrier, "preserving")
    view = perspective_modal_view(epistemic, "B", 0, correspondence=chi)

    # The relational current event remains e1 while the chosen B-clock chart is j=0.
    assert view.current_event == CURRENT_EVENT
    assert view.clock == "B"
    assert view.clock_index == 0
    assert view.current_event != view.clock_index


def test_stage8d_matched_typed_models_have_equal_transported_modal_views_at_all_nodes():
    epistemic, ontic = canonical_stage8b_models(selected_id="h_L")
    chi = modal_event_correspondence(epistemic.carrier, "preserving")

    for clock in SUBSYSTEMS:
        for index in range(3):
            left = perspective_modal_view(epistemic, clock, index, correspondence=chi)
            right = perspective_modal_view(ontic, clock, index, correspondence=chi)
            assert left == right

    assert DIAGNOSTIC.matched_modal_views_all_nodes is True
    assert DIAGNOSTIC.max_weight_transport_residual <= ATOL
    assert DIAGNOSTIC.class_weight_pv_covariance is True


def test_stage8d_hidden_selected_continuation_swap_does_not_change_public_modal_transport():
    epistemic, _ = canonical_stage8b_models(selected_id="h_L")
    carrier = epistemic.carrier
    swapped = make_epistemic_quantum_model(
        carrier,
        continuation_by_id(carrier, "h_R"),
        matched_uniform_weights(carrier),
    )
    chi = modal_event_correspondence(carrier, "preserving")

    for clock in SUBSYSTEMS:
        for index in range(3):
            assert perspective_modal_view(
                epistemic, clock, index, correspondence=chi
            ) == perspective_modal_view(swapped, clock, index, correspondence=chi)

    assert DIAGNOSTIC.selected_swap_modal_views_all_nodes is True


def test_stage8d_public_modal_view_schema_does_not_expose_hidden_selected_future():
    names = {field.name for field in fields(PerspectiveModalView)}
    for forbidden in (
        "selected_continuation",
        "selected_history",
        "selector",
        "model_type",
    ):
        assert forbidden not in names
    assert DIAGNOSTIC.hidden_selected_absent_from_modal_view_schema is True


def test_stage8d_swapping_physical_continuation_classes_is_not_a_valid_correspondence():
    epistemic, _ = canonical_stage8b_models()
    wrong = modal_event_correspondence(epistemic.carrier, "swapped-classes")
    audit = audit_modal_correspondence(epistemic.carrier, wrong)

    assert audit.bijective is True
    assert audit.current_event_preserved is True
    assert audit.physical_classes_preserved is False
    assert audit.valid is False
    with pytest.raises(ValueError, match="does not preserve current QExt physical classes"):
        perspective_modal_view(epistemic, "B", 0, correspondence=wrong)
    assert DIAGNOSTIC.wrong_class_correspondence_rejected is True


def test_stage8d_misdeclaring_terminal_e2_as_current_e1_fails_qext_correspondence():
    epistemic, _ = canonical_stage8b_models()
    wrong = modal_event_correspondence(
        epistemic.carrier, "misdeclared-terminal-preserving"
    )
    audit = audit_modal_correspondence(epistemic.carrier, wrong)

    assert wrong.source_current_event == CURRENT_EVENT
    assert wrong.target_current_event == UPPER_EVENT
    assert audit.current_event_preserved is False
    assert audit.source_qext_size == 2
    assert audit.target_qext_size == 0
    assert audit.valid is False
    with pytest.raises(ValueError, match="does not preserve current QExt physical classes"):
        perspective_modal_view(epistemic, "C", 1, correspondence=wrong)
    assert DIAGNOSTIC.terminal_current_correspondence_rejected is True


def test_stage8d_reusing_h_left_map_for_h_right_is_a_detectable_negative_control():
    assert DIAGNOSTIC.wrong_continuation_map_residual > ATOL, (
        "wrong h_L map unexpectedly transported every tested h_R state; residual="
        f"{DIAGNOSTIC.wrong_continuation_map_residual}"
    )
    assert DIAGNOSTIC.wrong_continuation_map_rejected is True


def test_stage8d_continuation_specific_atlases_are_not_assumed_identical():
    assert DIAGNOSTIC.max_cross_continuation_map_difference > ATOL, (
        "h_L/h_R support-map difference was below tolerance: "
        f"{DIAGNOSTIC.max_cross_continuation_map_difference}"
    )
    assert DIAGNOSTIC.one_rederived_map_suffices_for_all_continuations is False


def test_stage8d_a_e1_shared_current_actuality_remains_the_stage8a_anchor_control():
    assert continuation_family_density_residual("A", CURRENT_EVENT) <= ATOL
    assert DIAGNOSTIC.a_e1_shared_current_density_residual <= ATOL


def test_stage8d_non_a_same_reading_family_residuals_are_measured_not_assumed_zero():
    # Stage 8D records how the A/e1 shared-current construction looks in B/C
    # conditional charts. No claim of equality is hard-coded here.
    assert DIAGNOSTIC.min_non_a_same_reading_density_residual >= 0.0
    assert DIAGNOSTIC.max_non_a_same_reading_density_residual >= (
        DIAGNOSTIC.min_non_a_same_reading_density_residual
    )


def test_stage8d_does_not_promote_class_transport_to_full_stage8c_measurement_covariance():
    # The two continuation-specific atlases differ, so Stage 8D must not silently
    # reuse one map as a universal transport of the Stage 8C cross-continuation
    # future-signature measurement.
    assert DIAGNOSTIC.continuation_level_pv_covariance is True
    assert DIAGNOSTIC.class_weight_pv_covariance is True
    assert DIAGNOSTIC.one_rederived_map_suffices_for_all_continuations is False
    assert DIAGNOSTIC.full_stage8c_measurement_covariance_established is False


def test_stage8d_summary_preserves_typing_and_interpretation_guards():
    summary = stage8d_summary()
    guards = summary["guards"]
    assert "equal numeric clock readings != event identity" in guards
    assert "continuation-aware P-V transport != one universal h-independent linear map" in guards
    assert "branch-specific perspective map != hidden branch selection" in guards
    assert "P-V covariance != P=V" in guards
    assert "QExt represented != ontically real futures by definition" in guards
    assert summary["next"] == "Stage 8E — P/O/R/V compatibility and underdetermination"
