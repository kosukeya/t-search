from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_stage10d_checkpoint_status_and_next_stage_are_consistent() -> None:
    protocol = _read("docs/stage10_protocol.md")
    notes = _read("docs/stage10d_notes.md")
    results = _read("results/stage10d_probability_covariance.md")
    assert "Stage 10D completed" in notes
    assert "criteria 32–38 satisfied" in notes
    assert "Stage 10D completed" in results
    assert "criteria 32–38 satisfied" in results
    for text in (protocol, notes, results):
        assert "Stage 10E" in text
        assert "weights" in text.lower()
        assert "modal" in text.lower()


def test_stage10d_probability_scope_and_status_are_explicit() -> None:
    notes = _read("docs/stage10d_notes.md")
    results = _read("results/stage10d_probability_covariance.md")
    for text in (notes, results):
        assert "full typed future-measurement covariance = established" in text
        assert "per-continuation" in text
        assert "pre-weighting" in text
        assert "weighted/modal/update covariance" in text
        assert "not_established" in text
        assert "Stage 9C" in text


def test_stage10d_tomography_and_negative_controls_are_documented() -> None:
    notes = _read("docs/stage10d_notes.md")
    results = _read("results/stage10d_probability_covariance.md")
    for text in (notes, results):
        assert "196" in text
        assert "7056" in text
        assert "fresh" in text.lower() and "identity" in text.lower()
        assert "misaligned" in text.lower() and "metric" in text.lower()
        assert "swapped" in text.lower() and "outcome" in text.lower()
        assert "typed-resource distinction != numerical inequality" in text


def test_stage10d_pilot_failure_and_corrected_validation_are_recorded() -> None:
    notes = _read("docs/stage10d_notes.md")
    results = _read("results/stage10d_probability_covariance.md")
    for text in (notes, results):
        assert "#1209" in text
        assert "818 passed / 4 failed" in text
        assert "#1213" in text
        assert "823 passed in 311.17s" in text


def test_stage10d_criteria_32_through_38_are_closed() -> None:
    notes = _read("docs/stage10d_notes.md")
    results = _read("results/stage10d_probability_covariance.md")
    for criterion in range(32, 39):
        assert f"{criterion}." in notes
        assert f"{criterion}." in results
    assert notes.count("**satisfied**") >= 7
    assert results.count("**satisfied**") >= 7
