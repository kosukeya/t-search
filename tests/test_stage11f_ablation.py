from t_search.stage11_ablation import (
    STAGE11F_EVENT_RECONSTRUCTIBLE,
    STAGE11F_MISSING_LAPSE_SEMANTICS,
    STAGE11F_NONINJECTIVE,
    STAGE11F_ORIENTATION_REVERSE,
    STAGE11F_WRONG_LAPSE_JACOBIAN,
    stage11f_diagnostics,
)
from t_search.stage11_lift import STAGE11C_CORRUPTION_CLASSIFICATION
from t_search.stage11_relational import STAGE11B_RAW_MATCH_INVALID


def test_stage11f_event_correspondence_is_reconstructible_but_typed_identity_is_lost() -> None:
    diagnostics = stage11f_diagnostics()
    event = diagnostics.classifications[0]
    assert event.ablation == "remove_parameter_event_correspondence"
    assert event.numerical_payload_status == "reconstructible"
    assert event.typed_identification_status == "lost"
    assert event.covariance_status == "not_established"
    assert event.classification == STAGE11F_EVENT_RECONSTRUCTIBLE
    assert event.residual <= 1e-10
    assert diagnostics.event_correspondence_numerically_reconstructible
    assert diagnostics.event_correspondence_typed_identity_lost


def test_stage11f_missing_lapse_semantics_is_distinct_from_wrong_lapse_value() -> None:
    diagnostics = stage11f_diagnostics()
    missing = diagnostics.classifications[1]
    wrong = diagnostics.classifications[2]

    assert missing.ablation == "remove_lapse_jacobian_semantics"
    assert missing.numerical_payload_status == "preserved"
    assert missing.typed_identification_status == "underdetermined"
    assert missing.covariance_status == "not_established"
    assert missing.classification == STAGE11F_MISSING_LAPSE_SEMANTICS
    assert diagnostics.missing_lapse_semantics_rejected
    assert diagnostics.missing_lapse_numeric_derivative_residual <= 1e-10

    assert wrong.ablation == "wrong_lapse_jacobian_value"
    assert wrong.numerical_payload_status == "corrupted"
    assert wrong.typed_identification_status == "lost"
    assert wrong.covariance_status == "refuted"
    assert wrong.classification == STAGE11F_WRONG_LAPSE_JACOBIAN
    assert diagnostics.wrong_lapse_jacobian_rejected
    assert diagnostics.wrong_lapse_value_residual > 1e-9
    assert diagnostics.wrong_lapse_relational_derivative_residual > 1e-9


def test_stage11f_orientation_and_noninjective_controls_have_explicit_witnesses() -> None:
    diagnostics = stage11f_diagnostics()
    controls = {item.control: item for item in diagnostics.false_positive_controls}

    reverse = controls["orientation_reversal"]
    assert reverse.rejected
    assert reverse.classification == STAGE11F_ORIENTATION_REVERSE
    assert reverse.witness_count == 12
    assert reverse.residual > 0.0
    assert diagnostics.orientation_reverse_decreasing_step_count == 12

    noninjective = controls["noninjective_square"]
    assert noninjective.rejected
    assert noninjective.classification == STAGE11F_NONINJECTIVE
    assert noninjective.witness_count == 6
    assert diagnostics.noninjective_collision_count == 6


def test_stage11f_raw_lambda_false_matching_remains_explicit() -> None:
    diagnostics = stage11f_diagnostics()
    raw = next(
        item for item in diagnostics.false_positive_controls
        if item.control == "raw_lambda_event_matching"
    )
    assert raw.rejected
    assert raw.classification == STAGE11B_RAW_MATCH_INVALID
    assert raw.witness_count == 6
    assert diagnostics.raw_lambda_matching_rejected
    assert diagnostics.raw_lambda_false_identity_count == 6


def test_stage11f_parameter_dependent_oprv_corruption_controls_are_consolidated() -> None:
    diagnostics = stage11f_diagnostics()
    controls = tuple(
        item
        for item in diagnostics.false_positive_controls
        if item.control.startswith("parameter_dependent_")
    )
    assert len(controls) == 4
    assert all(item.rejected for item in controls)
    assert all(item.classification == STAGE11C_CORRUPTION_CLASSIFICATION for item in controls)
    assert diagnostics.parameter_corruption_control_count == 4
    assert diagnostics.parameter_corruption_detected_count == 4


def test_stage11f_all_declared_false_positive_controls_are_rejected() -> None:
    diagnostics = stage11f_diagnostics()
    assert diagnostics.false_positive_control_count == 7
    assert diagnostics.rejected_false_positive_control_count == 7
    assert all(item.rejected for item in diagnostics.false_positive_controls)


def test_stage11f_interpretation_boundary_blocks_metaphysical_promotion() -> None:
    diagnostics = stage11f_diagnostics()
    assert diagnostics.metaphysical_promotion_avoided


def test_stage11f_closes_only_criteria_44_47() -> None:
    diagnostics = stage11f_diagnostics()
    assert diagnostics.criteria_44_47_satisfied
