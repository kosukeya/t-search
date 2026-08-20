import numpy as np
import pytest

from t_search.stage4_conditional import (
    clock_outcome_probability,
    clock_probability_profile,
    condition_on_clock,
    conditional_schrodinger_residual,
    full_period_system_residual,
    normalized_physical_conditional_state,
    one_step_conditional_residuals,
    physical_reduction,
    system_evolution_unitary,
)
from t_search.stage4_quantum import (
    DEFAULT_ATOL,
    clock_reading_times,
    clock_step,
    equal_amplitude_physical_state,
    physical_state_from_coefficients,
    tensor_basis_state,
)


def generic_coefficients(dimension: int = 4) -> np.ndarray:
    if dimension == 4:
        raw = np.array(
            [1.0 + 0.5j, -0.3 + 0.7j, 0.2 - 0.4j, 0.9 + 0.1j],
            dtype=np.complex128,
        )
    else:
        raw = np.array(
            [complex(j + 1, (-1) ** j * 0.2 * (j + 1)) for j in range(dimension)],
            dtype=np.complex128,
        )
    return raw / np.linalg.norm(raw)


def test_equal_amplitude_clock_probabilities_are_uniform_and_normalized() -> None:
    state = equal_amplitude_physical_state(4)
    probabilities = clock_probability_profile(state, 4)

    assert probabilities == pytest.approx(np.full(4, 0.25))
    assert probabilities.sum() == pytest.approx(1.0)
    for j in range(4):
        assert clock_outcome_probability(state, j, 4) == pytest.approx(0.25)


def test_generic_complex_physical_state_has_uniform_ideal_clock_probabilities() -> None:
    coefficients = generic_coefficients(4)
    state = physical_state_from_coefficients(coefficients, 4)

    assert clock_probability_profile(state, 4) == pytest.approx(np.full(4, 0.25))


def test_physical_reduction_matches_analytic_coefficient_phase_formula() -> None:
    coefficients = generic_coefficients(4)
    state = physical_state_from_coefficients(coefficients, 4)
    n = np.arange(4, dtype=float)

    for j, time in enumerate(clock_reading_times(4)):
        expected = coefficients * np.exp(-1j * n * time)
        reduced = physical_reduction(state, j, 4)
        assert np.allclose(reduced, expected, atol=DEFAULT_ATOL, rtol=0.0)


def test_normalized_physical_reductions_have_unit_norm() -> None:
    state = physical_state_from_coefficients(generic_coefficients(4), 4)

    for j in range(4):
        reduced = physical_reduction(state, j, 4)
        normalized = normalized_physical_conditional_state(state, j, 4)
        assert np.linalg.norm(reduced) == pytest.approx(1.0)
        assert np.linalg.norm(normalized) == pytest.approx(1.0)
        assert np.allclose(normalized, reduced, atol=DEFAULT_ATOL, rtol=0.0)


def test_conditional_states_follow_discrete_schrodinger_evolution_from_reference() -> None:
    state = physical_state_from_coefficients(generic_coefficients(4), 4)

    residuals = [conditional_schrodinger_residual(state, j, 4) for j in range(4)]
    assert max(residuals) <= DEFAULT_ATOL


def test_one_step_schrodinger_relation_includes_periodic_wraparound() -> None:
    state = physical_state_from_coefficients(generic_coefficients(4), 4)
    residuals = one_step_conditional_residuals(state, 4)

    assert residuals.shape == (4,)
    assert np.max(residuals) <= DEFAULT_ATOL


def test_full_period_system_evolution_returns_each_conditional_state() -> None:
    state = physical_state_from_coefficients(generic_coefficients(4), 4)

    for j in range(4):
        assert full_period_system_residual(state, 4, index=j) <= DEFAULT_ATOL


def test_equal_amplitude_baseline_has_nontrivial_relative_ray_change() -> None:
    state = equal_amplitude_physical_state(4)
    psi_0 = physical_reduction(state, 0, 4)
    psi_1 = physical_reduction(state, 1, 4)

    assert abs(np.vdot(psi_0, psi_1)) <= DEFAULT_ATOL
    assert not np.allclose(psi_0, psi_1, atol=DEFAULT_ATOL, rtol=0.0)


def test_unnormalized_physical_state_preserves_linearity_of_reduction_and_probability() -> None:
    coefficients = np.array([1.0, 2.0j, -0.5, 0.25 - 0.75j], dtype=np.complex128)
    state = physical_state_from_coefficients(coefficients, 4, normalize=False)
    norm_squared = float(np.vdot(state, state).real)

    assert clock_probability_profile(state, 4) == pytest.approx(
        np.full(4, norm_squared / 4.0)
    )
    for j in range(4):
        assert np.linalg.norm(physical_reduction(state, j, 4)) == pytest.approx(
            np.sqrt(norm_squared)
        )


def test_conditional_dynamics_generalizes_to_dimension_five() -> None:
    dimension = 5
    coefficients = generic_coefficients(dimension)
    state = physical_state_from_coefficients(coefficients, dimension)

    assert clock_probability_profile(state, dimension) == pytest.approx(
        np.full(dimension, 1.0 / dimension)
    )
    assert max(
        conditional_schrodinger_residual(state, j, dimension)
        for j in range(dimension)
    ) <= DEFAULT_ATOL
    assert np.max(one_step_conditional_residuals(state, dimension)) <= DEFAULT_ATOL


def test_formal_conditioning_exists_for_nonphysical_state_but_physical_reduction_rejects_it() -> None:
    nonphysical = tensor_basis_state(0, 1, 4)

    conditioned = condition_on_clock(nonphysical, 0, 4)
    assert conditioned.shape == (4,)
    assert np.linalg.norm(conditioned) == pytest.approx(0.5)

    with pytest.raises(ValueError, match="zero-constraint"):
        physical_reduction(nonphysical, 0, 4)
    with pytest.raises(ValueError, match="zero-constraint"):
        conditional_schrodinger_residual(nonphysical, 1, 4)


def test_system_unitary_and_invalid_inputs_are_checked() -> None:
    unitary = system_evolution_unitary(clock_step(4), 4)
    assert np.allclose(
        unitary.conj().T @ unitary,
        np.eye(4),
        atol=DEFAULT_ATOL,
        rtol=0.0,
    )

    state = equal_amplitude_physical_state(4)
    with pytest.raises(ValueError, match="clock index"):
        condition_on_clock(state, 4, 4)
    with pytest.raises(ValueError, match="shape"):
        condition_on_clock(np.zeros(4, dtype=np.complex128), 0, 4)
