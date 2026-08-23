"""Stage 12B Dirac/relational observables and physical-orbit discrimination.

Stage 12A supplied four canonical physical orbits, five explicit
constraint-generated gauge representatives per orbit, and the inherited Stage
11 external positive parameterization family.  Stage 12B independently
recomputes the frozen Dirac data from phase-space values and asks whether the
same data both (a) remain representative-independent within one declared orbit
and (b) prevent physically distinct canonical orbits from being gauge-collapsed.

The finite result is deliberately bounded: a successful full-Dirac-pair
classifier in this declared model family is not a universal theorem about
constrained systems, general covariance, or ontology.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import numpy as np

from .stage11_parametrized import STAGE11A_POSITIVE_PARAMETERIZATION_IDS
from .stage12_multi_orbit import (
    STAGE12A_ATOL,
    STAGE12A_OMEGA_ALPHA,
    STAGE12A_OMEGA_BETA,
    STAGE12A_OMEGA_GAMMA,
    Stage12ExternalParameterizationView,
    Stage12GaugeRepresentative,
    Stage12PhysicalOrbit,
    canonical_stage12a_external_views,
    canonical_stage12a_orbits,
    canonical_stage12a_representatives,
    canonical_stage12a_representatives_for_orbit,
)

STAGE12B_ATOL = STAGE12A_ATOL
STAGE12B_TAU_VALUES = (-1.25, -0.25, 0.75, 1.50)
STAGE12B_SAME_ORBIT = "same_physical_orbit_by_full_dirac_pair"
STAGE12B_DIFFERENT_ORBIT = "different_physical_orbit_by_dirac_pair"
STAGE12B_FALSE_POSITIVE_REJECTED = "false_positive_rejected"


@dataclass(frozen=True, slots=True)
class Stage12DiracEstimate:
    orbit_id: str
    representative_id: str
    event_id: str
    Q_D: float
    P_D: float
    stored_Q_D_residual: float
    stored_P_D_residual: float
    constraint_residual: float
    provenance: str


@dataclass(frozen=True, slots=True)
class Stage12ExternalDiracEstimate:
    orbit_id: str
    parameterization_id: str
    Q_D: float
    P_D: float
    max_Q_D_spread: float
    max_P_D_spread: float
    provenance: str


@dataclass(frozen=True, slots=True)
class Stage12OrbitComparison:
    source_orbit_id: str
    target_orbit_id: str
    Q_D_equal: bool
    P_D_equal: bool
    full_dirac_pair_equal: bool
    single_invariant_match: str | None
    classification: str


@dataclass(frozen=True, slots=True)
class Stage12RelationalEvaluation:
    orbit_id: str
    source_kind: str
    source_id: str
    tau: float
    reconstructed_q: float
    expected_q: float
    residual: float


@dataclass(frozen=True, slots=True)
class Stage12DerivativeEvaluation:
    orbit_id: str
    source_kind: str
    source_id: str
    dq_dT: float
    expected_P_D: float
    residual: float


@dataclass(frozen=True, slots=True)
class Stage12FalseMatchControl:
    same_P_different_Q_rejected: bool
    same_Q_different_P_rejected: bool
    equal_T_cross_orbit_match_count: int
    equal_q_cross_orbit_match_count: int
    equal_raw_lambda_cross_orbit_match_count: int
    all_equal_single_variable_matches_rejected: bool
    classification: str


@dataclass(frozen=True, slots=True)
class Stage12BDiagnostics:
    representative_dirac_estimate_count: int
    external_dirac_estimate_count: int
    physical_orbit_comparison_count: int
    relational_evaluation_count: int
    derivative_evaluation_count: int
    max_independent_stored_Q_D_residual: float
    max_independent_stored_P_D_residual: float
    max_same_orbit_Q_D_residual: float
    max_same_orbit_P_D_residual: float
    max_external_Q_D_spread: float
    max_external_P_D_spread: float
    max_relational_q_residual: float
    max_relational_derivative_residual: float
    distinct_orbits_not_collapsed: bool
    same_P_different_Q_control_passed: bool
    same_Q_different_P_control_passed: bool
    equal_T_cross_orbit_match_count: int
    equal_q_cross_orbit_match_count: int
    equal_raw_lambda_cross_orbit_match_count: int
    false_match_controls_rejected: bool
    criteria_17_23_satisfied: bool


def _orbit_lookup() -> dict[str, Stage12PhysicalOrbit]:
    return {orbit.orbit_id: orbit for orbit in canonical_stage12a_orbits()}


def stage12b_dirac_from_representative(
    representative: Stage12GaugeRepresentative,
) -> Stage12DiracEstimate:
    """Recompute Q_D and P_D from phase-space values, not stored invariants."""

    P_D = float(representative.p)
    Q_D = float(representative.q - representative.p * representative.T)
    constraint = float(representative.p_T + 0.5 * representative.p**2)
    return Stage12DiracEstimate(
        orbit_id=representative.orbit_id,
        representative_id=representative.representative_id,
        event_id=representative.event_id,
        Q_D=Q_D,
        P_D=P_D,
        stored_Q_D_residual=float(abs(Q_D - representative.Q_D)),
        stored_P_D_residual=float(abs(P_D - representative.P_D)),
        constraint_residual=float(abs(constraint)),
        provenance="independently recomputed from sampled phase-space fields (q,p,T,p_T)",
    )


def canonical_stage12b_dirac_estimates() -> tuple[Stage12DiracEstimate, ...]:
    return tuple(
        stage12b_dirac_from_representative(representative)
        for representative in canonical_stage12a_representatives()
    )


def stage12b_external_dirac_estimate(
    view: Stage12ExternalParameterizationView,
) -> Stage12ExternalDiracEstimate:
    """Recompute one Dirac pair from all events in an external representation."""

    Q_values = np.asarray(view.q_values - view.p_values * view.clock_values, dtype=float)
    P_values = np.asarray(view.p_values, dtype=float)
    Q_D = float(np.mean(Q_values))
    P_D = float(np.mean(P_values))
    return Stage12ExternalDiracEstimate(
        orbit_id=view.orbit_id,
        parameterization_id=view.parameterization_id,
        Q_D=Q_D,
        P_D=P_D,
        max_Q_D_spread=float(np.max(np.abs(Q_values - Q_D))),
        max_P_D_spread=float(np.max(np.abs(P_values - P_D))),
        provenance="independently recomputed from every event in one Stage 11 external representation",
    )


def canonical_stage12b_external_dirac_estimates() -> tuple[Stage12ExternalDiracEstimate, ...]:
    return tuple(stage12b_external_dirac_estimate(view) for view in canonical_stage12a_external_views())


def stage12b_compare_orbits(
    source: Stage12PhysicalOrbit,
    target: Stage12PhysicalOrbit,
    *,
    atol: float = STAGE12B_ATOL,
) -> Stage12OrbitComparison:
    """Compare physical-orbit data using both frozen Dirac invariants."""

    Q_equal = bool(np.isclose(source.Q_D, target.Q_D, atol=atol, rtol=0.0))
    P_equal = bool(np.isclose(source.P_D, target.P_D, atol=atol, rtol=0.0))
    full_equal = Q_equal and P_equal
    if Q_equal and not P_equal:
        single = "Q_D_only"
    elif P_equal and not Q_equal:
        single = "P_D_only"
    else:
        single = None
    return Stage12OrbitComparison(
        source_orbit_id=source.orbit_id,
        target_orbit_id=target.orbit_id,
        Q_D_equal=Q_equal,
        P_D_equal=P_equal,
        full_dirac_pair_equal=full_equal,
        single_invariant_match=single,
        classification=(STAGE12B_SAME_ORBIT if full_equal else STAGE12B_DIFFERENT_ORBIT),
    )


def canonical_stage12b_orbit_comparisons() -> tuple[Stage12OrbitComparison, ...]:
    return tuple(
        stage12b_compare_orbits(source, target)
        for source, target in combinations(canonical_stage12a_orbits(), 2)
    )


def _relational_q(Q_D: float, P_D: float, tau: float) -> float:
    return float(Q_D + P_D * float(tau))


def canonical_stage12b_relational_evaluations() -> tuple[Stage12RelationalEvaluation, ...]:
    """Reconstruct q(T=tau) from representative- and chart-derived Dirac data."""

    orbits = _orbit_lookup()
    evaluations: list[Stage12RelationalEvaluation] = []

    for estimate in canonical_stage12b_dirac_estimates():
        orbit = orbits[estimate.orbit_id]
        for tau in STAGE12B_TAU_VALUES:
            reconstructed = _relational_q(estimate.Q_D, estimate.P_D, tau)
            expected = _relational_q(orbit.Q_D, orbit.P_D, tau)
            evaluations.append(
                Stage12RelationalEvaluation(
                    orbit_id=estimate.orbit_id,
                    source_kind="gauge_representative",
                    source_id=estimate.representative_id,
                    tau=float(tau),
                    reconstructed_q=reconstructed,
                    expected_q=expected,
                    residual=float(abs(reconstructed - expected)),
                )
            )

    for estimate in canonical_stage12b_external_dirac_estimates():
        orbit = orbits[estimate.orbit_id]
        for tau in STAGE12B_TAU_VALUES:
            reconstructed = _relational_q(estimate.Q_D, estimate.P_D, tau)
            expected = _relational_q(orbit.Q_D, orbit.P_D, tau)
            evaluations.append(
                Stage12RelationalEvaluation(
                    orbit_id=estimate.orbit_id,
                    source_kind="external_parameterization",
                    source_id=f"{estimate.orbit_id}:{estimate.parameterization_id}",
                    tau=float(tau),
                    reconstructed_q=reconstructed,
                    expected_q=expected,
                    residual=float(abs(reconstructed - expected)),
                )
            )
    return tuple(evaluations)


def canonical_stage12b_derivative_evaluations() -> tuple[Stage12DerivativeEvaluation, ...]:
    """Reconstruct dq/dT from finite relational differences.

    Gauge representatives use all unordered representative pairs. External
    parameterizations use every adjacent physical-clock interval.  The raw
    external labels are never used as the differentiation denominator.
    """

    evaluations: list[Stage12DerivativeEvaluation] = []

    for orbit in canonical_stage12a_orbits():
        representatives = canonical_stage12a_representatives_for_orbit(orbit)
        for source, target in combinations(representatives, 2):
            delta_T = float(target.T - source.T)
            if abs(delta_T) <= STAGE12B_ATOL:
                raise ValueError("Stage 12B representative derivative requires distinct T values")
            derivative = float((target.q - source.q) / delta_T)
            evaluations.append(
                Stage12DerivativeEvaluation(
                    orbit_id=orbit.orbit_id,
                    source_kind="gauge_representative_pair",
                    source_id=f"{source.representative_id}->{target.representative_id}",
                    dq_dT=derivative,
                    expected_P_D=float(orbit.P_D),
                    residual=float(abs(derivative - orbit.P_D)),
                )
            )

    orbits = _orbit_lookup()
    for view in canonical_stage12a_external_views():
        orbit = orbits[view.orbit_id]
        for index in range(len(view.clock_values) - 1):
            delta_T = float(view.clock_values[index + 1] - view.clock_values[index])
            if abs(delta_T) <= STAGE12B_ATOL:
                raise ValueError("Stage 12B external derivative requires distinct physical-clock values")
            derivative = float((view.q_values[index + 1] - view.q_values[index]) / delta_T)
            evaluations.append(
                Stage12DerivativeEvaluation(
                    orbit_id=view.orbit_id,
                    source_kind="external_parameterization_interval",
                    source_id=f"{view.orbit_id}:{view.parameterization_id}:{index:02d}->{index + 1:02d}",
                    dq_dT=derivative,
                    expected_P_D=float(orbit.P_D),
                    residual=float(abs(derivative - orbit.P_D)),
                )
            )
    return tuple(evaluations)


def stage12b_false_match_control() -> Stage12FalseMatchControl:
    """Reject equal-single-variable and equal-label cross-orbit matching rules."""

    orbit_by_id = _orbit_lookup()
    alpha_beta = stage12b_compare_orbits(
        orbit_by_id[STAGE12A_OMEGA_ALPHA], orbit_by_id[STAGE12A_OMEGA_BETA]
    )
    alpha_gamma = stage12b_compare_orbits(
        orbit_by_id[STAGE12A_OMEGA_ALPHA], orbit_by_id[STAGE12A_OMEGA_GAMMA]
    )
    same_P_rejected = (
        alpha_beta.P_D_equal
        and not alpha_beta.Q_D_equal
        and not alpha_beta.full_dirac_pair_equal
        and alpha_beta.classification == STAGE12B_DIFFERENT_ORBIT
    )
    same_Q_rejected = (
        alpha_gamma.Q_D_equal
        and not alpha_gamma.P_D_equal
        and not alpha_gamma.full_dirac_pair_equal
        and alpha_gamma.classification == STAGE12B_DIFFERENT_ORBIT
    )

    equal_T_count = 0
    equal_q_count = 0
    all_single_matches_rejected = True
    for source_orbit, target_orbit in combinations(canonical_stage12a_orbits(), 2):
        comparison = stage12b_compare_orbits(source_orbit, target_orbit)
        source_reps = canonical_stage12a_representatives_for_orbit(source_orbit)
        target_reps = canonical_stage12a_representatives_for_orbit(target_orbit)
        for source in source_reps:
            for target in target_reps:
                same_T = np.isclose(source.T, target.T, atol=STAGE12B_ATOL, rtol=0.0)
                same_q = np.isclose(source.q, target.q, atol=STAGE12B_ATOL, rtol=0.0)
                if same_T:
                    equal_T_count += 1
                if same_q:
                    equal_q_count += 1
                if (same_T or same_q) and comparison.full_dirac_pair_equal:
                    all_single_matches_rejected = False

    equal_raw_count = 0
    views = canonical_stage12a_external_views()
    by_key = {(view.orbit_id, view.parameterization_id): view for view in views}
    for parameterization_id in STAGE11A_POSITIVE_PARAMETERIZATION_IDS:
        for source_orbit, target_orbit in combinations(canonical_stage12a_orbits(), 2):
            source = by_key[(source_orbit.orbit_id, parameterization_id)]
            target = by_key[(target_orbit.orbit_id, parameterization_id)]
            comparison = stage12b_compare_orbits(source_orbit, target_orbit)
            for source_label, target_label in zip(source.parameter_labels, target.parameter_labels, strict=True):
                if np.isclose(source_label, target_label, atol=STAGE12B_ATOL, rtol=0.0):
                    equal_raw_count += 1
                    if comparison.full_dirac_pair_equal:
                        all_single_matches_rejected = False

    passed = (
        same_P_rejected
        and same_Q_rejected
        and equal_T_count > 0
        and equal_q_count > 0
        and equal_raw_count > 0
        and all_single_matches_rejected
    )
    return Stage12FalseMatchControl(
        same_P_different_Q_rejected=same_P_rejected,
        same_Q_different_P_rejected=same_Q_rejected,
        equal_T_cross_orbit_match_count=equal_T_count,
        equal_q_cross_orbit_match_count=equal_q_count,
        equal_raw_lambda_cross_orbit_match_count=equal_raw_count,
        all_equal_single_variable_matches_rejected=all_single_matches_rejected,
        classification=(STAGE12B_FALSE_POSITIVE_REJECTED if passed else "inconclusive"),
    )


def stage12b_diagnostics() -> Stage12BDiagnostics:
    orbit_by_id = _orbit_lookup()
    estimates = canonical_stage12b_dirac_estimates()
    external_estimates = canonical_stage12b_external_dirac_estimates()
    comparisons = canonical_stage12b_orbit_comparisons()
    relational = canonical_stage12b_relational_evaluations()
    derivatives = canonical_stage12b_derivative_evaluations()
    control = stage12b_false_match_control()

    max_stored_Q = max(item.stored_Q_D_residual for item in estimates)
    max_stored_P = max(item.stored_P_D_residual for item in estimates)

    max_same_Q = 0.0
    max_same_P = 0.0
    for orbit in canonical_stage12a_orbits():
        orbit_estimates = [item for item in estimates if item.orbit_id == orbit.orbit_id]
        max_same_Q = max(max_same_Q, max(abs(item.Q_D - orbit.Q_D) for item in orbit_estimates))
        max_same_P = max(max_same_P, max(abs(item.P_D - orbit.P_D) for item in orbit_estimates))

    max_external_Q = max(item.max_Q_D_spread for item in external_estimates)
    max_external_P = max(item.max_P_D_spread for item in external_estimates)
    external_targets_ok = all(
        abs(item.Q_D - orbit_by_id[item.orbit_id].Q_D) <= STAGE12B_ATOL
        and abs(item.P_D - orbit_by_id[item.orbit_id].P_D) <= STAGE12B_ATOL
        for item in external_estimates
    )

    distinct_not_collapsed = (
        len(comparisons) == 6
        and all(not item.full_dirac_pair_equal for item in comparisons)
        and all(item.classification == STAGE12B_DIFFERENT_ORBIT for item in comparisons)
    )
    max_relational = max(item.residual for item in relational)
    max_derivative = max(item.residual for item in derivatives)

    expected_relational_count = (
        len(estimates) + len(external_estimates)
    ) * len(STAGE12B_TAU_VALUES)
    expected_derivative_count = 4 * 10 + len(canonical_stage12a_external_views()) * 12

    criteria = (
        len(estimates) == 20
        and max_stored_Q <= STAGE12B_ATOL
        and max_stored_P <= STAGE12B_ATOL
        and max_same_Q <= STAGE12B_ATOL
        and max_same_P <= STAGE12B_ATOL
        and len(external_estimates) == 16
        and max_external_Q <= STAGE12B_ATOL
        and max_external_P <= STAGE12B_ATOL
        and external_targets_ok
        and distinct_not_collapsed
        and len(relational) == expected_relational_count
        and max_relational <= STAGE12B_ATOL
        and len(derivatives) == expected_derivative_count
        and max_derivative <= STAGE12B_ATOL
        and control.same_P_different_Q_rejected
        and control.same_Q_different_P_rejected
        and control.all_equal_single_variable_matches_rejected
        and control.classification == STAGE12B_FALSE_POSITIVE_REJECTED
    )

    return Stage12BDiagnostics(
        representative_dirac_estimate_count=len(estimates),
        external_dirac_estimate_count=len(external_estimates),
        physical_orbit_comparison_count=len(comparisons),
        relational_evaluation_count=len(relational),
        derivative_evaluation_count=len(derivatives),
        max_independent_stored_Q_D_residual=float(max_stored_Q),
        max_independent_stored_P_D_residual=float(max_stored_P),
        max_same_orbit_Q_D_residual=float(max_same_Q),
        max_same_orbit_P_D_residual=float(max_same_P),
        max_external_Q_D_spread=float(max_external_Q),
        max_external_P_D_spread=float(max_external_P),
        max_relational_q_residual=float(max_relational),
        max_relational_derivative_residual=float(max_derivative),
        distinct_orbits_not_collapsed=distinct_not_collapsed,
        same_P_different_Q_control_passed=control.same_P_different_Q_rejected,
        same_Q_different_P_control_passed=control.same_Q_different_P_rejected,
        equal_T_cross_orbit_match_count=control.equal_T_cross_orbit_match_count,
        equal_q_cross_orbit_match_count=control.equal_q_cross_orbit_match_count,
        equal_raw_lambda_cross_orbit_match_count=control.equal_raw_lambda_cross_orbit_match_count,
        false_match_controls_rejected=(
            control.all_equal_single_variable_matches_rejected
            and control.classification == STAGE12B_FALSE_POSITIVE_REJECTED
        ),
        criteria_17_23_satisfied=criteria,
    )


def stage12b_summary() -> dict[str, object]:
    diagnostics = stage12b_diagnostics()
    return {
        "status": (
            "Stage 12B completed; criteria 17–23 satisfied"
            if diagnostics.criteria_17_23_satisfied
            else "Stage 12B incomplete"
        ),
        "dirac_invariants": ("Q_D=q-pT", "P_D=p"),
        "relational_observable": "q(T=tau)=Q_D+P_D tau",
        "relational_derivative": "dq/dT=P_D",
        "tau_values": STAGE12B_TAU_VALUES,
        "representative_dirac_estimates": diagnostics.representative_dirac_estimate_count,
        "external_dirac_estimates": diagnostics.external_dirac_estimate_count,
        "physical_orbit_comparisons": diagnostics.physical_orbit_comparison_count,
        "relational_evaluations": diagnostics.relational_evaluation_count,
        "derivative_evaluations": diagnostics.derivative_evaluation_count,
        "max_same_orbit_Q_D_residual": diagnostics.max_same_orbit_Q_D_residual,
        "max_same_orbit_P_D_residual": diagnostics.max_same_orbit_P_D_residual,
        "max_relational_q_residual": diagnostics.max_relational_q_residual,
        "max_relational_derivative_residual": diagnostics.max_relational_derivative_residual,
        "same_P_different_Q_control_passed": diagnostics.same_P_different_Q_control_passed,
        "same_Q_different_P_control_passed": diagnostics.same_Q_different_P_control_passed,
        "equal_T_cross_orbit_matches_rejected": diagnostics.equal_T_cross_orbit_match_count,
        "equal_q_cross_orbit_matches_rejected": diagnostics.equal_q_cross_orbit_match_count,
        "equal_raw_lambda_cross_orbit_matches_rejected": diagnostics.equal_raw_lambda_cross_orbit_match_count,
        "bounded_result": "Stage 12B Dirac/relational physical-orbit discrimination on the frozen finite family = established",
        "guards": (
            "Dirac invariant != timeless ontology by definition",
            "Dirac-invariant orbit data + relational change != proof of eternalism",
            "different physical orbit != later event on one orbit",
            "full-Dirac-pair discrimination in this finite family != universal orbit-classification theorem",
            "relational change != ontological becoming by definition",
        ),
    }
