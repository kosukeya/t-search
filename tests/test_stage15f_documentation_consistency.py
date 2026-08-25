from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NOTES = (ROOT / "docs" / "stage15f_notes.md").read_text(encoding="utf-8")
RESULT = (ROOT / "results" / "stage15f_controls.md").read_text(encoding="utf-8")

SOURCE_HEAD = "96b7ca36af8a13d5925b0433052c84af97e0ca80"


def test_stage15f_documents_record_validated_checkpoint_and_deterministic_counts():
    combined = NOTES + "\n" + RESULT
    assert SOURCE_HEAD in combined
    for phrase in (
        "run: **#1982**",
        "1242 passed in 489.65s (0:08:09)",
        "**15**",
        "**15/15**",
        "**72**",
        "**648**",
        "**360**",
        "**108/108**",
        "**8748/8748**",
        "**4/4**",
        "depth **2**",
    ):
        assert phrase in combined


def test_stage15f_closes_only_criteria_44_through_47():
    combined = NOTES + "\n" + RESULT
    assert "criteria **44–47**" in combined or "Criteria **44–47**" in combined
    assert "criteria 1–47 satisfied / 48–50 pending" in combined
    assert "Criteria **48–50 remain pending at the Stage 15F checkpoint**" in combined
    assert "Stage 15G — executable synthesis and evidence-selected Stage 16 gate" in combined


def test_stage15f_documents_record_required_control_vocabulary():
    combined = NOTES + "\n" + RESULT
    for phrase in (
        "structure_function_removed_control_rejected",
        "disconnected_site_false_positive_rejected",
        "support_expansion_detected",
        "distance2_basis_nonlocal_detected",
        "singular_basis_map_rejected",
        "smearing_antisymmetry_corruption_detected",
        "constraint_algebra_anomaly_detected",
        "cross_orbit_false_positive_rejected",
        "relational_observable_incomplete",
        "representative_dependent_payload_corruption_detected",
    ):
        assert phrase in combined


def test_stage15f_documents_preserve_control_interpretation_guards():
    combined = NOTES + "\n" + RESULT
    for phrase in (
        "negative-control rejection != proof of continuum correctness",
        "graph disconnection control != relativistic causal disconnection",
        "locality-breaking detection != physical causal locality",
        "constraint-algebra anomaly detection != quantum anomaly theorem",
        "cross-orbit rejection != ontological superselection",
        "incomplete relational rejection != ontological becoming",
        "typed corruption detection != ontological equivalence",
        "local Abelianization surviving controls != physical triviality",
        "known seed non-L1 classification != universal nonlocality of Abelianization",
        "spatially indexed constraint precursor != general relativity",
        "repository validation != new scientific evidence",
    ):
        assert phrase in combined


def test_stage15f_bounded_result_is_identical_in_notes_and_result():
    bounded = (
        "Stage 15F frozen locality-breaking, anomaly, false-positive, relational, "
        "and typed-payload controls on the Stage 15 finite carrier = all declared "
        "controls rejected as intended"
    )
    assert bounded in NOTES
    assert bounded in RESULT
