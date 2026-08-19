from fractions import Fraction
from math import log2

import pytest

from t_search.stage3_diagnostics import component_mutual_information
from t_search.stage3_accessibility import (
    LocalAccessPolicy,
    compatible_history_count,
    local_observation_decoding_accuracy,
    local_observation_mutual_information,
    make_local_observation_ensemble,
    outcome_distribution,
    posterior_histories_given_outcome,
    record_readout_accessibility_arrow_score,
    record_readout_decoding_accuracy,
    record_readout_mutual_information,
    record_readout_arrow_score,
)
from t_search.stage3_local import (
    canonical_record_block,
    compatible_global_histories,
    project_record_view,
)


def _binary_entropy(probability: float) -> float:
    if probability in (0.0, 1.0):
        return 0.0
    return -probability * log2(probability) - (1.0 - probability) * log2(1.0 - probability)


def test_access_policy_validates_degradation_range_and_hidden_record_noise() -> None:
    with pytest.raises(ValueError, match="\[0, 1/2\]"):
        LocalAccessPolicy(record_error_probability=Fraction(-1, 4))
    with pytest.raises(ValueError, match="\[0, 1/2\]"):
        LocalAccessPolicy(record_error_probability=Fraction(3, 4))
    with pytest.raises(ValueError, match="hidden"):
        LocalAccessPolicy(expose_m=False, record_error_probability=Fraction(1, 4))


def test_exact_record_only_channel_reproduces_stage3b_record_accessibility() -> None:
    block = canonical_record_block()
    observations = make_local_observation_ensemble(
        block,
        LocalAccessPolicy(expose_x=False, expose_m=True),
    )

    assert record_readout_mutual_information(observations, target_position=0) == pytest.approx(1.0)
    assert record_readout_mutual_information(observations, target_position=2) == pytest.approx(0.0)
    assert record_readout_decoding_accuracy(observations, target_position=0) == pytest.approx(1.0)
    assert record_readout_decoding_accuracy(observations, target_position=2) == pytest.approx(0.5)
    assert record_readout_arrow_score(observations) == pytest.approx(1.0)
    assert record_readout_accessibility_arrow_score(observations) == pytest.approx(0.5)


def test_quarter_record_noise_degrades_information_exactly_as_binary_symmetric_channel() -> None:
    block = canonical_record_block()
    epsilon = Fraction(1, 4)
    observations = make_local_observation_ensemble(
        block,
        LocalAccessPolicy(
            expose_x=False,
            expose_m=True,
            record_error_probability=epsilon,
        ),
    )
    expected_information = 1.0 - _binary_entropy(float(epsilon))

    assert record_readout_mutual_information(observations, target_position=0) == pytest.approx(
        expected_information
    )
    assert record_readout_mutual_information(observations, target_position=2) == pytest.approx(0.0)
    assert record_readout_decoding_accuracy(observations, target_position=0) == pytest.approx(0.75)
    assert record_readout_decoding_accuracy(observations, target_position=2) == pytest.approx(0.5)
    assert record_readout_arrow_score(observations) == pytest.approx(expected_information)
    assert record_readout_accessibility_arrow_score(observations) == pytest.approx(0.25)


def test_half_record_noise_removes_accessible_record_contrast() -> None:
    block = canonical_record_block()
    observations = make_local_observation_ensemble(
        block,
        LocalAccessPolicy(
            expose_x=False,
            expose_m=True,
            record_error_probability=Fraction(1, 2),
        ),
    )

    assert record_readout_mutual_information(observations, target_position=0) == pytest.approx(0.0)
    assert record_readout_mutual_information(observations, target_position=2) == pytest.approx(0.0)
    assert record_readout_decoding_accuracy(observations, target_position=0) == pytest.approx(0.5)
    assert record_readout_decoding_accuracy(observations, target_position=2) == pytest.approx(0.5)
    assert record_readout_arrow_score(observations) == pytest.approx(0.0)
    assert record_readout_accessibility_arrow_score(observations) == pytest.approx(0.0)


def test_record_accessibility_degrades_monotonically_without_changing_global_register_information() -> None:
    block = canonical_record_block()
    global_information = component_mutual_information(block.ensemble, 1, "m", 0, "x")
    accessible = []
    for epsilon in (Fraction(0, 1), Fraction(1, 4), Fraction(1, 2)):
        observations = make_local_observation_ensemble(
            block,
            LocalAccessPolicy(
                expose_x=False,
                expose_m=True,
                record_error_probability=epsilon,
            ),
        )
        accessible.append(record_readout_mutual_information(observations, target_position=0))

    assert global_information == pytest.approx(1.0)
    assert accessible[0] > accessible[1] > accessible[2]
    assert accessible[2] == pytest.approx(0.0)
    assert component_mutual_information(block.ensemble, 1, "m", 0, "x") == pytest.approx(1.0)


def test_visible_current_x_redundantly_preserves_total_local_access_when_record_is_maximally_noisy() -> None:
    block = canonical_record_block()
    observations = make_local_observation_ensemble(
        block,
        LocalAccessPolicy(
            expose_x=True,
            expose_m=True,
            record_error_probability=Fraction(1, 2),
        ),
    )

    assert record_readout_mutual_information(observations, target_position=0) == pytest.approx(0.0)
    assert record_readout_decoding_accuracy(observations, target_position=0) == pytest.approx(0.5)
    assert local_observation_mutual_information(observations, target_position=0) == pytest.approx(1.0)
    assert local_observation_decoding_accuracy(observations, target_position=0) == pytest.approx(1.0)


def test_x_only_interface_preserves_redundant_lower_side_access_but_has_no_record_readout() -> None:
    block = canonical_record_block()
    observations = make_local_observation_ensemble(
        block,
        LocalAccessPolicy(expose_x=True, expose_m=False),
    )

    assert local_observation_mutual_information(observations, target_position=0) == pytest.approx(1.0)
    assert local_observation_decoding_accuracy(observations, target_position=0) == pytest.approx(1.0)
    assert local_observation_mutual_information(observations, target_position=2) == pytest.approx(0.0)
    assert local_observation_decoding_accuracy(observations, target_position=2) == pytest.approx(0.5)
    with pytest.raises(ValueError, match="hidden"):
        record_readout_mutual_information(observations, target_position=0)


def test_masking_x_exposes_record_noise_as_history_ambiguity() -> None:
    block = canonical_record_block()

    exact = make_local_observation_ensemble(
        block,
        LocalAccessPolicy(expose_x=False, expose_m=True),
    )
    noisy = make_local_observation_ensemble(
        block,
        LocalAccessPolicy(
            expose_x=False,
            expose_m=True,
            record_error_probability=Fraction(1, 4),
        ),
    )

    assert compatible_history_count(exact, (None, 1)) == 2
    assert compatible_history_count(noisy, (None, 1)) == 4

    posterior = posterior_histories_given_outcome(noisy, (None, 1))
    weights = sorted(weight for _, weight in posterior)
    assert weights == [Fraction(1, 8), Fraction(1, 8), Fraction(3, 8), Fraction(3, 8)]

    probability_x0_one = sum(
        (weight for trajectory, weight in posterior if trajectory[0].x == 1),
        Fraction(0, 1),
    )
    assert probability_x0_one == Fraction(3, 4)


def test_visible_x_blocks_record_noise_from_expanding_positive_support_history_class() -> None:
    block = canonical_record_block()
    observations = make_local_observation_ensemble(
        block,
        LocalAccessPolicy(
            expose_x=True,
            expose_m=True,
            record_error_probability=Fraction(1, 4),
        ),
    )

    assert compatible_history_count(observations, (1, 1)) == 2
    posterior = posterior_histories_given_outcome(observations, (1, 1))
    assert all(trajectory[0].x == 1 for trajectory, _ in posterior)
    assert sorted(weight for _, weight in posterior) == [Fraction(1, 2), Fraction(1, 2)]


def test_masking_both_local_bits_gives_prior_level_access_and_all_histories_compatible() -> None:
    block = canonical_record_block()
    observations = make_local_observation_ensemble(
        block,
        LocalAccessPolicy(expose_x=False, expose_m=False),
    )

    assert outcome_distribution(observations) == {(None, None): Fraction(1, 1)}
    assert local_observation_mutual_information(observations, target_position=0) == pytest.approx(0.0)
    assert local_observation_decoding_accuracy(observations, target_position=0) == pytest.approx(0.5)
    assert compatible_history_count(observations, (None, None)) == 4


def test_view_coverage_control_reproduces_single_view_ambiguity_and_two_view_reconstruction() -> None:
    block = canonical_record_block()
    trajectory = next(
        trajectory
        for trajectory in block.ensemble.trajectories
        if trajectory[0].x == 1 and trajectory[0].n == 1
    )
    view1 = project_record_view(block, trajectory, position=1)
    view2 = project_record_view(block, trajectory, position=2)

    assert len(compatible_global_histories(block, (view1,))) == 2
    assert len(compatible_global_histories(block, (view1, view2))) == 1


def test_zero_probability_outcomes_and_invalid_targets_are_rejected() -> None:
    block = canonical_record_block()
    observations = make_local_observation_ensemble(
        block,
        LocalAccessPolicy(expose_x=False, expose_m=True),
    )

    with pytest.raises(ValueError, match="zero probability"):
        posterior_histories_given_outcome(observations, (1, 1))
    with pytest.raises(ValueError, match="target position"):
        local_observation_mutual_information(observations, target_position=3)
    with pytest.raises(ValueError, match="both comparison positions"):
        record_readout_arrow_score(observations, delta=2)
