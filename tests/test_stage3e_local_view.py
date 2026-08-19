from dataclasses import fields

import pytest

from t_search.stage2_epistemic import (
    EpistemicPotentiality,
    canonical_epistemic_model,
    project_epistemic_view,
)
from t_search.stage2_ontic import (
    OnticPotentiality,
    canonical_ontic_model,
    project_ontic_view,
)
from t_search.stage3 import Microstate
from t_search.stage3_local import (
    EpistemicCompleteLocalView,
    OnticCompleteLocalView,
    canonical_projection_classification,
    canonical_record_block,
    combine_with_epistemic_potentiality,
    combine_with_ontic_potentiality,
    compatible_global_histories,
    project_record_view,
    reconstruct_global_history,
)


def _example_trajectory():
    block = canonical_record_block()
    return next(
        trajectory
        for trajectory in block.ensemble.trajectories
        if trajectory[0] == Microstate(1, 0, 1)
    )


def test_canonical_record_block_is_explicit_and_reversible() -> None:
    block = canonical_record_block()

    assert len(block.state_space) == 8
    assert len(block.ensemble.trajectories) == 4
    assert all(
        z1 == block.first_update(z0) and z2 == block.second_update(z1)
        for z0, z1, z2 in block.ensemble.trajectories
    )


def test_central_local_view_exposes_x_m_record_interface_but_not_n() -> None:
    block = canonical_record_block()
    view = project_record_view(block, _example_trajectory(), position=1)

    assert view.position == 1
    assert view.actuality.x == 1
    assert view.actuality.m == 1
    assert view.records.register_value == 1
    assert dict(view.records.information_profile) == pytest.approx({0: 1.0, 1: 1.0, 2: 0.0})
    assert view.records.orientation == "lower-index"

    actuality_fields = {field.name for field in fields(view.actuality)}
    view_fields = {field.name for field in fields(view)}
    assert "n" not in actuality_fields
    assert "trajectory" not in view_fields
    assert "opposite_state" not in view_fields


def test_single_central_view_is_ambiguous_over_hidden_environment_bit() -> None:
    block = canonical_record_block()
    view = project_record_view(block, _example_trajectory(), position=1)

    compatible = compatible_global_histories(block, (view,))

    assert len(compatible) == 2
    assert {trajectory[1].n for trajectory in compatible} == {0, 1}
    with pytest.raises(ValueError, match="do not uniquely reconstruct"):
        reconstruct_global_history(block, (view,))


def test_two_position_view_family_uniquely_reconstructs_complete_history() -> None:
    block = canonical_record_block()
    trajectory = _example_trajectory()
    central = project_record_view(block, trajectory, position=1)
    upper = project_record_view(block, trajectory, position=2)

    assert reconstruct_global_history(block, (central, upper)) == trajectory


def test_incompatible_local_views_have_no_global_completion() -> None:
    block = canonical_record_block()
    trajectory = _example_trajectory()
    central = project_record_view(block, trajectory, position=1)
    other = next(t for t in block.ensemble.trajectories if t[2].x == trajectory[2].x ^ 1)
    upper = project_record_view(block, other, position=2)

    assert compatible_global_histories(block, (central, upper)) == ()
    with pytest.raises(ValueError, match="incompatible with every global trajectory"):
        reconstruct_global_history(block, (central, upper))


def test_projection_rejects_nonmember_trajectory_and_duplicate_positions() -> None:
    block = canonical_record_block()
    fake = (
        Microstate(0, 0, 0),
        Microstate(1, 0, 0),
        Microstate(1, 0, 0),
    )

    with pytest.raises(ValueError, match="must belong"):
        project_record_view(block, fake, position=1)

    view = project_record_view(block, _example_trajectory(), position=1)
    with pytest.raises(ValueError, match="positions must be unique"):
        compatible_global_histories(block, (view, view))


def test_epistemic_complete_view_preserves_typed_potentiality_without_hidden_history() -> None:
    record_view = project_record_view(canonical_record_block(), _example_trajectory(), position=1)
    model = canonical_epistemic_model()
    modal_view = project_epistemic_view(model, ("p", "n"))

    complete = combine_with_epistemic_potentiality(record_view, modal_view)

    assert isinstance(complete, EpistemicCompleteLocalView)
    assert isinstance(complete.potentiality, EpistemicPotentiality)
    assert complete.actuality.record_actuality == record_view.actuality
    assert complete.actuality.modal_actuality == ("p", "n")
    assert complete.records == record_view.records
    assert "selected_history" not in {field.name for field in fields(complete)}


def test_ontic_complete_view_preserves_typed_potentiality_without_selected_future() -> None:
    record_view = project_record_view(canonical_record_block(), _example_trajectory(), position=1)
    modal_view = project_ontic_view(canonical_ontic_model())

    complete = combine_with_ontic_potentiality(record_view, modal_view)

    assert isinstance(complete, OnticCompleteLocalView)
    assert isinstance(complete.potentiality, OnticPotentiality)
    assert complete.actuality.record_actuality == record_view.actuality
    assert complete.actuality.modal_actuality == ("p", "n")
    assert complete.records == record_view.records
    assert "selected_history" not in {field.name for field in fields(complete)}


def test_same_record_layer_attaches_to_both_modal_semantics_without_changing_orientation() -> None:
    record_view = project_record_view(canonical_record_block(), _example_trajectory(), position=1)
    epistemic = combine_with_epistemic_potentiality(
        record_view,
        project_epistemic_view(canonical_epistemic_model(), ("p", "n")),
    )
    ontic = combine_with_ontic_potentiality(
        record_view,
        project_ontic_view(canonical_ontic_model()),
    )

    assert epistemic.records == ontic.records
    assert epistemic.records.orientation == "lower-index"
    assert type(epistemic.potentiality) is not type(ontic.potentiality)
    assert epistemic.actuality.modal_actuality == ontic.actuality.modal_actuality


def test_projection_information_classification_is_explicit() -> None:
    classification = canonical_projection_classification()

    assert "current N_k environment bit" in classification.globally_hidden
    assert "complete actual trajectory" in classification.ambiguous_from_single_view
    assert any("complete actual trajectory" in item for item in classification.reconstructible_from_view_family)
    assert any("probability weights" in item for item in classification.lost_without_weighted_global_structure)
