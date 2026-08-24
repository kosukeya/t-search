from dataclasses import replace

import pytest

from t_search.stage13_synthesis import (
    SELECTED_STAGE14_GATE_LABEL,
    Stage13SynthesisChoice,
    evidence_snapshot,
    select_synthesis_choice,
    stage13g_summary,
    stage13g_synthesis,
    stage14_gate_candidates,
    unresolved_boundaries,
)


@pytest.fixture(scope="module")
def synthesis():
    return stage13g_synthesis()


@pytest.fixture(scope="module")
def snapshot():
    return evidence_snapshot()


def test_stage13g_selects_multi_constraint_path_covariant_from_full_stage13a_f_evidence(synthesis) -> None:
    assert synthesis.choice is Stage13SynthesisChoice.MULTI_CONSTRAINT_PATH_COVARIANT
    assert select_synthesis_choice() is Stage13SynthesisChoice.MULTI_CONSTRAINT_PATH_COVARIANT
    assert synthesis.top_level_candidate.startswith("T13_candidate=(O,P,R,V;Xi)")


def test_stage13g_choice_vocabulary_matches_frozen_protocol() -> None:
    assert {item.value for item in Stage13SynthesisChoice} == {
        "multi_constraint_path_covariant",
        "multi_constraint_path_partial",
        "multi_constraint_path_obstructed",
        "inconclusive",
    }


def test_stage13g_full_evidence_snapshot_closes_all_stage13a_f_layers(snapshot) -> None:
    assert snapshot.stage13a.criteria_11_16_satisfied
    assert snapshot.stage13b.criteria_17_23_satisfied
    assert snapshot.stage13c.criteria_24_31_satisfied
    assert snapshot.stage13d.criteria_32_38_satisfied
    assert snapshot.stage13e.criteria_39_43_satisfied
    assert snapshot.stage13f.criteria_44_47_satisfied


def test_stage13g_status_logic_separates_obstructed_partial_and_inconclusive(snapshot) -> None:
    obstructed = replace(
        snapshot,
        stage13b=replace(
            snapshot.stage13b,
            compensated_closure_count=snapshot.stage13b.mixed_pair_count - 1,
            criteria_17_23_satisfied=False,
        ),
    )
    assert select_synthesis_choice(obstructed) is Stage13SynthesisChoice.MULTI_CONSTRAINT_PATH_OBSTRUCTED

    partial = replace(
        snapshot,
        stage13f=replace(snapshot.stage13f, criteria_44_47_satisfied=False),
    )
    assert select_synthesis_choice(partial) is Stage13SynthesisChoice.MULTI_CONSTRAINT_PATH_PARTIAL

    inconclusive = replace(
        snapshot,
        stage13a=replace(snapshot.stage13a, criteria_11_16_satisfied=False),
        stage13b=replace(snapshot.stage13b, criteria_17_23_satisfied=False),
        stage13c=replace(snapshot.stage13c, criteria_24_31_satisfied=False),
        stage13d=replace(snapshot.stage13d, criteria_32_38_satisfied=False),
        stage13e=replace(snapshot.stage13e, criteria_39_43_satisfied=False),
        stage13f=replace(snapshot.stage13f, criteria_44_47_satisfied=False),
    )
    assert select_synthesis_choice(inconclusive) is Stage13SynthesisChoice.INCONCLUSIVE


def test_stage13g_established_scope_integrates_paths_quotient_measurement_basis_and_controls(synthesis) -> None:
    scope = " ".join(synthesis.established_scope)
    assert "4 physical orbits" in scope
    assert "36 sampled representatives" in scope
    assert "144/144 exact compensated mixed-path closures" in scope
    assert "6/6 distinct orbit-pair discrimination" in scope
    assert "4 typed quotient classes of size 9" in scope
    assert "144 compensated path comparisons" in scope
    assert "36/36 basis checks" in scope
    assert "144/144 mixed-path closures" in scope
    assert "6/6 rejected controls" in scope


def test_stage13g_retains_typing_resources_without_promoting_them_to_metaphysics(synthesis) -> None:
    assert set(synthesis.retained_typing_resources) == {
        "physical-orbit identity and quotient-class correspondence",
        "constraint-generator identity and constraint-basis provenance",
        "gauge representative and path-word/compensator provenance",
        "physical event and two-clock correspondence",
        "continuation-class and outcome correspondence",
        "measurement normalization semantics",
        "separation of path word from physical temporal history",
        "separation of constraint-generated gauge flow from modal continuation",
    }
    derived = " ".join(synthesis.derived_or_reconstructible_roles)
    assert "numerically reconstructible" in derived
    assert "typed operational provenance remains lost" in derived
    assert "equivalent commuting presentation" in derived
    assert "representation-dependent" in derived


def test_stage13g_project_questions_close_path_covariance_but_keep_refoliation_and_ontology_guards(synthesis) -> None:
    answers = {item.question_id: item for item in synthesis.project_questions}
    for question_id in ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6"):
        assert answers[question_id].evidence_class == "established_finite_model_result"
    assert "not refoliation invariance" in answers["Q1"].boundary
    assert "ontological becoming" in answers["Q2"].boundary
    assert "not general covariance" in answers["Q3"].boundary
    assert "not future actuality" in answers["Q4"].boundary
    assert "not fundamental physical non-Abelianity" in answers["Q5"].boundary
    assert answers["Q7"].evidence_class == "interpretation_guard"
    assert "No refoliation/GR or eternalism/becoming verdict" in answers["Q7"].boundary
    assert answers["Q8"].evidence_class == "evidence_selected_research_gate"
    assert "not an assumption of GR" in answers["Q8"].boundary


def test_stage13g_unresolved_boundaries_keep_structure_functions_refoliation_gravity_and_ontology_open() -> None:
    unresolved = unresolved_boundaries()
    assert "basis_trivializable_noncommuting_presentation => phase_space_dependent_structure_function_algebra" in unresolved
    assert "finite_multi_constraint_path_covariance => refoliation_invariance" in unresolved
    assert "finite_first_class_constraint_algebra => hypersurface_deformation_algebra" in unresolved
    assert "six_dimensional_toy_phase_space => dynamical_gravitational_field_degrees_of_freedom" in unresolved
    assert "Dirac_invariant_data_plus_relational_change => eternalism_or_ontological_becoming" in unresolved


def test_stage13g_gate_ranking_uniquely_selects_phase_space_structure_function_precursor(synthesis) -> None:
    gates = synthesis.stage14_candidates
    assert gates[0].gate_id == "phase_space_structure_function_precursor"
    assert gates[0].label == SELECTED_STAGE14_GATE_LABEL
    assert gates[0].score == 12
    assert gates[0].score > gates[1].score
    assert synthesis.selected_stage14_gate == "phase_space_structure_function_precursor"


def test_stage13g_gate_scores_follow_current_evidence(snapshot) -> None:
    scores = {item.gate_id: item.score for item in stage14_gate_candidates(snapshot)}
    assert scores == {
        "phase_space_structure_function_precursor": 12,
        "gravitational_minisuperspace_extension": 8,
        "richer_causal_order": 8,
        "nonideal_povm_clocks": 7,
    }


def test_stage13g_selected_gate_targets_stage13f_basis_trivialization_before_gravity(synthesis) -> None:
    selected = synthesis.stage14_candidates[0]
    signals = " ".join(selected.pressure_signals)
    assert "basis-trivialization" in signals
    assert "36/36 basis-equivalence checks" in signals
    assert "K_X_bad anomaly control" in signals
    gravity = next(item for item in synthesis.stage14_candidates if item.gate_id == "gravitational_minisuperspace_extension")
    assert gravity.score < selected.score
    assert "confound algebraic structure-function effects with gravitational dynamics" in gravity.rationale


def test_stage13g_summary_closes_48_49_in_source_and_keeps_50_external() -> None:
    summary = stage13g_summary()
    criteria = summary["current_execution_criteria"]
    assert tuple(criteria.keys()) == ("48", "49", "50")
    assert "exactly one frozen Stage 13 status" in criteria["48"]
    assert "without presupposing GR, refoliation invariance, or a hypersurface-deformation algebra" in criteria["49"]
    assert "external" in criteria["50"].lower()
    assert summary["choice"] == "multi_constraint_path_covariant"
    assert summary["selected_stage14_gate"] == "phase_space_structure_function_precursor"
    guards = summary["guards"]
    assert "multi_constraint_path_covariant finite family != refoliation invariance" in guards
    assert "finite first-class constraint algebra != hypersurface-deformation algebra" in guards
    assert "constraint-basis equivalence != universal basis trivializability" in guards
    assert "structure-function precursor != general relativity" in guards
    assert "Dirac-invariant data + relational change != proof of eternalism" in guards
