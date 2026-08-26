from t_search.stage16_basis import (
    STAGE16D_CLASSIFICATION,
    STAGE16D_L0,
    STAGE16D_L1,
    STAGE16D_NONLOCAL,
    canonical_stage16d_candidates,
)
from t_search.stage16_measurement import (
    STAGE16E_BASIS_DESCENT,
    STAGE16E_BOUNDED_RESULT,
    STAGE16E_CYCLE_ORIENTATION,
    STAGE16E_GUARDS,
    STAGE16E_LOCAL_PATH_DESCENT,
    STAGE16E_SMEARED_PATH_DESCENT,
    canonical_stage16e_architectures,
    canonical_stage16e_basis_checks,
    canonical_stage16e_local_path_checks,
    canonical_stage16e_orbit_witnesses,
    canonical_stage16e_quotient_projections,
    canonical_stage16e_smeared_path_checks,
    stage16e_diagnostics,
    stage16e_quotient_projection,
    stage16e_summary,
    stage16e_validate_architecture,
)
from t_search.stage16_local import canonical_stage16a_orbits


def test_stage16e_typed_architectures_descend_to_four_public_payloads_with_four_clock_events():
    architectures = canonical_stage16e_architectures()
    assert len(architectures) == 324
    assert all(stage16e_validate_architecture(x)[0] for x in architectures)
    assert len({repr(x) for x in canonical_stage16e_quotient_projections()}) == 4
    for orbit in canonical_stage16a_orbits():
        subset = [x for x in architectures if x.orbit_id == orbit.orbit_id]
        assert len(subset) == 81
        assert len({repr(stage16e_quotient_projection(x)) for x in subset}) == 1
        assert len({x.Xi.representative_coordinates for x in subset}) == 81
        for architecture in subset:
            events = architecture.O.relational_events
            assert len(events) == 2
            assert events[0].stage10_event == "e1"
            assert events[1].stage10_event == "e2"
            assert abs(events[0].q_value - (orbit.Q_D - 2.0)) <= 1e-10
            assert abs(events[1].q_value - (orbit.Q_D + 2.0)) <= 1e-10
            assert architecture.Xi.cycle_orientation == STAGE16E_CYCLE_ORIENTATION
            assert architecture.Xi.stage16d_basis_search_classification == STAGE16D_CLASSIFICATION


def test_stage16e_inherited_measurement_weighted_and_posterior_payloads_are_complete_without_future_actuality():
    architectures = canonical_stage16e_architectures()
    assert all(x.future_measurement.measurement for x in architectures)
    assert all(x.future_measurement.weighted for x in architectures)
    assert all(x.future_measurement.posterior for x in architectures)
    assert all(x.future_measurement.future_actuality_status == "not_licensed" for x in architectures)
    assert all(x.future_measurement.empirical_claim_status == "not_licensed" for x in architectures)


def test_stage16e_local_path_descent_keeps_presented_compensator_provenance_in_xi():
    checks = canonical_stage16e_local_path_checks()
    assert len(checks) == 2592
    assert all(x.classification == STAGE16E_LOCAL_PATH_DESCENT for x in checks)
    assert all(x.provenance_distinct for x in checks)
    assert all(x.endpoint_descent for x in checks)
    assert all(x.public_equal for x in checks)
    assert all(x.future_equal for x in checks)
    assert all(x.witness_equal for x in checks)
    assert all(x.raw_Xi.compensator_type == "none" for x in checks)
    assert all(x.compensated_Xi.compensator_type == "presented_C_word_search" for x in checks)
    assert all(x.compensated_Xi.presented_compensator_word is not None for x in checks)
    assert all(x.compensated_Xi.presented_compensator_parameters is not None for x in checks)


def test_stage16e_smeared_path_descent_keeps_global_seed_compensation_in_xi_only():
    checks = canonical_stage16e_smeared_path_checks()
    assert len(checks) == 2592
    assert all(x.classification == STAGE16E_SMEARED_PATH_DESCENT for x in checks)
    assert all(x.provenance_distinct for x in checks)
    assert all(x.endpoint_descent for x in checks)
    assert all(x.public_equal for x in checks)
    assert all(x.future_equal for x in checks)
    assert all(x.witness_equal for x in checks)
    assert all(x.nm_Xi.compensator_type == "none" for x in checks)
    assert all(x.mn_compensated_Xi.compensator_type == "global_seed_oracle" for x in checks)


def test_stage16e_basis_and_locality_depth_provenance_descend_across_all_explicit_stage16d_candidates():
    checks = canonical_stage16e_basis_checks()
    candidates = canonical_stage16d_candidates()
    assert len(candidates) == 21
    assert len(checks) == 324 * 21
    assert all(x.classification == STAGE16E_BASIS_DESCENT for x in checks)
    assert all(x.provenance_distinct for x in checks)
    assert all(x.stage16d_content_preserved for x in checks)
    assert all(x.public_equal for x in checks)
    assert all(x.future_equal for x in checks)
    assert all(x.witness_equal for x in checks)
    assert {x.locality_class for x in checks} == {STAGE16D_L0, STAGE16D_L1, STAGE16D_NONLOCAL}
    assert {x.lfinite_depth for x in checks} >= {None, 1}
    assert all(x.candidate_Xi.stage16d_basis_search_classification == STAGE16D_CLASSIFICATION for x in checks)


def test_stage16e_orbit_witness_is_representative_and_basis_independent_but_orbit_sensitive():
    witnesses = canonical_stage16e_orbit_witnesses()
    assert len(witnesses) == 324
    reference = []
    for orbit in canonical_stage16a_orbits():
        subset = [x for x in witnesses if x.orbit_id == orbit.orbit_id]
        assert len(subset) == 81
        assert len({x.probabilities for x in subset}) == 1
        assert all(x.probability_sum_residual <= 1e-10 for x in subset)
        reference.append(subset[0])
    assert len({x.probabilities for x in reference}) == 4
    vectors = [tuple(v for _, v in x.probabilities) for x in reference]
    minimum = min(
        max(abs(a - b) for a, b in zip(left, right, strict=True))
        for index, left in enumerate(vectors)
        for right in vectors[index + 1:]
    )
    assert minimum > 1e-3


def test_stage16e_diagnostics_close_only_criteria_40_44_and_preserve_guards():
    d = stage16e_diagnostics()
    assert d.representative_count == 324
    assert d.quotient_class_count == 4
    assert d.distinct_public_count == 4
    assert d.local_path_check_count == 2592
    assert d.local_path_xi_count == 5184
    assert d.smeared_path_check_count == 2592
    assert d.smeared_path_xi_count == 5184
    assert d.basis_candidate_count == 21
    assert d.basis_check_count == 6804
    assert d.basis_xi_count == 13608
    assert d.witness_count == 324
    assert d.distinct_witness_count == 4
    assert d.minimum_witness_separation > 1e-3
    assert d.same_orbit_descent
    assert d.local_path_descent
    assert d.smeared_path_descent
    assert d.basis_depth_descent
    assert d.future_payload_complete
    assert d.public_provenance_absent
    assert d.xi_provenance_explicit
    assert d.criteria_40_44_satisfied
    summary = stage16e_summary()
    assert summary["criteria_40_44_satisfied"]
    assert summary["bounded_result"] == STAGE16E_BOUNDED_RESULT
    guards = set(STAGE16E_GUARDS)
    for expected in (
        "future-measurement covariance != future actuality",
        "path-independent evidence update != ontological becoming",
        "typed operational descent != ontological equivalence",
        "Potentiality != quantum randomness by definition",
        "only nonlocal witness found in frozen search != fundamental physical non-Abelianity",
        "repository validation != new scientific evidence",
    ):
        assert expected in guards
