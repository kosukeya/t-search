"""Run the Stage 2B epistemic-history baseline experiment."""

from t_search.stage2_epistemic import (
    actual_next_from_hidden_history,
    belief_distribution,
    canonical_epistemic_model,
    condition_epistemic_model,
    project_epistemic_view,
    selected_history,
)

H_LEFT = ("p", "n", "l1", "l2")
H_RIGHT = ("p", "n", "r1")
D0 = ("p", "n")


def main() -> None:
    left_hidden = canonical_epistemic_model(selected_history=H_LEFT)
    right_hidden = canonical_epistemic_model(selected_history=H_RIGHT)

    left_view = project_epistemic_view(left_hidden, D0)
    right_view = project_epistemic_view(right_hidden, D0)

    print("Stage 2B — epistemic-history model")
    print("formal representational difference != empirical physical difference")
    print()
    print(f"current prefix: {D0}")
    print(f"hidden selected history (left fixture): {selected_history(left_hidden)}")
    print(f"beliefs: {belief_distribution(left_hidden)}")
    print(f"local potentiality: {left_view.potentiality.histories}")
    print(f"local next probabilities: {dict(left_view.next_probabilities)}")
    print(
        "hidden-h* swap preserves local view:",
        left_view == right_view,
    )
    print(
        "privileged actual next differs:",
        actual_next_from_hidden_history(left_hidden, D0),
        actual_next_from_hidden_history(right_hidden, D0),
    )

    updated, prefix = condition_epistemic_model(left_hidden, D0, "l1")
    updated_view = project_epistemic_view(updated, prefix)
    print()
    print(f"after observation l1, prefix: {prefix}")
    print(f"hidden selected history unchanged: {selected_history(updated)}")
    print(f"conditioned beliefs: {belief_distribution(updated)}")
    print(f"remaining epistemic potentiality: {updated_view.potentiality.histories}")
    print(f"next probabilities: {dict(updated_view.next_probabilities)}")


if __name__ == "__main__":
    main()
