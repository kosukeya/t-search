from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")
ROADMAP = (ROOT / "docs" / "roadmap.md").read_text(encoding="utf-8")
PROTOCOL = (ROOT / "docs" / "stage11_protocol.md").read_text(encoding="utf-8")
FREEZE = (ROOT / "results" / "stage11_0_protocol_freeze.md").read_text(encoding="utf-8")
NOTES_A = (ROOT / "docs" / "stage11a_notes.md").read_text(encoding="utf-8")
RESULT_A = (ROOT / "results" / "stage11a_parametrized.md").read_text(encoding="utf-8")
NOTES_B = (ROOT / "docs" / "stage11b_notes.md").read_text(encoding="utf-8")
RESULT_B = (ROOT / "results" / "stage11b_relational.md").read_text(encoding="utf-8")
NOTES_C = (ROOT / "docs" / "stage11c_notes.md").read_text(encoding="utf-8")
RESULT_C = (ROOT / "results" / "stage11c_lift.md").read_text(encoding="utf-8")
NOTES_D = (ROOT / "docs" / "stage11d_notes.md").read_text(encoding="utf-8")
RESULT_D = (ROOT / "results" / "stage11d_measurement.md").read_text(encoding="utf-8")
NOTES_E = (ROOT / "docs" / "stage11e_notes.md").read_text(encoding="utf-8")
RESULT_E = (ROOT / "results" / "stage11e_compatibility.md").read_text(encoding="utf-8")

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


def test_stage11_freeze_remains_historical_after_stage11e_closure() -> None:
    assert "Stage 11.0 completed; criteria 1–10 satisfied; criteria 11–50 pending" in FREEZE
    assert "criteria 1–43 satisfied" in PROTOCOL.lower()
    assert "criteria 44–50 pending" in PROTOCOL.lower()
    for criterion in range(1, 51):
        assert f"{criterion}." in PROTOCOL
    assert PROTOCOL.count("**satisfied**") == 43
    assert PROTOCOL.count("**pending**") == 7
    for stage in (
        "Stage 11A — minimal parametrized constrained carrier and admissible family — completed",
        "Stage 11B — relational observables and relational derivatives — completed",
        "Stage 11C — typed O/P/R/V/Xi lift — completed",
        "Stage 11D — future-measurement reparameterization covariance — completed",
        "Stage 11E — clock-change × parameterization compatibility — completed",
    ):
        assert stage in PROTOCOL
    assert "Stage 11F — ablation / wrong-gauge / false-positive controls — next" in PROTOCOL
    for status in (
        "parametrized_covariant",
        "parametrized_partial",
        "parametrized_obstructed",
        "inconclusive",
    ):
        assert status in PROTOCOL
    assert "finite typed parametrized covariance != general covariance" in PROTOCOL
    assert "absence of preferred external parameterization != absence of ontological becoming" in PROTOCOL


def test_stage11a_documented_diagnostics_remain_historical() -> None:
    for text in (README, ROADMAP, PROTOCOL, NOTES_A, RESULT_A):
        assert "Stage 11A" in text
        assert "36" in text
        assert "24" in text
        assert "0.5" in text
        assert "same constraint orbit != established general covariance" in text
    for text in (PROTOCOL, NOTES_A, RESULT_A):
        assert "criteria 11–16" in text.lower()
    assert "minimum positive lapse" in RESULT_A
    assert "max constraint residual" in RESULT_A
    assert "max lapse chain-rule residual" in RESULT_A


def test_stage11b_documented_relational_evidence_remains_historical() -> None:
    for text in (README, ROADMAP, PROTOCOL, NOTES_B, RESULT_B):
        assert "Stage 11B" in text
        assert "52" in text
        assert "24" in text
        assert "7" in text
        assert "6" in text
        assert "1.25" in text
        assert "invalid_equal_raw_parameter_event_rule" in text
        assert "relational covariance on one finite orbit != general covariance" in text
    for text in (PROTOCOL, NOTES_B, RESULT_B):
        assert "criteria 17–23" in text.lower()
    assert "q(T=tau)" in RESULT_B
    assert "dq/dT" in RESULT_B
    assert "equal raw lambda != physical-event correspondence" in NOTES_B


def test_stage11c_documented_typed_lift_remains_historical() -> None:
    for text in (README, ROADMAP, PROTOCOL, NOTES_C, RESULT_C):
        assert "Stage 11C" in text
        assert "typed O/P/R/V/Xi lift != full future-measurement covariance" in text
        assert "typed product lift feasibility != independent dynamical covariance evidence" in text
        assert "Stage 10 event-role bridge != dynamical identification of quantum and classical carriers" in text
    for text in (ROADMAP, PROTOCOL, NOTES_C, RESULT_C):
        assert "QExt(e1)={h_L,h_R}" in text
    assert "parameter_dependent_oprv_corruption_detected" in PROTOCOL
    assert "parameter_dependent_oprv_corruption_detected" in RESULT_C
    assert "4 / 4" in RESULT_C
    assert "continuation/class correspondence entries: **8**" in RESULT_C
    assert "outcome correspondence entries: **8**" in RESULT_C


def test_stage11d_documented_measurement_covariance_remains_historical() -> None:
    bounded = (
        "Stage 11D future-measurement reparameterization covariance on the frozen positive family = established"
    )
    for text in (README, ROADMAP, PROTOCOL, NOTES_D, RESULT_D):
        assert "Stage 11D" in text
        assert "QExt(e1)={h_L,h_R}" in text
        assert bounded in text
        assert "future-measurement reparameterization covariance != clock-change x reparameterization compatibility" in text
        assert "typed Stage 10/11 bridge != dynamical derivation of quantum measurement from the classical precursor" in text
    assert "run #1361" in NOTES_D
    assert "907 passed in 590.98s (0:09:50)" in NOTES_D
    assert "run #1361" in RESULT_D
    assert "907 passed in 590.98s (0:09:50)" in RESULT_D
    assert "external lapse != quantum measurement normalization form" in NOTES_D
    assert "wrong-normalization matrix residual: **> 1e-9**" in RESULT_D
    assert "wrong-normalization probability residual: **> 1e-9**" in RESULT_D


def test_stage11e_documents_exhaustive_commuting_square_evidence() -> None:
    bounded = (
        "Stage 11E clock-change x parameterization compatibility on the frozen finite family = established"
    )
    for text in (README, ROADMAP, PROTOCOL, RESULT_E):
        assert bounded in text
        assert "12" in text
        assert "108" in text
        assert "648" in text
        assert "1296" in text
        assert "noncommuting_wrong_clock_path_detected" in text
        assert "commuting typed product square != independent interaction law" in text
        assert "commuting typed diagram != general covariance" in text
        assert "path-independent future probabilities != future actuality" in text
        assert "path-independent evidence update != ontological becoming" in text
    for text in (NOTES_E, RESULT_E):
        assert "Stage 11E" in text
        assert "C_{X->Y} o G_{rho->sigma} ~= G_{rho->sigma} o C_{X->Y}" in text
        assert "Stage 11F" in text
    assert "run #1407" in RESULT_E
    assert "915 passed in 482.25s (0:08:02)" in RESULT_E
    assert "event/O commuting squares: **648**" in RESULT_E
    assert "measurement commuting squares: **1296**" in RESULT_E
    assert "weighted/modal squares: **648**" in RESULT_E
    assert "common-evidence posterior squares: **648**" in RESULT_E
    assert "cached repeated evaluation != reduced scientific comparison family" in RESULT_E


def test_stage11_planning_documents_advance_to_stage11f_without_full_synthesis_claim() -> None:
    for text in (README, ROADMAP, PROTOCOL):
        assert "Stage 11F" in text
        assert "next" in text.lower()
        assert "criteria 1–43" in text
        assert "finite typed parametrized covariance != general covariance" in text
    # Stage 11G, not Stage 11E, chooses the frozen overall Stage 11 status.
    assert "parametrized_covariant" in PROTOCOL
    assert "criteria 48–49" in PROTOCOL.lower()
