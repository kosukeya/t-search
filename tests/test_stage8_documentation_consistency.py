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


def test_stage8_randomness_guards_remain_explicit() -> None:
    protocol = _read("docs/stage8_protocol.md")
    concepts = _read("docs/stage8_concepts.md")
    for guard in (
        "Potentiality != quantum randomness by definition",
        "Potentiality != superposition by definition",
        "Potentiality != Born probability by definition",
        "density matrix decomposition != unique modal semantics",
    ):
        assert guard in protocol or guard in concepts
    assert "Potentiality != quantum randomness by definition" in protocol
    assert "Potentiality != quantum randomness by definition" in concepts


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
    assert "Stage 8A — common quantum-extension substrate — completed" in protocol
    assert "Stage 8B — typed epistemic and ontic-extension quantum models — completed" in protocol
    assert "Stage 8C — operational underdetermination and explicit update — completed" in protocol
    assert "Stage 8D — genuine clock-change modal transport — next" in protocol

    # Stage 8.0 remains an immutable historical checkpoint of what was next then.
    assert "Stage 8A — common quantum-extension substrate — next" in checkpoint


def test_stage8_exit_criteria_advance_only_through_stage8c() -> None:
    protocol = _read("docs/stage8_protocol.md")
    stage8a = _read("results/stage8a_quantum_extensions.md")
    stage8b = _read("results/stage8b_typed_modal_models.md")
    stage8c = _read("results/stage8c_operational_update.md")

    assert "Stage 8A satisfies criteria 11–16" in protocol
    assert "Stage 8B satisfies criteria 17–21" in protocol
    assert "Stage 8C satisfies criteria 22–29" in protocol
    assert "Criteria 30–50 remain future scientific work" in protocol
    assert "criteria **11–16**" in stage8a
    assert "criteria **17–21**" in stage8b
    assert "Criteria 22–50 remain future scientific work" in stage8b
    assert "criteria **22–29**" in stage8c
    assert "criteria **30–50**" in stage8c


def test_stage8a_checkpoint_has_real_qext_not_only_labels() -> None:
    results = _read("results/stage8a_quantum_extensions.md")
    assert "QExt(e1) = {h_L, h_R}" in results
    assert "future-operator Frobenius residual = `4`" in results
    assert "normalized `e2` state overlap squared = `0`" in results
    assert "memory" in results and "record" in results


def test_stage8b_checkpoint_uses_same_qext_with_distinct_selected_semantics() -> None:
    protocol = _read("docs/stage8_protocol.md")
    notes = _read("docs/stage8b_notes.md")
    results = _read("results/stage8b_typed_modal_models.md")
    for text in (protocol, notes, results):
        assert "h_L" in text and "h_R" in text
        assert "Epistemic" in text and "Ontic" in text
    assert "same carrier object" in protocol
    assert "EpistemicQuantumPotentiality" in notes
    assert "OnticExtensionQuantumPotentiality" in notes
    assert "no selected continuation field != proof of ontic openness in nature" in protocol
    assert "Stage 8B pre-discriminating view != full Stage 8C O_Q interface" in protocol


def test_stage8c_checkpoint_records_full_oq_mismatch_and_explicit_update() -> None:
    protocol = _read("docs/stage8_protocol.md")
    notes = _read("docs/stage8c_notes.md")
    results = _read("results/stage8c_operational_update.md")

    for text in (protocol, notes, results):
        assert "future_signature_0" in text
        assert "(0.5,0.5)" in text
        assert "(0.75,0.25)" in text
        assert "QExt(e2)=empty" in text
    assert "full declared `O_Q` views agree" in results
    assert "pre-existing `h*=h_L` preserved" in results
    assert "no selected/selector/seed/singleton-continuation datum" in results
    assert "same current superposition, density matrix, and matched Born prediction" in results
    assert "612 passed in 203.50s" in results


def test_stage8c_planning_documents_point_to_stage8d_next() -> None:
    readme = _read("README.md")
    roadmap = _read("docs/roadmap.md")
    for text in (readme, roadmap):
        assert "Stage 8C" in text and "completed" in text
        assert "Stage 8D" in text and "next" in text
        assert "criteria 22–29" in text
        assert "Criteria 30–50 remain future scientific work" in text


def test_roadmap_keeps_selected_stage8_and_deferred_stage9_gravity() -> None:
    roadmap = _read("docs/roadmap.md")
    assert "## Stage 8 — Quantum Potentiality inside the shared constrained construction" in roadmap
    assert "## Stage 9 — Generally covariant / gravitational extension — deferred gate" in roadmap
    assert "Potentiality != quantum randomness by definition" in roadmap
    assert "Earlier roadmap versions assigned Stage 7 directly" in roadmap
