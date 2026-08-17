from dataclasses import replace

import pytest

from t_search.stage1 import (
    canonical_block,
    compare_blocks,
    glue_incoming_views,
    project_all_incoming_views,
    views_by_id,
)


def test_incoming_only_views_match_protocol() -> None:
    views = views_by_id(project_all_incoming_views(canonical_block()))
    assert views["a"].predecessors == frozenset()
    assert views["b"].predecessors == frozenset({"a"})
    assert views["c"].predecessors == frozenset({"a"})
    assert views["d"].predecessors == frozenset({"b", "c"})
    assert views["e"].predecessors == frozenset({"d"})
    assert views["f"].predecessors == frozenset({"d"})


def test_stage1b_incoming_only_reconstructs_block() -> None:
    original = canonical_block()
    incoming_views = project_all_incoming_views(original)
    reconstructed = glue_incoming_views(incoming_views)
    comparison = compare_blocks(original, reconstructed)

    assert comparison.labeled_equal is True
    assert comparison.unlabeled_isomorphic is True
    assert comparison.reachability_equal is True


def test_incoming_only_gluing_rejects_unknown_reference() -> None:
    views = list(project_all_incoming_views(canonical_block()))
    d_index = next(i for i, view in enumerate(views) if view.event_id == "d")
    views[d_index] = replace(
        views[d_index], predecessors=frozenset({"b", "c", "ghost"})
    )

    with pytest.raises(ValueError, match="unknown events"):
        glue_incoming_views(views)


def test_incoming_only_gluing_requires_view_for_referenced_event() -> None:
    views = tuple(
        view for view in project_all_incoming_views(canonical_block()) if view.event_id != "a"
    )

    with pytest.raises(ValueError, match="unknown events"):
        glue_incoming_views(views)
