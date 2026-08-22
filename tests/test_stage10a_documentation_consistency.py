from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_stage10a_checkpoint_status_and_next_stage_are_consistent() -> None:
    protocol = _read("docs/stage10_protocol.md")
    notes = _read("docs/stage10a_notes.md")
    results = _read("results/stage10a_reference_measurement.md")
    assert "Stage 10A completed" in protocol
    assert "criteria 1–16 completed" in protocol
    assert "Stage 10A completed; criteria 11–16 satisfied" in results
    assert "Stage 10B — continuation-specific measurement lift / normalization choice" in protocol
    assert "Stage 10B — continuation-specific measurement lift / normalization choice" in notes
    assert "Stage 10B — continuation-specific measurement lift / normalization choice" in results


def test_stage10a_reference_typing_and_scope_guards_are_documented() -> None:
    protocol = _read("docs/stage10_protocol.md")
    notes = _read("docs/stage10a_notes.md")
    results = _read("results/stage10a_reference_measurement.md")
    for text in (protocol, notes, results):
        assert "e1" in text and "e2" in text
        assert "future_signature_left" in text
        assert "future_signature_other" in text
        assert "reference" in text.lower()
    assert "typed continuation id != hidden selected continuation" in protocol
    assert "reference-node validity != cross-clock measurement covariance" in protocol
    assert "reference-node measurement validity != cross-clock measurement covariance" in results


def test_stage10a_criteria_11_through_16_are_closed_without_advancing_later_criteria() -> None:
    protocol = _read("docs/stage10_protocol.md")
    results = _read("results/stage10a_reference_measurement.md")
    for criterion in range(11, 17):
        assert f"{criterion}." in protocol
        assert f"{criterion}." in results
    assert results.count("**satisfied**") >= 6
    assert "does **not** establish criteria 17–50" in results


def test_stage10a_validation_checkpoint_is_recorded() -> None:
    protocol = _read("docs/stage10_protocol.md")
    results = _read("results/stage10a_reference_measurement.md")
    for text in (protocol, results):
        assert "run #1145" in text
        assert "783 passed in 461.16s" in text
