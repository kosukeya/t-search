from dataclasses import fields

import numpy as np

from t_search.stage5_clock_change import DEFAULT_ATOL, SUBSYSTEMS
from t_search.stage9_modal import (
    FUTURE_SIGNATURE_LEFT,
    Stage9Evidence,
    canonical_stage9c_models,
    continuation_by_id,
    make_stage9_epistemic_model,
    make_stage9_ontic_model,
    matched_uniform_weights,
)
from t_search.stage10_modal import (
    Stage10EPublicMeasurementView,
    stage10e_modal_diagnostics,
    stage10e_posterior_view,
    stage10e_public_measurement_view,
    stage10e_weighted_prediction,
)


DIAGNOSTICS = stage10e_modal_diagnostics()


def _residual(left, right) -> float:
    lhs = dict(left)
    rhs = dict(right)
    assert set(lhs) == set(rhs)
    return max(abs(lhs[name] - rhs[name]) for name in lhs)


def test_stage10e_criterion39_weighted_future_predictions_are_covariant() -> None:
    epistemic, ontic = canonical_stage9c_models(selected_id="h_L")
    assert DIAGNOSTICS.weighted_prediction_covariance
    reference_e = stage10e_weighted_prediction(epistemic, "A", 0)
    reference_o = stage10e_weighted_prediction(ontic, "A", 0)
    assert _residual(reference_e, reference_o) <= 10 * DEFAULT_ATOL
    for clock in SUBSYSTEMS:
        for index in range(3):
            assert _residual(
                reference_e,
                stage10e_weighted_prediction(epistemic, clock, index),
            ) <= 10 * DEFAULT_ATOL
            assert _residual(
                reference_o,
                stage10e_weighted_prediction(ontic, clock, index),
            ) <= 10 * DEFAULT_ATOL
    assert DIAGNOSTICS.max_weighted_prediction_covariance_residual <= 1e-9


def test_stage10e_criterion40_matched_epistemic_ontic_public_views_agree_all_nodes() -> None:
    epistemic, ontic = canonical_stage9c_models(selected_id="h_L")
    assert DIAGNOSTICS.matched_epistemic_ontic_views_all_nodes
    assert DIAGNOSTICS.matched_modal_public_view_covariance
    for clock in SUBSYSTEMS:
        for index in range(3):
            e = stage10e_public_measurement_view(epistemic, clock, index)
            o = stage10e_public_measurement_view(ontic, clock, index)
            assert e.current_event == o.current_event
            assert e.clock == o.clock and e.clock_index == o.clock_index
            assert e.continuation_ids == o.continuation_ids
            assert e.next_outcomes == o.next_outcomes
            assert np.allclose(e.continuation_weights, o.continuation_weights)
            assert np.allclose(e.predictive_density, o.predictive_density)
            assert _residual(e.next_probabilities, o.next_probabilities) <= 10 * DEFAULT_ATOL


def test_stage10e_criterion41_hidden_hstar_swap_is_publicly_invariant_and_schema_free() -> None:
    epistemic, _ = canonical_stage9c_models(selected_id="h_L")
    carrier = epistemic.carrier
    weights = matched_uniform_weights(carrier)
    swapped = make_stage9_epistemic_model(
        carrier,
        continuation_by_id(carrier, "h_R"),
        weights,
    )
    assert DIAGNOSTICS.hidden_selected_absent_from_public_schema
    assert DIAGNOSTICS.hidden_hstar_swap_views_all_nodes
    assert DIAGNOSTICS.hidden_hstar_swap_invariant
    assert DIAGNOSTICS.privileged_modal_roles_still_distinct

    schema = {field.name for field in fields(Stage10EPublicMeasurementView)}
    for forbidden in (
        "selected_continuation",
        "selected_continuation_id",
        "selector",
        "model_type",
        "modal_type",
        "belief_weights",
        "extension_weights",
    ):
        assert forbidden not in schema

    for clock in SUBSYSTEMS:
        for index in range(3):
            left = stage10e_public_measurement_view(epistemic, clock, index)
            right = stage10e_public_measurement_view(swapped, clock, index)
            assert left == right


def test_stage10e_criterion42_weight_mismatch_remains_visible_with_same_meaning() -> None:
    epistemic, _ = canonical_stage9c_models(selected_id="h_L")
    mismatch = make_stage9_ontic_model(epistemic.carrier, (0.75, 0.25))
    assert DIAGNOSTICS.weight_mismatch_visible_all_nodes
    assert DIAGNOSTICS.weight_mismatch_transport_covariance
    assert DIAGNOSTICS.minimum_weight_mismatch_prediction_difference > 1e-9
    assert DIAGNOSTICS.max_weight_mismatch_covariance_residual <= 1e-9

    reference_uniform = stage10e_weighted_prediction(epistemic, "A", 0)
    reference_mismatch = stage10e_weighted_prediction(mismatch, "A", 0)
    assert _residual(reference_uniform, reference_mismatch) > 1e-9
    for clock in SUBSYSTEMS:
        for index in range(3):
            assert _residual(
                reference_mismatch,
                stage10e_weighted_prediction(mismatch, clock, index),
            ) <= 10 * DEFAULT_ATOL


def test_stage10e_criterion43_common_evidence_posteriors_are_covariant_and_ontic_selector_free() -> None:
    epistemic, ontic = canonical_stage9c_models(selected_id="h_L")
    evidence = Stage9Evidence(FUTURE_SIGNATURE_LEFT)
    assert DIAGNOSTICS.evidence_update_covariance
    assert DIAGNOSTICS.epistemic_hidden_selection_preserved
    assert DIAGNOSTICS.ontic_updated_selector_free_all_nodes
    assert DIAGNOSTICS.max_epistemic_posterior_covariance_residual <= 1e-9
    assert DIAGNOSTICS.max_ontic_posterior_covariance_residual <= 1e-9
    assert DIAGNOSTICS.max_epistemic_ontic_posterior_residual <= 1e-9
    assert DIAGNOSTICS.stage9c_epistemic_posterior_residual <= 1e-9
    assert DIAGNOSTICS.stage9c_ontic_posterior_residual <= 1e-9

    reference = stage10e_posterior_view(epistemic, ontic, evidence, "A", 0)
    for clock in SUBSYSTEMS:
        for index in range(3):
            view = stage10e_posterior_view(epistemic, ontic, evidence, clock, index)
            assert np.allclose(
                view.epistemic_posterior_weights,
                reference.epistemic_posterior_weights,
                atol=10 * DEFAULT_ATOL,
                rtol=0.0,
            )
            assert np.allclose(
                view.ontic_posterior_weights,
                reference.ontic_posterior_weights,
                atol=10 * DEFAULT_ATOL,
                rtol=0.0,
            )
            assert view.epistemic_selected_continuation_id == "h_L"
            assert view.ontic_no_selected_complete_continuation_datum


def test_stage10e_weighted_modal_update_covariance_is_established_only_as_operational_scope() -> None:
    assert DIAGNOSTICS.weighted_modal_update_covariance_established
