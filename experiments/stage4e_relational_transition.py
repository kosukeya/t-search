"""Deterministic Stage 4E relational-transition checkpoint."""

import numpy as np

from t_search.stage4_quantum import physical_state_from_coefficients
from t_search.stage4_transition import (
    origin_covariance_residual,
    physical_reduction_transition_residual,
    transition_composition_residual,
    transition_expected_residual,
    transition_identity_residual,
    transition_inverse_residual,
    transition_unitarity_residual,
)


def main() -> None:
    d = 4
    alpha = 0.37
    coeffs = np.array(
        [1 + 0.5j, 2 - 1.5j, 3 + 2.5j, 4 - 3.5j], dtype=np.complex128
    )
    coeffs /= np.linalg.norm(coeffs)
    state = physical_state_from_coefficients(coeffs, d)

    expected = [
        transition_expected_residual(j, k, d)
        for j in range(d)
        for k in range(d)
    ]
    identities = [transition_identity_residual(j, d) for j in range(d)]
    inverses = [
        transition_inverse_residual(j, k, d)
        for j in range(d)
        for k in range(d)
    ]
    compositions = [
        transition_composition_residual(j, k, ell, d)
        for j in range(d)
        for k in range(d)
        for ell in range(d)
    ]
    unitarities = [
        transition_unitarity_residual(j, k, d)
        for j in range(d)
        for k in range(d)
    ]
    state_propagation = [
        physical_reduction_transition_residual(state, j, k, d)
        for j in range(d)
        for k in range(d)
    ]
    origins = [
        origin_covariance_residual(j, k, alpha, d)
        for j in range(d)
        for k in range(d)
    ]

    print(f"dimension={d}")
    print(f"origin_shift={alpha}")
    print(f"max_expected_transition_residual={max(expected):.3e}")
    print(f"max_identity_residual={max(identities):.3e}")
    print(f"max_inverse_residual={max(inverses):.3e}")
    print(f"max_composition_residual={max(compositions):.3e}")
    print(f"max_unitarity_residual={max(unitarities):.3e}")
    print(f"max_state_propagation_residual={max(state_propagation):.3e}")
    print(f"max_origin_covariance_residual={max(origins):.3e}")


if __name__ == "__main__":
    main()
