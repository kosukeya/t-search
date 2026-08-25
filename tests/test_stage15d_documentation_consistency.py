from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = (ROOT / "docs" / "stage15d_notes.md").read_text(encoding="utf-8")
RESULT = (ROOT / "results" / "stage15d_basis.md").read_text(encoding="utf-8")

SOURCE_HEAD = "1c24fe88f0bec2d6d557fa21d353eb9385019436"


def test_stage15d_documents_record_validated_checkpoint_and_counts():
    combined = NOTES + "\n" + RESULT
    assert SOURCE_HEAD in combined
    for phrase in (
        "run #1968",
        "1217 passed in 551.47s (0:09:11)",
        "**14**",
        "**216 = 108 positive + 108 off-surface**",
        "strict L1 candidates: **7**, strongly commuting: **2**",
        "one-step local candidates including L0: **10**, strongly commuting: **2**",
        "**9072**",
        "**18144**",
        "exact Lfinite depth **2**",
        "minimum exhibited local Abelianization depth: **1**",
    ):
        assert phrase in combined


def test_stage15d_closes_only_criteria_32_through_38():
    combined = NOTES + "\n" + RESULT
    assert "criteria **32–38**" in combined or "Criteria **32–38**" in combined
    assert "Criteria **39–50 remain pending at the Stage 15D checkpoint**" in combined
    assert "local_abelianization_persists" in combined
    assert "Stage 15D locality-preserving basis pressure test on the frozen three-site carrier = local_abelianization_persists" in combined


def test_stage15d_documents_preserve_locality_and_interpretation_guards():
    combined = NOTES + "\n" + RESULT
    for phrase in (
        "basis locality != physical causal locality",
        "finite graph locality != relativistic microcausality",
        "locality-preserving basis map != gauge transformation",
        "local Abelianization != absence of meaningful local constraint structure",
        "known nonlocal seed reconstruction != proof that all Abelianizations are nonlocal",
        "constraint-basis change != physical-orbit change",
        "strongly commuting finite basis != refoliation invariance",
        "Stage 15D basis equivalence != general relativity",
        "repository validation != new scientific evidence",
    ):
        assert phrase in combined


def test_stage15d_documents_keep_stage15e_boundary_explicit():
    combined = NOTES + "\n" + RESULT
    assert "Stage 15E — typed O/P/R/V/Xi and future-measurement descent" in combined
    assert "typed O/P/R/V/Xi preservation" in NOTES
