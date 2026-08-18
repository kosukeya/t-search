"""Stage 2E experiment: compare both model updates under observation l1."""

from t_search.stage2_epistemic import (
    canonical_epistemic_model,
    project_epistemic_view,
)
from t_search.stage2_ontic import (
    canonical_ontic_model,
    project_ontic_view,
    update_ontic_model,
)
from t_search.stage2_update import (
    compare_common_observation,
    ontic_selected_future_fields,
)


def main() -> None:
    epistemic = canonical_epistemic_model()
    ontic = canonical_ontic_model()

    result = compare_common_observation(
        epistemic,
        ("p", "n"),
        ontic,
        "l1",
    )

    epistemic_modal_after = project_epistemic_view(
        result.updated_epistemic_model,
        result.updated_epistemic_prefix,
    )
    ontic_modal_after = project_ontic_view(result.updated_ontic_model)

    print("Stage 2E — update comparison")
    print("simulation order != modeled temporal order")
    print("observation:", result.observed_next)
    print("operational equality before:", result.before_comparison.equal)
    print("operational equality after:", result.after_comparison.equal)
    print("epistemic after:", result.epistemic_after)
    print("ontic after:", result.ontic_after)
    print(
        "epistemic selected history preserved:",
        result.epistemic_selected_history_preserved,
    )
    print(
        "epistemic selected history:",
        result.epistemic_selected_history_after,
    )
    print(
        "ontic selected-future-like fields after:",
        ontic_selected_future_fields(result.updated_ontic_model),
    )
    print(
        "typed Potentiality classes after:",
        type(epistemic_modal_after.potentiality).__name__,
        type(ontic_modal_after.potentiality).__name__,
    )
    print(
        "typed Potentiality carriers equal after:",
        epistemic_modal_after.potentiality.histories
        == ontic_modal_after.potentiality.histories,
    )

    # Formal update-domain contrast already exposed by Stage 2B/C.
    ontic_right = update_ontic_model(canonical_ontic_model(), "r1")
    print("ontic r1 update actuality:", ontic_right.actuality)
    try:
        compare_common_observation(
            canonical_epistemic_model(),
            ("p", "n"),
            canonical_ontic_model(),
            "r1",
        )
    except ValueError as error:
        print("paired r1 update with epistemic h*=h_L rejected:", str(error))


if __name__ == "__main__":
    main()
