"""Stage 14B phase-space-dependent mixed paths and third-direction compensation.

This module consumes the validated Stage 14A carrier and implements only the
Stage 14B path evidence frozen in ``docs/stage14_protocol.md``.  The positive
family is the canonical set of 864 ordered same-orbit source/target pairs for
which T1, T2, and X all change.  For every pair it compares the ordered words
``12D`` and ``21D`` and applies the exact third-direction D compensator.

The module deliberately keeps raw path-order difference separate from physical
path dependence.  Correct compensation is tested against the licensed sampled
target; wrong/missing compensators and cross-orbit pairs are negative controls.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp

from .stage14_structure_function import (
    STAGE14A_A,
    STAGE14A_ATOL,
    STAGE14A_B,
    STAGE14A_D,
    STAGE14A_H1,
    STAGE14A_H2,
    STAGE14A_KAPPA,
    Stage14PhaseSpacePoint,
    Stage14Representative,
    canonical_stage14a_orbits,
    canonical_stage14a_representatives,
    canonical_stage14a_representatives_for_orbit,
    stage14a_apply_flow,
    stage14a_dirac_data,
)

STAGE14B_PATH_12D = "12D"
STAGE14B_PATH_21D = "21D"
STAGE14B_WRONG_STRUCTURE_FUNCTION = "wrong_structure_function_compensator_detected"
STAGE14B_MISSING_THIRD_COMPENSATOR = "missing_third_direction_compensator_detected"
STAGE14B_STAGE13_STYLE = "stage13_style_two_generator_compensator_rejected"
STAGE14B_CROSS_ORBIT = "cross_orbit_false_positive_rejected"


@dataclass(frozen=True, slots=True)
class Stage14BMixedPair:
    pair_id: str
    orbit_id: str
    source: Stage14Representative
    target: Stage14Representative
    s: float
    u: float
    v_12D: float
    v_21D: float
    compensator_difference: float
    expected_compensator_difference: float


@dataclass(frozen=True, slots=True)
class Stage14BPathResult:
    pair_id: str
    path_word: str
    raw_X: float
    expected_raw_X: float
    raw_q: float
    expected_raw_q: float
    compensator: float
    raw_formula_residual: float
    final_endpoint_residual: float
    final_dirac_residual: float


@dataclass(frozen=True, slots=True)
class Stage14BDiagnostics:
    orbit_count: int
    representative_count: int
    mixed_pair_count: int
    path_result_count: int
    nontrivial_X0_pair_count: int
    zero_X0_pair_count: int
    nonzero_compensator_difference_count: int
    zero_compensator_difference_count: int
    cross_orbit_rejected_count: int
    wrong_sign_rejected_count: int
    wrong_half_value_rejected_count: int
    missing_compensator_rejected_count: int
    stage13_style_rejected_nontrivial_count: int
    stage13_style_zero_difference_compatible_count: int
    min_nonzero_compensator_difference: float
    max_compensator_difference: float
    max_compensator_identity_residual: float
    max_raw_formula_residual: float
    max_positive_endpoint_residual: float
    max_positive_dirac_residual: float
    all_positive_pairs_closed: bool
    nontrivial_path_order_detected: bool
    zero_difference_subfamily_exact: bool
    wrong_controls_detected: bool
    cross_orbit_false_positive_rejected: bool
    criteria_18_24_satisfied: bool


def _phase_space_residual(a: Stage14PhaseSpacePoint, b: Stage14PhaseSpacePoint) -> float:
    return float(max(abs(x - y) for x, y in zip(a.vector(), b.vector(), strict=True)))


def _dirac_residual(a: Stage14PhaseSpacePoint, b: Stage14PhaseSpacePoint) -> float:
    qa, pa = stage14a_dirac_data(a)
    qb, pb = stage14a_dirac_data(b)
    return float(max(abs(qa - qb), abs(pa - pb)))


def stage14b_make_mixed_pair(
    source: Stage14Representative,
    target: Stage14Representative,
) -> Stage14BMixedPair:
    if source.orbit_id != target.orbit_id:
        raise ValueError("Stage 14B licensed mixed paths cannot connect distinct physical orbits")
    if source.representative_id == target.representative_id:
        raise ValueError("Stage 14B mixed paths require distinct source and target")
    if (
        abs(source.T1 - target.T1) <= STAGE14A_ATOL
        or abs(source.T2 - target.T2) <= STAGE14A_ATOL
        or abs(source.X - target.X) <= STAGE14A_ATOL
    ):
        raise ValueError("Stage 14B canonical mixed pair requires T1, T2, and X all to change")

    s = float(target.T1 - source.T1)
    u = float(target.T2 - source.T2)
    raw_X_12D = float(source.X * exp(STAGE14A_KAPPA * target.T1 * u))
    raw_X_21D = float(source.X * exp(STAGE14A_KAPPA * source.T1 * u))
    v_12D = float(target.X - raw_X_12D)
    v_21D = float(target.X - raw_X_21D)
    expected_difference = float(
        source.X
        * (
            exp(STAGE14A_KAPPA * target.T1 * u)
            - exp(STAGE14A_KAPPA * source.T1 * u)
        )
    )
    pair_id = f"{source.representative_id}->{target.representative_id}"
    return Stage14BMixedPair(
        pair_id=pair_id,
        orbit_id=source.orbit_id,
        source=source,
        target=target,
        s=s,
        u=u,
        v_12D=v_12D,
        v_21D=v_21D,
        compensator_difference=float(v_21D - v_12D),
        expected_compensator_difference=expected_difference,
    )


def canonical_stage14b_mixed_pairs() -> tuple[Stage14BMixedPair, ...]:
    result: list[Stage14BMixedPair] = []
    for orbit in canonical_stage14a_orbits():
        reps = canonical_stage14a_representatives_for_orbit(orbit)
        for source in reps:
            for target in reps:
                if source.representative_id == target.representative_id:
                    continue
                if (
                    abs(source.T1 - target.T1) > STAGE14A_ATOL
                    and abs(source.T2 - target.T2) > STAGE14A_ATOL
                    and abs(source.X - target.X) > STAGE14A_ATOL
                ):
                    result.append(stage14b_make_mixed_pair(source, target))
    return tuple(result)


def _apply_ordered_raw_path(pair: Stage14BMixedPair, path_word: str) -> Stage14PhaseSpacePoint:
    source = pair.source.point()
    if path_word == STAGE14B_PATH_12D:
        after_1 = stage14a_apply_flow(source, STAGE14A_H1, pair.s)
        return stage14a_apply_flow(after_1, STAGE14A_H2, pair.u)
    if path_word == STAGE14B_PATH_21D:
        after_2 = stage14a_apply_flow(source, STAGE14A_H2, pair.u)
        return stage14a_apply_flow(after_2, STAGE14A_H1, pair.s)
    raise ValueError(f"unknown Stage 14B path word: {path_word}")


def _expected_raw_endpoint(pair: Stage14BMixedPair, path_word: str) -> Stage14PhaseSpacePoint:
    source = pair.source
    T1_final = float(source.T1 + pair.s)
    T2_final = float(source.T2 + pair.u)
    if path_word == STAGE14B_PATH_12D:
        X_final = float(source.X * exp(STAGE14A_KAPPA * T1_final * pair.u))
    elif path_word == STAGE14B_PATH_21D:
        X_final = float(source.X * exp(STAGE14A_KAPPA * source.T1 * pair.u))
    else:
        raise ValueError(f"unknown Stage 14B path word: {path_word}")
    q_final = float(
        source.q
        + source.p * pair.s
        + STAGE14A_B * pair.u
        + STAGE14A_A * (X_final - source.X)
    )
    return Stage14PhaseSpacePoint(
        T1=T1_final,
        p_1=source.p_1,
        T2=T2_final,
        p_2=source.p_2,
        X=X_final,
        p_X=source.p_X,
        q=q_final,
        p=source.p,
    )


def stage14b_apply_path(
    pair: Stage14BMixedPair,
    path_word: str,
    *,
    compensator: float | None = None,
) -> Stage14BPathResult:
    raw = _apply_ordered_raw_path(pair, path_word)
    expected_raw = _expected_raw_endpoint(pair, path_word)
    if compensator is None:
        compensator = pair.v_12D if path_word == STAGE14B_PATH_12D else pair.v_21D
    final = stage14a_apply_flow(raw, STAGE14A_D, float(compensator))
    target = pair.target.point()
    return Stage14BPathResult(
        pair_id=pair.pair_id,
        path_word=path_word,
        raw_X=raw.X,
        expected_raw_X=expected_raw.X,
        raw_q=raw.q,
        expected_raw_q=expected_raw.q,
        compensator=float(compensator),
        raw_formula_residual=_phase_space_residual(raw, expected_raw),
        final_endpoint_residual=_phase_space_residual(final, target),
        final_dirac_residual=_dirac_residual(final, target),
    )


def canonical_stage14b_path_results() -> tuple[Stage14BPathResult, ...]:
    return tuple(
        result
        for pair in canonical_stage14b_mixed_pairs()
        for result in (
            stage14b_apply_path(pair, STAGE14B_PATH_12D),
            stage14b_apply_path(pair, STAGE14B_PATH_21D),
        )
    )


def _control_endpoint_residual(
    pair: Stage14BMixedPair,
    path_word: str,
    compensator: float,
) -> float:
    return stage14b_apply_path(pair, path_word, compensator=compensator).final_endpoint_residual


def canonical_stage14b_cross_orbit_rejections() -> int:
    reps = canonical_stage14a_representatives()
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
                raise AssertionError("cross-orbit pair was incorrectly licensed")
    return rejected


def stage14b_diagnostics() -> Stage14BDiagnostics:
    pairs = canonical_stage14b_mixed_pairs()
    results = canonical_stage14b_path_results()

    differences = [abs(pair.compensator_difference) for pair in pairs]
    nonzero_differences = [value for value in differences if value > STAGE14A_ATOL]
    zero_differences = [value for value in differences if value <= STAGE14A_ATOL]
    nontrivial_pairs = [pair for pair in pairs if abs(pair.source.X) > STAGE14A_ATOL]
    zero_x_pairs = [pair for pair in pairs if abs(pair.source.X) <= STAGE14A_ATOL]

    max_identity_residual = max(
        abs(pair.compensator_difference - pair.expected_compensator_difference)
        for pair in pairs
    )
    max_raw_formula = max(result.raw_formula_residual for result in results)
    max_endpoint = max(result.final_endpoint_residual for result in results)
    max_dirac = max(result.final_dirac_residual for result in results)

    wrong_sign_rejected = 0
    wrong_half_rejected = 0
    missing_rejected = 0
    for pair in pairs:
        for path_word, correct_v in (
            (STAGE14B_PATH_12D, pair.v_12D),
            (STAGE14B_PATH_21D, pair.v_21D),
        ):
            if _control_endpoint_residual(pair, path_word, -correct_v) > STAGE14A_ATOL:
                wrong_sign_rejected += 1
            if _control_endpoint_residual(pair, path_word, 0.5 * correct_v) > STAGE14A_ATOL:
                wrong_half_rejected += 1
            if _control_endpoint_residual(pair, path_word, 0.0) > STAGE14A_ATOL:
                missing_rejected += 1

    stage13_style_rejected = 0
    stage13_style_compatible = 0
    for pair in pairs:
        residual = _control_endpoint_residual(pair, STAGE14B_PATH_21D, pair.v_12D)
        if abs(pair.source.X) > STAGE14A_ATOL:
            if residual > STAGE14A_ATOL:
                stage13_style_rejected += 1
        else:
            if residual <= STAGE14A_ATOL:
                stage13_style_compatible += 1

    cross_orbit_rejected = canonical_stage14b_cross_orbit_rejections()

    all_positive_pairs_closed = (
        len(pairs) == 864
        and len(results) == 1728
        and max_raw_formula <= STAGE14A_ATOL
        and max_endpoint <= STAGE14A_ATOL
        and max_dirac <= STAGE14A_ATOL
        and max_identity_residual <= STAGE14A_ATOL
    )
    nontrivial_path_order_detected = (
        len(nontrivial_pairs) == 576
        and len(nonzero_differences) == 576
        and min(nonzero_differences) > STAGE14A_ATOL
    )
    zero_difference_subfamily_exact = (
        len(zero_x_pairs) == 288
        and len(zero_differences) == 288
        and max(zero_differences, default=0.0) <= STAGE14A_ATOL
    )
    wrong_controls_detected = (
        wrong_sign_rejected == 1728
        and wrong_half_rejected == 1728
        and missing_rejected == 1728
        and stage13_style_rejected == 576
        and stage13_style_compatible == 288
    )
    cross_orbit_ok = cross_orbit_rejected == 8748
    criteria = (
        all_positive_pairs_closed
        and nontrivial_path_order_detected
        and zero_difference_subfamily_exact
        and wrong_controls_detected
        and cross_orbit_ok
    )

    return Stage14BDiagnostics(
        orbit_count=4,
        representative_count=108,
        mixed_pair_count=len(pairs),
        path_result_count=len(results),
        nontrivial_X0_pair_count=len(nontrivial_pairs),
        zero_X0_pair_count=len(zero_x_pairs),
        nonzero_compensator_difference_count=len(nonzero_differences),
        zero_compensator_difference_count=len(zero_differences),
        cross_orbit_rejected_count=cross_orbit_rejected,
        wrong_sign_rejected_count=wrong_sign_rejected,
        wrong_half_value_rejected_count=wrong_half_rejected,
        missing_compensator_rejected_count=missing_rejected,
        stage13_style_rejected_nontrivial_count=stage13_style_rejected,
        stage13_style_zero_difference_compatible_count=stage13_style_compatible,
        min_nonzero_compensator_difference=float(min(nonzero_differences)),
        max_compensator_difference=float(max(differences)),
        max_compensator_identity_residual=float(max_identity_residual),
        max_raw_formula_residual=float(max_raw_formula),
        max_positive_endpoint_residual=float(max_endpoint),
        max_positive_dirac_residual=float(max_dirac),
        all_positive_pairs_closed=all_positive_pairs_closed,
        nontrivial_path_order_detected=nontrivial_path_order_detected,
        zero_difference_subfamily_exact=zero_difference_subfamily_exact,
        wrong_controls_detected=wrong_controls_detected,
        cross_orbit_false_positive_rejected=cross_orbit_ok,
        criteria_18_24_satisfied=criteria,
    )
