from t_search.stage5_clock_change import DEFAULT_ATOL
from t_search.stage10_probability import (
    stage10d_probability_diagnostics,
    stage10d_probe_family,
)


DIAGNOSTICS = stage10d_probability_diagnostics()


def test_stage10d_criterion32_per_continuation_probabilities_are_invariant_over_all_nodes() -> None:
    assert DIAGNOSTICS.continuation_count == 2
    assert DIAGNOSTICS.charts_per_continuation == 9
    assert DIAGNOSTICS.canonical_probability_evaluations == 36
    assert DIAGNOSTICS.max_pairwise_canonical_probability_residual <= 10 * DEFAULT_ATOL
    assert DIAGNOSTICS.per_continuation_probability_covariance


def test_stage10d_criterion33_every_chart_reproduces_stage9c_reference_likelihoods() -> None:
    assert DIAGNOSTICS.stage9c_reference_likelihood_covariance
    assert DIAGNOSTICS.max_stage9c_reference_probability_residual <= 10 * DEFAULT_ATOL
    assert DIAGNOSTICS.max_canonical_probability_sum_residual <= 10 * DEFAULT_ATOL
    assert DIAGNOSTICS.minimum_canonical_probability >= -10 * DEFAULT_ATOL
    assert DIAGNOSTICS.maximum_canonical_probability <= 1.0 + 10 * DEFAULT_ATOL
    assert DIAGNOSTICS.minimum_canonical_denominator > DEFAULT_ATOL


def test_stage10d_criterion34_covariance_is_per_continuation_before_weighting() -> None:
    assert DIAGNOSTICS.per_continuation_before_weighting
    assert not DIAGNOSTICS.branch_weight_aggregation_performed
    assert not DIAGNOSTICS.weighted_modal_update_covariance_established


def test_stage10d_criterion35_swapped_outcome_semantics_are_detected() -> None:
    assert DIAGNOSTICS.swapped_outcome_semantics_rejected
    assert DIAGNOSTICS.swapped_outcome_numeric_residual > 10 * DEFAULT_ATOL


def test_stage10d_criterion36_wrong_normalization_and_misaligned_metric_are_detected() -> None:
    assert DIAGNOSTICS.wrong_identity_normalization_rejected
    assert DIAGNOSTICS.misaligned_metric_rejected
    assert (
        DIAGNOSTICS.wrong_identity_normalization_probability_residual
        > 10 * DEFAULT_ATOL
        or DIAGNOSTICS.wrong_identity_normalization_sum_residual
        > 10 * DEFAULT_ATOL
    )
    assert DIAGNOSTICS.misaligned_metric_form_residual > 10 * DEFAULT_ATOL
    assert (
        DIAGNOSTICS.misaligned_metric_probability_residual
        > 10 * DEFAULT_ATOL
        or DIAGNOSTICS.misaligned_metric_sum_residual
        > 10 * DEFAULT_ATOL
    )


def test_stage10d_same_chart_physical_metric_relation_is_recorded_without_forcing_inequality() -> None:
    if DIAGNOSTICS.physical_metric_operational_normalization_numerically_coincident:
        assert DIAGNOSTICS.max_operational_physical_metric_form_residual <= 10 * DEFAULT_ATOL
    else:
        assert DIAGNOSTICS.max_operational_physical_metric_form_residual > 10 * DEFAULT_ATOL


def test_stage10d_criterion37_tomography_complete_probes_rule_out_accidental_equality() -> None:
    probes = stage10d_probe_family()
    expected = 14 + 2 * (14 * 13 // 2)
    assert len(probes) == expected == 196
    assert DIAGNOSTICS.probe_family_size == len(probes)
    assert DIAGNOSTICS.probe_states_in_physical_span
    assert DIAGNOSTICS.probe_probability_evaluations == 2 * expected * 9 * 2
    assert DIAGNOSTICS.max_probe_chart_covariance_residual <= 10 * DEFAULT_ATOL
    assert DIAGNOSTICS.max_probe_probability_sum_residual <= 10 * DEFAULT_ATOL
    assert DIAGNOSTICS.minimum_probe_probability >= -10 * DEFAULT_ATOL
    assert DIAGNOSTICS.maximum_probe_probability <= 1.0 + 10 * DEFAULT_ATOL
    assert DIAGNOSTICS.minimum_probe_denominator > DEFAULT_ATOL
    assert DIAGNOSTICS.accidental_canonical_equality_ruled_out


def test_stage10d_criterion38_measurement_covariance_status_is_explicitly_established() -> None:
    assert DIAGNOSTICS.completeness_probability_covariance
    assert DIAGNOSTICS.positivity_probability_covariance
    assert DIAGNOSTICS.per_continuation_probability_covariance
    assert DIAGNOSTICS.measurement_covariance_status == "established"
    # Weighted/modal/update covariance is a distinct Stage 10E boundary.
    assert not DIAGNOSTICS.weighted_modal_update_covariance_established
