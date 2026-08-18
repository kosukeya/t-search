from t_search.stage2 import (
    canonical_stage2_substrate,
    extension_equivalence_classes,
    extensions,
    histories_equivalent,
    next_events,
)


def main() -> None:
    substrate = canonical_stage2_substrate()
    prefix = ("p", "n")
    live = extensions(substrate, prefix)
    classes = extension_equivalence_classes(substrate, prefix)

    print("Stage 2A — common branching substrate")
    print("simulation order != modeled temporal order")
    print()
    print(f"events: {len(substrate.events)}")
    print(f"direct edges: {len(substrate.direct_edges)}")
    print(f"maximal histories: {len(substrate.histories)}")
    print(f"current prefix: {prefix}")
    print(f"tip: {prefix[-1]}")
    print(f"extensions: {live}")
    print(f"next events: {sorted(next_events(substrate, prefix))}")
    print(f"extension equivalence classes: {len(classes)}")
    print(
        "h_L equivalent to h_R by renaming: "
        f"{histories_equivalent(live[0], live[1])}"
    )


if __name__ == "__main__":
    main()
