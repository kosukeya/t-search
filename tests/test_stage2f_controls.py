import pytest

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
    update_ontic_model,
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


def test_pure_event_renaming_preserves_branching_structure_up_to_isomorphism():
    original = canonical_stage2_substrate()
    renamed = rename_epistemic_model(canonical_epistemic_model(), RENAMING).substrate

    assert original.events != renamed.events
    assert branching_structures_equivalent(original, renamed)


def test_epistemic_operational_view_is_covariant_under_event_renaming():
    original_model = canonical_epistemic_model()
    renamed_model = rename_epistemic_model(original_model, RENAMING)

    original = operationalize_epistemic_view(
        project_epistemic_view(original_model, ("p", "n"))
    )
    renamed = operationalize_epistemic_view(
        project_epistemic_view(renamed_model, rename_prefix(("p", "n"), RENAMING))
    )

    assert rename_operational_view(original, RENAMING) == renamed


def test_ontic_operational_view_is_covariant_under_event_renaming():
    original_model = canonical_ontic_model()
    renamed_model = rename_ontic_model(original_model, RENAMING)

    original = operationalize_ontic_view(project_ontic_view(original_model))
    renamed = operationalize_ontic_view(project_ontic_view(renamed_model))

    assert rename_operational_view(original, RENAMING) == renamed


def test_common_update_is_covariant_under_event_renaming():
    original = compare_common_observation(
        canonical_epistemic_model(),
        ("p", "n"),
        canonical_ontic_model(),
        "l1",
    )

    renamed_epistemic = rename_epistemic_model(canonical_epistemic_model(), RENAMING)
    renamed_ontic = rename_ontic_model(canonical_ontic_model(), RENAMING)
    renamed = compare_common_observation(
        renamed_epistemic,
        rename_prefix(("p", "n"), RENAMING),
        renamed_ontic,
        RENAMING["l1"],
    )

    assert rename_operational_view(original.epistemic_after, RENAMING) == renamed.epistemic_after
    assert rename_operational_view(original.ontic_after, RENAMING) == renamed.ontic_after
    assert renamed.after_comparison.equal


def test_repeated_state_values_do_not_collapse_distinct_next_events():
    substrate = canonical_stage2_substrate()
    state_labels = {
        "p": "P",
        "n": "N",
        "l1": "X",
        "l2": "Y",
        "r1": "X",
    }
    operational = operationalize_ontic_view(project_ontic_view(canonical_ontic_model()))

    collisions = state_collision_groups(substrate, state_labels)
    assert collisions == {"X": frozenset({"l1", "r1"})}
    assert operational.next_events == ("l1", "r1")
    assert len(operational.next_events) == 2
    assert operational_next_state_values(operational, state_labels) == frozenset({"X"})


def test_repeated_state_values_still_leave_two_distinct_continuation_classes():
    substrate = canonical_stage2_substrate()
    state_labels = {
        "p": "P",
        "n": "N",
        "l1": "X",
        "l2": "X",
        "r1": "X",
    }

    classes = extension_equivalence_classes(
        substrate,
        ("p", "n"),
        state_labels=state_labels,
    )

    assert len(classes) == 2


def test_matched_nonuniform_positive_weights_remain_operationally_equal():
    substrate = canonical_stage2_substrate()
    h_left = ("p", "n", "l1", "l2")
    h_right = ("p", "n", "r1")

    epistemic = make_epistemic_history_model(
        substrate,
        h_left,
        {h_left: 0.75, h_right: 0.25},
    )
    ontic = make_ontic_extension_model(
        substrate,
        ("p", "n"),
        {h_left: 0.75, h_right: 0.25},
    )

    e_op = operationalize_epistemic_view(project_epistemic_view(epistemic, ("p", "n")))
    o_op = operationalize_ontic_view(project_ontic_view(ontic))

    assert compare_operational_views(e_op, o_op).equal
    assert e_op.next_probabilities == (("l1", 0.75), ("r1", 0.25))


def test_weight_mismatch_breaks_only_probability_component_when_support_matches():
    substrate = canonical_stage2_substrate()
    h_left = ("p", "n", "l1", "l2")
    h_right = ("p", "n", "r1")

    epistemic = make_epistemic_history_model(
        substrate,
        h_left,
        {h_left: 0.75, h_right: 0.25},
    )
    ontic = make_ontic_extension_model(
        substrate,
        ("p", "n"),
        {h_left: 0.5, h_right: 0.5},
    )

    comparison = compare_operational_views(
        operationalize_epistemic_view(project_epistemic_view(epistemic, ("p", "n"))),
        operationalize_ontic_view(project_ontic_view(ontic)),
    )

    assert not comparison.equal
    assert comparison.actuality_equal
    assert comparison.next_events_equal
    assert not comparison.probabilities_equal


def test_zero_weight_support_semantics_can_break_operational_equality():
    substrate = canonical_stage2_substrate()
    h_left = ("p", "n", "l1", "l2")
    h_right = ("p", "n", "r1")

    epistemic = make_epistemic_history_model(
        substrate,
        h_left,
        {h_left: 1.0, h_right: 0.0},
    )
    ontic = make_ontic_extension_model(
        substrate,
        ("p", "n"),
        {h_left: 1.0, h_right: 0.0},
    )

    e_op = operationalize_epistemic_view(project_epistemic_view(epistemic, ("p", "n")))
    o_op = operationalize_ontic_view(project_ontic_view(ontic))
    comparison = compare_operational_views(e_op, o_op)

    assert e_op.next_events == ("l1",)
    assert o_op.next_events == ("l1", "r1")
    assert not comparison.equal
    assert comparison.actuality_equal
    assert not comparison.next_events_equal


def test_terminal_operational_equality_and_no_further_update():
    first = compare_common_observation(
        canonical_epistemic_model(),
        ("p", "n"),
        canonical_ontic_model(),
        "l1",
    )
    second = compare_common_observation(
        first.updated_epistemic_model,
        first.updated_epistemic_prefix,
        first.updated_ontic_model,
        "l2",
    )

    assert second.after_comparison.equal
    assert second.epistemic_after.next_events == ()
    assert second.ontic_after.next_events == ()

    with pytest.raises(ValueError, match="not an admissible immediate successor"):
        update_ontic_model(second.updated_ontic_model, "r1")


def test_invalid_renaming_controls_are_rejected():
    with pytest.raises(ValueError, match="exactly every event"):
        rename_epistemic_model(
            canonical_epistemic_model(),
            {"p": "q0"},
        )

    noninjective = dict(RENAMING)
    noninjective["r1"] = noninjective["l1"]
    with pytest.raises(ValueError, match="injective"):
        rename_ontic_model(canonical_ontic_model(), noninjective)


def test_incomplete_state_labels_are_rejected():
    substrate = canonical_stage2_substrate()
    with pytest.raises(ValueError, match="exactly every event"):
        state_collision_groups(substrate, {"p": "P"})
