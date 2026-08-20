"""Stage 4D checkpoint experiment: physical reversibility vs kinematic loss."""

import numpy as np

from t_search.stage4_conditional import physical_reduction
from t_search.stage4_quantum import physical_state_from_coefficients, tensor_basis_state
from t_search.stage4_reduction import (
    kinematic_projection_matrix,
    kinematic_projection_nullity,
    kinematic_projection_rank,
    physical_reduction_matrix,
    physical_roundtrip_residual,
    reconstruct_physical_state,
    system_roundtrip_residual,
)


def main() -> None:
    d = 4
    raw = np.array(
        [1.0 + 0.5j, -0.4 + 0.8j, 0.25 - 0.3j, -0.7 - 0.2j],
        dtype=np.complex128,
    )
    state = physical_state_from_coefficients(raw / np.linalg.norm(raw), d)

    print("Stage 4D — reduction-map reversibility")
    print("kinematic shape:", kinematic_projection_matrix(0, d).shape)
    print("kinematic rank:", kinematic_projection_rank(0, d))
    print("kinematic nullity:", kinematic_projection_nullity(0, d))

    for j in range(d):
        reduction = physical_reduction_matrix(j, d)
        unitary_residual = np.max(
            np.abs(reduction.conj().T @ reduction - np.eye(d))
        )
        local = physical_reduction(state, j, d)
        print(
            f"j={j}: unitary_residual={unitary_residual:.3e}, "
            f"physical_roundtrip={physical_roundtrip_residual(state, j, d):.3e}, "
            f"system_roundtrip={system_roundtrip_residual(local, j, d):.3e}"
        )

    kernel = (
        tensor_basis_state(0, 2, d) - tensor_basis_state(1, 2, d)
    ) / np.sqrt(2.0)
    print(
        "explicit nonzero kinematic-kernel projection norm:",
        np.linalg.norm(kinematic_projection_matrix(0, d) @ kernel),
    )
    lifted = reconstruct_physical_state(physical_reduction(state, 0, d), 0, d)
    print("reconstructed state physical roundtrip residual:", np.linalg.norm(lifted - state))


if __name__ == "__main__":
    main()
