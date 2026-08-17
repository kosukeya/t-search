import networkx as nx
import pytest

from t_search.stage1 import Block, canonical_block
from t_search.stage1_anonymous import (
    AnonymousStarView,
    contains_isomorphic_candidate,
    enumerate_topological_dags,
    find_compatible_anonymous_dags,
    project_anonymous_star_family,
    project_refined_anonymous_family,
    reachability_pair_count,
)


@pytest.fixture(scope="module")
def canonical() -> Block:
    return canonical_block()


@pytest.fixture(scope="module")
def star_search(canonical: Block):
    return find_compatible_anonymous_dags(
        project_anonymous_star_family(canonical),
        mode="star",
    )


@pytest.fixture(scope="module")
def refined_search(canonical: Block):
    return find_compatible_anonymous_dags(
        project_refined_anonymous_family(canonical),
        mode="refined",
    )


def test_canonical_anonymous_star_multiset(canonical: Block) -> None:
    assert project_anonymous_star_family(canonical) == (
        AnonymousStarView(0, 2),
        AnonymousStarView(1, 0),
        AnonymousStarView(1, 0),
        AnonymousStarView(1, 1),
        AnonymousStarView(1, 1),
        AnonymousStarView(2, 2),
    )


def test_anonymous_families_are_invariant_under_event_renaming(canonical: Block) -> None:
    rename = {
        "a": "q5",
        "b": "q2",
        "c": "q9",
        "d": "q1",
        "e": "q8",
        "f": "q4",
    }
    renamed = Block(
        events=frozenset(rename[event] for event in canonical.events),
        direct_edges=frozenset(
            (rename[source], rename[target])
            for source, target in canonical.direct_edges
        ),
    )

    assert project_anonymous_star_family(renamed) == project_anonymous_star_family(canonical)
    assert project_refined_anonymous_family(renamed) == project_refined_anonymous_family(canonical)


def test_b6a_star_family_is_globally_ambiguous(canonical: Block, star_search) -> None:
    assert star_search.scanned_graphs == 32768
    assert star_search.topological_label_matches == 5
    assert star_search.n_compatible == 3
    assert star_search.unique_up_to_isomorphism is False
    assert contains_isomorphic_candidate(canonical, star_search.isomorphism_classes) is True


def test_b6a_candidates_include_nonisomorphic_global_orders(star_search) -> None:
    counts = sorted(reachability_pair_count(candidate) for candidate in star_search.isomorphism_classes)
    assert counts == [13, 13, 14]


def test_b6b_refined_family_is_unique_up_to_isomorphism(
    canonical: Block,
    refined_search,
) -> None:
    assert refined_search.scanned_graphs == 32768
    assert refined_search.topological_label_matches == 1
    assert refined_search.n_compatible == 1
    assert refined_search.unique_up_to_isomorphism is True
    assert contains_isomorphic_candidate(canonical, refined_search.isomorphism_classes) is True


def test_b6b_unique_candidate_is_canonical_graph(canonical: Block, refined_search) -> None:
    candidate = refined_search.isomorphism_classes[0]
    original = nx.DiGraph()
    original.add_nodes_from(canonical.events)
    original.add_edges_from(canonical.direct_edges)
    recovered = nx.DiGraph()
    recovered.add_nodes_from(candidate.events)
    recovered.add_edges_from(candidate.direct_edges)

    assert nx.is_isomorphic(original, recovered)
    assert reachability_pair_count(candidate) == 13


def test_exhaustive_enumeration_is_deliberately_capped() -> None:
    with pytest.raises(ValueError, match="capped at six events"):
        tuple(enumerate_topological_dags(7))
