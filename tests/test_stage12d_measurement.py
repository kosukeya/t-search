import numpy as np

from t_search.stage9_modal import FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_OTHER
from t_search.stage11_measurement import STAGE11D_REFERENCE_CLOCK, STAGE11D_REFERENCE_CLOCK_INDEX
from t_search.stage11_parametrized import STAGE11A_IDENTITY
from t_search.stage12_measurement import (
    STAGE12D_ATOL,
    STAGE12D_FALSE_POSITIVE_REJECTED,
    STAGE12D_NORMALIZATION_REJECTION,
    STAGE12D_ORBIT_WITNESS_SEMANTICS,
    STAGE12D_TYPED_REJECTION,
    canonical_stage12d_architectures,
    canonical_stage12d_measurement_views,
    canonical_stage12d_orbit_witnesses,
    canonical_stage12d_posterior_views,
    canonical_stage12d_quotient_projections,
    canonical_stage12d_weighted_views,
    stage12d_controls,
    stage12d_diagnostics,
    stage12d_quotient_projection,
    stage12d_summary,
    stage12d_validate_architecture,
)
from t_search.stage12_multi_orbit import canonical_stage12a_orbits


def _probabilities(item):
    return tuple(value for _, value in item.probabilities)


def test_stage12d_lifts_typed_oprvxi_to_every_gauge_representative() -> None:
    architectures = canonical_stage12d_architectures()
    assert len(architectures) == 20
    assert {item.orbit_id for item in architectures} == {
        orbit.orbit_id for orbit in canonical_stage12a_orbits()
    }
    assert all(item.Xi.parameterization_id == STAGE11A_IDENTITY for item in architectures)
    assert all(item.Xi.orbit_id == item.orbit_id for item in architectures)
    assert all(item.Xi.quotient_id == item.quotient_id for item in architectures)
    assert all(item.Xi.representative_id == item.representative_id for item in architectures)
    assert all(stage12d_validate_architecture(item).valid for item in architectures)
    assert all(item.P.qext_ids == ("h_L", "h_R") for item in architectures)
    assert all(
        item.Xi.outcome_correspondence
        == (
            (FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_LEFT),
            (FUTURE_SIGNATURE_OTHER, FUTURE_SIGNATURE_OTHER),
        )
        for item in architectures
    )


def test_stage12d_within_orbit_quotient_projection_preserves_typed_oprv_content() -> None:
    projections = canonical_stage12d_quotient_projections()
    assert len(projections) == 20
    assert len(set(projections)) == 4
    for orbit in canonical_stage12a_orbits():
        subset = [item for item in projections if item.orbit_id == orbit.orbit_id]
        assert len(subset) == 5
        assert len(set(subset)) == 1
        assert subset[0] == stage12d_quotient_projection(
            next(
                item
                for item in canonical_stage12d_architectures()
                if item.orbit_id == orbit.orbit_id
            )
        )


def test_stage12d_relational_O_is_orbit_sensitive_but_representative_independent_with_tolerance() -> None:
    architectures = canonical_stage12d_architectures()
    quotient_signatures = {}
    for orbit in canonical_stage12a_orbits():
        subset = [item for item in architectures if item.orbit_id == orbit.orbit_id]
        assert len(subset) == 5
        reference = subset[0].O.relational_events
        for item in subset[1:]:
            assert len(item.O.relational_events) == len(reference)
            for left, right in zip(reference, item.O.relational_events, strict=True):
                assert left.role == right.role
                assert left.stage10_event == right.stage10_event
                assert left.physical_event_id == right.physical_event_id
                assert np.isclose(left.clock_value, right.clock_value, atol=STAGE12D_ATOL, rtol=0.0)
                assert np.isclose(left.q_value, right.q_value, atol=STAGE12D_ATOL, rtol=0.0)

        quotient = stage12d_quotient_projection(subset[0])
        quotient_signatures[orbit.orbit_id] = tuple(
            (event.clock_value, event.q_value) for event in quotient.O.relational_events
        )
    assert len(set(quotient_signatures.values())) == 4


def test_stage12d_inherited_future_measurement_descends_within_each_orbit() -> None:
    views = canonical_stage12d_measurement_views()
    assert len(views) == 40
    assert sum(len(item.probabilities) for item in views) == 80
    assert all(item.internal_clock == STAGE11D_REFERENCE_CLOCK for item in views)
    assert all(item.internal_clock_index == STAGE11D_REFERENCE_CLOCK_INDEX for item in views)
    assert all(item.outcome_ids == (FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_OTHER) for item in views)
    assert max(item.probability_sum_residual for item in views) <= 1e-9
    assert max(item.completeness_residual for item in views) <= 1e-9
    assert min(item.minimum_effect_eigenvalue for item in views) >= -1e-9
    assert min(item.minimum_normalization_eigenvalue for item in views) > 1e-9
    assert min(item.normalization_denominator for item in views) > 1e-9

    for orbit in canonical_stage12a_orbits():
        for continuation in ("h_L", "h_R"):
            subset = [
                item
                for item in views
                if item.orbit_id == orbit.orbit_id and item.continuation_id == continuation
            ]
            assert len(subset) == 5
            reference = dict(subset[0].probabilities)
            assert all(
                max(abs(dict(item.probabilities)[key] - reference[key]) for key in reference)
                <= 1e-9
                for item in subset
            )


def test_stage12d_weighted_and_posterior_public_outputs_descend_within_each_orbit() -> None:
    weighted = canonical_stage12d_weighted_views()
    posterior = canonical_stage12d_posterior_views()
    assert len(weighted) == 20
    assert len(posterior) == 20
    for orbit in canonical_stage12a_orbits():
        weighted_subset = [item for item in weighted if item.orbit_id == orbit.orbit_id]
        posterior_subset = [item for item in posterior if item.orbit_id == orbit.orbit_id]
        assert len(weighted_subset) == 5
        assert len(posterior_subset) == 5
        assert len({item.next_probabilities for item in weighted_subset}) == 1
        assert len({item.epistemic_posterior_weights for item in posterior_subset}) == 1
        assert len({item.ontic_posterior_weights for item in posterior_subset}) == 1
        assert all(item.ontic_no_selected_complete_continuation_datum for item in posterior_subset)


def test_stage12d_orbit_sensitive_witness_is_gauge_invariant_and_distinguishes_all_four_orbits() -> None:
    witnesses = canonical_stage12d_orbit_witnesses()
    assert len(witnesses) == 20
    assert all(item.semantics == STAGE12D_ORBIT_WITNESS_SEMANTICS for item in witnesses)
    assert all(item.probability_sum_residual <= STAGE12D_ATOL for item in witnesses)
    assert all(
        tuple(name for name, _ in item.probabilities)
        == (FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_OTHER)
        for item in witnesses
    )

    references = []
    for orbit in canonical_stage12a_orbits():
        subset = [item for item in witnesses if item.orbit_id == orbit.orbit_id]
        assert len(subset) == 5
        assert len({item.probabilities for item in subset}) == 1
        assert len({round(item.Q_D, 12) for item in subset}) == 1
        assert len({round(item.P_D, 12) for item in subset}) == 1
        assert len({round(item.relational_q_target, 12) for item in subset}) == 1
        references.append(subset[0])

    signatures = {_probabilities(item) for item in references}
    assert len(signatures) == 4
    separations = [
        max(
            abs(a - b)
            for a, b in zip(_probabilities(left), _probabilities(right), strict=True)
        )
        for index, left in enumerate(references)
        for right in references[index + 1 :]
    ]
    assert min(separations) > 1e-9


def test_stage12d_wrong_context_and_trivialization_controls_are_rejected() -> None:
    controls = stage12d_controls()
    assert len(controls) == 6
    assert all(item.rejected for item in controls)
    by_id = {item.control_id: item for item in controls}
    for control_id in (
        "wrong_orbit_correspondence",
        "wrong_event_correspondence",
        "wrong_class_correspondence",
        "wrong_outcome_correspondence",
    ):
        assert by_id[control_id].classification == STAGE12D_TYPED_REJECTION
    assert by_id["wrong_normalization"].classification == STAGE12D_NORMALIZATION_REJECTION
    assert by_id["wrong_normalization"].numerical_witness_residual > 1e-9
    assert (
        by_id["orbit_insensitive_measurement_clone"].classification
        == STAGE12D_FALSE_POSITIVE_REJECTED
    )
    assert by_id["orbit_insensitive_measurement_clone"].numerical_witness_residual == 3.0


def test_stage12d_diagnostics_close_criteria_32_through_38() -> None:
    d = stage12d_diagnostics()
    assert d.physical_orbit_count == 4
    assert d.representative_count == 20
    assert d.quotient_class_count == 4
    assert d.architecture_view_count == 20
    assert d.distinct_quotient_architecture_count == 4
    assert d.measurement_view_count == 40
    assert d.probability_evaluation_count == 80
    assert d.weighted_public_view_count == 20
    assert d.posterior_view_count == 20
    assert d.orbit_witness_count == 20
    assert d.distinct_orbit_witness_count == 4
    assert d.max_same_orbit_architecture_residual <= STAGE12D_ATOL
    assert d.max_same_orbit_measurement_probability_residual <= 1e-9
    assert d.max_same_orbit_weighted_probability_residual <= 1e-9
    assert d.max_same_orbit_posterior_residual <= 1e-9
    assert d.max_same_orbit_witness_residual <= STAGE12D_ATOL
    assert d.minimum_cross_orbit_witness_separation > 1e-9
    assert d.matched_epistemic_ontic_public_architecture
    assert d.public_schema_selector_free
    assert d.control_count == 6
    assert d.rejected_control_count == 6
    assert d.criteria_32_38_satisfied


def test_stage12d_summary_keeps_interpretive_boundaries_explicit() -> None:
    summary = stage12d_summary()
    assert summary["criteria_32_38_satisfied"]
    assert summary["bounded_result"].endswith("= established")
    assert summary["distinct_orbit_witness_count"] == 4
    assert summary["rejected_control_count"] == 6
    guards = set(summary["guards"])
    assert (
        "same gauge-invariant probability within an orbit != all physical orbits operationally identical"
        in guards
    )
    assert (
        "typed bridge to orbit data != dynamical derivation of quantum measurement from the classical constraint"
        in guards
    )
    assert "future-measurement covariance != future actuality" in guards
