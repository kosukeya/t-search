from dataclasses import fields

import pytest

from t_search.stage2 import canonical_stage2_substrate
from t_search.stage2_epistemic import (
    EpistemicPotentiality,
    canonical_epistemic_model,
    make_epistemic_history_model,
    project_epistemic_view,
)
from t_search.stage2_ontic import (
    OnticLocalView,
    OnticPotentiality,
    canonical_ontic_model,
    make_ontic_extension_model,
    project_ontic_view,
)
from t_search.stage2_operational import (
    OperationalView,
    compare_operational_views,
    operationalize_epistemic_view,
    operationalize_ontic_view,
)


D0 = ("p", "n")
H_LEFT = ("p", "n", "l1", "l2")
H_RIGHT = ("p", "n", "r1")


def _baseline_operational_views():
    epistemic = canonical_epistemic_model()
    ontic = canonical_ontic_model()
    epistemic_view = project_epistemic_view(epistemic, D0)
    ontic_view = project_ontic_view(ontic)
    return (
        epistemic_view,
        ontic_view,
        operationalize_epistemic_view(epistemic_view),
        operationalize_ontic_view(ontic_view),
    )


def test_typed_modal_views_remain_semantically_distinct_before_erasure():
    epistemic_view, ontic_view, _, _ = _baseline_operational_views()

    assert isinstance(epistemic_view.potentiality, EpistemicPotentiality)
    assert isinstance(ontic_view.potentiality, OnticPotentiality)
    assert type(epistemic_view.potentiality) is not type(ontic_view.potentiality)
    assert epistemic_view != ontic_view


def test_matched_baseline_operational_views_are_equal():
    _, _, epistemic_operational, ontic_operational = _baseline_operational_views()

    comparison = compare_operational_views(
        epistemic_operational,
        ontic_operational,
    )

    assert epistemic_operational == ontic_operational
    assert comparison.equal
    assert comparison.actuality_equal
    assert comparison.next_events_equal
    assert comparison.probabilities_equal


def test_baseline_operational_interface_has_expected_contents():
    _, _, operational, _ = _baseline_operational_views()

    assert operational.actuality == D0
    assert operational.next_events == ("l1", "r1")
    assert operational.next_probabilities == (("l1", 0.5), ("r1", 0.5))


def test_hidden_selected_history_swap_is_operationally_invisible():
    left_model = canonical_epistemic_model(selected_history=H_LEFT)
    right_model = canonical_epistemic_model(selected_history=H_RIGHT)

    left = operationalize_epistemic_view(project_epistemic_view(left_model, D0))
    right = operationalize_epistemic_view(project_epistemic_view(right_model, D0))

    assert left == right


def test_probability_mismatch_breaks_operational_equality_without_changing_structure():
    substrate = canonical_stage2_substrate()
    epistemic = make_epistemic_history_model(
        substrate,
        H_LEFT,
        {H_LEFT: 0.75, H_RIGHT: 0.25},
    )
    ontic = canonical_ontic_model()

    epistemic_operational = operationalize_epistemic_view(
        project_epistemic_view(epistemic, D0)
    )
    ontic_operational = operationalize_ontic_view(project_ontic_view(ontic))
    comparison = compare_operational_views(
        epistemic_operational,
        ontic_operational,
    )

    assert not comparison.equal
    assert comparison.actuality_equal
    assert comparison.next_events_equal
    assert not comparison.probabilities_equal


def test_ontic_weight_mismatch_also_breaks_only_probability_component():
    substrate = canonical_stage2_substrate()
    epistemic = canonical_epistemic_model()
    ontic = make_ontic_extension_model(
        substrate,
        D0,
        {H_LEFT: 0.25, H_RIGHT: 0.75},
    )

    epistemic_operational = operationalize_epistemic_view(
        project_epistemic_view(epistemic, D0)
    )
    ontic_operational = operationalize_ontic_view(project_ontic_view(ontic))
    comparison = compare_operational_views(
        epistemic_operational,
        ontic_operational,
    )

    assert not comparison.equal
    assert comparison.actuality_equal
    assert comparison.next_events_equal
    assert not comparison.probabilities_equal


def test_operational_view_contains_no_potentiality_or_selected_history_semantics():
    _, _, operational, _ = _baseline_operational_views()
    field_names = {field.name for field in fields(OperationalView)}

    assert field_names == {"actuality", "next_events", "next_probabilities"}
    assert not hasattr(operational, "potentiality")
    assert not hasattr(operational, "selected_history")


def test_operational_erasure_rejects_probability_keys_that_do_not_match_next_events():
    malformed = OnticLocalView(
        actuality=D0,
        potentiality=OnticPotentiality((H_LEFT, H_RIGHT)),
        next_probabilities=(("l1", 1.0),),
    )

    with pytest.raises(ValueError, match="keys must match"):
        operationalize_ontic_view(malformed)
