from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")
ROADMAP = (ROOT / "docs" / "roadmap.md").read_text(encoding="utf-8")
PROTOCOL = (ROOT / "docs" / "stage11_protocol.md").read_text(encoding="utf-8")
FREEZE = (ROOT / "results" / "stage11_0_protocol_freeze.md").read_text(encoding="utf-8")
NOTES_A = (ROOT / "docs" / "stage11a_notes.md").read_text(encoding="utf-8")
RESULT_A = (ROOT / "results" / "stage11a_parametrized.md").read_text(encoding="utf-8")

SELECTED_STAGE11 = (
    "Construct a parametrized covariance precursor that preserves the typed "
    "O/P/R/V measurement architecture without assuming a preferred external "
    "time parameterization."
)
STAGE10_MERGE = "4a322634a5b83e416d374ee18e96ac6c7a5c88ba"


def test_stage10_merge_and_stage11_gate_are_synchronized() -> None:
    assert "Stages 1–10 are completed and merged" in README
    assert STAGE10_MERGE in README
    assert "Stage 10 criteria 1–50 are completed and Stage 10 is merged" in ROADMAP
    assert STAGE10_MERGE in ROADMAP
    for text in (README, ROADMAP, PROTOCOL, FREEZE):
        assert SELECTED_STAGE11 in text
        assert "parametrized covariance precursor != general relativity" in text


def test_stage11_type_separation_is_frozen() -> None:
    for text in (README, ROADMAP, PROTOCOL, FREEZE):
        assert "parameter label != internal clock reading" in text
        assert "parameter label != event identity" in text
        assert "internal clock perspective != external parameterization" in text
    assert "same numerical parameter value != same physical event" in PROTOCOL
    assert "parameterization correspondence != event identity" in PROTOCOL


def test_stage11_parametrized_constraint_and_positive_family_are_preserved() -> None:
    for phrase in (
        "C = p_T + H(q,p) approx 0",
        "H(q,p)=p^2/2",
        "N'(lambda') = N(lambda) dlambda/dlambda' = N(lambda)/f'(lambda)",
        "f_id(lambda)=lambda",
        "f_aff(lambda)=2 lambda + 1",
        "f_cub(lambda)=lambda + lambda^3/4",
        "f_sinh(lambda)=sinh(lambda)",
    ):
        assert phrase in PROTOCOL
    assert "dq/dT" in PROTOCOL
    assert "raw parameter derivative equality != reparameterization covariance criterion" in PROTOCOL


def test_stage11_reuses_stage10_typed_architecture() -> None:
    for text in (PROTOCOL, FREEZE):
        assert "T10_candidate=(O,P,R,V;Xi)" in text
        assert "R=(R_content,R_direction,R_access)" in text
        assert "V=(V_extension,V_semantics,V_weights)" in text
        assert "QExt(e1)={h_L,h_R}" in text
        assert "future_signature_left" in text
        assert "future_signature_other" in text
    assert "C_{X->Y} o G_{rho->sigma} ~= G_{rho->sigma} o C_{X->Y}" in PROTOCOL
    assert "internal-clock covariance != reparameterization covariance" in PROTOCOL


def test_stage11_negative_controls_and_antitriviality_remain_frozen() -> None:
    combined = PROTOCOL + "\n" + FREEZE
    for phrase in (
        "raw-equal-parameter",
        "wrong/missing parameter-event correspondence",
        "wrong derivative Jacobian",
        "lambda^2",
        "f_rev(lambda)=-lambda",
        "parameter-dependent corruption",
        "same labels after relabeling != sufficient evidence of covariance",
    ):
        assert phrase in combined
    assert "orientation-preserving reparameterization != time reversal" in combined
    assert "orientation reversal != physical record reversal by definition" in combined
    assert "non-injective relabeling != admissible reparameterization" in combined


def test_stage11_freeze_remains_historical_after_stage11a_closure() -> None:
    assert "Stage 11.0 completed; criteria 1–10 satisfied; criteria 11–50 pending" in FREEZE
    assert "criteria 1–16 satisfied" in PROTOCOL.lower()
    assert "criteria 17–50 pending" in PROTOCOL.lower()
    for criterion in range(1, 51):
        assert f"{criterion}." in PROTOCOL
    assert PROTOCOL.count("**satisfied**") == 16
    assert PROTOCOL.count("**pending**") == 34
    assert "Stage 11A — minimal parametrized constrained carrier and admissible family — completed" in PROTOCOL
    assert "Stage 11B — relational observables and relational derivatives — next" in PROTOCOL
    for status in (
        "parametrized_covariant",
        "parametrized_partial",
        "parametrized_obstructed",
        "inconclusive",
    ):
        assert status in PROTOCOL
    assert "finite typed parametrized covariance != general covariance" in PROTOCOL
    assert "absence of preferred external parameterization != absence of ontological becoming" in PROTOCOL


def test_stage11a_documented_diagnostics_close_only_criteria_11_16() -> None:
    for text in (PROTOCOL, NOTES_A, RESULT_A):
        assert "criteria 11–16" in text
        assert "36" in text
        assert "24" in text
        assert "0.5" in text
        assert "same constraint orbit != established general covariance" in text
    assert "minimum transformed positive lapse" in RESULT_A
    assert "max constraint residual" in RESULT_A
    assert "max lapse chain-rule residual" in RESULT_A
    assert "Stage 11B" in NOTES_A and "next" in NOTES_A.lower()
    assert "Stage 11B" in RESULT_A and "Next checkpoint" in RESULT_A
