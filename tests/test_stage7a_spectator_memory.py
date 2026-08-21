import itertools

import numpy as np

from t_search.stage5_clock_change import (
    SUBSYSTEMS,
    analytic_physical_basis,
    physical_subspace_projector,
    total_constraint_operator,
)
from t_search.stage5_clock_transforms import genuine_clock_change_operator
from t_search.stage5_reductions import (
    clock_reconstruction_operator,
    clock_relative_support_basis,
    clock_relative_support_projector,
    physical_clock_reduction_operator,
    same_clock_transition_operator,
)
from t_search.stage7_spectator import (
    MEMORY_DIMENSION,
    canonical_stage7a_state,
    memory_identity,
    spectator_clock_change_diagnostics,
    spectator_clock_change_operator,
    spectator_clock_probability,
    spectator_composition_diagnostics,
    spectator_constraint_residual,
    spectator_kinematic_dimension,
    spectator_no_record_diagnostics,
    spectator_physical_basis,
    spectator_physical_dimension,
    spectator_physical_projector,
    spectator_reconstruction_operator,
    spectator_reduction_operator,
    spectator_same_clock_transition_operator,
    spectator_support_basis,
    spectator_support_dimension,
    spectator_support_projector,
    spectator_total_constraint_operator,
    stage7a_summary,
)

ATOL = 1e-10


def test_stage7a_carrier_is_stage5_constraint_tensor_memory_identity():
    h5 = total_constraint_operator()
    h7 = spectator_total_constraint_operator()
    assert MEMORY_DIMENSION == 2
    assert spectator_kinematic_dimension() == 54
    assert h7.shape == (54, 54)
    assert np.allclose(h7, np.kron(h5, memory_identity()), atol=ATOL, rtol=0.0)


def test_stage7a_physical_space_is_exact_spectator_tensor_extension():
    b5 = analytic_physical_basis()
    b7 = spectator_physical_basis()
    assert b5.shape == (27, 7)
    assert b7.shape == (54, 14)
    assert spectator_physical_dimension() == 14
    assert np.allclose(b7, np.kron(b5, memory_identity()), atol=ATOL, rtol=0.0)
    assert np.allclose(b7.conj().T @ b7, np.eye(14), atol=ATOL, rtol=0.0)
    assert np.linalg.norm(spectator_total_constraint_operator() @ b7) <= ATOL


def test_stage7a_analytic_physical_projector_matches_numerical_kernel():
    h7 = spectator_total_constraint_operator()
    eigenvalues, eigenvectors = np.linalg.eigh(h7)
    kernel = eigenvectors[:, np.abs(eigenvalues) <= ATOL]
    numerical_projector = kernel @ kernel.conj().T
    analytic_projector = spectator_physical_projector()
    assert kernel.shape[1] == 14
    assert np.allclose(
        analytic_projector,
        np.kron(physical_subspace_projector(), memory_identity()),
        atol=ATOL,
        rtol=0.0,
    )
    assert np.allclose(analytic_projector, numerical_projector, atol=ATOL, rtol=0.0)


def test_stage7a_supports_are_stage5_supports_tensor_memory():
    for clock in SUBSYSTEMS:
        b5 = clock_relative_support_basis(clock)
        b7 = spectator_support_basis(clock)
        assert b7.shape == (18, 14)
        assert spectator_support_dimension(clock) == 14
        assert np.allclose(b7, np.kron(b5, memory_identity()), atol=ATOL, rtol=0.0)
        assert np.allclose(b7.conj().T @ b7, np.eye(14), atol=ATOL, rtol=0.0)
        assert np.allclose(
            spectator_support_projector(clock),
            np.kron(clock_relative_support_projector(clock), memory_identity()),
            atol=ATOL,
            rtol=0.0,
        )


def test_stage7a_reduction_and_reconstruction_are_identity_extensions():
    for clock in SUBSYSTEMS:
        for index in range(3):
            assert np.allclose(
                spectator_reduction_operator(clock, index),
                np.kron(physical_clock_reduction_operator(clock, index), memory_identity()),
                atol=ATOL,
                rtol=0.0,
            )
            assert np.allclose(
                spectator_reconstruction_operator(clock, index),
                np.kron(clock_reconstruction_operator(clock, index), memory_identity()),
                atol=ATOL,
                rtol=0.0,
            )


def test_stage7a_declared_round_trips_hold_on_physical_and_support_spaces():
    p_phys = spectator_physical_projector()
    for clock in SUBSYSTEMS:
        p_support = spectator_support_projector(clock)
        for index in range(3):
            reduction = spectator_reduction_operator(clock, index)
            reconstruction = spectator_reconstruction_operator(clock, index)
            assert np.allclose(
                reduction @ reconstruction,
                p_support,
                atol=ATOL,
                rtol=0.0,
            )
            assert np.allclose(
                reconstruction @ reduction @ p_phys,
                p_phys,
                atol=ATOL,
                rtol=0.0,
            )


def test_stage7a_canonical_state_is_normalized_physical_and_uniform_clock_probability():
    state = canonical_stage7a_state()
    assert state.shape == (54,)
    assert np.isclose(np.linalg.norm(state), 1.0, atol=ATOL, rtol=0.0)
    assert spectator_constraint_residual(state) <= ATOL
    for clock in SUBSYSTEMS:
        probabilities = [spectator_clock_probability(state, clock, j) for j in range(3)]
        assert np.allclose(probabilities, np.full(3, 1.0 / 3.0), atol=ATOL, rtol=0.0)


def test_stage7a_same_clock_transitions_are_identity_extensions():
    for clock in SUBSYSTEMS:
        for source_index, target_index in itertools.product(range(3), repeat=2):
            assert np.allclose(
                spectator_same_clock_transition_operator(clock, target_index, source_index),
                np.kron(
                    same_clock_transition_operator(clock, target_index, source_index),
                    memory_identity(),
                ),
                atol=ATOL,
                rtol=0.0,
            )


def test_stage7a_genuine_clock_change_is_identity_extension_and_lands_on_direct_target():
    state = canonical_stage7a_state()
    diagnostics = spectator_clock_change_diagnostics()
    assert diagnostics.comparisons == 54
    assert diagnostics.max_state_residual <= ATOL
    assert diagnostics.max_born_residual <= ATOL
    assert diagnostics.max_inverse_residual <= ATOL

    for source_clock, target_clock in itertools.permutations(SUBSYSTEMS, 2):
        operator = spectator_clock_change_operator(target_clock, 2, source_clock, 1)
        assert np.allclose(
            operator,
            np.kron(
                genuine_clock_change_operator(target_clock, 2, source_clock, 1),
                memory_identity(),
            ),
            atol=ATOL,
            rtol=0.0,
        )
        source_state = spectator_reduction_operator(source_clock, 1) @ state
        direct_target = spectator_reduction_operator(target_clock, 2) @ state
        assert np.allclose(operator @ source_state, direct_target, atol=ATOL, rtol=0.0)


def test_stage7a_clock_change_support_inverse_is_preserved():
    for source_clock, target_clock in itertools.permutations(SUBSYSTEMS, 2):
        source_projector = spectator_support_projector(source_clock)
        for source_index, target_index in itertools.product(range(3), repeat=2):
            forward = spectator_clock_change_operator(
                target_clock, target_index, source_clock, source_index
            )
            backward = spectator_clock_change_operator(
                source_clock, source_index, target_clock, target_index
            )
            assert np.allclose(
                backward @ forward,
                source_projector,
                atol=ATOL,
                rtol=0.0,
            )


def test_stage7a_three_clock_composition_survives_spectator_extension():
    diagnostics = spectator_composition_diagnostics()
    assert diagnostics.comparisons == 162
    assert diagnostics.max_composition_residual <= ATOL


def test_stage7a_spectator_memory_is_a_strict_no_record_control():
    diagnostics = spectator_no_record_diagnostics()
    assert diagnostics.comparisons == 18
    assert diagnostics.record_coupling_present is False
    assert diagnostics.max_target_memory_mutual_information <= ATOL
    assert diagnostics.positive_record_witness is False

    summary = stage7a_summary()
    assert summary["physical_dimension"] == 14
    assert summary["support_dimensions"] == {"A": 14, "B": 14, "C": 14}
    assert summary["record_control"]["positive_record_witness"] is False
