import numpy as np
import pytest

from t_search.stage4_quantum import (
    DEFAULT_ATOL,
    canonical_stage4a_kinematics,
    clock_basis_matrix,
    clock_gram_matrix,
    clock_hamiltonian,
    clock_reading_times,
    clock_state,
    clock_state_at_time,
    clock_step,
    clock_translation_unitary,
    cyclic_clock_index,
    is_clock_basis_orthonormal,
    kinematic_dimension,
    standard_basis,
    system_hamiltonian,
    translate_clock_state,
    unitary_from_hermitian,
)


def test_canonical_dimensions_and_energy_bases_are_explicit() -> None:
    fixture = canonical_stage4a_kinematics()

    assert fixture.clock_dimension == 4
    assert fixture.system_dimension == 4
    assert fixture.kinematic_dimension == 16
    assert fixture.h_clock.shape == (4, 4)
    assert fixture.h_system.shape == (4, 4)
    assert fixture.clock_basis.shape == (4, 4)
    assert standard_basis(4).shape == (4, 4)
    assert np.allclose(standard_basis(4).conj().T @ standard_basis(4), np.eye(4))


def test_clock_and_system_hamiltonians_have_declared_spectra_and_are_hermitian() -> None:
    h_system = system_hamiltonian(4)
    h_clock = clock_hamiltonian(4)

    assert np.allclose(np.diag(h_system), np.array([0.0, 1.0, 2.0, 3.0]))
    assert np.allclose(np.diag(h_clock), np.array([0.0, -1.0, -2.0, -3.0]))
    assert np.allclose(h_system, h_system.conj().T)
    assert np.allclose(h_clock, h_clock.conj().T)


def test_canonical_clock_readings_match_four_step_cycle() -> None:
    times = clock_reading_times(4)

    assert times == pytest.approx((0.0, np.pi / 2, np.pi, 3 * np.pi / 2))
    assert clock_step(4) == pytest.approx(np.pi / 2)
    assert kinematic_dimension(4, 4) == 16


def test_dft_clock_basis_is_orthonormal() -> None:
    gram = clock_gram_matrix(4)

    assert is_clock_basis_orthonormal(4)
    assert np.allclose(gram, np.eye(4), atol=DEFAULT_ATOL, rtol=0.0)
    assert np.allclose(
        clock_basis_matrix(4).conj().T @ clock_basis_matrix(4),
        np.eye(4),
        atol=DEFAULT_ATOL,
        rtol=0.0,
    )


def test_every_clock_state_is_normalized_and_matches_arbitrary_time_constructor() -> None:
    for j, time in enumerate(clock_reading_times(4)):
        state = clock_state(j, 4)
        assert np.vdot(state, state).real == pytest.approx(1.0)
        assert np.allclose(state, clock_state_at_time(time, 4), atol=DEFAULT_ATOL, rtol=0.0)


def test_one_step_clock_translation_advances_every_reading_cyclically() -> None:
    for j in range(4):
        translated = translate_clock_state(clock_state(j, 4), 4, steps=1)
        expected = clock_state((j + 1) % 4, 4)
        assert np.allclose(translated, expected, atol=DEFAULT_ATOL, rtol=0.0)


def test_multi_step_translation_and_wraparound_follow_modular_clock_labels() -> None:
    for j in range(4):
        for steps in (-5, -1, 0, 1, 2, 4, 7):
            translated = translate_clock_state(clock_state(j, 4), 4, steps=steps)
            expected = clock_state((j + steps) % 4, 4)
            assert np.allclose(translated, expected, atol=DEFAULT_ATOL, rtol=0.0)
            assert cyclic_clock_index(j + steps, 4) == (j + steps) % 4


def test_full_period_clock_translation_is_identity() -> None:
    full_period = clock_translation_unitary(4, steps=4)

    assert np.allclose(full_period, np.eye(4), atol=DEFAULT_ATOL, rtol=0.0)
    assert np.allclose(
        full_period.conj().T @ full_period,
        np.eye(4),
        atol=DEFAULT_ATOL,
        rtol=0.0,
    )


def test_clock_origin_shift_preserves_orthonormality_and_translation_rule() -> None:
    origin = 0.37

    assert is_clock_basis_orthonormal(4, origin=origin)
    shifted_times = clock_reading_times(4, origin=origin)
    assert shifted_times[0] == pytest.approx(origin)

    for j in range(4):
        translated = translate_clock_state(clock_state(j, 4, origin=origin), 4)
        expected_time = shifted_times[j] + clock_step(4)
        expected = clock_state_at_time(expected_time, 4)
        assert np.allclose(translated, expected, atol=DEFAULT_ATOL, rtol=0.0)


def test_clock_kinematics_generalizes_to_another_finite_dimension() -> None:
    dimension = 5

    assert kinematic_dimension(dimension, dimension) == 25
    assert is_clock_basis_orthonormal(dimension)

    for j in range(dimension):
        translated = translate_clock_state(clock_state(j, dimension), dimension)
        expected = clock_state((j + 1) % dimension, dimension)
        assert np.allclose(translated, expected, atol=DEFAULT_ATOL, rtol=0.0)

    assert np.allclose(
        clock_translation_unitary(dimension, steps=dimension),
        np.eye(dimension),
        atol=DEFAULT_ATOL,
        rtol=0.0,
    )


def test_generic_hermitian_exponential_is_unitary() -> None:
    hamiltonian = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128)
    unitary = unitary_from_hermitian(hamiltonian, 0.4)

    assert np.allclose(unitary.conj().T @ unitary, np.eye(2), atol=DEFAULT_ATOL, rtol=0.0)


def test_invalid_dimensions_indices_states_and_hamiltonians_are_rejected() -> None:
    with pytest.raises(ValueError, match="at least two"):
        system_hamiltonian(1)
    with pytest.raises(ValueError, match="integer"):
        clock_hamiltonian(4.5)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="clock index"):
        clock_state(4, 4)
    with pytest.raises(ValueError, match="shape"):
        translate_clock_state(np.zeros(3, dtype=np.complex128), 4)
    with pytest.raises(ValueError, match="square matrix"):
        unitary_from_hermitian(np.zeros((2, 3)), 1.0)
    with pytest.raises(ValueError, match="Hermitian"):
        unitary_from_hermitian(np.array([[0.0, 1.0], [0.0, 0.0]]), 1.0)
