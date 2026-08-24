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
NOTES_C = (ROOT / "docs" / "stage14c_notes.md").read_text(encoding="utf-8")
RESULT_C = (ROOT / "results" / "stage14c_relational.md").read_text(encoding="utf-8")
NOTES_D = (ROOT / "docs" / "stage14d_notes.md").read_text(encoding="utf-8")
RESULT_D = (ROOT / "results" / "stage14d_basis.md").read_text(encoding="utf-8")
NOTES_E = (ROOT / "docs" / "stage14e_notes.md").read_text(encoding="utf-8")
RESULT_E = (ROOT / "results" / "stage14e_measurement.md").read_text(encoding="utf-8")
NOTES_F = (ROOT / "docs" / "stage14f_notes.md").read_text(encoding="utf-8")
RESULT_F = (ROOT / "results" / "stage14f_ablation.md").read_text(encoding="utf-8")
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
STAGE14B_SYNC_HEAD = "318d6a34a7f8ddac29966493c31bd0cf8120ac4e"
STAGE14C_SOURCE_HEAD = "3e390ea59af879cc0b2962989467cdfe2b4ee1ca"
STAGE14C_SYNC_HEAD = "4011b90078c6a223e6d948a3034e07376fca4dbd"
STAGE14D_SOURCE_HEAD = "3e44454952d71ebbe9b0a52bbd9d68cd398d0635"
STAGE14D_SYNC_HEAD = "69c979896cc2855869a6637b41faac010b4b0b36"
STAGE14E_SOURCE_HEAD = "ac2376323f9d2b442bbbf448b22bc683ed2fd3ad"
STAGE14E_MERGE_CHECKOUT = "1662684069cfe0f44708e7d69b4cada4ae5b72d6"
STAGE14F_SOURCE_HEAD = "9f20ad22940ba827d346fbb7386eced5e26daedd"
STAGE14F_SOURCE_MERGE_CHECKOUT = "d636706b8e141befe0e80b2841413aaeb8f0cabc"
STAGE14F_NOTES_RESULTS_HEAD = "1274f2d64e8964dd0eb46c4bc0bbe9f8ba9f8497"
STAGE14F_NOTES_RESULTS_MERGE_CHECKOUT = "880169d21c3d1f217ea79f04ac761468c1bba8b9"


def test_stage14_selected_gate_and_merged_stage13_baseline_are_frozen():
    for text in (PROTOCOL, FREEZE, STAGE13_G, README, ROADMAP):
        assert SELECTED_STAGE14 in text
    combined = PROTOCOL + "\n" + FREEZE
    assert MERGED_STAGE13_MAIN in combined
    assert FINAL_STAGE13_HEAD in combined
    assert "1099 passed in 893.92s (0:14:53)" in combined
    assert "multi_constraint_path_covariant" in combined
    assert "phase_space_structure_function_precursor" in combined


def test_stage14f_status_closes_exactly_criteria_1_through_47():
    assert (
        "Stage 14F source/test and notes/results checkpoints validated; criteria 1–47 satisfied; "
        "criteria 48–50 pending. Stage 14G is next."
    ) in PROTOCOL
    assert PROTOCOL.count("**satisfied**") == 47
    assert PROTOCOL.count("**pending**") == 3
    assert "Stage 14.0 completed; criteria 1–10 satisfied; criteria 11–50 pending." in FREEZE
    assert "Stage 14A — three-constraint first-class structure-function carrier and finite representative family — **completed**" in PROTOCOL
    assert "Stage 14B — phase-space-dependent mixed paths and third-direction compensation — **completed**" in PROTOCOL
    assert "Stage 14C — Dirac / three-condition complete relational observables, physical quotient, and orbit discrimination — **completed**" in PROTOCOL
    assert "Stage 14D — simple-scalar-rescaling obstruction vs triangular-basis equivalence pressure test — **completed**" in PROTOCOL
    assert "Stage 14E — typed O/P/R/V/Xi and future-measurement descent across structure-function paths/bases — **completed**" in PROTOCOL
    assert "Stage 14F — ablation / anomaly / false-positive controls — **completed**" in PROTOCOL
    assert "Stage 14G — executable synthesis and evidence-selected next gate — **next**" in PROTOCOL


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
        "path_dependent_payload_corruption_detected",
        "basis_dependent_payload_corruption_detected",
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
        "108", "648", "0.7812880785647448", "-0.5", "0.0", "0.5",
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
    assert STAGE14B_SYNC_HEAD in combined
    assert "1123 passed in 548.54s (0:09:08)" in combined
    for phrase in (
        "864", "1728", "576", "288", "8748",
        "0.3934693402873666", "2.3504023872876028", "4.440892098500626e-16",
        "wrong_structure_function_compensator_detected",
        "missing_third_direction_compensator_detected",
        "cross_orbit_false_positive_rejected",
        "Stage 14B phase-space-dependent mixed paths and exact third-direction compensation on the frozen finite family = established",
        "raw path-word inequality != physical path dependence",
        "compensated mixed-path closure != refoliation invariance",
        "repository validation != new scientific evidence",
    ):
        assert phrase in combined


def test_stage14c_repository_checkpoint_and_deterministic_evidence_are_synchronized():
    combined = "\n".join((PROTOCOL, NOTES_C, RESULT_C))
    assert STAGE14C_SOURCE_HEAD in combined
    assert "1130 passed in 898.22s (0:14:58)" in combined
    assert STAGE14C_SYNC_HEAD in combined
    assert "1132 passed in 877.20s (0:14:37)" in combined
    for phrase in (
        "108", "2916", "23328", "36/36", "8748",
        "1.6653345369377348e-16", "2.220446049250313e-16", "8.881784197001252e-16",
        "0.5", "3.0 to 5.0", "0.9999999999999998", "1.0000000000000002",
        "two_clock_observable_incomplete",
        "four_class_physical_quotient_established",
        "Stage 14C representative-independent Dirac / three-condition relational / four-class quotient descent = established",
        "compensated relational descent != refoliation invariance",
        "repository validation != new scientific evidence",
    ):
        assert phrase in combined


def test_stage14d_repository_checkpoint_and_deterministic_evidence_are_synchronized():
    combined = "\n".join((PROTOCOL, NOTES_D, RESULT_D))
    assert STAGE14D_SOURCE_HEAD in combined
    assert "1139 passed in 889.88s (0:14:49)" in combined
    assert STAGE14D_SYNC_HEAD in combined
    assert "1140 passed in 562.70s (0:09:22)" in combined
    for phrase in (
        "324", "216/216", "72/72", "108/108",
        "0.3843557173958058", "1.135254038874606",
        "singular_scalar_rescaling_rejected",
        "216 = 108 positive + 108 off-surface",
        "determinant", "4 classes × 27 representatives",
        "Stage 14D Stage-13-style scalar-rescaling obstruction with triangular basis equivalence on the frozen finite carrier = established",
        "Stage-13-style scalar-rescaling obstruction != universal non-Abelianizability",
        "triangular basis equivalence != universal basis trivializability",
        "basis-equivalent finite quotient != refoliation invariance",
        "repository validation != new scientific evidence",
    ):
        assert phrase in combined


def test_stage14e_repository_checkpoint_and_deterministic_evidence_are_synchronized():
    combined = "\n".join((PROTOCOL, NOTES_E, RESULT_E))
    assert STAGE14E_SOURCE_HEAD in combined
    assert STAGE14E_MERGE_CHECKOUT in combined
    assert "#1890" in combined
    assert "1148 passed in 897.57s (0:14:57)" in combined
    for phrase in (
        "108",
        "4",
        "864",
        "1728",
        "216",
        "0.014943579189526601",
        "structure_function_path_operational_payloads_descend",
        "basis_operational_payloads_descend",
        "representative_dependent_payload_corruption_detected",
        "path_dependent_payload_corruption_detected",
        "basis_dependent_payload_corruption_detected",
        "criteria_39_43_satisfied",
        "Stage 14E typed O/P/R/V/Xi and future-measurement descent across structure-function paths and original/triangular basis choices on the frozen finite family = established",
        "compensated-path operational descent != refoliation invariance",
        "basis-equivalent operational descent != refoliation invariance",
        "future-measurement covariance != future actuality",
        "orbit-sensitive witness != empirical prediction",
        "repository validation != new scientific evidence",
    ):
        assert phrase in combined


def test_stage14f_repository_checkpoint_and_deterministic_evidence_are_synchronized():
    combined = "\n".join((PROTOCOL, NOTES_F, RESULT_F))
    assert STAGE14F_SOURCE_HEAD in combined
    assert STAGE14F_SOURCE_MERGE_CHECKOUT in combined
    assert "#1900" in combined
    assert "1154 passed in 664.20s (0:11:04)" in combined
    assert STAGE14F_NOTES_RESULTS_HEAD in combined
    assert STAGE14F_NOTES_RESULTS_MERGE_CHECKOUT in combined
    assert "#1904" in combined
    assert "1154 passed in 562.70s (0:09:22)" in combined
    for phrase in (
        "14 controls",
        "14/14",
        "108/108",
        "1728",
        "8748",
        "36/36",
        "72",
        "0.075",
        "0.175",
        "criteria_44_47_satisfied",
        "typed_operational_context_rejected",
        "false_universal_abelianization_interpretation_rejected",
        "Stage 14F ablation / anomaly / false-positive controls on the frozen structure-function carrier = established",
        "negative-control rejection != positive-family obstruction",
        "constraint-algebra anomaly != fundamental physical non-Abelianity",
        "control rejection != hypersurface-deformation algebra",
        "control rejection != general relativity",
        "repository validation != new scientific evidence",
    ):
        assert phrase in combined


def test_stage14f_closes_frozen_criteria_44_through_47_only():
    for criterion in (
        "39. Stage 14E constructs representative-level typed O/P/R/V/Xi architectures over the 108 positive representatives — **satisfied**.",
        "40. Licensed compensated path choices preserve quotient-level public O/P/R/V and future-measurement payloads — **satisfied**.",
        "41. Path, structure-function, compensator, and basis provenance are retained in Xi without being silently collapsed into quotient-level physical content — **satisfied**.",
        "42. Orbit-sensitive public / measurement signatures remain stable within each physical quotient class and discriminate the frozen physical classes where declared — **satisfied**.",
        "43. Representative/path/basis-dependent payload corruption controls are detected, while successful operational descent is not promoted to future actuality or empirical discovery — **satisfied**.",
        "44. Stage 14F executes the frozen ablation family, including missing-third-direction and structure-function-removed controls — **satisfied**.",
        "45. `H_2_bad=H_2+epsilon q` is detected as a constraint-algebra anomaly rather than admitted as positive evidence — **satisfied**.",
        "46. Wrong-compensator, incomplete-observable, cross-orbit, singular-basis, and false-typing controls are explicitly classified and rejected — **satisfied**.",
        "47. Control results remain bounded away from hypersurface-deformation algebra, GR, fundamental non-Abelianity, eternalism, or ontological becoming — **satisfied**.",
    ):
        assert criterion in PROTOCOL
    assert "48. Stage 14G executable synthesis selects exactly one frozen Stage 14 status from the validated Stage 14A–F evidence chain — **pending**." in PROTOCOL
    assert "49. The next research gate is evidence-selected without presupposing GR, refoliation invariance, gravitational field degrees of freedom, or a metaphysical conclusion — **pending**." in PROTOCOL
    assert "50. External final full-repository regression and merge-readiness review — **pending**." in PROTOCOL


def test_stage14_interpretation_boundaries_remain_explicit():
    combined = "\n".join(
        (
            PROTOCOL, FREEZE,
            NOTES_A, RESULT_A, NOTES_B, RESULT_B, NOTES_C, RESULT_C,
            NOTES_D, RESULT_D, NOTES_E, RESULT_E, NOTES_F, RESULT_F,
        )
    )
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
        "compensated relational descent != refoliation invariance",
        "compensated-path operational descent != refoliation invariance",
        "basis-equivalent operational descent != refoliation invariance",
        "Stage-13-style scalar-rescaling obstruction != universal non-Abelianizability",
        "triangular basis equivalence != universal basis trivializability",
        "constraint-basis change != physical-orbit change",
        "basis-equivalent finite quotient != refoliation invariance",
        "commuting triangular presentation != proof that all admissible presentations commute",
        "basis equivalence != hypersurface-deformation algebra",
        "basis equivalence != general relativity",
        "basis equivalence != ontological becoming",
        "structure-function/path Xi provenance != quotient-level physical content",
        "basis-specific Xi provenance != quotient-level physical content",
        "path word != physical temporal history",
        "path word != modal continuation",
        "wrong compensator failure != physical time asymmetry",
        "two-clock incompleteness != physical time asymmetry",
        "compensated path closure != ontological becoming",
        "complete relational observable != ontological becoming by definition",
        "complete three-condition relational observable != ontological becoming by definition",
        "Dirac-invariant data + relational change != proof of eternalism",
        "gauge quotient != elimination of physical change",
        "four-class gauge quotient != elimination of physical change",
        "finite relational covariance != metaphysical becoming",
        "future-measurement covariance != future actuality",
        "orbit-sensitive witness != empirical prediction",
        "negative-control rejection != positive-family obstruction",
        "structure-function removal != evidence against the positive carrier",
        "missing-third-direction failure != physical time asymmetry",
        "constraint-algebra anomaly != ontological becoming",
        "constraint-algebra anomaly != fundamental physical non-Abelianity",
        "control rejection != hypersurface-deformation algebra",
        "control rejection != general relativity",
        "cross-orbit rejection != spacetime causal separation",
        "singular-basis rejection != universal non-Abelianizability",
        "false typing rejection != empirical discovery",
        "finite-model success != empirical discovery",
        "repository validation != new scientific evidence",
        "not_established != false",
    ):
        assert phrase in combined
