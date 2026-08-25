from dataclasses import fields

from t_search.stage9_modal import FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_OTHER
from t_search.stage14_basis import STAGE14D_TRIANGULAR_BASIS_ID
from t_search.stage14_measurement import (
    STAGE14E_BASIS_CORRUPTION,
    STAGE14E_BASIS_DESCENT_CLASSIFICATION,
    STAGE14E_BOUNDED_RESULT,
    STAGE14E_PATH_CORRUPTION,
    STAGE14E_PATH_DESCENT_CLASSIFICATION,
    STAGE14E_REPRESENTATIVE_CORRUPTION,
    Stage14EQuotientArchitecture,
    canonical_stage14e_architectures,
    canonical_stage14e_basis_descent_checks,
    canonical_stage14e_orbit_witnesses,
    canonical_stage14e_path_descent_checks,
    canonical_stage14e_quotient_projections,
    stage14e_controls,
    stage14e_diagnostics,
    stage14e_summary,
    stage14e_validate_architecture,
)
from t_search.stage14_paths import STAGE14B_PATH_12D, STAGE14B_PATH_21D
from t_search.stage14_structure_function import STAGE14A_BASIS_ID, canonical_stage14a_orbits


def _pv(w):
    return tuple(value for _, value in w.probabilities)


def test_stage14e_builds_108_typed_architectures_with_public_provenance_separation():
    items = canonical_stage14e_architectures()
    assert len(items) == 108
    assert all(stage14e_validate_architecture(item)[0] for item in items)
    assert all(item.Xi.constraint_basis_id == STAGE14A_BASIS_ID for item in items)
    assert all(item.Xi.licensed_path_words == (STAGE14B_PATH_12D, STAGE14B_PATH_21D) for item in items)
    assert all(item.P.qext_ids == ("h_L", "h_R") for item in items)
    assert all(item.Xi.outcome_correspondence == ((FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_LEFT), (FUTURE_SIGNATURE_OTHER, FUTURE_SIGNATURE_OTHER)) for item in items)
    public_fields = {f.name for f in fields(Stage14EQuotientArchitecture)}
    assert not public_fields & {"representative_id", "constraint_basis_id", "path_word", "s", "u", "v", "source_structure_functions"}


def test_stage14e_public_and_future_payloads_descend_to_four_by_twenty_seven_quotient():
    projections = canonical_stage14e_quotient_projections()
    assert len(projections) == 108
    assert len({repr(item) for item in projections}) == 4
    for orbit in canonical_stage14a_orbits():
        subset = [item for item in projections if item.orbit_id == orbit.orbit_id]
        assert len(subset) == 27
        assert len({repr(item) for item in subset}) == 1
        future = subset[0].future_measurement
        assert future.measurement and future.weighted and future.posterior


def test_stage14e_orbit_sensitive_witness_is_rep_independent_and_discriminating():
    witnesses = canonical_stage14e_orbit_witnesses()
    assert len(witnesses) == 108
    refs = []
    for orbit in canonical_stage14a_orbits():
        subset = [item for item in witnesses if item.orbit_id == orbit.orbit_id]
        assert len(subset) == 27
        assert len({_pv(item) for item in subset}) == 1
        refs.append(subset[0])
    assert len({_pv(item) for item in refs}) == 4
    separations = [max(abs(a-b) for a,b in zip(_pv(left),_pv(right),strict=True)) for i,left in enumerate(refs) for right in refs[i+1:]]
    assert min(separations) > 1e-9
    assert all(item.probability_sum_residual <= 1e-9 for item in witnesses)
    assert all("not an empirical prediction" in item.semantics for item in witnesses)


def test_stage14e_all_864_structure_function_paths_preserve_public_and_future_payloads_while_xi_differs():
    checks = canonical_stage14e_path_descent_checks()
    assert len(checks) == 864
    assert all(item.path_Xi_12D.path_word == STAGE14B_PATH_12D for item in checks)
    assert all(item.path_Xi_21D.path_word == STAGE14B_PATH_21D for item in checks)
    assert all(item.provenance_distinct and item.trace_distinct for item in checks)
    assert all(item.path_Xi_12D.compensator_provenance.endswith("v_12D") for item in checks)
    assert all(item.path_Xi_21D.compensator_provenance.endswith("v_21D") for item in checks)
    assert all(item.public_equal and item.future_equal and item.witness_equal for item in checks)
    assert all(item.classification == STAGE14E_PATH_DESCENT_CLASSIFICATION for item in checks)


def test_stage14e_all_108_original_triangular_basis_correspondences_preserve_public_payloads_while_xi_differs():
    checks = canonical_stage14e_basis_descent_checks()
    assert len(checks) == 108
    assert all(item.original_Xi.constraint_basis_id == STAGE14A_BASIS_ID for item in checks)
    assert all(item.triangular_Xi.constraint_basis_id == STAGE14D_TRIANGULAR_BASIS_ID for item in checks)
    assert all(item.provenance_distinct for item in checks)
    assert all(item.public_equal and item.future_equal and item.witness_equal for item in checks)
    assert all(item.classification == STAGE14E_BASIS_DESCENT_CLASSIFICATION for item in checks)


def test_stage14e_rep_path_basis_payload_corruption_controls_are_rejected():
    controls = stage14e_controls()
    assert len(controls) == 3
    assert all(item.rejected for item in controls)
    by_id = {item.control_id: item for item in controls}
    assert by_id["representative_dependent_public_payload"].classification == STAGE14E_REPRESENTATIVE_CORRUPTION
    assert by_id["path_dependent_future_measurement_payload"].classification == STAGE14E_PATH_CORRUPTION
    assert by_id["basis_dependent_future_measurement_payload"].classification == STAGE14E_BASIS_CORRUPTION


def test_stage14e_diagnostics_close_criteria_39_through_43():
    d = stage14e_diagnostics()
    assert d.representative_count == 108
    assert d.quotient_class_count == 4 and d.distinct_public_count == 4
    assert d.path_check_count == 864 and d.path_xi_count == 1728
    assert d.basis_check_count == 108 and d.basis_xi_count == 216
    assert d.witness_count == 108 and d.distinct_witness_count == 4
    assert d.minimum_witness_separation > 1e-9
    assert d.same_orbit_descent and d.path_descent and d.basis_descent
    assert d.public_provenance_absent and d.xi_provenance_explicit
    assert d.control_count == 3 and d.rejected_control_count == 3
    assert d.criteria_39_43_satisfied


def test_stage14e_summary_keeps_interpretation_boundaries_explicit():
    summary = stage14e_summary()
    assert summary["criteria_39_43_satisfied"]
    assert summary["bounded_result"] == STAGE14E_BOUNDED_RESULT
    guards = set(summary["guards"])
    for phrase in (
        "structure-function/path Xi provenance != quotient-level physical content",
        "basis-specific Xi provenance != quotient-level physical content",
        "path word != physical temporal history",
        "path word != modal continuation",
        "compensated-path operational descent != refoliation invariance",
        "basis-equivalent operational descent != refoliation invariance",
        "future-measurement covariance != future actuality",
        "orbit-sensitive witness != empirical prediction",
        "basis equivalence != general relativity",
        "finite-model success != empirical discovery",
    ):
        assert phrase in guards
