from dataclasses import replace

from t_search.stage15_synthesis import (
    SELECTED_STAGE16_GATE_ID,
    SELECTED_STAGE16_GATE_LABEL,
    Stage15SynthesisChoice,
    evidence_snapshot,
    select_synthesis_choice,
    stage15g_summary,
    stage15g_synthesis,
    stage16_gate_candidates,
)


def test_stage15g_criterion_48_selects_exact_frozen_synthesis_status_from_validated_a_to_f_evidence():
    snapshot = evidence_snapshot()
    assert snapshot.stage15a.criteria_11_17_satisfied
    assert snapshot.stage15b.criteria_18_24_satisfied
    assert snapshot.stage15c.criteria_25_31_satisfied
    assert snapshot.stage15d.criteria_32_38_satisfied
    assert snapshot.stage15e.criteria_39_43_satisfied
    assert snapshot.stage15f.criteria_44_47_satisfied

    assert select_synthesis_choice(snapshot) == (
        Stage15SynthesisChoice.SPATIAL_LOCAL_PATH_COVARIANT_LOCAL_ABELIANIZABLE
    )
    assert stage15g_synthesis().choice.value == (
        "spatial_local_path_covariant_local_abelianizable"
    )


def test_stage15g_synthesis_enum_matches_the_frozen_protocol_vocabulary_exactly():
    assert {item.value for item in Stage15SynthesisChoice} == {
        "spatial_local_path_covariant_local_abelianizable",
        "spatial_local_path_covariant_locality_obstructed",
        "spatial_local_path_covariant_basis_inconclusive",
        "spatial_local_path_partial",
        "spatial_local_path_obstructed",
        "inconclusive",
    }


def test_stage15g_basis_result_records_local_abelianization_without_promoting_universal_triviality():
    synthesis = stage15g_synthesis()
    assert any("does not protect noncommutativity" in item for item in synthesis.basis_pressure_result)
    assert any("terminal C2=K2" in item for item in synthesis.basis_pressure_result)
    assert any("Lfinite depth 2" in item for item in synthesis.basis_pressure_result)
    assert any("universal local Abelianizability is not" in item for item in synthesis.basis_pressure_result)


def test_stage15g_criterion_49_ranks_stage16_gates_and_selects_four_site_closed_cycle():
    candidates = stage16_gate_candidates()
    assert len(candidates) == 5
    assert [item.score for item in candidates] == [15, 11, 9, 8, 6]
    assert candidates[0].gate_id == SELECTED_STAGE16_GATE_ID
    assert candidates[0].label == SELECTED_STAGE16_GATE_LABEL
    assert "four-site closed-cycle" in candidates[0].label
    assert "no terminal seed generator" in candidates[0].label
    assert "one-step L1 or finite-depth" in candidates[0].label
    assert "without assuming general relativity or refoliation invariance" in candidates[0].label


def test_stage15g_selected_gate_is_more_discriminating_than_repeating_open_chain_or_jumping_to_minisuperspace():
    candidates = {item.gate_id: item for item in stage16_gate_candidates()}
    selected = candidates[SELECTED_STAGE16_GATE_ID]
    assert selected.score > candidates["larger_sparse_graph_locality_scaling_audit"].score
    assert selected.score > candidates["admissible_basis_transformation_completeness_audit"].score
    assert selected.score > candidates["gravitational_minisuperspace_extension"].score
    assert any("terminal C2=K2" in signal for signal in selected.pressure_signals)
    assert any("four-cycle keeps N1 locality nontrivial" in signal for signal in selected.pressure_signals)


def test_stage15g_counterfactual_basis_inconclusive_branch_does_not_mislabel_local_abelianization():
    snapshot = evidence_snapshot()
    altered_d = replace(
        snapshot.stage15d,
        local_abelianization_established=False,
        classification="basis_audit_inconclusive",
    )
    altered = replace(snapshot, stage15d=altered_d)
    assert select_synthesis_choice(altered) == (
        Stage15SynthesisChoice.SPATIAL_LOCAL_PATH_COVARIANT_BASIS_INCONCLUSIVE
    )


def test_stage15g_project_answers_and_boundaries_keep_metaphysical_and_physical_guards_explicit():
    synthesis = stage15g_synthesis()
    assert len(synthesis.project_questions) == 8
    q7 = next(item for item in synthesis.project_questions if item.question_id == "Q7")
    assert "No." in q7.answer
    assert "eternalism" in q7.question
    assert "becoming" in q7.question
    assert "local Abelianizability != physical triviality" in q7.boundary

    boundaries = set(synthesis.unresolved_boundaries)
    for boundary in (
        "one_step_L1_Abelianization_on_open_three_site_chain => universal_local_Abelianizability",
        "finite_graph_locality => continuum_or_relativistic_locality",
        "compensated_local_smeared_paths => refoliation_invariance",
        "Dirac_invariant_data_plus_relational_change => eternalism_or_ontological_becoming",
        "future_measurement_covariance => future_actuality",
    ):
        assert boundary in boundaries


def test_stage15g_closes_criteria_48_and_49_but_not_final_regression_criterion_50():
    synthesis = stage15g_synthesis()
    assert synthesis.criteria_48_49_satisfied
    summary = stage15g_summary()
    assert summary["criteria_48_49_satisfied"]
    assert summary["selected_stage16_gate"] == SELECTED_STAGE16_GATE_LABEL
