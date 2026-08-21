import json

import pytest

from t_search.stage6_record_modality import (
    CANONICAL_SOURCE_PERSPECTIVE,
    CANONICAL_TARGET_PERSPECTIVE,
    canonical_modal_description_map,
    canonical_modal_transport,
    canonical_preserving_record_transport,
    canonical_reversing_record_transport,
    extension_transport_diagnostics,
    misdeclared_record_correspondence,
    mismatched_modal_description_map,
    modal_mismatch_control,
    record_accessibility_controls,
    record_orientation_mismatch_control,
    preserving_record_correspondence,
    renamed_modal_substrate,
    reversing_record_correspondence,
    stage6e_rows,
)
from t_search.stage2 import canonical_stage2_substrate
from t_search.stage2_epistemic import canonical_epistemic_model, project_epistemic_view
from t_search.stage2_ontic import canonical_ontic_model, project_ontic_view


TOL = 1e-12


def test_preserving_record_correspondence_is_explicit_and_identity_on_record_events() -> None:
    chi = preserving_record_correspondence()
    assert chi.source == CANONICAL_SOURCE_PERSPECTIVE
    assert chi.target == CANONICAL_TARGET_PERSPECTIVE
    assert chi.orientation == "preserving"
    assert dict(chi.mapping) == {"e0": "e0", "e1": "e1", "e2": "e2"}


def test_reversing_record_correspondence_is_explicit_and_reverses_endpoints() -> None:
    chi = reversing_record_correspondence()
    assert chi.orientation == "reversing"
    assert dict(chi.mapping) == {"e0": "e2", "e1": "e1", "e2": "e0"}


def test_orientation_preserving_record_transport_preserves_profiles_and_score() -> None:
    diagnostics = canonical_preserving_record_transport()
    assert diagnostics.globally_compatible
    assert diagnostics.source_orientation == "lower-index"
    assert diagnostics.target_orientation == "lower-index"
    assert diagnostics.max_information_profile_residual <= TOL
    assert diagnostics.max_accessibility_profile_residual <= TOL
    assert diagnostics.record_score_transport_residual <= TOL
    assert diagnostics.accessibility_score_transport_residual <= TOL


def test_orientation_reversing_record_transport_reverses_record_orientation_covariantly() -> None:
    diagnostics = canonical_reversing_record_transport()
    assert diagnostics.globally_compatible
    assert diagnostics.source_orientation == "lower-index"
    assert diagnostics.target_orientation == "upper-index"
    assert diagnostics.max_information_profile_residual <= TOL
    assert diagnostics.max_accessibility_profile_residual <= TOL
    assert diagnostics.record_score_transport_residual <= TOL
    assert diagnostics.accessibility_score_transport_residual <= TOL
    assert diagnostics.source_local.record_score == pytest.approx(
        -diagnostics.target_local.record_score, abs=TOL
    )


def test_misdeclared_record_orientation_is_detected_without_changing_event_bijection() -> None:
    chi = misdeclared_record_correspondence()
    assert len(set(dict(chi.mapping).values())) == 3
    diagnostics = record_orientation_mismatch_control()
    assert not diagnostics.globally_compatible
    assert diagnostics.max_information_profile_residual <= TOL
    assert diagnostics.record_score_transport_residual > TOL
    assert diagnostics.accessibility_score_transport_residual > TOL


def test_hidden_target_record_is_locally_inaccessible_while_global_transport_remains_valid() -> None:
    diagnostics = record_accessibility_controls()["target-hidden"]
    assert diagnostics.globally_compatible
    assert diagnostics.source_local.record_exposed
    assert not diagnostics.target_local.record_exposed
    assert diagnostics.target_local.record_score is None
    assert diagnostics.target_local.accessibility_score is None


def test_maximally_noisy_target_readout_erases_local_record_contrast_not_global_record_structure() -> None:
    diagnostics = record_accessibility_controls()["target-maximally-noisy"]
    assert diagnostics.globally_compatible
    assert diagnostics.target_local.record_exposed
    assert diagnostics.target_local.record_error_probability == pytest.approx(0.5)
    assert diagnostics.target_local.record_score == pytest.approx(0.0, abs=TOL)
    assert diagnostics.target_local.accessibility_score == pytest.approx(0.0, abs=TOL)
    assert diagnostics.source_local.record_score is not None
    assert abs(diagnostics.source_local.record_score) > TOL


def test_exact_access_control_retains_local_record_transport() -> None:
    diagnostics = record_accessibility_controls()["exact"]
    assert diagnostics.globally_compatible
    assert diagnostics.source_local.record_exposed
    assert diagnostics.target_local.record_exposed
    assert diagnostics.source_local.record_score == pytest.approx(
        diagnostics.target_local.record_score, abs=TOL
    )


def test_canonical_modal_description_map_pushes_substrate_to_isomorphic_renamed_tree() -> None:
    source = canonical_stage2_substrate()
    mapping = canonical_modal_description_map()
    target = renamed_modal_substrate(source, mapping)
    assert target.root == "q_p"
    assert set(target.histories) == {
        ("q_p", "q_n", "q_l1", "q_l2"),
        ("q_p", "q_n", "q_r1"),
    }


def test_epistemic_and_ontic_extension_sets_transport_by_declared_bijection() -> None:
    diagnostics = canonical_modal_transport()
    assert diagnostics.epistemic_extensions.relation == "bijection"
    assert diagnostics.ontic_extensions.relation == "bijection"
    assert diagnostics.epistemic_extensions.relation_holds
    assert diagnostics.ontic_extensions.relation_holds
    assert diagnostics.epistemic_extensions.source_extension_count == 2
    assert diagnostics.ontic_extensions.source_extension_count == 2


def test_operational_underdetermination_survives_modal_transport() -> None:
    diagnostics = canonical_modal_transport()
    assert diagnostics.source_operational_equal
    assert diagnostics.target_operational_equal
    assert diagnostics.epistemic_operational_transport_equal
    assert diagnostics.ontic_operational_transport_equal
    assert diagnostics.underdetermination_preserved


def test_modal_transport_keeps_potentiality_semantic_types_distinct() -> None:
    diagnostics = canonical_modal_transport()
    assert diagnostics.source_potentiality_types_distinct
    assert diagnostics.target_potentiality_types_distinct
    assert diagnostics.epistemic_selected_history_present
    assert not diagnostics.ontic_selected_future_field_present


def test_bijective_event_renaming_need_not_preserve_extension_structure() -> None:
    control = modal_mismatch_control()
    assert control.event_map_is_bijective
    assert not control.epistemic_relation_holds
    assert not control.ontic_relation_holds
    assert control.epistemic_invalid_mapped_extension_count > 0
    assert control.ontic_invalid_mapped_extension_count > 0


def test_extension_transport_diagnostic_changes_when_map_changes() -> None:
    source_ep = project_epistemic_view(canonical_epistemic_model(), ("p", "n"))
    source_on = project_ontic_view(canonical_ontic_model())
    canonical_map = canonical_modal_description_map()
    target = renamed_modal_substrate(canonical_stage2_substrate(), canonical_map)
    target_histories = target.histories

    good = extension_transport_diagnostics(
        source_ep.potentiality.histories, target_histories, canonical_map
    )
    bad = extension_transport_diagnostics(
        source_on.potentiality.histories,
        target_histories,
        mismatched_modal_description_map(),
    )
    assert good.relation_holds
    assert not bad.relation_holds


def test_stage6e_rows_are_json_serializable_and_preserve_interpretation_guards() -> None:
    rows = stage6e_rows()
    json.dumps(rows)
    assert rows["interpretation_guards"]["record_transport_is_phenomenal_passage"] is False
    assert (
        rows["interpretation_guards"]["operational_equality_implies_modal_equivalence"]
        is False
    )
