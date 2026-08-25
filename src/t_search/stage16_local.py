"""Stage 16A four-site cyclic first-class carrier and local/smeared algebra.

This module implements only the Stage 16A evidence frozen in
``docs/stage16_protocol.md``.  It constructs the 324 positive representatives
and deterministic off-surface probes, derives the cyclic local/smeared
Poisson algebra, reconstructs the same brackets in the presented C basis,
and audits rank plus the deliberately separated canonical-function and
closure-coordinate support notions.

Finite path compensation is deferred to Stage 16B.  Complete quotient /
relational claims are deferred to Stage 16C.  Locality-preserving basis
search is deferred to Stage 16D.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from itertools import product

import numpy as np

STAGE16A_ATOL = 1e-10
STAGE16A_KAPPA = 0.5
STAGE16A_C = (1.0, 0.5, -0.25, 0.75)
STAGE16A_GRID_VALUES = (-1.0, 0.0, 1.0)
STAGE16A_BASIS_ID = "stage16_four_site_cycle_positive_basis"
STAGE16A_OFF_SURFACE_PI_SHIFTS = (0.125, -0.25, 0.375, -0.5)

STAGE16A_OMEGA_ALPHA = "omega_alpha"
STAGE16A_OMEGA_BETA = "omega_beta"
STAGE16A_OMEGA_GAMMA = "omega_gamma"
STAGE16A_OMEGA_DELTA = "omega_delta"
STAGE16A_CANONICAL_ORBIT_IDS = (
    STAGE16A_OMEGA_ALPHA,
    STAGE16A_OMEGA_BETA,
    STAGE16A_OMEGA_GAMMA,
    STAGE16A_OMEGA_DELTA,
)

STAGE16A_GENERATOR_SUPPORTS = {
    0: frozenset((0, 1)),
    1: frozenset((1, 2)),
    2: frozenset((2, 3)),
    3: frozenset((3, 0)),
}
STAGE16A_ADJACENT_FORWARD_EDGES = ((0, 1), (1, 2), (2, 3), (3, 0))
STAGE16A_OPPOSITE_PAIRS = ((0, 2), (1, 3))

STAGE16A_N_01 = (1.0, -0.5, 0.0, 0.0)
STAGE16A_N_12 = (0.0, 1.0, -0.5, 0.0)
STAGE16A_N_23 = (0.0, 0.0, 1.0, -0.5)
STAGE16A_N_30 = (-0.5, 0.0, 0.0, 1.0)
STAGE16A_N_FULL_A = (1.0, -0.5, 0.25, 0.75)
STAGE16A_N_FULL_B = (-0.25, 0.75, 1.0, -0.5)
STAGE16A_N_PARALLEL = tuple(2.0 * value for value in STAGE16A_N_FULL_A)

STAGE16A_SMEARING_PAIRS = (
    (STAGE16A_N_01, STAGE16A_N_12),
    (STAGE16A_N_12, STAGE16A_N_23),
    (STAGE16A_N_23, STAGE16A_N_30),
    (STAGE16A_N_30, STAGE16A_N_01),
    (STAGE16A_N_01, STAGE16A_N_FULL_A),
    (STAGE16A_N_12, STAGE16A_N_FULL_B),
    (STAGE16A_N_FULL_A, STAGE16A_N_FULL_B),
    (STAGE16A_N_FULL_A, STAGE16A_N_PARALLEL),
)


@dataclass(frozen=True, slots=True)
class Stage16PhysicalOrbit:
    orbit_id: str
    Q_D: float
    P_D: float


@dataclass(frozen=True, slots=True)
class Stage16PhaseSpacePoint:
    Q: float
    P: float
    T0: float
    pi0: float
    T1: float
    pi1: float
    T2: float
    pi2: float
    T3: float
    pi3: float

    def vector(self) -> np.ndarray:
        return np.asarray(
            [
                self.Q,
                self.P,
                self.T0,
                self.pi0,
                self.T1,
                self.pi1,
                self.T2,
                self.pi2,
                self.T3,
                self.pi3,
            ],
            dtype=float,
        )

    def clocks(self) -> tuple[float, float, float, float]:
        return (self.T0, self.T1, self.T2, self.T3)

    def momenta(self) -> tuple[float, float, float, float]:
        return (self.pi0, self.pi1, self.pi2, self.pi3)


@dataclass(frozen=True, slots=True)
class Stage16Representative:
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
    T3: float
    pi3: float
    C0_value: float
    C1_value: float
    C2_value: float
    C3_value: float
    declared_Q_D: float
    declared_P_D: float
    constraint_basis_id: str = STAGE16A_BASIS_ID

    def point(self) -> Stage16PhaseSpacePoint:
        return Stage16PhaseSpacePoint(
            self.Q,
            self.P,
            self.T0,
            self.pi0,
            self.T1,
            self.pi1,
            self.T2,
            self.pi2,
            self.T3,
            self.pi3,
        )


@dataclass(frozen=True, slots=True)
class Stage16SmearedProbe:
    source_kind: str
    source_id: str
    N: tuple[float, float, float, float]
    M: tuple[float, float, float, float]
    direct_value: float
    seed_expected_value: float
    reconstructed_value: float
    antisymmetry_residual: float
    canonical_support_ok: bool
    closure_coordinate_support_size: int


@dataclass(frozen=True, slots=True)
class Stage16ADiagnostics:
    orbit_count: int
    representative_count: int
    representatives_per_orbit: int
    off_surface_probe_count: int
    smeared_pair_count: int
    smeared_probe_count: int
    jacobi_probe_count: int
    structure_function_values: tuple[float, ...]
    frame_determinant_values: tuple[float, ...]
    minimum_abs_frame_determinant: float
    minimum_constraint_gradient_rank: int
    minimum_generator_vector_rank: int
    minimum_constraint_gradient_sigma_min: float
    minimum_generator_vector_sigma_min: float
    max_constraint_residual: float
    max_seed_inverse_residual: float
    max_unsmeared_seed_formula_residual: float
    max_unsmeared_presented_reconstruction_residual: float
    max_jacobi_residual: float
    max_smeared_seed_formula_residual: float
    max_smeared_presented_reconstruction_residual: float
    max_smeared_antisymmetry_residual: float
    off_surface_nonzero_adjacent_forward_count: int
    cycle_spanning_closure_coordinate_count: int
    max_closure_coordinate_support_size: int
    representative_family_complete: bool
    declared_dirac_family_consistent: bool
    frame_invertible_on_positive_family: bool
    independent_constraint_directions: bool
    structure_functions_nontrivial: bool
    first_class_presented_closure_established: bool
    smeared_presented_closure_established: bool
    canonical_function_support_established: bool
    closure_coordinate_cycle_spanning_observed: bool
    criteria_11_17_satisfied: bool


def canonical_stage16a_orbits() -> tuple[Stage16PhysicalOrbit, ...]:
    return (
        Stage16PhysicalOrbit(STAGE16A_OMEGA_ALPHA, -0.35, 1.25),
        Stage16PhysicalOrbit(STAGE16A_OMEGA_BETA, 0.40, 1.25),
        Stage16PhysicalOrbit(STAGE16A_OMEGA_GAMMA, -0.35, 0.75),
        Stage16PhysicalOrbit(STAGE16A_OMEGA_DELTA, 0.20, 1.75),
    )


def _clock_array(point: Stage16PhaseSpacePoint) -> np.ndarray:
    return np.asarray(point.clocks(), dtype=float)


def stage16a_seed_constraints(point: Stage16PhaseSpacePoint) -> tuple[float, float, float, float]:
    return tuple(
        float(pi + c * point.P)
        for pi, c in zip(point.momenta(), STAGE16A_C, strict=True)
    )


def stage16a_frame_matrix(
    point: Stage16PhaseSpacePoint, *, kappa: float = STAGE16A_KAPPA
) -> np.ndarray:
    clocks = _clock_array(point)
    matrix = np.eye(4, dtype=float)
    for index in range(4):
        matrix[index, (index + 1) % 4] = float(kappa * clocks[index])
    return matrix


def stage16a_frame_determinant(
    point: Stage16PhaseSpacePoint, *, kappa: float = STAGE16A_KAPPA
) -> float:
    clocks = _clock_array(point)
    return float(1.0 - (kappa**4) * np.prod(clocks))


def stage16a_constraints(
    point: Stage16PhaseSpacePoint, *, kappa: float = STAGE16A_KAPPA
) -> tuple[float, float, float, float]:
    values = stage16a_frame_matrix(point, kappa=kappa) @ np.asarray(
        stage16a_seed_constraints(point), dtype=float
    )
    return tuple(float(value) for value in values)


def stage16a_dirac_data(point: Stage16PhaseSpacePoint) -> tuple[float, float]:
    return (
        float(point.Q - sum(c * t for c, t in zip(STAGE16A_C, point.clocks(), strict=True))),
        float(point.P),
    )


def stage16a_seed_inverse_matrix(
    point: Stage16PhaseSpacePoint, *, kappa: float = STAGE16A_KAPPA
) -> np.ndarray:
    clocks = _clock_array(point)
    a = kappa * clocks
    determinant = stage16a_frame_determinant(point, kappa=kappa)
    if abs(determinant) <= STAGE16A_ATOL:
        raise ValueError("singular Stage 16 cyclic constraint frame")
    inverse = np.zeros((4, 4), dtype=float)
    for i in range(4):
        inverse[i, i] = 1.0
        inverse[i, (i + 1) % 4] = -a[i]
        inverse[i, (i + 2) % 4] = a[i] * a[(i + 1) % 4]
        inverse[i, (i + 3) % 4] = -a[i] * a[(i + 1) % 4] * a[(i + 2) % 4]
    return inverse / determinant


def stage16a_reconstruct_seeds_from_presented(
    point: Stage16PhaseSpacePoint, *, kappa: float = STAGE16A_KAPPA
) -> tuple[float, float, float, float]:
    values = stage16a_seed_inverse_matrix(point, kappa=kappa) @ np.asarray(
        stage16a_constraints(point, kappa=kappa), dtype=float
    )
    return tuple(float(value) for value in values)


def stage16a_constraint_gradients(
    point: Stage16PhaseSpacePoint, *, kappa: float = STAGE16A_KAPPA
) -> np.ndarray:
    seeds = stage16a_seed_constraints(point)
    clocks = point.clocks()
    result = np.zeros((4, 10), dtype=float)
    for i in range(4):
        j = (i + 1) % 4
        result[i, 1] = STAGE16A_C[i] + kappa * clocks[i] * STAGE16A_C[j]
        result[i, 2 + 2 * i] = kappa * seeds[j]
        result[i, 3 + 2 * i] = 1.0
        result[i, 3 + 2 * j] = kappa * clocks[i]
    return result


def _hamiltonian_vector_from_gradient(gradient: np.ndarray) -> np.ndarray:
    result: list[float] = []
    for q_index, p_index in ((0, 1), (2, 3), (4, 5), (6, 7), (8, 9)):
        result.extend((float(gradient[p_index]), float(-gradient[q_index])))
    return np.asarray(result, dtype=float)


def stage16a_generator_vectors(point: Stage16PhaseSpacePoint) -> np.ndarray:
    return np.asarray(
        [_hamiltonian_vector_from_gradient(row) for row in stage16a_constraint_gradients(point)],
        dtype=float,
    )


def _poisson_from_gradients(df: np.ndarray, dg: np.ndarray) -> float:
    return float(
        sum(
            df[q_index] * dg[p_index] - df[p_index] * dg[q_index]
            for q_index, p_index in ((0, 1), (2, 3), (4, 5), (6, 7), (8, 9))
        )
    )


def stage16a_poisson_pair(point: Stage16PhaseSpacePoint, i: int, j: int) -> float:
    gradients = stage16a_constraint_gradients(point)
    return _poisson_from_gradients(gradients[i], gradients[j])


def _forward_edge_index(i: int, j: int) -> tuple[int, float] | None:
    if i == j:
        return None
    if j == (i + 1) % 4:
        return i, -1.0
    if i == (j + 1) % 4:
        return j, 1.0
    return None


def stage16a_pair_seed_coefficients(
    point: Stage16PhaseSpacePoint, i: int, j: int
) -> tuple[float, float, float, float]:
    coefficients = np.zeros(4, dtype=float)
    edge = _forward_edge_index(i, j)
    if edge is None:
        return tuple(float(value) for value in coefficients)
    forward_index, sign = edge
    seed_index = (forward_index + 2) % 4
    coefficients[seed_index] = sign * (STAGE16A_KAPPA**2) * point.clocks()[forward_index]
    return tuple(float(value) for value in coefficients)


def stage16a_expected_seed_pair(point: Stage16PhaseSpacePoint, i: int, j: int) -> float:
    return float(
        np.dot(
            np.asarray(stage16a_pair_seed_coefficients(point, i, j), dtype=float),
            np.asarray(stage16a_seed_constraints(point), dtype=float),
        )
    )


def stage16a_closure_coefficients(
    point: Stage16PhaseSpacePoint, i: int, j: int
) -> tuple[float, float, float, float]:
    seed_coefficients = np.asarray(stage16a_pair_seed_coefficients(point, i, j), dtype=float)
    coefficients = seed_coefficients @ stage16a_seed_inverse_matrix(point)
    return tuple(float(value) for value in coefficients)


def stage16a_reconstructed_pair(point: Stage16PhaseSpacePoint, i: int, j: int) -> float:
    return float(
        np.dot(
            np.asarray(stage16a_closure_coefficients(point, i, j), dtype=float),
            np.asarray(stage16a_constraints(point), dtype=float),
        )
    )


def _gradient_expected_pair(
    point: Stage16PhaseSpacePoint, i: int, j: int
) -> np.ndarray:
    gradient = np.zeros(10, dtype=float)
    edge = _forward_edge_index(i, j)
    if edge is None:
        return gradient
    forward_index, sign = edge
    seed_index = (forward_index + 2) % 4
    factor = sign * (STAGE16A_KAPPA**2)
    clocks = point.clocks()
    seeds = stage16a_seed_constraints(point)
    gradient[1] = factor * clocks[forward_index] * STAGE16A_C[seed_index]
    gradient[2 + 2 * forward_index] = factor * seeds[seed_index]
    gradient[3 + 2 * seed_index] = factor * clocks[forward_index]
    return gradient


def stage16a_jacobi_residual(
    point: Stage16PhaseSpacePoint, i: int, j: int, k: int
) -> float:
    gradients = stage16a_constraint_gradients(point)
    return float(
        _poisson_from_gradients(gradients[i], _gradient_expected_pair(point, j, k))
        + _poisson_from_gradients(gradients[j], _gradient_expected_pair(point, k, i))
        + _poisson_from_gradients(gradients[k], _gradient_expected_pair(point, i, j))
    )


def stage16a_generator_support(index: int) -> frozenset[int]:
    return STAGE16A_GENERATOR_SUPPORTS[index]


def stage16a_pair_canonical_support(i: int, j: int) -> frozenset[int]:
    edge = _forward_edge_index(i, j)
    if edge is None:
        return frozenset()
    forward_index, _ = edge
    return frozenset((forward_index, (forward_index + 2) % 4))


def stage16a_unsmeared_canonical_support_ok(i: int, j: int) -> bool:
    output_support = stage16a_pair_canonical_support(i, j)
    input_union = stage16a_generator_support(i) | stage16a_generator_support(j)
    return output_support <= input_union


def stage16a_closure_coordinate_support(
    point: Stage16PhaseSpacePoint, i: int, j: int
) -> frozenset[int]:
    return frozenset(
        index
        for index, coefficient in enumerate(stage16a_closure_coefficients(point, i, j))
        if abs(coefficient) > STAGE16A_ATOL
    )


def stage16a_smeared_gradient(
    point: Stage16PhaseSpacePoint, smearing: tuple[float, float, float, float]
) -> np.ndarray:
    gradients = stage16a_constraint_gradients(point)
    return sum(
        (float(weight) * gradients[index] for index, weight in enumerate(smearing)),
        start=np.zeros(10, dtype=float),
    )


def stage16a_smeared_direct(
    point: Stage16PhaseSpacePoint,
    N: tuple[float, float, float, float],
    M: tuple[float, float, float, float],
) -> float:
    return _poisson_from_gradients(
        stage16a_smeared_gradient(point, N),
        stage16a_smeared_gradient(point, M),
    )


def stage16a_smeared_seed_coefficients(
    point: Stage16PhaseSpacePoint,
    N: tuple[float, float, float, float],
    M: tuple[float, float, float, float],
) -> tuple[float, float, float, float]:
    clocks = point.clocks()
    result = np.zeros(4, dtype=float)
    for i in range(4):
        wedge = float(N[i]) * float(M[(i + 1) % 4]) - float(N[(i + 1) % 4]) * float(M[i])
        result[(i + 2) % 4] += -(STAGE16A_KAPPA**2) * wedge * clocks[i]
    return tuple(float(value) for value in result)


def stage16a_smeared_expected_seed(
    point: Stage16PhaseSpacePoint,
    N: tuple[float, float, float, float],
    M: tuple[float, float, float, float],
) -> float:
    return float(
        np.dot(
            np.asarray(stage16a_smeared_seed_coefficients(point, N, M), dtype=float),
            np.asarray(stage16a_seed_constraints(point), dtype=float),
        )
    )


def stage16a_smeared_closure_coefficients(
    point: Stage16PhaseSpacePoint,
    N: tuple[float, float, float, float],
    M: tuple[float, float, float, float],
) -> tuple[float, float, float, float]:
    seed_coefficients = np.asarray(stage16a_smeared_seed_coefficients(point, N, M), dtype=float)
    coefficients = seed_coefficients @ stage16a_seed_inverse_matrix(point)
    return tuple(float(value) for value in coefficients)


def stage16a_smeared_reconstructed(
    point: Stage16PhaseSpacePoint,
    N: tuple[float, float, float, float],
    M: tuple[float, float, float, float],
) -> float:
    return float(
        np.dot(
            np.asarray(stage16a_smeared_closure_coefficients(point, N, M), dtype=float),
            np.asarray(stage16a_constraints(point), dtype=float),
        )
    )


def _smearing_generator_support(
    smearing: tuple[float, float, float, float],
) -> frozenset[int]:
    support: set[int] = set()
    for index, weight in enumerate(smearing):
        if abs(float(weight)) > STAGE16A_ATOL:
            support.update(stage16a_generator_support(index))
    return frozenset(support)


def stage16a_smeared_canonical_support(
    N: tuple[float, float, float, float],
    M: tuple[float, float, float, float],
) -> frozenset[int]:
    support: set[int] = set()
    for i in range(4):
        wedge = float(N[i]) * float(M[(i + 1) % 4]) - float(N[(i + 1) % 4]) * float(M[i])
        if abs(wedge) > STAGE16A_ATOL:
            support.update((i, (i + 2) % 4))
    return frozenset(support)


def stage16a_smeared_canonical_support_ok(
    N: tuple[float, float, float, float],
    M: tuple[float, float, float, float],
) -> bool:
    output_support = stage16a_smeared_canonical_support(N, M)
    input_union = _smearing_generator_support(N) | _smearing_generator_support(M)
    return output_support <= input_union


def _grid_label(value: float) -> str:
    if value == 0:
        return "z0"
    sign = "m" if value < 0 else "p"
    return f"{sign}{abs(value):.1f}".replace(".", "p")


def canonical_stage16a_representatives_for_orbit(
    orbit: Stage16PhysicalOrbit,
) -> tuple[Stage16Representative, ...]:
    result: list[Stage16Representative] = []
    for T0, T1, T2, T3 in product(STAGE16A_GRID_VALUES, repeat=4):
        clocks = (T0, T1, T2, T3)
        P = float(orbit.P_D)
        Q = float(orbit.Q_D + sum(c * t for c, t in zip(STAGE16A_C, clocks, strict=True)))
        point = Stage16PhaseSpacePoint(
            Q=Q,
            P=P,
            T0=float(T0),
            pi0=float(-STAGE16A_C[0] * P),
            T1=float(T1),
            pi1=float(-STAGE16A_C[1] * P),
            T2=float(T2),
            pi2=float(-STAGE16A_C[2] * P),
            T3=float(T3),
            pi3=float(-STAGE16A_C[3] * P),
        )
        constraint_values = stage16a_constraints(point)
        suffix = ":".join(
            f"T{index}_{_grid_label(value)}" for index, value in enumerate(clocks)
        )
        result.append(
            Stage16Representative(
                orbit_id=orbit.orbit_id,
                representative_id=f"{orbit.orbit_id}:rep:{suffix}",
                Q=point.Q,
                P=point.P,
                T0=point.T0,
                pi0=point.pi0,
                T1=point.T1,
                pi1=point.pi1,
                T2=point.T2,
                pi2=point.pi2,
                T3=point.T3,
                pi3=point.pi3,
                C0_value=constraint_values[0],
                C1_value=constraint_values[1],
                C2_value=constraint_values[2],
                C3_value=constraint_values[3],
                declared_Q_D=float(orbit.Q_D),
                declared_P_D=float(orbit.P_D),
            )
        )
    return tuple(result)


@lru_cache(maxsize=1)
def canonical_stage16a_representatives() -> tuple[Stage16Representative, ...]:
    return tuple(
        representative
        for orbit in canonical_stage16a_orbits()
        for representative in canonical_stage16a_representatives_for_orbit(orbit)
    )


@lru_cache(maxsize=1)
def canonical_stage16a_off_surface_probes() -> tuple[Stage16PhaseSpacePoint, ...]:
    result: list[Stage16PhaseSpacePoint] = []
    shifts = STAGE16A_OFF_SURFACE_PI_SHIFTS
    for representative in canonical_stage16a_representatives():
        point = representative.point()
        result.append(
            Stage16PhaseSpacePoint(
                Q=point.Q,
                P=point.P,
                T0=point.T0,
                pi0=float(point.pi0 + shifts[0]),
                T1=point.T1,
                pi1=float(point.pi1 + shifts[1]),
                T2=point.T2,
                pi2=float(point.pi2 + shifts[2]),
                T3=point.T3,
                pi3=float(point.pi3 + shifts[3]),
            )
        )
    return tuple(result)


@lru_cache(maxsize=1)
def canonical_stage16a_smeared_probes() -> tuple[Stage16SmearedProbe, ...]:
    result: list[Stage16SmearedProbe] = []
    sources: tuple[tuple[str, str, Stage16PhaseSpacePoint], ...] = tuple(
        ("positive", representative.representative_id, representative.point())
        for representative in canonical_stage16a_representatives()
    ) + tuple(
        ("off_surface", f"off:{index}", point)
        for index, point in enumerate(canonical_stage16a_off_surface_probes())
    )
    for source_kind, source_id, point in sources:
        for N, M in STAGE16A_SMEARING_PAIRS:
            direct = stage16a_smeared_direct(point, N, M)
            expected = stage16a_smeared_expected_seed(point, N, M)
            reconstructed = stage16a_smeared_reconstructed(point, N, M)
            reverse = stage16a_smeared_direct(point, M, N)
            closure_support = frozenset(
                index
                for index, coefficient in enumerate(
                    stage16a_smeared_closure_coefficients(point, N, M)
                )
                if abs(coefficient) > STAGE16A_ATOL
            )
            result.append(
                Stage16SmearedProbe(
                    source_kind=source_kind,
                    source_id=source_id,
                    N=N,
                    M=M,
                    direct_value=float(direct),
                    seed_expected_value=float(expected),
                    reconstructed_value=float(reconstructed),
                    antisymmetry_residual=float(abs(direct + reverse)),
                    canonical_support_ok=stage16a_smeared_canonical_support_ok(N, M),
                    closure_coordinate_support_size=len(closure_support),
                )
            )
    return tuple(result)


@lru_cache(maxsize=1)
def stage16a_diagnostics() -> Stage16ADiagnostics:
    representatives = canonical_stage16a_representatives()
    positive = tuple(representative.point() for representative in representatives)
    off_surface = canonical_stage16a_off_surface_probes()
    all_points = positive + off_surface

    gradient_ranks: list[int] = []
    generator_ranks: list[int] = []
    gradient_sigma_min: list[float] = []
    generator_sigma_min: list[float] = []
    for point in positive:
        gradients = stage16a_constraint_gradients(point)
        generators = stage16a_generator_vectors(point)
        gradient_ranks.append(int(np.linalg.matrix_rank(gradients, tol=STAGE16A_ATOL)))
        generator_ranks.append(int(np.linalg.matrix_rank(generators, tol=STAGE16A_ATOL)))
        gradient_sigma_min.append(float(np.linalg.svd(gradients, compute_uv=False)[-1]))
        generator_sigma_min.append(float(np.linalg.svd(generators, compute_uv=False)[-1]))

    max_constraint_residual = max(
        max(abs(value) for value in stage16a_constraints(point)) for point in positive
    )
    max_seed_inverse_residual = max(
        max(
            abs(a - b)
            for a, b in zip(
                stage16a_seed_constraints(point),
                stage16a_reconstruct_seeds_from_presented(point),
                strict=True,
            )
        )
        for point in all_points
    )

    unsmeared_seed_residuals: list[float] = []
    unsmeared_presented_residuals: list[float] = []
    closure_support_sizes: list[int] = []
    cycle_spanning_count = 0
    off_surface_nonzero = 0
    canonical_support_ok = True
    for point in all_points:
        for i in range(4):
            for j in range(4):
                direct = stage16a_poisson_pair(point, i, j)
                expected = stage16a_expected_seed_pair(point, i, j)
                reconstructed = stage16a_reconstructed_pair(point, i, j)
                unsmeared_seed_residuals.append(abs(direct - expected))
                unsmeared_presented_residuals.append(abs(direct - reconstructed))
                canonical_support_ok = (
                    canonical_support_ok and stage16a_unsmeared_canonical_support_ok(i, j)
                )
                support_size = len(stage16a_closure_coordinate_support(point, i, j))
                closure_support_sizes.append(support_size)
                if (i, j) in STAGE16A_ADJACENT_FORWARD_EDGES and support_size == 4:
                    cycle_spanning_count += 1
    for point in off_surface:
        for i, j in STAGE16A_ADJACENT_FORWARD_EDGES:
            if abs(stage16a_poisson_pair(point, i, j)) > STAGE16A_ATOL:
                off_surface_nonzero += 1

    jacobi_residuals = [
        abs(stage16a_jacobi_residual(point, *triple))
        for point in all_points
        for triple in ((0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3))
    ]

    smeared_probes = canonical_stage16a_smeared_probes()
    determinant_values = tuple(
        sorted(
            {
                0.0 if abs(stage16a_frame_determinant(point)) <= STAGE16A_ATOL
                else stage16a_frame_determinant(point)
                for point in positive
            }
        )
    )
    structure_values = tuple(
        sorted(
            {
                0.0 if abs(-(STAGE16A_KAPPA**2) * clock) <= STAGE16A_ATOL
                else -(STAGE16A_KAPPA**2) * clock
                for point in positive
                for clock in point.clocks()
            }
        )
    )

    representative_family_complete = (
        len(representatives) == 324
        and len({representative.representative_id for representative in representatives}) == 324
        and all(
            sum(1 for representative in representatives if representative.orbit_id == orbit.orbit_id)
            == 81
            for orbit in canonical_stage16a_orbits()
        )
    )
    declared_dirac_family_consistent = all(
        max(
            abs(stage16a_dirac_data(representative.point())[0] - representative.declared_Q_D),
            abs(stage16a_dirac_data(representative.point())[1] - representative.declared_P_D),
        )
        <= STAGE16A_ATOL
        for representative in representatives
    )
    frame_invertible = (
        min(abs(stage16a_frame_determinant(point)) for point in positive) > STAGE16A_ATOL
    )
    independent = min(gradient_ranks) == 4 and min(generator_ranks) == 4
    structure_nontrivial = structure_values == (-0.25, 0.0, 0.25)
    first_class = (
        max(unsmeared_seed_residuals) <= STAGE16A_ATOL
        and max(unsmeared_presented_residuals) <= STAGE16A_ATOL
        and max(jacobi_residuals) <= STAGE16A_ATOL
    )
    smeared_established = (
        max(abs(probe.direct_value - probe.seed_expected_value) for probe in smeared_probes)
        <= STAGE16A_ATOL
        and max(abs(probe.direct_value - probe.reconstructed_value) for probe in smeared_probes)
        <= STAGE16A_ATOL
        and max(probe.antisymmetry_residual for probe in smeared_probes) <= STAGE16A_ATOL
        and all(probe.canonical_support_ok for probe in smeared_probes)
    )
    closure_cycle_spanning = cycle_spanning_count > 0 and max(closure_support_sizes) == 4

    criteria = all(
        (
            representative_family_complete,
            declared_dirac_family_consistent,
            frame_invertible,
            independent,
            structure_nontrivial,
            first_class,
            smeared_established,
            canonical_support_ok,
            closure_cycle_spanning,
        )
    )

    return Stage16ADiagnostics(
        orbit_count=len(canonical_stage16a_orbits()),
        representative_count=len(representatives),
        representatives_per_orbit=81,
        off_surface_probe_count=len(off_surface),
        smeared_pair_count=len(STAGE16A_SMEARING_PAIRS),
        smeared_probe_count=len(smeared_probes),
        jacobi_probe_count=len(jacobi_residuals),
        structure_function_values=structure_values,
        frame_determinant_values=determinant_values,
        minimum_abs_frame_determinant=float(
            min(abs(stage16a_frame_determinant(point)) for point in positive)
        ),
        minimum_constraint_gradient_rank=min(gradient_ranks),
        minimum_generator_vector_rank=min(generator_ranks),
        minimum_constraint_gradient_sigma_min=min(gradient_sigma_min),
        minimum_generator_vector_sigma_min=min(generator_sigma_min),
        max_constraint_residual=float(max_constraint_residual),
        max_seed_inverse_residual=float(max_seed_inverse_residual),
        max_unsmeared_seed_formula_residual=float(max(unsmeared_seed_residuals)),
        max_unsmeared_presented_reconstruction_residual=float(
            max(unsmeared_presented_residuals)
        ),
        max_jacobi_residual=float(max(jacobi_residuals)),
        max_smeared_seed_formula_residual=float(
            max(abs(probe.direct_value - probe.seed_expected_value) for probe in smeared_probes)
        ),
        max_smeared_presented_reconstruction_residual=float(
            max(abs(probe.direct_value - probe.reconstructed_value) for probe in smeared_probes)
        ),
        max_smeared_antisymmetry_residual=float(
            max(probe.antisymmetry_residual for probe in smeared_probes)
        ),
        off_surface_nonzero_adjacent_forward_count=off_surface_nonzero,
        cycle_spanning_closure_coordinate_count=cycle_spanning_count,
        max_closure_coordinate_support_size=max(closure_support_sizes),
        representative_family_complete=representative_family_complete,
        declared_dirac_family_consistent=declared_dirac_family_consistent,
        frame_invertible_on_positive_family=frame_invertible,
        independent_constraint_directions=independent,
        structure_functions_nontrivial=structure_nontrivial,
        first_class_presented_closure_established=first_class,
        smeared_presented_closure_established=smeared_established,
        canonical_function_support_established=canonical_support_ok,
        closure_coordinate_cycle_spanning_observed=closure_cycle_spanning,
        criteria_11_17_satisfied=criteria,
    )
