"""Stage 12G executable synthesis and evidence-selected Stage 13 gate.

Stage 12A--F build and pressure-test a finite typed multi-orbit constraint-
generated gauge atlas.  Stage 12G integrates those diagnostics into exactly
one frozen Stage 12 status and ranks the next research gates without promoting
the result to general covariance or general relativity.

``multi_orbit_gauge_covariant`` is deliberately bounded.  It means that on the
declared four-orbit finite family, same-orbit constraint-generated gauge
representatives form the tested quotient structure; distinct physical orbits
are not collapsed; relational/Dirac and typed O/P/R/V measurement content
descend as declared; the bounded orbit-sensitive witness remains distinct
across the four physical orbits; C x G x Phi compatibility holds on the tested
families; and frozen false-positive controls are rejected.

It does not mean diffeomorphism invariance, refoliation invariance, general
covariance, general relativity, eternalism, future actuality, or refutation of
ontological becoming.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from functools import lru_cache
from typing import Any

from .stage12_ablation import Stage12FDiagnostics, stage12f_diagnostics
from .stage12_compatibility import Stage12EDiagnostics, stage12e_diagnostics
from .stage12_gauge_atlas import Stage12CDiagnostics, stage12c_diagnostics
from .stage12_measurement import Stage12DDiagnostics, stage12d_diagnostics
from .stage12_multi_orbit import Stage12ADiagnostics, stage12a_diagnostics
from .stage12_relational import Stage12BDiagnostics, stage12b_diagnostics


class Stage12SynthesisChoice(str, Enum):
    MULTI_ORBIT_GAUGE_COVARIANT = "multi_orbit_gauge_covariant"
    MULTI_ORBIT_GAUGE_PARTIAL = "multi_orbit_gauge_partial"
    MULTI_ORBIT_GAUGE_OBSTRUCTED = "multi_orbit_gauge_obstructed"
    INCONCLUSIVE = "inconclusive"


@dataclass(frozen=True, slots=True)
class Stage12ProjectQuestionAnswer:
    question_id: str
    question: str
    answer: str
    evidence_class: str
    evidence_refs: tuple[str, ...]
    boundary: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class Stage13GateCandidate:
    gate_id: str
    label: str
    score: int
    pressure_signals: tuple[str, ...]
    rationale: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class Stage12EvidenceSnapshot:
    stage12a: Stage12ADiagnostics
    stage12b: Stage12BDiagnostics
    stage12c: Stage12CDiagnostics
    stage12d: Stage12DDiagnostics
    stage12e: Stage12EDiagnostics
    stage12f: Stage12FDiagnostics


@dataclass(frozen=True, slots=True)
class Stage12GSynthesis:
    choice: Stage12SynthesisChoice
    top_level_candidate: str
    established_scope: tuple[str, ...]
    retained_typing_resources: tuple[str, ...]
    derived_or_reconstructible_roles: tuple[str, ...]
    project_questions: tuple[Stage12ProjectQuestionAnswer, ...]
    unresolved_boundaries: tuple[str, ...]
    stage13_candidates: tuple[Stage13GateCandidate, ...]
    selected_stage13_gate: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "choice": self.choice.value,
            "top_level_candidate": self.top_level_candidate,
            "established_scope": list(self.established_scope),
            "retained_typing_resources": list(self.retained_typing_resources),
            "derived_or_reconstructible_roles": list(self.derived_or_reconstructible_roles),
            "project_questions": [item.as_dict() for item in self.project_questions],
            "unresolved_boundaries": list(self.unresolved_boundaries),
            "stage13_candidates": [item.as_dict() for item in self.stage13_candidates],
            "selected_stage13_gate": self.selected_stage13_gate,
        }


@lru_cache(maxsize=1)
def evidence_snapshot() -> Stage12EvidenceSnapshot:
    """Evaluate the completed Stage 12A--F diagnostics once per process."""

    return Stage12EvidenceSnapshot(
        stage12a=stage12a_diagnostics(),
        stage12b=stage12b_diagnostics(),
        stage12c=stage12c_diagnostics(),
        stage12d=stage12d_diagnostics(),
        stage12e=stage12e_diagnostics(),
        stage12f=stage12f_diagnostics(),
    )


def _layer_validity(snapshot: Stage12EvidenceSnapshot) -> tuple[bool, ...]:
    return (
        snapshot.stage12a.criteria_11_16_satisfied,
        snapshot.stage12b.criteria_17_23_satisfied,
        snapshot.stage12c.criteria_24_31_satisfied,
        snapshot.stage12d.criteria_32_38_satisfied,
        snapshot.stage12e.criteria_39_43_satisfied,
        snapshot.stage12f.criteria_44_47_satisfied,
    )


def select_synthesis_choice(
    snapshot: Stage12EvidenceSnapshot | None = None,
) -> Stage12SynthesisChoice:
    evidence = evidence_snapshot() if snapshot is None else snapshot
    a, b, c, d, e, f = (
        evidence.stage12a,
        evidence.stage12b,
        evidence.stage12c,
        evidence.stage12d,
        evidence.stage12e,
        evidence.stage12f,
    )
    validity = _layer_validity(evidence)

    if all(validity):
        return Stage12SynthesisChoice.MULTI_ORBIT_GAUGE_COVARIANT

    # ``obstructed`` is reserved for an explicit positive-family failure.  A
    # deliberately wrong control behaving correctly is not an obstruction.
    explicit_positive_obstruction = bool(
        not a.canonical_orbits_distinct
        or not a.gauge_representatives_complete
        or not a.gauge_invariants_preserved
        or not a.external_parameterization_family_complete
        or not b.distinct_orbits_not_collapsed
        or not c.quotient_partition_exact
        or c.cross_orbit_gauge_arrow_count > 0
        or not d.all_positive_architectures_valid
        or d.distinct_orbit_signature_count < 4
        or e.max_clock_gauge_residual > 1e-8
        or e.max_reparameterization_gauge_residual > 1e-8
        or e.max_triple_residual > 1e-8
    )
    if explicit_positive_obstruction:
        return Stage12SynthesisChoice.MULTI_ORBIT_GAUGE_OBSTRUCTED

    if any(validity):
        return Stage12SynthesisChoice.MULTI_ORBIT_GAUGE_PARTIAL

    return Stage12SynthesisChoice.INCONCLUSIVE


def unresolved_boundaries() -> tuple[str, ...]:
    return (
        "single_hamiltonian_constraint => nontrivial_multi_constraint_algebra",
        "finite_multi_orbit_gauge_covariance => general_covariance",
        "finite_constraint_generated_gauge_atlas => diffeomorphism_invariance",
        "finite_C_x_G_x_Phi_compatibility => refoliation_invariance",
        "fixed_free_particle_constraint => dynamical_metric_or_gravitational_clock_structure",
        "finite_orbit_sensitive_measurement_bridge => independent_dynamical_or_empirical_measurement_law",
        "minimal_relational_event_order => robustness_under_richer_causal_order",
        "ideal_projective_clock_family => nonideal_POVM_clock_covariance",
        "typed_correspondence_resources => metaphysically_fundamental_structure",
        "Dirac_invariant_orbit_data_plus_relational_change => eternalism_or_ontological_becoming",
        "path_independent_future_probabilities => future_actuality",
        "finite_model_success => empirical_discovery",
    )


def answer_project_questions() -> tuple[Stage12ProjectQuestionAnswer, ...]:
    return (
        Stage12ProjectQuestionAnswer(
            "Q1",
            "Can same-orbit constraint-generated gauge representatives be quotiented in the tested finite family?",
            "Yes. The sampled same-orbit Phi groupoid closes and its connected components recover four quotient classes of five representatives without licensed cross-orbit gauge arrows.",
            "established_finite_model_result",
            ("Stage12A-C:gauge-atlas-and-quotient",),
            "A finite sampled gauge quotient is not diffeomorphism invariance or general covariance.",
        ),
        Stage12ProjectQuestionAnswer(
            "Q2",
            "Are physically distinct canonical orbits collapsed by weak labels or a single Dirac invariant?",
            "No. The full Dirac pair distinguishes all six canonical orbit pairs, including same-P/different-Q and same-Q/different-P controls, while equal-T, equal-q, and equal-raw-label coincidences are rejected.",
            "established_finite_model_result",
            ("Stage12B:physical-orbit-discrimination", "Stage12F:false-positive-matrix"),
            "Full-Dirac-pair discrimination is established only for the frozen finite family, not as a universal orbit-classification theorem.",
        ),
        Stage12ProjectQuestionAnswer(
            "Q3",
            "Does quotienting gauge representatives eliminate relational change?",
            "No in the tested construction. Q_D and P_D descend as orbit data while q(T=tau)=Q_D+P_D tau and dq/dT=P_D remain nontrivial relational observables on the quotient classes.",
            "established_finite_model_result",
            ("Stage12B-C:Dirac-relational-descent",),
            "Gauge quotienting does not by itself decide whether physical change is ontological becoming.",
        ),
        Stage12ProjectQuestionAnswer(
            "Q4",
            "Does the typed O/P/R/V future-measurement architecture descend over the gauge atlas?",
            "Yes on the frozen family. Same-orbit representatives agree on quotient-level typed architecture and inherited measurement outputs, while a declared bounded witness retains four distinct physical-orbit signatures.",
            "established_finite_model_result",
            ("Stage12D:typed-measurement-descent",),
            "The orbit-sensitive bridge is diagnostic, not a derivation of quantum measurement from the classical constraint and not an empirical prediction.",
        ),
        Stage12ProjectQuestionAnswer(
            "Q5",
            "Are internal-clock, external-reparameterization, and gauge transports compatible in the tested construction?",
            "Yes. Stage 12E finds the declared C x Phi, G x Phi, and spanning C x G x Phi path families compatible while mixed-orbit and untyped paths are rejected.",
            "established_finite_model_result",
            ("Stage12E:three-way-compatibility",),
            "Finite commuting typed diagrams are not refoliation invariance, diffeomorphism invariance, or general covariance.",
        ),
        Stage12ProjectQuestionAnswer(
            "Q6",
            "Do orbit/correspondence typing resources become redundant when numerical classes can be reconstructed?",
            "No at the declared operational level. Stage 12F keeps numerical reconstructibility, typed identification, and covariance status separate; representative-dependent O/P/R/V/measurement corruptions and orbit-insensitive trivialization remain detectable.",
            "established_finite_model_result",
            ("Stage12F:ablation-and-false-positive-matrix",),
            "Reconstructibility does not imply universal redundancy, and typed-resource use does not imply metaphysical fundamentality.",
        ),
        Stage12ProjectQuestionAnswer(
            "Q7",
            "Does Stage 12 establish eternalism, a block universe, or refute ontological becoming?",
            "No. The finite model supports invariant orbit data, representative redundancy, physical-orbit plurality, and nontrivial relational change simultaneously, but these structural facts do not determine which events exist simpliciter or whether reality objectively becomes.",
            "interpretation_guard",
            ("Stage12B-F:bounded-structural-evidence",),
            "Dirac invariance plus relational change is compatible with multiple ontological interpretations; no eternalism/becoming verdict is licensed.",
        ),
        Stage12ProjectQuestionAnswer(
            "Q8",
            "What is the strongest unresolved structural boundary and next pressure test?",
            "The carrier still has a single Hamiltonian constraint. The next discriminating step is a minimal multi-constraint constraint-algebra/refoliation precursor that tests whether the Stage 12 quotient, relational observables, and typed measurement architecture survive nontrivial relations among constraint-generated gauge directions before any claim of general covariance or GR.",
            "evidence_selected_research_gate",
            ("Stage12G:gate-ranking",),
            "This is a constraint-algebra/refoliation precursor, not general relativity and not established refoliation invariance.",
        ),
    )


SELECTED_STAGE13_GATE_LABEL = (
    "Construct a minimal multi-constraint constraint-algebra/refoliation precursor with at least two "
    "nontrivially related first-class constraint directions, and test whether the Stage 12 physical-orbit "
    "quotient, relational observables, and typed O/P/R/V measurement architecture remain compatible under "
    "the resulting constraint-generated path structure without assuming general relativity"
)


def stage13_gate_candidates(
    snapshot: Stage12EvidenceSnapshot | None = None,
) -> tuple[Stage13GateCandidate, ...]:
    evidence = evidence_snapshot() if snapshot is None else snapshot
    a, b, c, d, e, f = (
        evidence.stage12a,
        evidence.stage12b,
        evidence.stage12c,
        evidence.stage12d,
        evidence.stage12e,
        evidence.stage12f,
    )

    algebra_score = 5
    algebra_signals = [
        "Stage 12 still uses one Hamiltonian constraint, so nontrivial relations among multiple constraint-generated gauge directions remain untested"
    ]
    if a.criteria_11_16_satisfied and b.criteria_17_23_satisfied:
        algebra_score += 1
        algebra_signals.append("a stable multi-orbit constrained carrier and relational/Dirac observables now provide the baseline for a multi-constraint perturbation")
    if c.criteria_24_31_satisfied:
        algebra_score += 1
        algebra_signals.append("the typed gauge groupoid and quotient are explicit enough to test whether a richer constraint algebra changes equivalence classes")
    if d.criteria_32_38_satisfied:
        algebra_score += 1
        algebra_signals.append("typed O/P/R/V measurement descent is available as a nontrivial payload to transport across richer gauge paths")
    if e.criteria_39_43_satisfied:
        algebra_score += 1
        algebra_signals.append("C x G x Phi compatibility closes the one-gauge-direction precursor but not refoliation or a nontrivial constraint algebra")
    if f.criteria_44_47_satisfied:
        algebra_score += 1
        algebra_signals.append("wrong-orbit and false-positive controls are mature enough to distinguish true algebraic obstruction from deliberately invalid paths")

    gravity_score = 4
    gravity_signals = [
        "a dynamical metric and gravitational clock structure remain absent"
    ]
    if c.criteria_24_31_satisfied and e.criteria_39_43_satisfied:
        gravity_score += 2
        gravity_signals.append("multi-orbit gauge quotient and three-way compatibility make a gravitational toy model more timely than after Stage 11")
    if f.criteria_44_47_satisfied:
        gravity_score += 1
        gravity_signals.append("the ablation matrix supplies controls that a gravitational extension should preserve")

    order_score = 6
    order_signals = ["the relational event/order scaffold remains deliberately minimal"]
    if d.criteria_32_38_satisfied:
        order_score += 1
        order_signals.append("the typed measurement architecture is stable enough for a richer causal-order robustness test")

    clock_score = 5
    clock_signals = ["the A/B/C clock family remains ideal/projective and finite"]
    if d.criteria_32_38_satisfied and e.criteria_39_43_satisfied:
        clock_score += 1
        clock_signals.append("measurement descent and C x G x Phi compatibility provide a mature baseline for nonideal/POVM-clock perturbations")

    candidates = (
        Stage13GateCandidate(
            "multi_constraint_refoliation_precursor",
            SELECTED_STAGE13_GATE_LABEL,
            algebra_score,
            tuple(algebra_signals),
            "This changes the strongest remaining structural assumption one step at a time: Stage 12 has multiple physical orbits but only one Hamiltonian constraint direction. A minimal nontrivial constraint algebra is therefore a cleaner next test than jumping directly to a dynamical spacetime theory.",
        ),
        Stage13GateCandidate(
            "gravitational_minisuperspace_extension",
            "Introduce a minimal gravitational/minisuperspace carrier with dynamical geometric degrees of freedom and test the inherited typed architecture",
            gravity_score,
            tuple(gravity_signals),
            "Stage 12 substantially strengthens the case for a gravitational toy model, but it still does not isolate whether failure would come from gravity or merely from adding a nontrivial constraint algebra; therefore this remains below the algebra precursor.",
        ),
        Stage13GateCandidate(
            "richer_causal_order",
            "Replace the minimal relational-event skeleton with a richer causal/order family and retest records, Potentiality, quotient descent, and measurements",
            order_score,
            tuple(order_signals),
            "This remains a clean robustness direction, but it does not target the newly exposed single-constraint boundary as directly as the selected gate.",
        ),
        Stage13GateCandidate(
            "nonideal_povm_clocks",
            "Replace ideal/projective clocks with a finite nonideal/POVM clock family and retest the typed covariance stack",
            clock_score,
            tuple(clock_signals),
            "Clock idealization remains important, but the single-constraint algebra gap is structurally prior to claiming a stronger gauge/refoliation result.",
        ),
    )
    return tuple(sorted(candidates, key=lambda item: (-item.score, item.gate_id)))


def established_scope(snapshot: Stage12EvidenceSnapshot | None = None) -> tuple[str, ...]:
    evidence = evidence_snapshot() if snapshot is None else snapshot
    return (
        f"{evidence.stage12a.physical_orbit_count if hasattr(evidence.stage12a, 'physical_orbit_count') else evidence.stage12a.orbit_count} canonical physical orbits with 20 sampled gauge representatives",
        "full-Dirac-pair discrimination with nontrivial q(T=tau) and dq/dT relational change",
        "100-arrow finite same-orbit gauge groupoid and 4 quotient classes of size 5",
        "typed O/P/R/V/Xi and inherited future-measurement descent with 4 orbit-sensitive signatures",
        "C x Phi, G x Phi, and spanning C x G x Phi finite path compatibility",
        "2 typed-resource ablations and 27/27 rejected false-positive controls",
    )


def retained_typing_resources() -> tuple[str, ...]:
    return (
        "physical-orbit identity and quotient-class correspondence",
        "constraint-generated gauge representative and Phi provenance",
        "physical event correspondence",
        "external parameterization identity and lapse/Jacobian semantics",
        "internal-clock perspective and readout correspondence",
        "continuation-class and outcome correspondence",
        "measurement normalization semantics",
        "separation of constraint orbit from modal continuation",
    )


def derived_or_reconstructible_roles() -> tuple[str, ...]:
    return (
        "the finite four-class orbit partition is numerically reconstructible from the full Dirac pair after typed orbit labels are removed, without restoring typed identity",
        "representative-specific q values are reduced to quotient-level relational content through Q_D and P_D while relational q(T=tau) remains tau-dependent",
        "representative-specific gauge metadata remain representation-dependent Xi provenance and do not become quotient-level physical content",
    )


@lru_cache(maxsize=1)
def stage12g_synthesis() -> Stage12GSynthesis:
    snapshot = evidence_snapshot()
    candidates = stage13_gate_candidates(snapshot)
    return Stage12GSynthesis(
        choice=select_synthesis_choice(snapshot),
        top_level_candidate=(
            "T12_candidate=(O,P,R,V;Xi) equipped with typed physical-orbit quotient Q_Phi "
            "and separately typed C, G, Phi transport families on the frozen finite carrier"
        ),
        established_scope=established_scope(snapshot),
        retained_typing_resources=retained_typing_resources(),
        derived_or_reconstructible_roles=derived_or_reconstructible_roles(),
        project_questions=answer_project_questions(),
        unresolved_boundaries=unresolved_boundaries(),
        stage13_candidates=candidates,
        selected_stage13_gate=candidates[0].gate_id,
    )


def stage12g_summary() -> dict[str, object]:
    synthesis = stage12g_synthesis()
    return {
        "stage": "12G",
        "choice": synthesis.choice.value,
        "top_level_candidate": synthesis.top_level_candidate,
        "established_scope": synthesis.established_scope,
        "retained_typing_resources": synthesis.retained_typing_resources,
        "derived_or_reconstructible_roles": synthesis.derived_or_reconstructible_roles,
        "project_questions": tuple(item.as_dict() for item in synthesis.project_questions),
        "unresolved_boundaries": synthesis.unresolved_boundaries,
        "stage13_candidates": tuple(item.as_dict() for item in synthesis.stage13_candidates),
        "selected_stage13_gate": synthesis.selected_stage13_gate,
        "selected_stage13_gate_label": SELECTED_STAGE13_GATE_LABEL,
        "current_execution_criteria": {
            "48": "Executable synthesis selects exactly one frozen Stage 12 status from the full Stage 12A-F evidence chain — satisfied",
            "49": "Next research gate is evidence-selected without presupposing GR or general covariance — satisfied",
            "50": "External final full-repository regression and merge-readiness review — pending",
        },
        "guards": (
            "multi_orbit_gauge_covariant finite family != general covariance",
            "finite constraint-generated gauge atlas != diffeomorphism invariance",
            "finite C x G x Phi compatibility != refoliation invariance",
            "single Hamiltonian constraint != hypersurface-deformation algebra",
            "constraint-algebra/refoliation precursor != general relativity",
            "Dirac-invariant data + relational change != proof of eternalism",
            "relational change != ontological becoming by definition",
            "path-independent future probabilities != future actuality",
            "typed-resource necessity != metaphysical fundamentality",
            "finite-model success != empirical discovery",
            "repository validation != new scientific evidence",
            "not_established != false",
        ),
    }
