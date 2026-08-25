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
NOTES_G = (ROOT / "docs" / "stage14g_notes.md").read_text(encoding="utf-8")
RESULT_G = (ROOT / "results" / "stage14g_synthesis_stage15_gate.md").read_text(encoding="utf-8")
RESULT_50 = (ROOT / "results" / "stage14_criterion50_merge_readiness.md").read_text(encoding="utf-8")
STAGE13_G = (ROOT / "results" / "stage13g_synthesis_stage14_gate.md").read_text(encoding="utf-8")

SELECTED_STAGE14 = (
    "Construct a minimal phase-space-dependent structure-function / hypersurface-deformation precursor "
    "designed to test whether the Stage 13F simple commuting-basis trivialization persists, and retest "
    "the physical quotient, relational observables, and typed O/P/R/V measurement architecture without "
    "assuming general relativity or refoliation invariance."
)
SELECTED_STAGE15 = (
    "Construct a minimal spatially indexed first-class constraint-algebra precursor with explicit "
    "local/smeared generators and nontrivial structure-function dependence, test whether the Stage 14 "
    "triangular Abelianization persists under the declared locality-preserving basis class, and retest "
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
STAGE14F_CLOSURE_HEAD = "83e00e4ada2870c33e09006e25074b909be5a975"
STAGE14G_SOURCE_HEAD = "c109d1ed1c9a1f043ed741a934c32b139ca15e09"
STAGE14G_SOURCE_MERGE_CHECKOUT = "45a13aeff70010e05ee97f32f3114f7335a13502"
STAGE14_CRITERION50_REVIEWED_HEAD = "ab500148975ecea6e03fe8678ba1e8dcc50cb666"
STAGE14_CRITERION50_MERGE_CHECKOUT = "c4cafff62da2ba0726153e977724f3f78c8d2ff7"


def test_stage14_selected_gate_and_merged_stage13_baseline_are_frozen():
    for text in (PROTOCOL, FREEZE, STAGE13_G, README, ROADMAP):
        assert SELECTED_STAGE14 in text
    combined = PROTOCOL + "\n" + FREEZE
    assert MERGED_STAGE13_MAIN in combined
    assert FINAL_STAGE13_HEAD in combined
    assert "1099 passed in 893.92s (0:14:53)" in combined
    assert "multi_constraint_path_covariant" in combined
    assert "phase_space_structure_function_precursor" in combined


def test_stage14_status_closes_exactly_criteria_1_through_50():
    assert (
        "Stage 14 completed at the criterion-50 merge-readiness checkpoint; criteria 1–50 satisfied. "
        "PR #15 is merge-ready, Draft, open, and unmerged."
    ) in PROTOCOL
    assert PROTOCOL.count("**satisfied**") == 50
    assert PROTOCOL.count("**pending**") == 0
    assert "Stage 14.0 completed; criteria 1–10 satisfied; criteria 11–50 pending." in FREEZE
    for phrase in (
        "Stage 14A — three-constraint first-class structure-function carrier and finite representative family — **completed**",
        "Stage 14B — phase-space-dependent mixed paths and third-direction compensation — **completed**",
        "Stage 14C — Dirac / three-condition complete relational observables, physical quotient, and orbit discrimination — **completed**",
        "Stage 14D — simple-scalar-rescaling obstruction vs triangular-basis-equivalence pressure test — **completed**",
        "Stage 14E — typed O/P/R/V/Xi and future-measurement descent across structure-function paths/bases — **completed**",
        "Stage 14F — ablation / anomaly / false-positive controls — **completed**",
        "Stage 14G — executable synthesis and evidence-selected next gate — **completed**",
        "criterion 50 — external final full-repository regression / merge-readiness review — **completed**",
    ):
        assert phrase in PROTOCOL


def test_stage14_positive_carrier_paths_relational_and_basis_targets_remain_frozen():
    combined = PROTOCOL + "\n" + FREEZE
    for phrase in (
        "(T1,p_1; T2,p_2; X,p_X; q,p)",
        "a=0.5", "b=0.25", "kappa=0.5",
        "D = p_X + a p approx 0",
        "H_1 = p_1 + p^2/2 approx 0",
        "H_2 = p_2 + b p + kappa T1 X D approx 0",
        "{H_1,D}=0", "{H_1,H_2}=-kappa X D", "{H_2,D}=kappa T1 D",
        "f_12^D(z)=-kappa X", "f_2D^D(z)=kappa T1", "Jacobi",
        "27 representatives per physical orbit", "108 positive representatives total",
        "864 ordered mixed pairs", "v_21D-v_12D",
        "X_0 [exp(kappa T1_1 u)-exp(kappa T1_0 u)]",
        "P_D=p", "Q_D=q-p T1-b T2-a X",
        "q(T1=tau1,T2=tau2,X=chi)", "two-clock",
        "simple_scalar_rescaling", "-kappa X f_1 f_2 / f_D",
        "H_2_tilde = H_2 - kappa T1 X D = p_2 + b p",
    ):
        assert phrase in combined


def test_stage14_control_and_synthesis_vocabularies_remain_frozen():
    combined = PROTOCOL + "\n" + FREEZE
    for phrase in (
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
        "structure_function_path_covariant_scalar_obstructed",
        "structure_function_path_covariant_scalar_trivializable",
        "structure_function_path_partial",
        "structure_function_path_obstructed",
        "inconclusive",
    ):
        assert phrase in combined


def test_stage14a_b_repository_checkpoints_remain_synchronized():
    a = "\n".join((PROTOCOL, NOTES_A, RESULT_A))
    assert STAGE14_FREEZE_HEAD in a
    assert STAGE14A_SOURCE_HEAD in a
    assert STAGE14A_SYNC_HEAD in a
    assert "1106 passed in 879.78s (0:14:39)" in a
    assert "1113 passed in 545.23s (0:09:05)" in a
    assert "1114 passed in 900.17s (0:15:00)" in a
    assert "0.7812880785647448" in a
    assert "Stage 14A three-constraint first-class structure-function carrier and finite representative family = established" in a

    b = "\n".join((PROTOCOL, NOTES_B, RESULT_B))
    assert STAGE14B_SOURCE_HEAD in b
    assert STAGE14B_SYNC_HEAD in b
    assert "1122 passed in 891.20s (0:14:51)" in b
    assert "1123 passed in 548.54s (0:09:08)" in b
    for phrase in ("864", "1728", "576", "288", "8748", "0.3934693402873666", "2.3504023872876028"):
        assert phrase in b
    assert "Stage 14B phase-space-dependent mixed paths and exact third-direction compensation on the frozen finite family = established" in b


def test_stage14c_d_repository_checkpoints_remain_synchronized():
    c = "\n".join((PROTOCOL, NOTES_C, RESULT_C))
    assert STAGE14C_SOURCE_HEAD in c
    assert STAGE14C_SYNC_HEAD in c
    assert "1130 passed in 898.22s (0:14:58)" in c
    assert "1132 passed in 877.20s (0:14:37)" in c
    for phrase in ("2916", "23328", "36/36", "8748", "8.881784197001252e-16"):
        assert phrase in c
    assert "Stage 14C representative-independent Dirac / three-condition relational / four-class quotient descent = established" in c

    d = "\n".join((PROTOCOL, NOTES_D, RESULT_D))
    assert STAGE14D_SOURCE_HEAD in d
    assert STAGE14D_SYNC_HEAD in d
    assert "1139 passed in 889.88s (0:14:49)" in d
    assert "1140 passed in 562.70s (0:09:22)" in d
    for phrase in ("324", "216/216", "72/72", "0.3843557173958058", "1.135254038874606", "determinant"):
        assert phrase in d
    assert "Stage 14D Stage-13-style scalar-rescaling obstruction with triangular basis equivalence on the frozen finite carrier = established" in d


def test_stage14e_f_repository_checkpoints_remain_synchronized():
    e = "\n".join((PROTOCOL, NOTES_E, RESULT_E))
    assert STAGE14E_SOURCE_HEAD in e
    assert STAGE14E_MERGE_CHECKOUT in e
    assert "#1890" in e
    assert "1148 passed in 897.57s (0:14:57)" in e
    for phrase in (
        "864", "1728", "216", "0.014943579189526601",
        "representative_dependent_payload_corruption_detected",
        "path_dependent_payload_corruption_detected",
        "basis_dependent_payload_corruption_detected",
        "criteria_39_43_satisfied",
    ):
        assert phrase in e
    assert "Stage 14E typed O/P/R/V/Xi and future-measurement descent across structure-function paths and original/triangular basis choices on the frozen finite family = established" in e

    f = "\n".join((PROTOCOL, NOTES_F, RESULT_F))
    assert STAGE14F_SOURCE_HEAD in f
    assert STAGE14F_SOURCE_MERGE_CHECKOUT in f
    assert STAGE14F_NOTES_RESULTS_HEAD in f
    assert STAGE14F_NOTES_RESULTS_MERGE_CHECKOUT in f
    assert STAGE14F_CLOSURE_HEAD in f
    assert "#1900" in f and "#1904" in f and "#1906" in f
    assert "1154 passed in 664.20s (0:11:04)" in f
    assert "1154 passed in 562.70s (0:09:22)" in f
    assert "1155 passed in 850.27s (0:14:10)" in f
    for phrase in ("14/14", "108/108", "1728", "8748", "36/36", "72", "0.075", "0.175"):
        assert phrase in f
    assert "Stage 14F ablation / anomaly / false-positive controls on the frozen structure-function carrier = established" in f


def test_stage14g_repository_checkpoint_synthesis_and_gate_are_synchronized():
    combined = "\n".join((PROTOCOL, NOTES_G, RESULT_G))
    assert STAGE14G_SOURCE_HEAD in combined
    assert STAGE14G_SOURCE_MERGE_CHECKOUT in combined
    assert "#1910" in combined
    assert "1168 passed in 891.95s (0:14:51)" in combined
    assert "1 failed, 1167 passed in 551.59s (0:09:11)" in combined
    assert (
        "Stage 14G synthesis on the validated Stage 14A-F finite evidence chain = "
        "structure_function_path_covariant_scalar_obstructed"
    ) in combined
    for phrase in (
        "864/864",
        "6/6",
        "4 quotient classes × 27 representatives",
        "23328",
        "216/216",
        "108/108",
        "14/14",
        "spatially_indexed_constraint_algebra_precursor",
        "admissible_basis_transformation_audit",
        "gravitational_minisuperspace_extension",
        "richer_causal_order",
        "nonideal_povm_clocks",
        "score **13**",
        "score **10**",
        "score **8**",
        "score **7**",
    ):
        assert phrase in combined
    assert SELECTED_STAGE15 in combined


def test_stage14_criterion50_review_is_synchronized():
    combined = "\n".join((PROTOCOL, RESULT_50))
    assert STAGE14_CRITERION50_REVIEWED_HEAD in combined
    assert STAGE14_CRITERION50_MERGE_CHECKOUT in combined
    assert "#1922" in combined
    assert "1166 passed in 709.02s (0:11:49)" in combined
    for phrase in (
        "ahead: **46** commits",
        "behind: **0** commits",
        "changed files: **39**",
        "mergeable = true",
        "submitted reviews: **0**",
        "unresolved inline review threads: **0**",
        "PR conversation comments: **0**",
        "Stage 14 criterion 50 external final full-repository regression / merge-readiness review = satisfied",
        "Stage 14 criteria **1–50** are completed",
        "structure_function_path_covariant_scalar_obstructed",
        "spatially_indexed_constraint_algebra_precursor",
        "repository validation != new scientific evidence",
        "merge-ready != merged",
    ):
        assert phrase in combined


def test_stage14_closes_frozen_criteria_48_through_50():
    assert "48. Stage 14G executable synthesis selects exactly one frozen Stage 14 status from the validated Stage 14A–F evidence chain — **satisfied**." in PROTOCOL
    assert "49. The next research gate is evidence-selected without presupposing GR, refoliation invariance, gravitational field degrees of freedom, or a metaphysical conclusion — **satisfied**." in PROTOCOL
    assert "50. External final full-repository regression and merge-readiness review — **satisfied**." in PROTOCOL


def test_stage14g_basis_pressure_and_next_gate_boundaries_remain_explicit():
    combined = "\n".join((PROTOCOL, NOTES_G, RESULT_G, RESULT_50))
    for phrase in (
        "diagonal scalar-rescaling obstruction != fundamental physical non-Abelianity",
        "triangular basis equivalence != universal basis trivializability",
        "structure_function_path_covariant_scalar_obstructed finite family != refoliation invariance",
        "finite first-class structure-function algebra != hypersurface-deformation algebra",
        "spatially indexed constraint precursor != hypersurface-deformation algebra by definition",
        "spatially indexed constraint precursor != general relativity",
        "local/smeared precursor != spacetime diffeomorphism invariance by definition",
        "future-measurement covariance != future actuality",
        "Dirac-invariant data + relational change != proof of eternalism",
        "complete relational observable != ontological becoming by definition",
        "finite-model success != empirical discovery",
        "repository validation != new scientific evidence",
    ):
        assert phrase in combined


def test_stage14_persistent_interpretation_boundaries_remain_explicit():
    combined = "\n".join(
        (
            PROTOCOL, FREEZE,
            NOTES_A, RESULT_A, NOTES_B, RESULT_B, NOTES_C, RESULT_C,
            NOTES_D, RESULT_D, NOTES_E, RESULT_E, NOTES_F, RESULT_F,
            NOTES_G, RESULT_G, RESULT_50,
        )
    )
    for phrase in (
        "phase-space-dependent structure-function precursor != hypersurface-deformation algebra by definition",
        "structure functions != spacetime geometry by definition",
        "three constraint labels != three independent gauge directions",
        "raw path-word inequality != physical path dependence",
        "third-direction compensation != refoliation invariance",
        "compensated mixed-path closure != refoliation invariance",
        "Stage-13-style scalar-rescaling obstruction != universal non-Abelianizability",
        "constraint-basis change != physical-orbit change",
        "basis-equivalent finite quotient != refoliation invariance",
        "path word != physical temporal history",
        "wrong compensator failure != physical time asymmetry",
        "two-clock incompleteness != physical time asymmetry",
        "complete three-condition relational observable != ontological becoming by definition",
        "gauge quotient != elimination of physical change",
        "negative-control rejection != positive-family obstruction",
        "constraint-algebra anomaly != ontological becoming",
        "constraint-algebra anomaly != fundamental physical non-Abelianity",
        "control rejection != general relativity",
        "cross-orbit rejection != spacetime causal separation",
        "singular-basis rejection != universal non-Abelianizability",
        "false typing rejection != empirical discovery",
        "not_established != false",
    ):
        assert phrase in combined
