"""Stage 12E internal-clock x reparameterization x gauge-flow compatibility.

Three transformations remain separately typed throughout:

* C: genuine continuation-aware Stage 10/11 internal-clock transport;
* G: Stage 11 external reparameterization transport;
* Phi: Stage 12 constraint-generated same-physical-orbit gauge transport.

Stage 11E already established C x G compatibility on the frozen positive
parameterization/clock family. Stage 12E fibers those operational endpoints over
the Stage 12 physical-orbit/gauge atlas and checks C x Phi, G x Phi, and a
three-way spanning C x G x Phi family. Relational outputs come from orbit-
specific Stage 12A external views, future-measurement probabilities from Stage
11E, and the Stage 12D orbit-sensitive witness remains attached as a physical-
orbit discriminator.

This finite compatibility result is not general covariance, diffeomorphism
invariance, general relativity, eternalism, or a claim about ontological
becoming.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from functools import lru_cache
from itertools import permutations

from .stage11_compatibility import (
    canonical_stage11e_clock_transports,
    canonical_stage11e_reparameterization_transports,
    stage11e_measurement_view,
)
from .stage11_measurement import STAGE11D_REFERENCE_CLOCK, STAGE11D_REFERENCE_CLOCK_INDEX
from .stage11_parametrized import STAGE11A_IDENTITY, STAGE11A_POSITIVE_PARAMETERIZATION_IDS
from .stage11_relational import STAGE11B_ANCHOR_INDEX, STAGE11B_TARGET_INDEX
from .stage12_gauge_atlas import canonical_stage12c_quotient_classes
from .stage12_measurement import canonical_stage12d_orbit_witnesses
from .stage12_multi_orbit import (
    STAGE12A_ATOL,
    Stage12GaugeRepresentative,
    canonical_stage12a_external_views,
    canonical_stage12a_gauge_transports,
    canonical_stage12a_orbits,
    canonical_stage12a_representatives,
)

STAGE12E_CLOCK_TYPE = "internal_clock_transport"
STAGE12E_REPARAMETERIZATION_TYPE = "external_reparameterization_transport"
STAGE12E_GAUGE_TYPE = "constraint_generated_gauge_transport"
STAGE12E_PATH_REJECTION = "mixed_or_untyped_path_rejected"
STAGE12E_RESULT = (
    "Stage 12E internal-clock x external-parameterization x gauge-flow compatibility "
    "on the frozen finite multi-orbit family = established"
)
STAGE12E_GUARD = "commuting finite gauge/clock diagrams != general covariance"


@dataclass(frozen=True, slots=True)
class Stage12EClockTransport:
    transform_type: str
    continuation_id: str
    source_clock: str
    source_index: int
    target_clock: str
    target_index: int
    valid: bool


@dataclass(frozen=True, slots=True)
class Stage12EReparameterizationTransport:
    transform_type: str
    source_parameterization_id: str
    target_parameterization_id: str
    valid: bool


@dataclass(frozen=True, slots=True)
class Stage12EGaugeTransport:
    transform_type: str
    orbit_id: str
    source_representative_id: str
    target_representative_id: str
    delta_s: float
    valid: bool


@dataclass(frozen=True, slots=True)
class Stage12EOperationalState:
    orbit_id: str
    quotient_id: str
    representative_id: str
    gauge_parameter_s: float
    parameterization_id: str
    internal_clock: str
    internal_clock_index: int
    continuation_id: str
    anchor_event_id: str
    target_event_id: str
    anchor_parameter_value: float
    target_parameter_value: float
    anchor_lapse: float
    target_lapse: float
    anchor_relational_T: float
    target_relational_T: float
    anchor_relational_q: float
    target_relational_q: float
    measurement_probabilities: tuple[tuple[str, float], ...]
    orbit_witness_probabilities: tuple[tuple[str, float], ...]


@dataclass(frozen=True, slots=True)
class Stage12EPathFamilyDiagnostics:
    family_id: str
    object_count: int
    path_evaluation_count: int
    max_relational_residual: float
    max_measurement_residual: float
    max_orbit_witness_residual: float
    max_total_residual: float
    compatible: bool


@dataclass(frozen=True, slots=True)
class Stage12EControl:
    control_id: str
    classification: str
    rejected: bool
    reason: str


@dataclass(frozen=True, slots=True)
class Stage12EDiagnostics:
    physical_orbit_count: int
    representative_count: int
    clock_transport_count: int
    reparameterization_transport_count: int
    gauge_transport_count: int
    distinct_transform_type_count: int
    clock_gauge_square_count: int
    reparameterization_gauge_square_count: int
    triple_spanning_gauge_count: int
    triple_cube_count: int
    triple_path_evaluation_count: int
    max_clock_gauge_residual: float
    max_reparameterization_gauge_residual: float
    max_triple_residual: float
    orbit_sensitive_signature_count: int
    control_count: int
    rejected_control_count: int
    criteria_39_43_satisfied: bool


@lru_cache(maxsize=1)
def _representative_lookup() -> dict[str, Stage12GaugeRepresentative]:
    return {item.representative_id: item for item in canonical_stage12a_representatives()}


@lru_cache(maxsize=1)
def _quotient_lookup() -> dict[str, str]:
    result: dict[str, str] = {}
    for quotient in canonical_stage12c_quotient_classes():
        if len(quotient.inferred_orbit_ids) != 1:
            raise ValueError("Stage 12E quotient class mixes physical orbits")
        for representative_id in quotient.representative_ids:
            result[representative_id] = quotient.quotient_id
    if set(result) != set(_representative_lookup()):
        raise ValueError("Stage 12E quotient lookup does not cover all representatives")
    return result


@lru_cache(maxsize=1)
def _external_view_lookup():
    return {
        (item.orbit_id, item.parameterization_id): item
        for item in canonical_stage12a_external_views()
    }


@lru_cache(maxsize=1)
def _witness_lookup():
    return {
        item.representative_id: item
        for item in canonical_stage12d_orbit_witnesses()
    }


@lru_cache(maxsize=1)
def canonical_stage12e_clock_transports() -> tuple[Stage12EClockTransport, ...]:
    return tuple(
        Stage12EClockTransport(
            STAGE12E_CLOCK_TYPE,
            item.continuation_id,
            item.source_clock,
            item.source_index,
            item.target_clock,
            item.target_index,
            bool(item.valid),
        )
        for item in canonical_stage11e_clock_transports()
    )


@lru_cache(maxsize=1)
def canonical_stage12e_reparameterization_transports() -> tuple[
    Stage12EReparameterizationTransport, ...
]:
    return tuple(
        Stage12EReparameterizationTransport(
            STAGE12E_REPARAMETERIZATION_TYPE,
            item.source_parameterization_id,
            item.target_parameterization_id,
            bool(item.valid),
        )
        for item in canonical_stage11e_reparameterization_transports()
    )


@lru_cache(maxsize=1)
def canonical_stage12e_gauge_transports() -> tuple[Stage12EGaugeTransport, ...]:
    return tuple(
        Stage12EGaugeTransport(
            STAGE12E_GAUGE_TYPE,
            item.orbit_id,
            item.source_representative_id,
            item.target_representative_id,
            float(item.delta_s),
            bool(
                item.phase_space_residual <= STAGE12A_ATOL
                and item.Q_D_drift <= STAGE12A_ATOL
                and item.P_D_drift <= STAGE12A_ATOL
                and item.max_constraint_residual <= STAGE12A_ATOL
            ),
        )
        for item in canonical_stage12a_gauge_transports()
    )


@lru_cache(maxsize=1)
def canonical_stage12e_triple_spanning_gauge_transports() -> tuple[
    Stage12EGaugeTransport, ...
]:
    """Choose one maximally nontrivial Phi edge per physical orbit.

    Pairwise C x Phi and G x Phi diagnostics already use all 80 nonidentity
    arrows.  The three-way cube therefore needs only an orbit-spanning Phi
    family to test interaction rather than redundantly repeating each cube 20x.
    """

    result = []
    for orbit in canonical_stage12a_orbits():
        candidates = [
            item
            for item in canonical_stage12e_gauge_transports()
            if item.orbit_id == orbit.orbit_id
        ]
        result.append(max(candidates, key=lambda item: abs(item.delta_s)))
    return tuple(result)


@lru_cache(maxsize=1)
def _clock_transport_lookup() -> dict[
    tuple[str, str, int, str, int], Stage12EClockTransport
]:
    return {
        (
            item.continuation_id,
            item.source_clock,
            item.source_index,
            item.target_clock,
            item.target_index,
        ): item
        for item in canonical_stage12e_clock_transports()
    }


@lru_cache(maxsize=1)
def _reparameterization_transport_lookup() -> dict[
    tuple[str, str], Stage12EReparameterizationTransport
]:
    return {
        (item.source_parameterization_id, item.target_parameterization_id): item
        for item in canonical_stage12e_reparameterization_transports()
    }


@lru_cache(maxsize=1)
def _gauge_transport_lookup() -> dict[tuple[str, str], Stage12EGaugeTransport]:
    return {
        (item.source_representative_id, item.target_representative_id): item
        for item in canonical_stage12e_gauge_transports()
    }


@lru_cache(maxsize=None)
def stage12e_state(
    representative_id: str,
    parameterization_id: str,
    internal_clock: str,
    internal_clock_index: int,
    continuation_id: str,
) -> Stage12EOperationalState:
    representative = _representative_lookup().get(representative_id)
    if representative is None:
        raise ValueError(f"unknown Stage 12E representative {representative_id!r}")
    if parameterization_id not in STAGE11A_POSITIVE_PARAMETERIZATION_IDS:
        raise ValueError(f"unknown Stage 12E positive parameterization {parameterization_id!r}")
    external = _external_view_lookup().get((representative.orbit_id, parameterization_id))
    if external is None:
        raise ValueError("Stage 12E external parameterization view is missing")
    measurement = stage11e_measurement_view(
        parameterization_id,
        continuation_id,
        internal_clock,
        internal_clock_index,
    )
    witness = _witness_lookup()[representative_id]
    a = STAGE11B_ANCHOR_INDEX
    t = STAGE11B_TARGET_INDEX
    return Stage12EOperationalState(
        orbit_id=representative.orbit_id,
        quotient_id=_quotient_lookup()[representative_id],
        representative_id=representative_id,
        gauge_parameter_s=float(representative.gauge_parameter_s),
        parameterization_id=parameterization_id,
        internal_clock=internal_clock,
        internal_clock_index=int(internal_clock_index),
        continuation_id=continuation_id,
        anchor_event_id=f"{representative.orbit_id}:relational:e1",
        target_event_id=f"{representative.orbit_id}:relational:e2",
        anchor_parameter_value=float(external.parameter_labels[a]),
        target_parameter_value=float(external.parameter_labels[t]),
        anchor_lapse=float(external.lapse_values[a]),
        target_lapse=float(external.lapse_values[t]),
        anchor_relational_T=float(external.clock_values[a]),
        target_relational_T=float(external.clock_values[t]),
        anchor_relational_q=float(external.q_values[a]),
        target_relational_q=float(external.q_values[t]),
        measurement_probabilities=tuple(measurement.probabilities),
        orbit_witness_probabilities=tuple(witness.probabilities),
    )


def stage12e_apply_clock(
    state: Stage12EOperationalState,
    transport: Stage12EClockTransport,
) -> Stage12EOperationalState:
    if transport.transform_type != STAGE12E_CLOCK_TYPE or not transport.valid:
        raise ValueError("Stage 12E requires a valid typed C transport")
    expected = _clock_transport_lookup().get(
        (
            state.continuation_id,
            state.internal_clock,
            state.internal_clock_index,
            transport.target_clock,
            transport.target_index,
        )
    )
    if expected != transport:
        raise ValueError("Stage 12E C transport does not match the state source")
    return stage12e_state(
        state.representative_id,
        state.parameterization_id,
        transport.target_clock,
        transport.target_index,
        state.continuation_id,
    )


def stage12e_apply_reparameterization(
    state: Stage12EOperationalState,
    transport: Stage12EReparameterizationTransport,
) -> Stage12EOperationalState:
    if transport.transform_type != STAGE12E_REPARAMETERIZATION_TYPE or not transport.valid:
        raise ValueError("Stage 12E requires a valid typed G transport")
    expected = _reparameterization_transport_lookup().get(
        (state.parameterization_id, transport.target_parameterization_id)
    )
    if expected != transport:
        raise ValueError("Stage 12E G transport does not match the state source")
    return stage12e_state(
        state.representative_id,
        transport.target_parameterization_id,
        state.internal_clock,
        state.internal_clock_index,
        state.continuation_id,
    )


def stage12e_apply_gauge(
    state: Stage12EOperationalState,
    transport: Stage12EGaugeTransport,
) -> Stage12EOperationalState:
    if transport.transform_type != STAGE12E_GAUGE_TYPE or not transport.valid:
        raise ValueError("Stage 12E requires a valid typed Phi transport")
    expected = _gauge_transport_lookup().get(
        (state.representative_id, transport.target_representative_id)
    )
    if expected != transport:
        raise ValueError("Stage 12E Phi transport does not match the state source")
    target = _representative_lookup().get(transport.target_representative_id)
    if target is None or target.orbit_id != state.orbit_id or transport.orbit_id != state.orbit_id:
        raise ValueError("Stage 12E Phi transport cannot cross physical orbits")
    return stage12e_state(
        target.representative_id,
        state.parameterization_id,
        state.internal_clock,
        state.internal_clock_index,
        state.continuation_id,
    )


def _probability_residual(
    left: tuple[tuple[str, float], ...],
    right: tuple[tuple[str, float], ...],
) -> float:
    lhs = dict(left)
    rhs = dict(right)
    if set(lhs) != set(rhs):
        return float("inf")
    return max((abs(lhs[key] - rhs[key]) for key in lhs), default=0.0)


def _state_residuals(
    left: Stage12EOperationalState,
    right: Stage12EOperationalState,
) -> tuple[float, float, float, float]:
    if (
        left.orbit_id != right.orbit_id
        or left.quotient_id != right.quotient_id
        or left.representative_id != right.representative_id
        or left.parameterization_id != right.parameterization_id
        or left.internal_clock != right.internal_clock
        or left.internal_clock_index != right.internal_clock_index
        or left.continuation_id != right.continuation_id
        or left.anchor_event_id != right.anchor_event_id
        or left.target_event_id != right.target_event_id
    ):
        return float("inf"), float("inf"), float("inf"), float("inf")
    relational = max(
        abs(left.gauge_parameter_s - right.gauge_parameter_s),
        abs(left.anchor_parameter_value - right.anchor_parameter_value),
        abs(left.target_parameter_value - right.target_parameter_value),
        abs(left.anchor_lapse - right.anchor_lapse),
        abs(left.target_lapse - right.target_lapse),
        abs(left.anchor_relational_T - right.anchor_relational_T),
        abs(left.target_relational_T - right.target_relational_T),
        abs(left.anchor_relational_q - right.anchor_relational_q),
        abs(left.target_relational_q - right.target_relational_q),
    )
    measurement = _probability_residual(
        left.measurement_probabilities, right.measurement_probabilities
    )
    witness = _probability_residual(
        left.orbit_witness_probabilities, right.orbit_witness_probabilities
    )
    return relational, measurement, witness, max(relational, measurement, witness)


def _family_result(
    family_id: str,
    count: int,
    path_count: int,
    max_relational: float,
    max_measurement: float,
    max_witness: float,
) -> Stage12EPathFamilyDiagnostics:
    total = max(max_relational, max_measurement, max_witness)
    return Stage12EPathFamilyDiagnostics(
        family_id,
        count,
        path_count,
        float(max_relational),
        float(max_measurement),
        float(max_witness),
        float(total),
        bool(total <= STAGE12A_ATOL),
    )


@lru_cache(maxsize=1)
def stage12e_clock_gauge_diagnostics() -> Stage12EPathFamilyDiagnostics:
    mr = mm = mw = 0.0
    count = 0
    for phi in canonical_stage12e_gauge_transports():
        for clock in canonical_stage12e_clock_transports():
            start = stage12e_state(
                phi.source_representative_id,
                STAGE11A_IDENTITY,
                clock.source_clock,
                clock.source_index,
                clock.continuation_id,
            )
            candidates = (
                stage12e_apply_gauge(stage12e_apply_clock(start, clock), phi),
                stage12e_apply_clock(stage12e_apply_gauge(start, phi), clock),
            )
            direct = stage12e_state(
                phi.target_representative_id,
                STAGE11A_IDENTITY,
                clock.target_clock,
                clock.target_index,
                clock.continuation_id,
            )
            for candidate in candidates:
                r, m, w, _ = _state_residuals(candidate, direct)
                mr, mm, mw = max(mr, r), max(mm, m), max(mw, w)
            count += 1
    return _family_result("C_x_Phi", count, 2 * count, mr, mm, mw)


@lru_cache(maxsize=1)
def stage12e_reparameterization_gauge_diagnostics() -> Stage12EPathFamilyDiagnostics:
    continuation_ids = tuple(
        sorted({item.continuation_id for item in canonical_stage12e_clock_transports()})
    )
    mr = mm = mw = 0.0
    count = 0
    for phi in canonical_stage12e_gauge_transports():
        for reparam in canonical_stage12e_reparameterization_transports():
            for continuation_id in continuation_ids:
                start = stage12e_state(
                    phi.source_representative_id,
                    reparam.source_parameterization_id,
                    STAGE11D_REFERENCE_CLOCK,
                    STAGE11D_REFERENCE_CLOCK_INDEX,
                    continuation_id,
                )
                candidates = (
                    stage12e_apply_gauge(
                        stage12e_apply_reparameterization(start, reparam), phi
                    ),
                    stage12e_apply_reparameterization(
                        stage12e_apply_gauge(start, phi), reparam
                    ),
                )
                direct = stage12e_state(
                    phi.target_representative_id,
                    reparam.target_parameterization_id,
                    STAGE11D_REFERENCE_CLOCK,
                    STAGE11D_REFERENCE_CLOCK_INDEX,
                    continuation_id,
                )
                for candidate in candidates:
                    r, m, w, _ = _state_residuals(candidate, direct)
                    mr, mm, mw = max(mr, r), max(mm, m), max(mw, w)
                count += 1
    return _family_result("G_x_Phi", count, 2 * count, mr, mm, mw)


def _apply_order(
    start: Stage12EOperationalState,
    order: tuple[str, ...],
    clock: Stage12EClockTransport,
    reparam: Stage12EReparameterizationTransport,
    phi: Stage12EGaugeTransport,
) -> Stage12EOperationalState:
    result = start
    for label in order:
        if label == "C":
            result = stage12e_apply_clock(result, clock)
        elif label == "G":
            result = stage12e_apply_reparameterization(result, reparam)
        elif label == "Phi":
            result = stage12e_apply_gauge(result, phi)
        else:
            raise ValueError(f"unknown Stage 12E path label {label!r}")
    return result


@lru_cache(maxsize=1)
def stage12e_triple_diagnostics() -> Stage12EPathFamilyDiagnostics:
    orders = tuple(permutations(("C", "G", "Phi"), 3))
    mr = mm = mw = 0.0
    count = 0
    for phi in canonical_stage12e_triple_spanning_gauge_transports():
        for reparam in canonical_stage12e_reparameterization_transports():
            for clock in canonical_stage12e_clock_transports():
                start = stage12e_state(
                    phi.source_representative_id,
                    reparam.source_parameterization_id,
                    clock.source_clock,
                    clock.source_index,
                    clock.continuation_id,
                )
                direct = stage12e_state(
                    phi.target_representative_id,
                    reparam.target_parameterization_id,
                    clock.target_clock,
                    clock.target_index,
                    clock.continuation_id,
                )
                for order in orders:
                    candidate = _apply_order(start, order, clock, reparam, phi)
                    r, m, w, _ = _state_residuals(candidate, direct)
                    mr, mm, mw = max(mr, r), max(mm, m), max(mw, w)
                count += 1
    return _family_result(
        "C_x_G_x_Phi_spanning", count, len(orders) * count, mr, mm, mw
    )


@lru_cache(maxsize=1)
def stage12e_controls() -> tuple[Stage12EControl, ...]:
    representatives = canonical_stage12a_representatives()
    alpha = next(item for item in representatives if item.orbit_id == "omega_alpha")
    beta = next(item for item in representatives if item.orbit_id == "omega_beta")
    base_clock = canonical_stage12e_clock_transports()[0]
    base_g = canonical_stage12e_reparameterization_transports()[0]
    base_phi = next(
        item
        for item in canonical_stage12e_gauge_transports()
        if item.source_representative_id == alpha.representative_id
    )
    start = stage12e_state(
        alpha.representative_id,
        base_g.source_parameterization_id,
        base_clock.source_clock,
        base_clock.source_index,
        base_clock.continuation_id,
    )
    controls = (
        (
            "mixed_orbit_phi",
            "phi",
            replace(base_phi, target_representative_id=beta.representative_id),
            "Phi endpoint forced onto a distinct physical orbit",
        ),
        (
            "clock_label_as_parameterization",
            "g",
            replace(base_g, target_parameterization_id=base_clock.target_clock),
            "internal-clock label inserted into external-parameterization slot",
        ),
        (
            "parameterization_label_as_clock",
            "c",
            replace(base_clock, target_clock=base_g.target_parameterization_id),
            "external-parameterization label inserted into internal-clock slot",
        ),
        (
            "gauge_type_relabelled_as_reparameterization",
            "phi",
            replace(base_phi, transform_type=STAGE12E_REPARAMETERIZATION_TYPE),
            "Phi transport relabelled with the G transform type",
        ),
    )
    result = []
    for control_id, kind, transport, reason in controls:
        rejected = False
        try:
            if kind == "phi":
                stage12e_apply_gauge(start, transport)  # type: ignore[arg-type]
            elif kind == "g":
                stage12e_apply_reparameterization(start, transport)  # type: ignore[arg-type]
            else:
                stage12e_apply_clock(start, transport)  # type: ignore[arg-type]
        except (ValueError, TypeError):
            rejected = True
        result.append(
            Stage12EControl(
                control_id,
                STAGE12E_PATH_REJECTION if rejected else "inconclusive",
                rejected,
                reason,
            )
        )
    return tuple(result)


@lru_cache(maxsize=1)
def stage12e_diagnostics() -> Stage12EDiagnostics:
    clocks = canonical_stage12e_clock_transports()
    reparams = canonical_stage12e_reparameterization_transports()
    gauges = canonical_stage12e_gauge_transports()
    spanning = canonical_stage12e_triple_spanning_gauge_transports()
    c_phi = stage12e_clock_gauge_diagnostics()
    g_phi = stage12e_reparameterization_gauge_diagnostics()
    triple = stage12e_triple_diagnostics()
    controls = stage12e_controls()
    transform_types = {
        *(item.transform_type for item in clocks),
        *(item.transform_type for item in reparams),
        *(item.transform_type for item in gauges),
    }
    witness_signatures = {
        tuple(item.probabilities) for item in canonical_stage12d_orbit_witnesses()
    }
    criteria = bool(
        len(canonical_stage12a_orbits()) == 4
        and len(canonical_stage12a_representatives()) == 20
        and len(clocks) == 108
        and len(reparams) == 12
        and len(gauges) == 80
        and len(transform_types) == 3
        and all(item.valid for item in clocks)
        and all(item.valid for item in reparams)
        and all(item.valid for item in gauges)
        and c_phi.object_count == 8640
        and c_phi.compatible
        and g_phi.object_count == 1920
        and g_phi.compatible
        and len(spanning) == 4
        and {item.orbit_id for item in spanning}
        == {item.orbit_id for item in canonical_stage12a_orbits()}
        and triple.object_count == 5184
        and triple.path_evaluation_count == 31104
        and triple.compatible
        and len(witness_signatures) == 4
        and len(controls) == 4
        and all(item.rejected for item in controls)
    )
    return Stage12EDiagnostics(
        physical_orbit_count=4,
        representative_count=20,
        clock_transport_count=len(clocks),
        reparameterization_transport_count=len(reparams),
        gauge_transport_count=len(gauges),
        distinct_transform_type_count=len(transform_types),
        clock_gauge_square_count=c_phi.object_count,
        reparameterization_gauge_square_count=g_phi.object_count,
        triple_spanning_gauge_count=len(spanning),
        triple_cube_count=triple.object_count,
        triple_path_evaluation_count=triple.path_evaluation_count,
        max_clock_gauge_residual=c_phi.max_total_residual,
        max_reparameterization_gauge_residual=g_phi.max_total_residual,
        max_triple_residual=triple.max_total_residual,
        orbit_sensitive_signature_count=len(witness_signatures),
        control_count=len(controls),
        rejected_control_count=sum(item.rejected for item in controls),
        criteria_39_43_satisfied=criteria,
    )


def stage12e_summary() -> dict[str, object]:
    d = stage12e_diagnostics()
    return {
        "stage": "12E",
        "clock_transport_count": d.clock_transport_count,
        "reparameterization_transport_count": d.reparameterization_transport_count,
        "gauge_transport_count": d.gauge_transport_count,
        "distinct_transform_type_count": d.distinct_transform_type_count,
        "clock_gauge_square_count": d.clock_gauge_square_count,
        "reparameterization_gauge_square_count": d.reparameterization_gauge_square_count,
        "triple_spanning_gauge_count": d.triple_spanning_gauge_count,
        "triple_cube_count": d.triple_cube_count,
        "triple_path_evaluation_count": d.triple_path_evaluation_count,
        "max_clock_gauge_residual": d.max_clock_gauge_residual,
        "max_reparameterization_gauge_residual": d.max_reparameterization_gauge_residual,
        "max_triple_residual": d.max_triple_residual,
        "orbit_sensitive_signature_count": d.orbit_sensitive_signature_count,
        "control_count": d.control_count,
        "rejected_control_count": d.rejected_control_count,
        "criteria_39_43_satisfied": d.criteria_39_43_satisfied,
        "bounded_result": STAGE12E_RESULT if d.criteria_39_43_satisfied else "not_established",
        "guards": (
            STAGE12E_GUARD,
            "internal-clock covariance != external-reparameterization covariance",
            "constraint-generated gauge flow != internal-clock change",
            "constraint-generated gauge flow != external reparameterization",
            "path-independent future probabilities != future actuality",
            "path-independent relational outputs != ontological becoming",
            "finite three-way compatibility != diffeomorphism invariance",
        ),
    }
