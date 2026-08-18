"""Run the Stage 2C ontic-extension baseline and update controls."""

from dataclasses import fields

from t_search.stage2_ontic import (
    OnticExtensionModel,
    canonical_ontic_model,
    extension_distribution,
    ontic_next_probabilities,
    project_ontic_view,
    update_ontic_model,
)


def main() -> None:
    model = canonical_ontic_model()
    view = project_ontic_view(model)

    print("Stage 2C — ontic-extension model")
    print("formal representational difference != empirical physical difference")
    print()
    print(f"actuality: {model.actuality}")
    print(f"extensions: {model.potentiality.histories}")
    print(f"extension weights: {extension_distribution(model)}")
    print(f"next probabilities: {view.next_probabilities}")
    print(
        "model fields:",
        tuple(field.name for field in fields(OnticExtensionModel)),
    )
    print("selected future field present:", hasattr(model, "selected_history"))

    left = update_ontic_model(model, "l1")
    right = update_ontic_model(model, "r1")

    print()
    print("after observing l1:")
    print(f"  actuality: {left.actuality}")
    print(f"  extensions: {left.potentiality.histories}")
    print(f"  next probabilities: {ontic_next_probabilities(left)}")
    print("  selected future field present:", hasattr(left, "selected_history"))

    print()
    print("alternative admissible update r1 from the same unselected baseline:")
    print(f"  actuality: {right.actuality}")
    print(f"  extensions: {right.potentiality.histories}")
    print(f"  next probabilities: {ontic_next_probabilities(right)}")
    print("  selected future field present:", hasattr(right, "selected_history"))


if __name__ == "__main__":
    main()
