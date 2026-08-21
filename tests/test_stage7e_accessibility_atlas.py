import math

import numpy as np
import pytest

from t_search.stage7_accessibility_atlas import (
    apply_memory_interface,
    local_accessibility_assessment,
    memory_readout_channel,
    partial_atlas_path_assessment,
    stage7e_accessibility_diagnostics,
    stage7e_partial_atlas_diagnostics,
    stage7e_summary,
)

ATOL = 1e-9


def test_memory_interfaces_are_explicit_stochastic_channels():
    for kind in ("full", "hidden", "maximally-noisy", "coarse"):
        channel = memory_readout_channel(kind)
        assert channel.shape == (2, 2)
        assert np.min(channel) >= 0.0
        assert np.allclose(np.sum(channel, axis=1), 1.0, atol=ATOL, rtol=0.0)


def test_hidden_and_maximally_noisy_are_distinct_interfaces():
    hidden = memory_readout_channel("hidden")
    noisy = memory_readout_channel("maximally-noisy")
    assert not np.allclose(hidden, noisy, atol=ATOL, rtol=0.0)
    assert np.allclose(hidden, [[1.0, 0.0], [1.0, 0.0]], atol=ATOL, rtol=0.0)
    assert np.allclose(noisy, 0.5, atol=ATOL, rtol=0.0)


def test_interface_application_preserves_total_probability():
    joint = np.array([[0.5, 0.0], [0.0, 0.5]])
    for kind in ("full", "hidden", "maximally-noisy", "coarse"):
        visible = apply_memory_interface(joint, kind)
        assert visible.shape == (2, 2)
        assert np.min(visible) >= -ATOL
        assert np.sum(visible) == pytest.approx(1.0, abs=ATOL)


@pytest.mark.parametrize("clock", ("A", "B", "C"))
@pytest.mark.parametrize("index", range(3))
def test_full_access_recovers_global_record_profile(clock, index):
    assessment = local_accessibility_assessment(clock, index, "full")
    assert assessment.globally_represented
    assert assessment.locally_accessible
    assert assessment.global_record_score == pytest.approx(1.0, abs=ATOL)
    assert assessment.global_accessibility_score == pytest.approx(0.5, abs=ATOL)
    assert assessment.local_record_score == pytest.approx(1.0, abs=ATOL)
    assert assessment.local_accessibility_score == pytest.approx(0.5, abs=ATOL)
    assert assessment.local_orientation == "lower-index"


@pytest.mark.parametrize("interface", ("hidden", "maximally-noisy"))
def test_inaccessible_interfaces_leave_global_record_present(interface):
    assessment = local_accessibility_assessment("B", 0, interface)
    assert assessment.globally_represented
    assert assessment.global_record_score == pytest.approx(1.0, abs=ATOL)
    assert assessment.global_orientation == "lower-index"
    assert assessment.local_record_score == pytest.approx(0.0, abs=ATOL)
    assert assessment.local_accessibility_score == pytest.approx(0.0, abs=ATOL)
    assert assessment.local_orientation == "none"
    assert not assessment.locally_accessible


def test_coarse_access_is_degraded_without_erasing_orientation():
    assessment = local_accessibility_assessment("C", 2, "coarse")
    expected_information = 1.0 - (
        -0.25 * math.log2(0.25) - 0.75 * math.log2(0.75)
    )
    assert assessment.globally_represented
    assert assessment.locally_accessible
    assert assessment.local_lower_information == pytest.approx(expected_information, abs=ATOL)
    assert assessment.local_upper_information == pytest.approx(0.0, abs=ATOL)
    assert assessment.local_record_score == pytest.approx(expected_information, abs=ATOL)
    assert assessment.local_accessibility_score == pytest.approx(0.25, abs=ATOL)
    assert assessment.local_orientation == "lower-index"
    assert assessment.local_record_score < assessment.global_record_score
    assert assessment.local_accessibility_score < assessment.global_accessibility_score


def test_accessibility_diagnostic_separates_global_and_local_roles_at_all_nodes():
    diagnostic = stage7e_accessibility_diagnostics()
    assert diagnostic.nodes_tested == 9
    assert diagnostic.interfaces_tested == 4
    assert diagnostic.max_full_global_local_record_residual <= ATOL
    assert diagnostic.max_full_global_local_accessibility_residual <= ATOL
    assert diagnostic.max_hidden_local_record_score <= ATOL
    assert diagnostic.max_hidden_local_accessibility_score <= ATOL
    assert diagnostic.max_noisy_local_record_score <= ATOL
    assert diagnostic.max_noisy_local_accessibility_score <= ATOL
    assert diagnostic.global_record_survives_hidden
    assert diagnostic.global_record_survives_noisy
    assert diagnostic.hidden_is_inaccessible
    assert diagnostic.noisy_is_inaccessible
    assert diagnostic.coarse_is_degraded_but_accessible


@pytest.mark.parametrize("intermediate_index", range(3))
def test_missing_direct_edge_has_three_consistent_indirect_paths(intermediate_index):
    assessment = partial_atlas_path_assessment(intermediate_index)
    assert assessment.source == "A/e1"
    assert assessment.target == "B/e0"
    assert not assessment.direct_edge_available
    assert not assessment.perturbed
    assert assessment.map_residual <= ATOL
    assert assessment.state_residual <= ATOL
    assert assessment.metric_covariance_residual <= ATOL
    assert assessment.max_observable_residual <= ATOL
    assert assessment.record_score == pytest.approx(1.0, abs=ATOL)
    assert assessment.accessibility_score == pytest.approx(0.5, abs=ATOL)
    assert assessment.record_score_residual <= ATOL
    assert assessment.accessibility_score_residual <= ATOL
    assert assessment.consistent


def test_perturbation_is_attached_to_one_declared_local_edge():
    assessment = partial_atlas_path_assessment(1, perturb_local_edge=True)
    assert assessment.intermediate == "C/e1"
    assert assessment.perturbed
    assert assessment.map_residual > 1e-3
    assert assessment.state_residual > 1e-3
    assert assessment.metric_covariance_residual > 1e-3
    assert assessment.max_observable_residual > 1e-3
    assert assessment.record_score_residual > 1e-4
    assert not assessment.consistent


def test_perturbation_request_on_other_edge_is_rejected():
    with pytest.raises(ValueError):
        partial_atlas_path_assessment(0, perturb_local_edge=True)


def test_partial_atlas_diagnostic_localizes_failure_to_perturbed_path():
    diagnostic = stage7e_partial_atlas_diagnostics()
    assert diagnostic.source == "A/e1"
    assert diagnostic.target == "B/e0"
    assert not diagnostic.direct_edge_available
    assert diagnostic.ideal_indirect_paths == 3
    assert diagnostic.max_ideal_map_residual <= ATOL
    assert diagnostic.max_ideal_state_residual <= ATOL
    assert diagnostic.max_ideal_metric_residual <= ATOL
    assert diagnostic.max_ideal_observable_residual <= ATOL
    assert diagnostic.max_ideal_record_score_residual <= ATOL
    assert diagnostic.max_ideal_accessibility_residual <= ATOL
    assert diagnostic.perturbed_intermediate == "C/e1"
    assert diagnostic.perturbed_map_residual > 1e-3
    assert diagnostic.perturbed_state_residual > 1e-3
    assert diagnostic.perturbed_metric_residual > 1e-3
    assert diagnostic.perturbed_observable_residual > 1e-3
    assert diagnostic.perturbed_record_score_residual > 1e-4
    assert diagnostic.ideal_paths_consistent
    assert diagnostic.perturbation_detected
    assert diagnostic.localized_failure


def test_stage7e_summary_preserves_typing_guards():
    summary = stage7e_summary()
    guards = summary["guards"]
    assert "locally inaccessible record != globally absent record" in guards
    assert "global reconstructibility != local accessibility" in guards
    assert "indirect reconstructibility != direct local edge availability" in guards
    assert "partial atlas path consistency != universal frame availability" in guards
    assert "localized path inconsistency != spacetime curvature" in guards
    assert "record covariance != P=R" in guards
    assert summary["canonical_missing_edge"] == "A/e1 -> B/e0"
    assert summary["perturbed_edge"] == "C/e1 -> B/e0"
