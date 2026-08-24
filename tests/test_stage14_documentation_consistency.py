from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")
ROADMAP = (ROOT / "docs" / "roadmap.md").read_text(encoding="utf-8")
PROTOCOL = (ROOT / "docs" / "stage14_protocol.md").read_text(encoding="utf-8")
FREEZE = (ROOT / "results" / "stage14_0_protocol_freeze.md").read_text(encoding="utf-8")
NOTES_A = (ROOT / "docs" / "stage14a_notes.md").read_text(encoding="utf-8")
RESULT_A = (ROOT / "results" / "stage14a_structure_function.md").read_text(encoding="utf-8")
NOTES_B = (ROOT / "docs" / "stage14b_notes.md").read_text(encoding="utf-8")
RESULT_B = (ROOT / "results" / "stage14b_paths.md").read_text(encoding="utf-8")
STAGE13_G = (ROOT / "results" / "stage13g_synthesis_stage14_gate.md").read_text(encoding="utf-8")

SELECTED_STAGE14 = (
    "Construct a minimal phase-space-dependent structure-function / hypersurface-deformation precursor "
    "designed to test whether the Stage 13F simple commuting-basis trivialization persists, and retest "
    "the physical quotient, relational observables, and typed O/P/R/V measurement architecture without "
    "assuming general relativity or refoliation invariance."
)

MERGED_STAGE13_MAIN = "468fe6667ec6484fbe9e402135cd75f5d69420cf"
FINAL_STAGE13_HEAD = "d0b541acb4345933a95f592f726827acf00604c0"
STAGE14_FREEZE_HEAD = "afe0598362ccf0e808d2c690491cda810594d87e"
STAGE14A_SOURCE_HEAD = "d1116a743b0374c96993c476331f5cceacfbb077"
STAGE14A_SYNC_HEAD = "db72c8715a3b58d4422932640807dbb20297005e"
STAGE14B_SOURCE_HEAD = "2b0866b63e6fb4d4951f883839e6693b12ceddfc"


def test_stage14_selected_gate_and_merged_stage13_baseline_are_frozen():
    for text in (PROTOCOL, FREEZE, STAGE13_G, README, ROADMAP):
        assert SELECTED_STAGE14 in text
    combined = PROTOCOL + "\n" + FREEZE
    assert MERGED_STAGE13_MAIN in combined
    assert FINAL_STAGE13_HEAD in combined
    assert "1099 passed in 893.92s (0:14:53)" in combined
    assert "multi_constraint_path_covariant" in combined
    assert "phase_space_structure_function_precursor" in combined


def test_stage14b_status_closes_exactly_criteria_1_through_24():
    assert (
        "Stage 14B source/test checkpoint validated; criteria 1–24 satisfied; "
        "criteria 25–50 pending. Stage 14C is next."
    ) in PROTOCOL
    assert PROTOCOL.count("**satisfied**") == 24
    assert PROTOCOL.count("**pending**") == 26
    assert "Stage 14.0 completed; criteria 1–10 satisfied; criteria 11–50 pending." in FREEZE
    assert "Stage 14A — three-constraint first-class structure-function carrier and finite representative family — **completed**" in PROTOCOL
    assert "Stage 14B — phase-space-dependent mixed paths and third-direction compensation — **completed**" in PROTOCOL
    assert "Stage 14C — Dirac / three-condition complete relational observables, physical quotient, and orbit discrimination — **next**" in PROTOCOL


def test_stage14_positive_carrier_and_structure_functions_remain_frozen():
    combined = PROTOCOL + "\n" + FREEZE
    for phrase in (
        "(T1,p_1; T2,p_2; X,p_X; q,p)",
        "a=0.5",
        "b=0.25",
        "kappa=0.5",
        "D = p_X + a p approx 0",
        "H_1 = p_1 + p^2/2 approx 0",
        "H_2 = p_2 + b p + kappa T1 X D approx 0",
        "{H_1,D}=0",
        "{H_1,H_2}=-kappa X D",
        "{H_2,D}=kappa T1 D",
        "f_12^D(z)=-kappa X",
        "f_2D^D(z)=kappa T1",
        "Jacobi",
        "phase-space-dependent first-class closure != hypersurface-deformation algebra",
    ):
        assert phrase in combined


def test_stage14_finite_family_paths_and_relational_targets_remain_frozen():
    combined = PROTOCOL + "\n" + FREEZE
    for phrase in (
        "27 representatives per physical orbit",
        "108 positive representatives total",
        "864 ordered mixed pairs",
        "v_21D-v_12D",
        "X_0 [exp(kappa T1_1 u)-exp(kappa T1_0 u)]",
        "P_D=p",
        "Q_D=q-p T1",
        "q(T1=tau1,T2=tau2,X=chi)",
        "two-clock",
        "exactly four",
        "third-direction compensation != refoliation invariance",
    ):
        assert phrase in combined


def test_stage14_basis_controls_sequence_and_synthesis_vocabulary_remain_frozen():
    combined = PROTOCOL + "\n" + FREEZE
    for phrase in (
        "simple_scalar_rescaling",
        "H_1' = f_1(z) H_1",
        "H_2' = f_2(z) H_2",
        "D' = f_D(z) D",
        "-kappa X f_1 f_2 / f_D",
        "singular",
        "H_2_tilde = H_2 - kappa T1 X D",
        "triangular",
        "structure_function_removed_control_rejected",
        "rank_deficient_constraint_control_rejected",
        "missing_third_direction_control_rejected",
        "wrong_structure_function_compensator_detected",
        "missing_third_direction_compensator_detected",
        "cross_orbit_false_positive_rejected",
        "two_clock_observable_incomplete",
        "singular_scalar_rescaling_rejected",
        "stage13_style_scalar_rescaling_obstructed",
        "triangular_basis_equivalent",
        "constraint_algebra_anomaly_detected",
        "representative_dependent_payload_corruption_detected",
        "Stage 14A",
        "Stage 14B",
        "Stage 14C",
        "Stage 14D",
        "Stage 14E",
        "Stage 14F",
        "Stage 14G",
        "structure_function_path_covariant_scalar_obstructed",
        "structure_function_path_covariant_scalar_trivializable",
        "structure_function_path_partial",
        "structure_function_path_obstructed",
        "inconclusive",
    ):
        assert phrase in combined


def test_stage14a_repository_checkpoint_and_deterministic_evidence_are_synchronized():
    combined = "\n".join((PROTOCOL, NOTES_A, RESULT_A))
    assert STAGE14_FREEZE_HEAD in combined
    assert "1106 passed in 879.78s (0:14:39)" in combined
    assert STAGE14A_SOURCE_HEAD in combined
    assert "1113 passed in 545.23s (0:09:05)" in combined
    assert STAGE14A_SYNC_HEAD in combined
    assert "1114 passed in 900.17s (0:15:00)" in combined
    for phrase in (
        "108",
        "648",
        "0.7812880785647448",
        "-0.5",
        "0.0",
        "0.5",
        "2.220446049250313e-16",
        "structure_function_removed_control_rejected",
        "rank_deficient_constraint_control_rejected",
        "Stage 14A three-constraint first-class structure-function carrier and finite representative family = established",
        "repository validation != new scientific evidence",
    ):
        assert phrase in combined


def test_stage14b_repository_checkpoint_and_deterministic_evidence_are_synchronized():
    combined = "\n".join((PROTOCOL, NOTES_B, RESULT_B))
    assert STAGE14B_SOURCE_HEAD in combined
    assert "1122 passed in 891.20s (0:14:51)" in combined
    for phrase in (
        "864",
        "1728",
        "576",
        "288",
        "8748",
        "0.3934693402873666",
        "2.3504023872876028",
        "4.440892098500626e-16",
        "wrong_structure_function_compensator_detected",
        "missing_third_direction_compensator_detected",
        "cross_orbit_false_positive_rejected",
        "Stage 14B phase-space-dependent mixed paths and exact third-direction compensation on the frozen finite family = established",
        "raw path-word inequality != physical path dependence",
        "compensated mixed-path closure != refoliation invariance",
        "repository validation != new scientific evidence",
    ):
        assert phrase in combined


def test_stage14b_closes_frozen_criteria_18_through_24_only():
    for criterion in (
        "18. Stage 14B constructs the canonical 864 ordered mixed source/target pairs — **satisfied**.",
        "19. Both `12D` and `21D` path implementations match the frozen exact flow formulas — **satisfied**.",
        "20. Exact third-direction compensation closes every positive mixed pair on the same licensed target within tolerance — **satisfied**.",
        "21. The nontrivial `X_0 != 0` subfamily exhibits the expected path-order-dependent raw compensator difference — **satisfied**.",
        "22. Wrong-sign, wrong-value, missing, and Stage-13-style compensators are rejected on the required nontrivial cases — **satisfied**.",
        "23. Cross-orbit source/target pairs are not licensed as gauge paths — **satisfied**.",
        "24. Path-order / compensator results remain explicitly bounded away from refoliation invariance, time asymmetry, and ontological becoming — **satisfied**.",
    ):
        assert criterion in PROTOCOL
    assert "25. Stage 14C reconstructs representative-independent `(Q_D,P_D)` across all 108 positive representatives — **pending**." in PROTOCOL
    assert "50. External final full-repository regression and merge-readiness review — **pending**." in PROTOCOL


def test_stage14_interpretation_boundaries_remain_explicit():
    combined = "\n".join((PROTOCOL, FREEZE, NOTES_A, RESULT_A, NOTES_B, RESULT_B))
    for phrase in (
        "phase-space-dependent structure-function precursor != hypersurface-deformation algebra by definition",
        "finite first-class structure-function algebra != hypersurface-deformation algebra",
        "hypersurface-deformation precursor != general relativity",
        "structure functions != spacetime geometry by definition",
        "three constraint labels != three independent gauge directions",
        "Stage 14A single-generator surface/Dirac preservation != third-direction compensated mixed-path closure",
        "raw path-word inequality != physical path dependence",
        "third-direction compensation != refoliation invariance",
        "compensated mixed-path closure != refoliation invariance",
        "Stage-13-style scalar-rescaling obstruction != universal non-Abelianizability",
        "triangular basis equivalence != universal basis trivializability",
        "wrong compensator failure != physical time asymmetry",
        "compensated path closure != ontological becoming",
        "complete relational observable != ontological becoming by definition",
        "Dirac-invariant data + relational change != proof of eternalism",
        "gauge quotient != elimination of physical change",
        "future-measurement covariance != future actuality",
        "constraint-algebra anomaly != ontological becoming",
        "finite-model success != empirical discovery",
        "repository validation != new scientific evidence",
        "not_established != false",
    ):
        assert phrase in combined
