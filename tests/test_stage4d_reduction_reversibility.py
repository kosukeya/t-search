import numpy as np
import pytest

from t_search.stage4_conditional import condition_on_clock, physical_reduction
from t_search.stage4_quantum import (
    DEFAULT_ATOL,
    is_physical_state,
    matched_energy_basis,
    physical_state_from_coefficients,
    tensor_basis_state,
)
from t_search.stage4_reduction import (
    kinematic_projection_matrix,
    kinematic_projection_nullity,
    kinematic_projection_rank,
    lift_after_kinematic_projection_operator,
    physical_reduction_matrix,
    physical_roundtrip_residual,
    reconstruct_physical_state,
    reconstruction_matrix,
    system_roundtrip_residual,
)


def _generic_coefficients() -> np.ndarray:
    raw = np.array(
        [1.0 + 0.5j, -0.4 + 0.8j, 0.25 - 0.3j, -0.7 - 0.2j],
        dtype=np.complex128,
    )
    return raw / np.linalg.norm(raw)


def test_kinematic_projection_has_expected_shape_rank_and_nullity() -> None:
    for j in range(4):
        projection = kinematic_projection_matrix(j, 4)
        assert projection.shape == (4, 16)
        assert kinematic_projection_rank(j, 4) == 4
        assert kinematic_projection_nullity(j, 4) == 12


def test_explicit_nonzero_kinematic_kernel_vector_projects_to_zero() -> None:
    kernel_vector = (
        tensor_basis_state(0, 2, 4) - tensor_basis_state(1, 2, 4)
    ) / np.sqrt(2.0)

    assert np.linalg.norm(kernel_vector) == pytest.approx(1.0)
    assert np.linalg.norm(kinematic_projection_matrix(0, 4) @ kernel_vector) < DEFAULT_ATOL
    assert np.linalg.norm(condition_on_clock(kernel_vector, 0, 4)) < DEFAULT_ATOL


def test_distinct_kinematic_vectors_can_have_identical_clock_projection() -> None:
    base = tensor_basis_state(0, 0, 4)
    kernel_vector = (
        tensor_basis_state(0, 2, 4) - tensor_basis_state(1, 2, 4)
    ) / np.sqrt(2.0)
    shifted = base + kernel_vector

    assert not np.allclose(base, shifted, atol=DEFAULT_ATOL, rtol=0.0)
    assert np.allclose(
        kinematic_projection_matrix(0, 4) @ base,
        kinematic_projection_matrix(0, 4) @ shifted,
        atol=DEFAULT_ATOL,
        rtol=0.0,
    )


def test_physical_reduction_matrix_is_unitary_in_physical_coordinates() -> None:
    identity = np.eye(4, dtype=np.complex128)
    for j in range(4):
        reduction = physical_reduction_matrix(j, 4)
        assert reduction.shape == (4, 4)
        assert np.allclose(
            reduction.conj().T @ reduction,
            identity,
            atol=DEFAULT_ATOL,
            rtol=0.0,
        )
        assert np.allclose(
            reduction @ reduction.conj().T,
            identity,
            atol=DEFAULT_ATOL,
            rtol=0.0,
        )


def test_reduction_followed_by_explicit_inverse_is_identity_on_system_space() -> None:
    identity = np.eye(4, dtype=np.complex128)
    for j in range(4):
        reduction_from_kinematic = np.sqrt(4.0) * kinematic_projection_matrix(j, 4)
        inverse = reconstruction_matrix(j, 4)
        assert np.allclose(
            reduction_from_kinematic @ inverse,
            identity,
            atol=DEFAULT_ATOL,
            rtol=0.0,
        )


def test_reconstruction_maps_arbitrary_system_vector_into_physical_subspace() -> None:
    system_state = np.array(
        [0.3 + 0.1j, -0.2 + 0.4j, 0.8 - 0.1j, -0.5j],
        dtype=np.complex128,
    )
    for j in range(4):
        reconstructed = reconstruct_physical_state(system_state, j, 4)
        assert is_physical_state(reconstructed, 4)
        assert system_roundtrip_residual(system_state, j, 4) < DEFAULT_ATOL


def test_physical_state_roundtrip_is_identity_for_generic_complex_state() -> None:
    state = physical_state_from_coefficients(_generic_coefficients(), 4)

    for j in range(4):
        assert physical_roundtrip_residual(state, j, 4) < DEFAULT_ATOL


def test_physical_reduction_preserves_inner_products() -> None:
    coefficients_a = _generic_coefficients()
    coefficients_b = np.array(
        [0.2 - 0.6j, 0.7 + 0.1j, -0.3 + 0.2j, 0.1 + 0.4j],
        dtype=np.complex128,
    )
    coefficients_b /= np.linalg.norm(coefficients_b)
    state_a = physical_state_from_coefficients(coefficients_a, 4)
    state_b = physical_state_from_coefficients(coefficients_b, 4)
    global_inner = np.vdot(state_a, state_b)

    for j in range(4):
        reduced_inner = np.vdot(
            physical_reduction(state_a, j, 4),
            physical_reduction(state_b, j, 4),
        )
        assert reduced_inner == pytest.approx(global_inner, abs=DEFAULT_ATOL)


def test_physical_reduction_preserves_norm_for_unnormalized_physical_vectors() -> None:
    coefficients = np.array(
        [2.0 + 0.5j, -1.0j, 0.25 + 0.1j, 0.8 - 0.4j],
        dtype=np.complex128,
    )
    state = physical_state_from_coefficients(coefficients, 4)
    global_norm = np.linalg.norm(state)

    for j in range(4):
        assert np.linalg.norm(physical_reduction(state, j, 4)) == pytest.approx(
            global_norm, abs=DEFAULT_ATOL
        )


def test_full_kinematic_lift_after_projection_is_not_identity_but_is_identity_on_physical_subspace() -> None:
    physical_basis = matched_energy_basis(4)
    identity_kinematic = np.eye(16, dtype=np.complex128)

    for j in range(4):
        operator = lift_after_kinematic_projection_operator(j, 4)
        assert np.linalg.matrix_rank(operator, tol=DEFAULT_ATOL) == 4
        assert not np.allclose(
            operator, identity_kinematic, atol=DEFAULT_ATOL, rtol=0.0
        )
        assert np.allclose(
            operator @ physical_basis,
            physical_basis,
            atol=DEFAULT_ATOL,
            rtol=0.0,
        )


def test_reduction_reversibility_generalizes_to_dimension_five() -> None:
    dimension = 5
    raw = np.array(
        [1.0 + 0.1j, -0.2 + 0.3j, 0.4 - 0.5j, 0.6 + 0.2j, -0.1 - 0.7j],
        dtype=np.complex128,
    )
    state = physical_state_from_coefficients(raw / np.linalg.norm(raw), dimension)

    for j in range(dimension):
        assert kinematic_projection_rank(j, dimension) == dimension
        assert kinematic_projection_nullity(j, dimension) == dimension**2 - dimension
        reduction = physical_reduction_matrix(j, dimension)
        assert np.allclose(
            reduction.conj().T @ reduction,
            np.eye(dimension),
            atol=DEFAULT_ATOL,
            rtol=0.0,
        )
        assert physical_roundtrip_residual(state, j, dimension) < DEFAULT_ATOL


def test_invalid_inputs_and_nonphysical_roundtrip_are_rejected() -> None:
    with pytest.raises(ValueError, match="clock index"):
        kinematic_projection_matrix(4, 4)
    with pytest.raises(ValueError, match="system state"):
        reconstruct_physical_state(np.zeros(3), 0, 4)
    with pytest.raises(ValueError, match="zero-constraint"):
        physical_roundtrip_residual(tensor_basis_state(0, 1, 4), 0, 4)
