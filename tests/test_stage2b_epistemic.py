import pytest

from t_search.stage2 import canonical_stage2_substrate
from t_search.stage2_epistemic import (
    actual_next_from_hidden_history,
    belief_distribution,
    canonical_epistemic_model,
    condition_epistemic_model,
    make_epistemic_history_model,
    project_epistemic_view,
    selected_history,
)

H_LEFT = ("p", "n", "l1", "l2")
H_RIGHT = ("p", "n", "r1")
D0 = ("p", "n")


def test_canonical_model_contains_selected_complete_history() -> None:
    model = canonical_epistemic_model()

    assert selected_history(model) == H_LEFT
    assert belief_distribution(model) == {H_LEFT: 0.5, H_RIGHT: 0.5}


def test_baseline_projection_has_two_live_hypotheses_and_equal_next_predictions() -> None:
    view = project_epistemic_view(canonical_epistemic_model(), D0)

    assert view.actuality == D0
    assert view.potentiality.histories == (H_LEFT, H_RIGHT)
    assert dict(view.next_probabilities) == {"l1": 0.5, "r1": 0.5}


def test_hidden_selected_history_swap_does_not_change_local_projection() -> None:
    left_hidden = canonical_epistemic_model(selected_history=H_LEFT)
    right_hidden = canonical_epistemic_model(selected_history=H_RIGHT)

    assert project_epistemic_view(left_hidden, D0) == project_epistemic_view(
        right_hidden,
        D0,
    )


def test_privileged_hidden_history_diagnostic_distinguishes_models() -> None:
    left_hidden = canonical_epistemic_model(selected_history=H_LEFT)
    right_hidden = canonical_epistemic_model(selected_history=H_RIGHT)

    assert actual_next_from_hidden_history(left_hidden, D0) == "l1"
    assert actual_next_from_hidden_history(right_hidden, D0) == "r1"


def test_local_view_does_not_expose_selected_history() -> None:
    view = project_epistemic_view(canonical_epistemic_model(), D0)

    assert not hasattr(view, "selected_history")
    assert set(view.__dataclass_fields__) == {
        "actuality",
        "potentiality",
        "next_probabilities",
    }


def test_observation_conditions_beliefs_without_changing_hidden_history() -> None:
    model = canonical_epistemic_model()

    updated, prefix = condition_epistemic_model(model, D0, "l1")

    assert prefix == ("p", "n", "l1")
    assert selected_history(updated) == H_LEFT
    assert belief_distribution(updated) == {H_LEFT: 1.0, H_RIGHT: 0.0}

    view = project_epistemic_view(updated, prefix)
    assert view.potentiality.histories == (H_LEFT,)
    assert dict(view.next_probabilities) == {"l2": 1.0}


def test_observation_contradicting_hidden_history_is_rejected() -> None:
    with pytest.raises(ValueError, match="contradicts"):
        condition_epistemic_model(canonical_epistemic_model(), D0, "r1")


def test_invalid_belief_distributions_are_rejected() -> None:
    substrate = canonical_stage2_substrate()

    with pytest.raises(ValueError, match="exactly all"):
        make_epistemic_history_model(substrate, H_LEFT, {H_LEFT: 1.0})

    with pytest.raises(ValueError, match="sum to 1"):
        make_epistemic_history_model(
            substrate,
            H_LEFT,
            {H_LEFT: 0.6, H_RIGHT: 0.6},
        )

    with pytest.raises(ValueError, match="non-negative"):
        make_epistemic_history_model(
            substrate,
            H_LEFT,
            {H_LEFT: 1.1, H_RIGHT: -0.1},
        )


def test_projection_rejects_evidence_with_zero_epistemic_support() -> None:
    substrate = canonical_stage2_substrate()
    model = make_epistemic_history_model(
        substrate,
        H_LEFT,
        {H_LEFT: 1.0, H_RIGHT: 0.0},
    )

    with pytest.raises(ValueError, match="zero epistemic support"):
        project_epistemic_view(model, ("p", "n", "r1"))


def test_terminal_projection_has_no_next_event() -> None:
    model = canonical_epistemic_model()
    updated, prefix = condition_epistemic_model(model, D0, "l1")
    updated, terminal = condition_epistemic_model(updated, prefix, "l2")

    view = project_epistemic_view(updated, terminal)

    assert view.potentiality.histories == (H_LEFT,)
    assert view.next_probabilities == ()
