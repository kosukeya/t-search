from t_search.stage2 import canonical_stage2_substrate
from t_search.stage2_epistemic import (
    canonical_epistemic_model,
    make_epistemic_history_model,
    project_epistemic_view,
)
from t_search.stage2_ontic import canonical_ontic_model, project_ontic_view
from t_search.stage2_operational import (
    compare_operational_views,
    operationalize_epistemic_view,
    operationalize_ontic_view,
)


D0 = ("p", "n")
H_LEFT = ("p", "n", "l1", "l2")
H_RIGHT = ("p", "n", "r1")


def main() -> None:
    epistemic_model = canonical_epistemic_model()
    ontic_model = canonical_ontic_model()

    epistemic_modal = project_epistemic_view(epistemic_model, D0)
    ontic_modal = project_ontic_view(ontic_model)

    epistemic_operational = operationalize_epistemic_view(epistemic_modal)
    ontic_operational = operationalize_ontic_view(ontic_modal)
    baseline = compare_operational_views(
        epistemic_operational,
        ontic_operational,
    )

    right_hidden = canonical_epistemic_model(selected_history=H_RIGHT)
    right_hidden_operational = operationalize_epistemic_view(
        project_epistemic_view(right_hidden, D0)
    )

    substrate = canonical_stage2_substrate()
    mismatched_epistemic = make_epistemic_history_model(
        substrate,
        H_LEFT,
        {H_LEFT: 0.75, H_RIGHT: 0.25},
    )
    mismatch_operational = operationalize_epistemic_view(
        project_epistemic_view(mismatched_epistemic, D0)
    )
    mismatch = compare_operational_views(
        mismatch_operational,
        ontic_operational,
    )

    print("Stage 2D — operational equivalence")
    print("formal representational difference != empirical physical difference")
    print()
    print("typed modal view classes:")
    print("  epistemic:", type(epistemic_modal).__name__)
    print("  ontic:", type(ontic_modal).__name__)
    print("typed potentiality classes:")
    print("  epistemic:", type(epistemic_modal.potentiality).__name__)
    print("  ontic:", type(ontic_modal.potentiality).__name__)
    print()
    print("operational epistemic:", epistemic_operational)
    print("operational ontic:", ontic_operational)
    print("baseline operational equality:", baseline.equal)
    print("  actuality equal:", baseline.actuality_equal)
    print("  next events equal:", baseline.next_events_equal)
    print("  probabilities equal:", baseline.probabilities_equal)
    print()
    print(
        "hidden h* swap operationally invisible:",
        epistemic_operational == right_hidden_operational,
    )
    print()
    print("weight-mismatch control:")
    print("  actuality equal:", mismatch.actuality_equal)
    print("  next events equal:", mismatch.next_events_equal)
    print("  probabilities equal:", mismatch.probabilities_equal)
    print("  full operational equality:", mismatch.equal)


if __name__ == "__main__":
    main()
