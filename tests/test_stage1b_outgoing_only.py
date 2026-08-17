from dataclasses import replace

import pytest

from t_search.stage1 import (
    canonical_block,
    compare_blocks,
    glue_outgoing_views,
    project_all_outgoing_views,
    views_by_id,
)


def test_outgoing_only_views_match_protocol() -> None:
    views = views_by_id(project_all_outgoing_views(canonical_block()))
    assert views["a"].successors == frozenset({"b", "c"})
    assert views["b"].successors == frozenset({"d"})
    assert views["c"].successors == frozenset({"d"})
    assert views["d"].successors == frozenset({"e", "f"})
    assert views["e"].successors == frozenset()
    assert views["f"].successors == frozenset()


def test_stage1b_outgoing_only_reconstructs_block() -> None:
    original = canonical_block()
    outgoing_views = project_all_outgoing_views(original)
    reconstructed = glue_outgoing_views(outgoing_views)
    comparison = compare_blocks(original, reconstructed)

    assert comparison.labeled_equal is True
    assert comparison.unlabeled_isomorphic is True
    assert comparison.reachability_equal is True


def test_outgoing_only_gluing_rejects_unknown_reference() -> None:
    views = list(project_all_outgoing_views(canonical_block()))
    a_index = next(i for i, view in enumerate(views) if view.event_id == "a")
    views[a_index] = replace(views[a_index], successors=frozenset({"b", "c", "ghost"}))

    with pytest.raises(ValueError, match="unknown events"):
        glue_outgoing_views(views)


def test_outgoing_only_gluing_requires_view_for_referenced_event() -> None:
    views = tuple(
        view for view in project_all_outgoing_views(canonical_block()) if view.event_id != "f"
    )

    with pytest.raises(ValueError, match="unknown events"):
        glue_outgoing_views(views)
