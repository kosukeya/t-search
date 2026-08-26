from pathlib import Path


def test_stage16e_documents_record_validated_checkpoint_and_criteria_state():
    notes = Path("docs/stage16e_notes.md").read_text(encoding="utf-8")
    result = Path("results/stage16e_measurement.md").read_text(encoding="utf-8")
    for text in (notes, result):
        assert "d87a84dca0c553ab1a0c203e3f12b4670e9dbcbd" in text
        assert "#2046" in text or "run #2046" in text
        assert "1320 passed in 933.85s (0:15:33)" in text
        assert "criteria 1–44 satisfied" in text.lower()
        assert "criteria 45–50" in text.lower()


def test_stage16e_documents_match_executable_evidence_counts():
    notes = Path("docs/stage16e_notes.md").read_text(encoding="utf-8")
    result = Path("results/stage16e_measurement.md").read_text(encoding="utf-8")
    for text in (notes, result):
        for marker in ("324", "2,592", "5,184", "21", "6,804", "13,608"):
            assert marker in text
        assert "future-measurement" in text
        assert "Xi" in text


def test_stage16e_documents_preserve_interpretation_guards_and_next_stage():
    notes = Path("docs/stage16e_notes.md").read_text(encoding="utf-8")
    result = Path("results/stage16e_measurement.md").read_text(encoding="utf-8")
    for text in (notes, result):
        assert "future-measurement covariance != future actuality" in text
        assert "path-independent evidence update != ontological becoming" in text
        assert "typed operational descent != ontological equivalence" in text
        assert "Potentiality != quantum randomness by definition" in text
        assert "repository validation != new scientific evidence" in text
    assert "Stage 16F" in notes
