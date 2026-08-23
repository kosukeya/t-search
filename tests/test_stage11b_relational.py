import numpy as np
import pytest

from t_search.stage11_parametrized import (
    STAGE11A_ATOL,
    STAGE11A_AFFINE,
    STAGE11A_CUBIC,
    STAGE11A_HYPERBOLIC,
    STAGE11A_IDENTITY,
    canonical_stage11a_positive_family,
)
from t_search.stage11_relational import (
    STAGE11B_RAW_MATCH_INVALID,
    canonical_stage11b_anchor_target_views,
    stage11b_corresponded_relational_observables,
    stage11b_diagnostics,
    stage11b_raw_equal_parameter_matches,
    stage11b_raw_parameter_match_control,
    stage11b_relational_derivatives,
    stage11b_relational_observable,
)


def _family_by_id():
    return {
        item.parameterization_id: item for item in canonical_stage11a_positive_family()
    }


def test_stage11b_q_of_T_agrees_across_all_corresponding_events() -> None:
    family = _family_by_id()
    reference = family[STAGE11A_IDENTITY]
    evaluations = 0

    for trajectory in family.values():
        pairs = stage11b_corresponded_relational_observables(reference, trajectory)
        assert len(pairs) == len(reference.event_ids) == 13
        evaluations += len(pairs)
        for pair in pairs:
            assert pair.source.event_id == pair.target.event_id == pair.event_id
            assert abs(pair.source.clock_value - pair.target.clock_value) <= STAGE11A_ATOL
            assert abs(pair.source.q_value - pair.target.q_value) <= STAGE11A_ATOL

            reconstructed = stage11b_relational_observable(
                trajectory, pair.source.clock_value
            )
            assert reconstructed.event_id == pair.event_id
            assert abs(reconstructed.q_value - pair.source.q_value) <= STAGE11A_ATOL

    assert evaluations == 52


def test_stage11b_relational_derivative_is_parameterization_invariant() -> None:
    family = _family_by_id()
    reference = family[STAGE11A_IDENTITY]
    reference_derivative = stage11b_relational_derivatives(reference)

    assert np.allclose(reference_derivative, 1.25, atol=STAGE11A_ATOL, rtol=0.0)
    for trajectory in family.values():
        derivative = stage11b_relational_derivatives(trajectory)
        assert np.allclose(
            derivative, reference_derivative, atol=STAGE11A_ATOL, rtol=0.0
        )
        assert np.allclose(
            derivative, trajectory.p_values, atol=STAGE11A_ATOL, rtol=0.0
        )


def test_stage11b_nonlinear_maps_change_raw_parameter_derivatives() -> None:
    family = _family_by_id()
    reference = family[STAGE11A_IDENTITY]
    changed = 0

    for parameterization_id in (STAGE11A_CUBIC, STAGE11A_HYPERBOLIC):
        trajectory = family[parameterization_id]
        difference = np.abs(trajectory.raw_q_rates - reference.raw_q_rates)
        changed += int(np.count_nonzero(difference > STAGE11A_ATOL))
        assert np.max(difference) > STAGE11A_ATOL
        assert np.allclose(
            stage11b_relational_derivatives(trajectory),
            stage11b_relational_derivatives(reference),
            atol=STAGE11A_ATOL,
            rtol=0.0,
        )

    assert changed == 24


def test_stage11b_anchor_and_target_events_remain_explicitly_typed() -> None:
    views = canonical_stage11b_anchor_target_views()
    assert len(views) == 8

    anchors = [item for item in views if item.role == "prediction_anchor"]
    targets = [item for item in views if item.role == "measurement_target"]
    assert len(anchors) == len(targets) == 4
    assert len({item.event_id for item in anchors}) == 1
    assert len({item.event_id for item in targets}) == 1
    assert anchors[0].event_id != targets[0].event_id
    assert len({item.parameter_value for item in anchors}) > 1
    assert len({item.parameter_value for item in targets}) > 1
    assert len({item.clock_value for item in anchors}) == 1
    assert len({item.clock_value for item in targets}) == 1


def test_stage11b_equal_raw_parameter_matching_has_false_event_witnesses() -> None:
    family = _family_by_id()
    witnesses = stage11b_raw_equal_parameter_matches(
        family[STAGE11A_IDENTITY], family[STAGE11A_AFFINE]
    )
    control = stage11b_raw_parameter_match_control()

    assert len(witnesses) == 7
    assert sum(not item.same_physical_event for item in witnesses) == 6
    assert sum(item.same_physical_event for item in witnesses) == 1
    assert any(
        abs(item.raw_parameter_value) <= STAGE11A_ATOL
        and item.source_event_id != item.target_event_id
        and abs(item.source_clock_value - item.target_clock_value) > STAGE11A_ATOL
        for item in witnesses
    )
    assert control.equal_raw_parameter_overlap_count == 7
    assert control.false_event_identity_count == 6
    assert control.coincident_same_event_count == 1
    assert control.classification == STAGE11B_RAW_MATCH_INVALID
    assert control.raw_parameter_matching_rejected


def test_stage11b_relational_observable_requires_a_unique_internal_clock_event() -> None:
    trajectory = _family_by_id()[STAGE11A_IDENTITY]
    with pytest.raises(ValueError, match="exactly one physical event"):
        stage11b_relational_observable(trajectory, 100.0)


def test_stage11b_diagnostics_close_criteria_17_23_only() -> None:
    diagnostics = stage11b_diagnostics()
    assert diagnostics.positive_parameterization_count == 4
    assert diagnostics.event_count == 13
    assert diagnostics.relational_observable_evaluation_count == 52
    assert diagnostics.relational_derivative_evaluation_count == 52
    assert diagnostics.max_relational_observable_residual <= STAGE11A_ATOL
    assert diagnostics.max_relational_derivative_residual <= STAGE11A_ATOL
    assert diagnostics.max_momentum_relational_derivative_residual <= STAGE11A_ATOL
    assert abs(diagnostics.reference_relational_derivative - 1.25) <= STAGE11A_ATOL
    assert diagnostics.nonlinear_raw_rate_difference_count == 24
    assert diagnostics.max_nonlinear_raw_rate_difference > STAGE11A_ATOL
    assert diagnostics.anchor_target_view_count == 8
    assert diagnostics.anchor_event_id != diagnostics.target_event_id
    assert diagnostics.raw_equal_parameter_overlap_count == 7
    assert diagnostics.raw_equal_parameter_false_identity_count == 6
    assert diagnostics.raw_equal_parameter_coincident_same_event_count == 1
    assert diagnostics.raw_parameter_matching_classification == STAGE11B_RAW_MATCH_INVALID
    assert diagnostics.raw_parameter_matching_rejected
    assert diagnostics.criteria_17_23_satisfied
