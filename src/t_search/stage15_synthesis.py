"""Stage 15G executable synthesis and evidence-selected Stage 16 gate.

Stage 15A--F establish a bounded finite spatially indexed first-class carrier,
exact local/smeared compensated paths, a four-class Dirac/relational quotient,
a typed O/P/R/V/Xi operational descent, an explicit one-step L1 Abelianizing
basis, and destructive controls that reject the frozen false positives.

The synthesis therefore selects exactly the frozen status
``spatial_local_path_covariant_local_abelianizable``.  The strongest unresolved
pressure is not whether the open three-site chain can be locally Abelianized --
it can -- but whether that success depends on its acyclic/terminal-seed
triangular structure.  The evidence-selected Stage 16 gate is consequently a
minimal four-site closed-cycle precursor, where one-step L1 locality remains
nontrivial but no terminal seed generator is available for the Stage 15 tail
peeling argument.

This is a finite structural research gate.  It does not assume general
relativity, a hypersurface-deformation algebra, refoliation invariance, causal
locality, eternalism, ontological becoming, or future actuality.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from functools import lru_cache
from typing import Any

from .stage15_basis import stage15d_diagnostics
from .stage15_controls import stage15f_diagnostics
from .stage15_local import stage15a_diagnostics
from .stage15_measurement import stage15e_diagnostics
from .stage15_paths import stage15b_diagnostics
from .stage15_relational import stage15c_diagnostics


class Stage15SynthesisChoice(str, Enum):
    SPATIAL_LOCAL_PATH_COVARIANT_LOCAL_ABELIANIZABLE = (
        "spatial_local_path_covariant_local_abelianizable"
    )
    SPATIAL_LOCAL_PATH_COVARIANT_LOCALITY_OBSTRUCTED = (
        "spatial_local_path_covariant_locality_obstructed"
    )
    SPATIAL_LOCAL_PATH_COVARIANT_BASIS_INCONCLUSIVE = (
        "spatial_local_path_covariant_basis_inconclusive"
    )
    SPATIAL_LOCAL_PATH_PARTIAL = "spatial_local_path_partial"
    SPATIAL_LOCAL_PATH_OBSTRUCTED = "spatial_local_path_obstructed"
    INCONCLUSIVE = "inconclusive"


@dataclass(frozen=True, slots=True)
class Stage15EvidenceSnapshot:
    stage15a: Any
    stage15b: Any
    stage15c: Any
    stage15d: Any
    stage15e: Any
    stage15f: Any


@dataclass(frozen=True, slots=True)
class Stage15ProjectQuestionAnswer:
    question_id: str
    question: str
    answer: str
    evidence_class: str
    evidence_refs: tuple[str, ...]
    boundary: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class Stage16GateCandidate:
    gate_id: str
    label: str
    score: int
    pressure_signals: tuple[str, ...]
    rationale: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class Stage15GSynthesis:
    choice: Stage15SynthesisChoice
    top_level_candidate: str
    established_scope: tuple[str, ...]
    basis_pressure_result: tuple[str, ...]
    retained_typing_resources: tuple[str, ...]
    project_questions: tuple[Stage15ProjectQuestionAnswer, ...]
    unresolved_boundaries: tuple[str, ...]
    stage16_candidates: tuple[Stage16GateCandidate, ...]
    selected_stage16_gate: str
    criteria_48_49_satisfied: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "choice": self.choice.value,
            "top_level_candidate": self.top_level_candidate,
            "established_scope": list(self.established_scope),
            "basis_pressure_result": list(self.basis_pressure_result),
            "retained_typing_resources": list(self.retained_typing_resources),
            "project_questions": [item.as_dict() for item in self.project_questions],
            "unresolved_boundaries": list(self.unresolved_boundaries),
            "stage16_candidates": [item.as_dict() for item in self.stage16_candidates],
            "selected_stage16_gate": self.selected_stage16_gate,
            "criteria_48_49_satisfied": self.criteria_48_49_satisfied,
        }


@lru_cache(maxsize=1)
def evidence_snapshot() -> Stage15EvidenceSnapshot:
    return Stage15EvidenceSnapshot(
        stage15a=stage15a_diagnostics(),
        stage15b=stage15b_diagnostics(),
        stage15c=stage15c_diagnostics(),
        stage15d=stage15d_diagnostics(),
        stage15e=stage15e_diagnostics(),
        stage15f=stage15f_diagnostics(),
    )


def select_synthesis_choice(
    snapshot: Stage15EvidenceSnapshot | None = None,
) -> Stage15SynthesisChoice:
    evidence = evidence_snapshot() if snapshot is None else snapshot
    a, b, c, d, e, f = (
        evidence.stage15a,
        evidence.stage15b,
        evidence.stage15c,
        evidence.stage15d,
        evidence.stage15e,
        evidence.stage15f,
    )

    core = (
        a.criteria_11_17_satisfied,
        b.criteria_18_24_satisfied,
        c.criteria_25_31_satisfied,
        e.criteria_39_43_satisfied,
        f.criteria_44_47_satisfied,
    )

    explicit_obstruction = bool(
        not a.first_class_local_closure_established
        or not b.local_compensated_path_closure_established
        or not b.smeared_compensated_path_closure_established
        or not c.quotient_exactly_four_by_twenty_seven
        or not c.local_path_relational_descent_established
        or not c.smeared_path_relational_descent_established
        or not e.same_orbit_descent
        or not e.local_path_descent
        or not e.smeared_path_descent
        or not f.all_controls_rejected
    )
    if explicit_obstruction:
        return Stage15SynthesisChoice.SPATIAL_LOCAL_PATH_OBSTRUCTED

    if all(core):
        if (
            d.criteria_32_38_satisfied
            and d.local_abelianization_established
            and d.classification == "local_abelianization_persists"
        ):
            return Stage15SynthesisChoice.SPATIAL_LOCAL_PATH_COVARIANT_LOCAL_ABELIANIZABLE
        if d.criteria_32_38_satisfied and d.classification in {
            "L1_obstructed_but_Lfinite_abelianizable",
            "only_nonlocal_abelianization_found",
        }:
            return Stage15SynthesisChoice.SPATIAL_LOCAL_PATH_COVARIANT_LOCALITY_OBSTRUCTED
        if d.classification in {
            "no_abelianization_found_in_declared_search",
            "basis_audit_inconclusive",
        }:
            return Stage15SynthesisChoice.SPATIAL_LOCAL_PATH_COVARIANT_BASIS_INCONCLUSIVE
        return Stage15SynthesisChoice.SPATIAL_LOCAL_PATH_PARTIAL

    if any((*core, d.criteria_32_38_satisfied)):
        return Stage15SynthesisChoice.SPATIAL_LOCAL_PATH_PARTIAL
    return Stage15SynthesisChoice.INCONCLUSIVE


SELECTED_STAGE16_GATE_ID = "four_site_closed_cycle_constraint_algebra_precursor"
SELECTED_STAGE16_GATE_LABEL = (
    "Construct a minimal four-site closed-cycle spatially indexed first-class constraint-algebra "
    "precursor with no terminal seed generator, retain explicit local/smeared structure-function "
    "dependence, test whether one-step L1 or finite-depth locality-preserving Abelianization still "
    "exists, and retest compensated paths, the physical quotient, complete relational observables, "
    "and typed O/P/R/V/Xi descent without assuming general relativity or refoliation invariance."
)


def stage16_gate_candidates() -> tuple[Stage16GateCandidate, ...]:
    candidates = (
        Stage16GateCandidate(
            SELECTED_STAGE16_GATE_ID,
            SELECTED_STAGE16_GATE_LABEL,
            15,
            (
                "Stage15D found a one-step L1 Abelianizing tail shear",
                "the positive witness uses the open chain's terminal C2=K2 seed",
                "the three-site path is acyclic and admits recursive triangular peeling",
                "a four-cycle keeps N1 locality nontrivial while removing a terminal site",
            ),
            "Directly pressure-tests the structural feature most plausibly responsible for the Stage 15 local Abelianization before adding gravitational assumptions.",
        ),
        Stage16GateCandidate(
            "larger_sparse_graph_locality_scaling_audit",
            "Extend the spatial precursor to a larger sparse open/branched graph and test scaling of local Abelianization depth, support growth, path compensation, quotient descent, and typed provenance.",
            11,
            (
                "Stage15 was only three sites",
                "Lfinite depth and support growth may scale with graph diameter",
                "branching can frustrate a single triangular elimination order",
            ),
            "Useful scaling pressure, but less minimal than first removing the terminal-seed loophole with a closed cycle.",
        ),
        Stage16GateCandidate(
            "admissible_basis_transformation_completeness_audit",
            "Broaden the symbolic locality-preserving basis search beyond the finite Stage 15D candidate family and classify additional L0/L1/Lfinite equivalences.",
            9,
            (
                "Stage15D search was not exhaustive",
                "existence of a local witness is established but uniqueness/classification is not",
            ),
            "Improves basis classification, but cannot overturn the existential fact that the current open-chain carrier is locally Abelianizable.",
        ),
        Stage16GateCandidate(
            "gravitational_minisuperspace_extension",
            "Introduce a constrained gravitational/minisuperspace carrier and retest relational, quotient, basis, and typed operational structure.",
            8,
            (
                "GR remains outside the current precursor",
                "gravitational variables would improve physical specificity",
            ),
            "Important later, but minisuperspace again suppresses spatial locality and would not isolate why the Stage 15 L1 witness exists.",
        ),
        Stage16GateCandidate(
            "nonideal_povm_clock_extension",
            "Replace ideal relational clock conditions with nonideal/POVM clock readouts while retaining the Stage 15 typed future-measurement architecture.",
            6,
            (
                "clock idealization remains unresolved",
                "typed future-measurement descent is currently inherited rather than empirically grounded",
            ),
            "Relevant to temporal operationalism, but less directly selected by the new Stage 15 basis/locality evidence.",
        ),
    )
    return tuple(sorted(candidates, key=lambda item: (-item.score, item.gate_id)))


def unresolved_boundaries() -> tuple[str, ...]:
    return (
        "one_step_L1_Abelianization_on_open_three_site_chain => universal_local_Abelianizability",
        "terminal_seed_tail_peeling => closed_cycle_or_branched_graph_Abelianization",
        "finite_graph_locality => continuum_or_relativistic_locality",
        "finite_smeared_constraint_algebra => hypersurface_deformation_algebra",
        "compensated_local_smeared_paths => refoliation_invariance",
        "sampled_four_class_quotient => continuum_reduced_phase_space",
        "typed_OPRVXi_descent => independent_empirical_measurement_law",
        "orbit_sensitive_future_witness => empirical_prediction",
        "Dirac_invariant_data_plus_relational_change => eternalism_or_ontological_becoming",
        "future_measurement_covariance => future_actuality",
        "negative_control_rejection => continuum_correctness",
        "finite_model_success => empirical_discovery",
    )


def answer_project_questions() -> tuple[Stage15ProjectQuestionAnswer, ...]:
    return (
        Stage15ProjectQuestionAnswer(
            "Q1",
            "Does Stage 15 realize a nontrivial spatially indexed local/smeared first-class structure-function precursor?",
            "Yes on the frozen three-site finite carrier. The positive family contains four physical classes and 108 representatives, the three constraint directions remain independent, the local structure coefficient samples negative/zero/positive values, and unsmeared/smeared closure plus off-surface Jacobi checks pass.",
            "established_finite_model_result",
            ("Stage15A:local-smeared-carrier",),
            "Spatial indexing and finite graph locality are not continuum field theory, relativistic locality, or spacetime geometry.",
        ),
        Stage15ProjectQuestionAnswer(
            "Q2",
            "Do local and smeared ordered paths close after the algebraically predicted compensation?",
            "Yes on the tested family. All 864 local pairs and all 540 smeared ordering probes satisfy the predicted compensated closure, with independent Hamiltonian-flow and non-grid endpoint checks guarding against circular reconstruction.",
            "established_finite_model_result",
            ("Stage15B:compensated-paths", "Stage15E:non-grid-endpoints"),
            "Compensated finite path closure is not refoliation invariance or physical temporal passage.",
        ),
        Stage15ProjectQuestionAnswer(
            "Q3",
            "Do Dirac data, complete relational observables, and the physical quotient descend without eliminating relational change?",
            "Yes. The Dirac pair yields exactly four sampled classes of 27 representatives, same-orbit sampled pairs are constraint-flow reachable, all six physical-class pairs remain separated, complete three-clock relational observables descend across licensed paths, and incomplete/raw-coordinate controls fail.",
            "established_finite_model_result",
            ("Stage15C:Dirac-relational-quotient",),
            "Dirac invariance plus relational change does not decide eternalism or ontological becoming.",
        ),
        Stage15ProjectQuestionAnswer(
            "Q4",
            "Does the frozen locality class protect noncommutativity from Abelianizing basis changes?",
            "No on the open three-site carrier. A distinct one-step L1 nearest-neighbour shear C1 -> C1-kappa*T1*C2 produces a strongly commuting basis while preserving the tested physical content. The full seed reconstruction itself remains Lfinite depth 2, so the positive result is not obtained by silently widening L1.",
            "established_finite_model_result",
            ("Stage15D:local-basis-pressure",),
            "Local Abelianization on this carrier is not universal basis triviality or absence of meaningful local constraint structure.",
        ),
        Stage15ProjectQuestionAnswer(
            "Q5",
            "Does typed O/P/R/V/Xi future-measurement content descend across representative, path, and basis choices?",
            "Yes on the frozen family. 108 representative architectures descend to four public payloads; 864 local paths, 540 smeared paths, 1080 independently rebuilt non-grid endpoints, and all 1512 basis correspondences preserve public/future payloads while provenance remains in Xi.",
            "established_finite_model_result",
            ("Stage15E:typed-descent",),
            "Typed operational descent is not future actuality, ontological equivalence, or an empirical measurement law.",
        ),
        Stage15ProjectQuestionAnswer(
            "Q6",
            "Do the frozen destructive controls reject the intended false positives?",
            "Yes. Stage 15F rejects 15/15 structure, disconnection, locality, singular-basis, smearing, Jacobi-anomaly, cross-orbit, incomplete-relational, typed-payload, and known-seed false positives.",
            "established_finite_model_result",
            ("Stage15F:destructive-controls",),
            "Negative-control rejection demonstrates validator discrimination only.",
        ),
        Stage15ProjectQuestionAnswer(
            "Q7",
            "Does Stage 15 establish GR, HDA/refoliation invariance, relativistic locality, fundamental non-Abelianity, eternalism, or becoming?",
            "No. The strongest result is a finite spatially indexed local/smeared path-covariant precursor that is locally Abelianizable in the frozen one-step L1 class. None of the excluded physical or metaphysical claims follows.",
            "interpretation_guard",
            ("Stage15A-F:bounded-structural-evidence",),
            "not_established != false, and local Abelianizability != physical triviality.",
        ),
        Stage15ProjectQuestionAnswer(
            "Q8",
            "What is the strongest evidence-selected next structural pressure test?",
            "The Stage 15 L1 witness peels a terminal seed from an acyclic open chain. The next minimal discriminating carrier should remove that terminal/triangular loophole while preserving a nontrivial locality notion. A four-site closed cycle is the smallest cycle for which N1(i) does not already contain every site.",
            "evidence_selected_research_gate",
            ("Stage15G:gate-ranking",),
            "The selected gate tests closed-cycle locality before introducing GR or refoliation assumptions.",
        ),
    )


@lru_cache(maxsize=1)
def stage15g_synthesis() -> Stage15GSynthesis:
    snapshot = evidence_snapshot()
    choice = select_synthesis_choice(snapshot)
    candidates = stage16_gate_candidates()
    selected = candidates[0]
    criteria = bool(
        choice == Stage15SynthesisChoice.SPATIAL_LOCAL_PATH_COVARIANT_LOCAL_ABELIANIZABLE
        and selected.gate_id == SELECTED_STAGE16_GATE_ID
        and snapshot.stage15a.criteria_11_17_satisfied
        and snapshot.stage15b.criteria_18_24_satisfied
        and snapshot.stage15c.criteria_25_31_satisfied
        and snapshot.stage15d.criteria_32_38_satisfied
        and snapshot.stage15e.criteria_39_43_satisfied
        and snapshot.stage15f.criteria_44_47_satisfied
    )
    return Stage15GSynthesis(
        choice=choice,
        top_level_candidate="T15_candidate=(O,P,R,V;Xi) on a spatially indexed four-class relational quotient",
        established_scope=(
            "three-site spatially indexed first-class structure-function precursor",
            "exact local and constant-smeared compensated-path covariance on the frozen finite family",
            "four classes of 27 representatives with strong Dirac pair and complete three-clock relational observables",
            "one-step L1 locality-preserving Abelianizing witness with physical-content preservation",
            "typed O/P/R/V/Xi representative/path/basis descent with orbit-sensitive diagnostic witness",
            "15/15 frozen destructive controls rejected as intended",
        ),
        basis_pressure_result=(
            "declared one-step L1 locality does not protect noncommutativity on the open three-site chain",
            "the positive L1 witness removes the C1 tail using terminal C2=K2",
            "the known full seed reconstruction remains non-one-step-L1 but factors at Lfinite depth 2",
            "therefore local Abelianization is established for this carrier but universal local Abelianizability is not",
        ),
        retained_typing_resources=(
            "O/P/R/V public quotient architecture",
            "Xi spatial/representative/path/structure-function/basis provenance",
            "future-measurement / weighted / posterior payload inherited from the validated earlier family",
            "complete relational O-events and four orbit-sensitive diagnostic signatures",
        ),
        project_questions=answer_project_questions(),
        unresolved_boundaries=unresolved_boundaries(),
        stage16_candidates=candidates,
        selected_stage16_gate=selected.label,
        criteria_48_49_satisfied=criteria,
    )


def stage15g_summary() -> dict[str, Any]:
    synthesis = stage15g_synthesis()
    return synthesis.as_dict()
