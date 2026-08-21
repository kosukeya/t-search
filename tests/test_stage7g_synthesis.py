import json

from t_search.stage7_synthesis import (
    Stage7SynthesisChoice,
    answer_project_questions,
    build_stage7g_synthesis,
    evidence_snapshot,
    pre_merge_exit_criteria,
    select_synthesis_choice,
    stage7_gate_candidates if False else stage8_gate_candidates,
    stage7g_rows,
    unresolved_implications,
)


def test_stage7g_evidence_snapshot_preserves_core_positive_and_negative_witnesses():
    evidence = evidence_snapshot()
    assert evidence.forward.record_defined is True
    assert evidence.forward.record_score > 0.9
    assert evidence.reversed.record_score < -0.9
    assert evidence.no_record.record_defined is False
    assert evidence.stage7d_transport.preserving_covariance is True
    assert evidence.stage7e_accessibility.hidden_is_inaccessible is True
    assert evidence.r_reconstruction.p_and_o_retained_without_r is True
    assert evidence.r_reconstruction.reconstruction_witness_found is False


def test_stage7g_selects_strengthened_not_reduced_or_broken():
    assert select_synthesis_choice() is Stage7SynthesisChoice.STRENGTHENED


def test_stage7g_strengthening_is_bounded_to_p_o_r_core_and_keeps_v_unintegrated():
    synthesis = build_stage7g_synthesis(include_exit_audit=False)
    assert synthesis.choice is Stage7SynthesisChoice.STRENGTHENED
    assert synthesis.strengthened_scope == ("P", "O", "R", "Xi_PR")
    assert synthesis.unintegrated_layers == ("V / Potentiality-extension semantics",)


def test_stage7g_refines_explicit_p_edges_as_derived_without_eliminating_p():
    synthesis = build_stage7g_synthesis(include_exit_audit=False)
    text = " ".join(synthesis.refinement_inside_p)
    assert "reconstructed" in text
    assert "per-perspective reductions" in text


def test_stage7g_project_questions_cover_single_model_covariance_minimality_access_and_boundaries():
    answers = answer_project_questions()
    assert tuple(item.question_id for item in answers) == ("Q1", "Q2", "Q3", "Q4", "Q5", "Q6")
    assert "Yes" in answers[0].answer
    assert "No" in answers[1].answer
    assert "No" in answers[2].answer
    assert "Not" in answers[3].answer or "reconstructible" in answers[3].answer
    assert answers[4].evidence_class == "untested_not_established"


def test_stage7g_keeps_metaphysical_and_modal_implications_not_established():
    unresolved = unresolved_implications()
    assert "record_defined_direction => phenomenal_passage" in unresolved
    assert "record_defined_direction => ontological_future_openness" in unresolved
    assert "perspective_consistency => modal_equivalence" in unresolved
    assert "finite_P_O_R_compatibility => general_covariance" in unresolved


def test_stage8_gate_ranking_selects_quantum_potentiality_uniquely():
    candidates = stage8_gate_candidates()
    assert len(candidates) == 4
    assert candidates[0].gate_id == "quantum_potentiality"
    assert candidates[0].score > candidates[1].score
    assert {item.gate_id for item in candidates} == {
        "quantum_potentiality",
        "richer_causal_order",
        "nonideal_povm_clocks",
        "parametrized_covariance_precursor",
    }


def test_stage8_quantum_potentiality_rationale_targets_the_only_unintegrated_stage6_layer():
    selected = stage8_gate_candidates()[0]
    assert "V" in " ".join(selected.pressure_signals)
    assert "only" in " ".join(selected.pressure_signals).lower()
    assert "modal" in selected.rationale.lower()


def test_pre_merge_exit_audit_covers_criteria_1_to_35_exactly():
    audit = pre_merge_exit_criteria()
    assert tuple(sorted(audit)) == tuple(range(1, 36))
    assert all(audit.values())


def test_stage7g_exit_criteria_32_to_35_are_derived_as_satisfied():
    audit = pre_merge_exit_criteria()
    assert {key: audit[key] for key in range(32, 36)} == {
        32: True,
        33: True,
        34: True,
        35: True,
    }


def test_stage7g_synthesis_reports_all_pre_merge_criteria_passed():
    synthesis = build_stage7g_synthesis()
    assert synthesis.pre_merge_exit_criteria_passed == 35
    assert synthesis.pre_merge_exit_criteria_total == 35
    assert synthesis.selected_stage8_gate == "quantum_potentiality"


def test_stage7g_rows_keep_criterion_36_external_until_final_ci_review():
    rows = stage7g_rows()
    json.dumps(rows)
    assert rows["criterion_36"]["passed_in_python_module"] is False
    assert rows["criterion_36"]["status"] == "external_final_ci_and_merge_readiness_review_required"


def test_stage7g_interpretation_guards_block_overclaiming():
    rows = stage7g_rows()
    guards = set(rows["interpretation_guards"])
    assert "lost != metaphysically irreducible" in guards
    assert "reconstructible != universally redundant" in guards
    assert "record-defined orientation != phenomenal passage" in guards
    assert "P-R covariance != P=R" in guards
    assert "Stage 7 synthesis != empirical discovery" in guards
