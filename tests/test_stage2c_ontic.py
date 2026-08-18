from dataclasses import fields

import pytest

from t_search.stage2 import canonical_stage2_substrate
from t_search.stage2_epistemic import EpistemicPotentiality
from t_search.stage2_ontic import (
    OnticExtensionModel,
    OnticPotentiality,
    canonical_ontic_model,
    extension_distribution,
    make_ontic_extension_model,
    ontic_next_probabilities,
    project_ontic_view,
    update_ontic_model,
)


def test_baseline_model_contains_current_actuality_and_all_extensions() -> None:
    model = canonical_ontic_model()
    h_left = ("p", "n", "l1", "l2")
    h_right = ("p", "n", "r1")

    assert model.actuality == ("p", "n")
    assert model.potentiality == OnticPotentiality((h_left, h_right))
    assert extension_distribution(model) == {h_left: 0.5, h_right: 0.5}


def test_ontic_model_has_no_selected_future_field_or_epistemic_potentiality() -> None:
    model = canonical_ontic_model()
    field_names = {field.name for field in fields(OnticExtensionModel)}

    assert "selected_history" not in field_names
    assert "hidden_history" not in field_names
    assert not hasattr(model, "selected_history")
    assert isinstance(model.potentiality, OnticPotentiality)
    assert not isinstance(model.potentiality, EpistemicPotentiality)


def test_baseline_next_probabilities_are_half_half() -> None:
    model = canonical_ontic_model()

    assert ontic_next_probabilities(model) == (("l1", 0.5), ("r1", 0.5))


def test_local_view_exposes_no_selected_history() -> None:
    view = project_ontic_view(canonical_ontic_model())

    assert view.actuality == ("p", "n")
    assert view.next_probabilities == (("l1", 0.5), ("r1", 0.5))
    assert not hasattr(view, "selected_history")


def test_left_update_extends_actuality_and_prunes_extensions_without_selector() -> None:
    updated = update_ontic_model(canonical_ontic_model(), "l1")
    h_left = ("p", "n", "l1", "l2")

    assert updated.actuality == ("p", "n", "l1")
    assert updated.potentiality == OnticPotentiality((h_left,))
    assert extension_distribution(updated) == {h_left: 1.0}
    assert ontic_next_probabilities(updated) == (("l2", 1.0),)
    assert not hasattr(updated, "selected_history")


def test_right_update_is_also_admissible_from_unselected_baseline() -> None:
    updated = update_ontic_model(canonical_ontic_model(), "r1")
    h_right = ("p", "n", "r1")

    assert updated.actuality == h_right
    assert updated.potentiality == OnticPotentiality((h_right,))
    assert extension_distribution(updated) == {h_right: 1.0}
    assert ontic_next_probabilities(updated) == ()
    assert not hasattr(updated, "selected_history")


def test_terminal_left_update_has_no_immediate_next_event() -> None:
    model = update_ontic_model(canonical_ontic_model(), "l1")
    terminal = update_ontic_model(model, "l2")
    h_left = ("p", "n", "l1", "l2")

    assert terminal.actuality == h_left
    assert terminal.potentiality == OnticPotentiality((h_left,))
    assert ontic_next_probabilities(terminal) == ()


def test_invalid_observation_is_rejected() -> None:
    with pytest.raises(ValueError, match="not an admissible immediate successor"):
        update_ontic_model(canonical_ontic_model(), "l2")


def test_extension_weights_must_cover_exact_live_extensions_and_normalize() -> None:
    substrate = canonical_stage2_substrate()
    h_left = ("p", "n", "l1", "l2")
    h_right = ("p", "n", "r1")

    with pytest.raises(ValueError, match="exactly all admissible"):
        make_ontic_extension_model(substrate, ("p", "n"), {h_left: 1.0})

    with pytest.raises(ValueError, match="sum to 1"):
        make_ontic_extension_model(
            substrate,
            ("p", "n"),
            {h_left: 0.4, h_right: 0.4},
        )


def test_zero_weight_branch_remains_admissible_but_cannot_be_actualized_by_update() -> None:
    substrate = canonical_stage2_substrate()
    h_left = ("p", "n", "l1", "l2")
    h_right = ("p", "n", "r1")
    model = make_ontic_extension_model(
        substrate,
        ("p", "n"),
        {h_left: 1.0, h_right: 0.0},
    )

    assert model.potentiality.histories == (h_left, h_right)
    assert ontic_next_probabilities(model) == (("l1", 1.0), ("r1", 0.0))
    with pytest.raises(ValueError, match="zero ontic transition weight"):
        update_ontic_model(model, "r1")
