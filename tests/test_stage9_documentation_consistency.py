from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_stage9_gate_matches_stage8g_selection() -> None:
    protocol = _read("docs/stage9_protocol.md")
    stage8g = _read("results/stage8g_synthesis_stage9_gate.md")
    gate = "Integrate directional record formation with nontrivial quantum Potentiality in one constrained continuation family."
    assert gate in stage8g
    assert gate in protocol
    assert "directional_record_potentiality" in stage8g


def test_stage9_protocol_preserves_refined_r_and_v_typing() -> None:
    protocol = _read("docs/stage9_protocol.md")
    assert "R=(R_content,R_direction,R_access)" in protocol
    assert "V=(V_extension,V_semantics,V_weights)" in protocol
    assert "record content != directional record arrow" in protocol
    assert "underdetermined != ontically open" in protocol


def test_stage9_strong_integration_requires_nontrivial_v_and_per_continuation_direction() -> None:
    protocol = _read("docs/stage9_protocol.md")
    checkpoint = _read("results/stage9_0_protocol_freeze.md")
    for text in (protocol, checkpoint):
        assert "|QExt(D_*)| >= 2" in text
        assert "A_R(h,D_*)" in text
        assert "continuation identity != record-direction identity" in text
        assert "weighted directional score != continuation-independent directional structure" in text


def test_stage9_modal_distinction_is_not_decided_by_direction() -> None:
    protocol = _read("docs/stage9_protocol.md")
    assert "M_E^QR=(QRCarrier,D_*,h*,q_E)" in protocol
    assert "M_O^QR(D_*)=(QRCarrier,D_*,QExt(D_*),K)" in protocol
    assert "no selected complete continuation datum exists before or after" in protocol.lower()
    assert "operational directional equality != modal/ontological identity" in protocol
    assert "directional record arrow != ontological future openness" in protocol
    assert "directional record arrow != ontological becoming" in protocol
    assert "explicit evidence update != ontological becoming" in protocol


def test_stage9_directional_controls_remain_typed_after_stage9b() -> None:
    protocol = _read("docs/stage9_protocol.md")
    checkpoint = _read("results/stage9_0_protocol_freeze.md")
    for text in (protocol, checkpoint):
        for control in ("Forward", "Reversed", "Balanced", "No-record"):
            assert control.lower() in text.lower()
    assert "order != directional record arrow" in protocol
    assert "balanced mixture != pure constrained history" in protocol
    assert "reversed diagnostic sign != reversed Python iteration" in protocol


def test_stage9_clock_transport_keeps_event_class_and_observable_typing_explicit() -> None:
    protocol = _read("docs/stage9_protocol.md")
    for fragment in (
        "S^h_{Y<-X}(k,j)=R^h_Y(k)E^h_X(j)",
        "event correspondence",
        "continuation/class correspondence",
        "equal numeric clock readings != event identity",
        "covariance of a wrongly typed observable != semantic correctness",
    ):
        assert fragment in protocol


def test_stage9_r_direction_v_questions_are_split_not_collapsed() -> None:
    protocol = _read("docs/stage9_protocol.md")
    for fragment in (
        "`R_direction` with `V_extension`",
        "`R_direction` with `V_weights`",
        "`R_direction` with `V_semantics`",
        "`R_access` with `V`",
        "`P-R_direction-V`",
        "`O-R_direction-V`",
    ):
        assert fragment in protocol


def test_stage9_sequence_and_exit_criteria_advance_through_stage9g() -> None:
    protocol = _read("docs/stage9_protocol.md")
    readme = _read("README.md")
    roadmap = _read("docs/roadmap.md")
    for text in (protocol, readme, roadmap):
        for stage in (
            "Stage 9A",
            "Stage 9B",
            "Stage 9C",
            "Stage 9D",
            "Stage 9E",
            "Stage 9F",
            "Stage 9G",
        ):
            assert stage in text and "completed" in text
        assert "criterion 50" in text.lower()
    assert "Stage 9G closes **48–49**" in protocol
    assert "Criterion 50 remains future work" in protocol
    assert "criterion **50**: external final full-repository regression and merge-readiness review" in protocol
    selected = "Construct and validate a fully typed cross-continuation future-measurement family under genuine continuation-aware clock changes."
    assert selected in protocol
    assert selected in readme
    assert selected in roadmap


def test_stage90_checkpoint_remains_a_historical_freeze_record() -> None:
    checkpoint = _read("results/stage9_0_protocol_freeze.md")
    lowered = checkpoint.lower()
    assert "historical protocol-freeze checkpoint" in checkpoint
    assert "only criteria **1–10** were frozen as completed" in checkpoint
    assert "criteria **11–50 remained future scientific work**" in checkpoint
    assert "stage 9a later closes criteria 11–16" in lowered


def test_stage9a_checkpoint_records_common_directional_v_substrate() -> None:
    notes = _read("docs/stage9a_notes.md")
    results = _read("results/stage9a_directional_substrate.md")
    protocol = _read("docs/stage9_protocol.md")
    for text in (notes, results, protocol):
        assert "QExt(e1)" in text
        assert "h_L" in text and "h_R" in text
        assert "U_scr U_rec" in text
        assert "Z_C U_scr U_rec" in text
        assert "continuation identity != record-direction identity" in text
        assert "directional record arrow != ontological future openness" in text
    assert "physical dimension = `14`" in results
    assert "minimum reduction rank" in results and "`14`" in results
    assert "695 passed in 199.79s" in results


def test_stage9b_checkpoint_records_exact_directional_control_family() -> None:
    notes = _read("docs/stage9b_notes.md")
    results = _read("results/stage9b_directional_controls.md")
    protocol = _read("docs/stage9_protocol.md")
    for text in (notes, results, protocol):
        assert "(+1,+0.5)" in text
        assert "(-1,-0.5)" in text
        assert "balanced" in text.lower()
        assert "no-record" in text.lower()
        assert "balanced mixture != pure constrained history" in text
        assert "continuation identity != record-direction identity" in text
        assert "directional record arrow != ontological future openness" in text
    assert "balanced zero R_direction != no R_content" in results
    assert "criteria 17–23" in results.lower()
    assert "708 passed in 196.73s" in results


def test_stage9c_checkpoint_records_directional_modal_underdetermination() -> None:
    notes = _read("docs/stage9c_notes.md")
    results = _read("results/stage9c_directional_modal.md")
    protocol = _read("docs/stage9_protocol.md")
    for text in (notes, results, protocol):
        assert "O_QR" in text
        assert "M_E^QR" in text
        assert "M_O^QR" in text
        assert "operational directional equality != modal/ontological identity" in text
        assert "control of V_weights != determination of V_semantics" in text
        assert "directional record arrow != ontological future openness" in text
    assert "criteria 24–30" in results.lower()
    assert "720 passed in 265.06s" in results
    assert "K=(0.75,0.25)" in results


def test_stage9d_checkpoint_records_typed_continuation_aware_clock_transport() -> None:
    notes = _read("docs/stage9d_notes.md")
    results = _read("results/stage9d_clock_transport.md")
    protocol = _read("docs/stage9_protocol.md")
    for text in (notes, results, protocol):
        assert "18" in text and "108" in text and "324" in text
        assert "rank" in text.lower() and "14" in text
        assert "perspective change != temporal-direction reversal" in text
        assert "covariance of a wrongly typed observable != semantic correctness" in text
        assert "full Stage 9C future" in text and "not_established" in text
        assert "finite clock covariance != general covariance" in text
    assert "criteria 31–36" in results.lower()
    assert "733 passed in 372.31s" in results
    assert "(+1,+0.5)" in results
    assert "(-1,-0.5)" in results


def test_stage9e_checkpoint_records_compatibility_matrix_and_constraints() -> None:
    notes = _read("docs/stage9e_notes.md")
    results = _read("results/stage9e_compatibility.md")
    protocol = _read("docs/stage9_protocol.md")
    for text in (notes, results, protocol):
        for relation in (
            "R_direction-V_extension",
            "R_direction-V_weights",
            "R_direction-V_semantics",
            "R_access-V",
            "P-R_direction-V",
            "O-R_direction-V",
        ):
            assert relation in text
        assert "compatible" in text
        assert "underdetermined" in text
        assert "implication_refuted" in text
        assert "direct" in text and "Xi_RV" in text and "not_established" in text
        assert "full Stage 9C future" in text and "not_established" in text
        assert "accessible canonical R_access-V compatibility != accessibility independence" in text
        assert "directional record arrow != ontological becoming" in text
    assert "criteria 37–42" in results.lower()
    assert "743 passed in 404.42s" in results


def test_stage9f_checkpoint_records_ablation_reconstruction_and_accessibility() -> None:
    notes = _read("docs/stage9f_notes.md")
    results = _read("results/stage9f_ablation.md")
    protocol = _read("docs/stage9_protocol.md")
    for text in (notes, results, protocol):
        lowered = text.lower()
        assert "scrambler neutralized" in lowered
        assert "singleton" in lowered
        assert "R_content" in text and "R_direction" in text and "R_access" in text
        assert "reconstructible" in text
        assert "inaccessible" in text
        assert "underdetermined" in text
        assert "not_established" in text
        assert "record content != directional record arrow" in text
        assert "local P transport without chi != typed event/class identification" in text
        assert "covariance of a wrongly typed observable != semantic correctness" in text
        assert "directional record arrow != ontological becoming" in text
    assert "criteria 43–47" in results.lower()
    assert "A_acc=0 != inaccessible record content" in results
    assert "108" in results and "54" in results
    assert "754 passed in 438.94s" in results


def test_stage9g_checkpoint_records_synthesis_and_selected_stage10_gate() -> None:
    notes = _read("docs/stage9g_notes.md")
    results = _read("results/stage9g_synthesis_stage10_gate.md")
    protocol = _read("docs/stage9_protocol.md")
    readme = _read("README.md")
    roadmap = _read("docs/roadmap.md")
    selected = "Construct and validate a fully typed cross-continuation future-measurement family under genuine continuation-aware clock changes."
    for text in (notes, results, protocol, readme, roadmap):
        assert "refined_layered" in text
        assert "full_measurement_covariance" in text
        assert selected in text
        assert "finite-family bidirectional countermodels != universal R-V independence theorem" in text
        assert "P edge reconstruction != P layer universally redundant" in text
        assert "full Stage 9C future-measurement covariance remains not_established" in text
        assert "finite clock covariance != general covariance" in text
    assert "criteria 48–49" in results.lower()
    assert "765 passed in 248.81s" in results
    assert "755 passed in 348.67s" in results
    assert "criterion **50**" in results
    assert "not yet closed" in results.lower()
    assert "parametrized_covariance_precursor" in results
    assert "nonideal_povm_clocks" in results


def test_stage9_ablation_and_status_vocabulary_remain_explicit() -> None:
    protocol = _read("docs/stage9_protocol.md")
    checkpoint = _read("results/stage9_0_protocol_freeze.md")
    for text in (protocol, checkpoint):
        lowered = text.lower()
        assert "qext" in lowered and "singleton" in lowered
        assert "local record access hidden" in lowered
        assert "event/class correspondence removed" in lowered
        assert "wrong record-observable" in lowered
        for status in (
            "preserved",
            "reconstructible",
            "inaccessible",
            "lost",
            "underdetermined",
            "not_established",
        ):
            assert status in text


def test_readme_records_stage8_as_merged_and_stage9g_as_current_checkpoint() -> None:
    readme = _read("README.md")
    lowered = readme.lower()
    assert "Stages 1–8 are completed and merged" in readme
    assert "stage 9.0 through stage 9g are completed" in lowered
    assert "criterion 50" in lowered and "next" in lowered
    assert "765 passed in 248.81s" in readme
    assert "755 passed in 348.67s" in readme
    assert "Draft PR #9" not in readme
