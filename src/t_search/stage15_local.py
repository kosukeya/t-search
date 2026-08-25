"""Stage 15A spatially indexed local/smeared first-class carrier.

This module implements only the Stage 15A evidence frozen in
``docs/stage15_protocol.md``. It constructs the 108 positive representatives,
checks independence of the three local constraint/generator directions,
verifies the phase-space-dependent first-class algebra on- and off-surface,
and checks local/smeared consistency, antisymmetry, Jacobi, and support.

Finite path ordering and compensators are intentionally deferred to Stage 15B.
Complete quotient/relational claims are deferred to Stage 15C, and basis-search
claims are deferred to Stage 15D.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

STAGE15A_ATOL = 1e-10
STAGE15A_KAPPA = 0.5
STAGE15A_C = (1.0, 0.5, -0.25)
STAGE15A_GRID_VALUES = (-1.0, 0.0, 1.0)
STAGE15A_BASIS_ID = "stage15_spatial_local_positive_basis"

STAGE15A_OMEGA_ALPHA = "omega_alpha"
STAGE15A_OMEGA_BETA = "omega_beta"
STAGE15A_OMEGA_GAMMA = "omega_gamma"
STAGE15A_OMEGA_DELTA = "omega_delta"
STAGE15A_CANONICAL_ORBIT_IDS = (
    STAGE15A_OMEGA_ALPHA,
    STAGE15A_OMEGA_BETA,
    STAGE15A_OMEGA_GAMMA,
    STAGE15A_OMEGA_DELTA,
)

STAGE15A_GENERATOR_SUPPORTS = {
    0: frozenset((0, 1)),
    1: frozenset((1, 2)),
    2: frozenset((2,)),
}

STAGE15A_SMEARING_PAIRS = (
    ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0)),
    ((0.0, 1.0, 0.0), (1.0, 0.0, 0.0)),
    ((1.0, -0.5, 0.0), (0.25, 1.0, 0.0)),
    ((0.0, 1.0, -0.5), (0.0, 0.25, 1.0)),
    ((1.0, -0.5, 0.25), (-0.25, 0.75, 1.0)),
    ((1.0, 0.0, 1.0), (0.0, 1.0, -1.0)),
)


@dataclass(frozen=True, slots=True)
class Stage15PhysicalOrbit:
    orbit_id: str
    Q_D: float
    P_D: float


@dataclass(frozen=True, slots=True)
class Stage15PhaseSpacePoint:
    Q: float
    P: float
    T0: float
    pi0: float
    T1: float
    pi1: float
    T2: float
    pi2: float

    def vector(self) -> np.ndarray:
        return np.asarray(
            [self.Q, self.P, self.T0, self.pi0, self.T1, self.pi1, self.T2, self.pi2],
            dtype=float,
        )


@dataclass(frozen=True, slots=True)
class Stage15Representative:
    orbit_id: str
    representative_id: str
    Q: float
    P: float
    T0: float
    pi0: float
    T1: float
    pi1: float
    T2: float
    pi2: float
    C0_value: float
    C1_value: float
    C2_value: float
    declared_Q_D: float
    declared_P_D: float
    constraint_basis_id: str = STAGE15A_BASIS_ID

    def point(self) -> Stage15PhaseSpacePoint:
        return Stage15PhaseSpacePoint(
            self.Q, self.P, self.T0, self.pi0, self.T1, self.pi1, self.T2, self.pi2
        )


@dataclass(frozen=True, slots=True)
class Stage15SmearedProbe:
    source_kind: str
    representative_id: str
    N: tuple[float, float, float]
    M: tuple[float, float, float]
    direct_value: float
    reconstructed_value: float
    antisymmetry_residual: float
    support_ok: bool


@dataclass(frozen=True, slots=True)
class Stage15ADiagnostics:
    orbit_count: int
    representative_count: int
    representatives_per_orbit: int
    off_surface_probe_count: int
    smeared_probe_count: int
    structure_function_values: tuple[float, ...]
    minimum_constraint_gradient_rank: int
    minimum_generator_vector_rank: int
    minimum_constraint_gradient_sigma_min: float
    minimum_generator_vector_sigma_min: float
    max_constraint_residual: float
    max_unsmeared_closure_residual: float
    max_jacobi_residual: float
    max_smeared_reconstruction_residual: float
    max_smeared_antisymmetry_residual: float
    representative_family_complete: bool
    declared_dirac_family_consistent: bool
    independent_constraint_directions: bool
    structure_functions_nontrivial: bool
    first_class_local_closure_established: bool
    smeared_local_consistency_established: bool
    support_locality_established: bool
    criteria_11_17_satisfied: bool


def canonical_stage15a_orbits() -> tuple[Stage15PhysicalOrbit, ...]:
    return (
        Stage15PhysicalOrbit(STAGE15A_OMEGA_ALPHA, -0.35, 1.25),
        Stage15PhysicalOrbit(STAGE15A_OMEGA_BETA, 0.40, 1.25),
        Stage15PhysicalOrbit(STAGE15A_OMEGA_GAMMA, -0.35, 0.75),
        Stage15PhysicalOrbit(STAGE15A_OMEGA_DELTA, 0.20, 1.75),
    )


def stage15a_seed_constraints(point: Stage15PhaseSpacePoint) -> tuple[float, float, float]:
    c0, c1, c2 = STAGE15A_C
    return (
        float(point.pi0 + c0 * point.P),
        float(point.pi1 + c1 * point.P),
        float(point.pi2 + c2 * point.P),
    )


def stage15a_constraints(
    point: Stage15PhaseSpacePoint, *, kappa: float = STAGE15A_KAPPA
) -> tuple[float, float, float]:
    K0, K1, K2 = stage15a_seed_constraints(point)
    return (
        float(K0 + kappa * point.T0 * K1),
        float(K1 + kappa * point.T1 * K2),
        float(K2),
    )


def stage15a_C0(point: Stage15PhaseSpacePoint) -> float:
    return stage15a_constraints(point)[0]


def stage15a_C1(point: Stage15PhaseSpacePoint) -> float:
    return stage15a_constraints(point)[1]


def stage15a_C2(point: Stage15PhaseSpacePoint) -> float:
    return stage15a_constraints(point)[2]


def stage15a_dirac_data(point: Stage15PhaseSpacePoint) -> tuple[float, float]:
    c0, c1, c2 = STAGE15A_C
    return (
        float(point.Q - c0 * point.T0 - c1 * point.T1 - c2 * point.T2),
        float(point.P),
    )


def stage15a_constraint_gradients(
    point: Stage15PhaseSpacePoint, *, kappa: float = STAGE15A_KAPPA
) -> np.ndarray:
    """Constraint gradients in canonical order (Q,P,T0,pi0,T1,pi1,T2,pi2)."""

    c0, c1, c2 = STAGE15A_C
    _, K1, K2 = stage15a_seed_constraints(point)
    g0 = np.asarray(
        [0.0, c0 + kappa * point.T0 * c1, kappa * K1, 1.0,
         0.0, kappa * point.T0, 0.0, 0.0],
        dtype=float,
    )
    g1 = np.asarray(
        [0.0, c1 + kappa * point.T1 * c2, 0.0, 0.0,
         kappa * K2, 1.0, 0.0, kappa * point.T1],
        dtype=float,
    )
    g2 = np.asarray([0.0, c2, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0], dtype=float)
    return np.asarray([g0, g1, g2], dtype=float)


def _hamiltonian_vector_from_gradient(gradient: np.ndarray) -> np.ndarray:
    result: list[float] = []
    for q_index, p_index in ((0, 1), (2, 3), (4, 5), (6, 7)):
        result.extend((float(gradient[p_index]), float(-gradient[q_index])))
    return np.asarray(result, dtype=float)


def stage15a_generator_vectors(point: Stage15PhaseSpacePoint) -> np.ndarray:
    return np.asarray(
        [_hamiltonian_vector_from_gradient(row) for row in stage15a_constraint_gradients(point)],
        dtype=float,
    )


def _poisson_from_gradients(df: np.ndarray, dg: np.ndarray) -> float:
    return float(sum(
        df[q_index] * dg[p_index] - df[p_index] * dg[q_index]
        for q_index, p_index in ((0, 1), (2, 3), (4, 5), (6, 7))
    ))


def stage15a_poisson_pair(point: Stage15PhaseSpacePoint, i: int, j: int) -> float:
    gradients = stage15a_constraint_gradients(point)
    return _poisson_from_gradients(gradients[i], gradients[j])


def stage15a_structure_function(point: Stage15PhaseSpacePoint) -> float:
    return float(-(STAGE15A_KAPPA**2) * point.T0)


def stage15a_expected_pair(point: Stage15PhaseSpacePoint, i: int, j: int) -> float:
    if i == j:
        return 0.0
    if (i, j) == (0, 1):
        return float(stage15a_structure_function(point) * stage15a_C2(point))
    if (i, j) == (1, 0):
        return float(-stage15a_structure_function(point) * stage15a_C2(point))
    return 0.0


def _gradient_bracket_C0_C1(point: Stage15PhaseSpacePoint) -> np.ndarray:
    c2 = STAGE15A_C[2]
    k2 = STAGE15A_KAPPA**2
    K2 = stage15a_seed_constraints(point)[2]
    return np.asarray(
        [0.0, -k2 * point.T0 * c2, -k2 * K2, 0.0,
         0.0, 0.0, 0.0, -k2 * point.T0],
        dtype=float,
    )


def stage15a_jacobi_residual(point: Stage15PhaseSpacePoint) -> float:
    gradients = stage15a_constraint_gradients(point)
    return float(_poisson_from_gradients(_gradient_bracket_C0_C1(point), gradients[2]))


def stage15a_generator_support(index: int) -> frozenset[int]:
    return STAGE15A_GENERATOR_SUPPORTS[index]


def stage15a_unsmeared_support_ok(point: Stage15PhaseSpacePoint, i: int, j: int) -> bool:
    expected = stage15a_expected_pair(point, i, j)
    if abs(expected) <= STAGE15A_ATOL:
        return True
    output_support = stage15a_generator_support(2)
    input_union = stage15a_generator_support(i) | stage15a_generator_support(j)
    return output_support <= input_union


def stage15a_smeared_gradient(
    point: Stage15PhaseSpacePoint, smearing: tuple[float, float, float]
) -> np.ndarray:
    gradients = stage15a_constraint_gradients(point)
    return sum(
        (float(weight) * gradients[index] for index, weight in enumerate(smearing)),
        start=np.zeros(8, dtype=float),
    )


def stage15a_smeared_direct(
    point: Stage15PhaseSpacePoint,
    N: tuple[float, float, float],
    M: tuple[float, float, float],
) -> float:
    return _poisson_from_gradients(
        stage15a_smeared_gradient(point, N), stage15a_smeared_gradient(point, M)
    )


def stage15a_smeared_decomposition(
    point: Stage15PhaseSpacePoint,
    N: tuple[float, float, float],
    M: tuple[float, float, float],
) -> tuple[float, float, float]:
    coefficient = stage15a_structure_function(point) * (
        float(N[0]) * float(M[1]) - float(N[1]) * float(M[0])
    )
    return (0.0, 0.0, float(coefficient))


def stage15a_smeared_reconstructed(
    point: Stage15PhaseSpacePoint,
    N: tuple[float, float, float],
    M: tuple[float, float, float],
) -> float:
    coeffs = stage15a_smeared_decomposition(point, N, M)
    constraints = stage15a_constraints(point)
    return float(sum(a * b for a, b in zip(coeffs, constraints)))


def _smearing_generator_support(smearing: tuple[float, float, float]) -> frozenset[int]:
    support: set[int] = set()
    for index, weight in enumerate(smearing):
        if abs(float(weight)) > STAGE15A_ATOL:
            support.update(stage15a_generator_support(index))
    return frozenset(support)


def stage15a_smeared_support_ok(
    point: Stage15PhaseSpacePoint,
    N: tuple[float, float, float],
    M: tuple[float, float, float],
) -> bool:
    coeffs = stage15a_smeared_decomposition(point, N, M)
    output_support: set[int] = set()
    for index, coefficient in enumerate(coeffs):
        if abs(coefficient) > STAGE15A_ATOL:
            output_support.update(stage15a_generator_support(index))
    input_union = _smearing_generator_support(N) | _smearing_generator_support(M)
    return frozenset(output_support) <= input_union


def _grid_label(value: float) -> str:
    if value == 0:
        return "z0"
    sign = "m" if value < 0 else "p"
    return f"{sign}{abs(value):.1f}".replace(".", "p")


def canonical_stage15a_representatives_for_orbit(
    orbit: Stage15PhysicalOrbit,
) -> tuple[Stage15Representative, ...]:
    c0, c1, c2 = STAGE15A_C
    result: list[Stage15Representative] = []
    for T0 in STAGE15A_GRID_VALUES:
        for T1 in STAGE15A_GRID_VALUES:
            for T2 in STAGE15A_GRID_VALUES:
                P = float(orbit.P_D)
                point = Stage15PhaseSpacePoint(
                    Q=float(orbit.Q_D + c0 * T0 + c1 * T1 + c2 * T2),
                    P=P,
                    T0=float(T0), pi0=float(-c0 * P),
                    T1=float(T1), pi1=float(-c1 * P),
                    T2=float(T2), pi2=float(-c2 * P),
                )
                C0, C1, C2 = stage15a_constraints(point)
                suffix = (
                    f"T0_{_grid_label(T0)}:T1_{_grid_label(T1)}:T2_{_grid_label(T2)}"
                )
                result.append(Stage15Representative(
                    orbit_id=orbit.orbit_id,
                    representative_id=f"{orbit.orbit_id}:rep:{suffix}",
                    Q=point.Q, P=point.P,
                    T0=point.T0, pi0=point.pi0,
                    T1=point.T1, pi1=point.pi1,
                    T2=point.T2, pi2=point.pi2,
                    C0_value=C0, C1_value=C1, C2_value=C2,
                    declared_Q_D=float(orbit.Q_D), declared_P_D=float(orbit.P_D),
                ))
    return tuple(result)


def canonical_stage15a_representatives() -> tuple[Stage15Representative, ...]:
    return tuple(
        rep for orbit in canonical_stage15a_orbits()
        for rep in canonical_stage15a_representatives_for_orbit(orbit)
    )


def canonical_stage15a_off_surface_probes() -> tuple[Stage15PhaseSpacePoint, ...]:
    probes: list[Stage15PhaseSpacePoint] = []
    for rep in canonical_stage15a_representatives():
        p = rep.point()
        probes.append(Stage15PhaseSpacePoint(
            Q=float(p.Q - 0.075), P=p.P,
            T0=p.T0, pi0=float(p.pi0 + 0.125),
            T1=p.T1, pi1=float(p.pi1 - 0.10),
            T2=p.T2, pi2=float(p.pi2 + 0.20),
        ))
    return tuple(probes)


def _constraint_residual(point: Stage15PhaseSpacePoint) -> float:
    return float(max(abs(value) for value in stage15a_constraints(point)))


def canonical_stage15a_smeared_probes() -> tuple[Stage15SmearedProbe, ...]:
    result: list[Stage15SmearedProbe] = []
    positive = tuple((rep.representative_id, rep.point()) for rep in canonical_stage15a_representatives())
    off_surface = tuple(
        (f"off:{index}", point)
        for index, point in enumerate(canonical_stage15a_off_surface_probes())
    )
    for source_kind, sources in (("positive", positive), ("off_surface", off_surface)):
        for representative_id, point in sources:
            for N, M in STAGE15A_SMEARING_PAIRS:
                direct = stage15a_smeared_direct(point, N, M)
                reconstructed = stage15a_smeared_reconstructed(point, N, M)
                reverse = stage15a_smeared_direct(point, M, N)
                result.append(Stage15SmearedProbe(
                    source_kind=source_kind,
                    representative_id=representative_id,
                    N=N, M=M,
                    direct_value=direct,
                    reconstructed_value=reconstructed,
                    antisymmetry_residual=float(abs(direct + reverse)),
                    support_ok=stage15a_smeared_support_ok(point, N, M),
                ))
    return tuple(result)


def stage15a_diagnostics() -> Stage15ADiagnostics:
    reps = canonical_stage15a_representatives()
    off_surface = canonical_stage15a_off_surface_probes()
    all_points = tuple(rep.point() for rep in reps) + off_surface

    grad_ranks: list[int] = []
    gen_ranks: list[int] = []
    grad_sigma: list[float] = []
    gen_sigma: list[float] = []
    closure_residuals: list[float] = []
    jacobi_residuals: list[float] = []
    support_checks: list[bool] = []

    for point in all_points:
        gradients = stage15a_constraint_gradients(point)
        generators = stage15a_generator_vectors(point)
        grad_ranks.append(int(np.linalg.matrix_rank(gradients, tol=STAGE15A_ATOL)))
        gen_ranks.append(int(np.linalg.matrix_rank(generators, tol=STAGE15A_ATOL)))
        grad_sigma.append(float(np.linalg.svd(gradients, compute_uv=False)[-1]))
        gen_sigma.append(float(np.linalg.svd(generators, compute_uv=False)[-1]))
        for i in range(3):
            for j in range(3):
                closure_residuals.append(abs(
                    stage15a_poisson_pair(point, i, j) - stage15a_expected_pair(point, i, j)
                ))
                support_checks.append(stage15a_unsmeared_support_ok(point, i, j))
        jacobi_residuals.append(abs(stage15a_jacobi_residual(point)))

    structure_values = tuple(sorted({
        0.0 if abs(stage15a_structure_function(rep.point())) <= STAGE15A_ATOL
        else stage15a_structure_function(rep.point())
        for rep in reps
    }))
    smeared = canonical_stage15a_smeared_probes()
    max_smeared_reconstruction = max(
        abs(item.direct_value - item.reconstructed_value) for item in smeared
    )
    max_smeared_antisymmetry = max(item.antisymmetry_residual for item in smeared)

    family_complete = (
        len(reps) == 108
        and len({rep.representative_id for rep in reps}) == 108
        and all(
            sum(rep.orbit_id == orbit.orbit_id for rep in reps) == 27
            for orbit in canonical_stage15a_orbits()
        )
    )
    dirac_consistent = all(
        np.allclose(
            stage15a_dirac_data(rep.point()),
            (rep.declared_Q_D, rep.declared_P_D),
            atol=STAGE15A_ATOL, rtol=0.0,
        ) for rep in reps
    ) and len({
        (round(stage15a_dirac_data(rep.point())[0], 12),
         round(stage15a_dirac_data(rep.point())[1], 12))
        for rep in reps
    }) == 4

    max_constraint = max(_constraint_residual(rep.point()) for rep in reps)
    independent = (
        min(grad_ranks) == 3 and min(gen_ranks) == 3
        and min(grad_sigma) > STAGE15A_ATOL and min(gen_sigma) > STAGE15A_ATOL
    )
    structure_nontrivial = (
        any(value < 0 for value in structure_values)
        and 0.0 in structure_values
        and any(value > 0 for value in structure_values)
    )
    local_closure = (
        max(closure_residuals) <= STAGE15A_ATOL
        and max(jacobi_residuals) <= STAGE15A_ATOL
    )
    smeared_consistency = (
        max_smeared_reconstruction <= STAGE15A_ATOL
        and max_smeared_antisymmetry <= STAGE15A_ATOL
    )
    support_locality = all(support_checks) and all(item.support_ok for item in smeared)
    criteria = (
        family_complete and dirac_consistent and independent and structure_nontrivial
        and max_constraint <= STAGE15A_ATOL and local_closure
        and smeared_consistency and support_locality
    )

    return Stage15ADiagnostics(
        orbit_count=4,
        representative_count=len(reps), representatives_per_orbit=27,
        off_surface_probe_count=len(off_surface), smeared_probe_count=len(smeared),
        structure_function_values=structure_values,
        minimum_constraint_gradient_rank=min(grad_ranks),
        minimum_generator_vector_rank=min(gen_ranks),
        minimum_constraint_gradient_sigma_min=min(grad_sigma),
        minimum_generator_vector_sigma_min=min(gen_sigma),
        max_constraint_residual=max_constraint,
        max_unsmeared_closure_residual=max(closure_residuals),
        max_jacobi_residual=max(jacobi_residuals),
        max_smeared_reconstruction_residual=max_smeared_reconstruction,
        max_smeared_antisymmetry_residual=max_smeared_antisymmetry,
        representative_family_complete=family_complete,
        declared_dirac_family_consistent=dirac_consistent,
        independent_constraint_directions=independent,
        structure_functions_nontrivial=structure_nontrivial,
        first_class_local_closure_established=local_closure,
        smeared_local_consistency_established=smeared_consistency,
        support_locality_established=support_locality,
        criteria_11_17_satisfied=criteria,
    )
