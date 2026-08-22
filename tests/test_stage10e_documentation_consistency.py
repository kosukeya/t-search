from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_stage10e_checkpoint_status_and_next_stage_are_consistent() -> None:
    protocol = _read("docs/stage10_protocol.md")
    notes = _read("docs/stage10e_notes.md")
    results = _read("results/stage10e_modal_covariance.md")
    assert "Stage 10E completed; criteria 39–43 satisfied" in notes
    assert "Stage 10E completed; criteria 39–43 satisfied" in results
    for text in (notes, results):
        assert "Stage 10F — ablation / wrong-typing / false-positive controls" in text
    # The protocol must be advanced from the Stage 10D checkpoint before this
    # documentation-synchronized guard can pass.
    assert "Stage 10E — weights, modal models, and evidence-update covariance — completed" in protocol
    assert "criteria 1–43 completed" in protocol


def test_stage10e_weighted_modal_and_hidden_selector_guards_are_documented() -> None:
    notes = _read("docs/stage10e_notes.md")
    results = _read("results/stage10e_modal_covariance.md")
    for text in (notes, results):
        assert "weighted" in text.lower()
        assert "epistemic" in text.lower()
        assert "ontic" in text.lower()
        assert "h*" in text
        assert "selector" in text.lower()
        assert "weight mismatch" in text.lower()
    assert "matched public measurement views != modal/ontological identity" in notes
    assert "hidden h* diagnostic != operational access to h*" in results


def test_stage10e_evidence_update_scope_and_status_are_explicit() -> None:
    notes = _read("docs/stage10e_notes.md")
    results = _read("results/stage10e_modal_covariance.md")
    for text in (notes, results):
        assert "future_signature_left" in text
        assert "posterior" in text.lower()
        assert "evidence-update covariance" in text
        assert "ontological becoming" in text
        assert "weighted/modal/update operational covariance = established" in text


def test_stage10e_criteria_39_through_43_are_closed() -> None:
    protocol = _read("docs/stage10_protocol.md")
    results = _read("results/stage10e_modal_covariance.md")
    for criterion in range(39, 44):
        assert f"{criterion}." in protocol
        assert f"{criterion}." in results
    assert results.count("**satisfied**") >= 5


def test_stage10e_validation_checkpoint_is_recorded() -> None:
    notes = _read("docs/stage10e_notes.md")
    results = _read("results/stage10e_modal_covariance.md")
    for text in (notes, results):
        assert "run #1233" in text
        assert "834 passed in 455.24s" in text
