"""Stage 16G executable synthesis and evidence-selected Stage 17 gate."""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache

from .stage16_basis import (
    STAGE16D_CLASSIFICATION,
    stage16d_diagnostics,
)
from .stage16_controls import stage16f_diagnostics
from .stage16_local import stage16a_diagnostics
from .stage16_measurement import stage16e_diagnostics
from .stage16_paths import stage16b_diagnostics
from .stage16_relational import stage16c_diagnostics

STAGE16G_SYNTHESIS_VOCABULARY = (
    "closed_cycle_local_path_covariant_L1_abelianizable",
    "closed_cycle_local_path_covariant_Lfinite_abelianizable",
    "closed_cycle_local_path_covariant_nonlocal_only_in_declared_search",
    "closed_cycle_local_path_covariant_basis_inconclusive",
    "closed_cycle_local_path_partial",
    "closed_cycle_local_path_obstructed",
    "inconclusive",
)

STAGE16G_SELECTED_CLASSIFICATION = (
    "closed_cycle_local_path_covariant_nonlocal_only_in_declared_search"
)

STAGE17_CANDIDATE_POOL = (
    "larger_sparse_graph_locality_scaling_audit",
    "admissible_basis_transformation_completeness_audit",
    "path_cycle_tree_topology_comparison_family",
    "gravitational_minisuperspace_extension",
    "nonideal_povm_clock_extension",
    "record_thermodynamic_potentiality_integration",
    "closed_cycle_carrier_repair_or_reformulation",
)

STAGE17_SELECTED_GATE = "admissible_basis_transformation_completeness_audit"
STAGE17_SELECTED_GATE_STATEMENT = (
    "Audit a broader admissible locality-preserving basis-transformation class on the "
    "validated four-site closed-cycle carrier beyond the frozen affine cyclic one-step "
    "L1 ansatz and depth<=4 elementary-shear compositions; seek either a constructive "
    "local strongly commuting witness or a bounded completeness/nonexistence certificate, "
    "while preserving invertibility, the four-class quotient, the Dirac pair, complete "
    "four-clock relational observables, and typed O/P/R/V/Xi content, without promoting "
    "search failure to a universal physical locality obstruction."
)

STAGE16G_BOUNDED_RESULT = (
    "Stage 16 closed four-cycle first-class/path/quotient/typed structure is validated; "
    "a global strongly commuting basis exists, while no local strongly commuting witness "
    "was found in the declared Stage 16D local searches, and topology-opening controls "
    "recover finite-depth local witnesses. This supports only the bounded classification "
    "closed_cycle_local_path_covariant_nonlocal_only_in_declared_search."
)

STAGE16G_GUARDS = (
    "nonlocal_only_in_declared_search != universal locality obstruction",
    "no L1 witness in frozen search != no L1 Abelianization exists",
    "global Abelianization != physical triviality",
    "cycle opening changes graph topology != proof that topology is ontic",
    "topology-sensitive exhibited depth != spacetime topology theorem",
    "local canonical support != local closure-coordinate support",
    "compensated cycle path closure != refoliation invariance",
    "complete relational observable != ontological becoming by definition",
    "failure to Abelianize != ontological becoming",
    "future-measurement covariance != future actuality",
    "typed operational descent != ontological equivalence",
    "Stage 17 completeness audit selection != predicted locality obstruction",
    "repository validation != new scientific evidence",
)


@dataclass(frozen=True, slots=True)
class Stage17CandidateScore:
    selector_id: str
    discriminating_power: int
    prerequisite_readiness: int
    locality_topology_specificity: int
    confound_resistance: int
    tractability: int
    rationale: str

    @property
    def total(self) -> int:
        return (
            self.discriminating_power
            + self.prerequisite_readiness
            + self.locality_topology_specificity
            + self.confound_resistance
            + self.tractability
        )


@dataclass(frozen=True, slots=True)
class Stage16GDiagnostics:
    stage16a_validated: bool
    stage16b_validated: bool
    stage16c_validated: bool
    stage16d_validated: bool
    stage16e_validated: bool
    stage16f_validated: bool
    all_stage16a_f_evidence_validated: bool
    global_abelianization_established: bool
    local_witness_found_in_frozen_search: bool
    stage16d_classification: str
    presented_local_compensator_success_count: int
    presented_local_compensator_probe_count: int
    quotient_class_count: int
    typed_public_quotient_count: int
    control_count: int
    rejected_control_count: int
    cycle_opening_exhibited_depth: int | None
    three_site_projection_one_step_l1: bool
    synthesis_classification: str
    candidate_count: int
    selected_stage17_gate: str
    selected_stage17_score: int
    runner_up_stage17_gate: str
    runner_up_stage17_score: int
    criteria_48_49_satisfied: bool


def _validate_score(score: Stage17CandidateScore) -> None:
    values = (
        score.discriminating_power,
        score.prerequisite_readiness,
        score.locality_topology_specificity,
        score.confound_resistance,
        score.tractability,
    )
    if any(value < 0 or value > 3 for value in values):
        raise ValueError("Stage 17 frozen rubric axes must each be scored from 0 to 3")


@lru_cache(maxsize=1)
def canonical_stage17_candidate_scores() -> tuple[Stage17CandidateScore, ...]:
    """Evidence-specific Stage 17 scoring under the Stage 16.0 frozen five-axis rubric."""
    scores = (
        Stage17CandidateScore(
            "larger_sparse_graph_locality_scaling_audit", 2, 3, 3, 3, 2,
            "Directly tests scaling of locality cost, but Stage 16 first leaves a completeness "
            "confound: larger-graph failures would remain hard to interpret if the admissible "
            "basis class is still incompletely audited.",
        ),
        Stage17CandidateScore(
            "admissible_basis_transformation_completeness_audit", 3, 3, 3, 3, 3,
            "Targets the central residual uncertainty left by Stage 16D: whether the bounded "
            "absence of local witnesses reflects the frozen search families or a certifiable "
            "obstruction within a broader declared admissible class. The validated C4 carrier, "
            "exact symbolic tooling, quotient, relational, and typed audits are already ready.",
        ),
        Stage17CandidateScore(
            "path_cycle_tree_topology_comparison_family", 3, 3, 3, 3, 2,
            "Stage 16F shows depth-1 open C3 and depth-2 wrap-open C4 witnesses while the closed "
            "C4 declared search finds none, so topology comparison is highly discriminating; "
            "however it remains partly confounded until the closed-cycle basis class is audited "
            "more completely.",
        ),
        Stage17CandidateScore(
            "gravitational_minisuperspace_extension", 1, 2, 1, 1, 1,
            "Physically richer, but it does not directly resolve the current basis-completeness "
            "uncertainty and would introduce substantial new covariance/interpretation confounds.",
        ),
        Stage17CandidateScore(
            "nonideal_povm_clock_extension", 1, 2, 0, 2, 2,
            "Useful for quantum-clock robustness, but orthogonal to the locality/topology basis "
            "uncertainty that Stage 16 newly exposed.",
        ),
        Stage17CandidateScore(
            "record_thermodynamic_potentiality_integration", 1, 2, 0, 1, 2,
            "Relevant to longer-term becoming/record questions, but premature before the current "
            "representation/locality ambiguity is better controlled.",
        ),
        Stage17CandidateScore(
            "closed_cycle_carrier_repair_or_reformulation", 0, 3, 2, 3, 3,
            "The carrier did not fail: algebra, paths, quotient, relational, typed descent, and "
            "destructive controls all validate. Repair is therefore not evidence-selected now.",
        ),
    )
    if {score.selector_id for score in scores} != set(STAGE17_CANDIDATE_POOL):
        raise ValueError("Stage 17 score table must exactly cover the frozen candidate pool")
    for score in scores:
        _validate_score(score)
    return scores


def ranked_stage17_candidates() -> tuple[Stage17CandidateScore, ...]:
    """Frozen tie-break: total, discriminating power, readiness, lexical selector id."""
    return tuple(
        sorted(
            canonical_stage17_candidate_scores(),
            key=lambda score: (
                -score.total,
                -score.discriminating_power,
                -score.prerequisite_readiness,
                score.selector_id,
            ),
        )
    )


def stage16g_select_classification() -> str:
    a = stage16a_diagnostics()
    b = stage16b_diagnostics()
    c = stage16c_diagnostics()
    d = stage16d_diagnostics()
    e = stage16e_diagnostics()
    f = stage16f_diagnostics()

    if not all((
        a.criteria_11_17_satisfied,
        b.criteria_18_24_satisfied,
        c.criteria_25_31_satisfied,
        d.criteria_32_39_satisfied,
        e.criteria_40_44_satisfied,
        f.criteria_45_47_satisfied,
    )):
        return "inconclusive"

    if d.classification == "one_step_L1_abelianization_witness_found":
        return "closed_cycle_local_path_covariant_L1_abelianizable"
    if d.classification == "no_L1_witness_in_frozen_search_but_Lfinite_witness_found":
        return "closed_cycle_local_path_covariant_Lfinite_abelianizable"
    if d.classification == "only_nonlocal_abelianization_witness_found_in_frozen_search":
        return "closed_cycle_local_path_covariant_nonlocal_only_in_declared_search"
    if d.classification in (
        "no_local_witness_found_in_declared_search",
        "basis_search_inconclusive",
    ):
        return "closed_cycle_local_path_covariant_basis_inconclusive"
    return "closed_cycle_local_path_partial"


@lru_cache(maxsize=1)
def stage16g_diagnostics() -> Stage16GDiagnostics:
    a = stage16a_diagnostics()
    b = stage16b_diagnostics()
    c = stage16c_diagnostics()
    d = stage16d_diagnostics()
    e = stage16e_diagnostics()
    f = stage16f_diagnostics()
    ranking = ranked_stage17_candidates()
    selected = stage16g_select_classification()
    all_validated = all((
        a.criteria_11_17_satisfied,
        b.criteria_18_24_satisfied,
        c.criteria_25_31_satisfied,
        d.criteria_32_39_satisfied,
        e.criteria_40_44_satisfied,
        f.criteria_45_47_satisfied,
    ))
    criteria = (
        all_validated
        and selected in STAGE16G_SYNTHESIS_VOCABULARY
        and selected == STAGE16G_SELECTED_CLASSIFICATION
        and len(ranking) == len(STAGE17_CANDIDATE_POOL) == 7
        and ranking[0].selector_id == STAGE17_SELECTED_GATE
        and ranking[0].total > ranking[1].total
    )
    return Stage16GDiagnostics(
        stage16a_validated=a.criteria_11_17_satisfied,
        stage16b_validated=b.criteria_18_24_satisfied,
        stage16c_validated=c.criteria_25_31_satisfied,
        stage16d_validated=d.criteria_32_39_satisfied,
        stage16e_validated=e.criteria_40_44_satisfied,
        stage16f_validated=f.criteria_45_47_satisfied,
        all_stage16a_f_evidence_validated=all_validated,
        global_abelianization_established=d.global_abelianization_established,
        local_witness_found_in_frozen_search=d.local_witness_found_in_frozen_search,
        stage16d_classification=STAGE16D_CLASSIFICATION,
        presented_local_compensator_success_count=b.presented_search_success_count,
        presented_local_compensator_probe_count=b.local_probe_count,
        quotient_class_count=c.quotient_class_count,
        typed_public_quotient_count=e.distinct_public_count,
        control_count=f.control_count,
        rejected_control_count=f.rejected_control_count,
        cycle_opening_exhibited_depth=f.cycle_opening_exhibited_depth,
        three_site_projection_one_step_l1=f.three_site_projection_one_step_l1,
        synthesis_classification=selected,
        candidate_count=len(ranking),
        selected_stage17_gate=ranking[0].selector_id,
        selected_stage17_score=ranking[0].total,
        runner_up_stage17_gate=ranking[1].selector_id,
        runner_up_stage17_score=ranking[1].total,
        criteria_48_49_satisfied=bool(criteria),
    )


def stage16g_summary() -> dict[str, object]:
    d = stage16g_diagnostics()
    return {
        "classification": d.synthesis_classification,
        "selected_stage17_gate": d.selected_stage17_gate,
        "selected_stage17_score": d.selected_stage17_score,
        "runner_up_stage17_gate": d.runner_up_stage17_gate,
        "runner_up_stage17_score": d.runner_up_stage17_score,
        "criteria_48_49_satisfied": d.criteria_48_49_satisfied,
        "bounded_result": STAGE16G_BOUNDED_RESULT,
        "selected_gate_statement": STAGE17_SELECTED_GATE_STATEMENT,
        "guards": STAGE16G_GUARDS,
    }
