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
)
from t_search.stage5_cross_clock_composition import (
    apply_cross_clock_route,
    closed_three_clock_loop_operator,
    closed_three_clock_loop_support_matrix,
    composed_cross_clock_operator,
    cross_clock_composition_support_matrices,
    direct_cross_clock_operator,
    ordered_distinct_clock_triples,
    source_support_projector,
)
from t_search.stage5_reductions import (
    clock_relative_support_basis,
    physical_clock_reduction,
)


def _generic_physical_state() -> np.ndarray:
    coefficients = np.array(
        [1.0, 1.0j, -0.5, 2.0 - 1.0j, 0.25, -1.5j, 0.75 + 0.5j],
        dtype=np.complex128,
    )
    return physical_state_from_coefficients(coefficients, 3, normalize=True)


def test_ordered_distinct_clock_triples_are_exactly_the_six_permutations() -> None:
    triples = ordered_distinct_clock_triples()
    assert len(triples) == 6
    assert len(set(triples)) == 6
    assert set(triples) == {
        ("A", "B", "C"),
        ("A", "C", "B"),
        ("B", "A", "C"),
        ("B", "C", "A"),
        ("C", "A", "B"),
        ("C", "B", "A"),
    }


def test_canonical_composition_scan_contains_162_three_clock_cases() -> None:
    case_count = 0
    for _source, _middle, _target in ordered_distinct_clock_triples():
        for _j in range(3):
            for _k in range(3):
                for _ell in range(3):
                    case_count += 1
    assert case_count == 6 * 3**3 == 162


def test_ambient_cross_clock_composition_matches_direct_map_for_all_162_cases() -> None:
    for source, middle, target in ordered_distinct_clock_triples():
        for j in range(3):
            for k in range(3):
                for ell in range(3):
                    composed = composed_cross_clock_operator(
                        target, ell, middle, k, source, j, 3
                    )
                    direct = direct_cross_clock_operator(
                        target, ell, middle, source, j, 3
                    )
                    assert np.allclose(composed, direct, atol=DEFAULT_ATOL, rtol=0.0)


def test_support_coordinate_cross_clock_composition_matches_direct_for_all_cases() -> None:
    for source, middle, target in ordered_distinct_clock_triples():
        for j in range(3):
            for k in range(3):
                for ell in range(3):
                    composed, direct = cross_clock_composition_support_matrices(
                        target, ell, middle, k, source, j, 3
                    )
                    assert composed.shape == direct.shape == (7, 7)
                    assert np.allclose(composed, direct, atol=DEFAULT_ATOL, rtol=0.0)


def test_intermediate_clock_reading_cancels_from_the_final_map() -> None:
    for source, middle, target in ordered_distinct_clock_triples():
        for j in range(3):
            for ell in range(3):
                references = [
                    composed_cross_clock_operator(target, ell, middle, k, source, j, 3)
                    for k in range(3)
                ]
                assert np.allclose(references[0], references[1], atol=DEFAULT_ATOL, rtol=0.0)
                assert np.allclose(references[0], references[2], atol=DEFAULT_ATOL, rtol=0.0)


def test_generic_physical_state_is_path_independent_for_all_162_cases() -> None:
    state = _generic_physical_state()
    for source, middle, target in ordered_distinct_clock_triples():
        for j in range(3):
            source_state = physical_clock_reduction(state, source, j, 3)
            for k in range(3):
                for ell in range(3):
                    routed = apply_cross_clock_route(
                        source_state, target, ell, middle, k, source, j, 3
                    )
                    direct = apply_genuine_clock_change(
                        source_state, target, ell, source, j, 3
                    )
                    expected = physical_clock_reduction(state, target, ell, 3)
                    assert np.allclose(routed, direct, atol=DEFAULT_ATOL, rtol=0.0)
                    assert np.allclose(routed, expected, atol=DEFAULT_ATOL, rtol=0.0)


def test_every_physical_basis_state_obeys_three_clock_path_independence() -> None:
    physical_basis = analytic_physical_basis(3)
    for basis_index in range(physical_basis.shape[1]):
        state = physical_basis[:, basis_index]
        for source, middle, target in ordered_distinct_clock_triples():
            for j in range(3):
                source_state = physical_clock_reduction(state, source, j, 3)
                for k in range(3):
                    for ell in range(3):
                        routed = apply_cross_clock_route(
                            source_state, target, ell, middle, k, source, j, 3
                        )
                        expected = physical_clock_reduction(state, target, ell, 3)
                        assert np.allclose(routed, expected, atol=DEFAULT_ATOL, rtol=0.0)


def test_closed_three_clock_loop_equals_source_support_projector_ambiently() -> None:
    for source, second, third in ordered_distinct_clock_triples():
        projector = source_support_projector(source, 3)
        for j in range(3):
            for k in range(3):
                for ell in range(3):
                    loop = closed_three_clock_loop_operator(
                        source, j, second, k, third, ell, 3
                    )
                    assert np.allclose(loop, projector, atol=DEFAULT_ATOL, rtol=0.0)


def test_closed_three_clock_loop_is_identity_on_source_support_coordinates() -> None:
    for source, second, third in ordered_distinct_clock_triples():
        for j in range(3):
            for k in range(3):
                for ell in range(3):
                    loop = closed_three_clock_loop_support_matrix(
                        source, j, second, k, third, ell, 3
                    )
                    assert np.allclose(loop, np.eye(7), atol=DEFAULT_ATOL, rtol=0.0)


def test_decisive_c_to_a_to_b_route_matches_direct_c_to_b_and_is_nontrivial() -> None:
    composed = composed_cross_clock_operator("B", 2, "A", 1, "C", 0, 3)
    direct = genuine_clock_change_operator("B", 2, "C", 0, 3)
    assert np.allclose(composed, direct, atol=DEFAULT_ATOL, rtol=0.0)
    assert not np.allclose(composed, np.eye(9), atol=DEFAULT_ATOL, rtol=0.0)


def test_two_leg_route_preserves_norms_and_inner_products_on_source_support() -> None:
    coefficients_a = np.array([1, 1j, 2, -1, 0.5j, 0.25, -2j], dtype=np.complex128)
    coefficients_b = np.array([0.5, -1j, 1, 2j, -0.5, 1.25, 0.75j], dtype=np.complex128)
    global_a = physical_state_from_coefficients(coefficients_a, 3, normalize=True)
    global_b = physical_state_from_coefficients(coefficients_b, 3, normalize=True)

    source_a = physical_clock_reduction(global_a, "C", 0, 3)
    source_b = physical_clock_reduction(global_b, "C", 0, 3)
    routed_a = apply_cross_clock_route(source_a, "B", 2, "A", 1, "C", 0, 3)
    routed_b = apply_cross_clock_route(source_b, "B", 2, "A", 1, "C", 0, 3)

    assert np.linalg.norm(routed_a) == pytest.approx(np.linalg.norm(source_a), abs=DEFAULT_ATOL)
    assert np.linalg.norm(routed_b) == pytest.approx(np.linalg.norm(source_b), abs=DEFAULT_ATOL)
    assert np.vdot(routed_a, routed_b) == pytest.approx(np.vdot(source_a, source_b), abs=DEFAULT_ATOL)


def test_invalid_repeated_clocks_and_off_support_source_states_are_rejected() -> None:
    with pytest.raises(ValueError, match="three distinct"):
        composed_cross_clock_operator("C", 0, "A", 0, "A", 0, 3)
    with pytest.raises(ValueError, match="three distinct"):
        composed_cross_clock_operator("A", 0, "A", 0, "C", 0, 3)

    source_basis = clock_relative_support_basis("C", 3)
    projector = source_basis @ source_basis.conj().T
    off_support_index = next(
        idx for idx in range(9) if np.linalg.norm(projector[:, idx]) <= DEFAULT_ATOL
    )
    off_support = np.zeros(9, dtype=np.complex128)
    off_support[off_support_index] = 1.0

    with pytest.raises(ValueError, match="source-clock support"):
        apply_cross_clock_route(off_support, "B", 0, "A", 0, "C", 0, 3)

    with pytest.raises(ValueError, match="shape"):
        apply_cross_clock_route(np.zeros(8), "B", 0, "A", 0, "C", 0, 3)
