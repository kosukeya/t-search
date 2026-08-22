from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_stage7_gate_matches_stage6g_selection() -> None:
    protocol = _read("docs/stage7_protocol.md")
    stage6g = _read("results/stage6g_synthesis_stage7_gate.md")

    selected = "Add explicit memory/record subsystems to the constrained multi-clock quantum model."
    assert selected in stage6g
    assert "explicit memory degree of freedom" in protocol
    assert "genuine clock changes" in protocol


def test_roadmap_no_longer_assigns_gravity_to_stage7_and_tracks_later_reranking() -> None:
    roadmap = _read("docs/roadmap.md")

    assert "## Stage 7 — Quantum records inside a constrained multi-clock model" in roadmap
    assert "## Stage 7 — Generally covariant / gravitational extension" not in roadmap
    assert "## Stage 10 — Fully typed future-measurement covariance — selected next gate" in roadmap
    assert "## Stage 11 — Parametrized / generally covariant / gravitational extension — deferred gate" in roadmap
    assert "Earlier roadmap versions assigned Stage 7 directly" in roadmap
    assert "Gravity/general covariance is deferred, not abandoned" in roadmap


def test_stage7_protocol_marks_old_roadmap_as_superseded() -> None:
    protocol = _read("docs/stage7_protocol.md")
    concepts = _read("docs/stage7_concepts.md")
    checkpoint = _read("results/stage7_0_protocol_freeze.md")

    assert "superseded by the Stage 6G gate selection" in protocol
    assert "memory present != record present" in protocol
    assert "entanglement != record" in protocol
    assert "physical-subspace automorphism != time-localized dynamical interaction" in concepts
    assert "generally covariant / gravitational extension" in checkpoint


def test_core_planning_documents_contain_no_old_stage7_header() -> None:
    for relative in (
        "README.md",
        "docs/roadmap.md",
        "docs/stage6_protocol.md",
        "docs/stage6g_notes.md",
        "results/stage6g_synthesis_stage7_gate.md",
        "docs/stage7_protocol.md",
        "results/stage7_0_protocol_freeze.md",
    ):
        assert "## Stage 7 — Generally covariant / gravitational extension" not in _read(relative)
