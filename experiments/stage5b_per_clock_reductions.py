"""Deterministic Stage 5B diagnostics for the canonical three-qutrit model."""

import numpy as np

from t_search.stage5_clock_change import physical_state_from_coefficients
from t_search.stage5_reductions import (
    clock_reconstruction_operator,
    clock_relative_support_basis,
    clock_relative_support_projector,
    expected_same_clock_transition_operator,
    physical_clock_probability,
    physical_clock_reduction_operator,
    same_clock_transition_operator,
    same_clock_transition_support_matrix,
    support_coordinate_reduction_matrix,
)

CLOCKS = ("A", "B", "C")


def main() -> None:
    coefficients = np.array(
        [1.0, 1.0j, -0.5, 2.0 - 1.0j, 0.25, -1.5j, 0.75 + 0.5j],
        dtype=np.complex128,
    )
    state = physical_state_from_coefficients(coefficients, 3, normalize=True)

    max_isometry = 0.0
    max_support_roundtrip = 0.0
    max_physical_roundtrip = 0.0
    max_transition = 0.0
    max_composition = 0.0

    for clock in CLOCKS:
        support = clock_relative_support_basis(clock, 3)
        projector = clock_relative_support_projector(clock, 3)
        probabilities = [physical_clock_probability(state, clock, j, 3) for j in range(3)]
        print(f"{clock}: support shape={support.shape}, probabilities={probabilities}")

        for j in range(3):
            coordinates = support_coordinate_reduction_matrix(clock, j, 3)
            max_isometry = max(
                max_isometry,
                float(np.linalg.norm(coordinates.conj().T @ coordinates - np.eye(7))),
            )

            reduction = physical_clock_reduction_operator(clock, j, 3)
            reconstruction = clock_reconstruction_operator(clock, j, 3)
            max_support_roundtrip = max(
                max_support_roundtrip,
                float(np.linalg.norm(reduction @ reconstruction - projector)),
            )

            from t_search.stage5_clock_change import analytic_physical_basis

            physical_basis = analytic_physical_basis(3)
            max_physical_roundtrip = max(
                max_physical_roundtrip,
                float(np.linalg.norm(reconstruction @ reduction @ physical_basis - physical_basis)),
            )

            for k in range(3):
                actual = same_clock_transition_operator(clock, k, j, 3)
                expected = expected_same_clock_transition_operator(clock, k, j, 3)
                max_transition = max(max_transition, float(np.linalg.norm(actual - expected)))

                first = same_clock_transition_support_matrix(clock, k, j, 3)
                for ell in range(3):
                    second = same_clock_transition_support_matrix(clock, ell, k, 3)
                    direct = same_clock_transition_support_matrix(clock, ell, j, 3)
                    max_composition = max(
                        max_composition,
                        float(np.linalg.norm(second @ first - direct)),
                    )

    print(f"max support-coordinate isometry residual: {max_isometry:.3e}")
    print(f"max R_X E_X - P_K residual: {max_support_roundtrip:.3e}")
    print(f"max E_X R_X physical residual: {max_physical_roundtrip:.3e}")
    print(f"max same-clock expected-transition residual: {max_transition:.3e}")
    print(f"max same-clock composition residual: {max_composition:.3e}")


if __name__ == "__main__":
    main()
