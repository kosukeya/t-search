"""Run Stage 1B B4 reachability-only reconstruction."""

from t_search.stage1 import canonical_block, compare_blocks, make_block, transitive_closure
from t_search.stage1_reachability import (
    check_reachability_consistency,
    project_all_reachability_views,
    reconstruct_cover_from_reachability,
)


def main() -> None:
    canonical = canonical_block()
    canonical_views = project_all_reachability_views(canonical)
    canonical_consistency = check_reachability_consistency(canonical_views)
    canonical_reconstructed = reconstruct_cover_from_reachability(canonical_views)
    canonical_comparison = compare_blocks(canonical, canonical_reconstructed)

    redundant = make_block(
        canonical.events,
        set(canonical.direct_edges) | {("a", "d")},
    )
    redundant_views = project_all_reachability_views(redundant)
    redundant_reconstructed = reconstruct_cover_from_reachability(redundant_views)
    redundant_comparison = compare_blocks(redundant, redundant_reconstructed)

    print("Stage 1B B4 — reachability-only")
    print(f"events: {len(canonical.events)}")
    print(f"canonical direct edges: {len(canonical.direct_edges)}")
    print(f"reachability pairs: {len(transitive_closure(canonical))}")
    print(f"reachability views consistent: {canonical_consistency.consistent}")
    print(f"reconstructed cover edges: {len(canonical_reconstructed.direct_edges)}")
    print(f"canonical labeled equality: {canonical_comparison.labeled_equal}")
    print(f"canonical unlabeled isomorphism: {canonical_comparison.unlabeled_isomorphic}")
    print(f"canonical reachability equality: {canonical_comparison.reachability_equal}")
    print()
    print("Redundant shortcut control: add a -> d")
    print(f"redundant direct edges: {len(redundant.direct_edges)}")
    print(f"same reachability views as canonical: {redundant_views == canonical_views}")
    print(f"shortcut retained after reduction: {('a', 'd') in redundant_reconstructed.direct_edges}")
    print(f"redundant labeled equality: {redundant_comparison.labeled_equal}")
    print(f"redundant unlabeled isomorphism: {redundant_comparison.unlabeled_isomorphic}")
    print(f"redundant reachability equality: {redundant_comparison.reachability_equal}")


if __name__ == "__main__":
    main()
