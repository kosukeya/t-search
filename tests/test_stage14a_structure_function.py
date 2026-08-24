import numpy as np
import pytest

from t_search.stage14_structure_function import (
    STAGE14A_ATOL,
    STAGE14A_D,
    STAGE14A_H1,
    STAGE14A_H2,
    STAGE14A_RANK_DEFICIENT,
    STAGE14A_STRUCTURE_FUNCTION_REMOVED,
    canonical_stage14a_flow_probes,
    canonical_stage14a_off_surface_bracket_probes,
    canonical_stage14a_orbits,
    canonical_stage14a_representatives,
    stage14a_D,
    stage14a_H1,
    stage14a_H2,
    stage14a_apply_flow,
    stage14a_constraint_gradients,
    stage14a_diagnostics,
    stage14a_dirac_data,
    stage14a_generator_vectors,
    stage14a_jacobi_residual,
    stage14a_poisson_H1_D,
    stage14a_poisson_H1_H2,
    stage14a_poisson_H2_D,
    stage14a_rank_deficient_control_status,
    stage14a_structure_function_removed_control_status,
    stage14a_structure_functions,
)


def test_stage14a_constructs_frozen_108_representatives_on_surface():
    orbits = canonical_stage14a_orbits()
    reps = canonical_stage14a_representatives()
    assert len(orbits) == 4
    assert len(reps) == 108
    assert {rep.orbit_id for rep in reps} == {orbit.orbit_id for orbit in orbits}
    for orbit in orbits:
        assert sum(rep.orbit_id == orbit.orbit_id for rep in reps) == 27
    assert len({rep.representative_id for rep in reps}) == 108
    assert max(abs(rep.D_value) for rep in reps) <= STAGE14A_ATOL
    assert max(abs(rep.H1_value) for rep in reps) <= STAGE14A_ATOL
    assert max(abs(rep.H2_value) for rep in reps) <= STAGE14A_ATOL


def test_stage14a_constraint_and_generator_directions_have_rank_three():
    sigma_grad = []
    sigma_gen = []
    for rep in canonical_stage14a_representatives():
        gradients = stage14a_constraint_gradients(rep.point())
        generators = stage14a_generator_vectors(rep.point())
        assert np.linalg.matrix_rank(gradients, tol=STAGE14A_ATOL) == 3
        assert np.linalg.matrix_rank(generators, tol=STAGE14A_ATOL) == 3
        sigma_grad.append(np.linalg.svd(gradients, compute_uv=False)[-1])
        sigma_gen.append(np.linalg.svd(generators, compute_uv=False)[-1])
    assert min(sigma_grad) > STAGE14A_ATOL
    assert min(sigma_gen) > STAGE14A_ATOL


def test_stage14a_structure_functions_vary_negative_zero_positive():
    values = {
        value
        for rep in canonical_stage14a_representatives()
        for value in stage14a_structure_functions(rep.point())
    }
    assert values == {-0.5, 0.0, 0.5}
    assert any(value < 0 for value in values)
    assert 0.0 in values
    assert any(value > 0 for value in values)


def test_stage14a_first_class_brackets_and_jacobi_hold_off_surface_too():
    reps = canonical_stage14a_representatives()
    probes = canonical_stage14a_off_surface_bracket_probes()
    assert len(probes) == 108
    assert all(abs(stage14a_D(point)) > 0 for point in probes)

    for point in tuple(rep.point() for rep in reps) + probes:
        D = stage14a_D(point)
        assert stage14a_poisson_H1_D(point) == pytest.approx(0.0, abs=STAGE14A_ATOL)
        assert stage14a_poisson_H1_H2(point) == pytest.approx(
            -0.5 * point.X * D, abs=STAGE14A_ATOL
        )
        assert stage14a_poisson_H2_D(point) == pytest.approx(
            0.5 * point.T1 * D, abs=STAGE14A_ATOL
        )
        assert stage14a_jacobi_residual(point) == pytest.approx(
            0.0, abs=STAGE14A_ATOL
        )


def test_stage14a_single_generator_flows_preserve_surface_and_dirac_data():
    probes = canonical_stage14a_flow_probes()
    assert len(probes) == 648
    assert {item.generator_id for item in probes} == {
        STAGE14A_D,
        STAGE14A_H1,
        STAGE14A_H2,
    }
    assert max(item.target_constraint_residual for item in probes) <= STAGE14A_ATOL
    assert max(item.dirac_Q_residual for item in probes) <= STAGE14A_ATOL
    assert max(item.dirac_P_residual for item in probes) <= STAGE14A_ATOL

    source = canonical_stage14a_representatives()[0].point()
    for generator in (STAGE14A_D, STAGE14A_H1, STAGE14A_H2):
        target = stage14a_apply_flow(source, generator, 0.5)
        assert max(
            abs(stage14a_D(target)),
            abs(stage14a_H1(target)),
            abs(stage14a_H2(target)),
        ) <= STAGE14A_ATOL
        assert stage14a_dirac_data(target) == pytest.approx(
            stage14a_dirac_data(source), abs=STAGE14A_ATOL
        )


def test_stage14a_rejects_structure_function_removed_and_rank_deficient_controls():
    assert (
        stage14a_structure_function_removed_control_status()
        == STAGE14A_STRUCTURE_FUNCTION_REMOVED
    )
    assert stage14a_rank_deficient_control_status() == STAGE14A_RANK_DEFICIENT


def test_stage14a_diagnostics_close_only_frozen_criteria_11_through_17():
    diag = stage14a_diagnostics()
    assert diag.orbit_count == 4
    assert diag.representative_count == 108
    assert diag.representatives_per_orbit == 27
    assert diag.off_surface_probe_count == 108
    assert diag.single_generator_flow_probe_count == 648
    assert diag.structure_function_values == (-0.5, 0.0, 0.5)
    assert diag.minimum_constraint_gradient_rank == 3
    assert diag.minimum_generator_vector_rank == 3
    assert diag.minimum_constraint_gradient_sigma_min > STAGE14A_ATOL
    assert diag.minimum_generator_vector_sigma_min > STAGE14A_ATOL
    assert diag.max_constraint_residual <= STAGE14A_ATOL
    assert diag.max_bracket_closure_residual <= STAGE14A_ATOL
    assert diag.max_jacobi_residual <= STAGE14A_ATOL
    assert diag.max_flow_constraint_residual <= STAGE14A_ATOL
    assert diag.max_flow_dirac_residual <= STAGE14A_ATOL
    assert diag.representative_family_complete
    assert diag.independent_constraint_directions
    assert diag.structure_functions_nontrivial
    assert diag.first_class_structure_function_closure_established
    assert diag.jacobi_established
    assert diag.individual_flows_preserve_surface_and_dirac_data
    assert diag.structure_function_removed_control_rejected
    assert diag.rank_deficient_control_rejected
    assert diag.criteria_11_17_satisfied
