"""Stage 13C Dirac / two-clock complete relational observables.

This module consumes the Stage 13A two-constraint carrier and the Stage 13B
compensated mixed-path family.  It closes only the Stage 13C questions frozen
in ``docs/stage13_protocol.md``:

* independently reconstruct ``Q_D=q-pT-aX`` and ``P_D=p`` from all 36 raw
  representatives;
* verify the Dirac pair against both constraint generators;
* preserve same-orbit agreement and discriminate all six distinct orbit pairs;
* evaluate the two-clock complete observable on the frozen 3x3 clock grid;
* test representative- and compensated-path-choice independence;
* explicitly reject a one-clock expression that leaves ``X`` gauge-dependent;
* retain the same-P/different-Q and same-Q/different-P anti-triviality controls;
* keep the finite relational result separate from eternalism and ontological
  becoming claims.

The positive result remains a finite constrained-model statement.  It is not
refoliation invariance, general covariance, or a metaphysical result.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from t_search.stage13_multi_constraint import (
    STAGE13A_A,
    STAGE13A_ATOL,
    Stage13PhaseSpacePoint,
    Stage13Representative,
    canonical_stage13a_grid_values,
    canonical_stage13a_orbits,
    canonical_stage13a_representatives,
    canonical_stage13a_representatives_for_orbit,
    stage13a_constraint_gradients,
)
from t_search.stage13_paths import canonical_stage13b_mixed_path_comparisons

STAGE13C_DIRAC_ROLE = "two_constraint_dirac_initial_data"
STAGE13C_COMPLETE_RELATIONAL_ROLE = "two_clock_complete_relational_observable"
STAGE13C_ONE_CLOCK_ROLE = "one_clock_incomplete_relational_expression"
STAGE13C_ONE_CLOCK_CLASSIFICATION = "one_clock_observable_incomplete"
STAGE13C_ORBIT_DISCRIMINATION = "full_dirac_pair_orbit_discrimination_established"
STAGE13C_PATH_COVARIANCE = "compensated_path_complete_relational_covariance_established"
STAGE13C_METAPHYSICAL_CLAIM_STATUS = "not_licensed"


@dataclass(frozen=True, slots=True)
class Stage13CDiracEstimate:
    orbit_id: str
    representative_id: str
    event_id: str
    Q_D: float
    P_D: float
    Q_declared_residual: float
    P_declared_residual: float
    bracket_Q_KT_residual: float
    bracket_Q_KX_residual: float
    bracket_P_KT_residual: float
    bracket_P_KX_residual: float
    role: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage13COrbitDiracSummary:
    orbit_id: str
    representative_count: int
    Q_D_mean: float
    P_D_mean: float
    Q_D_spread: float
    P_D_spread: float


@dataclass(frozen=True, slots=True)
class Stage13COrbitPairDiscrimination:
    left_orbit_id: str
    right_orbit_id: str
    delta_Q_D: float
    delta_P_D: float
    full_pair_separation: float
    same_P_different_Q: bool
    same_Q_different_P: bool
    physically_distinct: bool
    classification: str


@dataclass(frozen=True, slots=True)
class Stage13CCompleteRelationalEvaluation:
    orbit_id: str
    representative_id: str
    tau: float
    chi: float
    Q_D: float
    P_D: float
    q_complete: float
    canonical_target_q: float
    target_residual: float
    role: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage13CCompensatedRelationalComparison:
    comparison_id: str
    orbit_id: str
    tau: float
    chi: float
    q_TX: float
    q_XT: float
    q_target: float
    TX_XT_residual: float
    TX_target_residual: float
    XT_target_residual: float
    classification: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage13COneClockEvaluation:
    orbit_id: str
    tau: float
    X_raw: float
    q_one_clock: float
    role: str
    classification: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage13CDiagnostics:
    representative_count: int
    dirac_estimate_count: int
    orbit_summary_count: int
    distinct_orbit_pair_count: int
    physically_distinct_pair_count: int
    complete_relational_evaluation_count: int
    compensated_path_relational_comparison_count: int
    one_clock_evaluation_count: int
    one_clock_group_count: int
    one_clock_incomplete_group_count: int
    same_P_different_Q_control_count: int
    same_Q_different_P_control_count: int
    max_Q_declared_residual: float
    max_P_declared_residual: float
    max_dirac_bracket_residual: float
    max_same_orbit_Q_spread: float
    max_same_orbit_P_spread: float
    min_distinct_orbit_full_pair_separation: float
    max_complete_relational_target_residual: float
    max_compensated_path_relational_residual: float
    min_one_clock_spread: float
    max_one_clock_spread: float
    nontrivial_complete_relational_change: bool
    one_clock_incompleteness_explicit: bool
    metaphysical_boundary_explicit: bool
    criteria_24_31_satisfied: bool


def _poisson_from_gradients(df: tuple[float, ...], dg: tuple[float, ...] | list[float]) -> float:
    total = 0.0
    for q_index, p_index in ((0, 1), (2, 3), (4, 5)):
        total += df[q_index] * dg[p_index] - df[p_index] * dg[q_index]
    return float(total)


def stage13c_reconstruct_dirac_from_point(point: Stage13PhaseSpacePoint) -> tuple[float, float]:
    """Reconstruct the Stage 13 Dirac pair using only raw phase-space data."""

    Q_D = float(point.q - point.p * point.T - STAGE13A_A * point.X)
    P_D = float(point.p)
    return Q_D, P_D


def _dirac_bracket_residuals(point: Stage13PhaseSpacePoint) -> tuple[float, float, float, float]:
    # Coordinate order is (T,p_T,X,p_X,q,p).
    grad_Q = (-point.p, 0.0, -STAGE13A_A, 0.0, 1.0, -point.T)
    grad_P = (0.0, 0.0, 0.0, 0.0, 0.0, 1.0)
    gradients = stage13a_constraint_gradients(point)
    grad_KT = tuple(float(value) for value in gradients[0])
    grad_KX = tuple(float(value) for value in gradients[1])
    return (
        abs(_poisson_from_gradients(grad_Q, grad_KT)),
        abs(_poisson_from_gradients(grad_Q, grad_KX)),
        abs(_poisson_from_gradients(grad_P, grad_KT)),
        abs(_poisson_from_gradients(grad_P, grad_KX)),
    )


def stage13c_dirac_estimate(representative: Stage13Representative) -> Stage13CDiracEstimate:
    Q_D, P_D = stage13c_reconstruct_dirac_from_point(representative.point())
    qkt, qkx, pkt, pkx = _dirac_bracket_residuals(representative.point())
    return Stage13CDiracEstimate(
        orbit_id=representative.orbit_id,
        representative_id=representative.representative_id,
        event_id=representative.event_id,
        Q_D=Q_D,
        P_D=P_D,
        Q_declared_residual=abs(Q_D - representative.declared_Q_D),
        P_declared_residual=abs(P_D - representative.declared_P_D),
        bracket_Q_KT_residual=qkt,
        bracket_Q_KX_residual=qkx,
        bracket_P_KT_residual=pkt,
        bracket_P_KX_residual=pkx,
        role=STAGE13C_DIRAC_ROLE,
        metaphysical_claim_status=STAGE13C_METAPHYSICAL_CLAIM_STATUS,
    )


def canonical_stage13c_dirac_estimates() -> tuple[Stage13CDiracEstimate, ...]:
    return tuple(stage13c_dirac_estimate(rep) for rep in canonical_stage13a_representatives())


def stage13c_orbit_dirac_summaries() -> tuple[Stage13COrbitDiracSummary, ...]:
    estimates = canonical_stage13c_dirac_estimates()
    result: list[Stage13COrbitDiracSummary] = []
    for orbit in canonical_stage13a_orbits():
        members = [item for item in estimates if item.orbit_id == orbit.orbit_id]
        q_values = [item.Q_D for item in members]
        p_values = [item.P_D for item in members]
        result.append(
            Stage13COrbitDiracSummary(
                orbit_id=orbit.orbit_id,
                representative_count=len(members),
                Q_D_mean=float(sum(q_values) / len(q_values)),
                P_D_mean=float(sum(p_values) / len(p_values)),
                Q_D_spread=float(max(q_values) - min(q_values)),
                P_D_spread=float(max(p_values) - min(p_values)),
            )
        )
    return tuple(result)


def stage13c_orbit_pair_discriminations() -> tuple[Stage13COrbitPairDiscrimination, ...]:
    summaries = {item.orbit_id: item for item in stage13c_orbit_dirac_summaries()}
    result: list[Stage13COrbitPairDiscrimination] = []
    for left, right in combinations(canonical_stage13a_orbits(), 2):
        left_summary = summaries[left.orbit_id]
        right_summary = summaries[right.orbit_id]
        delta_Q = float(abs(left_summary.Q_D_mean - right_summary.Q_D_mean))
        delta_P = float(abs(left_summary.P_D_mean - right_summary.P_D_mean))
        separation = float(max(delta_Q, delta_P))
        result.append(
            Stage13COrbitPairDiscrimination(
                left_orbit_id=left.orbit_id,
                right_orbit_id=right.orbit_id,
                delta_Q_D=delta_Q,
                delta_P_D=delta_P,
                full_pair_separation=separation,
                same_P_different_Q=delta_P <= STAGE13A_ATOL and delta_Q > STAGE13A_ATOL,
                same_Q_different_P=delta_Q <= STAGE13A_ATOL and delta_P > STAGE13A_ATOL,
                physically_distinct=separation > STAGE13A_ATOL,
                classification=STAGE13C_ORBIT_DISCRIMINATION,
            )
        )
    return tuple(result)


def stage13c_complete_relational_value(Q_D: float, P_D: float, tau: float, chi: float) -> float:
    return float(Q_D + P_D * tau + STAGE13A_A * chi)


def canonical_stage13c_complete_relational_evaluations() -> tuple[Stage13CCompleteRelationalEvaluation, ...]:
    result: list[Stage13CCompleteRelationalEvaluation] = []
    grid = canonical_stage13a_grid_values()
    for orbit in canonical_stage13a_orbits():
        reps = canonical_stage13a_representatives_for_orbit(orbit)
        target_lookup = {(rep.T, rep.X): rep for rep in reps}
        for source in reps:
            Q_D, P_D = stage13c_reconstruct_dirac_from_point(source.point())
            for tau in grid:
                for chi in grid:
                    q_complete = stage13c_complete_relational_value(Q_D, P_D, tau, chi)
                    target = target_lookup[(float(tau), float(chi))]
                    result.append(
                        Stage13CCompleteRelationalEvaluation(
                            orbit_id=orbit.orbit_id,
                            representative_id=source.representative_id,
                            tau=float(tau),
                            chi=float(chi),
                            Q_D=Q_D,
                            P_D=P_D,
                            q_complete=q_complete,
                            canonical_target_q=target.q,
                            target_residual=abs(q_complete - target.q),
                            role=STAGE13C_COMPLETE_RELATIONAL_ROLE,
                            metaphysical_claim_status=STAGE13C_METAPHYSICAL_CLAIM_STATUS,
                        )
                    )
    return tuple(result)


def canonical_stage13c_compensated_relational_comparisons() -> tuple[Stage13CCompensatedRelationalComparison, ...]:
    result: list[Stage13CCompensatedRelationalComparison] = []
    grid = canonical_stage13a_grid_values()
    orbit_targets = {
        orbit.orbit_id: {(rep.T, rep.X): rep for rep in canonical_stage13a_representatives_for_orbit(orbit)}
        for orbit in canonical_stage13a_orbits()
    }
    for comparison in canonical_stage13b_mixed_path_comparisons():
        Q_TX, P_TX = stage13c_reconstruct_dirac_from_point(comparison.compensated_TX_endpoint)
        Q_XT, P_XT = stage13c_reconstruct_dirac_from_point(comparison.compensated_XT_endpoint)
        for tau in grid:
            for chi in grid:
                q_TX = stage13c_complete_relational_value(Q_TX, P_TX, tau, chi)
                q_XT = stage13c_complete_relational_value(Q_XT, P_XT, tau, chi)
                target = orbit_targets[comparison.orbit_id][(float(tau), float(chi))]
                result.append(
                    Stage13CCompensatedRelationalComparison(
                        comparison_id=comparison.comparison_id,
                        orbit_id=comparison.orbit_id,
                        tau=float(tau),
                        chi=float(chi),
                        q_TX=q_TX,
                        q_XT=q_XT,
                        q_target=float(target.q),
                        TX_XT_residual=abs(q_TX - q_XT),
                        TX_target_residual=abs(q_TX - target.q),
                        XT_target_residual=abs(q_XT - target.q),
                        classification=STAGE13C_PATH_COVARIANCE,
                        metaphysical_claim_status=STAGE13C_METAPHYSICAL_CLAIM_STATUS,
                    )
                )
    return tuple(result)


def canonical_stage13c_one_clock_evaluations() -> tuple[Stage13COneClockEvaluation, ...]:
    result: list[Stage13COneClockEvaluation] = []
    grid = canonical_stage13a_grid_values()
    summaries = {item.orbit_id: item for item in stage13c_orbit_dirac_summaries()}
    for orbit in canonical_stage13a_orbits():
        summary = summaries[orbit.orbit_id]
        for tau in grid:
            for X_raw in grid:
                result.append(
                    Stage13COneClockEvaluation(
                        orbit_id=orbit.orbit_id,
                        tau=float(tau),
                        X_raw=float(X_raw),
                        q_one_clock=stage13c_complete_relational_value(
                            summary.Q_D_mean,
                            summary.P_D_mean,
                            float(tau),
                            float(X_raw),
                        ),
                        role=STAGE13C_ONE_CLOCK_ROLE,
                        classification=STAGE13C_ONE_CLOCK_CLASSIFICATION,
                        metaphysical_claim_status=STAGE13C_METAPHYSICAL_CLAIM_STATUS,
                    )
                )
    return tuple(result)


def stage13c_one_clock_group_spreads() -> tuple[tuple[str, float, float], ...]:
    evaluations = canonical_stage13c_one_clock_evaluations()
    result: list[tuple[str, float, float]] = []
    for orbit in canonical_stage13a_orbits():
        for tau in canonical_stage13a_grid_values():
            values = [
                item.q_one_clock
                for item in evaluations
                if item.orbit_id == orbit.orbit_id and abs(item.tau - tau) <= STAGE13A_ATOL
            ]
            result.append((orbit.orbit_id, float(tau), float(max(values) - min(values))))
    return tuple(result)


def stage13c_diagnostics() -> Stage13CDiagnostics:
    estimates = canonical_stage13c_dirac_estimates()
    summaries = stage13c_orbit_dirac_summaries()
    pairs = stage13c_orbit_pair_discriminations()
    complete = canonical_stage13c_complete_relational_evaluations()
    compensated = canonical_stage13c_compensated_relational_comparisons()
    one_clock = canonical_stage13c_one_clock_evaluations()
    one_clock_spreads = stage13c_one_clock_group_spreads()

    max_bracket = max(
        max(
            item.bracket_Q_KT_residual,
            item.bracket_Q_KX_residual,
            item.bracket_P_KT_residual,
            item.bracket_P_KX_residual,
        )
        for item in estimates
    )
    max_compensated_relational = max(
        max(item.TX_XT_residual, item.TX_target_residual, item.XT_target_residual)
        for item in compensated
    )
    same_p_diff_q = [item for item in pairs if item.same_P_different_Q]
    same_q_diff_p = [item for item in pairs if item.same_Q_different_P]

    complete_values_by_orbit: dict[str, set[float]] = {}
    for item in complete:
        complete_values_by_orbit.setdefault(item.orbit_id, set()).add(round(item.q_complete, 12))
    nontrivial_change = all(len(values) > 1 for values in complete_values_by_orbit.values())
    one_clock_incomplete = all(spread > STAGE13A_ATOL for _, _, spread in one_clock_spreads)
    metaphysical_boundary = all(
        item.metaphysical_claim_status == STAGE13C_METAPHYSICAL_CLAIM_STATUS
        for item in (*estimates, *complete, *compensated, *one_clock)
    )

    criteria = (
        len(estimates) == 36
        and len(summaries) == 4
        and all(item.representative_count == 9 for item in summaries)
        and max(item.Q_D_spread for item in summaries) <= STAGE13A_ATOL
        and max(item.P_D_spread for item in summaries) <= STAGE13A_ATOL
        and max(item.Q_declared_residual for item in estimates) <= STAGE13A_ATOL
        and max(item.P_declared_residual for item in estimates) <= STAGE13A_ATOL
        and max_bracket <= STAGE13A_ATOL
        and len(pairs) == 6
        and all(item.physically_distinct for item in pairs)
        and len(same_p_diff_q) >= 1
        and len(same_q_diff_p) >= 1
        and len(complete) == 324
        and max(item.target_residual for item in complete) <= STAGE13A_ATOL
        and len(compensated) == 1296
        and max_compensated_relational <= STAGE13A_ATOL
        and len(one_clock) == 36
        and len(one_clock_spreads) == 12
        and one_clock_incomplete
        and nontrivial_change
        and metaphysical_boundary
    )

    return Stage13CDiagnostics(
        representative_count=len(canonical_stage13a_representatives()),
        dirac_estimate_count=len(estimates),
        orbit_summary_count=len(summaries),
        distinct_orbit_pair_count=len(pairs),
        physically_distinct_pair_count=sum(item.physically_distinct for item in pairs),
        complete_relational_evaluation_count=len(complete),
        compensated_path_relational_comparison_count=len(compensated),
        one_clock_evaluation_count=len(one_clock),
        one_clock_group_count=len(one_clock_spreads),
        one_clock_incomplete_group_count=sum(spread > STAGE13A_ATOL for _, _, spread in one_clock_spreads),
        same_P_different_Q_control_count=len(same_p_diff_q),
        same_Q_different_P_control_count=len(same_q_diff_p),
        max_Q_declared_residual=max(item.Q_declared_residual for item in estimates),
        max_P_declared_residual=max(item.P_declared_residual for item in estimates),
        max_dirac_bracket_residual=max_bracket,
        max_same_orbit_Q_spread=max(item.Q_D_spread for item in summaries),
        max_same_orbit_P_spread=max(item.P_D_spread for item in summaries),
        min_distinct_orbit_full_pair_separation=min(item.full_pair_separation for item in pairs),
        max_complete_relational_target_residual=max(item.target_residual for item in complete),
        max_compensated_path_relational_residual=max_compensated_relational,
        min_one_clock_spread=min(spread for _, _, spread in one_clock_spreads),
        max_one_clock_spread=max(spread for _, _, spread in one_clock_spreads),
        nontrivial_complete_relational_change=nontrivial_change,
        one_clock_incompleteness_explicit=one_clock_incomplete,
        metaphysical_boundary_explicit=metaphysical_boundary,
        criteria_24_31_satisfied=criteria,
    )
