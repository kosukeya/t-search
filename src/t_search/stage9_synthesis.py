"""Stage 9G synthesis and evidence-selected Stage 10 gate.

Stages 9A--F integrated directional records with nontrivial quantum
Potentiality in one constrained continuation family, transported the typed
structure through genuine clock changes, classified P/O/R_direction/V
compatibility, and pressure-tested the roles by ablation.

Stage 9G synthesizes those executable diagnostics without promoting a finite
model result into a metaphysical or empirical claim.  The synthesis asks:

1. whether the refined layered candidate should be retained, reduced, rejected,
   or left inconclusive;
2. whether Stage 9 evidence requires a new direct Xi_RV value law; and
3. which unresolved pressure test is now the most discriminating next gate.

The current evidence supports retaining

    T9_candidate=(O,P,R,V;Xi)
    R=(R_content,R_direction,R_access)
    V=(V_extension,V_semantics,V_weights)

as a finite-model bookkeeping candidate.  Explicit P edge matrices are derived
from per-node coordinates in the tested atlas, while event/class/observable
typing remains an explicit correspondence resource.  No direct Xi_RV value
constraint is inferred merely from compatibility or covariance.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from functools import lru_cache
from typing import Any

from .stage5_clock_change import DEFAULT_ATOL
from .stage9_ablation import stage9f_ablation_matrix, stage9f_diagnostics
from .stage9_compatibility import stage9e_compatibility_diagnostics
from .stage9_controls import stage9b_control_diagnostics
from .stage9_modal import stage9c_modal_diagnostics
from .stage9_substrate import stage9a_substrate_diagnostics
from .stage9_transport import stage9d_transport_diagnostics


class Stage9SynthesisChoice(str, Enum):
    REFINED_LAYERED = "refined_layered"
    REDUCED = "reduced"
    BROKEN = "broken"
    INCONCLUSIVE = "inconclusive"


@dataclass(frozen=True, slots=True)
class LayerRefinement:
    layer_id: str
    components: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    interpretation: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


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
class Stage10GateCandidate:
    gate_id: str
    label: str
    score: int
    pressure_signals: tuple[str, ...]
    rationale: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class Stage9EvidenceSnapshot:
    stage9a: object
    stage9b: object
    stage9c: object
    stage9d: object
    stage9e: object
    stage9f: object
    ablation_matrix: tuple[object, ...]


@dataclass(frozen=True, slots=True)
class Stage9GSynthesis:
    choice: Stage9SynthesisChoice
    top_level_candidate: str
    layer_refinements: tuple[LayerRefinement, ...]
    compatibility_links: tuple[str, ...]
    derived_representation_roles: tuple[str, ...]
    project_questions: tuple[ProjectQuestionAnswer, ...]
    unresolved_implications: tuple[str, ...]
    stage10_candidates: tuple[Stage10GateCandidate, ...]
    selected_stage10_gate: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "choice": self.choice.value,
            "top_level_candidate": self.top_level_candidate,
            "layer_refinements": [item.as_dict() for item in self.layer_refinements],
            "compatibility_links": list(self.compatibility_links),
            "derived_representation_roles": list(self.derived_representation_roles),
            "project_questions": [item.as_dict() for item in self.project_questions],
            "unresolved_implications": list(self.unresolved_implications),
            "stage10_candidates": [item.as_dict() for item in self.stage10_candidates],
            "selected_stage10_gate": self.selected_stage10_gate,
        }


@lru_cache(maxsize=1)
def evidence_snapshot() -> Stage9EvidenceSnapshot:
    return Stage9EvidenceSnapshot(
        stage9a=stage9a_substrate_diagnostics(),
        stage9b=stage9b_control_diagnostics(),
        stage9c=stage9c_modal_diagnostics(),
        stage9d=stage9d_transport_diagnostics(),
        stage9e=stage9e_compatibility_diagnostics(),
        stage9f=stage9f_diagnostics(),
        ablation_matrix=stage9f_ablation_matrix(),
    )


def select_synthesis_choice(
    snapshot: Stage9EvidenceSnapshot | None = None,
    *,
    atol: float = DEFAULT_ATOL,
) -> Stage9SynthesisChoice:
    evidence = evidence_snapshot() if snapshot is None else snapshot
    e = evidence.stage9e
    f = evidence.stage9f

    integrated_compatibility = bool(
        e.r_direction_v_extension_compatible
        and e.r_direction_v_weights_compatible
        and e.r_direction_v_semantics_underdetermined
        and e.r_access_v_compatible
        and e.p_direction_v_compatible
        and e.o_direction_v_compatible
    )

    directional = f.directional_mechanism
    singleton = f.singleton_qext
    access = f.accessibility
    semantic = f.semantic_weights
    reconstruction = f.edge_reconstruction
    correspondence = f.correspondence

    r_internal_separation = bool(
        directional.no_scramble_direction_lost_while_current_record_retained
        and access.global_direction_preserved
        and access.local_access_inaccessible
    )

    finite_family_r_v_separation = bool(
        directional.record_write_v_nontrivial
        and all(abs(value) <= 10 * atol for _, value in directional.record_write_record_scores)
        and singleton.qext_size == 1
        and singleton.record_defined
        and singleton.record_score > atol
        and singleton.accessibility_score > atol
    )

    v_internal_stratification = bool(
        semantic.matched_public_views_equal
        and semantic.privileged_modal_structures_distinct
        and not semantic.modal_semantics_reconstructible_from_public_carrier
        and semantic.prediction_changes_with_weights
        and semantic.weight_change_preserves_directional_data
        and not semantic.weights_reconstructible_from_carrier
        and singleton.singleton_weight_reconstructible_from_normalization
    )

    p_representation_refined = bool(
        reconstruction.reconstructible_from_node_coordinates
        and reconstruction.valid
        and correspondence.local_p_atlas_retained
        and not correspondence.event_class_correspondence_declared
        and not correspondence.typed_cross_perspective_rv_identification_established
        and f.wrong_observable.detected
    )

    if (
        integrated_compatibility
        and r_internal_separation
        and finite_family_r_v_separation
        and v_internal_stratification
        and p_representation_refined
    ):
        return Stage9SynthesisChoice.REFINED_LAYERED

    if not integrated_compatibility:
        return Stage9SynthesisChoice.BROKEN

    if (
        semantic.modal_semantics_reconstructible_from_public_carrier
        or e.direct_xi_rv_value_constraint_established
    ):
        return Stage9SynthesisChoice.REDUCED

    return Stage9SynthesisChoice.INCONCLUSIVE


def layer_refinements() -> tuple[LayerRefinement, ...]:
    return (
        LayerRefinement(
            "R",
            ("R_content", "R_direction", "R_access"),
            (
                "Stage9F:scrambler-neutralized",
                "Stage9F:local-record-access-hidden",
                "Stage9B:directional-controls",
            ),
            (
                "Record content, record-defined direction, and local accessibility "
                "show different executable ablation behavior in the declared family."
            ),
        ),
        LayerRefinement(
            "V",
            ("V_extension", "V_semantics", "V_weights"),
            (
                "Stage9F:singleton-QExt",
                "Stage9F:modal-semantics-erased",
                "Stage9F:weights-unfixed",
            ),
            (
                "Continuation multiplicity, selected-vs-unselected modal typing, "
                "and continuation weights show different loss/reconstruction/"
                "underdetermination behavior and remain distinct bookkeeping roles."
            ),
        ),
    )


def unresolved_implications() -> tuple[str, ...]:
    return (
        "finite_family_R_direction_V_separation => universal_R_V_independence",
        "record_defined_direction => ontological_future_openness",
        "record_defined_direction => ontological_becoming",
        "selected_vs_unselected_modal_semantics => ontic_openness_in_nature",
        "Potentiality => phenomenal_passage",
        "physical_clock_change => temporal_succession",
        "finite_clock_covariance => general_covariance",
        "full_Stage9C_future_measurement_family_covariance",
        "direct_Xi_RV_value_law",
        "P_edge_reconstructibility => P_layer_redundant",
        "refined_O_P_R_V_Xi_candidate => fundamental_or_unique_time_ontology",
    )


def answer_project_questions() -> tuple[ProjectQuestionAnswer, ...]:
    return (
        ProjectQuestionAnswer(
            "Q1",
            "Can directional quantum records coexist with nontrivial Potentiality in one constrained continuation family?",
            (
                "Yes in the declared Stage 9 family. Two physically inequivalent "
                "continuations share one current Actuality and each carries the same "
                "nonzero direction before weighting, while genuine clock transport, "
                "modal underdetermination, and weight sensitivity remain available."
            ),
            "established_finite_model_result",
            ("Stage9A:directional-QExt", "Stage9D:typed-transport", "Stage9E:compatibility"),
            (
                "This establishes bounded structural compatibility, not ontically real "
                "alternative futures or ontological becoming."
            ),
        ),
        ProjectQuestionAnswer(
            "Q2",
            "Does V_extension multiplicity determine R_direction, or does R_direction determine V_extension multiplicity?",
            (
                "No in the declared finite ablation family. Nontrivial h_L/h_R V "
                "survives record/direction neutralization, while a singleton QExt "
                "retains nonzero directional R."
            ),
            "established_finite_model_result",
            ("Stage9E:implication-controls", "Stage9F:bidirectional-countermodels"),
            "Finite-family countermodels do not constitute a universal R-V independence theorem.",
        ),
        ProjectQuestionAnswer(
            "Q3",
            "Are record content, record-defined direction, and local record accessibility one role?",
            (
                "No in the declared family. Scrambler neutralization preserves one-bit "
                "record content while directional asymmetry vanishes, and the access "
                "ablation preserves global record/direction while hiding local R_access."
            ),
            "established_finite_model_result",
            ("Stage9F:scrambler-neutralized", "Stage9F:local-access-hidden"),
            "Role separation in this model does not prove three fundamental primitives.",
        ),
        ProjectQuestionAnswer(
            "Q4",
            "Does nonzero directional R determine selected-vs-unselected V_semantics?",
            (
                "No operational determination is established. Matched directional "
                "public views and hidden-selector swap invariance coexist with distinct "
                "privileged modal structures."
            ),
            "established_finite_model_result",
            ("Stage9C:directional-modal-underdetermination", "Stage9E:R_direction-V_semantics"),
            "Operational underdetermination does not establish which modal interpretation describes nature.",
        ),
        ProjectQuestionAnswer(
            "Q5",
            "Does Stage 9 require a new direct Xi_RV value law?",
            (
                "No such law is required or established by the current evidence. "
                "R_direction and V are compatible and partly separable while explicit "
                "event/class/observable correspondence remains the necessary typed Xi resource."
            ),
            "candidate_structural_interpretation",
            ("Stage9E:direct-Xi_RV-not-established", "Stage9F:chi-ablation"),
            "Failure to establish a direct Xi_RV law is not proof that no such law can exist in a broader theory.",
        ),
        ProjectQuestionAnswer(
            "Q6",
            "Are explicit P edge matrices primitive in the current representation?",
            (
                "No. All 108 canonical continuation-aware edges are reconstructed "
                "from retained per-node coordinates, but removing event/class chi "
                "makes typed cross-perspective P-R-V identification not established."
            ),
            "established_finite_model_result",
            ("Stage9F:P-edge-reconstruction", "Stage9F:chi-ablation"),
            "Reconstructible edge matrices do not imply P is universally redundant or identical to R/V.",
        ),
        ProjectQuestionAnswer(
            "Q7",
            "Has the full Stage 9 operational transport problem been closed?",
            (
                "No. State, record-observable, continuation-class, and weight transport "
                "are established in the declared atlas, but the full cross-continuation "
                "Stage 9C future-signature measurement family remains not established."
            ),
            "untested_not_established",
            ("Stage9D:future-measurement-boundary", "Stage9E:measurement-boundary"),
            "Not established is not false and is the strongest explicit operational boundary left by Stage 9.",
        ),
        ProjectQuestionAnswer(
            "Q8",
            "How should the temporal candidate be updated after Stage 9?",
            (
                "Retain the top-level layered candidate T=(O,P,R,V;Xi), keep the "
                "internal R/V refinements, treat explicit P edges as derived when "
                "node coordinates are retained, and retain Xi as typed correspondence "
                "without adding an unsupported direct Xi_RV value law."
            ),
            "candidate_structural_interpretation",
            ("Stage9E:compatibility", "Stage9F:ablation"),
            "This is a finite-model architecture candidate, not a fundamental or unique ontology of time.",
        ),
    )


SELECTED_STAGE10_GATE_LABEL = (
    "Construct and validate a fully typed cross-continuation future-measurement "
    "family under genuine continuation-aware clock changes"
)


def stage10_gate_candidates(
    snapshot: Stage9EvidenceSnapshot | None = None,
) -> tuple[Stage10GateCandidate, ...]:
    evidence = evidence_snapshot() if snapshot is None else snapshot
    d = evidence.stage9d
    e = evidence.stage9e
    f = evidence.stage9f

    measurement_signals: list[str] = []
    measurement_score = 4
    if not d.full_stage9c_future_measurement_covariance_established:
        measurement_score += 3
        measurement_signals.append(
            "full Stage 9C cross-continuation future-signature measurement-family covariance remains not established"
        )
    if d.continuation_level_transport_covariance:
        measurement_score += 1
        measurement_signals.append(
            "continuation-specific state/metric/record transport is already covariant, isolating the missing measurement-family layer"
        )
    if e.p_direction_v_compatible:
        measurement_score += 1
        measurement_signals.append(
            "typed P-R_direction-V compatibility is positive, so the remaining operational gap is narrower and directly testable"
        )

    order_signals: list[str] = [
        "O remains a deliberately minimal e0<e1<e2 skeleton"
    ]
    order_score = 4
    if e.o_does_not_determine_r_direction:
        order_score += 1
        order_signals.append(
            "the minimal O skeleton does not determine record direction in the tested controls"
        )
    if e.same_order_skeleton_supports_positive_negative_and_zero_direction:
        order_score += 1
        order_signals.append(
            "one order skeleton supports positive, negative, and zero directional diagnostics"
        )

    covariance_signals: list[str] = [
        "the finite O/P/R/V architecture is substantially more mature after Stage 9"
    ]
    covariance_score = 3
    if e.r_direction_v_extension_compatible:
        covariance_score += 1
        covariance_signals.append(
            "the previous directional-R/V integration blocker is now positive"
        )
    if (
        f.edge_reconstruction.reconstructible_from_node_coordinates
        and f.directional_mechanism.no_scramble_direction_lost_while_current_record_retained
    ):
        covariance_score += 1
        covariance_signals.append(
            "ablation/reconstruction evidence now isolates several finite-model roles before a covariance extension"
        )

    clock_signals = (
        "current clock charts are ideal finite projective readings",
        "robustness to nonideal/POVM clocks remains open after the directional-R/V gate",
    )
    clock_score = 4

    candidates = (
        Stage10GateCandidate(
            "full_measurement_covariance",
            SELECTED_STAGE10_GATE_LABEL,
            measurement_score,
            tuple(measurement_signals),
            (
                "Closes the last explicit Stage 9 operational-transport boundary by "
                "constructing one typed future-signature measurement family whose "
                "effects, outcomes, continuation semantics, and probabilities can be "
                "compared under genuine clock changes rather than inferred from state/record covariance."
            ),
        ),
        Stage10GateCandidate(
            "richer_causal_order",
            "Replace the minimal three-event O layer with richer causal/order structure",
            order_score,
            tuple(order_signals),
            (
                "Tests whether the current O/R/V separations survive a less schematic "
                "history structure, but the existing measurement-family boundary is "
                "more sharply isolated and therefore more discriminating first."
            ),
        ),
        Stage10GateCandidate(
            "parametrized_covariance_precursor",
            "Begin a parametrized / generally covariant precursor",
            covariance_score,
            tuple(covariance_signals),
            (
                "The finite architecture is now mature enough to make this a serious "
                "next-near-term option, but moving to covariance before closing the "
                "known future-measurement transport gap would add avoidable confounds."
            ),
        ),
        Stage10GateCandidate(
            "nonideal_povm_clocks",
            "Test interacting nonideal and POVM clock perspectives",
            clock_score,
            clock_signals,
            (
                "Important P robustness work, but it does not directly close the one "
                "operational relation repeatedly marked not_established in Stages 9D-F."
            ),
        ),
    )
    return tuple(sorted(candidates, key=lambda item: (-item.score, item.gate_id)))


def stage9g_synthesis() -> Stage9GSynthesis:
    choice = select_synthesis_choice()
    candidates = stage10_gate_candidates()
    return Stage9GSynthesis(
        choice=choice,
        top_level_candidate=(
            "T9_candidate=(O,P,R,V;Xi), refined-layered with typed internal R and V roles"
        ),
        layer_refinements=layer_refinements(),
        compatibility_links=(
            "Xi_PO:event/current-anchor compatibility",
            "Xi_PR:typed directional-record covariance",
            "Xi_PV:continuation-class/weight covariance",
            "Xi_event_class_observable:explicit cross-perspective semantic correspondence",
            "direct Xi_RV value law:not_established",
        ),
        derived_representation_roles=(
            "explicit P edge matrices from per-node continuation coordinates",
            "singleton continuation weight from normalization",
        ),
        project_questions=answer_project_questions(),
        unresolved_implications=unresolved_implications(),
        stage10_candidates=candidates,
        selected_stage10_gate=candidates[0].gate_id,
    )


def stage9g_summary() -> dict[str, object]:
    synthesis = stage9g_synthesis()
    return {
        "stage": "9G",
        "synthesis": synthesis.as_dict(),
        "current_execution_criteria": {
            "48": (
                "derive the Stage 9 synthesis choice and refined finite-model candidate "
                "from executable Stage 9A-F evidence"
            ),
            "49": (
                "rank evidence-selected Stage 10 gates and select one uniquely most "
                "discriminating next pressure test"
            ),
            "50": "external final full-repository regression and merge-readiness review",
        },
        "guards": (
            "refined layered candidate != fundamental ontology",
            "finite-family bidirectional countermodels != universal R-V independence theorem",
            "no direct Xi_RV law established != no possible R-V constraint",
            "P edge reconstruction != P layer universally redundant",
            "operational underdetermination != ontic openness",
            "directional record arrow != ontological future openness",
            "directional record arrow != ontological becoming",
            "full Stage 9C future-measurement covariance remains not_established",
            "finite clock covariance != general covariance",
            "not_established != false",
        ),
    }
