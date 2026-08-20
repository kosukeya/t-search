"""Deterministic Stage 5C diagnostics for genuine cross-clock maps."""

import itertools

import numpy as np

from t_search.stage5_clock_change import physical_state_from_coefficients
from t_search.stage5_clock_transforms import (
    apply_genuine_clock_change,
    genuine_clock_change_operator,
    genuine_clock_change_support_matrix,
)
from t_search.stage5_reductions import (
    clock_relative_support_projector,
    physical_clock_reduction,
)

CLOCKS = ("A", "B", "C")
ORDERED_DISTINCT_CLOCKS = tuple(itertools.permutations(CLOCKS, 2))


def main() -> None:
    coefficients = np.array(
        [1.0, 1.0j, -0.5, 2.0 - 1.0j, 0.25, -1.5j, 0.75 + 0.5j],
        dtype=np.complex128,
    )
    state = physical_state_from_coefficients(coefficients, 3, normalize=True)

    max_support_unitarity = 0.0
    max_source_partial_isometry = 0.0
    max_target_partial_isometry = 0.0
    max_direct_route = 0.0
    max_ambient_roundtrip = 0.0
    max_support_roundtrip = 0.0

    for source, target in ORDERED_DISTINCT_CLOCKS:
        p_source = clock_relative_support_projector(source, 3)
        p_target = clock_relative_support_projector(target, 3)

        for j in range(3):
            source_state = physical_clock_reduction(state, source, j, 3)
            for k in range(3):
                operator = genuine_clock_change_operator(target, k, source, j, 3)
                coordinates = genuine_clock_change_support_matrix(target, k, source, j, 3)
                reverse = genuine_clock_change_operator(source, j, target, k, 3)
                reverse_coordinates = genuine_clock_change_support_matrix(source, j, target, k, 3)

                max_support_unitarity = max(
                    max_support_unitarity,
                    float(np.linalg.norm(coordinates.conj().T @ coordinates - np.eye(7))),
                    float(np.linalg.norm(coordinates @ coordinates.conj().T - np.eye(7))),
                )
                max_source_partial_isometry = max(
                    max_source_partial_isometry,
                    float(np.linalg.norm(operator.conj().T @ operator - p_source)),
                )
                max_target_partial_isometry = max(
                    max_target_partial_isometry,
                    float(np.linalg.norm(operator @ operator.conj().T - p_target)),
                )

                via_change = apply_genuine_clock_change(source_state, target, k, source, j, 3)
                direct = physical_clock_reduction(state, target, k, 3)
                max_direct_route = max(
                    max_direct_route,
                    float(np.linalg.norm(via_change - direct)),
                )

                max_ambient_roundtrip = max(
                    max_ambient_roundtrip,
                    float(np.linalg.norm(reverse @ operator - p_source)),
                )
                max_support_roundtrip = max(
                    max_support_roundtrip,
                    float(np.linalg.norm(reverse_coordinates @ coordinates - np.eye(7))),
                )

    zero_change = genuine_clock_change_operator("A", 0, "C", 0, 3)
    print(f"ordered distinct clock pairs: {len(ORDERED_DISTINCT_CLOCKS)}")
    print("reading pairs per ordered clock pair: 9")
    print(f"max support-coordinate unitarity residual: {max_support_unitarity:.3e}")
    print(f"max S^dagger S - P_source residual: {max_source_partial_isometry:.3e}")
    print(f"max S S^dagger - P_target residual: {max_target_partial_isometry:.3e}")
    print(f"max direct-global route residual: {max_direct_route:.3e}")
    print(f"max ambient two-way round-trip residual: {max_ambient_roundtrip:.3e}")
    print(f"max support-coordinate round-trip residual: {max_support_roundtrip:.3e}")
    print(f"||S_A<-C(0,0)-I_9||: {np.linalg.norm(zero_change - np.eye(9)):.3e}")


if __name__ == "__main__":
    main()
