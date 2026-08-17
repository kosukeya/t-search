"""Stage 1B outgoing-only experiment.

Run from the repository root after installing the package:

    python experiments/stage1b_outgoing_only.py
"""

from t_search.stage1 import (
    canonical_block,
    compare_blocks,
    glue_outgoing_views,
    project_all_outgoing_views,
    transitive_closure,
)


def main() -> None:
    original = canonical_block()
    views = project_all_outgoing_views(original)
    reconstructed = glue_outgoing_views(views)
    comparison = compare_blocks(original, reconstructed)

    print("Stage 1B — outgoing-only")
    print(f"events: {len(original.events)}")
    print(f"direct edges: {len(original.direct_edges)}")
    print(f"reachability pairs: {len(transitive_closure(original))}")
    print("local views:")
    for view in views:
        print(f"  {view.event_id}: successors={sorted(view.successors)}")
    print(f"labeled equality: {comparison.labeled_equal}")
    print(f"unlabeled graph isomorphism: {comparison.unlabeled_isomorphic}")
    print(f"reachability equality: {comparison.reachability_equal}")


if __name__ == "__main__":
    main()
