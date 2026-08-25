"""Stage 14C Dirac / three-condition complete relational observables.

This module consumes the validated Stage 14A carrier and Stage 14B compensated
mixed-path family.  It closes only the Stage 14C questions frozen in
``docs/stage14_protocol.md``:

* reconstruct ``Q_D=q-p T1-b T2-a X`` and ``P_D=p`` from all 108 raw
  representatives and verify strong commutation with the three constraints;
* separate all six pairs among the four physical orbit classes;
* evaluate the three-condition complete relational observable on the frozen
  3x3x3 relational grid and test compensated-path descent;
* retain nontrivial relational change while rejecting a two-clock expression
  that leaves the third ``X``/``D`` gauge direction unresolved;
* reconstruct exactly four sampled quotient classes of 27 representatives and
  audit that no cross-orbit representative pair is licensed as a gauge path;
* keep the finite relational/quotient result explicitly separate from
  eternalism, timeless ontology, and ontological becoming claims.

The result remains a finite constrained-model statement.  It is not
refoliation invariance, a hypersurface-deformation algebra, general covariance,
or a metaphysical result.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations, product

import numpy as np

from .stage14_paths import (
    STAGE14B_PATH_12D,
    STAGE14B_PATH_21D,
    Stage14BMixedPair,
    canonical_stage14b_mixed_pairs,
    stage14b_make_mixed_pair,
)
from .stage14_structure_function import (
    STAGE14A_A,
    STAGE14A_ATOL,
    STAGE14A_B,
    STAGE14A_D,
    STAGE14A_GRID_VALUES,
    STAGE14A_H1,
    STAGE14A_H2,
    Stage14PhaseSpacePoint,
    Stage14Representative,
    canonical_stage14a_orbits,
    canonical_stage14a_representatives,
    canonical_stage14a_representatives_for_orbit,
    stage14a_apply_flow,
    stage14a_constraint_gradients,
)

STAGE14C_DIRAC_ROLE = "three_constraint_dirac_initial_data"
STAGE14C_COMPLETE_RELATIONAL_ROLE = "three_condition_complete_relational_observable"
STAGE14C_TWO_CLOCK_ROLE = "two_clock_incomplete_relational_expression"
STAGE14C_TWO_CLOCK_CLASSIFICATION = "two_clock_observable_incomplete"
STAGE14C_ORBIT_DISCRIMINATION = "full_dirac_pair_orbit_discrimination_established"
STAGE14C_PATH_COVARIANCE = "compensated_path_complete_relational_covariance_established"
STAGE14C_QUOTIENT_CLASSIFICATION = "four_class_physical_quotient_established"
STAGE14C_METAPHYSICAL_CLAIM_STATUS = "not_licensed"


@dataclass(frozen=True, slots=True)
class Stage14CDiracEstimate:
    orbit_id: str
    representative_id: str
    Q_D: float
    P_D: float
    Q_declared_residual: float
    P_declared_residual: float
    bracket_Q_D_residual: float
    bracket_Q_H1_residual: float
    bracket_Q_H2_residual: float
    bracket_P_D_residual: float
    bracket_P_H1_residual: float
    bracket_P_H2_residual: float
    role: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage14COrbitDiracSummary:
    orbit_id: str
    representative_count: int
    Q_D_mean: float
    P_D_mean: float
    Q_D_spread: float
    P_D_spread: float


@dataclass(frozen=True, slots=True)
class Stage14COrbitPairDiscrimination:
    left_orbit_id: str
    right_orbit_id: str
    delta_Q_D: float
    delta_P_D: float
    full_pair_separation: float
    same_P_different_Q: bool
    same_Q_different_P: bool
    physically_distinct: bool
    classification: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage14CCompleteRelationalEvaluation:
    orbit_id: str
    representative_id: str
    tau1: float
    tau2: float
    chi: float
    Q_D: float
    P_D: float
    q_complete: float
    canonical_target_q: float
    target_residual: float
    role: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage14CCompensatedRelationalComparison:
    pair_id: str
    orbit_id: str
    tau1: float
    tau2: float
    chi: float
    q_12D: float
    q_21D: float
    q_target: float
    path_order_residual: float
    path_12_target_residual: float
    path_21_target_residual: float
    classification: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage14CTwoClockEvaluation:
    orbit_id: str
    tau1: float
    tau2: float
    X_raw: float
    q_two_clock: float
    role: str
    classification: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage14CQuotientClass:
    class_id: str
    Q_D: float
    P_D: float
    member_representative_ids: tuple[str, ...]
    member_orbit_ids: tuple[str, ...]
    classification: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage14CDiagnostics:
    representative_count: int
    dirac_estimate_count: int
    orbit_summary_count: int
    distinct_orbit_pair_count: int
    physically_distinct_pair_count: int
    complete_relational_evaluation_count: int
    compensated_pair_count: int
    compensated_path_relational_comparison_count: int
    two_clock_evaluation_count: int
    two_clock_group_count: int
    two_clock_incomplete_group_count: int
    quotient_class_count: int
    min_quotient_class_size: int
    max_quotient_class_size: int
    cross_orbit_licensed_arrow_count: int
    cross_orbit_rejected_count: int
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
    min_complete_relational_spread: float
    max_complete_relational_spread: float
    min_two_clock_spread: float
    max_two_clock_spread: float
    nontrivial_complete_relational_change: bool
    two_clock_incompleteness_explicit: bool
    quotient_exactly_four_by_twenty_seven: bool
    metaphysical_boundary_explicit: bool
    criteria_25_31_satisfied: bool


def _poisson_from_gradients(df: np.ndarray, dg: np.ndarray) -> float:
    return float(
        sum(
            df[q_index] * dg[p_index] - df[p_index] * dg[q_index]
            for q_index, p_index in ((0, 1), (2, 3), (4, 5), (6, 7))
        )
    )


def stage14c_reconstruct_dirac_from_point(point: Stage14PhaseSpacePoint) -> tuple[float, float]:
    """Reconstruct the frozen Dirac pair using only raw phase-space data."""

    Q_D = float(point.q - point.p * point.T1 - STAGE14A_B * point.T2 - STAGE14A_A * point.X)
    P_D = float(point.p)
    return Q_D, P_D


def _dirac_bracket_residuals(point: Stage14PhaseSpacePoint) -> tuple[float, ...]:
    # Canonical coordinate order is (T1,p_1,T2,p_2,X,p_X,q,p).
    grad_Q = np.asarray(
        [-point.p, 0.0, -STAGE14A_B, 0.0, -STAGE14A_A, 0.0, 1.0, -point.T1],
        dtype=float,
    )
    grad_P = np.asarray([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0], dtype=float)
    grad_D, grad_H1, grad_H2 = stage14a_constraint_gradients(point)
    return (
        abs(_poisson_from_gradients(grad_Q, grad_D)),
        abs(_poisson_from_gradients(grad_Q, grad_H1)),
        abs(_poisson_from_gradients(grad_Q, grad_H2)),
        abs(_poisson_from_gradients(grad_P, grad_D)),
        abs(_poisson_from_gradients(grad_P, grad_H1)),
        abs(_poisson_from_gradients(grad_P, grad_H2)),
    )


def stage14c_dirac_estimate(representative: Stage14Representative) -> Stage14CDiracEstimate:
    Q_D, P_D = stage14c_reconstruct_dirac_from_point(representative.point())
    qd, qh1, qh2, pd, ph1, ph2 = _dirac_bracket_residuals(representative.point())
    return Stage14CDiracEstimate(
        orbit_id=representative.orbit_id,
        representative_id=representative.representative_id,
        Q_D=Q_D,
        P_D=P_D,
        Q_declared_residual=abs(Q_D - representative.declared_Q_D),
        P_declared_residual=abs(P_D - representative.declared_P_D),
        bracket_Q_D_residual=qd,
        bracket_Q_H1_residual=qh1,
        bracket_Q_H2_residual=qh2,
        bracket_P_D_residual=pd,
        bracket_P_H1_residual=ph1,
        bracket_P_H2_residual=ph2,
        role=STAGE14C_DIRAC_ROLE,
        metaphysical_claim_status=STAGE14C_METAPHYSICAL_CLAIM_STATUS,
    )


def canonical_stage14c_dirac_estimates() -> tuple[Stage14CDiracEstimate, ...]:
    return tuple(stage14c_dirac_estimate(rep) for rep in canonical_stage14a_representatives())


def stage14c_orbit_dirac_summaries() -> tuple[Stage14COrbitDiracSummary, ...]:
    estimates = canonical_stage14c_dirac_estimates()
    result: list[Stage14COrbitDiracSummary] = []
    for orbit in canonical_stage14a_orbits():
        members = [item for item in estimates if item.orbit_id == orbit.orbit_id]
        q_values = [item.Q_D for item in members]
        p_values = [item.P_D for item in members]
        result.append(
            Stage14COrbitDiracSummary(
                orbit_id=orbit.orbit_id,
                representative_count=len(members),
                Q_D_mean=float(sum(q_values) / len(q_values)),
                P_D_mean=float(sum(p_values) / len(p_values)),
                Q_D_spread=float(max(q_values) - min(q_values)),
                P_D_spread=float(max(p_values) - min(p_values)),
            )
        )
    return tuple(result)


def stage14c_orbit_pair_discriminations() -> tuple[Stage14COrbitPairDiscrimination, ...]:
    summaries = {item.orbit_id: item for item in stage14c_orbit_dirac_summaries()}
    result: list[Stage14COrbitPairDiscrimination] = []
    for left, right in combinations(canonical_stage14a_orbits(), 2):
        left_summary = summaries[left.orbit_id]
        right_summary = summaries[right.orbit_id]
        delta_Q = float(abs(left_summary.Q_D_mean - right_summary.Q_D_mean))
        delta_P = float(abs(left_summary.P_D_mean - right_summary.P_D_mean))
        separation = float(max(delta_Q, delta_P))
        result.append(
            Stage14COrbitPairDiscrimination(
                left_orbit_id=left.orbit_id,
                right_orbit_id=right.orbit_id,
                delta_Q_D=delta_Q,
                delta_P_D=delta_P,
                full_pair_separation=separation,
                same_P_different_Q=delta_P <= STAGE14A_ATOL and delta_Q > STAGE14A_ATOL,
                same_Q_different_P=delta_Q <= STAGE14A_ATOL and delta_P > STAGE14A_ATOL,
                physically_distinct=separation > STAGE14A_ATOL,
                classification=STAGE14C_ORBIT_DISCRIMINATION,
                metaphysical_claim_status=STAGE14C_METAPHYSICAL_CLAIM_STATUS,
            )
        )
    return tuple(result)


def stage14c_complete_relational_value(
    Q_D: float,
    P_D: float,
    tau1: float,
    tau2: float,
    chi: float,
) -> float:
    return float(Q_D + P_D * tau1 + STAGE14A_B * tau2 + STAGE14A_A * chi)


def canonical_stage14c_complete_relational_evaluations() -> tuple[Stage14CCompleteRelationalEvaluation, ...]:
    result: list[Stage14CCompleteRelationalEvaluation] = []
    grid = STAGE14A_GRID_VALUES
    for orbit in canonical_stage14a_orbits():
        reps = canonical_stage14a_representatives_for_orbit(orbit)
        target_lookup = {(rep.T1, rep.T2, rep.X): rep for rep in reps}
        for source in reps:
            Q_D, P_D = stage14c_reconstruct_dirac_from_point(source.point())
            for tau1, tau2, chi in product(grid, repeat=3):
                q_complete = stage14c_complete_relational_value(Q_D, P_D, tau1, tau2, chi)
                target = target_lookup[(float(tau1), float(tau2), float(chi))]
                result.append(
                    Stage14CCompleteRelationalEvaluation(
                        orbit_id=orbit.orbit_id,
                        representative_id=source.representative_id,
                        tau1=float(tau1),
                        tau2=float(tau2),
                        chi=float(chi),
                        Q_D=Q_D,
                        P_D=P_D,
                        q_complete=q_complete,
                        canonical_target_q=float(target.q),
                        target_residual=abs(q_complete - target.q),
                        role=STAGE14C_COMPLETE_RELATIONAL_ROLE,
                        metaphysical_claim_status=STAGE14C_METAPHYSICAL_CLAIM_STATUS,
                    )
                )
    return tuple(result)


def _stage14c_compensated_endpoint(pair: Stage14BMixedPair, path_word: str) -> Stage14PhaseSpacePoint:
    source = pair.source.point()
    if path_word == STAGE14B_PATH_12D:
        raw = stage14a_apply_flow(
            stage14a_apply_flow(source, STAGE14A_H1, pair.s),
            STAGE14A_H2,
            pair.u,
        )
        return stage14a_apply_flow(raw, STAGE14A_D, pair.v_12D)
    if path_word == STAGE14B_PATH_21D:
        raw = stage14a_apply_flow(
            stage14a_apply_flow(source, STAGE14A_H2, pair.u),
            STAGE14A_H1,
            pair.s,
        )
        return stage14a_apply_flow(raw, STAGE14A_D, pair.v_21D)
    raise ValueError(f"unknown Stage 14C path word: {path_word}")


def canonical_stage14c_compensated_relational_comparisons() -> tuple[Stage14CCompensatedRelationalComparison, ...]:
    result: list[Stage14CCompensatedRelationalComparison] = []
    orbit_targets = {
        orbit.orbit_id: {
            (rep.T1, rep.T2, rep.X): rep
            for rep in canonical_stage14a_representatives_for_orbit(orbit)
        }
        for orbit in canonical_stage14a_orbits()
    }
    for pair in canonical_stage14b_mixed_pairs():
        endpoint_12 = _stage14c_compensated_endpoint(pair, STAGE14B_PATH_12D)
        endpoint_21 = _stage14c_compensated_endpoint(pair, STAGE14B_PATH_21D)
        Q_12, P_12 = stage14c_reconstruct_dirac_from_point(endpoint_12)
        Q_21, P_21 = stage14c_reconstruct_dirac_from_point(endpoint_21)
        for tau1, tau2, chi in product(STAGE14A_GRID_VALUES, repeat=3):
            q_12 = stage14c_complete_relational_value(Q_12, P_12, tau1, tau2, chi)
            q_21 = stage14c_complete_relational_value(Q_21, P_21, tau1, tau2, chi)
            target = orbit_targets[pair.orbit_id][(float(tau1), float(tau2), float(chi))]
            result.append(
                Stage14CCompensatedRelationalComparison(
                    pair_id=pair.pair_id,
                    orbit_id=pair.orbit_id,
                    tau1=float(tau1),
                    tau2=float(tau2),
                    chi=float(chi),
                    q_12D=q_12,
                    q_21D=q_21,
                    q_target=float(target.q),
                    path_order_residual=abs(q_12 - q_21),
                    path_12_target_residual=abs(q_12 - target.q),
                    path_21_target_residual=abs(q_21 - target.q),
                    classification=STAGE14C_PATH_COVARIANCE,
                    metaphysical_claim_status=STAGE14C_METAPHYSICAL_CLAIM_STATUS,
                )
            )
    return tuple(result)


def stage14c_complete_relational_spreads() -> tuple[tuple[str, float], ...]:
    summaries = {item.orbit_id: item for item in stage14c_orbit_dirac_summaries()}
    result: list[tuple[str, float]] = []
    for orbit in canonical_stage14a_orbits():
        summary = summaries[orbit.orbit_id]
        values = [
            stage14c_complete_relational_value(summary.Q_D_mean, summary.P_D_mean, tau1, tau2, chi)
            for tau1, tau2, chi in product(STAGE14A_GRID_VALUES, repeat=3)
        ]
        result.append((orbit.orbit_id, float(max(values) - min(values))))
    return tuple(result)


def canonical_stage14c_two_clock_evaluations() -> tuple[Stage14CTwoClockEvaluation, ...]:
    summaries = {item.orbit_id: item for item in stage14c_orbit_dirac_summaries()}
    result: list[Stage14CTwoClockEvaluation] = []
    for orbit in canonical_stage14a_orbits():
        summary = summaries[orbit.orbit_id]
        for tau1, tau2, X_raw in product(STAGE14A_GRID_VALUES, repeat=3):
            result.append(
                Stage14CTwoClockEvaluation(
                    orbit_id=orbit.orbit_id,
                    tau1=float(tau1),
                    tau2=float(tau2),
                    X_raw=float(X_raw),
                    q_two_clock=stage14c_complete_relational_value(
                        summary.Q_D_mean,
                        summary.P_D_mean,
                        float(tau1),
                        float(tau2),
                        float(X_raw),
                    ),
                    role=STAGE14C_TWO_CLOCK_ROLE,
                    classification=STAGE14C_TWO_CLOCK_CLASSIFICATION,
                    metaphysical_claim_status=STAGE14C_METAPHYSICAL_CLAIM_STATUS,
                )
            )
    return tuple(result)


def stage14c_two_clock_group_spreads() -> tuple[tuple[str, float, float, float], ...]:
    evaluations = canonical_stage14c_two_clock_evaluations()
    result: list[tuple[str, float, float, float]] = []
    for orbit in canonical_stage14a_orbits():
        for tau1, tau2 in product(STAGE14A_GRID_VALUES, repeat=2):
            values = [
                item.q_two_clock
                for item in evaluations
                if item.orbit_id == orbit.orbit_id
                and abs(item.tau1 - tau1) <= STAGE14A_ATOL
                and abs(item.tau2 - tau2) <= STAGE14A_ATOL
            ]
            result.append((orbit.orbit_id, float(tau1), float(tau2), float(max(values) - min(values))))
    return tuple(result)


def stage14c_quotient_classes() -> tuple[Stage14CQuotientClass, ...]:
    estimates = canonical_stage14c_dirac_estimates()
    grouped: dict[tuple[float, float], list[Stage14CDiracEstimate]] = {}
    for item in estimates:
        key = (round(item.Q_D, 12), round(item.P_D, 12))
        grouped.setdefault(key, []).append(item)

    result: list[Stage14CQuotientClass] = []
    for index, ((Q_D, P_D), members) in enumerate(sorted(grouped.items()), start=1):
        result.append(
            Stage14CQuotientClass(
                class_id=f"stage14c_quotient_{index}",
                Q_D=float(Q_D),
                P_D=float(P_D),
                member_representative_ids=tuple(sorted(item.representative_id for item in members)),
                member_orbit_ids=tuple(sorted({item.orbit_id for item in members})),
                classification=STAGE14C_QUOTIENT_CLASSIFICATION,
                metaphysical_claim_status=STAGE14C_METAPHYSICAL_CLAIM_STATUS,
            )
        )
    return tuple(result)


def stage14c_cross_orbit_arrow_audit() -> tuple[int, int]:
    reps = canonical_stage14a_representatives()
    licensed = 0
    rejected = 0
    for source in reps:
        for target in reps:
            if source.orbit_id == target.orbit_id:
                continue
            try:
                stage14b_make_mixed_pair(source, target)
            except ValueError:
                rejected += 1
            else:
                licensed += 1
    return licensed, rejected


def stage14c_diagnostics() -> Stage14CDiagnostics:
    estimates = canonical_stage14c_dirac_estimates()
    summaries = stage14c_orbit_dirac_summaries()
    orbit_pairs = stage14c_orbit_pair_discriminations()
    complete = canonical_stage14c_complete_relational_evaluations()
    compensated_pairs = canonical_stage14b_mixed_pairs()
    compensated = canonical_stage14c_compensated_relational_comparisons()
    complete_spreads = stage14c_complete_relational_spreads()
    two_clock = canonical_stage14c_two_clock_evaluations()
    two_clock_spreads = stage14c_two_clock_group_spreads()
    quotient = stage14c_quotient_classes()
    licensed_cross, rejected_cross = stage14c_cross_orbit_arrow_audit()

    max_bracket = max(
        max(
            item.bracket_Q_D_residual,
            item.bracket_Q_H1_residual,
            item.bracket_Q_H2_residual,
            item.bracket_P_D_residual,
            item.bracket_P_H1_residual,
            item.bracket_P_H2_residual,
        )
        for item in estimates
    )
    max_compensated = max(
        max(
            item.path_order_residual,
            item.path_12_target_residual,
            item.path_21_target_residual,
        )
        for item in compensated
    )
    same_p_diff_q = [item for item in orbit_pairs if item.same_P_different_Q]
    same_q_diff_p = [item for item in orbit_pairs if item.same_Q_different_P]
    nontrivial_change = all(spread > STAGE14A_ATOL for _, spread in complete_spreads)
    two_clock_incomplete = all(spread > STAGE14A_ATOL for _, _, _, spread in two_clock_spreads)
    quotient_exact = (
        len(quotient) == 4
        and all(len(item.member_representative_ids) == 27 for item in quotient)
        and all(len(item.member_orbit_ids) == 1 for item in quotient)
        and licensed_cross == 0
        and rejected_cross == 8748
    )
    metaphysical_boundary = all(
        item.metaphysical_claim_status == STAGE14C_METAPHYSICAL_CLAIM_STATUS
        for item in (*estimates, *orbit_pairs, *complete, *compensated, *two_clock, *quotient)
    )

    criteria = (
        len(estimates) == 108
        and len(summaries) == 4
        and all(item.representative_count == 27 for item in summaries)
        and max(item.Q_D_spread for item in summaries) <= STAGE14A_ATOL
        and max(item.P_D_spread for item in summaries) <= STAGE14A_ATOL
        and max(item.Q_declared_residual for item in estimates) <= STAGE14A_ATOL
        and max(item.P_declared_residual for item in estimates) <= STAGE14A_ATOL
        and max_bracket <= STAGE14A_ATOL
        and len(orbit_pairs) == 6
        and all(item.physically_distinct for item in orbit_pairs)
        and len(same_p_diff_q) >= 1
        and len(same_q_diff_p) >= 1
        and len(complete) == 2916
        and max(item.target_residual for item in complete) <= STAGE14A_ATOL
        and len(compensated_pairs) == 864
        and len(compensated) == 23328
        and max_compensated <= STAGE14A_ATOL
        and nontrivial_change
        and len(two_clock) == 108
        and len(two_clock_spreads) == 36
        and two_clock_incomplete
        and quotient_exact
        and metaphysical_boundary
    )

    return Stage14CDiagnostics(
        representative_count=len(canonical_stage14a_representatives()),
        dirac_estimate_count=len(estimates),
        orbit_summary_count=len(summaries),
        distinct_orbit_pair_count=len(orbit_pairs),
        physically_distinct_pair_count=sum(item.physically_distinct for item in orbit_pairs),
        complete_relational_evaluation_count=len(complete),
        compensated_pair_count=len(compensated_pairs),
        compensated_path_relational_comparison_count=len(compensated),
        two_clock_evaluation_count=len(two_clock),
        two_clock_group_count=len(two_clock_spreads),
        two_clock_incomplete_group_count=sum(
            spread > STAGE14A_ATOL for _, _, _, spread in two_clock_spreads
        ),
        quotient_class_count=len(quotient),
        min_quotient_class_size=min(len(item.member_representative_ids) for item in quotient),
        max_quotient_class_size=max(len(item.member_representative_ids) for item in quotient),
        cross_orbit_licensed_arrow_count=licensed_cross,
        cross_orbit_rejected_count=rejected_cross,
        same_P_different_Q_control_count=len(same_p_diff_q),
        same_Q_different_P_control_count=len(same_q_diff_p),
        max_Q_declared_residual=max(item.Q_declared_residual for item in estimates),
        max_P_declared_residual=max(item.P_declared_residual for item in estimates),
        max_dirac_bracket_residual=max_bracket,
        max_same_orbit_Q_spread=max(item.Q_D_spread for item in summaries),
        max_same_orbit_P_spread=max(item.P_D_spread for item in summaries),
        min_distinct_orbit_full_pair_separation=min(item.full_pair_separation for item in orbit_pairs),
        max_complete_relational_target_residual=max(item.target_residual for item in complete),
        max_compensated_path_relational_residual=max_compensated,
        min_complete_relational_spread=min(spread for _, spread in complete_spreads),
        max_complete_relational_spread=max(spread for _, spread in complete_spreads),
        min_two_clock_spread=min(spread for _, _, _, spread in two_clock_spreads),
        max_two_clock_spread=max(spread for _, _, _, spread in two_clock_spreads),
        nontrivial_complete_relational_change=nontrivial_change,
        two_clock_incompleteness_explicit=two_clock_incomplete,
        quotient_exactly_four_by_twenty_seven=quotient_exact,
        metaphysical_boundary_explicit=metaphysical_boundary,
        criteria_25_31_satisfied=criteria,
    )
