import pytest

from t_search.stage2_epistemic import (
    EpistemicPotentiality,
    canonical_epistemic_model,
    project_epistemic_view,
    selected_history,
)
from t_search.stage2_ontic import (
    OnticPotentiality,
    canonical_ontic_model,
    project_ontic_view,
    update_ontic_model,
)
from t_search.stage2_operational import (
    operationalize_epistemic_view,
    operationalize_ontic_view,
)
from t_search.stage2_update import (
    compare_common_observation,
    ontic_selected_future_fields,
)


def test_common_l1_update_is_operationally_equal_before_and_after():
    epistemic = canonical_epistemic_model()
    ontic = canonical_ontic_model()

    result = compare_common_observation(
        epistemic,
        ("p", "n"),
        ontic,
        "l1",
    )

    assert result.before_comparison.equal
    assert result.after_comparison.equal


def test_common_l1_update_has_expected_operational_after_view():
    result = compare_common_observation(
        canonical_epistemic_model(),
        ("p", "n"),
        canonical_ontic_model(),
        "l1",
    )

    expected_actuality = ("p", "n", "l1")
    expected_next = ("l2",)
    expected_probabilities = (("l2", 1.0),)

    assert result.epistemic_after.actuality == expected_actuality
    assert result.ontic_after.actuality == expected_actuality
    assert result.epistemic_after.next_events == expected_next
    assert result.ontic_after.next_events == expected_next
    assert result.epistemic_after.next_probabilities == expected_probabilities
    assert result.ontic_after.next_probabilities == expected_probabilities


def test_epistemic_selected_history_is_preserved_by_update():
    epistemic = canonical_epistemic_model()
    before = selected_history(epistemic)

    result = compare_common_observation(
        epistemic,
        ("p", "n"),
        canonical_ontic_model(),
        "l1",
    )

    assert result.epistemic_selected_history_before == before
    assert result.epistemic_selected_history_after == before
    assert result.epistemic_selected_history_preserved
    assert selected_history(result.updated_epistemic_model) == before


def test_ontic_model_still_has_no_selected_future_field_after_update():
    result = compare_common_observation(
        canonical_epistemic_model(),
        ("p", "n"),
        canonical_ontic_model(),
        "l1",
    )

    assert ontic_selected_future_fields(canonical_ontic_model()) == ()
    assert ontic_selected_future_fields(result.updated_ontic_model) == ()
    assert not hasattr(result.updated_ontic_model, "selected_history")


def test_typed_potentialities_remain_distinct_after_common_update():
    result = compare_common_observation(
        canonical_epistemic_model(),
        ("p", "n"),
        canonical_ontic_model(),
        "l1",
    )

    epistemic_view = project_epistemic_view(
        result.updated_epistemic_model,
        result.updated_epistemic_prefix,
    )
    ontic_view = project_ontic_view(result.updated_ontic_model)

    assert isinstance(epistemic_view.potentiality, EpistemicPotentiality)
    assert isinstance(ontic_view.potentiality, OnticPotentiality)
    assert type(epistemic_view.potentiality) is not type(ontic_view.potentiality)
    assert epistemic_view.potentiality.histories == ontic_view.potentiality.histories


def test_second_common_update_reaches_same_terminal_operational_view():
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
    assert second.epistemic_after.actuality == ("p", "n", "l1", "l2")
    assert second.ontic_after.actuality == ("p", "n", "l1", "l2")
    assert second.epistemic_after.next_events == ()
    assert second.ontic_after.next_events == ()
    assert second.epistemic_after.next_probabilities == ()
    assert second.ontic_after.next_probabilities == ()
    assert second.epistemic_selected_history_preserved
    assert ontic_selected_future_fields(second.updated_ontic_model) == ()


def test_mismatched_starting_actualities_are_rejected():
    ontic_after_left = update_ontic_model(canonical_ontic_model(), "l1")

    with pytest.raises(ValueError, match="same current Actuality"):
        compare_common_observation(
            canonical_epistemic_model(),
            ("p", "n"),
            ontic_after_left,
            "l2",
        )


def test_r1_is_not_a_common_actual_run_for_epistemic_h_left_fixture():
    epistemic = canonical_epistemic_model()  # h* = h_L
    ontic = canonical_ontic_model()

    # The ontic model alone accepts r1 from the unselected baseline.
    ontic_right = update_ontic_model(ontic, "r1")
    assert ontic_right.actuality == ("p", "n", "r1")

    # But the paired actual-run comparison rejects it because the epistemic
    # fixture already encodes h* = h_L and must not rewrite that hidden history.
    with pytest.raises(ValueError, match="contradicts the hidden selected history"):
        compare_common_observation(
            epistemic,
            ("p", "n"),
            ontic,
            "r1",
        )


def test_operationalization_after_update_still_erases_modal_semantics():
    result = compare_common_observation(
        canonical_epistemic_model(),
        ("p", "n"),
        canonical_ontic_model(),
        "l1",
    )

    epistemic_view = project_epistemic_view(
        result.updated_epistemic_model,
        result.updated_epistemic_prefix,
    )
    ontic_view = project_ontic_view(result.updated_ontic_model)

    assert operationalize_epistemic_view(epistemic_view) == result.epistemic_after
    assert operationalize_ontic_view(ontic_view) == result.ontic_after
