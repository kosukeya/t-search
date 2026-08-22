from t_search.stage9_synthesis import (
    SELECTED_STAGE10_GATE_LABEL,
    Stage9SynthesisChoice,
    answer_project_questions,
    layer_refinements,
    select_synthesis_choice,
    stage10_gate_candidates,
    stage9g_summary,
    stage9g_synthesis,
    unresolved_implications,
)


SYNTHESIS = stage9g_synthesis()
GATES = stage10_gate_candidates()


def test_stage9g_selects_refined_layered_candidate_from_stage9a_f_evidence():
    assert select_synthesis_choice() is Stage9SynthesisChoice.REFINED_LAYERED
    assert SYNTHESIS.choice is Stage9SynthesisChoice.REFINED_LAYERED
    assert SYNTHESIS.top_level_candidate.startswith("T9_candidate=(O,P,R,V;Xi)")


def test_stage9g_keeps_r_and_v_internal_refinements_after_bidirectional_ablations():
    refinements = {item.layer_id: item for item in layer_refinements()}
    assert refinements["R"].components == ("R_content", "R_direction", "R_access")
    assert refinements["V"].components == ("V_extension", "V_semantics", "V_weights")
    assert "different" in refinements["R"].interpretation
    assert "different" in refinements["V"].interpretation


def test_stage9g_retains_typed_xi_but_does_not_invent_a_direct_rv_value_law():
    assert any("Xi_event_class_observable" in item for item in SYNTHESIS.compatibility_links)
    assert "direct Xi_RV value law:not_established" in SYNTHESIS.compatibility_links
    assert not any("direct Xi_RV value law:established" in item for item in SYNTHESIS.compatibility_links)


def test_stage9g_keeps_explicit_p_edges_derived_without_collapsing_p_layer():
    assert any("explicit P edge matrices" in item for item in SYNTHESIS.derived_representation_roles)
    unresolved = unresolved_implications()
    assert "P_edge_reconstructibility => P_layer_redundant" in unresolved


def test_stage9g_project_questions_separate_finite_results_interpretation_and_open_boundary():
    answers = {item.question_id: item for item in answer_project_questions()}
    assert answers["Q2"].evidence_class == "established_finite_model_result"
    assert "universal R-V independence theorem" in answers["Q2"].boundary
    assert answers["Q5"].evidence_class == "candidate_structural_interpretation"
    assert "not proof" in answers["Q5"].boundary.lower()
    assert answers["Q7"].evidence_class == "untested_not_established"
    assert "not false" in answers["Q7"].boundary.lower()
    assert answers["Q8"].evidence_class == "candidate_structural_interpretation"


def test_stage9g_unresolved_implications_keep_measurement_covariance_and_metaphysics_open():
    unresolved = unresolved_implications()
    assert "full_Stage9C_future_measurement_family_covariance" in unresolved
    assert "finite_family_R_direction_V_separation => universal_R_V_independence" in unresolved
    assert "record_defined_direction => ontological_future_openness" in unresolved
    assert "finite_clock_covariance => general_covariance" in unresolved
    assert "refined_O_P_R_V_Xi_candidate => fundamental_or_unique_time_ontology" in unresolved


def test_stage9g_gate_ranking_uniquely_selects_full_measurement_covariance():
    assert GATES[0].gate_id == "full_measurement_covariance"
    assert GATES[0].label == SELECTED_STAGE10_GATE_LABEL
    assert GATES[0].score > GATES[1].score
    assert GATES[0].score == 9


def test_stage9g_gate_ranking_places_measurement_before_richer_order_and_covariance():
    scores = {item.gate_id: item.score for item in GATES}
    assert scores == {
        "full_measurement_covariance": 9,
        "richer_causal_order": 6,
        "parametrized_covariance_precursor": 5,
        "nonideal_povm_clocks": 4,
    }
    assert [item.gate_id for item in GATES] == [
        "full_measurement_covariance",
        "richer_causal_order",
        "parametrized_covariance_precursor",
        "nonideal_povm_clocks",
    ]


def test_stage9g_does_not_keep_completed_directional_record_gate_as_future_candidate():
    ids = {item.gate_id for item in GATES}
    assert "directional_record_potentiality" not in ids
    assert ids == {
        "full_measurement_covariance",
        "richer_causal_order",
        "parametrized_covariance_precursor",
        "nonideal_povm_clocks",
    }


def test_stage9g_summary_allocates_48_49_and_keeps_50_external():
    summary = stage9g_summary()
    criteria = summary["current_execution_criteria"]
    assert tuple(criteria.keys()) == ("48", "49", "50")
    assert "synthesis" in criteria["48"]
    assert "Stage 10" in criteria["49"]
    assert "external" in criteria["50"]
    guards = summary["guards"]
    assert "refined layered candidate != fundamental ontology" in guards
    assert "finite-family bidirectional countermodels != universal R-V independence theorem" in guards
    assert "full Stage 9C future-measurement covariance remains not_established" in guards
    assert "finite clock covariance != general covariance" in guards
