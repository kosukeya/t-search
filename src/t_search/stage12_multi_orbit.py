"""Stage 12A multi-orbit constrained carrier and gauge-flow representatives.

Stage 12A extends the Stage 11 parametrized free-particle scaffold from one
constraint orbit to four physically distinct canonical orbits.  The module
keeps three notions deliberately separate:

* physical-orbit identity ``omega``;
* constraint-generated gauge flow ``Phi_s`` between representatives of one
  orbit;
* Stage 11 external reparameterization ``G`` of a trajectory representation.

The finite carrier is diagnostic only.  In particular, constraint-generated
gauge flow is not promoted to ontological becoming and this finite gauge atlas
is not general covariance or a model of general relativity.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from t_search.stage11_parametrized import (
    STAGE11A_ATOL,
    STAGE11A_POSITIVE_PARAMETERIZATION_IDS,
    canonical_stage11a_parameterizations,
    canonical_stage11a_trajectory,
    stage11a_lapse_chain_rule_residual,
)

STAGE12A_ATOL = STAGE11A_ATOL

STAGE12A_CONSTRAINT_ID = "free_particle_parametrized_constraint"
STAGE12A_GAUGE_CHART_ID = "stage12a_seed_gauge_chart"
STAGE12A_GAUGE_FLOW_TYPE = "constraint_generated_gauge_flow"
STAGE12A_EXTERNAL_REPARAM_TYPE = "external_reparameterization"
STAGE12A_EVENT_ROLE = "relational_clock_evaluation"

STAGE12A_OMEGA_ALPHA = "omega_alpha"
STAGE12A_OMEGA_BETA = "omega_beta"
STAGE12A_OMEGA_GAMMA = "omega_gamma"
STAGE12A_OMEGA_DELTA = "omega_delta"

STAGE12A_CANONICAL_ORBIT_IDS = (
    STAGE12A_OMEGA_ALPHA,
    STAGE12A_OMEGA_BETA,
    STAGE12A_OMEGA_GAMMA,
    STAGE12A_OMEGA_DELTA,
)

STAGE12A_GAUGE_PARAMETERS = (-1.0, -0.5, 0.0, 0.5, 1.0)


@dataclass(frozen=True, slots=True)
class Stage12PhysicalOrbit:
    orbit_id: str
    Q_D: float
    P_D: float
    constraint_id: str
    physical_role: str


@dataclass(frozen=True, slots=True)
class Stage12GaugeRepresentative:
    orbit_id: str
    representative_id: str
    event_id: str
    event_role: str
    gauge_chart_id: str
    gauge_flow_type: str
    gauge_parameter_s: float
    T: float
    q: float
    p: float
    p_T: float
    constraint_value: float
    Q_D: float
    P_D: float
    provenance: str


@dataclass(frozen=True, slots=True)
class Stage12GaugeTransport:
    transport_id: str
    transform_type: str
    orbit_id: str
    source_representative_id: str
    target_representative_id: str
    source_event_id: str
    target_event_id: str
    delta_s: float
    phase_space_residual: float
    Q_D_drift: float
    P_D_drift: float
    max_constraint_residual: float
    provenance: str


@dataclass(frozen=True, slots=True)
class Stage12ExternalParameterizationView:
    orbit_id: str
    parameterization_id: str
    transform_type: str
    event_ids: tuple[str, ...]
    source_parameter_type: str
    parameter_label_type: str
    source_labels: np.ndarray
    parameter_labels: np.ndarray
    clock_values: np.ndarray
    q_values: np.ndarray
    p_values: np.ndarray
    p_T_values: np.ndarray
    lapse_values: np.ndarray
    constraint_values: np.ndarray
    lapse_chain_rule_residual: float
    provenance: str


@dataclass(frozen=True, slots=True)
class Stage12ADiagnostics:
    orbit_count: int
    representative_count: int
    representatives_per_orbit: int
    gauge_transport_count: int
    external_parameterization_view_count: int
    external_parameterized_event_count: int
    distinct_dirac_pair_count: int
    max_constraint_residual: float
    max_representative_Q_D_residual: float
    max_representative_P_D_residual: float
    max_gauge_transport_residual: float
    max_gauge_Q_D_drift: float
    max_gauge_P_D_drift: float
    max_external_constraint_residual: float
    max_external_Q_D_residual: float
    max_external_P_D_residual: float
    max_external_lapse_chain_rule_residual: float
    minimum_external_positive_lapse: float
    canonical_orbits_distinct: bool
    gauge_representatives_complete: bool
    gauge_invariants_preserved: bool
    external_parameterization_family_complete: bool
    typed_provenance_explicit: bool
    criteria_11_16_satisfied: bool


def canonical_stage12a_orbits() -> tuple[Stage12PhysicalOrbit, ...]:
    """Return the four protocol-frozen physical-orbit controls."""

    return (
        Stage12PhysicalOrbit(
            STAGE12A_OMEGA_ALPHA,
            -0.35,
            1.25,
            STAGE12A_CONSTRAINT_ID,
            "canonical physical orbit; exact Stage 11 baseline",
        ),
        Stage12PhysicalOrbit(
            STAGE12A_OMEGA_BETA,
            0.40,
            1.25,
            STAGE12A_CONSTRAINT_ID,
            "canonical physical orbit; same P_D as alpha, different Q_D",
        ),
        Stage12PhysicalOrbit(
            STAGE12A_OMEGA_GAMMA,
            -0.35,
            0.75,
            STAGE12A_CONSTRAINT_ID,
            "canonical physical orbit; same Q_D as alpha, different P_D",
        ),
        Stage12PhysicalOrbit(
            STAGE12A_OMEGA_DELTA,
            0.20,
            1.75,
            STAGE12A_CONSTRAINT_ID,
            "canonical physical orbit; both Dirac invariants differ from alpha",
        ),
    )


def canonical_stage12a_gauge_parameters() -> tuple[float, ...]:
    """Finite sample of the constraint-generated gauge-flow parameter s."""

    return STAGE12A_GAUGE_PARAMETERS


def _orbit_lookup() -> dict[str, Stage12PhysicalOrbit]:
    return {orbit.orbit_id: orbit for orbit in canonical_stage12a_orbits()}


def canonical_stage12a_representatives_for_orbit(
    orbit: Stage12PhysicalOrbit,
) -> tuple[Stage12GaugeRepresentative, ...]:
    """Sample five representatives related by Hamiltonian flow of C.

    The seed chart uses ``T=s`` only as a convenient numerical chart choice.
    ``T`` and ``s`` remain separately typed fields and are not identified by
    definition.  External parameter labels are represented separately below.
    """

    result: list[Stage12GaugeRepresentative] = []
    for index, s in enumerate(canonical_stage12a_gauge_parameters()):
        T = float(s)
        p = float(orbit.P_D)
        q = float(orbit.Q_D + orbit.P_D * T)
        p_T = float(-0.5 * orbit.P_D**2)
        constraint = float(p_T + 0.5 * p**2)
        Q_D = float(q - p * T)
        P_D = p
        result.append(
            Stage12GaugeRepresentative(
                orbit_id=orbit.orbit_id,
                representative_id=f"{orbit.orbit_id}:rep_{index:02d}",
                event_id=f"{orbit.orbit_id}:event_{index:02d}",
                event_role=STAGE12A_EVENT_ROLE,
                gauge_chart_id=STAGE12A_GAUGE_CHART_ID,
                gauge_flow_type=STAGE12A_GAUGE_FLOW_TYPE,
                gauge_parameter_s=float(s),
                T=T,
                q=q,
                p=p,
                p_T=p_T,
                constraint_value=constraint,
                Q_D=Q_D,
                P_D=P_D,
                provenance="Hamiltonian flow of C within one declared physical orbit",
            )
        )
    return tuple(result)


def canonical_stage12a_representatives() -> tuple[Stage12GaugeRepresentative, ...]:
    return tuple(
        representative
        for orbit in canonical_stage12a_orbits()
        for representative in canonical_stage12a_representatives_for_orbit(orbit)
    )


def stage12a_gauge_transport(
    source: Stage12GaugeRepresentative,
    target: Stage12GaugeRepresentative,
) -> Stage12GaugeTransport:
    """Construct one licensed same-orbit ``Phi_s`` transport.

    Cross-orbit transport is rejected at construction time.  Stage 12F later
    treats attempted cross-orbit transport as an explicit negative control.
    """

    if source.orbit_id != target.orbit_id:
        raise ValueError("Stage 12A gauge transport cannot connect distinct physical orbits")
    if source.gauge_flow_type != STAGE12A_GAUGE_FLOW_TYPE:
        raise ValueError("Stage 12A source is not typed as a constraint-generated gauge representative")
    if target.gauge_flow_type != STAGE12A_GAUGE_FLOW_TYPE:
        raise ValueError("Stage 12A target is not typed as a constraint-generated gauge representative")

    delta_s = float(target.gauge_parameter_s - source.gauge_parameter_s)
    predicted_T = source.T + delta_s
    predicted_q = source.q + source.p * delta_s
    predicted_p = source.p
    predicted_p_T = source.p_T
    phase_space_residual = max(
        abs(target.T - predicted_T),
        abs(target.q - predicted_q),
        abs(target.p - predicted_p),
        abs(target.p_T - predicted_p_T),
    )

    return Stage12GaugeTransport(
        transport_id=(
            f"Phi:{source.orbit_id}:"
            f"{source.representative_id.split(':')[-1]}->"
            f"{target.representative_id.split(':')[-1]}"
        ),
        transform_type=STAGE12A_GAUGE_FLOW_TYPE,
        orbit_id=source.orbit_id,
        source_representative_id=source.representative_id,
        target_representative_id=target.representative_id,
        source_event_id=source.event_id,
        target_event_id=target.event_id,
        delta_s=delta_s,
        phase_space_residual=float(phase_space_residual),
        Q_D_drift=float(abs(target.Q_D - source.Q_D)),
        P_D_drift=float(abs(target.P_D - source.P_D)),
        max_constraint_residual=float(
            max(abs(source.constraint_value), abs(target.constraint_value))
        ),
        provenance="typed Phi_s generated by Hamiltonian flow of C",
    )


def canonical_stage12a_gauge_transports() -> tuple[Stage12GaugeTransport, ...]:
    """Return all ordered non-identity same-orbit transports in the sample."""

    result: list[Stage12GaugeTransport] = []
    for orbit in canonical_stage12a_orbits():
        representatives = canonical_stage12a_representatives_for_orbit(orbit)
        for source in representatives:
            for target in representatives:
                if source.representative_id == target.representative_id:
                    continue
                result.append(stage12a_gauge_transport(source, target))
    return tuple(result)


def stage12a_external_parameterization_view(
    orbit: Stage12PhysicalOrbit,
    parameterization_id: str,
) -> Stage12ExternalParameterizationView:
    """Lift one Stage 11 positive external representation to one orbit."""

    positive_ids = {
        item.parameterization_id for item in canonical_stage11a_parameterizations()
    }
    if parameterization_id not in positive_ids:
        raise ValueError(
            f"{parameterization_id!r} is not in the Stage 11 positive external parameterization family"
        )

    trajectory = canonical_stage11a_trajectory(
        parameterization_id,
        q0=orbit.Q_D,
        momentum=orbit.P_D,
    )
    return Stage12ExternalParameterizationView(
        orbit_id=orbit.orbit_id,
        parameterization_id=parameterization_id,
        transform_type=STAGE12A_EXTERNAL_REPARAM_TYPE,
        event_ids=tuple(f"{orbit.orbit_id}:{event_id}" for event_id in trajectory.event_ids),
        source_parameter_type="external_seed_label_lambda",
        parameter_label_type="external_parameter_label_lambda_rho",
        source_labels=trajectory.source_labels.copy(),
        parameter_labels=trajectory.parameter_labels.copy(),
        clock_values=trajectory.clock_values.copy(),
        q_values=trajectory.q_values.copy(),
        p_values=trajectory.p_values.copy(),
        p_T_values=trajectory.p_T_values.copy(),
        lapse_values=trajectory.lapse_values.copy(),
        constraint_values=trajectory.constraint_values.copy(),
        lapse_chain_rule_residual=stage11a_lapse_chain_rule_residual(trajectory),
        provenance="Stage 11 positive external reparameterization lifted to a typed Stage 12 physical orbit",
    )


def canonical_stage12a_external_views() -> tuple[Stage12ExternalParameterizationView, ...]:
    return tuple(
        stage12a_external_parameterization_view(orbit, parameterization_id)
        for orbit in canonical_stage12a_orbits()
        for parameterization_id in STAGE11A_POSITIVE_PARAMETERIZATION_IDS
    )


def stage12a_diagnostics() -> Stage12ADiagnostics:
    orbits = canonical_stage12a_orbits()
    orbit_by_id = _orbit_lookup()
    representatives = canonical_stage12a_representatives()
    transports = canonical_stage12a_gauge_transports()
    external_views = canonical_stage12a_external_views()

    distinct_pairs = {(orbit.Q_D, orbit.P_D) for orbit in orbits}
    canonical_orbits_distinct = (
        len(orbits) == 4
        and tuple(orbit.orbit_id for orbit in orbits) == STAGE12A_CANONICAL_ORBIT_IDS
        and len(distinct_pairs) == 4
        and len({orbit.constraint_id for orbit in orbits}) == 1
    )

    representatives_per_orbit = len(canonical_stage12a_gauge_parameters())
    representative_counts = {
        orbit.orbit_id: sum(rep.orbit_id == orbit.orbit_id for rep in representatives)
        for orbit in orbits
    }
    gauge_representatives_complete = (
        representatives_per_orbit >= 2
        and all(count == representatives_per_orbit for count in representative_counts.values())
        and len(representatives) == len(orbits) * representatives_per_orbit
    )

    max_constraint = max(abs(rep.constraint_value) for rep in representatives)
    max_Q_residual = max(
        abs(rep.Q_D - orbit_by_id[rep.orbit_id].Q_D) for rep in representatives
    )
    max_P_residual = max(
        abs(rep.P_D - orbit_by_id[rep.orbit_id].P_D) for rep in representatives
    )
    max_transport = max(item.phase_space_residual for item in transports)
    max_Q_drift = max(item.Q_D_drift for item in transports)
    max_P_drift = max(item.P_D_drift for item in transports)
    gauge_invariants_preserved = (
        max_constraint <= STAGE12A_ATOL
        and max_Q_residual <= STAGE12A_ATOL
        and max_P_residual <= STAGE12A_ATOL
        and max_transport <= STAGE12A_ATOL
        and max_Q_drift <= STAGE12A_ATOL
        and max_P_drift <= STAGE12A_ATOL
    )

    max_external_constraint = 0.0
    max_external_Q = 0.0
    max_external_P = 0.0
    max_external_chain = 0.0
    min_external_lapse = float("inf")
    external_parameterized_event_count = 0
    ids_by_orbit: dict[str, set[str]] = {orbit.orbit_id: set() for orbit in orbits}

    for view in external_views:
        orbit = orbit_by_id[view.orbit_id]
        ids_by_orbit[view.orbit_id].add(view.parameterization_id)
        max_external_constraint = max(
            max_external_constraint,
            float(np.max(np.abs(view.constraint_values))),
        )
        Q_values = view.q_values - view.p_values * view.clock_values
        max_external_Q = max(
            max_external_Q,
            float(np.max(np.abs(Q_values - orbit.Q_D))),
        )
        max_external_P = max(
            max_external_P,
            float(np.max(np.abs(view.p_values - orbit.P_D))),
        )
        max_external_chain = max(max_external_chain, view.lapse_chain_rule_residual)
        min_external_lapse = min(min_external_lapse, float(np.min(view.lapse_values)))
        external_parameterized_event_count += len(view.event_ids)

    expected_external_ids = set(STAGE11A_POSITIVE_PARAMETERIZATION_IDS)
    external_parameterization_family_complete = (
        len(external_views) == len(orbits) * len(expected_external_ids)
        and all(ids == expected_external_ids for ids in ids_by_orbit.values())
        and min_external_lapse > 0.0
        and max_external_constraint <= STAGE12A_ATOL
        and max_external_Q <= STAGE12A_ATOL
        and max_external_P <= STAGE12A_ATOL
        and max_external_chain <= STAGE12A_ATOL
    )

    representative_event_ids = {rep.event_id for rep in representatives}
    typed_provenance_explicit = (
        len(representative_event_ids) == len(representatives)
        and all(rep.orbit_id in rep.representative_id for rep in representatives)
        and all(rep.orbit_id in rep.event_id for rep in representatives)
        and all(rep.event_role == STAGE12A_EVENT_ROLE for rep in representatives)
        and all(rep.gauge_flow_type == STAGE12A_GAUGE_FLOW_TYPE for rep in representatives)
        and all(item.transform_type == STAGE12A_GAUGE_FLOW_TYPE for item in transports)
        and all(item.transform_type == STAGE12A_EXTERNAL_REPARAM_TYPE for item in external_views)
        and STAGE12A_GAUGE_FLOW_TYPE != STAGE12A_EXTERNAL_REPARAM_TYPE
        and all(
            view.source_parameter_type != view.parameter_label_type
            for view in external_views
        )
    )

    criteria = (
        canonical_orbits_distinct
        and gauge_representatives_complete
        and gauge_invariants_preserved
        and external_parameterization_family_complete
        and typed_provenance_explicit
    )

    return Stage12ADiagnostics(
        orbit_count=len(orbits),
        representative_count=len(representatives),
        representatives_per_orbit=representatives_per_orbit,
        gauge_transport_count=len(transports),
        external_parameterization_view_count=len(external_views),
        external_parameterized_event_count=external_parameterized_event_count,
        distinct_dirac_pair_count=len(distinct_pairs),
        max_constraint_residual=float(max_constraint),
        max_representative_Q_D_residual=float(max_Q_residual),
        max_representative_P_D_residual=float(max_P_residual),
        max_gauge_transport_residual=float(max_transport),
        max_gauge_Q_D_drift=float(max_Q_drift),
        max_gauge_P_D_drift=float(max_P_drift),
        max_external_constraint_residual=float(max_external_constraint),
        max_external_Q_D_residual=float(max_external_Q),
        max_external_P_D_residual=float(max_external_P),
        max_external_lapse_chain_rule_residual=float(max_external_chain),
        minimum_external_positive_lapse=float(min_external_lapse),
        canonical_orbits_distinct=canonical_orbits_distinct,
        gauge_representatives_complete=gauge_representatives_complete,
        gauge_invariants_preserved=gauge_invariants_preserved,
        external_parameterization_family_complete=external_parameterization_family_complete,
        typed_provenance_explicit=typed_provenance_explicit,
        criteria_11_16_satisfied=criteria,
    )


def stage12a_summary() -> dict[str, object]:
    diagnostics = stage12a_diagnostics()
    return {
        "status": (
            "Stage 12A completed; criteria 11–16 satisfied"
            if diagnostics.criteria_11_16_satisfied
            else "Stage 12A incomplete"
        ),
        "constraint": "C = p_T + p^2/2 = 0",
        "physical_orbits": {
            orbit.orbit_id: {"Q_D": orbit.Q_D, "P_D": orbit.P_D}
            for orbit in canonical_stage12a_orbits()
        },
        "gauge_flow_type": STAGE12A_GAUGE_FLOW_TYPE,
        "external_reparameterization_type": STAGE12A_EXTERNAL_REPARAM_TYPE,
        "gauge_parameters": canonical_stage12a_gauge_parameters(),
        "representatives_per_orbit": diagnostics.representatives_per_orbit,
        "representative_count": diagnostics.representative_count,
        "gauge_transport_count": diagnostics.gauge_transport_count,
        "external_parameterizations_per_orbit": len(STAGE11A_POSITIVE_PARAMETERIZATION_IDS),
        "external_parameterization_view_count": diagnostics.external_parameterization_view_count,
        "external_parameterized_event_count": diagnostics.external_parameterized_event_count,
        "max_constraint_residual": diagnostics.max_constraint_residual,
        "max_gauge_transport_residual": diagnostics.max_gauge_transport_residual,
        "max_gauge_Q_D_drift": diagnostics.max_gauge_Q_D_drift,
        "max_gauge_P_D_drift": diagnostics.max_gauge_P_D_drift,
        "max_external_lapse_chain_rule_residual": diagnostics.max_external_lapse_chain_rule_residual,
        "minimum_external_positive_lapse": diagnostics.minimum_external_positive_lapse,
        "typed_provenance_explicit": diagnostics.typed_provenance_explicit,
        "guards": (
            "constraint-generated gauge flow != ontological becoming",
            "different physical orbit != later event on one orbit",
            "constraint-generated gauge flow != external reparameterization by definition",
            "multi-orbit constrained carrier != general covariance",
        ),
    }
