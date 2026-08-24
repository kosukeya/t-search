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
NOTES_F = (ROOT / "docs" / "stage13f_notes.md").read_text(encoding="utf-8")
RESULT_F = (ROOT / "results" / "stage13f_ablation.md").read_text(encoding="utf-8")
NOTES_G = (ROOT / "docs" / "stage13g_notes.md").read_text(encoding="utf-8")
RESULT_G = (ROOT / "results" / "stage13g_synthesis_stage14_gate.md").read_text(encoding="utf-8")
RESULT_50 = (ROOT / "results" / "stage13_criterion50_merge_readiness.md").read_text(encoding="utf-8")
STAGE12_G = (ROOT / "results" / "stage12g_synthesis_stage13_gate.md").read_text(encoding="utf-8")

SELECTED_STAGE13 = (
    "Construct a minimal multi-constraint constraint-algebra/refoliation precursor with at least two "
    "nontrivially related first-class constraint directions, and test whether the Stage 12 physical-orbit "
    "quotient, relational observables, and typed O/P/R/V measurement architecture remain compatible under "
    "the resulting constraint-generated path structure without assuming general relativity."
)
SELECTED_STAGE14 = (
    "Construct a minimal phase-space-dependent structure-function / hypersurface-deformation precursor "
    "designed to test whether the Stage 13F simple commuting-basis trivialization persists, and retest "
    "the physical quotient, relational observables, and typed O/P/R/V measurement architecture without "
    "assuming general relativity or refoliation invariance."
)
MERGED_STAGE12_MAIN = "ee4baec55fa994217b275f9f2451e25fc6736787"
STAGE13E_VALIDATED_HEAD = "5da1f7b07189ac9fd23c756ed432bfc7406caf37"
STAGE13F_VALIDATED_HEAD = "518a92315575b4b1d75ef51cad5a2dedd9dd40da"
STAGE13G_VALIDATED_HEAD = "013f90303ededbf769aaeef11a0336a480b02e2b"
STAGE13_CRITERION50_REVIEWED_HEAD = "5b6b4641f082f6554cf14ce6f55eba1ce5905ad0"


def test_stage13_selected_gate_and_stage12_baseline_remain_frozen():
    for text in (PROTOCOL, FREEZE, STAGE12_G, README, ROADMAP):
        assert SELECTED_STAGE13 in text
    assert MERGED_STAGE12_MAIN in PROTOCOL
    assert "1025 passed in 693.84s (0:11:33)" in PROTOCOL
    assert "multi_orbit_gauge_covariant" in PROTOCOL


def test_stage13_current_status_is_criterion50_complete_and_merge_ready():
    assert (
        "Stage 13 completed at the criterion-50 merge-readiness checkpoint; criteria 1–50 satisfied. "
        "PR #14 is merge-ready, Draft, open, and unmerged."
    ) in PROTOCOL
    assert PROTOCOL.count("**satisfied**") == 50
    assert PROTOCOL.count("**pending**") == 0
    assert "Stage 13E — O/P/R/V/Xi and future-measurement descent across compensated path choices — **completed**" in PROTOCOL
    assert "Stage 13F — basis / ablation / anomaly / false-positive controls — **completed**" in PROTOCOL
    assert "Stage 13G — executable synthesis and evidence-selected next gate — **completed**" in PROTOCOL
    assert "criterion 50 — external final full-repository regression / merge-readiness review — **completed**" in PROTOCOL


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


def test_stage13f_protocol_and_validated_checkpoint_remain_synchronized():
    frozen = PROTOCOL + "\n" + PROTOCOL_F
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
    ):
        assert phrase in frozen
    assert "Stage 13F source diagnostics satisfied != repository-validated Stage 13F completion" in PROTOCOL_F

    validated = "\n".join((PROTOCOL, NOTES_F, RESULT_F))
    assert STAGE13F_VALIDATED_HEAD in validated
    assert "1085 passed in 562.97s (0:09:22)" in validated
    for phrase in (
        "36 / 36",
        "144 / 144",
        "4 / 4",
        "6 / 6",
        "Stage 13F basis equivalence, ablation, anomaly, and false-positive controls on the frozen finite family = established",
        "constraint-algebra anomaly != ontological becoming",
        "repository validation != new scientific evidence",
    ):
        assert phrase in validated


def test_stage13g_validated_checkpoint_and_selected_gate_are_synchronized():
    combined = "\n".join((PROTOCOL, NOTES_G, RESULT_G))
    assert STAGE13G_VALIDATED_HEAD in combined
    assert "1099 passed in 878.58s (0:14:38)" in combined
    assert "multi_constraint_path_covariant" in combined
    assert "Stage 13G synthesis on the validated Stage 13A-F finite evidence chain = multi_constraint_path_covariant" in combined
    assert "phase_space_structure_function_precursor" in combined
    assert SELECTED_STAGE14 in combined
    for phrase in (
        "36 / 36",
        "144 / 144",
        "6 / 6",
        "score **12**",
        "score **8**",
        "score **7**",
        "constraint-basis equivalence != universal basis trivializability",
        "multi_constraint_path_covariant finite family != refoliation invariance",
        "phase-space-dependent structure-function precursor != hypersurface-deformation algebra by definition",
        "structure-function precursor != general relativity",
        "repository validation != new scientific evidence",
    ):
        assert phrase in combined


def test_stage13_criterion50_review_is_synchronized_across_top_level_docs():
    combined = "\n".join((PROTOCOL, RESULT_50, README, ROADMAP))
    assert STAGE13_CRITERION50_REVIEWED_HEAD in combined
    assert "1098 passed in 695.62s (0:11:35)" in combined
    for phrase in (
        "ahead 83 / behind 0",
        "mergeable = true",
        "41",
        "unresolved inline review threads: **0**",
        "PR conversation comments: **0**",
        "Stage 13 criterion 50 external final repository validation / merge-readiness review = satisfied",
        "Stage 13 criteria 1–50 are completed",
        "multi_constraint_path_covariant",
        "phase_space_structure_function_precursor",
        "repository validation != new scientific evidence",
        "merge-ready != merged",
    ):
        assert phrase in combined
    assert "Stage 13 criteria **1–50** are completed" in README
    assert "Stage 13 criteria **1–50** are completed" in ROADMAP
    assert "PR #14" in README and "merge-ready" in README
    assert "PR #14" in ROADMAP and "merge-ready" in ROADMAP


def test_stage13_closes_all_criteria_48_through_50():
    assert "48. Executable synthesis selects exactly one frozen Stage 13 status from the full Stage 13A–F evidence chain — **satisfied**." in PROTOCOL
    assert "49. The next research gate is evidence-selected without presupposing GR, refoliation invariance, or a hypersurface-deformation algebra — **satisfied**." in PROTOCOL
    assert "50. External final full-repository regression and merge-readiness review — **satisfied**." in PROTOCOL


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


def test_stage13_synthesis_vocabulary_and_candidate_families_remain_frozen():
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
    combined = "\n".join((PROTOCOL, FREEZE, NOTES_E, RESULT_E, PROTOCOL_F, NOTES_F, RESULT_F, NOTES_G, RESULT_G, RESULT_50))
    for phrase in (
        "two constraint labels != two independent gauge directions",
        "noncommuting constraint presentation != fundamental physical non-Abelianity",
        "constraint-basis change != physical-orbit change",
        "basis-equivalent finite quotient != refoliation invariance",
        "constraint-basis equivalence != universal basis trivializability",
        "multi-constraint path covariance != refoliation invariance",
        "multi_constraint_path_covariant finite family != refoliation invariance",
        "finite first-class constraint algebra != hypersurface-deformation algebra",
        "phase-space-dependent structure-function precursor != hypersurface-deformation algebra by definition",
        "structure-function precursor != general relativity",
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
        "repository validation != new scientific evidence",
        "merge-ready != merged",
        "not_established != false",
    ):
        assert phrase in combined
