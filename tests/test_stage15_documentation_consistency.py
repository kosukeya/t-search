from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")
ROADMAP = (ROOT / "docs" / "roadmap.md").read_text(encoding="utf-8")
PROTOCOL = (ROOT / "docs" / "stage15_protocol.md").read_text(encoding="utf-8")
FREEZE = (ROOT / "results" / "stage15_0_protocol_freeze.md").read_text(encoding="utf-8")

SELECTED_STAGE15 = (
    "Construct a minimal spatially indexed first-class constraint-algebra precursor with explicit "
    "local/smeared generators and nontrivial structure-function dependence, test whether the Stage 14 "
    "triangular Abelianization persists under the declared locality-preserving basis class, and retest "
    "the physical quotient, relational observables, and typed O/P/R/V measurement architecture without "
    "assuming general relativity or refoliation invariance."
)


def test_stage15_selected_gate_and_stage14_baseline_are_frozen():
    for text in (README, ROADMAP, PROTOCOL, FREEZE):
        assert SELECTED_STAGE15 in text
    combined = PROTOCOL + "\n" + FREEZE
    assert "Stage 14 is completed and merged via PR #15" in combined
    assert "structure_function_path_covariant_scalar_obstructed" in combined
    assert "spatially_indexed_constraint_algebra_precursor" in combined


def test_stage15_protocol_freezes_the_outcome_discriminating_carrier():
    combined = PROTOCOL + "\n" + FREEZE
    for phrase in (
        "Lambda={0,1,2}",
        "0~1~2",
        "K_i = pi_i + c_i P",
        "C_0 = K_0 + kappa T_0 K_1",
        "C_1 = K_1 + kappa T_1 K_2",
        "C_2 = K_2",
        "{C_0,C_1} = -kappa^2 T_0 C_2",
        "27 representatives per physical orbit",
        "108 positive representatives total",
        "four classes of 27 representatives",
        "P_D=P",
        "Q_D=Q-sum_i c_i T_i",
    ):
        assert phrase in combined


def test_stage15_locality_class_is_frozen_before_basis_results():
    combined = PROTOCOL + "\n" + FREEZE
    for phrase in (
        "L1-locality-preserving",
        "L0",
        "Lfinite",
        "nonlocal_for_stage15_L1",
        "K_2=C_2",
        "K_1=C_1-kappa T_1 C_2",
        "K_0=C_0-kappa T_0 C_1+kappa^2 T_0 T_1 C_2",
        "known distance-2 seed reconstruction != proof that every Abelianization is nonlocal",
        "L1 obstruction != universal non-Abelianizability",
        "only-nonlocal Abelianization found != fundamental physical non-Abelianity",
    ):
        assert phrase in combined


def test_stage15_freeze_closes_only_criteria_one_through_ten():
    assert "Stage 15.0 completed; criteria 1–10 satisfied; criteria 11–50 pending." in FREEZE
    assert "Criteria **1–10** are satisfied by the freeze." in FREEZE
    assert "Criteria **11–50** remain pending." in FREEZE
    assert "protocol preflight != Stage 15A scientific evidence" in FREEZE
    assert "Stage 15A — local/smeared first-class carrier and finite representative family — **next**" in FREEZE


def test_stage15_synthesis_vocabulary_and_interpretation_guards_are_frozen():
    combined = PROTOCOL + "\n" + FREEZE
    for phrase in (
        "spatial_local_path_covariant_local_abelianizable",
        "spatial_local_path_covariant_locality_obstructed",
        "spatial_local_path_covariant_basis_inconclusive",
        "spatial_local_path_partial",
        "spatial_local_path_obstructed",
        "spatially indexed constraint precursor != general relativity",
        "nearest-neighbor graph locality != relativistic locality",
        "finite smeared algebra != continuum hypersurface-deformation algebra",
        "known nonlocal Abelianization != proof of locality-protected non-Abelianity",
        "complete relational observable != ontological becoming by definition",
        "future-measurement covariance != future actuality",
        "not_established != false",
    ):
        assert phrase in combined
