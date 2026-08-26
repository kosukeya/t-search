from pathlib import Path

from t_search.stage16_controls import (
    STAGE16F_BOUNDED_RESULT,
    STAGE16F_REQUIRED_VOCABULARY,
    canonical_stage16f_controls,
    stage16f_diagnostics,
)


SCIENTIFIC_HEAD = "38559933e42111efb241b764881684b978804aec"
VALIDATION_HEAD = "217a201c3f7cf5bd9b37db31ef58cd18ef6b8525"
CHECKPOINT = "1329 passed in 964.64s (0:16:04)"


def test_stage16f_documents_record_validated_checkpoint_and_criteria_state():
    notes = Path("docs/stage16f_notes.md").read_text(encoding="utf-8")
    result = Path("results/stage16f_controls.md").read_text(encoding="utf-8")
    for text in (notes, result):
        assert SCIENTIFIC_HEAD in text
        assert VALIDATION_HEAD in text
        assert "#2052" in text or "run #2052" in text
        assert CHECKPOINT in text
        assert "criteria 1–47 satisfied" in text.lower()
        assert STAGE16F_BOUNDED_RESULT in text


def test_stage16f_documents_and_executable_diagnostics_agree():
    diagnostics = stage16f_diagnostics()
    assert diagnostics.control_count == 20
    assert diagnostics.rejected_control_count == 20
    assert diagnostics.required_vocabulary_count == 16
    assert diagnostics.required_vocabulary_covered
    assert diagnostics.cycle_opening_exhibited_depth == 2
    assert diagnostics.three_site_projection_one_step_l1
    assert diagnostics.typed_corruption_control_count == 4
    assert diagnostics.typed_corruption_detected_count == 4
    assert diagnostics.all_controls_rejected
    assert diagnostics.criteria_45_47_satisfied

    classifications = {item.classification for item in canonical_stage16f_controls()}
    assert set(STAGE16F_REQUIRED_VOCABULARY) <= classifications


def test_stage16f_documents_retain_bounded_interpretation_guards():
    notes = Path("docs/stage16f_notes.md").read_text(encoding="utf-8")
    result = Path("results/stage16f_controls.md").read_text(encoding="utf-8")
    required = (
        "cycle opening changes graph topology != proof that topology is ontic",
        "three-cycle L1 label != nontrivial locality evidence",
        "repository validation != new scientific evidence",
    )
    for marker in required:
        assert marker in notes
        assert marker in result
