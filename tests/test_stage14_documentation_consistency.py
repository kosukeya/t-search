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


def test_stage14_protocol_closes_all_fifty_criteria():
    assert (
        "Stage 14 completed at the criterion-50 merge-readiness checkpoint; criteria 1–50 satisfied. "
        "PR #15 is merge-ready, Draft, open, and unmerged."
    ) in PROTOCOL
    assert PROTOCOL.count("**satisfied**") == 50
    assert PROTOCOL.count("**pending**") == 0
    for phrase in (
        "Stage 14A — three-constraint first-class structure-function carrier and finite representative family — **completed**",
        "Stage 14B — phase-space-dependent mixed paths and third-direction compensation — **completed**",
        "Stage 14C — Dirac / three-condition complete relational observables, physical quotient, and orbit discrimination — **completed**",
        "Stage 14D — simple-scalar-rescaling obstruction vs triangular-basis equivalence pressure test — **completed**",
        "Stage 14E — typed O/P/R/V/Xi and future-measurement descent across structure-function paths/bases — **completed**",
        "Stage 14F — ablation / anomaly / false-positive controls — **completed**",
        "Stage 14G — executable synthesis and evidence-selected next gate — **completed**",
        "criterion 50 — external final full-repository regression / merge-readiness review — **completed**",
        "50. External final full-repository regression and merge-readiness review — **satisfied**.",
    ):
        assert phrase in PROTOCOL


def test_stage14_frozen_mathematical_targets_remain_present():
    combined = PROTOCOL + "\n" + FREEZE
    for phrase in (
        "(T1,p_1; T2,p_2; X,p_X; q,p)",
        "a=0.5", "b=0.25", "kappa=0.5",
        "D = p_X + a p approx 0",
        "H_1 = p_1 + p^2/2 approx 0",
        "H_2 = p_2 + b p + kappa T1 X D approx 0",
        "{H_1,D}=0", "{H_1,H_2}=-kappa X D", "{H_2,D}=kappa T1 D",
        "f_12^D(z)=-kappa X", "f_2D^D(z)=kappa T1",
        "27 representatives per physical orbit", "108 positive representatives total",
        "864 ordered mixed pairs", "v_21D-v_12D",
        "P_D=p", "Q_D=q-p T1-b T2-a X",
        "q(T1=tau1,T2=tau2,X=chi)",
        "simple_scalar_rescaling", "-kappa X f_1 f_2 / f_D",
        "H_2_tilde = H_2 - kappa T1 X D = p_2 + b p",
    ):
        assert phrase in combined


def test_stage14_a_through_f_validated_evidence_remains_synchronized():
    a = "\n".join((PROTOCOL, NOTES_A, RESULT_A))
    for phrase in (
        "1106 passed in 879.78s (0:14:39)",
        "1113 passed in 545.23s (0:09:05)",
        "1114 passed in 900.17s (0:15:00)",
        "0.7812880785647448",
        "Stage 14A three-constraint first-class structure-function carrier and finite representative family = established",
    ):
        assert phrase in a

    b = "\n".join((PROTOCOL, NOTES_B, RESULT_B))
    for phrase in (
        "1122 passed in 891.20s (0:14:51)",
        "1123 passed in 548.54s (0:09:08)",
        "0.3934693402873666", "2.3504023872876028", "8748",
        "Stage 14B phase-space-dependent mixed paths and exact third-direction compensation on the frozen finite family = established",
    ):
        assert phrase in b

    c = "\n".join((PROTOCOL, NOTES_C, RESULT_C))
    for phrase in (
        "1130 passed in 898.22s (0:14:58)",
        "1132 passed in 877.20s (0:14:37)",
        "2916", "23328", "36/36", "8.881784197001252e-16",
        "Stage 14C representative-independent Dirac / three-condition relational / four-class quotient descent = established",
    ):
        assert phrase in c

    d = "\n".join((PROTOCOL, NOTES_D, RESULT_D))
    for phrase in (
        "1139 passed in 889.88s (0:14:49)",
        "1140 passed in 562.70s (0:09:22)",
        "216/216", "72/72", "0.3843557173958058", "1.135254038874606",
        "Stage 14D Stage-13-style scalar-rescaling obstruction with triangular basis equivalence on the frozen finite carrier = established",
    ):
        assert phrase in d

    e = "\n".join((PROTOCOL, NOTES_E, RESULT_E))
    for phrase in (
        "1148 passed in 897.57s (0:14:57)",
        "0.014943579189526601",
        "representative_dependent_payload_corruption_detected",
        "path_dependent_payload_corruption_detected",
        "basis_dependent_payload_corruption_detected",
        "Stage 14E typed O/P/R/V/Xi and future-measurement descent across structure-function paths and original/triangular basis choices on the frozen finite family = established",
    ):
        assert phrase in e

    f = "\n".join((PROTOCOL, NOTES_F, RESULT_F))
    for phrase in (
        "1154 passed in 664.20s (0:11:04)",
        "1154 passed in 562.70s (0:09:22)",
        "1155 passed in 850.27s (0:14:10)",
        "14/14", "108/108", "0.075", "0.175",
        "Stage 14F ablation / anomaly / false-positive controls on the frozen structure-function carrier = established",
    ):
        assert phrase in f


def test_stage14g_synthesis_and_stage15_gate_are_synchronized():
    combined = "\n".join((PROTOCOL, NOTES_G, RESULT_G))
    assert "#1910" in combined
    assert "1168 passed in 891.95s (0:14:51)" in combined
    assert "1 failed, 1167 passed in 551.59s (0:09:11)" in combined
    assert (
        "Stage 14G synthesis on the validated Stage 14A-F finite evidence chain = "
        "structure_function_path_covariant_scalar_obstructed"
    ) in combined
    for phrase in (
        "864/864", "6/6", "4 quotient classes × 27 representatives", "23328",
        "216/216", "108/108", "14/14",
        "spatially_indexed_constraint_algebra_precursor",
        "admissible_basis_transformation_audit",
        "gravitational_minisuperspace_extension",
        "richer_causal_order", "nonideal_povm_clocks",
        "score **13**", "score **10**", "score **8**", "score **7**",
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


def test_stage14_interpretation_boundaries_remain_explicit():
    combined = "\n".join(
        (PROTOCOL, FREEZE, NOTES_A, RESULT_A, NOTES_B, RESULT_B, NOTES_C, RESULT_C,
         NOTES_D, RESULT_D, NOTES_E, RESULT_E, NOTES_F, RESULT_F, NOTES_G, RESULT_G, RESULT_50)
    )
    for phrase in (
        "phase-space-dependent structure-function precursor != hypersurface-deformation algebra by definition",
        "structure functions != spacetime geometry by definition",
        "three constraint labels != three independent gauge directions",
        "raw path-word inequality != physical path dependence",
        "third-direction compensation != refoliation invariance",
        "Stage-13-style scalar-rescaling obstruction != universal non-Abelianizability",
        "diagonal scalar-rescaling obstruction != fundamental physical non-Abelianity",
        "triangular basis equivalence != universal basis trivializability",
        "constraint-basis change != physical-orbit change",
        "path word != physical temporal history",
        "wrong compensator failure != physical time asymmetry",
        "complete three-condition relational observable != ontological becoming by definition",
        "Dirac-invariant data + relational change != proof of eternalism",
        "gauge quotient != elimination of physical change",
        "negative-control rejection != positive-family obstruction",
        "constraint-algebra anomaly != fundamental physical non-Abelianity",
        "future-measurement covariance != future actuality",
        "spatially indexed constraint precursor != general relativity",
        "local/smeared precursor != spacetime diffeomorphism invariance by definition",
        "finite-model success != empirical discovery",
        "repository validation != new scientific evidence",
        "merge-ready != merged",
        "not_established != false",
    ):
        assert phrase in combined
