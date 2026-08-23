"""Stage 12C typed gauge atlas, quotient, and relational descent.

Stage 12C turns the Stage 12A sampled representatives into an explicit finite
typed gauge groupoid.  The groupoid contains only same-physical-orbit
constraint-generated transports.  Its quotient is built from gauge-arrow
connectivity rather than from predeclared orbit labels, then checked against
the four canonical physical-orbit controls supplied by Stage 12A/B.

The construction is deliberately finite and typed.  It is not a claim of
full diffeomorphism invariance, refoliation invariance, or general covariance.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from itertools import product

import numpy as np

from .stage12_multi_orbit import (
    STAGE12A_ATOL,
    STAGE12A_EXTERNAL_REPARAM_TYPE,
    STAGE12A_GAUGE_FLOW_TYPE,
    Stage12GaugeRepresentative,
    canonical_stage12a_external_views,
    canonical_stage12a_orbits,
    canonical_stage12a_representatives,
    canonical_stage12a_representatives_for_orbit,
)
from .stage12_relational import (
    STAGE12B_TAU_VALUES,
    stage12b_dirac_from_representative,
)

STAGE12C_ATOL = STAGE12A_ATOL

STAGE12C_NODE_PHYSICAL_ORBIT = "physical_orbit"
STAGE12C_NODE_GAUGE_REPRESENTATIVE = "gauge_representative"
STAGE12C_NODE_EXTERNAL_PARAMETERIZATION = "external_parameterization"
STAGE12C_NODE_RELATIONAL_EVENT = "relational_event"
STAGE12C_NODE_INTERNAL_CLOCK = "internal_clock"
STAGE12C_NODE_MODAL_CONTINUATION = "modal_continuation"

STAGE12C_TYPED_STATUS_LOST = "lost"
STAGE12C_NUMERICAL_STATUS_RECONSTRUCTIBLE = "reconstructible"
STAGE12C_NUMERICALLY_REFUTED = "numerically_refuted"
STAGE12C_FALSE_POSITIVE_REJECTED = "false_positive_rejected"

STAGE12C_MODAL_CONTINUATIONS = ("h_L", "h_R")


@dataclass(frozen=True, slots=True)
class Stage12CTypedNode:
    node_id: str
    node_type: str
    orbit_id: str | None
    role: str
    provenance: str


@dataclass(frozen=True, slots=True)
class Stage12CGaugeArrow:
    arrow_id: str
    transform_type: str
    orbit_id: str
    source_representative_id: str
    target_representative_id: str
    delta_s: float
    is_identity: bool
    phase_space_residual: float
    Q_D_drift: float
    P_D_drift: float
    max_constraint_residual: float
    provenance: str


@dataclass(frozen=True, slots=True)
class Stage12CInverseCheck:
    arrow_id: str
    inverse_arrow_id: str
    orbit_id: str
    delta_sum_residual: float
    endpoint_residual: float
    invariant_residual: float
    passed: bool


@dataclass(frozen=True, slots=True)
class Stage12CCompositionCheck:
    orbit_id: str
    source_representative_id: str
    middle_representative_id: str
    target_representative_id: str
    delta_composition_residual: float
    direct_transport_residual: float
    invariant_residual: float
    passed: bool


@dataclass(frozen=True, slots=True)
class Stage12CQuotientClass:
    quotient_id: str
    representative_ids: tuple[str, ...]
    inferred_orbit_ids: tuple[str, ...]
    Q_D: float
    P_D: float
    max_Q_D_spread: float
    max_P_D_spread: float
    provenance: str


@dataclass(frozen=True, slots=True)
class Stage12CDescentEvaluation:
    quotient_id: str
    inferred_orbit_id: str
    tau: float
    Q_D: float
    P_D: float
    relational_q: float
    relational_dq_dT: float
    max_Q_D_spread: float
    max_P_D_spread: float
    max_relational_q_spread: float
    max_relational_dq_dT_spread: float


@dataclass(frozen=True, slots=True)
class Stage12COrbitIdentityAblation:
    resource: str
    typed_status: str
    numerical_status: str
    reconstructed_class_count: int
    reconstructed_class_sizes: tuple[int, ...]
    provenance: str


@dataclass(frozen=True, slots=True)
class Stage12CWrongInvariantControl:
    control_id: str
    corrupted_field: str
    Q_D_drift: float
    P_D_drift: float
    phase_space_residual: float
    constraint_residual: float
    classification: str


@dataclass(frozen=True, slots=True)
class Stage12CModalSeparationControl:
    quotient_ids: tuple[str, ...]
    continuation_node_ids: tuple[str, ...]
    gauge_arrow_touches_continuation: bool
    quotient_identifies_continuation: bool
    classification: str


@dataclass(frozen=True, slots=True)
class Stage12CDiagnostics:
    typed_node_count: int
    node_types: tuple[str, ...]
    gauge_arrow_count: int
    identity_arrow_count: int
    inverse_check_count: int
    composition_check_count: int
    quotient_class_count: int
    quotient_member_count: int
    quotient_class_sizes: tuple[int, ...]
    descent_evaluation_count: int
    max_gauge_phase_space_residual: float
    max_gauge_Q_D_drift: float
    max_gauge_P_D_drift: float
    max_inverse_residual: float
    max_composition_residual: float
    max_descent_Q_D_spread: float
    max_descent_P_D_spread: float
    max_descent_q_spread: float
    max_descent_dq_dT_spread: float
    cross_orbit_gauge_arrow_count: int
    quotient_partition_exact: bool
    orbit_identity_ablation_typed_status: str
    orbit_identity_ablation_numerical_status: str
    wrong_invariant_controls_detected: int
    modal_continuation_separated: bool
    criteria_24_31_satisfied: bool


def _representative_lookup() -> dict[str, Stage12GaugeRepresentative]:
    return {
        representative.representative_id: representative
        for representative in canonical_stage12a_representatives()
    }


def canonical_stage12c_typed_nodes() -> tuple[Stage12CTypedNode, ...]:
    """Return typed orbit/representative/parameterization/event/clock/modal nodes."""

    nodes: dict[str, Stage12CTypedNode] = {}

    for orbit in canonical_stage12a_orbits():
        nodes[f"orbit::{orbit.orbit_id}"] = Stage12CTypedNode(
            node_id=f"orbit::{orbit.orbit_id}",
            node_type=STAGE12C_NODE_PHYSICAL_ORBIT,
            orbit_id=orbit.orbit_id,
            role="physical-orbit identity",
            provenance="Stage 12 frozen canonical orbit",
        )
        nodes[f"clock::{orbit.orbit_id}::T"] = Stage12CTypedNode(
            node_id=f"clock::{orbit.orbit_id}::T",
            node_type=STAGE12C_NODE_INTERNAL_CLOCK,
            orbit_id=orbit.orbit_id,
            role="internal relational clock T",
            provenance="clock role remains distinct from gauge parameter s and external lambda",
        )

    for representative in canonical_stage12a_representatives():
        nodes[f"representative::{representative.representative_id}"] = Stage12CTypedNode(
            node_id=f"representative::{representative.representative_id}",
            node_type=STAGE12C_NODE_GAUGE_REPRESENTATIVE,
            orbit_id=representative.orbit_id,
            role="constraint-generated gauge representative",
            provenance=representative.provenance,
        )
        nodes[f"event::{representative.event_id}"] = Stage12CTypedNode(
            node_id=f"event::{representative.event_id}",
            node_type=STAGE12C_NODE_RELATIONAL_EVENT,
            orbit_id=representative.orbit_id,
            role=representative.event_role,
            provenance="relational event attached to a sampled gauge representative",
        )

    for view in canonical_stage12a_external_views():
        parameter_node_id = f"parameterization::{view.orbit_id}::{view.parameterization_id}"
        nodes[parameter_node_id] = Stage12CTypedNode(
            node_id=parameter_node_id,
            node_type=STAGE12C_NODE_EXTERNAL_PARAMETERIZATION,
            orbit_id=view.orbit_id,
            role=STAGE12A_EXTERNAL_REPARAM_TYPE,
            provenance=view.provenance,
        )
        for event_id in view.event_ids:
            node_id = f"event::{event_id}"
            nodes.setdefault(
                node_id,
                Stage12CTypedNode(
                    node_id=node_id,
                    node_type=STAGE12C_NODE_RELATIONAL_EVENT,
                    orbit_id=view.orbit_id,
                    role="physical event under an external parameterization",
                    provenance="event identity shared across positive external parameterizations of one orbit",
                ),
            )

    for continuation in STAGE12C_MODAL_CONTINUATIONS:
        node_id = f"continuation::{continuation}"
        nodes[node_id] = Stage12CTypedNode(
            node_id=node_id,
            node_type=STAGE12C_NODE_MODAL_CONTINUATION,
            orbit_id=None,
            role="modal continuation",
            provenance="Stage 10/11 modal continuation role; not a constraint orbit",
        )

    return tuple(nodes[key] for key in sorted(nodes))


def stage12c_gauge_arrow(
    source: Stage12GaugeRepresentative,
    target: Stage12GaugeRepresentative,
) -> Stage12CGaugeArrow:
    """Construct one typed same-orbit gauge arrow, including identities."""

    if source.orbit_id != target.orbit_id:
        raise ValueError("Stage 12C licensed gauge arrows cannot connect distinct physical orbits")
    if source.gauge_flow_type != STAGE12A_GAUGE_FLOW_TYPE:
        raise ValueError("Stage 12C source lacks constraint-generated gauge-flow typing")
    if target.gauge_flow_type != STAGE12A_GAUGE_FLOW_TYPE:
        raise ValueError("Stage 12C target lacks constraint-generated gauge-flow typing")

    delta_s = float(target.gauge_parameter_s - source.gauge_parameter_s)
    predicted_T = float(source.T + delta_s)
    predicted_q = float(source.q + source.p * delta_s)
    phase_residual = max(
        abs(target.T - predicted_T),
        abs(target.q - predicted_q),
        abs(target.p - source.p),
        abs(target.p_T - source.p_T),
    )
    source_dirac = stage12b_dirac_from_representative(source)
    target_dirac = stage12b_dirac_from_representative(target)

    return Stage12CGaugeArrow(
        arrow_id=f"Phi::{source.representative_id}->{target.representative_id}",
        transform_type=STAGE12A_GAUGE_FLOW_TYPE,
        orbit_id=source.orbit_id,
        source_representative_id=source.representative_id,
        target_representative_id=target.representative_id,
        delta_s=delta_s,
        is_identity=source.representative_id == target.representative_id,
        phase_space_residual=float(phase_residual),
        Q_D_drift=float(abs(target_dirac.Q_D - source_dirac.Q_D)),
        P_D_drift=float(abs(target_dirac.P_D - source_dirac.P_D)),
        max_constraint_residual=float(
            max(source_dirac.constraint_residual, target_dirac.constraint_residual)
        ),
        provenance="typed finite Phi arrow generated within one declared constraint orbit",
    )


def canonical_stage12c_gauge_arrows() -> tuple[Stage12CGaugeArrow, ...]:
    """Return the complete finite same-orbit groupoid, including identities."""

    arrows: list[Stage12CGaugeArrow] = []
    for orbit in canonical_stage12a_orbits():
        representatives = canonical_stage12a_representatives_for_orbit(orbit)
        for source in representatives:
            for target in representatives:
                arrows.append(stage12c_gauge_arrow(source, target))
    return tuple(arrows)


def canonical_stage12c_inverse_checks() -> tuple[Stage12CInverseCheck, ...]:
    lookup = _representative_lookup()
    checks: list[Stage12CInverseCheck] = []
    for arrow in canonical_stage12c_gauge_arrows():
        source = lookup[arrow.source_representative_id]
        target = lookup[arrow.target_representative_id]
        inverse = stage12c_gauge_arrow(target, source)
        delta_residual = abs(arrow.delta_s + inverse.delta_s)
        endpoint_residual = max(
            abs(source.T - (target.T + inverse.delta_s)),
            abs(source.q - (target.q + target.p * inverse.delta_s)),
            abs(source.p - target.p),
            abs(source.p_T - target.p_T),
        )
        invariant_residual = max(
            arrow.Q_D_drift,
            arrow.P_D_drift,
            inverse.Q_D_drift,
            inverse.P_D_drift,
        )
        passed = max(delta_residual, endpoint_residual, invariant_residual) <= STAGE12C_ATOL
        checks.append(
            Stage12CInverseCheck(
                arrow_id=arrow.arrow_id,
                inverse_arrow_id=inverse.arrow_id,
                orbit_id=arrow.orbit_id,
                delta_sum_residual=float(delta_residual),
                endpoint_residual=float(endpoint_residual),
                invariant_residual=float(invariant_residual),
                passed=passed,
            )
        )
    return tuple(checks)


def canonical_stage12c_composition_checks() -> tuple[Stage12CCompositionCheck, ...]:
    checks: list[Stage12CCompositionCheck] = []
    for orbit in canonical_stage12a_orbits():
        representatives = canonical_stage12a_representatives_for_orbit(orbit)
        for source, middle, target in product(representatives, repeat=3):
            first = stage12c_gauge_arrow(source, middle)
            second = stage12c_gauge_arrow(middle, target)
            direct = stage12c_gauge_arrow(source, target)
            delta_residual = abs((first.delta_s + second.delta_s) - direct.delta_s)
            direct_residual = max(
                first.phase_space_residual,
                second.phase_space_residual,
                direct.phase_space_residual,
            )
            invariant_residual = max(
                first.Q_D_drift,
                first.P_D_drift,
                second.Q_D_drift,
                second.P_D_drift,
                direct.Q_D_drift,
                direct.P_D_drift,
            )
            passed = max(delta_residual, direct_residual, invariant_residual) <= STAGE12C_ATOL
            checks.append(
                Stage12CCompositionCheck(
                    orbit_id=orbit.orbit_id,
                    source_representative_id=source.representative_id,
                    middle_representative_id=middle.representative_id,
                    target_representative_id=target.representative_id,
                    delta_composition_residual=float(delta_residual),
                    direct_transport_residual=float(direct_residual),
                    invariant_residual=float(invariant_residual),
                    passed=passed,
                )
            )
    return tuple(checks)


def canonical_stage12c_quotient_classes() -> tuple[Stage12CQuotientClass, ...]:
    """Build connected components from gauge arrows without using orbit ids to union."""

    representatives = canonical_stage12a_representatives()
    lookup = {item.representative_id: item for item in representatives}
    adjacency: dict[str, set[str]] = {
        item.representative_id: set() for item in representatives
    }
    for arrow in canonical_stage12c_gauge_arrows():
        adjacency[arrow.source_representative_id].add(arrow.target_representative_id)
        adjacency[arrow.target_representative_id].add(arrow.source_representative_id)

    unseen = set(adjacency)
    components: list[tuple[str, ...]] = []
    while unseen:
        seed = min(unseen)
        stack = [seed]
        component: set[str] = set()
        while stack:
            current = stack.pop()
            if current in component:
                continue
            component.add(current)
            stack.extend(sorted(adjacency[current] - component))
        unseen -= component
        components.append(tuple(sorted(component)))

    result: list[Stage12CQuotientClass] = []
    for index, component in enumerate(sorted(components, key=lambda items: items[0])):
        estimates = [stage12b_dirac_from_representative(lookup[item]) for item in component]
        Q_values = np.asarray([item.Q_D for item in estimates], dtype=float)
        P_values = np.asarray([item.P_D for item in estimates], dtype=float)
        Q_D = float(np.mean(Q_values))
        P_D = float(np.mean(P_values))
        inferred_orbit_ids = tuple(sorted({lookup[item].orbit_id for item in component}))
        result.append(
            Stage12CQuotientClass(
                quotient_id=f"gauge_quotient_class_{index:02d}",
                representative_ids=component,
                inferred_orbit_ids=inferred_orbit_ids,
                Q_D=Q_D,
                P_D=P_D,
                max_Q_D_spread=float(np.max(np.abs(Q_values - Q_D))),
                max_P_D_spread=float(np.max(np.abs(P_values - P_D))),
                provenance="connected component of typed same-orbit Phi arrows",
            )
        )
    return tuple(result)


def canonical_stage12c_descent_evaluations() -> tuple[Stage12CDescentEvaluation, ...]:
    lookup = _representative_lookup()
    evaluations: list[Stage12CDescentEvaluation] = []
    for quotient in canonical_stage12c_quotient_classes():
        if len(quotient.inferred_orbit_ids) != 1:
            raise ValueError("Stage 12C quotient class mixes declared physical orbits")
        orbit_id = quotient.inferred_orbit_ids[0]
        estimates = [
            stage12b_dirac_from_representative(lookup[item])
            for item in quotient.representative_ids
        ]
        for tau in STAGE12B_TAU_VALUES:
            Q_values = np.asarray([item.Q_D for item in estimates], dtype=float)
            P_values = np.asarray([item.P_D for item in estimates], dtype=float)
            q_values = Q_values + P_values * float(tau)
            derivative_values = P_values.copy()
            evaluations.append(
                Stage12CDescentEvaluation(
                    quotient_id=quotient.quotient_id,
                    inferred_orbit_id=orbit_id,
                    tau=float(tau),
                    Q_D=float(np.mean(Q_values)),
                    P_D=float(np.mean(P_values)),
                    relational_q=float(np.mean(q_values)),
                    relational_dq_dT=float(np.mean(derivative_values)),
                    max_Q_D_spread=float(np.max(np.abs(Q_values - np.mean(Q_values)))),
                    max_P_D_spread=float(np.max(np.abs(P_values - np.mean(P_values)))),
                    max_relational_q_spread=float(np.max(np.abs(q_values - np.mean(q_values)))),
                    max_relational_dq_dT_spread=float(
                        np.max(np.abs(derivative_values - np.mean(derivative_values)))
                    ),
                )
            )
    return tuple(evaluations)


def stage12c_orbit_identity_ablation() -> Stage12COrbitIdentityAblation:
    """Remove typed orbit identity but reconstruct the finite partition numerically."""

    estimates = [
        stage12b_dirac_from_representative(item)
        for item in canonical_stage12a_representatives()
    ]
    numerical_groups: dict[tuple[float, float], list[str]] = {}
    for estimate in estimates:
        key = (round(estimate.Q_D, 12), round(estimate.P_D, 12))
        numerical_groups.setdefault(key, []).append(estimate.representative_id)

    sizes = tuple(sorted(len(items) for items in numerical_groups.values()))
    reconstructible = len(numerical_groups) == 4 and sizes == (5, 5, 5, 5)
    return Stage12COrbitIdentityAblation(
        resource="typed orbit identity/correspondence",
        typed_status=STAGE12C_TYPED_STATUS_LOST,
        numerical_status=(
            STAGE12C_NUMERICAL_STATUS_RECONSTRUCTIBLE if reconstructible else "not_established"
        ),
        reconstructed_class_count=len(numerical_groups),
        reconstructed_class_sizes=sizes,
        provenance=(
            "orbit labels removed by construction; full Dirac pair used only to test numerical reconstructibility"
        ),
    )


def canonical_stage12c_wrong_invariant_controls() -> tuple[Stage12CWrongInvariantControl, ...]:
    """Corrupt Q_D-sensitive and P_D-sensitive phase-space fields on purported paths."""

    orbit = canonical_stage12a_orbits()[0]
    source, target = canonical_stage12a_representatives_for_orbit(orbit)[:2]
    controls: list[Stage12CWrongInvariantControl] = []

    corrupted_Q_target = replace(target, q=float(target.q + 0.125))
    corrupted_P_target = replace(target, p=float(target.p + 0.125))

    for control_id, field, corrupted in (
        ("wrong_Q_D_path", "q", corrupted_Q_target),
        ("wrong_P_D_path", "p", corrupted_P_target),
    ):
        source_estimate = stage12b_dirac_from_representative(source)
        target_estimate = stage12b_dirac_from_representative(corrupted)
        delta_s = float(corrupted.gauge_parameter_s - source.gauge_parameter_s)
        phase_residual = max(
            abs(corrupted.T - (source.T + delta_s)),
            abs(corrupted.q - (source.q + source.p * delta_s)),
            abs(corrupted.p - source.p),
            abs(corrupted.p_T - source.p_T),
        )
        Q_drift = abs(target_estimate.Q_D - source_estimate.Q_D)
        P_drift = abs(target_estimate.P_D - source_estimate.P_D)
        detected = max(
            phase_residual,
            Q_drift,
            P_drift,
            target_estimate.constraint_residual,
        ) > STAGE12C_ATOL
        controls.append(
            Stage12CWrongInvariantControl(
                control_id=control_id,
                corrupted_field=field,
                Q_D_drift=float(Q_drift),
                P_D_drift=float(P_drift),
                phase_space_residual=float(phase_residual),
                constraint_residual=float(target_estimate.constraint_residual),
                classification=(STAGE12C_NUMERICALLY_REFUTED if detected else "inconclusive"),
            )
        )
    return tuple(controls)


def stage12c_modal_separation_control() -> Stage12CModalSeparationControl:
    quotient_ids = tuple(item.quotient_id for item in canonical_stage12c_quotient_classes())
    continuation_ids = tuple(
        f"continuation::{continuation}" for continuation in STAGE12C_MODAL_CONTINUATIONS
    )
    arrows = canonical_stage12c_gauge_arrows()
    touches_continuation = any(
        arrow.source_representative_id in continuation_ids
        or arrow.target_representative_id in continuation_ids
        for arrow in arrows
    )
    identifies_continuation = bool(set(quotient_ids) & set(continuation_ids))
    passed = not touches_continuation and not identifies_continuation
    return Stage12CModalSeparationControl(
        quotient_ids=quotient_ids,
        continuation_node_ids=continuation_ids,
        gauge_arrow_touches_continuation=touches_continuation,
        quotient_identifies_continuation=identifies_continuation,
        classification=(STAGE12C_FALSE_POSITIVE_REJECTED if passed else "inconclusive"),
    )


def stage12c_diagnostics() -> Stage12CDiagnostics:
    nodes = canonical_stage12c_typed_nodes()
    arrows = canonical_stage12c_gauge_arrows()
    inverse_checks = canonical_stage12c_inverse_checks()
    composition_checks = canonical_stage12c_composition_checks()
    quotient = canonical_stage12c_quotient_classes()
    descent = canonical_stage12c_descent_evaluations()
    ablation = stage12c_orbit_identity_ablation()
    wrong_controls = canonical_stage12c_wrong_invariant_controls()
    modal_control = stage12c_modal_separation_control()

    node_types = tuple(sorted({item.node_type for item in nodes}))
    required_types = {
        STAGE12C_NODE_PHYSICAL_ORBIT,
        STAGE12C_NODE_GAUGE_REPRESENTATIVE,
        STAGE12C_NODE_EXTERNAL_PARAMETERIZATION,
        STAGE12C_NODE_RELATIONAL_EVENT,
        STAGE12C_NODE_INTERNAL_CLOCK,
        STAGE12C_NODE_MODAL_CONTINUATION,
    }
    typed_nodes_complete = required_types.issubset(node_types)

    max_gauge_phase = max(item.phase_space_residual for item in arrows)
    max_gauge_Q = max(item.Q_D_drift for item in arrows)
    max_gauge_P = max(item.P_D_drift for item in arrows)
    max_inverse = max(
        max(item.delta_sum_residual, item.endpoint_residual, item.invariant_residual)
        for item in inverse_checks
    )
    max_composition = max(
        max(
            item.delta_composition_residual,
            item.direct_transport_residual,
            item.invariant_residual,
        )
        for item in composition_checks
    )

    cross_orbit_arrows = sum(
        _representative_lookup()[item.source_representative_id].orbit_id
        != _representative_lookup()[item.target_representative_id].orbit_id
        for item in arrows
    )

    class_sizes = tuple(sorted(len(item.representative_ids) for item in quotient))
    intended_orbits = {orbit.orbit_id for orbit in canonical_stage12a_orbits()}
    quotient_partition_exact = (
        len(quotient) == 4
        and class_sizes == (5, 5, 5, 5)
        and {item.inferred_orbit_ids[0] for item in quotient if len(item.inferred_orbit_ids) == 1}
        == intended_orbits
        and all(len(item.inferred_orbit_ids) == 1 for item in quotient)
    )

    max_descent_Q = max(item.max_Q_D_spread for item in descent)
    max_descent_P = max(item.max_P_D_spread for item in descent)
    max_descent_q = max(item.max_relational_q_spread for item in descent)
    max_descent_derivative = max(item.max_relational_dq_dT_spread for item in descent)
    descent_passed = max(
        max_descent_Q,
        max_descent_P,
        max_descent_q,
        max_descent_derivative,
    ) <= STAGE12C_ATOL

    wrong_detected = sum(
        item.classification == STAGE12C_NUMERICALLY_REFUTED for item in wrong_controls
    )
    groupoid_passed = (
        len(arrows) == 100
        and sum(item.is_identity for item in arrows) == 20
        and len(inverse_checks) == 100
        and all(item.passed for item in inverse_checks)
        and len(composition_checks) == 500
        and all(item.passed for item in composition_checks)
        and max(max_gauge_phase, max_gauge_Q, max_gauge_P, max_inverse, max_composition)
        <= STAGE12C_ATOL
    )
    ablation_passed = (
        ablation.typed_status == STAGE12C_TYPED_STATUS_LOST
        and ablation.numerical_status == STAGE12C_NUMERICAL_STATUS_RECONSTRUCTIBLE
    )
    modal_separated = modal_control.classification == STAGE12C_FALSE_POSITIVE_REJECTED

    criteria = (
        typed_nodes_complete
        and groupoid_passed
        and cross_orbit_arrows == 0
        and quotient_partition_exact
        and descent_passed
        and ablation_passed
        and wrong_detected == 2
        and modal_separated
    )

    return Stage12CDiagnostics(
        typed_node_count=len(nodes),
        node_types=node_types,
        gauge_arrow_count=len(arrows),
        identity_arrow_count=sum(item.is_identity for item in arrows),
        inverse_check_count=len(inverse_checks),
        composition_check_count=len(composition_checks),
        quotient_class_count=len(quotient),
        quotient_member_count=sum(len(item.representative_ids) for item in quotient),
        quotient_class_sizes=class_sizes,
        descent_evaluation_count=len(descent),
        max_gauge_phase_space_residual=float(max_gauge_phase),
        max_gauge_Q_D_drift=float(max_gauge_Q),
        max_gauge_P_D_drift=float(max_gauge_P),
        max_inverse_residual=float(max_inverse),
        max_composition_residual=float(max_composition),
        max_descent_Q_D_spread=float(max_descent_Q),
        max_descent_P_D_spread=float(max_descent_P),
        max_descent_q_spread=float(max_descent_q),
        max_descent_dq_dT_spread=float(max_descent_derivative),
        cross_orbit_gauge_arrow_count=int(cross_orbit_arrows),
        quotient_partition_exact=quotient_partition_exact,
        orbit_identity_ablation_typed_status=ablation.typed_status,
        orbit_identity_ablation_numerical_status=ablation.numerical_status,
        wrong_invariant_controls_detected=wrong_detected,
        modal_continuation_separated=modal_separated,
        criteria_24_31_satisfied=criteria,
    )


def stage12c_summary() -> dict[str, object]:
    diagnostics = stage12c_diagnostics()
    return {
        "status": (
            "Stage 12C completed; criteria 24–31 satisfied"
            if diagnostics.criteria_24_31_satisfied
            else "Stage 12C incomplete"
        ),
        "typed_node_count": diagnostics.typed_node_count,
        "node_types": diagnostics.node_types,
        "gauge_arrow_count": diagnostics.gauge_arrow_count,
        "identity_arrow_count": diagnostics.identity_arrow_count,
        "inverse_check_count": diagnostics.inverse_check_count,
        "composition_check_count": diagnostics.composition_check_count,
        "quotient_class_count": diagnostics.quotient_class_count,
        "quotient_class_sizes": diagnostics.quotient_class_sizes,
        "descent_evaluation_count": diagnostics.descent_evaluation_count,
        "cross_orbit_gauge_arrow_count": diagnostics.cross_orbit_gauge_arrow_count,
        "orbit_identity_ablation": {
            "typed_status": diagnostics.orbit_identity_ablation_typed_status,
            "numerical_status": diagnostics.orbit_identity_ablation_numerical_status,
        },
        "wrong_invariant_controls_detected": diagnostics.wrong_invariant_controls_detected,
        "modal_continuation_separated": diagnostics.modal_continuation_separated,
        "guards": (
            "gauge quotient != elimination of physical change",
            "constraint orbit != modal continuation",
            "operational quotient descent != modal/ontological identity",
            "finite gauge atlas != diffeomorphism invariance",
            "multi-orbit gauge covariance != general covariance",
        ),
    }
