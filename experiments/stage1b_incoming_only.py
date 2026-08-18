"""Run the Stage 1B incoming-only reconstruction experiment."""

from t_search.stage1 import (
    canonical_block,
    compare_blocks,
    glue_incoming_views,
    project_all_incoming_views,
    transitive_closure,
)


def main() -> None:
    original = canonical_block()
    views = project_all_incoming_views(original)
    reconstructed = glue_incoming_views(views)
    comparison = compare_blocks(original, reconstructed)

    print("Stage 1B incoming-only")
    print(f"events: {len(original.events)}")
    print(f"direct edges: {len(original.direct_edges)}")
    print(f"reachability pairs: {len(transitive_closure(original))}")
    print("local views:")
    for view in views:
        print(f"  {view.event_id}: predecessors={sorted(view.predecessors)}")
    print(f"labeled equality: {comparison.labeled_equal}")
    print(f"unlabeled isomorphism: {comparison.unlabeled_isomorphic}")
    print(f"reachability equality: {comparison.reachability_equal}")


if __name__ == "__main__":
    main()
