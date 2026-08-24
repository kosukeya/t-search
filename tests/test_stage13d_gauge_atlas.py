from dataclasses import replace

import pytest

from t_search.stage13_gauge_atlas import (
    STAGE13D_MODAL_STATUS,
    STAGE13D_NODE_BASIS,
    STAGE13D_NODE_CLOCK,
    STAGE13D_NODE_EVENT,
    STAGE13D_NODE_GENERATOR,
    STAGE13D_NODE_MODAL,
    STAGE13D_NODE_PATH_WORD,
    STAGE13D_NODE_PHYSICAL_ORBIT,
    STAGE13D_NODE_REPRESENTATIVE,
    STAGE13D_NUMERICAL_STATUS_RECONSTRUCTIBLE,
    STAGE13D_TYPED_STATUS_LOST,
    canonical_stage13d_atlas_arrows,
    canonical_stage13d_compensated_descent_checks,
    canonical_stage13d_quotient_classes,
    canonical_stage13d_quotient_descent_evaluations,
    canonical_stage13d_typed_nodes,
    stage13d_atlas_arrow,
    stage13d_diagnostics,
    stage13d_path_provenance_ablation,
)
from t_search.stage13_multi_constraint import (
    STAGE13A_ATOL,
    canonical_stage13a_orbits,
    canonical_stage13a_phi_T_transports,
    canonical_stage13a_representatives_for_orbit,
)
from t_search.stage13_paths import (
    STAGE13B_PATH_WORD_ROLE,
    STAGE13B_PHI_T,
    STAGE13B_PHI_X,
    STAGE13B_TEMPORAL_ORDER_STATUS,
)


def test_stage13d_typed_nodes_keep_all_required_roles_distinct() -> None:
    nodes = canonical_stage13d_typed_nodes()
    node_types = {item.node_type for item in nodes}

    assert len(nodes) == 87
    assert {
        STAGE13D_NODE_PHYSICAL_ORBIT,
        STAGE13D_NODE_REPRESENTATIVE,
        STAGE13D_NODE_GENERATOR,
        STAGE13D_NODE_BASIS,
        STAGE13D_NODE_PATH_WORD,
        STAGE13D_NODE_EVENT,
        STAGE13D_NODE_CLOCK,
        STAGE13D_NODE_MODAL,
    }.issubset(node_types)
    assert sum(item.node_type == STAGE13D_NODE_PHYSICAL_ORBIT for item in nodes) == 4
    assert sum(item.node_type == STAGE13D_NODE_REPRESENTATIVE for item in nodes) == 36
    assert sum(item.node_type == STAGE13D_NODE_GENERATOR for item in nodes) == 2
    assert sum(item.node_type == STAGE13D_NODE_BASIS for item in nodes) == 1
    assert sum(item.node_type == STAGE13D_NODE_PATH_WORD for item in nodes) == 4
    assert sum(item.node_type == STAGE13D_NODE_EVENT for item in nodes) == 36
    assert sum(item.node_type == STAGE13D_NODE_CLOCK for item in nodes) == 2
    assert sum(item.node_type == STAGE13D_NODE_MODAL for item in nodes) == 2


def test_stage13d_atlas_uses_typed_single_generator_connectivity() -> None:
    arrows = canonical_stage13d_atlas_arrows()

    assert len(arrows) == 144
    assert sum(item.path_word == (STAGE13B_PHI_T,) for item in arrows) == 72
    assert sum(item.path_word == (STAGE13B_PHI_X,) for item in arrows) == 72
    assert all(item.path_word_role == STAGE13B_PATH_WORD_ROLE for item in arrows)
    assert max(item.phase_space_residual for item in arrows) <= STAGE13A_ATOL
    assert max(item.constraint_residual for item in arrows) <= STAGE13A_ATOL


def test_stage13d_atlas_rejects_cross_orbit_generator_edge() -> None:
    transport = canonical_stage13a_phi_T_transports()[0]
    beta_rep = canonical_stage13a_representatives_for_orbit(canonical_stage13a_orbits()[1])[0]
    corrupted = replace(transport, target_representative_id=beta_rep.representative_id)

    with pytest.raises(ValueError, match="cross-orbit"):
        stage13d_atlas_arrow(corrupted)


def test_stage13d_connectivity_quotient_recovers_four_nine_member_classes() -> None:
    quotients = canonical_stage13d_quotient_classes()

    assert len(quotients) == 4
    assert tuple(sorted(len(item.representative_ids) for item in quotients)) == (9, 9, 9, 9)
    assert sum(len(item.representative_ids) for item in quotients) == 36
    assert all(len(item.inferred_orbit_ids) == 1 for item in quotients)
    assert all(item.internal_arrow_count == 36 for item in quotients)
    assert max(item.max_Q_D_spread for item in quotients) <= STAGE13A_ATOL
    assert max(item.max_P_D_spread for item in quotients) <= STAGE13A_ATOL


def test_stage13d_quotient_does_not_collapse_distinct_dirac_data() -> None:
    quotients = canonical_stage13d_quotient_classes()
    separations = []
    for index, left in enumerate(quotients):
        for right in quotients[index + 1 :]:
            separations.append(max(abs(left.Q_D - right.Q_D), abs(left.P_D - right.P_D)))

    assert len(separations) == 6
    assert min(separations) >= 0.5 - STAGE13A_ATOL
    assert all(value > STAGE13A_ATOL for value in separations)


def test_stage13d_dirac_and_two_clock_payload_descend_to_quotient() -> None:
    evaluations = canonical_stage13d_quotient_descent_evaluations()

    assert len(evaluations) == 36
    assert max(item.max_Q_D_spread for item in evaluations) <= STAGE13A_ATOL
    assert max(item.max_P_D_spread for item in evaluations) <= STAGE13A_ATOL
    assert max(item.max_relational_q_spread for item in evaluations) <= STAGE13A_ATOL
    values_by_quotient: dict[str, set[float]] = {}
    for item in evaluations:
        values_by_quotient.setdefault(item.quotient_id, set()).add(round(item.relational_q, 12))
    assert all(len(values) > 1 for values in values_by_quotient.values())


def test_stage13d_compensated_path_words_descend_to_same_payload() -> None:
    checks = canonical_stage13d_compensated_descent_checks()

    assert len(checks) == 144
    assert sum(item.relational_evaluation_count for item in checks) == 1296
    assert all(item.path_word_TX == (STAGE13B_PHI_T, STAGE13B_PHI_X) for item in checks)
    assert all(item.path_word_XT == (STAGE13B_PHI_X, STAGE13B_PHI_T) for item in checks)
    assert all(item.path_word_TX != item.path_word_XT for item in checks)
    assert max(item.max_dirac_payload_residual for item in checks) <= STAGE13A_ATOL
    assert max(item.max_relational_payload_residual for item in checks) <= STAGE13A_ATOL


def test_stage13d_path_provenance_ablation_separates_typing_from_numbers() -> None:
    ablation = stage13d_path_provenance_ablation()

    assert ablation.typed_status == STAGE13D_TYPED_STATUS_LOST
    assert ablation.numerical_status == STAGE13D_NUMERICAL_STATUS_RECONSTRUCTIBLE
    assert ablation.comparison_count == 144
    assert ablation.uniquely_reconstructed_target_count == 144
    assert "path_word_compensator_provenance_lost_numerically_reconstructible" == ablation.classification


def test_stage13d_path_word_is_neither_modal_continuation_nor_temporal_history() -> None:
    nodes = canonical_stage13d_typed_nodes()
    path_nodes = {item.node_id for item in nodes if item.node_type == STAGE13D_NODE_PATH_WORD}
    modal_nodes = {item.node_id for item in nodes if item.node_type == STAGE13D_NODE_MODAL}
    checks = canonical_stage13d_compensated_descent_checks()

    assert path_nodes
    assert modal_nodes
    assert path_nodes.isdisjoint(modal_nodes)
    assert all(item.modal_role_status == STAGE13D_MODAL_STATUS for item in checks)
    assert all(item.temporal_order_status == STAGE13B_TEMPORAL_ORDER_STATUS for item in checks)
    assert all(item.metaphysical_claim_status == "not_licensed" for item in checks)


def test_stage13d_diagnostics_close_criteria_32_38() -> None:
    diagnostics = stage13d_diagnostics()

    assert diagnostics.typed_node_count == 87
    assert diagnostics.atlas_arrow_count == 144
    assert diagnostics.phi_T_arrow_count == 72
    assert diagnostics.phi_X_arrow_count == 72
    assert diagnostics.cross_orbit_arrow_count == 0
    assert diagnostics.quotient_class_count == 4
    assert diagnostics.quotient_member_count == 36
    assert diagnostics.quotient_class_sizes == (9, 9, 9, 9)
    assert diagnostics.mixed_orbit_quotient_count == 0
    assert diagnostics.quotient_descent_evaluation_count == 36
    assert diagnostics.compensated_descent_check_count == 144
    assert diagnostics.compensated_relational_evaluation_count == 1296
    assert diagnostics.distinct_quotient_dirac_pair_count == 6
    assert diagnostics.max_quotient_Q_D_spread <= STAGE13A_ATOL
    assert diagnostics.max_quotient_P_D_spread <= STAGE13A_ATOL
    assert diagnostics.max_quotient_relational_q_spread <= STAGE13A_ATOL
    assert diagnostics.max_compensated_dirac_payload_residual <= STAGE13A_ATOL
    assert diagnostics.max_compensated_relational_payload_residual <= STAGE13A_ATOL
    assert diagnostics.path_ablation_typed_status == STAGE13D_TYPED_STATUS_LOST
    assert diagnostics.path_ablation_numerical_status == STAGE13D_NUMERICAL_STATUS_RECONSTRUCTIBLE
    assert diagnostics.path_ablation_reconstructed_target_count == 144
    assert diagnostics.path_word_modal_separation_explicit
    assert diagnostics.path_word_temporal_separation_explicit
    assert diagnostics.quotient_partition_exact
    assert diagnostics.physical_dirac_data_not_collapsed
    assert diagnostics.criteria_32_38_satisfied
