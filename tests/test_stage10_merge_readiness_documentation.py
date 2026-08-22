from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")
ROADMAP = (ROOT / "docs" / "roadmap.md").read_text(encoding="utf-8")
PROTOCOL = (ROOT / "docs" / "stage10_protocol.md").read_text(encoding="utf-8")
CHECKPOINT = (ROOT / "results" / "stage10_criterion50_merge_readiness.md").read_text(encoding="utf-8")

SELECTED_STAGE10 = (
    "Construct and validate a fully typed cross-continuation future-measurement "
    "family under genuine continuation-aware clock changes."
)
SELECTED_STAGE11 = (
    "Construct a parametrized covariance precursor that preserves the typed "
    "O/P/R/V measurement architecture without assuming a preferred external "
    "time parameterization."
)
VALIDATED_HEAD = "11b4357fccb0b73b7b7b80bc13e34f904290107b"


def test_stage10_planning_documents_are_synchronized_through_criterion50():
    for text in (README, ROADMAP, PROTOCOL):
        assert "Stage 10G" in text and "completed" in text
        assert "criteria 1–50" in text.lower()
        assert SELECTED_STAGE10 in text
        assert SELECTED_STAGE11 in text
        assert "measurement_covariant" in text


def test_stage11_is_selected_without_claiming_general_covariance():
    for text in (README, ROADMAP, PROTOCOL, CHECKPOINT):
        assert SELECTED_STAGE11 in text
        assert "general covariance" in text
    assert "parametrized covariance precursor != general relativity" in README
    assert "parametrized covariance precursor != general relativity" in ROADMAP


def test_criterion50_external_validation_is_recorded():
    for text in (README, ROADMAP, PROTOCOL, CHECKPOINT):
        assert "#1271" in text
        assert "868 passed in 345.59s" in text
    assert "criterion 50 satisfied externally" in CHECKPOINT.lower()
    assert VALIDATED_HEAD in README
    assert VALIDATED_HEAD in ROADMAP
    assert VALIDATED_HEAD in PROTOCOL
    assert VALIDATED_HEAD in CHECKPOINT
    assert "behind 0" in CHECKPOINT
    assert "mergeable = true" in CHECKPOINT


def test_final_checkpoint_preserves_historical_boundaries():
    assert "Stage 9 checkpoint" in README
    assert "Stage 9C" in README and "not_established" in README
    assert "Stage 9 checkpoint" in ROADMAP
    assert "Stage 9C" in ROADMAP and "not_established" in ROADMAP
    assert "full per-continuation probability covariance = not_established" in PROTOCOL
    assert "weighted/modal/update covariance = not_established" in PROTOCOL


def test_merge_readiness_is_not_a_merge_action():
    assert "merge-ready != merged" in README
    assert "merge-ready != merged" in ROADMAP
    assert "merge-ready != merged" in PROTOCOL
    assert "merge-ready != merged" in CHECKPOINT
    assert "repository validation != new scientific evidence" in CHECKPOINT
