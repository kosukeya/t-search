from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = (ROOT / "docs" / "stage12_protocol.md").read_text(encoding="utf-8")
FREEZE = (ROOT / "results" / "stage12_0_protocol_freeze.md").read_text(encoding="utf-8")
NOTES_A = (ROOT / "docs" / "stage12a_notes.md").read_text(encoding="utf-8")
NOTES_B = (ROOT / "docs" / "stage12b_notes.md").read_text(encoding="utf-8")
RESULT_B = (ROOT / "results" / "stage12b_relational.md").read_text(encoding="utf-8")

SELECTED_STAGE12 = (
    "Construct a multi-orbit constraint-generated gauge atlas that separates "
    "gauge-related parameterizations from physically distinct orbits and tests "
    "whether relational/Dirac observables and the typed O/P/R/V measurement "
    "architecture descend consistently across that atlas."
)


def test_stage12_gate_and_stage11_boundary_are_synchronized() -> None:
    for text in (PROTOCOL, FREEZE):
        assert SELECTED_STAGE12 in text
        assert "one-orbit covariance != multi-orbit gauge covariance" in text
        assert "constraint-generated gauge precursor != general relativity" in text


def test_stage12_type_separation_is_frozen() -> None:
    combined = PROTOCOL + "\n" + FREEZE
    for phrase in (
        "physical orbit identity != point on orbit",
        "constraint-generated gauge flow != external reparameterization by definition",
        "constraint orbit != modal continuation",
        "different physical orbit != later event on one orbit",
        "internal clock perspective != external parameterization != gauge-flow parameter",
    ):
        assert phrase in combined


def test_stage12_constraint_flow_and_dirac_invariants_are_frozen() -> None:
    for phrase in (
        "C = p_T + p^2/2 approx 0",
        "dT/ds = 1",
        "dq/ds = p",
        "dp/ds = 0",
        "dp_T/ds = 0",
        "P_D = p",
        "Q_D = q - p T",
        "q(T=tau) = Q_D + P_D tau",
    ):
        assert phrase in PROTOCOL
    assert "Dirac-invariant orbit data can be constant while relational change" in PROTOCOL


def test_stage12_canonical_multi_orbit_family_is_frozen() -> None:
    compact = PROTOCOL.replace(" ", "")
    for orbit_id, pair in (
        ("omega_alpha", "(-0.35,1.25)"),
        ("omega_beta", "(0.40,1.25)"),
        ("omega_gamma", "(-0.35,0.75)"),
        ("omega_delta", "(0.20,1.75)"),
    ):
        assert orbit_id in PROTOCOL
        assert pair in compact
    assert "same momentum, different relational intercept" in PROTOCOL
    assert "same intercept, different momentum" in PROTOCOL


def test_stage12_gauge_equivalence_and_noncollapse_rules_are_frozen() -> None:
    combined = PROTOCOL + "\n" + FREEZE
    assert "different (Q_D,P_D) => different physical orbit" in combined
    assert "same physical orbit -> quotient-invariant licensed content" in PROTOCOL
    assert "different physical orbit -> not collapsed merely by gauge quotienting" in PROTOCOL
    assert (
        "quotient invariance without physical-orbit discrimination != successful multi-orbit gauge atlas"
        in combined
    )


def test_stage12_reuses_stage11_parameter_and_measurement_architecture() -> None:
    for phrase in (
        "f_id(lambda)=lambda",
        "f_aff(lambda)=2 lambda + 1",
        "f_cub(lambda)=lambda + lambda^3/4",
        "f_sinh(lambda)=sinh(lambda)",
        "N'(lambda') = N(lambda)/f'(lambda)",
        "T11_candidate=(O,P,R,V;Xi)",
        "QExt(e1)={h_L,h_R}",
        "future_signature_left",
        "future_signature_other",
        "orbit-sensitive operational witness",
    ):
        assert phrase in PROTOCOL


def test_stage12_clock_reparameterization_gauge_targets_are_frozen() -> None:
    for phrase in (
        "C o Phi ~= Phi o C",
        "G o Phi ~= Phi o G",
        "C o G ~= G o C",
        "commuting finite gauge/clock diagrams != general covariance",
    ):
        assert phrase in PROTOCOL


def test_stage12_false_positive_controls_are_frozen() -> None:
    combined = PROTOCOL + "\n" + FREEZE
    for phrase in (
        "omega_alpha",
        "omega_beta",
        "omega_gamma",
        "equal raw",
        "orbit-insensitive measurement",
        "modal continuation",
        "orientation reversal",
        "physically distinct orbits",
    ):
        assert phrase in combined


def test_stage12b_closes_criteria_17_23_while_freeze_remains_historical() -> None:
    assert "Stage 12B completed; criteria 1–23 satisfied; criteria 24–50 pending" in PROTOCOL
    assert "Stage 12.0 completed; criteria 1–10 satisfied; criteria 11–50 pending" in FREEZE
    for criterion in range(1, 51):
        assert f"{criterion}." in PROTOCOL
    assert PROTOCOL.count("**satisfied**") == 23
    assert PROTOCOL.count("**pending**") == 27


def test_stage12a_implementation_checkpoint_remains_documented() -> None:
    combined = PROTOCOL + "\n" + NOTES_A
    for phrase in (
        "20 representatives total",
        "80 transports total",
        "16 external parameterization views",
        "constraint_generated_gauge_flow",
        "external_reparameterization",
        "clock coordinate T != gauge-flow parameter s by type",
    ):
        assert phrase in combined


def test_stage12b_implementation_checkpoint_is_documented() -> None:
    combined = PROTOCOL + "\n" + NOTES_B + "\n" + RESULT_B
    for phrase in (
        "20 representative Dirac estimates",
        "16 external Dirac estimates",
        "144 relational q(T=tau) evaluations",
        "232 relational derivative evaluations",
        "30 equal-T",
        "2 equal-q",
        "312 equal-raw-lambda",
        "full-Dirac-pair discrimination in this finite family != universal orbit-classification theorem",
        "relational change != ontological becoming by definition",
    ):
        assert phrase in combined


def test_stage12_sequence_and_synthesis_vocabulary_are_frozen() -> None:
    for stage in (
        "Stage 12A — multi-orbit constrained carrier and explicit gauge-flow representatives — **completed**",
        "Stage 12B — Dirac/relational observables and physical-orbit discrimination — **completed**",
        "Stage 12C — typed gauge atlas, quotient, and descent of relational structure — **next**",
        "Stage 12D — O/P/R/V/Xi and orbit-sensitive future-measurement descent",
        "Stage 12E — internal clock × external parameterization × gauge-flow compatibility",
        "Stage 12F — ablation / wrong-orbit / false-positive controls",
        "Stage 12G — executable synthesis and evidence-selected next gate",
    ):
        assert stage in PROTOCOL
    for status in (
        "multi_orbit_gauge_covariant",
        "multi_orbit_gauge_partial",
        "multi_orbit_gauge_obstructed",
        "inconclusive",
    ):
        assert status in PROTOCOL


def test_stage12_interpretation_guards_remain_explicit() -> None:
    combined = PROTOCOL + "\n" + FREEZE + "\n" + NOTES_A + "\n" + NOTES_B
    for phrase in (
        "constraint-generated gauge flow != ontological becoming",
        "Dirac invariant != timeless ontology by definition",
        "Dirac-invariant data + relational change != proof of eternalism",
        "relational change != ontological becoming by definition",
        "gauge quotient != elimination of physical change",
        "multi-orbit gauge covariance != general covariance",
        "single Hamiltonian constraint != hypersurface-deformation algebra",
        "finite-model success != empirical discovery",
        "not_established != false",
    ):
        assert phrase in combined
