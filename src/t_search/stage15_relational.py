"""Stage 15C Dirac data, complete relational observables, and quotient descent.

This module consumes the validated Stage 15A spatially indexed carrier and
Stage 15B compensated local/smeared path families.  It closes only the Stage
15C questions frozen in ``docs/stage15_protocol.md``:

* reconstruct ``Q_D=Q-sum_i c_i T_i`` and ``P_D=P`` from raw representatives;
* verify strong Poisson commutation with every presented constraint on both the
  positive and the frozen off-surface probe families;
* reconstruct the sampled physical quotient as exactly four classes of 27
  representatives and separate all six physical-orbit pairs with the Dirac
  pair;
* evaluate the three-condition complete relational observable on the frozen
  3x3x3 clock grid and show nontrivial relational change;
* verify descent across both Stage 15B compensated local paths and the frozen
  constant-smeared path orderings using the algebraically predicted C2
  compensator;
* reject all three one-clock-omitted expressions and the raw representative Q
  coordinate as complete quotient observables.

These are finite-carrier structural statements.  They do not establish general
relativity, continuum refoliation invariance, eternalism, ontological becoming,
or a universal reduced-phase-space theorem.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations, product

import numpy as np

from .stage15_local import (
    STAGE15A_ATOL,
    STAGE15A_C,
    STAGE15A_GRID_VALUES,
    Stage15PhaseSpacePoint,
    Stage15Representative,
    canonical_stage15a_off_surface_probes,
    canonical_stage15a_orbits,
    canonical_stage15a_representatives,
    canonical_stage15a_representatives_for_orbit,
    stage15a_constraint_gradients,
)
from .stage15_paths import (
    STAGE15B_PATH_012,
    STAGE15B_PATH_102,
    STAGE15B_SMEARED_CASES,
    Stage15BLocalPair,
    canonical_stage15b_local_pairs,
    stage15b_apply_local_flow,
    stage15b_apply_smeared_flow,
    stage15b_expected_smeared_c2_defect,
    stage15b_make_local_pair,
)

STAGE15C_DIRAC_ROLE = "three_site_dirac_initial_data"
STAGE15C_COMPLETE_RELATIONAL_ROLE = "three_condition_complete_relational_observable"
STAGE15C_OMITTED_CLOCK_ROLE = "one_clock_condition_omitted_relational_expression"
STAGE15C_OMITTED_CLOCK_CLASSIFICATION = "relational_observable_incomplete"
STAGE15C_RAW_Q_ROLE = "raw_representative_coordinate"
STAGE15C_RAW_Q_CLASSIFICATION = "raw_representative_coordinate_not_complete_relational"
STAGE15C_ORBIT_DISCRIMINATION = "full_dirac_pair_orbit_discrimination_established"
STAGE15C_LOCAL_PATH_COVARIANCE = "local_compensated_path_complete_relational_covariance_established"
STAGE15C_SMEARED_PATH_COVARIANCE = "smeared_compensated_path_complete_relational_covariance_established"
STAGE15C_QUOTIENT_CLASSIFICATION = "four_class_physical_quotient_established"
STAGE15C_METAPHYSICAL_CLAIM_STATUS = "not_licensed"


@dataclass(frozen=True, slots=True)
class Stage15CDiracEstimate:
    orbit_id: str
    representative_id: str
    Q_D: float
    P_D: float
    Q_declared_residual: float
    P_declared_residual: float
    bracket_Q_residuals: tuple[float, float, float]
    bracket_P_residuals: tuple[float, float, float]
    role: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage15COrbitDiracSummary:
    orbit_id: str
    representative_count: int
    Q_D_mean: float
    P_D_mean: float
    Q_D_spread: float
    P_D_spread: float


@dataclass(frozen=True, slots=True)
class Stage15COrbitPairDiscrimination:
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
class Stage15CCompleteRelationalEvaluation:
    orbit_id: str
    representative_id: str
    tau0: float
    tau1: float
    tau2: float
    Q_D: float
    P_D: float
    Q_complete: float
    canonical_target_Q: float
    target_residual: float
    role: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage15CLocalPathRelationalComparison:
    pair_id: str
    orbit_id: str
    tau0: float
    tau1: float
    tau2: float
    Q_012: float
    Q_102: float
    Q_target: float
    endpoint_order_residual: float
    relational_order_residual: float
    path_012_target_residual: float
    path_102_target_residual: float
    classification: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage15CSmearedPathRelationalComparison:
    representative_id: str
    orbit_id: str
    case_id: str
    tau0: float
    tau1: float
    tau2: float
    predicted_compensator: float
    endpoint_residual: float
    Q_nm: float
    Q_compensated_mn: float
    Q_target: float
    relational_order_residual: float
    nm_target_residual: float
    compensated_target_residual: float
    classification: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage15COmittedClockEvaluation:
    orbit_id: str
    omitted_clock_index: int
    tau0: float | None
    tau1: float | None
    tau2: float | None
    raw_omitted_clock: float
    Q_incomplete: float
    role: str
    classification: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage15CRawQEvaluation:
    orbit_id: str
    representative_id: str
    raw_Q: float
    role: str
    classification: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage15CQuotientClass:
    class_id: str
    Q_D: float
    P_D: float
    member_representative_ids: tuple[str, ...]
    member_orbit_ids: tuple[str, ...]
    classification: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage15CDiagnostics:
    representative_count: int
    dirac_estimate_count: int
    strong_commutation_probe_count: int
    orbit_summary_count: int
    distinct_orbit_pair_count: int
    physically_distinct_pair_count: int
    complete_relational_evaluation_count: int
    local_compensated_pair_count: int
    local_relational_comparison_count: int
    smeared_ordering_count: int
    smeared_relational_comparison_count: int
    omitted_clock_evaluation_count: int
    omitted_clock_group_count: int
    omitted_clock_incomplete_group_count: int
    raw_Q_evaluation_count: int
    raw_Q_group_count: int
    raw_Q_nondescending_group_count: int
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
    max_local_endpoint_order_residual: float
    max_local_relational_residual: float
    max_smeared_endpoint_residual: float
    max_smeared_relational_residual: float
    min_complete_relational_spread: float
    max_complete_relational_spread: float
    omitted_clock_spreads: tuple[float, float, float]
    min_raw_Q_spread: float
    max_raw_Q_spread: float
    strong_dirac_commutation_established: bool
    nontrivial_complete_relational_change: bool
    local_path_relational_descent_established: bool
    smeared_path_relational_descent_established: bool
    omitted_clock_incompleteness_explicit: bool
    raw_coordinate_non_descent_explicit: bool
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


def _phase_space_residual(a: Stage15PhaseSpacePoint, b: Stage15PhaseSpacePoint) -> float:
    return float(max(abs(x - y) for x, y in zip(a.vector(), b.vector(), strict=True)))


def stage15c_reconstruct_dirac_from_point(point: Stage15PhaseSpacePoint) -> tuple[float, float]:
    c0, c1, c2 = STAGE15A_C
    return (
        float(point.Q - c0 * point.T0 - c1 * point.T1 - c2 * point.T2),
        float(point.P),
    )


def stage15c_dirac_bracket_residuals(point: Stage15PhaseSpacePoint) -> tuple[float, ...]:
    c0, c1, c2 = STAGE15A_C
    grad_QD = np.asarray([1.0, 0.0, -c0, 0.0, -c1, 0.0, -c2, 0.0], dtype=float)
    grad_PD = np.asarray([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=float)
    gradients = stage15a_constraint_gradients(point)
    return tuple(
        abs(_poisson_from_gradients(gradient, constraint_gradient))
        for gradient in (grad_QD, grad_PD)
        for constraint_gradient in gradients
    )


def stage15c_dirac_estimate(representative: Stage15Representative) -> Stage15CDiracEstimate:
    Q_D, P_D = stage15c_reconstruct_dirac_from_point(representative.point())
    residuals = stage15c_dirac_bracket_residuals(representative.point())
    return Stage15CDiracEstimate(
        orbit_id=representative.orbit_id,
        representative_id=representative.representative_id,
        Q_D=Q_D,
        P_D=P_D,
        Q_declared_residual=abs(Q_D - representative.declared_Q_D),
        P_declared_residual=abs(P_D - representative.declared_P_D),
        bracket_Q_residuals=(residuals[0], residuals[1], residuals[2]),
        bracket_P_residuals=(residuals[3], residuals[4], residuals[5]),
        role=STAGE15C_DIRAC_ROLE,
        metaphysical_claim_status=STAGE15C_METAPHYSICAL_CLAIM_STATUS,
    )


@lru_cache(maxsize=1)
def canonical_stage15c_dirac_estimates() -> tuple[Stage15CDiracEstimate, ...]:
    return tuple(stage15c_dirac_estimate(rep) for rep in canonical_stage15a_representatives())


@lru_cache(maxsize=1)
def stage15c_orbit_dirac_summaries() -> tuple[Stage15COrbitDiracSummary, ...]:
    estimates = canonical_stage15c_dirac_estimates()
    result: list[Stage15COrbitDiracSummary] = []
    for orbit in canonical_stage15a_orbits():
        members = [item for item in estimates if item.orbit_id == orbit.orbit_id]
        q_values = [item.Q_D for item in members]
        p_values = [item.P_D for item in members]
        result.append(
            Stage15COrbitDiracSummary(
                orbit_id=orbit.orbit_id,
                representative_count=len(members),
                Q_D_mean=float(sum(q_values) / len(q_values)),
                P_D_mean=float(sum(p_values) / len(p_values)),
                Q_D_spread=float(max(q_values) - min(q_values)),
                P_D_spread=float(max(p_values) - min(p_values)),
            )
        )
    return tuple(result)


@lru_cache(maxsize=1)
def stage15c_orbit_pair_discriminations() -> tuple[Stage15COrbitPairDiscrimination, ...]:
    summaries = {item.orbit_id: item for item in stage15c_orbit_dirac_summaries()}
    result: list[Stage15COrbitPairDiscrimination] = []
    for left, right in combinations(canonical_stage15a_orbits(), 2):
        left_summary = summaries[left.orbit_id]
        right_summary = summaries[right.orbit_id]
        delta_Q = float(abs(left_summary.Q_D_mean - right_summary.Q_D_mean))
        delta_P = float(abs(left_summary.P_D_mean - right_summary.P_D_mean))
        separation = float(max(delta_Q, delta_P))
        result.append(
            Stage15COrbitPairDiscrimination(
                left_orbit_id=left.orbit_id,
                right_orbit_id=right.orbit_id,
                delta_Q_D=delta_Q,
                delta_P_D=delta_P,
                full_pair_separation=separation,
                same_P_different_Q=delta_P <= STAGE15A_ATOL and delta_Q > STAGE15A_ATOL,
                same_Q_different_P=delta_Q <= STAGE15A_ATOL and delta_P > STAGE15A_ATOL,
                physically_distinct=separation > STAGE15A_ATOL,
                classification=STAGE15C_ORBIT_DISCRIMINATION,
                metaphysical_claim_status=STAGE15C_METAPHYSICAL_CLAIM_STATUS,
            )
        )
    return tuple(result)


def stage15c_complete_relational_value(Q_D: float, tau0: float, tau1: float, tau2: float) -> float:
    c0, c1, c2 = STAGE15A_C
    return float(Q_D + c0 * tau0 + c1 * tau1 + c2 * tau2)


@lru_cache(maxsize=1)
def canonical_stage15c_complete_relational_evaluations() -> tuple[Stage15CCompleteRelationalEvaluation, ...]:
    result: list[Stage15CCompleteRelationalEvaluation] = []
    for orbit in canonical_stage15a_orbits():
        reps = canonical_stage15a_representatives_for_orbit(orbit)
        target_lookup = {(rep.T0, rep.T1, rep.T2): rep for rep in reps}
        for source in reps:
            Q_D, P_D = stage15c_reconstruct_dirac_from_point(source.point())
            for tau0, tau1, tau2 in product(STAGE15A_GRID_VALUES, repeat=3):
                Q_complete = stage15c_complete_relational_value(Q_D, tau0, tau1, tau2)
                target = target_lookup[(float(tau0), float(tau1), float(tau2))]
                result.append(
                    Stage15CCompleteRelationalEvaluation(
                        orbit_id=orbit.orbit_id,
                        representative_id=source.representative_id,
                        tau0=float(tau0),
                        tau1=float(tau1),
                        tau2=float(tau2),
                        Q_D=Q_D,
                        P_D=P_D,
                        Q_complete=Q_complete,
                        canonical_target_Q=float(target.Q),
                        target_residual=abs(Q_complete - target.Q),
                        role=STAGE15C_COMPLETE_RELATIONAL_ROLE,
                        metaphysical_claim_status=STAGE15C_METAPHYSICAL_CLAIM_STATUS,
                    )
                )
    return tuple(result)


@lru_cache(maxsize=1)
def stage15c_complete_relational_spreads() -> tuple[tuple[str, float], ...]:
    summaries = {item.orbit_id: item for item in stage15c_orbit_dirac_summaries()}
    result: list[tuple[str, float]] = []
    for orbit in canonical_stage15a_orbits():
        Q_D = summaries[orbit.orbit_id].Q_D_mean
        values = [
            stage15c_complete_relational_value(Q_D, tau0, tau1, tau2)
            for tau0, tau1, tau2 in product(STAGE15A_GRID_VALUES, repeat=3)
        ]
        result.append((orbit.orbit_id, float(max(values) - min(values))))
    return tuple(result)


def _stage15c_local_compensated_endpoint(pair: Stage15BLocalPair, path_word: str) -> Stage15PhaseSpacePoint:
    source = pair.source.point()
    if path_word == STAGE15B_PATH_012:
        raw = stage15b_apply_local_flow(stage15b_apply_local_flow(source, 0, pair.s), 1, pair.u)
        return stage15b_apply_local_flow(raw, 2, pair.v_012)
    if path_word == STAGE15B_PATH_102:
        raw = stage15b_apply_local_flow(stage15b_apply_local_flow(source, 1, pair.u), 0, pair.s)
        return stage15b_apply_local_flow(raw, 2, pair.v_102)
    raise ValueError(f"unknown Stage 15C local path word: {path_word}")


@lru_cache(maxsize=1)
def canonical_stage15c_local_path_relational_comparisons() -> tuple[Stage15CLocalPathRelationalComparison, ...]:
    result: list[Stage15CLocalPathRelationalComparison] = []
    target_lookups = {
        orbit.orbit_id: {(rep.T0, rep.T1, rep.T2): rep for rep in canonical_stage15a_representatives_for_orbit(orbit)}
        for orbit in canonical_stage15a_orbits()
    }
    for pair in canonical_stage15b_local_pairs():
        endpoint_012 = _stage15c_local_compensated_endpoint(pair, STAGE15B_PATH_012)
        endpoint_102 = _stage15c_local_compensated_endpoint(pair, STAGE15B_PATH_102)
        QD_012, _ = stage15c_reconstruct_dirac_from_point(endpoint_012)
        QD_102, _ = stage15c_reconstruct_dirac_from_point(endpoint_102)
        endpoint_residual = _phase_space_residual(endpoint_012, endpoint_102)
        for tau0, tau1, tau2 in product(STAGE15A_GRID_VALUES, repeat=3):
            Q_012 = stage15c_complete_relational_value(QD_012, tau0, tau1, tau2)
            Q_102 = stage15c_complete_relational_value(QD_102, tau0, tau1, tau2)
            target = target_lookups[pair.orbit_id][(float(tau0), float(tau1), float(tau2))]
            result.append(
                Stage15CLocalPathRelationalComparison(
                    pair_id=pair.pair_id,
                    orbit_id=pair.orbit_id,
                    tau0=float(tau0), tau1=float(tau1), tau2=float(tau2),
                    Q_012=Q_012,
                    Q_102=Q_102,
                    Q_target=float(target.Q),
                    endpoint_order_residual=endpoint_residual,
                    relational_order_residual=abs(Q_012 - Q_102),
                    path_012_target_residual=abs(Q_012 - target.Q),
                    path_102_target_residual=abs(Q_102 - target.Q),
                    classification=STAGE15C_LOCAL_PATH_COVARIANCE,
                    metaphysical_claim_status=STAGE15C_METAPHYSICAL_CLAIM_STATUS,
                )
            )
    return tuple(result)


@lru_cache(maxsize=1)
def canonical_stage15c_smeared_path_relational_comparisons() -> tuple[Stage15CSmearedPathRelationalComparison, ...]:
    result: list[Stage15CSmearedPathRelationalComparison] = []
    orbit_by_id = {orbit.orbit_id: orbit for orbit in canonical_stage15a_orbits()}
    target_lookups = {
        orbit.orbit_id: {(rep.T0, rep.T1, rep.T2): rep for rep in canonical_stage15a_representatives_for_orbit(orbit)}
        for orbit in canonical_stage15a_orbits()
    }
    for rep in canonical_stage15a_representatives():
        source = rep.point()
        orbit_id = rep.orbit_id
        _ = orbit_by_id[orbit_id]
        for case_id, N, M, alpha, beta, _nontrivial_expected in STAGE15B_SMEARED_CASES:
            path_nm = stage15b_apply_smeared_flow(stage15b_apply_smeared_flow(source, N, alpha), M, beta)
            path_mn = stage15b_apply_smeared_flow(stage15b_apply_smeared_flow(source, M, beta), N, alpha)
            predicted = stage15b_expected_smeared_c2_defect(source, N, M, alpha, beta)
            compensated_mn = stage15b_apply_local_flow(path_mn, 2, predicted)
            endpoint_residual = _phase_space_residual(path_nm, compensated_mn)
            QD_nm, _ = stage15c_reconstruct_dirac_from_point(path_nm)
            QD_mn, _ = stage15c_reconstruct_dirac_from_point(compensated_mn)
            for tau0, tau1, tau2 in product(STAGE15A_GRID_VALUES, repeat=3):
                Q_nm = stage15c_complete_relational_value(QD_nm, tau0, tau1, tau2)
                Q_mn = stage15c_complete_relational_value(QD_mn, tau0, tau1, tau2)
                target = target_lookups[orbit_id][(float(tau0), float(tau1), float(tau2))]
                result.append(
                    Stage15CSmearedPathRelationalComparison(
                        representative_id=rep.representative_id,
                        orbit_id=orbit_id,
                        case_id=case_id,
                        tau0=float(tau0), tau1=float(tau1), tau2=float(tau2),
                        predicted_compensator=float(predicted),
                        endpoint_residual=endpoint_residual,
                        Q_nm=Q_nm,
                        Q_compensated_mn=Q_mn,
                        Q_target=float(target.Q),
                        relational_order_residual=abs(Q_nm - Q_mn),
                        nm_target_residual=abs(Q_nm - target.Q),
                        compensated_target_residual=abs(Q_mn - target.Q),
                        classification=STAGE15C_SMEARED_PATH_COVARIANCE,
                        metaphysical_claim_status=STAGE15C_METAPHYSICAL_CLAIM_STATUS,
                    )
                )
    return tuple(result)


@lru_cache(maxsize=1)
def canonical_stage15c_omitted_clock_evaluations() -> tuple[Stage15COmittedClockEvaluation, ...]:
    summaries = {item.orbit_id: item for item in stage15c_orbit_dirac_summaries()}
    c = STAGE15A_C
    result: list[Stage15COmittedClockEvaluation] = []
    for orbit in canonical_stage15a_orbits():
        Q_D = summaries[orbit.orbit_id].Q_D_mean
        for omitted in range(3):
            specified = [index for index in range(3) if index != omitted]
            for tau_a, tau_b in product(STAGE15A_GRID_VALUES, repeat=2):
                fixed = {specified[0]: float(tau_a), specified[1]: float(tau_b)}
                for raw_omitted in STAGE15A_GRID_VALUES:
                    values: list[float | None] = [None, None, None]
                    values[specified[0]] = float(tau_a)
                    values[specified[1]] = float(tau_b)
                    effective = [0.0, 0.0, 0.0]
                    for index in range(3):
                        effective[index] = float(raw_omitted) if index == omitted else fixed[index]
                    Q_incomplete = float(Q_D + sum(c[index] * effective[index] for index in range(3)))
                    result.append(
                        Stage15COmittedClockEvaluation(
                            orbit_id=orbit.orbit_id,
                            omitted_clock_index=omitted,
                            tau0=values[0], tau1=values[1], tau2=values[2],
                            raw_omitted_clock=float(raw_omitted),
                            Q_incomplete=Q_incomplete,
                            role=STAGE15C_OMITTED_CLOCK_ROLE,
                            classification=STAGE15C_OMITTED_CLOCK_CLASSIFICATION,
                            metaphysical_claim_status=STAGE15C_METAPHYSICAL_CLAIM_STATUS,
                        )
                    )
    return tuple(result)


@lru_cache(maxsize=1)
def stage15c_omitted_clock_group_spreads() -> tuple[tuple[str, int, tuple[float, float], float], ...]:
    evaluations = canonical_stage15c_omitted_clock_evaluations()
    result: list[tuple[str, int, tuple[float, float], float]] = []
    for orbit in canonical_stage15a_orbits():
        for omitted in range(3):
            specified = [index for index in range(3) if index != omitted]
            for tau_a, tau_b in product(STAGE15A_GRID_VALUES, repeat=2):
                fixed = (float(tau_a), float(tau_b))
                values = []
                for item in evaluations:
                    if item.orbit_id != orbit.orbit_id or item.omitted_clock_index != omitted:
                        continue
                    taus = (item.tau0, item.tau1, item.tau2)
                    if taus[specified[0]] == fixed[0] and taus[specified[1]] == fixed[1]:
                        values.append(item.Q_incomplete)
                result.append((orbit.orbit_id, omitted, fixed, float(max(values) - min(values))))
    return tuple(result)


@lru_cache(maxsize=1)
def canonical_stage15c_raw_Q_evaluations() -> tuple[Stage15CRawQEvaluation, ...]:
    return tuple(
        Stage15CRawQEvaluation(
            orbit_id=rep.orbit_id,
            representative_id=rep.representative_id,
            raw_Q=float(rep.Q),
            role=STAGE15C_RAW_Q_ROLE,
            classification=STAGE15C_RAW_Q_CLASSIFICATION,
            metaphysical_claim_status=STAGE15C_METAPHYSICAL_CLAIM_STATUS,
        )
        for rep in canonical_stage15a_representatives()
    )


@lru_cache(maxsize=1)
def stage15c_raw_Q_spreads() -> tuple[tuple[str, float], ...]:
    evaluations = canonical_stage15c_raw_Q_evaluations()
    result = []
    for orbit in canonical_stage15a_orbits():
        values = [item.raw_Q for item in evaluations if item.orbit_id == orbit.orbit_id]
        result.append((orbit.orbit_id, float(max(values) - min(values))))
    return tuple(result)


@lru_cache(maxsize=1)
def stage15c_quotient_classes() -> tuple[Stage15CQuotientClass, ...]:
    grouped: dict[tuple[float, float], list[Stage15CDiracEstimate]] = {}
    for item in canonical_stage15c_dirac_estimates():
        grouped.setdefault((round(item.Q_D, 12), round(item.P_D, 12)), []).append(item)
    result: list[Stage15CQuotientClass] = []
    for index, ((Q_D, P_D), members) in enumerate(sorted(grouped.items()), start=1):
        result.append(
            Stage15CQuotientClass(
                class_id=f"stage15c_quotient_{index}",
                Q_D=float(Q_D),
                P_D=float(P_D),
                member_representative_ids=tuple(sorted(item.representative_id for item in members)),
                member_orbit_ids=tuple(sorted({item.orbit_id for item in members})),
                classification=STAGE15C_QUOTIENT_CLASSIFICATION,
                metaphysical_claim_status=STAGE15C_METAPHYSICAL_CLAIM_STATUS,
            )
        )
    return tuple(result)


def stage15c_cross_orbit_arrow_audit() -> tuple[int, int]:
    reps = canonical_stage15a_representatives()
    licensed = 0
    rejected = 0
    for source in reps:
        for target in reps:
            if source.orbit_id == target.orbit_id:
                continue
            try:
                stage15b_make_local_pair(source, target)
            except ValueError:
                rejected += 1
            else:
                licensed += 1
    return licensed, rejected


@lru_cache(maxsize=1)
def stage15c_diagnostics() -> Stage15CDiagnostics:
    reps = canonical_stage15a_representatives()
    estimates = canonical_stage15c_dirac_estimates()
    summaries = stage15c_orbit_dirac_summaries()
    orbit_pairs = stage15c_orbit_pair_discriminations()
    complete = canonical_stage15c_complete_relational_evaluations()
    complete_spreads = stage15c_complete_relational_spreads()
    local_pairs = canonical_stage15b_local_pairs()
    local = canonical_stage15c_local_path_relational_comparisons()
    smeared = canonical_stage15c_smeared_path_relational_comparisons()
    omitted = canonical_stage15c_omitted_clock_evaluations()
    omitted_spreads = stage15c_omitted_clock_group_spreads()
    raw_Q = canonical_stage15c_raw_Q_evaluations()
    raw_Q_spreads = stage15c_raw_Q_spreads()
    quotient = stage15c_quotient_classes()
    licensed_cross, rejected_cross = stage15c_cross_orbit_arrow_audit()

    all_commutation_points = tuple(rep.point() for rep in reps) + canonical_stage15a_off_surface_probes()
    all_bracket_residuals = [value for point in all_commutation_points for value in stage15c_dirac_bracket_residuals(point)]
    max_bracket = float(max(all_bracket_residuals, default=0.0))
    strong_commutation = len(all_commutation_points) == 216 and max_bracket <= STAGE15A_ATOL

    same_p_diff_q = [item for item in orbit_pairs if item.same_P_different_Q]
    same_q_diff_p = [item for item in orbit_pairs if item.same_Q_different_P]
    nontrivial_change = all(spread > STAGE15A_ATOL for _, spread in complete_spreads)

    max_local_endpoint = max(item.endpoint_order_residual for item in local)
    max_local_relational = max(
        max(item.relational_order_residual, item.path_012_target_residual, item.path_102_target_residual)
        for item in local
    )
    local_descent = (
        len(local_pairs) == 864
        and len(local) == 23328
        and max_local_endpoint <= STAGE15A_ATOL
        and max_local_relational <= STAGE15A_ATOL
    )

    max_smeared_endpoint = max(item.endpoint_residual for item in smeared)
    max_smeared_relational = max(
        max(item.relational_order_residual, item.nm_target_residual, item.compensated_target_residual)
        for item in smeared
    )
    smeared_descent = (
        len(smeared) == 14580
        and len({(item.representative_id, item.case_id) for item in smeared}) == 540
        and max_smeared_endpoint <= STAGE15A_ATOL
        and max_smeared_relational <= STAGE15A_ATOL
    )

    incomplete_groups = [item for item in omitted_spreads if item[3] > STAGE15A_ATOL]
    omitted_by_index = tuple(
        float(min(item[3] for item in omitted_spreads if item[1] == index))
        for index in range(3)
    )
    omitted_incomplete = (
        len(omitted) == 324
        and len(omitted_spreads) == 108
        and len(incomplete_groups) == 108
        and all(abs(observed - expected) <= STAGE15A_ATOL for observed, expected in zip(omitted_by_index, (2.0, 1.0, 0.5), strict=True))
    )
    raw_nondescending = all(spread > STAGE15A_ATOL for _, spread in raw_Q_spreads)

    quotient_exact = (
        len(quotient) == 4
        and all(len(item.member_representative_ids) == 27 for item in quotient)
        and all(len(item.member_orbit_ids) == 1 for item in quotient)
        and licensed_cross == 0
        and rejected_cross == 8748
    )

    metaphysical_objects = (*estimates, *orbit_pairs, *complete, *local, *smeared, *omitted, *raw_Q, *quotient)
    metaphysical_boundary = all(
        item.metaphysical_claim_status == STAGE15C_METAPHYSICAL_CLAIM_STATUS
        for item in metaphysical_objects
    )

    max_complete_target = max(item.target_residual for item in complete)
    criteria = (
        len(reps) == 108
        and len(estimates) == 108
        and len(summaries) == 4
        and all(item.representative_count == 27 for item in summaries)
        and max(item.Q_declared_residual for item in estimates) <= STAGE15A_ATOL
        and max(item.P_declared_residual for item in estimates) <= STAGE15A_ATOL
        and max(item.Q_D_spread for item in summaries) <= STAGE15A_ATOL
        and max(item.P_D_spread for item in summaries) <= STAGE15A_ATOL
        and strong_commutation
        and len(orbit_pairs) == 6
        and all(item.physically_distinct for item in orbit_pairs)
        and len(same_p_diff_q) == 1
        and len(same_q_diff_p) == 1
        and len(complete) == 2916
        and max_complete_target <= STAGE15A_ATOL
        and nontrivial_change
        and local_descent
        and smeared_descent
        and omitted_incomplete
        and len(raw_Q) == 108
        and len(raw_Q_spreads) == 4
        and raw_nondescending
        and quotient_exact
        and metaphysical_boundary
    )

    return Stage15CDiagnostics(
        representative_count=len(reps),
        dirac_estimate_count=len(estimates),
        strong_commutation_probe_count=len(all_commutation_points),
        orbit_summary_count=len(summaries),
        distinct_orbit_pair_count=len(orbit_pairs),
        physically_distinct_pair_count=sum(item.physically_distinct for item in orbit_pairs),
        complete_relational_evaluation_count=len(complete),
        local_compensated_pair_count=len(local_pairs),
        local_relational_comparison_count=len(local),
        smeared_ordering_count=len({(item.representative_id, item.case_id) for item in smeared}),
        smeared_relational_comparison_count=len(smeared),
        omitted_clock_evaluation_count=len(omitted),
        omitted_clock_group_count=len(omitted_spreads),
        omitted_clock_incomplete_group_count=len(incomplete_groups),
        raw_Q_evaluation_count=len(raw_Q),
        raw_Q_group_count=len(raw_Q_spreads),
        raw_Q_nondescending_group_count=sum(spread > STAGE15A_ATOL for _, spread in raw_Q_spreads),
        quotient_class_count=len(quotient),
        min_quotient_class_size=min(len(item.member_representative_ids) for item in quotient),
        max_quotient_class_size=max(len(item.member_representative_ids) for item in quotient),
        cross_orbit_licensed_arrow_count=licensed_cross,
        cross_orbit_rejected_count=rejected_cross,
        same_P_different_Q_control_count=len(same_p_diff_q),
        same_Q_different_P_control_count=len(same_q_diff_p),
        max_Q_declared_residual=float(max(item.Q_declared_residual for item in estimates)),
        max_P_declared_residual=float(max(item.P_declared_residual for item in estimates)),
        max_dirac_bracket_residual=max_bracket,
        max_same_orbit_Q_spread=float(max(item.Q_D_spread for item in summaries)),
        max_same_orbit_P_spread=float(max(item.P_D_spread for item in summaries)),
        min_distinct_orbit_full_pair_separation=float(min(item.full_pair_separation for item in orbit_pairs)),
        max_complete_relational_target_residual=float(max_complete_target),
        max_local_endpoint_order_residual=float(max_local_endpoint),
        max_local_relational_residual=float(max_local_relational),
        max_smeared_endpoint_residual=float(max_smeared_endpoint),
        max_smeared_relational_residual=float(max_smeared_relational),
        min_complete_relational_spread=float(min(spread for _, spread in complete_spreads)),
        max_complete_relational_spread=float(max(spread for _, spread in complete_spreads)),
        omitted_clock_spreads=omitted_by_index,
        min_raw_Q_spread=float(min(spread for _, spread in raw_Q_spreads)),
        max_raw_Q_spread=float(max(spread for _, spread in raw_Q_spreads)),
        strong_dirac_commutation_established=strong_commutation,
        nontrivial_complete_relational_change=nontrivial_change,
        local_path_relational_descent_established=local_descent,
        smeared_path_relational_descent_established=smeared_descent,
        omitted_clock_incompleteness_explicit=omitted_incomplete,
        raw_coordinate_non_descent_explicit=raw_nondescending,
        quotient_exactly_four_by_twenty_seven=quotient_exact,
        metaphysical_boundary_explicit=metaphysical_boundary,
        criteria_25_31_satisfied=criteria,
    )
