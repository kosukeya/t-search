"""Run the Stage 4F operational and negative controls."""

from __future__ import annotations

import numpy as np

from t_search.stage4_conditional import physical_reduction
from t_search.stage4_controls import (
    born_consistency_residual,
    density_matrix_residual,
    energy_basis_projection_nullity,
    energy_basis_projection_rank,
    formal_conditional_schrodinger_residual,
    global_conditional_born_probability,
    local_born_probability,
    plus01_projector,
    ray_fidelity,
)
from t_search.stage4_quantum import (
    equal_amplitude_physical_state,
    tensor_basis_state,
)


def main() -> None:
    d = 4
    state = equal_amplitude_physical_state(d)
    projector = plus01_projector(d)

    global_profile = [
        global_conditional_born_probability(state, j, projector, d) for j in range(d)
    ]
    local_profile = [local_born_probability(state, j, projector, d) for j in range(d)]
    born_residuals = [born_consistency_residual(state, j, projector, d) for j in range(d)]

    bad = (
        tensor_basis_state(0, 0, d) + tensor_basis_state(0, 1, d)
    ) / np.sqrt(2.0)
    bad_schrodinger_residual = formal_conditional_schrodinger_residual(
        bad, 1, d, reference_index=0
    )

    trivial = tensor_basis_state(1, 1, d)
    psi_0 = physical_reduction(trivial, 0, d)
    psi_1 = physical_reduction(trivial, 1, d)

    print("global conditional profile:", global_profile)
    print("local conditional profile:", local_profile)
    print("Born consistency residuals:", born_residuals)
    print("constraint-violating formal Schrodinger residual:", bad_schrodinger_residual)
    print("single-energy vector distance:", float(np.linalg.norm(psi_1 - psi_0)))
    print("single-energy ray fidelity:", ray_fidelity(psi_0, psi_1, d))
    print("single-energy density residual:", density_matrix_residual(psi_0, psi_1, d))
    print("energy-basis rank:", energy_basis_projection_rank(0, d))
    print("energy-basis nullity:", energy_basis_projection_nullity(0, d))


if __name__ == "__main__":
    main()
