from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")
ROADMAP = (ROOT / "docs" / "roadmap.md").read_text(encoding="utf-8")
PROTOCOL = (ROOT / "docs" / "stage13_protocol.md").read_text(encoding="utf-8")
FREEZE = (ROOT / "results" / "stage13_0_protocol_freeze.md").read_text(encoding="utf-8")
NOTES_A = (ROOT / "docs" / "stage13a_notes.md").read_text(encoding="utf-8")
RESULT_A = (ROOT / "results" / "stage13a_multi_constraint.md").read_text(encoding="utf-8")
STAGE12_G = (ROOT / "results" / "stage12g_synthesis_stage13_gate.md").read_text(encoding="utf-8")

SELECTED_STAGE13 = (
    "Construct a minimal multi-constraint constraint-algebra/refoliation precursor with at least two "
    "nontrivially related first-class constraint directions, and test whether the Stage 12 physical-orbit "
    "quotient, relational observables, and typed O/P/R/V measurement architecture remain compatible under "
    "the resulting constraint-generated path structure without assuming general relativity."
)
MERGED_STAGE12_MAIN = "ee4baec55fa994217b275f9f2451e25fc6736787"
STAGE13_0_HEAD = "898f36682b3cadac4abd953ba1bac8e32f17103e"
STAGE13A_SOURCE_HEAD = "ccd35956ac034de5d73d8b884a361fbe2fc92784"


def test_stage13_selected_gate_and_stage12_baseline_are_frozen() -> None:
    for text in (PROTOCOL, FREEZE, STAGE12_G, README, ROADMAP):
        assert SELECTED_STAGE13 in text
    for text in (PROTOCOL, FREEZE, README, ROADMAP):
        assert MERGED_STAGE12_MAIN in text
        assert "1025 passed in 693.84s (0:11:33)" in text
        assert "multi_orbit_gauge_covariant" in text


def test_stage13_0_historical_freeze_remains_closed_at_10_40() -> None:
    assert "Stage 13.0 completed; criteria 1–10 satisfied; criteria 11–50 pending" in FREEZE
    for criterion in range(1, 51):
        assert f"{criterion}." in PROTOCOL
    assert STAGE13_0_HEAD in NOTES_A
    assert "1039 passed in 542.21s (0:09:02)" in NOTES_A


def test_stage13_current_status_is_stage13a_16_34() -> None:
    assert "Stage 13A completed; criteria 1–16 satisfied; criteria 17–50 pending" in PROTOCOL
    assert PROTOCOL.count("**satisfied**") == 16
    assert PROTOCOL.count("**pending**") == 34
    for text in (README, ROADMAP):
        assert "Stage 13A" in text
        assert "criteria 1–16" in text
        assert "criteria 17–50" in text
        assert "Stage 13B" in text
        assert "36" in text and "representatives" in text
        assert "144" in text
        assert "raw gauge-path commutativity != successful multi-constraint closure" in text
        assert "noncommuting constraint presentation != fundamental physical non-Abelianity" in text
    assert "docs/stage13_protocol.md" in README
    assert "results/stage13_0_protocol_freeze.md" in README
    assert "docs/stage13a_notes.md" in README
    assert "results/stage13a_multi_constraint.md" in README


def test_stage13_two_constraint_carrier_is_frozen() -> None:
    combined = PROTOCOL + "\n" + FREEZE
    for phrase in (
        "(T,p_T; X,p_X; q,p)",
        "K_T = p_T + p^2/2 approx 0",
        "K_X = exp(T) (p_X + a p) approx 0",
        "a = 0.5",
        "{K_T,K_X} = -K_X",
        "two constraint labels != two independent gauge directions",
        "first-class closure on this toy carrier != hypersurface-deformation algebra",
    ):
        assert phrase in combined


def test_stage13_generator_flows_and_types_are_frozen() -> None:
    for phrase in (
        "dT/ds = 1",
        "dq/ds = p",
        "dX/ds = 0",
        "dX/du = exp(T)",
        "dq/du = a exp(T)",
        "dT/du = 0",
        "Phi_T(s)",
        "Phi_X(u)",
        "constraint-generator identity != physical-event identity",
    ):
        assert phrase in PROTOCOL


def test_stage13_compensated_path_law_remains_frozen_for_stage13b() -> None:
    combined = PROTOCOL + "\n" + FREEZE
    for phrase in (
        "s = T1 - T0",
        "DeltaX = X1 - X0",
        "u_TX = DeltaX / exp(T1)",
        "u_XT = DeltaX / exp(T0)",
        "u_XT = exp(s) u_TX",
        "raw gauge-path commutativity != successful multi-constraint closure",
        "same raw generator parameters under reordered paths != corresponding gauge path",
        "wrong compensator failure != physical time asymmetry",
    ):
        assert phrase in combined


def test_stage13_dirac_and_two_clock_relational_structure_remains_frozen() -> None:
    combined = PROTOCOL + "\n" + FREEZE
    for phrase in (
        "P_D = p",
        "Q_D = q - p T - a X",
        "q(T=tau,X=chi) = Q_D + P_D tau + a chi",
        "q(T=tau; X raw) = Q_D + P_D tau + a X",
        "one clock condition in a two-gauge-direction model != complete relational observable",
        "complete relational observable != ontological becoming by definition",
    ):
        assert phrase in combined


def test_stage13_physical_orbit_and_grid_are_frozen() -> None:
    compact = PROTOCOL.replace(" ", "")
    for orbit_id, pair in (
        ("omega_alpha", "(-0.35,1.25)"),
        ("omega_beta", "(0.40,1.25)"),
        ("omega_gamma", "(-0.35,0.75)"),
        ("omega_delta", "(0.20,1.75)"),
    ):
        assert orbit_id in PROTOCOL
        assert pair in compact
    for phrase in (
        "9 representatives per physical orbit",
        "36 representatives total",
        "288 ordered nonidentity same-orbit source/target pairs",
        "144 ordered mixed pairs",
        "different path word != different physical orbit",
        "path-word history != quotient-level physical state",
    ):
        assert phrase in PROTOCOL + "\n" + FREEZE


def test_stage13_constraint_basis_control_is_frozen() -> None:
    combined = PROTOCOL + "\n" + FREEZE
    for phrase in (
        "K_X_tilde = exp(-T) K_X = p_X + a p",
        "{K_T,K_X_tilde}=0",
        "noncommuting constraint presentation != fundamental physical non-Abelianity",
        "constraint-basis change != physical-orbit change",
    ):
        assert phrase in combined


def test_stage13_anomaly_and_false_positive_family_is_frozen() -> None:
    combined = PROTOCOL + "\n" + FREEZE
    for phrase in (
        "K_X_bad",
        "epsilon q",
        "wrong_compensator_detected",
        "same_raw_parameter_reorder_false_positive_rejected",
        "one_clock_observable_incomplete",
        "constraint_algebra_anomaly_detected",
        "basis_presentation_equivalent",
        "cross_orbit_path_rejected",
        "representative_dependent_payload_corruption_detected",
    ):
        assert phrase in combined


def test_stage13_oprv_xi_carryover_is_frozen() -> None:
    combined = PROTOCOL + "\n" + FREEZE
    for phrase in (
        "T12_candidate=(O,P,R,V;Xi)",
        "R=(R_content,R_direction,R_access)",
        "V=(V_extension,V_semantics,V_weights)",
        "QExt(e1)={h_L,h_R}",
        "future_signature_left",
        "future_signature_other",
        "identity",
        "A/e2",
        "path-specific Xi provenance != quotient-level physical content",
        "basis-specific Xi provenance != quotient-level physical content",
    ):
        assert phrase in combined


def test_stage13a_executable_evidence_is_synchronized() -> None:
    combined = PROTOCOL + "\n" + NOTES_A + "\n" + RESULT_A
    assert STAGE13A_SOURCE_HEAD in combined
    assert "1048 passed in 592.23s (0:09:52)" in combined
    for phrase in (
        "36 representatives",
        "72",
        "Phi_T",
        "Phi_X",
        "144 single-generator",
        "144 mixed",
        "36 off-surface",
        "rank **2**",
        "0.3778026572933153",
        "{K_T,K_X}+K_X=0",
        "Stage 13A two-constraint first-class carrier and finite representative family on the frozen four-orbit family = established",
        "Stage 13A single-generator surface preservation != compensated multi-generator path closure",
    ):
        assert phrase in combined


def test_stage13a_closes_exactly_criteria_11_16() -> None:
    for criterion in range(11, 17):
        marker = f"{criterion}."
        position = PROTOCOL.index(marker)
        assert "**satisfied**" in PROTOCOL[position : position + 350]
    for criterion in range(17, 51):
        marker = f"{criterion}."
        position = PROTOCOL.index(marker)
        assert "**pending**" in PROTOCOL[position : position + 500]


def test_stage13_sequence_moves_only_to_stage13b() -> None:
    for stage in (
        "Stage 13A — two-constraint first-class carrier and finite representative family — **completed**",
        "Stage 13B — noncommuting gauge paths and compensated closure — **next**",
        "Stage 13C — Dirac / two-clock complete relational observables and physical-orbit discrimination — pending",
        "Stage 13D — typed multi-constraint gauge atlas, path words, quotient, and descent — pending",
        "Stage 13E — O/P/R/V/Xi and future-measurement descent across compensated path choices — pending",
        "Stage 13F — basis / ablation / anomaly / false-positive controls — pending",
        "Stage 13G — executable synthesis and evidence-selected next gate — pending",
        "criterion 50 — external final full-repository regression / merge-readiness review — pending",
    ):
        assert stage in PROTOCOL


def test_stage13_synthesis_vocabulary_remains_frozen() -> None:
    for status in (
        "multi_constraint_path_covariant",
        "multi_constraint_path_partial",
        "multi_constraint_path_obstructed",
        "inconclusive",
    ):
        assert status in PROTOCOL + "\n" + FREEZE
    for candidate in (
        "phase-space-dependent structure-function / hypersurface-deformation precursor",
        "gravitational/minisuperspace extension",
        "richer causal/order layer",
        "nonideal/POVM clocks",
    ):
        assert candidate in PROTOCOL


def test_stage13_interpretation_guards_are_explicit() -> None:
    combined = (
        PROTOCOL
        + "\n"
        + FREEZE
        + "\n"
        + NOTES_A
        + "\n"
        + RESULT_A
        + "\n"
        + README
        + "\n"
        + ROADMAP
    )
    for phrase in (
        "two constraint labels != two independent gauge directions",
        "Stage 13A single-generator surface preservation != compensated multi-generator path closure",
        "noncommuting constraint presentation != fundamental physical non-Abelianity",
        "multi-constraint path covariance != refoliation invariance",
        "constraint-algebra/refoliation precursor != general relativity",
        "path word != physical temporal history",
        "path-order mismatch != arrow of time by definition",
        "one clock condition in a two-gauge-direction model != complete relational observable",
        "complete relational observable != ontological becoming by definition",
        "Dirac-invariant data + relational change != proof of eternalism",
        "gauge quotient != elimination of physical change",
        "finite-model success != empirical discovery",
        "not_established != false",
    ):
        assert phrase in combined
