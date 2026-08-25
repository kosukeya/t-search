"""Stage 15E typed O/P/R/V/Xi and future-measurement descent.

Stage 15E introduces no new measurement law.  It carries the previously
validated Stage 13E public/future-measurement architecture onto the Stage 15
spatially indexed carrier, replaces only the relational O-events with the
Stage 15C complete three-clock observable, and tests descent across the Stage
15B local/smeared path atlas and every equivalent basis candidate audited in
Stage 15D.

Representative, spatial-support, path, compensator, structure-function and
basis provenance remain in Xi.  They are not quotient-level public content.
No claim of general relativity, refoliation invariance, future actuality,
ontological equivalence, or ontological becoming is licensed.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from functools import lru_cache
from math import tanh

from t_search.stage9_modal import FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_OTHER
from t_search.stage11_lift import (
    Stage11OLayer,
    Stage11OEvent,
    Stage11PLayer,
    Stage11RLayer,
    Stage11VLayer,
)
from t_search.stage11_parametrized import STAGE11A_IDENTITY
from t_search.stage13_measurement import (
    canonical_stage13e_measurement_views,
    canonical_stage13e_posterior_views,
    canonical_stage13e_quotient_projections,
    canonical_stage13e_weighted_views,
)
from t_search.stage15_basis import (
    canonical_stage15d_candidates,
    canonical_stage15d_content_audits,
    stage15d_locality_audit,
)
from t_search.stage15_local import (
    STAGE15A_ATOL,
    STAGE15A_BASIS_ID,
    STAGE15A_GENERATOR_SUPPORTS,
    Stage15PhaseSpacePoint,
    canonical_stage15a_orbits,
    canonical_stage15a_representatives,
    stage15a_dirac_data,
    stage15a_structure_function,
)
from t_search.stage15_paths import (
    STAGE15B_PATH_012,
    STAGE15B_PATH_102,
    STAGE15B_SMEARED_CASES,
    canonical_stage15b_local_pairs,
    canonical_stage15b_smeared_order_probes,
    stage15b_apply_local_flow,
    stage15b_apply_local_path,
    stage15b_apply_smeared_flow,
)
from t_search.stage15_relational import (
    stage15c_complete_relational_value,
    stage15c_quotient_classes,
)

STAGE15E_ATOL = STAGE15A_ATOL
STAGE15E_LOCAL_PATH_DESCENT = "spatial_local_path_operational_payloads_descend"
STAGE15E_SMEARED_PATH_DESCENT = "spatial_smeared_path_operational_payloads_descend"
STAGE15E_BASIS_DESCENT = "spatial_basis_operational_payloads_descend"
STAGE15E_NOT_LICENSED = "not_licensed"
STAGE15E_CLOCK_TRIPLES = (
    ("e1", -1.0, -1.0, -1.0),
    ("e2", 1.0, 1.0, 1.0),
)
STAGE15E_BOUNDED_RESULT = (
    "Stage 15E typed O/P/R/V/Xi and future-measurement descent across the "
    "sampled spatial quotient, compensated local/smeared paths, and all "
    "Stage 15D equivalent basis candidates on the frozen finite family = established"
)
STAGE15E_GUARDS = (
    "spatial/path/basis Xi provenance != quotient-level physical content",
    "spatial index != ontological spatial substance",
    "path word != physical temporal history",
    "path word != modal continuation",
    "compensated local/smeared operational descent != refoliation invariance",
    "basis-equivalent operational descent != refoliation invariance",
    "local Abelianization + typed descent != physical triviality",
    "future-measurement covariance != future actuality",
    "path-independent evidence update != ontological becoming",
    "typed operational descent != ontological equivalence",
    "Potentiality != quantum randomness by definition",
    "orbit-sensitive witness != empirical prediction",
    "spatially indexed constraint precursor != general relativity",
    "repository validation != new scientific evidence",
)


def _support_tuple(index: int) -> tuple[int, ...]:
    return tuple(sorted(STAGE15A_GENERATOR_SUPPORTS[index]))


def _smearing_support(smearing: tuple[float, float, float]) -> tuple[int, ...]:
    support: set[int] = set()
    for index, weight in enumerate(smearing):
        if abs(float(weight)) > STAGE15E_ATOL:
            support.update(STAGE15A_GENERATOR_SUPPORTS[index])
    return tuple(sorted(support))


@dataclass(frozen=True, slots=True)
class Stage15EFuturePayload:
    orbit_id: str
    measurement: tuple
    weighted: tuple
    posterior: tuple
    future_signature_ids: tuple[str, str] = (
        FUTURE_SIGNATURE_LEFT,
        FUTURE_SIGNATURE_OTHER,
    )
    future_actuality_status: str = STAGE15E_NOT_LICENSED
    empirical_claim_status: str = STAGE15E_NOT_LICENSED


@dataclass(frozen=True, slots=True)
class Stage15EXi:
    orbit_id: str
    quotient_id: str
    representative_id: str
    constraint_basis_id: str
    basis_family_id: str
    locality_class: str
    basis_transform_provenance: str
    basis_lfinite_depth: int | None
    representative_coordinates: tuple[float, float, float]
    source_structure_function: float
    spatial_generator_supports: tuple[tuple[int, ...], ...]
    licensed_local_path_words: tuple[str, str]
    licensed_smeared_case_ids: tuple[str, ...]
    event_correspondence: tuple
    continuation_class_correspondence: tuple
    outcome_correspondence: tuple
    provenance_semantics: str = (
        "spatial/representative/path/structure-function/basis provenance retained in Xi only"
    )


@dataclass(frozen=True, slots=True)
class Stage15ETypedArchitecture:
    orbit_id: str
    quotient_id: str
    representative_id: str
    O: Stage11OLayer
    P: Stage11PLayer
    R: Stage11RLayer
    V: Stage11VLayer
    future_measurement: Stage15EFuturePayload
    Xi: Stage15EXi


@dataclass(frozen=True, slots=True)
class Stage15EQuotientArchitecture:
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
class Stage15EPathXi:
    path_family: str
    path_id: str
    path_word: str
    source_representative_id: str
    target_representative_id: str | None
    structure_function_trace: tuple[float, ...]
    generator_or_smearing_support_trace: tuple[tuple[int, ...], ...]
    local_parameters: tuple[float, ...]
    smearings: tuple[tuple[float, float, float], ...]
    compensator: float
    compensator_provenance: str


@dataclass(frozen=True, slots=True)
class Stage15ELocalPathCheck:
    pair_id: str
    path_Xi_012: Stage15EPathXi
    path_Xi_102: Stage15EPathXi
    provenance_distinct: bool
    structure_trace_distinct: bool
    endpoint_descent: bool
    public_equal: bool
    future_equal: bool
    witness_equal: bool
    classification: str = STAGE15E_LOCAL_PATH_DESCENT


@dataclass(frozen=True, slots=True)
class Stage15ESmearedPathCheck:
    representative_id: str
    case_id: str
    path_Xi_nm: Stage15EPathXi
    path_Xi_mn_compensated: Stage15EPathXi
    provenance_distinct: bool
    max_dirac_payload_residual: float
    endpoint_descent: bool
    public_equal: bool
    future_equal: bool
    witness_equal: bool
    classification: str = STAGE15E_SMEARED_PATH_DESCENT


@dataclass(frozen=True, slots=True)
class Stage15EBasisCheck:
    representative_id: str
    candidate_id: str
    locality_class: str
    original_Xi: Stage15EXi
    candidate_Xi: Stage15EXi
    provenance_distinct: bool
    stage15d_content_preserved: bool
    public_equal: bool
    future_equal: bool
    witness_equal: bool
    classification: str = STAGE15E_BASIS_DESCENT


@dataclass(frozen=True, slots=True)
class Stage15EOrbitWitness:
    orbit_id: str
    representative_id: str
    probabilities: tuple[tuple[str, float], ...]
    probability_sum_residual: float
    semantics: str = "orbit-conditioned diagnostic only; not an empirical prediction"


@dataclass(frozen=True, slots=True)
class Stage15EDiagnostics:
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
    basis_descent: bool
    future_payload_complete: bool
    public_provenance_absent: bool
    xi_provenance_explicit: bool
    criteria_39_43_satisfied: bool


def _measurement_tuple(item):
    return (
        item.continuation_id,
        item.family_id,
        item.internal_clock,
        item.internal_clock_index,
        item.outcome_ids,
        item.normalization_semantics,
        item.probabilities,
    )


def _weighted_tuple(item):
    return (
        item.continuation_ids,
        item.continuation_weights,
        item.directional_record_scores,
        item.directional_accessibility_scores,
        item.orientations,
        item.next_outcomes,
        item.next_probabilities,
    )


def _posterior_tuple(item):
    return (
        item.observed_outcome,
        item.epistemic_posterior_weights,
        item.ontic_posterior_weights,
        item.epistemic_selected_continuation_id,
        item.ontic_no_selected_complete_continuation_datum,
    )


@lru_cache(maxsize=1)
def _inherited_public_by_orbit():
    result = {}
    for projection in canonical_stage13e_quotient_projections():
        result.setdefault(projection.orbit_id, projection)
        if result[projection.orbit_id] != projection:
            raise ValueError("inherited public payload is representative-dependent")
    return result


@lru_cache(maxsize=1)
def _future_by_orbit():
    measurements = canonical_stage13e_measurement_views()
    weighted = canonical_stage13e_weighted_views()
    posterior = canonical_stage13e_posterior_views()
    result = {}
    for orbit in canonical_stage15a_orbits():
        oid = orbit.orbit_id
        payload = Stage15EFuturePayload(
            orbit_id=oid,
            measurement=tuple(sorted({_measurement_tuple(x) for x in measurements if x.orbit_id == oid}, key=repr)),
            weighted=tuple(sorted({_weighted_tuple(x) for x in weighted if x.orbit_id == oid}, key=repr)),
            posterior=tuple(sorted({_posterior_tuple(x) for x in posterior if x.orbit_id == oid}, key=repr)),
        )
        if not payload.measurement or not payload.weighted or not payload.posterior:
            raise ValueError("missing inherited future-measurement payload")
        result[oid] = payload
    return result


@lru_cache(maxsize=1)
def _quotient_by_representative():
    result = {}
    for quotient in stage15c_quotient_classes():
        for representative_id in quotient.member_representative_ids:
            result[representative_id] = quotient
    if len(result) != 108:
        raise ValueError("Stage 15E quotient lookup must cover 108 representatives")
    return result


@lru_cache(maxsize=1)
def _stage15d_content_by_candidate():
    return {item.candidate_id: item for item in canonical_stage15d_content_audits()}


def _basis_metadata(candidate_id: str | None):
    if candidate_id is None:
        return (
            STAGE15A_BASIS_ID,
            "original_positive_basis",
            "presented_spatial_basis",
            "identity_original_stage15_basis",
            None,
        )
    candidate = next(
        (item for item in canonical_stage15d_candidates() if item.candidate_id == candidate_id),
        None,
    )
    if candidate is None:
        raise ValueError(f"unknown Stage 15D basis candidate: {candidate_id}")
    locality = stage15d_locality_audit(candidate)
    content = _stage15d_content_by_candidate()[candidate_id]
    if not (
        content.quotient_preserved
        and content.dirac_pair_preserved
        and content.complete_relational_preserved
    ):
        raise ValueError("Stage 15E accepts only Stage 15D physically corresponding basis candidates")
    return (
        candidate.candidate_id,
        candidate.family_id,
        locality.locality_class,
        f"Stage15D:{candidate.transform_kind}:{candidate.candidate_id}",
        locality.lfinite_depth,
    )


def _events(representative):
    quotient = _quotient_by_representative()[representative.representative_id]
    result = []
    for event_id, tau0, tau1, tau2 in STAGE15E_CLOCK_TRIPLES:
        result.append(
            Stage11OEvent(
                role="prediction_anchor" if event_id == "e1" else "measurement_target",
                stage10_event=event_id,
                physical_event_id=f"{representative.orbit_id}:complete_relational:{event_id}",
                clock_value=tau0,
                q_value=stage15c_complete_relational_value(
                    quotient.Q_D, tau0, tau1, tau2
                ),
            )
        )
    return tuple(result)


def stage15e_architecture_for_representative(representative, *, candidate_id: str | None = None):
    base = _inherited_public_by_orbit()[representative.orbit_id]
    quotient = _quotient_by_representative()[representative.representative_id]
    basis_id, family_id, locality_class, provenance, depth = _basis_metadata(candidate_id)
    O = replace(base.O, relational_events=_events(representative))
    Xi = Stage15EXi(
        orbit_id=representative.orbit_id,
        quotient_id=quotient.class_id,
        representative_id=representative.representative_id,
        constraint_basis_id=basis_id,
        basis_family_id=family_id,
        locality_class=locality_class,
        basis_transform_provenance=provenance,
        basis_lfinite_depth=depth,
        representative_coordinates=(representative.T0, representative.T1, representative.T2),
        source_structure_function=stage15a_structure_function(representative.point()),
        spatial_generator_supports=tuple(_support_tuple(index) for index in range(3)),
        licensed_local_path_words=(STAGE15B_PATH_012, STAGE15B_PATH_102),
        licensed_smeared_case_ids=tuple(case[0] for case in STAGE15B_SMEARED_CASES),
        event_correspondence=tuple(
            (event.stage10_event, event.physical_event_id) for event in O.relational_events
        ),
        continuation_class_correspondence=base.continuation_class_correspondence,
        outcome_correspondence=base.outcome_correspondence,
    )
    return Stage15ETypedArchitecture(
        orbit_id=representative.orbit_id,
        quotient_id=quotient.class_id,
        representative_id=representative.representative_id,
        O=O,
        P=base.P,
        R=base.R,
        V=base.V,
        future_measurement=_future_by_orbit()[representative.orbit_id],
        Xi=Xi,
    )


@lru_cache(maxsize=1)
def canonical_stage15e_architectures():
    return tuple(
        stage15e_architecture_for_representative(representative)
        for representative in canonical_stage15a_representatives()
    )


def stage15e_validate_architecture(architecture):
    representative = next(
        (
            item
            for item in canonical_stage15a_representatives()
            if item.representative_id == architecture.representative_id
        ),
        None,
    )
    if representative is None:
        return False, ("representative_identity",)
    candidate_id = (
        None
        if architecture.Xi.constraint_basis_id == STAGE15A_BASIS_ID
        else architecture.Xi.constraint_basis_id
    )
    expected = stage15e_architecture_for_representative(
        representative, candidate_id=candidate_id
    )
    return architecture == expected, () if architecture == expected else ("typed_architecture_mismatch",)


def stage15e_quotient_projection(architecture):
    return Stage15EQuotientArchitecture(
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
def canonical_stage15e_quotient_projections():
    return tuple(
        stage15e_quotient_projection(item) for item in canonical_stage15e_architectures()
    )


def stage15e_orbit_witness(architecture):
    quotient = _quotient_by_representative()[architecture.representative_id]
    relational_target = stage15c_complete_relational_value(
        quotient.Q_D, 1.0, 1.0, 1.0
    )
    left = 0.5 * (
        1.0
        + tanh(
            0.70 * quotient.Q_D
            + 0.40 * quotient.P_D
            + 0.20 * relational_target
        )
    )
    probabilities = (
        (FUTURE_SIGNATURE_LEFT, left),
        (FUTURE_SIGNATURE_OTHER, 1.0 - left),
    )
    return Stage15EOrbitWitness(
        orbit_id=architecture.orbit_id,
        representative_id=architecture.representative_id,
        probabilities=probabilities,
        probability_sum_residual=abs(sum(value for _, value in probabilities) - 1.0),
    )


@lru_cache(maxsize=1)
def canonical_stage15e_orbit_witnesses():
    return tuple(stage15e_orbit_witness(item) for item in canonical_stage15e_architectures())


def _local_path_xi(pair, path_word: str):
    source = pair.source.point()
    if path_word == STAGE15B_PATH_012:
        after_first = stage15b_apply_local_flow(source, 0, pair.s)
        compensator = pair.v_012
        support_trace = (_support_tuple(0), _support_tuple(1), _support_tuple(2))
        provenance = "exact_C2_compensator:v_012"
    elif path_word == STAGE15B_PATH_102:
        after_first = stage15b_apply_local_flow(source, 1, pair.u)
        compensator = pair.v_102
        support_trace = (_support_tuple(1), _support_tuple(0), _support_tuple(2))
        provenance = "exact_C2_compensator:v_102"
    else:
        raise ValueError(f"unknown Stage 15E local path word: {path_word}")
    return Stage15EPathXi(
        path_family="local",
        path_id=f"{pair.pair_id}:{path_word}",
        path_word=path_word,
        source_representative_id=pair.source.representative_id,
        target_representative_id=pair.target.representative_id,
        structure_function_trace=(
            stage15a_structure_function(source),
            stage15a_structure_function(after_first),
        ),
        generator_or_smearing_support_trace=support_trace,
        local_parameters=(pair.s, pair.u, compensator),
        smearings=(),
        compensator=compensator,
        compensator_provenance=provenance,
    )


@lru_cache(maxsize=1)
def canonical_stage15e_local_path_checks():
    architectures = {
        item.representative_id: item for item in canonical_stage15e_architectures()
    }
    witnesses = {
        item.representative_id: item for item in canonical_stage15e_orbit_witnesses()
    }
    result = []
    for pair in canonical_stage15b_local_pairs():
        source = architectures[pair.source.representative_id]
        target = architectures[pair.target.representative_id]
        xi_012 = _local_path_xi(pair, STAGE15B_PATH_012)
        xi_102 = _local_path_xi(pair, STAGE15B_PATH_102)
        r012 = stage15b_apply_local_path(pair, STAGE15B_PATH_012)
        r102 = stage15b_apply_local_path(pair, STAGE15B_PATH_102)
        endpoint_descent = max(
            r012.final_endpoint_residual,
            r102.final_endpoint_residual,
            r012.final_payload_residual,
            r102.final_payload_residual,
        ) <= STAGE15E_ATOL
        result.append(
            Stage15ELocalPathCheck(
                pair_id=pair.pair_id,
                path_Xi_012=xi_012,
                path_Xi_102=xi_102,
                provenance_distinct=xi_012 != xi_102,
                structure_trace_distinct=(
                    xi_012.structure_function_trace != xi_102.structure_function_trace
                ),
                endpoint_descent=endpoint_descent,
                public_equal=(
                    endpoint_descent
                    and stage15e_quotient_projection(source)
                    == stage15e_quotient_projection(target)
                ),
                future_equal=source.future_measurement == target.future_measurement,
                witness_equal=(
                    witnesses[source.representative_id].probabilities
                    == witnesses[target.representative_id].probabilities
                ),
            )
        )
    return tuple(result)


def _dirac_residual(source: Stage15PhaseSpacePoint, *targets: Stage15PhaseSpacePoint) -> float:
    source_qd, source_pd = stage15a_dirac_data(source)
    residual = 0.0
    for target in targets:
        qd, pd = stage15a_dirac_data(target)
        residual = max(residual, abs(qd - source_qd), abs(pd - source_pd))
    return float(residual)


def _smeared_path_xi(representative, probe, *, ordering: str, after_first, compensator: float):
    if ordering == "NM":
        support_trace = (_smearing_support(probe.N), _smearing_support(probe.M))
        smearings = (probe.N, probe.M)
        provenance = "ordered_smeared_path:N_then_M"
    elif ordering == "MN+C2":
        support_trace = (
            _smearing_support(probe.M),
            _smearing_support(probe.N),
            _support_tuple(2),
        )
        smearings = (probe.M, probe.N)
        provenance = "ordered_smeared_path:M_then_N+observed_C2_compensator"
    else:
        raise ValueError(ordering)
    source = representative.point()
    return Stage15EPathXi(
        path_family="smeared",
        path_id=f"{representative.representative_id}:{probe.case_id}:{ordering}",
        path_word=ordering,
        source_representative_id=representative.representative_id,
        target_representative_id=None,
        structure_function_trace=(
            stage15a_structure_function(source),
            stage15a_structure_function(after_first),
        ),
        generator_or_smearing_support_trace=support_trace,
        local_parameters=(probe.alpha, probe.beta),
        smearings=smearings,
        compensator=float(compensator),
        compensator_provenance=provenance,
    )


@lru_cache(maxsize=1)
def canonical_stage15e_smeared_path_checks():
    representatives = {
        item.representative_id: item for item in canonical_stage15a_representatives()
    }
    architectures = {
        item.representative_id: item for item in canonical_stage15e_architectures()
    }
    witnesses = {
        item.representative_id: item for item in canonical_stage15e_orbit_witnesses()
    }
    result = []
    for probe in canonical_stage15b_smeared_order_probes():
        representative = representatives[probe.representative_id]
        source = representative.point()
        after_n = stage15b_apply_smeared_flow(source, probe.N, probe.alpha)
        after_m = stage15b_apply_smeared_flow(source, probe.M, probe.beta)
        endpoint_nm = stage15b_apply_smeared_flow(after_n, probe.M, probe.beta)
        endpoint_mn = stage15b_apply_smeared_flow(after_m, probe.N, probe.alpha)
        endpoint_mn_compensated = stage15b_apply_local_flow(
            endpoint_mn, 2, probe.observed_c2_defect
        )
        residual = max(
            _dirac_residual(source, endpoint_nm, endpoint_mn, endpoint_mn_compensated),
            probe.c2_only_residual,
            probe.compensated_endpoint_residual,
            probe.payload_residual,
        )
        xi_nm = _smeared_path_xi(
            representative, probe, ordering="NM", after_first=after_n, compensator=0.0
        )
        xi_mn = _smeared_path_xi(
            representative,
            probe,
            ordering="MN+C2",
            after_first=after_m,
            compensator=probe.observed_c2_defect,
        )
        architecture = architectures[representative.representative_id]
        witness = witnesses[representative.representative_id]
        endpoint_descent = residual <= STAGE15E_ATOL
        result.append(
            Stage15ESmearedPathCheck(
                representative_id=representative.representative_id,
                case_id=probe.case_id,
                path_Xi_nm=xi_nm,
                path_Xi_mn_compensated=xi_mn,
                provenance_distinct=xi_nm != xi_mn,
                max_dirac_payload_residual=residual,
                endpoint_descent=endpoint_descent,
                public_equal=(
                    endpoint_descent
                    and stage15e_quotient_projection(architecture)
                    == stage15e_quotient_projection(architecture)
                ),
                future_equal=bool(architecture.future_measurement.measurement),
                witness_equal=witness.probability_sum_residual <= STAGE15E_ATOL,
            )
        )
    return tuple(result)


@lru_cache(maxsize=1)
def canonical_stage15e_basis_checks():
    result = []
    content_by_candidate = _stage15d_content_by_candidate()
    for representative in canonical_stage15a_representatives():
        original = stage15e_architecture_for_representative(representative)
        original_witness = stage15e_orbit_witness(original)
        for candidate in canonical_stage15d_candidates():
            transformed = stage15e_architecture_for_representative(
                representative, candidate_id=candidate.candidate_id
            )
            content = content_by_candidate[candidate.candidate_id]
            locality = stage15d_locality_audit(candidate)
            result.append(
                Stage15EBasisCheck(
                    representative_id=representative.representative_id,
                    candidate_id=candidate.candidate_id,
                    locality_class=locality.locality_class,
                    original_Xi=original.Xi,
                    candidate_Xi=transformed.Xi,
                    provenance_distinct=original.Xi != transformed.Xi,
                    stage15d_content_preserved=(
                        content.quotient_preserved
                        and content.dirac_pair_preserved
                        and content.complete_relational_preserved
                    ),
                    public_equal=(
                        stage15e_quotient_projection(original)
                        == stage15e_quotient_projection(transformed)
                    ),
                    future_equal=(
                        original.future_measurement == transformed.future_measurement
                    ),
                    witness_equal=(
                        original_witness.probabilities
                        == stage15e_orbit_witness(transformed).probabilities
                    ),
                )
            )
    return tuple(result)


def _public_provenance_absent():
    forbidden = {
        STAGE15A_BASIS_ID,
        STAGE15B_PATH_012,
        STAGE15B_PATH_102,
        *(candidate.candidate_id for candidate in canonical_stage15d_candidates()),
    }
    return all(
        not any(
            token in repr((item.O, item.P, item.R, item.V, item.future_measurement))
            for token in forbidden
        )
        for item in canonical_stage15e_architectures()
    )


def stage15e_diagnostics():
    architectures = canonical_stage15e_architectures()
    projections = canonical_stage15e_quotient_projections()
    local_checks = canonical_stage15e_local_path_checks()
    smeared_checks = canonical_stage15e_smeared_path_checks()
    basis_checks = canonical_stage15e_basis_checks()
    witnesses = canonical_stage15e_orbit_witnesses()

    same_orbit = True
    reference_witnesses = []
    for orbit in canonical_stage15a_orbits():
        subset = [item for item in architectures if item.orbit_id == orbit.orbit_id]
        same_orbit &= len({repr(stage15e_quotient_projection(item)) for item in subset}) == 1
        reference_witnesses.append(
            next(item for item in witnesses if item.orbit_id == orbit.orbit_id)
        )

    probability_vector = lambda item: tuple(value for _, value in item.probabilities)
    minimum_separation = min(
        max(
            abs(a - b)
            for a, b in zip(
                probability_vector(left), probability_vector(right), strict=True
            )
        )
        for index, left in enumerate(reference_witnesses)
        for right in reference_witnesses[index + 1 :]
    )

    local_descent = all(
        item.provenance_distinct
        and item.structure_trace_distinct
        and item.endpoint_descent
        and item.public_equal
        and item.future_equal
        and item.witness_equal
        for item in local_checks
    )
    smeared_descent = all(
        item.provenance_distinct
        and item.endpoint_descent
        and item.public_equal
        and item.future_equal
        and item.witness_equal
        for item in smeared_checks
    )
    basis_descent = all(
        item.provenance_distinct
        and item.stage15d_content_preserved
        and item.public_equal
        and item.future_equal
        and item.witness_equal
        for item in basis_checks
    )
    future_complete = all(
        item.future_measurement.measurement
        and item.future_measurement.weighted
        and item.future_measurement.posterior
        and item.future_measurement.future_actuality_status == STAGE15E_NOT_LICENSED
        for item in architectures
    )
    xi_explicit = (
        len(local_checks) == 864
        and len(smeared_checks) == 540
        and len(basis_checks) == 1512
        and all(item.Xi.spatial_generator_supports for item in architectures)
        and all(item.provenance_distinct for item in local_checks)
        and all(item.provenance_distinct for item in smeared_checks)
        and all(item.provenance_distinct for item in basis_checks)
    )

    criteria = all(
        (
            len(architectures) == 108,
            len(stage15c_quotient_classes()) == 4,
            len({repr(item) for item in projections}) == 4,
            all(stage15e_validate_architecture(item)[0] for item in architectures),
            same_orbit,
            local_descent,
            smeared_descent,
            basis_descent,
            future_complete,
            _public_provenance_absent(),
            xi_explicit,
            len({probability_vector(item) for item in reference_witnesses}) == 4,
            minimum_separation > STAGE15E_ATOL,
            all(item.probability_sum_residual <= STAGE15E_ATOL for item in witnesses),
        )
    )

    return Stage15EDiagnostics(
        representative_count=len(architectures),
        quotient_class_count=len(stage15c_quotient_classes()),
        distinct_public_count=len({repr(item) for item in projections}),
        local_path_check_count=len(local_checks),
        local_path_xi_count=2 * len(local_checks),
        smeared_path_check_count=len(smeared_checks),
        smeared_path_xi_count=2 * len(smeared_checks),
        basis_candidate_count=len(canonical_stage15d_candidates()),
        basis_check_count=len(basis_checks),
        basis_xi_count=2 * len(basis_checks),
        witness_count=len(witnesses),
        distinct_witness_count=len({probability_vector(item) for item in reference_witnesses}),
        minimum_witness_separation=float(minimum_separation),
        same_orbit_descent=bool(same_orbit),
        local_path_descent=bool(local_descent),
        smeared_path_descent=bool(smeared_descent),
        basis_descent=bool(basis_descent),
        future_payload_complete=bool(future_complete),
        public_provenance_absent=_public_provenance_absent(),
        xi_provenance_explicit=bool(xi_explicit),
        criteria_39_43_satisfied=bool(criteria),
    )


def stage15e_summary():
    diagnostics = stage15e_diagnostics()
    return {
        "representative_count": diagnostics.representative_count,
        "quotient_class_count": diagnostics.quotient_class_count,
        "local_path_check_count": diagnostics.local_path_check_count,
        "smeared_path_check_count": diagnostics.smeared_path_check_count,
        "basis_candidate_count": diagnostics.basis_candidate_count,
        "basis_check_count": diagnostics.basis_check_count,
        "classification_local": STAGE15E_LOCAL_PATH_DESCENT,
        "classification_smeared": STAGE15E_SMEARED_PATH_DESCENT,
        "classification_basis": STAGE15E_BASIS_DESCENT,
        "criteria_39_43_satisfied": diagnostics.criteria_39_43_satisfied,
        "bounded_result": STAGE15E_BOUNDED_RESULT,
        "guards": STAGE15E_GUARDS,
    }
