from dataclasses import replace

import pytest

from t_search.stage11_synthesis import (
    SELECTED_STAGE12_GATE_LABEL,
    Stage11SynthesisChoice,
    evidence_snapshot,
    select_synthesis_choice,
    stage11g_summary,
    stage11g_synthesis,
    stage12_gate_candidates,
    unresolved_boundaries,
)


@pytest.fixture(scope="module")
def synthesis():
    return stage11g_synthesis()


@pytest.fixture(scope="module")
def snapshot():
    return evidence_snapshot()


def test_stage11g_selects_parametrized_covariant_from_full_stage11a_f_evidence(synthesis) -> None:
    assert synthesis.choice is Stage11SynthesisChoice.PARAMETRIZED_COVARIANT
    assert select_synthesis_choice() is Stage11SynthesisChoice.PARAMETRIZED_COVARIANT
    assert synthesis.top_level_candidate.startswith("T11_candidate=(O,P,R,V;Xi)")


def test_stage11g_choice_vocabulary_matches_frozen_protocol() -> None:
    assert {item.value for item in Stage11SynthesisChoice} == {
        "parametrized_covariant",
        "parametrized_partial",
        "parametrized_obstructed",
        "inconclusive",
    }


def test_stage11g_full_evidence_snapshot_closes_all_stage11a_f_layers(snapshot) -> None:
    assert snapshot.stage11a.criteria_11_16_satisfied
    assert snapshot.stage11b.criteria_17_23_satisfied
    assert snapshot.stage11c.criteria_24_31_satisfied
    assert snapshot.stage11d.criteria_32_38_satisfied
    assert snapshot.stage11e.criteria_39_43_satisfied
    assert snapshot.stage11f.criteria_44_47_satisfied


def test_stage11g_status_logic_separates_obstructed_partial_and_inconclusive(snapshot) -> None:
    obstructed = replace(
        snapshot,
        stage11a=replace(
            snapshot.stage11a,
            constraint_orbit_preserved=False,
            criteria_11_16_satisfied=False,
        ),
    )
    assert select_synthesis_choice(obstructed) is Stage11SynthesisChoice.PARAMETRIZED_OBSTRUCTED

    partial = replace(
        snapshot,
        stage11f=replace(snapshot.stage11f, criteria_44_47_satisfied=False),
    )
    assert select_synthesis_choice(partial) is Stage11SynthesisChoice.PARAMETRIZED_PARTIAL

    inconclusive = replace(
        snapshot,
        stage11a=replace(snapshot.stage11a, criteria_11_16_satisfied=False),
        stage11b=replace(snapshot.stage11b, criteria_17_23_satisfied=False),
        stage11c=replace(snapshot.stage11c, criteria_24_31_satisfied=False),
        stage11d=replace(snapshot.stage11d, criteria_32_38_satisfied=False),
        stage11e=replace(snapshot.stage11e, criteria_39_43_satisfied=False),
        stage11f=replace(snapshot.stage11f, criteria_44_47_satisfied=False),
    )
    assert select_synthesis_choice(inconclusive) is Stage11SynthesisChoice.INCONCLUSIVE


def test_stage11g_established_scope_integrates_relational_typed_measurement_square_and_ablation_layers(synthesis) -> None:
    scope = " ".join(synthesis.established_scope)
    assert "4 admissible external parameterizations" in scope
    assert "52 relational-observable" in scope
    assert "typed O/P/R/V/Xi" in scope
    assert "16 canonical outcome evaluations" in scope
    assert "1296 measurement/probability" in scope
    assert "7/7 false-positive controls" in scope


def test_stage11g_retains_typing_resources_without_promoting_them_to_metaphysics(synthesis) -> None:
    assert set(synthesis.retained_typing_resources) == {
        "physical event correspondence",
        "lapse/Jacobian transformation semantics",
        "continuation-class correspondence",
        "outcome correspondence",
        "measurement normalization semantics",
        "continuation-weight/class alignment",
        "separation of external parameterization identity from internal clock perspective",
    }
    derived = " ".join(synthesis.derived_or_reconstructible_roles)
    assert "reconstructed" in derived
    assert "without restoring typed identity" in derived
    assert "representation-dependent" in derived


def test_stage11g_project_questions_close_parametrization_gap_but_keep_ontology_guards(synthesis) -> None:
    answers = {item.question_id: item for item in synthesis.project_questions}
    assert answers["Q1"].evidence_class == "established_finite_model_result"
    assert "not general covariance" in answers["Q1"].boundary
    assert answers["Q2"].evidence_class == "established_finite_model_result"
    assert "not general covariance" in answers["Q2"].boundary
    assert answers["Q4"].evidence_class == "interpretation_guard"
    assert "ontological" in answers["Q4"].boundary
    assert answers["Q5"].evidence_class == "interpretation_guard"
    assert "ontological becoming" in answers["Q5"].boundary
    assert answers["Q7"].evidence_class == "untested_not_established"
    assert "not false" in answers["Q7"].boundary.lower()
    assert answers["Q8"].evidence_class == "evidence_selected_research_gate"
    assert "not general relativity" in answers["Q8"].boundary.lower()


def test_stage11g_unresolved_boundaries_remove_preferred_parameter_gap_but_keep_larger_gauge_and_gravity_claims_open() -> None:
    unresolved = unresolved_boundaries()
    assert "one_frozen_constraint_orbit_reparameterization_covariance => multi_orbit_constraint_generated_gauge_covariance" in unresolved
    assert "single_hamiltonian_constraint_precursor => nontrivial_constraint_algebra_or_refoliation_structure" in unresolved
    assert "finite_typed_parametrized_covariance => general_covariance" in unresolved
    assert "external_parameterization_independence => diffeomorphism_invariance" in unresolved
    assert "fixed_background_precursor => dynamical_metric_or_gravitational_clock_structure" in unresolved
    assert "absence_of_preferred_external_parameterization => absence_of_ontological_becoming" in unresolved


def test_stage11g_gate_ranking_uniquely_selects_multi_orbit_constraint_gauge_atlas(synthesis) -> None:
    gates = synthesis.stage12_candidates
    assert gates[0].gate_id == "multi_orbit_constraint_gauge_atlas"
    assert gates[0].label == SELECTED_STAGE12_GATE_LABEL
    assert gates[0].score == 10
    assert gates[0].score > gates[1].score
    assert synthesis.selected_stage12_gate == "multi_orbit_constraint_gauge_atlas"


def test_stage11g_gate_scores_follow_current_evidence(snapshot) -> None:
    scores = {item.gate_id: item.score for item in stage12_gate_candidates(snapshot)}
    assert scores == {
        "multi_orbit_constraint_gauge_atlas": 10,
        "richer_causal_order": 7,
        "nonideal_povm_clocks": 6,
        "gravitational_minisuperspace_extension": 5,
    }


def test_stage11g_does_not_jump_directly_to_general_relativity(synthesis) -> None:
    ids = [item.gate_id for item in synthesis.stage12_candidates]
    assert ids[0] == "multi_orbit_constraint_gauge_atlas"
    assert ids[-1] == "gravitational_minisuperspace_extension"
    gravity = next(item for item in synthesis.stage12_candidates if item.gate_id == "gravitational_minisuperspace_extension")
    assert "intentionally ranked below" in gravity.rationale
    assert "does not yet provide" in gravity.rationale


def test_stage11g_summary_closes_48_49_and_keeps_50_external() -> None:
    summary = stage11g_summary()
    criteria = summary["current_execution_criteria"]
    assert tuple(criteria.keys()) == ("48", "49", "50")
    assert "exactly one frozen Stage 11 status" in criteria["48"]
    assert "without presupposing general covariance" in criteria["49"]
    assert "external" in criteria["50"]
    guards = summary["guards"]
    assert "parametrized_covariant finite family != general covariance" in guards
    assert "one-orbit covariance != multi-orbit gauge covariance" in guards
    assert "constraint-generated gauge precursor != general relativity" in guards
    assert "absence of preferred external parameterization != absence of ontological becoming" in guards
