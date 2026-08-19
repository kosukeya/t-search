from fractions import Fraction

import pytest

from t_search.stage3 import (
    Microstate,
    canonical_forward_ensemble,
    forward_trajectory,
    make_trajectory_ensemble,
)
from t_search.stage3_diagnostics import (
    accessibility_arrow_score,
    accessibility_profile,
    bayes_optimal_accuracy,
    component_conditional_entropy,
    component_decoding_accuracy,
    component_distribution,
    component_entropy,
    component_joint_distribution,
    component_mutual_information,
    component_variable,
    conditional_entropy,
    joint_distribution,
    mutual_information,
    record_arrow_score,
    record_profile,
    variable_distribution,
    variable_entropy,
)


def test_component_marginals_are_exact_for_canonical_ensemble() -> None:
    ensemble = canonical_forward_ensemble()

    assert component_distribution(ensemble, 0, "m") == {0: Fraction(1, 1)}
    assert component_distribution(ensemble, 1, "m") == {
        0: Fraction(1, 2),
        1: Fraction(1, 2),
    }
    assert component_distribution(ensemble, 0, "x") == {
        0: Fraction(1, 2),
        1: Fraction(1, 2),
    }
    assert component_distribution(ensemble, 2, "x") == {
        0: Fraction(1, 2),
        1: Fraction(1, 2),
    }


def test_variable_and_joint_distribution_helpers_preserve_exact_mass() -> None:
    ensemble = canonical_forward_ensemble()
    m1 = component_variable(1, "m")
    x0 = component_variable(0, "x")

    marginal = variable_distribution(ensemble, m1)
    joint = joint_distribution(ensemble, m1, x0)

    assert sum(marginal.values(), Fraction(0, 1)) == Fraction(1, 1)
    assert sum(joint.values(), Fraction(0, 1)) == Fraction(1, 1)
    assert joint == {
        (0, 0): Fraction(1, 2),
        (1, 1): Fraction(1, 2),
    }
    assert component_joint_distribution(ensemble, 1, "m", 0, "x") == joint


def test_component_entropies_capture_subsystem_redistribution_without_global_claim() -> None:
    ensemble = canonical_forward_ensemble()

    assert component_entropy(ensemble, 0, "m") == pytest.approx(0.0)
    assert component_entropy(ensemble, 1, "m") == pytest.approx(1.0)
    assert component_entropy(ensemble, 0, "x") == pytest.approx(1.0)
    assert component_entropy(ensemble, 2, "x") == pytest.approx(1.0)

    m1 = component_variable(1, "m")
    assert variable_entropy(ensemble, m1) == pytest.approx(1.0)


def test_mutual_information_distinguishes_perfect_dependence_from_independence() -> None:
    ensemble = canonical_forward_ensemble()

    i_m1_x0 = component_mutual_information(ensemble, 1, "m", 0, "x")
    i_m1_x2 = component_mutual_information(ensemble, 1, "m", 2, "x")

    assert i_m1_x0 == pytest.approx(1.0)
    assert i_m1_x2 == pytest.approx(0.0)
    assert component_mutual_information(ensemble, 0, "x", 1, "m") == pytest.approx(
        i_m1_x0
    )

    assert mutual_information(
        ensemble, component_variable(1, "m"), component_variable(0, "x")
    ) == pytest.approx(1.0)


def test_conditional_entropy_matches_exact_canonical_dependencies() -> None:
    ensemble = canonical_forward_ensemble()

    assert component_conditional_entropy(ensemble, 0, "x", 1, "m") == pytest.approx(
        0.0
    )
    assert component_conditional_entropy(ensemble, 2, "x", 1, "m") == pytest.approx(
        1.0
    )

    assert conditional_entropy(
        ensemble,
        component_variable(0, "x"),
        component_variable(1, "m"),
    ) == pytest.approx(0.0)


def test_bayes_optimal_decoder_accuracy_matches_exact_canonical_accessibility() -> None:
    ensemble = canonical_forward_ensemble()

    assert component_decoding_accuracy(ensemble, 1, "m", 0, "x") == pytest.approx(1.0)
    assert component_decoding_accuracy(ensemble, 1, "m", 2, "x") == pytest.approx(0.5)

    assert bayes_optimal_accuracy(
        ensemble,
        component_variable(1, "m"),
        component_variable(0, "x"),
    ) == pytest.approx(1.0)


def test_record_profile_reports_unsigned_information_by_neutral_position() -> None:
    ensemble = canonical_forward_ensemble()

    assert record_profile(ensemble) == pytest.approx({0: 1.0, 1: 1.0, 2: 0.0})


def test_accessibility_profile_reports_decoder_accuracy_by_neutral_position() -> None:
    ensemble = canonical_forward_ensemble()

    assert accessibility_profile(ensemble) == pytest.approx({0: 1.0, 1: 1.0, 2: 0.5})


def test_signed_scores_are_defined_as_neutral_side_contrasts_only() -> None:
    ensemble = canonical_forward_ensemble()

    assert record_arrow_score(ensemble, current_position=1, delta=1) == pytest.approx(1.0)
    assert accessibility_arrow_score(
        ensemble, current_position=1, delta=1
    ) == pytest.approx(0.5)


def test_single_trajectory_value_equality_is_not_sufficient_for_mutual_information_record() -> None:
    trajectory = forward_trajectory(Microstate(0, 0, 0))
    ensemble = make_trajectory_ensemble(((trajectory, Fraction(1, 1)),))

    # M_1 == X_0 numerically on this one trajectory, but both variables are
    # constant across the ensemble, so there is no statistical information.
    assert trajectory[1].m == trajectory[0].x
    assert component_mutual_information(ensemble, 1, "m", 0, "x") == pytest.approx(0.0)
    assert component_entropy(ensemble, 0, "x") == pytest.approx(0.0)


def test_invalid_positions_components_and_directional_windows_are_rejected() -> None:
    ensemble = canonical_forward_ensemble()

    with pytest.raises(ValueError, match="position must be"):
        component_distribution(ensemble, 3, "x")
    with pytest.raises(ValueError, match="component must be"):
        component_distribution(ensemble, 1, "q")
    with pytest.raises(ValueError, match="positive integer"):
        record_arrow_score(ensemble, current_position=1, delta=0)
    with pytest.raises(ValueError, match="both comparison positions"):
        record_arrow_score(ensemble, current_position=0, delta=1)
