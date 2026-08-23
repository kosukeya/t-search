from functools import lru_cache

import numpy as np

from t_search.stage7_history import CURRENT_EVENT, UPPER_EVENT
from t_search.stage9_modal import FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_OTHER
from t_search.stage10_reference import STAGE10_REFERENCE_FAMILY_ID
from t_search.stage11_measurement import (
    STAGE11D_REFERENCE_CLOCK,
    Stage11DWeightedPublicView,
    canonical_stage11d_measurement_views,
    stage11d_controls,
    stage11d_diagnostics,
)
from t_search.stage11_parametrized import STAGE11A_ATOL, STAGE11A_IDENTITY


@lru_cache(maxsize=1)
def _diagnostics():
    return stage11d_diagnostics()


def _probability_residual(left, right) -> float:
    lhs = dict(left)
    rhs = dict(right)
    assert set(lhs) == set(rhs)
    return max(abs(lhs[name] - rhs[name]) for name in lhs)


def test_stage11d_reference_measurement_question_and_typed_event_bridge() -> None:
    views = canonical_stage11d_measurement_views()
    assert len(views) == 8
    assert {item.family_id for item in views} == {STAGE10_REFERENCE_FAMILY_ID}
    assert {item.continuation_id for item in views} == {"h_L", "h_R"}
    assert {item.prediction_anchor for item in views} == {CURRENT_EVENT}
    assert {item.target_event for item in views} == {UPPER_EVENT}
    assert {item.internal_clock for item in views} == {STAGE11D_REFERENCE_CLOCK}
    assert {item.internal_clock_index for item in views} == {UPPER_EVENT}
    assert {item.outcome_ids for item in views} == {
        (FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_OTHER)
    }

    assert len({item.anchor_physical_event_id for item in views}) == 1
    assert len({item.target_physical_event_id for item in views}) == 1
    assert views[0].anchor_physical_event_id != views[0].target_physical_event_id
    assert len({item.anchor_parameter_value for item in views}) > 1
    assert len({item.target_parameter_value for item in views}) > 1
    assert len({item.anchor_clock_value for item in views}) == 1
    assert len({item.target_clock_value for item in views}) == 1


def test_stage11d_per_continuation_probabilities_are_reparameterization_covariant() -> None:
    views = canonical_stage11d_measurement_views()
    for continuation_id in ("h_L", "h_R"):
        group = [item for item in views if item.continuation_id == continuation_id]
        assert len(group) == 4
        reference = next(
            item for item in group if item.parameterization_id == STAGE11A_IDENTITY
        )
        for item in group:
            assert _probability_residual(reference.probabilities, item.probabilities) <= 1e-9
            assert item.probability_sum_residual <= 1e-9
            assert all(-1e-9 <= value <= 1.0 + 1e-9 for _, value in item.probabilities)


def test_stage11d_completeness_positivity_and_normalization_remain_valid() -> None:
    views = canonical_stage11d_measurement_views()
    for item in views:
        assert item.completeness_residual <= 1e-9
        assert item.minimum_effect_eigenvalue >= -1e-9
        assert item.minimum_normalization_eigenvalue > 1e-9
        assert item.normalization_denominator > 1e-9
        assert item.normalization_semantics


def test_stage11d_weighted_predictions_and_matched_modal_views_are_covariant() -> None:
    diagnostics = _diagnostics()
    assert diagnostics.weighted_public_view_count == 8
    assert diagnostics.max_weighted_prediction_reparameterization_residual <= 1e-9
    assert diagnostics.matched_epistemic_ontic_public_views_all_parameterizations
    assert diagnostics.hidden_hstar_swap_public_views_all_parameterizations
    assert diagnostics.privileged_modal_roles_still_distinct
    assert diagnostics.public_weighted_schema_selector_free


def test_stage11d_common_evidence_posteriors_are_reparameterization_covariant() -> None:
    diagnostics = _diagnostics()
    assert diagnostics.posterior_parameterization_count == 4
    assert diagnostics.max_epistemic_posterior_reparameterization_residual <= 1e-9
    assert diagnostics.max_ontic_posterior_reparameterization_residual <= 1e-9
    assert diagnostics.max_epistemic_ontic_posterior_residual <= 1e-9
    assert diagnostics.epistemic_hidden_selection_preserved
    assert diagnostics.ontic_updated_selector_free_all_parameterizations


def test_stage11d_wrong_event_jacobian_normalization_outcome_controls_are_rejected() -> None:
    controls = {item.control: item for item in stage11d_controls()}
    assert set(controls) == {
        "wrong_event_correspondence",
        "wrong_lapse_jacobian",
        "wrong_normalization",
        "wrong_outcome_correspondence",
    }
    assert all(item.rejected for item in controls.values())
    assert controls["wrong_event_correspondence"].typed_rejection
    assert "event_bridge" in controls["wrong_event_correspondence"].rejection_reasons
    assert controls["wrong_lapse_jacobian"].typed_rejection
    assert "lapse_jacobian" in controls["wrong_lapse_jacobian"].rejection_reasons
    assert controls["wrong_outcome_correspondence"].typed_rejection
    assert "outcome_correspondence" in controls["wrong_outcome_correspondence"].rejection_reasons
    assert not controls["wrong_normalization"].typed_rejection
    assert controls["wrong_normalization"].numerical_witness_residual > 1e-9


def test_stage11d_public_weighted_schema_does_not_expose_hidden_selector() -> None:
    names = set(Stage11DWeightedPublicView.__dataclass_fields__)
    assert not names.intersection(
        {
            "selected_continuation",
            "selected_continuation_id",
            "selector",
            "hidden_selector",
            "modal_type",
            "model_type",
            "belief_weights",
            "extension_weights",
        }
    )


def test_stage11d_diagnostics_close_criteria_32_38_only() -> None:
    diagnostics = _diagnostics()
    assert diagnostics.parameterization_count == 4
    assert diagnostics.continuation_count == 2
    assert diagnostics.measurement_view_count == 8
    assert diagnostics.probability_evaluation_count == 16
    assert diagnostics.max_per_continuation_reparameterization_probability_residual <= 1e-9
    assert diagnostics.max_stage10_reference_probability_residual <= 1e-9
    assert diagnostics.max_probability_sum_residual <= 1e-9
    assert diagnostics.minimum_probability >= -1e-9
    assert diagnostics.maximum_probability <= 1.0 + 1e-9
    assert diagnostics.max_completeness_residual <= 1e-9
    assert diagnostics.minimum_effect_eigenvalue >= -1e-9
    assert diagnostics.minimum_normalization_eigenvalue > 1e-9
    assert diagnostics.minimum_normalization_denominator > 1e-9
    assert diagnostics.anchor_raw_parameter_value_count > 1
    assert diagnostics.target_raw_parameter_value_count > 1
    assert diagnostics.control_count == 4
    assert diagnostics.rejected_control_count == 4
    assert diagnostics.wrong_normalization_matrix_residual > 1e-9
    assert diagnostics.wrong_normalization_probability_residual > 1e-9
    assert diagnostics.criteria_32_38_satisfied
