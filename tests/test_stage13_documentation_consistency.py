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
STAGE13A_FINAL_HEAD = "178f4ac8d160e7b261cd854f8c1856aa80c76675"
STAGE13B_SOURCE_HEAD = "645ce6ab099d5f9db573c29ba81ac0854c4c26ca"
STAGE13B_FINAL_HEAD = "d559c031590a058962c50d170b144acbe8eabadd"
STAGE13C_SOURCE_HEAD = "56f80e8984872591a26f27eb5902310e36616bf0"
STAGE13C_FINAL_HEAD = "51f119845ec0e9ade3ee8cdeeb4e00ca7b992569"
STAGE13D_SOURCE_HEAD = "ab7a5c4a917e7612ee89b547baddf127d48947e7"


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


def test_stage13_current_status_is_stage13d_38_12() -> None:
    assert "Stage 13D completed; criteria 1–38 satisfied; criteria 39–50 pending" in PROTOCOL
    assert PROTOCOL.count("**satisfied**") == 38
    assert PROTOCOL.count("**pending**") == 12
    for text in (README, ROADMAP):
        assert "Stage 13D" in text
        assert "criteria 1–38" in text
        assert "criteria 39–50" in text
        assert "Stage 13E" in text
        assert "87" in text
        assert "144" in text
        assert "4" in text
        assert "9" in text
        assert "36" in text
        assert "1296" in text
        assert "path_provenance_typed_lost_numerically_reconstructible" in text
    for path in (
        "docs/stage13_protocol.md",
        "results/stage13_0_protocol_freeze.md",
        "docs/stage13a_notes.md",
        "results/stage13a_multi_constraint.md",
        "docs/stage13b_notes.md",
        "results/stage13b_paths.md",
        "docs/stage13c_notes.md",
        "results/stage13c_relational.md",
        "docs/stage13d_notes.md",
        "results/stage13d_gauge_atlas.md",
    ):
        assert path in README


def test_stage13_two_constraint_carrier_and_flows_remain_frozen() -> None:
    combined = PROTOCOL + "\n" + FREEZE
    for phrase in (
        "(T,p_T; X,p_X; q,p)",
        "K_T = p_T + p^2/2 approx 0",
        "K_X = exp(T) (p_X + a p) approx 0",
        "a = 0.5",
        "{K_T,K_X} = -K_X",
        "dT/ds = 1",
        "dq/ds = p",
        "dX/du = exp(T)",
        "dq/du = a exp(T)",
        "Phi_T(s)",
        "Phi_X(u)",
        "two constraint labels != two independent gauge directions",
        "first-class closure on this toy carrier != hypersurface-deformation algebra",
    ):
        assert phrase in combined


def test_stage13_compensated_path_law_remains_executable_evidence() -> None:
    combined = "\n".join((PROTOCOL, FREEZE, NOTES_B, RESULT_B))
    for phrase in (
        "s = T1 - T0",
        "DeltaX = X1 - X0",
        "u_TX = DeltaX / exp(T1)",
        "u_XT = DeltaX / exp(T0)",
        "u_XT = exp(s) u_TX",
        "compensated_path_closure_established",
        "wrong_compensator_detected",
        "same_raw_parameter_reorder_false_positive_rejected",
        "raw gauge-path commutativity != successful multi-constraint closure",
        "wrong compensator failure != physical time asymmetry",
    ):
        assert phrase in combined


def test_stage13_dirac_and_two_clock_structure_is_executable_evidence() -> None:
    combined = "\n".join((PROTOCOL, FREEZE, NOTES_C, RESULT_C))
    for phrase in (
        "P_D = p",
        "Q_D = q - p T - a X",
        "q(T=tau,X=chi) = Q_D + P_D tau + a chi",
        "q(T=tau; X raw) = Q_D + P_D tau + a X",
        "one clock condition in a two-gauge-direction model != complete relational observable",
        "complete relational observable != ontological becoming by definition",
        "one_clock_observable_incomplete",
        "compensated_path_complete_relational_covariance_established",
    ):
        assert phrase in combined


def test_stage13_physical_orbit_grid_and_basis_controls_remain_frozen() -> None:
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
        "K_X_tilde = exp(-T) K_X = p_X + a p",
        "{K_T,K_X_tilde}=0",
        "noncommuting constraint presentation != fundamental physical non-Abelianity",
        "constraint-basis change != physical-orbit change",
        "path-word history != quotient-level physical state",
    ):
        assert phrase in PROTOCOL + "\n" + FREEZE


def test_stage13_false_positive_and_oprv_resources_remain_frozen() -> None:
    combined = PROTOCOL + "\n" + FREEZE
    for phrase in (
        "K_X_bad",
        "epsilon q",
        "rank_deficient_constraint_control_rejected",
        "constraint_algebra_anomaly_detected",
        "basis_presentation_equivalent",
        "cross_orbit_path_rejected",
        "representative_dependent_payload_corruption_detected",
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


def test_stage13a_through_stage13c_evidence_is_preserved() -> None:
    combined_a = "\n".join((PROTOCOL, NOTES_A, RESULT_A))
    combined_b = "\n".join((PROTOCOL, NOTES_B, RESULT_B))
    combined_c = "\n".join((PROTOCOL, NOTES_C, RESULT_C))
    assert STAGE13A_SOURCE_HEAD in combined_a
    assert STAGE13A_FINAL_HEAD in combined_b
    assert STAGE13B_SOURCE_HEAD in combined_b
    assert STAGE13B_FINAL_HEAD in combined_c
    assert STAGE13C_SOURCE_HEAD in combined_c
    assert STAGE13C_FINAL_HEAD in README
    assert "1048 passed in 592.23s (0:09:52)" in combined_a
    assert "1050 passed in 886.76s (0:14:46)" in combined_b
    assert "1058 passed in 696.20s (0:11:36)" in combined_b
    assert "1059 passed in 538.54s (0:08:58)" in combined_c
    assert "1069 passed in 550.80s (0:09:10)" in combined_c
    assert "1066 passed in 892.04s (0:14:52)" in README


def test_stage13d_executable_evidence_is_synchronized() -> None:
    combined = "\n".join((PROTOCOL, NOTES_D, RESULT_D, README, ROADMAP))
    assert STAGE13D_SOURCE_HEAD in combined
    assert "1076 passed in 908.96s (0:15:08)" in combined
    for phrase in (
        "87 typed nodes",
        "144 typed single-generator arrows",
        "4 quotient classes",
        "9 representatives",
        "36 quotient-level descent evaluations",
        "144 / 144",
        "1296",
        "path_provenance_typed_lost_numerically_reconstructible",
        "typed_status = lost",
        "numerical_status = reconstructible",
        "path word != modal continuation",
        "path word != physical temporal history",
        "Stage 13D typed multi-constraint gauge atlas, path words, quotient, and descent on the frozen finite family = established",
    ):
        assert phrase in combined


def test_stage13d_closes_exactly_criteria_32_38() -> None:
    satisfied_lines = (
        "32. Typed nodes distinguish physical orbit, representative, generator/basis, path word, event, clock, and modal roles — **satisfied**.",
        "33. The multi-constraint atlas is built from typed `Phi_T` / `Phi_X` connectivity rather than stored orbit labels — **satisfied**.",
        "34. The quotient recovers exactly four physical classes of nine representatives each — **satisfied**.",
        "35. Different compensated path words to corresponding representatives descend to the same quotient-level Dirac/relational payload — **satisfied**.",
        "36. Distinct physical Dirac data are not collapsed by path connectivity — **satisfied**.",
        "37. Path-word / compensator removal is classified separately from numerical reconstructibility — **satisfied**.",
        "38. Path word is not identified with modal continuation or physical temporal history — **satisfied**.",
    )
    for line in satisfied_lines:
        assert line in PROTOCOL
    assert PROTOCOL.count("**satisfied**") == 38
    assert PROTOCOL.count("**pending**") == 12
    assert "39. O/P/R/V/Xi architecture is lifted over every canonical Stage 13 representative with path/basis provenance confined to Xi — **pending**." in PROTOCOL
    assert "50. External final full-repository regression and merge-readiness review — **pending**." in PROTOCOL


def test_stage13_sequence_moves_only_to_stage13e() -> None:
    for stage in (
        "Stage 13A — two-constraint first-class carrier and finite representative family — **completed**",
        "Stage 13B — noncommuting gauge paths and compensated closure — **completed**",
        "Stage 13C — Dirac / two-clock complete relational observables and physical-orbit discrimination — **completed**",
        "Stage 13D — typed multi-constraint gauge atlas, path words, quotient, and descent — **completed**",
        "Stage 13E — O/P/R/V/Xi and future-measurement descent across compensated path choices — **next**",
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
    combined = "\n".join(
        (PROTOCOL, FREEZE, NOTES_A, RESULT_A, NOTES_B, RESULT_B, NOTES_C, RESULT_C, NOTES_D, RESULT_D, README, ROADMAP)
    )
    for phrase in (
        "two constraint labels != two independent gauge directions",
        "Stage 13A single-generator surface preservation != compensated multi-generator path closure",
        "raw gauge-path commutativity != successful multi-constraint closure",
        "same raw generator parameters under reordered paths != corresponding gauge path",
        "constraint-surface preservation != correct source/target path correspondence",
        "compensated multi-constraint path closure != refoliation invariance",
        "compensated-path relational covariance != refoliation invariance",
        "noncommuting constraint presentation != fundamental physical non-Abelianity",
        "constraint-algebra/refoliation precursor != general relativity",
        "path word != physical temporal history",
        "path word != modal continuation",
        "path-order mismatch != arrow of time by definition",
        "wrong compensator failure != physical time asymmetry",
        "one clock condition in a two-gauge-direction model != complete relational observable",
        "complete relational observable != ontological becoming by definition",
        "Dirac invariant != timeless ontology by definition",
        "Dirac-invariant data + relational change != proof of eternalism",
        "full-Dirac-pair discrimination in this finite family != universal orbit-classification theorem",
        "gauge quotient != elimination of physical change",
        "path-independent complete-relational values != future actuality",
        "numerical reconstructibility != typed operational identification",
        "reconstructible != universally redundant",
        "lost != metaphysically irreducible",
        "finite-model success != empirical discovery",
        "not_established != false",
    ):
        assert phrase in combined
