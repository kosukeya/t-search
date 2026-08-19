"""Compact Stage 3A report for the reversible record substrate."""

from t_search.stage3 import (
    all_microstates,
    canonical_forward_ensemble,
    canonical_reversed_ensemble,
    full_state_entropies,
    is_bijective,
    is_forward_dynamically_valid,
    is_reverse_dynamically_valid,
    u_rec,
    u_scr,
)


def main() -> None:
    forward = canonical_forward_ensemble()
    reversed_ensemble = canonical_reversed_ensemble()

    print("Stage 3A — reversible record substrate")
    print(f"microstates: {len(all_microstates())}")
    print(f"U_rec bijective: {is_bijective(u_rec)}")
    print(f"U_scr bijective: {is_bijective(u_scr)}")
    print(f"forward trajectories: {len(forward.trajectories)}")
    print(
        "forward dynamically valid:",
        all(is_forward_dynamically_valid(t) for t in forward.trajectories),
    )
    print(f"reversed trajectories: {len(reversed_ensemble.trajectories)}")
    print(
        "reverse dynamically valid:",
        all(is_reverse_dynamically_valid(t) for t in reversed_ensemble.trajectories),
    )
    print(f"full-state entropies forward: {full_state_entropies(forward)}")
    print(f"full-state entropies reversed: {full_state_entropies(reversed_ensemble)}")
    print("arrow claim: none at Stage 3A")


if __name__ == "__main__":
    main()
