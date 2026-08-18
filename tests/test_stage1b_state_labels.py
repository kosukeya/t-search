from dataclasses import replace

import pytest

from t_search.stage1 import canonical_block, compare_blocks
from t_search.stage1_state_labels import (
    canonical_state_labeled_world,
    collapse_world_by_state,
    glue_state_labeled_views,
    make_state_labeled_world,
    project_all_state_labeled_views,
    state_collision_groups,
)


def test_collision_assignment_allows_distinct_events_with_same_state() -> None:
    world = canonical_state_labeled_world(canonical_block())
    states = world.states()
    assert states["b"] == "X"
    assert states["c"] == "X"
    assert "b" != "c"
    assert state_collision_groups(world.state_assignment) == {
        "X": frozenset({"b", "c"})
    }


def test_projected_views_preserve_colliding_ids_separately() -> None:
    views = {
        view.event_id: view
        for view in project_all_state_labeled_views(
            canonical_state_labeled_world(canonical_block())
        )
    }
    assert views["b"].state_value == views["c"].state_value == "X"
    assert views["b"].event_id != views["c"].event_id
    assert views["b"].predecessors == views["c"].predecessors == frozenset({"a"})
    assert views["b"].successors == views["c"].successors == frozenset({"d"})


def test_id_based_gluing_reconstructs_graph_and_state_map_exactly() -> None:
    original = canonical_state_labeled_world(canonical_block())
    reconstructed = glue_state_labeled_views(project_all_state_labeled_views(original))
    comparison = compare_blocks(original.block, reconstructed.world.block)

    assert comparison.labeled_equal is True
    assert comparison.unlabeled_isomorphic is True
    assert comparison.reachability_equal is True
    assert reconstructed.world.state_assignment == original.state_assignment
    assert reconstructed.collision_groups == {"X": frozenset({"b", "c"})}
    assert len(reconstructed.world.block.events) == 6


def test_naive_state_identity_collapse_loses_event_multiplicity_and_structure() -> None:
    original = canonical_state_labeled_world(canonical_block())
    collapsed = collapse_world_by_state(original)
    comparison = compare_blocks(original.block, collapsed)

    assert len(collapsed.events) == 5
    assert len(collapsed.direct_edges) == 4
    assert collapsed.events == frozenset({"A", "X", "D", "E", "F"})
    assert collapsed.direct_edges == frozenset(
        {("A", "X"), ("X", "D"), ("D", "E"), ("D", "F")}
    )
    assert comparison.labeled_equal is False
    assert comparison.unlabeled_isomorphic is False
    assert comparison.reachability_equal is False


def test_incomplete_state_assignment_is_rejected() -> None:
    with pytest.raises(ValueError, match="missing events"):
        make_state_labeled_world(
            canonical_block(),
            {"a": "A", "b": "X", "c": "X", "d": "D", "e": "E"},
        )


def test_unknown_state_owner_is_rejected() -> None:
    with pytest.raises(ValueError, match="unknown events"):
        make_state_labeled_world(
            canonical_block(),
            {
                "a": "A",
                "b": "X",
                "c": "X",
                "d": "D",
                "e": "E",
                "f": "F",
                "ghost": "G",
            },
        )


def test_duplicate_event_owned_views_are_rejected() -> None:
    views = list(
        project_all_state_labeled_views(
            canonical_state_labeled_world(canonical_block())
        )
    )
    views.append(views[0])
    with pytest.raises(ValueError, match="duplicate event IDs"):
        glue_state_labeled_views(views)


def test_structural_inconsistency_is_still_rejected_with_state_labels() -> None:
    views = list(
        project_all_state_labeled_views(
            canonical_state_labeled_world(canonical_block())
        )
    )
    index = next(i for i, view in enumerate(views) if view.event_id == "d")
    views[index] = replace(views[index], predecessors=frozenset({"c"}))
    with pytest.raises(ValueError, match="inconsistent state-labeled local views"):
        glue_state_labeled_views(views)
