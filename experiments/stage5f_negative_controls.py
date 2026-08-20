"""Stage 5F negative-control diagnostic script."""

import numpy as np

from t_search.stage5_clock_change import physical_state_from_coefficients, tensor_basis_state
from t_search.stage5_clock_transforms import genuine_clock_change_operator
from t_search.stage5_negative_controls import (
    ambient_clock_change_rank,
    ambient_clock_change_unitarity_residuals,
    energy_basis_conditioning_rank,
    first_off_support_pair,
    same_numeric_reading_semantic_witness,
)
from t_search.stage5_operational import reduced_expectation_value, transform_reduced_observable
from t_search.stage5_reductions import (
    formal_clock_conditioning,
    physical_clock_reduction,
    rest_basis_state,
)


def main() -> None:
    print("Stage 5F negative controls")

    print("\nFull-rest-space overextension: C@0 -> A@0")
    print("ambient rank:", ambient_clock_change_rank("A", 0, "C", 0))
    print(
        "unitarity residuals vs I_9:",
        ambient_clock_change_unitarity_residuals("A", 0, "C", 0),
    )
    off_pair = first_off_support_pair("C")
    off_state = rest_basis_state(off_pair)
    transform = genuine_clock_change_operator("A", 0, "C", 0)
    print("first C-off-support pair:", off_pair)
    print("off-support output norm:", np.linalg.norm(transform @ off_state))

    print("\nWrong energy-basis conditioning ranks")
    for clock in ("A", "B", "C"):
        ranks = {m: energy_basis_conditioning_rank(clock, m) for m in (-1, 0, 1)}
        print(clock, ranks)

    print("\nNonphysical formal conditioning")
    bad = tensor_basis_state(1, 1, 1)
    for clock in ("A", "B", "C"):
        print(clock, np.linalg.norm(formal_clock_conditioning(bad, clock, 0)))

    print("\nNaive untransformed observable")
    coeffs = np.zeros(7, dtype=np.complex128)
    coeffs[0] = 2.0
    coeffs[5] = 1.0
    physical = physical_state_from_coefficients(coeffs, normalize=True)
    psi_c = physical_clock_reduction(physical, "C", 0)
    psi_a = physical_clock_reduction(physical, "A", 0)
    ket = rest_basis_state((-1, 0))
    observable_c = np.outer(ket, ket.conj())
    observable_a_correct = transform_reduced_observable(
        observable_c, "A", 0, "C", 0
    )
    print("source expectation:", reduced_expectation_value(psi_c, observable_c))
    print("naive target expectation:", reduced_expectation_value(psi_a, observable_c))
    print(
        "properly transformed target expectation:",
        reduced_expectation_value(psi_a, observable_a_correct),
    )

    print("\nEqual numeric reading semantic witness")
    print(same_numeric_reading_semantic_witness("C", "A", (-1, 0, 1)))
    print("||S_A<-C(0,0)-I_9||:", np.linalg.norm(transform - np.eye(9)))


if __name__ == "__main__":
    main()
