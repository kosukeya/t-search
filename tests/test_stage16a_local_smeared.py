from fractions import Fraction
from itertools import combinations

import numpy as np
import pytest

from t_search.stage16_local import (
    STAGE16A_ADJACENT_FORWARD_EDGES,
    STAGE16A_ATOL,
    STAGE16A_GENERATOR_SUPPORTS,
    STAGE16A_N_FULL_A,
    STAGE16A_N_PARALLEL,
    STAGE16A_SMEARING_PAIRS,
    canonical_stage16a_off_surface_probes,
    canonical_stage16a_orbits,
    canonical_stage16a_representatives,
    canonical_stage16a_smeared_probes,
    stage16a_closure_coefficients,
    stage16a_closure_coordinate_support,
    stage16a_constraint_gradients,
    stage16a_constraints,
    stage16a_diagnostics,
    stage16a_dirac_data,
    stage16a_expected_seed_pair,
    stage16a_frame_determinant,
    stage16a_generator_vectors,
    stage16a_jacobi_residual,
    stage16a_pair_canonical_support,
    stage16a_poisson_pair,
    stage16a_reconstruct_seeds_from_presented,
    stage16a_seed_constraints,
    stage16a_smeared_direct,
    stage16a_smeared_expected_seed,
    stage16a_smeared_reconstructed,
    stage16a_smeared_canonical_support_ok,
    stage16a_unsmeared_canonical_support_ok,
)

_NVAR = 10
_ZERO_MONOMIAL = (0,) * _NVAR


def _clean(poly):
    return {monomial: coefficient for monomial, coefficient in poly.items() if coefficient}


def _add(a, b):
    result = dict(a)
    for monomial, coefficient in b.items():
        result[monomial] = result.get(monomial, Fraction(0)) + coefficient
    return _clean(result)


def _scale(a, scalar):
    scalar = Fraction(scalar)
    return _clean({monomial: scalar * coefficient for monomial, coefficient in a.items()})


def _mul(a, b):
    result = {}
    for ma, ca in a.items():
        for mb, cb in b.items():
            monomial = tuple(x + y for x, y in zip(ma, mb, strict=True))
            result[monomial] = result.get(monomial, Fraction(0)) + ca * cb
    return _clean(result)


def _derivative(poly, index):
    result = {}
    for monomial, coefficient in poly.items():
        power = monomial[index]
        if not power:
            continue
        derived = list(monomial)
        derived[index] -= 1
        key = tuple(derived)
        result[key] = result.get(key, Fraction(0)) + coefficient * power
    return _clean(result)


def _poisson(a, b):
    result = {}
    for q_index, p_index in ((0, 1), (2, 3), (4, 5), (6, 7), (8, 9)):
        result = _add(
            result,
            _add(
                _mul(_derivative(a, q_index), _derivative(b, p_index)),
                _scale(_mul(_derivative(a, p_index), _derivative(b, q_index)), -1),
            ),
        )
    return _clean(result)


def _variable(index):
    monomial = [0] * _NVAR
    monomial[index] = 1
    return {tuple(monomial): Fraction(1)}


def _symbolic_carrier():
    variables = tuple(_variable(index) for index in range(_NVAR))
    P = variables[1]
    clocks = (variables[2], variables[4], variables[6], variables[8])
    momenta = (variables[3], variables[5], variables[7], variables[9])
    c = (Fraction(1), Fraction(1, 2), Fraction(-1, 4), Fraction(3, 4))
    kappa = Fraction(1, 2)
    seeds = tuple(_add(momenta[i], _scale(P, c[i])) for i in range(4))
    constraints = tuple(
        _add(seeds[i], _scale(_mul(clocks[i], seeds[(i + 1) % 4]), kappa))
        for i in range(4)
    )
    return clocks, seeds, constraints, kappa


def _symbolic_expected_pair(i, j):
    clocks, seeds, _, kappa = _symbolic_carrier()
    if j == (i + 1) % 4:
        return _scale(_mul(clocks[i], seeds[(i + 2) % 4]), -(kappa**2))
    if i == (j + 1) % 4:
        return _scale(_mul(clocks[j], seeds[(j + 2) % 4]), kappa**2)
    return {}


def _symbolic_smeared(smearing, constraints):
    result = {}
    for weight, constraint in zip(smearing, constraints, strict=True):
        result = _add(result, _scale(constraint, Fraction(str(weight))))
    return result


def _symbolic_smeared_expected(N, M):
    clocks, seeds, _, kappa = _symbolic_carrier()
    result = {}
    for i in range(4):
        n_i = Fraction(str(N[i]))
        n_j = Fraction(str(N[(i + 1) % 4]))
        m_i = Fraction(str(M[i]))
        m_j = Fraction(str(M[(i + 1) % 4]))
        wedge = n_i * m_j - n_j * m_i
        term = _scale(_mul(clocks[i], seeds[(i + 2) % 4]), -(kappa**2) * wedge)
        result = _add(result, term)
    return result


def test_stage16a_exact_symbolic_unsmeared_and_smeared_algebra():
    _, _, constraints, _ = _symbolic_carrier()
    for i in range(4):
        for j in range(4):
            assert _poisson(constraints[i], constraints[j]) == _symbolic_expected_pair(i, j)
    for N, M in STAGE16A_SMEARING_PAIRS:
        direct = _poisson(_symbolic_smeared(N, constraints), _symbolic_smeared(M, constraints))
        assert direct == _symbolic_smeared_expected(N, M)


def test_stage16a_constructs_frozen_324_representatives_and_invertible_cycle_frame():
    orbits = canonical_stage16a_orbits()
    reps = canonical_stage16a_representatives()
    assert len(orbits) == 4
    assert len(reps) == 324
    assert len({rep.representative_id for rep in reps}) == 324
    determinants = set()
    for orbit in orbits:
        orbit_reps = [rep for rep in reps if rep.orbit_id == orbit.orbit_id]
        assert len(orbit_reps) == 81
        for rep in orbit_reps:
            point = rep.point()
            assert max(abs(value) for value in stage16a_constraints(point)) <= STAGE16A_ATOL
            assert stage16a_dirac_data(point) == pytest.approx(
                (orbit.Q_D, orbit.P_D), abs=STAGE16A_ATOL
            )
            determinants.add(stage16a_frame_determinant(point))
            assert stage16a_reconstruct_seeds_from_presented(point) == pytest.approx(
                stage16a_seed_constraints(point), abs=STAGE16A_ATOL
            )
    assert determinants == {0.9375, 1.0, 1.0625}


def test_stage16a_constraint_and_generator_directions_have_rank_four():
    sigma_grad = []
    sigma_gen = []
    for rep in canonical_stage16a_representatives():
        gradients = stage16a_constraint_gradients(rep.point())
        generators = stage16a_generator_vectors(rep.point())
        assert np.linalg.matrix_rank(gradients, tol=STAGE16A_ATOL) == 4
        assert np.linalg.matrix_rank(generators, tol=STAGE16A_ATOL) == 4
        sigma_grad.append(np.linalg.svd(gradients, compute_uv=False)[-1])
        sigma_gen.append(np.linalg.svd(generators, compute_uv=False)[-1])
    assert min(sigma_grad) > STAGE16A_ATOL
    assert min(sigma_gen) > STAGE16A_ATOL


def test_stage16a_unsmeared_closure_is_exact_on_positive_and_off_surface_family():
    positive = tuple(rep.point() for rep in canonical_stage16a_representatives())
    off_surface = canonical_stage16a_off_surface_probes()
    assert len(off_surface) == 324
    nonzero_adjacent_forward = 0
    full_coordinate_support = 0
    for source_kind, points in (("positive", positive), ("off_surface", off_surface)):
        for point in points:
            for i in range(4):
                for j in range(4):
                    direct = stage16a_poisson_pair(point, i, j)
                    assert direct == pytest.approx(
                        stage16a_expected_seed_pair(point, i, j), abs=STAGE16A_ATOL
                    )
                    coefficients = stage16a_closure_coefficients(point, i, j)
                    reconstructed = sum(
                        coefficient * value
                        for coefficient, value in zip(
                            coefficients, stage16a_constraints(point), strict=True
                        )
                    )
                    assert direct == pytest.approx(reconstructed, abs=STAGE16A_ATOL)
                    assert stage16a_unsmeared_canonical_support_ok(i, j)
                    if (i, j) in STAGE16A_ADJACENT_FORWARD_EDGES:
                        if len(stage16a_closure_coordinate_support(point, i, j)) == 4:
                            full_coordinate_support += 1
                        if source_kind == "off_surface" and abs(direct) > STAGE16A_ATOL:
                            nonzero_adjacent_forward += 1
            for triple in combinations(range(4), 3):
                assert stage16a_jacobi_residual(point, *triple) == pytest.approx(
                    0.0, abs=STAGE16A_ATOL
                )
    assert nonzero_adjacent_forward == 864
    assert full_coordinate_support == 768


def test_stage16a_support_audit_separates_canonical_and_closure_coordinate_support():
    assert stage16a_pair_canonical_support(0, 1) == frozenset((0, 2))
    assert stage16a_pair_canonical_support(3, 0) == frozenset((3, 1))
    assert stage16a_pair_canonical_support(0, 2) == frozenset()
    point = next(
        rep.point()
        for rep in canonical_stage16a_representatives()
        if rep.T0 == rep.T1 == rep.T2 == rep.T3 == 1.0
    )
    assert stage16a_closure_coordinate_support(point, 0, 1) == frozenset((0, 1, 2, 3))
    assert stage16a_closure_coordinate_support(point, 0, 2) == frozenset()
    assert STAGE16A_GENERATOR_SUPPORTS == {
        0: frozenset((0, 1)),
        1: frozenset((1, 2)),
        2: frozenset((2, 3)),
        3: frozenset((3, 0)),
    }


def test_stage16a_kronecker_smearings_recover_all_unsmeared_pairs():
    point = canonical_stage16a_off_surface_probes()[0]
    basis = tuple(tuple(1.0 if i == j else 0.0 for i in range(4)) for j in range(4))
    for i in range(4):
        for j in range(4):
            assert stage16a_smeared_direct(point, basis[i], basis[j]) == pytest.approx(
                stage16a_poisson_pair(point, i, j), abs=STAGE16A_ATOL
            )


def test_stage16a_frozen_smeared_family_is_derived_antisymmetric_and_reconstructed():
    probes = canonical_stage16a_smeared_probes()
    assert len(STAGE16A_SMEARING_PAIRS) == 8
    assert len(probes) == 5184
    assert {probe.source_kind for probe in probes} == {"positive", "off_surface"}
    assert all(probe.canonical_support_ok for probe in probes)
    assert max(abs(probe.direct_value - probe.seed_expected_value) for probe in probes) <= STAGE16A_ATOL
    assert max(abs(probe.direct_value - probe.reconstructed_value) for probe in probes) <= STAGE16A_ATOL
    assert max(probe.antisymmetry_residual for probe in probes) <= STAGE16A_ATOL
    for point in canonical_stage16a_off_surface_probes()[:8]:
        for N, M in STAGE16A_SMEARING_PAIRS:
            assert stage16a_smeared_direct(point, N, M) == pytest.approx(
                stage16a_smeared_expected_seed(point, N, M), abs=STAGE16A_ATOL
            )
            assert stage16a_smeared_direct(point, N, M) == pytest.approx(
                stage16a_smeared_reconstructed(point, N, M), abs=STAGE16A_ATOL
            )
            assert stage16a_smeared_canonical_support_ok(N, M)
    parallel = [
        probe
        for probe in probes
        if probe.N == STAGE16A_N_FULL_A and probe.M == STAGE16A_N_PARALLEL
    ]
    assert len(parallel) == 648
    assert max(abs(probe.direct_value) for probe in parallel) <= STAGE16A_ATOL


def test_stage16a_diagnostics_close_only_frozen_criteria_11_through_17():
    diag = stage16a_diagnostics()
    assert diag.orbit_count == 4
    assert diag.representative_count == 324
    assert diag.representatives_per_orbit == 81
    assert diag.off_surface_probe_count == 324
    assert diag.smeared_pair_count == 8
    assert diag.smeared_probe_count == 5184
    assert diag.jacobi_probe_count == 2592
    assert diag.structure_function_values == (-0.25, 0.0, 0.25)
    assert diag.frame_determinant_values == (0.9375, 1.0, 1.0625)
    assert diag.minimum_abs_frame_determinant == pytest.approx(0.9375, abs=STAGE16A_ATOL)
    assert diag.minimum_constraint_gradient_rank == 4
    assert diag.minimum_generator_vector_rank == 4
    assert diag.minimum_constraint_gradient_sigma_min > STAGE16A_ATOL
    assert diag.minimum_generator_vector_sigma_min > STAGE16A_ATOL
    assert diag.max_constraint_residual <= STAGE16A_ATOL
    assert diag.max_seed_inverse_residual <= STAGE16A_ATOL
    assert diag.max_unsmeared_seed_formula_residual <= STAGE16A_ATOL
    assert diag.max_unsmeared_presented_reconstruction_residual <= STAGE16A_ATOL
    assert diag.max_jacobi_residual <= STAGE16A_ATOL
    assert diag.max_smeared_seed_formula_residual <= STAGE16A_ATOL
    assert diag.max_smeared_presented_reconstruction_residual <= STAGE16A_ATOL
    assert diag.max_smeared_antisymmetry_residual <= STAGE16A_ATOL
    assert diag.off_surface_nonzero_adjacent_forward_count == 864
    assert diag.cycle_spanning_closure_coordinate_count == 768
    assert diag.max_closure_coordinate_support_size == 4
    assert diag.representative_family_complete
    assert diag.declared_dirac_family_consistent
    assert diag.frame_invertible_on_positive_family
    assert diag.independent_constraint_directions
    assert diag.structure_functions_nontrivial
    assert diag.first_class_presented_closure_established
    assert diag.smeared_presented_closure_established
    assert diag.canonical_function_support_established
    assert diag.closure_coordinate_cycle_spanning_observed
    assert diag.criteria_11_17_satisfied
