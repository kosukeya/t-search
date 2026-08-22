import numpy as np
import pytest

from t_search.stage5_clock_change import DEFAULT_ATOL
from t_search.stage9_modal import (
    canonical_stage9_directional_carrier,
    continuation_future_signature_probabilities,
)
from t_search.stage10_lift import (
    STAGE10B_RETAINED_NORMALIZATION,
    STAGE10B_RETAINED_REPRESENTATION,
    canonical_stage10b_lifts,
    lift_stage10_reference_measurement,
    stage10b_effect_form_probabilities,
    stage10b_lift_diagnostics,
    stage10b_normalization_decision,
    stage10b_support_probabilities,
)


DIAGNOSTICS = stage10b_lift_diagnostics()


def test_stage10b_criterion17_each_continuation_has_independent_lift() -> None:
    carrier = canonical_stage9_directional_carrier()
    lifts = canonical_stage10b_lifts()
    assert len(lifts) == len(carrier.continuations) == 2
    assert DIAGNOSTICS.all_lifts_continuation_specific
    assert {lift.continuation_id for lift in lifts} == {
        item.continuation_id for item in carrier.continuations
    }
    for continuation, lift in zip(carrier.continuations, lifts, strict=True):
        independently = lift_stage10_reference_measurement(continuation)
        assert independently.continuation_id == lift.continuation_id
        assert independently is not lift
        assert all(
            "continuation-specific A/e2 reduction" in effect.effect_provenance
            for effect in lift.effects
        )


def test_stage10b_criterion18_no_universal_h_independent_lift_is_assumed() -> None:
    lifts = canonical_stage10b_lifts()
    assert len(lifts) == 2
    assert lifts[0].continuation_id != lifts[1].continuation_id
    assert lifts[0].class_correspondence != lifts[1].class_correspondence
    # Cross-use is rejected even though both physical coordinate arrays have shape 14.
    carrier = canonical_stage9_directional_carrier()
    with pytest.raises(ValueError, match="different continuation class"):
        stage10b_effect_form_probabilities(lifts[0], carrier.continuations[1])


def test_stage10b_criterion19_effect_forms_and_normalization_are_well_defined() -> None:
    assert DIAGNOSTICS.max_support_completeness_residual <= 10 * DEFAULT_ATOL
    assert DIAGNOSTICS.max_physical_completeness_residual <= 10 * DEFAULT_ATOL
    assert DIAGNOSTICS.minimum_support_effect_eigenvalue >= -10 * DEFAULT_ATOL
    assert DIAGNOSTICS.minimum_physical_effect_eigenvalue >= -10 * DEFAULT_ATOL
    assert DIAGNOSTICS.minimum_physical_normalization_eigenvalue > DEFAULT_ATOL

    for lift in canonical_stage10b_lifts():
        support_sum = sum(
            (effect.support_effect_matrix for effect in lift.effects),
            start=np.zeros((14, 14), dtype=np.complex128),
        )
        physical_sum = sum(
            (effect.physical_effect_form for effect in lift.effects),
            start=np.zeros((14, 14), dtype=np.complex128),
        )
        assert np.allclose(
            support_sum,
            lift.support_normalization_matrix,
            atol=10 * DEFAULT_ATOL,
            rtol=0.0,
        )
        assert np.allclose(
            physical_sum,
            lift.physical_normalization_form,
            atol=10 * DEFAULT_ATOL,
            rtol=0.0,
        )


def test_stage10b_criterion20_normalization_is_selected_by_reference_equivalence_and_nonunitarity() -> None:
    decision = stage10b_normalization_decision()
    assert decision.retained_representation == STAGE10B_RETAINED_REPRESENTATION
    assert decision.retained_normalization == STAGE10B_RETAINED_NORMALIZATION
    assert decision.reference_support_povm_equivalent
    assert decision.physical_effect_form_equivalent
    assert decision.genuine_maps_nonunitary
    assert decision.local_identity_reset_not_transport_covariant
    assert decision.max_nonunitarity_residual > 10 * DEFAULT_ATOL
    assert decision.max_identity_reset_residual > 10 * DEFAULT_ATOL
    # Stage 9D physical-norm metric and Stage 10 operational normalization remain typed separately.
    assert not decision.physical_metric_identified_with_operational_normalization


def test_stage10b_criterion21_both_representations_reproduce_stage9c_reference_likelihoods() -> None:
    carrier = canonical_stage9_directional_carrier()
    for continuation, lift in zip(
        carrier.continuations, canonical_stage10b_lifts(), strict=True
    ):
        reference = dict(
            continuation_future_signature_probabilities(carrier, continuation)
        )
        support = dict(stage10b_support_probabilities(lift, continuation))
        effect_form = dict(stage10b_effect_form_probabilities(lift, continuation))
        assert set(reference) == set(support) == set(effect_form)
        for outcome in reference:
            assert abs(support[outcome] - reference[outcome]) <= 10 * DEFAULT_ATOL
            assert abs(effect_form[outcome] - reference[outcome]) <= 10 * DEFAULT_ATOL
            assert abs(effect_form[outcome] - support[outcome]) <= 10 * DEFAULT_ATOL
    assert DIAGNOSTICS.max_support_stage9_probability_residual <= 10 * DEFAULT_ATOL
    assert DIAGNOSTICS.max_effect_form_stage9_probability_residual <= 10 * DEFAULT_ATOL
    assert DIAGNOSTICS.max_support_vs_form_probability_residual <= 10 * DEFAULT_ATOL


def test_stage10b_criterion22_class_and_outcome_correspondences_are_explicit() -> None:
    assert DIAGNOSTICS.class_correspondences_explicit
    assert DIAGNOSTICS.outcome_correspondences_explicit
    for lift in canonical_stage10b_lifts():
        assert lift.class_correspondence == (
            lift.continuation_id,
            lift.continuation_id,
        )
        assert lift.outcome_correspondence == (
            ("future_signature_left", "future_signature_left"),
            ("future_signature_other", "future_signature_other"),
        )


def test_stage10b_criterion23_wrong_continuation_lift_is_rejected() -> None:
    carrier = canonical_stage9_directional_carrier()
    lifts = canonical_stage10b_lifts()
    assert DIAGNOSTICS.wrong_continuation_lift_rejected
    with pytest.raises(ValueError, match="different continuation class"):
        stage10b_support_probabilities(lifts[0], carrier.continuations[1])
    with pytest.raises(ValueError, match="different continuation class"):
        stage10b_effect_form_probabilities(lifts[1], carrier.continuations[0])


def test_stage10b_does_not_preclaim_stage10c_covariance() -> None:
    assert not DIAGNOSTICS.full_cross_clock_measurement_covariance_established
