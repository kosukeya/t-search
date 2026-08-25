from dataclasses import fields

from t_search.stage9_modal import FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_OTHER
from t_search.stage15_basis import (
    STAGE15D_L0,
    STAGE15D_L1,
    STAGE15D_L1_WITNESS_ID,
    STAGE15D_LFINITE,
    STAGE15D_NONLOCAL,
    canonical_stage15d_candidates,
)
from t_search.stage15_local import STAGE15A_BASIS_ID, canonical_stage15a_orbits
from t_search.stage15_measurement import (
    STAGE15E_BASIS_DESCENT,
    STAGE15E_BOUNDED_RESULT,
    STAGE15E_GUARDS,
    STAGE15E_LOCAL_PATH_DESCENT,
    STAGE15E_NOT_LICENSED,
    STAGE15E_SMEARED_PATH_DESCENT,
    Stage15EQuotientArchitecture,
    canonical_stage15e_architectures,
    canonical_stage15e_basis_checks,
    canonical_stage15e_local_path_checks,
    canonical_stage15e_orbit_witnesses,
    canonical_stage15e_quotient_projections,
    canonical_stage15e_smeared_path_checks,
    stage15e_diagnostics,
    stage15e_summary,
    stage15e_validate_architecture,
)
from t_search.stage15_paths import STAGE15B_PATH_012, STAGE15B_PATH_102


def _probability_vector(witness):
    return tuple(value for _, value in witness.probabilities)


def test_stage15e_criterion_39_builds_typed_architecture_and_keeps_provenance_in_xi():
    architectures = canonical_stage15e_architectures()
    assert len(architectures) == 108
    assert all(stage15e_validate_architecture(item)[0] for item in architectures)
    assert all(item.Xi.constraint_basis_id == STAGE15A_BASIS_ID for item in architectures)
    assert all(
        item.Xi.licensed_local_path_words == (STAGE15B_PATH_012, STAGE15B_PATH_102)
        for item in architectures
    )
    assert all(len(item.Xi.licensed_smeared_case_ids) == 5 for item in architectures)
    assert all(len(item.Xi.spatial_generator_supports) == 3 for item in architectures)
    assert all(item.P.qext_ids == ("h_L", "h_R") for item in architectures)
    assert all(
        item.Xi.outcome_correspondence
        == (
            (FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_LEFT),
            (FUTURE_SIGNATURE_OTHER, FUTURE_SIGNATURE_OTHER),
        )
        for item in architectures
    )

    public_fields = {field.name for field in fields(Stage15EQuotientArchitecture)}
    assert not public_fields & {
        "representative_id",
        "constraint_basis_id",
        "basis_family_id",
        "locality_class",
        "basis_transform_provenance",
        "representative_coordinates",
        "source_structure_function",
        "spatial_generator_supports",
        "path_word",
        "compensator",
    }


def test_stage15e_criterion_40_public_and_future_payloads_descend_to_four_by_twenty_seven_quotient():
    projections = canonical_stage15e_quotient_projections()
    assert len(projections) == 108
    assert len({repr(item) for item in projections}) == 4
    for orbit in canonical_stage15a_orbits():
        subset = [item for item in projections if item.orbit_id == orbit.orbit_id]
        assert len(subset) == 27
        assert len({repr(item) for item in subset}) == 1
        future = subset[0].future_measurement
        assert future.measurement and future.weighted and future.posterior
        assert future.future_actuality_status == STAGE15E_NOT_LICENSED


def test_stage15e_criterion_41_all_local_and_smeared_compensated_paths_descend_while_xi_remains_distinct():
    local = canonical_stage15e_local_path_checks()
    assert len(local) == 864
    assert all(item.path_Xi_012.path_word == STAGE15B_PATH_012 for item in local)
    assert all(item.path_Xi_102.path_word == STAGE15B_PATH_102 for item in local)
    assert all(item.provenance_distinct and item.structure_trace_distinct for item in local)
    assert all(item.endpoint_descent for item in local)
    assert all(item.public_equal and item.future_equal and item.witness_equal for item in local)
    assert all(item.classification == STAGE15E_LOCAL_PATH_DESCENT for item in local)

    smeared = canonical_stage15e_smeared_path_checks()
    assert len(smeared) == 540
    assert all(item.path_Xi_nm.path_word == "NM" for item in smeared)
    assert all(item.path_Xi_mn_compensated.path_word == "MN+C2" for item in smeared)
    assert all(item.provenance_distinct for item in smeared)
    assert all(item.endpoint_descent for item in smeared)
    assert all(item.public_equal and item.future_equal and item.witness_equal for item in smeared)
    assert all(item.max_dirac_payload_residual <= 1e-9 for item in smeared)
    assert all(item.classification == STAGE15E_SMEARED_PATH_DESCENT for item in smeared)


def test_stage15e_criterion_42_all_stage15d_equivalent_basis_candidates_preserve_public_future_payloads_while_xi_retains_basis_class():
    candidates = canonical_stage15d_candidates()
    checks = canonical_stage15e_basis_checks()
    assert len(candidates) == 14
    assert len(checks) == 14 * 108 == 1512
    assert {item.candidate_id for item in checks} == {item.candidate_id for item in candidates}
    assert all(item.original_Xi.constraint_basis_id == STAGE15A_BASIS_ID for item in checks)
    assert all(item.provenance_distinct for item in checks)
    assert all(item.stage15d_content_preserved for item in checks)
    assert all(item.public_equal and item.future_equal and item.witness_equal for item in checks)
    assert all(item.classification == STAGE15E_BASIS_DESCENT for item in checks)

    classes = {item.locality_class for item in checks}
    assert {STAGE15D_L0, STAGE15D_L1, STAGE15D_LFINITE, STAGE15D_NONLOCAL} <= classes
    witness = [item for item in checks if item.candidate_id == STAGE15D_L1_WITNESS_ID]
    assert len(witness) == 108
    assert all(item.locality_class == STAGE15D_L1 for item in witness)


def test_stage15e_criterion_43_future_measurement_family_and_orbit_witness_remain_bounded_and_discriminating():
    witnesses = canonical_stage15e_orbit_witnesses()
    assert len(witnesses) == 108
    references = []
    for orbit in canonical_stage15a_orbits():
        subset = [item for item in witnesses if item.orbit_id == orbit.orbit_id]
        assert len(subset) == 27
        assert len({_probability_vector(item) for item in subset}) == 1
        references.append(subset[0])
    assert len({_probability_vector(item) for item in references}) == 4
    separations = [
        max(
            abs(a - b)
            for a, b in zip(
                _probability_vector(left), _probability_vector(right), strict=True
            )
        )
        for index, left in enumerate(references)
        for right in references[index + 1 :]
    ]
    assert min(separations) > 1e-9
    assert all(item.probability_sum_residual <= 1e-9 for item in witnesses)
    assert all("not an empirical prediction" in item.semantics for item in witnesses)


def test_stage15e_diagnostics_close_criteria_39_through_43():
    diagnostics = stage15e_diagnostics()
    assert diagnostics.representative_count == 108
    assert diagnostics.quotient_class_count == 4
    assert diagnostics.distinct_public_count == 4
    assert diagnostics.local_path_check_count == 864
    assert diagnostics.local_path_xi_count == 1728
    assert diagnostics.smeared_path_check_count == 540
    assert diagnostics.smeared_path_xi_count == 1080
    assert diagnostics.basis_candidate_count == 14
    assert diagnostics.basis_check_count == 1512
    assert diagnostics.basis_xi_count == 3024
    assert diagnostics.witness_count == 108
    assert diagnostics.distinct_witness_count == 4
    assert diagnostics.minimum_witness_separation > 1e-9
    assert diagnostics.same_orbit_descent
    assert diagnostics.local_path_descent
    assert diagnostics.smeared_path_descent
    assert diagnostics.basis_descent
    assert diagnostics.future_payload_complete
    assert diagnostics.public_provenance_absent
    assert diagnostics.xi_provenance_explicit
    assert diagnostics.criteria_39_43_satisfied


def test_stage15e_summary_keeps_interpretation_boundaries_explicit():
    summary = stage15e_summary()
    assert summary["criteria_39_43_satisfied"]
    assert summary["bounded_result"] == STAGE15E_BOUNDED_RESULT
    guards = set(summary["guards"])
    for phrase in (
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
    ):
        assert phrase in guards
