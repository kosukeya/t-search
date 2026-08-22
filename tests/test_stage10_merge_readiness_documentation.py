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


def test_stage10_planning_documents_are_synchronized_through_stage10g():
    for text in (README, ROADMAP, PROTOCOL):
        assert "Stage 10G" in text and "completed" in text
        assert "criteria 1–49" in text.lower()
        assert SELECTED_STAGE10 in text
        assert SELECTED_STAGE11 in text
        assert "measurement_covariant" in text


def test_stage11_is_selected_without_claiming_general_covariance():
    for text in (README, ROADMAP, PROTOCOL, CHECKPOINT):
        assert SELECTED_STAGE11 in text
        assert "finite clock covariance != general covariance" in text or "general covariance" in text
    assert "parametrized covariance precursor != general relativity" in README
    assert "parametrized covariance precursor != general relativity" in ROADMAP


def test_criterion50_is_explicitly_pending_before_external_regression():
    assert "criterion 50" in README.lower() and "remaining" in README.lower()
    assert "criterion 50" in ROADMAP.lower() and "remains" in ROADMAP.lower()
    assert "criterion 50" in PROTOCOL.lower() and "pending" in PROTOCOL.lower()
    assert "final external full-repository regression pending" in CHECKPOINT.lower()


def test_final_checkpoint_does_not_rewrite_historical_boundaries():
    assert "Stage 9 checkpoint" in README
    assert "Stage 9C" in README and "not_established" in README
    assert "Stage 9 checkpoint" in ROADMAP
    assert "Stage 9C" in ROADMAP and "not_established" in ROADMAP
    assert "full per-continuation probability covariance = not_established" in PROTOCOL
    assert "weighted/modal/update covariance = not_established" in PROTOCOL


def test_merge_readiness_guard_is_not_merge_action():
    assert "merge-ready != merged" in CHECKPOINT
    assert "repository validation != new scientific evidence" in CHECKPOINT
