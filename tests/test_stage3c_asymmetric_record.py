from fractions import Fraction

import pytest

from t_search.stage3 import Microstate, forward_trajectory, make_trajectory_ensemble
from t_search.stage3_asymmetry import (
    AsymmetricRecordModel,
    assess_record_orientation,
    canonical_asymmetric_record_model,
    canonical_record_orientation_assessment,
    orientation_from_scores,
)
from t_search.stage3_diagnostics import component_distribution


def test_canonical_model_keeps_blank_boundary_and_neutral_interface() -> None:
    model = canonical_asymmetric_record_model()

    assert model.current_position == 1
    assert model.delta == 1
    assert model.record_component == "m"
    assert model.target_component == "x"
    assert component_distribution(model.ensemble, 0, "m") == {0: Fraction(1, 1)}


def test_canonical_assessment_has_expected_information_and_accessibility_contrasts() -> None:
    assessment = canonical_record_orientation_assessment()

    assert assessment.lower_position == 0
    assert assessment.upper_position == 2
    assert assessment.lower_information == pytest.approx(1.0)
    assert assessment.upper_information == pytest.approx(0.0)
    assert assessment.lower_accuracy == pytest.approx(1.0)
    assert assessment.upper_accuracy == pytest.approx(0.5)
    assert assessment.record_score == pytest.approx(1.0)
    assert assessment.accessibility_score == pytest.approx(0.5)


def test_canonical_model_supports_lower_index_record_defined_orientation() -> None:
    assessment = canonical_record_orientation_assessment()

    assert assessment.diagnostics_agree is True
    assert assessment.orientation == "lower-index"
    assert assessment.record_defined is True
    assert assessment.microscopic_maps_reversible is True


def test_orientation_labels_remain_neutral_and_do_not_encode_past_future() -> None:
    assessment = canonical_record_orientation_assessment()

    assert assessment.orientation in {"lower-index", "upper-index", "none"}
    assert "past" not in assessment.orientation
    assert "future" not in assessment.orientation


def test_zero_contrasts_do_not_define_an_orientation() -> None:
    trajectory = forward_trajectory(Microstate(0, 0, 0))
    ensemble = make_trajectory_ensemble(((trajectory, Fraction(1, 1)),))
    assessment = assess_record_orientation(AsymmetricRecordModel(ensemble=ensemble))

    assert assessment.record_score == pytest.approx(0.0)
    assert assessment.accessibility_score == pytest.approx(0.0)
    assert assessment.orientation == "none"
    assert assessment.diagnostics_agree is False
    assert assessment.record_defined is False


def test_orientation_requires_information_and_accessibility_scores_to_agree() -> None:
    assert orientation_from_scores(1.0, 0.5) == "lower-index"
    assert orientation_from_scores(-1.0, -0.5) == "upper-index"
    assert orientation_from_scores(1.0, -0.5) == "none"
    assert orientation_from_scores(-1.0, 0.5) == "none"


def test_one_zero_diagnostic_is_insufficient_for_stage3c_orientation() -> None:
    assert orientation_from_scores(1.0, 0.0) == "none"
    assert orientation_from_scores(0.0, 0.5) == "none"


def test_orientation_tolerance_must_be_nonnegative() -> None:
    with pytest.raises(ValueError, match="tolerance must be non-negative"):
        orientation_from_scores(1.0, 0.5, tolerance=-1.0)
