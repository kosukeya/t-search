from dataclasses import replace

import pytest

from t_search.stage1 import canonical_block, compare_blocks, make_block
from t_search.stage1_reachability import (
    ReachabilityLocalView,
    check_reachability_consistency,
    project_all_reachability_views,
    reconstruct_cover_from_reachability,
)


def test_reachability_views_match_canonical_order() -> None:
    views = {view.event_id: view for view in project_all_reachability_views(canonical_block())}

    assert views["a"].ancestors == frozenset()
    assert views["a"].descendants == frozenset({"b", "c", "d", "e", "f"})
    assert views["d"].ancestors == frozenset({"a", "b", "c"})
    assert views["d"].descendants == frozenset({"e", "f"})


def test_reachability_only_recovers_canonical_cover_relation() -> None:
    original = canonical_block()
    views = project_all_reachability_views(original)
    consistency = check_reachability_consistency(views)
    reconstructed = reconstruct_cover_from_reachability(views)
    comparison = compare_blocks(original, reconstructed)

    assert consistency.consistent is True
    assert comparison.labeled_equal is True
    assert comparison.unlabeled_isomorphic is True
    assert comparison.reachability_equal is True


def test_redundant_shortcut_is_not_identifiable_from_reachability() -> None:
    canonical = canonical_block()
    redundant = make_block(
        canonical.events,
        set(canonical.direct_edges) | {("a", "d")},
    )

    canonical_views = project_all_reachability_views(canonical)
    redundant_views = project_all_reachability_views(redundant)
    reconstructed = reconstruct_cover_from_reachability(redundant_views)
    comparison = compare_blocks(redundant, reconstructed)

    assert redundant_views == canonical_views
    assert ("a", "d") not in reconstructed.direct_edges
    assert comparison.labeled_equal is False
    assert comparison.unlabeled_isomorphic is False
    assert comparison.reachability_equal is True


def test_reachability_gluing_rejects_ancestor_descendant_mismatch() -> None:
    views = list(project_all_reachability_views(canonical_block()))
    index = next(i for i, view in enumerate(views) if view.event_id == "d")
    views[index] = replace(views[index], ancestors=frozenset({"b", "c"}))

    consistency = check_reachability_consistency(views)
    assert consistency.consistent is False
    assert ("a", "d") in consistency.missing_from_ancestors

    with pytest.raises(ValueError, match="inconsistent reachability views"):
        reconstruct_cover_from_reachability(views)


def test_reachability_gluing_rejects_non_transitive_relation() -> None:
    views = (
        ReachabilityLocalView("a", frozenset(), frozenset({"b"})),
        ReachabilityLocalView("b", frozenset({"a"}), frozenset({"c"})),
        ReachabilityLocalView("c", frozenset({"b"}), frozenset()),
    )

    consistency = check_reachability_consistency(views)
    assert consistency.acyclic is True
    assert consistency.transitive is False
    assert consistency.consistent is False

    with pytest.raises(ValueError, match="inconsistent reachability views"):
        reconstruct_cover_from_reachability(views)


def test_reachability_gluing_rejects_self_relation() -> None:
    views = (
        ReachabilityLocalView("a", frozenset({"a"}), frozenset({"a"})),
    )

    consistency = check_reachability_consistency(views)
    assert consistency.consistent is False
    assert consistency.self_references == frozenset({("a", "a")})

    with pytest.raises(ValueError, match="inconsistent reachability views"):
        reconstruct_cover_from_reachability(views)
