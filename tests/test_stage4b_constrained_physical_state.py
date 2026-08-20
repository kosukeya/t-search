import numpy as np
import pytest

from t_search.stage4_quantum import (
    DEFAULT_ATOL,
    canonical_stage4b_model,
    constraint_kernel_basis,
    constraint_kernel_projector,
    constraint_residual,
    equal_amplitude_physical_state,
    evolve_under_constraint,
    is_physical_state,
    matched_energy_basis,
    physical_state_from_coefficients,
    physical_subspace_dimension,
    physical_subspace_projector,
    stationarity_residual,
    tensor_basis_state,
    total_constraint_operator,
)


def test_total_constraint_has_declared_shape_spectrum_and_hermiticity() -> None:
    h_total = total_constraint_operator(4)

    assert h_total.shape == (16, 16)
    assert np.allclose(h_total, h_total.conj().T, atol=DEFAULT_ATOL, rtol=0.0)
    expected_diagonal = np.array(
        [
            0, 1, 2, 3,
            -1, 0, 1, 2,
            -2, -1, 0, 1,
            -3, -2, -1, 0,
        ],
        dtype=float,
    )
    assert np.allclose(np.diag(h_total), expected_diagonal)


def test_analytic_matched_energy_basis_is_orthonormal_and_annihilated_by_constraint() -> None:
    basis = matched_energy_basis(4)
    h_total = total_constraint_operator(4)

    assert basis.shape == (16, 4)
    assert np.allclose(basis.conj().T @ basis, np.eye(4), atol=DEFAULT_ATOL, rtol=0.0)
    assert np.allclose(h_total @ basis, np.zeros((16, 4)), atol=DEFAULT_ATOL, rtol=0.0)


def test_numerical_kernel_matches_analytic_matched_energy_subspace() -> None:
    numerical_basis = constraint_kernel_basis(4)

    assert numerical_basis.shape == (16, 4)
    assert physical_subspace_dimension(4) == 4
    assert np.allclose(
        constraint_kernel_projector(4),
        physical_subspace_projector(4),
        atol=DEFAULT_ATOL,
        rtol=0.0,
    )


def test_canonical_model_reports_16_kinematic_and_4_physical_dimensions() -> None:
    model = canonical_stage4b_model(4)

    assert model.kinematic_dimension == 16
    assert model.physical_dimension == 4
    assert model.h_total.shape == (16, 16)
    assert model.physical_basis.shape == (16, 4)


def test_equal_amplitude_state_is_normalized_and_exactly_physical() -> None:
    state = equal_amplitude_physical_state(4)

    assert np.vdot(state, state).real == pytest.approx(1.0)
    assert constraint_residual(state, 4) == pytest.approx(0.0, abs=DEFAULT_ATOL)
    assert is_physical_state(state, 4)


def test_generic_complex_coefficients_define_physical_state_not_just_equal_amplitudes() -> None:
    coefficients = np.array([1.0, 1.0j, -2.0, 0.5 - 0.5j], dtype=np.complex128)
    coefficients /= np.linalg.norm(coefficients)
    state = physical_state_from_coefficients(coefficients, 4)

    recovered = matched_energy_basis(4).conj().T @ state
    assert np.allclose(recovered, coefficients, atol=DEFAULT_ATOL, rtol=0.0)
    assert np.vdot(state, state).real == pytest.approx(1.0)
    assert constraint_residual(state, 4) == pytest.approx(0.0, abs=DEFAULT_ATOL)
    assert is_physical_state(state, 4)


def test_explicit_off_diagonal_energy_state_is_not_physical() -> None:
    state = tensor_basis_state(0, 1, 4)

    assert constraint_residual(state, 4) == pytest.approx(1.0)
    assert is_physical_state(state, 4) is False


def test_equal_amplitude_physical_state_is_stationary_for_multiple_external_parameters() -> None:
    state = equal_amplitude_physical_state(4)

    for parameter in (-3.1, -0.4, 0.0, 0.37, 2.5, 9.0):
        evolved = evolve_under_constraint(state, parameter, 4)
        assert np.allclose(evolved, state, atol=DEFAULT_ATOL, rtol=0.0)
        assert stationarity_residual(state, parameter, 4) == pytest.approx(
            0.0, abs=DEFAULT_ATOL
        )


def test_generic_physical_state_is_stationary_but_nonphysical_state_is_not() -> None:
    coefficients = np.array([1.0, 2.0j, -1.0, 3.0 - 1.0j], dtype=np.complex128)
    physical = physical_state_from_coefficients(coefficients, 4, normalize=True)
    nonphysical = tensor_basis_state(0, 1, 4)

    assert stationarity_residual(physical, 0.37, 4) == pytest.approx(
        0.0, abs=DEFAULT_ATOL
    )
    assert stationarity_residual(nonphysical, 0.37, 4) > 1e-3


def test_stage4b_kernel_structure_generalizes_to_dimension_five() -> None:
    dimension = 5

    assert total_constraint_operator(dimension).shape == (25, 25)
    assert constraint_kernel_basis(dimension).shape == (25, 5)
    assert physical_subspace_dimension(dimension) == 5
    assert np.allclose(
        constraint_kernel_projector(dimension),
        physical_subspace_projector(dimension),
        atol=DEFAULT_ATOL,
        rtol=0.0,
    )


def test_normalize_option_preserves_direction_and_returns_unit_state() -> None:
    coefficients = np.array([1.0, 2.0, 0.0, -1.0j], dtype=np.complex128)
    state = physical_state_from_coefficients(coefficients, 4, normalize=True)
    recovered = matched_energy_basis(4).conj().T @ state

    assert np.vdot(state, state).real == pytest.approx(1.0)
    assert np.allclose(
        recovered,
        coefficients / np.linalg.norm(coefficients),
        atol=DEFAULT_ATOL,
        rtol=0.0,
    )


def test_invalid_global_shapes_coefficients_and_basis_indices_are_rejected() -> None:
    with pytest.raises(ValueError, match="coefficients must have shape"):
        physical_state_from_coefficients(np.ones(3), 4)
    with pytest.raises(ValueError, match="nonzero"):
        physical_state_from_coefficients(np.zeros(4), 4)
    with pytest.raises(ValueError, match="global state must have shape"):
        constraint_residual(np.zeros(4), 4)
    with pytest.raises(ValueError, match="basis indices"):
        tensor_basis_state(4, 0, 4)
