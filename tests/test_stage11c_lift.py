from dataclasses import replace

from t_search.stage9_modal import (
    canonical_stage9c_models,
    continuation_by_id,
    make_stage9_epistemic_model,
    matched_uniform_weights,
    privileged_stage9_modal_diagnostic,
)
from t_search.stage11_lift import (
    STAGE11C_CORRUPTION_CLASSIFICATION,
    canonical_stage11c_public_architectures,
    stage11c_corruption_controls,
    stage11c_diagnostics,
    stage11c_public_architecture,
    stage11c_selector_schema_audit,
    stage11c_validate_architecture,
)
from t_search.stage11_parametrized import (
    STAGE11A_ATOL,
    STAGE11A_IDENTITY,
    canonical_stage11a_positive_family,
)


def test_stage11c_o_p_r_v_are_preserved_across_positive_parameterizations() -> None:
    architectures = canonical_stage11c_public_architectures()
    assert len(architectures) == 4
    reference = next(
        item for item in architectures if item.Xi.parameterization_id == STAGE11A_IDENTITY
    )

    for item in architectures:
        assert item.O == reference.O
        assert item.P == reference.P
        assert item.R == reference.R
        assert item.V == reference.V
        assert item.P.current_anchor == 1
        assert item.P.qext_ids == ("h_L", "h_R")
        assert tuple(name for name, _ in item.P.continuation_classes) == ("h_L", "h_R")
        assert len(item.R.R_content) == 2
        assert len(item.R.R_direction) == 2
        assert len(item.R.R_access) == 2
        assert item.V.V_extension == ("h_L", "h_R")
        assert item.V.V_weights == (0.5, 0.5)


def test_stage11c_xi_carries_parameterization_event_lapse_and_correspondences() -> None:
    architectures = canonical_stage11c_public_architectures()
    ids = {item.Xi.parameterization_id for item in architectures}
    assert ids == {item.parameterization_id for item in canonical_stage11a_positive_family()}
    assert len({item.Xi.anchor_parameter_value for item in architectures}) > 1
    assert len({item.Xi.target_parameter_value for item in architectures}) > 1

    for item in architectures:
        assert item.Xi.anchor_lapse > 0.0
        assert item.Xi.target_lapse > 0.0
        assert item.Xi.event_correspondence == (
            ("e1", item.O.relational_events[0].physical_event_id),
            ("e2", item.O.relational_events[1].physical_event_id),
        )
        assert item.Xi.continuation_class_correspondence == (
            ("h_L", "h_L"),
            ("h_R", "h_R"),
        )
        assert item.Xi.outcome_correspondence == (
            ("future_signature_left", "future_signature_left"),
            ("future_signature_other", "future_signature_other"),
        )
        validation = stage11c_validate_architecture(item)
        assert validation.valid
        assert validation.continuation_correspondence_valid
        assert validation.outcome_correspondence_valid
        assert validation.corrupted_layers == ()


def test_stage11c_matched_epistemic_and_ontic_public_lifts_agree() -> None:
    epistemic, ontic = canonical_stage9c_models(selected_id="h_L")
    for trajectory in canonical_stage11a_positive_family():
        public_e = stage11c_public_architecture(epistemic, trajectory.parameterization_id)
        public_o = stage11c_public_architecture(ontic, trajectory.parameterization_id)
        assert public_e == public_o


def test_stage11c_hidden_hstar_swap_does_not_leak_into_public_architecture() -> None:
    epistemic_left, ontic = canonical_stage9c_models(selected_id="h_L")
    carrier = epistemic_left.carrier
    epistemic_right = make_stage9_epistemic_model(
        carrier,
        continuation_by_id(carrier, "h_R"),
        matched_uniform_weights(carrier),
    )
    assert privileged_stage9_modal_diagnostic(epistemic_left) != privileged_stage9_modal_diagnostic(
        epistemic_right
    )

    for trajectory in canonical_stage11a_positive_family():
        left = stage11c_public_architecture(
            epistemic_left, trajectory.parameterization_id
        )
        right = stage11c_public_architecture(
            epistemic_right, trajectory.parameterization_id
        )
        ontic_view = stage11c_public_architecture(ontic, trajectory.parameterization_id)
        assert left == right == ontic_view
        audit = stage11c_selector_schema_audit(left)
        assert audit.selector_free
        assert audit.forbidden_public_fields == ()


def test_stage11c_wrong_correspondence_is_detected_as_xi_failure() -> None:
    architecture = canonical_stage11c_public_architectures()[0]
    broken = replace(
        architecture,
        Xi=replace(
            architecture.Xi,
            continuation_class_correspondence=(("h_L", "h_R"), ("h_R", "h_L")),
        ),
    )
    validation = stage11c_validate_architecture(broken)
    assert not validation.valid
    assert not validation.Xi_valid
    assert not validation.continuation_correspondence_valid
    assert "Xi" in validation.corrupted_layers


def test_stage11c_parameter_dependent_oprv_corruptions_are_all_detected() -> None:
    controls = stage11c_corruption_controls()
    assert len(controls) == 4
    assert {item.layer for item in controls} == {"O", "P", "R", "V"}
    for item in controls:
        assert item.detected
        assert item.classification == STAGE11C_CORRUPTION_CLASSIFICATION
        assert item.layer in item.validator_corrupted_layers


def test_stage11c_diagnostics_close_criteria_24_31_only() -> None:
    diagnostics = stage11c_diagnostics()
    assert diagnostics.parameterization_count == 4
    assert diagnostics.matched_modal_public_projection_count == 8
    assert diagnostics.qext_size == 2
    assert diagnostics.directional_content_rows == 2
    assert diagnostics.directional_direction_rows == 2
    assert diagnostics.directional_access_rows == 2
    assert diagnostics.xi_view_count == 4
    assert diagnostics.continuation_correspondence_entries == 8
    assert diagnostics.outcome_correspondence_entries == 8
    assert diagnostics.max_current_density_residual <= STAGE11A_ATOL
    assert diagnostics.max_relational_O_residual <= STAGE11A_ATOL
    assert diagnostics.max_R_residual <= STAGE11A_ATOL
    assert diagnostics.max_V_weight_residual <= STAGE11A_ATOL
    assert diagnostics.all_positive_architectures_valid
    assert diagnostics.matched_epistemic_ontic_public_equal
    assert diagnostics.hidden_hstar_swap_public_invariant
    assert diagnostics.privileged_modal_roles_distinct
    assert diagnostics.public_schema_selector_free
    assert diagnostics.corruption_control_count == 4
    assert diagnostics.corruption_detected_count == 4
    assert diagnostics.criteria_24_31_satisfied
