from dataclasses import replace

import pytest

from t_search.stage14_synthesis import (
    SELECTED_STAGE15_GATE_LABEL,
    Stage14SynthesisChoice,
    evidence_snapshot,
    select_synthesis_choice,
    stage14g_summary,
    stage14g_synthesis,
    stage15_gate_candidates,
    unresolved_boundaries,
)


@pytest.fixture(scope="module")
def synthesis():
    return stage14g_synthesis()


@pytest.fixture(scope="module")
def snapshot():
    return evidence_snapshot()


def test_stage14g_selects_scalar_obstructed_path_covariant_status(synthesis) -> None:
    assert synthesis.choice is Stage14SynthesisChoice.STRUCTURE_FUNCTION_PATH_COVARIANT_SCALAR_OBSTRUCTED
    assert select_synthesis_choice() is Stage14SynthesisChoice.STRUCTURE_FUNCTION_PATH_COVARIANT_SCALAR_OBSTRUCTED
    assert synthesis.top_level_candidate.startswith("T14_candidate=(O,P,R,V;Xi)")


def test_stage14g_choice_vocabulary_matches_frozen_protocol() -> None:
    assert {item.value for item in Stage14SynthesisChoice} == {
        "structure_function_path_covariant_scalar_obstructed",
        "structure_function_path_covariant_scalar_trivializable",
        "structure_function_path_partial",
        "structure_function_path_obstructed",
        "inconclusive",
    }


def test_stage14g_full_evidence_snapshot_closes_all_stage14a_f_layers(snapshot) -> None:
    assert snapshot.stage14a.criteria_11_17_satisfied
    assert snapshot.stage14b.criteria_18_24_satisfied
    assert snapshot.stage14c.criteria_25_31_satisfied
    assert snapshot.stage14d.criteria_32_38_satisfied
    assert snapshot.stage14e.criteria_39_43_satisfied
    assert snapshot.stage14f.criteria_44_47_satisfied


def test_stage14g_status_logic_distinguishes_scalar_trivializable_obstructed_partial_and_inconclusive(snapshot) -> None:
    scalar_trivializable = replace(
        snapshot,
        stage14d=replace(
            snapshot.stage14d,
            scalar_x_nonzero_obstructed_count=0,
            criteria_32_38_satisfied=False,
        ),
    )
    assert (
        select_synthesis_choice(scalar_trivializable)
        is Stage14SynthesisChoice.STRUCTURE_FUNCTION_PATH_COVARIANT_SCALAR_TRIVIALIZABLE
    )

    obstructed = replace(
        snapshot,
        stage14b=replace(
            snapshot.stage14b,
            all_positive_pairs_closed=False,
            criteria_18_24_satisfied=False,
        ),
    )
    assert select_synthesis_choice(obstructed) is Stage14SynthesisChoice.STRUCTURE_FUNCTION_PATH_OBSTRUCTED

    partial = replace(
        snapshot,
        stage14f=replace(snapshot.stage14f, criteria_44_47_satisfied=False),
    )
    assert select_synthesis_choice(partial) is Stage14SynthesisChoice.STRUCTURE_FUNCTION_PATH_PARTIAL

    inconclusive = replace(
        snapshot,
        stage14a=replace(snapshot.stage14a, criteria_11_17_satisfied=False),
        stage14b=replace(snapshot.stage14b, criteria_18_24_satisfied=False),
        stage14c=replace(snapshot.stage14c, criteria_25_31_satisfied=False),
        stage14d=replace(snapshot.stage14d, criteria_32_38_satisfied=False),
        stage14e=replace(snapshot.stage14e, criteria_39_43_satisfied=False),
        stage14f=replace(snapshot.stage14f, criteria_44_47_satisfied=False),
    )
    assert select_synthesis_choice(inconclusive) is Stage14SynthesisChoice.INCONCLUSIVE


def test_stage14g_established_scope_integrates_carrier_paths_relational_basis_operational_and_controls(synthesis) -> None:
    scope = " ".join(synthesis.established_scope)
    assert "108 sampled representatives" in scope
    assert "864/864" in scope
    assert "6/6 physical-orbit pair discrimination" in scope
    assert "4 quotient classes of size 27" in scope
    assert "23328" in scope
    assert "216/216 X!=0 diagonal scalar evaluations" in scope
    assert "216 triangular probes" in scope
    assert "864 typed path-descent checks" in scope
    assert "14/14" in scope


def test_stage14g_basis_pressure_result_keeps_scalar_obstruction_and_triangular_equivalence_separate(synthesis) -> None:
    result = " ".join(synthesis.basis_pressure_result)
    assert "diagonal scalar-rescaling obstruction" in result
    assert "triangular commuting-basis equivalence" in result
    assert "not established as quotient-level basis-independent physical content" in result


def test_stage14g_retains_typing_resources_without_promoting_path_or_basis_provenance(synthesis) -> None:
    retained = set(synthesis.retained_typing_resources)
    assert "physical-orbit identity and four-class quotient correspondence" in retained
    assert "three constraint-generator identities and structure-function provenance" in retained
    assert "representative, path-word, compensator, and basis provenance in Xi" in retained
    assert "separation of path word from physical temporal history" in retained
    assert "separation of constraint-basis presentation from quotient-level physical content" in retained


def test_stage14g_project_questions_close_finite_result_but_keep_hda_gr_and_ontology_open(synthesis) -> None:
    answers = {item.question_id: item for item in synthesis.project_questions}
    for question_id in ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6"):
        assert answers[question_id].evidence_class == "established_finite_model_result"
    assert "not a hypersurface-deformation algebra" in answers["Q1"].boundary
    assert "not refoliation invariance" in answers["Q2"].boundary
    assert "ontological becoming" in answers["Q3"].boundary
    assert "not universal non-Abelianizability" in answers["Q4"].boundary
    assert "not future actuality" in answers["Q5"].boundary
    assert answers["Q7"].evidence_class == "interpretation_guard"
    assert "No HDA/refoliation/GR or eternalism/becoming verdict" in answers["Q7"].boundary
    assert answers["Q8"].evidence_class == "evidence_selected_research_gate"
    assert "without assuming GR" in answers["Q8"].boundary


def test_stage14g_unresolved_boundaries_keep_locality_hda_refoliation_gravity_and_ontology_open() -> None:
    unresolved = unresolved_boundaries()
    assert "finite_phase_space_structure_function_path_covariance => refoliation_invariance" in unresolved
    assert "finite_first_class_structure_function_algebra => hypersurface_deformation_algebra" in unresolved
    assert "triangular_Abelianization_on_regular_finite_carrier => universal_basis_trivializability" in unresolved
    assert "finite_dimensional_constraint_carrier => spatially_local_smeared_constraint_algebra" in unresolved
    assert "spatially_indexed_constraint_precursor => general_relativity" in unresolved
    assert "Dirac_invariant_data_plus_relational_change => eternalism_or_ontological_becoming" in unresolved


def test_stage14g_gate_ranking_uniquely_selects_spatially_indexed_constraint_precursor(synthesis) -> None:
    gates = synthesis.stage15_candidates
    assert gates[0].gate_id == "spatially_indexed_constraint_algebra_precursor"
    assert gates[0].label == SELECTED_STAGE15_GATE_LABEL
    assert gates[0].score == 13
    assert gates[0].score > gates[1].score
    assert synthesis.selected_stage15_gate == "spatially_indexed_constraint_algebra_precursor"


def test_stage14g_gate_scores_follow_current_evidence(snapshot) -> None:
    scores = {item.gate_id: item.score for item in stage15_gate_candidates(snapshot)}
    assert scores == {
        "spatially_indexed_constraint_algebra_precursor": 13,
        "admissible_basis_transformation_audit": 10,
        "gravitational_minisuperspace_extension": 8,
        "richer_causal_order": 7,
        "nonideal_povm_clocks": 7,
    }


def test_stage14g_selected_gate_targets_missing_locality_before_gravity(synthesis) -> None:
    selected = synthesis.stage15_candidates[0]
    signals = " ".join(selected.pressure_signals)
    assert "locality/smearing" in signals
    assert "216 X!=0 evaluations" in signals
    assert "triangular commuting basis" in signals
    gravity = next(item for item in synthesis.stage15_candidates if item.gate_id == "gravitational_minisuperspace_extension")
    assert gravity.score < selected.score
    assert "minisuperspace suppresses spatial dependence" in gravity.rationale
    assert "confound" in gravity.rationale


def test_stage14g_summary_closes_48_49_in_source_and_keeps_50_external() -> None:
    summary = stage14g_summary()
    criteria = summary["current_execution_criteria"]
    assert tuple(criteria.keys()) == ("48", "49", "50")
    assert "exactly one frozen Stage 14 status" in criteria["48"]
    assert "without presupposing GR, refoliation invariance" in criteria["49"]
    assert "external" in criteria["50"].lower()
    assert summary["choice"] == "structure_function_path_covariant_scalar_obstructed"
    assert summary["selected_stage15_gate"] == "spatially_indexed_constraint_algebra_precursor"
    assert summary["bounded_result"].endswith("structure_function_path_covariant_scalar_obstructed")
    guards = summary["guards"]
    assert "structure_function_path_covariant_scalar_obstructed finite family != refoliation invariance" in guards
    assert "finite first-class structure-function algebra != hypersurface-deformation algebra" in guards
    assert "diagonal scalar-rescaling obstruction != fundamental physical non-Abelianity" in guards
    assert "triangular basis equivalence != universal basis trivializability" in guards
    assert "spatially indexed constraint precursor != general relativity" in guards
