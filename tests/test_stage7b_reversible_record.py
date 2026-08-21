import numpy as np

from t_search.stage7_record import (
    CANONICAL_CLOCK,
    CANONICAL_CLOCK_INDEX,
    TARGET_LABEL,
    TARGET_POSITION,
    WRONG_TARGET_LABEL,
    WRONG_TARGET_POSITION,
    apply_record_write,
    canonical_record_source_state,
    canonical_target_pair_projector,
    canonical_wrong_target_pair_projector,
    controlled_record_write_ambient_operator,
    controlled_record_write_support_matrix,
    memory_pauli_z,
    no_record_support_matrix,
    physical_record_automorphism_operator,
    stage7b_record_diagnostics,
    stage7b_summary,
    target_memory_joint_distribution,
    target_memory_mutual_information,
)
from t_search.stage7_spectator import (
    spectator_constraint_residual,
    spectator_physical_basis,
    spectator_reconstruction_operator,
    spectator_reduction_operator,
    spectator_support_basis,
    spectator_support_projector,
)

ATOL = 1e-10


def test_stage7b_explicit_target_wrong_target_and_memory_readout_are_nontrivial():
    assert CANONICAL_CLOCK == "A"
    assert CANONICAL_CLOCK_INDEX == 0
    assert (TARGET_POSITION, TARGET_LABEL) == (0, -1)
    assert (WRONG_TARGET_POSITION, WRONG_TARGET_LABEL) == (1, 1)

    q = canonical_target_pair_projector()
    w = canonical_wrong_target_pair_projector()
    z = memory_pauli_z()
    assert q.shape == (7, 7)
    assert w.shape == (7, 7)
    assert z.shape == (2, 2)
    assert np.allclose(q @ q, q, atol=ATOL, rtol=0.0)
    assert np.allclose(w @ w, w, atol=ATOL, rtol=0.0)
    assert not np.allclose(q, w, atol=ATOL, rtol=0.0)
    assert np.allclose(np.linalg.eigvalsh(z), [-1.0, 1.0], atol=ATOL, rtol=0.0)


def test_stage7b_canonical_source_balances_target_and_wrong_target_independently():
    state = canonical_record_source_state()
    support = spectator_support_projector(CANONICAL_CLOCK)
    assert np.isclose(np.linalg.norm(state), 1.0, atol=ATOL, rtol=0.0)
    assert np.linalg.norm((np.eye(state.size) - support) @ state) <= ATOL

    q_joint = target_memory_joint_distribution(
        state, position=TARGET_POSITION, label=TARGET_LABEL
    )
    w_joint = target_memory_joint_distribution(
        state, position=WRONG_TARGET_POSITION, label=WRONG_TARGET_LABEL
    )
    expected_unwritten = np.array([[0.5, 0.0], [0.5, 0.0]])
    assert np.allclose(q_joint, expected_unwritten, atol=ATOL, rtol=0.0)
    assert np.allclose(w_joint, expected_unwritten, atol=ATOL, rtol=0.0)
    assert target_memory_mutual_information(state) <= ATOL


def test_stage7b_record_write_is_reversible_unitary_on_declared_support():
    u = controlled_record_write_support_matrix()
    identity = np.eye(u.shape[0])
    assert u.shape == (14, 14)
    assert np.allclose(u.conj().T @ u, identity, atol=ATOL, rtol=0.0)
    assert np.allclose(u @ u, identity, atol=ATOL, rtol=0.0)
    assert np.allclose(no_record_support_matrix(), identity, atol=ATOL, rtol=0.0)


def test_stage7b_ambient_completion_is_unitary_and_support_preserving():
    u = controlled_record_write_ambient_operator()
    support = spectator_support_projector(CANONICAL_CLOCK)
    identity = np.eye(u.shape[0])
    assert u.shape == (18, 18)
    assert np.allclose(u.conj().T @ u, identity, atol=ATOL, rtol=0.0)
    assert np.allclose(u @ support, support @ u, atol=ATOL, rtol=0.0)


def test_stage7b_intended_write_creates_one_bit_target_specific_record():
    initial = canonical_record_source_state()
    recorded = apply_record_write(initial)

    q_joint = target_memory_joint_distribution(
        recorded, position=TARGET_POSITION, label=TARGET_LABEL
    )
    expected_record = np.array([[0.5, 0.0], [0.0, 0.5]])
    assert np.allclose(q_joint, expected_record, atol=ATOL, rtol=0.0)
    assert np.isclose(
        target_memory_mutual_information(recorded), 1.0, atol=ATOL, rtol=0.0
    )


def test_stage7b_wrong_target_remains_independent_after_record_write():
    recorded = apply_record_write(canonical_record_source_state())
    wrong_joint = target_memory_joint_distribution(
        recorded,
        position=WRONG_TARGET_POSITION,
        label=WRONG_TARGET_LABEL,
    )
    assert np.allclose(wrong_joint, np.full((2, 2), 0.25), atol=ATOL, rtol=0.0)
    wrong_information = target_memory_mutual_information(
        recorded,
        position=WRONG_TARGET_POSITION,
        label=WRONG_TARGET_LABEL,
    )
    assert wrong_information <= ATOL


def test_stage7b_no_record_identity_control_does_not_create_target_information():
    initial = canonical_record_source_state()
    support = spectator_support_basis(CANONICAL_CLOCK)
    coords = support.conj().T @ initial
    unchanged = support @ (no_record_support_matrix() @ coords)
    assert np.allclose(unchanged, initial, atol=ATOL, rtol=0.0)
    assert target_memory_mutual_information(unchanged) <= ATOL


def test_stage7b_second_application_erases_record_and_recovers_source_exactly():
    initial = canonical_record_source_state()
    once = apply_record_write(initial)
    twice = apply_record_write(once)
    assert np.allclose(twice, initial, atol=ATOL, rtol=0.0)
    assert target_memory_mutual_information(twice) <= ATOL


def test_stage7b_lifted_write_is_unitary_on_common_physical_subspace_and_constraint_safe():
    physical_basis = spectator_physical_basis()
    u_phys = physical_record_automorphism_operator()
    coordinates = physical_basis.conj().T @ u_phys @ physical_basis
    assert np.allclose(
        coordinates.conj().T @ coordinates,
        np.eye(coordinates.shape[0]),
        atol=ATOL,
        rtol=0.0,
    )

    reduced_initial = canonical_record_source_state()
    physical_initial = spectator_reconstruction_operator(CANONICAL_CLOCK, 0) @ reduced_initial
    physical_recorded = u_phys @ physical_initial
    assert spectator_constraint_residual(physical_recorded) <= ATOL
    reduced_again = spectator_reduction_operator(CANONICAL_CLOCK, 0) @ physical_recorded
    assert np.allclose(reduced_again, apply_record_write(reduced_initial), atol=ATOL, rtol=0.0)


def test_stage7b_diagnostics_require_target_specific_gain_not_generic_correlation():
    diagnostics = stage7b_record_diagnostics()
    assert diagnostics.target_information_before <= ATOL
    assert diagnostics.target_information_no_record <= ATOL
    assert np.isclose(diagnostics.target_information_after, 1.0, atol=ATOL, rtol=0.0)
    assert np.isclose(diagnostics.target_information_gain, 1.0, atol=ATOL, rtol=0.0)
    assert diagnostics.wrong_target_information_after <= ATOL
    assert diagnostics.support_unitarity_residual <= ATOL
    assert diagnostics.ambient_unitarity_residual <= ATOL
    assert diagnostics.inverse_recovery_residual <= ATOL
    assert diagnostics.physical_automorphism_residual <= ATOL
    assert diagnostics.physical_constraint_residual <= ATOL
    assert diagnostics.positive_target_specific_record_witness is True
    assert diagnostics.directional_score_defined is False


def test_stage7b_summary_preserves_non_directional_interpretation_guards():
    summary = stage7b_summary()
    record = summary["record"]
    assert record["positive_target_specific_record_witness"] is True
    assert record["directional_score_defined"] is False
    assert "target-specific correlation != record-defined temporal orientation" in summary["guards"]
    assert "support-local reversible write != time-localized dynamical interaction" in summary["guards"]
