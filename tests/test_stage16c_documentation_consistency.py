from pathlib import Path

SCIENTIFIC_HEAD = "04deb0ae259cee8cf40ec606b77d2972f5c0ab17"
RUN_SUMMARY = "1299 passed in 922.38s (0:15:22)"
BOUNDED_RESULT = (
    "Stage 16C Dirac pair, four-clock complete relational observables, "
    "physical quotient, reachability, and orbit discrimination = established"
)


def _read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def test_stage16c_notes_and_result_pin_scientific_checkpoint_and_evidence():
    for path in ("docs/stage16c_notes.md", "results/stage16c_relational.md"):
        text = _read(path)
        assert SCIENTIFIC_HEAD in text
        assert RUN_SUMMARY in text
        for marker in (
            "5,184",
            "78,732",
            "320",
            "26,244",
            "209,952",
            "1,296",
            "16 / 16",
            "4 / 4",
            "0.5",
            "5.0",
        ):
            assert marker in text
        assert BOUNDED_RESULT in text


def test_stage16c_documents_preserve_reachability_and_interpretation_guards():
    joined = _read("docs/stage16c_notes.md") + _read("results/stage16c_relational.md")
    for guard in (
        "same-orbit reachability != ontological identity",
        "complete relational observable != ontological becoming by definition",
        "Dirac-invariant data + relational change != proof of eternalism",
        "compensated path descent != refoliation invariance",
        "Stage 16C relational descent != Stage 16D basis Abelianization",
        "repository validation != new scientific evidence",
    ):
        assert guard in joined
    assert "derived from" in joined
    assert "independent nonlinear solves" in joined


def test_stage16c_documents_close_only_criteria_25_31():
    joined = (_read("docs/stage16c_notes.md") + _read("results/stage16c_relational.md")).lower()
    assert "criteria 1–31 satisfied" in joined
    assert "criteria 32–50 pending" in joined
    assert "stage 16d" in joined
