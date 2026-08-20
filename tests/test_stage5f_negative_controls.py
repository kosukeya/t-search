from itertools import permutations, product

import numpy as np
import pytest

from t_search.stage5_clock_change import (
    SUBSYSTEMS,
    analytic_physical_basis,
    physical_state_from_coefficients,
    tensor_basis_state,
)
from t_search.stage5_clock_transforms import (
    apply_genuine_clock_change,
    genuine_clock_change_operator,
)
from t_search.stage5_negative_controls import (
    ambient_clock_change_rank,
    ambient_clock_change_unitarity_residuals,
    energy_basis_conditioning_physical_matrix,
    energy_basis_conditioning_rank,
    first_off_support_pair,
    same_numeric_reading_semantic_witness,
)
from t_search.stage5_operational import (
    reduced_expectation_value,
    transform_reduced_observable,
    validate_reduced_observable,
)
from t_search.stage5_reductions import (
    clock_relative_support_projector,
    formal_clock_conditioning,
    physical_clock_reduction,
    rest_basis_state,
    support_coordinate_reduction_matrix,
)

CLOCKS = SUBSYSTEMS


def _naive_observable_control_state() -> np.ndarray:
    # Physical basis ordering is lexicographic in the zero-sum triples.  The
    # first and sixth canonical triples are (-1,0,+1) and (+1,-1,0).
    coefficients = np.zeros(7, dtype=np.complex128)
    coefficients[0] = 2.0
    coefficients[5] = 1.0
    return physical_state_from_coefficients(coefficients, normalize=True)


def test_embedded_clock_changes_are_rank_seven_not_full_rest_unitaries():
    for source, target in permutations(CLOCKS, 2):
        for j, k in product(range(3), repeat=2):
            assert ambient_clock_change_rank(target, k, source, j) == 7
            left, right = ambient_clock_change_unitarity_residuals(
                target, k, source, j
            )
            assert left > 1.0
            assert right > 1.0


def test_off_support_rest_vectors_are_annihilated_by_embedded_clock_change():
    for source, target in permutations(CLOCKS, 2):
        pair = first_off_support_pair(source)
        state = rest_basis_state(pair)
        operator = genuine_clock_change_operator(target, 0, source, 0)
        assert np.linalg.norm(operator @ state) <= 1e-10


def test_full_rest_round_trip_is_support_projector_not_identity():
    for source, target in permutations(CLOCKS, 2):
        forward = genuine_clock_change_operator(target, 1, source, 0)
        reverse = genuine_clock_change_operator(source, 0, target, 1)
        round_trip = reverse @ forward
        support = clock_relative_support_projector(source)
        identity = np.eye(9, dtype=np.complex128)
        assert np.linalg.norm(round_trip - support) <= 1e-10
        assert np.linalg.norm(round_trip - identity) > 1.0


def test_energy_basis_conditioning_has_expected_232_rank_pattern():
    expected = {-1: 2, 0: 3, 1: 2}
    for clock in CLOCKS:
        for label, rank in expected.items():
            assert energy_basis_conditioning_rank(clock, label) == rank


def test_energy_basis_conditioning_has_nontrivial_physical_kernel():
    for clock in CLOCKS:
        for label in (-1, 0, 1):
            matrix = energy_basis_conditioning_physical_matrix(clock, label)
            _, singular_values, vh = np.linalg.svd(matrix, full_matrices=True)
            rank = int(np.sum(singular_values > 1e-10))
            null_vector = vh.conj().T[:, rank]
            assert np.linalg.norm(null_vector) == pytest.approx(1.0)
            assert np.linalg.norm(matrix @ null_vector) <= 1e-10


def test_ideal_dft_reduction_is_full_rank_on_physical_coordinates():
    for clock in CLOCKS:
        for j in range(3):
            ideal = support_coordinate_reduction_matrix(clock, j)
            assert ideal.shape == (7, 7)
            assert np.linalg.matrix_rank(ideal, tol=1e-10) == 7
        assert max(energy_basis_conditioning_rank(clock, m) for m in (-1, 0, 1)) < 7


def test_nonphysical_state_can_still_be_formally_conditioned():
    nonphysical = tensor_basis_state(1, 1, 1)
    for clock in CLOCKS:
        for j in range(3):
            conditioned = formal_clock_conditioning(nonphysical, clock, j)
            assert np.linalg.norm(conditioned) == pytest.approx(1.0 / np.sqrt(3.0))


def test_nonphysical_state_is_rejected_by_physical_clock_reduction():
    nonphysical = tensor_basis_state(1, 1, 1)
    for clock in CLOCKS:
        for j in range(3):
            with pytest.raises(ValueError, match="must satisfy"):
                physical_clock_reduction(nonphysical, clock, j)


def test_genuine_clock_change_api_rejects_off_support_source_state():
    for source, target in permutations(CLOCKS, 2):
        pair = first_off_support_pair(source)
        off_support = rest_basis_state(pair)
        with pytest.raises(ValueError, match="source-clock support"):
            apply_genuine_clock_change(off_support, target, 0, source, 0)


def test_same_bare_valid_observable_can_change_expectation_across_perspectives():
    state = _naive_observable_control_state()
    source_state = physical_clock_reduction(state, "C", 0)
    target_state = physical_clock_reduction(state, "A", 0)

    # The same ambient basis projector |(-1,0)><(-1,0)| is support-valid in
    # both perspectives, but refers to (A,B)=(-1,0) for C-clock and
    # (B,C)=(-1,0) for A-clock.  These correspond to different global sectors.
    ket = rest_basis_state((-1, 0))
    bare = np.outer(ket, ket.conj())
    validate_reduced_observable(bare, "C")
    validate_reduced_observable(bare, "A")

    source_value = reduced_expectation_value(source_state, bare)
    naive_target_value = reduced_expectation_value(target_state, bare)
    assert source_value == pytest.approx(0.8)
    assert naive_target_value == pytest.approx(0.2)
    assert abs(source_value - naive_target_value) > 0.5


def test_transforming_observable_restores_operational_equality():
    state = _naive_observable_control_state()
    source_state = physical_clock_reduction(state, "C", 0)
    target_state = physical_clock_reduction(state, "A", 0)
    ket = rest_basis_state((-1, 0))
    source_observable = np.outer(ket, ket.conj())

    target_observable = transform_reduced_observable(
        source_observable,
        "A",
        0,
        "C",
        0,
    )
    source_value = reduced_expectation_value(source_state, source_observable)
    target_value = reduced_expectation_value(target_state, target_observable)
    assert source_value == pytest.approx(0.8)
    assert target_value == pytest.approx(source_value, abs=1e-10)


def test_equal_numeric_readings_do_not_identify_rest_factor_semantics():
    source_rest, source_pair, target_rest, target_pair = same_numeric_reading_semantic_witness(
        "C", "A", (-1, 0, 1)
    )
    assert source_rest == ("A", "B")
    assert source_pair == (-1, 0)
    assert target_rest == ("B", "C")
    assert target_pair == (0, 1)

    source_ket = rest_basis_state(source_pair)
    target_ket = rest_basis_state(target_pair)
    transform = genuine_clock_change_operator("A", 0, "C", 0)
    assert np.linalg.norm(transform @ source_ket - target_ket) <= 1e-10
    assert np.linalg.norm(transform - np.eye(9, dtype=np.complex128)) > 1.0
