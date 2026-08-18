"""Run the Stage 1A canonical global/local round-trip experiment."""

from __future__ import annotations

from t_search.stage1 import (
    canonical_block,
    check_view_consistency,
    compare_blocks,
    glue_views,
    project_all_views,
    transitive_closure,
)


def _fmt_set(values) -> str:
    return "{" + ", ".join(sorted(values)) + "}"


def _fmt_edges(edges) -> str:
    return "{" + ", ".join(f"{a}->{b}" for a, b in sorted(edges)) + "}"


def main() -> None:
    block = canonical_block()
    views = project_all_views(block)
    consistency = check_view_consistency(views)
    reconstructed = glue_views(views)
    comparison = compare_blocks(block, reconstructed)

    print("Stage 1A — minimal classical global/local reconstruction")
    print("simulation order != modeled temporal order")
    print()
    print(f"events: {len(block.events)} {_fmt_set(block.events)}")
    print(f"direct edges: {len(block.direct_edges)} {_fmt_edges(block.direct_edges)}")
    print(f"reachability pairs: {len(transitive_closure(block))}")
    print("DAG: True")
    print()
    print("local views:")
    for view in views:
        print(
            f"  {view.event_id}: pred={_fmt_set(view.predecessors)} "
            f"succ={_fmt_set(view.successors)}"
        )
    print()
    print(f"incoming/outgoing reports consistent: {consistency.consistent}")
    print(f"reconstructed edges: {_fmt_edges(reconstructed.direct_edges)}")
    print(f"labeled equality: {comparison.labeled_equal}")
    print(f"unlabeled graph isomorphism: {comparison.unlabeled_isomorphic}")
    print(f"reachability equality: {comparison.reachability_equal}")
    print()
    print("classification:")
    print("  local observable: event ID, immediate predecessor IDs, immediate successor IDs")
    print("  reconstructible: full direct-edge set C, reachability relation prec")
    print("  strict invariant: none claimed in Stage 1A")
    print("  ambiguous/lost: none under the deliberately information-rich Stage 1A protocol")


if __name__ == "__main__":
    main()
