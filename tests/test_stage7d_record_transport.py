import numpy as np
import pytest

from t_search.stage5_clock_change import SUBSYSTEMS
from t_search.stage7_history import CURRENT_EVENT, canonical_physical_history_state
from t_search.stage7_record_transport import (
    event_correspondence,
    history_clock_change_support_matrix,
    history_clock_probability,
    history_clock_reconstruction_operator,
    history_clock_reduction_matrix,
    history_clock_reduction_operator,
    history_clock_support_basis,
    history_clock_support_projector,
    history_support_metric,
    perspective_record_assessment,
    perspective_record_joint_distribution,
    reduced_history_support_coordinates,
    stage7d_reduction_diagnostics,
    stage7d_summary,
    stage7d_transport_diagnostics,
)

ATOL = 1e-9


def test_event_correspondences_are_explicit_and_typed():
    preserving = event_correspondence("preserving")
    reversing = event_correspondence("reversing")
    wrong = event_correspondence("misdeclared-preserving")

    assert preserving.target_events == ("e0", "e1", "e2")
    assert preserving.orientation_sign == 1
    assert reversing.target_events == ("e2", "e1", "e0")
    assert reversing.orientation_sign == -1
    assert wrong.target_events == reversing.target_events
    assert wrong.orientation_sign == 1
    assert wrong.declared_orientation == "preserving"


def test_all_nine_interacting_clock_nodes_remain_full_rank_with_proper_supports():
    for clock in SUBSYSTEMS:
        for index in range(3):
            reduction = history_clock_reduction_matrix("forward", clock, index)
            support = history_clock_support_basis("forward", clock, index)
            assert reduction.shape == (18, 14)
            assert support.shape == (18, 14)
            assert np.linalg.matrix_rank(reduction, tol=1e-10) == 14
            assert np.linalg.norm(support.conj().T @ support - np.eye(14)) <= ATOL


def test_a_clock_stays_isometric_but_b_c_become_nonisometric():
    diagnostic = stage7d_reduction_diagnostics()
    assert diagnostic.nodes == 9
    assert diagnostic.min_rank == 14
    assert diagnostic.max_a_isometry_residual <= ATOL
    assert diagnostic.min_non_a_isometry_residual > 1e-3
    assert diagnostic.max_non_a_isometry_residual > 1e-3
    assert diagnostic.max_condition_number > 1.0


def test_rederived_reconstruction_roundtrips_all_clock_nodes():
    diagnostic = stage7d_reduction_diagnostics()
    assert diagnostic.max_support_roundtrip_residual <= ATOL
    assert diagnostic.max_physical_roundtrip_residual <= ATOL


def test_clock_probabilities_are_normalized_but_interaction_makes_b_c_nonuniform():
    state = canonical_physical_history_state("forward")
    probabilities = {
        clock: np.array(
            [history_clock_probability(state, "forward", clock, j) for j in range(3)]
        )
        for clock in SUBSYSTEMS
    }
    assert np.allclose(probabilities["A"], [1 / 3, 1 / 3, 1 / 3], atol=ATOL, rtol=0.0)
    assert np.allclose(probabilities["B"], [4 / 9, 5 / 18, 5 / 18], atol=ATOL, rtol=0.0)
    assert np.allclose(probabilities["C"], [7 / 18, 7 / 18, 2 / 9], atol=ATOL, rtol=0.0)
    for clock in SUBSYSTEMS:
        assert abs(float(np.sum(probabilities[clock])) - 1.0) <= ATOL


def test_induced_support_metrics_are_positive_and_recover_physical_norm():
    state = canonical_physical_history_state("forward")
    for clock in SUBSYSTEMS:
        for index in range(3):
            metric = history_support_metric("forward", clock, index)
            eigenvalues = np.linalg.eigvalsh(metric)
            coordinates = reduced_history_support_coordinates(
                state, "forward", clock, index
            )
            norm = np.vdot(coordinates, metric @ coordinates)
            assert np.min(eigenvalues) > 0.0
            assert abs(norm.imag) <= ATOL
            assert abs(float(norm.real) - 1.0) <= ATOL


def test_rederived_genuine_clock_changes_transport_same_physical_state():
    diagnostic = stage7d_transport_diagnostics()
    assert diagnostic.distinct_clock_comparisons == 54
    assert diagnostic.max_state_transport_residual <= ATOL
    assert diagnostic.max_inverse_residual <= ATOL


def test_nonunitary_interacting_maps_preserve_induced_physical_metric():
    diagnostic = stage7d_transport_diagnostics()
    assert diagnostic.max_metric_covariance_residual <= ATOL
    assert diagnostic.max_euclidean_unitarity_residual > 1e-3


def test_direct_metric_covariance_for_one_a_to_b_map():
    transform = history_clock_change_support_matrix(
        "forward", "B", 0, "A", CURRENT_EVENT
    )
    source_metric = history_support_metric("forward", "A", CURRENT_EVENT)
    target_metric = history_support_metric("forward", "B", 0)
    assert (
        np.linalg.norm(transform.conj().T @ target_metric @ transform - source_metric)
        <= ATOL
    )


def test_record_projectors_are_metric_self_adjoint_idempotent_and_commuting():
    diagnostic = stage7d_transport_diagnostics()
    assert diagnostic.max_metric_self_adjoint_residual <= ATOL
    assert diagnostic.max_projector_residual <= ATOL
    assert diagnostic.max_record_memory_commutator_residual <= ATOL


@pytest.mark.parametrize("clock", SUBSYSTEMS)
@pytest.mark.parametrize("index", range(3))
def test_orientation_preserving_chi_preserves_stage7c_record_profile(clock, index):
    assessment = perspective_record_assessment(clock, index, chi="preserving")
    assert assessment.lower_information == pytest.approx(1.0, abs=ATOL)
    assert assessment.upper_information == pytest.approx(0.0, abs=ATOL)
    assert assessment.lower_accuracy == pytest.approx(1.0, abs=ATOL)
    assert assessment.upper_accuracy == pytest.approx(0.5, abs=ATOL)
    assert assessment.record_score == pytest.approx(1.0, abs=ATOL)
    assert assessment.accessibility_score == pytest.approx(0.5, abs=ATOL)
    assert assessment.orientation == "lower-index"
    assert assessment.record_defined
    assert assessment.metric_norm == pytest.approx(1.0, abs=ATOL)


@pytest.mark.parametrize("clock", SUBSYSTEMS)
@pytest.mark.parametrize("index", range(3))
def test_orientation_reversing_chi_flips_signed_record_profile(clock, index):
    assessment = perspective_record_assessment(clock, index, chi="reversing")
    assert assessment.lower_information == pytest.approx(0.0, abs=ATOL)
    assert assessment.upper_information == pytest.approx(1.0, abs=ATOL)
    assert assessment.record_score == pytest.approx(-1.0, abs=ATOL)
    assert assessment.accessibility_score == pytest.approx(-0.5, abs=ATOL)
    assert assessment.orientation == "upper-index"
    assert assessment.record_defined


def test_transporting_corresponding_record_observables_preserves_statistics():
    diagnostic = stage7d_transport_diagnostics()
    assert diagnostic.max_observable_transport_residual <= ATOL
    assert diagnostic.max_preserving_record_score_residual <= ATOL
    assert diagnostic.max_preserving_accessibility_residual <= ATOL
    assert diagnostic.preserving_covariance


def test_orientation_reversing_correspondence_obeys_predeclared_sign_rule():
    diagnostic = stage7d_transport_diagnostics()
    assert diagnostic.max_reversing_record_sign_residual <= ATOL
    assert diagnostic.max_reversing_accessibility_sign_residual <= ATOL
    assert diagnostic.reversing_covariance


def test_stage7a_spectator_map_is_not_reused_as_interacting_clock_change():
    diagnostic = stage7d_transport_diagnostics()
    assert diagnostic.legacy_spectator_map_state_residual > 1e-3
    assert diagnostic.legacy_map_rejected


def test_leaving_source_bare_observable_untransported_is_rejected():
    diagnostic = stage7d_transport_diagnostics()
    assert diagnostic.bare_observable_residual > 1e-3
    assert diagnostic.bare_metric_self_adjoint_residual > 1e-3
    assert diagnostic.bare_observable_rejected


def test_misdeclared_reversing_chi_fails_preserving_covariance_rule():
    diagnostic = stage7d_transport_diagnostics()
    assert diagnostic.wrong_chi_record_score_residual == pytest.approx(2.0, abs=ATOL)
    assert diagnostic.wrong_chi_accessibility_residual == pytest.approx(1.0, abs=ATOL)
    assert diagnostic.wrong_chi_rejected


def test_joint_distributions_are_normalized_in_nonideal_b_clock_perspective():
    for event in (0, 2):
        joint, *_ = perspective_record_joint_distribution("B", 0, event)
        assert np.min(joint) >= -ATOL
        assert np.sum(joint) == pytest.approx(1.0, abs=ATOL)


def test_stage7d_summary_preserves_typing_guards():
    summary = stage7d_summary()
    guards = summary["guards"]
    assert "equal numeric clock readings != event identity" in guards
    assert "interacting clock change != inherited spectator clock change" in guards
    assert "record covariance != P=R" in guards
    assert summary["transport"]["preserving_covariance"] is True
    assert summary["transport"]["legacy_map_rejected"] is True
