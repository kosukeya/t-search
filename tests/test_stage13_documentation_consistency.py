from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = (ROOT / "docs" / "stage13_protocol.md").read_text(encoding="utf-8")
FREEZE = (ROOT / "results" / "stage13_0_protocol_freeze.md").read_text(encoding="utf-8")
STAGE12_G = (ROOT / "results" / "stage12g_synthesis_stage13_gate.md").read_text(encoding="utf-8")

SELECTED_STAGE13 = (
    "Construct a minimal multi-constraint constraint-algebra/refoliation precursor with at least two "
    "nontrivially related first-class constraint directions, and test whether the Stage 12 physical-orbit "
    "quotient, relational observables, and typed O/P/R/V measurement architecture remain compatible under "
    "the resulting constraint-generated path structure without assuming general relativity."
)
MERGED_STAGE12_MAIN = "ee4baec55fa994217b275f9f2451e25fc6736787"


def test_stage13_selected_gate_and_stage12_baseline_are_frozen() -> None:
    for text in (PROTOCOL, FREEZE, STAGE12_G):
        assert SELECTED_STAGE13 in text
    for text in (PROTOCOL, FREEZE):
        assert MERGED_STAGE12_MAIN in text
        assert "1025 passed in 693.84s (0:11:33)" in text
        assert "multi_orbit_gauge_covariant" in text


def test_stage13_protocol_closes_only_criteria_1_10() -> None:
    assert "Stage 13.0 completed; criteria 1–10 satisfied; criteria 11–50 pending" in PROTOCOL
    assert "Stage 13.0 completed; criteria 1–10 satisfied; criteria 11–50 pending" in FREEZE
    for criterion in range(1, 51):
        assert f"{criterion}." in PROTOCOL
    assert PROTOCOL.count("**satisfied**") == 10
    assert PROTOCOL.count("**pending**") == 40


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


def test_stage13_compensated_path_law_is_frozen() -> None:
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


def test_stage13_dirac_and_two_clock_relational_structure_is_frozen() -> None:
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


def test_stage13_sequence_is_frozen() -> None:
    for stage in (
        "Stage 13A — two-constraint first-class carrier and finite representative family — **next**",
        "Stage 13B — noncommuting gauge paths and compensated closure — pending",
        "Stage 13C — Dirac / two-clock complete relational observables and physical-orbit discrimination — pending",
        "Stage 13D — typed multi-constraint gauge atlas, path words, quotient, and descent — pending",
        "Stage 13E — O/P/R/V/Xi and future-measurement descent across compensated path choices — pending",
        "Stage 13F — basis / ablation / anomaly / false-positive controls — pending",
        "Stage 13G — executable synthesis and evidence-selected next gate — pending",
        "criterion 50 — external final full-repository regression / merge-readiness review — pending",
    ):
        assert stage in PROTOCOL


def test_stage13_synthesis_vocabulary_is_frozen() -> None:
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
    combined = PROTOCOL + "\n" + FREEZE
    for phrase in (
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
