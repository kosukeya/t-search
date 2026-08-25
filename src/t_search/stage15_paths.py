"""Stage 15B finite local/smeared path closure and compensation.

This module consumes the validated Stage 15A spatially indexed carrier and
implements only the Stage 15B path evidence frozen in ``docs/stage15_protocol.md``.
It integrates the declared local and constant-smeared generators exactly on the
positive constraint surface, compares noncommuting path orderings, and checks
that the algebraically predicted C2 compensation restores the same tested
endpoint.  Off-surface smeared Jacobi cancellation is checked separately from
the positive finite-flow formulas.

Complete quotient/Dirac-observable claims are deferred to Stage 15C.  Basis
locality/Abelianization claims are deferred to Stage 15D.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations

import numpy as np

from .stage15_local import (
    STAGE15A_ATOL,
    STAGE15A_C,
    STAGE15A_KAPPA,
    Stage15PhaseSpacePoint,
    Stage15Representative,
    canonical_stage15a_off_surface_probes,
    canonical_stage15a_orbits,
    canonical_stage15a_representatives,
    canonical_stage15a_representatives_for_orbit,
    stage15a_constraints,
    stage15a_dirac_data,
    stage15a_smeared_gradient,
)

STAGE15B_PATH_012 = "012"
STAGE15B_PATH_102 = "102"
STAGE15B_FLOW_PARAMETERS = (-0.5, 0.5)

STAGE15B_SMEAR_01 = (1.0, -0.5, 0.0)
STAGE15B_SMEAR_12 = (0.0, 1.0, -0.5)
STAGE15B_SMEAR_FULL_A = (1.0, -0.5, 0.25)
STAGE15B_SMEAR_FULL_B = (-0.25, 0.75, 1.0)
STAGE15B_SMEAR_PARALLEL_PLUS_C2 = (2.0, -1.0, 1.0)

STAGE15B_SMEARED_CASES = (
    (
        "compact01_vs_compact12",
        STAGE15B_SMEAR_01,
        STAGE15B_SMEAR_12,
        0.5,
        0.5,
        True,
    ),
    (
        "compact01_vs_full",
        STAGE15B_SMEAR_01,
        STAGE15B_SMEAR_FULL_B,
        0.5,
        0.5,
        True,
    ),
    (
        "compact12_vs_full",
        STAGE15B_SMEAR_12,
        STAGE15B_SMEAR_FULL_A,
        0.5,
        0.5,
        True,
    ),
    (
        "full_vs_full",
        STAGE15B_SMEAR_FULL_A,
        STAGE15B_SMEAR_FULL_B,
        0.5,
        0.5,
        True,
    ),
    (
        "parallel_plus_c2_zero_wedge",
        STAGE15B_SMEAR_01,
        STAGE15B_SMEAR_PARALLEL_PLUS_C2,
        0.5,
        0.5,
        False,
    ),
)

STAGE15B_JACOBI_SMEARINGS = (
    STAGE15B_SMEAR_01,
    STAGE15B_SMEAR_12,
    STAGE15B_SMEAR_FULL_A,
    STAGE15B_SMEAR_FULL_B,
)


@dataclass(frozen=True, slots=True)
class Stage15BLocalPair:
    pair_id: str
    orbit_id: str
    source: Stage15Representative
    target: Stage15Representative
    s: float
    delta_0_to_1: float
    u: float
    v_012: float
    v_102: float
    compensator_difference: float
    expected_compensator_difference: float


@dataclass(frozen=True, slots=True)
class Stage15BLocalPathResult:
    pair_id: str
    path_word: str
    compensator: float
    raw_formula_residual: float
    final_endpoint_residual: float
    final_payload_residual: float
    final_relational_residual: float


@dataclass(frozen=True, slots=True)
class Stage15BSmearedOrderProbe:
    representative_id: str
    case_id: str
    N: tuple[float, float, float]
    M: tuple[float, float, float]
    alpha: float
    beta: float
    observed_c2_defect: float
    expected_c2_defect: float
    c2_only_residual: float
    compensated_endpoint_residual: float
    payload_residual: float
    nontrivial_expected: bool


@dataclass(frozen=True, slots=True)
class Stage15BDiagnostics:
    orbit_count: int
    representative_count: int
    single_local_flow_probe_count: int
    single_smeared_flow_probe_count: int
    local_pair_count: int
    local_path_result_count: int
    local_nonzero_order_defect_count: int
    local_zero_order_defect_count: int
    local_wrong_sign_rejected_count: int
    local_wrong_half_rejected_count: int
    local_missing_rejected_count: int
    local_shared_compensator_rejected_count: int
    local_shared_compensator_zero_defect_compatible_count: int
    smeared_order_probe_count: int
    smeared_nonzero_order_defect_count: int
    smeared_zero_order_defect_count: int
    smeared_wrong_sign_rejected_count: int
    smeared_missing_rejected_count: int
    smeared_jacobi_probe_count: int
    max_single_flow_constraint_residual: float
    max_single_flow_payload_residual: float
    max_local_compensator_identity_residual: float
    max_local_raw_formula_residual: float
    max_local_endpoint_residual: float
    max_local_payload_residual: float
    max_local_relational_residual: float
    max_smeared_compensator_identity_residual: float
    max_smeared_c2_only_residual: float
    max_smeared_endpoint_residual: float
    max_smeared_payload_residual: float
    max_smeared_jacobi_residual: float
    max_smeared_jacobi_term_magnitude: float
    exact_finite_flows_established: bool
    local_compensated_path_closure_established: bool
    local_order_defect_detected: bool
    local_controls_detected: bool
    smeared_compensated_path_closure_established: bool
    smeared_order_defect_detected: bool
    smeared_zero_wedge_control_exact: bool
    smeared_jacobi_established_off_surface: bool
    criteria_18_24_satisfied: bool


def _phase_space_residual(a: Stage15PhaseSpacePoint, b: Stage15PhaseSpacePoint) -> float:
    return float(max(abs(x - y) for x, y in zip(a.vector(), b.vector(), strict=True)))


def _payload_residual(a: Stage15PhaseSpacePoint, b: Stage15PhaseSpacePoint) -> float:
    qa, pa = stage15a_dirac_data(a)
    qb, pb = stage15a_dirac_data(b)
    return float(max(abs(qa - qb), abs(pa - pb)))


def _constraint_residual(point: Stage15PhaseSpacePoint) -> float:
    return float(max(abs(value) for value in stage15a_constraints(point)))


def _require_on_surface(point: Stage15PhaseSpacePoint) -> None:
    if _constraint_residual(point) > STAGE15A_ATOL:
        raise ValueError("Stage 15B exact finite path formulas require an on-surface source")


def _point_with_clocks(
    source: Stage15PhaseSpacePoint,
    T0: float,
    T1: float,
    T2: float,
) -> Stage15PhaseSpacePoint:
    """Return the same tested physical payload at the requested clock values."""

    Q_D, P_D = stage15a_dirac_data(source)
    c0, c1, c2 = STAGE15A_C
    return Stage15PhaseSpacePoint(
        Q=float(Q_D + c0 * T0 + c1 * T1 + c2 * T2),
        P=float(P_D),
        T0=float(T0),
        pi0=float(-c0 * P_D),
        T1=float(T1),
        pi1=float(-c1 * P_D),
        T2=float(T2),
        pi2=float(-c2 * P_D),
    )


def stage15b_apply_local_flow(
    point: Stage15PhaseSpacePoint,
    generator_index: int,
    parameter: float,
) -> Stage15PhaseSpacePoint:
    """Exact positive-surface flow of C0, C1, or C2.

    The formulas are derived from the Hamiltonian vector fields after imposing
    the positive constraint surface.  They are deliberately rejected off the
    surface rather than being promoted to a general integration rule.
    """

    _require_on_surface(point)
    parameter = float(parameter)
    kappa = STAGE15A_KAPPA

    if generator_index == 0:
        T0 = float(point.T0 + parameter)
        T1 = float(
            point.T1
            + kappa * (point.T0 * parameter + 0.5 * parameter**2)
        )
        return _point_with_clocks(point, T0, T1, point.T2)

    if generator_index == 1:
        T1 = float(point.T1 + parameter)
        T2 = float(
            point.T2
            + kappa * (point.T1 * parameter + 0.5 * parameter**2)
        )
        return _point_with_clocks(point, point.T0, T1, T2)

    if generator_index == 2:
        return _point_with_clocks(
            point, point.T0, point.T1, float(point.T2 + parameter)
        )

    raise ValueError(f"unknown Stage 15B local generator index: {generator_index}")


def stage15b_apply_smeared_flow(
    point: Stage15PhaseSpacePoint,
    smearing: tuple[float, float, float],
    parameter: float,
) -> Stage15PhaseSpacePoint:
    """Exact positive-surface flow of a constant smearing C[N]."""

    _require_on_surface(point)
    n0, n1, n2 = (float(value) for value in smearing)
    lam = float(parameter)
    kappa = STAGE15A_KAPPA

    T0 = float(point.T0 + n0 * lam)
    T1 = float(
        point.T1
        + n1 * lam
        + kappa * n0 * (point.T0 * lam + 0.5 * n0 * lam**2)
    )
    T2 = float(
        point.T2
        + n2 * lam
        + kappa
        * n1
        * (
            point.T1 * lam
            + 0.5 * (n1 + kappa * n0 * point.T0) * lam**2
            + (kappa * n0**2 * lam**3) / 6.0
        )
    )
    return _point_with_clocks(point, T0, T1, T2)


def stage15b_relational_endpoint_value(point: Stage15PhaseSpacePoint) -> float:
    """Stage 15B endpoint comparator, not a Stage 15C Dirac theorem.

    On the carried positive surface the expression equals the declared Q_D.
    Stage 15C still owns the general Poisson/quotient descent claims.
    """

    return float(stage15a_dirac_data(point)[0])


def stage15b_make_local_pair(
    source: Stage15Representative,
    target: Stage15Representative,
) -> Stage15BLocalPair:
    if source.orbit_id != target.orbit_id:
        raise ValueError("Stage 15B licensed local paths cannot connect distinct physical orbits")
    if source.representative_id == target.representative_id:
        raise ValueError("Stage 15B local mixed paths require distinct source and target")
    if (
        abs(source.T0 - target.T0) <= STAGE15A_ATOL
        or abs(source.T1 - target.T1) <= STAGE15A_ATOL
        or abs(source.T2 - target.T2) <= STAGE15A_ATOL
    ):
        raise ValueError(
            "Stage 15B canonical local pair requires T0, T1, and T2 all to change"
        )

    kappa = STAGE15A_KAPPA
    s = float(target.T0 - source.T0)
    delta = float(kappa * (source.T0 * s + 0.5 * s**2))
    u = float(target.T1 - source.T1 - delta)

    raw_012_T2 = float(
        source.T2
        + kappa * ((source.T1 + delta) * u + 0.5 * u**2)
    )
    raw_102_T2 = float(
        source.T2 + kappa * (source.T1 * u + 0.5 * u**2)
    )
    v_012 = float(target.T2 - raw_012_T2)
    v_102 = float(target.T2 - raw_102_T2)
    expected_difference = float(
        (kappa**2) * u * (source.T0 * s + 0.5 * s**2)
    )

    return Stage15BLocalPair(
        pair_id=f"{source.representative_id}->{target.representative_id}",
        orbit_id=source.orbit_id,
        source=source,
        target=target,
        s=s,
        delta_0_to_1=delta,
        u=u,
        v_012=v_012,
        v_102=v_102,
        compensator_difference=float(v_102 - v_012),
        expected_compensator_difference=expected_difference,
    )


def canonical_stage15b_local_pairs() -> tuple[Stage15BLocalPair, ...]:
    result: list[Stage15BLocalPair] = []
    for orbit in canonical_stage15a_orbits():
        reps = canonical_stage15a_representatives_for_orbit(orbit)
        for source in reps:
            for target in reps:
                if source.representative_id == target.representative_id:
                    continue
                if (
                    abs(source.T0 - target.T0) > STAGE15A_ATOL
                    and abs(source.T1 - target.T1) > STAGE15A_ATOL
                    and abs(source.T2 - target.T2) > STAGE15A_ATOL
                ):
                    result.append(stage15b_make_local_pair(source, target))
    return tuple(result)


def _local_raw_path(
    pair: Stage15BLocalPair, path_word: str
) -> Stage15PhaseSpacePoint:
    source = pair.source.point()
    if path_word == STAGE15B_PATH_012:
        after_0 = stage15b_apply_local_flow(source, 0, pair.s)
        return stage15b_apply_local_flow(after_0, 1, pair.u)
    if path_word == STAGE15B_PATH_102:
        after_1 = stage15b_apply_local_flow(source, 1, pair.u)
        return stage15b_apply_local_flow(after_1, 0, pair.s)
    raise ValueError(f"unknown Stage 15B local path word: {path_word}")


def _expected_local_raw_endpoint(
    pair: Stage15BLocalPair, path_word: str
) -> Stage15PhaseSpacePoint:
    source = pair.source.point()
    kappa = STAGE15A_KAPPA
    T0 = float(source.T0 + pair.s)
    T1 = float(source.T1 + pair.delta_0_to_1 + pair.u)
    if path_word == STAGE15B_PATH_012:
        T2 = float(
            source.T2
            + kappa
            * (
                (source.T1 + pair.delta_0_to_1) * pair.u
                + 0.5 * pair.u**2
            )
        )
    elif path_word == STAGE15B_PATH_102:
        T2 = float(
            source.T2
            + kappa * (source.T1 * pair.u + 0.5 * pair.u**2)
        )
    else:
        raise ValueError(f"unknown Stage 15B local path word: {path_word}")
    return _point_with_clocks(source, T0, T1, T2)


def stage15b_apply_local_path(
    pair: Stage15BLocalPair,
    path_word: str,
    *,
    compensator: float | None = None,
) -> Stage15BLocalPathResult:
    raw = _local_raw_path(pair, path_word)
    expected_raw = _expected_local_raw_endpoint(pair, path_word)
    if compensator is None:
        compensator = (
            pair.v_012 if path_word == STAGE15B_PATH_012 else pair.v_102
        )
    final = stage15b_apply_local_flow(raw, 2, float(compensator))
    target = pair.target.point()
    return Stage15BLocalPathResult(
        pair_id=pair.pair_id,
        path_word=path_word,
        compensator=float(compensator),
        raw_formula_residual=_phase_space_residual(raw, expected_raw),
        final_endpoint_residual=_phase_space_residual(final, target),
        final_payload_residual=_payload_residual(final, target),
        final_relational_residual=abs(
            stage15b_relational_endpoint_value(final)
            - stage15b_relational_endpoint_value(target)
        ),
    )


def canonical_stage15b_local_path_results() -> tuple[Stage15BLocalPathResult, ...]:
    return tuple(
        result
        for pair in canonical_stage15b_local_pairs()
        for result in (
            stage15b_apply_local_path(pair, STAGE15B_PATH_012),
            stage15b_apply_local_path(pair, STAGE15B_PATH_102),
        )
    )


def _smearing_wedge(
    N: tuple[float, float, float], M: tuple[float, float, float]
) -> float:
    return float(N[0] * M[1] - N[1] * M[0])


def stage15b_expected_smeared_c2_defect(
    source: Stage15PhaseSpacePoint,
    N: tuple[float, float, float],
    M: tuple[float, float, float],
    alpha: float,
    beta: float,
) -> float:
    """Integrated C2 defect for N(alpha) then M(beta) minus the reverse."""

    alpha = float(alpha)
    beta = float(beta)
    wedge = _smearing_wedge(N, M)
    return float(
        alpha
        * beta
        * (STAGE15A_KAPPA**2)
        * wedge
        * (source.T0 + 0.5 * (alpha * N[0] + beta * M[0]))
    )


def stage15b_make_smeared_order_probe(
    representative: Stage15Representative,
    case: tuple[
        str,
        tuple[float, float, float],
        tuple[float, float, float],
        float,
        float,
        bool,
    ],
) -> Stage15BSmearedOrderProbe:
    case_id, N, M, alpha, beta, nontrivial_expected = case
    source = representative.point()
    path_nm = stage15b_apply_smeared_flow(
        stage15b_apply_smeared_flow(source, N, alpha), M, beta
    )
    path_mn = stage15b_apply_smeared_flow(
        stage15b_apply_smeared_flow(source, M, beta), N, alpha
    )

    observed = float(path_nm.T2 - path_mn.T2)
    expected = stage15b_expected_smeared_c2_defect(source, N, M, alpha, beta)

    c2_projection = stage15b_apply_local_flow(path_mn, 2, observed)
    c2_only_residual = _phase_space_residual(c2_projection, path_nm)
    compensated = c2_projection
    payload_residual = _payload_residual(compensated, path_nm)

    return Stage15BSmearedOrderProbe(
        representative_id=representative.representative_id,
        case_id=case_id,
        N=N,
        M=M,
        alpha=float(alpha),
        beta=float(beta),
        observed_c2_defect=observed,
        expected_c2_defect=expected,
        c2_only_residual=c2_only_residual,
        compensated_endpoint_residual=_phase_space_residual(compensated, path_nm),
        payload_residual=payload_residual,
        nontrivial_expected=bool(nontrivial_expected),
    )


def canonical_stage15b_smeared_order_probes() -> tuple[Stage15BSmearedOrderProbe, ...]:
    return tuple(
        stage15b_make_smeared_order_probe(rep, case)
        for rep in canonical_stage15a_representatives()
        for case in STAGE15B_SMEARED_CASES
    )


def _poisson_from_gradients(df: np.ndarray, dg: np.ndarray) -> float:
    return float(
        sum(
            df[q_index] * dg[p_index] - df[p_index] * dg[q_index]
            for q_index, p_index in ((0, 1), (2, 3), (4, 5), (6, 7))
        )
    )


def _smeared_inner_bracket_gradient(
    point: Stage15PhaseSpacePoint,
    N: tuple[float, float, float],
    M: tuple[float, float, float],
) -> np.ndarray:
    """Gradient of {C[N],C[M]}=f*w*C2 on the full carrier."""

    c2 = STAGE15A_C[2]
    k2 = STAGE15A_KAPPA**2
    wedge = _smearing_wedge(N, M)
    C2 = stage15a_constraints(point)[2]
    f = float(-k2 * point.T0)
    return np.asarray(
        [
            0.0,
            f * wedge * c2,
            -k2 * wedge * C2,
            0.0,
            0.0,
            0.0,
            0.0,
            f * wedge,
        ],
        dtype=float,
    )


def stage15b_smeared_nested_bracket(
    point: Stage15PhaseSpacePoint,
    L: tuple[float, float, float],
    N: tuple[float, float, float],
    M: tuple[float, float, float],
) -> float:
    return _poisson_from_gradients(
        stage15a_smeared_gradient(point, L),
        _smeared_inner_bracket_gradient(point, N, M),
    )


def stage15b_smeared_jacobi_residual(
    point: Stage15PhaseSpacePoint,
    L: tuple[float, float, float],
    N: tuple[float, float, float],
    M: tuple[float, float, float],
) -> float:
    return float(
        stage15b_smeared_nested_bracket(point, L, N, M)
        + stage15b_smeared_nested_bracket(point, N, M, L)
        + stage15b_smeared_nested_bracket(point, M, L, N)
    )


def stage15b_diagnostics() -> Stage15BDiagnostics:
    reps = canonical_stage15a_representatives()

    max_single_constraint = 0.0
    max_single_payload = 0.0
    single_local_count = 0
    for rep in reps:
        source = rep.point()
        for generator_index in range(3):
            for parameter in STAGE15B_FLOW_PARAMETERS:
                target = stage15b_apply_local_flow(source, generator_index, parameter)
                single_local_count += 1
                max_single_constraint = max(
                    max_single_constraint, _constraint_residual(target)
                )
                max_single_payload = max(
                    max_single_payload, _payload_residual(source, target)
                )

    unique_smearings = (
        STAGE15B_SMEAR_01,
        STAGE15B_SMEAR_12,
        STAGE15B_SMEAR_FULL_A,
        STAGE15B_SMEAR_FULL_B,
    )
    single_smeared_count = 0
    for rep in reps:
        source = rep.point()
        for smearing in unique_smearings:
            for parameter in STAGE15B_FLOW_PARAMETERS:
                target = stage15b_apply_smeared_flow(source, smearing, parameter)
                single_smeared_count += 1
                max_single_constraint = max(
                    max_single_constraint, _constraint_residual(target)
                )
                max_single_payload = max(
                    max_single_payload, _payload_residual(source, target)
                )

    local_pairs = canonical_stage15b_local_pairs()
    local_results = canonical_stage15b_local_path_results()
    local_differences = [abs(pair.compensator_difference) for pair in local_pairs]
    local_nonzero = [value for value in local_differences if value > STAGE15A_ATOL]
    local_zero = [value for value in local_differences if value <= STAGE15A_ATOL]

    max_local_identity = max(
        abs(pair.compensator_difference - pair.expected_compensator_difference)
        for pair in local_pairs
    )
    max_local_raw = max(result.raw_formula_residual for result in local_results)
    max_local_endpoint = max(result.final_endpoint_residual for result in local_results)
    max_local_payload = max(result.final_payload_residual for result in local_results)
    max_local_relational = max(
        result.final_relational_residual for result in local_results
    )

    local_wrong_sign = 0
    local_wrong_half = 0
    local_missing = 0
    shared_rejected = 0
    shared_compatible = 0
    for pair in local_pairs:
        raw_012 = _local_raw_path(pair, STAGE15B_PATH_012)
        raw_102 = _local_raw_path(pair, STAGE15B_PATH_102)
        target = pair.target.point()
        for raw, correct_v in ((raw_012, pair.v_012), (raw_102, pair.v_102)):
            if _phase_space_residual(
                stage15b_apply_local_flow(raw, 2, -correct_v), target
            ) > STAGE15A_ATOL:
                local_wrong_sign += 1
            if _phase_space_residual(
                stage15b_apply_local_flow(raw, 2, 0.5 * correct_v), target
            ) > STAGE15A_ATOL:
                local_wrong_half += 1
            if _phase_space_residual(raw, target) > STAGE15A_ATOL:
                local_missing += 1

        shared_residual = _phase_space_residual(
            stage15b_apply_local_flow(raw_102, 2, pair.v_012), target
        )
        if abs(pair.compensator_difference) > STAGE15A_ATOL:
            if shared_residual > STAGE15A_ATOL:
                shared_rejected += 1
        else:
            if shared_residual <= STAGE15A_ATOL:
                shared_compatible += 1

    smeared_probes = canonical_stage15b_smeared_order_probes()
    smeared_nonzero = [
        probe for probe in smeared_probes
        if abs(probe.observed_c2_defect) > STAGE15A_ATOL
    ]
    smeared_zero = [
        probe for probe in smeared_probes
        if abs(probe.observed_c2_defect) <= STAGE15A_ATOL
    ]
    max_smeared_identity = max(
        abs(probe.observed_c2_defect - probe.expected_c2_defect)
        for probe in smeared_probes
    )
    max_smeared_c2_only = max(probe.c2_only_residual for probe in smeared_probes)
    max_smeared_endpoint = max(
        probe.compensated_endpoint_residual for probe in smeared_probes
    )
    max_smeared_payload = max(probe.payload_residual for probe in smeared_probes)

    smeared_wrong_sign = 0
    smeared_missing = 0
    for rep in reps:
        point = rep.point()
        for case in STAGE15B_SMEARED_CASES:
            case_id, N, M, alpha, beta, nontrivial_expected = case
            if not nontrivial_expected:
                continue
            path_nm = stage15b_apply_smeared_flow(
                stage15b_apply_smeared_flow(point, N, alpha), M, beta
            )
            path_mn = stage15b_apply_smeared_flow(
                stage15b_apply_smeared_flow(point, M, beta), N, alpha
            )
            defect = float(path_nm.T2 - path_mn.T2)
            if _phase_space_residual(
                stage15b_apply_local_flow(path_mn, 2, -defect), path_nm
            ) > STAGE15A_ATOL:
                smeared_wrong_sign += 1
            if _phase_space_residual(path_mn, path_nm) > STAGE15A_ATOL:
                smeared_missing += 1

    off_surface = canonical_stage15a_off_surface_probes()
    jacobi_residuals: list[float] = []
    jacobi_terms: list[float] = []
    jacobi_probe_count = 0
    for point in off_surface:
        for L, N, M in permutations(STAGE15B_JACOBI_SMEARINGS, 3):
            jacobi_probe_count += 1
            jacobi_residuals.append(
                abs(stage15b_smeared_jacobi_residual(point, L, N, M))
            )
            jacobi_terms.extend(
                (
                    abs(stage15b_smeared_nested_bracket(point, L, N, M)),
                    abs(stage15b_smeared_nested_bracket(point, N, M, L)),
                    abs(stage15b_smeared_nested_bracket(point, M, L, N)),
                )
            )

    max_jacobi = float(max(jacobi_residuals, default=0.0))
    max_jacobi_term = float(max(jacobi_terms, default=0.0))

    exact_flows = (
        single_local_count == 648
        and single_smeared_count == 864
        and max_single_constraint <= STAGE15A_ATOL
        and max_single_payload <= STAGE15A_ATOL
    )
    local_closed = (
        len(local_pairs) == 864
        and len(local_results) == 1728
        and max_local_identity <= STAGE15A_ATOL
        and max_local_raw <= STAGE15A_ATOL
        and max_local_endpoint <= STAGE15A_ATOL
        and max_local_payload <= STAGE15A_ATOL
        and max_local_relational <= STAGE15A_ATOL
    )
    local_order = len(local_nonzero) == 576 and len(local_zero) == 288
    local_controls = (
        local_wrong_sign == 1728
        and local_wrong_half == 1728
        and local_missing == 1728
        and shared_rejected == 576
        and shared_compatible == 288
    )

    smeared_closed = (
        len(smeared_probes) == 540
        and max_smeared_identity <= STAGE15A_ATOL
        and max_smeared_c2_only <= STAGE15A_ATOL
        and max_smeared_endpoint <= STAGE15A_ATOL
        and max_smeared_payload <= STAGE15A_ATOL
    )
    smeared_order = (
        len(smeared_nonzero) == 432
        and smeared_wrong_sign == 432
        and smeared_missing == 432
    )
    smeared_zero_exact = (
        len(smeared_zero) == 108
        and all(not probe.nontrivial_expected for probe in smeared_zero)
    )
    smeared_jacobi = (
        jacobi_probe_count == 2592
        and max_jacobi <= STAGE15A_ATOL
        and max_jacobi_term > STAGE15A_ATOL
    )

    criteria = (
        exact_flows
        and local_closed
        and local_order
        and local_controls
        and smeared_closed
        and smeared_order
        and smeared_zero_exact
        and smeared_jacobi
    )

    return Stage15BDiagnostics(
        orbit_count=4,
        representative_count=108,
        single_local_flow_probe_count=single_local_count,
        single_smeared_flow_probe_count=single_smeared_count,
        local_pair_count=len(local_pairs),
        local_path_result_count=len(local_results),
        local_nonzero_order_defect_count=len(local_nonzero),
        local_zero_order_defect_count=len(local_zero),
        local_wrong_sign_rejected_count=local_wrong_sign,
        local_wrong_half_rejected_count=local_wrong_half,
        local_missing_rejected_count=local_missing,
        local_shared_compensator_rejected_count=shared_rejected,
        local_shared_compensator_zero_defect_compatible_count=shared_compatible,
        smeared_order_probe_count=len(smeared_probes),
        smeared_nonzero_order_defect_count=len(smeared_nonzero),
        smeared_zero_order_defect_count=len(smeared_zero),
        smeared_wrong_sign_rejected_count=smeared_wrong_sign,
        smeared_missing_rejected_count=smeared_missing,
        smeared_jacobi_probe_count=jacobi_probe_count,
        max_single_flow_constraint_residual=float(max_single_constraint),
        max_single_flow_payload_residual=float(max_single_payload),
        max_local_compensator_identity_residual=float(max_local_identity),
        max_local_raw_formula_residual=float(max_local_raw),
        max_local_endpoint_residual=float(max_local_endpoint),
        max_local_payload_residual=float(max_local_payload),
        max_local_relational_residual=float(max_local_relational),
        max_smeared_compensator_identity_residual=float(max_smeared_identity),
        max_smeared_c2_only_residual=float(max_smeared_c2_only),
        max_smeared_endpoint_residual=float(max_smeared_endpoint),
        max_smeared_payload_residual=float(max_smeared_payload),
        max_smeared_jacobi_residual=float(max_jacobi),
        max_smeared_jacobi_term_magnitude=float(max_jacobi_term),
        exact_finite_flows_established=exact_flows,
        local_compensated_path_closure_established=local_closed,
        local_order_defect_detected=local_order,
        local_controls_detected=local_controls,
        smeared_compensated_path_closure_established=smeared_closed,
        smeared_order_defect_detected=smeared_order,
        smeared_zero_wedge_control_exact=smeared_zero_exact,
        smeared_jacobi_established_off_surface=smeared_jacobi,
        criteria_18_24_satisfied=criteria,
    )
