from dataclasses import fields

import numpy as np

from t_search.stage7_history import CURRENT_EVENT, UPPER_EVENT
from t_search.stage9_modal import (
    FUTURE_SIGNATURE_LEFT,
    Stage9Evidence,
    Stage9QROperationalView,
    canonical_stage9_directional_carrier,
    canonical_stage9_future_signature_measurement,
    canonical_stage9c_models,
    compare_common_stage9_evidence,
    compare_stage9_qr_views,
    continuation_by_id,
    make_stage9_epistemic_model,
    make_stage9_ontic_model,
    matched_uniform_weights,
    ontic_selector_audit,
    privileged_stage9_modal_diagnostic,
    stage9_qr_operational_view,
    stage9c_modal_diagnostics,
    stage9c_summary,
)

ATOL = 1e-10


def test_stage9c_models_share_exact_directional_carrier_but_have_distinct_modal_structure():
    epistemic, ontic = canonical_stage9c_models(selected_id="h_L")
    assert epistemic.carrier is ontic.carrier
    assert epistemic.carrier.current_anchor == CURRENT_EVENT
    assert tuple(item.continuation_id for item in epistemic.carrier.continuations) == (
        "h_L",
        "h_R",
    )
    assert privileged_stage9_modal_diagnostic(epistemic) != privileged_stage9_modal_diagnostic(
        ontic
    )


def test_stage9c_ontic_model_has_no_selected_complete_continuation_datum():
    _, ontic = canonical_stage9c_models()
    audit = ontic_selector_audit(ontic)
    assert audit.no_selected_complete_continuation_datum is True
    assert audit.all_qext_members_represented is True
    assert audit.full_weight_support is True
    assert audit.forbidden_selector_fields == ()
    assert audit.direct_continuation_fields == ()
    assert audit.arbitrary_instance_dict_present is False


def test_stage9c_public_oqr_schema_excludes_hidden_selector_and_modal_type():
    names = {field.name for field in fields(Stage9QROperationalView)}
    for forbidden in (
        "selected_continuation",
        "selected_history",
        "selector",
        "model_type",
        "belief_weights",
        "extension_weights",
    ):
        assert forbidden not in names
    assert "directional_record" in names
    assert "next_probabilities" in names


def test_stage9c_matched_epistemic_and_ontic_views_are_equal_with_direction_present():
    epistemic, ontic = canonical_stage9c_models(selected_id="h_L")
    view_e = stage9_qr_operational_view(epistemic)
    view_o = stage9_qr_operational_view(ontic)
    comparison = compare_stage9_qr_views(view_e, view_o)

    assert comparison.equal is True
    assert view_e.directional_record is not None
    assert view_e.directional_record.orientation == "lower-index"
    assert np.isclose(view_e.directional_record.record_score, 1.0, atol=ATOL, rtol=0.0)
    assert np.isclose(
        view_e.directional_record.accessibility_score, 0.5, atol=ATOL, rtol=0.0
    )


def test_stage9c_hidden_selected_continuation_swap_does_not_change_oqr():
    epistemic_left, ontic = canonical_stage9c_models(selected_id="h_L")
    carrier = epistemic_left.carrier
    weights = matched_uniform_weights(carrier)
    epistemic_right = make_stage9_epistemic_model(
        carrier, continuation_by_id(carrier, "h_R"), weights
    )

    left_view = stage9_qr_operational_view(epistemic_left)
    right_view = stage9_qr_operational_view(epistemic_right)
    ontic_view = stage9_qr_operational_view(ontic)

    assert compare_stage9_qr_views(left_view, right_view).equal is True
    assert compare_stage9_qr_views(left_view, ontic_view).equal is True
    assert privileged_stage9_modal_diagnostic(epistemic_left).selected_continuation_id == "h_L"
    assert privileged_stage9_modal_diagnostic(epistemic_right).selected_continuation_id == "h_R"


def test_stage9c_future_signature_measurement_is_valid_and_branch_sensitive():
    carrier = canonical_stage9_directional_carrier()
    measurement = canonical_stage9_future_signature_measurement(carrier)
    assert measurement.completeness_residual <= ATOL
    assert measurement.minimum_effect_eigenvalue >= -ATOL
    assert measurement.branch_overlap_squared < 1.0 - ATOL


def test_stage9c_weight_mismatch_changes_future_prediction_not_current_direction():
    epistemic, _ = canonical_stage9c_models(selected_id="h_L")
    carrier = epistemic.carrier
    mismatch = make_stage9_ontic_model(carrier, (0.75, 0.25))

    baseline = stage9_qr_operational_view(epistemic)
    changed = stage9_qr_operational_view(mismatch)
    comparison = compare_stage9_qr_views(baseline, changed)

    assert comparison.current_anchor_equal is True
    assert comparison.density_equal is True
    assert comparison.record_joint_equal is True
    assert comparison.record_information_equal is True
    assert comparison.directional_record_equal is True
    assert comparison.next_outcomes_equal is True
    assert comparison.next_probabilities_equal is False
    assert comparison.equal is False


def test_stage9c_explicit_common_evidence_updates_both_models_without_ontic_selector():
    epistemic, ontic = canonical_stage9c_models(selected_id="h_L")
    result = compare_common_stage9_evidence(
        epistemic, ontic, Stage9Evidence(FUTURE_SIGNATURE_LEFT)
    )

    assert result.before_comparison.equal is True
    assert result.after_comparison.equal is True
    assert result.epistemic_selected_before == "h_L"
    assert result.epistemic_selected_after == "h_L"
    assert result.epistemic_selected_preserved is True
    assert np.allclose(
        np.asarray(result.epistemic_posterior_weights),
        np.asarray(result.ontic_posterior_weights),
        atol=ATOL,
        rtol=0.0,
    )
    assert result.ontic_no_selected_complete_continuation_datum is True


def test_stage9c_post_update_public_view_advances_and_no_longer_claims_current_e1_direction():
    epistemic, ontic = canonical_stage9c_models(selected_id="h_L")
    result = compare_common_stage9_evidence(
        epistemic, ontic, Stage9Evidence(FUTURE_SIGNATURE_LEFT)
    )
    assert result.after_comparison.current_anchor_equal is True
    assert stage9c_modal_diagnostics().update_anchor_advanced is True
    assert UPPER_EVENT > CURRENT_EVENT


def test_stage9c_diagnostics_close_matched_undertermination_and_weight_control():
    diagnostics = stage9c_modal_diagnostics()
    assert diagnostics.qext_size == 2
    assert diagnostics.shared_carrier_identity is True
    assert diagnostics.matched_operational_equal is True
    assert diagnostics.selected_swap_operational_equal is True
    assert diagnostics.privileged_structures_distinct is True
    assert diagnostics.hidden_selected_absent_from_operational_schema is True
    assert diagnostics.directional_interface_present is True
    assert diagnostics.directional_interface_shared_across_continuations is True
    assert np.isclose(diagnostics.directional_record_score, 1.0, atol=ATOL, rtol=0.0)
    assert np.isclose(
        diagnostics.directional_accessibility_score, 0.5, atol=ATOL, rtol=0.0
    )
    assert diagnostics.weight_mismatch_changes_prediction is True
    assert diagnostics.weight_mismatch_preserves_current_directional_data is True
    assert diagnostics.ontic_no_selected_complete_continuation_datum is True
    assert diagnostics.ontic_full_weight_support is True
    assert diagnostics.update_before_equal is True
    assert diagnostics.update_after_equal is True
    assert diagnostics.epistemic_selected_preserved is True
    assert diagnostics.posterior_weights_match is True
    assert diagnostics.updated_ontic_no_selected_complete_continuation_datum is True


def test_stage9c_summary_preserves_modal_and_becoming_guards():
    summary = stage9c_summary()
    assert summary["stage"] == "9C"
    assert summary["exit_criteria_satisfied"] == tuple(range(24, 31))
    assert "O_QR=" in summary["interface"]
    assert "operational directional equality != modal/ontological identity" in summary[
        "guards"
    ]
    assert "directional record arrow != ontological future openness" in summary["guards"]
    assert "directional record arrow != ontological becoming" in summary["guards"]
    assert "explicit evidence update != ontological becoming" in summary["guards"]
    assert "control of V_weights != determination of V_semantics" in summary["guards"]
