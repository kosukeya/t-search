"""Stage 10G synthesis and evidence-selected Stage 11 gate.

Stages 10A--F promoted the Stage 9C future-signature measurement into a fully
typed continuation-aware measurement family, transported its effect and
normalization forms through genuine A/B/C clock changes, established
per-continuation Born covariance on a tomography-complete probe family, restored
weights/modal models/evidence updates, and pressure-tested the positive result
with typing and normalization ablations.

Stage 10G synthesizes those executable diagnostics.  The synthesis is purposely
bounded: ``measurement_covariant`` means that the declared finite typed
measurement family is operationally covariant under the tested clock changes.
It does not mean general covariance, modal identity, eternalism, or the absence
of ontological becoming.

The Stage 10 evidence closes the explicit measurement-family boundary selected
at Stage 9G.  The next gate is therefore chosen from the remaining structural
boundaries rather than by extending Stage 10 indefinitely.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from functools import lru_cache
from typing import Any

from .stage5_clock_change import DEFAULT_ATOL
from .stage10_ablation import Stage10FDiagnostics, stage10f_ablation_diagnostics
from .stage10_lift import Stage10BLiftDiagnostics, stage10b_lift_diagnostics
from .stage10_modal import Stage10EModalDiagnostics, stage10e_modal_diagnostics
from .stage10_probability import (
    Stage10DProbabilityDiagnostics,
    stage10d_probability_diagnostics,
)
from .stage10_reference import Stage10ReferenceDiagnostics, stage10a_reference_diagnostics
from .stage10_transport import Stage10CTransportDiagnostics, stage10c_transport_diagnostics


class Stage10SynthesisChoice(str, Enum):
    MEASUREMENT_COVARIANT = "measurement_covariant"
    MEASUREMENT_PARTIAL = "measurement_partial"
    MEASUREMENT_OBSTRUCTED = "measurement_obstructed"
    INCONCLUSIVE = "inconclusive"


@dataclass(frozen=True, slots=True)
class ProjectQuestionAnswer:
    question_id: str
    question: str
    answer: str
    evidence_class: str
    evidence_refs: tuple[str, ...]
    boundary: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class Stage11GateCandidate:
    gate_id: str
    label: str
    score: int
    pressure_signals: tuple[str, ...]
    rationale: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class Stage10EvidenceSnapshot:
    stage10a: Stage10ReferenceDiagnostics
    stage10b: Stage10BLiftDiagnostics
    stage10c: Stage10CTransportDiagnostics
    stage10d: Stage10DProbabilityDiagnostics
    stage10e: Stage10EModalDiagnostics
    stage10f: Stage10FDiagnostics


@dataclass(frozen=True, slots=True)
class Stage10GSynthesis:
    choice: Stage10SynthesisChoice
    top_level_candidate: str
    established_scope: tuple[str, ...]
    retained_typing_resources: tuple[str, ...]
    derived_or_reconstructible_roles: tuple[str, ...]
    project_questions: tuple[ProjectQuestionAnswer, ...]
    unresolved_boundaries: tuple[str, ...]
    stage11_candidates: tuple[Stage11GateCandidate, ...]
    selected_stage11_gate: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "choice": self.choice.value,
            "top_level_candidate": self.top_level_candidate,
            "established_scope": list(self.established_scope),
            "retained_typing_resources": list(self.retained_typing_resources),
            "derived_or_reconstructible_roles": list(self.derived_or_reconstructible_roles),
            "project_questions": [item.as_dict() for item in self.project_questions],
            "unresolved_boundaries": list(self.unresolved_boundaries),
            "stage11_candidates": [item.as_dict() for item in self.stage11_candidates],
            "selected_stage11_gate": self.selected_stage11_gate,
        }


@lru_cache(maxsize=1)
def evidence_snapshot() -> Stage10EvidenceSnapshot:
    """Evaluate the completed Stage 10A--F diagnostics once per process."""

    return Stage10EvidenceSnapshot(
        stage10a=stage10a_reference_diagnostics(),
        stage10b=stage10b_lift_diagnostics(),
        stage10c=stage10c_transport_diagnostics(),
        stage10d=stage10d_probability_diagnostics(),
        stage10e=stage10e_modal_diagnostics(),
        stage10f=stage10f_ablation_diagnostics(),
    )


def select_synthesis_choice(
    snapshot: Stage10EvidenceSnapshot | None = None,
    *,
    atol: float = DEFAULT_ATOL,
) -> Stage10SynthesisChoice:
    evidence = evidence_snapshot() if snapshot is None else snapshot
    a = evidence.stage10a
    b = evidence.stage10b
    c = evidence.stage10c
    d = evidence.stage10d
    e = evidence.stage10e
    f = evidence.stage10f

    reference_valid = bool(
        a.canonical_outcomes_reproduced
        and a.canonical_effects_reproduced
        and a.prediction_anchor_explicit
        and a.target_event_explicit
        and a.anchor_target_distinct
        and a.operationally_discriminating
        and a.max_stage9_probability_residual <= 10 * atol
        and a.all_reference_probabilities_normalized
        and a.public_schema_selector_free
    )

    decision = b.normalization_decision
    lift_valid = bool(
        b.all_lifts_continuation_specific
        and b.max_support_completeness_residual <= 10 * atol
        and b.max_physical_completeness_residual <= 10 * atol
        and b.max_support_stage9_probability_residual <= 10 * atol
        and b.max_effect_form_stage9_probability_residual <= 10 * atol
        and b.class_correspondences_explicit
        and b.outcome_correspondences_explicit
        and b.wrong_continuation_lift_rejected
        and decision.reference_support_povm_equivalent
        and decision.physical_effect_form_equivalent
        and decision.genuine_maps_nonunitary
        and decision.local_identity_reset_not_transport_covariant
    )

    representation_covariant = bool(
        c.total_charts == 18
        and c.genuine_measurement_transports == 108
        and c.three_clock_measurement_compositions == 324
        and c.max_direct_transport_normalization_residual <= 10 * atol
        and c.max_direct_transport_effect_residual <= 10 * atol
        and c.max_composition_normalization_residual <= 10 * atol
        and c.max_composition_effect_residual <= 10 * atol
        and c.max_completeness_residual <= 10 * atol
        and c.max_hermiticity_residual <= 10 * atol
        and c.minimum_effect_eigenvalue >= -10 * atol
        and c.minimum_normalization_eigenvalue > atol
        and c.all_chart_typing_valid
        and c.preserving_correspondence_valid
        and c.wrong_event_correspondence_rejected
        and c.wrong_class_correspondence_rejected
        and c.bare_effect_rejected
    )

    probability_covariant = bool(
        d.measurement_covariance_status == "established"
        and d.per_continuation_before_weighting
        and not d.branch_weight_aggregation_performed
        and d.per_continuation_probability_covariance
        and d.stage9c_reference_likelihood_covariance
        and d.completeness_probability_covariance
        and d.positivity_probability_covariance
        and d.accidental_canonical_equality_ruled_out
        and d.wrong_identity_normalization_rejected
        and d.misaligned_metric_rejected
    )

    weighted_modal_update_covariant = bool(
        e.weighted_prediction_covariance
        and e.matched_modal_public_view_covariance
        and e.hidden_hstar_swap_invariant
        and e.privileged_modal_roles_still_distinct
        and e.weight_mismatch_transport_covariance
        and e.evidence_update_covariance
        and e.weighted_modal_update_covariance_established
    )

    ablation_guarded = bool(
        f.correspondence_ablations_classified
        and f.normalization_ablations_classified
        and f.all_required_false_positive_controls_rejected
        and f.metaphysical_promotion_avoided
        and f.missing_normalization_semantics_status == "not_established"
    )

    if (
        reference_valid
        and lift_valid
        and representation_covariant
        and probability_covariant
        and weighted_modal_update_covariant
        and ablation_guarded
    ):
        return Stage10SynthesisChoice.MEASUREMENT_COVARIANT

    explicit_obstruction = bool(
        d.measurement_covariance_status == "refuted"
        or not c.preserving_correspondence_valid
    )
    if explicit_obstruction:
        return Stage10SynthesisChoice.MEASUREMENT_OBSTRUCTED

    any_positive_layer = bool(
        reference_valid
        or lift_valid
        or representation_covariant
        or d.per_continuation_probability_covariance
        or e.weighted_prediction_covariance
    )
    if any_positive_layer:
        return Stage10SynthesisChoice.MEASUREMENT_PARTIAL

    return Stage10SynthesisChoice.INCONCLUSIVE


def unresolved_boundaries() -> tuple[str, ...]:
    return (
        "finite_typed_clock_measurement_covariance => general_covariance",
        "minimal_three_event_O => robustness_under_richer_causal_order",
        "ideal_projective_clock_family => nonideal_POVM_clock_covariance",
        "typed_correspondence_resources => metaphysically_fundamental_structure",
        "operational_measurement_covariance => modal_ontological_identity",
        "perspective_invariant_future_probabilities => eternalism",
        "perspective_invariant_future_probabilities => absence_of_ontological_becoming",
        "future_measurement_covariance => future_actuality",
        "selected_vs_unselected_modal_semantics => empirical_discrimination",
        "direct_Xi_RV_value_law",
        "refined_O_P_R_V_Xi_candidate => fundamental_or_unique_time_ontology",
        "finite_model_success => empirical_discovery",
    )


def answer_project_questions() -> tuple[ProjectQuestionAnswer, ...]:
    return (
        ProjectQuestionAnswer(
            "Q1",
            "Has the Stage 9 future-measurement transport boundary been closed?",
            (
                "Yes for the declared finite typed family. Stage 10 constructs the same "
                "future-signature operational question at all continuation-specific A/B/C "
                "charts and establishes representation, per-continuation probability, "
                "weighted prediction, and evidence-update covariance."
            ),
            "established_finite_model_result",
            (
                "Stage10C:measurement-form-transport",
                "Stage10D:tomography-complete-probability-covariance",
                "Stage10E:weighted-modal-update-covariance",
            ),
            (
                "The result is finite-clock and family-specific; it is not general "
                "covariance and does not establish a fundamental ontology of time."
            ),
        ),
        ProjectQuestionAnswer(
            "Q2",
            "Does full operational covariance collapse epistemic and ontic-extension modal semantics?",
            (
                "No. Matched public measurement views, weighted predictions, and "
                "posteriors remain covariant while the epistemic model retains a hidden "
                "selected continuation and the ontic-extension model remains selector-free."
            ),
            "established_finite_model_result",
            ("Stage10E:matched-public-views", "Stage10E:hidden-selector-controls"),
            (
                "Operational indistinguishability in the tested interface does not decide "
                "which modal semantics, if either, describes nature."
            ),
        ),
        ProjectQuestionAnswer(
            "Q3",
            "Are event/class/outcome correspondence and normalization semantics numerically redundant?",
            (
                "Not at the typed operational level. Stage 10F preserves or reconstructs "
                "several numerical payloads after removing their semantics, but the "
                "cross-perspective identification of one operational question becomes lost, "
                "underdetermined, or not established."
            ),
            "established_finite_model_result",
            ("Stage10F:correspondence-ablations", "Stage10F:normalization-ablations"),
            (
                "Non-redundant formal work in this representation does not make these "
                "resources metaphysically primitive."
            ),
        ),
        ProjectQuestionAnswer(
            "Q4",
            "Do perspective-invariant future probabilities establish a block universe or eternalism?",
            (
                "No. They establish covariance of a typed prediction rule across the "
                "tested clock perspectives. The construction remains compatible with "
                "distinct privileged modal semantics and does not convert a probability "
                "for a future outcome into an already-actual future event."
            ),
            "interpretation_guard",
            ("Stage10D:probability-covariance", "Stage10E:modal-distinction"),
            "Operational covariance is weaker than an ontological claim about what exists.",
        ),
        ProjectQuestionAnswer(
            "Q5",
            "Does Stage 10 refute ontological becoming?",
            (
                "No. Correctly typed covariance succeeds, while wrong typing and wrong "
                "normalization fail, but neither result tests whether reality itself "
                "contains an objective process of becoming."
            ),
            "interpretation_guard",
            ("Stage10F:false-positive-controls",),
            "Measurement-covariance success or failure is not a direct test of ontological becoming.",
        ),
        ProjectQuestionAnswer(
            "Q6",
            "How should the temporal candidate be updated after Stage 10?",
            (
                "Retain T=(O,P,R,V;Xi) with the existing R/V refinements and add the "
                "stronger bounded fact that Xi-typed future-measurement structure is "
                "operationally covariant across the finite continuation-aware clock atlas."
            ),
            "candidate_structural_interpretation",
            ("Stage10A-F:integrated-evidence",),
            (
                "This strengthens the finite architecture without proving that its layers "
                "are fundamental, unique, or sufficient for physical time."
            ),
        ),
        ProjectQuestionAnswer(
            "Q7",
            "What is the strongest unresolved structural boundary after Stage 10?",
            (
                "The project has repeatedly established finite clock-perspective covariance "
                "but has not tested reparametrization/gauge covariance or gravitational "
                "clock structure. The O layer also remains a deliberately minimal "
                "three-event skeleton."
            ),
            "untested_not_established",
            ("Stage10G:remaining-gates",),
            (
                "General covariance and richer causal order remain open; not established "
                "is not false."
            ),
        ),
        ProjectQuestionAnswer(
            "Q8",
            "Which next pressure test is selected?",
            (
                "A parametrized covariance precursor is selected: preserve the typed "
                "O/P/R/V measurement architecture while removing dependence on one "
                "preferred external parameterization before attempting a gravitational "
                "extension."
            ),
            "evidence_selected_research_gate",
            ("Stage10G:gate-ranking",),
            (
                "A parametrized precursor is not yet general relativity or quantum gravity; "
                "it is a controlled bridge from finite clock covariance toward those questions."
            ),
        ),
    )


SELECTED_STAGE11_GATE_LABEL = (
    "Construct a parametrized covariance precursor that preserves the typed "
    "O/P/R/V measurement architecture without assuming a preferred external "
    "time parameterization"
)


def stage11_gate_candidates(
    snapshot: Stage10EvidenceSnapshot | None = None,
) -> tuple[Stage11GateCandidate, ...]:
    evidence = evidence_snapshot() if snapshot is None else snapshot
    d = evidence.stage10d
    e = evidence.stage10e
    f = evidence.stage10f
    b = evidence.stage10b

    covariance_signals: list[str] = [
        "finite continuation-aware state/record/measurement covariance is now mature enough to carry into a parametrized constraint test"
    ]
    covariance_score = 5
    if d.measurement_covariance_status == "established":
        covariance_score += 2
        covariance_signals.append(
            "the explicit Stage 9 measurement-family boundary is closed at per-continuation probability level"
        )
    if e.weighted_modal_update_covariance_established:
        covariance_score += 1
        covariance_signals.append(
            "weights, matched modal public views, and evidence updates are also perspective-covariant"
        )
    if f.all_required_false_positive_controls_rejected:
        covariance_score += 1
        covariance_signals.append(
            "typing/normalization ablations identify which semantic resources must be carried into a broader covariance test"
        )

    order_signals: list[str] = [
        "O remains a deliberately minimal e0<e1<e2 order skeleton"
    ]
    order_score = 6
    if d.measurement_covariance_status == "established":
        order_score += 1
        order_signals.append(
            "the previously higher-priority measurement gap is closed, increasing the relative value of richer order structure"
        )

    clock_signals: list[str] = [
        "the current clock family remains ideal/projective and finite",
        "Stage 10B shows normalization transport is nontrivial under non-Euclidean-unitary clock maps",
    ]
    clock_score = 4
    if b.normalization_decision.genuine_maps_nonunitary:
        clock_score += 1
        clock_signals.append(
            "nonunitary support-coordinate changes already expose a meaningful normalization robustness target"
        )
    if d.accidental_canonical_equality_ruled_out:
        clock_score += 1
        clock_signals.append(
            "the tomography-complete measurement suite provides a strong probe set for future nonideal-clock tests"
        )

    candidates = (
        Stage11GateCandidate(
            "parametrized_covariance_precursor",
            SELECTED_STAGE11_GATE_LABEL,
            covariance_score,
            tuple(covariance_signals),
            (
                "Stage 10 has closed the known finite measurement-covariance gap and "
                "made the required typing resources explicit. A parametrized constraint "
                "test now changes one major assumption at a time: whether the retained "
                "structure survives redundancy in the external evolution parameter. "
                "This is a controlled precursor to general/gravitational covariance, "
                "not an immediate gravity claim."
            ),
        ),
        Stage11GateCandidate(
            "richer_causal_order",
            "Replace the minimal three-event O layer with richer causal/order structure",
            order_score,
            tuple(order_signals),
            (
                "This remains an important robustness test because the current O layer is "
                "schematic. It is ranked second because the repeated finite-clock versus "
                "general-covariance boundary is now the sharper project-wide gap after "
                "Stage 10 closes measurement transport."
            ),
        ),
        Stage11GateCandidate(
            "nonideal_povm_clocks",
            "Test interacting nonideal and POVM clock perspectives with the typed measurement family",
            clock_score,
            tuple(clock_signals),
            (
                "This probes P-layer robustness and the operational normalization scheme. "
                "It remains valuable, but it is a narrower clock-model perturbation than "
                "the parametrized-covariance boundary now selected."
            ),
        ),
    )
    return tuple(sorted(candidates, key=lambda item: (-item.score, item.gate_id)))


def stage10g_synthesis() -> Stage10GSynthesis:
    choice = select_synthesis_choice()
    candidates = stage11_gate_candidates()
    return Stage10GSynthesis(
        choice=choice,
        top_level_candidate=(
            "T10_candidate=(O,P,R,V;Xi), refined-layered with fully typed finite "
            "future-measurement covariance"
        ),
        established_scope=(
            "typed reference future-signature measurement at the A/e2 anchor",
            "continuation-specific effect/normalization lift",
            "18-chart / 108-transport / 324-composition measurement representation covariance",
            "per-continuation Born/completeness/positivity covariance on canonical and 196 tomography-complete probes",
            "weighted prediction, matched modal public-view, and evidence-update covariance",
            "explicit rejection/classification of wrong typing, wrong normalization, and weight/class misalignment",
        ),
        retained_typing_resources=(
            "event correspondence",
            "continuation-class correspondence",
            "outcome correspondence",
            "normalization semantics",
            "continuation-weight/class alignment",
        ),
        derived_or_reconstructible_roles=(
            "chart-local effect and normalization matrices from shared physical forms plus chart coordinates",
            "several numerical payloads after typing ablation, without preservation of typed operational identity",
        ),
        project_questions=answer_project_questions(),
        unresolved_boundaries=unresolved_boundaries(),
        stage11_candidates=candidates,
        selected_stage11_gate=candidates[0].gate_id,
    )


def stage10g_summary() -> dict[str, object]:
    synthesis = stage10g_synthesis()
    return {
        "stage": "10G",
        "synthesis": synthesis.as_dict(),
        "current_execution_criteria": {
            "48": (
                "derive the Stage 10 measurement-covariance synthesis choice from "
                "executable Stage 10A-F evidence"
            ),
            "49": (
                "rank unresolved Stage 11 gates and uniquely select the next "
                "evidence-driven pressure test"
            ),
            "50": "external final full-repository regression and merge-readiness review",
        },
        "guards": (
            "measurement_covariant finite family != general covariance",
            "future-measurement covariance != future actuality",
            "perspective-invariant future probabilities != proof of eternalism",
            "measurement covariance != modal/ontological identity",
            "measurement covariance != refutation of ontological becoming",
            "numerical reconstructibility != typed operational identification",
            "typed-resource necessity != metaphysical fundamentality",
            "parametrized covariance precursor != general relativity",
            "finite-model success != empirical discovery",
        ),
    }
