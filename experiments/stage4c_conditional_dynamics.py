"""Compact Stage 4C report for ideal clock-relative conditional dynamics."""

import numpy as np

from t_search.stage4_conditional import (
    clock_probability_profile,
    conditional_schrodinger_residual,
    one_step_conditional_residuals,
    physical_reduction,
)
from t_search.stage4_quantum import (
    equal_amplitude_physical_state,
    physical_state_from_coefficients,
)


def main() -> None:
    dimension = 4
    canonical = equal_amplitude_physical_state(dimension)
    raw = np.array(
        [1.0 + 0.5j, -0.3 + 0.7j, 0.2 - 0.4j, 0.9 + 0.1j],
        dtype=np.complex128,
    )
    coefficients = raw / np.linalg.norm(raw)
    generic = physical_state_from_coefficients(coefficients, dimension)

    probabilities = clock_probability_profile(generic, dimension)
    reference_residuals = tuple(
        conditional_schrodinger_residual(generic, j, dimension)
        for j in range(dimension)
    )
    step_residuals = one_step_conditional_residuals(generic, dimension)

    print("Stage 4C — conditional dynamics")
    print(f"generic clock probabilities: {probabilities}")
    print(f"generic reference residuals: {reference_residuals}")
    print(f"generic one-step residuals: {tuple(step_residuals)}")
    print(
        "equal-amplitude |<psi_0|psi_1>|:",
        abs(
            np.vdot(
                physical_reduction(canonical, 0, dimension),
                physical_reduction(canonical, 1, dimension),
            )
        ),
    )
    print("interpretation: exact finite clock-relative dynamics only")


if __name__ == "__main__":
    main()
