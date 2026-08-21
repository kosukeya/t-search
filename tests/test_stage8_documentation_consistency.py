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


def test_stage8_protocol_preserves_selected_vs_unselected_distinction() -> None:
    protocol = _read("docs/stage8_protocol.md")
    assert "M_E^Q=(QCarrier, D, h*, q_E)" in protocol
    assert "M_O^Q(D)=(QCarrier, D, QExt(D), K)" in protocol
    assert "No selected complete continuation datum may exist before update" in protocol
    assert "hidden selected continuation must not be consulted" in protocol


def test_stage8_randomness_and_integration_guards_remain_explicit() -> None:
    protocol = _read("docs/stage8_protocol.md")
    concepts = _read("docs/stage8_concepts.md")
    for guard in (
        "Potentiality != quantum randomness by definition",
        "Potentiality != superposition by definition",
        "Potentiality != Born probability by definition",
        "density matrix decomposition != unique modal semantics",
    ):
        assert guard in protocol or guard in concepts
    assert "typed modal wrapper beside quantum model != quantum-modal integration" in protocol
    assert "physically admissible quantum continuation" in protocol


def test_stage8_current_sequence_and_stage80_historical_checkpoint_agree() -> None:
    protocol = _read("docs/stage8_protocol.md")
    checkpoint = _read("results/stage8_0_protocol_freeze.md")
    for stage in ("8A", "8B", "8C", "8D", "8E", "8F", "8G"):
        assert f"Stage {stage}" in protocol and "completed" in protocol
    assert "Stage 9 — directional records with nontrivial quantum Potentiality — selected next gate" in protocol
    assert "Stage 8A — common quantum-extension substrate — next" in checkpoint


def test_stage8_exit_criteria_advance_through_stage8g_but_keep_50_external() -> None:
    protocol = _read("docs/stage8_protocol.md")
    stage8a = _read("results/stage8a_quantum_extensions.md")
    stage8b = _read("results/stage8b_typed_modal_models.md")
    stage8c = _read("results/stage8c_operational_update.md")
    stage8d = _read("results/stage8d_modal_transport.md")
    stage8e = _read("results/stage8e_compatibility.md")
    stage8f = _read("results/stage8f_ablation.md")
    stage8g = _read("results/stage8g_synthesis_stage9_gate.md")

    assert "Stage 8A satisfies criteria 11–16" in protocol
    assert "Stage 8B satisfies criteria 17–21" in protocol
    assert "Stage 8C satisfies criteria 22–29" in protocol
    assert "Stage 8D closes criteria **30–35**" in protocol
    assert "Stage 8E closes criteria **36–41**" in protocol
    assert "Stage 8F closes criteria **42–47**" in protocol
    assert "Stage 8G closes criteria **48–49**" in protocol
    assert "Criterion **50** is external" in protocol
    assert "criteria **11–16**" in stage8a
    assert "criteria **17–21**" in stage8b
    assert "criteria **22–29**" in stage8c
    assert "criteria **30–35**" in stage8d
    assert "criteria **36–41**" in stage8e
    assert "criteria **42–47**" in stage8f
    assert "Criteria 48–49" in stage8g
    assert "Criterion 50 is external" in stage8g


def test_stage8a_checkpoint_has_real_qext_not_only_labels() -> None:
    results = _read("results/stage8a_quantum_extensions.md")
    assert "QExt(e1) = {h_L, h_R}" in results
    assert "future-operator Frobenius residual = `4`" in results
    assert "normalized `e2` state overlap squared = `0`" in results


def test_stage8b_checkpoint_uses_same_qext_with_distinct_selected_semantics() -> None:
    notes = _read("docs/stage8b_notes.md")
    results = _read("results/stage8b_typed_modal_models.md")
    for text in (notes, results):
        assert "h_L" in text and "h_R" in text
        assert "Epistemic" in text and "Ontic" in text
    assert "EpistemicQuantumPotentiality" in notes
    assert "OnticExtensionQuantumPotentiality" in notes


def test_stage8c_checkpoint_records_full_oq_mismatch_and_explicit_update() -> None:
    results = _read("results/stage8c_operational_update.md")
    for fragment in (
        "future_signature_0",
        "(0.5,0.5)",
        "(0.75,0.25)",
        "QExt(e2)=empty",
        "full declared `O_Q` views agree",
        "pre-existing `h*=h_L` preserved",
        "612 passed in 203.50s",
    ):
        assert fragment in results


def test_stage8d_checkpoint_records_genuine_continuation_aware_transport() -> None:
    protocol = _read("docs/stage8_protocol.md")
    notes = _read("docs/stage8d_notes.md")
    results = _read("results/stage8d_modal_transport.md")
    for text in (protocol, notes, results):
        assert "108" in text
        assert "324" in text
        assert "P-V covariance != P=V" in text
        assert "equal numeric clock readings != event identity" in text
        assert "full Stage 8C measurement covariance" in text
        assert "not_established" in text
    for fragment in (
        "7.406835737661463e-16",
        "3.627704160496353e-15",
        "1.0000000000000002",
        "0.9128709291752769",
        "1.1547005383792515",
        "634 passed in 131.34s",
        "renamed representative",
    ):
        assert fragment in results


def test_stage8e_checkpoint_records_compatibility_and_underdetermination() -> None:
    protocol = _read("docs/stage8_protocol.md")
    notes = _read("docs/stage8e_notes.md")
    results = _read("results/stage8e_compatibility.md")
    for text in (protocol, notes, results):
        assert "P-O(event effects)" in text
        assert "P-R(current record)" in text
        assert "R(current)-V" in text
        assert "O=>R(direction)" in text
        assert "P/O/current-R=>V semantics" in text
        assert "full P/O/directional-R/V" in text
        assert "covariance of a wrongly typed observable != semantic correctness" in text
    assert "650 passed / 1 failed" in results
    assert "record score = 0" in notes
    assert "record score `+1`" in notes


def test_stage8f_checkpoint_records_ablation_reconstruction_and_mismatch_results() -> None:
    protocol = _read("docs/stage8_protocol.md")
    notes = _read("docs/stage8f_notes.md")
    results = _read("results/stage8f_ablation.md")
    for text in (protocol, notes, results):
        assert "record-neutral" in text.lower()
        assert "reconstructible" in text
        assert "underdetermined" in text
        assert "inaccessible" in text
        assert "lost" in text
        assert "not_established" in text
        assert "108" in text
        assert "record-neutral V witness != universal R-V independence theorem" in text
        assert "P-V map reconstruction != P=V" in text
        assert "full Stage 8C measurement covariance" in text
    assert "record coupling neutralized" in results
    assert "QExt collapsed to singleton" in results
    assert "weights unfixed" in results
    assert "event/class correspondence removed" in results
    assert "current record access hidden" in results
    assert "662 passed in 139.81s" in results


def test_stage8g_checkpoint_records_refined_candidate_and_unique_stage9_gate() -> None:
    protocol = _read("docs/stage8_protocol.md")
    notes = _read("docs/stage8g_notes.md")
    results = _read("results/stage8g_synthesis_stage9_gate.md")
    for text in (protocol, notes, results):
        assert "refined_layered" in text
        assert "R=(R_content,R_direction,R_access)" in text
        assert "V=(V_extension,V_semantics,V_weights)" in text
        assert "directional_record_potentiality" in text
        assert "full_measurement_covariance" in text
        assert "parametrized_covariance_precursor" in text
        assert "directional record" in text.lower()
        assert "ontological future openness" in text
    assert "score 9" in results
    assert "score 6" in results
    assert "selected as the next finite-model gate" in results.lower() or "Selected Stage 9 gate" in results


def test_stage8g_planning_documents_point_to_stage9_and_defer_gravity() -> None:
    readme = _read("README.md")
    roadmap = _read("docs/roadmap.md")
    concepts = _read("docs/stage8_concepts.md")
    protocol = _read("docs/stage8_protocol.md")
    for text in (readme, roadmap, concepts, protocol):
        assert "Stage 8G" in text
        assert "48–49" in text
        assert "50" in text
        assert "directional" in text.lower()
    assert "## Stage 9 — Directional records with nontrivial quantum Potentiality — selected next gate" in roadmap
    assert "## Stage 10 — Generally covariant / gravitational extension — deferred gate" in roadmap
    assert "Earlier roadmap versions placed the generally covariant / gravitational extension at Stage 9" in roadmap


def test_roadmap_keeps_stage7_historical_deferral_and_stage8_selected_gate() -> None:
    roadmap = _read("docs/roadmap.md")
    assert "## Stage 8 — Quantum Potentiality inside the shared constrained construction" in roadmap
    assert "Potentiality != quantum randomness by definition" in roadmap
    assert "Earlier roadmap versions assigned Stage 7 directly" in roadmap
