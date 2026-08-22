from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_stage10b_checkpoint_status_and_next_stage_are_consistent() -> None:
    protocol = _read("docs/stage10_protocol.md")
    notes = _read("docs/stage10b_notes.md")
    results = _read("results/stage10b_measurement_lift.md")
    assert "Stage 10A and Stage 10B completed" in protocol
    assert "criteria 1–23 completed" in protocol
    assert "Stage 10B completed; criteria 17–23 satisfied" in notes
    assert "Stage 10B completed; criteria 17–23 satisfied" in results
    for text in (protocol, notes, results):
        assert "Stage 10C — continuation-aware A/B/C measurement transport" in text


def test_stage10b_selected_representation_and_normalization_boundary_are_documented() -> None:
    protocol = _read("docs/stage10_protocol.md")
    notes = _read("docs/stage10b_notes.md")
    results = _read("results/stage10b_measurement_lift.md")
    for text in (protocol, notes, results):
        assert "reference-induced" in text
        assert "effect form" in text or "effect-form" in text
        assert "Stage 9C" in text
        assert "non-Euclidean-unitary" in text
    assert "reference-chart identity normalization != identity normalization in every transported chart" in protocol
    assert "physical metric != operational normalization by definition" in results
    assert "normalization representation selected != measurement covariance established" in protocol


def test_stage10b_criteria_17_through_23_are_closed() -> None:
    protocol = _read("docs/stage10_protocol.md")
    results = _read("results/stage10b_measurement_lift.md")
    for criterion in range(17, 24):
        assert f"{criterion}." in protocol
        assert f"{criterion}." in results
    assert results.count("**satisfied**") >= 7


def test_stage10b_correspondence_and_wrong_continuation_controls_are_documented() -> None:
    notes = _read("docs/stage10b_notes.md")
    results = _read("results/stage10b_measurement_lift.md")
    for text in (notes, results):
        assert "h_L -> h_L" in text or "h_L and h_R lifts" in text
        assert "future_signature_left" in text
        assert "future_signature_other" in text
        assert "wrong-continuation" in text.lower()
    assert "same coordinate dimension != same continuation-specific measurement representation" in notes
    assert "same shape != same typed measurement" in results


def test_stage10b_validation_checkpoint_is_recorded() -> None:
    protocol = _read("docs/stage10_protocol.md")
    notes = _read("docs/stage10b_notes.md")
    results = _read("results/stage10b_measurement_lift.md")
    for text in (protocol, notes, results):
        assert "run #1163" in text
        assert "795 passed in 462.74s" in text
