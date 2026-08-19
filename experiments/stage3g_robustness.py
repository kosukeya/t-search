"""Run the Stage 3G robustness/control summary.

This script reports only toy-model robustness facts.  It does not identify a
fundamental physical arrow of time.
"""

from fractions import Fraction

from t_search.stage2_epistemic import canonical_epistemic_model, project_epistemic_view
from t_search.stage2_ontic import canonical_ontic_model, project_ontic_view
from t_search.stage3 import Microstate, canonical_forward_ensemble
from t_search.stage3_accessibility import (
    LocalAccessPolicy,
    make_local_observation_ensemble,
    record_readout_mutual_information,
)
from t_search.stage3_asymmetry import AsymmetricRecordModel, assess_record_orientation
from t_search.stage3_diagnostics import component_mutual_information
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
    forward_reverse_balance_ensemble,
    position_tagged_trajectory,
    relabeled_record_profile,
    relabeled_selected_side,
)


def main() -> None:
    canonical = canonical_forward_ensemble()
    canonical_assessment = assess_record_orientation(AsymmetricRecordModel(canonical))

    renaming = PositionRenaming(("alpha", "pivot", "omega"))
    print("bookkeeping profile:", relabeled_record_profile(canonical, renaming))
    print("selected symbolic side:", relabeled_selected_side(canonical_assessment, renaming))

    all_zero = next(
        trajectory
        for trajectory in canonical.trajectories
        if trajectory == (Microstate(0, 0, 0),) * 3
    )
    print("repeated-state tagged occurrences:", position_tagged_trajectory(all_zero))

    print("\nMemory-boundary sweep P(M0=0):")
    for p in (
        Fraction(1, 1),
        Fraction(3, 4),
        Fraction(1, 2),
        Fraction(1, 4),
        Fraction(0, 1),
    ):
        assessment = assess_record_orientation(
            AsymmetricRecordModel(biased_memory_forward_ensemble(p))
        )
        print(
            p,
            "A_R=", round(assessment.record_score, 12),
            "A_Acc=", round(assessment.accessibility_score, 12),
            "orientation=", assessment.orientation,
        )

    print("\nForward/reverse balance sweep:")
    for weight in (Fraction(1, 1), Fraction(3, 4), Fraction(1, 2), Fraction(1, 4), Fraction(0, 1)):
        assessment = assess_record_orientation(
            AsymmetricRecordModel(forward_reverse_balance_ensemble(weight))
        )
        print(
            weight,
            "A_R=", round(assessment.record_score, 12),
            "A_Acc=", round(assessment.accessibility_score, 12),
            "orientation=", assessment.orientation,
        )

    boundary = biased_memory_forward_ensemble(Fraction(3, 4))
    boundary_true_mi = component_mutual_information(boundary, 1, "m", 0, "x")
    block = canonical_record_block()
    noisy = make_local_observation_ensemble(
        block,
        LocalAccessPolicy(
            expose_x=False,
            expose_m=True,
            record_error_probability=Fraction(1, 4),
        ),
    )
    noisy_accessible_mi = record_readout_mutual_information(noisy, target_position=0)
    canonical_true_mi = component_mutual_information(block.ensemble, 1, "m", 0, "x")
    print("\nboundary true MI:", boundary_true_mi)
    print("canonical noisy accessible MI:", noisy_accessible_mi)
    print("canonical true MI remains:", canonical_true_mi)

    trajectory = next(t for t in block.ensemble.trajectories if t[0] == Microstate(1, 0, 1))
    record_view = project_record_view(block, trajectory, position=1)
    left = combine_with_epistemic_potentiality(
        record_view,
        project_epistemic_view(
            canonical_epistemic_model(selected_history=("p", "n", "l1", "l2")),
            ("p", "n"),
        ),
    )
    right = combine_with_epistemic_potentiality(
        record_view,
        project_epistemic_view(
            canonical_epistemic_model(selected_history=("p", "n", "r1")),
            ("p", "n"),
        ),
    )
    ontic = combine_with_ontic_potentiality(record_view, project_ontic_view(canonical_ontic_model()))
    print("\nhidden-h* swap changes complete local view:", left != right)
    print("shared record layer across E/O:", left.records == ontic.records)
    print("potentiality types distinct:", type(left.potentiality) is not type(ontic.potentiality))

    repeated_views = tuple(project_record_view(block, all_zero, position=p) for p in (0, 1, 2))
    print("repeated local values, positions 0+1 compatible histories:", len(compatible_global_histories(block, repeated_views[:2])))
    print("repeated local values, positions 0+1+2 compatible histories:", len(compatible_global_histories(block, repeated_views)))

    print("\nGuard: robustness under these controls != fundamental physical temporal arrow")


if __name__ == "__main__":
    main()
