import numpy as np

from t_search.stage5_clock_change import DEFAULT_ATOL
from t_search.stage9_modal import canonical_stage9_directional_carrier
from t_search.stage10_lift import canonical_stage10b_lifts
from t_search.stage10_transport import (
    audit_measurement_correspondence,
    canonical_stage10c_charts,
    direct_stage10_chart_measurement,
    stage10c_transport_diagnostics,
    transport_stage10_chart_measurement,
)


DIAGNOSTICS = stage10c_transport_diagnostics()


def test_stage10c_criterion24_valid_typed_measurement_exists_at_every_chart() -> None:
    charts = canonical_stage10c_charts()
    assert len(charts) == 18
    assert DIAGNOSTICS.qext_size == 2
    assert DIAGNOSTICS.charts_per_continuation == 9
    assert DIAGNOSTICS.total_charts == 18
    assert DIAGNOSTICS.all_chart_typing_valid
    assert DIAGNOSTICS.max_reference_support_normalization_residual <= 10 * DEFAULT_ATOL
    assert DIAGNOSTICS.max_reference_support_effect_residual <= 10 * DEFAULT_ATOL
    keys = {(chart.continuation_id, chart.clock, chart.clock_index) for chart in charts}
    assert len(keys) == 18


def test_stage10c_criterion25_all_genuine_ordered_distinct_clock_transports_are_tested() -> None:
    # 2 continuations * 6 ordered distinct clock pairs * 9 reading pairs.
    assert DIAGNOSTICS.genuine_measurement_transports == 108


def test_stage10c_criterion26_dual_transport_matches_direct_physical_reconstruction() -> None:
    assert DIAGNOSTICS.max_direct_transport_normalization_residual <= 100 * DEFAULT_ATOL
    assert DIAGNOSTICS.max_direct_transport_effect_residual <= 100 * DEFAULT_ATOL

    carrier = canonical_stage9_directional_carrier()
    lifts = {item.continuation_id: item for item in canonical_stage10b_lifts()}
    continuation = carrier.continuations[0]
    source = direct_stage10_chart_measurement(
        continuation, "A", 2, lift=lifts[continuation.continuation_id]
    )
    transported = transport_stage10_chart_measurement(source, continuation, "B", 1)
    reconstructed = direct_stage10_chart_measurement(
        continuation, "B", 1, lift=lifts[continuation.continuation_id]
    )
    assert np.allclose(
        transported.normalization_form,
        reconstructed.normalization_form,
        atol=100 * DEFAULT_ATOL,
        rtol=0.0,
    )
    for left, right in zip(transported.effects, reconstructed.effects, strict=True):
        assert left.outcome_id == right.outcome_id
        assert np.allclose(
            left.matrix, right.matrix, atol=100 * DEFAULT_ATOL, rtol=0.0
        )


def test_stage10c_criterion27_three_clock_compositions_match_direct_transport() -> None:
    # 2 continuations * 6 clock permutations * 27 reading triples.
    assert DIAGNOSTICS.three_clock_measurement_compositions == 324
    assert DIAGNOSTICS.max_composition_normalization_residual <= 100 * DEFAULT_ATOL
    assert DIAGNOSTICS.max_composition_effect_residual <= 100 * DEFAULT_ATOL


def test_stage10c_criterion28_completeness_is_covariant_in_operational_normalization() -> None:
    assert DIAGNOSTICS.max_completeness_residual <= 100 * DEFAULT_ATOL
    for chart in canonical_stage10c_charts():
        effect_sum = sum(
            (effect.matrix for effect in chart.effects),
            start=np.zeros_like(chart.normalization_form),
        )
        assert np.allclose(
            effect_sum,
            chart.normalization_form,
            atol=100 * DEFAULT_ATOL,
            rtol=0.0,
        )


def test_stage10c_criterion29_positivity_and_hermiticity_are_covariant() -> None:
    assert DIAGNOSTICS.max_hermiticity_residual <= 100 * DEFAULT_ATOL
    assert DIAGNOSTICS.minimum_effect_eigenvalue >= -100 * DEFAULT_ATOL
    assert DIAGNOSTICS.minimum_normalization_eigenvalue > DEFAULT_ATOL


def test_stage10c_criterion30_outcome_event_and_class_typing_remain_valid() -> None:
    preserving = audit_measurement_correspondence(
        event_kind="preserving", class_kind="preserving", outcome_kind="preserving"
    )
    assert preserving.valid
    assert preserving.event_roles_preserved
    assert preserving.class_correspondence_valid
    assert preserving.outcome_correspondence_bijective
    assert preserving.outcome_semantics_preserved
    assert DIAGNOSTICS.preserving_correspondence_valid
    assert DIAGNOSTICS.all_chart_typing_valid


def test_stage10c_criterion31_bare_effect_and_wrong_event_class_controls_are_rejected() -> None:
    wrong_event = audit_measurement_correspondence(
        event_kind="misdeclared-preserving",
        class_kind="preserving",
        outcome_kind="preserving",
    )
    wrong_class = audit_measurement_correspondence(
        event_kind="preserving",
        class_kind="swapped-classes",
        outcome_kind="preserving",
    )
    assert not wrong_event.valid
    assert not wrong_event.event_roles_preserved
    assert not wrong_class.valid
    assert not wrong_class.class_correspondence_valid
    assert DIAGNOSTICS.wrong_event_correspondence_rejected
    assert DIAGNOSTICS.wrong_class_correspondence_rejected
    assert DIAGNOSTICS.bare_effect_residual > 10 * DEFAULT_ATOL
    assert DIAGNOSTICS.bare_effect_rejected


def test_stage10c_does_not_preclaim_stage10d_probability_covariance() -> None:
    assert not DIAGNOSTICS.full_per_continuation_probability_covariance_established
