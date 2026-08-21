"""Stage 8G synthesis and evidence-selected Stage 9 gate.

Stage 8A--F integrated executable quantum continuations V into the constrained
P/O/R construction, typed selected-vs-unselected semantics, tested operational
underdetermination and genuine clock transport, and then ablated the resulting
roles. Stage 8G synthesizes those executable diagnostics without upgrading a
finite-model result into a metaphysical claim.

The synthesis keeps the top-level candidate T=(O,P,R,V;Xi), but asks whether R
and V should be refined internally. The current evidence supports the typed
refinements

    R = (R_content, R_direction, R_access)
    V = (V_extension, V_semantics, V_weights)

as a candidate bookkeeping structure. These component labels describe roles
that showed different compatibility/ablation behavior; they are not asserted to
be fundamental primitives.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from functools import lru_cache
from typing import Any

from .stage5_clock_change import DEFAULT_ATOL
from .stage8_ablation import (
    mismatch_diagnostics,
    no_record_v_family_diagnostics,
    perspective_map_reconstruction_diagnostics,
    semantic_weight_reconstruction_diagnostics,
    singleton_qext_diagnostics,
    stage8f_ablation_matrix,
)
from .stage8_compatibility import stage8e_compatibility_diagnostics
from .stage8_continuations import stage8a_substrate_diagnostics
from .stage8_modal import stage8b_modal_diagnostics
from .stage8_modal_transport import stage8d_transport_diagnostics
from .stage8_operational import stage8c_operational_diagnostics


class Stage8SynthesisChoice(str, Enum):
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
class Stage9GateCandidate:
    gate_id: str
    label: str
    score: int
    pressure_signals: tuple[str, ...]
    rationale: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class Stage8EvidenceSnapshot:
    stage8a: object
    stage8b: object
    stage8c: object
    stage8d: object
    stage8e: object
    no_record_v: object
    singleton_v: object
    semantic_weight: object
    p_map_reconstruction: object
    ablation_matrix: tuple[object, ...]
    mismatch_matrix: tuple[object, ...]


@dataclass(frozen=True, slots=True)
class Stage8GSynthesis:
    choice: Stage8SynthesisChoice
    top_level_candidate: str
    layer_refinements: tuple[LayerRefinement, ...]
    compatibility_links: tuple[str, ...]
    derived_representation_roles: tuple[str, ...]
    project_questions: tuple[ProjectQuestionAnswer, ...]
    unresolved_implications: tuple[str, ...]
    stage9_candidates: tuple[Stage9GateCandidate, ...]
    selected_stage9_gate: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "choice": self.choice.value,
            "top_level_candidate": self.top_level_candidate,
            "layer_refinements": [item.as_dict() for item in self.layer_refinements],
            "compatibility_links": list(self.compatibility_links),
            "derived_representation_roles": list(self.derived_representation_roles),
            "project_questions": [item.as_dict() for item in self.project_questions],
            "unresolved_implications": list(self.unresolved_implications),
            "stage9_candidates": [item.as_dict() for item in self.stage9_candidates],
            "selected_stage9_gate": self.selected_stage9_gate,
        }


@lru_cache(maxsize=1)
def evidence_snapshot() -> Stage8EvidenceSnapshot:
    return Stage8EvidenceSnapshot(
        stage8a=stage8a_substrate_diagnostics(),
        stage8b=stage8b_modal_diagnostics(),
        stage8c=stage8c_operational_diagnostics(),
        stage8d=stage8d_transport_diagnostics(),
        stage8e=stage8e_compatibility_diagnostics(),
        no_record_v=no_record_v_family_diagnostics(),
        singleton_v=singleton_qext_diagnostics(),
        semantic_weight=semantic_weight_reconstruction_diagnostics(),
        p_map_reconstruction=perspective_map_reconstruction_diagnostics(),
        ablation_matrix=stage8f_ablation_matrix(),
        mismatch_matrix=mismatch_diagnostics(),
    )


def select_synthesis_choice(
    snapshot: Stage8EvidenceSnapshot | None = None,
    *,
    atol: float = DEFAULT_ATOL,
) -> Stage8SynthesisChoice:
    evidence = evidence_snapshot() if snapshot is None else snapshot
    e = evidence.stage8e
    no_record = evidence.no_record_v
    singleton = evidence.singleton_v
    semantic_weight = evidence.semantic_weight
    maps = evidence.p_map_reconstruction

    compatibility_positive = bool(
        e.p_o_event_effect_covariance
        and e.p_r_current_record_covariance
        and e.p_v_class_weight_covariance
        and e.o_v_difference_after_current_anchor
    )
    r_v_separation = bool(
        no_record.current_record_lost
        and no_record.perspective_structure_preserved
        and no_record.physically_inequivalent
        and no_record.privileged_modal_structures_distinct
        and no_record.weight_mismatch_changes_prediction
    )
    v_internal_stratification = bool(
        singleton.physical_multiplicity_lost
        and singleton.semantic_types_distinct
        and singleton.singleton_weight_reconstructible_from_normalization
        and semantic_weight.same_carrier_distinct_modal_semantics
        and not semantic_weight.modal_semantics_reconstructible_from_public_por
        and semantic_weight.same_carrier_admits_distinct_weights
        and semantic_weight.prediction_changes_with_weights
        and not semantic_weight.weights_reconstructible_from_carrier
    )
    p_representation_refined = bool(
        maps.reconstructible
        and maps.max_reference_map_residual <= atol
        and maps.max_state_transport_residual <= atol
        and maps.max_metric_covariance_residual <= atol
    )

    if compatibility_positive and r_v_separation and v_internal_stratification and p_representation_refined:
        return Stage8SynthesisChoice.REFINED_LAYERED
    if not compatibility_positive:
        return Stage8SynthesisChoice.BROKEN
    if semantic_weight.modal_semantics_reconstructible_from_public_por:
        return Stage8SynthesisChoice.REDUCED
    return Stage8SynthesisChoice.INCONCLUSIVE


def layer_refinements() -> tuple[LayerRefinement, ...]:
    return (
        LayerRefinement(
            "R",
            ("R_content", "R_direction", "R_access"),
            (
                "Stage8E:one-bit-current-record-with-zero-directional-score",
                "Stage7C:directional-record-control",
                "Stage8F:hidden-access-ablation",
            ),
            "Record content, record-defined direction, and local accessibility have different witnesses and ablation behavior in the declared family.",
        ),
        LayerRefinement(
            "V",
            ("V_extension", "V_semantics", "V_weights"),
            (
                "Stage8F:no-record-V-family",
                "Stage8F:singleton-QExt",
                "Stage8F:semantic-weight-reconstruction",
            ),
            "Physical continuation multiplicity, selected-vs-unselected modal typing, and continuation weights have different ablation/reconstruction behavior and are retained as internal V roles rather than collapsed into one primitive quantity.",
        ),
    )


def unresolved_implications() -> tuple[str, ...]:
    return (
        "directional_record_structure <=> nontrivial_V_structure",
        "record_defined_direction => ontological_future_openness",
        "selected_vs_unselected_modal_semantics => ontic_openness_in_nature",
        "Potentiality => phenomenal_passage",
        "physical_clock_change => temporal_succession",
        "P_V_covariance => general_covariance",
        "full_Stage8C_measurement_family_covariance",
        "V_internal_roles => fundamental_independent_primitives",
        "refined_O_P_R_V_Xi_candidate => fundamental_or_unique_time_ontology",
    )


def answer_project_questions() -> tuple[ProjectQuestionAnswer, ...]:
    return (
        ProjectQuestionAnswer(
            "Q1",
            "Can nontrivial quantum Potentiality coexist with P, O, and current target-specific R in one constrained model family?",
            "Yes in the declared Stage 8 canonical family: executable continuation classes, genuine clock perspectives, event/order structure, and one-bit current record content coexist with matched selected-vs-unselected operational views.",
            "established_finite_model_result",
            ("Stage8A:QExt", "Stage8D:P-V", "Stage8E:P/O/R/V"),
            "This is a bounded finite-model compatibility result, not a claim of ontically real alternative futures.",
        ),
        ProjectQuestionAnswer(
            "Q2",
            "Does current target-specific record content determine or remain necessary for nontrivial V/P/O structure?",
            "No in the declared ablation family. Neutralizing the current record write removes current target-memory information while two physically inequivalent continuations, genuine clock transport, modal underdetermination, and weight-sensitive prediction remain.",
            "established_finite_model_result",
            ("Stage8F:no-record-V-family",),
            "This refutes the implication only for the declared family; it is not a universal R-V independence theorem.",
        ),
        ProjectQuestionAnswer(
            "Q3",
            "Do the retained public quantum state, Born predictions, P/O/current-R structure, or carrier uniquely determine selected-vs-unselected modal semantics?",
            "No in the declared family. The same carrier and matched public views support both a hidden selected continuation model and a no-selected-continuation model.",
            "established_finite_model_result",
            ("Stage8B:typed-semantics", "Stage8C:operational-underdetermination", "Stage8E:modal-underdetermination"),
            "Formal semantic underdetermination does not establish which interpretation, if either, describes nature.",
        ),
        ProjectQuestionAnswer(
            "Q4",
            "Should V remain one undifferentiated role after Stage 8F?",
            "No as a bookkeeping choice: continuation multiplicity, modal selection semantics, and weights show distinct ablation/reconstruction behavior, so V is better represented internally as V=(V_extension,V_semantics,V_weights).",
            "candidate_structural_interpretation",
            ("Stage8F:singleton-QExt", "Stage8F:semantic-weight-reconstruction"),
            "Internal role separation does not prove three fundamental metaphysical primitives.",
        ),
        ProjectQuestionAnswer(
            "Q5",
            "Are explicit P-V edge matrices primitive?",
            "Not in the declared representation. All tested continuation-aware edge matrices are reconstructed from retained per-node coordinates, while explicit event/class correspondence remains necessary to type cross-perspective identification.",
            "established_finite_model_result",
            ("Stage8F:P-map-reconstruction", "Stage8F:chi-ablation"),
            "Reconstructible explicit maps do not imply P=V or eliminate the perspective layer.",
        ),
        ProjectQuestionAnswer(
            "Q6",
            "Has full P/O/directional-R/V integration been established?",
            "No. The canonical V carrier has current record content but no directional record arrow, and full Stage 8C measurement-family covariance remains not established.",
            "untested_not_established",
            ("Stage8E:directional-partial", "Stage8D:measurement-boundary"),
            "Absence of a positive witness here is not a proof of universal R_direction-V incompatibility.",
        ),
        ProjectQuestionAnswer(
            "Q7",
            "How should the temporal candidate be updated after Stage 8?",
            "Retain the top-level layered candidate T=(O,P,R,V;Xi), refine R and V internally by their distinct tested roles, retain Xi for typed compatibility/correspondence, and treat explicit P edge matrices as a derived representation when per-node coordinates are retained.",
            "candidate_structural_interpretation",
            ("Stage8E:compatibility", "Stage8F:ablation"),
            "This is a finite-model architecture candidate, not a fundamental or unique ontology of time.",
        ),
    )


def stage9_gate_candidates(
    snapshot: Stage8EvidenceSnapshot | None = None,
) -> tuple[Stage9GateCandidate, ...]:
    evidence = evidence_snapshot() if snapshot is None else snapshot
    e = evidence.stage8e
    d = evidence.stage8d
    no_record = evidence.no_record_v

    directional_signals: list[str] = [
        "Stage 8E leaves full P/O/directional-R/V integration partial because directional R is absent in the canonical nontrivial V carrier"
    ]
    directional_score = 5
    if e.record_scramble_control_directional_r_present:
        directional_score += 2
        directional_signals.append("Stage 7C/8E already provides a physically constrained directional-record control with the same current prefix")
    if no_record.current_record_lost and no_record.physically_inequivalent:
        directional_score += 1
        directional_signals.append("Stage 8F separately shows nontrivial V survives removal of current record content, sharpening the remaining directional-R/V question")
    if e.p_v_class_weight_covariance:
        directional_score += 1
        directional_signals.append("continuation-class/weight P-V covariance is already positive, allowing a focused R_direction-V pressure test")

    measurement_signals: list[str] = []
    measurement_score = 2
    if not d.full_stage8c_measurement_covariance_established:
        measurement_score += 3
        measurement_signals.append("full Stage 8C cross-continuation measurement-family covariance remains not established")
    if not d.one_rederived_map_suffices_for_all_continuations:
        measurement_score += 1
        measurement_signals.append("continuation-specific clock maps differ, so a genuinely typed measurement-family transport remains nontrivial")

    order_signals = (
        "O remains a deliberately minimal three-event skeleton",
        "order does not force directional R in the current finite family",
    )
    order_score = 5

    clock_signals = (
        "current clocks remain finite/projective and continuation-specific",
        "nonideal/POVM robustness is still open but no longer the most discriminating missing compatibility link",
    )
    clock_score = 3

    gravity_signals = (
        "the finite layered architecture is substantially more mature after Stage 8",
        "directional R-V compatibility and full measurement-family covariance remain unresolved and would confound an immediate generally covariant extension",
    )
    gravity_score = 2

    candidates = (
        Stage9GateCandidate(
            "directional_record_potentiality",
            "Integrate directional record formation with nontrivial quantum Potentiality in one constrained continuation family",
            directional_score,
            tuple(directional_signals),
            "Directly targets the strongest remaining partial compatibility row: construct nontrivial QExt with internally anchored directional record formation, then test R_direction-V compatibility, reversal controls, and genuine clock transport without assuming record direction implies ontic openness.",
        ),
        Stage9GateCandidate(
            "full_measurement_covariance",
            "Construct a fully typed cross-continuation measurement family under genuine clock changes",
            measurement_score,
            tuple(measurement_signals),
            "Resolves the main Stage 8D operational-transport limitation, but is narrower than the unresolved directional-R/V structural link.",
        ),
        Stage9GateCandidate(
            "richer_causal_order",
            "Replace the minimal three-event O layer with richer causal/order structure",
            order_score,
            order_signals,
            "Tests robustness of O/R/V separation under a less schematic history structure after the more immediate directional-R/V gap is addressed.",
        ),
        Stage9GateCandidate(
            "nonideal_povm_clocks",
            "Test interacting nonideal and POVM clock perspectives",
            clock_score,
            clock_signals,
            "Important P robustness work, but current evidence points more directly to the unresolved R_direction-V link.",
        ),
        Stage9GateCandidate(
            "parametrized_covariance_precursor",
            "Begin a parametrized / generally covariant precursor",
            gravity_score,
            gravity_signals,
            "Still important, but evidence-selected sequencing favors closing the remaining finite-model directional-R/V gap before adding covariance/gravity confounds.",
        ),
    )
    return tuple(sorted(candidates, key=lambda item: (-item.score, item.gate_id)))


def stage8g_synthesis() -> Stage8GSynthesis:
    choice = select_synthesis_choice()
    candidates = stage9_gate_candidates()
    return Stage8GSynthesis(
        choice=choice,
        top_level_candidate="T8_candidate=(O,P,R,V;Xi), with typed internal R and V roles",
        layer_refinements=layer_refinements(),
        compatibility_links=(
            "Xi_PO:event-effect covariance",
            "Xi_PR:current-record covariance with corresponding observables",
            "Xi_PV:continuation-class/weight covariance with explicit event/class correspondence",
            "Xi_OV:future-only continuation extension relation",
        ),
        derived_representation_roles=(
            "explicit P-V edge matrices from per-node continuation coordinates",
            "singleton continuation weight from normalization",
        ),
        project_questions=answer_project_questions(),
        unresolved_implications=unresolved_implications(),
        stage9_candidates=candidates,
        selected_stage9_gate=candidates[0].gate_id,
    )


def stage8g_summary() -> dict[str, object]:
    synthesis = stage8g_synthesis()
    return {
        "stage": "8G",
        "synthesis": synthesis.as_dict(),
        "current_execution_criteria": {
            "48": "derive the Stage 8 synthesis choice and refined finite-model candidate from executable Stage 8A-F evidence",
            "49": "rank evidence-selected Stage 9 gates and select one uniquely most discriminating next pressure test",
            "50": "external final full-repository regression and merge-readiness review",
        },
        "guards": (
            "refined layered candidate != fundamental ontology",
            "V internal role separation != fundamental primitive decomposition",
            "record-neutral V witness != universal R-V independence theorem",
            "directional R absent from canonical V carrier != universal R_direction-V incompatibility",
            "operational underdetermination != ontic openness",
            "P-V map reconstruction != P=V",
            "not_established != false",
        ),
    }
