from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_stage8_gate_matches_stage7g_selection() -> None:
    protocol = _read("docs/stage8_protocol.md")
    stage7g = _read("results/stage7g_synthesis_stage8_gate.md")

    for fragment in (
        "Potentiality / extension semantics `V`",
        "same constrained quantum construction",
    ):
        assert fragment in stage7g
        assert fragment in protocol


def test_stage8_protocol_preserves_stage2_selected_vs_unselected_distinction() -> None:
    protocol = _read("docs/stage8_protocol.md")

    assert "M_E^Q=(QCarrier, D, h*, q_E)" in protocol
    assert "M_O^Q(D)=(QCarrier, D, QExt(D), K)" in protocol
    assert "No selected complete continuation datum may exist before update" in protocol
    assert "hidden selected continuation must not be consulted" in protocol


def test_stage8_protocol_does_not_define_potentiality_as_quantum_randomness() -> None:
    protocol = _read("docs/stage8_protocol.md")
    concepts = _read("docs/stage8_concepts.md")

    for guard in (
        "Potentiality != quantum randomness by definition",
        "Potentiality != superposition by definition",
        "Potentiality != Born probability by definition",
        "density matrix decomposition != unique modal semantics",
    ):
        assert guard in protocol
        assert guard in concepts


def test_stage8_integration_requires_executable_quantum_continuations() -> None:
    protocol = _read("docs/stage8_protocol.md")
    concepts = _read("docs/stage8_concepts.md")

    assert "typed modal wrapper beside quantum model != quantum-modal integration" in protocol
    assert "QExt(D)" in protocol
    assert "physically admissible quantum continuation" in protocol
    assert "product decoration != integrated layer" in concepts


def test_stage8_current_sequence_and_stage80_historical_checkpoint_agree() -> None:
    protocol = _read("docs/stage8_protocol.md")
    checkpoint = _read("results/stage8_0_protocol_freeze.md")

    assert "Stage 8.0 — Quantum Potentiality protocol freeze — completed" in protocol
    assert "Stage 8A — common quantum-extension substrate — completed" in protocol
    assert "Stage 8B — typed epistemic and ontic-extension quantum models — next" in protocol

    # The Stage 8.0 checkpoint remains an immutable historical record of what was next then.
    assert "Stage 8.0 — Quantum Potentiality protocol freeze — completed" in checkpoint
    assert "Stage 8A — common quantum-extension substrate — next" in checkpoint


def test_stage8_exit_criteria_advance_only_through_stage8a() -> None:
    protocol = _read("docs/stage8_protocol.md")
    checkpoint = _read("results/stage8_0_protocol_freeze.md")
    stage8a = _read("results/stage8a_quantum_extensions.md")

    assert "Stage 8 defines 50 exit criteria" in checkpoint
    assert "criteria 1–10 only" in checkpoint
    assert "Criteria 11–50 remain future scientific work" in checkpoint
    assert "Stage 8A satisfies criteria 11–16" in protocol
    assert "Criteria 17–50 remain future scientific work" in protocol
    assert "criteria **11–16**" in stage8a


def test_stage8a_checkpoint_has_real_qext_not_only_labels() -> None:
    protocol = _read("docs/stage8_protocol.md")
    notes = _read("docs/stage8a_notes.md")
    results = _read("results/stage8a_quantum_extensions.md")

    for text in (protocol, notes, results):
        assert "QExt(e1) = {h_L, h_R}" in text
        assert "memory" in text
        assert "record" in text
    assert "future-operator Frobenius residual = `4`" in results
    assert "normalized `e2` state overlap squared = `0`" in results


def test_roadmap_keeps_selected_stage8_and_deferred_stage9_gravity() -> None:
    roadmap = _read("docs/roadmap.md")

    assert "## Stage 8 — Quantum Potentiality inside the shared constrained construction" in roadmap
    assert "## Stage 9 — Generally covariant / gravitational extension — deferred gate" in roadmap
    assert "Potentiality != quantum randomness by definition" in roadmap
