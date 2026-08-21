import pytest

from t_search.stage8_exit_audit import pre_merge_exit_criteria, stage8_pre_merge_audit
from t_search.stage8_synthesis import (
    Stage8SynthesisChoice,
    answer_project_questions,
    layer_refinements,
    select_synthesis_choice,
    stage8g_summary,
    stage8g_synthesis,
    stage9_gate_candidates,
    unresolved_implications,
)


SYNTHESIS = stage8g_synthesis()
GATES = stage9_gate_candidates()
AUDIT = stage8_pre_merge_audit()


def test_stage8g_selects_refined_layered_candidate_from_executable_evidence():
    assert select_synthesis_choice() is Stage8SynthesisChoice.REFINED_LAYERED
    assert SYNTHESIS.choice is Stage8SynthesisChoice.REFINED_LAYERED
    assert SYNTHESIS.top_level_candidate.startswith("T8_candidate=(O,P,R,V;Xi)")


def test_stage8g_refines_r_and_v_internally_without_promoting_components_to_metaphysical_primitives():
    refinements = {item.layer_id: item for item in layer_refinements()}
    assert refinements["R"].components == ("R_content", "R_direction", "R_access")
    assert refinements["V"].components == ("V_extension", "V_semantics", "V_weights")
    assert "different" in refinements["R"].interpretation
    assert "different" in refinements["V"].interpretation


def test_stage8g_keeps_explicit_p_edges_derived_but_xi_correspondence_explicit():
    assert any("explicit P-V edge matrices" in item for item in SYNTHESIS.derived_representation_roles)
    assert any("Xi_PV" in item and "correspondence" in item for item in SYNTHESIS.compatibility_links)


def test_stage8g_project_questions_preserve_established_vs_not_established_boundary():
    answers = {item.question_id: item for item in answer_project_questions()}
    assert answers["Q2"].evidence_class == "established_finite_model_result"
    assert "does not establish" in answers["Q2"].boundary or "not a universal" in answers["Q2"].boundary
    assert answers["Q6"].evidence_class == "untested_not_established"
    assert "not a proof" in answers["Q6"].boundary
    assert answers["Q7"].evidence_class == "candidate_structural_interpretation"


def test_stage8g_unresolved_implications_keep_directional_r_measurement_and_metaphysics_open():
    unresolved = unresolved_implications()
    assert "directional_record_structure <=> nontrivial_V_structure" in unresolved
    assert "full_Stage8C_measurement_family_covariance" in unresolved
    assert "record_defined_direction => ontological_future_openness" in unresolved
    assert "refined_O_P_R_V_Xi_candidate => fundamental_or_unique_time_ontology" in unresolved


def test_stage8g_gate_ranking_uniquely_selects_directional_record_potentiality_before_gravity():
    assert GATES[0].gate_id == "directional_record_potentiality"
    assert GATES[0].score > GATES[1].score
    gravity = next(item for item in GATES if item.gate_id == "parametrized_covariance_precursor")
    assert GATES[0].score > gravity.score
    assert "directional record" in GATES[0].label.lower()


def test_stage8g_gate_ranking_retains_measurement_order_clock_and_covariance_alternatives():
    ids = {item.gate_id for item in GATES}
    assert ids == {
        "directional_record_potentiality",
        "full_measurement_covariance",
        "richer_causal_order",
        "nonideal_povm_clocks",
        "parametrized_covariance_precursor",
    }


def test_stage8g_pre_merge_exit_audit_recomputes_criteria_11_through_49_without_claiming_external_50():
    criteria = pre_merge_exit_criteria()
    assert tuple(criteria) == tuple(range(11, 50))
    assert all(criteria.values())
    assert AUDIT.passed == 39
    assert AUDIT.total == 39
    assert AUDIT.all_passed is True
    payload = AUDIT.as_dict()
    assert payload["criterion_50"] == "external final CI and merge-readiness review"


def test_stage8g_summary_allocates_48_49_to_synthesis_and_50_to_external_final_validation():
    summary = stage8g_summary()
    criteria = summary["current_execution_criteria"]
    assert tuple(criteria.keys()) == ("48", "49", "50")
    assert "synthesis" in criteria["48"]
    assert "Stage 9" in criteria["49"]
    assert "external" in criteria["50"]
    guards = summary["guards"]
    assert "refined layered candidate != fundamental ontology" in guards
    assert "not_established != false" in guards
