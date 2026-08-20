"""Compact Stage 4B report for the constrained global quantum state."""

import numpy as np

from t_search.stage4_quantum import (
    constraint_kernel_projector,
    constraint_residual,
    equal_amplitude_physical_state,
    matched_energy_basis,
    physical_state_from_coefficients,
    physical_subspace_dimension,
    physical_subspace_projector,
    stationarity_residual,
    tensor_basis_state,
    total_constraint_operator,
)


def main() -> None:
    dimension = 4
    equal_state = equal_amplitude_physical_state(dimension)
    coefficients = np.array([1.0, 1.0j, -2.0, 0.5 - 0.5j], dtype=np.complex128)
    coefficients /= np.linalg.norm(coefficients)
    generic_state = physical_state_from_coefficients(coefficients, dimension)
    nonphysical = tensor_basis_state(0, 1, dimension)

    projector_residual = np.max(
        np.abs(
            constraint_kernel_projector(dimension)
            - physical_subspace_projector(dimension)
        )
    )

    print("Stage 4B — constrained global physical state")
    print(f"kinematic dimension: {dimension * dimension}")
    print(f"physical dimension: {physical_subspace_dimension(dimension)}")
    print(f"H_tot shape: {total_constraint_operator(dimension).shape}")
    print(f"matched basis shape: {matched_energy_basis(dimension).shape}")
    print(f"kernel/projector residual: {projector_residual:.3e}")
    print(f"equal-state constraint residual: {constraint_residual(equal_state, dimension):.3e}")
    print(f"generic-state constraint residual: {constraint_residual(generic_state, dimension):.3e}")
    print(f"generic-state stationarity residual tau=0.37: {stationarity_residual(generic_state, 0.37, dimension):.3e}")
    print(f"off-diagonal control constraint residual: {constraint_residual(nonphysical, dimension):.3e}")
    print(f"off-diagonal control stationarity residual tau=0.37: {stationarity_residual(nonphysical, 0.37, dimension):.3e}")
    print("conditional dynamics claim: none at Stage 4B")


if __name__ == "__main__":
    main()
