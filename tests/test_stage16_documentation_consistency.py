from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = (ROOT / "docs" / "stage16_protocol.md").read_text(encoding="utf-8")
FREEZE = (ROOT / "results" / "stage16_0_protocol_freeze.md").read_text(encoding="utf-8")

BASELINE_MERGE = "cca49e37b3d4171ea74fd6c15fa119fcd4392e2d"
SELECTED_STAGE16 = (
    "Construct a minimal four-site closed-cycle spatially indexed first-class constraint-algebra precursor "
    "with no terminal seed generator, retain explicit local/smeared structure-function dependence, test "
    "whether one-step L1 or finite-depth locality-preserving Abelianization still exists, and retest "
    "compensated paths, the physical quotient, complete relational observables, and typed O/P/R/V/Xi "
    "descent without assuming general relativity or refoliation invariance."
)


def test_stage16_selected_gate_and_stage15_merged_baseline_are_frozen():
    combined = PROTOCOL + "\n" + FREEZE
    assert BASELINE_MERGE in combined
    assert "Stage 15 is completed and merged via PR #16" in combined
    assert "spatial_local_path_covariant_local_abelianizable" in combined
    assert "four_site_closed_cycle_constraint_algebra_precursor" in combined
    assert SELECTED_STAGE16 in combined


def test_stage16_cycle_carrier_and_global_inverse_are_frozen():
    combined = PROTOCOL + "\n" + FREEZE
    for phrase in (
        "Lambda=C4={0,1,2,3}",
        "0~1~2~3~0",
        "K_i=pi_i+c_i P",
        "a_i=kappa T_i",
        "C_i = K_i + a_i K_{i+1 mod 4}",
        "C_3=K_3+kappa T_3 K_0",
        "Delta=1-kappa^4 T_0 T_1 T_2 T_3",
        "Delta in {15/16, 1, 17/16}",
        "K_i = (C_i - a_i C_{i+1} + a_i a_{i+1} C_{i+2} - a_i a_{i+1} a_{i+2} C_{i+3}) / Delta",
        "known global seed reconstruction != proof that every Abelianization is nonlocal",
    ):
        assert phrase in combined


def test_stage16_algebra_support_and_representative_targets_are_frozen():
    combined = PROTOCOL + "\n" + FREEZE
    for phrase in (
        "{C_i,C_{i+1}}=-kappa^2 T_i K_{i+2}",
        "{C_0,C_2}=0",
        "{C_1,C_3}=0",
        "local canonical support != local closure-coordinate support",
        "81 representatives per physical orbit and 324 positive representatives total",
        "four classes of 81 representatives",
        "P_D=P",
        "Q_D=Q-sum_i c_i T_i",
        "Q(T_0=tau_0,T_1=tau_1,T_2=tau_2,T_3=tau_3)=Q_D+sum_i c_i tau_i",
    ):
        assert phrase in combined


def test_stage16_path_and_basis_search_bounds_are_frozen_before_results():
    combined = PROTOCOL + "\n" + FREEZE
    for phrase in (
        "STAGE16_LOCAL_STEP_PAIRS={(0.5,0.5),(-0.5,0.5)}",
        "all 24 permutations of the four labels `(0,1,2,3)`",
        "Parameters are bounded to `[-2,2]`",
        "N_1(i)={i-1,i,i+1}",
        "L1-locality-preserving",
        "L0",
        "Lfinite",
        "nonlocal_for_stage16_L1",
        "STAGE16_LFINITE_SEARCH_MAX_DEPTH=4",
        "translation-covariant affine L1 ansatz",
        "no L1 witness in frozen search != no L1 Abelianization exists",
    ):
        assert phrase in combined


def test_stage16_topology_controls_typed_carry_forward_and_guards_are_frozen():
    combined = PROTOCOL + "\n" + FREEZE
    for phrase in (
        "wrap-edge opening control",
        "three-site projection control",
        "three-cycle locality-degeneracy control",
        "singular-frame control using `kappa=1`",
        "T_candidate=(O,P,R,V;Xi)",
        "e1=(-1,-1,-1,-1)",
        "e2=(1,1,1,1)",
        "cycle path defect != spacetime curvature",
        "failure to Abelianize != ontological becoming",
        "presented compensator not found in frozen word search != physical obstruction",
        "future-measurement covariance != future actuality",
        "typed operational descent != ontological equivalence",
    ):
        assert phrase in combined


def test_stage16_freeze_closes_only_criteria_one_through_ten():
    assert "Stage 16.0 completed; criteria 1–10 satisfied; criteria 11–50 pending." in FREEZE
    assert "Criteria **1–10** are satisfied by the freeze." in FREEZE
    assert "Criteria **11–50** remain pending." in FREEZE
    assert "protocol preflight != Stage 16A scientific evidence" in FREEZE
    assert "Stage 16A — four-site cyclic first-class carrier, local/smeared algebra, support audits, and finite representative family — **next**" in FREEZE


def test_stage16_synthesis_vocabulary_and_stage17_ranking_pool_are_frozen():
    combined = PROTOCOL + "\n" + FREEZE
    for phrase in (
        "closed_cycle_local_path_covariant_L1_abelianizable",
        "closed_cycle_local_path_covariant_Lfinite_abelianizable",
        "closed_cycle_local_path_covariant_nonlocal_only_in_declared_search",
        "closed_cycle_local_path_covariant_basis_inconclusive",
        "closed_cycle_local_path_partial",
        "closed_cycle_local_path_obstructed",
        "larger_sparse_graph_locality_scaling_audit",
        "admissible_basis_transformation_completeness_audit",
        "path_cycle_tree_topology_comparison_family",
        "gravitational_minisuperspace_extension",
        "nonideal_povm_clock_extension",
        "record_thermodynamic_potentiality_integration",
        "closed_cycle_carrier_repair_or_reformulation",
    ):
        assert phrase in combined
