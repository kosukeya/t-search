from itertools import permutations, product

import numpy as np
import pytest

from t_search.stage5_clock_change import (
    analytic_physical_basis,
    physical_state_from_coefficients,
    tensor_basis_state,
)
from t_search.stage5_clock_transforms import (
    apply_genuine_clock_change,
    genuine_clock_change_operator,
)
from t_search.stage5_operational import (
    lift_reduced_observable_to_physical,
    perspective_entanglement_entropy,
    pure_bipartite_entanglement_entropy,
    reduce_physical_observable_to_clock,
    reduced_born_probability,
    reduced_expectation_value,
    support_operator_residual,
    transform_reduced_observable,
    validate_reduced_observable,
)
from t_search.stage5_reductions import (
    clock_relative_support_basis,
    clock_relative_support_projector,
    physical_clock_reduction,
)

CLOCKS = ("A", "B", "C")
ATOL = 1e-10


def _generic_physical_state() -> np.ndarray:
    raw = np.array(
        [
            1.0 + 0.2j,
            -0.4 + 0.7j,
            0.3 - 0.1j,
            0.8 + 0.5j,
            -0.2 - 0.6j,
            0.9 - 0.3j,
            0.1 + 0.4j,
        ],
        dtype=np.complex128,
    )
    return physical_state_from_coefficients(raw, normalize=True)


def _support_observable(clock: str) -> np.ndarray:
    basis = clock_relative_support_basis(clock)
    coordinates = np.diag(np.linspace(-1.2, 1.4, 7)).astype(np.complex128)
    coordinates[0, 1] = 0.31 + 0.17j
    coordinates[1, 0] = np.conjugate(coordinates[0, 1])
    coordinates[2, 5] = -0.22 + 0.09j
    coordinates[5, 2] = np.conjugate(coordinates[2, 5])
    return basis @ coordinates @ basis.conj().T


def _support_projector(clock: str) -> np.ndarray:
    basis = clock_relative_support_basis(clock)
    coordinates = np.array(
        [1.0, 0.4j, -0.3 + 0.2j, 0.5, -0.1j, 0.25, -0.45],
        dtype=np.complex128,
    )
    coordinates /= np.linalg.norm(coordinates)
    ket = basis @ coordinates
    return np.outer(ket, ket.conj())


def _perspective_entanglement_control_state() -> np.ndarray:
    return (
        tensor_basis_state(+1, -1, 0)
        + tensor_basis_state(+1, 0, -1)
    ) / np.sqrt(2.0)


def test_transformed_observables_are_hermitian_target_support_operators():
    for source, target in permutations(CLOCKS, 2):
        source_observable = _support_observable(source)
        for j, k in product(range(3), repeat=2):
            transformed = transform_reduced_observable(
                source_observable, target, k, source, j
            )
            assert np.linalg.norm(transformed - transformed.conj().T) <= ATOL
            assert support_operator_residual(transformed, target) <= ATOL


def test_expectation_values_are_clock_perspective_covariant_for_all_pairs():
    physical_state = _generic_physical_state()
    for source, target in permutations(CLOCKS, 2):
        source_observable = _support_observable(source)
        for j, k in product(range(3), repeat=2):
            source_state = physical_clock_reduction(physical_state, source, j)
            target_state = apply_genuine_clock_change(
                source_state, target, k, source, j
            )
            target_observable = transform_reduced_observable(
                source_observable, target, k, source, j
            )
            source_value = reduced_expectation_value(source_state, source_observable)
            target_value = reduced_expectation_value(target_state, target_observable)
            assert np.isclose(source_value, target_value, atol=ATOL, rtol=0.0)


def test_physical_lift_and_target_reduction_match_direct_observable_transform():
    for source, target in permutations(CLOCKS, 2):
        source_observable = _support_observable(source)
        for j, k in product(range(3), repeat=2):
            physical_observable = lift_reduced_observable_to_physical(
                source_observable, source, j
            )
            via_physical = reduce_physical_observable_to_clock(
                physical_observable, target, k
            )
            direct = transform_reduced_observable(
                source_observable, target, k, source, j
            )
            assert np.allclose(via_physical, direct, atol=ATOL, rtol=0.0)


def test_global_physical_and_reduced_expectations_agree():
    physical_state = _generic_physical_state()
    for clock in CLOCKS:
        observable = _support_observable(clock)
        for j in range(3):
            reduced_state = physical_clock_reduction(physical_state, clock, j)
            physical_observable = lift_reduced_observable_to_physical(
                observable, clock, j
            )
            global_value = np.vdot(physical_state, physical_observable @ physical_state)
            local_value = reduced_expectation_value(reduced_state, observable)
            assert abs(global_value.imag) <= ATOL
            assert np.isclose(global_value.real, local_value, atol=ATOL, rtol=0.0)


def test_reduced_density_matrix_transforms_covariantly():
    physical_state = _generic_physical_state()
    for source, target in permutations(CLOCKS, 2):
        for j, k in product(range(3), repeat=2):
            source_state = physical_clock_reduction(physical_state, source, j)
            target_state = physical_clock_reduction(physical_state, target, k)
            transform = genuine_clock_change_operator(target, k, source, j)
            source_density = np.outer(source_state, source_state.conj())
            target_density = np.outer(target_state, target_state.conj())
            transformed_density = transform @ source_density @ transform.conj().T
            assert np.allclose(
                transformed_density, target_density, atol=ATOL, rtol=0.0
            )


def test_rank_one_projectors_remain_projectors_under_clock_change():
    for source, target in permutations(CLOCKS, 2):
        projector = _support_projector(source)
        for j, k in product(range(3), repeat=2):
            transformed = transform_reduced_observable(
                projector, target, k, source, j
            )
            assert np.allclose(transformed @ transformed, transformed, atol=ATOL, rtol=0.0)
            assert np.isclose(np.trace(transformed).real, 1.0, atol=ATOL, rtol=0.0)
            assert support_operator_residual(transformed, target) <= ATOL


def test_born_probabilities_are_clock_perspective_covariant():
    physical_state = _generic_physical_state()
    for source, target in permutations(CLOCKS, 2):
        source_projector = _support_projector(source)
        for j, k in product(range(3), repeat=2):
            source_state = physical_clock_reduction(physical_state, source, j)
            target_state = physical_clock_reduction(physical_state, target, k)
            target_projector = transform_reduced_observable(
                source_projector, target, k, source, j
            )
            source_probability = reduced_born_probability(source_state, source_projector)
            target_probability = reduced_born_probability(target_state, target_projector)
            assert np.isclose(
                source_probability, target_probability, atol=ATOL, rtol=0.0
            )


def test_observable_transformations_follow_cross_clock_composition():
    for source, middle, target in permutations(CLOCKS, 3):
        source_observable = _support_observable(source)
        for j, k, ell in product(range(3), repeat=3):
            middle_observable = transform_reduced_observable(
                source_observable, middle, k, source, j
            )
            composed = transform_reduced_observable(
                middle_observable, target, ell, middle, k
            )
            direct = transform_reduced_observable(
                source_observable, target, ell, source, j
            )
            assert np.allclose(composed, direct, atol=ATOL, rtol=0.0)


def test_reverse_observable_clock_change_returns_source_observable():
    for source, target in permutations(CLOCKS, 2):
        source_observable = _support_observable(source)
        for j, k in product(range(3), repeat=2):
            target_observable = transform_reduced_observable(
                source_observable, target, k, source, j
            )
            recovered = transform_reduced_observable(
                target_observable, source, j, target, k
            )
            assert np.allclose(
                recovered, source_observable, atol=ATOL, rtol=0.0
            )


def test_declared_entanglement_control_is_zero_in_c_and_one_bit_in_a():
    physical_state = _perspective_entanglement_control_state()
    entropy_c = perspective_entanglement_entropy(physical_state, "C", 0)
    entropy_a = perspective_entanglement_entropy(physical_state, "A", 0)
    assert np.isclose(entropy_c, 0.0, atol=ATOL, rtol=0.0)
    assert np.isclose(entropy_a, 1.0, atol=ATOL, rtol=0.0)


def test_entanglement_control_persists_across_all_clock_readings():
    physical_state = _perspective_entanglement_control_state()
    for j in range(3):
        assert np.isclose(
            perspective_entanglement_entropy(physical_state, "A", j),
            1.0,
            atol=ATOL,
            rtol=0.0,
        )
        assert np.isclose(
            perspective_entanglement_entropy(physical_state, "B", j),
            0.0,
            atol=ATOL,
            rtol=0.0,
        )
        assert np.isclose(
            perspective_entanglement_entropy(physical_state, "C", j),
            0.0,
            atol=ATOL,
            rtol=0.0,
        )


def test_operational_api_rejects_invalid_support_observables_states_and_projectors():
    support_basis = clock_relative_support_basis("C")
    nonhermitian_coords = np.zeros((7, 7), dtype=np.complex128)
    nonhermitian_coords[0, 1] = 1.0
    nonhermitian = support_basis @ nonhermitian_coords @ support_basis.conj().T

    with pytest.raises(ValueError):
        validate_reduced_observable(nonhermitian, "C")
    with pytest.raises(ValueError):
        validate_reduced_observable(np.eye(9, dtype=np.complex128), "C")

    normalized = physical_clock_reduction(_generic_physical_state(), "C", 0)
    with pytest.raises(ValueError):
        reduced_expectation_value(2.0 * normalized, _support_observable("C"))

    bad_projector = 0.5 * clock_relative_support_projector("C")
    with pytest.raises(ValueError):
        reduced_born_probability(normalized, bad_projector)

    with pytest.raises(ValueError):
        pure_bipartite_entanglement_entropy(normalized, base=1.0)

    assert analytic_physical_basis().shape[1] == 7
