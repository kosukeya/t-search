import numpy as np
import pytest

from t_search.stage15_local import (
    STAGE15A_ATOL,
    STAGE15A_GENERATOR_SUPPORTS,
    STAGE15A_SMEARING_PAIRS,
    canonical_stage15a_off_surface_probes,
    canonical_stage15a_orbits,
    canonical_stage15a_representatives,
    canonical_stage15a_smeared_probes,
    stage15a_constraint_gradients,
    stage15a_constraints,
    stage15a_diagnostics,
    stage15a_dirac_data,
    stage15a_expected_pair,
    stage15a_generator_vectors,
    stage15a_jacobi_residual,
    stage15a_poisson_pair,
    stage15a_smeared_decomposition,
    stage15a_smeared_direct,
    stage15a_smeared_reconstructed,
    stage15a_smeared_support_ok,
    stage15a_structure_function,
    stage15a_unsmeared_support_ok,
)


def test_stage15a_constructs_frozen_108_representatives_on_surface():
    orbits = canonical_stage15a_orbits()
    reps = canonical_stage15a_representatives()
    assert len(orbits) == 4
    assert len(reps) == 108
    assert len({rep.representative_id for rep in reps}) == 108
    for orbit in orbits:
        orbit_reps = [rep for rep in reps if rep.orbit_id == orbit.orbit_id]
        assert len(orbit_reps) == 27
        for rep in orbit_reps:
            assert max(abs(value) for value in stage15a_constraints(rep.point())) <= STAGE15A_ATOL
            assert stage15a_dirac_data(rep.point()) == pytest.approx(
                (orbit.Q_D, orbit.P_D), abs=STAGE15A_ATOL
            )


def test_stage15a_constraint_and_generator_directions_have_rank_three():
    sigma_grad = []
    sigma_gen = []
    for rep in canonical_stage15a_representatives():
        gradients = stage15a_constraint_gradients(rep.point())
        generators = stage15a_generator_vectors(rep.point())
        assert np.linalg.matrix_rank(gradients, tol=STAGE15A_ATOL) == 3
        assert np.linalg.matrix_rank(generators, tol=STAGE15A_ATOL) == 3
        sigma_grad.append(np.linalg.svd(gradients, compute_uv=False)[-1])
        sigma_gen.append(np.linalg.svd(generators, compute_uv=False)[-1])
    assert min(sigma_grad) > STAGE15A_ATOL
    assert min(sigma_gen) > STAGE15A_ATOL


def test_stage15a_structure_function_samples_negative_zero_positive():
    values = {
        0.0 if abs(stage15a_structure_function(rep.point())) <= STAGE15A_ATOL
        else stage15a_structure_function(rep.point())
        for rep in canonical_stage15a_representatives()
    }
    assert values == {-0.25, 0.0, 0.25}


def test_stage15a_unsmeared_algebra_closes_on_and_off_surface():
    positive = tuple(rep.point() for rep in canonical_stage15a_representatives())
    off_surface = canonical_stage15a_off_surface_probes()
    assert len(off_surface) == 108

    nonzero_off_surface = 0
    for point in positive + off_surface:
        for i in range(3):
            for j in range(3):
                direct = stage15a_poisson_pair(point, i, j)
                expected = stage15a_expected_pair(point, i, j)
                assert direct == pytest.approx(expected, abs=STAGE15A_ATOL)
                assert stage15a_unsmeared_support_ok(point, i, j)
        assert stage15a_jacobi_residual(point) == pytest.approx(0.0, abs=STAGE15A_ATOL)

    for point in off_surface:
        if abs(stage15a_poisson_pair(point, 0, 1)) > STAGE15A_ATOL:
            nonzero_off_surface += 1
    assert nonzero_off_surface == 72


def test_stage15a_kronecker_smearings_recover_unsmeared_algebra():
    point = canonical_stage15a_off_surface_probes()[0]
    e0 = (1.0, 0.0, 0.0)
    e1 = (0.0, 1.0, 0.0)
    e2 = (0.0, 0.0, 1.0)

    assert stage15a_smeared_direct(point, e0, e1) == pytest.approx(
        stage15a_poisson_pair(point, 0, 1), abs=STAGE15A_ATOL
    )
    assert stage15a_smeared_direct(point, e1, e0) == pytest.approx(
        -stage15a_smeared_direct(point, e0, e1), abs=STAGE15A_ATOL
    )
    assert stage15a_smeared_direct(point, e0, e2) == pytest.approx(0.0, abs=STAGE15A_ATOL)
    assert stage15a_smeared_direct(point, e1, e2) == pytest.approx(0.0, abs=STAGE15A_ATOL)
    assert stage15a_smeared_decomposition(point, e0, e1) == pytest.approx(
        (0.0, 0.0, stage15a_structure_function(point)), abs=STAGE15A_ATOL
    )


def test_stage15a_smeared_family_is_derived_antisymmetric_and_local():
    probes = canonical_stage15a_smeared_probes()
    assert len(STAGE15A_SMEARING_PAIRS) == 6
    assert len(probes) == 1296
    assert {probe.source_kind for probe in probes} == {"positive", "off_surface"}
    assert all(probe.support_ok for probe in probes)
    assert max(abs(probe.direct_value - probe.reconstructed_value) for probe in probes) <= STAGE15A_ATOL
    assert max(probe.antisymmetry_residual for probe in probes) <= STAGE15A_ATOL

    point = canonical_stage15a_off_surface_probes()[1]
    for N, M in STAGE15A_SMEARING_PAIRS:
        assert stage15a_smeared_direct(point, N, M) == pytest.approx(
            stage15a_smeared_reconstructed(point, N, M), abs=STAGE15A_ATOL
        )
        assert stage15a_smeared_support_ok(point, N, M)

    assert STAGE15A_GENERATOR_SUPPORTS[0] == frozenset((0, 1))
    assert STAGE15A_GENERATOR_SUPPORTS[1] == frozenset((1, 2))
    assert STAGE15A_GENERATOR_SUPPORTS[2] == frozenset((2,))


def test_stage15a_diagnostics_close_only_frozen_criteria_11_through_17():
    diag = stage15a_diagnostics()
    assert diag.orbit_count == 4
    assert diag.representative_count == 108
    assert diag.representatives_per_orbit == 27
    assert diag.off_surface_probe_count == 108
    assert diag.smeared_probe_count == 1296
    assert diag.structure_function_values == (-0.25, 0.0, 0.25)
    assert diag.minimum_constraint_gradient_rank == 3
    assert diag.minimum_generator_vector_rank == 3
    assert diag.minimum_constraint_gradient_sigma_min > STAGE15A_ATOL
    assert diag.minimum_generator_vector_sigma_min > STAGE15A_ATOL
    assert diag.max_constraint_residual <= STAGE15A_ATOL
    assert diag.max_unsmeared_closure_residual <= STAGE15A_ATOL
    assert diag.max_jacobi_residual <= STAGE15A_ATOL
    assert diag.max_smeared_reconstruction_residual <= STAGE15A_ATOL
    assert diag.max_smeared_antisymmetry_residual <= STAGE15A_ATOL
    assert diag.representative_family_complete
    assert diag.declared_dirac_family_consistent
    assert diag.independent_constraint_directions
    assert diag.structure_functions_nontrivial
    assert diag.first_class_local_closure_established
    assert diag.smeared_local_consistency_established
    assert diag.support_locality_established
    assert diag.criteria_11_17_satisfied
