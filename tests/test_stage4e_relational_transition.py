import numpy as np
import pytest

from t_search.stage4_conditional import physical_reduction, system_evolution_unitary
from t_search.stage4_quantum import (
    DEFAULT_ATOL,
    clock_step,
    physical_state_from_coefficients,
)
from t_search.stage4_transition import (
    expected_system_transition_matrix,
    origin_covariance_residual,
    physical_reduction_transition_residual,
    relational_transition_matrix,
    transition_composition_residual,
    transition_expected_residual,
    transition_identity_residual,
    transition_inverse_residual,
    transition_unitarity_residual,
)


def _generic_coefficients(dimension: int) -> np.ndarray:
    values = np.array(
        [complex(1 + n, (-1) ** n * (n + 0.5)) for n in range(dimension)],
        dtype=np.complex128,
    )
    return values / np.linalg.norm(values)


def test_all_canonical_transitions_equal_expected_system_unitaries():
    d = 4
    for source in range(d):
        for target in range(d):
            assert transition_expected_residual(source, target, d) <= DEFAULT_ATOL


def test_transition_identity_holds_at_every_clock_reading():
    for j in range(4):
        assert transition_identity_residual(j, 4) <= DEFAULT_ATOL


def test_transition_inverse_holds_for_every_ordered_pair():
    d = 4
    for source in range(d):
        for target in range(d):
            assert transition_inverse_residual(source, target, d) <= DEFAULT_ATOL


def test_transition_composition_holds_for_every_canonical_triple():
    d = 4
    for source in range(d):
        for middle in range(d):
            for target in range(d):
                assert (
                    transition_composition_residual(source, middle, target, d)
                    <= DEFAULT_ATOL
                )


def test_every_relational_transition_is_unitary():
    d = 4
    for source in range(d):
        for target in range(d):
            assert transition_unitarity_residual(source, target, d) <= DEFAULT_ATOL


def test_transition_propagates_actual_physical_reductions():
    d = 4
    state = physical_state_from_coefficients(_generic_coefficients(d), d)
    for source in range(d):
        for target in range(d):
            assert (
                physical_reduction_transition_residual(state, source, target, d)
                <= DEFAULT_ATOL
            )


def test_periodic_wraparound_is_the_same_one_step_system_unitary():
    d = 4
    wrap = relational_transition_matrix(d - 1, 0, d)
    one_step = system_evolution_unitary(clock_step(d), d)
    assert np.allclose(wrap, one_step, atol=DEFAULT_ATOL, rtol=0.0)


def test_common_non_grid_origin_shift_leaves_transition_family_unchanged():
    d = 4
    alpha = 0.37
    for source in range(d):
        for target in range(d):
            assert origin_covariance_residual(source, target, alpha, d) <= DEFAULT_ATOL


def test_origin_shift_changes_local_representatives_but_not_relational_transition():
    d = 4
    alpha = 0.37
    state = physical_state_from_coefficients(_generic_coefficients(d), d)
    psi_reference = physical_reduction(state, 1, d, origin=0.0)
    psi_shifted = physical_reduction(state, 1, d, origin=alpha)
    expected_shift = system_evolution_unitary(alpha, d) @ psi_reference
    assert np.allclose(psi_shifted, expected_shift, atol=DEFAULT_ATOL, rtol=0.0)
    assert not np.allclose(psi_shifted, psi_reference, atol=1e-6, rtol=0.0)
    assert origin_covariance_residual(1, 3, alpha, d) <= DEFAULT_ATOL


def test_d5_transition_structure_preserves_expected_unitary_and_composition():
    d = 5
    alpha = 0.23
    for source, middle, target in [(0, 2, 4), (4, 1, 3), (3, 0, 1)]:
        assert transition_expected_residual(source, target, d) <= DEFAULT_ATOL
        assert (
            transition_composition_residual(source, middle, target, d)
            <= DEFAULT_ATOL
        )
        assert origin_covariance_residual(source, target, alpha, d) <= DEFAULT_ATOL


def test_expected_transition_depends_only_on_clock_difference_not_absolute_origin():
    d = 4
    reference = expected_system_transition_matrix(1, 3, d, origin=0.0)
    shifted = expected_system_transition_matrix(1, 3, d, origin=0.618)
    assert np.allclose(reference, shifted, atol=DEFAULT_ATOL, rtol=0.0)


def test_invalid_transition_indices_are_rejected():
    with pytest.raises(ValueError, match="clock index"):
        relational_transition_matrix(-1, 0, 4)
    with pytest.raises(ValueError, match="clock index"):
        relational_transition_matrix(0, 4, 4)
