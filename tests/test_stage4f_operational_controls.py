import numpy as np
import pytest

from t_search.stage4_conditional import physical_reduction
from t_search.stage4_controls import (
    born_consistency_residual,
    density_matrix_residual,
    energy_basis_physical_projection_matrix,
    energy_basis_projection_nullity,
    energy_basis_projection_rank,
    formal_conditional_schrodinger_residual,
    global_conditional_born_probability,
    local_born_probability,
    normalized_formal_conditional_state,
    plus01_projector,
    ray_fidelity,
)
from t_search.stage4_quantum import (
    DEFAULT_ATOL,
    equal_amplitude_physical_state,
    physical_state_from_coefficients,
    system_hamiltonian,
    tensor_basis_state,
)


def _generic_coefficients(dimension: int) -> np.ndarray:
    values = np.array(
        [complex(1 + n, (-1) ** n * (n + 0.25)) for n in range(dimension)],
        dtype=np.complex128,
    )
    return values / np.linalg.norm(values)


def _constraint_violating_state(dimension: int = 4) -> np.ndarray:
    return (
        tensor_basis_state(0, 0, dimension)
        + tensor_basis_state(0, 1, dimension)
    ) / np.sqrt(2.0)


def test_plus01_projector_is_noncommuting_with_system_hamiltonian():
    projector = plus01_projector(4)
    commutator = system_hamiltonian(4) @ projector - projector @ system_hamiltonian(4)
    assert np.linalg.norm(commutator) > 0.1


def test_global_and_local_born_probabilities_agree_at_every_clock_reading():
    state = equal_amplitude_physical_state(4)
    projector = plus01_projector(4)
    for j in range(4):
        assert born_consistency_residual(state, j, projector, 4) <= DEFAULT_ATOL


def test_noncommuting_observable_has_expected_nontrivial_probability_profile():
    state = equal_amplitude_physical_state(4)
    projector = plus01_projector(4)
    expected = np.array([0.5, 0.25, 0.0, 0.25])
    global_profile = np.array(
        [global_conditional_born_probability(state, j, projector, 4) for j in range(4)]
    )
    local_profile = np.array(
        [local_born_probability(state, j, projector, 4) for j in range(4)]
    )
    assert np.allclose(global_profile, expected, atol=DEFAULT_ATOL, rtol=0.0)
    assert np.allclose(local_profile, expected, atol=DEFAULT_ATOL, rtol=0.0)


def test_generic_complex_physical_state_preserves_global_local_born_consistency():
    state = physical_state_from_coefficients(_generic_coefficients(4), 4)
    projector = plus01_projector(4)
    for j in range(4):
        assert born_consistency_residual(state, j, projector, 4) <= DEFAULT_ATOL


def test_global_conditional_born_probability_rejects_nonphysical_state():
    with pytest.raises(ValueError, match="zero-constraint"):
        global_conditional_born_probability(
            _constraint_violating_state(), 0, plus01_projector(4), 4
        )


def test_constraint_violating_formal_conditionals_are_reading_independent():
    state = _constraint_violating_state()
    reference = normalized_formal_conditional_state(state, 0, 4)
    for j in range(1, 4):
        conditional = normalized_formal_conditional_state(state, j, 4)
        assert np.allclose(conditional, reference, atol=DEFAULT_ATOL, rtol=0.0)


def test_constraint_violating_state_fails_expected_schrodinger_relation():
    state = _constraint_violating_state()
    residual = formal_conditional_schrodinger_residual(
        state, 1, 4, reference_index=0
    )
    assert residual > 0.5


def test_single_energy_physical_state_changes_as_vector_but_not_as_ray():
    state = tensor_basis_state(1, 1, 4)
    psi_0 = physical_reduction(state, 0, 4)
    psi_1 = physical_reduction(state, 1, 4)
    assert np.linalg.norm(psi_1 - psi_0) > 1.0
    assert abs(ray_fidelity(psi_0, psi_1, 4) - 1.0) <= DEFAULT_ATOL


def test_single_energy_density_matrix_is_identical_at_all_clock_readings():
    state = tensor_basis_state(1, 1, 4)
    psi_0 = physical_reduction(state, 0, 4)
    for j in range(1, 4):
        psi_j = physical_reduction(state, j, 4)
        assert density_matrix_residual(psi_0, psi_j, 4) <= DEFAULT_ATOL


def test_clock_energy_basis_projection_is_rank_one_and_noninjective_on_hphys():
    d = 4
    for m in range(d):
        assert energy_basis_projection_rank(m, d) == 1
        assert energy_basis_projection_nullity(m, d) == d - 1


def test_distinct_physical_coefficient_vectors_can_share_same_energy_basis_projection():
    d = 4
    projection = energy_basis_physical_projection_matrix(0, d)
    coefficients_a = np.array([1.0, 0.0, 0.0, 0.0], dtype=np.complex128)
    coefficients_b = np.array([1.0, 2.0j, -0.5, 3.0], dtype=np.complex128)
    assert not np.allclose(coefficients_a, coefficients_b, atol=DEFAULT_ATOL, rtol=0.0)
    assert np.allclose(
        projection @ coefficients_a,
        projection @ coefficients_b,
        atol=DEFAULT_ATOL,
        rtol=0.0,
    )


def test_d5_operational_consistency_and_wrong_basis_noninjectivity_persist():
    d = 5
    state = physical_state_from_coefficients(_generic_coefficients(d), d)
    projector = plus01_projector(d)
    for j in range(d):
        assert born_consistency_residual(state, j, projector, d) <= DEFAULT_ATOL
    assert energy_basis_projection_rank(2, d) == 1
    assert energy_basis_projection_nullity(2, d) == d - 1
