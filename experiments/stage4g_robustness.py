"""Executable Stage 4G robustness summary."""

from __future__ import annotations

import numpy as np

from t_search.stage4_quantum import physical_state_from_coefficients
from t_search.stage4_robustness import (
    ClockLabeling,
    ray_change_deficit_profile,
    relabeled_composition_residual,
    summarize_physical_state_robustness,
)


def generic_coefficients(dimension: int) -> np.ndarray:
    values = np.array(
        [complex(n + 1.0, ((-1) ** n) * (n + 0.37)) for n in range(dimension)],
        dtype=np.complex128,
    )
    return values / np.linalg.norm(values)


def main() -> None:
    print("Stage 4G robustness summary")
    for dimension in (3, 4, 5, 6):
        state = physical_state_from_coefficients(
            generic_coefficients(dimension), dimension
        )
        summary = summarize_physical_state_robustness(state, dimension)
        print(
            f"d={dimension}: max_structural_residual="
            f"{summary.max_structural_residual:.3e}"
        )

    d = 4
    two_sector = np.array([1.0, 1.0, 0.0, 0.0], dtype=np.complex128) / np.sqrt(2.0)
    state = physical_state_from_coefficients(two_sector, d)
    print("two-sector ray-change deficits:", ray_change_deficit_profile(state, d))

    labeling = ClockLabeling(("gamma", "alpha", "delta", "beta"))
    print(
        "renamed composition residual:",
        relabeled_composition_residual(labeling, "gamma", "delta", "beta"),
    )


if __name__ == "__main__":
    main()
