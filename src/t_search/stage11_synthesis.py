"""Stage 11G synthesis and evidence-selected Stage 12 gate.

Stage 11A--F built and pressure-tested a finite typed parametrized-covariance
precursor.  Stage 11G integrates those diagnostics into one frozen status
choice and ranks the next research gates without presupposing general
covariance.

``parametrized_covariant`` is deliberately bounded: it means that the declared
finite positive external-parameterization family preserves the tested
constraint orbit, relational observables/derivatives, typed O/P/R/V/Xi
architecture, future-measurement probabilities, weighted/modal/evidence-update
outputs, and clock-change x reparameterization product squares, while the
frozen wrong-gauge/false-positive controls are rejected as intended.

It does *not* mean general covariance, diffeomorphism invariance, general
relativity, eternalism, future actuality, or refutation of ontological
becoming.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from functools import lru_cache
from typing import Any

from .stage5_clock_change import DEFAULT_ATOL
from .stage11_ablation import Stage11FDiagnostics, stage11f_diagnostics
from .stage11_compatibility import Stage11EDiagnostics
from .stage11_compatibility_runtime import stage11e_diagnostics
from .stage11_lift import Stage11CDiagnostics, stage11c_diagnostics
from .stage11_measurement import Stage11DDiagnostics, stage11d_diagnostics
from .stage11_parametrized import Stage11ADiagnostics, stage11a_diagnostics
from .stage11_relational import Stage11BDiagnostics, stage11b_diagnostics


class Stage11SynthesisChoice(str, Enum):
    PARAMETRIZED_COVARIANT = "parametrized_covariant"
    PARAMETRIZED_PARTIAL = "parametrized_partial"
    PARAMETRIZED_OBSTRUCTED = "parametrized_obstructed"
    INCONCLUSIVE = "inconclusive"


@dataclass(frozen=True, slots=True)
class Stage11ProjectQuestionAnswer:
    question_id: str
    question: str
    answer: str
    evidence_class: str
    evidence_refs: tuple[str, ...]
    boundary: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class Stage12GateCandidate:
    gate_id: str
    label: str
    score: int
    pressure_signals: tuple[str, ...]
    rationale: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class Stage11EvidenceSnapshot:
    stage11a: Stage11ADiagnostics
    stage11b: Stage11BDiagnostics
    stage11c: Stage11CDiagnostics
    stage11d: Stage11DDiagnostics
    stage11e: Stage11EDiagnostics
    stage11f: Stage11FDiagnostics


@dataclass(frozen=True, slots=True)
class Stage11GSynthesis:
    choice: Stage11SynthesisChoice
    top_level_candidate: str
    established_scope: tuple[str, ...]
    retained_typing_resources: tuple[str, ...]
    derived_or_reconstructible_roles: tuple[str, ...]
    project_questions: tuple[Stage11ProjectQuestionAnswer, ...]
    unresolved_boundaries: tuple[str, ...]
    stage12_candidates: tuple[Stage12GateCandidate, ...]
    selected_stage12_gate: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "choice": self.choice.value,
            "top_level_candidate": self.top_level_candidate,
            "established_scope": list(self.established_scope),
            "retained_typing_resources": list(self.retained_typing_resources),
            "derived_or_reconstructible_roles": list(self.derived_or_reconstructible_roles),
            "project_questions": [item.as_dict() for item in self.project_questions],
            "unresolved_boundaries": list(self.unresolved_boundaries),
            "stage12_candidates": [item.as_dict() for item in self.stage12_candidates],
            "selected_stage12_gate": self.selected_stage12_gate,
        }


@lru_cache(maxsize=1)
def evidence_snapshot() -> Stage11EvidenceSnapshot:
    """Evaluate the completed Stage 11A--F diagnostics once per process."""

    return Stage11EvidenceSnapshot(
        stage11a=stage11a_diagnostics(),
        stage11b=stage11b_diagnostics(),
        stage11c=stage11c_diagnostics(),
        stage11d=stage11d_diagnostics(),
        stage11e=stage11e_diagnostics(),
        stage11f=stage11f_diagnostics(),
    )


def select_synthesis_choice(
    snapshot: Stage11EvidenceSnapshot | None = None,
    *,
    atol: float = DEFAULT_ATOL,
) -> Stage11SynthesisChoice:
    evidence = evidence_snapshot() if snapshot is None else snapshot
    a = evidence.stage11a
    b = evidence.stage11b
    c = evidence.stage11c
    d = evidence.stage11d
    e = evidence.stage11e
    f = evidence.stage11f

    layer_validity = (
        a.criteria_11_16_satisfied,
        b.criteria_17_23_satisfied,
        c.criteria_24_31_satisfied,
        d.criteria_32_38_satisfied,
        e.criteria_39_43_satisfied,
        f.criteria_44_47_satisfied,
    )

    if all(layer_validity):
        return Stage11SynthesisChoice.PARAMETRIZED_COVARIANT

    # Reserve ``obstructed`` for a failure of the declared positive family,
    # rather than for a deliberately wrong/excluded control behaving wrongly.
    explicit_positive_obstruction = bool(
        not a.positive_family_admissible
        or (a.positive_family_admissible and not a.constraint_orbit_preserved)
        or not c.all_positive_architectures_valid
        or d.max_per_continuation_reparameterization_probability_residual > 100 * atol
        or d.minimum_probability < -100 * atol
        or d.maximum_probability > 1.0 + 100 * atol
        or not e.all_reparameterization_transports_valid
        or not e.all_clock_transports_valid
        or e.max_event_path_residual > 100 * atol
        or e.max_measurement_probability_path_residual > 100 * atol
        or e.max_measurement_direct_target_probability_residual > 100 * atol
    )
    if explicit_positive_obstruction:
        return Stage11SynthesisChoice.PARAMETRIZED_OBSTRUCTED

    if any(layer_validity):
        return Stage11SynthesisChoice.PARAMETRIZED_PARTIAL

    return Stage11SynthesisChoice.INCONCLUSIVE


def unresolved_boundaries() -> tuple[str, ...]:
    return (
        "one_frozen_constraint_orbit_reparameterization_covariance => multi_orbit_constraint_generated_gauge_covariance",
        "single_hamiltonian_constraint_precursor => nontrivial_constraint_algebra_or_refoliation_structure",
        "finite_typed_parametrized_covariance => general_covariance",
        "external_parameterization_independence => diffeomorphism_invariance",
        "fixed_background_precursor => dynamical_metric_or_gravitational_clock_structure",
        "minimal_three_event_O => robustness_under_richer_causal_order",
        "ideal_projective_clock_family => nonideal_POVM_clock_covariance",
        "typed_correspondence_resources => metaphysically_fundamental_structure",
        "parameterization_covariant_future_probabilities => eternalism",
        "absence_of_preferred_external_parameterization => absence_of_ontological_becoming",
        "operational_covariance => modal_ontological_identity",
        "finite_model_success => empirical_discovery",
    )


def answer_project_questions() -> tuple[Stage11ProjectQuestionAnswer, ...]:
    return (
        Stage11ProjectQuestionAnswer(
            "Q1",
            "Is one preferred external trajectory parameter required by the tested finite architecture?",
            (
                "No for the frozen positive family. Four admissible external parameterizations preserve the same "
                "sampled constraint orbit, relational q(T) and dq/dT, typed O/P/R/V/Xi content, future-measurement "
                "probabilities, weighted/modal views, and evidence updates when corresponding physical events and "
                "the lapse/Jacobian semantics are carried explicitly."
            ),
            "established_finite_model_result",
            ("Stage11A-B:relational-covariance", "Stage11C-D:typed-measurement-covariance"),
            (
                "This establishes external reparameterization covariance only on the declared finite family and one "
                "sampled constraint orbit; it is not general covariance."
            ),
        ),
        Stage11ProjectQuestionAnswer(
            "Q2",
            "Are external reparameterization and internal-clock change compatible in the tested construction?",
            (
                "Yes. Stage 11E finds the declared G and C product squares path-independent for relational event/O, "
                "per-continuation measurement/probability, weighted/modal, and common-evidence posterior payloads, "
                "while a deliberately untransported wrong clock path is detectably noncommuting."
            ),
            "established_finite_model_result",
            ("Stage11E:typed-product-squares", "Stage11E:wrong-path-control"),
            "A commuting finite typed product diagram is not an interaction law and is not general covariance.",
        ),
        Stage11ProjectQuestionAnswer(
            "Q3",
            "Do the Stage 11 typing resources become redundant when their numerical payload can be reconstructed?",
            (
                "No at the declared operational level. Removing parameter-event correspondence can leave the mapping "
                "numerically reconstructible, and removing lapse semantics can leave dq/dT numerically correct, while "
                "the typed covariance claim becomes not established. A wrong lapse value instead produces an explicit "
                "numerical refutation in the tested construction."
            ),
            "established_finite_model_result",
            ("Stage11F:typed-resource-ablations",),
            "Reconstructibility does not imply universal redundancy, and typed-resource use does not imply metaphysical fundamentality.",
        ),
        Stage11ProjectQuestionAnswer(
            "Q4",
            "Does parametrized covariance establish a block universe or eternalism?",
            (
                "No. The result concerns invariance of typed relational and predictive descriptions under external "
                "reparameterization. It does not convert future probabilities into already-actual events or decide "
                "which events exist simpliciter."
            ),
            "interpretation_guard",
            ("Stage11D-E:future-probability-covariance",),
            "Parameterization-covariant future probabilities are weaker than an ontological claim about future actuality.",
        ),
        Stage11ProjectQuestionAnswer(
            "Q5",
            "Does the absence of a preferred external parameter refute ontological becoming?",
            (
                "No. Stage 11 removes dependence on one external trajectory label inside the tested representation, "
                "but it does not test whether reality contains an objective production, passage, or becoming relation."
            ),
            "interpretation_guard",
            ("Stage11F:interpretation-boundary",),
            "Absence of preferred external parameterization is not absence of ontological becoming.",
        ),
        Stage11ProjectQuestionAnswer(
            "Q6",
            "How should the temporal candidate be updated after Stage 11?",
            (
                "Retain T=(O,P,R,V;Xi) and add the bounded structural fact that its typed external-parameterization "
                "atlas G is compatible with the finite internal-clock atlas C for the tested relational, modal, record, "
                "measurement, weighting, and update interfaces."
            ),
            "candidate_structural_interpretation",
            ("Stage11A-F:integrated-evidence",),
            "This equips the finite candidate with a parametrized-covariance precursor without making G, C, or Xi fundamental or unique.",
        ),
        Stage11ProjectQuestionAnswer(
            "Q7",
            "What is the strongest unresolved structural boundary after Stage 11?",
            (
                "Stage 11 tests four representations of one frozen sampled constraint orbit. It does not yet separate "
                "constraint-generated gauge motion from physically distinct orbits across a family of initial data, "
                "nor does it construct a nontrivial constraint algebra, refoliation structure, or dynamical metric."
            ),
            "untested_not_established",
            ("Stage11G:remaining-gates",),
            "General covariance remains open; not established is not false.",
        ),
        Stage11ProjectQuestionAnswer(
            "Q8",
            "Which next pressure test is selected?",
            (
                "A multi-orbit constraint-generated gauge atlas is selected. The next test should distinguish "
                "gauge-related representations from physically distinct constraint orbits and ask whether relational "
                "Dirac-type observables plus the typed O/P/R/V measurement architecture descend consistently across "
                "that atlas before any direct gravitational extension."
            ),
            "evidence_selected_research_gate",
            ("Stage11G:gate-ranking",),
            (
                "This is a gauge-structure precursor, not general relativity. It changes the one-orbit assumption before "
                "introducing a dynamical metric or claiming general covariance."
            ),
        ),
    )


SELECTED_STAGE12_GATE_LABEL = (
    "Construct a multi-orbit constraint-generated gauge atlas that separates gauge-related parameterizations "
    "from physically distinct orbits and tests whether relational/Dirac observables and the typed O/P/R/V "
    "measurement architecture descend consistently across that atlas"
)


def stage12_gate_candidates(
    snapshot: Stage11EvidenceSnapshot | None = None,
) -> tuple[Stage12GateCandidate, ...]:
    evidence = evidence_snapshot() if snapshot is None else snapshot
    a, b, c, d, e, f = (
        evidence.stage11a,
        evidence.stage11b,
        evidence.stage11c,
        evidence.stage11d,
        evidence.stage11e,
        evidence.stage11f,
    )

    gauge_score = 5
    gauge_signals = [
        "Stage 11 still represents one frozen sampled constraint orbit, so gauge-related versus physically distinct orbit structure remains untested"
    ]
    if a.criteria_11_16_satisfied:
        gauge_score += 1
        gauge_signals.append("the positive reparameterization family preserves the frozen constraint orbit")
    if b.criteria_17_23_satisfied:
        gauge_score += 1
        gauge_signals.append("relational q(T) and dq/dT are already available as observables to carry across multiple orbits")
    if d.criteria_32_38_satisfied:
        gauge_score += 1
        gauge_signals.append("the typed future-measurement family survives external reparameterization")
    if e.criteria_39_43_satisfied:
        gauge_score += 1
        gauge_signals.append("external-parameterization and internal-clock transports commute on the frozen finite product family")
    if f.criteria_44_47_satisfied:
        gauge_score += 1
        gauge_signals.append("ablation controls identify event and lapse/Jacobian typing resources that a genuine gauge atlas must preserve")

    order_score = 6
    order_signals = ["O remains a deliberately minimal three-event/order skeleton"]
    if c.criteria_24_31_satisfied:
        order_score += 1
        order_signals.append("the typed O/P/R/V lift is stable enough that richer causal order is now a clean independent robustness test")

    clock_score = 5
    clock_signals = [
        "the internal A/B/C clock family remains ideal/projective and finite",
        "the transported measurement normalization is already nontrivial",
    ]
    if d.criteria_32_38_satisfied and e.criteria_39_43_satisfied:
        clock_score += 1
        clock_signals.append("measurement and clock-change covariance provide a mature baseline for nonideal/POVM-clock perturbations")

    gravity_score = 3
    gravity_signals = [
        "Stage 11 is a parametrized precursor and does not contain a dynamical metric, refoliation algebra, or gravitational clock degrees of freedom"
    ]
    if a.criteria_11_16_satisfied:
        gravity_score += 1
        gravity_signals.append("the single-constraint parametrized scaffold is now stable enough to motivate, but not yet justify, a gravitational model")
    if e.criteria_39_43_satisfied:
        gravity_score += 1
        gravity_signals.append("clock x reparameterization compatibility closes one prerequisite without closing the general-covariance gap")

    candidates = (
        Stage12GateCandidate(
            "multi_orbit_constraint_gauge_atlas",
            SELECTED_STAGE12_GATE_LABEL,
            gauge_score,
            tuple(gauge_signals),
            (
                "This changes the strongest remaining assumption one step at a time. Stage 11 shows covariance for "
                "several labels of one orbit; the next discriminating question is whether a family of constraint "
                "orbits admits a typed gauge atlas that separates gauge redundancy from physical initial-data "
                "differences. Success would be a stronger precursor to generally covariant systems without assuming GR."
            ),
        ),
        Stage12GateCandidate(
            "richer_causal_order",
            "Replace the minimal three-event O layer with richer causal/order structure",
            order_score,
            tuple(order_signals),
            (
                "The minimal O layer remains a live robustness boundary. It is ranked below the gauge-atlas test because "
                "Stage 11 specifically exposes one-orbit gauge structure as the nearest unresolved assumption."
            ),
        ),
        Stage12GateCandidate(
            "nonideal_povm_clocks",
            "Test interacting nonideal and POVM clock perspectives with the typed parametrized measurement family",
            clock_score,
            tuple(clock_signals),
            (
                "This is a valuable operational robustness test, but it perturbs the clock model rather than the "
                "one-orbit gauge boundary isolated by Stage 11."
            ),
        ),
        Stage12GateCandidate(
            "gravitational_minisuperspace_extension",
            "Attempt a minimal gravitational/minisuperspace extension with dynamical clock geometry",
            gravity_score,
            tuple(gravity_signals),
            (
                "A gravitational model is intentionally ranked below the intermediate gauge-atlas test. Stage 11 does "
                "not yet provide a multi-orbit gauge separation, nontrivial constraint algebra, refoliation structure, "
                "or dynamical metric, so jumping directly to GR would conflate several new assumptions."
            ),
        ),
    )
    return tuple(sorted(candidates, key=lambda item: (-item.score, item.gate_id)))


def stage11g_synthesis() -> Stage11GSynthesis:
    snapshot = evidence_snapshot()
    choice = select_synthesis_choice(snapshot)
    candidates = stage12_gate_candidates(snapshot)
    return Stage11GSynthesis(
        choice=choice,
        top_level_candidate=(
            "T11_candidate=(O,P,R,V;Xi) equipped with a finite typed external reparameterization atlas G "
            "compatible with the continuation-aware internal-clock atlas C"
        ),
        established_scope=(
            "4 admissible external parameterizations of 13 corresponding physical events on one sampled constraint orbit",
            "52 relational-observable and 52 relational-derivative evaluations with nonlinear raw-rate variation",
            "typed O/P/R/V/Xi lift with selector-free public schema and explicit event/lapse/class/outcome semantics",
            "8 typed future-measurement views and 16 canonical outcome evaluations with reparameterization-covariant probabilities",
            "648 event/O, 1296 measurement/probability, 648 weighted/modal, and 648 posterior clock x reparameterization squares",
            "Stage 11F separation of reconstructible, not-established, and numerically-refuted resource ablations plus 7/7 false-positive controls",
        ),
        retained_typing_resources=(
            "physical event correspondence",
            "lapse/Jacobian transformation semantics",
            "continuation-class correspondence",
            "outcome correspondence",
            "measurement normalization semantics",
            "continuation-weight/class alignment",
            "separation of external parameterization identity from internal clock perspective",
        ),
        derived_or_reconstructible_roles=(
            "parameter-event mapping can be numerically reconstructed from retained O in the tested ablation without restoring typed identity",
            "dq/dT can remain numerically reconstructible when lapse transformation semantics are removed without establishing typed covariance",
            "raw external parameter labels and raw rates are representation-dependent and do not define physical event identity",
        ),
        project_questions=answer_project_questions(),
        unresolved_boundaries=unresolved_boundaries(),
        stage12_candidates=candidates,
        selected_stage12_gate=candidates[0].gate_id,
    )


def stage11g_summary() -> dict[str, object]:
    synthesis = stage11g_synthesis()
    return {
        "stage": "11G",
        "synthesis": synthesis.as_dict(),
        "current_execution_criteria": {
            "48": "derive exactly one frozen Stage 11 status from executable Stage 11A-F evidence",
            "49": "rank unresolved Stage 12 gates and uniquely select the next evidence-driven pressure test without presupposing general covariance",
            "50": "external final full-repository regression and merge-readiness review",
        },
        "guards": (
            "parametrized_covariant finite family != general covariance",
            "external parameterization independence != diffeomorphism invariance",
            "one-orbit covariance != multi-orbit gauge covariance",
            "constraint-generated gauge precursor != general relativity",
            "absence of preferred external parameterization != absence of ontological becoming",
            "parameterization-covariant future probabilities != future actuality",
            "parameterization-covariant future probabilities != proof of eternalism",
            "numerical reconstructibility != typed operational identification",
            "typed-resource necessity != metaphysical fundamentality",
            "finite-model success != empirical discovery",
            "repository validation != new scientific evidence",
        ),
    }
