import pytest

from t_search.stage9_compatibility import (
    stage9e_compatibility_diagnostics,
    stage9e_compatibility_matrix,
    stage9e_constraint_assessment,
    stage9e_summary,
)


@pytest.fixture(scope="module")
def diagnostics():
    return stage9e_compatibility_diagnostics()


def _matrix_by_relation():
    return {entry.relation: entry for entry in stage9e_compatibility_matrix()}


def _constraints_by_relation():
    return {entry.relation: entry for entry in stage9e_constraint_assessment()}


def test_stage9e_matrix_classifies_exactly_six_frozen_relations(diagnostics):
    matrix = _matrix_by_relation()
    assert tuple(matrix) == (
        "R_direction-V_extension",
        "R_direction-V_weights",
        "R_direction-V_semantics",
        "R_access-V",
        "P-R_direction-V",
        "O-R_direction-V",
    )
    assert tuple(entry.status for entry in matrix.values()) == (
        "compatible",
        "compatible",
        "underdetermined",
        "compatible",
        "compatible",
        "compatible",
    )
    assert diagnostics.qext_nontrivial is True


def test_stage9e_direction_and_v_extension_are_compatible_but_not_identified(diagnostics):
    assert diagnostics.coherent_direction_on_canonical_carrier is True
    assert diagnostics.direction_v_extension_coexistence is True
    assert diagnostics.direction_controls_retain_v_extension is True
    assert diagnostics.r_direction_v_extension_compatible is True
    assert diagnostics.v_extension_identity_does_not_determine_direction is True
    assert diagnostics.direction_does_not_determine_v_extension_identity is True

    constraints = _constraints_by_relation()
    assert constraints["V_extension=>R_direction"].status == "implication_refuted"
    assert constraints["R_direction=>V_extension identity"].status == "implication_refuted"


def test_stage9e_v_weights_can_change_without_changing_current_direction(diagnostics):
    assert diagnostics.weight_change_detected is True
    assert diagnostics.weight_change_preserves_current_direction is True
    assert diagnostics.r_direction_v_weights_compatible is True
    assert _matrix_by_relation()["R_direction-V_weights"].status == "compatible"


def test_stage9e_direction_does_not_resolve_modal_semantics(diagnostics):
    assert diagnostics.matched_directional_public_views is True
    assert diagnostics.privileged_modal_structures_distinct is True
    assert diagnostics.hidden_selector_swap_publicly_invariant is True
    assert diagnostics.r_direction_v_semantics_underdetermined is True
    assert _matrix_by_relation()["R_direction-V_semantics"].status == "underdetermined"


def test_stage9e_accessibility_and_v_coexist_across_declared_clock_atlas(diagnostics):
    assert diagnostics.positive_access_shared_across_continuations is True
    assert diagnostics.access_covariant_across_clock_atlas is True
    assert diagnostics.r_access_v_compatible is True
    assert _matrix_by_relation()["R_access-V"].status == "compatible"


def test_stage9e_p_direction_v_joint_transport_is_compatible_with_scope_boundary(diagnostics):
    assert diagnostics.p_transport_covariant is True
    assert diagnostics.p_direction_v_compatible is True
    assert _matrix_by_relation()["P-R_direction-V"].status == "compatible"
    assert diagnostics.full_future_measurement_covariance_established is False
    assert _constraints_by_relation()["full future-measurement covariance"].status == "not_established"


def test_stage9e_o_direction_v_joint_compatibility_refutes_order_determining_arrow(diagnostics):
    assert diagnostics.same_order_skeleton_supports_positive_negative_and_zero_direction is True
    assert diagnostics.o_direction_v_compatible is True
    assert diagnostics.o_does_not_determine_r_direction is True
    assert _matrix_by_relation()["O-R_direction-V"].status == "compatible"
    assert _constraints_by_relation()["O=>R_direction"].status == "implication_refuted"


def test_stage9e_does_not_invent_a_direct_xi_rv_value_law(diagnostics):
    assert diagnostics.direct_xi_rv_value_constraint_established is False
    assert _constraints_by_relation()["direct Xi_RV value constraint"].status == "not_established"


def test_stage9e_summary_closes_37_to_42_and_preserves_interpretation_guards():
    summary = stage9e_summary()
    assert summary["stage"] == "9E"
    assert summary["exit_criteria_satisfied"] == tuple(range(37, 43))
    assert summary["next"] == "Stage 9F — ablation / reconstruction / accessibility matrix"
    assert "R-V compatibility != R=V" in summary["guards"]
    assert "accessible canonical R_access-V compatibility != accessibility independence" in summary["guards"]
    assert "absence of an established direct Xi_RV value constraint != proof that no such constraint exists" in summary["guards"]
    assert "full Stage 9C future-measurement covariance remains not_established" in summary["guards"]
    assert "directional record arrow != ontological becoming" in summary["guards"]
