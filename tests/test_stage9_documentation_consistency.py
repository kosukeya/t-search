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
    assert "M_E^Q=(QCarrier,D_*,h*,q_E)" in protocol
    assert "M_O^Q(D_*)=(QCarrier,D_*,QExt(D_*),K)" in protocol
    assert "no selected complete continuation datum exists before update" in protocol.lower()
    assert "directional record arrow != ontological future openness" in protocol
    assert "directional record arrow != ontological becoming" in protocol
    assert "explicit evidence update != ontological becoming" in protocol


def test_stage9_directional_controls_remain_frozen_after_stage9a() -> None:
    protocol = _read("docs/stage9_protocol.md")
    checkpoint = _read("results/stage9_0_protocol_freeze.md")
    for text in (protocol, checkpoint):
        for control in ("Forward", "Reversed", "Balanced", "No-record"):
            assert control.lower() in text.lower()
    assert "order != directional record arrow" in protocol


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


def test_stage9_sequence_and_exit_criteria_advance_through_stage9a_only() -> None:
    protocol = _read("docs/stage9_protocol.md")
    readme = _read("README.md")
    roadmap = _read("docs/roadmap.md")
    for text in (protocol, readme, roadmap):
        assert "Stage 9A" in text and "completed" in text
        assert "Stage 9B" in text and "next" in text
    assert "Stage 9A closes criteria **11–16**" in protocol
    assert "Criteria 17–50 remain future work" in protocol
    assert "criteria **17–23**: Stage 9B" in protocol
    assert "criterion **50**: external final full-repository regression and merge-readiness review" in protocol


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


def test_stage9_ablation_and_status_vocabulary_remain_explicit() -> None:
    protocol = _read("docs/stage9_protocol.md")
    checkpoint = _read("results/stage9_0_protocol_freeze.md")
    for text in (protocol, checkpoint):
        lowered = text.lower()
        assert "qext" in lowered and "singleton" in lowered
        assert "local record access hidden" in lowered
        assert "event/class correspondence removed" in lowered
        assert "wrong record-observable" in lowered
        for status in ("preserved", "reconstructible", "inaccessible", "lost", "underdetermined", "not_established"):
            assert status in text


def test_readme_records_stage8_as_merged_and_stage9a_as_current_checkpoint() -> None:
    readme = _read("README.md")
    lowered = readme.lower()
    assert "Stages 1–8 are completed and merged" in readme
    assert "stage 9.0 and stage 9a are completed" in lowered
    assert "stage 9b" in lowered and "next" in lowered
    assert "Draft PR #9" not in readme
