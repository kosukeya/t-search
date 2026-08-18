"""Run the Stage 2F robustness and boundary controls."""

from t_search.stage2 import (
    branching_structures_equivalent,
    canonical_stage2_substrate,
    extension_equivalence_classes,
)
from t_search.stage2_controls import (
    operational_next_state_values,
    rename_epistemic_model,
    rename_ontic_model,
    rename_operational_view,
    rename_prefix,
    state_collision_groups,
)
from t_search.stage2_epistemic import (
    canonical_epistemic_model,
    make_epistemic_history_model,
    project_epistemic_view,
)
from t_search.stage2_ontic import (
    canonical_ontic_model,
    make_ontic_extension_model,
    project_ontic_view,
)
from t_search.stage2_operational import (
    compare_operational_views,
    operationalize_epistemic_view,
    operationalize_ontic_view,
)
from t_search.stage2_update import compare_common_observation


RENAMING = {
    "p": "q0",
    "n": "q1",
    "l1": "q2",
    "l2": "q3",
    "r1": "q4",
}


def main() -> None:
    substrate = canonical_stage2_substrate()
    epistemic = canonical_epistemic_model()
    ontic = canonical_ontic_model()
    prefix = ("p", "n")

    original_e = operationalize_epistemic_view(
        project_epistemic_view(epistemic, prefix)
    )
    original_o = operationalize_ontic_view(project_ontic_view(ontic))

    renamed_e_model = rename_epistemic_model(epistemic, RENAMING)
    renamed_o_model = rename_ontic_model(ontic, RENAMING)
    renamed_prefix = rename_prefix(prefix, RENAMING)
    renamed_e = operationalize_epistemic_view(
        project_epistemic_view(renamed_e_model, renamed_prefix)
    )
    renamed_o = operationalize_ontic_view(project_ontic_view(renamed_o_model))

    print("=== renaming control ===")
    print(
        "branching isomorphic:",
        branching_structures_equivalent(substrate, renamed_e_model.substrate),
    )
    print(
        "epistemic operational covariance:",
        rename_operational_view(original_e, RENAMING) == renamed_e,
    )
    print(
        "ontic operational covariance:",
        rename_operational_view(original_o, RENAMING) == renamed_o,
    )

    original_update = compare_common_observation(epistemic, prefix, ontic, "l1")
    renamed_update = compare_common_observation(
        renamed_e_model,
        renamed_prefix,
        renamed_o_model,
        RENAMING["l1"],
    )
    print(
        "update covariance:",
        rename_operational_view(original_update.epistemic_after, RENAMING)
        == renamed_update.epistemic_after
        and rename_operational_view(original_update.ontic_after, RENAMING)
        == renamed_update.ontic_after,
    )

    state_labels = {
        "p": "P",
        "n": "N",
        "l1": "X",
        "l2": "X",
        "r1": "X",
    }
    classes = extension_equivalence_classes(
        substrate,
        prefix,
        state_labels=state_labels,
    )
    print("\n=== repeated-state control ===")
    print(
        "collisions:",
        {
            state: sorted(events)
            for state, events in state_collision_groups(substrate, state_labels).items()
        },
    )
    print("next event count:", len(original_o.next_events))
    print(
        "next state-value count:",
        len(operational_next_state_values(original_o, state_labels)),
    )
    print("continuation equivalence classes:", len(classes))

    h_left = ("p", "n", "l1", "l2")
    h_right = ("p", "n", "r1")
    matched_e = make_epistemic_history_model(
        substrate,
        h_left,
        {h_left: 0.75, h_right: 0.25},
    )
    matched_o = make_ontic_extension_model(
        substrate,
        prefix,
        {h_left: 0.75, h_right: 0.25},
    )
    matched_comparison = compare_operational_views(
        operationalize_epistemic_view(project_epistemic_view(matched_e, prefix)),
        operationalize_ontic_view(project_ontic_view(matched_o)),
    )

    mismatched_o = make_ontic_extension_model(
        substrate,
        prefix,
        {h_left: 0.5, h_right: 0.5},
    )
    mismatch = compare_operational_views(
        operationalize_epistemic_view(project_epistemic_view(matched_e, prefix)),
        operationalize_ontic_view(project_ontic_view(mismatched_o)),
    )

    print("\n=== weight controls ===")
    print("matched nonuniform equality:", matched_comparison.equal)
    print(
        "mismatch components:",
        {
            "actuality": mismatch.actuality_equal,
            "next": mismatch.next_events_equal,
            "probabilities": mismatch.probabilities_equal,
        },
    )

    zero_e = make_epistemic_history_model(
        substrate,
        h_left,
        {h_left: 1.0, h_right: 0.0},
    )
    zero_o = make_ontic_extension_model(
        substrate,
        prefix,
        {h_left: 1.0, h_right: 0.0},
    )
    zero_e_op = operationalize_epistemic_view(project_epistemic_view(zero_e, prefix))
    zero_o_op = operationalize_ontic_view(project_ontic_view(zero_o))
    zero_comparison = compare_operational_views(zero_e_op, zero_o_op)

    print("\n=== zero-support boundary ===")
    print("epistemic Next:", zero_e_op.next_events)
    print("ontic Next:", zero_o_op.next_events)
    print("operational equality:", zero_comparison.equal)

    terminal = compare_common_observation(
        original_update.updated_epistemic_model,
        original_update.updated_epistemic_prefix,
        original_update.updated_ontic_model,
        "l2",
    )
    print("\n=== terminal control ===")
    print("terminal equality:", terminal.after_comparison.equal)
    print("terminal Next:", terminal.epistemic_after.next_events)


if __name__ == "__main__":
    main()
