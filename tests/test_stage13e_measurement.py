from dataclasses import fields

from t_search.stage9_modal import FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_OTHER
from t_search.stage13_multi_constraint import STAGE13A_BASIS_ID, canonical_stage13a_orbits
from t_search.stage13_paths import (
    STAGE13B_PHI_T,
    STAGE13B_PHI_X,
    STAGE13B_TEMPORAL_ORDER_STATUS,
)
from t_search.stage13_measurement import (
    STAGE13E_ATOL,
    STAGE13E_BOUNDED_RESULT,
    STAGE13E_NORMALIZATION_REJECTION,
    STAGE13E_ORBIT_WITNESS_SEMANTICS,
    STAGE13E_PATH_DESCENT_CLASSIFICATION,
    STAGE13E_REPRESENTATIVE_CORRUPTION_REJECTED,
    STAGE13E_TYPED_REJECTION,
    STAGE13E_WRONG_PATH_REJECTION,
    Stage13EQuotientArchitecture,
    canonical_stage13e_architectures,
    canonical_stage13e_compensated_operational_descent_checks,
    canonical_stage13e_measurement_views,
    canonical_stage13e_orbit_witnesses,
    canonical_stage13e_posterior_views,
    canonical_stage13e_quotient_projections,
    canonical_stage13e_weighted_views,
    stage13e_controls,
    stage13e_diagnostics,
    stage13e_summary,
    stage13e_validate_architecture,
)


def _probabilities(item):
    return tuple(value for _, value in item.probabilities)


def test_stage13e_lifts_oprvxi_to_all_36_representatives_with_path_basis_provenance_only_in_xi():
    architectures = canonical_stage13e_architectures()
    assert len(architectures) == 36
    assert all(stage13e_validate_architecture(item)[0] for item in architectures)
    assert all(item.Xi.constraint_basis_id == STAGE13A_BASIS_ID for item in architectures)
    assert all(
        item.Xi.licensed_path_words
        == ((STAGE13B_PHI_T, STAGE13B_PHI_X), (STAGE13B_PHI_X, STAGE13B_PHI_T))
        for item in architectures
    )
    assert all(item.P.qext_ids == ("h_L", "h_R") for item in architectures)
    assert all(
        item.Xi.outcome_correspondence
        == (
            (FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_LEFT),
            (FUTURE_SIGNATURE_OTHER, FUTURE_SIGNATURE_OTHER),
        )
        for item in architectures
    )
    public_fields = {item.name for item in fields(Stage13EQuotientArchitecture)}
    assert not public_fields & {
        "representative_id",
        "constraint_basis_id",
        "path_word",
        "path_word_role",
        "licensed_path_words",
        "s",
        "u",
        "representative_T",
        "representative_X",
    }


def test_stage13e_quotient_projection_is_representative_independent_and_retains_four_physical_classes():
    projections = canonical_stage13e_quotient_projections()
    assert len(projections) == 36
    assert len(set(projections)) == 4
    for orbit in canonical_stage13a_orbits():
        subset = [item for item in projections if item.orbit_id == orbit.orbit_id]
        assert len(subset) == 9
        assert len(set(subset)) == 1
    signatures = {
        item.orbit_id: tuple((e.clock_value, round(e.q_value, 12)) for e in item.O.relational_events)
        for item in projections[::9]
    }
    assert len(set(signatures.values())) == 4


def test_stage13e_inherited_future_measurement_weighted_and_posterior_payloads_descend_within_orbits():
    measurements = canonical_stage13e_measurement_views()
    weighted = canonical_stage13e_weighted_views()
    posterior = canonical_stage13e_posterior_views()
    assert len(measurements) == 72
    assert sum(len(item.probabilities) for item in measurements) == 144
    assert len(weighted) == 36
    assert len(posterior) == 36
    assert max(item.probability_sum_residual for item in measurements) <= 1e-9
    assert max(item.completeness_residual for item in measurements) <= 1e-9
    assert min(item.minimum_effect_eigenvalue for item in measurements) >= -1e-9
    assert min(item.minimum_normalization_eigenvalue for item in measurements) > 1e-9
    assert min(item.normalization_denominator for item in measurements) > 1e-9

    for orbit in canonical_stage13a_orbits():
        for continuation in ("h_L", "h_R"):
            subset = [
                item for item in measurements
                if item.orbit_id == orbit.orbit_id and item.continuation_id == continuation
            ]
            assert len(subset) == 9
            assert len({item.probabilities for item in subset}) == 1
        w_subset = [item for item in weighted if item.orbit_id == orbit.orbit_id]
        p_subset = [item for item in posterior if item.orbit_id == orbit.orbit_id]
        assert len(w_subset) == 9 and len({item.next_probabilities for item in w_subset}) == 1
        assert len(p_subset) == 9
        assert len({item.epistemic_posterior_weights for item in p_subset}) == 1
        assert len({item.ontic_posterior_weights for item in p_subset}) == 1


def test_stage13e_two_clock_orbit_sensitive_witness_is_rep_and_path_independent_but_orbit_discriminating():
    witnesses = canonical_stage13e_orbit_witnesses()
    assert len(witnesses) == 36
    assert all(item.target_tau == 1.0 and item.target_chi == 1.0 for item in witnesses)
    assert all(item.semantics == STAGE13E_ORBIT_WITNESS_SEMANTICS for item in witnesses)
    references = []
    for orbit in canonical_stage13a_orbits():
        subset = [item for item in witnesses if item.orbit_id == orbit.orbit_id]
        assert len(subset) == 9
        assert len({item.probabilities for item in subset}) == 1
        assert len({round(item.Q_D, 12) for item in subset}) == 1
        assert len({round(item.P_D, 12) for item in subset}) == 1
        assert len({round(item.relational_q_target, 12) for item in subset}) == 1
        references.append(subset[0])
    assert len({_probabilities(item) for item in references}) == 4
    separations = [
        max(abs(a - b) for a, b in zip(_probabilities(left), _probabilities(right), strict=True))
        for index, left in enumerate(references)
        for right in references[index + 1:]
    ]
    assert min(separations) > 1e-9


def test_stage13e_all_144_compensated_path_pairs_preserve_public_operational_payloads():
    checks = canonical_stage13e_compensated_operational_descent_checks()
    assert len(checks) == 144
    assert all(item.path_Xi_TX.path_word == (STAGE13B_PHI_T, STAGE13B_PHI_X) for item in checks)
    assert all(item.path_Xi_XT.path_word == (STAGE13B_PHI_X, STAGE13B_PHI_T) for item in checks)
    assert all(item.path_provenance_distinct for item in checks)
    assert all(item.path_Xi_TX.temporal_order_status == STAGE13B_TEMPORAL_ORDER_STATUS for item in checks)
    assert all(item.path_Xi_XT.temporal_order_status == STAGE13B_TEMPORAL_ORDER_STATUS for item in checks)
    assert all(item.classification == STAGE13E_PATH_DESCENT_CLASSIFICATION for item in checks)
    assert max(item.public_architecture_residual for item in checks) <= STAGE13E_ATOL
    assert max(item.measurement_probability_residual for item in checks) <= 1e-9
    assert max(item.weighted_probability_residual for item in checks) <= 1e-9
    assert max(item.posterior_residual for item in checks) <= 1e-9
    assert max(item.witness_residual for item in checks) <= STAGE13E_ATOL
    assert sum(item.measurement_evaluation_count for item in checks) == 576


def test_stage13e_wrong_context_path_normalization_and_representative_corruption_controls_are_rejected():
    controls = stage13e_controls()
    assert len(controls) == 10
    assert all(item.rejected for item in controls)
    by_id = {item.control_id: item for item in controls}
    for control_id in ("wrong_event_correspondence", "wrong_class_correspondence", "wrong_outcome_correspondence"):
        assert by_id[control_id].classification == STAGE13E_TYPED_REJECTION
    assert by_id["wrong_path_correspondence"].classification == STAGE13E_WRONG_PATH_REJECTION
    assert by_id["wrong_path_correspondence"].numerical_witness_residual > STAGE13E_ATOL
    assert by_id["wrong_normalization"].classification == STAGE13E_NORMALIZATION_REJECTION
    assert by_id["wrong_normalization"].numerical_witness_residual > 1e-9
    for control_id in (
        "representative_dependent_O",
        "representative_dependent_P",
        "representative_dependent_R",
        "representative_dependent_V",
        "representative_dependent_measurement",
    ):
        assert by_id[control_id].classification == STAGE13E_REPRESENTATIVE_CORRUPTION_REJECTED


def test_stage13e_diagnostics_close_criteria_39_through_43():
    d = stage13e_diagnostics()
    assert d.physical_orbit_count == 4
    assert d.representative_count == 36
    assert d.quotient_class_count == 4
    assert d.architecture_view_count == 36
    assert d.distinct_quotient_architecture_count == 4
    assert d.measurement_view_count == 72
    assert d.probability_evaluation_count == 144
    assert d.weighted_view_count == 36
    assert d.posterior_view_count == 36
    assert d.orbit_witness_count == 36
    assert d.distinct_orbit_witness_count == 4
    assert d.compensated_path_check_count == 144
    assert d.path_xi_view_count == 288
    assert d.compensated_measurement_evaluation_count == 576
    assert d.minimum_cross_orbit_witness_separation > 1e-9
    assert d.max_compensated_public_architecture_residual <= 1e-9
    assert d.max_compensated_measurement_probability_residual <= 1e-9
    assert d.max_compensated_weighted_probability_residual <= 1e-9
    assert d.max_compensated_posterior_residual <= 1e-9
    assert d.max_compensated_witness_residual <= 1e-9
    assert d.public_path_basis_provenance_absent
    assert d.path_xi_provenance_explicit
    assert d.control_count == 10
    assert d.rejected_control_count == 10
    assert d.criteria_39_43_satisfied


def test_stage13e_summary_keeps_interpretive_boundaries_explicit():
    summary = stage13e_summary()
    assert summary["criteria_39_43_satisfied"]
    assert summary["bounded_result"] == STAGE13E_BOUNDED_RESULT
    guards = set(summary["guards"])
    assert "path-specific Xi provenance != quotient-level physical content" in guards
    assert "path word != modal continuation" in guards
    assert "path word != physical temporal history" in guards
    assert "compensated-path operational descent != refoliation invariance" in guards
    assert "future-measurement covariance != future actuality" in guards
    assert "orbit-sensitive witness != empirical prediction" in guards
