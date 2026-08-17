"""Run Stage 1B B6 anonymous / global-ID-free reconstruction."""

from t_search.stage1 import canonical_block
from t_search.stage1_anonymous import (
    contains_isomorphic_candidate,
    find_compatible_anonymous_dags,
    project_anonymous_star_family,
    project_refined_anonymous_family,
    reachability_pair_count,
)


def _print_search(label, original, family, mode):
    result = find_compatible_anonymous_dags(family, mode=mode)
    print(f"[{label}]")
    print("anonymous family:", family)
    print("scanned graphs:", result.scanned_graphs)
    print("topological-label matches:", result.topological_label_matches)
    print("non-isomorphic compatible candidates:", result.n_compatible)
    print("canonical class present:", contains_isomorphic_candidate(original, result.isomorphism_classes))
    print("unique up to isomorphism:", result.unique_up_to_isomorphism)
    for index, candidate in enumerate(result.isomorphism_classes, start=1):
        print(
            f"candidate {index}:",
            sorted(candidate.direct_edges),
            "reachability_pairs=",
            reachability_pair_count(candidate),
        )
    print()
    return result


def main() -> None:
    original = canonical_block()

    star_result = _print_search(
        "B6a minimal anonymous star",
        original,
        project_anonymous_star_family(original),
        "star",
    )
    refined_result = _print_search(
        "B6b one-step anonymous refinement",
        original,
        project_refined_anonymous_family(original),
        "refined",
    )

    assert star_result.n_compatible == 3
    assert refined_result.n_compatible == 1


if __name__ == "__main__":
    main()
