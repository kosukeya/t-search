from dataclasses import replace

import pytest

from t_search.stage1 import canonical_block, compare_blocks, project_all_views
from t_search.stage1_missing_views import (
    enumerate_latent_edge_completions,
    reconstruct_missing_views,
)


def _without(*event_ids: str):
    removed = set(event_ids)
    return tuple(
        view for view in project_all_views(canonical_block()) if view.event_id not in removed
    )


def test_single_missing_view_strict_policy_keeps_only_view_owners() -> None:
    result = reconstruct_missing_views(_without("d"), policy="strict")

    assert result.block.events == frozenset({"a", "b", "c", "e", "f"})
    assert result.block.direct_edges == frozenset({("a", "b"), ("a", "c")})
    assert result.dangling_references == frozenset({"d"})
    assert result.latent_events == frozenset()


def test_single_missing_view_latent_policy_exactly_recovers_canonical_block() -> None:
    original = canonical_block()
    result = reconstruct_missing_views(_without("d"), policy="latent")
    comparison = compare_blocks(original, result.block)

    assert result.latent_events == frozenset({"d"})
    assert result.singly_reported_edges == frozenset(
        {("b", "d"), ("c", "d"), ("d", "e"), ("d", "f")}
    )
    assert result.doubly_reported_edges == frozenset({("a", "b"), ("a", "c")})
    assert comparison.labeled_equal is True
    assert comparison.unlabeled_isomorphic is True
    assert comparison.reachability_equal is True


def test_two_adjacent_missing_views_create_latent_edge_ambiguity() -> None:
    original = canonical_block()
    result = reconstruct_missing_views(_without("b", "d"), policy="latent")
    candidates = enumerate_latent_edge_completions(result)

    assert result.latent_events == frozenset({"b", "d"})
    assert result.block.events == original.events
    assert ("b", "d") not in result.block.direct_edges
    assert len(candidates) == 3
    assert original in candidates


def test_two_adjacent_missing_views_have_three_expected_completions() -> None:
    result = reconstruct_missing_views(_without("b", "d"), policy="latent")
    candidates = enumerate_latent_edge_completions(result)
    candidate_edges = {candidate.direct_edges for candidate in candidates}
    base_edges = result.block.direct_edges

    assert candidate_edges == {
        base_edges,
        base_edges | frozenset({("b", "d")}),
        base_edges | frozenset({("d", "b")}),
    }


def test_completely_unreferenced_missing_event_is_lost() -> None:
    result = reconstruct_missing_views(_without("d", "e"), policy="latent")

    assert "d" in result.latent_events
    assert "e" not in result.block.events
    assert result.block.events == frozenset({"a", "b", "c", "d", "f"})


def test_surviving_owner_owner_inconsistency_is_rejected() -> None:
    views = list(_without("d"))
    b_index = next(i for i, view in enumerate(views) if view.event_id == "b")
    views[b_index] = replace(views[b_index], predecessors=frozenset())

    with pytest.raises(ValueError, match="owner-owner reports are inconsistent"):
        reconstruct_missing_views(views, policy="latent")
