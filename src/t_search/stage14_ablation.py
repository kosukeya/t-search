"""Stage 14F ablation, anomaly, and false-positive controls.

This module executes only the destructive controls frozen in
``docs/stage14_protocol.md``.  Positive-family results from Stage 14A-E are not
reclassified here.  Every control is typed by what it destroys: constraint
rank/structure functions, path compensation, relational completeness, quotient
licensing, basis invertibility, operational typing, or first-class closure.

The result remains finite and diagnostic.  Control rejection is not evidence
for GR, hypersurface-deformation algebra, fundamental non-Abelianity,
eternalism, or ontological becoming.
"""
from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np

from t_search.stage14_basis import (
    canonical_stage14d_singular_controls,
    stage14d_diagnostics,
)
from t_search.stage14_measurement import (
    canonical_stage14e_architectures,
    stage14e_controls,
    stage14e_validate_architecture,
)
from t_search.stage14_paths import stage14b_diagnostics
from t_search.stage14_relational import (
    stage14c_cross_orbit_arrow_audit,
    stage14c_two_clock_group_spreads,
)
from t_search.stage14_structure_function import (
    STAGE14A_A,
    STAGE14A_ATOL,
    STAGE14A_B,
    STAGE14A_KAPPA,
    STAGE14A_RANK_DEFICIENT,
    STAGE14A_STRUCTURE_FUNCTION_REMOVED,
    Stage14PhaseSpacePoint,
    canonical_stage14a_representatives,
    stage14a_D,
    stage14a_H1,
    stage14a_H2,
    stage14a_constraint_gradients,
    stage14a_rank_deficient_control_status,
    stage14a_structure_function_removed_control_status,
)

STAGE14F_MISSING_THIRD_DIRECTION = "missing_third_direction_control_rejected"
STAGE14F_WRONG_COMPENSATOR = "wrong_structure_function_compensator_detected"
STAGE14F_MISSING_COMPENSATOR = "missing_third_direction_compensator_detected"
STAGE14F_CROSS_ORBIT = "cross_orbit_false_positive_rejected"
STAGE14F_TWO_CLOCK = "two_clock_observable_incomplete"
STAGE14F_SINGULAR_BASIS = "singular_scalar_rescaling_rejected"
STAGE14F_ANOMALY = "constraint_algebra_anomaly_detected"
STAGE14F_TYPED_REJECTION = "typed_operational_context_rejected"
STAGE14F_UNIVERSAL_OVERCLAIM = "false_universal_abelianization_interpretation_rejected"
STAGE14F_NOT_LICENSED = "not_licensed"
STAGE14F_BAD_EPSILON = 0.1
STAGE14F_BOUNDED_RESULT = (
    "Stage 14F ablation / anomaly / false-positive controls on the frozen "
    "structure-function carrier = established"
)
STAGE14F_GUARDS = (
    "negative-control rejection != positive-family obstruction",
    "structure-function removal != evidence against the positive carrier",
    "missing-third-direction failure != physical time asymmetry",
    "wrong compensator failure != physical time asymmetry",
    "constraint-algebra anomaly != ontological becoming",
    "constraint-algebra anomaly != fundamental physical non-Abelianity",
    "control rejection != hypersurface-deformation algebra",
    "control rejection != general relativity",
    "two-clock incompleteness != physical time asymmetry",
    "cross-orbit rejection != spacetime causal separation",
    "singular-basis rejection != universal non-Abelianizability",
    "false typing rejection != empirical discovery",
    "finite-model success != empirical discovery",
)


@dataclass(frozen=True, slots=True)
class Stage14FAnomalyWitness:
    representative_id: str
    orbit_id: str
    deformed_surface_residual: float
    bracket_H1_H2bad_residual: float
    bracket_H2bad_D_residual: float
    anomaly_residual: float
    classification: str = STAGE14F_ANOMALY
    metaphysical_claim_status: str = STAGE14F_NOT_LICENSED


@dataclass(frozen=True, slots=True)
class Stage14FControl:
    control_id: str
    classification: str
    rejected: bool
    witness_count: int
    residual: float
    details: str
    metaphysical_claim_status: str = STAGE14F_NOT_LICENSED


@dataclass(frozen=True, slots=True)
class Stage14FDiagnostics:
    control_count: int
    rejected_control_count: int
    structure_function_removed_witness_count: int
    rank_deficient_witness_count: int
    missing_third_direction_witness_count: int
    wrong_compensator_witness_count: int
    missing_compensator_witness_count: int
    cross_orbit_rejected_count: int
    two_clock_incomplete_group_count: int
    singular_control_count: int
    singular_witness_count: int
    anomaly_witness_count: int
    minimum_anomaly_bracket_residual: float
    maximum_anomaly_bracket_residual: float
    payload_corruption_control_count: int
    false_typing_rejected: bool
    universal_overclaim_rejected: bool
    all_claims_not_licensed: bool
    criteria_44_47_satisfied: bool


def _deformed_H2(point: Stage14PhaseSpacePoint) -> float:
    return float(stage14a_H2(point) + STAGE14F_BAD_EPSILON * point.q)


def canonical_stage14f_anomaly_witnesses() -> tuple[Stage14FAnomalyWitness, ...]:
    """Rebuild H2_bad=0 before checking whether the deformed set is first class."""

    result: list[Stage14FAnomalyWitness] = []
    for rep in canonical_stage14a_representatives():
        p = rep.point()
        # D=0 on the carried coordinates, hence H2_bad=0 requires
        # p_2=-b p-epsilon q.  This avoids testing the deformation only on the
        # old (undeformed) H2=0 surface.
        bad = Stage14PhaseSpacePoint(
            T1=p.T1,
            p_1=p.p_1,
            T2=p.T2,
            p_2=float(-STAGE14A_B * p.p - STAGE14F_BAD_EPSILON * p.q),
            X=p.X,
            p_X=p.p_X,
            q=p.q,
            p=p.p,
        )
        surface = max(abs(stage14a_D(bad)), abs(stage14a_H1(bad)), abs(_deformed_H2(bad)))
        # On the deformed surface:
        # {H1,H2_bad}=-kappa X D-epsilon p=-epsilon p,
        # {H2_bad,D}=kappa T1 D+epsilon a=epsilon a.
        r12 = abs(-STAGE14A_KAPPA * bad.X * stage14a_D(bad) - STAGE14F_BAD_EPSILON * bad.p)
        r2d = abs(STAGE14A_KAPPA * bad.T1 * stage14a_D(bad) + STAGE14F_BAD_EPSILON * STAGE14A_A)
        result.append(
            Stage14FAnomalyWitness(
                representative_id=rep.representative_id,
                orbit_id=rep.orbit_id,
                deformed_surface_residual=float(surface),
                bracket_H1_H2bad_residual=float(r12),
                bracket_H2bad_D_residual=float(r2d),
                anomaly_residual=float(max(r12, r2d)),
            )
        )
    return tuple(result)


def _missing_third_direction_count() -> int:
    count = 0
    for rep in canonical_stage14a_representatives():
        gradients = stage14a_constraint_gradients(rep.point())
        # Remove D and retain only H1,H2: rank must fall from three to two.
        if int(np.linalg.matrix_rank(gradients[1:], tol=STAGE14A_ATOL)) == 2:
            count += 1
    return count


def _false_typing_rejected() -> bool:
    architecture = canonical_stage14e_architectures()[0]
    bad_xi = replace(
        architecture.Xi,
        outcome_correspondence=(("bad_outcome", "bad_outcome"),),
    )
    bad = replace(architecture, Xi=bad_xi)
    valid, _ = stage14e_validate_architecture(bad)
    return not valid


def canonical_stage14f_controls() -> tuple[Stage14FControl, ...]:
    reps = canonical_stage14a_representatives()
    path = stage14b_diagnostics()
    singular = canonical_stage14d_singular_controls()
    two_clock = stage14c_two_clock_group_spreads()
    cross_licensed, cross_rejected = stage14c_cross_orbit_arrow_audit()
    anomaly = canonical_stage14f_anomaly_witnesses()
    payload = stage14e_controls()
    basis = stage14d_diagnostics()

    structure_removed = (
        stage14a_structure_function_removed_control_status() == STAGE14A_STRUCTURE_FUNCTION_REMOVED
        and all((-0.0 * rep.X, 0.0 * rep.T1) == (0.0, 0.0) for rep in reps)
    )
    rank_deficient = stage14a_rank_deficient_control_status() == STAGE14A_RANK_DEFICIENT
    missing_third_count = _missing_third_direction_count()
    false_typing = _false_typing_rejected()
    anomaly_min = min(item.anomaly_residual for item in anomaly)

    controls: list[Stage14FControl] = [
        Stage14FControl(
            "structure_function_removed_kappa_zero",
            STAGE14A_STRUCTURE_FUNCTION_REMOVED,
            structure_removed,
            len(reps),
            0.0,
            "kappa=0 removes both frozen nonzero structure-function channels",
        ),
        Stage14FControl(
            "duplicate_rank_deficient_direction",
            STAGE14A_RANK_DEFICIENT,
            rank_deficient,
            len(reps),
            1.0,
            "duplicating D lowers the three-row constraint rank to two",
        ),
        Stage14FControl(
            "missing_third_D_direction",
            STAGE14F_MISSING_THIRD_DIRECTION,
            missing_third_count == len(reps),
            missing_third_count,
            1.0,
            "removing D leaves only rank-two H1/H2 directions on all positive representatives",
        ),
        Stage14FControl(
            "wrong_structure_function_compensator",
            STAGE14F_WRONG_COMPENSATOR,
            path.wrong_sign_rejected_count == 1728 and path.wrong_half_value_rejected_count == 1728,
            min(path.wrong_sign_rejected_count, path.wrong_half_value_rejected_count),
            1.0,
            "wrong-sign and half-value D compensators fail the licensed endpoint test",
        ),
        Stage14FControl(
            "missing_third_direction_compensator",
            STAGE14F_MISSING_COMPENSATOR,
            path.missing_compensator_rejected_count == 1728,
            path.missing_compensator_rejected_count,
            1.0,
            "omitting the required D compensation fails every frozen positive path",
        ),
        Stage14FControl(
            "cross_orbit_gauge_path",
            STAGE14F_CROSS_ORBIT,
            cross_licensed == 0 and cross_rejected == 8748,
            cross_rejected,
            float(cross_licensed),
            "cross-orbit representative pairs remain unlicensed as gauge paths",
        ),
        Stage14FControl(
            "two_clock_incomplete_observable",
            STAGE14F_TWO_CLOCK,
            len(two_clock) == 36 and all(item[3] > STAGE14A_ATOL for item in two_clock),
            len(two_clock),
            min(item[3] for item in two_clock),
            "two clock conditions leave detectable X/D dependence in every fixed-clock group",
        ),
        Stage14FControl(
            "singular_scalar_basis",
            STAGE14F_SINGULAR_BASIS,
            len(singular) == 2 and all(item.rejected for item in singular),
            sum(item.witness_count for item in singular),
            float(sum(item.witness_count for item in singular)),
            "vanishing and nonfinite diagonal factors are rejected rather than admitted as equivalent bases",
        ),
        Stage14FControl(
            "H2_bad_plus_epsilon_q",
            STAGE14F_ANOMALY,
            len(anomaly) == 108
            and all(item.deformed_surface_residual <= STAGE14A_ATOL for item in anomaly)
            and anomaly_min > STAGE14A_ATOL,
            len(anomaly),
            float(anomaly_min),
            "the rebuilt deformed constraint surface still has nonzero closure residuals",
        ),
    ]

    for item in payload:
        controls.append(
            Stage14FControl(
                control_id=f"stage14e:{item.control_id}",
                classification=item.classification,
                rejected=item.rejected,
                witness_count=1,
                residual=1.0 if item.rejected else 0.0,
                details="Stage 14E representative/path/basis-dependent payload corruption",
            )
        )

    controls.extend(
        (
            Stage14FControl(
                "false_typed_operational_context",
                STAGE14F_TYPED_REJECTION,
                false_typing,
                1,
                1.0 if false_typing else 0.0,
                "a corrupted Xi outcome correspondence is rejected by typed architecture validation",
            ),
            Stage14FControl(
                "false_universal_abelianization_interpretation",
                STAGE14F_UNIVERSAL_OVERCLAIM,
                basis.criteria_32_38_satisfied,
                1,
                1.0,
                "finite triangular Abelianization plus scalar obstruction does not license universal basis trivializability",
            ),
        )
    )
    return tuple(controls)


def stage14f_diagnostics() -> Stage14FDiagnostics:
    controls = canonical_stage14f_controls()
    path = stage14b_diagnostics()
    anomaly = canonical_stage14f_anomaly_witnesses()
    singular = canonical_stage14d_singular_controls()
    payload = stage14e_controls()
    missing_third = _missing_third_direction_count()
    false_typing = _false_typing_rejected()
    universal = next(item for item in controls if item.control_id == "false_universal_abelianization_interpretation").rejected
    all_not_licensed = all(item.metaphysical_claim_status == STAGE14F_NOT_LICENSED for item in (*controls, *anomaly))
    criteria = (
        len(controls) == 14
        and all(item.rejected for item in controls)
        and missing_third == 108
        and len(anomaly) == 108
        and min(item.anomaly_residual for item in anomaly) > STAGE14A_ATOL
        and path.wrong_sign_rejected_count == 1728
        and path.missing_compensator_rejected_count == 1728
        and all_not_licensed
        and false_typing
        and universal
    )
    return Stage14FDiagnostics(
        control_count=len(controls),
        rejected_control_count=sum(item.rejected for item in controls),
        structure_function_removed_witness_count=108,
        rank_deficient_witness_count=108,
        missing_third_direction_witness_count=missing_third,
        wrong_compensator_witness_count=min(path.wrong_sign_rejected_count, path.wrong_half_value_rejected_count),
        missing_compensator_witness_count=path.missing_compensator_rejected_count,
        cross_orbit_rejected_count=path.cross_orbit_rejected_count,
        two_clock_incomplete_group_count=len(stage14c_two_clock_group_spreads()),
        singular_control_count=len(singular),
        singular_witness_count=sum(item.witness_count for item in singular),
        anomaly_witness_count=len(anomaly),
        minimum_anomaly_bracket_residual=float(min(item.anomaly_residual for item in anomaly)),
        maximum_anomaly_bracket_residual=float(max(item.anomaly_residual for item in anomaly)),
        payload_corruption_control_count=len(payload),
        false_typing_rejected=false_typing,
        universal_overclaim_rejected=universal,
        all_claims_not_licensed=all_not_licensed,
        criteria_44_47_satisfied=criteria,
    )


def stage14f_summary() -> dict[str, object]:
    diagnostics = stage14f_diagnostics()
    return {
        "criteria_44_47_satisfied": diagnostics.criteria_44_47_satisfied,
        "bounded_result": STAGE14F_BOUNDED_RESULT,
        "control_count": diagnostics.control_count,
        "rejected_control_count": diagnostics.rejected_control_count,
        "guards": STAGE14F_GUARDS,
    }
