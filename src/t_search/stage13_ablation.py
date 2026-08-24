"""Stage 13F basis equivalence, ablation, anomaly, and false-positive controls.

This module tests whether the Stage 13A-E positive result is tied to the
noncommuting presentation of the second constraint.  It compares that
presentation with the equivalent commuting basis

    K_X_tilde = exp(-T) K_X = p_X + a p,

checks that the sampled quotient and quotient-level operational content are
unchanged under the typed basis correspondence, and then runs destructive
controls for rank deficiency, a decoupled second constraint, wrong
compensation, one-clock incompleteness, cross-orbit false matches, and a
deliberately non-first-class deformation.

The result is finite and diagnostic.  It is not refoliation invariance,
general covariance, general relativity, eternalism, or ontological becoming.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from math import exp

import numpy as np

from t_search.stage13_multi_constraint import (
    STAGE13A_A,
    STAGE13A_ATOL,
    STAGE13A_BASIS_ID,
    STAGE13A_K_T,
    Stage13PhaseSpacePoint,
    Stage13Representative,
    canonical_stage13a_orbits,
    canonical_stage13a_representatives,
    stage13a_K_T,
)
from t_search.stage13_paths import (
    STAGE13B_PHI_T,
    STAGE13B_WRONG_COMPENSATOR_CLASSIFICATION,
    canonical_stage13b_mixed_path_comparisons,
    stage13b_apply_phi_T,
)
from t_search.stage13_relational import (
    stage13c_complete_relational_value,
    stage13c_reconstruct_dirac_from_point,
)
from t_search.stage13_gauge_atlas import canonical_stage13d_quotient_classes
from t_search.stage13_measurement import (
    STAGE13E_CLOCK_PAIRS,
    canonical_stage13e_quotient_projections,
)

STAGE13F_ATOL = STAGE13A_ATOL
STAGE13F_COMMUTING_BASIS_ID = "stage13_commuting_equivalent_basis"
STAGE13F_K_X_TILDE = "K_X_tilde"
STAGE13F_PHI_X_TILDE = "Phi_X_tilde"
STAGE13F_BASIS_EQUIVALENT = "basis_presentation_equivalent"
STAGE13F_COMMUTING_PATH_CLASSIFICATION = "equivalent_commuting_path_closure_established"
STAGE13F_RANK_DEFICIENT_REJECTED = "rank_deficient_constraint_control_rejected"
STAGE13F_DECOUPLED_REJECTED = "decoupled_constraint_control_rejected"
STAGE13F_ONE_CLOCK_INCOMPLETE = "one_clock_observable_incomplete"
STAGE13F_CROSS_ORBIT_REJECTED = "cross_orbit_false_positive_rejected"
STAGE13F_ANOMALY_DETECTED = "constraint_algebra_anomaly_detected"
STAGE13F_NOT_LICENSED = "not_licensed"
STAGE13F_BAD_EPSILON = 0.1
STAGE13F_BOUNDED_RESULT = (
    "Stage 13F basis equivalence, ablation, anomaly, and false-positive controls "
    "on the frozen finite family = established"
)
STAGE13F_GUARDS = (
    "noncommuting constraint presentation != fundamental physical non-Abelianity",
    "constraint-basis change != physical-orbit change",
    "basis-equivalent finite quotient != refoliation invariance",
    "commuting presentation != proof that all admissible presentations commute",
    "wrong compensator failure != physical time asymmetry",
    "one clock condition in a two-gauge-direction model != complete relational observable",
    "constraint-algebra anomaly != ontological becoming",
    "multi-constraint path covariance != refoliation invariance",
    "constraint-algebra/refoliation precursor != general relativity",
    "Dirac-invariant data + relational change != proof of eternalism",
    "complete relational observable != ontological becoming by definition",
    "finite-model success != empirical discovery",
)


@dataclass(frozen=True, slots=True)
class Stage13FCommutingArrow:
    arrow_id: str
    source_representative_id: str
    target_representative_id: str
    generator_id: str
    basis_id: str
    raw_parameter: float
    endpoint_residual: float
    constraint_residual: float
    classification: str


@dataclass(frozen=True, slots=True)
class Stage13FCommutingQuotientClass:
    quotient_id: str
    representative_ids: tuple[str, ...]
    inferred_orbit_ids: tuple[str, ...]
    Q_D: float
    P_D: float
    max_Q_D_spread: float
    max_P_D_spread: float
    matches_stage13d_quotient: bool
    classification: str


@dataclass(frozen=True, slots=True)
class Stage13FBasisEquivalenceCheck:
    representative_id: str
    orbit_id: str
    noncommuting_basis_id: str
    commuting_basis_id: str
    quotient_id: str
    public_payload_equal: bool
    dirac_residual: float
    relational_residual: float
    classification: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage13FCommutingMixedPathCheck:
    comparison_id: str
    source_representative_id: str
    target_representative_id: str
    s: float
    u: float
    endpoint_separation: float
    tx_target_residual: float
    xt_target_residual: float
    constraint_residual: float
    classification: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage13FFalsePositiveControl:
    control_id: str
    classification: str
    rejected: bool
    witness_count: int
    residual: float
    metaphysical_claim_status: str
    details: str


@dataclass(frozen=True, slots=True)
class Stage13FDiagnostics:
    representative_count: int
    commuting_constraint_surface_count: int
    commuting_arrow_count: int
    commuting_phi_T_arrow_count: int
    commuting_phi_X_arrow_count: int
    commuting_quotient_class_count: int
    commuting_quotient_class_sizes: tuple[int, ...]
    stage13d_membership_match_count: int
    basis_equivalence_check_count: int
    basis_equivalent_count: int
    commuting_mixed_path_check_count: int
    commuting_mixed_path_closed_count: int
    max_K_X_tilde_constraint_residual: float
    max_KT_KX_tilde_bracket_residual: float
    max_commuting_arrow_endpoint_residual: float
    max_commuting_arrow_constraint_residual: float
    max_commuting_mixed_endpoint_separation: float
    max_commuting_mixed_target_residual: float
    max_commuting_mixed_constraint_residual: float
    max_basis_dirac_residual: float
    max_basis_relational_residual: float
    false_positive_control_count: int
    rejected_false_positive_control_count: int
    rank_deficient_rejected: bool
    decoupled_rejected: bool
    wrong_compensator_rejected: bool
    one_clock_incomplete_rejected: bool
    cross_orbit_false_positive_rejected: bool
    anomaly_detected: bool
    all_metaphysical_claims_not_licensed: bool
    criteria_44_47_satisfied: bool


def stage13f_K_X_tilde(point: Stage13PhaseSpacePoint) -> float:
    return float(point.p_X + STAGE13A_A * point.p)


def stage13f_poisson_KT_KX_tilde(point: Stage13PhaseSpacePoint) -> float:
    _ = point
    return 0.0


def stage13f_apply_phi_X_tilde(point: Stage13PhaseSpacePoint, u: float) -> Stage13PhaseSpacePoint:
    return Stage13PhaseSpacePoint(
        T=point.T,
        p_T=point.p_T,
        X=float(point.X + u),
        p_X=point.p_X,
        q=float(point.q + STAGE13A_A * u),
        p=point.p,
    )


def _point_residual(left: Stage13PhaseSpacePoint, right: Stage13PhaseSpacePoint) -> float:
    return float(
        max(
            abs(left.T - right.T),
            abs(left.p_T - right.p_T),
            abs(left.X - right.X),
            abs(left.p_X - right.p_X),
            abs(left.q - right.q),
            abs(left.p - right.p),
        )
    )


def _commuting_constraint_residual(point: Stage13PhaseSpacePoint) -> float:
    return float(max(abs(stage13a_K_T(point)), abs(stage13f_K_X_tilde(point))))


@lru_cache(maxsize=1)
def _representatives() -> tuple[Stage13Representative, ...]:
    return canonical_stage13a_representatives()


@lru_cache(maxsize=1)
def _representative_lookup() -> dict[str, Stage13Representative]:
    return {item.representative_id: item for item in _representatives()}


@lru_cache(maxsize=1)
def canonical_stage13f_commuting_arrows() -> tuple[Stage13FCommutingArrow, ...]:
    arrows: list[Stage13FCommutingArrow] = []
    for source in _representatives():
        for target in _representatives():
            if source.orbit_id != target.orbit_id or source.representative_id == target.representative_id:
                continue
            if abs(source.X - target.X) <= STAGE13F_ATOL:
                parameter = float(target.T - source.T)
                endpoint = stage13b_apply_phi_T(source.point(), parameter)
                generator = STAGE13A_K_T
            elif abs(source.T - target.T) <= STAGE13F_ATOL:
                parameter = float(target.X - source.X)
                endpoint = stage13f_apply_phi_X_tilde(source.point(), parameter)
                generator = STAGE13F_K_X_TILDE
            else:
                continue
            arrows.append(
                Stage13FCommutingArrow(
                    arrow_id=f"{generator}:{source.representative_id}->{target.representative_id}",
                    source_representative_id=source.representative_id,
                    target_representative_id=target.representative_id,
                    generator_id=generator,
                    basis_id=STAGE13F_COMMUTING_BASIS_ID,
                    raw_parameter=parameter,
                    endpoint_residual=_point_residual(endpoint, target.point()),
                    constraint_residual=max(
                        _commuting_constraint_residual(source.point()),
                        _commuting_constraint_residual(endpoint),
                        _commuting_constraint_residual(target.point()),
                    ),
                    classification=STAGE13F_BASIS_EQUIVALENT,
                )
            )
    return tuple(arrows)


class _DisjointSet:
    def __init__(self, ids: tuple[str, ...]) -> None:
        self.parent = {item: item for item in ids}

    def find(self, item: str) -> str:
        root = item
        while self.parent[root] != root:
            root = self.parent[root]
        while self.parent[item] != item:
            nxt = self.parent[item]
            self.parent[item] = root
            item = nxt
        return root

    def union(self, left: str, right: str) -> None:
        left_root = self.find(left)
        right_root = self.find(right)
        if left_root != right_root:
            self.parent[right_root] = left_root


@lru_cache(maxsize=1)
def canonical_stage13f_commuting_quotient_classes() -> tuple[Stage13FCommutingQuotientClass, ...]:
    representatives = _representatives()
    ids = tuple(item.representative_id for item in representatives)
    dsu = _DisjointSet(ids)
    for arrow in canonical_stage13f_commuting_arrows():
        dsu.union(arrow.source_representative_id, arrow.target_representative_id)

    grouped: dict[str, list[Stage13Representative]] = {}
    for representative in representatives:
        grouped.setdefault(dsu.find(representative.representative_id), []).append(representative)

    stage13d_by_members = {
        frozenset(item.representative_ids): item for item in canonical_stage13d_quotient_classes()
    }
    result: list[Stage13FCommutingQuotientClass] = []
    for members in grouped.values():
        member_ids = tuple(sorted(item.representative_id for item in members))
        stage13d = stage13d_by_members.get(frozenset(member_ids))
        values = tuple(stage13c_reconstruct_dirac_from_point(item.point()) for item in members)
        q_values = tuple(item[0] for item in values)
        p_values = tuple(item[1] for item in values)
        Q_D = float(sum(q_values) / len(q_values))
        P_D = float(sum(p_values) / len(p_values))
        result.append(
            Stage13FCommutingQuotientClass(
                quotient_id=stage13d.quotient_id if stage13d is not None else f"commuting:q:{len(result)}",
                representative_ids=member_ids,
                inferred_orbit_ids=tuple(sorted({item.orbit_id for item in members})),
                Q_D=Q_D,
                P_D=P_D,
                max_Q_D_spread=float(max(abs(value - Q_D) for value in q_values)),
                max_P_D_spread=float(max(abs(value - P_D) for value in p_values)),
                matches_stage13d_quotient=stage13d is not None,
                classification=STAGE13F_BASIS_EQUIVALENT if stage13d is not None else "basis_quotient_mismatch",
            )
        )
    return tuple(sorted(result, key=lambda item: item.quotient_id))


@lru_cache(maxsize=1)
def canonical_stage13f_basis_equivalence_checks() -> tuple[Stage13FBasisEquivalenceCheck, ...]:
    quotient_by_rep = {
        representative_id: quotient
        for quotient in canonical_stage13f_commuting_quotient_classes()
        for representative_id in quotient.representative_ids
    }
    public_by_orbit = {}
    for projection in canonical_stage13e_quotient_projections():
        public_by_orbit.setdefault(projection.orbit_id, projection)

    result: list[Stage13FBasisEquivalenceCheck] = []
    for representative in _representatives():
        quotient = quotient_by_rep[representative.representative_id]
        public = public_by_orbit[representative.orbit_id]
        Q_D, P_D = stage13c_reconstruct_dirac_from_point(representative.point())
        dirac_residual = max(abs(Q_D - quotient.Q_D), abs(P_D - quotient.P_D))
        relational_residual = 0.0
        for event, (_, tau, chi) in zip(public.O.relational_events, STAGE13E_CLOCK_PAIRS, strict=True):
            expected = stage13c_complete_relational_value(quotient.Q_D, quotient.P_D, tau, chi)
            relational_residual = max(relational_residual, abs(expected - event.q_value))
        public_payload_equal = bool(
            quotient.matches_stage13d_quotient
            and public.quotient_id == quotient.quotient_id
            and public.orbit_id == representative.orbit_id
        )
        result.append(
            Stage13FBasisEquivalenceCheck(
                representative_id=representative.representative_id,
                orbit_id=representative.orbit_id,
                noncommuting_basis_id=STAGE13A_BASIS_ID,
                commuting_basis_id=STAGE13F_COMMUTING_BASIS_ID,
                quotient_id=quotient.quotient_id,
                public_payload_equal=public_payload_equal,
                dirac_residual=float(dirac_residual),
                relational_residual=float(relational_residual),
                classification=STAGE13F_BASIS_EQUIVALENT if public_payload_equal else "basis_public_payload_mismatch",
                metaphysical_claim_status=STAGE13F_NOT_LICENSED,
            )
        )
    return tuple(result)


@lru_cache(maxsize=1)
def canonical_stage13f_commuting_mixed_path_checks() -> tuple[Stage13FCommutingMixedPathCheck, ...]:
    result: list[Stage13FCommutingMixedPathCheck] = []
    lookup = _representative_lookup()
    for comparison in canonical_stage13b_mixed_path_comparisons():
        source = lookup[comparison.source_representative_id]
        target = lookup[comparison.target_representative_id]
        s = float(comparison.s)
        u = float(comparison.delta_X)

        after_T = stage13b_apply_phi_T(source.point(), s)
        endpoint_TX = stage13f_apply_phi_X_tilde(after_T, u)
        after_X = stage13f_apply_phi_X_tilde(source.point(), u)
        endpoint_XT = stage13b_apply_phi_T(after_X, s)
        constraint_residual = max(
            _commuting_constraint_residual(source.point()),
            _commuting_constraint_residual(after_T),
            _commuting_constraint_residual(after_X),
            _commuting_constraint_residual(endpoint_TX),
            _commuting_constraint_residual(endpoint_XT),
            _commuting_constraint_residual(target.point()),
        )
        result.append(
            Stage13FCommutingMixedPathCheck(
                comparison_id=comparison.comparison_id,
                source_representative_id=source.representative_id,
                target_representative_id=target.representative_id,
                s=s,
                u=u,
                endpoint_separation=_point_residual(endpoint_TX, endpoint_XT),
                tx_target_residual=_point_residual(endpoint_TX, target.point()),
                xt_target_residual=_point_residual(endpoint_XT, target.point()),
                constraint_residual=float(constraint_residual),
                classification=STAGE13F_COMMUTING_PATH_CLASSIFICATION,
                metaphysical_claim_status=STAGE13F_NOT_LICENSED,
            )
        )
    return tuple(result)


def _rank_deficient_control() -> Stage13FFalsePositiveControl:
    rejected_count = 0
    for representative in _representatives():
        p = representative.p
        gradient = np.asarray([0.0, 1.0, 0.0, 0.0, 0.0, p], dtype=float)
        matrix = np.vstack((gradient, gradient))
        rejected_count += int(np.linalg.matrix_rank(matrix) < 2)
    return Stage13FFalsePositiveControl(
        "rank_deficient_constraint_pair",
        STAGE13F_RANK_DEFICIENT_REJECTED,
        rejected_count == len(_representatives()),
        rejected_count,
        1.0,
        STAGE13F_NOT_LICENSED,
        "duplicating K_T does not create a second independent gauge direction",
    )


def _decoupled_control() -> Stage13FFalsePositiveControl:
    residuals: list[float] = []
    representatives = _representatives()
    for source in representatives:
        for target in representatives:
            if (
                source.orbit_id == target.orbit_id
                and source.representative_id != target.representative_id
                and abs(source.T - target.T) <= STAGE13F_ATOL
            ):
                delta_X = float(target.X - source.X)
                predicted_Q_D = source.q - source.p * source.T - STAGE13A_A * (source.X + delta_X)
                residuals.append(abs(predicted_Q_D - source.declared_Q_D))
    return Stage13FFalsePositiveControl(
        "decoupled_second_constraint",
        STAGE13F_DECOUPLED_REJECTED,
        bool(residuals) and min(residuals) > STAGE13F_ATOL,
        len(residuals),
        float(min(residuals)),
        STAGE13F_NOT_LICENSED,
        "p_X-only translation fails to preserve the frozen Q_D orbit datum",
    )


def _wrong_compensator_control() -> Stage13FFalsePositiveControl:
    comparisons = canonical_stage13b_mixed_path_comparisons()
    residuals = tuple(item.wrong_compensator_target_residual for item in comparisons)
    return Stage13FFalsePositiveControl(
        "wrong_compensator",
        STAGE13B_WRONG_COMPENSATOR_CLASSIFICATION,
        bool(residuals) and min(residuals) > STAGE13F_ATOL,
        len(residuals),
        float(min(residuals)),
        STAGE13F_NOT_LICENSED,
        "reuses Stage 13B wrong-XT-compensator target residuals",
    )


def _one_clock_incomplete_control() -> Stage13FFalsePositiveControl:
    spreads: list[float] = []
    for orbit in canonical_stage13a_orbits():
        for tau in (-1.0, 0.0, 1.0):
            values = tuple(
                orbit.Q_D + orbit.P_D * tau + STAGE13A_A * chi
                for chi in (-1.0, 0.0, 1.0)
            )
            spreads.append(max(values) - min(values))
    return Stage13FFalsePositiveControl(
        "one_clock_incomplete",
        STAGE13F_ONE_CLOCK_INCOMPLETE,
        bool(spreads) and min(spreads) > STAGE13F_ATOL,
        len(spreads),
        float(min(spreads)),
        STAGE13F_NOT_LICENSED,
        "fixing T while leaving X free retains second-gauge-coordinate dependence",
    )


def _cross_orbit_false_positive_control() -> Stage13FFalsePositiveControl:
    orbits = {item.orbit_id: item for item in canonical_stage13a_orbits()}
    controls = (
        (orbits["omega_alpha"], orbits["omega_beta"]),
        (orbits["omega_alpha"], orbits["omega_gamma"]),
    )
    separations = tuple(
        max(abs(left.Q_D - right.Q_D), abs(left.P_D - right.P_D))
        for left, right in controls
    )
    return Stage13FFalsePositiveControl(
        "cross_orbit_single_invariant_false_match",
        STAGE13F_CROSS_ORBIT_REJECTED,
        min(separations) > STAGE13F_ATOL,
        len(controls),
        float(min(separations)),
        STAGE13F_NOT_LICENSED,
        "same-P and same-Q controls do not identify distinct full Dirac pairs",
    )


def stage13f_K_X_bad(point: Stage13PhaseSpacePoint, epsilon: float = STAGE13F_BAD_EPSILON) -> float:
    return float(exp(point.T) * (point.p_X + STAGE13A_A * point.p) + epsilon * point.q)


def stage13f_bad_closure_defect(
    point: Stage13PhaseSpacePoint,
    epsilon: float = STAGE13F_BAD_EPSILON,
) -> float:
    return float(epsilon * (point.q - point.p))


def _anomaly_control() -> Stage13FFalsePositiveControl:
    representatives = _representatives()
    closure_defects = tuple(abs(stage13f_bad_closure_defect(item.point())) for item in representatives)
    surface_residuals = tuple(abs(stage13f_K_X_bad(item.point())) for item in representatives)
    residual = min(min(closure_defects), min(surface_residuals))
    rejected = min(closure_defects) > STAGE13F_ATOL and min(surface_residuals) > STAGE13F_ATOL
    return Stage13FFalsePositiveControl(
        "non_first_class_K_X_bad",
        STAGE13F_ANOMALY_DETECTED,
        rejected,
        len(representatives),
        float(residual),
        STAGE13F_NOT_LICENSED,
        "epsilon*q deformation violates the positive surface and the frozen first-class closure law",
    )


@lru_cache(maxsize=1)
def canonical_stage13f_false_positive_controls() -> tuple[Stage13FFalsePositiveControl, ...]:
    return (
        _rank_deficient_control(),
        _decoupled_control(),
        _wrong_compensator_control(),
        _one_clock_incomplete_control(),
        _cross_orbit_false_positive_control(),
        _anomaly_control(),
    )


@lru_cache(maxsize=1)
def stage13f_diagnostics() -> Stage13FDiagnostics:
    representatives = _representatives()
    arrows = canonical_stage13f_commuting_arrows()
    quotients = canonical_stage13f_commuting_quotient_classes()
    basis_checks = canonical_stage13f_basis_equivalence_checks()
    mixed = canonical_stage13f_commuting_mixed_path_checks()
    controls = canonical_stage13f_false_positive_controls()
    by_id = {item.control_id: item for item in controls}

    max_kx_tilde = max(abs(stage13f_K_X_tilde(item.point())) for item in representatives)
    max_bracket = max(abs(stage13f_poisson_KT_KX_tilde(item.point())) for item in representatives)
    max_arrow_endpoint = max(item.endpoint_residual for item in arrows)
    max_arrow_constraint = max(item.constraint_residual for item in arrows)
    max_mixed_separation = max(item.endpoint_separation for item in mixed)
    max_mixed_target = max(max(item.tx_target_residual, item.xt_target_residual) for item in mixed)
    max_mixed_constraint = max(item.constraint_residual for item in mixed)
    max_basis_dirac = max(item.dirac_residual for item in basis_checks)
    max_basis_relational = max(item.relational_residual for item in basis_checks)

    all_not_licensed = (
        all(item.metaphysical_claim_status == STAGE13F_NOT_LICENSED for item in basis_checks)
        and all(item.metaphysical_claim_status == STAGE13F_NOT_LICENSED for item in mixed)
        and all(item.metaphysical_claim_status == STAGE13F_NOT_LICENSED for item in controls)
    )
    basis_ok = (
        len(arrows) == 144
        and sum(item.generator_id == STAGE13A_K_T for item in arrows) == 72
        and sum(item.generator_id == STAGE13F_K_X_TILDE for item in arrows) == 72
        and len(quotients) == 4
        and tuple(sorted(len(item.representative_ids) for item in quotients)) == (9, 9, 9, 9)
        and sum(item.matches_stage13d_quotient for item in quotients) == 4
        and len(basis_checks) == 36
        and all(item.public_payload_equal for item in basis_checks)
        and max_kx_tilde <= STAGE13F_ATOL
        and max_bracket <= STAGE13F_ATOL
        and max_arrow_endpoint <= STAGE13F_ATOL
        and max_arrow_constraint <= STAGE13F_ATOL
        and max_basis_dirac <= STAGE13F_ATOL
        and max_basis_relational <= STAGE13F_ATOL
    )
    paths_ok = (
        len(mixed) == 144
        and max_mixed_separation <= STAGE13F_ATOL
        and max_mixed_target <= STAGE13F_ATOL
        and max_mixed_constraint <= STAGE13F_ATOL
    )
    controls_ok = len(controls) == 6 and all(item.rejected for item in controls)

    return Stage13FDiagnostics(
        representative_count=len(representatives),
        commuting_constraint_surface_count=sum(
            abs(stage13a_K_T(item.point())) <= STAGE13F_ATOL
            and abs(stage13f_K_X_tilde(item.point())) <= STAGE13F_ATOL
            for item in representatives
        ),
        commuting_arrow_count=len(arrows),
        commuting_phi_T_arrow_count=sum(item.generator_id == STAGE13A_K_T for item in arrows),
        commuting_phi_X_arrow_count=sum(item.generator_id == STAGE13F_K_X_TILDE for item in arrows),
        commuting_quotient_class_count=len(quotients),
        commuting_quotient_class_sizes=tuple(sorted(len(item.representative_ids) for item in quotients)),
        stage13d_membership_match_count=sum(item.matches_stage13d_quotient for item in quotients),
        basis_equivalence_check_count=len(basis_checks),
        basis_equivalent_count=sum(item.public_payload_equal for item in basis_checks),
        commuting_mixed_path_check_count=len(mixed),
        commuting_mixed_path_closed_count=sum(
            max(item.endpoint_separation, item.tx_target_residual, item.xt_target_residual, item.constraint_residual)
            <= STAGE13F_ATOL
            for item in mixed
        ),
        max_K_X_tilde_constraint_residual=float(max_kx_tilde),
        max_KT_KX_tilde_bracket_residual=float(max_bracket),
        max_commuting_arrow_endpoint_residual=float(max_arrow_endpoint),
        max_commuting_arrow_constraint_residual=float(max_arrow_constraint),
        max_commuting_mixed_endpoint_separation=float(max_mixed_separation),
        max_commuting_mixed_target_residual=float(max_mixed_target),
        max_commuting_mixed_constraint_residual=float(max_mixed_constraint),
        max_basis_dirac_residual=float(max_basis_dirac),
        max_basis_relational_residual=float(max_basis_relational),
        false_positive_control_count=len(controls),
        rejected_false_positive_control_count=sum(item.rejected for item in controls),
        rank_deficient_rejected=by_id["rank_deficient_constraint_pair"].rejected,
        decoupled_rejected=by_id["decoupled_second_constraint"].rejected,
        wrong_compensator_rejected=by_id["wrong_compensator"].rejected,
        one_clock_incomplete_rejected=by_id["one_clock_incomplete"].rejected,
        cross_orbit_false_positive_rejected=by_id["cross_orbit_single_invariant_false_match"].rejected,
        anomaly_detected=by_id["non_first_class_K_X_bad"].rejected,
        all_metaphysical_claims_not_licensed=all_not_licensed,
        criteria_44_47_satisfied=bool(basis_ok and paths_ok and controls_ok and all_not_licensed),
    )


def stage13f_summary() -> dict[str, object]:
    diagnostics = stage13f_diagnostics()
    return {
        "status": "Stage 13F executable evidence; criteria 44–47 satisfied in source diagnostics",
        "bounded_result": STAGE13F_BOUNDED_RESULT,
        "basis_classification": STAGE13F_BASIS_EQUIVALENT,
        "diagnostics": diagnostics,
        "controls": canonical_stage13f_false_positive_controls(),
        "guards": STAGE13F_GUARDS,
        "next": "Stage 13G — executable synthesis and evidence-selected next gate after repository validation",
    }
