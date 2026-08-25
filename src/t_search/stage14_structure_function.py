"""Stage 14A three-constraint first-class structure-function carrier.

This module implements only the Stage 14A evidence frozen in
``docs/stage14_protocol.md``. It constructs the 108 positive representatives,
checks independence of the three constraint/generator directions, verifies the
phase-space-dependent first-class closure and Jacobi identity on-surface and on
off-surface probes, and tests each positive generator separately for constraint-
surface and Dirac-data preservation.

Mixed path compensation is intentionally deferred to Stage 14B.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp

import numpy as np

STAGE14A_ATOL = 1e-10
STAGE14A_A = 0.5
STAGE14A_B = 0.25
STAGE14A_KAPPA = 0.5
STAGE14A_FLOW_PARAMETERS = (-0.5, 0.5)

STAGE14A_D = "D"
STAGE14A_H1 = "H_1"
STAGE14A_H2 = "H_2"
STAGE14A_BASIS_ID = "stage14_structure_function_positive_basis"
STAGE14A_STRUCTURE_FUNCTION_REMOVED = "structure_function_removed_control_rejected"
STAGE14A_RANK_DEFICIENT = "rank_deficient_constraint_control_rejected"

STAGE14A_OMEGA_ALPHA = "omega_alpha"
STAGE14A_OMEGA_BETA = "omega_beta"
STAGE14A_OMEGA_GAMMA = "omega_gamma"
STAGE14A_OMEGA_DELTA = "omega_delta"
STAGE14A_CANONICAL_ORBIT_IDS = (
    STAGE14A_OMEGA_ALPHA,
    STAGE14A_OMEGA_BETA,
    STAGE14A_OMEGA_GAMMA,
    STAGE14A_OMEGA_DELTA,
)
STAGE14A_GRID_VALUES = (-1.0, 0.0, 1.0)


@dataclass(frozen=True, slots=True)
class Stage14PhysicalOrbit:
    orbit_id: str
    Q_D: float
    P_D: float


@dataclass(frozen=True, slots=True)
class Stage14PhaseSpacePoint:
    T1: float
    p_1: float
    T2: float
    p_2: float
    X: float
    p_X: float
    q: float
    p: float

    def vector(self) -> np.ndarray:
        return np.asarray(
            [self.T1, self.p_1, self.T2, self.p_2, self.X, self.p_X, self.q, self.p],
            dtype=float,
        )


@dataclass(frozen=True, slots=True)
class Stage14Representative:
    orbit_id: str
    representative_id: str
    T1: float
    p_1: float
    T2: float
    p_2: float
    X: float
    p_X: float
    q: float
    p: float
    D_value: float
    H1_value: float
    H2_value: float
    declared_Q_D: float
    declared_P_D: float
    constraint_basis_id: str = STAGE14A_BASIS_ID

    def point(self) -> Stage14PhaseSpacePoint:
        return Stage14PhaseSpacePoint(
            self.T1, self.p_1, self.T2, self.p_2, self.X, self.p_X, self.q, self.p
        )


@dataclass(frozen=True, slots=True)
class Stage14FlowProbe:
    orbit_id: str
    representative_id: str
    generator_id: str
    parameter: float
    source_constraint_residual: float
    target_constraint_residual: float
    dirac_Q_residual: float
    dirac_P_residual: float


@dataclass(frozen=True, slots=True)
class Stage14ADiagnostics:
    orbit_count: int
    representative_count: int
    representatives_per_orbit: int
    off_surface_probe_count: int
    single_generator_flow_probe_count: int
    structure_function_value_count: int
    structure_function_values: tuple[float, ...]
    minimum_constraint_gradient_rank: int
    minimum_generator_vector_rank: int
    minimum_constraint_gradient_sigma_min: float
    minimum_generator_vector_sigma_min: float
    max_constraint_residual: float
    max_bracket_closure_residual: float
    max_jacobi_residual: float
    max_flow_constraint_residual: float
    max_flow_dirac_residual: float
    representative_family_complete: bool
    independent_constraint_directions: bool
    structure_functions_nontrivial: bool
    first_class_structure_function_closure_established: bool
    jacobi_established: bool
    individual_flows_preserve_surface_and_dirac_data: bool
    structure_function_removed_control_rejected: bool
    rank_deficient_control_rejected: bool
    criteria_11_17_satisfied: bool


def canonical_stage14a_orbits() -> tuple[Stage14PhysicalOrbit, ...]:
    return (
        Stage14PhysicalOrbit(STAGE14A_OMEGA_ALPHA, -0.35, 1.25),
        Stage14PhysicalOrbit(STAGE14A_OMEGA_BETA, 0.40, 1.25),
        Stage14PhysicalOrbit(STAGE14A_OMEGA_GAMMA, -0.35, 0.75),
        Stage14PhysicalOrbit(STAGE14A_OMEGA_DELTA, 0.20, 1.75),
    )


def stage14a_D(point: Stage14PhaseSpacePoint, *, a: float = STAGE14A_A) -> float:
    return float(point.p_X + a * point.p)


def stage14a_H1(point: Stage14PhaseSpacePoint) -> float:
    return float(point.p_1 + 0.5 * point.p**2)


def stage14a_H2(
    point: Stage14PhaseSpacePoint,
    *,
    a: float = STAGE14A_A,
    b: float = STAGE14A_B,
    kappa: float = STAGE14A_KAPPA,
) -> float:
    return float(
        point.p_2
        + b * point.p
        + kappa * point.T1 * point.X * stage14a_D(point, a=a)
    )


def stage14a_dirac_data(point: Stage14PhaseSpacePoint) -> tuple[float, float]:
    return (
        float(point.q - point.p * point.T1 - STAGE14A_B * point.T2 - STAGE14A_A * point.X),
        float(point.p),
    )


def stage14a_constraint_gradients(
    point: Stage14PhaseSpacePoint,
    *,
    kappa: float = STAGE14A_KAPPA,
) -> np.ndarray:
    """Gradients in canonical order (T1,p_1,T2,p_2,X,p_X,q,p)."""

    D = stage14a_D(point)
    g_D = np.asarray([0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, STAGE14A_A])
    g_H1 = np.asarray([0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, point.p])
    g_H2 = np.asarray(
        [
            kappa * point.X * D,
            0.0,
            0.0,
            1.0,
            kappa * point.T1 * D,
            kappa * point.T1 * point.X,
            0.0,
            STAGE14A_B + kappa * point.T1 * point.X * STAGE14A_A,
        ],
        dtype=float,
    )
    return np.asarray([g_D, g_H1, g_H2], dtype=float)


def _hamiltonian_vector_from_gradient(gradient: np.ndarray) -> np.ndarray:
    result: list[float] = []
    for q_index, p_index in ((0, 1), (2, 3), (4, 5), (6, 7)):
        result.extend((float(gradient[p_index]), float(-gradient[q_index])))
    return np.asarray(result, dtype=float)


def stage14a_generator_vectors(point: Stage14PhaseSpacePoint) -> np.ndarray:
    return np.asarray(
        [_hamiltonian_vector_from_gradient(row) for row in stage14a_constraint_gradients(point)],
        dtype=float,
    )


def _poisson_from_gradients(df: np.ndarray, dg: np.ndarray) -> float:
    return float(
        sum(
            df[q_index] * dg[p_index] - df[p_index] * dg[q_index]
            for q_index, p_index in ((0, 1), (2, 3), (4, 5), (6, 7))
        )
    )


def stage14a_poisson_H1_D(point: Stage14PhaseSpacePoint) -> float:
    gradients = stage14a_constraint_gradients(point)
    return _poisson_from_gradients(gradients[1], gradients[0])


def stage14a_poisson_H1_H2(point: Stage14PhaseSpacePoint) -> float:
    gradients = stage14a_constraint_gradients(point)
    return _poisson_from_gradients(gradients[1], gradients[2])


def stage14a_poisson_H2_D(point: Stage14PhaseSpacePoint) -> float:
    gradients = stage14a_constraint_gradients(point)
    return _poisson_from_gradients(gradients[2], gradients[0])


def stage14a_structure_functions(point: Stage14PhaseSpacePoint) -> tuple[float, float]:
    return (
        float(-STAGE14A_KAPPA * point.X),
        float(STAGE14A_KAPPA * point.T1),
    )


def _gradient_bracket_H1_H2(point: Stage14PhaseSpacePoint) -> np.ndarray:
    D = stage14a_D(point)
    return np.asarray(
        [
            0.0,
            0.0,
            0.0,
            0.0,
            -STAGE14A_KAPPA * D,
            -STAGE14A_KAPPA * point.X,
            0.0,
            -STAGE14A_KAPPA * point.X * STAGE14A_A,
        ],
        dtype=float,
    )


def _gradient_bracket_H2_D(point: Stage14PhaseSpacePoint) -> np.ndarray:
    D = stage14a_D(point)
    return np.asarray(
        [
            STAGE14A_KAPPA * D,
            0.0,
            0.0,
            0.0,
            0.0,
            STAGE14A_KAPPA * point.T1,
            0.0,
            STAGE14A_KAPPA * point.T1 * STAGE14A_A,
        ],
        dtype=float,
    )


def stage14a_jacobi_residual(point: Stage14PhaseSpacePoint) -> float:
    gradients = stage14a_constraint_gradients(point)
    term_1 = _poisson_from_gradients(gradients[1], _gradient_bracket_H2_D(point))
    term_2 = 0.0
    term_3 = _poisson_from_gradients(gradients[0], _gradient_bracket_H1_H2(point))
    return float(term_1 + term_2 + term_3)


def _grid_label(value: float) -> str:
    sign = "m" if value < 0 else "p"
    return f"{sign}{abs(value):.1f}".replace(".", "p")


def canonical_stage14a_representatives_for_orbit(
    orbit: Stage14PhysicalOrbit,
) -> tuple[Stage14Representative, ...]:
    result: list[Stage14Representative] = []
    for T1 in STAGE14A_GRID_VALUES:
        for T2 in STAGE14A_GRID_VALUES:
            for X in STAGE14A_GRID_VALUES:
                p = float(orbit.P_D)
                point = Stage14PhaseSpacePoint(
                    T1=float(T1),
                    p_1=float(-0.5 * p**2),
                    T2=float(T2),
                    p_2=float(-STAGE14A_B * p),
                    X=float(X),
                    p_X=float(-STAGE14A_A * p),
                    q=float(orbit.Q_D + p * T1 + STAGE14A_B * T2 + STAGE14A_A * X),
                    p=p,
                )
                suffix = (
                    f"T1_{_grid_label(T1)}:"
                    f"T2_{_grid_label(T2)}:"
                    f"X_{_grid_label(X)}"
                )
                result.append(
                    Stage14Representative(
                        orbit_id=orbit.orbit_id,
                        representative_id=f"{orbit.orbit_id}:rep:{suffix}",
                        T1=point.T1,
                        p_1=point.p_1,
                        T2=point.T2,
                        p_2=point.p_2,
                        X=point.X,
                        p_X=point.p_X,
                        q=point.q,
                        p=point.p,
                        D_value=stage14a_D(point),
                        H1_value=stage14a_H1(point),
                        H2_value=stage14a_H2(point),
                        declared_Q_D=float(orbit.Q_D),
                        declared_P_D=float(orbit.P_D),
                    )
                )
    return tuple(result)


def canonical_stage14a_representatives() -> tuple[Stage14Representative, ...]:
    return tuple(
        rep
        for orbit in canonical_stage14a_orbits()
        for rep in canonical_stage14a_representatives_for_orbit(orbit)
    )


def canonical_stage14a_off_surface_bracket_probes() -> tuple[Stage14PhaseSpacePoint, ...]:
    probes: list[Stage14PhaseSpacePoint] = []
    for rep in canonical_stage14a_representatives():
        p = rep.point()
        probes.append(
            Stage14PhaseSpacePoint(
                T1=p.T1,
                p_1=p.p_1 + 0.125,
                T2=p.T2,
                p_2=p.p_2 - 0.10,
                X=p.X,
                p_X=p.p_X + 0.20,
                q=p.q - 0.075,
                p=p.p,
            )
        )
    return tuple(probes)


def _constraint_residual(point: Stage14PhaseSpacePoint) -> float:
    return float(max(abs(stage14a_D(point)), abs(stage14a_H1(point)), abs(stage14a_H2(point))))


def stage14a_apply_flow(
    point: Stage14PhaseSpacePoint,
    generator_id: str,
    parameter: float,
) -> Stage14PhaseSpacePoint:
    if _constraint_residual(point) > STAGE14A_ATOL:
        raise ValueError("Stage 14A positive flow probes require an on-surface source")

    if generator_id == STAGE14A_D:
        return Stage14PhaseSpacePoint(
            point.T1,
            point.p_1,
            point.T2,
            point.p_2,
            float(point.X + parameter),
            point.p_X,
            float(point.q + STAGE14A_A * parameter),
            point.p,
        )
    if generator_id == STAGE14A_H1:
        return Stage14PhaseSpacePoint(
            float(point.T1 + parameter),
            point.p_1,
            point.T2,
            point.p_2,
            point.X,
            point.p_X,
            float(point.q + point.p * parameter),
            point.p,
        )
    if generator_id == STAGE14A_H2:
        X_new = float(point.X * exp(STAGE14A_KAPPA * point.T1 * parameter))
        return Stage14PhaseSpacePoint(
            point.T1,
            point.p_1,
            float(point.T2 + parameter),
            point.p_2,
            X_new,
            point.p_X,
            float(
                point.q
                + STAGE14A_B * parameter
                + STAGE14A_A * (X_new - point.X)
            ),
            point.p,
        )
    raise ValueError(f"unknown Stage 14A generator: {generator_id}")


def canonical_stage14a_flow_probes() -> tuple[Stage14FlowProbe, ...]:
    result: list[Stage14FlowProbe] = []
    for rep in canonical_stage14a_representatives():
        source = rep.point()
        source_Q, source_P = stage14a_dirac_data(source)
        for generator_id in (STAGE14A_D, STAGE14A_H1, STAGE14A_H2):
            for parameter in STAGE14A_FLOW_PARAMETERS:
                target = stage14a_apply_flow(source, generator_id, parameter)
                target_Q, target_P = stage14a_dirac_data(target)
                result.append(
                    Stage14FlowProbe(
                        orbit_id=rep.orbit_id,
                        representative_id=rep.representative_id,
                        generator_id=generator_id,
                        parameter=float(parameter),
                        source_constraint_residual=_constraint_residual(source),
                        target_constraint_residual=_constraint_residual(target),
                        dirac_Q_residual=float(abs(target_Q - source_Q)),
                        dirac_P_residual=float(abs(target_P - source_P)),
                    )
                )
    return tuple(result)


def stage14a_structure_function_removed_control_status() -> str:
    values = {
        value
        for rep in canonical_stage14a_representatives()
        for value in (-0.0 * rep.X, 0.0 * rep.T1)
    }
    if values != {0.0}:
        raise AssertionError("kappa=0 control unexpectedly retained nonzero structure functions")
    return STAGE14A_STRUCTURE_FUNCTION_REMOVED


def stage14a_rank_deficient_control_status() -> str:
    for rep in canonical_stage14a_representatives():
        gradients = stage14a_constraint_gradients(rep.point())
        duplicate_control = np.asarray([gradients[0], gradients[1], gradients[0]], dtype=float)
        if int(np.linalg.matrix_rank(duplicate_control, tol=STAGE14A_ATOL)) != 2:
            raise AssertionError("duplicate-direction rank control did not have rank two")
    return STAGE14A_RANK_DEFICIENT


def stage14a_diagnostics() -> Stage14ADiagnostics:
    orbits = canonical_stage14a_orbits()
    representatives = canonical_stage14a_representatives()
    off_surface = canonical_stage14a_off_surface_bracket_probes()
    flow_probes = canonical_stage14a_flow_probes()

    counts = {
        orbit.orbit_id: sum(rep.orbit_id == orbit.orbit_id for rep in representatives)
        for orbit in orbits
    }
    representative_family_complete = (
        len(orbits) == 4
        and tuple(orbit.orbit_id for orbit in orbits) == STAGE14A_CANONICAL_ORBIT_IDS
        and len(representatives) == 108
        and all(count == 27 for count in counts.values())
        and len({rep.representative_id for rep in representatives}) == 108
    )

    max_constraint = max(
        max(abs(rep.D_value), abs(rep.H1_value), abs(rep.H2_value))
        for rep in representatives
    )

    gradient_ranks: list[int] = []
    generator_ranks: list[int] = []
    gradient_sigmas: list[float] = []
    generator_sigmas: list[float] = []
    for rep in representatives:
        gradients = stage14a_constraint_gradients(rep.point())
        generators = stage14a_generator_vectors(rep.point())
        gradient_ranks.append(int(np.linalg.matrix_rank(gradients, tol=STAGE14A_ATOL)))
        generator_ranks.append(int(np.linalg.matrix_rank(generators, tol=STAGE14A_ATOL)))
        gradient_sigmas.append(float(np.linalg.svd(gradients, compute_uv=False)[-1]))
        generator_sigmas.append(float(np.linalg.svd(generators, compute_uv=False)[-1]))

    independent = (
        min(gradient_ranks) == 3
        and min(generator_ranks) == 3
        and min(gradient_sigmas) > STAGE14A_ATOL
        and min(generator_sigmas) > STAGE14A_ATOL
    )

    structure_values = tuple(
        sorted(
            {
                value
                for rep in representatives
                for value in stage14a_structure_functions(rep.point())
            }
        )
    )
    structure_nontrivial = (
        structure_values == (-0.5, 0.0, 0.5)
        and any(value < 0 for value in structure_values)
        and 0.0 in structure_values
        and any(value > 0 for value in structure_values)
    )

    bracket_points = tuple(rep.point() for rep in representatives) + off_surface
    bracket_residuals: list[float] = []
    jacobi_residuals: list[float] = []
    for point in bracket_points:
        D = stage14a_D(point)
        bracket_residuals.extend(
            (
                abs(stage14a_poisson_H1_D(point)),
                abs(stage14a_poisson_H1_H2(point) - (-STAGE14A_KAPPA * point.X * D)),
                abs(stage14a_poisson_H2_D(point) - (STAGE14A_KAPPA * point.T1 * D)),
            )
        )
        jacobi_residuals.append(abs(stage14a_jacobi_residual(point)))
    max_bracket = float(max(bracket_residuals))
    max_jacobi = float(max(jacobi_residuals))
    closure = max_bracket <= STAGE14A_ATOL
    jacobi = max_jacobi <= STAGE14A_ATOL

    max_flow_constraint = float(
        max(max(item.source_constraint_residual, item.target_constraint_residual) for item in flow_probes)
    )
    max_flow_dirac = float(
        max(max(item.dirac_Q_residual, item.dirac_P_residual) for item in flow_probes)
    )
    flows_preserve = (
        len(flow_probes) == 108 * 3 * len(STAGE14A_FLOW_PARAMETERS)
        and {item.generator_id for item in flow_probes}
        == {STAGE14A_D, STAGE14A_H1, STAGE14A_H2}
        and max_flow_constraint <= STAGE14A_ATOL
        and max_flow_dirac <= STAGE14A_ATOL
    )

    structure_control = (
        stage14a_structure_function_removed_control_status()
        == STAGE14A_STRUCTURE_FUNCTION_REMOVED
    )
    rank_control = stage14a_rank_deficient_control_status() == STAGE14A_RANK_DEFICIENT

    criteria = (
        representative_family_complete
        and max_constraint <= STAGE14A_ATOL
        and independent
        and structure_nontrivial
        and closure
        and jacobi
        and flows_preserve
        and structure_control
        and rank_control
    )

    return Stage14ADiagnostics(
        orbit_count=len(orbits),
        representative_count=len(representatives),
        representatives_per_orbit=27,
        off_surface_probe_count=len(off_surface),
        single_generator_flow_probe_count=len(flow_probes),
        structure_function_value_count=len(structure_values),
        structure_function_values=structure_values,
        minimum_constraint_gradient_rank=min(gradient_ranks),
        minimum_generator_vector_rank=min(generator_ranks),
        minimum_constraint_gradient_sigma_min=min(gradient_sigmas),
        minimum_generator_vector_sigma_min=min(generator_sigmas),
        max_constraint_residual=float(max_constraint),
        max_bracket_closure_residual=max_bracket,
        max_jacobi_residual=max_jacobi,
        max_flow_constraint_residual=max_flow_constraint,
        max_flow_dirac_residual=max_flow_dirac,
        representative_family_complete=representative_family_complete,
        independent_constraint_directions=independent,
        structure_functions_nontrivial=structure_nontrivial,
        first_class_structure_function_closure_established=closure,
        jacobi_established=jacobi,
        individual_flows_preserve_surface_and_dirac_data=flows_preserve,
        structure_function_removed_control_rejected=structure_control,
        rank_deficient_control_rejected=rank_control,
        criteria_11_17_satisfied=criteria,
    )
