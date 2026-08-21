from dataclasses import fields

import numpy as np
import pytest

from t_search.stage7_history import UPPER_EVENT
from t_search.stage8_modal import (
    canonical_stage8b_models,
    continuation_by_id,
    make_epistemic_quantum_model,
    make_ontic_quantum_extension_model,
    matched_uniform_weights,
)
from t_search.stage8_operational import (
    FUTURE_SIGNATURE_0,
    FUTURE_SIGNATURE_1,
    FUTURE_SIGNATURE_REMAINDER,
    QuantumEvidence,
    QuantumOperationalView,
    canonical_future_signature_measurement,
    compare_common_quantum_evidence,
    compare_quantum_operational_views,
    continuation_future_signature_probabilities,
    privileged_quantum_modal_diagnostic,
    quantum_operational_view,
    stage8c_operational_diagnostics,
    stage8c_summary,
    update_epistemic_quantum_model,
    update_ontic_quantum_model,
    updated_ontic_remaining_qext,
    updated_ontic_selector_audit,
)

ATOL = 1e-10


def test_stage8c_future_signature_measurement_is_complete_positive_and_projective():
    epistemic, _ = canonical_stage8b_models()
    measurement = canonical_future_signature_measurement(epistemic.carrier)

    assert measurement.outcome_names == (
        FUTURE_SIGNATURE_0,
        FUTURE_SIGNATURE_1,
        FUTURE_SIGNATURE_REMAINDER,
    )
    assert measurement.completeness_residual <= ATOL
    assert measurement.orthogonality_residual <= ATOL
    assert measurement.minimum_effect_eigenvalue >= -ATOL

    identity = np.eye(measurement.effects[0].shape[0], dtype=np.complex128)
    assert np.allclose(sum(measurement.effects), identity, atol=ATOL, rtol=0.0)
    for effect in measurement.effects:
        assert np.allclose(effect, effect.conj().T, atol=ATOL, rtol=0.0)


def test_stage8c_canonical_continuations_have_distinct_deterministic_born_signatures():
    epistemic, _ = canonical_stage8b_models()
    carrier = epistemic.carrier
    left = continuation_by_id(carrier, "h_L")
    right = continuation_by_id(carrier, "h_R")

    left_probs = dict(continuation_future_signature_probabilities(carrier, left))
    right_probs = dict(continuation_future_signature_probabilities(carrier, right))

    assert np.isclose(left_probs[FUTURE_SIGNATURE_0], 1.0, atol=ATOL, rtol=0.0)
    assert np.isclose(left_probs[FUTURE_SIGNATURE_1], 0.0, atol=ATOL, rtol=0.0)
    assert np.isclose(left_probs[FUTURE_SIGNATURE_REMAINDER], 0.0, atol=ATOL, rtol=0.0)
    assert np.isclose(right_probs[FUTURE_SIGNATURE_0], 0.0, atol=ATOL, rtol=0.0)
    assert np.isclose(right_probs[FUTURE_SIGNATURE_1], 1.0, atol=ATOL, rtol=0.0)
    assert np.isclose(right_probs[FUTURE_SIGNATURE_REMAINDER], 0.0, atol=ATOL, rtol=0.0)


def test_stage8c_operational_schema_excludes_modal_type_selector_and_internal_weights():
    names = {field.name for field in fields(QuantumOperationalView)}
    for forbidden in (
        "selected_continuation",
        "selected_history",
        "selector",
        "model_type",
        "belief_weights",
        "extension_weights",
        "potentiality",
    ):
        assert forbidden not in names


def test_stage8c_matched_models_are_operationally_equal_under_full_oq_interface():
    epistemic, ontic = canonical_stage8b_models(selected_id="h_L")
    e_view = quantum_operational_view(epistemic)
    o_view = quantum_operational_view(ontic)
    comparison = compare_quantum_operational_views(e_view, o_view)

    assert comparison.equal is True
    assert comparison.current_anchor_equal is True
    assert comparison.density_equal is True
    assert comparison.record_joint_equal is True
    assert comparison.record_information_equal is True
    assert comparison.next_outcomes_equal is True
    assert comparison.next_probabilities_equal is True
    assert e_view.next_outcomes == (FUTURE_SIGNATURE_0, FUTURE_SIGNATURE_1)
    assert np.allclose(
        [probability for _, probability in e_view.next_probabilities],
        [0.5, 0.5],
        atol=ATOL,
        rtol=0.0,
    )
    assert np.isclose(e_view.current_record_information, 1.0, atol=ATOL, rtol=0.0)


def test_stage8c_privileged_diagnostics_distinguish_modal_structures_while_oq_matches():
    epistemic, ontic = canonical_stage8b_models(selected_id="h_L")
    e_privileged = privileged_quantum_modal_diagnostic(epistemic)
    o_privileged = privileged_quantum_modal_diagnostic(ontic)

    assert e_privileged != o_privileged
    assert e_privileged.selected_complete_continuation_present is True
    assert e_privileged.selected_continuation_id == "h_L"
    assert o_privileged.selected_complete_continuation_present is False
    assert o_privileged.selected_continuation_id is None
    assert compare_quantum_operational_views(
        quantum_operational_view(epistemic),
        quantum_operational_view(ontic),
    ).equal


def test_stage8c_swapping_hidden_hstar_alone_does_not_change_full_oq():
    epistemic, _ = canonical_stage8b_models(selected_id="h_L")
    carrier = epistemic.carrier
    weights = matched_uniform_weights(carrier)
    swapped = make_epistemic_quantum_model(
        carrier,
        continuation_by_id(carrier, "h_R"),
        weights,
    )

    assert privileged_quantum_modal_diagnostic(epistemic) != privileged_quantum_modal_diagnostic(swapped)
    assert compare_quantum_operational_views(
        quantum_operational_view(epistemic),
        quantum_operational_view(swapped),
    ).equal is True


def test_stage8c_weight_mismatch_changes_prediction_but_not_current_actuality():
    epistemic, _ = canonical_stage8b_models(selected_id="h_L")
    mismatch = make_ontic_quantum_extension_model(
        epistemic.carrier,
        (0.75, 0.25),
    )
    baseline = quantum_operational_view(epistemic)
    changed = quantum_operational_view(mismatch)
    comparison = compare_quantum_operational_views(baseline, changed)

    assert comparison.current_anchor_equal is True
    assert comparison.density_equal is True
    assert comparison.record_joint_equal is True
    assert comparison.record_information_equal is True
    assert comparison.next_outcomes_equal is True
    assert comparison.next_probabilities_equal is False
    assert comparison.equal is False
    assert np.allclose(
        [probability for _, probability in changed.next_probabilities],
        [0.75, 0.25],
        atol=ATOL,
        rtol=0.0,
    )


def test_stage8c_epistemic_update_preserves_hstar_and_conditions_beliefs():
    epistemic, _ = canonical_stage8b_models(selected_id="h_L")
    updated = update_epistemic_quantum_model(
        epistemic,
        QuantumEvidence(FUTURE_SIGNATURE_0),
    )

    assert updated.current_anchor == UPPER_EVENT
    assert updated.observed_outcome == FUTURE_SIGNATURE_0
    assert updated.selected_continuation.continuation_id == "h_L"
    assert np.allclose(updated.posterior_weights, (1.0, 0.0), atol=ATOL, rtol=0.0)


def test_stage8c_epistemic_update_rejects_evidence_contradicting_hidden_selected_continuation():
    epistemic, _ = canonical_stage8b_models(selected_id="h_L")
    with pytest.raises(ValueError, match="contradicts the hidden selected continuation"):
        update_epistemic_quantum_model(
            epistemic,
            QuantumEvidence(FUTURE_SIGNATURE_1),
        )


def test_stage8c_ontic_update_prunes_weights_without_creating_selector():
    _, ontic = canonical_stage8b_models(selected_id="h_L")
    updated = update_ontic_quantum_model(
        ontic,
        QuantumEvidence(FUTURE_SIGNATURE_0),
    )
    audit = updated_ontic_selector_audit(updated)

    assert updated.current_anchor == UPPER_EVENT
    assert updated.observed_outcome == FUTURE_SIGNATURE_0
    assert np.allclose(updated.posterior_weights, (1.0, 0.0), atol=ATOL, rtol=0.0)
    assert audit.forbidden_selector_fields == ()
    assert audit.direct_continuation_fields == ()
    assert audit.arbitrary_instance_dict_present is False
    assert audit.no_selected_complete_continuation_datum is True
    assert not hasattr(updated, "selected_continuation")
    assert not hasattr(updated, "selector")
    assert not hasattr(updated, "seed")
    assert updated_ontic_remaining_qext(updated) == ()


def test_stage8c_update_api_requires_explicit_valid_evidence_outcome():
    epistemic, ontic = canonical_stage8b_models(selected_id="h_L")
    invalid = QuantumEvidence(FUTURE_SIGNATURE_REMAINDER)
    with pytest.raises(ValueError, match="not in the declared current Next_Q set"):
        update_epistemic_quantum_model(epistemic, invalid)
    with pytest.raises(ValueError, match="not in the declared current Next_Q set"):
        update_ontic_quantum_model(ontic, invalid)


def test_stage8c_common_explicit_evidence_advances_actuality_consistently():
    epistemic, ontic = canonical_stage8b_models(selected_id="h_L")
    comparison = compare_common_quantum_evidence(
        epistemic,
        ontic,
        QuantumEvidence(FUTURE_SIGNATURE_0),
    )

    assert comparison.before_comparison.equal is True
    assert comparison.after_comparison.equal is True
    assert comparison.epistemic_before.current_anchor < comparison.epistemic_after.current_anchor
    assert comparison.epistemic_after.current_anchor == UPPER_EVENT
    assert comparison.ontic_after.current_anchor == UPPER_EVENT
    assert comparison.epistemic_after.observed_outcome == FUTURE_SIGNATURE_0
    assert comparison.ontic_after.observed_outcome == FUTURE_SIGNATURE_0
    assert comparison.epistemic_after.next_outcomes == ()
    assert comparison.ontic_after.next_outcomes == ()
    assert comparison.epistemic_after.next_probabilities == ()
    assert comparison.ontic_after.next_probabilities == ()
    assert comparison.epistemic_selected_preserved is True
    assert np.allclose(comparison.epistemic_posterior_weights, (1.0, 0.0), atol=ATOL, rtol=0.0)
    assert np.allclose(comparison.ontic_posterior_weights, (1.0, 0.0), atol=ATOL, rtol=0.0)
    assert comparison.ontic_remaining_qext_size == 0
    assert comparison.ontic_no_selected_complete_continuation_datum is True


def test_stage8c_same_density_and_born_data_do_not_determine_modal_semantics():
    epistemic, ontic = canonical_stage8b_models(selected_id="h_L")
    comparison = compare_quantum_operational_views(
        quantum_operational_view(epistemic),
        quantum_operational_view(ontic),
    )
    assert comparison.density_equal is True
    assert comparison.next_probabilities_equal is True
    assert privileged_quantum_modal_diagnostic(epistemic) != privileged_quantum_modal_diagnostic(ontic)

    diagnostics = stage8c_operational_diagnostics()
    assert diagnostics.same_density_with_distinct_modal_structure is True
    assert diagnostics.same_born_prediction_with_distinct_modal_structure is True
    assert diagnostics.state_and_born_data_do_not_select_modal_semantics is True


def test_stage8c_superposed_current_state_occurs_in_both_modal_types_and_is_not_discriminating():
    diagnostics = stage8c_operational_diagnostics()
    assert diagnostics.current_state_has_multiple_coherent_amplitudes is True
    assert diagnostics.matched_operational_equal is True
    assert diagnostics.privileged_structures_distinct is True
    assert diagnostics.superposition_does_not_select_modal_semantics is True


def test_stage8c_diagnostics_close_only_operational_update_criteria_22_to_29():
    diagnostics = stage8c_operational_diagnostics()
    assert diagnostics.qext_size == 2
    assert diagnostics.matched_operational_equal is True
    assert diagnostics.selected_swap_operational_equal is True
    assert diagnostics.privileged_structures_distinct is True
    assert diagnostics.hidden_selected_absent_from_operational_schema is True
    assert diagnostics.weight_mismatch_changes_prediction is True
    assert diagnostics.update_before_equal is True
    assert diagnostics.update_after_equal is True
    assert diagnostics.update_anchor_advanced is True
    assert diagnostics.update_outcome_equal is True
    assert diagnostics.epistemic_selected_preserved is True
    assert np.allclose(diagnostics.epistemic_posterior_weights, (1.0, 0.0), atol=ATOL, rtol=0.0)
    assert np.allclose(diagnostics.ontic_posterior_weights, (1.0, 0.0), atol=ATOL, rtol=0.0)
    assert diagnostics.ontic_posterior_pruned is True
    assert diagnostics.ontic_remaining_qext_size == 0
    assert diagnostics.ontic_no_selected_complete_continuation_datum is True
    assert diagnostics.superposition_does_not_select_modal_semantics is True
    assert diagnostics.state_and_born_data_do_not_select_modal_semantics is True
    assert diagnostics.measurement_completeness_residual <= ATOL
    assert diagnostics.measurement_orthogonality_residual <= ATOL
    assert diagnostics.minimum_effect_eigenvalue >= -ATOL

    summary = stage8c_summary()
    assert summary["exit_criteria_satisfied"] == tuple(range(22, 30))
    assert summary["next"] == "Stage 8D — genuine clock-change modal transport"
    assert "operational quantum equality != modal/ontological identity" in summary["guards"]
    assert "explicit evidence update != ontological becoming" in summary["guards"]
