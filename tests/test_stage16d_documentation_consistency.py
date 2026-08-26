from pathlib import Path

SCIENTIFIC_HEAD = "16a26c4ea08b315af4581cbdc5550649703951d8"
VALIDATION_HEAD = "85b8312a958e66b17d5d0e11837de2d8f938dc01"
RUN_SUMMARY = "1310 passed in 700.22s (0:11:40)"
BOUNDED_CLASSIFICATION = "only_nonlocal_abelianization_witness_found_in_frozen_search"
BOUNDED_RESULT = (
    "Stage 16D closed-cycle locality-preserving Abelianization pressure test: "
    "only nonlocal Abelianization witnesses were found in the frozen search, "
    "with no L0/L1/depth<=4 local witness and an exact no-solution certificate "
    "for the frozen affine cyclic L1 ansatz."
)


def _read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def test_stage16d_notes_and_result_pin_checkpoint_and_evidence():
    for path in ("docs/stage16d_notes.md", "results/stage16d_basis.md"):
        text = _read(path)
        assert SCIENTIFIC_HEAD in text
        assert VALIDATION_HEAD in text
        assert RUN_SUMMARY in text
        for marker in (
            "21",
            "3 L0",
            "16 one-step L1",
            "0.09375",
            "3/32",
            "69,904",
            "7/32",
            "0.21875",
            "12 parameters",
            "608",
            "137",
            "(1)",
            "21 / 21",
            BOUNDED_CLASSIFICATION,
        ):
            assert marker in text
        assert BOUNDED_RESULT in text


def test_stage16d_documents_record_bounded_negative_semantics_and_guards():
    joined = _read("docs/stage16d_notes.md") + _read("results/stage16d_basis.md")
    for guard in (
        "known global Abelianization != proof that all Abelianizations are nonlocal",
        "no L1 witness in frozen search != no L1 Abelianization exists",
        "only nonlocal witness found != fundamental physical non-Abelianity",
        "global Abelianization != physical triviality",
        "failure to Abelianize != ontological becoming",
        "Stage 16D basis equivalence != refoliation invariance",
        "repository validation != new scientific evidence",
    ):
        assert guard in joined
    assert "universal" in joined
    assert "#2032" in joined
    assert "2 failed, 1308 passed" in joined


def test_stage16d_documents_close_only_criteria_32_39():
    joined = (_read("docs/stage16d_notes.md") + _read("results/stage16d_basis.md")).lower()
    assert "criteria 1–39 satisfied" in joined or "1–39 satisfied" in joined
    assert "criteria 40–50 pending" in joined or "40–50 pending" in joined
    assert "stage 16e" in joined
