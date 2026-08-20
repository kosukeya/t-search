import numpy as np
import pytest

from t_search.stage5_clock_change import (
    DEFAULT_ATOL,
    analytic_physical_basis,
    clock_reading_times,
    constraint_residual,
    physical_state_from_coefficients,
    tensor_basis_state,
)
from t_search.stage5_reductions import (
    clock_reconstruction_operator,
    clock_relative_support_basis,
    clock_relative_support_dimension,
    clock_relative_support_pairs,
    clock_relative_support_projector,
    expected_same_clock_transition_operator,
    formal_clock_conditioning,
    physical_clock_probability,
    physical_clock_reduction,
    physical_clock_reduction_operator,
    reconstruct_physical_state,
    rest_hamiltonian,
    rest_subsystems,
    same_clock_transition_operator,
    same_clock_transition_support_matrix,
    support_coordinate_reduction_matrix,
)

CLOCKS = ("A", "B", "C")


def _normalized_physical_state() -> np.ndarray:
    coefficients = np.array(
        [1.0, 1.0j, -0.5, 2.0 - 1.0j, 0.25, -1.5j, 0.75 + 0.5j],
        dtype=np.complex128,
    )
    return physical_state_from_coefficients(coefficients, 3, normalize=True)


def test_each_clock_support_is_seven_dimensional_inside_nine_dimensional_rest_space() -> None:
    for clock in CLOCKS:
        basis = clock_relative_support_basis(clock, 3)
        projector = clock_relative_support_projector(clock, 3)

        assert basis.shape == (9, 7)
        assert clock_relative_support_dimension(clock, 3) == 7
        assert np.linalg.matrix_rank(basis) == 7
        assert np.allclose(basis.conj().T @ basis, np.eye(7), atol=DEFAULT_ATOL, rtol=0.0)
        assert np.allclose(projector @ projector, projector, atol=DEFAULT_ATOL, rtol=0.0)
        assert np.trace(projector).real == pytest.approx(7.0)
        assert np.linalg.matrix_rank(projector) == 7
        assert np.linalg.matrix_rank(projector) < projector.shape[0]


def test_support_pairs_are_unique_and_follow_the_declared_rest_factor_order() -> None:
    assert rest_subsystems("A") == ("B", "C")
    assert rest_subsystems("B") == ("A", "C")
    assert rest_subsystems("C") == ("A", "B")

    expected_c = (
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 0),
        (0, 1),
        (1, -1),
        (1, 0),
    )
    assert clock_relative_support_pairs("C", 3) == expected_c
    for clock in CLOCKS:
        pairs = clock_relative_support_pairs(clock, 3)
        assert len(pairs) == len(set(pairs)) == 7


def test_reduction_coordinate_matrix_is_unitary_for_all_clocks_and_readings() -> None:
    for clock in CLOCKS:
        for index in range(3):
            matrix = support_coordinate_reduction_matrix(clock, index, 3)
            assert matrix.shape == (7, 7)
            assert np.allclose(matrix.conj().T @ matrix, np.eye(7), atol=DEFAULT_ATOL, rtol=0.0)
            assert np.allclose(matrix @ matrix.conj().T, np.eye(7), atol=DEFAULT_ATOL, rtol=0.0)


def test_ideal_clock_probability_is_one_third_for_generic_physical_state() -> None:
    state = _normalized_physical_state()

    for clock in CLOCKS:
        probabilities = [physical_clock_probability(state, clock, j, 3) for j in range(3)]
        assert probabilities == pytest.approx([1.0 / 3.0] * 3, abs=DEFAULT_ATOL)
        assert sum(probabilities) == pytest.approx(1.0, abs=DEFAULT_ATOL)


def test_physical_reduction_preserves_norm_and_lands_in_declared_support() -> None:
    state = _normalized_physical_state()

    for clock in CLOCKS:
        projector = clock_relative_support_projector(clock, 3)
        for index in range(3):
            reduced = physical_clock_reduction(state, clock, index, 3)
            assert np.linalg.norm(reduced) == pytest.approx(1.0, abs=DEFAULT_ATOL)
            assert np.allclose(projector @ reduced, reduced, atol=DEFAULT_ATOL, rtol=0.0)


def test_reduction_and_reconstruction_round_trip_on_both_physical_sides() -> None:
    state = _normalized_physical_state()

    for clock in CLOCKS:
        support_projector = clock_relative_support_projector(clock, 3)
        for index in range(3):
            reduction = physical_clock_reduction_operator(clock, index, 3)
            reconstruction = clock_reconstruction_operator(clock, index, 3)

            assert np.allclose(
                reduction @ reconstruction,
                support_projector,
                atol=DEFAULT_ATOL,
                rtol=0.0,
            )

            reduced = physical_clock_reduction(state, clock, index, 3)
            recovered = reconstruct_physical_state(reduced, clock, index, 3)
            assert np.allclose(recovered, state, atol=DEFAULT_ATOL, rtol=0.0)

            physical_basis = analytic_physical_basis(3)
            assert np.allclose(
                reconstruction @ reduction @ physical_basis,
                physical_basis,
                atol=DEFAULT_ATOL,
                rtol=0.0,
            )


def test_reduction_preserves_inner_products_between_generic_physical_states() -> None:
    coefficients_a = np.array([1, 1j, 2, -1, 0.5j, 0.25, -2j], dtype=np.complex128)
    coefficients_b = np.array([0.5, -1j, 1, 2j, -0.5, 1.25, 0.75j], dtype=np.complex128)
    state_a = physical_state_from_coefficients(coefficients_a, 3, normalize=True)
    state_b = physical_state_from_coefficients(coefficients_b, 3, normalize=True)
    global_overlap = np.vdot(state_a, state_b)

    for clock in CLOCKS:
        for index in range(3):
            reduced_a = physical_clock_reduction(state_a, clock, index, 3)
            reduced_b = physical_clock_reduction(state_b, clock, index, 3)
            assert np.vdot(reduced_a, reduced_b) == pytest.approx(global_overlap, abs=DEFAULT_ATOL)


def test_rest_hamiltonian_has_expected_shape_and_preserves_support() -> None:
    expected_diagonal = {
        "A": np.array([-2, -1, 0, -1, 0, 1, 0, 1, 2], dtype=float),
        "B": np.array([-2, -1, 0, -1, 0, 1, 0, 1, 2], dtype=float),
        "C": np.array([-2, -1, 0, -1, 0, 1, 0, 1, 2], dtype=float),
    }
    for clock in CLOCKS:
        h_rest = rest_hamiltonian(clock, 3)
        projector = clock_relative_support_projector(clock, 3)
        assert h_rest.shape == (9, 9)
        assert np.allclose(np.diag(h_rest).real, expected_diagonal[clock])
        assert np.allclose(h_rest @ projector, projector @ h_rest, atol=DEFAULT_ATOL, rtol=0.0)


def test_same_clock_transition_matches_rest_hamiltonian_evolution_on_support() -> None:
    for clock in CLOCKS:
        for source in range(3):
            for target in range(3):
                actual = same_clock_transition_operator(clock, target, source, 3)
                expected = expected_same_clock_transition_operator(clock, target, source, 3)
                assert np.allclose(actual, expected, atol=DEFAULT_ATOL, rtol=0.0)


def test_same_clock_transition_has_identity_inverse_and_composition_on_support() -> None:
    for clock in CLOCKS:
        for j in range(3):
            identity = same_clock_transition_support_matrix(clock, j, j, 3)
            assert np.allclose(identity, np.eye(7), atol=DEFAULT_ATOL, rtol=0.0)

        for j in range(3):
            for k in range(3):
                forward = same_clock_transition_support_matrix(clock, k, j, 3)
                backward = same_clock_transition_support_matrix(clock, j, k, 3)
                assert np.allclose(backward @ forward, np.eye(7), atol=DEFAULT_ATOL, rtol=0.0)

                for ell in range(3):
                    second = same_clock_transition_support_matrix(clock, ell, k, 3)
                    direct = same_clock_transition_support_matrix(clock, ell, j, 3)
                    assert np.allclose(second @ forward, direct, atol=DEFAULT_ATOL, rtol=0.0)


def test_formal_conditioning_remains_defined_but_physical_reduction_rejects_nonphysical_state() -> None:
    nonphysical = tensor_basis_state(1, 1, 1, 3)
    assert constraint_residual(nonphysical, 3) == pytest.approx(3.0)

    conditioned = formal_clock_conditioning(nonphysical, "A", 0, 3)
    assert conditioned.shape == (9,)
    assert np.linalg.norm(conditioned) > 0.0

    with pytest.raises(ValueError, match="must satisfy"):
        physical_clock_reduction(nonphysical, "A", 0, 3)
    with pytest.raises(ValueError, match="must satisfy"):
        physical_clock_probability(nonphysical, "A", 0, 3)


def test_off_support_reconstruction_unnormalized_probability_and_invalid_inputs_are_rejected() -> None:
    support_projector = clock_relative_support_projector("C", 3)
    off_support_basis_index = next(
        index for index in range(9) if np.linalg.norm(support_projector[:, index]) <= DEFAULT_ATOL
    )
    off_support = np.zeros(9, dtype=np.complex128)
    off_support[off_support_basis_index] = 1.0

    with pytest.raises(ValueError, match="must lie"):
        reconstruct_physical_state(off_support, "C", 0, 3)

    normalized = _normalized_physical_state()
    with pytest.raises(ValueError, match="normalized"):
        physical_clock_probability(2.0 * normalized, "C", 0, 3)

    with pytest.raises(ValueError, match="one of"):
        clock_relative_support_basis("D", 3)
    with pytest.raises(ValueError, match="clock index"):
        physical_clock_reduction(normalized, "A", 3, 3)
