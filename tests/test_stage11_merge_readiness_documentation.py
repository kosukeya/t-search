from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")
ROADMAP = (ROOT / "docs" / "roadmap.md").read_text(encoding="utf-8")
PROTOCOL = (ROOT / "docs" / "stage11_protocol.md").read_text(encoding="utf-8")
CHECKPOINT = (ROOT / "results" / "stage11_criterion50_merge_readiness.md").read_text(encoding="utf-8")

SELECTED_STAGE12 = (
    "Construct a multi-orbit constraint-generated gauge atlas that separates "
    "gauge-related parameterizations from physically distinct orbits and tests "
    "whether relational/Dirac observables and the typed O/P/R/V measurement "
    "architecture descend consistently across that atlas."
)
VALIDATED_HEAD = "6b5ae9ffb2f1fe784080d9d2a02e349430d4f01a"
STAGE10_MERGE = "4a322634a5b83e416d374ee18e96ac6c7a5c88ba"


def test_stage11_planning_documents_are_synchronized_through_criterion50() -> None:
    for text in (README, ROADMAP, PROTOCOL):
        assert "Stage 11G" in text and "completed" in text
        assert "criteria 1–50" in text.lower()
        assert "parametrized_covariant" in text
        assert SELECTED_STAGE12 in text


def test_criterion50_external_validation_is_recorded() -> None:
    for text in (README, ROADMAP, PROTOCOL, CHECKPOINT):
        assert "#1469" in text
        assert "938 passed in 682.23s" in text
        assert "repository validation != new scientific evidence" in text
    assert "criterion 50 satisfied externally" in CHECKPOINT.lower()
    assert VALIDATED_HEAD in README
    assert VALIDATED_HEAD in ROADMAP
    assert VALIDATED_HEAD in PROTOCOL
    assert VALIDATED_HEAD in CHECKPOINT
    assert STAGE10_MERGE in CHECKPOINT
    assert "behind 0" in CHECKPOINT
    assert "mergeable = true" in CHECKPOINT
    assert "unresolved inline review threads: **0**" in CHECKPOINT
    assert "submitted review blockers: **0**" in CHECKPOINT


def test_stage12_gate_and_scope_guards_survive_merge_readiness() -> None:
    for text in (README, ROADMAP, PROTOCOL, CHECKPOINT):
        assert SELECTED_STAGE12 in text
        assert "parametrized_covariant finite family != general covariance" in text
        assert "one-orbit covariance != multi-orbit gauge covariance" in text
        assert "external parameterization independence != diffeomorphism invariance" in text
        assert "constraint-generated gauge precursor != general relativity" in text
    assert "parameterization-covariant future probabilities != future actuality" in CHECKPOINT
    assert "absence of preferred external parameterization != absence of ontological becoming" in CHECKPOINT


def test_merge_readiness_is_not_a_merge_action() -> None:
    for text in (README, ROADMAP, PROTOCOL, CHECKPOINT):
        assert "merge-ready != merged" in text
    assert "merge-ready and unmerged" in CHECKPOINT
    assert "Stage 11 was not merged" in CHECKPOINT
