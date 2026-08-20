"""Report the Stage 5A symmetric three-qutrit constrained baseline."""

from __future__ import annotations

import numpy as np

from t_search.stage5_clock_change import (
    analytic_physical_basis,
    canonical_stage5a_model,
    clock_state,
    clock_translation_unitary,
    constraint_compatible_triples,
    numerical_kernel_projector,
    physical_subspace_projector,
)


def main() -> None:
    model = canonical_stage5a_model(3)
    projector_residual = np.linalg.norm(
        numerical_kernel_projector(3) - physical_subspace_projector(3)
    )

    gram_residuals = []
    translation_residuals = []
    for subsystem in ("A", "B", "C"):
        basis = model.clock_bases[subsystem]
        gram_residuals.append(np.linalg.norm(basis.conj().T @ basis - np.eye(3)))
        translation = clock_translation_unitary(3)
        for j in range(3):
            translation_residuals.append(
                np.linalg.norm(translation @ clock_state(j, 3) - clock_state((j + 1) % 3, 3))
            )

    full_cycle_residual = np.linalg.norm(
        clock_translation_unitary(3, steps=3) - np.eye(3)
    )

    print("Stage 5A — symmetric three-subsystem constrained model")
    print(f"kinematic_dimension={model.kinematic_dimension}")
    print(f"physical_dimension={model.physical_dimension}")
    print(f"physical_basis_shape={analytic_physical_basis(3).shape}")
    print(f"allowed_triples={constraint_compatible_triples(3)}")
    print(f"analytic_vs_numerical_projector_residual={projector_residual:.3e}")
    print(f"max_clock_gram_residual={max(gram_residuals):.3e}")
    print(f"max_clock_translation_residual={max(translation_residuals):.3e}")
    print(f"full_cycle_residual={full_cycle_residual:.3e}")


if __name__ == "__main__":
    main()
