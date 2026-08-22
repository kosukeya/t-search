from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_stage10_gate_matches_stage9g_selection() -> None:
    protocol = _read("docs/stage10_protocol.md")
    stage9g = _read("results/stage9g_synthesis_stage10_gate.md")
    roadmap = _read("docs/roadmap.md")
    gate = (
        "Construct and validate a fully typed cross-continuation "
        "future-measurement family under genuine continuation-aware clock changes."
    )
    for text in (protocol, stage9g, roadmap):
        assert gate in text


def test_stage10_freeze_keeps_stage9_carrier_and_reference_measurement_fixed() -> None:
    protocol = _read("docs/stage10_protocol.md")
    checkpoint = _read("results/stage10_0_protocol_freeze.md")
    for text in (protocol, checkpoint):
        assert "QExt(e1)={h_L,h_R}" in text
        assert "future_signature_left" in text
        assert "future_signature_other" in text
        assert "prediction anchor" in text.lower()
        assert "measurement target" in text.lower()
        assert "e1" in text and "e2" in text
    assert "reference h_L-ray effect !=" in checkpoint


def test_stage10_measurement_typing_resources_are_explicit() -> None:
    protocol = _read("docs/stage10_protocol.md")
    for fragment in (
        "measurement-family identity",
        "continuation class / continuation id",
        "prediction anchor",
        "measurement target event",
        "clock perspective",
        "clock reading",
        "outcome identity",
        "outcome semantics / provenance",
        "effect representation",
        "coordinate basis",
        "normalization / inner-product convention",
        "event correspondence",
        "continuation-class correspondence",
        "outcome correspondence",
        "continuation-weight semantics",
    ):
        assert fragment in protocol
    assert "same outcome label != outcome identity" in protocol
    assert "same matrix entries != same typed effect" in protocol


def test_stage10_normalization_is_frozen_as_a_scientific_decision_boundary() -> None:
    protocol = _read("docs/stage10_protocol.md")
    checkpoint = _read("results/stage10_0_protocol_freeze.md")
    for text in (protocol, checkpoint):
        assert "chart-local POVM" in text or "chart-local POVMs" in text
        assert "metric-aware" in text
        assert "sum_o F_o=G" in text
        assert "z^dagger F_o z" in text
        assert "Stage 9C reference" in text
    assert "metric-aware candidate law != established measurement covariance" in protocol
    assert "normalization convention != mere implementation detail" in protocol


def test_stage10_strong_covariance_requires_per_continuation_probability_equality() -> None:
    protocol = _read("docs/stage10_protocol.md")
    checkpoint = _read("results/stage10_0_protocol_freeze.md")
    for text in (protocol, checkpoint):
        assert "p^h" in text
        assert "chi_outcome" in text
        assert "per-continuation" in text.lower()
        assert "before weighting" in text.lower()
    assert "weighted probability equality != per-continuation measurement covariance" in protocol
    assert "effect covariance without outcome typing != full measurement covariance" in protocol


def test_stage10_modal_weight_and_update_layer_is_separate() -> None:
    protocol = _read("docs/stage10_protocol.md")
    assert "M_E^QR=(QRCarrier,e1,h*,q_E)" in protocol
    assert "M_O^QR(e1)=(QRCarrier,e1,QExt(e1),K)" in protocol
    assert "hidden epistemic `h*` swap" in protocol
    assert "weight mismatch" in protocol
    assert "common explicit evidence" in protocol
    assert "measurement covariance != modal/ontological identity" in protocol
    assert "evidence-update covariance != ontological becoming" in protocol


def test_stage10_negative_controls_are_frozen() -> None:
    protocol = _read("docs/stage10_protocol.md")
    required = (
        "bare-effect reuse",
        "wrong-continuation map",
        "swapped continuation classes",
        "swapped/misdeclared outcomes",
        "anchor/target confusion",
        "wrong/missing event correspondence",
        "wrong normalization/metric",
        "weight misalignment",
        "outcome-typing removal",
        "mixed normalization convention",
    )
    for fragment in required:
        assert fragment in protocol
    assert "accidental probability equality != validated covariance" in protocol
    assert "covariance of a wrongly typed measurement != semantic correctness" in protocol


def test_stage10_sequence_and_criterion_allocation_are_frozen() -> None:
    protocol = _read("docs/stage10_protocol.md")
    checkpoint = _read("results/stage10_0_protocol_freeze.md")
    for stage in (
        "Stage 10.0",
        "Stage 10A",
        "Stage 10B",
        "Stage 10C",
        "Stage 10D",
        "Stage 10E",
        "Stage 10F",
        "Stage 10G",
    ):
        assert stage in protocol
        assert stage in checkpoint
    for allocation in (
        "criteria 1–10",
        "criteria 11–16",
        "criteria 17–23",
        "criteria 24–31",
        "criteria 32–38",
        "criteria 39–43",
        "criteria 44–47",
        "criteria 48–49",
    ):
        assert allocation in protocol.lower()
    assert "criteria **1–10**" in checkpoint
    assert "Criteria **11–50 remain future scientific/repository work**" in checkpoint
    assert "criterion 50" in protocol.lower()


def test_stage10_interpretation_guards_block_metaphysical_overclaim() -> None:
    protocol = _read("docs/stage10_protocol.md")
    for guard in (
        "future-measurement covariance != future actuality",
        "future-measurement covariance != ontic future openness",
        "future-measurement covariance != hidden selected future",
        "measurement-covariance failure != ontological becoming",
        "perspective-invariant future probabilities != proof of eternalism",
        "full finite-clock measurement covariance != general covariance",
        "finite-model measurement success != empirical discovery",
        "not_established != false",
    ):
        assert guard in protocol


def test_stage100_checkpoint_is_explicitly_only_a_freeze_checkpoint() -> None:
    checkpoint = _read("results/stage10_0_protocol_freeze.md")
    assert "criteria 1–10 frozen and satisfied" in checkpoint.lower()
    assert "before any Stage 10A" in checkpoint
    assert "Criteria **11–50 remain future scientific/repository work**" in checkpoint
    assert "Stage 10A — typed reference future-measurement family" in checkpoint
