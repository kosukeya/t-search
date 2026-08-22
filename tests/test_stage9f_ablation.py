import pytest

from t_search.stage9_ablation import (
    ABLATION_IDS,
    ROLE_IDS,
    accessibility_diagnostics,
    directional_mechanism_diagnostics,
    perspective_edge_reconstruction_diagnostics,
    singleton_qext_diagnostics,
    stage9f_ablation_matrix,
    stage9f_diagnostics,
    stage9f_status_table,
    stage9f_summary,
)


@pytest.fixture(scope="module")
def diagnostics():
    return stage9f_diagnostics()


@pytest.fixture(scope="module")
def status_table():
    return stage9f_status_table()


def test_stage9f_frozen_role_and_ablation_orders_are_explicit():
    assert ROLE_IDS == (
        "R_content",
        "R_direction",
        "R_access",
        "V_extension_multiplicity",
        "V_selected_vs_unselected_semantics",
        "V_weights",
        "P_perspective_transport",
        "event_class_correspondence",
        "P_RV_typed_identification",
        "O_V_extension_relation",
    )
    assert ABLATION_IDS == (
        "record_write_neutralized",
        "scrambler_neutralized",
        "qext_collapsed_singleton",
        "modal_semantics_removed",
        "weights_unfixed",
        "local_record_access_hidden",
        "explicit_perspective_edges_removed",
        "event_class_correspondence_removed",
    )
    assert tuple(case.ingredient for case in stage9f_ablation_matrix()) == ABLATION_IDS


def test_record_write_neutralization_removes_r_but_preserves_nontrivial_v_and_p(
    diagnostics, status_table
):
    directional = diagnostics.directional_mechanism
    assert all(abs(value) <= 1e-9 for _, value in directional.record_write_current_information)
    assert all(abs(value) <= 1e-9 for _, value in directional.record_write_record_scores)
    assert all(abs(value) <= 1e-9 for _, value in directional.record_write_accessibility_scores)
    assert directional.record_write_v_nontrivial is True
    assert directional.record_write_valid_constrained_carriers is True
    assert directional.record_write_transport.comparisons == 108
    assert directional.record_write_transport.minimum_chart_rank == 14
    assert directional.record_write_transport.valid is True

    row = status_table["record_write_neutralized"]
    assert row["R_content"] == "lost"
    assert row["R_direction"] == "lost"
    assert row["R_access"] == "lost"
    assert row["V_extension_multiplicity"] == "preserved"
    assert row["P_perspective_transport"] == "preserved"


def test_scrambler_neutralization_keeps_record_content_but_removes_direction(
    diagnostics, status_table
):
    directional = diagnostics.directional_mechanism
    assert all(value == pytest.approx(1.0, abs=1e-9) for _, value in directional.no_scramble_current_information)
    assert all(abs(value) <= 1e-9 for _, value in directional.no_scramble_record_scores)
    assert all(abs(value) <= 1e-9 for _, value in directional.no_scramble_accessibility_scores)
    assert directional.no_scramble_direction_lost_while_current_record_retained is True
    assert directional.no_scramble_v_nontrivial is True
    assert directional.no_scramble_valid_constrained_carriers is True
    assert directional.no_scramble_transport.comparisons == 108
    assert directional.no_scramble_transport.minimum_chart_rank == 14
    assert directional.no_scramble_transport.valid is True

    row = status_table["scrambler_neutralized"]
    assert row["R_content"] == "preserved"
    assert row["R_direction"] == "lost"
    assert row["R_access"] == "preserved"
    assert row["V_extension_multiplicity"] == "preserved"
    assert row["P_perspective_transport"] == "preserved"


def test_singleton_qext_removes_v_multiplicity_but_retains_directional_r(
    diagnostics, status_table
):
    singleton = diagnostics.singleton_qext
    assert singleton.qext_size == 1
    assert singleton.current_record_information == pytest.approx(1.0, abs=1e-9)
    assert singleton.record_score == pytest.approx(1.0, abs=1e-9)
    assert singleton.accessibility_score == pytest.approx(0.5, abs=1e-9)
    assert singleton.record_defined is True
    assert singleton.semantic_types_distinct is True
    assert singleton.ontic_has_no_selected_continuation_field is True
    assert singleton.singleton_weight == pytest.approx(1.0, abs=1e-12)
    assert singleton.singleton_weight_reconstructible_from_normalization is True
    assert singleton.future_extension_present is True
    assert singleton.transport.comparisons == 54
    assert singleton.transport.minimum_chart_rank == 14
    assert singleton.transport.valid is True

    row = status_table["qext_collapsed_singleton"]
    assert row["R_direction"] == "preserved"
    assert row["R_access"] == "preserved"
    assert row["V_extension_multiplicity"] == "lost"
    assert row["V_selected_vs_unselected_semantics"] == "preserved"
    assert row["V_weights"] == "reconstructible"
    assert row["P_perspective_transport"] == "preserved"


def test_modal_semantics_and_weights_have_distinct_ablation_statuses(
    diagnostics, status_table
):
    semantic = diagnostics.semantic_weights
    assert semantic.matched_public_views_equal is True
    assert semantic.privileged_modal_structures_distinct is True
    assert semantic.modal_semantics_reconstructible_from_public_carrier is False
    assert semantic.uniform_weights == (0.5, 0.5)
    assert semantic.alternative_weights == (0.75, 0.25)
    assert semantic.prediction_changes_with_weights is True
    assert semantic.weight_change_preserves_directional_data is True
    assert semantic.weights_reconstructible_from_carrier is False

    assert (
        status_table["modal_semantics_removed"]["V_selected_vs_unselected_semantics"]
        == "lost"
    )
    assert status_table["weights_unfixed"]["V_weights"] == "underdetermined"
    assert status_table["weights_unfixed"]["R_direction"] == "preserved"


def test_hidden_local_access_keeps_global_direction_and_v_but_makes_access_inaccessible(
    diagnostics, status_table
):
    access = diagnostics.accessibility
    assert access.global_record_information == pytest.approx(1.0, abs=1e-9)
    assert access.global_record_score == pytest.approx(1.0, abs=1e-9)
    assert access.global_accessibility_score == pytest.approx(0.5, abs=1e-9)
    assert access.global_direction_preserved is True
    assert access.local_accessibility_field_exposed is False
    assert access.local_access_inaccessible is True
    assert access.v_extension_count_retained == 2
    assert access.weights_retained == (0.5, 0.5)
    assert "accessibility_score" not in access.hidden_view_field_names

    row = status_table["local_record_access_hidden"]
    assert row["R_content"] == "preserved"
    assert row["R_direction"] == "preserved"
    assert row["R_access"] == "inaccessible"
    assert row["V_extension_multiplicity"] == "preserved"


def test_explicit_p_edges_are_reconstructible_from_per_node_coordinates(
    diagnostics, status_table
):
    reconstruction = diagnostics.edge_reconstruction
    assert reconstruction.comparisons == 108
    assert reconstruction.minimum_chart_rank == 14
    assert reconstruction.valid is True
    assert reconstruction.reconstructible_from_node_coordinates is True
    assert reconstruction.max_reference_map_residual is not None
    assert reconstruction.max_reference_map_residual <= 1e-9
    assert (
        status_table["explicit_perspective_edges_removed"]["P_perspective_transport"]
        == "reconstructible"
    )


def test_removing_event_class_chi_keeps_local_p_but_not_typed_rv_identification(
    diagnostics, status_table
):
    correspondence = diagnostics.correspondence
    assert correspondence.local_p_atlas_retained is True
    assert correspondence.local_p_comparisons == 108
    assert correspondence.event_class_correspondence_declared is False
    assert correspondence.typed_cross_perspective_rv_identification_established is False
    assert correspondence.wrong_class_control_rejected is True
    assert correspondence.wrong_event_control_rejected is True

    row = status_table["event_class_correspondence_removed"]
    assert row["P_perspective_transport"] == "preserved"
    assert row["event_class_correspondence"] == "lost"
    assert row["P_RV_typed_identification"] == "not_established"


def test_wrong_record_observable_coordinates_are_detected(diagnostics):
    mismatch = diagnostics.wrong_observable
    assert mismatch.mismatch == "wrong_record_observable_coordinates"
    assert mismatch.affected_role == "P_RV_typed_identification"
    assert mismatch.detected is True
    measurements = dict(mismatch.measurements)
    assert measurements["bare_observable_residual"] > 1e-9
    assert measurements["typed_observable_transport_residual"] <= 1e-9


def test_stage9f_summary_closes_43_to_47_and_preserves_guards():
    summary = stage9f_summary()
    assert summary["stage"] == "9F"
    assert summary["exit_criteria_satisfied"] == tuple(range(43, 48))
    assert summary["next"] == "Stage 9G — synthesis and evidence-selected next gate"
    assert "record content != directional record arrow" in summary["guards"]
    assert "inaccessible != globally absent" in summary["guards"]
    assert "reconstructible != universally redundant" in summary["guards"]
    assert "local P transport without chi != typed event/class identification" in summary["guards"]
    assert "covariance of a wrongly typed observable != semantic correctness" in summary["guards"]
    assert "directional record arrow != ontological becoming" in summary["guards"]
    assert "full Stage 9C future-measurement covariance remains not_established" in summary["guards"]
