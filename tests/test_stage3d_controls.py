from fractions import Fraction

import pytest

from t_search.stage3 import (
    canonical_forward_ensemble,
    full_state_entropies,
    is_bijective,
    is_reverse_dynamically_valid,
    u_scr,
)
from t_search.stage3_controls import (
    assess_control_ensemble,
    canonical_reversed_control_ensemble,
    mix_ensembles,
    no_record_forward_ensemble,
    stage3d_control_assessments,
    symmetric_forward_reverse_ensemble,
    u_identity,
    uniform_memory_forward_ensemble,
    uniform_memory_initial_distribution,
)
from t_search.stage3_diagnostics import component_entropy


def test_reversal_flips_both_signed_diagnostics_and_orientation() -> None:
    forward = assess_control_ensemble(canonical_forward_ensemble())
    reversed_assessment = assess_control_ensemble(canonical_reversed_control_ensemble())

    assert forward.record_score == pytest.approx(1.0)
    assert forward.accessibility_score == pytest.approx(0.5)
    assert forward.orientation == "lower-index"

    assert reversed_assessment.record_score == pytest.approx(-forward.record_score)
    assert reversed_assessment.accessibility_score == pytest.approx(
        -forward.accessibility_score
    )
    assert reversed_assessment.lower_information == pytest.approx(
        forward.upper_information
    )
    assert reversed_assessment.upper_information == pytest.approx(
        forward.lower_information
    )
    assert reversed_assessment.orientation == "upper-index"
    assert reversed_assessment.record_defined is True


def test_reversed_control_uses_exact_modeled_history_reversal() -> None:
    reversed_ensemble = canonical_reversed_control_ensemble()

    assert len(reversed_ensemble.trajectories) == 4
    assert all(is_reverse_dynamically_valid(t) for t in reversed_ensemble.trajectories)


def test_symmetric_mixture_merges_duplicate_histories_and_preserves_mass() -> None:
    symmetric = symmetric_forward_reverse_ensemble()

    assert len(symmetric.trajectories) == 7
    assert sum((weight for _, weight in symmetric.weighted_trajectories), Fraction()) == Fraction(1, 1)
    assert sorted(weight for _, weight in symmetric.weighted_trajectories) == [
        Fraction(1, 8),
        Fraction(1, 8),
        Fraction(1, 8),
        Fraction(1, 8),
        Fraction(1, 8),
        Fraction(1, 8),
        Fraction(1, 4),
    ]


def test_symmetric_mixture_cancels_signed_bias_without_erasing_correlations() -> None:
    assessment = assess_control_ensemble(symmetric_forward_reverse_ensemble())

    assert assessment.lower_information == pytest.approx(assessment.upper_information)
    assert assessment.lower_information > 0.0
    assert assessment.lower_accuracy == pytest.approx(assessment.upper_accuracy)
    assert assessment.lower_accuracy == pytest.approx(0.75)
    assert assessment.record_score == pytest.approx(0.0, abs=1e-12)
    assert assessment.accessibility_score == pytest.approx(0.0, abs=1e-12)
    assert assessment.orientation == "none"
    assert assessment.record_defined is False


def test_no_record_control_keeps_order_and_scrambling_but_has_no_orientation() -> None:
    ensemble = no_record_forward_ensemble()
    assessment = assess_control_ensemble(ensemble)

    assert is_bijective(u_identity)
    assert is_bijective(u_scr)
    assert len(ensemble.trajectories) == 4
    assert all(z1 == u_identity(z0) and z2 == u_scr(z1) for z0, z1, z2 in ensemble.trajectories)
    assert any(z0.x != z2.x for z0, _, z2 in ensemble.trajectories)
    assert assessment.lower_information == pytest.approx(0.0)
    assert assessment.upper_information == pytest.approx(0.0)
    assert assessment.lower_accuracy == pytest.approx(0.5)
    assert assessment.upper_accuracy == pytest.approx(0.5)
    assert assessment.record_score == pytest.approx(0.0)
    assert assessment.accessibility_score == pytest.approx(0.0)
    assert assessment.orientation == "none"
    assert assessment.record_defined is False


def test_uniform_memory_boundary_is_exact_and_removes_canonical_record() -> None:
    initial = uniform_memory_initial_distribution()
    ensemble = uniform_memory_forward_ensemble()
    assessment = assess_control_ensemble(ensemble)

    assert len(initial) == 8
    assert set(initial.values()) == {Fraction(1, 8)}
    assert component_entropy(ensemble, 0, "m") == pytest.approx(1.0)
    assert assessment.lower_information == pytest.approx(0.0)
    assert assessment.upper_information == pytest.approx(0.0)
    assert assessment.lower_accuracy == pytest.approx(0.5)
    assert assessment.upper_accuracy == pytest.approx(0.5)
    assert assessment.orientation == "none"
    assert assessment.record_defined is False


def test_uniform_memory_control_keeps_canonical_reversible_dynamics_and_global_entropy() -> None:
    ensemble = uniform_memory_forward_ensemble()

    assert len(ensemble.trajectories) == 8
    assert full_state_entropies(ensemble) == pytest.approx((3.0, 3.0, 3.0))


def test_control_summary_separates_orientation_from_mere_order_and_boundary_choice() -> None:
    assessments = stage3d_control_assessments()

    assert assessments["forward"].orientation == "lower-index"
    assert assessments["reversed"].orientation == "upper-index"
    assert assessments["symmetric"].orientation == "none"
    assert assessments["no-record"].orientation == "none"
    assert assessments["uniform-memory"].orientation == "none"

    for name in ("forward", "reversed", "symmetric", "uniform-memory"):
        assert assessments[name].microscopic_maps_reversible is True


def test_mixture_rejects_invalid_weights() -> None:
    forward = canonical_forward_ensemble()

    with pytest.raises(ValueError, match="at least one"):
        mix_ensembles(())

    with pytest.raises(ValueError, match="strictly positive"):
        mix_ensembles(((forward, Fraction(0, 1)), (forward, Fraction(1, 1))))

    with pytest.raises(ValueError, match="sum exactly to one"):
        mix_ensembles(((forward, Fraction(1, 4)), (forward, Fraction(1, 4))))
