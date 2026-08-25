from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = (ROOT / "docs" / "stage15c_notes.md").read_text(encoding="utf-8")
RESULT = (ROOT / "results" / "stage15c_relational.md").read_text(encoding="utf-8")

SOURCE_HEAD = "8d2952585c106c6f56843657aa28b30e67fbd077"


def test_stage15c_documents_record_validated_checkpoint_and_counts():
    combined = NOTES + "\n" + RESULT
    assert SOURCE_HEAD in combined
    for phrase in (
        "run #1962",
        "1203 passed in 618.87s (0:10:18)",
        "**216**",
        "**2916/2916**",
        "**8748**",
        "**23328**",
        "**14580**",
        "**324**",
        "**108/108**",
        "**2.0 / 1.0 / 0.5**",
        "**3.5**",
    ):
        assert phrase in combined


def test_stage15c_closes_only_criteria_25_through_31():
    combined = NOTES + "\n" + RESULT
    assert "criteria **25–31**" in combined or "Criteria **25–31**" in combined
    assert "Criteria **32–50 remain pending at the Stage 15C checkpoint**" in combined
    assert "Stage 15C representative-independent Dirac / complete-relational / sampled four-class quotient descent = established" in combined


def test_stage15c_preserves_interpretation_and_stage15d_boundary():
    combined = NOTES + "\n" + RESULT
    for phrase in (
        "sampled four-class quotient != universal reduced-phase-space theorem",
        "sampled same-orbit reachability != universal gauge-orbit theorem",
        "complete relational observable != ontological becoming by definition",
        "Dirac-invariant data + relational change != proof of eternalism",
        "compensated relational descent != refoliation invariance",
        "Stage 15C quotient descent != Stage 15D locality-protected non-Abelianity",
        "repository validation != new scientific evidence",
    ):
        assert phrase in combined
