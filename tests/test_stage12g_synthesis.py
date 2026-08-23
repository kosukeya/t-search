from dataclasses import replace

import pytest

from t_search.stage12_synthesis import (
    SELECTED_STAGE13_GATE_LABEL,
    Stage12SynthesisChoice,
    evidence_snapshot,
    select_synthesis_choice,
    stage12g_summary,
    stage12g_synthesis,
    stage13_gate_candidates,
    unresolved_boundaries,
)


@pytest.fixture(scope="module")
def synthesis():
    return stage12g_synthesis()


@pytest.fixture(scope="module")
def snapshot():
    return evidence_snapshot()


def test_stage12g_selects_multi_orbit_gauge_covariant_from_full_stage12a_f_evidence(synthesis) -> None:
    assert synthesis.choice is Stage12SynthesisChoice.MULTI_ORBIT_GAUGE_COVARIANT
    assert select_synthesis_choice() is Stage12SynthesisChoice.MULTI_ORBIT_GAUGE_COVARIANT
    assert synthesis.top_level_candidate.startswith("T12_candidate=(O,P,R,V;Xi)")


def test_stage12g_choice_vocabulary_matches_frozen_protocol() -> None:
    assert {item.value for item in Stage12SynthesisChoice} == {
        "multi_orbit_gauge_covariant",
        "multi_orbit_gauge_partial",
        "multi_orbit_gauge_obstructed",
        "inconclusive",
    }


def test_stage12g_full_evidence_snapshot_closes_all_stage12a_f_layers(snapshot) -> None:
    assert snapshot.stage12a.criteria_11_16_satisfied
    assert snapshot.stage12b.criteria_17_23_satisfied
    assert snapshot.stage12c.criteria_24_31_satisfied
    assert snapshot.stage12d.criteria_32_38_satisfied
    assert snapshot.stage12e.criteria_39_43_satisfied
    assert snapshot.stage12f.criteria_44_47_satisfied


def test_stage12g_status_logic_separates_obstructed_partial_and_inconclusive(snapshot) -> None:
    obstructed = replace(
        snapshot,
        stage12c=replace(
            snapshot.stage12c,
            quotient_partition_exact=False,
            criteria_24_31_satisfied=False,
        ),
    )
    assert select_synthesis_choice(obstructed) is Stage12SynthesisChoice.MULTI_ORBIT_GAUGE_OBSTRUCTED

    partial = replace(
        snapshot,
        stage12f=replace(snapshot.stage12f, criteria_44_47_satisfied=False),
    )
    assert select_synthesis_choice(partial) is Stage12SynthesisChoice.MULTI_ORBIT_GAUGE_PARTIAL

    inconclusive = replace(
        snapshot,
        stage12a=replace(snapshot.stage12a, criteria_11_16_satisfied=False),
        stage12b=replace(snapshot.stage12b, criteria_17_23_satisfied=False),
        stage12c=replace(snapshot.stage12c, criteria_24_31_satisfied=False),
        stage12d=replace(snapshot.stage12d, criteria_32_38_satisfied=False),
        stage12e=replace(snapshot.stage12e, criteria_39_43_satisfied=False),
        stage12f=replace(snapshot.stage12f, criteria_44_47_satisfied=False),
    )
    assert select_synthesis_choice(inconclusive) is Stage12SynthesisChoice.INCONCLUSIVE


def test_stage12g_established_scope_integrates_orbits_quotient_measurement_compatibility_and_controls(synthesis) -> None:
    scope = " ".join(synthesis.established_scope)
    assert "4 canonical physical orbits" in scope
    assert "20 sampled gauge representatives" in scope
    assert "100-arrow" in scope
    assert "4 quotient classes" in scope
    assert "4 orbit-sensitive signatures" in scope
    assert "C x Phi" in scope
    assert "27/27 rejected false-positive controls" in scope


def test_stage12g_retains_typing_resources_without_promoting_them_to_metaphysics(synthesis) -> None:
    assert set(synthesis.retained_typing_resources) == {
        "physical-orbit identity and quotient-class correspondence",
        "constraint-generated gauge representative and Phi provenance",
        "physical event correspondence",
        "external parameterization identity and lapse/Jacobian semantics",
        "internal-clock perspective and readout correspondence",
        "continuation-class and outcome correspondence",
        "measurement normalization semantics",
        "separation of constraint orbit from modal continuation",
    }
    derived = " ".join(synthesis.derived_or_reconstructible_roles)
    assert "numerically reconstructible" in derived
    assert "without restoring typed identity" in derived
    assert "q(T=tau) remains tau-dependent" in derived
    assert "representation-dependent Xi provenance" in derived


def test_stage12g_project_questions_close_multi_orbit_gap_but_keep_ontology_guards(synthesis) -> None:
    answers = {item.question_id: item for item in synthesis.project_questions}
    for question_id in ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6"):
        assert answers[question_id].evidence_class == "established_finite_model_result"
    assert "not diffeomorphism invariance" in answers["Q1"].boundary
    assert "ontological becoming" in answers["Q3"].boundary
    assert answers["Q7"].evidence_class == "interpretation_guard"
    assert "no eternalism/becoming verdict" in answers["Q7"].boundary
    assert answers["Q8"].evidence_class == "evidence_selected_research_gate"
    assert "not general relativity" in answers["Q8"].boundary


def test_stage12g_unresolved_boundaries_close_multi_orbit_gap_but_keep_constraint_algebra_and_gravity_open() -> None:
    unresolved = unresolved_boundaries()
    assert "single_hamiltonian_constraint => nontrivial_multi_constraint_algebra" in unresolved
    assert "finite_multi_orbit_gauge_covariance => general_covariance" in unresolved
    assert "finite_constraint_generated_gauge_atlas => diffeomorphism_invariance" in unresolved
    assert "finite_C_x_G_x_Phi_compatibility => refoliation_invariance" in unresolved
    assert "fixed_free_particle_constraint => dynamical_metric_or_gravitational_clock_structure" in unresolved
    assert "Dirac_invariant_orbit_data_plus_relational_change => eternalism_or_ontological_becoming" in unresolved


def test_stage12g_gate_ranking_uniquely_selects_multi_constraint_refoliation_precursor(synthesis) -> None:
    gates = synthesis.stage13_candidates
    assert gates[0].gate_id == "multi_constraint_refoliation_precursor"
    assert gates[0].label == SELECTED_STAGE13_GATE_LABEL
    assert gates[0].score == 10
    assert gates[0].score > gates[1].score
    assert synthesis.selected_stage13_gate == "multi_constraint_refoliation_precursor"


def test_stage12g_gate_scores_follow_current_evidence(snapshot) -> None:
    scores = {item.gate_id: item.score for item in stage13_gate_candidates(snapshot)}
    assert scores == {
        "multi_constraint_refoliation_precursor": 10,
        "gravitational_minisuperspace_extension": 7,
        "richer_causal_order": 7,
        "nonideal_povm_clocks": 6,
    }


def test_stage12g_does_not_jump_directly_to_general_relativity(synthesis) -> None:
    assert synthesis.stage13_candidates[0].gate_id == "multi_constraint_refoliation_precursor"
    gravity = next(
        item for item in synthesis.stage13_candidates
        if item.gate_id == "gravitational_minisuperspace_extension"
    )
    assert gravity.score < synthesis.stage13_candidates[0].score
    assert "below the algebra precursor" in gravity.rationale
    assert "dynamical metric" in " ".join(gravity.pressure_signals)


def test_stage12g_summary_closes_48_49_and_keeps_50_external() -> None:
    summary = stage12g_summary()
    criteria = summary["current_execution_criteria"]
    assert tuple(criteria.keys()) == ("48", "49", "50")
    assert "exactly one frozen Stage 12 status" in criteria["48"]
    assert "without presupposing GR or general covariance" in criteria["49"]
    assert "external" in criteria["50"]
    assert summary["choice"] == "multi_orbit_gauge_covariant"
    assert summary["selected_stage13_gate"] == "multi_constraint_refoliation_precursor"
    guards = summary["guards"]
    assert "multi_orbit_gauge_covariant finite family != general covariance" in guards
    assert "finite C x G x Phi compatibility != refoliation invariance" in guards
    assert "single Hamiltonian constraint != hypersurface-deformation algebra" in guards
    assert "constraint-algebra/refoliation precursor != general relativity" in guards
    assert "Dirac-invariant data + relational change != proof of eternalism" in guards
