from dataclasses import FrozenInstanceError, fields

import pytest

from t_search.stage8_continuations import (
    canonical_continuation_left,
    continuation_equivalent,
)
from t_search.stage8_modal import (
    EpistemicQuantumPotentiality,
    OnticExtensionQuantumPotentiality,
    canonical_quantum_continuation_carrier,
    canonical_stage8b_models,
    continuation_by_id,
    continuation_ids,
    epistemic_quantum_potentiality,
    make_epistemic_quantum_model,
    make_ontic_quantum_extension_model,
    matched_uniform_weights,
    ontic_extension_quantum_potentiality,
    ontic_selector_audit,
    pre_discriminating_quantum_view,
    selected_quantum_continuation,
    stage8b_modal_diagnostics,
    stage8b_summary,
)

ATOL = 1e-10


def test_stage8b_epistemic_model_contains_one_selected_continuation():
    epistemic, _ = canonical_stage8b_models(selected_id="h_L")
    selected = selected_quantum_continuation(epistemic)
    assert selected.continuation_id == "h_L"
    assert any(
        continuation_equivalent(selected, item)
        for item in epistemic.carrier.continuations
    )


def test_stage8b_epistemic_and_ontic_potentiality_are_type_distinct():
    epistemic, ontic = canonical_stage8b_models()
    epot = epistemic_quantum_potentiality(epistemic)
    opot = ontic_extension_quantum_potentiality(ontic)

    assert isinstance(epot, EpistemicQuantumPotentiality)
    assert isinstance(opot, OnticExtensionQuantumPotentiality)
    assert type(epot) is not type(opot)
    assert tuple(item.continuation_id for item in epot.continuations) == ("h_L", "h_R")
    assert tuple(item.continuation_id for item in opot.continuations) == ("h_L", "h_R")


def test_stage8b_both_models_use_the_exact_same_physical_carrier_object():
    epistemic, ontic = canonical_stage8b_models()
    assert epistemic.carrier is ontic.carrier
    assert continuation_ids(epistemic.carrier) == ("h_L", "h_R")


def test_stage8b_uniform_matched_weights_do_not_take_selected_continuation():
    carrier = canonical_quantum_continuation_carrier()
    weights = matched_uniform_weights(carrier)
    assert weights == (0.5, 0.5)

    left = make_epistemic_quantum_model(
        carrier,
        continuation_by_id(carrier, "h_L"),
        weights,
    )
    right = make_epistemic_quantum_model(
        carrier,
        continuation_by_id(carrier, "h_R"),
        weights,
    )
    ontic = make_ontic_quantum_extension_model(carrier, weights)

    assert left.belief_weights == right.belief_weights == ontic.extension_weights


def test_stage8b_swapping_hidden_selected_continuation_changes_privileged_diagnostic_only():
    carrier = canonical_quantum_continuation_carrier()
    weights = matched_uniform_weights(carrier)
    left = make_epistemic_quantum_model(
        carrier, continuation_by_id(carrier, "h_L"), weights
    )
    right = make_epistemic_quantum_model(
        carrier, continuation_by_id(carrier, "h_R"), weights
    )

    assert selected_quantum_continuation(left).continuation_id == "h_L"
    assert selected_quantum_continuation(right).continuation_id == "h_R"
    assert pre_discriminating_quantum_view(left) == pre_discriminating_quantum_view(right)


def test_stage8b_pre_discriminating_view_schema_does_not_expose_selector_or_model_type():
    names = {field.name for field in fields(type(pre_discriminating_quantum_view(canonical_stage8b_models()[0])))}
    assert "selected_continuation" not in names
    assert "selected_history" not in names
    assert "model_type" not in names
    assert "selector" not in names


def test_stage8b_matched_typed_models_have_equal_minimal_pre_view_without_claiming_full_oq():
    epistemic, ontic = canonical_stage8b_models()
    assert pre_discriminating_quantum_view(epistemic) == pre_discriminating_quantum_view(ontic)
    summary = stage8b_summary()
    assert "Stage 8B pre-discriminating view != full Stage 8C O_Q interface" in summary["guards"]


def test_stage8b_ontic_model_schema_has_no_selected_or_selector_like_stored_datum():
    _, ontic = canonical_stage8b_models()
    audit = ontic_selector_audit(ontic)

    assert audit.forbidden_selector_fields == ()
    assert audit.direct_continuation_fields == ()
    assert audit.arbitrary_instance_dict_present is False
    assert audit.all_qext_members_represented is True
    assert audit.full_weight_support is True
    assert audit.no_selected_complete_continuation_datum is True
    assert not hasattr(ontic, "selected_continuation")
    assert not hasattr(ontic, "selected_history")
    assert not hasattr(ontic, "selector")
    assert not hasattr(ontic, "seed")


def test_stage8b_ontic_slots_and_frozen_schema_reject_injected_selector_state():
    _, ontic = canonical_stage8b_models()
    with pytest.raises((FrozenInstanceError, AttributeError)):
        setattr(ontic, "selected_continuation", canonical_continuation_left())


def test_stage8b_epistemic_selected_continuation_must_belong_to_qext():
    carrier = canonical_quantum_continuation_carrier()
    weights = matched_uniform_weights(carrier)
    invalid = canonical_continuation_left()
    invalid = type(invalid)(
        continuation_id="invalid-current",
        future_action=invalid.future_action,
        current_action="identity",
    )
    with pytest.raises(ValueError, match="selected continuation must belong"):
        make_epistemic_quantum_model(carrier, invalid, weights)


def test_stage8b_selected_continuation_requires_positive_epistemic_support():
    carrier = canonical_quantum_continuation_carrier()
    left = continuation_by_id(carrier, "h_L")
    with pytest.raises(ValueError, match="positive epistemic support"):
        make_epistemic_quantum_model(carrier, left, (0.0, 1.0))


def test_stage8b_weight_validation_rejects_incomplete_negative_or_unnormalized_distributions():
    carrier = canonical_quantum_continuation_carrier()
    left = continuation_by_id(carrier, "h_L")

    with pytest.raises(ValueError, match="one weight per QExt"):
        make_epistemic_quantum_model(carrier, left, (1.0,))
    with pytest.raises(ValueError, match="finite and non-negative"):
        make_ontic_quantum_extension_model(carrier, (-0.1, 1.1))
    with pytest.raises(ValueError, match="sum to 1"):
        make_ontic_quantum_extension_model(carrier, (0.4, 0.4))


def test_stage8b_diagnostics_close_only_typed_modal_exit_criteria_17_to_21():
    diagnostics = stage8b_modal_diagnostics()
    assert diagnostics.qext_size == 2
    assert diagnostics.epistemic_selected_left == "h_L"
    assert diagnostics.epistemic_selected_right == "h_R"
    assert diagnostics.privileged_selected_swap_detected is True
    assert diagnostics.potentiality_types_distinct is True
    assert diagnostics.potentiality_members_match is True
    assert diagnostics.shared_carrier_identity is True
    assert diagnostics.matched_weight_residual <= ATOL
    assert diagnostics.selected_swap_weight_residual <= ATOL
    assert diagnostics.matched_pre_view_equal is True
    assert diagnostics.selected_swap_pre_view_equal is True
    assert diagnostics.selected_hidden_from_pre_view_schema is True
    assert diagnostics.ontic_no_selected_complete_continuation_datum is True
    assert diagnostics.ontic_full_weight_support is True
    assert abs(diagnostics.current_record_information - 1.0) <= ATOL
    assert diagnostics.current_state_norm > 0.0

    summary = stage8b_summary()
    assert summary["exit_criteria_satisfied"] == (17, 18, 19, 20, 21)
    assert summary["next"] == "Stage 8C — operational underdetermination and explicit update"
    assert "no selected continuation field != proof of ontic openness in nature" in summary["guards"]
