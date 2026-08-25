import numpy as np

from t_search.stage15_basis import (
    canonical_stage15d_candidates,
    stage15d_matrix_and_derivatives,
    stage15d_transformed_values_and_gradients,
)
from t_search.stage15_local import (
    STAGE15A_ATOL,
    STAGE15A_KAPPA,
    STAGE15A_SMEARING_PAIRS,
    canonical_stage15a_off_surface_probes,
    canonical_stage15a_representatives,
    stage15a_constraint_gradients,
    stage15a_constraints,
)


def _poisson(df, dg):
    return float(sum(
        df[q] * dg[p] - df[p] * dg[q]
        for q, p in ((0, 1), (2, 3), (4, 5), (6, 7))
    ))


def _coefficient_in_original_basis(candidate, point, i, j):
    A, dA = stage15d_matrix_and_derivatives(candidate, point)
    gradients = stage15a_constraint_gradients(point)
    coefficient = np.zeros(3, dtype=float)

    structure = -(STAGE15A_KAPPA**2) * point.T0
    coefficient[2] += (
        A[i, 0] * A[j, 1] * structure
        - A[i, 1] * A[j, 0] * structure
    )

    # All frozen Stage 15D candidate coefficients are clock-coordinate
    # functions (or constants), so coefficient-coefficient Poisson brackets
    # vanish.  The remaining product-rule terms are retained explicitly.
    for a in range(3):
        for b in range(3):
            coefficient[b] += A[i, a] * _poisson(gradients[a], dA[j, b])
            coefficient[a] += _poisson(dA[i, a], gradients[b]) * A[j, b]
    return coefficient


def test_stage15d_all_candidate_brackets_reconstruct_in_the_transformed_constraint_ideal():
    points = (
        tuple(rep.point() for rep in canonical_stage15a_representatives())
        + canonical_stage15a_off_surface_probes()
    )
    unsmeared_comparisons = 0
    smeared_comparisons = 0
    max_original_basis_residual = 0.0
    max_transformed_basis_residual = 0.0
    max_smeared_residual = 0.0

    for candidate in canonical_stage15d_candidates():
        for point in points:
            A, transformed_values, transformed_gradients = (
                stage15d_transformed_values_and_gradients(candidate, point)
            )
            inverse = np.linalg.inv(A)
            original_values = np.asarray(stage15a_constraints(point), dtype=float)
            pair_coefficients = {}

            for i in range(3):
                pair_coefficients[(i, i)] = np.zeros(3, dtype=float)
                for j in range(i + 1, 3):
                    coefficient = _coefficient_in_original_basis(
                        candidate, point, i, j
                    )
                    pair_coefficients[(i, j)] = coefficient
                    pair_coefficients[(j, i)] = -coefficient

                    direct = _poisson(
                        transformed_gradients[i], transformed_gradients[j]
                    )
                    reconstructed_original = float(coefficient @ original_values)
                    coefficient_transformed = coefficient @ inverse
                    reconstructed_transformed = float(
                        coefficient_transformed @ transformed_values
                    )
                    unsmeared_comparisons += 1
                    max_original_basis_residual = max(
                        max_original_basis_residual,
                        abs(direct - reconstructed_original),
                    )
                    max_transformed_basis_residual = max(
                        max_transformed_basis_residual,
                        abs(direct - reconstructed_transformed),
                    )

            for N, M in STAGE15A_SMEARING_PAIRS:
                n = np.asarray(N, dtype=float)
                m = np.asarray(M, dtype=float)
                coefficient = np.zeros(3, dtype=float)
                for i in range(3):
                    for j in range(3):
                        coefficient += n[i] * m[j] * pair_coefficients[(i, j)]

                direct = _poisson(
                    n @ transformed_gradients,
                    m @ transformed_gradients,
                )
                coefficient_transformed = coefficient @ inverse
                reconstructed = float(coefficient_transformed @ transformed_values)
                smeared_comparisons += 1
                max_smeared_residual = max(
                    max_smeared_residual, abs(direct - reconstructed)
                )

    assert unsmeared_comparisons == 9072
    assert smeared_comparisons == 18144
    assert max_original_basis_residual <= STAGE15A_ATOL
    assert max_transformed_basis_residual <= STAGE15A_ATOL
    assert max_smeared_residual <= STAGE15A_ATOL
