from fractions import Fraction

import pytest

from t_search.stage3 import (
    Microstate,
    all_microstates,
    assert_bijective,
    canonical_forward_ensemble,
    canonical_initial_distribution,
    canonical_reversed_ensemble,
    distribution_entropy,
    forward_trajectory,
    full_state_entropies,
    is_bijective,
    is_forward_dynamically_valid,
    is_reverse_dynamically_valid,
    make_trajectory_ensemble,
    reverse_ensemble,
    reverse_trajectory,
    state_marginal,
    u_rec,
    u_scr,
)


def test_microstate_space_contains_exactly_all_eight_bit_states() -> None:
    states = all_microstates()

    assert len(states) == 8
    assert len(set(states)) == 8
    assert states[0] == Microstate(0, 0, 0)
    assert states[-1] == Microstate(1, 1, 1)

    with pytest.raises(ValueError, match="must be a bit"):
        Microstate(2, 0, 0)


def test_recording_map_is_bijective_and_self_inverse_on_full_space() -> None:
    assert is_bijective(u_rec)
    assert_bijective(u_rec, name="U_rec")

    for state in all_microstates():
        assert u_rec(u_rec(state)) == state


def test_scrambling_map_is_bijective_and_self_inverse_on_full_space() -> None:
    assert is_bijective(u_scr)
    assert_bijective(u_scr, name="U_scr")

    for state in all_microstates():
        assert u_scr(u_scr(state)) == state


def test_non_bijective_map_is_rejected_when_reversibility_is_claimed() -> None:
    def erase(_: Microstate) -> Microstate:
        return Microstate(0, 0, 0)

    assert is_bijective(erase) is False
    with pytest.raises(ValueError, match="not bijective"):
        assert_bijective(erase, name="erase")


def test_canonical_boundary_distribution_is_exact_four_state_ensemble() -> None:
    distribution = canonical_initial_distribution()

    assert len(distribution) == 4
    assert set(distribution.values()) == {Fraction(1, 4)}
    assert sum(distribution.values(), Fraction(0, 1)) == Fraction(1, 1)
    assert {state.m for state in distribution} == {0}
    assert {(state.x, state.n) for state in distribution} == {
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1),
    }


def test_canonical_forward_ensemble_has_four_valid_equiprobable_trajectories() -> None:
    ensemble = canonical_forward_ensemble()

    assert len(ensemble.trajectories) == 4
    assert set(weight for _, weight in ensemble.weighted_trajectories) == {
        Fraction(1, 4)
    }
    assert all(is_forward_dynamically_valid(t) for t in ensemble.trajectories)

    for initial in canonical_initial_distribution():
        trajectory = forward_trajectory(initial)
        assert trajectory in ensemble.trajectories
        z0, z1, z2 = trajectory
        assert z1 == u_rec(z0)
        assert z2 == u_scr(z1)


def test_history_reversal_is_involutive_and_uses_inverse_maps_in_reverse_order() -> None:
    forward = canonical_forward_ensemble()
    reversed_ensemble = canonical_reversed_ensemble()

    assert len(reversed_ensemble.trajectories) == len(forward.trajectories)
    assert all(
        is_reverse_dynamically_valid(trajectory)
        for trajectory in reversed_ensemble.trajectories
    )

    for trajectory in forward.trajectories:
        reversed_trajectory = reverse_trajectory(trajectory)
        assert reverse_trajectory(reversed_trajectory) == trajectory
        assert is_reverse_dynamically_valid(reversed_trajectory)

    assert reverse_ensemble(reversed_ensemble) == forward


def test_full_state_distribution_mass_and_entropy_are_preserved_at_all_positions() -> None:
    ensemble = canonical_forward_ensemble()

    marginals = tuple(state_marginal(ensemble, position) for position in (0, 1, 2))
    for marginal in marginals:
        assert len(marginal) == 4
        assert set(marginal.values()) == {Fraction(1, 4)}
        assert sum(marginal.values(), Fraction(0, 1)) == Fraction(1, 1)

    assert full_state_entropies(ensemble) == pytest.approx((2.0, 2.0, 2.0))
    assert tuple(distribution_entropy(marginal) for marginal in marginals) == pytest.approx(
        (2.0, 2.0, 2.0)
    )


def test_reversed_ensemble_has_same_full_state_entropy_profile_reversed() -> None:
    forward = canonical_forward_ensemble()
    reversed_ensemble = canonical_reversed_ensemble()

    assert full_state_entropies(reversed_ensemble) == pytest.approx(
        tuple(reversed(full_state_entropies(forward)))
    )


def test_invalid_ensemble_weights_and_positions_are_rejected() -> None:
    trajectory = forward_trajectory(Microstate(0, 0, 0))

    with pytest.raises(ValueError, match="sum exactly to one"):
        make_trajectory_ensemble(((trajectory, Fraction(1, 2)),))

    with pytest.raises(ValueError, match="strictly positive"):
        make_trajectory_ensemble(((trajectory, Fraction(0, 1)),))

    with pytest.raises(ValueError, match="position must be"):
        state_marginal(canonical_forward_ensemble(), 3)
