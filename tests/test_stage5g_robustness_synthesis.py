import itertools

import numpy as np
import pytest

from t_search.stage5_clock_change import (
    SUBSYSTEMS,
    analytic_physical_basis,
    clock_step,
    physical_subspace_projector,
    physical_state_from_coefficients,
    total_constraint_operator,
)
from t_search.stage5_clock_transforms import genuine_clock_change_operator
from t_search.stage5_reductions import (
    clock_relative_support_basis,
    physical_clock_reduction_operator,
)
from t_search.stage5_robustness import (
    deterministic_physical_coefficients,
    global_phase_density_residuals,
    global_subsystem_permutation_operator,
    rest_subsystem_permutation_operator,
    stage5_joint_robustness_summary,
    subsystem_permutations,
)

ATOL = 1e-10


def _assert_summary_clean(summary):
    assert summary.max_constraint_residual <= ATOL
    assert summary.max_clock_probability_residual <= ATOL
    assert summary.max_reduction_isometry_residual <= ATOL
    assert summary.max_physical_roundtrip_residual <= ATOL
    assert summary.max_same_clock_dynamics_residual <= ATOL
    assert summary.max_clock_change_unitarity_residual <= ATOL
    assert summary.max_direct_route_residual <= ATOL
    assert summary.max_composition_residual <= ATOL
    assert summary.max_born_covariance_residual <= ATOL


def test_canonical_joint_robustness_survives_three_coefficient_families():
    for family in ("generic", "alternating", "sparse"):
        summary = stage5_joint_robustness_summary(3, coefficient_family=family)
        assert summary.physical_dimension == 7
        assert summary.support_dimensions == (7, 7, 7)
        _assert_summary_clean(summary)


def test_symmetric_d5_has_nineteen_dimensional_physical_and_support_spaces():
    summary = stage5_joint_robustness_summary(5, coefficient_family="generic")
    assert summary.physical_dimension == 19
    assert summary.support_dimensions == (19, 19, 19)
    _assert_summary_clean(summary)


def test_symmetric_d5_sparse_family_preserves_cross_clock_structure():
    summary = stage5_joint_robustness_summary(5, coefficient_family="sparse")
    assert summary.physical_dimension == 19
    _assert_summary_clean(summary)


def test_asymmetric_rates_have_five_dimensional_physical_and_support_spaces():
    rates = (1.0, 1.0, 2.0)
    summary = stage5_joint_robustness_summary(3, rates=rates, coefficient_family="generic")
    assert summary.physical_dimension == 5
    assert summary.support_dimensions == (5, 5, 5)
    _assert_summary_clean(summary)


def test_asymmetric_clock_rate_changes_coordinate_step_without_breaking_joint_suite():
    rates = (1.0, 1.0, 2.0)
    assert np.isclose(clock_step(3, rate=rates[0]), 2.0 * np.pi / 3.0)
    assert np.isclose(clock_step(3, rate=rates[1]), 2.0 * np.pi / 3.0)
    assert np.isclose(clock_step(3, rate=rates[2]), np.pi / 3.0)
    summary = stage5_joint_robustness_summary(3, rates=rates, coefficient_family="alternating")
    _assert_summary_clean(summary)


def test_global_phase_leaves_reduced_density_and_clock_probabilities_unchanged():
    for dimension, rates in (
        (3, (1.0, 1.0, 1.0)),
        (5, (1.0, 1.0, 1.0)),
        (3, (1.0, 1.0, 2.0)),
    ):
        density_residual, probability_residual = global_phase_density_residuals(
            dimension, rates=rates, phase=0.731
        )
        assert density_residual <= ATOL
        assert probability_residual <= ATOL


def test_all_subsystem_permutation_operators_are_unitary_and_preserve_symmetric_constraint():
    h_total = total_constraint_operator(3)
    identity = np.eye(27, dtype=complex)
    for permutation in subsystem_permutations():
        operator = global_subsystem_permutation_operator(permutation, 3)
        assert np.linalg.norm(operator.conj().T @ operator - identity) <= ATOL
        assert np.linalg.norm(operator @ h_total @ operator.conj().T - h_total) <= ATOL


def test_all_subsystem_permutations_preserve_the_symmetric_physical_projector():
    projector = physical_subspace_projector(3)
    for permutation in subsystem_permutations():
        operator = global_subsystem_permutation_operator(permutation, 3)
        assert np.linalg.norm(operator @ projector @ operator.conj().T - projector) <= ATOL


def test_per_clock_reduction_is_covariant_under_every_subsystem_permutation():
    physical_basis = analytic_physical_basis(3)
    for permutation in subsystem_permutations():
        global_permutation = global_subsystem_permutation_operator(permutation, 3)
        for source_clock in SUBSYSTEMS:
            target_clock, rest_permutation = rest_subsystem_permutation_operator(
                source_clock, permutation, 3
            )
            for index in range(3):
                source_reduction = physical_clock_reduction_operator(source_clock, index, 3)
                target_reduction = physical_clock_reduction_operator(target_clock, index, 3)
                residual = (
                    target_reduction @ global_permutation @ physical_basis
                    - rest_permutation @ source_reduction @ physical_basis
                )
                assert np.linalg.norm(residual) <= ATOL


def test_genuine_clock_change_is_covariant_under_every_subsystem_permutation():
    for permutation in subsystem_permutations():
        mapping = dict(zip(SUBSYSTEMS, permutation))
        for source_clock, target_clock in itertools.permutations(SUBSYSTEMS, 2):
            mapped_source, source_rest_permutation = rest_subsystem_permutation_operator(
                source_clock, permutation, 3
            )
            mapped_target, target_rest_permutation = rest_subsystem_permutation_operator(
                target_clock, permutation, 3
            )
            assert mapped_source == mapping[source_clock]
            assert mapped_target == mapping[target_clock]
            source_support = clock_relative_support_basis(source_clock, 3)
            for source_index, target_index in itertools.product(range(3), repeat=2):
                original = genuine_clock_change_operator(
                    target_clock, target_index, source_clock, source_index, 3
                )
                permuted = genuine_clock_change_operator(
                    mapped_target, target_index, mapped_source, source_index, 3
                )
                left = permuted @ source_rest_permutation @ source_support
                right = target_rest_permutation @ original @ source_support
                assert np.linalg.norm(left - right) <= ATOL


def test_permutation_covariance_is_not_a_claim_for_unpermuted_asymmetric_rates():
    rates = (1.0, 1.0, 2.0)
    # Swapping A and C while holding the rate tuple fixed changes H_tot.  This is
    # a negative guard against treating symmetric bookkeeping covariance as an
    # unrestricted physical permutation symmetry.
    swap_ac = ("C", "B", "A")
    operator = global_subsystem_permutation_operator(swap_ac, 3)
    h_total = total_constraint_operator(3, rates=rates)
    residual = np.linalg.norm(operator @ h_total @ operator.conj().T - h_total)
    assert residual > 1e-6


def test_robustness_helpers_reject_invalid_coefficient_family_and_permutation():
    with pytest.raises(ValueError):
        deterministic_physical_coefficients(7, family="unknown")
    with pytest.raises(ValueError):
        global_subsystem_permutation_operator(("A", "A", "C"), 3)
    with pytest.raises(ValueError):
        rest_subsystem_permutation_operator("D", ("A", "B", "C"), 3)
