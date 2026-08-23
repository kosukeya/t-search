import pytest

from t_search.stage11_compatibility import (
    STAGE11E_WRONG_PATH_CLASSIFICATION,
    canonical_stage11e_clock_transports,
    canonical_stage11e_reparameterization_transports,
    stage11e_diagnostics,
    stage11e_wrong_path_control,
)


@pytest.fixture(scope="module")
def diagnostics():
    return stage11e_diagnostics()


def test_stage11e_represents_both_transport_families_with_explicit_typing(diagnostics) -> None:
    reparam = canonical_stage11e_reparameterization_transports()
    clock = canonical_stage11e_clock_transports()
    assert len(reparam) == 12
    assert len(clock) == 108
    assert diagnostics.parameterization_count == 4
    assert diagnostics.clock_node_count == 9
    assert diagnostics.continuation_count == 2
    assert diagnostics.all_reparameterization_transports_valid
    assert diagnostics.all_clock_transports_valid
    assert diagnostics.nontrivial_reparameterization_transport_count > 0
    assert diagnostics.nontrivial_clock_transport_count > 0


def test_stage11e_relational_event_squares_commute(diagnostics) -> None:
    assert diagnostics.event_square_count == 648
    assert diagnostics.max_event_path_residual <= 1e-9


def test_stage11e_measurement_and_probability_squares_commute(diagnostics) -> None:
    assert diagnostics.measurement_square_count == 1296
    assert diagnostics.max_measurement_path_normalization_residual <= 1e-9
    assert diagnostics.max_measurement_path_effect_residual <= 1e-9
    assert diagnostics.max_measurement_direct_target_normalization_residual <= 1e-9
    assert diagnostics.max_measurement_direct_target_effect_residual <= 1e-9
    assert diagnostics.max_measurement_probability_path_residual <= 1e-9
    assert diagnostics.max_measurement_direct_target_probability_residual <= 1e-9


def test_stage11e_weighted_modal_outputs_are_path_independent(diagnostics) -> None:
    assert diagnostics.weighted_square_count == 648
    assert diagnostics.max_weighted_path_residual <= 1e-9
    assert diagnostics.max_matched_modal_endpoint_residual <= 1e-9
    assert diagnostics.max_hidden_hstar_endpoint_residual <= 1e-9


def test_stage11e_common_evidence_updates_are_path_independent(diagnostics) -> None:
    assert diagnostics.posterior_square_count == 648
    assert diagnostics.max_epistemic_posterior_path_residual <= 1e-9
    assert diagnostics.max_ontic_posterior_path_residual <= 1e-9
    assert diagnostics.max_epistemic_ontic_posterior_endpoint_residual <= 1e-9
    assert diagnostics.epistemic_hidden_selection_preserved
    assert diagnostics.ontic_selector_free_all_endpoints


def test_stage11e_wrong_path_is_detectably_noncommuting(diagnostics) -> None:
    control = stage11e_wrong_path_control()
    assert control.detected
    assert control.classification == STAGE11E_WRONG_PATH_CLASSIFICATION
    assert control.normalization_residual > 1e-9
    assert control.effect_residual > 1e-9
    assert control.probability_residual > 1e-9
    assert diagnostics.wrong_path_control_detected


def test_stage11e_criteria_39_43_are_satisfied(diagnostics) -> None:
    assert diagnostics.criteria_39_43_satisfied
