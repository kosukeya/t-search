"""Stage 14G executable synthesis and evidence-selected Stage 15 gate.

Stage 14A--F establish a bounded finite phase-space-dependent structure-function
carrier, exact compensated mixed paths, representative-independent Dirac and
three-condition relational observables, a four-class quotient, typed O/P/R/V/Xi
operational descent, a frozen diagonal scalar-rescaling obstruction, a richer
triangular commuting-basis equivalence, and destructive/anomaly controls.

Stage 14G integrates those validated diagnostics into exactly one frozen Stage
14 synthesis status and ranks the next research gates.  The current positive
result is intentionally specific: the declared path/quotient/operational family
is covariant on the tested finite carrier, and the Stage-13-style diagonal
scalar-rescaling class is obstructed at X != 0.  A richer triangular mixing still
Abelianizes the carrier while preserving sampled quotient-level content, so the
result is not fundamental non-Abelianity or universal non-Abelianizability.

The evidence-selected next gate introduces spatial indexing/local smearing before
gravity.  This is motivated by the Stage 14 triangular Abelianization and by the
fact that a finite-dimensional/minisuperspace carrier suppresses the spatial
locality and smearing structure central to a hypersurface-deformation algebra.
The selected gate is therefore a locality/constraint-algebra precursor, not an
assumption of GR or refoliation invariance.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from functools import lru_cache
from typing import Any

from .stage14_ablation import Stage14FDiagnostics, stage14f_diagnostics
from .stage14_basis import Stage14DDiagnostics, stage14d_diagnostics
from .stage14_measurement import Stage14EDiagnostics, stage14e_diagnostics
from .stage14_paths import Stage14BDiagnostics, stage14b_diagnostics
from .stage14_relational import Stage14CDiagnostics, stage14c_diagnostics
from .stage14_structure_function import Stage14ADiagnostics, stage14a_diagnostics

STAGE14G_ATOL = 1e-8


class Stage14SynthesisChoice(str, Enum):
    STRUCTURE_FUNCTION_PATH_COVARIANT_SCALAR_OBSTRUCTED = (
        "structure_function_path_covariant_scalar_obstructed"
    )
    STRUCTURE_FUNCTION_PATH_COVARIANT_SCALAR_TRIVIALIZABLE = (
        "structure_function_path_covariant_scalar_trivializable"
    )
    STRUCTURE_FUNCTION_PATH_PARTIAL = "structure_function_path_partial"
    STRUCTURE_FUNCTION_PATH_OBSTRUCTED = "structure_function_path_obstructed"
    INCONCLUSIVE = "inconclusive"


@dataclass(frozen=True, slots=True)
class Stage14ProjectQuestionAnswer:
    question_id: str
    question: str
    answer: str
    evidence_class: str
    evidence_refs: tuple[str, ...]
    boundary: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class Stage15GateCandidate:
    gate_id: str
    label: str
    score: int
    pressure_signals: tuple[str, ...]
    rationale: str

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class Stage14EvidenceSnapshot:
    stage14a: Stage14ADiagnostics
    stage14b: Stage14BDiagnostics
    stage14c: Stage14CDiagnostics
    stage14d: Stage14DDiagnostics
    stage14e: Stage14EDiagnostics
    stage14f: Stage14FDiagnostics


@dataclass(frozen=True, slots=True)
class Stage14GSynthesis:
    choice: Stage14SynthesisChoice
    top_level_candidate: str
    established_scope: tuple[str, ...]
    basis_pressure_result: tuple[str, ...]
    retained_typing_resources: tuple[str, ...]
    project_questions: tuple[Stage14ProjectQuestionAnswer, ...]
    unresolved_boundaries: tuple[str, ...]
    stage15_candidates: tuple[Stage15GateCandidate, ...]
    selected_stage15_gate: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "choice": self.choice.value,
            "top_level_candidate": self.top_level_candidate,
            "established_scope": list(self.established_scope),
            "basis_pressure_result": list(self.basis_pressure_result),
            "retained_typing_resources": list(self.retained_typing_resources),
            "project_questions": [item.as_dict() for item in self.project_questions],
            "unresolved_boundaries": list(self.unresolved_boundaries),
            "stage15_candidates": [item.as_dict() for item in self.stage15_candidates],
            "selected_stage15_gate": self.selected_stage15_gate,
        }


@lru_cache(maxsize=1)
def evidence_snapshot() -> Stage14EvidenceSnapshot:
    """Evaluate the completed Stage 14A--F diagnostics once per process."""

    return Stage14EvidenceSnapshot(
        stage14a=stage14a_diagnostics(),
        stage14b=stage14b_diagnostics(),
        stage14c=stage14c_diagnostics(),
        stage14d=stage14d_diagnostics(),
        stage14e=stage14e_diagnostics(),
        stage14f=stage14f_diagnostics(),
    )


def _scalar_obstruction_established(diagnostics: Stage14DDiagnostics) -> bool:
    return bool(
        diagnostics.scalar_x_nonzero_evaluation_count > 0
        and diagnostics.scalar_x_nonzero_obstructed_count
        == diagnostics.scalar_x_nonzero_evaluation_count
        and diagnostics.scalar_invertible_evaluation_count
        == diagnostics.scalar_evaluation_count
        and diagnostics.rejected_singular_control_count
        == diagnostics.singular_control_count
    )


def _scalar_trivializable_established(diagnostics: Stage14DDiagnostics) -> bool:
    """Counterfactual branch for the frozen synthesis vocabulary.

    The current Stage 14 evidence does not take this branch.  It exists so the
    selector distinguishes a genuine diagonal trivialization from the observed
    diagonal obstruction.
    """

    return bool(
        diagnostics.scalar_x_nonzero_evaluation_count > 0
        and diagnostics.scalar_x_nonzero_obstructed_count == 0
        and diagnostics.scalar_invertible_evaluation_count
        == diagnostics.scalar_evaluation_count
        and diagnostics.rejected_singular_control_count
        == diagnostics.singular_control_count
    )


def _triangular_equivalence_established(diagnostics: Stage14DDiagnostics) -> bool:
    return bool(
        diagnostics.triangular_probe_count == 216
        and abs(diagnostics.minimum_triangular_determinant) > STAGE14G_ATOL
        and diagnostics.max_triangular_inverse_identity_residual <= STAGE14G_ATOL
        and diagnostics.max_triangular_constraint_correspondence_residual <= STAGE14G_ATOL
        and diagnostics.max_triangular_H2_formula_residual <= STAGE14G_ATOL
        and diagnostics.max_triangular_bracket_residual <= STAGE14G_ATOL
        and diagnostics.basis_content_check_count == 108
        and diagnostics.basis_quotient_preserved_count == diagnostics.basis_content_check_count
        and diagnostics.basis_public_payload_equal_count == diagnostics.basis_content_check_count
        and diagnostics.max_basis_dirac_residual <= STAGE14G_ATOL
        and diagnostics.max_basis_complete_relational_residual <= STAGE14G_ATOL
        and diagnostics.max_basis_triangular_dirac_bracket_residual <= STAGE14G_ATOL
        and diagnostics.public_basis_provenance_absent
    )


def _explicit_positive_obstruction(snapshot: Stage14EvidenceSnapshot) -> bool:
    a, b, c, e = snapshot.stage14a, snapshot.stage14b, snapshot.stage14c, snapshot.stage14e
    return bool(
        not a.representative_family_complete
        or not a.independent_constraint_directions
        or not a.first_class_structure_function_closure_established
        or not a.jacobi_established
        or not a.individual_flows_preserve_surface_and_dirac_data
        or not b.all_positive_pairs_closed
        or b.mixed_pair_count != 864
        or b.max_positive_endpoint_residual > STAGE14G_ATOL
        or b.max_positive_dirac_residual > STAGE14G_ATOL
        or c.physically_distinct_pair_count != c.distinct_orbit_pair_count
        or c.max_compensated_path_relational_residual > STAGE14G_ATOL
        or not c.nontrivial_complete_relational_change
        or not c.quotient_exactly_four_by_twenty_seven
        or c.cross_orbit_licensed_arrow_count != 0
        or not e.same_orbit_descent
        or not e.path_descent
        or e.distinct_public_count != e.quotient_class_count
    )


def select_synthesis_choice(
    snapshot: Stage14EvidenceSnapshot | None = None,
) -> Stage14SynthesisChoice:
    evidence = evidence_snapshot() if snapshot is None else snapshot
    a, b, c, d, e, f = (
        evidence.stage14a,
        evidence.stage14b,
        evidence.stage14c,
        evidence.stage14d,
        evidence.stage14e,
        evidence.stage14f,
    )

    if _explicit_positive_obstruction(evidence):
        return Stage14SynthesisChoice.STRUCTURE_FUNCTION_PATH_OBSTRUCTED

    core_validity = (
        a.criteria_11_17_satisfied,
        b.criteria_18_24_satisfied,
        c.criteria_25_31_satisfied,
        e.criteria_39_43_satisfied,
        f.criteria_44_47_satisfied,
    )

    if all(core_validity):
        if d.criteria_32_38_satisfied and _scalar_obstruction_established(d):
            return Stage14SynthesisChoice.STRUCTURE_FUNCTION_PATH_COVARIANT_SCALAR_OBSTRUCTED
        if _scalar_trivializable_established(d) and _triangular_equivalence_established(d):
            return Stage14SynthesisChoice.STRUCTURE_FUNCTION_PATH_COVARIANT_SCALAR_TRIVIALIZABLE
        return Stage14SynthesisChoice.STRUCTURE_FUNCTION_PATH_PARTIAL

    if any((*core_validity, d.criteria_32_38_satisfied)):
        return Stage14SynthesisChoice.STRUCTURE_FUNCTION_PATH_PARTIAL

    return Stage14SynthesisChoice.INCONCLUSIVE


def unresolved_boundaries() -> tuple[str, ...]:
    return (
        "finite_phase_space_structure_function_path_covariance => refoliation_invariance",
        "finite_first_class_structure_function_algebra => hypersurface_deformation_algebra",
        "triangular_Abelianization_on_regular_finite_carrier => universal_basis_trivializability",
        "diagonal_scalar_obstruction => fundamental_physical_non_Abelianity",
        "finite_dimensional_constraint_carrier => spatially_local_smeared_constraint_algebra",
        "spatially_indexed_constraint_precursor => general_relativity",
        "sampled_four_class_gauge_quotient => spacetime_diffeomorphism_invariance",
        "typed_operational_descent => independent_dynamical_or_empirical_measurement_law",
        "Dirac_invariant_data_plus_relational_change => eternalism_or_ontological_becoming",
        "future_measurement_covariance => future_actuality",
        "finite_model_success => empirical_discovery",
    )


def answer_project_questions() -> tuple[Stage14ProjectQuestionAnswer, ...]:
    return (
        Stage14ProjectQuestionAnswer(
            "Q1",
            "Does the frozen Stage 14 carrier realize a genuine phase-space-dependent first-class structure-function algebra on the tested family?",
            "Yes on the finite carrier. All 108 representatives satisfy the three constraints, the generator/gradient rank is three, the sampled structure functions take negative, zero, and positive values, and the bracket/Jacobi identities also hold on the declared off-surface probes.",
            "established_finite_model_result",
            ("Stage14A:carrier-structure-functions",),
            "Finite structure-function closure is not a hypersurface-deformation algebra or spacetime geometry.",
        ),
        Stage14ProjectQuestionAnswer(
            "Q2",
            "Do the phase-space-dependent ordered paths close under the exact third-direction compensator?",
            "Yes. All 864 same-orbit mixed pairs close for both 12D and 21D, with 576 nontrivial X0!=0 compensator differences and 288 exact-zero X0=0 cases, while wrong/missing compensators and cross-orbit paths are rejected.",
            "established_finite_model_result",
            ("Stage14B:compensated-paths",),
            "Compensated mixed-path closure is not refoliation invariance or physical time asymmetry.",
        ),
        Stage14ProjectQuestionAnswer(
            "Q3",
            "Do Dirac data, complete three-condition relational observables, and the physical quotient descend across the licensed path family without collapsing physical change?",
            "Yes on the frozen family. The raw Dirac pair reconstructs four classes of 27 representatives, all six class pairs remain separated, complete relational values descend across the compensated paths, and nontrivial relational change remains present while the two-clock expression stays incomplete.",
            "established_finite_model_result",
            ("Stage14C:Dirac-relational-quotient",),
            "Dirac invariance plus relational change does not decide eternalism or ontological becoming.",
        ),
        Stage14ProjectQuestionAnswer(
            "Q4",
            "Does Stage 14 establish noncommutativity as basis-independent physical content?",
            "No. The frozen diagonal simple_scalar_rescaling class is obstructed on every X!=0 evaluation, but the determinant-one triangular transformation H_2_tilde=H_2-kappa*T1*X*D yields a strongly commuting presentation that preserves the sampled quotient, Dirac/relational values, and inherited public O/P/R/V payloads.",
            "established_finite_model_result",
            ("Stage14D:scalar-obstruction-triangular-equivalence",),
            "Scalar obstruction is not universal non-Abelianizability, and triangular Abelianization is not universal basis trivializability.",
        ),
        Stage14ProjectQuestionAnswer(
            "Q5",
            "Does the typed O/P/R/V/Xi future-measurement architecture descend across path and basis choices?",
            "Yes on the tested family. All 864 path checks and 108 original/triangular basis checks preserve quotient-level public and future-measurement payloads while structure-function, compensator, path, and basis provenance remain explicit in Xi; the four orbit-sensitive witnesses remain distinct.",
            "established_finite_model_result",
            ("Stage14E:typed-operational-descent",),
            "Operational/future-measurement covariance is not future actuality or an empirical prediction.",
        ),
        Stage14ProjectQuestionAnswer(
            "Q6",
            "Do destructive controls fail in the intended typed layers without being promoted into positive evidence?",
            "Yes. The Stage 14F matrix rejects 14/14 structure-function, rank, path, relational, basis, anomaly, typing, and interpretation controls, including 108/108 H_2_bad anomaly witnesses on the rebuilt deformed surface.",
            "established_finite_model_result",
            ("Stage14F:ablation-anomaly-false-positive-matrix",),
            "Negative-control rejection is diagnostic only and is not evidence for GR, refoliation, or ontological becoming.",
        ),
        Stage14ProjectQuestionAnswer(
            "Q7",
            "Does Stage 14 establish a hypersurface-deformation algebra, refoliation invariance, GR, fundamental non-Abelianity, eternalism, or becoming?",
            "No. Stage 14 establishes a bounded finite structure-function path-covariance precursor with a diagonal scalar obstruction and an explicit richer commuting basis. It lacks spatially indexed local/smeared constraints and gravitational field degrees of freedom, and its structural results underdetermine blockness/becoming ontology.",
            "interpretation_guard",
            ("Stage14A-F:bounded-structural-evidence",),
            "No HDA/refoliation/GR or eternalism/becoming verdict is licensed.",
        ),
        Stage14ProjectQuestionAnswer(
            "Q8",
            "What is the strongest unresolved structural boundary and next pressure test?",
            "Stage 14 shows that phase-space-dependent structure functions defeat the Stage-13-style diagonal scalar rescaling but not a richer triangular Abelianization. The next discriminating step is therefore a minimal spatially indexed/local-smeared first-class constraint-algebra precursor that tests locality-preserving basis changes and retests quotient, relational, and operational descent before adding gravitational dynamics.",
            "evidence_selected_research_gate",
            ("Stage14G:gate-ranking",),
            "The selected gate introduces locality/smearing without assuming GR, refoliation invariance, or a hypersurface-deformation algebra.",
        ),
    )


SELECTED_STAGE15_GATE_LABEL = (
    "Construct a minimal spatially indexed first-class constraint-algebra precursor with explicit "
    "local/smeared generators and nontrivial structure-function dependence, test whether the Stage 14 "
    "triangular Abelianization persists under the declared locality-preserving basis class, and retest "
    "the physical quotient, relational observables, and typed O/P/R/V measurement architecture without "
    "assuming general relativity or refoliation invariance."
)


def stage15_gate_candidates(
    snapshot: Stage14EvidenceSnapshot | None = None,
) -> tuple[Stage15GateCandidate, ...]:
    evidence = evidence_snapshot() if snapshot is None else snapshot
    a, b, c, d, e, f = (
        evidence.stage14a,
        evidence.stage14b,
        evidence.stage14c,
        evidence.stage14d,
        evidence.stage14e,
        evidence.stage14f,
    )

    spatial_score = 7
    spatial_signals = [
        "the finite-dimensional Stage 14 carrier is triangularly Abelianizable, so the next pressure test should introduce locality/smearing rather than merely another diagonal rescaling"
    ]
    if a.criteria_11_17_satisfied and b.criteria_18_24_satisfied:
        spatial_score += 1
        spatial_signals.append("the structure-function carrier and 864 compensated mixed pairs provide a stable baseline for a spatially indexed extension")
    if c.criteria_25_31_satisfied:
        spatial_score += 1
        spatial_signals.append("the four-class quotient and complete relational observables provide explicit descent targets")
    if _scalar_obstruction_established(d):
        spatial_score += 1
        spatial_signals.append("Stage 14D verifies a diagonal scalar-rescaling obstruction on all 216 X!=0 evaluations")
    if _triangular_equivalence_established(d):
        spatial_score += 1
        spatial_signals.append("the same carrier still admits an exact determinant-one triangular commuting basis, exposing the finite regular-carrier limitation")
    if e.criteria_39_43_satisfied:
        spatial_score += 1
        spatial_signals.append("typed path/basis operational descent is already explicit and can be retested under locality")
    if f.criteria_44_47_satisfied:
        spatial_score += 1
        spatial_signals.append("the destructive-control matrix is mature enough to detect false locality/basis claims")

    basis_score = 6
    basis_signals = ["Stage 14D leaves the admissible basis-transformation class only partially characterized"]
    if _scalar_obstruction_established(d):
        basis_score += 1
        basis_signals.append("diagonal scalar transformations are explicitly obstructed")
    if _triangular_equivalence_established(d):
        basis_score += 1
        basis_signals.append("a richer triangular transformation explicitly Abelianizes the carrier")
    if e.criteria_39_43_satisfied:
        basis_score += 1
        basis_signals.append("basis provenance and quotient-level payload descent are separately typed")
    if f.criteria_44_47_satisfied:
        basis_score += 1
        basis_signals.append("singular and universal-Abelianization false positives are already controlled")

    gravity_score = 5
    gravity_signals = ["gravitational variables remain absent and therefore remain an important eventual extension"]
    if a.criteria_11_17_satisfied and b.criteria_18_24_satisfied:
        gravity_score += 1
        gravity_signals.append("the finite first-class path baseline is stable")
    if c.criteria_25_31_satisfied:
        gravity_score += 1
        gravity_signals.append("Dirac/relational targets are ready for a gravitational carrier")
    if e.criteria_39_43_satisfied:
        gravity_score += 1
        gravity_signals.append("typed measurement descent is available as a carried diagnostic")

    causal_score = 5
    causal_signals = ["the relational event order remains intentionally minimal"]
    if c.criteria_25_31_satisfied:
        causal_score += 1
        causal_signals.append("nontrivial three-condition relational change is explicit")
    if e.criteria_39_43_satisfied:
        causal_score += 1
        causal_signals.append("typed operational events provide a target for richer causal order")

    povm_score = 5
    povm_signals = ["the inherited clock/measurement family remains idealized"]
    if e.criteria_39_43_satisfied:
        povm_score += 1
        povm_signals.append("future-measurement path/basis descent is stable on the current idealized family")
    if f.criteria_44_47_satisfied:
        povm_score += 1
        povm_signals.append("typed corruption controls are available for a nonideal clock extension")

    candidates = (
        Stage15GateCandidate(
            "spatially_indexed_constraint_algebra_precursor",
            SELECTED_STAGE15_GATE_LABEL,
            spatial_score,
            tuple(spatial_signals),
            "This is the sharpest next structural test because Stage 14 already adds phase-space-dependent structure functions but remains finite-dimensional and triangularly Abelianizable. Spatial indexing and smearing add the locality structure needed to probe a genuinely closer hypersurface-deformation precursor without yet confounding the test with gravitational dynamics.",
        ),
        Stage15GateCandidate(
            "admissible_basis_transformation_audit",
            "Classify a broader finite family of admissible local constraint-basis transformations on the Stage 14 carrier and determine which preserve quotient, relational, and typed operational content.",
            basis_score,
            tuple(basis_signals),
            "This directly studies the scalar-obstruction/triangular-equivalence split, but remaining on the same regular finite carrier risks learning mostly about local Abelianization freedom rather than the locality structure missing from a hypersurface-deformation algebra.",
        ),
        Stage15GateCandidate(
            "gravitational_minisuperspace_extension",
            "Introduce minimal gravitational minisuperspace variables and retest the Stage 14 quotient, relational, basis, and typed measurement diagnostics.",
            gravity_score,
            tuple(gravity_signals),
            "Gravity remains important, but minisuperspace suppresses spatial dependence and therefore cannot by itself test the local/smeared algebraic feature currently missing. Selecting it now would also conflate new gravitational dynamics with the unresolved locality/basis question.",
        ),
        Stage15GateCandidate(
            "richer_causal_order",
            "Extend the relational event-order substrate while preserving the validated Stage 14 constraint/measurement distinctions.",
            causal_score,
            tuple(causal_signals),
            "This remains live for the blockness/becoming program but does not pressure-test the Stage 14D basis result as directly as spatially indexed constraints.",
        ),
        Stage15GateCandidate(
            "nonideal_povm_clocks",
            "Replace the idealized clock/measurement family with a bounded nonideal POVM-style clock family and retest typed descent.",
            povm_score,
            tuple(povm_signals),
            "This strengthens operational realism but is less diagnostic of the algebraic limitation exposed by the triangular Abelianization.",
        ),
    )
    return tuple(sorted(candidates, key=lambda item: (-item.score, item.gate_id)))


@lru_cache(maxsize=1)
def stage14g_synthesis() -> Stage14GSynthesis:
    snapshot = evidence_snapshot()
    choice = select_synthesis_choice(snapshot)
    candidates = stage15_gate_candidates(snapshot)
    selected = candidates[0].gate_id
    return Stage14GSynthesis(
        choice=choice,
        top_level_candidate="T14_candidate=(O,P,R,V;Xi) over the finite structure-function path-covariant quotient",
        established_scope=(
            "4 physical orbits and 108 sampled representatives with three independent first-class constraint directions",
            "phase-space-dependent structure functions sampling negative, zero, and positive values with off-surface closure/Jacobi checks",
            "864/864 same-orbit mixed pairs with exact third-direction compensated 12D/21D closure",
            "6/6 physical-orbit pair discrimination and exactly 4 quotient classes of size 27",
            "23328 compensated complete-relational path comparisons with nontrivial three-condition relational change",
            "216/216 X!=0 diagonal scalar evaluations obstructed in the frozen simple_scalar_rescaling class",
            "216 triangular probes and 108/108 basis-content checks preserving the sampled quotient/Dirac/relational/public payloads",
            "864 typed path-descent checks and 108 typed original/triangular basis-descent checks",
            "14/14 destructive/anomaly/false-positive controls rejected",
        ),
        basis_pressure_result=(
            "Stage-13-style diagonal scalar-rescaling obstruction = established on the frozen Stage 14 class",
            "determinant-one triangular commuting-basis equivalence = established on the frozen Stage 14 carrier",
            "original noncommutativity is therefore not established as quotient-level basis-independent physical content",
        ),
        retained_typing_resources=(
            "physical-orbit identity and four-class quotient correspondence",
            "three constraint-generator identities and structure-function provenance",
            "representative, path-word, compensator, and basis provenance in Xi",
            "three-condition physical-event correspondence",
            "continuation-class and outcome correspondence",
            "measurement normalization semantics and future-signature typing",
            "separation of path word from physical temporal history",
            "separation of constraint-basis presentation from quotient-level physical content",
        ),
        project_questions=answer_project_questions(),
        unresolved_boundaries=unresolved_boundaries(),
        stage15_candidates=candidates,
        selected_stage15_gate=selected,
    )


def stage14g_summary() -> dict[str, Any]:
    synthesis = stage14g_synthesis()
    return {
        **synthesis.as_dict(),
        "bounded_result": (
            "Stage 14G synthesis on the validated Stage 14A-F finite evidence chain = "
            f"{synthesis.choice.value}"
        ),
        "current_execution_criteria": {
            "48": "executable synthesis selects exactly one frozen Stage 14 status from the validated Stage 14A-F evidence chain",
            "49": "the next research gate is evidence-selected without presupposing GR, refoliation invariance, gravitational field degrees of freedom, or a metaphysical conclusion",
            "50": "external final full-repository regression and merge-readiness review remains pending",
        },
        "guards": (
            "structure_function_path_covariant_scalar_obstructed finite family != refoliation invariance",
            "finite first-class structure-function algebra != hypersurface-deformation algebra",
            "diagonal scalar-rescaling obstruction != fundamental physical non-Abelianity",
            "triangular basis equivalence != universal basis trivializability",
            "spatially indexed constraint precursor != general relativity",
            "future-measurement covariance != future actuality",
            "Dirac-invariant data + relational change != proof of eternalism",
            "complete relational observable != ontological becoming by definition",
            "finite-model success != empirical discovery",
            "repository validation != new scientific evidence",
        ),
    }
