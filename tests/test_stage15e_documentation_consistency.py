from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = (ROOT / "docs" / "stage15e_notes.md").read_text(encoding="utf-8")
RESULT = (ROOT / "results" / "stage15e_measurement.md").read_text(encoding="utf-8")

SOURCE_HEAD = "795de1afdb51b2936610ab870aa0eb7ed3a133cb"


def test_stage15e_documents_record_validated_checkpoint_and_counts():
    combined = NOTES + "\n" + RESULT
    assert SOURCE_HEAD in combined
    for phrase in (
        "run: **#1974**",
        "1230 passed in 892.67s (0:14:52)",
        "**108**",
        "**4**",
        "**864**",
        "**1728**",
        "**540**",
        "**1080**",
        "**14**",
        "**1512 = 14 × 108**",
        "**3024**",
        "0.0034784353473946705",
        "criteria_39_43_satisfied = true",
    ):
        assert phrase in combined


def test_stage15e_documents_record_non_grid_endpoint_strengthening():
    combined = NOTES + "\n" + RESULT
    for phrase in (
        "independent smeared non-grid endpoint reconstruction audit",
        "independent non-grid endpoint reconstructions: **1080**",
        "complete relational O-events",
        "orbit witness",
        "all residuals",
    ):
        assert phrase in combined


def test_stage15e_closes_only_criteria_39_through_43():
    combined = NOTES + "\n" + RESULT
    assert "criteria **39–43**" in combined or "Criteria **39–43**" in combined
    assert "criteria 1–43 satisfied / 44–50 pending" in combined
    assert "Criteria **44–50 remain pending at the Stage 15E checkpoint**" in combined
    assert "Stage 15F — locality-breaking / anomaly / false-positive controls" in combined


def test_stage15e_documents_preserve_typed_descent_interpretation_guards():
    combined = NOTES + "\n" + RESULT
    for phrase in (
        "spatial/path/basis Xi provenance != quotient-level physical content",
        "spatial index != ontological spatial substance",
        "path word != physical temporal history",
        "path word != modal continuation",
        "compensated local/smeared operational descent != refoliation invariance",
        "basis-equivalent operational descent != refoliation invariance",
        "local Abelianization + typed descent != physical triviality",
        "future-measurement covariance != future actuality",
        "path-independent evidence update != ontological becoming",
        "typed operational descent != ontological equivalence",
        "Potentiality != quantum randomness by definition",
        "orbit-sensitive witness != empirical prediction",
        "spatially indexed constraint precursor != general relativity",
        "repository validation != new scientific evidence",
    ):
        assert phrase in combined


def test_stage15e_documents_record_all_three_descent_classifications():
    combined = NOTES + "\n" + RESULT
    for classification in (
        "spatial_local_path_operational_payloads_descend",
        "spatial_smeared_path_operational_payloads_descend",
        "spatial_basis_operational_payloads_descend",
    ):
        assert classification in combined


def test_stage15e_bounded_result_is_identical_in_notes_and_result():
    bounded = (
        "Stage 15E typed O/P/R/V/Xi and future-measurement descent across the "
        "sampled spatial quotient, compensated local/smeared paths, and all "
        "Stage 15D equivalent basis candidates on the frozen finite family = established"
    )
    assert bounded in NOTES
    assert bounded in RESULT
