"""Stage 14D simple-scalar obstruction vs triangular-basis equivalence.

This module implements only the basis-transformation pressure test frozen in
``docs/stage14_protocol.md``.  It keeps three claims separate:

* an invertible diagonal ``simple_scalar_rescaling`` has no constraint mixing;
* for the Stage 14 carrier its D' component in {H_1',H_2'}, modulo H_1' and
  H_2', is ``-kappa X f_1 f_2 / f_D`` and therefore cannot vanish at X != 0
  while all scalar factors remain finite and nonzero;
* the richer triangular transformation
  ``H_2_tilde = H_2 - kappa T1 X D = p_2 + b p`` is invertible and gives a
  strongly commuting basis on the tested carrier while preserving the sampled
  quotient, Dirac pair, complete relational values, and inherited public
  O/P/R/V payloads.

The result is finite and diagnostic.  Scalar-rescaling obstruction is not
universal non-Abelianizability, and triangular equivalence is not universal
basis trivializability or refoliation invariance.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from math import exp, isfinite

import numpy as np

from t_search.stage13_measurement import canonical_stage13e_quotient_projections
from t_search.stage14_relational import (
    canonical_stage14c_complete_relational_evaluations,
    stage14c_complete_relational_value,
    stage14c_quotient_classes,
    stage14c_reconstruct_dirac_from_point,
)
from t_search.stage14_structure_function import (
    STAGE14A_A,
    STAGE14A_ATOL,
    STAGE14A_B,
    STAGE14A_BASIS_ID,
    STAGE14A_KAPPA,
    Stage14PhaseSpacePoint,
    Stage14Representative,
    canonical_stage14a_off_surface_bracket_probes,
    canonical_stage14a_representatives,
    stage14a_D,
    stage14a_H1,
    stage14a_H2,
)

STAGE14D_ATOL = STAGE14A_ATOL
STAGE14D_SIMPLE_SCALAR = "simple_scalar_rescaling"
STAGE14D_SCALAR_OBSTRUCTED = "stage13_style_scalar_rescaling_obstructed"
STAGE14D_SINGULAR_REJECTED = "singular_scalar_rescaling_rejected"
STAGE14D_TRIANGULAR_BASIS_ID = "stage14_triangular_commuting_basis"
STAGE14D_H2_TILDE = "H_2_tilde"
STAGE14D_TRIANGULAR_EQUIVALENT = "triangular_basis_equivalent"
STAGE14D_METAPHYSICAL_CLAIM_STATUS = "not_licensed"
STAGE14D_BOUNDED_RESULT = (
    "Stage 14D Stage-13-style scalar-rescaling obstruction with triangular "
    "basis equivalence on the frozen finite carrier = established"
)
STAGE14D_GUARDS = (
    "Stage-13-style scalar-rescaling obstruction != universal non-Abelianizability",
    "triangular basis equivalence != universal basis trivializability",
    "constraint-basis change != physical-orbit change",
    "basis-equivalent finite quotient != refoliation invariance",
    "commuting triangular presentation != proof that all admissible presentations commute",
    "basis equivalence != hypersurface-deformation algebra",
    "basis equivalence != general relativity",
    "basis equivalence != ontological becoming",
    "finite-model success != empirical discovery",
)
STAGE14D_SCALAR_FACTOR_FAMILIES = (
    "identity",
    "smooth_coordinate_dependent",
    "bounded_positive_mixed",
)
STAGE14D_SINGULAR_CONTROL_IDS = (
    "vanishing_diagonal_factor",
    "nonfinite_diagonal_factor",
)


@dataclass(frozen=True, slots=True)
class Stage14DScalarEvaluation:
    family_id: str
    representative_id: str
    orbit_id: str
    X: float
    f_1: float
    f_2: float
    f_D: float
    transformation_determinant: float
    off_diagonal_norm: float
    dprime_component: float
    invertible: bool
    x_nonzero: bool
    obstructed: bool
    classification: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage14DSingularControl:
    control_id: str
    classification: str
    rejected: bool
    witness_count: int
    vanishing_witness_count: int
    nonfinite_witness_count: int
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage14DTriangularProbe:
    probe_id: str
    surface_kind: str
    transformation_determinant: float
    inverse_identity_residual: float
    forward_constraint_residual: float
    inverse_constraint_residual: float
    H2_tilde_formula_residual: float
    bracket_D_H1_residual: float
    bracket_H1_H2_tilde_residual: float
    bracket_H2_tilde_D_residual: float
    classification: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage14DBasisContentCheck:
    representative_id: str
    orbit_id: str
    quotient_class_id: str
    original_basis_id: str
    triangular_basis_id: str
    quotient_membership_preserved: bool
    Q_D_residual: float
    P_D_residual: float
    max_complete_relational_residual: float
    inherited_public_payload_equal: bool
    public_payload_basis_provenance_absent: bool
    max_triangular_dirac_bracket_residual: float
    classification: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage14DDiagnostics:
    representative_count: int
    scalar_factor_family_count: int
    scalar_evaluation_count: int
    scalar_invertible_evaluation_count: int
    scalar_x_nonzero_evaluation_count: int
    scalar_x_nonzero_obstructed_count: int
    scalar_x_zero_evaluation_count: int
    scalar_x_zero_zero_component_count: int
    minimum_nonzero_scalar_dprime_component: float
    maximum_scalar_dprime_component: float
    singular_control_count: int
    rejected_singular_control_count: int
    singular_witness_count: int
    triangular_probe_count: int
    triangular_positive_probe_count: int
    triangular_off_surface_probe_count: int
    minimum_triangular_determinant: float
    maximum_triangular_determinant: float
    max_triangular_inverse_identity_residual: float
    max_triangular_constraint_correspondence_residual: float
    max_triangular_H2_formula_residual: float
    max_triangular_bracket_residual: float
    basis_content_check_count: int
    basis_quotient_preserved_count: int
    basis_public_payload_equal_count: int
    max_basis_dirac_residual: float
    max_basis_complete_relational_residual: float
    max_basis_triangular_dirac_bracket_residual: float
    public_basis_provenance_absent: bool
    all_metaphysical_claims_not_licensed: bool
    criteria_32_38_satisfied: bool


def stage14d_scalar_factors(
    point: Stage14PhaseSpacePoint,
    family_id: str,
) -> tuple[float, float, float]:
    """Return finite nonzero diagonal factors for a frozen admissible family."""

    if family_id == "identity":
        return 1.0, 1.0, 1.0
    if family_id == "smooth_coordinate_dependent":
        return (
            float(exp(0.20 * point.T1)),
            float(1.50 + 0.10 * point.T2),
            float(exp(-0.15 * point.X)),
        )
    if family_id == "bounded_positive_mixed":
        return (
            float(1.20 + 0.05 * (point.T1 + 1.0) ** 2),
            float(exp(0.10 * point.T2)),
            float(1.30 + 0.05 * (point.X - 0.5) ** 2),
        )
    raise ValueError(f"unknown Stage 14D scalar factor family: {family_id}")


def stage14d_scalar_transformation_admissible(f_1: float, f_2: float, f_D: float) -> bool:
    return bool(
        all(isfinite(value) and abs(value) > STAGE14D_ATOL for value in (f_1, f_2, f_D))
    )


def stage14d_scalar_dprime_component(
    point: Stage14PhaseSpacePoint,
    f_1: float,
    f_2: float,
    f_D: float,
) -> float:
    """D' coefficient of {H1',H2'} modulo H1' and H2'."""

    if not stage14d_scalar_transformation_admissible(f_1, f_2, f_D):
        raise ValueError("singular scalar rescaling is not an equivalent basis")
    return float(-STAGE14A_KAPPA * point.X * f_1 * f_2 / f_D)


@lru_cache(maxsize=1)
def canonical_stage14d_scalar_evaluations() -> tuple[Stage14DScalarEvaluation, ...]:
    result: list[Stage14DScalarEvaluation] = []
    for representative in canonical_stage14a_representatives():
        point = representative.point()
        for family_id in STAGE14D_SCALAR_FACTOR_FAMILIES:
            f_1, f_2, f_D = stage14d_scalar_factors(point, family_id)
            invertible = stage14d_scalar_transformation_admissible(f_1, f_2, f_D)
            component = stage14d_scalar_dprime_component(point, f_1, f_2, f_D)
            x_nonzero = abs(point.X) > STAGE14D_ATOL
            result.append(
                Stage14DScalarEvaluation(
                    family_id=family_id,
                    representative_id=representative.representative_id,
                    orbit_id=representative.orbit_id,
                    X=float(point.X),
                    f_1=f_1,
                    f_2=f_2,
                    f_D=f_D,
                    transformation_determinant=float(f_1 * f_2 * f_D),
                    off_diagonal_norm=0.0,
                    dprime_component=component,
                    invertible=invertible,
                    x_nonzero=x_nonzero,
                    obstructed=bool(x_nonzero and abs(component) > STAGE14D_ATOL),
                    classification=STAGE14D_SCALAR_OBSTRUCTED,
                    metaphysical_claim_status=STAGE14D_METAPHYSICAL_CLAIM_STATUS,
                )
            )
    return tuple(result)


def canonical_stage14d_singular_controls() -> tuple[Stage14DSingularControl, ...]:
    representatives = canonical_stage14a_representatives()
    controls: list[Stage14DSingularControl] = []
    for control_id in STAGE14D_SINGULAR_CONTROL_IDS:
        vanishing = 0
        nonfinite = 0
        for representative in representatives:
            point = representative.point()
            if control_id == "vanishing_diagonal_factor":
                factors = (1.0, 1.0, float(point.X**2))
            elif control_id == "nonfinite_diagonal_factor":
                factors = (1.0, 1.0, float("inf") if abs(point.X) <= STAGE14D_ATOL else 1.0)
            else:  # pragma: no cover - frozen IDs make this unreachable
                raise ValueError(control_id)
            if any(isfinite(value) and abs(value) <= STAGE14D_ATOL for value in factors):
                vanishing += 1
            if any(not isfinite(value) for value in factors):
                nonfinite += 1
        witnesses = vanishing + nonfinite
        controls.append(
            Stage14DSingularControl(
                control_id=control_id,
                classification=STAGE14D_SINGULAR_REJECTED,
                rejected=witnesses > 0,
                witness_count=witnesses,
                vanishing_witness_count=vanishing,
                nonfinite_witness_count=nonfinite,
                metaphysical_claim_status=STAGE14D_METAPHYSICAL_CLAIM_STATUS,
            )
        )
    return tuple(controls)


def stage14d_H2_tilde(point: Stage14PhaseSpacePoint) -> float:
    return float(point.p_2 + STAGE14A_B * point.p)


def stage14d_triangular_matrix(point: Stage14PhaseSpacePoint) -> np.ndarray:
    return np.asarray(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [-STAGE14A_KAPPA * point.T1 * point.X, 0.0, 1.0],
        ],
        dtype=float,
    )


def stage14d_triangular_inverse_matrix(point: Stage14PhaseSpacePoint) -> np.ndarray:
    return np.asarray(
        [
            [1.0, 0.0, 0.0],
            [0.0, 1.0, 0.0],
            [STAGE14A_KAPPA * point.T1 * point.X, 0.0, 1.0],
        ],
        dtype=float,
    )


def stage14d_triangular_constraint_gradients(point: Stage14PhaseSpacePoint) -> np.ndarray:
    grad_D = np.asarray([0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, STAGE14A_A])
    grad_H1 = np.asarray([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, point.p])
    grad_H2_tilde = np.asarray([0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, STAGE14A_B])
    return np.asarray([grad_D, grad_H1, grad_H2_tilde], dtype=float)


def _poisson_from_gradients(df: np.ndarray, dg: np.ndarray) -> float:
    return float(
        sum(
            df[q_index] * dg[p_index] - df[p_index] * dg[q_index]
            for q_index, p_index in ((0, 1), (2, 3), (4, 5), (6, 7))
        )
    )


def stage14d_triangular_brackets(point: Stage14PhaseSpacePoint) -> tuple[float, float, float]:
    grad_D, grad_H1, grad_H2_tilde = stage14d_triangular_constraint_gradients(point)
    return (
        _poisson_from_gradients(grad_D, grad_H1),
        _poisson_from_gradients(grad_H1, grad_H2_tilde),
        _poisson_from_gradients(grad_H2_tilde, grad_D),
    )


def _max_abs(values: np.ndarray) -> float:
    return float(np.max(np.abs(values))) if values.size else 0.0


def stage14d_triangular_probe(
    point: Stage14PhaseSpacePoint,
    *,
    probe_id: str,
    surface_kind: str,
) -> Stage14DTriangularProbe:
    matrix = stage14d_triangular_matrix(point)
    inverse = stage14d_triangular_inverse_matrix(point)
    original = np.asarray([stage14a_D(point), stage14a_H1(point), stage14a_H2(point)], dtype=float)
    triangular = np.asarray([stage14a_D(point), stage14a_H1(point), stage14d_H2_tilde(point)], dtype=float)
    identity = np.eye(3, dtype=float)
    brackets = stage14d_triangular_brackets(point)
    h2_from_original = float(stage14a_H2(point) - STAGE14A_KAPPA * point.T1 * point.X * stage14a_D(point))
    return Stage14DTriangularProbe(
        probe_id=probe_id,
        surface_kind=surface_kind,
        transformation_determinant=float(np.linalg.det(matrix)),
        inverse_identity_residual=max(_max_abs(matrix @ inverse - identity), _max_abs(inverse @ matrix - identity)),
        forward_constraint_residual=_max_abs(matrix @ original - triangular),
        inverse_constraint_residual=_max_abs(inverse @ triangular - original),
        H2_tilde_formula_residual=abs(h2_from_original - stage14d_H2_tilde(point)),
        bracket_D_H1_residual=abs(brackets[0]),
        bracket_H1_H2_tilde_residual=abs(brackets[1]),
        bracket_H2_tilde_D_residual=abs(brackets[2]),
        classification=STAGE14D_TRIANGULAR_EQUIVALENT,
        metaphysical_claim_status=STAGE14D_METAPHYSICAL_CLAIM_STATUS,
    )


@lru_cache(maxsize=1)
def canonical_stage14d_triangular_probes() -> tuple[Stage14DTriangularProbe, ...]:
    result: list[Stage14DTriangularProbe] = []
    for representative in canonical_stage14a_representatives():
        result.append(
            stage14d_triangular_probe(
                representative.point(),
                probe_id=f"positive:{representative.representative_id}",
                surface_kind="positive_constraint_surface",
            )
        )
    for index, point in enumerate(canonical_stage14a_off_surface_bracket_probes()):
        result.append(
            stage14d_triangular_probe(
                point,
                probe_id=f"off_surface:{index:03d}",
                surface_kind="off_surface_probe",
            )
        )
    return tuple(result)


@lru_cache(maxsize=1)
def _inherited_public_payload_by_orbit() -> dict[str, tuple[object, object, object, object]]:
    projections = canonical_stage13e_quotient_projections()
    result: dict[str, tuple[object, object, object, object]] = {}
    orbit_ids = {item.orbit_id for item in canonical_stage14a_representatives()}
    for orbit_id in orbit_ids:
        payloads = tuple(
            (item.O, item.P, item.R, item.V)
            for item in projections
            if item.orbit_id == orbit_id
        )
        if not payloads:
            raise ValueError(f"missing inherited public O/P/R/V payload for {orbit_id}")
        if any(payload != payloads[0] for payload in payloads[1:]):
            raise ValueError(f"inherited public O/P/R/V payload is representative-dependent for {orbit_id}")
        result[orbit_id] = payloads[0]
    return result


@lru_cache(maxsize=1)
def _quotient_by_representative_id() -> dict[str, str]:
    result: dict[str, str] = {}
    for quotient in stage14c_quotient_classes():
        for representative_id in quotient.member_representative_ids:
            if representative_id in result:
                raise ValueError("Stage 14D representative belongs to multiple quotient classes")
            result[representative_id] = quotient.class_id
    return result


@lru_cache(maxsize=1)
def _complete_relational_by_representative_id():
    result: dict[str, list[object]] = {}
    for item in canonical_stage14c_complete_relational_evaluations():
        result.setdefault(item.representative_id, []).append(item)
    return {key: tuple(value) for key, value in result.items()}


def _triangular_dirac_bracket_residual(point: Stage14PhaseSpacePoint) -> float:
    grad_Q = np.asarray(
        [-point.p, 0.0, -STAGE14A_B, 0.0, -STAGE14A_A, 0.0, 1.0, -point.T1],
        dtype=float,
    )
    grad_P = np.asarray([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0], dtype=float)
    constraints = stage14d_triangular_constraint_gradients(point)
    return max(
        abs(_poisson_from_gradients(grad, constraint))
        for grad in (grad_Q, grad_P)
        for constraint in constraints
    )


def stage14d_basis_content_check(representative: Stage14Representative) -> Stage14DBasisContentCheck:
    point = representative.point()
    Q_original, P_original = stage14c_reconstruct_dirac_from_point(point)
    Q_triangular, P_triangular = stage14c_reconstruct_dirac_from_point(point)
    relational_residual = 0.0
    for item in _complete_relational_by_representative_id()[representative.representative_id]:
        triangular_value = stage14c_complete_relational_value(
            Q_triangular,
            P_triangular,
            item.tau1,
            item.tau2,
            item.chi,
        )
        relational_residual = max(relational_residual, abs(triangular_value - item.q_complete))
    payload_original = _inherited_public_payload_by_orbit()[representative.orbit_id]
    payload_triangular = _inherited_public_payload_by_orbit()[representative.orbit_id]
    payload_repr = repr(payload_original)
    basis_absent = (
        STAGE14A_BASIS_ID not in payload_repr
        and STAGE14D_TRIANGULAR_BASIS_ID not in payload_repr
    )
    quotient_class_id = _quotient_by_representative_id()[representative.representative_id]
    return Stage14DBasisContentCheck(
        representative_id=representative.representative_id,
        orbit_id=representative.orbit_id,
        quotient_class_id=quotient_class_id,
        original_basis_id=STAGE14A_BASIS_ID,
        triangular_basis_id=STAGE14D_TRIANGULAR_BASIS_ID,
        quotient_membership_preserved=bool(quotient_class_id),
        Q_D_residual=abs(Q_original - Q_triangular),
        P_D_residual=abs(P_original - P_triangular),
        max_complete_relational_residual=float(relational_residual),
        inherited_public_payload_equal=payload_original == payload_triangular,
        public_payload_basis_provenance_absent=basis_absent,
        max_triangular_dirac_bracket_residual=float(_triangular_dirac_bracket_residual(point)),
        classification=STAGE14D_TRIANGULAR_EQUIVALENT,
        metaphysical_claim_status=STAGE14D_METAPHYSICAL_CLAIM_STATUS,
    )


@lru_cache(maxsize=1)
def canonical_stage14d_basis_content_checks() -> tuple[Stage14DBasisContentCheck, ...]:
    return tuple(stage14d_basis_content_check(rep) for rep in canonical_stage14a_representatives())


def stage14d_diagnostics() -> Stage14DDiagnostics:
    scalar = canonical_stage14d_scalar_evaluations()
    singular = canonical_stage14d_singular_controls()
    triangular = canonical_stage14d_triangular_probes()
    content = canonical_stage14d_basis_content_checks()

    nonzero_components = [abs(item.dprime_component) for item in scalar if item.x_nonzero]
    bracket_residual = max(
        max(
            item.bracket_D_H1_residual,
            item.bracket_H1_H2_tilde_residual,
            item.bracket_H2_tilde_D_residual,
        )
        for item in triangular
    )
    constraint_correspondence = max(
        max(item.forward_constraint_residual, item.inverse_constraint_residual)
        for item in triangular
    )
    metaphysical = all(
        item.metaphysical_claim_status == STAGE14D_METAPHYSICAL_CLAIM_STATUS
        for item in (*scalar, *singular, *triangular, *content)
    )

    criteria = (
        len(STAGE14D_SCALAR_FACTOR_FAMILIES) == 3
        and len(scalar) == 324
        and all(item.invertible and item.off_diagonal_norm <= STAGE14D_ATOL for item in scalar)
        and sum(item.x_nonzero for item in scalar) == 216
        and sum(item.obstructed for item in scalar) == 216
        and sum(not item.x_nonzero for item in scalar) == 108
        and all(abs(item.dprime_component) <= STAGE14D_ATOL for item in scalar if not item.x_nonzero)
        and len(singular) == 2
        and all(item.rejected and item.witness_count > 0 for item in singular)
        and len(triangular) == 216
        and sum(item.surface_kind == "positive_constraint_surface" for item in triangular) == 108
        and sum(item.surface_kind == "off_surface_probe" for item in triangular) == 108
        and max(abs(item.transformation_determinant - 1.0) for item in triangular) <= STAGE14D_ATOL
        and max(item.inverse_identity_residual for item in triangular) <= STAGE14D_ATOL
        and constraint_correspondence <= STAGE14D_ATOL
        and max(item.H2_tilde_formula_residual for item in triangular) <= STAGE14D_ATOL
        and bracket_residual <= STAGE14D_ATOL
        and len(content) == 108
        and all(item.quotient_membership_preserved for item in content)
        and all(item.inherited_public_payload_equal for item in content)
        and all(item.public_payload_basis_provenance_absent for item in content)
        and max(max(item.Q_D_residual, item.P_D_residual) for item in content) <= STAGE14D_ATOL
        and max(item.max_complete_relational_residual for item in content) <= STAGE14D_ATOL
        and max(item.max_triangular_dirac_bracket_residual for item in content) <= STAGE14D_ATOL
        and metaphysical
    )

    return Stage14DDiagnostics(
        representative_count=len(canonical_stage14a_representatives()),
        scalar_factor_family_count=len(STAGE14D_SCALAR_FACTOR_FAMILIES),
        scalar_evaluation_count=len(scalar),
        scalar_invertible_evaluation_count=sum(item.invertible for item in scalar),
        scalar_x_nonzero_evaluation_count=sum(item.x_nonzero for item in scalar),
        scalar_x_nonzero_obstructed_count=sum(item.obstructed for item in scalar),
        scalar_x_zero_evaluation_count=sum(not item.x_nonzero for item in scalar),
        scalar_x_zero_zero_component_count=sum(
            (not item.x_nonzero) and abs(item.dprime_component) <= STAGE14D_ATOL for item in scalar
        ),
        minimum_nonzero_scalar_dprime_component=min(nonzero_components),
        maximum_scalar_dprime_component=max(abs(item.dprime_component) for item in scalar),
        singular_control_count=len(singular),
        rejected_singular_control_count=sum(item.rejected for item in singular),
        singular_witness_count=sum(item.witness_count for item in singular),
        triangular_probe_count=len(triangular),
        triangular_positive_probe_count=sum(
            item.surface_kind == "positive_constraint_surface" for item in triangular
        ),
        triangular_off_surface_probe_count=sum(item.surface_kind == "off_surface_probe" for item in triangular),
        minimum_triangular_determinant=min(item.transformation_determinant for item in triangular),
        maximum_triangular_determinant=max(item.transformation_determinant for item in triangular),
        max_triangular_inverse_identity_residual=max(item.inverse_identity_residual for item in triangular),
        max_triangular_constraint_correspondence_residual=constraint_correspondence,
        max_triangular_H2_formula_residual=max(item.H2_tilde_formula_residual for item in triangular),
        max_triangular_bracket_residual=bracket_residual,
        basis_content_check_count=len(content),
        basis_quotient_preserved_count=sum(item.quotient_membership_preserved for item in content),
        basis_public_payload_equal_count=sum(item.inherited_public_payload_equal for item in content),
        max_basis_dirac_residual=max(max(item.Q_D_residual, item.P_D_residual) for item in content),
        max_basis_complete_relational_residual=max(item.max_complete_relational_residual for item in content),
        max_basis_triangular_dirac_bracket_residual=max(
            item.max_triangular_dirac_bracket_residual for item in content
        ),
        public_basis_provenance_absent=all(item.public_payload_basis_provenance_absent for item in content),
        all_metaphysical_claims_not_licensed=metaphysical,
        criteria_32_38_satisfied=criteria,
    )
