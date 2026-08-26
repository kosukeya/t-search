from pathlib import Path

from t_search.stage16_synthesis import (
    STAGE16G_BOUNDED_RESULT,
    STAGE16G_SELECTED_CLASSIFICATION,
    STAGE17_SELECTED_GATE,
    STAGE17_SELECTED_GATE_STATEMENT,
    ranked_stage17_candidates,
    stage16g_diagnostics,
)


SCIENTIFIC_HEAD = "e1a559abc2488e6ef23bda7c7dbb50bc43bd030d"
CHECKPOINT = "1338 passed in 738.18s (0:12:18)"


def _documents() -> tuple[str, str]:
    notes = Path("docs/stage16g_notes.md").read_text(encoding="utf-8")
    result = Path("results/stage16g_synthesis.md").read_text(encoding="utf-8")
    return notes, result


def test_stage16g_documents_record_scientific_checkpoint_and_criteria_state():
    notes, result = _documents()
    for text in (notes, result):
        assert SCIENTIFIC_HEAD in text
        assert "#2060" in text
        assert CHECKPOINT in text
        assert "criteria 1–49 satisfied" in text.lower()
        assert "criterion 50" in text.lower()
        assert "pending" in text.lower()
        assert STAGE16G_SELECTED_CLASSIFICATION in text
        assert STAGE17_SELECTED_GATE in text


def test_stage16g_documents_and_executable_synthesis_agree():
    d = stage16g_diagnostics()
    ranking = ranked_stage17_candidates()

    assert d.all_stage16a_f_evidence_validated
    assert d.synthesis_classification == STAGE16G_SELECTED_CLASSIFICATION
    assert d.global_abelianization_established
    assert not d.local_witness_found_in_frozen_search
    assert d.presented_local_compensator_success_count == d.presented_local_compensator_probe_count == 2592
    assert d.quotient_class_count == d.typed_public_quotient_count == 4
    assert d.control_count == d.rejected_control_count == 20
    assert d.cycle_opening_exhibited_depth == 2
    assert d.three_site_projection_one_step_l1
    assert d.criteria_48_49_satisfied

    assert len(ranking) == 7
    assert [item.total for item in ranking] == [15, 14, 13, 11, 7, 6, 6]
    assert ranking[0].selector_id == STAGE17_SELECTED_GATE
    assert ranking[0].total == 15
    assert ranking[1].selector_id == "path_cycle_tree_topology_comparison_family"
    assert ranking[1].total == 14
    assert ranking[2].selector_id == "larger_sparse_graph_locality_scaling_audit"
    assert ranking[2].total == 13


def test_stage16g_documents_record_bounded_result_and_selected_gate_statement():
    notes, result = _documents()
    assert STAGE16G_BOUNDED_RESULT in result

    required_gate_markers = (
        "broader admissible locality-preserving basis-transformation class",
        "constructive local strongly commuting witness",
        "bounded completeness/nonexistence certificate",
        "without promoting search failure to a universal physical locality obstruction",
    )
    for marker in required_gate_markers:
        assert marker in STAGE17_SELECTED_GATE_STATEMENT
        assert marker in notes
        assert marker in result


def test_stage16g_documents_retain_bounded_interpretation_guards():
    notes, result = _documents()
    required = (
        "nonlocal_only_in_declared_search != universal locality obstruction",
        "no L1 witness in frozen search != no L1 Abelianization exists",
        "global Abelianization != physical triviality",
        "cycle opening changes graph topology != proof that topology is ontic",
        "failure to Abelianize != ontological becoming",
        "future-measurement covariance != future actuality",
        "typed operational descent != ontological equivalence",
        "Stage 17 completeness audit selection != predicted locality obstruction",
        "repository validation != new scientific evidence",
    )
    for marker in required:
        assert marker in notes
        assert marker in result
