from fractions import Fraction
from math import log2

import pytest

from t_search.stage2_epistemic import canonical_epistemic_model, project_epistemic_view
from t_search.stage2_ontic import canonical_ontic_model, project_ontic_view
from t_search.stage3 import Microstate, canonical_forward_ensemble
from t_search.stage3_accessibility import (
    LocalAccessPolicy,
    make_local_observation_ensemble,
    record_readout_mutual_information,
)
from t_search.stage3_asymmetry import (
    AsymmetricRecordModel,
    assess_record_orientation,
    canonical_record_orientation_assessment,
)
from t_search.stage3_diagnostics import (
    bayes_optimal_accuracy,
    component_mutual_information,
    component_variable,
    mutual_information,
)
from t_search.stage3_local import (
    canonical_record_block,
    combine_with_epistemic_potentiality,
    combine_with_ontic_potentiality,
    compatible_global_histories,
    project_record_view,
)
from t_search.stage3_robustness import (
    PositionRenaming,
    biased_memory_forward_ensemble,
    biased_memory_initial_distribution,
    forward_reverse_balance_ensemble,
    position_tagged_trajectory,
    relabeled_record_profile,
    relabeled_selected_side,
)


def _binary_entropy(probability: float) -> float:
    if probability in (0.0, 1.0):
        return 0.0
    return -probability * log2(probability) - (1.0 - probability) * log2(1.0 - probability)


def _all_zero_trajectory():
    return next(
        trajectory
        for trajectory in canonical_forward_ensemble().trajectories
        if trajectory == (Microstate(0, 0, 0),) * 3
    )


def test_position_bookkeeping_renaming_preserves_profile_and_tracks_selected_side() -> None:
    ensemble = canonical_forward_ensemble()
    assessment = canonical_record_orientation_assessment()
    first = PositionRenaming(("alpha", "center", "omega"))
    second = PositionRenaming(("west", "pivot", "east"))

    assert relabeled_record_profile(ensemble, first) == pytest.approx(
        (("alpha", 1.0), ("center", 1.0), ("omega", 0.0))
    )
    assert relabeled_record_profile(ensemble, second) == pytest.approx(
        (("west", 1.0), ("pivot", 1.0), ("east", 0.0))
    )
    assert relabeled_selected_side(assessment, first) == "alpha"
    assert relabeled_selected_side(assessment, second) == "west"


def test_position_renaming_rejects_duplicate_or_empty_bookkeeping_names() -> None:
    with pytest.raises(ValueError, match="unique"):
        PositionRenaming(("a", "a", "c"))
    with pytest.raises(ValueError, match="non-empty"):
        PositionRenaming(("a", "", "c"))


def test_bijective_register_and_target_value_relabeling_preserves_information_and_decoding() -> None:
    ensemble = canonical_forward_ensemble()
    record = component_variable(1, "m")
    lower = component_variable(0, "x")

    original_mi = mutual_information(ensemble, record, lower)
    original_accuracy = bayes_optimal_accuracy(ensemble, record, lower)
    flipped_record = lambda trajectory: 1 - int(record(trajectory))
    flipped_target = lambda trajectory: 1 - int(lower(trajectory))

    assert mutual_information(ensemble, flipped_record, lower) == pytest.approx(original_mi)
    assert mutual_information(ensemble, flipped_record, flipped_target) == pytest.approx(original_mi)
    assert bayes_optimal_accuracy(ensemble, flipped_record, lower) == pytest.approx(original_accuracy)
    assert bayes_optimal_accuracy(ensemble, flipped_record, flipped_target) == pytest.approx(
        original_accuracy
    )


def test_repeated_microstate_values_do_not_collapse_position_occurrences() -> None:
    trajectory = _all_zero_trajectory()
    tagged = position_tagged_trajectory(trajectory)

    assert tagged[0].state == tagged[1].state == tagged[2].state
    assert len(set(tagged)) == 3
    assert [item.position for item in tagged] == [0, 1, 2]


def test_repeated_local_values_remain_distinct_views_and_coverage_still_matters() -> None:
    block = canonical_record_block()
    trajectory = _all_zero_trajectory()
    view0 = project_record_view(block, trajectory, position=0)
    view1 = project_record_view(block, trajectory, position=1)
    view2 = project_record_view(block, trajectory, position=2)

    assert view0.actuality == view1.actuality == view2.actuality
    assert {view0.position, view1.position, view2.position} == {0, 1, 2}
    assert len(compatible_global_histories(block, (view0, view1))) == 2
    assert compatible_global_histories(block, (view0, view1, view2)) == (trajectory,)


def test_memory_boundary_continuation_refines_blank_zero_to_nonuniform_low_uncertainty() -> None:
    assessments = {
        p: assess_record_orientation(AsymmetricRecordModel(biased_memory_forward_ensemble(p)))
        for p in (
            Fraction(1, 1),
            Fraction(3, 4),
            Fraction(1, 2),
            Fraction(1, 4),
            Fraction(0, 1),
        )
    }
    reduced_information = 1.0 - _binary_entropy(0.25)

    assert assessments[Fraction(1, 1)].record_score == pytest.approx(1.0)
    assert assessments[Fraction(0, 1)].record_score == pytest.approx(1.0)
    assert assessments[Fraction(3, 4)].record_score == pytest.approx(reduced_information)
    assert assessments[Fraction(1, 4)].record_score == pytest.approx(reduced_information)
    assert assessments[Fraction(1, 2)].record_score == pytest.approx(0.0)

    assert assessments[Fraction(1, 1)].orientation == "lower-index"
    assert assessments[Fraction(0, 1)].orientation == "lower-index"
    assert assessments[Fraction(3, 4)].orientation == "lower-index"
    assert assessments[Fraction(1, 4)].orientation == "lower-index"
    assert assessments[Fraction(1, 2)].orientation == "none"


def test_boundary_strength_is_symmetric_under_swapping_memory_zero_and_one_bias() -> None:
    left = assess_record_orientation(
        AsymmetricRecordModel(biased_memory_forward_ensemble(Fraction(3, 4)))
    )
    right = assess_record_orientation(
        AsymmetricRecordModel(biased_memory_forward_ensemble(Fraction(1, 4)))
    )

    assert left.record_score == pytest.approx(right.record_score)
    assert left.accessibility_score == pytest.approx(right.accessibility_score)
    assert left.orientation == right.orientation == "lower-index"


def test_forward_reverse_balance_controls_orientation_continuously_and_antisymmetrically() -> None:
    forward_biased = assess_record_orientation(
        AsymmetricRecordModel(forward_reverse_balance_ensemble(Fraction(3, 4)))
    )
    balanced = assess_record_orientation(
        AsymmetricRecordModel(forward_reverse_balance_ensemble(Fraction(1, 2)))
    )
    reverse_biased = assess_record_orientation(
        AsymmetricRecordModel(forward_reverse_balance_ensemble(Fraction(1, 4)))
    )

    assert forward_biased.orientation == "lower-index"
    assert balanced.orientation == "none"
    assert reverse_biased.orientation == "upper-index"
    assert forward_biased.record_score == pytest.approx(-reverse_biased.record_score)
    assert forward_biased.accessibility_score == pytest.approx(
        -reverse_biased.accessibility_score
    )
    assert balanced.record_score == pytest.approx(0.0)
    assert balanced.accessibility_score == pytest.approx(0.0)


def test_global_boundary_uncertainty_and_local_readout_noise_can_match_accessible_mi_but_not_global_relation() -> None:
    boundary_ensemble = biased_memory_forward_ensemble(Fraction(3, 4))
    boundary_true_information = component_mutual_information(
        boundary_ensemble, 1, "m", 0, "x"
    )

    canonical_block = canonical_record_block()
    noisy_observations = make_local_observation_ensemble(
        canonical_block,
        LocalAccessPolicy(
            expose_x=False,
            expose_m=True,
            record_error_probability=Fraction(1, 4),
        ),
    )
    noisy_accessible_information = record_readout_mutual_information(
        noisy_observations, target_position=0
    )
    canonical_true_information = component_mutual_information(
        canonical_block.ensemble, 1, "m", 0, "x"
    )

    assert boundary_true_information == pytest.approx(noisy_accessible_information)
    assert boundary_true_information == pytest.approx(1.0 - _binary_entropy(0.25))
    assert canonical_true_information == pytest.approx(1.0)
    assert canonical_true_information > noisy_accessible_information


def test_hidden_epistemic_selected_history_swap_does_not_leak_through_complete_local_product() -> None:
    block = canonical_record_block()
    trajectory = next(t for t in block.ensemble.trajectories if t[0] == Microstate(1, 0, 1))
    record_view = project_record_view(block, trajectory, position=1)

    left_model = canonical_epistemic_model(selected_history=("p", "n", "l1", "l2"))
    right_model = canonical_epistemic_model(selected_history=("p", "n", "r1"))
    left_modal = project_epistemic_view(left_model, ("p", "n"))
    right_modal = project_epistemic_view(right_model, ("p", "n"))

    assert left_modal == right_modal
    assert combine_with_epistemic_potentiality(record_view, left_modal) == (
        combine_with_epistemic_potentiality(record_view, right_modal)
    )


def test_epistemic_and_ontic_complete_products_keep_shared_records_but_distinct_potentiality_types() -> None:
    block = canonical_record_block()
    trajectory = next(t for t in block.ensemble.trajectories if t[0] == Microstate(1, 0, 1))
    record_view = project_record_view(block, trajectory, position=1)

    epistemic = combine_with_epistemic_potentiality(
        record_view,
        project_epistemic_view(canonical_epistemic_model(), ("p", "n")),
    )
    ontic = combine_with_ontic_potentiality(
        record_view,
        project_ontic_view(canonical_ontic_model()),
    )

    assert epistemic.records == ontic.records
    assert epistemic.next_probabilities == ontic.next_probabilities
    assert epistemic.actuality.modal_actuality == ontic.actuality.modal_actuality
    assert type(epistemic.potentiality) is not type(ontic.potentiality)


def test_stage3g_probability_controls_reject_out_of_range_values() -> None:
    with pytest.raises(ValueError, match=r"\[0,1\]"):
        biased_memory_initial_distribution(Fraction(-1, 4))
    with pytest.raises(ValueError, match=r"\[0,1\]"):
        forward_reverse_balance_ensemble(Fraction(5, 4))
