from pathlib import Path

from t_search.stage15_synthesis import (
    SELECTED_STAGE16_GATE_ID,
    SELECTED_STAGE16_GATE_LABEL,
    Stage15SynthesisChoice,
    stage15g_synthesis,
    stage16_gate_candidates,
)

ROOT = Path(__file__).resolve().parents[1]
NOTES = (ROOT / "docs" / "stage15g_notes.md").read_text(encoding="utf-8")
RESULT = (ROOT / "results" / "stage15g_synthesis_stage16_gate.md").read_text(encoding="utf-8")
PROTOCOL = (ROOT / "docs" / "stage15_protocol.md").read_text(encoding="utf-8")
README = (ROOT / "README.md").read_text(encoding="utf-8")
ROADMAP = (ROOT / "docs" / "roadmap.md").read_text(encoding="utf-8")

VALIDATED_HEAD = "de43fb44f4c0e6fc7095afef34805e7a1ba96b8b"
SOURCE_LOGIC_HEAD = "dca5dfb1c0faf3f7e57b07664529166f0f12b12d"


def test_stage15g_documents_validated_checkpoint_and_closes_only_criteria_48_49():
    for text in (NOTES, RESULT):
        assert VALIDATED_HEAD in text
        assert "1255 passed in 886.65s (0:14:46)" in text
        assert "1255 passed in 553.80s (0:09:13)" in text
        assert "criteria 48–49 satisfied" in text.lower()
        normalized = text.lower().replace("**", "")
        assert "criterion 50" in normalized
        assert "pending" in normalized
    assert SOURCE_LOGIC_HEAD in NOTES


def test_stage15g_documented_synthesis_matches_executable_frozen_choice():
    synthesis = stage15g_synthesis()
    assert synthesis.choice == (
        Stage15SynthesisChoice.SPATIAL_LOCAL_PATH_COVARIANT_LOCAL_ABELIANIZABLE
    )
    assert synthesis.criteria_48_49_satisfied
    for text in (NOTES, RESULT, PROTOCOL, README, ROADMAP):
        assert "spatial_local_path_covariant_local_abelianizable" in text


def test_stage15g_documented_ranking_and_selected_gate_match_executable_selector():
    candidates = stage16_gate_candidates()
    assert [item.score for item in candidates] == [15, 11, 9, 8, 6]
    assert candidates[0].gate_id == SELECTED_STAGE16_GATE_ID
    assert candidates[0].label == SELECTED_STAGE16_GATE_LABEL
    for text in (NOTES, RESULT, README, ROADMAP):
        assert SELECTED_STAGE16_GATE_ID in text
        assert "four-site closed-cycle" in text
        assert "no terminal seed generator" in text
    assert "four_site_closed_cycle_constraint_algebra_precursor` — **15**" in NOTES
    assert "larger_sparse_graph_locality_scaling_audit` — **11**" in NOTES
    assert "admissible_basis_transformation_completeness_audit` — **9**" in NOTES
    assert "gravitational_minisuperspace_extension` — **8**" in NOTES
    assert "nonideal_povm_clock_extension` — **6**" in NOTES


def test_stage15g_documents_why_four_sites_are_minimally_nontrivial_for_closed_cycle_locality():
    for text in (NOTES, RESULT, ROADMAP):
        assert "three-site cycle" in text.lower()
        assert "four-site cycle" in text.lower()
        assert "terminal" in text.lower()
    assert "closed-cycle selection != predicted locality obstruction" in NOTES
    assert "closed-cycle selection != predicted locality obstruction" in RESULT


def test_stage15g_interpretation_guards_remain_bounded():
    guards = (
        "one-step L1 Abelianization on an open three-site chain != universal local Abelianizability",
        "local Abelianization != absence of meaningful local constraint structure",
        "Dirac-invariant data + relational change != proof of eternalism",
        "complete relational observable != ontological becoming by definition",
        "future-measurement covariance != future actuality",
        "repository validation != new scientific evidence",
    )
    for guard in guards:
        assert guard in NOTES
    for guard in (
        "Dirac-invariant data + relational change != proof of eternalism",
        "complete relational observable != ontological becoming by definition",
        "future-measurement covariance != future actuality",
        "repository validation != new scientific evidence",
    ):
        assert guard in RESULT


def test_stage15g_does_not_start_stage16_or_close_criterion_50_by_documentation_only():
    assert "Stage 16 has not started" in NOTES
    assert "Criteria **1–49 are satisfied**" in RESULT
    assert "Criterion **50 remains pending**" in RESULT
    assert "criterion 50 — external final full-repository regression / merge-readiness review" in PROTOCOL
