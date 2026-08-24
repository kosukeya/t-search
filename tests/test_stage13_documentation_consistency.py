from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")
ROADMAP = (ROOT / "docs" / "roadmap.md").read_text(encoding="utf-8")
PROTOCOL = (ROOT / "docs" / "stage13_protocol.md").read_text(encoding="utf-8")
FREEZE = (ROOT / "results" / "stage13_0_protocol_freeze.md").read_text(encoding="utf-8")
NOTES_A = (ROOT / "docs" / "stage13a_notes.md").read_text(encoding="utf-8")
RESULT_A = (ROOT / "results" / "stage13a_multi_constraint.md").read_text(encoding="utf-8")
NOTES_B = (ROOT / "docs" / "stage13b_notes.md").read_text(encoding="utf-8")
RESULT_B = (ROOT / "results" / "stage13b_paths.md").read_text(encoding="utf-8")
NOTES_C = (ROOT / "docs" / "stage13c_notes.md").read_text(encoding="utf-8")
RESULT_C = (ROOT / "results" / "stage13c_relational.md").read_text(encoding="utf-8")
NOTES_D = (ROOT / "docs" / "stage13d_notes.md").read_text(encoding="utf-8")
RESULT_D = (ROOT / "results" / "stage13d_gauge_atlas.md").read_text(encoding="utf-8")
NOTES_E = (ROOT / "docs" / "stage13e_notes.md").read_text(encoding="utf-8")
RESULT_E = (ROOT / "results" / "stage13e_measurement.md").read_text(encoding="utf-8")
PROTOCOL_F = (ROOT / "docs" / "stage13f_protocol.md").read_text(encoding="utf-8")
STAGE12_G = (ROOT / "results" / "stage12g_synthesis_stage13_gate.md").read_text(encoding="utf-8")

SELECTED_STAGE13 = (
    "Construct a minimal multi-constraint constraint-algebra/refoliation precursor with at least two "
    "nontrivially related first-class constraint directions, and test whether the Stage 12 physical-orbit "
    "quotient, relational observables, and typed O/P/R/V measurement architecture remain compatible under "
    "the resulting constraint-generated path structure without assuming general relativity."
)
MERGED_STAGE12_MAIN = "ee4baec55fa994217b275f9f2451e25fc6736787"
STAGE13E_VALIDATED_HEAD = "5da1f7b07189ac9fd23c756ed432bfc7406caf37"


def test_stage13_selected_gate_and_stage12_baseline_remain_frozen():
    for text in (PROTOCOL, FREEZE, STAGE12_G, README, ROADMAP):
        assert SELECTED_STAGE13 in text
    assert MERGED_STAGE12_MAIN in PROTOCOL
    assert "1025 passed in 693.84s (0:11:33)" in PROTOCOL
    assert "multi_orbit_gauge_covariant" in PROTOCOL


def test_stage13_current_status_is_validated_e_and_frozen_f():
    assert (
        "Stage 13E completed; criteria 1–43 satisfied; criteria 44–50 pending. "
        "Stage 13F protocol frozen and executable source/test validation pending."
    ) in PROTOCOL
    assert PROTOCOL.count("**satisfied**") == 43
    assert PROTOCOL.count("**pending**") == 7
    assert "Stage 13E — O/P/R/V/Xi and future-measurement descent across compensated path choices — **completed**" in PROTOCOL
    assert "Stage 13F — basis / ablation / anomaly / false-positive controls — **active; protocol frozen, source/test validation pending**" in PROTOCOL


def test_stage13e_validated_checkpoint_is_synchronized():
    combined = "\n".join((PROTOCOL, NOTES_E, RESULT_E))
    assert STAGE13E_VALIDATED_HEAD in combined
    assert "1084 passed in 703.45s (0:11:43)" in combined
    for phrase in (
        "36",
        "144",
        "288",
        "576",
        "10 / 10",
        "Stage 13E typed O/P/R/V/Xi and future-measurement descent across compensated path choices on the frozen finite family = established",
        "compensated-path operational descent != refoliation invariance",
        "future-measurement covariance != future actuality",
        "repository validation != new scientific evidence",
    ):
        assert phrase in combined


def test_stage13e_closes_exactly_criteria_39_through_43():
    lines = (
        "39. O/P/R/V/Xi architecture is lifted over every canonical Stage 13 representative with path/basis provenance confined to Xi — **satisfied**.",
        "40. Licensed compensated path choices preserve quotient-level typed O/P/R/V content — **satisfied**.",
        "41. Inherited future-measurement payloads descend across compensated multi-constraint path choices — **satisfied**.",
        "42. An orbit-sensitive operational witness based on Dirac/complete-relational data remains representative/path independent within an orbit while preserving physical-orbit discrimination — **satisfied**.",
        "43. Wrong path/event/class/outcome/normalization or representative-dependent O/P/R/V/measurement payloads are rejected — **satisfied**.",
    )
    for line in lines:
        assert line in PROTOCOL
    assert "44. Noncommuting and equivalent commuting constraint presentations are compared and shown not to change licensed quotient-level physical content when typed correspondence is correct — **pending**." in PROTOCOL
    assert "50. External final full-repository regression and merge-readiness review — **pending**." in PROTOCOL


def test_stage13f_protocol_freezes_basis_ablation_and_anomaly_controls():
    combined = PROTOCOL + "\n" + PROTOCOL_F
    for phrase in (
        "K_X_tilde = exp(-T) K_X = p_X + a p",
        "{K_T,K_X_tilde}=0",
        "Phi_X_tilde(u): X -> X+u, q -> q+a u",
        "basis_presentation_equivalent",
        "rank_deficient_constraint_control_rejected",
        "decoupled_constraint_control_rejected",
        "wrong_compensator_detected",
        "one_clock_observable_incomplete",
        "cross_orbit_false_positive_rejected",
        "K_X_bad",
        "constraint_algebra_anomaly_detected",
        "basis-equivalent finite quotient != refoliation invariance",
        "commuting presentation != proof that all admissible presentations commute",
        "constraint-algebra anomaly != ontological becoming",
    ):
        assert phrase in combined
    assert "72 `Phi_T` + 72 `Phi_X_tilde`" in combined
    assert "Stage 13F source diagnostics satisfied != repository-validated Stage 13F completion" in PROTOCOL_F


def test_stage13_historical_a_through_d_evidence_remains_present():
    combined = "\n".join((PROTOCOL, NOTES_A, RESULT_A, NOTES_B, RESULT_B, NOTES_C, RESULT_C, NOTES_D, RESULT_D))
    for phrase in (
        "1048 passed in 592.23s (0:09:52)",
        "1058 passed in 696.20s (0:11:36)",
        "1069 passed in 550.80s (0:09:10)",
        "1076 passed in 908.96s (0:15:08)",
        "87 typed nodes",
        "72 `Phi_T` + 72 `Phi_X` = 144",
        "4 quotient classes",
        "path_provenance_typed_lost_numerically_reconstructible",
        "typed_status = lost",
        "numerical_status = reconstructible",
    ):
        assert phrase in combined


def test_stage13_synthesis_vocabulary_and_next_gate_candidates_remain_frozen():
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


def test_stage13_interpretation_boundaries_remain_explicit():
    combined = "\n".join((PROTOCOL, FREEZE, NOTES_E, RESULT_E, PROTOCOL_F))
    for phrase in (
        "two constraint labels != two independent gauge directions",
        "noncommuting constraint presentation != fundamental physical non-Abelianity",
        "constraint-basis change != physical-orbit change",
        "basis-equivalent finite quotient != refoliation invariance",
        "multi-constraint path covariance != refoliation invariance",
        "constraint-algebra/refoliation precursor != general relativity",
        "path word != physical temporal history",
        "path word != modal continuation",
        "wrong compensator failure != physical time asymmetry",
        "one clock condition in a two-gauge-direction model != complete relational observable",
        "complete relational observable != ontological becoming by definition",
        "Dirac invariant != timeless ontology by definition",
        "Dirac-invariant data + relational change != proof of eternalism",
        "gauge quotient != elimination of physical change",
        "future-measurement covariance != future actuality",
        "constraint-algebra anomaly != ontological becoming",
        "finite-model success != empirical discovery",
        "not_established != false",
    ):
        assert phrase in combined
