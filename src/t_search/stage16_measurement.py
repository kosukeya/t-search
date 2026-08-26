"""Stage 16E typed O/P/R/V/Xi and future-measurement descent.

No new measurement law is introduced. Stage 16E carries the validated Stage
15E public/future-measurement family onto the Stage 16 four-site closed cycle,
replacing only the relational O-events by the Stage 16C complete four-clock
observable. Representative, cycle/support, path/compensator, basis/locality/
depth, and Stage 16D search provenance remain in Xi only.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
from functools import lru_cache
from math import tanh

from t_search.stage9_modal import FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_OTHER
from t_search.stage11_lift import Stage11OEvent, Stage11OLayer, Stage11PLayer, Stage11RLayer, Stage11VLayer
from t_search.stage11_parametrized import STAGE11A_IDENTITY
from t_search.stage15_measurement import Stage15EFuturePayload, canonical_stage15e_quotient_projections
from t_search.stage16_basis import (
    STAGE16D_CLASSIFICATION,
    STAGE16D_LFINITE_MAX_DEPTH,
    canonical_stage16d_candidates,
    canonical_stage16d_content_audits,
)
from t_search.stage16_local import (
    STAGE16A_ATOL,
    STAGE16A_BASIS_ID,
    STAGE16A_GENERATOR_SUPPORTS,
    STAGE16A_KAPPA,
    STAGE16A_SMEARING_PAIRS,
    Stage16PhaseSpacePoint,
    canonical_stage16a_orbits,
    canonical_stage16a_representatives,
    stage16a_closure_coordinate_support,
    stage16a_dirac_data,
)
from t_search.stage16_paths import (
    STAGE16B_PRESENTED_COMPENSATION_KIND,
    STAGE16B_SEED_COMPENSATION_KIND,
    STAGE16B_SMEARED_PARAMETER_PAIR,
    canonical_stage16b_local_probes,
    canonical_stage16b_smeared_probes,
    stage16b_apply_local_flow,
    stage16b_apply_smeared_flow,
    stage16b_apply_word,
    stage16b_local_raw_endpoints,
    stage16b_seed_compensate,
)
from t_search.stage16_relational import stage16c_complete_value

STAGE16E_ATOL = STAGE16A_ATOL
STAGE16E_LOCAL_PATH_DESCENT = "cycle_local_path_operational_payloads_descend"
STAGE16E_SMEARED_PATH_DESCENT = "cycle_smeared_path_operational_payloads_descend"
STAGE16E_BASIS_DESCENT = "cycle_basis_depth_operational_payloads_descend"
STAGE16E_NOT_LICENSED = "not_licensed"
STAGE16E_CLOCK_QUADRUPLES = (
    ("e1", (-1.0, -1.0, -1.0, -1.0)),
    ("e2", (1.0, 1.0, 1.0, 1.0)),
)
STAGE16E_CYCLE_ORIENTATION = (0, 1, 2, 3, 0)
STAGE16E_BOUNDED_RESULT = (
    "Stage 16E typed O/P/R/V/Xi and inherited future-measurement descent across "
    "the sampled four-site cycle quotient, licensed local/smeared paths, and "
    "all Stage 16D explicit equivalent basis candidates = established"
)
STAGE16E_GUARDS = (
    "cycle/representative/path/basis/depth Xi provenance != quotient-level physical content",
    "spatial index != ontological spatial substance",
    "cycle orientation != physical temporal history",
    "path word != physical temporal history",
    "path word != modal continuation",
    "compensated local/smeared operational descent != refoliation invariance",
    "basis-equivalent operational descent != refoliation invariance",
    "only nonlocal witness found in frozen search != fundamental physical non-Abelianity",
    "future-measurement covariance != future actuality",
    "path-independent evidence update != ontological becoming",
    "typed operational descent != ontological equivalence",
    "Potentiality != quantum randomness by definition",
    "orbit-sensitive witness != empirical prediction",
    "four-site constraint precursor != general relativity",
    "repository validation != new scientific evidence",
)


def _support_tuple(index: int) -> tuple[int, ...]:
    return tuple(sorted(STAGE16A_GENERATOR_SUPPORTS[index]))


def _smearing_support(smearing: tuple[float, float, float, float]) -> tuple[int, ...]:
    support: set[int] = set()
    for index, weight in enumerate(smearing):
        if abs(float(weight)) > STAGE16E_ATOL:
            support.update(STAGE16A_GENERATOR_SUPPORTS[index])
    return tuple(sorted(support))


def _structure_factors(point: Stage16PhaseSpacePoint) -> tuple[float, float, float, float]:
    return tuple(float(-(STAGE16A_KAPPA ** 2) * t) for t in point.clocks())


@dataclass(frozen=True, slots=True)
class Stage16EXi:
    orbit_id: str
    quotient_id: str
    representative_id: str
    representative_coordinates: tuple[float, float, float, float]
    cycle_orientation: tuple[int, int, int, int, int]
    spatial_generator_supports: tuple[tuple[int, ...], ...]
    closure_coordinate_supports: tuple[tuple[int, ...], ...]
    source_structure_factors: tuple[float, float, float, float]
    constraint_basis_id: str
    basis_family_id: str
    locality_class: str
    basis_transform_provenance: str
    basis_lfinite_depth: int | None
    declared_lfinite_search_max_depth: int
    stage16d_basis_search_classification: str
    event_correspondence: tuple
    continuation_class_correspondence: tuple
    outcome_correspondence: tuple
    provenance_semantics: str = (
        "cycle/representative/path/structure/basis/locality/depth provenance retained in Xi only"
    )


@dataclass(frozen=True, slots=True)
class Stage16ETypedArchitecture:
    orbit_id: str
    quotient_id: str
    representative_id: str
    O: Stage11OLayer
    P: Stage11PLayer
    R: Stage11RLayer
    V: Stage11VLayer
    future_measurement: Stage15EFuturePayload
    Xi: Stage16EXi


@dataclass(frozen=True, slots=True)
class Stage16EQuotientArchitecture:
    orbit_id: str
    quotient_id: str
    O: Stage11OLayer
    P: Stage11PLayer
    R: Stage11RLayer
    V: Stage11VLayer
    future_measurement: Stage15EFuturePayload
    parameterization_id: str
    event_correspondence: tuple
    continuation_class_correspondence: tuple
    outcome_correspondence: tuple


@dataclass(frozen=True, slots=True)
class Stage16EPathXi:
    path_family: str
    path_id: str
    path_word: str
    source_representative_id: str
    cycle_orientation: tuple[int, int, int, int, int]
    structure_factor_trace: tuple[tuple[float, float, float, float], ...]
    generator_or_smearing_support_trace: tuple[tuple[int, ...], ...]
    local_parameters: tuple[float, ...]
    smearings: tuple[tuple[float, float, float, float], ...]
    compensator_type: str
    compensator_provenance: str
    presented_compensator_word: tuple[int, ...] | None
    presented_compensator_parameters: tuple[float, ...] | None


@dataclass(frozen=True, slots=True)
class Stage16ELocalPathCheck:
    representative_id: str
    edge: tuple[int, int]
    s: float
    u: float
    raw_Xi: Stage16EPathXi
    compensated_Xi: Stage16EPathXi
    provenance_distinct: bool
    endpoint_descent: bool
    public_equal: bool
    future_equal: bool
    witness_equal: bool
    classification: str = STAGE16E_LOCAL_PATH_DESCENT


@dataclass(frozen=True, slots=True)
class Stage16ESmearedPathCheck:
    representative_id: str
    pair_index: int
    nm_Xi: Stage16EPathXi
    mn_compensated_Xi: Stage16EPathXi
    provenance_distinct: bool
    endpoint_descent: bool
    public_equal: bool
    future_equal: bool
    witness_equal: bool
    classification: str = STAGE16E_SMEARED_PATH_DESCENT


@dataclass(frozen=True, slots=True)
class Stage16EBasisCheck:
    representative_id: str
    candidate_id: str
    locality_class: str
    lfinite_depth: int | None
    original_Xi: Stage16EXi
    candidate_Xi: Stage16EXi
    provenance_distinct: bool
    stage16d_content_preserved: bool
    public_equal: bool
    future_equal: bool
    witness_equal: bool
    classification: str = STAGE16E_BASIS_DESCENT


@dataclass(frozen=True, slots=True)
class Stage16EOrbitWitness:
    orbit_id: str
    representative_id: str
    probabilities: tuple[tuple[str, float], ...]
    probability_sum_residual: float
    semantics: str = "orbit-conditioned diagnostic only; not an empirical prediction"


@dataclass(frozen=True, slots=True)
class Stage16EDiagnostics:
    representative_count: int
    quotient_class_count: int
    distinct_public_count: int
    local_path_check_count: int
    local_path_xi_count: int
    smeared_path_check_count: int
    smeared_path_xi_count: int
    basis_candidate_count: int
    basis_check_count: int
    basis_xi_count: int
    witness_count: int
    distinct_witness_count: int
    minimum_witness_separation: float
    same_orbit_descent: bool
    local_path_descent: bool
    smeared_path_descent: bool
    basis_depth_descent: bool
    future_payload_complete: bool
    public_provenance_absent: bool
    xi_provenance_explicit: bool
    criteria_40_44_satisfied: bool


@lru_cache(maxsize=1)
def _inherited_public_by_orbit():
    result = {}
    for projection in canonical_stage15e_quotient_projections():
        result.setdefault(projection.orbit_id, projection)
        if result[projection.orbit_id] != projection:
            raise ValueError("inherited Stage 15E public payload is representative-dependent")
    if set(result) != {orbit.orbit_id for orbit in canonical_stage16a_orbits()}:
        raise ValueError("Stage 16E orbit ids do not match inherited public family")
    return result


@lru_cache(maxsize=1)
def _representatives_by_id():
    return {item.representative_id: item for item in canonical_stage16a_representatives()}


@lru_cache(maxsize=1)
def _stage16d_content_by_candidate():
    return {item.candidate_id: item for item in canonical_stage16d_content_audits()}


def _quotient_id(orbit_id: str) -> str:
    return f"stage16:four_clock_quotient:{orbit_id}"


def _basis_metadata(candidate_id: str | None):
    if candidate_id is None:
        return (
            STAGE16A_BASIS_ID,
            "original_positive_cycle_basis",
            "presented_cycle_basis",
            "identity_original_stage16_basis",
            None,
        )
    candidate = next((x for x in canonical_stage16d_candidates() if x.candidate_id == candidate_id), None)
    if candidate is None:
        raise ValueError(f"unknown Stage 16D basis candidate: {candidate_id}")
    content = _stage16d_content_by_candidate()[candidate_id]
    if not (content.quotient_preserved and content.dirac_pair_preserved and content.complete_relational_preserved):
        raise ValueError("Stage 16E accepts only Stage 16D physically corresponding basis candidates")
    return (
        candidate.candidate_id,
        candidate.family_id,
        candidate.locality_class,
        f"Stage16D:{candidate.transform_kind}:{candidate.candidate_id}",
        candidate.lfinite_depth,
    )


def _events(representative):
    out = []
    for event_id, tau in STAGE16E_CLOCK_QUADRUPLES:
        out.append(
            Stage11OEvent(
                role="prediction_anchor" if event_id == "e1" else "measurement_target",
                stage10_event=event_id,
                physical_event_id=f"{representative.orbit_id}:complete_four_clock_relational:{event_id}",
                clock_value=tau[0],
                q_value=stage16c_complete_value(representative.declared_Q_D, tau),
            )
        )
    return tuple(out)


def _xi_for_representative(representative, *, candidate_id: str | None = None):
    base = _inherited_public_by_orbit()[representative.orbit_id]
    basis_id, family_id, locality_class, provenance, depth = _basis_metadata(candidate_id)
    point = representative.point()
    O = replace(base.O, relational_events=_events(representative))
    Xi = Stage16EXi(
        orbit_id=representative.orbit_id,
        quotient_id=_quotient_id(representative.orbit_id),
        representative_id=representative.representative_id,
        representative_coordinates=point.clocks(),
        cycle_orientation=STAGE16E_CYCLE_ORIENTATION,
        spatial_generator_supports=tuple(_support_tuple(i) for i in range(4)),
        closure_coordinate_supports=tuple(
            tuple(sorted(stage16a_closure_coordinate_support(point, i, (i + 1) % 4)))
            for i in range(4)
        ),
        source_structure_factors=_structure_factors(point),
        constraint_basis_id=basis_id,
        basis_family_id=family_id,
        locality_class=locality_class,
        basis_transform_provenance=provenance,
        basis_lfinite_depth=depth,
        declared_lfinite_search_max_depth=STAGE16D_LFINITE_MAX_DEPTH,
        stage16d_basis_search_classification=STAGE16D_CLASSIFICATION,
        event_correspondence=tuple((e.stage10_event, e.physical_event_id) for e in O.relational_events),
        continuation_class_correspondence=base.continuation_class_correspondence,
        outcome_correspondence=base.outcome_correspondence,
    )
    return O, Xi


@lru_cache(maxsize=None)
def stage16e_architecture_for_representative(representative, candidate_id: str | None = None):
    base = _inherited_public_by_orbit()[representative.orbit_id]
    O, Xi = _xi_for_representative(representative, candidate_id=candidate_id)
    return Stage16ETypedArchitecture(
        orbit_id=representative.orbit_id,
        quotient_id=_quotient_id(representative.orbit_id),
        representative_id=representative.representative_id,
        O=O,
        P=base.P,
        R=base.R,
        V=base.V,
        future_measurement=base.future_measurement,
        Xi=Xi,
    )


@lru_cache(maxsize=1)
def canonical_stage16e_architectures():
    return tuple(stage16e_architecture_for_representative(r) for r in canonical_stage16a_representatives())


def stage16e_validate_architecture(architecture):
    representative = _representatives_by_id().get(architecture.representative_id)
    if representative is None:
        return False, ("representative_identity",)
    candidate_id = None if architecture.Xi.constraint_basis_id == STAGE16A_BASIS_ID else architecture.Xi.constraint_basis_id
    expected = stage16e_architecture_for_representative(representative, candidate_id)
    return architecture == expected, () if architecture == expected else ("typed_architecture_mismatch",)


def stage16e_quotient_projection(architecture):
    return Stage16EQuotientArchitecture(
        orbit_id=architecture.orbit_id,
        quotient_id=architecture.quotient_id,
        O=architecture.O,
        P=architecture.P,
        R=architecture.R,
        V=architecture.V,
        future_measurement=architecture.future_measurement,
        parameterization_id=STAGE11A_IDENTITY,
        event_correspondence=architecture.Xi.event_correspondence,
        continuation_class_correspondence=architecture.Xi.continuation_class_correspondence,
        outcome_correspondence=architecture.Xi.outcome_correspondence,
    )


@lru_cache(maxsize=1)
def canonical_stage16e_quotient_projections():
    return tuple(stage16e_quotient_projection(x) for x in canonical_stage16e_architectures())


def _orbit_id_for_point(point: Stage16PhaseSpacePoint) -> str:
    qd, pd = stage16a_dirac_data(point)
    matches = [
        orbit.orbit_id
        for orbit in canonical_stage16a_orbits()
        if max(abs(qd - orbit.Q_D), abs(pd - orbit.P_D)) <= STAGE16E_ATOL
    ]
    if len(matches) != 1:
        raise ValueError("endpoint does not descend to exactly one Stage 16 physical orbit")
    return matches[0]


def _witness_probabilities(qd: float, pd: float) -> tuple[tuple[str, float], ...]:
    relational_target = stage16c_complete_value(qd, (1.0, 1.0, 1.0, 1.0))
    left = 0.5 * (1.0 + tanh(0.70 * qd + 0.40 * pd + 0.20 * relational_target))
    return ((FUTURE_SIGNATURE_LEFT, left), (FUTURE_SIGNATURE_OTHER, 1.0 - left))


def _witness_residual(left, right) -> float:
    return float(max(abs(a[1] - b[1]) for a, b in zip(left, right, strict=True)))


def stage16e_orbit_witness(architecture):
    representative = _representatives_by_id()[architecture.representative_id]
    probabilities = _witness_probabilities(
        representative.declared_Q_D, representative.declared_P_D
    )
    return Stage16EOrbitWitness(
        orbit_id=architecture.orbit_id,
        representative_id=architecture.representative_id,
        probabilities=probabilities,
        probability_sum_residual=abs(sum(v for _, v in probabilities) - 1.0),
    )


@lru_cache(maxsize=1)
def canonical_stage16e_orbit_witnesses():
    return tuple(stage16e_orbit_witness(x) for x in canonical_stage16e_architectures())


def _local_path_xi(representative, probe, *, compensated: bool):
    i, j = probe.edge
    source = representative.point()
    after_first = stage16b_apply_local_flow(source, i if not compensated else j, probe.s if not compensated else probe.u)
    if not compensated:
        return Stage16EPathXi(
            path_family="local",
            path_id=f"{probe.representative_id}:{i}{j}:{probe.s}:{probe.u}:raw",
            path_word=f"C{i}->C{j}",
            source_representative_id=probe.representative_id,
            cycle_orientation=STAGE16E_CYCLE_ORIENTATION,
            structure_factor_trace=(_structure_factors(source), _structure_factors(after_first)),
            generator_or_smearing_support_trace=(_support_tuple(i), _support_tuple(j)),
            local_parameters=(probe.s, probe.u),
            smearings=(),
            compensator_type="none",
            compensator_provenance="raw_ordering_no_compensator",
            presented_compensator_word=None,
            presented_compensator_parameters=None,
        )
    word = tuple(probe.presented_word) if probe.presented_word is not None else None
    params = tuple(probe.presented_parameters) if probe.presented_parameters is not None else None
    trace = (_support_tuple(j), _support_tuple(i))
    if word is not None:
        trace = trace + tuple(_support_tuple(g) for g in word)
    return Stage16EPathXi(
        path_family="local",
        path_id=f"{probe.representative_id}:{j}{i}:{probe.s}:{probe.u}:presented_compensated",
        path_word=f"C{j}->C{i}+presented",
        source_representative_id=probe.representative_id,
        cycle_orientation=STAGE16E_CYCLE_ORIENTATION,
        structure_factor_trace=(_structure_factors(source), _structure_factors(after_first)),
        generator_or_smearing_support_trace=trace,
        local_parameters=(probe.u, probe.s) + (() if params is None else params),
        smearings=(),
        compensator_type=STAGE16B_PRESENTED_COMPENSATION_KIND,
        compensator_provenance="frozen_24_word_presented_C_search",
        presented_compensator_word=word,
        presented_compensator_parameters=params,
    )


@lru_cache(maxsize=1)
def canonical_stage16e_local_path_checks():
    reps = _representatives_by_id()
    architectures = {x.representative_id: x for x in canonical_stage16e_architectures()}
    result = []
    for probe in canonical_stage16b_local_probes():
        representative = reps[probe.representative_id]
        source = representative.point()
        i, j = probe.edge
        a, b = stage16b_local_raw_endpoints(source, i, j, probe.s, probe.u)
        if probe.presented_success and probe.presented_word is not None and probe.presented_parameters is not None:
            presented = stage16b_apply_word(b, probe.presented_word, probe.presented_parameters)
        else:
            presented = b
        seed = stage16b_seed_compensate(b, a)
        orbit_ids = {_orbit_id_for_point(x) for x in (source, a, b, seed, presented)}
        arch = architectures[probe.representative_id]
        source_qd, source_pd = stage16a_dirac_data(source)
        witness = _witness_probabilities(source_qd, source_pd)
        witness_equal = all(
            _witness_residual(_witness_probabilities(*stage16a_dirac_data(x)), witness) <= STAGE16E_ATOL
            for x in (a, b, seed, presented)
        )
        endpoint_descent = (
            probe.presented_success
            and probe.presented_residual <= STAGE16E_ATOL
            and probe.seed_compensated_residual <= STAGE16E_ATOL
            and probe.payload_residual <= STAGE16E_ATOL
            and orbit_ids == {representative.orbit_id}
        )
        raw_xi = _local_path_xi(representative, probe, compensated=False)
        comp_xi = _local_path_xi(representative, probe, compensated=True)
        result.append(Stage16ELocalPathCheck(
            representative_id=probe.representative_id,
            edge=probe.edge,
            s=probe.s,
            u=probe.u,
            raw_Xi=raw_xi,
            compensated_Xi=comp_xi,
            provenance_distinct=raw_xi != comp_xi,
            endpoint_descent=endpoint_descent,
            public_equal=endpoint_descent and len(orbit_ids) == 1,
            future_equal=bool(arch.future_measurement.measurement and arch.future_measurement.weighted and arch.future_measurement.posterior),
            witness_equal=witness_equal,
        ))
    return tuple(result)


def _smeared_path_xi(representative, pair_index: int, *, compensated: bool):
    N, M = STAGE16A_SMEARING_PAIRS[pair_index]
    alpha, beta = STAGE16B_SMEARED_PARAMETER_PAIR
    source = representative.point()
    if not compensated:
        after_first = stage16b_apply_smeared_flow(source, N, alpha)
        return Stage16EPathXi(
            path_family="smeared",
            path_id=f"{representative.representative_id}:{pair_index}:NM",
            path_word="N->M",
            source_representative_id=representative.representative_id,
            cycle_orientation=STAGE16E_CYCLE_ORIENTATION,
            structure_factor_trace=(_structure_factors(source), _structure_factors(after_first)),
            generator_or_smearing_support_trace=(_smearing_support(N), _smearing_support(M)),
            local_parameters=(alpha, beta),
            smearings=(N, M),
            compensator_type="none",
            compensator_provenance="raw_smeared_ordering_no_compensator",
            presented_compensator_word=None,
            presented_compensator_parameters=None,
        )
    after_first = stage16b_apply_smeared_flow(source, M, beta)
    return Stage16EPathXi(
        path_family="smeared",
        path_id=f"{representative.representative_id}:{pair_index}:MN+seed",
        path_word="M->N+seed",
        source_representative_id=representative.representative_id,
        cycle_orientation=STAGE16E_CYCLE_ORIENTATION,
        structure_factor_trace=(_structure_factors(source), _structure_factors(after_first)),
        generator_or_smearing_support_trace=(_smearing_support(M), _smearing_support(N), (0, 1, 2, 3)),
        local_parameters=(beta, alpha),
        smearings=(M, N),
        compensator_type=STAGE16B_SEED_COMPENSATION_KIND,
        compensator_provenance="global_seed_coordinate_endpoint_compensation",
        presented_compensator_word=None,
        presented_compensator_parameters=None,
    )


@lru_cache(maxsize=1)
def canonical_stage16e_smeared_path_checks():
    reps = _representatives_by_id()
    architectures = {x.representative_id: x for x in canonical_stage16e_architectures()}
    alpha, beta = STAGE16B_SMEARED_PARAMETER_PAIR
    result = []
    for probe in canonical_stage16b_smeared_probes():
        representative = reps[probe.representative_id]
        source = representative.point()
        N, M = STAGE16A_SMEARING_PAIRS[probe.pair_index]
        a = stage16b_apply_smeared_flow(stage16b_apply_smeared_flow(source, N, alpha), M, beta)
        b = stage16b_apply_smeared_flow(stage16b_apply_smeared_flow(source, M, beta), N, alpha)
        comp = stage16b_seed_compensate(b, a)
        orbit_ids = {_orbit_id_for_point(x) for x in (source, a, b, comp)}
        arch = architectures[probe.representative_id]
        source_qd, source_pd = stage16a_dirac_data(source)
        witness = _witness_probabilities(source_qd, source_pd)
        witness_equal = all(
            _witness_residual(_witness_probabilities(*stage16a_dirac_data(x)), witness) <= STAGE16E_ATOL
            for x in (a, b, comp)
        )
        endpoint_descent = (
            probe.seed_compensated_residual <= STAGE16E_ATOL
            and probe.payload_residual <= STAGE16E_ATOL
            and orbit_ids == {representative.orbit_id}
        )
        nm_xi = _smeared_path_xi(representative, probe.pair_index, compensated=False)
        comp_xi = _smeared_path_xi(representative, probe.pair_index, compensated=True)
        result.append(Stage16ESmearedPathCheck(
            representative_id=probe.representative_id,
            pair_index=probe.pair_index,
            nm_Xi=nm_xi,
            mn_compensated_Xi=comp_xi,
            provenance_distinct=nm_xi != comp_xi,
            endpoint_descent=endpoint_descent,
            public_equal=endpoint_descent and len(orbit_ids) == 1,
            future_equal=bool(arch.future_measurement.measurement and arch.future_measurement.weighted and arch.future_measurement.posterior),
            witness_equal=witness_equal,
        ))
    return tuple(result)


@lru_cache(maxsize=1)
def canonical_stage16e_basis_checks():
    content_by = _stage16d_content_by_candidate()
    result = []
    for representative in canonical_stage16a_representatives():
        original = stage16e_architecture_for_representative(representative)
        original_witness = stage16e_orbit_witness(original)
        for candidate in canonical_stage16d_candidates():
            transformed = stage16e_architecture_for_representative(representative, candidate.candidate_id)
            content = content_by[candidate.candidate_id]
            content_preserved = content.quotient_preserved and content.dirac_pair_preserved and content.complete_relational_preserved
            result.append(Stage16EBasisCheck(
                representative_id=representative.representative_id,
                candidate_id=candidate.candidate_id,
                locality_class=candidate.locality_class,
                lfinite_depth=candidate.lfinite_depth,
                original_Xi=original.Xi,
                candidate_Xi=transformed.Xi,
                provenance_distinct=original.Xi != transformed.Xi,
                stage16d_content_preserved=content_preserved,
                public_equal=stage16e_quotient_projection(original) == stage16e_quotient_projection(transformed),
                future_equal=original.future_measurement == transformed.future_measurement,
                witness_equal=original_witness.probabilities == stage16e_orbit_witness(transformed).probabilities,
            ))
    return tuple(result)


def _public_provenance_absent():
    forbidden = {
        STAGE16A_BASIS_ID,
        STAGE16D_CLASSIFICATION,
        STAGE16B_PRESENTED_COMPENSATION_KIND,
        STAGE16B_SEED_COMPENSATION_KIND,
        *(candidate.candidate_id for candidate in canonical_stage16d_candidates()),
    }
    return all(
        not any(token in repr((item.O, item.P, item.R, item.V, item.future_measurement)) for token in forbidden)
        for item in canonical_stage16e_architectures()
    )


@lru_cache(maxsize=1)
def stage16e_diagnostics():
    architectures = canonical_stage16e_architectures()
    projections = canonical_stage16e_quotient_projections()
    local_checks = canonical_stage16e_local_path_checks()
    smeared_checks = canonical_stage16e_smeared_path_checks()
    basis_checks = canonical_stage16e_basis_checks()
    witnesses = canonical_stage16e_orbit_witnesses()

    same_orbit = True
    references = []
    for orbit in canonical_stage16a_orbits():
        subset = [x for x in architectures if x.orbit_id == orbit.orbit_id]
        same_orbit &= len({repr(stage16e_quotient_projection(x)) for x in subset}) == 1
        references.append(next(x for x in witnesses if x.orbit_id == orbit.orbit_id))

    vector = lambda x: tuple(v for _, v in x.probabilities)
    minimum_separation = min(
        max(abs(a - b) for a, b in zip(vector(left), vector(right), strict=True))
        for index, left in enumerate(references)
        for right in references[index + 1:]
    )
    local_descent = all(
        x.provenance_distinct and x.endpoint_descent and x.public_equal and x.future_equal and x.witness_equal
        for x in local_checks
    )
    smeared_descent = all(
        x.provenance_distinct and x.endpoint_descent and x.public_equal and x.future_equal and x.witness_equal
        for x in smeared_checks
    )
    basis_descent = all(
        x.provenance_distinct and x.stage16d_content_preserved and x.public_equal and x.future_equal and x.witness_equal
        for x in basis_checks
    )
    future_complete = all(
        x.future_measurement.measurement
        and x.future_measurement.weighted
        and x.future_measurement.posterior
        and x.future_measurement.future_actuality_status == STAGE16E_NOT_LICENSED
        and x.future_measurement.empirical_claim_status == STAGE16E_NOT_LICENSED
        for x in architectures
    )
    xi_explicit = (
        len(local_checks) == 2592
        and len(smeared_checks) == 2592
        and len(basis_checks) == 6804
        and all(x.Xi.cycle_orientation == STAGE16E_CYCLE_ORIENTATION for x in architectures)
        and all(x.Xi.spatial_generator_supports for x in architectures)
        and all(x.provenance_distinct for x in local_checks)
        and all(x.provenance_distinct for x in smeared_checks)
        and all(x.provenance_distinct for x in basis_checks)
        and {x.candidate_Xi.basis_lfinite_depth for x in basis_checks} >= {None, 1}
    )
    criteria = all((
        len(architectures) == 324,
        len({x.quotient_id for x in architectures}) == 4,
        len({repr(x) for x in projections}) == 4,
        all(stage16e_validate_architecture(x)[0] for x in architectures),
        same_orbit,
        local_descent,
        smeared_descent,
        basis_descent,
        future_complete,
        _public_provenance_absent(),
        xi_explicit,
        len({vector(x) for x in references}) == 4,
        minimum_separation > STAGE16E_ATOL,
        all(x.probability_sum_residual <= STAGE16E_ATOL for x in witnesses),
    ))
    return Stage16EDiagnostics(
        representative_count=len(architectures),
        quotient_class_count=len({x.quotient_id for x in architectures}),
        distinct_public_count=len({repr(x) for x in projections}),
        local_path_check_count=len(local_checks),
        local_path_xi_count=2 * len(local_checks),
        smeared_path_check_count=len(smeared_checks),
        smeared_path_xi_count=2 * len(smeared_checks),
        basis_candidate_count=len(canonical_stage16d_candidates()),
        basis_check_count=len(basis_checks),
        basis_xi_count=2 * len(basis_checks),
        witness_count=len(witnesses),
        distinct_witness_count=len({vector(x) for x in references}),
        minimum_witness_separation=float(minimum_separation),
        same_orbit_descent=bool(same_orbit),
        local_path_descent=bool(local_descent),
        smeared_path_descent=bool(smeared_descent),
        basis_depth_descent=bool(basis_descent),
        future_payload_complete=bool(future_complete),
        public_provenance_absent=_public_provenance_absent(),
        xi_provenance_explicit=bool(xi_explicit),
        criteria_40_44_satisfied=bool(criteria),
    )


def stage16e_summary():
    d = stage16e_diagnostics()
    return {
        "representative_count": d.representative_count,
        "quotient_class_count": d.quotient_class_count,
        "local_path_check_count": d.local_path_check_count,
        "smeared_path_check_count": d.smeared_path_check_count,
        "basis_candidate_count": d.basis_candidate_count,
        "basis_check_count": d.basis_check_count,
        "classification_local": STAGE16E_LOCAL_PATH_DESCENT,
        "classification_smeared": STAGE16E_SMEARED_PATH_DESCENT,
        "classification_basis": STAGE16E_BASIS_DESCENT,
        "criteria_40_44_satisfied": d.criteria_40_44_satisfied,
        "bounded_result": STAGE16E_BOUNDED_RESULT,
        "guards": STAGE16E_GUARDS,
    }
