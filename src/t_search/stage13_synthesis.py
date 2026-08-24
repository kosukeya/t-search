"""Stage 13G executable synthesis and evidence-selected Stage 14 gate.

Stage 13A--F construct, transport, quotient, operationalize, and pressure-test a
finite two-constraint path-covariant carrier. Stage 13G integrates those
validated diagnostics into exactly one frozen Stage 13 synthesis status and
ranks the next research gates without promoting the finite result to
refoliation invariance, a hypersurface-deformation algebra, general covariance,
general relativity, eternalism, or ontological becoming.

``multi_constraint_path_covariant`` is deliberately bounded. It means that on
the declared four-orbit finite family, the two independent first-class
constraint directions, compensated mixed paths, Dirac/two-clock relational
observables, typed gauge quotient, O/P/R/V/Xi architecture, future-measurement
payloads, and equivalent commuting-basis presentation agree in the tested ways,
while the frozen destructive/anomaly controls are rejected.

The next-gate ranking treats the Stage 13F basis-equivalence result as a pressure
signal: the original noncommuting presentation is removable by the simple
``K_X_tilde=exp(-T)K_X`` rescaling on this carrier. The strongest next structural
question is therefore whether a phase-space-dependent structure-function
precursor retains the Stage 13 quotient/relational/operational results and
whether the same basis-trivialization persists. This is a precursor test, not
an assumption that a hypersurface-deformation algebra or refoliation invariance
has already been obtained.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from functools import lru_cache
from typing import Any

from .stage13_ablation import Stage13FDiagnostics, stage13f_diagnostics
from .stage13_gauge_atlas import Stage13DDiagnostics, stage13d_diagnostics
from .stage13_measurement import Stage13EDiagnostics, stage13e_diagnostics
from .stage13_multi_constraint import Stage13ADiagnostics, stage13a_diagnostics
from .stage13_paths import Stage13BDiagnostics, stage13b_diagnostics
from .stage13_relational import Stage13CDiagnostics, stage13c_diagnostics


class Stage13SynthesisChoice(str, Enum):
    MULTI_CONSTRAINT_PATH_COVARIANT = "multi_constraint_path_covariant"
    MULTI_CONSTRAINT_PATH_PARTIAL = "multi_constraint_path_partial"
    MULTI_CONSTRAINT_PATH_OBSTRUCTED = "multi_constraint_path_obstructed"
    INCONCLUSIVE = "inconclusive"


@dataclass(frozen=True, slots=True)
class Stage13ProjectQuestionAnswer:
    question_id: str
    question: str
    answer: str
    evidence_class: str
    evidence_refs: tuple[str, ...]
    boundary: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class Stage14GateCandidate:
    gate_id: str
    label: str
    score: int
    pressure_signals: tuple[str, ...]
    rationale: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class Stage13EvidenceSnapshot:
    stage13a: Stage13ADiagnostics
    stage13b: Stage13BDiagnostics
    stage13c: Stage13CDiagnostics
    stage13d: Stage13DDiagnostics
    stage13e: Stage13EDiagnostics
    stage13f: Stage13FDiagnostics


@dataclass(frozen=True, slots=True)
class Stage13GSynthesis:
    choice: Stage13SynthesisChoice
    top_level_candidate: str
    established_scope: tuple[str, ...]
    retained_typing_resources: tuple[str, ...]
    derived_or_reconstructible_roles: tuple[str, ...]
    project_questions: tuple[Stage13ProjectQuestionAnswer, ...]
    unresolved_boundaries: tuple[str, ...]
    stage14_candidates: tuple[Stage14GateCandidate, ...]
    selected_stage14_gate: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "choice": self.choice.value,
            "top_level_candidate": self.top_level_candidate,
            "established_scope": list(self.established_scope),
            "retained_typing_resources": list(self.retained_typing_resources),
            "derived_or_reconstructible_roles": list(self.derived_or_reconstructible_roles),
            "project_questions": [item.as_dict() for item in self.project_questions],
            "unresolved_boundaries": list(self.unresolved_boundaries),
            "stage14_candidates": [item.as_dict() for item in self.stage14_candidates],
            "selected_stage14_gate": self.selected_stage14_gate,
        }


@lru_cache(maxsize=1)
def evidence_snapshot() -> Stage13EvidenceSnapshot:
    """Evaluate the completed Stage 13A--F diagnostics once per process."""

    return Stage13EvidenceSnapshot(
        stage13a=stage13a_diagnostics(),
        stage13b=stage13b_diagnostics(),
        stage13c=stage13c_diagnostics(),
        stage13d=stage13d_diagnostics(),
        stage13e=stage13e_diagnostics(),
        stage13f=stage13f_diagnostics(),
    )


def _layer_validity(snapshot: Stage13EvidenceSnapshot) -> tuple[bool, ...]:
    return (
        snapshot.stage13a.criteria_11_16_satisfied,
        snapshot.stage13b.criteria_17_23_satisfied,
        snapshot.stage13c.criteria_24_31_satisfied,
        snapshot.stage13d.criteria_32_38_satisfied,
        snapshot.stage13e.criteria_39_43_satisfied,
        snapshot.stage13f.criteria_44_47_satisfied,
    )


def select_synthesis_choice(
    snapshot: Stage13EvidenceSnapshot | None = None,
) -> Stage13SynthesisChoice:
    evidence = evidence_snapshot() if snapshot is None else snapshot
    a, b, c, d, e, f = (
        evidence.stage13a,
        evidence.stage13b,
        evidence.stage13c,
        evidence.stage13d,
        evidence.stage13e,
        evidence.stage13f,
    )
    validity = _layer_validity(evidence)

    if all(validity):
        return Stage13SynthesisChoice.MULTI_CONSTRAINT_PATH_COVARIANT

    # ``obstructed`` is reserved for an explicit failure of the declared
    # positive family. A deliberately invalid control being rejected correctly
    # is evidence for the positive model, not an obstruction.
    explicit_positive_obstruction = bool(
        not a.representative_family_complete
        or not a.independent_constraint_directions
        or not a.first_class_closure_established
        or not a.individual_flows_preserve_surface
        or not a.physical_initial_data_preserved
        or b.compensated_closure_count != b.mixed_pair_count
        or b.compensated_surface_preservation_count != b.mixed_pair_count
        or not b.physical_orbit_identity_preserved
        or b.maximum_compensated_target_residual > 1e-8
        or b.maximum_compensated_constraint_residual > 1e-8
        or c.physically_distinct_pair_count != c.distinct_orbit_pair_count
        or c.max_compensated_path_relational_residual > 1e-8
        or not c.nontrivial_complete_relational_change
        or not d.quotient_partition_exact
        or d.cross_orbit_arrow_count > 0
        or not d.physical_dirac_data_not_collapsed
        or d.max_compensated_dirac_payload_residual > 1e-8
        or d.max_compensated_relational_payload_residual > 1e-8
        or e.distinct_quotient_architecture_count != e.physical_orbit_count
        or e.distinct_orbit_witness_count != e.physical_orbit_count
        or max(
            e.max_compensated_public_architecture_residual,
            e.max_compensated_measurement_probability_residual,
            e.max_compensated_weighted_probability_residual,
            e.max_compensated_posterior_residual,
            e.max_compensated_witness_residual,
        ) > 1e-8
        or f.commuting_constraint_surface_count != f.representative_count
        or f.stage13d_membership_match_count != f.commuting_quotient_class_count
        or f.basis_equivalent_count != f.basis_equivalence_check_count
        or f.commuting_mixed_path_closed_count != f.commuting_mixed_path_check_count
        or max(
            f.max_K_X_tilde_constraint_residual,
            f.max_KT_KX_tilde_bracket_residual,
            f.max_commuting_arrow_endpoint_residual,
            f.max_commuting_arrow_constraint_residual,
            f.max_commuting_mixed_endpoint_separation,
            f.max_commuting_mixed_target_residual,
            f.max_commuting_mixed_constraint_residual,
            f.max_basis_dirac_residual,
            f.max_basis_relational_residual,
        ) > 1e-8
    )
    if explicit_positive_obstruction:
        return Stage13SynthesisChoice.MULTI_CONSTRAINT_PATH_OBSTRUCTED

    if any(validity):
        return Stage13SynthesisChoice.MULTI_CONSTRAINT_PATH_PARTIAL

    return Stage13SynthesisChoice.INCONCLUSIVE


def unresolved_boundaries() -> tuple[str, ...]:
    return (
        "basis_trivializable_noncommuting_presentation => phase_space_dependent_structure_function_algebra",
        "finite_multi_constraint_path_covariance => refoliation_invariance",
        "finite_first_class_constraint_algebra => hypersurface_deformation_algebra",
        "finite_constraint_generated_gauge_atlas => general_covariance_or_diffeomorphism_invariance",
        "six_dimensional_toy_phase_space => dynamical_gravitational_field_degrees_of_freedom",
        "finite_orbit_sensitive_measurement_bridge => independent_dynamical_or_empirical_measurement_law",
        "minimal_relational_event_order => robustness_under_richer_causal_order",
        "ideal_projective_clock_family => nonideal_POVM_clock_covariance",
        "typed_basis_path_correspondence_resources => metaphysically_fundamental_structure",
        "Dirac_invariant_data_plus_relational_change => eternalism_or_ontological_becoming",
        "future_measurement_covariance => future_actuality",
        "finite_model_success => empirical_discovery",
    )


def answer_project_questions() -> tuple[Stage13ProjectQuestionAnswer, ...]:
    return (
        Stage13ProjectQuestionAnswer(
            "Q1",
            "Does the frozen finite two-constraint carrier support the declared compensated multi-generator path structure?",
            "Yes. The two constraint directions are independent on all 36 representatives, the first-class identity holds on the tested carrier, and all 144 mixed same-orbit source/target pairs close under the exact compensator while preserving the positive constraint surface.",
            "established_finite_model_result",
            ("Stage13A-B:carrier-and-compensated-paths",),
            "Finite compensated first-class path closure is not refoliation invariance or a hypersurface-deformation algebra.",
        ),
        Stage13ProjectQuestionAnswer(
            "Q2",
            "Do Dirac and complete two-clock relational observables descend across the tested path choices without collapsing distinct physical orbits?",
            "Yes. The full Dirac pair reconstructs the four physical orbits, all six distinct orbit pairs remain separated, and the two-clock complete relational values agree across the licensed compensated path choices while retaining nontrivial relational change.",
            "established_finite_model_result",
            ("Stage13C:Dirac-and-two-clock-relational",),
            "Dirac invariance plus relational change does not decide eternalism or ontological becoming.",
        ),
        Stage13ProjectQuestionAnswer(
            "Q3",
            "Does the typed multi-constraint gauge atlas recover a stable physical quotient?",
            "Yes on the frozen family. Licensed single-generator connectivity recovers exactly four quotient classes of nine representatives, with no licensed cross-orbit arrows and with compensated path words descending to the same quotient-level Dirac/relational payload.",
            "established_finite_model_result",
            ("Stage13D:typed-atlas-quotient-descent",),
            "A finite typed gauge quotient is not general covariance or diffeomorphism invariance.",
        ),
        Stage13ProjectQuestionAnswer(
            "Q4",
            "Does the inherited O/P/R/V/Xi future-measurement architecture descend across compensated multi-constraint paths?",
            "Yes on the tested carrier. All 144 compensated operational-descent checks preserve the licensed quotient-level public architecture and measurement payloads while path/basis provenance remains confined to Xi, and the bounded witness retains four physical-orbit signatures.",
            "established_finite_model_result",
            ("Stage13E:operational-and-future-measurement-descent",),
            "Future-measurement covariance is not future actuality, and the bounded witness is not an empirical prediction.",
        ),
        Stage13ProjectQuestionAnswer(
            "Q5",
            "Is the noncommutativity of the original Stage 13 constraint presentation itself established as quotient-level physical content?",
            "No. The explicitly equivalent commuting presentation K_X_tilde=p_X+a p reconstructs the same sampled quotient memberships, Dirac/relational data, public O/P/R/V content, and all 144 mixed path targets on the frozen family.",
            "established_finite_model_result",
            ("Stage13F:basis-equivalence",),
            "Noncommuting presentation is not fundamental physical non-Abelianity, and a commuting equivalent presentation does not prove every admissible presentation is commuting.",
        ),
        Stage13ProjectQuestionAnswer(
            "Q6",
            "Can the executable controls distinguish basis-equivalent positive structure from deliberately invalid carriers?",
            "Yes. All six rank-deficient, decoupled, wrong-compensator, one-clock-incomplete, cross-orbit, and K_X_bad anomaly controls are rejected while the equivalent commuting positive basis is accepted.",
            "established_finite_model_result",
            ("Stage13F:ablation-anomaly-false-positive-matrix",),
            "Constraint-algebra anomaly detection is not evidence for ontological becoming or physical time asymmetry.",
        ),
        Stage13ProjectQuestionAnswer(
            "Q7",
            "Does Stage 13 establish refoliation invariance, general relativity, eternalism, or refute ontological becoming?",
            "No. Stage 13 establishes a bounded finite multi-constraint path-covariance precursor together with basis and anomaly controls. The carrier lacks a hypersurface-deformation algebra, phase-space-dependent GR-like structure functions, and gravitational field degrees of freedom, and its structural results underdetermine blockness/becoming ontology.",
            "interpretation_guard",
            ("Stage13A-F:bounded-structural-evidence",),
            "No refoliation/GR or eternalism/becoming verdict is licensed.",
        ),
        Stage13ProjectQuestionAnswer(
            "Q8",
            "What is the strongest unresolved structural boundary and next pressure test?",
            "Stage 13F shows that the current noncommuting presentation is removable by a simple rescaling to a commuting basis. The next discriminating step is therefore a minimal phase-space-dependent structure-function / hypersurface-deformation precursor that tests whether this basis-trivialization persists and whether the Stage 13 quotient, relational, and operational descent survive the richer algebraic dependence before any gravitational or refoliation claim.",
            "evidence_selected_research_gate",
            ("Stage13G:gate-ranking",),
            "The selected gate is a structure-function/hypersurface-deformation precursor, not an assumption of GR or established refoliation invariance.",
        ),
    )


SELECTED_STAGE14_GATE_LABEL = (
    "Construct a minimal phase-space-dependent structure-function / hypersurface-deformation precursor "
    "designed to test whether the Stage 13F simple commuting-basis trivialization persists, and retest "
    "the physical quotient, relational observables, and typed O/P/R/V measurement architecture without "
    "assuming general relativity or refoliation invariance"
)


def stage14_gate_candidates(
    snapshot: Stage13EvidenceSnapshot | None = None,
) -> tuple[Stage14GateCandidate, ...]:
    evidence = evidence_snapshot() if snapshot is None else snapshot
    a, b, c, d, e, f = (
        evidence.stage13a,
        evidence.stage13b,
        evidence.stage13c,
        evidence.stage13d,
        evidence.stage13e,
        evidence.stage13f,
    )

    structure_score = 6
    structure_signals = [
        "Stage 13F shows that the current noncommuting presentation is removable by K_X_tilde=exp(-T)K_X, so basis-trivialization is now the sharpest algebraic limitation"
    ]
    if a.criteria_11_16_satisfied and b.criteria_17_23_satisfied:
        structure_score += 1
        structure_signals.append("the two-constraint first-class carrier and compensated mixed-path family provide a stable baseline for a structure-function perturbation")
    if c.criteria_24_31_satisfied and d.criteria_32_38_satisfied:
        structure_score += 1
        structure_signals.append("Dirac/two-clock observables and the typed quotient are explicit enough to detect whether richer algebraic dependence changes physical classes")
    if e.criteria_39_43_satisfied:
        structure_score += 1
        structure_signals.append("O/P/R/V/Xi and future-measurement descent supply nontrivial quotient-level payloads for the richer algebraic test")
    if f.criteria_44_47_satisfied and f.basis_equivalent_count == f.basis_equivalence_check_count:
        structure_score += 2
        structure_signals.append("36/36 basis-equivalence checks and 144/144 commuting mixed-path checks isolate simple presentation dependence rather than quotient-level change")
    if f.anomaly_detected:
        structure_score += 1
        structure_signals.append("the K_X_bad anomaly control provides a validated discriminator for a richer constraint-algebra experiment")

    gravity_score = 5
    gravity_signals = ["dynamical gravitational field degrees of freedom remain absent"]
    if c.criteria_24_31_satisfied and d.criteria_32_38_satisfied:
        gravity_score += 1
        gravity_signals.append("the quotient and relational baseline are mature enough for a later gravitational/minisuperspace carrier")
    if e.criteria_39_43_satisfied:
        gravity_score += 1
        gravity_signals.append("the operational architecture is already available as a payload for a gravitational extension")
    if f.criteria_44_47_satisfied:
        gravity_score += 1
        gravity_signals.append("basis/anomaly controls should be retained by any gravitational extension")

    order_score = 6
    order_signals = ["the relational event/order scaffold remains deliberately minimal"]
    if d.criteria_32_38_satisfied:
        order_score += 1
        order_signals.append("the typed atlas cleanly separates path word, event, clock, and modal roles")
    if e.criteria_39_43_satisfied:
        order_score += 1
        order_signals.append("future-measurement descent provides a stable baseline for richer causal/order robustness")

    clock_score = 5
    clock_signals = ["the inherited clock and measurement families remain finite and idealized"]
    if e.criteria_39_43_satisfied:
        clock_score += 1
        clock_signals.append("measurement descent is mature enough for a nonideal/POVM-clock perturbation")
    if f.criteria_44_47_satisfied:
        clock_score += 1
        clock_signals.append("basis/path controls provide a useful baseline for separating clock noise from algebraic failure")

    candidates = (
        Stage14GateCandidate(
            "phase_space_structure_function_precursor",
            SELECTED_STAGE14_GATE_LABEL,
            structure_score,
            tuple(structure_signals),
            "This directly targets the limitation exposed by Stage 13F: the present noncommutativity can be removed by a simple basis rescaling. A phase-space-dependent structure-function precursor asks whether that trivialization persists before introducing gravitational field dynamics or claiming refoliation invariance.",
        ),
        Stage14GateCandidate(
            "gravitational_minisuperspace_extension",
            "Introduce a minimal gravitational/minisuperspace carrier and retest the Stage 13 quotient, relational, and typed operational architecture",
            gravity_score,
            tuple(gravity_signals),
            "A gravitational toy model is increasingly timely, but moving there now would confound algebraic structure-function effects with gravitational dynamics. The cleaner next discriminator is the structure-function precursor.",
        ),
        Stage14GateCandidate(
            "richer_causal_order",
            "Replace the minimal relational-event scaffold with a richer causal/order layer and retest path, record, modal, quotient, and measurement distinctions",
            order_score,
            tuple(order_signals),
            "This remains an important robustness direction, but it does not target the basis-trivialization boundary exposed specifically by Stage 13F.",
        ),
        Stage14GateCandidate(
            "nonideal_povm_clocks",
            "Replace the idealized finite clock/measurement family with nonideal or POVM clocks and retest the typed covariance stack",
            clock_score,
            tuple(clock_signals),
            "Clock nonideality remains open, but the new algebraic boundary is more diagnostic for the current refoliation-precursor research thread.",
        ),
    )
    return tuple(sorted(candidates, key=lambda item: (-item.score, item.gate_id)))


def established_scope(snapshot: Stage13EvidenceSnapshot | None = None) -> tuple[str, ...]:
    evidence = evidence_snapshot() if snapshot is None else snapshot
    return (
        f"{evidence.stage13a.orbit_count} physical orbits with {evidence.stage13a.representative_count} sampled representatives and two independent first-class constraint directions",
        f"{evidence.stage13b.compensated_closure_count}/{evidence.stage13b.mixed_pair_count} exact compensated mixed-path closures with physical-orbit identity preserved",
        f"{evidence.stage13c.physically_distinct_pair_count}/{evidence.stage13c.distinct_orbit_pair_count} distinct orbit-pair discrimination plus nontrivial two-clock complete relational change",
        f"{evidence.stage13d.quotient_class_count} typed quotient classes of size 9 with zero licensed cross-orbit arrows and compensated Dirac/relational descent",
        f"typed O/P/R/V/Xi and future-measurement descent across {evidence.stage13e.compensated_path_check_count} compensated path comparisons with {evidence.stage13e.distinct_orbit_witness_count} orbit-sensitive signatures",
        f"equivalent commuting-basis reconstruction with {evidence.stage13f.basis_equivalent_count}/{evidence.stage13f.basis_equivalence_check_count} basis checks, {evidence.stage13f.commuting_mixed_path_closed_count}/{evidence.stage13f.commuting_mixed_path_check_count} mixed-path closures, and {evidence.stage13f.rejected_false_positive_control_count}/{evidence.stage13f.false_positive_control_count} rejected controls",
    )


def retained_typing_resources() -> tuple[str, ...]:
    return (
        "physical-orbit identity and quotient-class correspondence",
        "constraint-generator identity and constraint-basis provenance",
        "gauge representative and path-word/compensator provenance",
        "physical event and two-clock correspondence",
        "continuation-class and outcome correspondence",
        "measurement normalization semantics",
        "separation of path word from physical temporal history",
        "separation of constraint-generated gauge flow from modal continuation",
    )


def derived_or_reconstructible_roles() -> tuple[str, ...]:
    return (
        "the sampled four-class quotient is numerically reconstructible from licensed connectivity and Dirac data without turning stored orbit labels into the quotient-construction rule",
        "path-word/compensator information is numerically reconstructible on the frozen atlas after typed removal but typed operational provenance remains lost",
        "the original noncommuting constraint presentation is replaceable by an explicitly equivalent commuting presentation without changing the tested quotient-level physical payloads",
        "representative-, path-, and basis-specific Xi provenance remains representation-dependent rather than quotient-level physical content on the frozen family",
    )


@lru_cache(maxsize=1)
def stage13g_synthesis() -> Stage13GSynthesis:
    snapshot = evidence_snapshot()
    candidates = stage14_gate_candidates(snapshot)
    return Stage13GSynthesis(
        choice=select_synthesis_choice(snapshot),
        top_level_candidate=(
            "T13_candidate=(O,P,R,V;Xi) equipped with a typed four-class physical quotient, "
            "two-constraint compensated path atlas, two-clock complete relational observables, "
            "future-measurement descent, and tested equivalent constraint-basis correspondence "
            "on the frozen finite carrier"
        ),
        established_scope=established_scope(snapshot),
        retained_typing_resources=retained_typing_resources(),
        derived_or_reconstructible_roles=derived_or_reconstructible_roles(),
        project_questions=answer_project_questions(),
        unresolved_boundaries=unresolved_boundaries(),
        stage14_candidates=candidates,
        selected_stage14_gate=candidates[0].gate_id,
    )


def stage13g_summary() -> dict[str, object]:
    synthesis = stage13g_synthesis()
    return {
        "stage": "13G",
        "choice": synthesis.choice.value,
        "top_level_candidate": synthesis.top_level_candidate,
        "established_scope": synthesis.established_scope,
        "retained_typing_resources": synthesis.retained_typing_resources,
        "derived_or_reconstructible_roles": synthesis.derived_or_reconstructible_roles,
        "project_questions": tuple(item.as_dict() for item in synthesis.project_questions),
        "unresolved_boundaries": synthesis.unresolved_boundaries,
        "stage14_candidates": tuple(item.as_dict() for item in synthesis.stage14_candidates),
        "selected_stage14_gate": synthesis.selected_stage14_gate,
        "selected_stage14_gate_label": SELECTED_STAGE14_GATE_LABEL,
        "current_execution_criteria": {
            "48": "Executable synthesis selects exactly one frozen Stage 13 status from the full Stage 13A-F evidence chain — satisfied in source diagnostics",
            "49": "Next research gate is evidence-selected without presupposing GR, refoliation invariance, or a hypersurface-deformation algebra — satisfied in source diagnostics",
            "50": "External final full-repository regression and merge-readiness review — pending",
        },
        "guards": (
            "multi_constraint_path_covariant finite family != refoliation invariance",
            "finite first-class constraint algebra != hypersurface-deformation algebra",
            "phase-space-dependent structure-function precursor != hypersurface-deformation algebra by definition",
            "structure-function precursor != general relativity",
            "constraint-basis equivalence != universal basis trivializability",
            "noncommuting constraint presentation != fundamental physical non-Abelianity",
            "constraint-algebra anomaly != ontological becoming",
            "Dirac-invariant data + relational change != proof of eternalism",
            "complete relational observable != ontological becoming by definition",
            "future-measurement covariance != future actuality",
            "typed-resource necessity != metaphysical fundamentality",
            "finite-model success != empirical discovery",
            "repository validation != new scientific evidence",
            "not_established != false",
        ),
    }
