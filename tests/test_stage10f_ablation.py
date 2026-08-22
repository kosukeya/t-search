from t_search.stage10_ablation import (
    stage10f_ablation_diagnostics,
    stage10f_summary,
)


def test_stage10f_correspondence_removals_preserve_numbers_but_lose_typed_identity() -> None:
    diagnostics = stage10f_ablation_diagnostics()
    rows = diagnostics.classifications[:3]
    assert diagnostics.correspondence_ablations_classified
    assert tuple(item.ablation for item in rows) == (
        "remove_event_correspondence",
        "remove_class_correspondence",
        "remove_outcome_correspondence",
    )
    for item in rows:
        assert item.numerical_payload_status == "preserved"
        assert item.typed_identification_status == "lost"
        assert item.probability_covariance_status == "not_established"


def test_stage10f_normalization_missing_vs_corrupted_are_distinguished() -> None:
    diagnostics = stage10f_ablation_diagnostics()
    table = {item.ablation: item for item in diagnostics.classifications}
    missing = table["remove_normalization_semantics"]
    wrong = table["fresh_identity_normalization"]
    assert diagnostics.normalization_ablations_classified
    assert missing.numerical_payload_status == "reconstructible"
    assert missing.typed_identification_status == "underdetermined"
    assert missing.probability_covariance_status == "not_established"
    assert wrong.probability_covariance_status == "refuted"
    assert wrong.residual > 1e-9
    assert diagnostics.fresh_identity_rejected


def test_stage10f_required_false_positive_controls_have_witnesses() -> None:
    diagnostics = stage10f_ablation_diagnostics()
    assert diagnostics.bare_effect_rejected
    assert diagnostics.bare_effect_residual > 1e-9
    assert diagnostics.wrong_continuation_rejected
    assert diagnostics.wrong_continuation_form_residual > 1e-9
    assert diagnostics.wrong_outcome_rejected
    assert diagnostics.wrong_outcome_probability_residual > 1e-9
    assert diagnostics.wrong_event_rejected
    assert diagnostics.weight_misalignment_rejected
    assert diagnostics.weight_misalignment_prediction_residual > 1e-9
    assert diagnostics.fresh_identity_rejected
    assert diagnostics.fresh_identity_probe_residual > 1e-9
    assert diagnostics.all_required_false_positive_controls_rejected


def test_stage10f_does_not_promote_functional_loss_to_metaphysics() -> None:
    diagnostics = stage10f_ablation_diagnostics()
    summary = stage10f_summary()
    assert diagnostics.metaphysical_promotion_avoided
    assert summary["criteria_44_47_satisfied"] is True
    guards = set(summary["guards"])
    assert "numerical reconstructibility != typed operational identification" in guards
    assert "missing typing != metaphysical absence" in guards
    assert "lost != metaphysically irreducible" in guards
    assert "not_established != false" in guards
    assert "finite-model ablation != fundamental ontology" in guards
