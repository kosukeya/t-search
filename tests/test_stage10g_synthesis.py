from t_search.stage10_synthesis import (
    SELECTED_STAGE11_GATE_LABEL,
    Stage10SynthesisChoice,
    answer_project_questions,
    select_synthesis_choice,
    stage10g_summary,
    stage10g_synthesis,
    stage11_gate_candidates,
    unresolved_boundaries,
)


SYNTHESIS = stage10g_synthesis()
GATES = stage11_gate_candidates()


def test_stage10g_selects_measurement_covariant_from_stage10a_f_evidence():
    assert select_synthesis_choice() is Stage10SynthesisChoice.MEASUREMENT_COVARIANT
    assert SYNTHESIS.choice is Stage10SynthesisChoice.MEASUREMENT_COVARIANT
    assert SYNTHESIS.top_level_candidate.startswith("T10_candidate=(O,P,R,V;Xi)")


def test_stage10g_choice_vocabulary_matches_frozen_protocol():
    assert {item.value for item in Stage10SynthesisChoice} == {
        "measurement_covariant",
        "measurement_partial",
        "measurement_obstructed",
        "inconclusive",
    }


def test_stage10g_established_scope_contains_measurement_probability_modal_and_ablation_layers():
    scope = " ".join(SYNTHESIS.established_scope)
    assert "108-transport" in scope
    assert "196 tomography-complete probes" in scope
    assert "evidence-update covariance" in scope
    assert "wrong typing" in scope


def test_stage10g_retains_typing_resources_without_promoting_them_to_metaphysics():
    assert set(SYNTHESIS.retained_typing_resources) == {
        "event correspondence",
        "continuation-class correspondence",
        "outcome correspondence",
        "normalization semantics",
        "continuation-weight/class alignment",
    }
    assert any(
        "without preservation of typed operational identity" in item
        for item in SYNTHESIS.derived_or_reconstructible_roles
    )


def test_stage10g_project_questions_close_measurement_gap_but_keep_modal_and_becoming_guards():
    answers = {item.question_id: item for item in answer_project_questions()}
    assert answers["Q1"].evidence_class == "established_finite_model_result"
    assert "not general covariance" in answers["Q1"].boundary
    assert answers["Q2"].evidence_class == "established_finite_model_result"
    assert "does not decide" in answers["Q2"].boundary
    assert answers["Q4"].evidence_class == "interpretation_guard"
    assert "ontological" in answers["Q4"].boundary
    assert answers["Q5"].evidence_class == "interpretation_guard"
    assert "ontological becoming" in answers["Q5"].boundary
    assert answers["Q7"].evidence_class == "untested_not_established"
    assert "not false" in answers["Q7"].boundary.lower()
    assert answers["Q8"].evidence_class == "evidence_selected_research_gate"


def test_stage10g_unresolved_boundaries_remove_completed_measurement_gap_and_keep_larger_claims_open():
    unresolved = unresolved_boundaries()
    assert "full_Stage9C_future_measurement_family_covariance" not in unresolved
    assert "finite_typed_clock_measurement_covariance => general_covariance" in unresolved
    assert "minimal_three_event_O => robustness_under_richer_causal_order" in unresolved
    assert "ideal_projective_clock_family => nonideal_POVM_clock_covariance" in unresolved
    assert "perspective_invariant_future_probabilities => eternalism" in unresolved
    assert "perspective_invariant_future_probabilities => absence_of_ontological_becoming" in unresolved
    assert "refined_O_P_R_V_Xi_candidate => fundamental_or_unique_time_ontology" in unresolved


def test_stage10g_gate_ranking_uniquely_selects_parametrized_covariance_precursor():
    assert GATES[0].gate_id == "parametrized_covariance_precursor"
    assert GATES[0].label == SELECTED_STAGE11_GATE_LABEL
    assert GATES[0].score == 9
    assert GATES[0].score > GATES[1].score


def test_stage10g_gate_scores_follow_current_evidence():
    scores = {item.gate_id: item.score for item in GATES}
    assert scores == {
        "parametrized_covariance_precursor": 9,
        "richer_causal_order": 7,
        "nonideal_povm_clocks": 6,
    }
    assert [item.gate_id for item in GATES] == [
        "parametrized_covariance_precursor",
        "richer_causal_order",
        "nonideal_povm_clocks",
    ]


def test_stage10g_does_not_reselect_completed_stage10_measurement_gate():
    ids = {item.gate_id for item in GATES}
    assert "full_measurement_covariance" not in ids
    assert ids == {
        "parametrized_covariance_precursor",
        "richer_causal_order",
        "nonideal_povm_clocks",
    }


def test_stage10g_summary_closes_48_49_and_keeps_50_external():
    summary = stage10g_summary()
    criteria = summary["current_execution_criteria"]
    assert tuple(criteria.keys()) == ("48", "49", "50")
    assert "Stage 10" in criteria["48"]
    assert "Stage 11" in criteria["49"]
    assert "external" in criteria["50"]
    guards = summary["guards"]
    assert "measurement_covariant finite family != general covariance" in guards
    assert "future-measurement covariance != future actuality" in guards
    assert "measurement covariance != refutation of ontological becoming" in guards
    assert "parametrized covariance precursor != general relativity" in guards
