import pytest

import t_search.stage8_ablation as ablation_module
from t_search.stage8_ablation import (
    ROLE_IDS,
    RoleStatus,
    mismatch_diagnostics,
    no_record_v_family_diagnostics,
    perspective_map_reconstruction_diagnostics,
    semantic_weight_reconstruction_diagnostics,
    singleton_qext_diagnostics,
    stage8f_ablation_matrix,
    stage8f_status_table,
    stage8f_summary,
)

ATOL = 1e-9

NO_RECORD = no_record_v_family_diagnostics()
RECONSTRUCTION = perspective_map_reconstruction_diagnostics()
SINGLETON = singleton_qext_diagnostics()
SEMANTIC_WEIGHT = semantic_weight_reconstruction_diagnostics()
MATRIX = stage8f_ablation_matrix()


def _case(name: str):
    return next(case for case in MATRIX if case.ingredient == name)


def test_stage8f_status_vocabulary_keeps_functional_outcomes_distinct():
    assert tuple(status.value for status in RoleStatus) == (
        "preserved",
        "reconstructible",
        "inaccessible",
        "lost",
        "underdetermined",
        "not_established",
    )


def test_stage8f_record_neutralized_family_remains_a_constrained_two_continuation_v_witness():
    diagnostics = NO_RECORD
    assert diagnostics.qext_size == 2
    assert diagnostics.physical_dimension == 14
    assert diagnostics.minimum_clock_reduction_rank == 14
    assert diagnostics.max_constraint_residual <= ATOL
    assert diagnostics.common_current_state_residual <= ATOL
    assert diagnostics.future_overlap_squared < 1.0 - ATOL
    assert diagnostics.future_state_distance > ATOL
    assert diagnostics.physically_inequivalent is True
    assert diagnostics.distinct_clock_state_transports == 108
    assert diagnostics.max_state_transport_residual <= ATOL
    assert diagnostics.max_inverse_residual <= ATOL
    assert diagnostics.max_metric_covariance_residual <= ATOL
    assert diagnostics.perspective_structure_preserved is True


def test_stage8f_record_neutralized_family_loses_current_r_but_preserves_modal_underdetermination():
    diagnostics = NO_RECORD
    assert diagnostics.current_record_information_left == pytest.approx(0.0, abs=ATOL)
    assert diagnostics.current_record_information_right == pytest.approx(0.0, abs=ATOL)
    assert diagnostics.current_record_lost is True
    assert diagnostics.matched_operational_views_equal is True
    assert diagnostics.privileged_modal_structures_distinct is True
    assert diagnostics.weight_mismatch_changes_prediction is True

    case = _case("record_coupling_neutralized")
    assert case.status("V_physical_multiplicity") is RoleStatus.PRESERVED
    assert case.status("V_selected_vs_unselected_semantics") is RoleStatus.PRESERVED
    assert case.status("V_weights") is RoleStatus.PRESERVED
    assert case.status("P_V_class_transport") is RoleStatus.PRESERVED
    assert case.status("O_V_extension_relation") is RoleStatus.PRESERVED
    assert case.status("current_record_content") is RoleStatus.LOST
    assert case.status("local_record_access") is RoleStatus.LOST


def test_stage8f_singleton_qext_removes_multiplicity_but_not_formal_modal_typing():
    diagnostics = SINGLETON
    assert diagnostics.qext_size == 1
    assert diagnostics.physical_multiplicity_lost is True
    assert diagnostics.semantic_types_distinct is True
    assert diagnostics.ontic_selector_absent is True
    assert diagnostics.singleton_weight == pytest.approx(1.0, abs=ATOL)
    assert diagnostics.singleton_weight_reconstructible_from_normalization is True
    assert diagnostics.current_record_information == pytest.approx(1.0, abs=ATOL)
    assert diagnostics.perspective_transport_preserved is True
    assert diagnostics.future_extension_present is True

    case = _case("qext_collapsed_singleton")
    assert case.status("V_physical_multiplicity") is RoleStatus.LOST
    assert case.status("V_selected_vs_unselected_semantics") is RoleStatus.PRESERVED
    assert case.status("V_weights") is RoleStatus.RECONSTRUCTIBLE


def test_stage8f_selected_vs_unselected_semantics_are_not_reconstructed_from_public_por():
    diagnostics = SEMANTIC_WEIGHT
    assert diagnostics.same_carrier_distinct_modal_semantics is True
    assert diagnostics.modal_semantics_reconstructible_from_public_por is False
    case = _case("modal_semantics_removed")
    assert case.status("V_selected_vs_unselected_semantics") is RoleStatus.LOST
    for role in (
        "V_physical_multiplicity",
        "V_weights",
        "P_V_class_transport",
        "O_V_extension_relation",
        "current_record_content",
        "local_record_access",
    ):
        assert case.status(role) is RoleStatus.PRESERVED


def test_stage8f_weights_are_underdetermined_by_the_same_carrier():
    diagnostics = SEMANTIC_WEIGHT
    assert diagnostics.uniform_weights == (0.5, 0.5)
    assert diagnostics.alternative_weights == (0.75, 0.25)
    assert diagnostics.same_carrier_admits_distinct_weights is True
    assert diagnostics.prediction_density_residual > ATOL
    assert diagnostics.prediction_changes_with_weights is True
    assert diagnostics.weights_reconstructible_from_carrier is False
    case = _case("weights_unfixed")
    assert case.status("V_weights") is RoleStatus.UNDERDETERMINED


def test_stage8f_explicit_perspective_maps_are_reconstructible_from_node_coordinates():
    diagnostics = RECONSTRUCTION
    assert diagnostics.comparisons == 108
    assert diagnostics.max_reference_map_residual <= ATOL
    assert diagnostics.max_state_transport_residual <= ATOL
    assert diagnostics.max_inverse_residual <= ATOL
    assert diagnostics.max_metric_covariance_residual <= ATOL
    assert diagnostics.reconstructible is True
    case = _case("explicit_perspective_maps_removed")
    assert case.status("P_V_class_transport") is RoleStatus.RECONSTRUCTIBLE


def test_stage8f_removing_event_class_correspondence_makes_pv_correspondence_not_established():
    case = _case("event_correspondence_removed")
    assert case.status("P_V_class_transport") is RoleStatus.NOT_ESTABLISHED
    for role in (
        "V_physical_multiplicity",
        "V_selected_vs_unselected_semantics",
        "V_weights",
        "O_V_extension_relation",
        "current_record_content",
        "local_record_access",
    ):
        assert case.status(role) is RoleStatus.PRESERVED


def test_stage8f_hidden_record_access_is_inaccessible_not_lost():
    case = _case("current_record_access_hidden")
    assert case.status("current_record_content") is RoleStatus.PRESERVED
    assert case.status("local_record_access") is RoleStatus.INACCESSIBLE
    access_probe = next(probe for probe in case.probes if probe.role == "local_record_access")
    assert access_probe.globally_represented is True
    assert access_probe.locally_accessible is False


def test_stage8f_mismatch_matrix_detects_all_declared_controls():
    mismatches = {item.mismatch: item for item in mismatch_diagnostics()}
    assert set(mismatches) == {
        "wrong_continuation_map",
        "wrong_class_correspondence",
        "wrong_event_correspondence",
        "weight_mismatch",
        "wrong_observable_coordinates",
    }
    assert all(item.detected for item in mismatches.values())
    assert dict(mismatches["wrong_continuation_map"].measurements)["state_residual"] > ATOL
    assert (
        dict(mismatches["weight_mismatch"].measurements)[
            "transported_predictive_density_residual"
        ]
        > ATOL
    )
    assert (
        dict(mismatches["wrong_observable_coordinates"].measurements)[
            "bare_metric_self_adjoint_residual"
        ]
        > ATOL
    )


def test_stage8f_status_table_has_one_row_per_ablation_and_one_column_per_role():
    table = stage8f_status_table()
    assert tuple(table) == (
        "record_coupling_neutralized",
        "qext_collapsed_singleton",
        "modal_semantics_removed",
        "weights_unfixed",
        "explicit_perspective_maps_removed",
        "event_correspondence_removed",
        "current_record_access_hidden",
    )
    assert all(tuple(row) == ROLE_IDS for row in table.values())


def test_stage8f_summary_closes_criteria_42_to_47_only(monkeypatch):
    monkeypatch.setattr(
        ablation_module,
        "no_record_v_family_diagnostics",
        lambda: NO_RECORD,
    )
    monkeypatch.setattr(
        ablation_module,
        "perspective_map_reconstruction_diagnostics",
        lambda: RECONSTRUCTION,
    )
    monkeypatch.setattr(
        ablation_module,
        "semantic_weight_reconstruction_diagnostics",
        lambda: SEMANTIC_WEIGHT,
    )
    monkeypatch.setattr(ablation_module, "stage8f_ablation_matrix", lambda: MATRIX)
    summary = stage8f_summary()
    assert tuple(summary["current_execution_criteria"].keys()) == (
        "42",
        "43",
        "44",
        "45",
        "46",
        "47",
    )
    assert summary["next"] == "Stage 8G — synthesis and evidence-selected next gate"
    guards = summary["guards"]
    assert "lost != metaphysically irreducible" in guards
    assert "reconstructible != universally redundant" in guards
    assert "underdetermined != ontically open" in guards
    assert "inaccessible != globally absent" in guards
    assert "not_established != false" in guards
    assert "full Stage 8C measurement covariance remains not_established" in guards
