"""Run Stage 1B B5: state-label collision versus event identity."""

from t_search.stage1 import canonical_block, compare_blocks
from t_search.stage1_state_labels import (
    canonical_state_labeled_world,
    collapse_world_by_state,
    glue_state_labeled_views,
    project_all_state_labeled_views,
)


def main() -> None:
    original = canonical_state_labeled_world(canonical_block())
    views = project_all_state_labeled_views(original)
    reconstructed = glue_state_labeled_views(views)
    correct_comparison = compare_blocks(original.block, reconstructed.world.block)

    collapsed = collapse_world_by_state(original)
    collapsed_comparison = compare_blocks(original.block, collapsed)

    print("Stage 1B B5 — state-label collision")
    print(f"original events: {len(original.block.events)}")
    print(f"distinct state values: {len(set(original.states().values()))}")
    print(f"collision groups: {dict(reconstructed.collision_groups)}")
    print(f"reconstructed events: {len(reconstructed.world.block.events)}")
    print(f"reconstructed edges: {len(reconstructed.world.block.direct_edges)}")
    print(f"labeled equality: {correct_comparison.labeled_equal}")
    print(f"unlabeled isomorphism: {correct_comparison.unlabeled_isomorphic}")
    print(f"reachability equality: {correct_comparison.reachability_equal}")
    print(f"state-map equality: {reconstructed.world.state_assignment == original.state_assignment}")
    print(f"naive collapsed nodes: {len(collapsed.events)}")
    print(f"naive collapsed edges: {len(collapsed.direct_edges)}")
    print(f"naive graph isomorphic to original: {collapsed_comparison.unlabeled_isomorphic}")


if __name__ == "__main__":
    main()
