from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_stage10f_checkpoint_and_next_stage_are_documented() -> None:
    notes = _read("docs/stage10f_notes.md")
    results = _read("results/stage10f_ablation.md")
    for text in (notes, results):
        assert "Stage 10F completed; criteria 44–47 satisfied" in text
        assert "Stage 10G — synthesis and evidence-selected next gate" in text


def test_stage10f_correspondence_and_normalization_classifications_are_explicit() -> None:
    notes = _read("docs/stage10f_notes.md")
    results = _read("results/stage10f_ablation.md")
    for text in (notes, results):
        assert "event correspondence" in text
        assert "continuation-class correspondence" in text
        assert "outcome correspondence" in text
        assert "normalization" in text.lower()
        assert "preserved" in text
        assert "lost" in text
        assert "underdetermined" in text
        assert "not_established" in text
        assert "refuted" in text


def test_stage10f_false_positive_witnesses_and_guards_are_documented() -> None:
    notes = _read("docs/stage10f_notes.md")
    results = _read("results/stage10f_ablation.md")
    combined = notes + "\n" + results
    for phrase in (
        "bare-effect",
        "wrong continuation",
        "wrong outcome",
        "wrong event",
        "weight misalignment",
        "fresh numerical identity",
    ):
        assert phrase in combined
    for guard in (
        "numerical reconstructibility != typed operational identification",
        "lost != metaphysically irreducible",
        "reconstructible != universally redundant",
        "not_established != false",
        "finite-model ablation != fundamental ontology",
    ):
        assert guard in combined


def test_stage10f_criteria_44_through_47_are_closed() -> None:
    notes = _read("docs/stage10f_notes.md")
    results = _read("results/stage10f_ablation.md")
    for criterion in range(44, 48):
        assert f"{criterion}." in notes
        assert f"{criterion}." in results
    assert notes.count("**satisfied**") >= 4
    assert results.count("**satisfied**") >= 4


def test_stage10f_validation_checkpoint_is_recorded() -> None:
    notes = _read("docs/stage10f_notes.md")
    results = _read("results/stage10f_ablation.md")
    for text in (notes, results):
        assert "run #1249" in text
        assert "843 passed in 575.02s" in text
