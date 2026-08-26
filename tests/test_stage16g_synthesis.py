from t_search.stage16_synthesis import (
    STAGE16G_BOUNDED_RESULT,
    STAGE16G_GUARDS,
    STAGE16G_SELECTED_CLASSIFICATION,
    STAGE16G_SYNTHESIS_VOCABULARY,
    STAGE17_CANDIDATE_POOL,
    STAGE17_SELECTED_GATE,
    STAGE17_SELECTED_GATE_STATEMENT,
    canonical_stage17_candidate_scores,
    ranked_stage17_candidates,
    stage16g_diagnostics,
    stage16g_select_classification,
    stage16g_summary,
)


def test_stage16g_selects_exactly_one_frozen_synthesis_classification():
    selected = stage16g_select_classification()
    assert len(STAGE16G_SYNTHESIS_VOCABULARY) == 7
    assert len(set(STAGE16G_SYNTHESIS_VOCABULARY)) == 7
    assert selected in STAGE16G_SYNTHESIS_VOCABULARY
    assert selected == STAGE16G_SELECTED_CLASSIFICATION
    assert selected == "closed_cycle_local_path_covariant_nonlocal_only_in_declared_search"


def test_stage16g_synthesis_is_grounded_in_validated_stage16a_f_evidence():
    d = stage16g_diagnostics()
    assert d.stage16a_validated
    assert d.stage16b_validated
    assert d.stage16c_validated
    assert d.stage16d_validated
    assert d.stage16e_validated
    assert d.stage16f_validated
    assert d.all_stage16a_f_evidence_validated

    assert d.global_abelianization_established
    assert not d.local_witness_found_in_frozen_search
    assert d.stage16d_classification == "only_nonlocal_abelianization_witness_found_in_frozen_search"
    assert d.presented_local_compensator_success_count == d.presented_local_compensator_probe_count == 2592
    assert d.quotient_class_count == 4
    assert d.typed_public_quotient_count == 4
    assert d.control_count == d.rejected_control_count == 20
    assert d.cycle_opening_exhibited_depth == 2
    assert d.three_site_projection_one_step_l1


def test_stage17_candidate_pool_and_frozen_rubric_are_complete_and_bounded():
    scores = canonical_stage17_candidate_scores()
    assert len(scores) == len(STAGE17_CANDIDATE_POOL) == 7
    assert {item.selector_id for item in scores} == set(STAGE17_CANDIDATE_POOL)
    for item in scores:
        axes = (
            item.discriminating_power,
            item.prerequisite_readiness,
            item.locality_topology_specificity,
            item.confound_resistance,
            item.tractability,
        )
        assert all(0 <= value <= 3 for value in axes)
        assert item.total == sum(axes)
        assert 0 <= item.total <= 15
        assert item.rationale


def test_stage17_ranking_uses_frozen_tie_break_and_selects_completeness_audit():
    ranking = ranked_stage17_candidates()
    assert [item.total for item in ranking[:3]] == [15, 14, 13]
    assert ranking[0].selector_id == STAGE17_SELECTED_GATE
    assert ranking[0].selector_id == "admissible_basis_transformation_completeness_audit"
    assert ranking[1].selector_id == "path_cycle_tree_topology_comparison_family"
    assert ranking[2].selector_id == "larger_sparse_graph_locality_scaling_audit"
    assert ranking[0].total > ranking[1].total

    expected = sorted(
        ranking,
        key=lambda item: (
            -item.total,
            -item.discriminating_power,
            -item.prerequisite_readiness,
            item.selector_id,
        ),
    )
    assert list(ranking) == expected


def test_stage16g_criteria_48_49_and_selected_gate_statement_are_bounded():
    d = stage16g_diagnostics()
    assert d.synthesis_classification == STAGE16G_SELECTED_CLASSIFICATION
    assert d.selected_stage17_gate == STAGE17_SELECTED_GATE
    assert d.selected_stage17_score == 15
    assert d.runner_up_stage17_score == 14
    assert d.criteria_48_49_satisfied

    assert "broader admissible locality-preserving basis-transformation class" in STAGE17_SELECTED_GATE_STATEMENT
    assert "constructive local strongly commuting witness" in STAGE17_SELECTED_GATE_STATEMENT
    assert "bounded completeness/nonexistence certificate" in STAGE17_SELECTED_GATE_STATEMENT
    assert "without promoting search failure to a universal physical locality obstruction" in STAGE17_SELECTED_GATE_STATEMENT


def test_stage16g_summary_and_guards_do_not_promote_bounded_search_to_ontology():
    summary = stage16g_summary()
    assert summary["classification"] == STAGE16G_SELECTED_CLASSIFICATION
    assert summary["selected_stage17_gate"] == STAGE17_SELECTED_GATE
    assert summary["criteria_48_49_satisfied"] is True
    assert summary["bounded_result"] == STAGE16G_BOUNDED_RESULT
    assert summary["selected_gate_statement"] == STAGE17_SELECTED_GATE_STATEMENT

    required = {
        "nonlocal_only_in_declared_search != universal locality obstruction",
        "no L1 witness in frozen search != no L1 Abelianization exists",
        "global Abelianization != physical triviality",
        "cycle opening changes graph topology != proof that topology is ontic",
        "failure to Abelianize != ontological becoming",
        "future-measurement covariance != future actuality",
        "typed operational descent != ontological equivalence",
        "Stage 17 completeness audit selection != predicted locality obstruction",
        "repository validation != new scientific evidence",
    }
    assert required <= set(STAGE16G_GUARDS)
