import json

from t_search.stage6_synthesis import (
    SynthesisChoice,
    answer_project_questions,
    build_stage6g_synthesis,
    pre_merge_exit_criteria,
    select_synthesis_choice,
    stage6g_rows,
    stage7_gate_candidates,
)


def test_stage6g_answers_exactly_six_project_questions() -> None:
    answers = answer_project_questions()
    assert tuple(item.question_id for item in answers) == (
        "Q1", "Q2", "Q3", "Q4", "Q5", "Q6"
    )


def test_project_answers_preserve_not_established_boundaries() -> None:
    answers = {item.question_id: item for item in answer_project_questions()}
    assert "Not established" in answers["Q3"].answer
    assert "No reduction is established" in answers["Q2"].answer
    assert "fundamental" not in answers["Q6"].answer.lower()


def test_current_evidence_selects_layered_outcome_b() -> None:
    synthesis = build_stage6g_synthesis()
    assert synthesis.choice is SynthesisChoice.B_LAYERED
    assert synthesis.explicit_layers == ("O", "P", "R", "V")
    assert synthesis.compatibility_links == ("P_O", "P_R", "P_V")


def test_omega_is_derived_only_in_declared_quantum_interface() -> None:
    synthesis = build_stage6g_synthesis()
    assert len(synthesis.derived_roles) == 1
    assert synthesis.derived_roles[0].startswith("Omega")
    assert "tested Stage 5/6 quantum operator interface" in synthesis.derived_roles[0]


def test_outcome_classifier_is_not_hard_coded_to_b() -> None:
    reconstructed = {
        "O": "reconstructible",
        "P": "reconstructible",
        "R": "reconstructible",
        "V": "reconstructible",
        "Omega": "reconstructible",
    }
    assert select_synthesis_choice(
        reconstructed,
        {"P_O": True, "P_R": True, "P_V": True},
        omega_reconstructible=True,
    ) is SynthesisChoice.A_SINGLE_MINIMAL

    complementary = {
        "O": "lost",
        "P": "lost",
        "R": "lost",
        "V": "preserved",
        "Omega": "lost",
    }
    assert select_synthesis_choice(
        complementary,
        {"P_O": False, "P_R": False, "P_V": False},
        omega_reconstructible=False,
    ) is SynthesisChoice.C_COMPLEMENTARY

    assert select_synthesis_choice(
        {"O": "lost"},
        {},
        omega_reconstructible=False,
    ) is SynthesisChoice.D_INCONCLUSIVE


def test_unresolved_implications_remain_explicit() -> None:
    synthesis = build_stage6g_synthesis()
    assert synthesis.unresolved_implications == ("I3", "I7", "I8", "I9", "I10")


def test_stage7_gate_is_explicit_quantum_record_subsystem() -> None:
    synthesis = build_stage6g_synthesis()
    assert synthesis.selected_stage7_gate == "quantum_records"
    candidates = stage7_gate_candidates()
    assert candidates[0].gate_id == "quantum_records"
    assert candidates[0].score > candidates[1].score


def test_stage7_candidates_cover_all_protocol_gate_families() -> None:
    ids = {candidate.gate_id for candidate in stage7_gate_candidates()}
    assert ids == {
        "quantum_records",
        "joint_quantum_modality",
        "richer_causal_order",
        "nonideal_clocks",
    }


def test_pre_merge_exit_audit_passes_criteria_one_through_thirty_four() -> None:
    audit = pre_merge_exit_criteria()
    assert tuple(audit) == tuple(range(1, 35))
    assert all(audit.values())
    synthesis = build_stage6g_synthesis()
    assert synthesis.pre_merge_exit_criteria_passed == 34
    assert synthesis.pre_merge_exit_criteria_total == 34


def test_stage6g_rows_leave_criterion_35_to_external_ci_review() -> None:
    rows = stage6g_rows()
    assert rows["criterion_35"]["passed_in_python_module"] is False
    assert rows["criterion_35"]["status"] == "external_final_ci_and_merge_readiness_review_required"


def test_stage6g_rows_preserve_interpretation_guards() -> None:
    rows = stage6g_rows()
    guards = rows["interpretation_guards"]
    assert not guards["layered_candidate_is_fundamental_ontology"]
    assert not guards["lost_means_metaphysically_irreducible"]
    assert not guards["omega_reconstructible_here_means_universally_redundant"]
    assert not guards["perspective_change_is_temporal_succession"]
    assert not guards["stage6_synthesis_is_empirical_discovery"]


def test_stage6g_rows_are_json_serializable() -> None:
    json.dumps(stage6g_rows())
