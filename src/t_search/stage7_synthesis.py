"""Stage 7G synthesis, exit audit, and evidence-selected Stage 8 gate.

The synthesis is derived from executable Stage 7A--F diagnostics.  It decides
whether the Stage 6 layered candidate is strengthened, reduced, broken, or
inconclusive in the bounded finite-model sense, then ranks the frozen Stage 8
gates by discriminating power.

The decision deliberately separates three claims:

* the P/O/R core can be strengthened by one-model evidence;
* explicit edge matrices inside P can nevertheless be reconstructible;
* V has not yet been integrated into the same quantum construction.

None of these statements establishes a fundamental ontology of time.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from functools import lru_cache
from typing import Any

import numpy as np

from .stage5_clock_change import DEFAULT_ATOL, SUBSYSTEMS
from .stage6_record_modality import canonical_modal_transport
from .stage7_ablation import (
    ABLATION_IDS,
    RoleStatus,
    build_stage7f_ablation_matrix,
    r_reconstruction_from_p_o_diagnostics,
    stage7f_mismatch_matrix,
    stage7f_summary,
)
from .stage7_accessibility_atlas import (
    stage7e_accessibility_diagnostics,
    stage7e_partial_atlas_diagnostics,
)
from .stage7_history import (
    CURRENT_EVENT,
    assess_relational_record,
    balanced_forward_reverse_assessment,
    canonical_history_model,
    history_constraint_operator,
    uncertain_memory_control_assessment,
)
from .stage7_record import (
    canonical_target_pair_projector,
    memory_pauli_z,
    stage7b_record_diagnostics,
)
from .stage7_record_transport import (
    event_correspondence,
    stage7d_reduction_diagnostics,
    stage7d_transport_diagnostics,
)
from .stage7_spectator import (
    spectator_clock_change_diagnostics,
    spectator_composition_diagnostics,
    spectator_no_record_diagnostics,
    spectator_physical_projector,
    spectator_reconstruction_operator,
    spectator_reduction_operator,
    spectator_support_projector,
    spectator_total_constraint_operator,
    stage7a_summary,
)


class Stage7SynthesisChoice(str, Enum):
    STRENGTHENED = "strengthened"
    REDUCED = "reduced"
    BROKEN = "broken"
    INCONCLUSIVE = "inconclusive"


@dataclass(frozen=True)
class ProjectQuestionAnswer:
    question_id: str
    question: str
    answer: str
    evidence_class: str
    evidence_refs: tuple[str, ...]
    boundary: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "question_id": self.question_id,
            "question": self.question,
            "answer": self.answer,
            "evidence_class": self.evidence_class,
            "evidence_refs": list(self.evidence_refs),
            "boundary": self.boundary,
        }


@dataclass(frozen=True)
class Stage8GateCandidate:
    gate_id: str
    label: str
    score: int
    pressure_signals: tuple[str, ...]
    rationale: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "gate_id": self.gate_id,
            "label": self.label,
            "score": self.score,
            "pressure_signals": list(self.pressure_signals),
            "rationale": self.rationale,
        }


@dataclass(frozen=True)
class Stage7EvidenceSnapshot:
    stage7a: dict[str, object]
    stage7b: object
    forward: object
    reversed: object
    no_record: object
    uncertain: object
    balanced: object
    stage7d_reduction: object
    stage7d_transport: object
    stage7e_accessibility: object
    stage7e_atlas: object
    stage7f: dict[str, object]
    r_reconstruction: object


@dataclass(frozen=True)
class Stage7GSynthesis:
    choice: Stage7SynthesisChoice
    strengthened_scope: tuple[str, ...]
    refinement_inside_p: tuple[str, ...]
    unintegrated_layers: tuple[str, ...]
    compatibility_links: tuple[str, ...]
    project_questions: tuple[ProjectQuestionAnswer, ...]
    unresolved_implications: tuple[str, ...]
    stage8_candidates: tuple[Stage8GateCandidate, ...]
    selected_stage8_gate: str
    pre_merge_exit_criteria_passed: int
    pre_merge_exit_criteria_total: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "choice": self.choice.value,
            "strengthened_scope": list(self.strengthened_scope),
            "refinement_inside_P": list(self.refinement_inside_p),
            "unintegrated_layers": list(self.unintegrated_layers),
            "compatibility_links": list(self.compatibility_links),
            "project_questions": [item.as_dict() for item in self.project_questions],
            "unresolved_implications": list(self.unresolved_implications),
            "stage8_candidates": [item.as_dict() for item in self.stage8_candidates],
            "selected_stage8_gate": self.selected_stage8_gate,
            "pre_merge_exit_criteria_passed": self.pre_merge_exit_criteria_passed,
            "pre_merge_exit_criteria_total": self.pre_merge_exit_criteria_total,
        }


@lru_cache(maxsize=1)
def evidence_snapshot() -> Stage7EvidenceSnapshot:
    return Stage7EvidenceSnapshot(
        stage7a=stage7a_summary(),
        stage7b=stage7b_record_diagnostics(),
        forward=assess_relational_record("forward"),
        reversed=assess_relational_record("reversed"),
        no_record=assess_relational_record("no-record"),
        uncertain=uncertain_memory_control_assessment(),
        balanced=balanced_forward_reverse_assessment(),
        stage7d_reduction=stage7d_reduction_diagnostics(),
        stage7d_transport=stage7d_transport_diagnostics(),
        stage7e_accessibility=stage7e_accessibility_diagnostics(),
        stage7e_atlas=stage7e_partial_atlas_diagnostics(),
        stage7f=stage7f_summary(),
        r_reconstruction=r_reconstruction_from_p_o_diagnostics(),
    )


def select_synthesis_choice(snapshot: Stage7EvidenceSnapshot | None = None) -> Stage7SynthesisChoice:
    evidence = evidence_snapshot() if snapshot is None else snapshot
    transport = evidence.stage7d_transport
    reconstruction = evidence.r_reconstruction
    ablation = evidence.stage7f["own_role_status_after_neutralization"]

    pr_compatible = bool(
        transport.preserving_covariance
        and transport.reversing_covariance
        and transport.max_metric_covariance_residual <= 1e-9
    )
    p_o_without_r = bool(
        reconstruction.p_and_o_retained_without_r
        and not reconstruction.reconstruction_witness_found
    )
    r_resource_lost = bool(
        ablation["memory_record_resource"] == RoleStatus.LOST.value
        and ablation["record_coupling"] == RoleStatus.LOST.value
    )
    explicit_maps_reconstructible = bool(
        ablation["explicit_perspective_maps"] == RoleStatus.RECONSTRUCTIBLE.value
    )

    if pr_compatible and p_o_without_r and r_resource_lost and explicit_maps_reconstructible:
        return Stage7SynthesisChoice.STRENGTHENED
    if reconstruction.reconstruction_witness_found:
        return Stage7SynthesisChoice.REDUCED
    if not pr_compatible:
        return Stage7SynthesisChoice.BROKEN
    return Stage7SynthesisChoice.INCONCLUSIVE


def unresolved_implications() -> tuple[str, ...]:
    """Claims Stage 7 still does not establish.

    Stage 7 directly refutes the narrower implication P + internal O => the
    declared record role R in this model family.  Broader metaphysical or modal
    implications remain untested and are not converted into false claims.
    """

    return (
        "physical_clock_change => temporal_succession",
        "record_defined_direction => ontological_future_openness",
        "record_defined_direction => thermodynamic_arrow",
        "record_defined_direction => phenomenal_passage",
        "perspective_consistency => modal_equivalence",
        "Potentiality => phenomenal_passage",
        "finite_P_O_R_compatibility => general_covariance",
        "layered_O_P_R_V_Xi_candidate => fundamental_or_unique_time_ontology",
    )


def answer_project_questions() -> tuple[ProjectQuestionAnswer, ...]:
    return (
        ProjectQuestionAnswer(
            "Q1",
            "Can target-specific record structure coexist with genuine physical clock changes in one constrained quantum model?",
            "Yes in the declared Stage 7 interacting family, with corresponding states, induced metrics, observables, and event correspondence transported together.",
            "established_finite_model_result",
            ("Stage7C:record-history", "Stage7D:P-R-covariance"),
            "This is finite-model covariance, not general covariance or a universal reference-frame theorem.",
        ),
        ProjectQuestionAnswer(
            "Q2",
            "Do retained perspective structure P and internal neutral order/history O determine record structure R?",
            "No in the declared Stage 7 family: the internally anchored no-record construction retains full-rank multi-clock transport while A_R=A_acc=0.",
            "established_finite_model_result",
            ("Stage7F:no-record-P-plus-O",),
            "This counterexample refutes the implication only in the declared family; it does not prove universal impossibility of record emergence from other P/O dynamics.",
        ),
        ProjectQuestionAnswer(
            "Q3",
            "Does a globally represented record guarantee local accessibility?",
            "No. Hidden and maximally noisy interfaces preserve the global represented record while the local record diagnostic becomes inaccessible.",
            "established_finite_model_result",
            ("Stage7E:accessibility", "Stage7F:access-ablation"),
            "Local interface failure is not global record destruction.",
        ),
        ProjectQuestionAnswer(
            "Q4",
            "Are explicit cross-clock edge matrices primitive within P?",
            "Not in the declared Stage 7 interface: all 54 explicit edge matrices are reconstructible from the common physical carrier and per-node reductions C_X.",
            "established_finite_model_result",
            ("Stage7F:perspective-map-reconstruction",),
            "This refines the representation of P; it does not eliminate the perspective layer or its per-chart reductions.",
        ),
        ProjectQuestionAnswer(
            "Q5",
            "Does record-defined orientation establish a thermodynamic, ontological, or phenomenal arrow?",
            "Not established. Stage 7 measures a target-specific record-information orientation only.",
            "untested_not_established",
            ("Stage7C:orientation-controls", "Stage7G:interpretation-audit"),
            "record-defined orientation != thermodynamic arrow != ontological becoming != phenomenal passage.",
        ),
        ProjectQuestionAnswer(
            "Q6",
            "How should the Stage 6 layered candidate be updated after Stage 7?",
            "Strengthen the P/O/R layered core and retain Xi_PR; refine explicit P edge matrices as derived from the common carrier plus per-perspective reductions. V remains explicit but has not yet been integrated into this same quantum construction.",
            "candidate_structural_interpretation",
            ("Stage7D:P-R", "Stage7F:minimality", "Stage6E:P-V"),
            "The result strengthens a finite-model architecture, not a fundamental or unique ontology of time.",
        ),
    )


def stage8_gate_candidates() -> tuple[Stage8GateCandidate, ...]:
    evidence = evidence_snapshot()
    modal = canonical_modal_transport()
    reconstruction = evidence.r_reconstruction
    reduction = evidence.stage7d_reduction

    modality_signals: list[str] = [
        "V is the only Stage 6 explicit layer not yet integrated into the same Stage 7 constrained quantum construction"
    ]
    modality_score = 4
    if modal.epistemic_extensions.relation_holds and modal.ontic_extensions.relation_holds:
        modality_score += 2
        modality_signals.append("Stage 6 P-V extension transport is positive in its typed toy interface")
    if modal.underdetermination_preserved:
        modality_score += 2
        modality_signals.append("epistemic/ontic modal underdetermination survives Stage 6 transport")
    if select_synthesis_choice(evidence) is Stage7SynthesisChoice.STRENGTHENED:
        modality_score += 2
        modality_signals.append("P/O/R now have stronger single-model evidence, making V the cleanest missing-layer pressure test")

    order_signals: list[str] = []
    order_score = 0
    if canonical_history_model("forward").event_labels == ("e0", "e1", "e2"):
        order_score += 3
        order_signals.append("Stage 7 O is still a deliberately minimal three-event anchor")
    if reconstruction.p_and_o_retained_without_r:
        order_score += 3
        order_signals.append("P + the current simple O does not reconstruct R, so richer O could test whether that separation is robust")
    order_score += 1
    order_signals.append("physical clock change => temporal succession remains not established")

    clock_signals: list[str] = []
    clock_score = 2
    clock_signals.append("true interacting/nonideal/POVM clock robustness remains incomplete")
    if reduction.nonuniform_clock_probability_detected:
        clock_score += 2
        clock_signals.append("Stage 7 interaction already exposes nonuniform clock probabilities")
    if reduction.min_non_a_isometry_residual > DEFAULT_ATOL:
        clock_score += 1
        clock_signals.append("B/C charts are already non-Euclidean-isometric before induced-metric repair")

    covariance_signals = (
        "P/O/R finite-model architecture is now comparatively stable",
        "a generally covariant precursor would introduce several new confounds before V is integrated",
    )
    covariance_score = 3

    candidates = (
        Stage8GateCandidate(
            "quantum_potentiality",
            "Integrate explicit Potentiality / extension semantics V into the same constrained quantum construction",
            modality_score,
            tuple(modality_signals),
            "Directly tests the only explicit Stage 6 layer still separated from the strengthened Stage 7 P/O/R construction and pressures whether operationally equal quantum descriptions can retain distinct typed modal extension semantics.",
        ),
        Stage8GateCandidate(
            "richer_causal_order",
            "Replace the minimal three-event O layer with richer causal/order structure",
            order_score,
            tuple(order_signals),
            "Tests whether the Stage 7 P/O/R separation survives a less schematic order/history layer.",
        ),
        Stage8GateCandidate(
            "nonideal_povm_clocks",
            "Test interacting, nonideal, and POVM clock perspectives",
            clock_score,
            tuple(clock_signals),
            "Extends P robustness beyond the current projective finite-clock family, but Stage 7 already exposed and repaired one nonideal metric deformation.",
        ),
        Stage8GateCandidate(
            "parametrized_covariance_precursor",
            "Begin a parametrized / generally covariant precursor",
            covariance_score,
            covariance_signals,
            "Important eventually, but less discriminating now because it adds covariance and constraint complexity before the remaining V layer has entered the shared finite construction.",
        ),
    )
    return tuple(sorted(candidates, key=lambda item: (-item.score, item.gate_id)))


def _spectator_roundtrip_passes(tolerance: float = 1e-10) -> bool:
    physical_projector = spectator_physical_projector()
    for clock in SUBSYSTEMS:
        support_projector = spectator_support_projector(clock)
        for index in range(3):
            reduction = spectator_reduction_operator(clock, index)
            reconstruction = spectator_reconstruction_operator(clock, index)
            if np.linalg.norm(reduction @ reconstruction - support_projector) > tolerance:
                return False
            if (
                np.linalg.norm(
                    reconstruction @ reduction @ physical_projector - physical_projector
                )
                > tolerance
            ):
                return False
    return True


def pre_merge_exit_criteria() -> dict[int, bool]:
    """Recompute Stage 7 criteria 1--35; criterion 36 remains external CI/review."""

    evidence = evidence_snapshot()
    a = evidence.stage7a
    b = evidence.stage7b
    forward = evidence.forward
    reversed_record = evidence.reversed
    no_record = evidence.no_record
    uncertain = evidence.uncertain
    balanced = evidence.balanced
    d_red = evidence.stage7d_reduction
    d = evidence.stage7d_transport
    e_access = evidence.stage7e_accessibility
    e_atlas = evidence.stage7e_atlas
    f = evidence.stage7f
    reconstruction = evidence.r_reconstruction

    spectator_clock = spectator_clock_change_diagnostics()
    spectator_composition = spectator_composition_diagnostics()
    spectator_record = spectator_no_record_diagnostics()
    ablations = build_stage7f_ablation_matrix()
    mismatches = stage7f_mismatch_matrix()
    candidates = stage8_gate_candidates()
    choice = select_synthesis_choice(evidence)

    checks: dict[int, bool] = {}
    checks[1] = bool(
        a["kinematic_dimension"] == 54
        and a["physical_dimension"] == 14
        and a["memory_dimension"] == 2
    )
    checks[2] = bool(
        canonical_history_model("forward").event_labels == ("e0", "e1", "e2")
        and event_correspondence("preserving").source_events == ("e0", "e1", "e2")
        and canonical_target_pair_projector().shape == (7, 7)
        and memory_pauli_z().shape == (2, 2)
    )
    checks[3] = bool(b.positive_target_specific_record_witness and not b.directional_score_defined)
    checks[4] = bool(
        b.physical_automorphism_residual <= 1e-10
        and np.linalg.norm(
            history_constraint_operator("forward") - spectator_total_constraint_operator()
        )
        > 1e-6
    )
    checks[5] = bool(
        [status.value for status in RoleStatus]
        == ["preserved", "reconstructible", "inaccessible", "lost", "not_established"]
        and len(ablations) == len(ABLATION_IDS)
    )

    checks[6] = bool(a["physical_dimension"] == 14 and set(a["support_dimensions"].values()) == {14})
    checks[7] = _spectator_roundtrip_passes()
    checks[8] = bool(
        spectator_clock.comparisons == 54
        and spectator_clock.max_state_residual <= 1e-10
        and spectator_clock.max_born_residual <= 1e-10
        and spectator_clock.max_inverse_residual <= 1e-10
        and spectator_composition.comparisons == 162
        and spectator_composition.max_composition_residual <= 1e-10
    )
    checks[9] = bool(
        spectator_record.comparisons == 18
        and not spectator_record.positive_record_witness
        and not spectator_record.record_coupling_present
    )

    checks[10] = bool(canonical_target_pair_projector().shape == (7, 7) and memory_pauli_z().shape == (2, 2))
    checks[11] = bool(b.support_unitarity_residual <= 1e-10 and b.inverse_recovery_residual <= 1e-10)
    checks[12] = bool(b.target_information_after > b.target_information_before + 0.9)
    checks[13] = bool(b.target_information_no_record <= 1e-10 and b.wrong_target_information_after <= 1e-10)
    checks[14] = bool(forward.directional_score_defined and forward.internally_anchored and forward.record_defined)

    checks[15] = bool(not no_record.record_defined and abs(no_record.record_score) <= 1e-10)
    checks[16] = bool(not uncertain.record_defined and abs(uncertain.record_score) <= 1e-10)
    checks[17] = bool(
        forward.record_score > 0.9
        and reversed_record.record_score < -0.9
        and abs(forward.record_score + reversed_record.record_score) <= 1e-10
    )
    checks[18] = bool(
        abs(balanced.record_score) <= 1e-10
        and abs(balanced.accessibility_score) <= 1e-10
    )

    checks[19] = bool(d_red.nodes == 9 and d_red.min_rank == 14)
    checks[20] = bool(d.max_observable_transport_residual <= 1e-9)
    checks[21] = bool(event_correspondence("preserving").declared_orientation == "preserving")
    checks[22] = bool(d.preserving_covariance)
    checks[23] = bool(d.reversing_covariance)
    checks[24] = bool(d.bare_observable_rejected)
    checks[25] = bool(d.wrong_chi_rejected)

    checks[26] = bool(e_access.global_record_survives_hidden and e_access.hidden_is_inaccessible)
    checks[27] = bool(e_access.hidden_is_inaccessible and e_access.noisy_is_inaccessible)
    checks[28] = bool(e_atlas.ideal_indirect_paths == 3 and e_atlas.ideal_paths_consistent)
    checks[29] = bool(e_atlas.perturbation_detected and e_atlas.localized_failure)

    checks[30] = bool(len(ablations) == 7 and tuple(case.ingredient for case in ablations) == ABLATION_IDS)
    observed_statuses = {
        probe.status.value for case in ablations for probe in case.probes
    }
    checks[31] = bool(
        {"lost", "reconstructible", "inaccessible", "not_established"}.issubset(observed_statuses)
        and all(item.detected for item in mismatches)
    )
    checks[32] = choice is not Stage7SynthesisChoice.INCONCLUSIVE
    checks[33] = bool(
        choice is Stage7SynthesisChoice.STRENGTHENED
        and reconstruction.p_and_o_retained_without_r
        and not reconstruction.reconstruction_witness_found
        and "record_defined_direction => phenomenal_passage" in unresolved_implications()
        and "perspective_consistency => modal_equivalence" in unresolved_implications()
    )
    checks[34] = bool(
        len(candidates) == 4
        and candidates[0].gate_id == "quantum_potentiality"
        and candidates[0].score > candidates[1].score
    )
    checks[35] = bool(
        set(_interpretation_guards())
        >= {
            "lost != metaphysically irreducible",
            "reconstructible != universally redundant",
            "record-defined orientation != phenomenal passage",
            "P-R covariance != P=R",
            "Stage 7 synthesis != empirical discovery",
        }
    )

    if tuple(sorted(checks)) != tuple(range(1, 36)):
        raise RuntimeError("Stage 7 pre-merge audit must cover criteria 1--35 exactly")
    return checks


def _interpretation_guards() -> tuple[str, ...]:
    return (
        "memory subsystem != conscious observer",
        "memory present != record present",
        "target-specific record correlation != record-defined direction",
        "record-defined orientation != thermodynamic arrow",
        "record-defined orientation != ontological becoming",
        "record-defined orientation != phenomenal passage",
        "perspective change != temporal succession",
        "P-R covariance != P=R",
        "local inaccessibility != global record absence",
        "indirect reconstructibility != direct local edge availability",
        "observable-algebra correspondence != full state/metric path consistency",
        "lost != metaphysically irreducible",
        "reconstructible != universally redundant",
        "P + O retained without R != proof that P/O can never generate records in another model",
        "missing chi != false covariance",
        "explicit perspective-map reconstruction != elimination of the perspective layer",
        "not_established != false",
        "finite-model success != general covariance",
        "Stage 7 synthesis != empirical discovery",
    )


def _evidence_boundary() -> dict[str, str]:
    return {
        "established_finite_model_result": (
            "Executable Stage 7 witnesses establish target-specific record formation, relational record orientation, genuine multi-clock record covariance, access/path controls, and the declared ablation outcomes only in the finite constrained families tested."
        ),
        "candidate_structural_interpretation": (
            "The evidence strengthens the layered P/O/R core and retains V as an explicit but still separately modeled layer; explicit P edge matrices are derived in the current representation."
        ),
        "unsupported_claims": (
            "No Stage 7 result establishes fundamental time, universal irreducibility, thermodynamic time asymmetry, ontological becoming, phenomenal passage, general covariance, gravity, or a novel empirical prediction."
        ),
    }


def build_stage7g_synthesis(*, include_exit_audit: bool = True) -> Stage7GSynthesis:
    evidence = evidence_snapshot()
    choice = select_synthesis_choice(evidence)
    candidates = stage8_gate_candidates()
    audit = pre_merge_exit_criteria() if include_exit_audit else {}
    return Stage7GSynthesis(
        choice=choice,
        strengthened_scope=("P", "O", "R", "Xi_PR"),
        refinement_inside_p=(
            "explicit cross-clock edge matrices are reconstructed from common physical carrier + per-perspective reductions",
            "interacting charts may be non-Euclidean-unitary while preserving the induced physical metric",
        ),
        unintegrated_layers=("V / Potentiality-extension semantics",),
        compatibility_links=("P-O (typed)", "P-R (single constrained quantum model)", "P-V (Stage 6 typed transport only)"),
        project_questions=answer_project_questions(),
        unresolved_implications=unresolved_implications(),
        stage8_candidates=candidates,
        selected_stage8_gate=candidates[0].gate_id,
        pre_merge_exit_criteria_passed=sum(audit.values()) if audit else 0,
        pre_merge_exit_criteria_total=len(audit) if audit else 35,
    )


def stage7g_rows() -> dict[str, Any]:
    audit = pre_merge_exit_criteria()
    synthesis = build_stage7g_synthesis()
    return {
        "synthesis": synthesis.as_dict(),
        "pre_merge_exit_criteria": {str(key): value for key, value in audit.items()},
        "criterion_36": {
            "status": "external_final_ci_and_merge_readiness_review_required",
            "passed_in_python_module": False,
        },
        "evidence_boundary": _evidence_boundary(),
        "interpretation_guards": list(_interpretation_guards()),
        "stage7f_bounded_interpretation": evidence_snapshot().stage7f["bounded_interpretation"],
    }
