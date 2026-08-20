import itertools

import numpy as np
import pytest

from t_search.stage5_clock_change import (
    DEFAULT_ATOL,
    analytic_physical_basis,
    physical_state_from_coefficients,
)
from t_search.stage5_clock_transforms import (
    apply_genuine_clock_change,
    genuine_clock_change_operator,
    genuine_clock_change_support_matrix,
)
from t_search.stage5_reductions import (
    clock_relative_support_basis,
    clock_relative_support_projector,
    physical_clock_reduction,
    rest_basis_state,
    rest_subsystems,
)

CLOCKS = ("A", "B", "C")
ORDERED_DISTINCT_CLOCKS = tuple(
    (source, target) for source, target in itertools.permutations(CLOCKS, 2)
)


def _normalized_physical_state() -> np.ndarray:
    coefficients = np.array(
        [1.0, 1.0j, -0.5, 2.0 - 1.0j, 0.25, -1.5j, 0.75 + 0.5j],
        dtype=np.complex128,
    )
    return physical_state_from_coefficients(coefficients, 3, normalize=True)


def _second_normalized_physical_state() -> np.ndarray:
    coefficients = np.array(
        [0.5j, -1.0, 1.5 + 0.25j, 0.75, -0.5j, 2.0j, -1.25],
        dtype=np.complex128,
    )
    return physical_state_from_coefficients(coefficients, 3, normalize=True)


def test_cross_clock_support_matrix_is_unitary_for_all_distinct_clocks_and_readings() -> None:
    for source, target in ORDERED_DISTINCT_CLOCKS:
        for source_index in range(3):
            for target_index in range(3):
                matrix = genuine_clock_change_support_matrix(
                    target, target_index, source, source_index, 3
                )
                assert matrix.shape == (7, 7)
                assert np.allclose(
                    matrix.conj().T @ matrix,
                    np.eye(7),
                    atol=DEFAULT_ATOL,
                    rtol=0.0,
                )
                assert np.allclose(
                    matrix @ matrix.conj().T,
                    np.eye(7),
                    atol=DEFAULT_ATOL,
                    rtol=0.0,
                )


def test_ambient_cross_clock_operator_is_partial_isometry_between_declared_supports() -> None:
    for source, target in ORDERED_DISTINCT_CLOCKS:
        p_source = clock_relative_support_projector(source, 3)
        p_target = clock_relative_support_projector(target, 3)
        for source_index in range(3):
            for target_index in range(3):
                operator = genuine_clock_change_operator(
                    target, target_index, source, source_index, 3
                )
                assert operator.shape == (9, 9)
                assert np.allclose(
                    operator.conj().T @ operator,
                    p_source,
                    atol=DEFAULT_ATOL,
                    rtol=0.0,
                )
                assert np.allclose(
                    operator @ operator.conj().T,
                    p_target,
                    atol=DEFAULT_ATOL,
                    rtol=0.0,
                )


def test_direct_global_route_equals_reconstruct_then_change_clock_for_generic_state() -> None:
    state = _normalized_physical_state()

    for source, target in ORDERED_DISTINCT_CLOCKS:
        for source_index in range(3):
            source_state = physical_clock_reduction(state, source, source_index, 3)
            for target_index in range(3):
                via_change = apply_genuine_clock_change(
                    source_state,
                    target,
                    target_index,
                    source,
                    source_index,
                    3,
                )
                direct = physical_clock_reduction(state, target, target_index, 3)
                assert np.allclose(via_change, direct, atol=DEFAULT_ATOL, rtol=0.0)


def test_direct_global_route_holds_for_every_physical_basis_vector() -> None:
    basis = analytic_physical_basis(3)

    for column in range(basis.shape[1]):
        state = basis[:, column]
        for source, target in ORDERED_DISTINCT_CLOCKS:
            source_state = physical_clock_reduction(state, source, 1, 3)
            via_change = apply_genuine_clock_change(source_state, target, 2, source, 1, 3)
            direct = physical_clock_reduction(state, target, 2, 3)
            assert np.allclose(via_change, direct, atol=DEFAULT_ATOL, rtol=0.0)


def test_two_way_clock_change_round_trip_returns_source_support_projector_ambiently() -> None:
    for source, target in ORDERED_DISTINCT_CLOCKS:
        p_source = clock_relative_support_projector(source, 3)
        for source_index in range(3):
            for target_index in range(3):
                forward = genuine_clock_change_operator(
                    target, target_index, source, source_index, 3
                )
                backward = genuine_clock_change_operator(
                    source, source_index, target, target_index, 3
                )
                assert np.allclose(
                    backward @ forward,
                    p_source,
                    atol=DEFAULT_ATOL,
                    rtol=0.0,
                )


def test_two_way_clock_change_round_trip_is_identity_in_support_coordinates() -> None:
    for source, target in ORDERED_DISTINCT_CLOCKS:
        for source_index in range(3):
            for target_index in range(3):
                forward = genuine_clock_change_support_matrix(
                    target, target_index, source, source_index, 3
                )
                backward = genuine_clock_change_support_matrix(
                    source, source_index, target, target_index, 3
                )
                assert np.allclose(
                    backward @ forward,
                    np.eye(7),
                    atol=DEFAULT_ATOL,
                    rtol=0.0,
                )


def test_clock_change_preserves_norms_and_inner_products_of_physical_descriptions() -> None:
    state_a = _normalized_physical_state()
    state_b = _second_normalized_physical_state()

    for source, target in ORDERED_DISTINCT_CLOCKS:
        source_a = physical_clock_reduction(state_a, source, 1, 3)
        source_b = physical_clock_reduction(state_b, source, 1, 3)
        target_a = apply_genuine_clock_change(source_a, target, 2, source, 1, 3)
        target_b = apply_genuine_clock_change(source_b, target, 2, source, 1, 3)

        assert np.linalg.norm(target_a) == pytest.approx(
            np.linalg.norm(source_a), abs=DEFAULT_ATOL
        )
        assert np.vdot(target_a, target_b) == pytest.approx(
            np.vdot(source_a, source_b), abs=DEFAULT_ATOL
        )


def test_zero_reading_clock_change_relabels_rest_factor_semantics_via_global_triple() -> None:
    # Physical triple (-1,0,+1): C-clock support uses (A,B)=(-1,0),
    # while A-clock support uses (B,C)=(0,+1).
    source = rest_basis_state((-1, 0), 3)
    expected_target = rest_basis_state((0, 1), 3)
    operator = genuine_clock_change_operator("A", 0, "C", 0, 3)

    assert rest_subsystems("C") == ("A", "B")
    assert rest_subsystems("A") == ("B", "C")
    assert np.allclose(operator @ source, expected_target, atol=DEFAULT_ATOL, rtol=0.0)


def test_equal_numeric_zero_readings_do_not_make_genuine_clock_change_ambient_identity() -> None:
    operator = genuine_clock_change_operator("A", 0, "C", 0, 3)
    p_source = clock_relative_support_projector("C", 3)
    p_target = clock_relative_support_projector("A", 3)

    assert not np.allclose(operator, np.eye(9), atol=DEFAULT_ATOL, rtol=0.0)
    assert not np.allclose(operator, p_source, atol=DEFAULT_ATOL, rtol=0.0)
    assert not np.allclose(operator, p_target, atol=DEFAULT_ATOL, rtol=0.0)


def test_clock_change_output_lands_in_target_support_for_all_pairs_and_readings() -> None:
    state = _normalized_physical_state()
    for source, target in ORDERED_DISTINCT_CLOCKS:
        p_target = clock_relative_support_projector(target, 3)
        for source_index in range(3):
            source_state = physical_clock_reduction(state, source, source_index, 3)
            for target_index in range(3):
                transformed = apply_genuine_clock_change(
                    source_state, target, target_index, source, source_index, 3
                )
                assert np.allclose(
                    p_target @ transformed,
                    transformed,
                    atol=DEFAULT_ATOL,
                    rtol=0.0,
                )


def test_same_clock_request_is_rejected_as_not_a_genuine_clock_change() -> None:
    with pytest.raises(ValueError, match="distinct"):
        genuine_clock_change_operator("A", 1, "A", 0, 3)
    with pytest.raises(ValueError, match="distinct"):
        genuine_clock_change_support_matrix("B", 2, "B", 1, 3)


def test_off_support_wrong_shape_and_invalid_clock_inputs_are_rejected() -> None:
    source_projector = clock_relative_support_projector("C", 3)
    off_support_index = next(
        index for index in range(9) if np.linalg.norm(source_projector[:, index]) <= DEFAULT_ATOL
    )
    off_support = np.zeros(9, dtype=np.complex128)
    off_support[off_support_index] = 1.0

    with pytest.raises(ValueError, match="source-clock support"):
        apply_genuine_clock_change(off_support, "A", 0, "C", 0, 3)
    with pytest.raises(ValueError, match="shape"):
        apply_genuine_clock_change(np.zeros(8), "A", 0, "C", 0, 3)
    with pytest.raises(ValueError, match="one of"):
        genuine_clock_change_operator("D", 0, "C", 0, 3)
    with pytest.raises(ValueError, match="clock index"):
        genuine_clock_change_operator("A", 3, "C", 0, 3)
