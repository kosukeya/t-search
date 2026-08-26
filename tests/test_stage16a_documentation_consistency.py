from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = (ROOT / "docs" / "stage16a_notes.md").read_text(encoding="utf-8")
RESULT = (ROOT / "results" / "stage16a_local_smeared.md").read_text(encoding="utf-8")

SCIENTIFIC_HEAD = "20f448e676499ecdab87b890bef79c9e19302832"
PR_MERGE_CHECKOUT = "bc7b18714841751bf0107646298003059ff4ce70"
PYTEST_SUMMARY = "1276 passed in 716.34s (0:11:56)"
BOUNDED_RESULT = (
    "Stage 16A four-site cyclic first-class carrier, exact local/smeared algebra, "
    "support audits, and finite representative family = established"
)


def test_stage16a_docs_record_validated_scientific_checkpoint():
    for text in (NOTES, RESULT):
        assert SCIENTIFIC_HEAD in text
        assert PR_MERGE_CHECKOUT in text
        assert PYTEST_SUMMARY in text
        assert BOUNDED_RESULT in text


def test_stage16a_docs_record_deterministic_carrier_and_algebra_evidence():
    combined = NOTES + "\n" + RESULT
    for phrase in (
        "324 positive representatives",
        "324 deterministic off-surface",
        "81 representatives each",
        "2592",
        "5184",
        "864",
        "768",
        "0.9375",
        "1.3877787807814457e-17",
        "2.7755575615628914e-17",
        "exact sparse-polynomial oracle",
        "rank **4**",
    ):
        assert phrase in combined


def test_stage16a_docs_keep_support_notions_and_interpretation_separate():
    combined = NOTES + "\n" + RESULT
    for phrase in (
        "local canonical support != local closure-coordinate support",
        "cycle-spanning closure coordinates != physical nonlocality by definition",
        "Stage 16A support audit != Stage 16D locality obstruction",
        "cyclic first-class closure != hypersurface-deformation algebra",
        "known global Abelianization != proof that all Abelianizations are nonlocal",
        "failure to Abelianize != ontological becoming",
        "repository validation != new scientific evidence",
    ):
        assert phrase in combined


def test_stage16a_docs_close_only_criteria_11_through_17():
    combined = NOTES + "\n" + RESULT
    assert "criteria 11–17 satisfied" in combined.lower()
    assert "Criteria **18–50 remain pending**." in combined
    for criterion in range(11, 18):
        assert f"{criterion}." in NOTES or f"**{criterion}**" in RESULT
    assert "Stage 16B" in combined


def test_stage16a_docs_do_not_promote_later_stage_claims():
    combined = NOTES + "\n" + RESULT
    for phrase in (
        "Finite path defects and compensation remain Stage 16B",
        "Full quotient/reachability and complete-relational descent remain Stage 16C",
        "Locality-preserving Abelianization remains Stage 16D",
        "Typed O/P/R/V/Xi descent remains Stage 16E",
    ):
        assert phrase in NOTES
    assert "does **not** establish compensated path covariance" in RESULT
