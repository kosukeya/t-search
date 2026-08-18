from dataclasses import replace

import pytest

from t_search.stage1 import (
    canonical_block,
    check_view_consistency,
    compare_blocks,
    glue_views,
    make_block,
    project_all_views,
    transitive_closure,
    views_by_id,
)


def test_canonical_block_matches_protocol() -> None:
    block = canonical_block()
    assert block.events == frozenset({"a", "b", "c", "d", "e", "f"})
    assert block.direct_edges == frozenset(
        {
            ("a", "b"),
            ("a", "c"),
            ("b", "d"),
            ("c", "d"),
            ("d", "e"),
            ("d", "f"),
        }
    )


def test_local_views_match_protocol() -> None:
    views = views_by_id(project_all_views(canonical_block()))
    assert views["a"].predecessors == frozenset()
    assert views["a"].successors == frozenset({"b", "c"})
    assert views["d"].predecessors == frozenset({"b", "c"})
    assert views["d"].successors == frozenset({"e", "f"})
    assert views["e"].predecessors == frozenset({"d"})
    assert views["e"].successors == frozenset()


def test_stage1a_round_trip_reconstructs_block() -> None:
    original = canonical_block()
    views = project_all_views(original)
    consistency = check_view_consistency(views)
    reconstructed = glue_views(views)
    comparison = compare_blocks(original, reconstructed)

    assert consistency.consistent is True
    assert comparison.labeled_equal is True
    assert comparison.unlabeled_isomorphic is True
    assert comparison.reachability_equal is True


def test_reachability_is_separate_from_direct_adjacency() -> None:
    block = canonical_block()
    closure = transitive_closure(block)

    assert len(block.direct_edges) == 6
    assert len(closure) == 13
    assert ("a", "d") not in block.direct_edges
    assert ("a", "d") in closure
    assert ("a", "f") in closure


def test_gluing_rejects_inconsistent_incoming_outgoing_reports() -> None:
    views = list(project_all_views(canonical_block()))
    index = next(i for i, view in enumerate(views) if view.event_id == "d")
    views[index] = replace(views[index], predecessors=frozenset({"c"}))

    consistency = check_view_consistency(views)
    assert consistency.consistent is False
    assert ("b", "d") in consistency.missing_from_incoming

    with pytest.raises(ValueError, match="inconsistent local views"):
        glue_views(views)


def test_make_block_rejects_cycles() -> None:
    with pytest.raises(ValueError, match="directed acyclic graph"):
        make_block({"a", "b"}, {("a", "b"), ("b", "a")})


def test_input_iteration_order_does_not_change_modeled_structure() -> None:
    block_1 = make_block(
        ["a", "b", "c", "d", "e", "f"],
        [("a", "b"), ("a", "c"), ("b", "d"), ("c", "d"), ("d", "e"), ("d", "f")],
    )
    block_2 = make_block(
        ["f", "e", "d", "c", "b", "a"],
        [("d", "f"), ("d", "e"), ("c", "d"), ("b", "d"), ("a", "c"), ("a", "b")],
    )

    assert block_1 == block_2
    assert project_all_views(block_1) == project_all_views(block_2)
