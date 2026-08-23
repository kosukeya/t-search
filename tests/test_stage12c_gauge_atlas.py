import numpy as np
import pytest

from t_search.stage12_gauge_atlas import (
    STAGE12C_ATOL,
    STAGE12C_FALSE_POSITIVE_REJECTED,
    STAGE12C_NODE_EXTERNAL_PARAMETERIZATION,
    STAGE12C_NODE_GAUGE_REPRESENTATIVE,
    STAGE12C_NODE_INTERNAL_CLOCK,
    STAGE12C_NODE_MODAL_CONTINUATION,
    STAGE12C_NODE_PHYSICAL_ORBIT,
    STAGE12C_NODE_RELATIONAL_EVENT,
    STAGE12C_NUMERICALLY_REFUTED,
    STAGE12C_NUMERICAL_STATUS_RECONSTRUCTIBLE,
    STAGE12C_TYPED_STATUS_LOST,
    canonical_stage12c_composition_checks,
    canonical_stage12c_descent_evaluations,
    canonical_stage12c_gauge_arrows,
    canonical_stage12c_inverse_checks,
    canonical_stage12c_quotient_classes,
    canonical_stage12c_typed_nodes,
    canonical_stage12c_wrong_invariant_controls,
    stage12c_diagnostics,
    stage12c_gauge_arrow,
    stage12c_modal_separation_control,
    stage12c_orbit_identity_ablation,
)
from t_search.stage12_multi_orbit import (
    STAGE12A_GAUGE_FLOW_TYPE,
    canonical_stage12a_orbits,
    canonical_stage12a_representatives_for_orbit,
)
from t_search.stage12_relational import STAGE12B_TAU_VALUES


def test_stage12c_typed_nodes_keep_orbit_representative_parameter_event_clock_and_modal_roles_distinct() -> None:
    nodes = canonical_stage12c_typed_nodes()
    node_types = {item.node_type for item in nodes}
    assert {
        STAGE12C_NODE_PHYSICAL_ORBIT,
        STAGE12C_NODE_GAUGE_REPRESENTATIVE,
        STAGE12C_NODE_EXTERNAL_PARAMETERIZATION,
        STAGE12C_NODE_RELATIONAL_EVENT,
        STAGE12C_NODE_INTERNAL_CLOCK,
        STAGE12C_NODE_MODAL_CONTINUATION,
    }.issubset(node_types)
    assert len({item.node_id for item in nodes}) == len(nodes)

    orbit_nodes = [item for item in nodes if item.node_type == STAGE12C_NODE_PHYSICAL_ORBIT]
    representative_nodes = [
        item for item in nodes if item.node_type == STAGE12C_NODE_GAUGE_REPRESENTATIVE
    ]
    parameterization_nodes = [
        item for item in nodes if item.node_type == STAGE12C_NODE_EXTERNAL_PARAMETERIZATION
    ]
    clock_nodes = [item for item in nodes if item.node_type == STAGE12C_NODE_INTERNAL_CLOCK]
    continuation_nodes = [
        item for item in nodes if item.node_type == STAGE12C_NODE_MODAL_CONTINUATION
    ]
    assert len(orbit_nodes) == 4
    assert len(representative_nodes) == 20
    assert len(parameterization_nodes) == 16
    assert len(clock_nodes) == 4
    assert len(continuation_nodes) == 2
    assert all(item.orbit_id is not None for item in orbit_nodes + representative_nodes + parameterization_nodes + clock_nodes)
    assert all(item.orbit_id is None for item in continuation_nodes)


def test_stage12c_same_orbit_gauge_groupoid_has_identity_inverse_and_composition() -> None:
    arrows = canonical_stage12c_gauge_arrows()
    inverse_checks = canonical_stage12c_inverse_checks()
    composition_checks = canonical_stage12c_composition_checks()

    assert len(arrows) == 100
    assert sum(item.is_identity for item in arrows) == 20
    assert all(item.transform_type == STAGE12A_GAUGE_FLOW_TYPE for item in arrows)
    assert max(item.phase_space_residual for item in arrows) <= STAGE12C_ATOL
    assert max(item.Q_D_drift for item in arrows) <= STAGE12C_ATOL
    assert max(item.P_D_drift for item in arrows) <= STAGE12C_ATOL

    assert len(inverse_checks) == 100
    assert all(item.passed for item in inverse_checks)
    assert max(item.delta_sum_residual for item in inverse_checks) <= STAGE12C_ATOL
    assert max(item.endpoint_residual for item in inverse_checks) <= STAGE12C_ATOL
    assert max(item.invariant_residual for item in inverse_checks) <= STAGE12C_ATOL

    assert len(composition_checks) == 500
    assert all(item.passed for item in composition_checks)
    assert max(item.delta_composition_residual for item in composition_checks) <= STAGE12C_ATOL
    assert max(item.direct_transport_residual for item in composition_checks) <= STAGE12C_ATOL
    assert max(item.invariant_residual for item in composition_checks) <= STAGE12C_ATOL


def test_stage12c_cross_orbit_gauge_arrow_is_rejected_at_construction() -> None:
    source_orbit, target_orbit = canonical_stage12a_orbits()[:2]
    source = canonical_stage12a_representatives_for_orbit(source_orbit)[0]
    target = canonical_stage12a_representatives_for_orbit(target_orbit)[0]
    with pytest.raises(ValueError, match="cannot connect distinct physical orbits"):
        stage12c_gauge_arrow(source, target)


def test_stage12c_quotient_recovers_exact_four_orbit_partition_from_arrow_connectivity() -> None:
    quotient = canonical_stage12c_quotient_classes()
    assert len(quotient) == 4
    assert sorted(len(item.representative_ids) for item in quotient) == [5, 5, 5, 5]
    assert sum(len(item.representative_ids) for item in quotient) == 20
    assert all(len(item.inferred_orbit_ids) == 1 for item in quotient)
    assert {item.inferred_orbit_ids[0] for item in quotient} == {
        orbit.orbit_id for orbit in canonical_stage12a_orbits()
    }
    assert max(item.max_Q_D_spread for item in quotient) <= STAGE12C_ATOL
    assert max(item.max_P_D_spread for item in quotient) <= STAGE12C_ATOL


def test_stage12c_dirac_and_relational_observables_descend_to_quotient_classes() -> None:
    evaluations = canonical_stage12c_descent_evaluations()
    assert len(evaluations) == 4 * len(STAGE12B_TAU_VALUES) == 16
    assert {item.tau for item in evaluations} == set(STAGE12B_TAU_VALUES)
    assert max(item.max_Q_D_spread for item in evaluations) <= STAGE12C_ATOL
    assert max(item.max_P_D_spread for item in evaluations) <= STAGE12C_ATOL
    assert max(item.max_relational_q_spread for item in evaluations) <= STAGE12C_ATOL
    assert max(item.max_relational_dq_dT_spread for item in evaluations) <= STAGE12C_ATOL

    orbit_by_id = {orbit.orbit_id: orbit for orbit in canonical_stage12a_orbits()}
    for item in evaluations:
        orbit = orbit_by_id[item.inferred_orbit_id]
        assert np.isclose(item.Q_D, orbit.Q_D, atol=STAGE12C_ATOL, rtol=0.0)
        assert np.isclose(item.P_D, orbit.P_D, atol=STAGE12C_ATOL, rtol=0.0)
        assert np.isclose(
            item.relational_q,
            orbit.Q_D + orbit.P_D * item.tau,
            atol=STAGE12C_ATOL,
            rtol=0.0,
        )
        assert np.isclose(
            item.relational_dq_dT,
            orbit.P_D,
            atol=STAGE12C_ATOL,
            rtol=0.0,
        )


def test_stage12c_orbit_identity_ablation_separates_typed_loss_from_numerical_reconstructibility() -> None:
    ablation = stage12c_orbit_identity_ablation()
    assert ablation.resource == "typed orbit identity/correspondence"
    assert ablation.typed_status == STAGE12C_TYPED_STATUS_LOST
    assert ablation.numerical_status == STAGE12C_NUMERICAL_STATUS_RECONSTRUCTIBLE
    assert ablation.reconstructed_class_count == 4
    assert ablation.reconstructed_class_sizes == (5, 5, 5, 5)
    assert "orbit labels removed by construction" in ablation.provenance


def test_stage12c_wrong_invariant_gauge_paths_are_numerically_detected() -> None:
    controls = canonical_stage12c_wrong_invariant_controls()
    assert len(controls) == 2
    assert {item.control_id for item in controls} == {"wrong_Q_D_path", "wrong_P_D_path"}
    assert all(item.classification == STAGE12C_NUMERICALLY_REFUTED for item in controls)

    wrong_Q = next(item for item in controls if item.control_id == "wrong_Q_D_path")
    wrong_P = next(item for item in controls if item.control_id == "wrong_P_D_path")
    assert wrong_Q.Q_D_drift > STAGE12C_ATOL
    assert wrong_Q.phase_space_residual > STAGE12C_ATOL
    assert wrong_P.P_D_drift > STAGE12C_ATOL
    assert max(wrong_P.phase_space_residual, wrong_P.constraint_residual) > STAGE12C_ATOL


def test_stage12c_gauge_quotient_does_not_identify_constraint_orbits_with_modal_continuations() -> None:
    control = stage12c_modal_separation_control()
    assert len(control.quotient_ids) == 4
    assert control.continuation_node_ids == ("continuation::h_L", "continuation::h_R")
    assert not control.gauge_arrow_touches_continuation
    assert not control.quotient_identifies_continuation
    assert control.classification == STAGE12C_FALSE_POSITIVE_REJECTED


def test_stage12c_diagnostics_close_criteria_24_through_31() -> None:
    diagnostics = stage12c_diagnostics()
    assert diagnostics.gauge_arrow_count == 100
    assert diagnostics.identity_arrow_count == 20
    assert diagnostics.inverse_check_count == 100
    assert diagnostics.composition_check_count == 500
    assert diagnostics.quotient_class_count == 4
    assert diagnostics.quotient_member_count == 20
    assert diagnostics.quotient_class_sizes == (5, 5, 5, 5)
    assert diagnostics.descent_evaluation_count == 16
    assert diagnostics.max_gauge_phase_space_residual <= STAGE12C_ATOL
    assert diagnostics.max_gauge_Q_D_drift <= STAGE12C_ATOL
    assert diagnostics.max_gauge_P_D_drift <= STAGE12C_ATOL
    assert diagnostics.max_inverse_residual <= STAGE12C_ATOL
    assert diagnostics.max_composition_residual <= STAGE12C_ATOL
    assert diagnostics.max_descent_Q_D_spread <= STAGE12C_ATOL
    assert diagnostics.max_descent_P_D_spread <= STAGE12C_ATOL
    assert diagnostics.max_descent_q_spread <= STAGE12C_ATOL
    assert diagnostics.max_descent_dq_dT_spread <= STAGE12C_ATOL
    assert diagnostics.cross_orbit_gauge_arrow_count == 0
    assert diagnostics.quotient_partition_exact
    assert diagnostics.orbit_identity_ablation_typed_status == STAGE12C_TYPED_STATUS_LOST
    assert diagnostics.orbit_identity_ablation_numerical_status == STAGE12C_NUMERICAL_STATUS_RECONSTRUCTIBLE
    assert diagnostics.wrong_invariant_controls_detected == 2
    assert diagnostics.modal_continuation_separated
    assert diagnostics.criteria_24_31_satisfied
