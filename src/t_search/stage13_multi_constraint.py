"""Stage 13A two-constraint first-class carrier and finite representative family.

The module implements only the Stage 13A evidence frozen in
``docs/stage13_protocol.md``.  It establishes the positive two-constraint
carrier, the 36 canonical representatives, independence of the two constraint
/ generator directions, the first-class bracket identity, and preservation of
the constraint surface under each generator separately.

Mixed two-generator path closure is intentionally deferred to Stage 13B.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp

import numpy as np

STAGE13A_ATOL = 1e-10
STAGE13A_A = 0.5

STAGE13A_K_T = "K_T"
STAGE13A_K_X = "K_X"
STAGE13A_BASIS_ID = "stage13_noncommuting_positive_basis"
STAGE13A_BASIS_ROLE = "constraint_basis_presentation"
STAGE13A_GENERATOR_ROLE = "constraint_generator_identity"
STAGE13A_GAUGE_FLOW_TYPE = "constraint_generated_gauge_flow"
STAGE13A_ORBIT_ROLE = "physical_orbit_identity"
STAGE13A_REPRESENTATIVE_ROLE = "constraint_gauge_representative"
STAGE13A_EVENT_ROLE = "carrier_sample_event"
STAGE13A_CLOCK_T_ROLE = "gauge_coordinate_clock_T"
STAGE13A_CLOCK_X_ROLE = "gauge_coordinate_clock_X"

STAGE13A_OMEGA_ALPHA = "omega_alpha"
STAGE13A_OMEGA_BETA = "omega_beta"
STAGE13A_OMEGA_GAMMA = "omega_gamma"
STAGE13A_OMEGA_DELTA = "omega_delta"
STAGE13A_CANONICAL_ORBIT_IDS = (
    STAGE13A_OMEGA_ALPHA,
    STAGE13A_OMEGA_BETA,
    STAGE13A_OMEGA_GAMMA,
    STAGE13A_OMEGA_DELTA,
)
STAGE13A_GRID_VALUES = (-1.0, 0.0, 1.0)


@dataclass(frozen=True, slots=True)
class Stage13PhysicalOrbit:
    orbit_id: str
    orbit_role: str
    Q_D: float
    P_D: float
    physical_role: str


@dataclass(frozen=True, slots=True)
class Stage13PhaseSpacePoint:
    T: float
    p_T: float
    X: float
    p_X: float
    q: float
    p: float


@dataclass(frozen=True, slots=True)
class Stage13Representative:
    orbit_id: str
    orbit_role: str
    representative_id: str
    representative_role: str
    event_id: str
    event_role: str
    clock_T_id: str
    clock_T_role: str
    clock_X_id: str
    clock_X_role: str
    constraint_basis_id: str
    constraint_basis_role: str
    generator_family_type: str
    T: float
    p_T: float
    X: float
    p_X: float
    q: float
    p: float
    K_T_value: float
    K_X_value: float
    declared_Q_D: float
    declared_P_D: float
    provenance: str

    def point(self) -> Stage13PhaseSpacePoint:
        return Stage13PhaseSpacePoint(
            T=self.T,
            p_T=self.p_T,
            X=self.X,
            p_X=self.p_X,
            q=self.q,
            p=self.p,
        )


@dataclass(frozen=True, slots=True)
class Stage13SingleGeneratorTransport:
    transport_id: str
    transform_type: str
    generator_id: str
    generator_role: str
    constraint_basis_id: str
    orbit_id: str
    source_representative_id: str
    target_representative_id: str
    source_event_id: str
    target_event_id: str
    raw_parameter: float
    phase_space_residual: float
    source_constraint_residual: float
    predicted_constraint_residual: float
    target_constraint_residual: float
    provenance: str


@dataclass(frozen=True, slots=True)
class Stage13ADiagnostics:
    orbit_count: int
    representative_count: int
    representatives_per_orbit: int
    phi_T_transport_count: int
    phi_X_transport_count: int
    single_generator_transport_count: int
    mixed_ordered_pair_count: int
    off_surface_bracket_probe_count: int
    distinct_declared_initial_data_count: int
    minimum_constraint_gradient_rank: int
    minimum_generator_vector_rank: int
    minimum_constraint_gradient_sigma_min: float
    minimum_generator_vector_sigma_min: float
    max_K_T_constraint_residual: float
    max_K_X_constraint_residual: float
    max_bracket_identity_residual: float
    max_phi_T_endpoint_residual: float
    max_phi_X_endpoint_residual: float
    max_flow_constraint_residual: float
    canonical_orbits_distinct: bool
    representative_family_complete: bool
    independent_constraint_directions: bool
    first_class_closure_established: bool
    individual_flows_preserve_surface: bool
    physical_initial_data_preserved: bool
    typed_provenance_explicit: bool
    criteria_11_16_satisfied: bool


def canonical_stage13a_orbits() -> tuple[Stage13PhysicalOrbit, ...]:
    """Return the four Stage-12-carried physical initial-data classes."""

    return (
        Stage13PhysicalOrbit(
            STAGE13A_OMEGA_ALPHA,
            STAGE13A_ORBIT_ROLE,
            -0.35,
            1.25,
            "canonical physical orbit; Stage 12 alpha initial data",
        ),
        Stage13PhysicalOrbit(
            STAGE13A_OMEGA_BETA,
            STAGE13A_ORBIT_ROLE,
            0.40,
            1.25,
            "same P_D as alpha, different Q_D",
        ),
        Stage13PhysicalOrbit(
            STAGE13A_OMEGA_GAMMA,
            STAGE13A_ORBIT_ROLE,
            -0.35,
            0.75,
            "same Q_D as alpha, different P_D",
        ),
        Stage13PhysicalOrbit(
            STAGE13A_OMEGA_DELTA,
            STAGE13A_ORBIT_ROLE,
            0.20,
            1.75,
            "both declared initial-data components differ from alpha",
        ),
    )


def canonical_stage13a_grid_values() -> tuple[float, ...]:
    return STAGE13A_GRID_VALUES


def stage13a_K_T(point: Stage13PhaseSpacePoint) -> float:
    return float(point.p_T + 0.5 * point.p**2)


def stage13a_K_X(point: Stage13PhaseSpacePoint) -> float:
    return float(exp(point.T) * (point.p_X + STAGE13A_A * point.p))


def stage13a_constraint_gradients(point: Stage13PhaseSpacePoint) -> np.ndarray:
    """Gradients in coordinate order ``(T,p_T,X,p_X,q,p)``."""

    eT = exp(point.T)
    K_X = stage13a_K_X(point)
    return np.asarray(
        [
            [0.0, 1.0, 0.0, 0.0, 0.0, point.p],
            [K_X, 0.0, 0.0, eT, 0.0, STAGE13A_A * eT],
        ],
        dtype=float,
    )


def _hamiltonian_vector_from_gradient(gradient: np.ndarray) -> np.ndarray:
    """Return J grad(f) for canonical pairs (T,p_T),(X,p_X),(q,p)."""

    return np.asarray(
        [
            gradient[1],
            -gradient[0],
            gradient[3],
            -gradient[2],
            gradient[5],
            -gradient[4],
        ],
        dtype=float,
    )


def stage13a_generator_vectors(point: Stage13PhaseSpacePoint) -> np.ndarray:
    gradients = stage13a_constraint_gradients(point)
    return np.asarray(
        [
            _hamiltonian_vector_from_gradient(gradients[0]),
            _hamiltonian_vector_from_gradient(gradients[1]),
        ],
        dtype=float,
    )


def _poisson_from_gradients(df: np.ndarray, dg: np.ndarray) -> float:
    total = 0.0
    for q_index, p_index in ((0, 1), (2, 3), (4, 5)):
        total += df[q_index] * dg[p_index] - df[p_index] * dg[q_index]
    return float(total)


def stage13a_poisson_KT_KX(point: Stage13PhaseSpacePoint) -> float:
    gradients = stage13a_constraint_gradients(point)
    return _poisson_from_gradients(gradients[0], gradients[1])


def _grid_label(value: float) -> str:
    if value < 0:
        return f"m{abs(value):.1f}".replace(".", "p")
    return f"p{value:.1f}".replace(".", "p")


def canonical_stage13a_representatives_for_orbit(
    orbit: Stage13PhysicalOrbit,
) -> tuple[Stage13Representative, ...]:
    result: list[Stage13Representative] = []
    for T in STAGE13A_GRID_VALUES:
        for X in STAGE13A_GRID_VALUES:
            p = float(orbit.P_D)
            p_T = float(-0.5 * p**2)
            p_X = float(-STAGE13A_A * p)
            q = float(orbit.Q_D + p * T + STAGE13A_A * X)
            point = Stage13PhaseSpacePoint(T, p_T, X, p_X, q, p)
            suffix = f"T_{_grid_label(T)}:X_{_grid_label(X)}"
            result.append(
                Stage13Representative(
                    orbit_id=orbit.orbit_id,
                    orbit_role=STAGE13A_ORBIT_ROLE,
                    representative_id=f"{orbit.orbit_id}:rep:{suffix}",
                    representative_role=STAGE13A_REPRESENTATIVE_ROLE,
                    event_id=f"{orbit.orbit_id}:event:{suffix}",
                    event_role=STAGE13A_EVENT_ROLE,
                    clock_T_id="clock_T",
                    clock_T_role=STAGE13A_CLOCK_T_ROLE,
                    clock_X_id="clock_X",
                    clock_X_role=STAGE13A_CLOCK_X_ROLE,
                    constraint_basis_id=STAGE13A_BASIS_ID,
                    constraint_basis_role=STAGE13A_BASIS_ROLE,
                    generator_family_type=STAGE13A_GAUGE_FLOW_TYPE,
                    T=float(T),
                    p_T=p_T,
                    X=float(X),
                    p_X=p_X,
                    q=q,
                    p=p,
                    K_T_value=stage13a_K_T(point),
                    K_X_value=stage13a_K_X(point),
                    declared_Q_D=float(orbit.Q_D),
                    declared_P_D=float(orbit.P_D),
                    provenance="Stage 13 positive two-constraint representative grid",
                )
            )
    return tuple(result)


def canonical_stage13a_representatives() -> tuple[Stage13Representative, ...]:
    return tuple(
        representative
        for orbit in canonical_stage13a_orbits()
        for representative in canonical_stage13a_representatives_for_orbit(orbit)
    )


def _constraint_residual(point: Stage13PhaseSpacePoint) -> float:
    return float(max(abs(stage13a_K_T(point)), abs(stage13a_K_X(point))))


def _phase_space_residual(
    predicted: Stage13PhaseSpacePoint,
    target: Stage13Representative,
) -> float:
    return float(
        max(
            abs(predicted.T - target.T),
            abs(predicted.p_T - target.p_T),
            abs(predicted.X - target.X),
            abs(predicted.p_X - target.p_X),
            abs(predicted.q - target.q),
            abs(predicted.p - target.p),
        )
    )


def stage13a_phi_T_transport(
    source: Stage13Representative,
    target: Stage13Representative,
) -> Stage13SingleGeneratorTransport:
    if source.orbit_id != target.orbit_id:
        raise ValueError("Phi_T cannot connect distinct physical orbits")
    if abs(source.X - target.X) > STAGE13A_ATOL:
        raise ValueError("Phi_T licensed Stage 13A transport requires fixed X")
    if source.constraint_basis_id != STAGE13A_BASIS_ID or target.constraint_basis_id != STAGE13A_BASIS_ID:
        raise ValueError("Phi_T requires the frozen Stage 13A positive constraint basis")

    s = float(target.T - source.T)
    predicted = Stage13PhaseSpacePoint(
        T=float(source.T + s),
        p_T=source.p_T,
        X=source.X,
        p_X=source.p_X,
        q=float(source.q + source.p * s),
        p=source.p,
    )
    return Stage13SingleGeneratorTransport(
        transport_id=f"Phi_T:{source.representative_id}->{target.representative_id}",
        transform_type=STAGE13A_GAUGE_FLOW_TYPE,
        generator_id=STAGE13A_K_T,
        generator_role=STAGE13A_GENERATOR_ROLE,
        constraint_basis_id=STAGE13A_BASIS_ID,
        orbit_id=source.orbit_id,
        source_representative_id=source.representative_id,
        target_representative_id=target.representative_id,
        source_event_id=source.event_id,
        target_event_id=target.event_id,
        raw_parameter=s,
        phase_space_residual=_phase_space_residual(predicted, target),
        source_constraint_residual=_constraint_residual(source.point()),
        predicted_constraint_residual=_constraint_residual(predicted),
        target_constraint_residual=_constraint_residual(target.point()),
        provenance="licensed single-generator Hamiltonian flow of K_T",
    )


def stage13a_phi_X_transport(
    source: Stage13Representative,
    target: Stage13Representative,
) -> Stage13SingleGeneratorTransport:
    if source.orbit_id != target.orbit_id:
        raise ValueError("Phi_X cannot connect distinct physical orbits")
    if abs(source.T - target.T) > STAGE13A_ATOL:
        raise ValueError("Phi_X licensed Stage 13A transport requires fixed T")
    if source.constraint_basis_id != STAGE13A_BASIS_ID or target.constraint_basis_id != STAGE13A_BASIS_ID:
        raise ValueError("Phi_X requires the frozen Stage 13A positive constraint basis")

    eT = exp(source.T)
    u = float((target.X - source.X) / eT)
    source_K_X = stage13a_K_X(source.point())
    predicted = Stage13PhaseSpacePoint(
        T=source.T,
        p_T=float(source.p_T - u * source_K_X),
        X=float(source.X + eT * u),
        p_X=source.p_X,
        q=float(source.q + STAGE13A_A * eT * u),
        p=source.p,
    )
    return Stage13SingleGeneratorTransport(
        transport_id=f"Phi_X:{source.representative_id}->{target.representative_id}",
        transform_type=STAGE13A_GAUGE_FLOW_TYPE,
        generator_id=STAGE13A_K_X,
        generator_role=STAGE13A_GENERATOR_ROLE,
        constraint_basis_id=STAGE13A_BASIS_ID,
        orbit_id=source.orbit_id,
        source_representative_id=source.representative_id,
        target_representative_id=target.representative_id,
        source_event_id=source.event_id,
        target_event_id=target.event_id,
        raw_parameter=u,
        phase_space_residual=_phase_space_residual(predicted, target),
        source_constraint_residual=_constraint_residual(source.point()),
        predicted_constraint_residual=_constraint_residual(predicted),
        target_constraint_residual=_constraint_residual(target.point()),
        provenance="licensed single-generator Hamiltonian flow of K_X",
    )


def canonical_stage13a_phi_T_transports() -> tuple[Stage13SingleGeneratorTransport, ...]:
    result: list[Stage13SingleGeneratorTransport] = []
    for orbit in canonical_stage13a_orbits():
        representatives = canonical_stage13a_representatives_for_orbit(orbit)
        for source in representatives:
            for target in representatives:
                if source.representative_id == target.representative_id:
                    continue
                if abs(source.X - target.X) <= STAGE13A_ATOL:
                    result.append(stage13a_phi_T_transport(source, target))
    return tuple(result)


def canonical_stage13a_phi_X_transports() -> tuple[Stage13SingleGeneratorTransport, ...]:
    result: list[Stage13SingleGeneratorTransport] = []
    for orbit in canonical_stage13a_orbits():
        representatives = canonical_stage13a_representatives_for_orbit(orbit)
        for source in representatives:
            for target in representatives:
                if source.representative_id == target.representative_id:
                    continue
                if abs(source.T - target.T) <= STAGE13A_ATOL:
                    result.append(stage13a_phi_X_transport(source, target))
    return tuple(result)


def canonical_stage13a_single_generator_transports() -> tuple[Stage13SingleGeneratorTransport, ...]:
    return canonical_stage13a_phi_T_transports() + canonical_stage13a_phi_X_transports()


def canonical_stage13a_mixed_pairs() -> tuple[tuple[Stage13Representative, Stage13Representative], ...]:
    """Enumerate the Stage 13B mixed pair family without testing closure yet."""

    result: list[tuple[Stage13Representative, Stage13Representative]] = []
    for orbit in canonical_stage13a_orbits():
        representatives = canonical_stage13a_representatives_for_orbit(orbit)
        for source in representatives:
            for target in representatives:
                if source.representative_id == target.representative_id:
                    continue
                if abs(source.T - target.T) > STAGE13A_ATOL and abs(source.X - target.X) > STAGE13A_ATOL:
                    result.append((source, target))
    return tuple(result)


def canonical_stage13a_off_surface_bracket_probes() -> tuple[Stage13PhaseSpacePoint, ...]:
    """Create nonzero-K_X probes so the bracket identity is not tested only weakly."""

    probes: list[Stage13PhaseSpacePoint] = []
    for representative in canonical_stage13a_representatives():
        point = representative.point()
        probes.append(
            Stage13PhaseSpacePoint(
                T=point.T,
                p_T=point.p_T + 0.125,
                X=point.X,
                p_X=point.p_X + 0.20,
                q=point.q - 0.075,
                p=point.p,
            )
        )
    return tuple(probes)


def stage13a_diagnostics() -> Stage13ADiagnostics:
    orbits = canonical_stage13a_orbits()
    representatives = canonical_stage13a_representatives()
    phi_T = canonical_stage13a_phi_T_transports()
    phi_X = canonical_stage13a_phi_X_transports()
    transports = phi_T + phi_X
    mixed_pairs = canonical_stage13a_mixed_pairs()
    bracket_probes = canonical_stage13a_off_surface_bracket_probes()

    max_K_T = max(abs(rep.K_T_value) for rep in representatives)
    max_K_X = max(abs(rep.K_X_value) for rep in representatives)

    gradient_ranks: list[int] = []
    generator_ranks: list[int] = []
    gradient_sigma_mins: list[float] = []
    generator_sigma_mins: list[float] = []
    for representative in representatives:
        point = representative.point()
        gradients = stage13a_constraint_gradients(point)
        generators = stage13a_generator_vectors(point)
        gradient_ranks.append(int(np.linalg.matrix_rank(gradients, tol=STAGE13A_ATOL)))
        generator_ranks.append(int(np.linalg.matrix_rank(generators, tol=STAGE13A_ATOL)))
        gradient_sigma_mins.append(float(np.linalg.svd(gradients, compute_uv=False)[-1]))
        generator_sigma_mins.append(float(np.linalg.svd(generators, compute_uv=False)[-1]))

    bracket_points = tuple(rep.point() for rep in representatives) + bracket_probes
    max_bracket_residual = max(
        abs(stage13a_poisson_KT_KX(point) + stage13a_K_X(point))
        for point in bracket_points
    )

    max_phi_T_endpoint = max(item.phase_space_residual for item in phi_T)
    max_phi_X_endpoint = max(item.phase_space_residual for item in phi_X)
    max_flow_constraint = max(
        max(
            item.source_constraint_residual,
            item.predicted_constraint_residual,
            item.target_constraint_residual,
        )
        for item in transports
    )

    declared_pairs = {(orbit.Q_D, orbit.P_D) for orbit in orbits}
    counts = {
        orbit.orbit_id: sum(rep.orbit_id == orbit.orbit_id for rep in representatives)
        for orbit in orbits
    }
    canonical_orbits_distinct = (
        tuple(orbit.orbit_id for orbit in orbits) == STAGE13A_CANONICAL_ORBIT_IDS
        and len(declared_pairs) == 4
        and orbits[0].P_D == orbits[1].P_D
        and orbits[0].Q_D != orbits[1].Q_D
        and orbits[0].Q_D == orbits[2].Q_D
        and orbits[0].P_D != orbits[2].P_D
    )
    representative_family_complete = (
        len(representatives) == 36
        and all(count == 9 for count in counts.values())
        and len({rep.representative_id for rep in representatives}) == 36
        and len({rep.event_id for rep in representatives}) == 36
        and len(phi_T) == 72
        and len(phi_X) == 72
        and len(mixed_pairs) == 144
    )
    independent_constraint_directions = (
        min(gradient_ranks) == 2
        and min(generator_ranks) == 2
        and min(gradient_sigma_mins) > STAGE13A_ATOL
        and min(generator_sigma_mins) > STAGE13A_ATOL
    )
    first_class_closure_established = max_bracket_residual <= STAGE13A_ATOL
    individual_flows_preserve_surface = (
        max_phi_T_endpoint <= STAGE13A_ATOL
        and max_phi_X_endpoint <= STAGE13A_ATOL
        and max_flow_constraint <= STAGE13A_ATOL
    )
    physical_initial_data_preserved = (
        canonical_orbits_distinct
        and all(
            rep.declared_Q_D == next(orbit.Q_D for orbit in orbits if orbit.orbit_id == rep.orbit_id)
            and rep.declared_P_D == next(orbit.P_D for orbit in orbits if orbit.orbit_id == rep.orbit_id)
            for rep in representatives
        )
    )

    role_values = {
        STAGE13A_ORBIT_ROLE,
        STAGE13A_REPRESENTATIVE_ROLE,
        STAGE13A_EVENT_ROLE,
        STAGE13A_CLOCK_T_ROLE,
        STAGE13A_CLOCK_X_ROLE,
        STAGE13A_BASIS_ROLE,
        STAGE13A_GENERATOR_ROLE,
    }
    typed_provenance_explicit = (
        len(role_values) == 7
        and all(rep.orbit_role == STAGE13A_ORBIT_ROLE for rep in representatives)
        and all(rep.representative_role == STAGE13A_REPRESENTATIVE_ROLE for rep in representatives)
        and all(rep.event_role == STAGE13A_EVENT_ROLE for rep in representatives)
        and all(rep.clock_T_role == STAGE13A_CLOCK_T_ROLE for rep in representatives)
        and all(rep.clock_X_role == STAGE13A_CLOCK_X_ROLE for rep in representatives)
        and all(rep.constraint_basis_role == STAGE13A_BASIS_ROLE for rep in representatives)
        and all(item.generator_role == STAGE13A_GENERATOR_ROLE for item in transports)
        and {item.generator_id for item in transports} == {STAGE13A_K_T, STAGE13A_K_X}
    )

    criteria = (
        max_K_T <= STAGE13A_ATOL
        and max_K_X <= STAGE13A_ATOL
        and independent_constraint_directions
        and first_class_closure_established
        and individual_flows_preserve_surface
        and physical_initial_data_preserved
        and typed_provenance_explicit
        and representative_family_complete
    )

    return Stage13ADiagnostics(
        orbit_count=len(orbits),
        representative_count=len(representatives),
        representatives_per_orbit=9,
        phi_T_transport_count=len(phi_T),
        phi_X_transport_count=len(phi_X),
        single_generator_transport_count=len(transports),
        mixed_ordered_pair_count=len(mixed_pairs),
        off_surface_bracket_probe_count=len(bracket_probes),
        distinct_declared_initial_data_count=len(declared_pairs),
        minimum_constraint_gradient_rank=min(gradient_ranks),
        minimum_generator_vector_rank=min(generator_ranks),
        minimum_constraint_gradient_sigma_min=min(gradient_sigma_mins),
        minimum_generator_vector_sigma_min=min(generator_sigma_mins),
        max_K_T_constraint_residual=float(max_K_T),
        max_K_X_constraint_residual=float(max_K_X),
        max_bracket_identity_residual=float(max_bracket_residual),
        max_phi_T_endpoint_residual=float(max_phi_T_endpoint),
        max_phi_X_endpoint_residual=float(max_phi_X_endpoint),
        max_flow_constraint_residual=float(max_flow_constraint),
        canonical_orbits_distinct=canonical_orbits_distinct,
        representative_family_complete=representative_family_complete,
        independent_constraint_directions=independent_constraint_directions,
        first_class_closure_established=first_class_closure_established,
        individual_flows_preserve_surface=individual_flows_preserve_surface,
        physical_initial_data_preserved=physical_initial_data_preserved,
        typed_provenance_explicit=typed_provenance_explicit,
        criteria_11_16_satisfied=criteria,
    )


def stage13a_summary() -> dict[str, object]:
    diagnostics = stage13a_diagnostics()
    return {
        "stage": "13A",
        "bounded_result": (
            "Stage 13A two-constraint first-class carrier and finite representative family "
            "on the frozen four-orbit family = established"
        ),
        "orbit_count": diagnostics.orbit_count,
        "representative_count": diagnostics.representative_count,
        "representatives_per_orbit": diagnostics.representatives_per_orbit,
        "phi_T_transport_count": diagnostics.phi_T_transport_count,
        "phi_X_transport_count": diagnostics.phi_X_transport_count,
        "single_generator_transport_count": diagnostics.single_generator_transport_count,
        "mixed_ordered_pair_count_reserved_for_stage13b": diagnostics.mixed_ordered_pair_count,
        "off_surface_bracket_probe_count": diagnostics.off_surface_bracket_probe_count,
        "minimum_constraint_gradient_rank": diagnostics.minimum_constraint_gradient_rank,
        "minimum_generator_vector_rank": diagnostics.minimum_generator_vector_rank,
        "max_K_T_constraint_residual": diagnostics.max_K_T_constraint_residual,
        "max_K_X_constraint_residual": diagnostics.max_K_X_constraint_residual,
        "max_bracket_identity_residual": diagnostics.max_bracket_identity_residual,
        "max_phi_T_endpoint_residual": diagnostics.max_phi_T_endpoint_residual,
        "max_phi_X_endpoint_residual": diagnostics.max_phi_X_endpoint_residual,
        "max_flow_constraint_residual": diagnostics.max_flow_constraint_residual,
        "criteria_11_16_satisfied": diagnostics.criteria_11_16_satisfied,
        "guards": (
            "two constraint labels != two independent gauge directions",
            "first-class closure on this toy carrier != hypersurface-deformation algebra",
            "constraint-generator identity != physical-event identity",
            "constraint-generator identity != internal-clock perspective",
            "Stage 13A single-generator surface preservation != compensated multi-generator path closure",
            "finite-model success != empirical discovery",
        ),
        "next": "Stage 13B — noncommuting gauge paths and compensated closure",
    }
