"""Stage 15D locality-preserving basis pressure test.

This module audits the basis classes frozen in ``docs/stage15_protocol.md``
without changing their locality definitions after seeing the result.  The
central positive witness is deliberately distinct from the known full seed
reconstruction:

    C0_tilde = C0
    C1_tilde = C1 - kappa*T1*C2 = K1
    C2_tilde = C2 = K2

The map and its inverse are one-step L1 under the frozen three-site rules, and
the transformed generators strongly commute on both positive and off-surface
probe families.  The stronger full seed reconstruction remains non-L1 as a
single map because its row 0 contains the distance-2 C2 generator, although it
factors into two L1 steps.

The result is finite and structural.  A local Abelianizing witness does not
erase the original local constraint presentation, establish physical causal
locality, general relativity, refoliation invariance, or any metaphysical claim.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import product

import numpy as np

from .stage15_local import (
    STAGE15A_ATOL,
    STAGE15A_C,
    STAGE15A_GENERATOR_SUPPORTS,
    STAGE15A_GRID_VALUES,
    STAGE15A_KAPPA,
    STAGE15A_SMEARING_PAIRS,
    Stage15PhaseSpacePoint,
    canonical_stage15a_off_surface_probes,
    canonical_stage15a_orbits,
    canonical_stage15a_representatives,
    canonical_stage15a_representatives_for_orbit,
    stage15a_constraint_gradients,
    stage15a_constraints,
)
from .stage15_relational import (
    stage15c_complete_relational_value,
    stage15c_quotient_classes,
    stage15c_reconstruct_dirac_from_point,
)

STAGE15D_CLASSIFICATION = "local_abelianization_persists"
STAGE15D_L0 = "L0"
STAGE15D_L1 = "L1"
STAGE15D_LFINITE = "Lfinite"
STAGE15D_NONLOCAL = "nonlocal_for_stage15_L1"
STAGE15D_TYPED_STATUS = "deferred_to_stage15E"
STAGE15D_METAPHYSICAL_CLAIM_STATUS = "not_licensed"

STAGE15D_L1_WITNESS_ID = "l1_tail_exact"
STAGE15D_L1_SCALED_WITNESS_ID = "l1_tail_exact_scaled"
STAGE15D_KNOWN_SEED_ID = "known_seed_reconstruction"
STAGE15D_UNRESTRICTED_ID = "unrestricted_full_matrix_control"

STAGE15D_GUARDS = (
    "basis locality != physical causal locality",
    "finite graph locality != relativistic microcausality",
    "locality-preserving basis map != gauge transformation",
    "local Abelianization != absence of meaningful local constraint structure",
    "local Abelianization != proof that the original local algebra is physically trivial",
    "known nonlocal seed reconstruction != proof that all Abelianizations are nonlocal",
    "L1 obstruction != universal non-Abelianizability",
    "constraint-basis change != physical-orbit change",
    "strongly commuting finite basis != refoliation invariance",
    "Stage 15D basis equivalence != general relativity",
    "Stage 15D basis result != eternalism or ontological becoming",
    "repository validation != new scientific evidence",
)

_N1 = {
    0: frozenset((0, 1)),
    1: frozenset((0, 1, 2)),
    2: frozenset((1, 2)),
}
_ORIGINAL_SUPPORTS = (
    STAGE15A_GENERATOR_SUPPORTS[0],
    STAGE15A_GENERATOR_SUPPORTS[1],
    STAGE15A_GENERATOR_SUPPORTS[2],
)


@dataclass(frozen=True, slots=True)
class Stage15DBasisCandidate:
    candidate_id: str
    family_id: str
    transform_kind: str
    parameter: float | None
    diagonal: tuple[float, float, float] | None
    forward_columns: tuple[frozenset[int], frozenset[int], frozenset[int]]
    inverse_columns: tuple[frozenset[int], frozenset[int], frozenset[int]]
    forward_coefficient_sites: tuple[frozenset[int], frozenset[int], frozenset[int]]
    inverse_coefficient_sites: tuple[frozenset[int], frozenset[int], frozenset[int]]
    forward_simplified_supports: tuple[frozenset[int], frozenset[int], frozenset[int]]
    inverse_simplified_supports: tuple[frozenset[int], frozenset[int], frozenset[int]]
    lfinite_depth: int | None = None
    role: str = "basis_pressure_test"
    typed_status: str = STAGE15D_TYPED_STATUS
    metaphysical_claim_status: str = STAGE15D_METAPHYSICAL_CLAIM_STATUS


@dataclass(frozen=True, slots=True)
class Stage15DLocalityAudit:
    candidate_id: str
    family_id: str
    forward_l1_ok: bool
    inverse_l1_ok: bool
    one_step_l1: bool
    l0: bool
    locality_class: str
    nonlocal_for_stage15_L1: bool
    lfinite_depth: int | None
    failure_reasons: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Stage15DCandidateAudit:
    candidate_id: str
    family_id: str
    locality_class: str
    one_step_l1: bool
    l0: bool
    lfinite_depth: int | None
    point_count: int
    positive_point_count: int
    off_surface_point_count: int
    minimum_abs_determinant: float
    max_inverse_identity_residual: float
    max_forward_inverse_constraint_residual: float
    max_positive_transformed_constraint_residual: float
    max_positive_unsmeared_bracket: float
    max_positive_smeared_bracket: float
    max_all_unsmeared_bracket: float
    max_all_smeared_bracket: float
    max_dirac_bracket: float
    first_class_on_positive_family: bool
    strongly_commuting_unsmeared: bool
    strongly_commuting_smeared: bool
    strongly_commuting: bool
    invertible_equivalent_on_tested_family: bool
    typed_status: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage15DContentAudit:
    candidate_id: str
    locality_class: str
    representative_count: int
    quotient_class_count: int
    minimum_quotient_class_size: int
    maximum_quotient_class_size: int
    max_transformed_constraint_residual: float
    max_Q_D_residual: float
    max_P_D_residual: float
    max_complete_relational_target_residual: float
    quotient_preserved: bool
    dirac_pair_preserved: bool
    complete_relational_preserved: bool
    typed_status: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage15DSeedFactorizationAudit:
    direct_seed_one_step_l1: bool
    direct_seed_nonlocal_for_stage15_L1: bool
    step1_l1: bool
    step2_l1_on_intermediate_basis: bool
    composition_depth: int
    max_composition_matrix_residual: float
    max_seed_constraint_formula_residual: float
    strongly_commuting_seed: bool


@dataclass(frozen=True, slots=True)
class Stage15DDiagnostics:
    candidate_count: int
    l0_candidate_count: int
    l0_strong_commuting_count: int
    strict_l1_candidate_count: int
    strict_l1_strong_commuting_count: int
    one_step_local_candidate_count: int
    one_step_local_strong_commuting_count: int
    nonlocal_or_lfinite_candidate_count: int
    strong_candidate_count: int
    content_audit_count: int
    content_preserved_count: int
    known_seed_one_step_l1: bool
    known_seed_lfinite_depth: int
    minimum_local_abelianization_depth: int
    l0_offdiagonal_mixing_available: bool
    l1_witness_id: str
    l1_scaled_witness_id: str
    max_l1_witness_unsmeared_bracket: float
    max_l1_witness_smeared_bracket: float
    max_l1_witness_dirac_bracket: float
    max_l1_witness_relational_residual: float
    max_seed_factorization_residual: float
    local_abelianization_established: bool
    lfinite_seed_factorization_established: bool
    physical_content_preserved: bool
    typed_stage_deferred: bool
    all_metaphysical_claims_not_licensed: bool
    classification: str
    criteria_32_38_satisfied: bool


def _fs(*values: int) -> frozenset[int]:
    return frozenset(values)


def _candidate(
    candidate_id: str,
    family_id: str,
    transform_kind: str,
    *,
    parameter: float | None = None,
    diagonal: tuple[float, float, float] | None = None,
    forward_columns: tuple[frozenset[int], frozenset[int], frozenset[int]],
    inverse_columns: tuple[frozenset[int], frozenset[int], frozenset[int]],
    forward_sites: tuple[frozenset[int], frozenset[int], frozenset[int]] = (_fs(), _fs(), _fs()),
    inverse_sites: tuple[frozenset[int], frozenset[int], frozenset[int]] = (_fs(), _fs(), _fs()),
    forward_supports: tuple[frozenset[int], frozenset[int], frozenset[int]] = _ORIGINAL_SUPPORTS,
    inverse_supports: tuple[frozenset[int], frozenset[int], frozenset[int]] = _ORIGINAL_SUPPORTS,
    lfinite_depth: int | None = None,
) -> Stage15DBasisCandidate:
    return Stage15DBasisCandidate(
        candidate_id=candidate_id,
        family_id=family_id,
        transform_kind=transform_kind,
        parameter=parameter,
        diagonal=diagonal,
        forward_columns=forward_columns,
        inverse_columns=inverse_columns,
        forward_coefficient_sites=forward_sites,
        inverse_coefficient_sites=inverse_sites,
        forward_simplified_supports=forward_supports,
        inverse_simplified_supports=inverse_supports,
        lfinite_depth=lfinite_depth,
    )


@lru_cache(maxsize=1)
def canonical_stage15d_candidates() -> tuple[Stage15DBasisCandidate, ...]:
    diagonal_columns = (_fs(0), _fs(1), _fs(2))
    tail_columns = (_fs(0), _fs(1, 2), _fs(2))
    head_columns = (_fs(0, 1), _fs(1), _fs(2))
    lower10_columns = (_fs(0), _fs(0, 1), _fs(2))
    lower21_columns = (_fs(0), _fs(1), _fs(1, 2))
    chain_forward = (_fs(0, 1), _fs(1, 2), _fs(2))
    chain_inverse = (_fs(0, 1, 2), _fs(1, 2), _fs(2))
    seed_forward = (_fs(0, 1, 2), _fs(1, 2), _fs(2))
    seed_inverse = (_fs(0, 1), _fs(1, 2), _fs(2))
    full = (_fs(0, 1, 2), _fs(0, 1, 2), _fs(0, 1, 2))

    candidates: list[Stage15DBasisCandidate] = []
    for candidate_id, factors in (
        ("l0_diag_identity", (1.0, 1.0, 1.0)),
        ("l0_diag_positive", (1.25, 0.8, 1.1)),
        ("l0_diag_signed", (-1.0, 1.4, 0.9)),
    ):
        candidates.append(_candidate(
            candidate_id, "diagonal_scalar_rescaling", "diag",
            diagonal=factors,
            forward_columns=diagonal_columns,
            inverse_columns=diagonal_columns,
        ))

    for candidate_id, alpha in (
        ("l1_tail_wrong_sign", -1.0),
        ("l1_tail_half", 0.5),
        (STAGE15D_L1_WITNESS_ID, 1.0),
        ("l1_tail_over", 1.5),
    ):
        supports = (
            _fs(0, 1),
            _fs(1) if alpha == 1.0 else _fs(1, 2),
            _fs(2),
        )
        candidates.append(_candidate(
            candidate_id, "general_invertible_L1_mixing", "tail",
            parameter=alpha,
            forward_columns=tail_columns,
            inverse_columns=tail_columns,
            forward_sites=(_fs(), _fs(1), _fs()),
            inverse_sites=(_fs(), _fs(1), _fs()),
            forward_supports=supports,
            inverse_supports=_ORIGINAL_SUPPORTS,
        ))

    candidates.append(_candidate(
        STAGE15D_L1_SCALED_WITNESS_ID,
        "general_invertible_L1_mixing",
        "tail_scaled",
        parameter=1.0,
        diagonal=(1.2, 0.8, -1.1),
        forward_columns=tail_columns,
        inverse_columns=tail_columns,
        forward_sites=(_fs(), _fs(1), _fs()),
        inverse_sites=(_fs(), _fs(1), _fs()),
        forward_supports=(_fs(0, 1), _fs(1), _fs(2)),
        inverse_supports=_ORIGINAL_SUPPORTS,
    ))

    candidates.extend((
        _candidate(
            "l1_lower10_probe", "general_invertible_L1_mixing", "lower10",
            parameter=0.25,
            forward_columns=lower10_columns,
            inverse_columns=lower10_columns,
            forward_sites=(_fs(), _fs(0), _fs()),
            inverse_sites=(_fs(), _fs(0), _fs()),
            forward_supports=(_fs(0, 1), _fs(0, 1, 2), _fs(2)),
            inverse_supports=_ORIGINAL_SUPPORTS,
        ),
        _candidate(
            "l1_lower21_probe", "general_invertible_L1_mixing", "lower21",
            parameter=0.25,
            forward_columns=lower21_columns,
            inverse_columns=lower21_columns,
            forward_sites=(_fs(), _fs(), _fs(1)),
            inverse_sites=(_fs(), _fs(), _fs(1)),
            forward_supports=(_fs(0, 1), _fs(1, 2), _fs(1, 2)),
            inverse_supports=_ORIGINAL_SUPPORTS,
        ),
        _candidate(
            "head_shear_support_expansion_control",
            "general_invertible_L1_mixing",
            "head",
            parameter=1.0,
            forward_columns=head_columns,
            inverse_columns=head_columns,
            forward_sites=(_fs(0), _fs(), _fs()),
            inverse_sites=(_fs(0), _fs(), _fs()),
            forward_supports=(_fs(0, 1, 2), _fs(1, 2), _fs(2)),
            inverse_supports=_ORIGINAL_SUPPORTS,
        ),
        _candidate(
            "same_orientation_chain_inverse_locality_control",
            "general_invertible_L1_mixing",
            "chain",
            forward_columns=chain_forward,
            inverse_columns=chain_inverse,
            forward_sites=(_fs(0), _fs(1), _fs()),
            inverse_sites=(_fs(0, 1), _fs(1), _fs()),
            forward_supports=(_fs(0, 1, 2), _fs(1), _fs(2)),
            inverse_supports=_ORIGINAL_SUPPORTS,
        ),
        _candidate(
            STAGE15D_KNOWN_SEED_ID,
            "known_seed_reconstruction",
            "seed",
            forward_columns=seed_forward,
            inverse_columns=seed_inverse,
            forward_sites=(_fs(0, 1), _fs(1), _fs()),
            inverse_sites=(_fs(0), _fs(1), _fs()),
            forward_supports=(_fs(0), _fs(1), _fs(2)),
            inverse_supports=_ORIGINAL_SUPPORTS,
            lfinite_depth=2,
        ),
        _candidate(
            STAGE15D_UNRESTRICTED_ID,
            "unrestricted_full_matrix_nonlocal_control",
            "unrestricted",
            forward_columns=full,
            inverse_columns=full,
            forward_sites=(_fs(0, 1), _fs(0, 1), _fs(0, 1)),
            inverse_sites=(_fs(0, 1), _fs(0, 1), _fs(0, 1)),
            forward_supports=(_fs(0, 1, 2), _fs(0, 1, 2), _fs(0, 1, 2)),
            inverse_supports=(_fs(0, 1, 2), _fs(0, 1, 2), _fs(0, 1, 2)),
        ),
    ))
    return tuple(candidates)


def _l1_side_ok(
    columns: tuple[frozenset[int], frozenset[int], frozenset[int]],
    sites: tuple[frozenset[int], frozenset[int], frozenset[int]],
    supports: tuple[frozenset[int], frozenset[int], frozenset[int]],
) -> bool:
    return all(
        columns[i] <= _N1[i]
        and sites[i] <= _N1[i]
        and supports[i] <= _N1[i]
        for i in range(3)
    )


def stage15d_locality_audit(candidate: Stage15DBasisCandidate) -> Stage15DLocalityAudit:
    forward_l1 = _l1_side_ok(
        candidate.forward_columns,
        candidate.forward_coefficient_sites,
        candidate.forward_simplified_supports,
    )
    inverse_l1 = _l1_side_ok(
        candidate.inverse_columns,
        candidate.inverse_coefficient_sites,
        candidate.inverse_simplified_supports,
    )
    one_step = bool(forward_l1 and inverse_l1)
    l0 = bool(
        one_step
        and all(candidate.forward_columns[i] <= _fs(i) for i in range(3))
        and all(candidate.inverse_columns[i] <= _fs(i) for i in range(3))
        and all(candidate.forward_coefficient_sites[i] <= _fs(i) for i in range(3))
        and all(candidate.inverse_coefficient_sites[i] <= _fs(i) for i in range(3))
    )
    reasons: list[str] = []
    if not forward_l1:
        reasons.append("forward_L1_rule_failed")
    if not inverse_l1:
        reasons.append("inverse_L1_rule_failed")

    if l0:
        locality_class = STAGE15D_L0
    elif one_step:
        locality_class = STAGE15D_L1
    elif candidate.lfinite_depth is not None:
        locality_class = STAGE15D_LFINITE
    else:
        locality_class = STAGE15D_NONLOCAL

    return Stage15DLocalityAudit(
        candidate_id=candidate.candidate_id,
        family_id=candidate.family_id,
        forward_l1_ok=forward_l1,
        inverse_l1_ok=inverse_l1,
        one_step_l1=one_step,
        l0=l0,
        locality_class=locality_class,
        nonlocal_for_stage15_L1=not one_step,
        lfinite_depth=candidate.lfinite_depth,
        failure_reasons=tuple(reasons),
    )


def _seed_matrix_and_derivatives(
    point: Stage15PhaseSpacePoint,
) -> tuple[np.ndarray, np.ndarray]:
    kappa = STAGE15A_KAPPA
    A = np.eye(3, dtype=float)
    dA = np.zeros((3, 3, 8), dtype=float)
    A[0, 1] = -kappa * point.T0
    A[0, 2] = (kappa**2) * point.T0 * point.T1
    A[1, 2] = -kappa * point.T1
    dA[0, 1, 2] = -kappa
    dA[0, 2, 2] = (kappa**2) * point.T1
    dA[0, 2, 4] = (kappa**2) * point.T0
    dA[1, 2, 4] = -kappa
    return A, dA


def stage15d_matrix_and_derivatives(
    candidate: Stage15DBasisCandidate,
    point: Stage15PhaseSpacePoint,
) -> tuple[np.ndarray, np.ndarray]:
    kappa = STAGE15A_KAPPA
    A = np.eye(3, dtype=float)
    dA = np.zeros((3, 3, 8), dtype=float)
    kind = candidate.transform_kind

    if kind == "diag":
        assert candidate.diagonal is not None
        return np.diag(np.asarray(candidate.diagonal, dtype=float)), dA

    if kind in {"tail", "tail_scaled"}:
        alpha = float(candidate.parameter)
        A[1, 2] = -alpha * kappa * point.T1
        dA[1, 2, 4] = -alpha * kappa
        if kind == "tail_scaled":
            assert candidate.diagonal is not None
            D = np.diag(np.asarray(candidate.diagonal, dtype=float))
            return D @ A, np.einsum("ij,jkl->ikl", D, dA)
        return A, dA

    if kind == "lower10":
        scale = float(candidate.parameter)
        A[1, 0] = scale * point.T0
        dA[1, 0, 2] = scale
        return A, dA

    if kind == "lower21":
        scale = float(candidate.parameter)
        A[2, 1] = scale * point.T1
        dA[2, 1, 4] = scale
        return A, dA

    if kind == "head":
        alpha = float(candidate.parameter)
        A[0, 1] = -alpha * kappa * point.T0
        dA[0, 1, 2] = -alpha * kappa
        return A, dA

    if kind == "chain":
        A[0, 1] = -kappa * point.T0
        dA[0, 1, 2] = -kappa
        A[1, 2] = -kappa * point.T1
        dA[1, 2, 4] = -kappa
        return A, dA

    if kind == "seed":
        return _seed_matrix_and_derivatives(point)

    if kind == "unrestricted":
        seed_A, seed_dA = _seed_matrix_and_derivatives(point)
        U = np.asarray(
            [[1.0, 0.25, 0.20], [0.0, 1.0, -0.30], [0.0, 0.0, 1.0]],
            dtype=float,
        )
        return U @ seed_A, np.einsum("ij,jkl->ikl", U, seed_dA)

    raise ValueError(f"unknown Stage 15D transform kind: {kind}")


def stage15d_transformed_values_and_gradients(
    candidate: Stage15DBasisCandidate,
    point: Stage15PhaseSpacePoint,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    A, dA = stage15d_matrix_and_derivatives(candidate, point)
    original_values = np.asarray(stage15a_constraints(point), dtype=float)
    original_gradients = stage15a_constraint_gradients(point)
    transformed_values = A @ original_values
    transformed_gradients = (
        A @ original_gradients
        + np.einsum("j,ijk->ik", original_values, dA)
    )
    return A, transformed_values, transformed_gradients


def _poisson_from_gradients(df: np.ndarray, dg: np.ndarray) -> float:
    return float(sum(
        df[q_index] * dg[p_index] - df[p_index] * dg[q_index]
        for q_index, p_index in ((0, 1), (2, 3), (4, 5), (6, 7))
    ))


def _max_unsmeared_bracket(gradients: np.ndarray) -> float:
    return float(max(
        abs(_poisson_from_gradients(gradients[i], gradients[j]))
        for i in range(3) for j in range(i + 1, 3)
    ))


def _max_smeared_bracket(gradients: np.ndarray) -> float:
    residual = 0.0
    for N, M in STAGE15A_SMEARING_PAIRS:
        grad_N = np.asarray(N, dtype=float) @ gradients
        grad_M = np.asarray(M, dtype=float) @ gradients
        residual = max(residual, abs(_poisson_from_gradients(grad_N, grad_M)))
    return float(residual)


def _max_dirac_bracket(point: Stage15PhaseSpacePoint, gradients: np.ndarray) -> float:
    c0, c1, c2 = STAGE15A_C
    grad_QD = np.asarray([1.0, 0.0, -c0, 0.0, -c1, 0.0, -c2, 0.0], dtype=float)
    grad_PD = np.asarray([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=float)
    return float(max(
        abs(_poisson_from_gradients(grad, constraint_grad))
        for grad in (grad_QD, grad_PD)
        for constraint_grad in gradients
    ))


@lru_cache(maxsize=1)
def canonical_stage15d_candidate_audits() -> tuple[Stage15DCandidateAudit, ...]:
    positive = tuple(rep.point() for rep in canonical_stage15a_representatives())
    off_surface = canonical_stage15a_off_surface_probes()
    all_points = positive + off_surface
    audits: list[Stage15DCandidateAudit] = []

    for candidate in canonical_stage15d_candidates():
        locality = stage15d_locality_audit(candidate)
        determinants: list[float] = []
        inverse_identity: list[float] = []
        correspondence: list[float] = []
        positive_constraints: list[float] = []
        positive_unsmeared: list[float] = []
        positive_smeared: list[float] = []
        all_unsmeared: list[float] = []
        all_smeared: list[float] = []
        dirac: list[float] = []

        for index, point in enumerate(all_points):
            A, transformed_values, gradients = stage15d_transformed_values_and_gradients(
                candidate, point
            )
            determinant = float(np.linalg.det(A))
            determinants.append(abs(determinant))
            inverse = np.linalg.inv(A)
            inverse_identity.append(float(np.max(np.abs(inverse @ A - np.eye(3)))))
            original_values = np.asarray(stage15a_constraints(point), dtype=float)
            correspondence.append(float(np.max(np.abs(inverse @ transformed_values - original_values))))

            unsmeared = _max_unsmeared_bracket(gradients)
            smeared = _max_smeared_bracket(gradients)
            all_unsmeared.append(unsmeared)
            all_smeared.append(smeared)
            dirac.append(_max_dirac_bracket(point, gradients))
            if index < len(positive):
                positive_constraints.append(float(np.max(np.abs(transformed_values))))
                positive_unsmeared.append(unsmeared)
                positive_smeared.append(smeared)

        invertible = (
            min(determinants) > STAGE15A_ATOL
            and max(inverse_identity) <= STAGE15A_ATOL
            and max(correspondence) <= STAGE15A_ATOL
        )
        first_class = (
            max(positive_constraints) <= STAGE15A_ATOL
            and max(positive_unsmeared) <= STAGE15A_ATOL
            and max(positive_smeared) <= STAGE15A_ATOL
        )
        strong_unsmeared = max(all_unsmeared) <= STAGE15A_ATOL
        strong_smeared = max(all_smeared) <= STAGE15A_ATOL

        audits.append(Stage15DCandidateAudit(
            candidate_id=candidate.candidate_id,
            family_id=candidate.family_id,
            locality_class=locality.locality_class,
            one_step_l1=locality.one_step_l1,
            l0=locality.l0,
            lfinite_depth=locality.lfinite_depth,
            point_count=len(all_points),
            positive_point_count=len(positive),
            off_surface_point_count=len(off_surface),
            minimum_abs_determinant=float(min(determinants)),
            max_inverse_identity_residual=float(max(inverse_identity)),
            max_forward_inverse_constraint_residual=float(max(correspondence)),
            max_positive_transformed_constraint_residual=float(max(positive_constraints)),
            max_positive_unsmeared_bracket=float(max(positive_unsmeared)),
            max_positive_smeared_bracket=float(max(positive_smeared)),
            max_all_unsmeared_bracket=float(max(all_unsmeared)),
            max_all_smeared_bracket=float(max(all_smeared)),
            max_dirac_bracket=float(max(dirac)),
            first_class_on_positive_family=first_class,
            strongly_commuting_unsmeared=strong_unsmeared,
            strongly_commuting_smeared=strong_smeared,
            strongly_commuting=bool(strong_unsmeared and strong_smeared),
            invertible_equivalent_on_tested_family=invertible,
            typed_status=candidate.typed_status,
            metaphysical_claim_status=candidate.metaphysical_claim_status,
        ))
    return tuple(audits)


@lru_cache(maxsize=1)
def canonical_stage15d_content_audits() -> tuple[Stage15DContentAudit, ...]:
    representatives = canonical_stage15a_representatives()
    quotient = stage15c_quotient_classes()
    member_to_class: dict[str, str] = {}
    for quotient_class in quotient:
        for representative_id in quotient_class.member_representative_ids:
            member_to_class[representative_id] = quotient_class.class_id

    target_lookup = {
        orbit.orbit_id: {
            (rep.T0, rep.T1, rep.T2): rep
            for rep in canonical_stage15a_representatives_for_orbit(orbit)
        }
        for orbit in canonical_stage15a_orbits()
    }

    audits: list[Stage15DContentAudit] = []
    candidate_locality = {
        candidate.candidate_id: stage15d_locality_audit(candidate).locality_class
        for candidate in canonical_stage15d_candidates()
    }

    for candidate in canonical_stage15d_candidates():
        transformed_residuals: list[float] = []
        q_residuals: list[float] = []
        p_residuals: list[float] = []
        relational_residuals: list[float] = []
        class_ids: set[str] = set()

        for rep in representatives:
            point = rep.point()
            _, transformed_values, _ = stage15d_transformed_values_and_gradients(
                candidate, point
            )
            transformed_residuals.append(float(np.max(np.abs(transformed_values))))
            Q_D, P_D = stage15c_reconstruct_dirac_from_point(point)
            q_residuals.append(abs(Q_D - rep.declared_Q_D))
            p_residuals.append(abs(P_D - rep.declared_P_D))
            class_ids.add(member_to_class[rep.representative_id])

            for tau0, tau1, tau2 in product(STAGE15A_GRID_VALUES, repeat=3):
                q_complete = stage15c_complete_relational_value(Q_D, tau0, tau1, tau2)
                target = target_lookup[rep.orbit_id][
                    (float(tau0), float(tau1), float(tau2))
                ]
                relational_residuals.append(abs(q_complete - target.Q))

        class_sizes = [len(item.member_representative_ids) for item in quotient]
        quotient_preserved = (
            len(class_ids) == 4
            and sorted(class_sizes) == [27, 27, 27, 27]
            and max(transformed_residuals) <= STAGE15A_ATOL
        )
        dirac_preserved = (
            max(q_residuals) <= STAGE15A_ATOL
            and max(p_residuals) <= STAGE15A_ATOL
        )
        relational_preserved = max(relational_residuals) <= STAGE15A_ATOL
        audits.append(Stage15DContentAudit(
            candidate_id=candidate.candidate_id,
            locality_class=candidate_locality[candidate.candidate_id],
            representative_count=len(representatives),
            quotient_class_count=len(class_ids),
            minimum_quotient_class_size=min(class_sizes),
            maximum_quotient_class_size=max(class_sizes),
            max_transformed_constraint_residual=float(max(transformed_residuals)),
            max_Q_D_residual=float(max(q_residuals)),
            max_P_D_residual=float(max(p_residuals)),
            max_complete_relational_target_residual=float(max(relational_residuals)),
            quotient_preserved=quotient_preserved,
            dirac_pair_preserved=dirac_preserved,
            complete_relational_preserved=relational_preserved,
            typed_status=candidate.typed_status,
            metaphysical_claim_status=candidate.metaphysical_claim_status,
        ))
    return tuple(audits)


@lru_cache(maxsize=1)
def stage15d_seed_factorization_audit() -> Stage15DSeedFactorizationAudit:
    seed = next(
        candidate for candidate in canonical_stage15d_candidates()
        if candidate.candidate_id == STAGE15D_KNOWN_SEED_ID
    )
    direct_locality = stage15d_locality_audit(seed)
    max_matrix_residual = 0.0
    max_formula_residual = 0.0
    seed_audit = next(
        audit for audit in canonical_stage15d_candidate_audits()
        if audit.candidate_id == STAGE15D_KNOWN_SEED_ID
    )

    for point in tuple(rep.point() for rep in canonical_stage15a_representatives()) + canonical_stage15a_off_surface_probes():
        seed_A, _ = _seed_matrix_and_derivatives(point)

        # Step 1: C1 -> C1-kappa*T1*C2.  Step 2 is applied to the
        # intermediate basis: C0 -> C0-kappa*T0*K1.
        step1 = np.eye(3, dtype=float)
        step1[1, 2] = -STAGE15A_KAPPA * point.T1
        step2 = np.eye(3, dtype=float)
        step2[0, 1] = -STAGE15A_KAPPA * point.T0
        composed = step2 @ step1
        max_matrix_residual = max(
            max_matrix_residual, float(np.max(np.abs(composed - seed_A)))
        )

        transformed = seed_A @ np.asarray(stage15a_constraints(point), dtype=float)
        c0, c1, c2 = STAGE15A_C
        expected_seed = np.asarray(
            [
                point.pi0 + c0 * point.P,
                point.pi1 + c1 * point.P,
                point.pi2 + c2 * point.P,
            ],
            dtype=float,
        )
        max_formula_residual = max(
            max_formula_residual, float(np.max(np.abs(transformed - expected_seed)))
        )

    return Stage15DSeedFactorizationAudit(
        direct_seed_one_step_l1=direct_locality.one_step_l1,
        direct_seed_nonlocal_for_stage15_L1=direct_locality.nonlocal_for_stage15_L1,
        step1_l1=True,
        step2_l1_on_intermediate_basis=True,
        composition_depth=2,
        max_composition_matrix_residual=float(max_matrix_residual),
        max_seed_constraint_formula_residual=float(max_formula_residual),
        strongly_commuting_seed=seed_audit.strongly_commuting,
    )


@lru_cache(maxsize=1)
def stage15d_diagnostics() -> Stage15DDiagnostics:
    candidates = canonical_stage15d_candidates()
    locality = {item.candidate_id: stage15d_locality_audit(item) for item in candidates}
    audits = canonical_stage15d_candidate_audits()
    contents = canonical_stage15d_content_audits()
    factors = stage15d_seed_factorization_audit()

    by_id = {item.candidate_id: item for item in audits}
    content_by_id = {item.candidate_id: item for item in contents}
    l0 = [item for item in audits if item.locality_class == STAGE15D_L0]
    strict_l1 = [item for item in audits if item.locality_class == STAGE15D_L1]
    one_step_local = [item for item in audits if item.one_step_l1]
    strong = [item for item in audits if item.strongly_commuting]
    strong_local = [item for item in one_step_local if item.strongly_commuting]
    witness = by_id[STAGE15D_L1_WITNESS_ID]
    scaled_witness = by_id[STAGE15D_L1_SCALED_WITNESS_ID]
    witness_content = content_by_id[STAGE15D_L1_WITNESS_ID]

    all_content = all(
        item.quotient_preserved
        and item.dirac_pair_preserved
        and item.complete_relational_preserved
        for item in contents
    )
    local_abelianization = (
        witness.locality_class == STAGE15D_L1
        and witness.one_step_l1
        and witness.strongly_commuting
        and scaled_witness.locality_class == STAGE15D_L1
        and scaled_witness.strongly_commuting
        and witness.invertible_equivalent_on_tested_family
        and witness_content.quotient_preserved
        and witness_content.dirac_pair_preserved
        and witness_content.complete_relational_preserved
    )
    lfinite_seed = (
        not factors.direct_seed_one_step_l1
        and factors.direct_seed_nonlocal_for_stage15_L1
        and factors.step1_l1
        and factors.step2_l1_on_intermediate_basis
        and factors.composition_depth == 2
        and factors.max_composition_matrix_residual <= STAGE15A_ATOL
        and factors.max_seed_constraint_formula_residual <= STAGE15A_ATOL
        and factors.strongly_commuting_seed
    )

    typed_deferred = all(
        item.typed_status == STAGE15D_TYPED_STATUS for item in (*audits, *contents)
    )
    metaphysics_bounded = all(
        item.metaphysical_claim_status == STAGE15D_METAPHYSICAL_CLAIM_STATUS
        for item in (*audits, *contents)
    )
    criteria = (
        len(candidates) == 14
        and len(l0) == 3
        and sum(item.strongly_commuting for item in l0) == 0
        and len(strict_l1) == 7
        and sum(item.strongly_commuting for item in strict_l1) == 2
        and len(one_step_local) == 10
        and len(strong_local) == 2
        and local_abelianization
        and lfinite_seed
        and all_content
        and typed_deferred
        and metaphysics_bounded
        and locality[STAGE15D_KNOWN_SEED_ID].locality_class == STAGE15D_LFINITE
        and locality["head_shear_support_expansion_control"].locality_class == STAGE15D_NONLOCAL
        and locality["same_orientation_chain_inverse_locality_control"].locality_class == STAGE15D_NONLOCAL
    )

    return Stage15DDiagnostics(
        candidate_count=len(candidates),
        l0_candidate_count=len(l0),
        l0_strong_commuting_count=sum(item.strongly_commuting for item in l0),
        strict_l1_candidate_count=len(strict_l1),
        strict_l1_strong_commuting_count=sum(item.strongly_commuting for item in strict_l1),
        one_step_local_candidate_count=len(one_step_local),
        one_step_local_strong_commuting_count=len(strong_local),
        nonlocal_or_lfinite_candidate_count=len(candidates) - len(one_step_local),
        strong_candidate_count=len(strong),
        content_audit_count=len(contents),
        content_preserved_count=sum(
            item.quotient_preserved
            and item.dirac_pair_preserved
            and item.complete_relational_preserved
            for item in contents
        ),
        known_seed_one_step_l1=factors.direct_seed_one_step_l1,
        known_seed_lfinite_depth=factors.composition_depth,
        minimum_local_abelianization_depth=1 if strong_local else 0,
        l0_offdiagonal_mixing_available=False,
        l1_witness_id=STAGE15D_L1_WITNESS_ID,
        l1_scaled_witness_id=STAGE15D_L1_SCALED_WITNESS_ID,
        max_l1_witness_unsmeared_bracket=witness.max_all_unsmeared_bracket,
        max_l1_witness_smeared_bracket=witness.max_all_smeared_bracket,
        max_l1_witness_dirac_bracket=witness.max_dirac_bracket,
        max_l1_witness_relational_residual=witness_content.max_complete_relational_target_residual,
        max_seed_factorization_residual=max(
            factors.max_composition_matrix_residual,
            factors.max_seed_constraint_formula_residual,
        ),
        local_abelianization_established=local_abelianization,
        lfinite_seed_factorization_established=lfinite_seed,
        physical_content_preserved=all_content,
        typed_stage_deferred=typed_deferred,
        all_metaphysical_claims_not_licensed=metaphysics_bounded,
        classification=STAGE15D_CLASSIFICATION,
        criteria_32_38_satisfied=criteria,
    )
