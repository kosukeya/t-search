from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = (ROOT / "docs" / "stage15b_notes.md").read_text(encoding="utf-8")
RESULT = (ROOT / "results" / "stage15b_paths.md").read_text(encoding="utf-8")

SOURCE_HEAD = "54d508ea432953e966809677c736253ab9930d0d"


def test_stage15b_documents_record_validated_checkpoint_and_counts():
    combined = NOTES + "\n" + RESULT
    assert SOURCE_HEAD in combined
    for phrase in (
        "run #1956",
        "1193 passed in 890.90s",
        "**864**",
        "**1728**",
        "**576**",
        "**288**",
        "**540**",
        "**432**",
        "**108**",
        "**2592**",
    ):
        assert phrase in combined


def test_stage15b_closes_only_criteria_18_through_24():
    combined = NOTES + "\n" + RESULT
    assert "criteria **18–24**" in combined or "Criteria **18–24**" in combined
    assert "Criteria **25–50 remain pending at the Stage 15B checkpoint**" in combined
    assert "Stage 15B local/smeared finite compensated-path closure on the frozen three-site carrier = established" in combined


def test_stage15b_preserves_interpretation_guards():
    combined = NOTES + "\n" + RESULT
    for phrase in (
        "raw local path-word inequality != physical path dependence",
        "compensated local-path closure != refoliation invariance",
        "finite smeared path closure != continuum hypersurface-deformation algebra",
        "Stage 15B path closure != Stage 15D locality obstruction",
        "repository validation != new scientific evidence",
    ):
        assert phrase in combined
