"""Deterministic Stage 5D diagnostics for three-clock composition consistency."""

import numpy as np

from t_search.stage5_clock_change import analytic_physical_basis, physical_state_from_coefficients
from t_search.stage5_clock_transforms import apply_genuine_clock_change
from t_search.stage5_cross_clock_composition import (
    apply_cross_clock_route,
    closed_three_clock_loop_operator,
    closed_three_clock_loop_support_matrix,
    composed_cross_clock_operator,
    cross_clock_composition_support_matrices,
    direct_cross_clock_operator,
    ordered_distinct_clock_triples,
    source_support_projector,
)
from t_search.stage5_reductions import physical_clock_reduction


def main() -> None:
    coefficients = np.array(
        [1.0, 1.0j, -0.5, 2.0 - 1.0j, 0.25, -1.5j, 0.75 + 0.5j],
        dtype=np.complex128,
    )
    state = physical_state_from_coefficients(coefficients, 3, normalize=True)
    physical_basis = analytic_physical_basis(3)

    max_ambient_composition = 0.0
    max_support_composition = 0.0
    max_state_route = 0.0
    max_basis_route = 0.0
    max_intermediate_cancellation = 0.0
    max_loop_ambient = 0.0
    max_loop_support = 0.0
    case_count = 0

    for source, middle, target in ordered_distinct_clock_triples():
        projector = source_support_projector(source, 3)
        for j in range(3):
            source_state = physical_clock_reduction(state, source, j, 3)
            for ell in range(3):
                by_middle_reading = []
                for k in range(3):
                    case_count += 1
                    composed = composed_cross_clock_operator(
                        target, ell, middle, k, source, j, 3
                    )
                    direct = direct_cross_clock_operator(
                        target, ell, middle, source, j, 3
                    )
                    max_ambient_composition = max(
                        max_ambient_composition,
                        float(np.linalg.norm(composed - direct)),
                    )
                    by_middle_reading.append(composed)

                    support_composed, support_direct = cross_clock_composition_support_matrices(
                        target, ell, middle, k, source, j, 3
                    )
                    max_support_composition = max(
                        max_support_composition,
                        float(np.linalg.norm(support_composed - support_direct)),
                    )

                    routed = apply_cross_clock_route(
                        source_state, target, ell, middle, k, source, j, 3
                    )
                    expected = physical_clock_reduction(state, target, ell, 3)
                    max_state_route = max(
                        max_state_route,
                        float(np.linalg.norm(routed - expected)),
                    )

                    for basis_index in range(physical_basis.shape[1]):
                        basis_state = physical_basis[:, basis_index]
                        reduced_basis = physical_clock_reduction(basis_state, source, j, 3)
                        routed_basis = apply_cross_clock_route(
                            reduced_basis, target, ell, middle, k, source, j, 3
                        )
                        expected_basis = physical_clock_reduction(
                            basis_state, target, ell, 3
                        )
                        max_basis_route = max(
                            max_basis_route,
                            float(np.linalg.norm(routed_basis - expected_basis)),
                        )

                    loop = closed_three_clock_loop_operator(
                        source, j, middle, k, target, ell, 3
                    )
                    max_loop_ambient = max(
                        max_loop_ambient,
                        float(np.linalg.norm(loop - projector)),
                    )
                    loop_support = closed_three_clock_loop_support_matrix(
                        source, j, middle, k, target, ell, 3
                    )
                    max_loop_support = max(
                        max_loop_support,
                        float(np.linalg.norm(loop_support - np.eye(7))),
                    )

                for candidate in by_middle_reading[1:]:
                    max_intermediate_cancellation = max(
                        max_intermediate_cancellation,
                        float(np.linalg.norm(candidate - by_middle_reading[0])),
                    )

    decisive_source = physical_clock_reduction(state, "C", 0, 3)
    decisive_routed = apply_cross_clock_route(
        decisive_source, "B", 2, "A", 1, "C", 0, 3
    )
    decisive_direct = apply_genuine_clock_change(
        decisive_source, "B", 2, "C", 0, 3
    )

    print(f"canonical three-clock cases: {case_count}")
    print(f"max ambient composition residual: {max_ambient_composition:.3e}")
    print(f"max support composition residual: {max_support_composition:.3e}")
    print(f"max generic-state path residual: {max_state_route:.3e}")
    print(f"max physical-basis path residual: {max_basis_route:.3e}")
    print(f"max intermediate-reading cancellation residual: {max_intermediate_cancellation:.3e}")
    print(f"max closed-loop ambient residual: {max_loop_ambient:.3e}")
    print(f"max closed-loop support residual: {max_loop_support:.3e}")
    print(
        "decisive C->A->B vs C->B state residual: "
        f"{np.linalg.norm(decisive_routed - decisive_direct):.3e}"
    )


if __name__ == "__main__":
    main()
