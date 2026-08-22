from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_stage10c_checkpoint_status_and_next_stage_are_consistent() -> None:
    protocol = _read("docs/stage10_protocol.md")
    notes = _read("docs/stage10c_notes.md")
    results = _read("results/stage10c_measurement_transport.md")
    # Historical Stage 10C completion must remain explicit after later stages advance.
    assert "Stage 10C — continuation-aware A/B/C measurement transport — completed" in protocol
    assert "Stage 10C completed; criteria 24–31 satisfied" in notes
    assert "Stage 10C completed; criteria 24–31 satisfied" in results
    # Stage 10D must remain recorded as the completed successor, even when Stage 10E/F advance.
    assert "Stage 10D — per-continuation Born/completeness/positivity covariance — completed" in protocol
    for text in (notes, results):
        assert "Stage 10D — per-continuation Born/completeness/positivity covariance" in text


def test_stage10c_atlas_counts_and_dual_transport_are_documented() -> None:
    protocol = _read("docs/stage10_protocol.md")
    notes = _read("docs/stage10c_notes.md")
    results = _read("results/stage10c_measurement_transport.md")
    for text in (protocol, notes, results):
        assert "18" in text
        assert "108" in text
        assert "324" in text
        assert "S^{-dagger}" in text
        assert "direct" in text.lower()
    assert "future-measurement representation covariance = established" in protocol
    # This remains a historical Stage 10C checkpoint statement; Stage 10D later closes it.
    assert "full per-continuation probability covariance = not_established" in protocol


def test_stage10c_completeness_positivity_and_typing_guards_are_documented() -> None:
    protocol = _read("docs/stage10_protocol.md")
    notes = _read("docs/stage10c_notes.md")
    results = _read("results/stage10c_measurement_transport.md")
    for text in (protocol, notes, results):
        assert "sum" in text.lower() and "F" in text and "N" in text
        assert "positive" in text.lower()
        assert "event" in text.lower()
        assert "class" in text.lower()
        assert "outcome" in text.lower()
    assert "measurement representation covariance != probability covariance by definition" in protocol


def test_stage10c_negative_controls_are_documented() -> None:
    notes = _read("docs/stage10c_notes.md")
    results = _read("results/stage10c_measurement_transport.md")
    for text in (notes, results):
        assert "bare" in text.lower()
        assert "misdeclared" in text.lower()
        assert "swapped" in text.lower()
        assert "rejected" in text.lower()
    assert "same physical measurement != same numerical matrix in every chart" in notes
    assert "matrix transport correctness != semantic correspondence correctness" in results


def test_stage10c_criteria_24_through_31_are_closed() -> None:
    protocol = _read("docs/stage10_protocol.md")
    results = _read("results/stage10c_measurement_transport.md")
    for criterion in range(24, 32):
        assert f"{criterion}." in protocol
        assert f"{criterion}." in results
    assert results.count("**satisfied**") >= 8


def test_stage10c_validation_checkpoint_is_recorded() -> None:
    protocol = _read("docs/stage10_protocol.md")
    notes = _read("docs/stage10c_notes.md")
    results = _read("results/stage10c_measurement_transport.md")
    for text in (protocol, notes, results):
        assert "run #1185" in text
        assert "809 passed in 476.21s" in text
