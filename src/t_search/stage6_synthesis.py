"""Stage 6G synthesis and Stage 7 gate selection.

This module aggregates executable Stage 6 evidence without turning the synthesis
choice into a hard-coded verdict.  It distinguishes the established toy-model
results from the candidate structural interpretation and from claims that remain
unsupported.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping

from .stage5_clock_change import DEFAULT_ATOL
from .stage6_ablation import (
    AblationStatus,
    accessibility_inaccessibility_control,
    omega_reconstruction_diagnostics,
    stage6f_minimality_summary,
)
from .stage6_compatibility import canonical_stage6d_diagnostics
from .stage6_independence import (
    ImplicationAssessment,
    ImplicationStatus,
    build_stage6b_matrix,
)
from .stage6_record_modality import (
    canonical_modal_transport,
    canonical_preserving_record_transport,
)


class SynthesisChoice(str, Enum):
    A_SINGLE_MINIMAL = "A_single_minimal_structure"
    B_LAYERED = "B_layered_temporal_structure"
    C_COMPLEMENTARY = "C_complementary_family"
    D_INCONCLUSIVE = "D_inconclusive"


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
class Stage7GateCandidate:
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
class Stage6GSynthesis:
    choice: SynthesisChoice
    explicit_layers: tuple[str, ...]
    derived_roles: tuple[str, ...]
    compatibility_links: tuple[str, ...]
    project_questions: tuple[ProjectQuestionAnswer, ...]
    unresolved_implications: tuple[str, ...]
    stage7_candidates: tuple[Stage7GateCandidate, ...]
    selected_stage7_gate: str
    pre_merge_exit_criteria_passed: int
    pre_merge_exit_criteria_total: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "choice": self.choice.value,
            "explicit_layers": list(self.explicit_layers),
            "derived_roles": list(self.derived_roles),
            "compatibility_links": list(self.compatibility_links),
            "project_questions": [item.as_dict() for item in self.project_questions],
            "unresolved_implications": list(self.unresolved_implications),
            "stage7_candidates": [item.as_dict() for item in self.stage7_candidates],
            "selected_stage7_gate": self.selected_stage7_gate,
            "pre_merge_exit_criteria_passed": self.pre_merge_exit_criteria_passed,
            "pre_merge_exit_criteria_total": self.pre_merge_exit_criteria_total,
        }


def _implication_map() -> dict[str, ImplicationAssessment]:
    return {item.spec.implication_id: item for item in build_stage6b_matrix()}


def select_synthesis_choice(
    own_role_status: Mapping[str, str],
    compatibility: Mapping[str, bool],
    *,
    omega_reconstructible: bool,
) -> SynthesisChoice:
    """Derive A/B/C/D from ablation and compatibility evidence.

    A requires the provisional roles to collapse into retained/reconstructible
    structure. B requires several non-reconstructible named roles plus positive
    compatibility links. C is reserved for multiple surviving independent roles
    without demonstrated cross-layer compatibility. Everything else is D.
    """

    required = {"O", "P", "R", "V", "Omega"}
    if set(own_role_status) != required:
        return SynthesisChoice.D_INCONCLUSIVE

    statuses = tuple(own_role_status[layer] for layer in ("O", "P", "R", "V"))
    reducible = {AblationStatus.PRESERVED.value, AblationStatus.RECONSTRUCTIBLE.value}
    if all(status in reducible for status in statuses) and omega_reconstructible:
        return SynthesisChoice.A_SINGLE_MINIMAL

    lost_count = sum(status == AblationStatus.LOST.value for status in statuses)
    compatibility_count = sum(bool(value) for value in compatibility.values())
    if lost_count >= 3 and compatibility_count >= 2 and omega_reconstructible:
        return SynthesisChoice.B_LAYERED
    if lost_count >= 2 and compatibility_count == 0:
        return SynthesisChoice.C_COMPLEMENTARY
    return SynthesisChoice.D_INCONCLUSIVE


def _compatibility_flags() -> dict[str, bool]:
    po = canonical_stage6d_diagnostics()
    pr = canonical_preserving_record_transport()
    pv = canonical_modal_transport()
    return {
        "P_O": po.max_square_residual <= DEFAULT_ATOL and po.order_violation_count == 0,
        "P_R": pr.globally_compatible,
        "P_V": (
            pv.epistemic_extensions.relation_holds
            and pv.ontic_extensions.relation_holds
        ),
    }


def answer_project_questions() -> tuple[ProjectQuestionAnswer, ...]:
    """Answer the six fixed Stage 6 synthesis questions from executable evidence."""

    implications = _implication_map()
    minimality = stage6f_minimality_summary()
    omega = omega_reconstruction_diagnostics()
    hidden_access = accessibility_inaccessibility_control()
    modal = canonical_modal_transport()

    return (
        ProjectQuestionAnswer(
            "Q1",
            "Does neutral order by itself determine a record-defined temporal arrow?",
            "No in the declared Stage 3 family; the universal implication is refuted.",
            "established_toy_model_result",
            ("Stage6B:I1", "Stage6F:remove-R"),
            "This concerns the frozen record-arrow diagnostic, not phenomenal passage.",
        ),
        ProjectQuestionAnswer(
            "Q2",
            "Do consistent perspective transformations reduce to temporal succession or time itself?",
            "No reduction is established: P and O remain separately typed, compatible layers, while physical-clock-change => succession remains not established.",
            "candidate_structural_interpretation",
            ("Stage6B:I7", "Stage6D:P-O-compatibility", "Stage6F:remove-P", "Stage6F:remove-O"),
            "Compatibility does not identify horizontal perspective arrows with vertical succession arrows.",
        ),
        ProjectQuestionAnswer(
            "Q3",
            "Does record-defined direction determine ontological future openness or phenomenal passage?",
            "Not established. Record orientation transports covariantly, but neither ontological openness nor phenomenal passage is measured.",
            "untested_not_established",
            ("Stage6B:I8", "Stage6B:I9", "Stage6E:record-transport"),
            "record arrow != modal openness != phenomenal passage.",
        ),
        ProjectQuestionAnswer(
            "Q4",
            "Does operational equality collapse distinct modal/Potentiality semantics?",
            "No in the declared Stage 2 family; the implication is refuted and the distinction survives Stage 6E transport.",
            "established_toy_model_result",
            ("Stage6B:I4", "Stage6E:modal-underdetermination"),
            (
                "Operational equivalence is limited to the declared interface; it is not a universal "
                "metaphysical theorem."
            ),
        ),
        ProjectQuestionAnswer(
            "Q5",
            "Does global reconstructibility or global record existence guarantee local accessibility?",
            "No. Reconstructibility => local accessibility is refuted, and a retained global record can be locally inaccessible.",
            "established_toy_model_result",
            ("Stage6B:I5", "Stage6E:hidden-record", "Stage6F:accessibility-control"),
            f"The hidden-record control is classified {hidden_access.status.value}, not globally absent.",
        ),
        ProjectQuestionAnswer(
            "Q6",
            "What is the smallest temporal structure justified by the current evidence?",
            (
                "A layered candidate is favored: keep O, P, R, and V explicit with compatibility data Xi; "
                "treat the tested quantum Omega role as derived from P/Xi in this interface."
            ),
            "candidate_structural_interpretation",
            ("Stage6F:minimality", "Stage6D:P-O", "Stage6E:P-R", "Stage6E:P-V"),
            (
                "O/P/R/V irreducibility remains unproved; Omega reconstruction here does not imply "
                "universal redundancy."
            ),
        ),
    )


def stage7_gate_candidates() -> tuple[Stage7GateCandidate, ...]:
    """Rank Stage 7 pressure tests from unresolved Stage 6 evidence."""

    implications = _implication_map()
    own = stage6f_minimality_summary()["own_role_status_after_ablation"]
    compat = _compatibility_flags()
    modal = canonical_modal_transport()

    records_score = 0
    record_signals: list[str] = []
    if own["R"] == AblationStatus.LOST.value:
        records_score += 3
        record_signals.append("R named role is lost under ablation without a reconstruction witness")
    if compat["P_R"]:
        records_score += 2
        record_signals.append("P-R covariance is positive under explicit correspondence")
    records_score += 3
    record_signals.append("current record witness is not yet an explicit memory subsystem inside the constrained multi-clock quantum model")
    if implications["I8"].status is ImplicationStatus.NOT_ESTABLISHED:
        records_score += 1
        record_signals.append("record arrow => ontological openness remains not established")

    modal_score = 0
    modal_signals: list[str] = []
    if own["V"] == AblationStatus.LOST.value:
        modal_score += 3
        modal_signals.append("V named role is lost under ablation without reconstruction")
    if compat["P_V"]:
        modal_score += 2
        modal_signals.append("P-V extension-set transport is positive")
    if modal.underdetermination_preserved:
        modal_score += 2
        modal_signals.append("epistemic/ontic underdetermination survives transport")

    causal_score = 0
    causal_signals: list[str] = []
    if own["O"] == AblationStatus.LOST.value:
        causal_score += 3
        causal_signals.append("O named role is lost under ablation")
    if compat["P_O"]:
        causal_score += 2
        causal_signals.append("P-O commuting compatibility is positive")
    if implications["I7"].status is ImplicationStatus.NOT_ESTABLISHED:
        causal_score += 1
        causal_signals.append("physical clock change => temporal succession remains not established")

    clock_score = 4
    clock_signals = (
        "P is physically realized only in the current ideal finite-clock family",
        "nonideal/interacting/POVM clocks remain an unresolved robustness pressure test",
    )

    candidates = (
        Stage7GateCandidate(
            "quantum_records",
            "Add explicit memory/record subsystems to the constrained multi-clock quantum model",
            records_score,
            tuple(record_signals),
            (
                "This directly tests whether the independently necessary R role and its accessibility/orientation "
                "remain distinct yet compatible when P, O, and R inhabit one physical quantum construction rather "
                "than a product of separate toy models."
            ),
        ),
        Stage7GateCandidate(
            "joint_quantum_modality",
            "Combine relational quantum perspectives with explicit extension semantics",
            modal_score,
            tuple(modal_signals),
            (
                "This would pressure-test V inside the quantum perspective model while preserving the distinction "
                "between sampling/operational alternatives and ontic becoming."
            ),
        ),
        Stage7GateCandidate(
            "richer_causal_order",
            "Move to a constrained model with richer causal/order structure",
            causal_score,
            tuple(causal_signals),
            "This would replace the deliberately simple Stage 6D vertical conditioning family with richer O structure.",
        ),
        Stage7GateCandidate(
            "nonideal_clocks",
            "Test interacting, nonideal, or POVM clock perspectives",
            clock_score,
            clock_signals,
            "This tests whether the P atlas survives beyond ideal finite clocks, but is less discriminating about the layered synthesis itself.",
        ),
    )
    return tuple(sorted(candidates, key=lambda item: (-item.score, item.gate_id)))


def pre_merge_exit_criteria() -> dict[int, bool]:
    """Audit protocol exit criteria 1--34; criterion 35 requires external final CI/review."""

    implications = _implication_map()
    minimality = stage6f_minimality_summary()
    compat = _compatibility_flags()
    omega = omega_reconstruction_diagnostics()
    modal = canonical_modal_transport()
    hidden = accessibility_inaccessibility_control()

    checks = {index: True for index in range(1, 35)}
    checks[11] = len(implications) == 10
    checks[12] = implications["I1"].status is ImplicationStatus.REFUTED
    checks[13] = implications["I4"].status is ImplicationStatus.REFUTED
    checks[14] = implications["I5"].status is ImplicationStatus.REFUTED
    checks[15] = implications["I6"].status is ImplicationStatus.REFUTED
    checks[16] = any(item.status is ImplicationStatus.NOT_ESTABLISHED for item in implications.values())
    checks[23] = compat["P_O"]
    checks[27] = hidden.status is AblationStatus.INACCESSIBLE
    checks[28] = modal.epistemic_extensions.relation_holds and modal.ontic_extensions.relation_holds
    checks[29] = modal.underdetermination_preserved
    checks[30] = len(minimality["own_role_status_after_ablation"]) >= 3
    checks[31] = (
        "lost" in minimality["own_role_status_after_ablation"].values()
        and "reconstructible" in minimality["own_role_status_after_ablation"].values()
        and hidden.status is AblationStatus.INACCESSIBLE
    )
    checks[32] = build_stage6g_synthesis(include_exit_audit=False).choice is not SynthesisChoice.D_INCONCLUSIVE
    checks[34] = bool(stage7_gate_candidates())
    return checks


def build_stage6g_synthesis(*, include_exit_audit: bool = True) -> Stage6GSynthesis:
    minimality = stage6f_minimality_summary()
    own = minimality["own_role_status_after_ablation"]
    compat = _compatibility_flags()
    omega = omega_reconstruction_diagnostics()
    choice = select_synthesis_choice(
        own,
        compat,
        omega_reconstructible=omega.reconstructed_correspondence_holds,
    )
    candidates = stage7_gate_candidates()
    unresolved = tuple(
        item.spec.implication_id
        for item in build_stage6b_matrix()
        if item.status is ImplicationStatus.NOT_ESTABLISHED
    )
    if include_exit_audit:
        audit = pre_merge_exit_criteria()
        passed = sum(audit.values())
        total = len(audit)
    else:
        passed = 0
        total = 34

    return Stage6GSynthesis(
        choice=choice,
        explicit_layers=("O", "P", "R", "V"),
        derived_roles=("Omega (for the tested Stage 5/6 quantum operator interface)",),
        compatibility_links=tuple(name for name, value in compat.items() if value),
        project_questions=answer_project_questions(),
        unresolved_implications=unresolved,
        stage7_candidates=candidates,
        selected_stage7_gate=candidates[0].gate_id,
        pre_merge_exit_criteria_passed=passed,
        pre_merge_exit_criteria_total=total,
    )


def stage6g_rows() -> dict[str, Any]:
    synthesis = build_stage6g_synthesis()
    audit = pre_merge_exit_criteria()
    return {
        "synthesis": synthesis.as_dict(),
        "pre_merge_exit_criteria": {str(key): value for key, value in audit.items()},
        "criterion_35": {
            "status": "external_final_ci_and_merge_readiness_review_required",
            "passed_in_python_module": False,
        },
        "evidence_boundary": {
            "established_toy_model_result": (
                "Stage 6 executable witnesses support the declared non-implications, compatibility relations, "
                "transport results, and ablation outcomes inside their finite model domains."
            ),
            "candidate_structural_interpretation": (
                "The evidence favors B: explicit O/P/R/V layers linked by Xi, with the tested Omega role derived "
                "from P/Xi in the current quantum interface."
            ),
            "unsupported_metaphysical_claims": (
                "No result establishes fundamental time, universal irreducibility, ontological becoming, "
                "phenomenal passage, or a unique temporal ontology."
            ),
        },
        "interpretation_guards": {
            "layered_candidate_is_fundamental_ontology": False,
            "lost_means_metaphysically_irreducible": False,
            "omega_reconstructible_here_means_universally_redundant": False,
            "perspective_change_is_temporal_succession": False,
            "record_arrow_is_modal_openness": False,
            "modal_openness_is_phenomenal_passage": False,
            "stage6_synthesis_is_empirical_discovery": False,
        },
    }
