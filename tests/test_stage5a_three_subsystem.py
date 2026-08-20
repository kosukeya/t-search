import numpy as np
import pytest

from t_search.stage5_clock_change import (
    DEFAULT_ATOL,
    DEFAULT_RATES,
    analytic_physical_basis,
    canonical_stage5a_model,
    centered_energy_labels,
    clock_basis_matrix,
    clock_reading_times,
    clock_state,
    clock_step,
    clock_translation_unitary,
    constraint_compatible_triples,
    constraint_residual,
    kinematic_dimension,
    numerical_constraint_kernel_basis,
    numerical_kernel_projector,
    physical_state_from_coefficients,
    physical_subspace_dimension,
    physical_subspace_projector,
    subsystem_hamiltonian,
    tensor_basis_state,
    total_constraint_operator,
)


def test_canonical_qutrit_labels_local_hamiltonians_and_kinematic_dimension() -> None:
    labels = centered_energy_labels(3)
    h = subsystem_hamiltonian(3)

    assert np.array_equal(labels, np.array([-1, 0, 1]))
    assert np.allclose(np.diag(h), np.array([-1.0, 0.0, 1.0]))
    assert np.allclose(h, h.conj().T, atol=DEFAULT_ATOL, rtol=0.0)
    assert kinematic_dimension(3) == 27


def test_total_constraint_is_27_by_27_hermitian_and_has_expected_diagonal_rule() -> None:
    h_total = total_constraint_operator(3)
    labels = (-1, 0, 1)
    expected = np.array([a + b + c for a in labels for b in labels for c in labels])

    assert h_total.shape == (27, 27)
    assert np.allclose(h_total, h_total.conj().T, atol=DEFAULT_ATOL, rtol=0.0)
    assert np.allclose(np.diag(h_total), expected, atol=DEFAULT_ATOL, rtol=0.0)


def test_canonical_constraint_has_exactly_seven_zero_sum_energy_triples() -> None:
    triples = constraint_compatible_triples(3)
    expected = {
        (0, 0, 0),
        (1, -1, 0),
        (1, 0, -1),
        (-1, 1, 0),
        (-1, 0, 1),
        (0, 1, -1),
        (0, -1, 1),
    }

    assert len(triples) == 7
    assert set(triples) == expected
    assert physical_subspace_dimension(3) == 7


def test_analytic_physical_basis_is_orthonormal_and_annihilated_by_constraint() -> None:
    basis = analytic_physical_basis(3)
    h_total = total_constraint_operator(3)

    assert basis.shape == (27, 7)
    assert np.allclose(basis.conj().T @ basis, np.eye(7), atol=DEFAULT_ATOL, rtol=0.0)
    assert np.allclose(h_total @ basis, np.zeros((27, 7)), atol=DEFAULT_ATOL, rtol=0.0)


def test_numerical_zero_eigenspace_matches_analytic_physical_projector() -> None:
    numerical = numerical_constraint_kernel_basis(3)

    assert numerical.shape == (27, 7)
    assert np.allclose(
        numerical_kernel_projector(3),
        physical_subspace_projector(3),
        atol=DEFAULT_ATOL,
        rtol=0.0,
    )


def test_generic_complex_coefficients_embed_into_the_seven_dimensional_physical_space() -> None:
    coefficients = np.array(
        [1.0, 1.0j, -2.0, 0.5 - 0.25j, -1.5j, 0.75, -0.3 + 0.4j],
        dtype=np.complex128,
    )
    state = physical_state_from_coefficients(coefficients, 3, normalize=True)
    recovered = analytic_physical_basis(3).conj().T @ state

    assert np.vdot(state, state).real == pytest.approx(1.0)
    assert np.allclose(
        recovered,
        coefficients / np.linalg.norm(coefficients),
        atol=DEFAULT_ATOL,
        rtol=0.0,
    )
    assert constraint_residual(state, 3) == pytest.approx(0.0, abs=DEFAULT_ATOL)


def test_explicit_nonzero_total_energy_basis_state_is_not_physical() -> None:
    state = tensor_basis_state(1, 1, 1, 3)

    assert constraint_residual(state, 3) == pytest.approx(3.0)


def test_each_subsystem_has_the_declared_orthonormal_three_reading_dft_clock() -> None:
    model = canonical_stage5a_model(3)

    assert set(model.clock_bases) == {"A", "B", "C"}
    for subsystem in ("A", "B", "C"):
        basis = model.clock_bases[subsystem]
        assert basis.shape == (3, 3)
        assert np.allclose(
            basis.conj().T @ basis,
            np.eye(3),
            atol=DEFAULT_ATOL,
            rtol=0.0,
        )


def test_clock_reading_coordinates_and_step_match_symmetric_qutrit_protocol() -> None:
    expected_step = 2.0 * np.pi / 3.0

    assert clock_step(3) == pytest.approx(expected_step)
    assert np.allclose(
        clock_reading_times(3),
        np.array([0.0, expected_step, 2.0 * expected_step]),
        atol=DEFAULT_ATOL,
        rtol=0.0,
    )


def test_positive_hamiltonian_translates_each_clock_state_forward_cyclically() -> None:
    translation = clock_translation_unitary(3)

    for j in range(3):
        actual = translation @ clock_state(j, 3)
        expected = clock_state((j + 1) % 3, 3)
        assert np.allclose(actual, expected, atol=DEFAULT_ATOL, rtol=0.0)


def test_three_clock_steps_return_the_identity_without_introducing_external_time() -> None:
    full_cycle = clock_translation_unitary(3, steps=3)

    assert np.allclose(full_cycle, np.eye(3), atol=DEFAULT_ATOL, rtol=0.0)
    for j in range(3):
        assert np.allclose(
            full_cycle @ clock_state(j, 3),
            clock_state(j, 3),
            atol=DEFAULT_ATOL,
            rtol=0.0,
        )


def test_canonical_model_and_invalid_inputs_respect_stage5a_scope() -> None:
    model = canonical_stage5a_model(3, rates=DEFAULT_RATES)

    assert model.kinematic_dimension == 27
    assert model.physical_dimension == 7
    assert model.physical_basis.shape == (27, 7)
    assert np.array_equal(model.energy_labels, np.array([-1, 0, 1]))

    with pytest.raises(ValueError, match="odd integer"):
        centered_energy_labels(4)
    with pytest.raises(ValueError, match="positive real"):
        subsystem_hamiltonian(3, rate=0.0)
    with pytest.raises(ValueError, match="clock index"):
        clock_state(3, 3)
    with pytest.raises(ValueError, match="outside"):
        tensor_basis_state(2, 0, 0, 3)
    with pytest.raises(ValueError, match="shape"):
        physical_state_from_coefficients(np.ones(6), 3)
