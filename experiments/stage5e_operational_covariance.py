"""Stage 5E operational-covariance diagnostic experiment."""

from itertools import permutations, product

import numpy as np

from t_search.stage5_clock_change import physical_state_from_coefficients, tensor_basis_state
from t_search.stage5_clock_transforms import genuine_clock_change_operator
from t_search.stage5_operational import (
    lift_reduced_observable_to_physical,
    perspective_entanglement_entropy,
    reduce_physical_observable_to_clock,
    reduced_born_probability,
    reduced_expectation_value,
    transform_reduced_observable,
)
from t_search.stage5_reductions import (
    clock_relative_support_basis,
    physical_clock_reduction,
)

CLOCKS = ("A", "B", "C")


def generic_physical_state() -> np.ndarray:
    coefficients = np.array(
        [
            1.0 + 0.2j,
            -0.4 + 0.7j,
            0.3 - 0.1j,
            0.8 + 0.5j,
            -0.2 - 0.6j,
            0.9 - 0.3j,
            0.1 + 0.4j,
        ],
        dtype=np.complex128,
    )
    return physical_state_from_coefficients(coefficients, normalize=True)


def support_observable(clock: str) -> np.ndarray:
    basis = clock_relative_support_basis(clock)
    coordinates = np.diag(np.linspace(-1.2, 1.4, 7)).astype(np.complex128)
    coordinates[0, 1] = 0.31 + 0.17j
    coordinates[1, 0] = np.conjugate(coordinates[0, 1])
    coordinates[2, 5] = -0.22 + 0.09j
    coordinates[5, 2] = np.conjugate(coordinates[2, 5])
    return basis @ coordinates @ basis.conj().T


def support_projector(clock: str) -> np.ndarray:
    basis = clock_relative_support_basis(clock)
    coefficients = np.array(
        [1.0, 0.4j, -0.3 + 0.2j, 0.5, -0.1j, 0.25, -0.45],
        dtype=np.complex128,
    )
    coefficients /= np.linalg.norm(coefficients)
    ket = basis @ coefficients
    return np.outer(ket, ket.conj())


def main() -> None:
    physical_state = generic_physical_state()
    max_expectation = 0.0
    max_born = 0.0
    max_physical_route = 0.0
    max_density = 0.0
    max_observable_composition = 0.0
    max_observable_roundtrip = 0.0

    for source, target in permutations(CLOCKS, 2):
        observable = support_observable(source)
        projector = support_projector(source)
        for j, k in product(range(3), repeat=2):
            source_state = physical_clock_reduction(physical_state, source, j)
            target_state = physical_clock_reduction(physical_state, target, k)
            transform = genuine_clock_change_operator(target, k, source, j)

            target_observable = transform_reduced_observable(
                observable, target, k, source, j
            )
            target_projector = transform_reduced_observable(
                projector, target, k, source, j
            )

            expectation_source = reduced_expectation_value(source_state, observable)
            expectation_target = reduced_expectation_value(target_state, target_observable)
            max_expectation = max(
                max_expectation, abs(expectation_source - expectation_target)
            )

            born_source = reduced_born_probability(source_state, projector)
            born_target = reduced_born_probability(target_state, target_projector)
            max_born = max(max_born, abs(born_source - born_target))

            physical_observable = lift_reduced_observable_to_physical(
                observable, source, j
            )
            via_physical = reduce_physical_observable_to_clock(
                physical_observable, target, k
            )
            max_physical_route = max(
                max_physical_route, np.linalg.norm(via_physical - target_observable)
            )

            source_density = np.outer(source_state, source_state.conj())
            target_density = np.outer(target_state, target_state.conj())
            max_density = max(
                max_density,
                np.linalg.norm(
                    transform @ source_density @ transform.conj().T - target_density
                ),
            )

            reverse = genuine_clock_change_operator(source, j, target, k)
            recovered = reverse @ target_observable @ reverse.conj().T
            max_observable_roundtrip = max(
                max_observable_roundtrip, np.linalg.norm(recovered - observable)
            )

    for source, middle, target in permutations(CLOCKS, 3):
        observable = support_observable(source)
        for j, k, ell in product(range(3), repeat=3):
            middle_observable = transform_reduced_observable(
                observable, middle, k, source, j
            )
            composed = transform_reduced_observable(
                middle_observable, target, ell, middle, k
            )
            direct = transform_reduced_observable(
                observable, target, ell, source, j
            )
            max_observable_composition = max(
                max_observable_composition, np.linalg.norm(composed - direct)
            )

    entanglement_state = (
        tensor_basis_state(+1, -1, 0) + tensor_basis_state(+1, 0, -1)
    ) / np.sqrt(2.0)
    entropies = {
        clock: [
            perspective_entanglement_entropy(entanglement_state, clock, j)
            for j in range(3)
        ]
        for clock in CLOCKS
    }

    print("Stage 5E operational covariance diagnostics")
    print(f"max expectation residual: {max_expectation:.3e}")
    print(f"max Born residual: {max_born:.3e}")
    print(f"max physical-lift/reduction route residual: {max_physical_route:.3e}")
    print(f"max density-matrix covariance residual: {max_density:.3e}")
    print(f"max observable-composition residual: {max_observable_composition:.3e}")
    print(f"max observable-roundtrip residual: {max_observable_roundtrip:.3e}")
    for clock in CLOCKS:
        values = ", ".join(f"{value:.12g}" for value in entropies[clock])
        print(f"entanglement entropy {clock} readings: [{values}] bits")


if __name__ == "__main__":
    main()
