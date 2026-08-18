import pytest

from t_search.stage2 import (
    branching_structures_equivalent,
    canonical_stage2_substrate,
    extend_prefix,
    extension_equivalence_classes,
    extensions,
    histories_equivalent,
    is_valid_prefix,
    make_branching_structure,
    maximal_histories,
    next_events,
    prefix_tip,
)


def test_canonical_substrate_and_maximal_histories() -> None:
    substrate = canonical_stage2_substrate()

    assert substrate.events == frozenset({"p", "n", "l1", "l2", "r1"})
    assert substrate.direct_edges == frozenset(
        {("p", "n"), ("n", "l1"), ("l1", "l2"), ("n", "r1")}
    )
    assert substrate.root == "p"
    assert maximal_histories(substrate) == (
        ("p", "n", "l1", "l2"),
        ("p", "n", "r1"),
    )
    assert substrate.histories == maximal_histories(substrate)


def test_baseline_prefix_has_two_admissible_extensions_and_next_events() -> None:
    substrate = canonical_stage2_substrate()
    prefix = ("p", "n")

    assert is_valid_prefix(substrate, prefix) is True
    assert prefix_tip(prefix) == "n"
    assert extensions(substrate, prefix) == (
        ("p", "n", "l1", "l2"),
        ("p", "n", "r1"),
    )
    assert next_events(substrate, prefix) == frozenset({"l1", "r1"})


def test_canonical_extensions_are_not_merely_renamed_copies() -> None:
    substrate = canonical_stage2_substrate()
    left, right = extensions(substrate, ("p", "n"))

    assert histories_equivalent(left, right) is False
    classes = extension_equivalence_classes(substrate, ("p", "n"))
    assert len(classes) == 2
    assert {group[0] for group in classes} == {left, right}


def test_same_length_histories_are_equivalent_without_physical_labels() -> None:
    assert histories_equivalent(("a", "b", "c"), ("x", "y", "z")) is True


def test_rooted_branching_structure_is_invariant_under_event_renaming() -> None:
    original = canonical_stage2_substrate()
    rename = {"p": "q0", "n": "q1", "l1": "q2", "l2": "q3", "r1": "q4"}
    renamed = make_branching_structure(
        events={rename[event] for event in original.events},
        direct_edges={(rename[a], rename[b]) for a, b in original.direct_edges},
        root=rename[original.root],
    )

    assert branching_structures_equivalent(original, renamed) is True


def test_prefix_extension_and_terminal_behavior() -> None:
    substrate = canonical_stage2_substrate()

    left_prefix = extend_prefix(substrate, ("p", "n"), "l1")
    assert left_prefix == ("p", "n", "l1")
    assert extensions(substrate, left_prefix) == (("p", "n", "l1", "l2"),)
    assert next_events(substrate, left_prefix) == frozenset({"l2"})

    terminal = extend_prefix(substrate, left_prefix, "l2")
    assert terminal == ("p", "n", "l1", "l2")
    assert extensions(substrate, terminal) == (terminal,)
    assert next_events(substrate, terminal) == frozenset()


def test_invalid_prefix_and_invalid_extension_are_rejected() -> None:
    substrate = canonical_stage2_substrate()

    assert is_valid_prefix(substrate, ("p", "r1")) is False
    with pytest.raises(ValueError, match="not a valid prefix"):
        extensions(substrate, ("p", "r1"))
    with pytest.raises(ValueError, match="not an admissible immediate successor"):
        extend_prefix(substrate, ("p", "n"), "l2")


def test_branching_structure_rejects_non_tree_or_disconnected_inputs() -> None:
    with pytest.raises(ValueError, match="outward rooted tree"):
        make_branching_structure(
            events={"a", "b", "c"},
            direct_edges={("a", "b"), ("a", "c"), ("b", "c")},
            root="a",
        )

    with pytest.raises(ValueError, match="unreachable"):
        make_branching_structure(
            events={"a", "b", "c"},
            direct_edges={("a", "b")},
            root="a",
        )
