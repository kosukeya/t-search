import pytest

from t_search.stage14_ablation import (
    STAGE14F_ANOMALY,
    STAGE14F_BOUNDED_RESULT,
    STAGE14F_CROSS_ORBIT,
    STAGE14F_GUARDS,
    STAGE14F_MISSING_COMPENSATOR,
    STAGE14F_MISSING_THIRD_DIRECTION,
    STAGE14F_SINGULAR_BASIS,
    STAGE14F_TWO_CLOCK,
    STAGE14F_TYPED_REJECTION,
    STAGE14F_UNIVERSAL_OVERCLAIM,
    STAGE14F_WRONG_COMPENSATOR,
    canonical_stage14f_anomaly_witnesses,
    canonical_stage14f_controls,
    stage14f_diagnostics,
    stage14f_summary,
)


def test_stage14f_deformed_h2_surface_is_rebuilt_before_anomaly_detection():
    witnesses = canonical_stage14f_anomaly_witnesses()
    assert len(witnesses) == 108
    assert all(item.deformed_surface_residual <= 1e-10 for item in witnesses)
    assert all(item.classification == STAGE14F_ANOMALY for item in witnesses)
    assert min(item.anomaly_residual for item in witnesses) == pytest.approx(0.075)
    assert max(item.anomaly_residual for item in witnesses) == pytest.approx(0.175)
    assert all(item.anomaly_residual > 1e-10 for item in witnesses)


def test_stage14f_all_frozen_destructive_controls_are_rejected_with_typed_classifications():
    controls = canonical_stage14f_controls()
    assert len(controls) == 14
    assert all(item.rejected for item in controls)
    classifications = {item.classification for item in controls}
    for classification in (
        "structure_function_removed_control_rejected",
        "rank_deficient_constraint_control_rejected",
        STAGE14F_MISSING_THIRD_DIRECTION,
        STAGE14F_WRONG_COMPENSATOR,
        STAGE14F_MISSING_COMPENSATOR,
        STAGE14F_CROSS_ORBIT,
        STAGE14F_TWO_CLOCK,
        STAGE14F_SINGULAR_BASIS,
        STAGE14F_ANOMALY,
        "representative_dependent_payload_corruption_detected",
        "path_dependent_payload_corruption_detected",
        "basis_dependent_payload_corruption_detected",
        STAGE14F_TYPED_REJECTION,
        STAGE14F_UNIVERSAL_OVERCLAIM,
    ):
        assert classification in classifications


def test_stage14f_required_ablation_witness_counts_match_frozen_families():
    d = stage14f_diagnostics()
    assert d.structure_function_removed_witness_count == 108
    assert d.rank_deficient_witness_count == 108
    assert d.missing_third_direction_witness_count == 108
    assert d.wrong_compensator_witness_count == 1728
    assert d.missing_compensator_witness_count == 1728
    assert d.cross_orbit_rejected_count == 8748
    assert d.two_clock_incomplete_group_count == 36
    assert d.singular_control_count == 2
    assert d.singular_witness_count == 72


def test_stage14f_anomaly_payload_and_typing_controls_are_all_detected():
    d = stage14f_diagnostics()
    assert d.anomaly_witness_count == 108
    assert d.minimum_anomaly_bracket_residual == pytest.approx(0.075)
    assert d.maximum_anomaly_bracket_residual == pytest.approx(0.175)
    assert d.payload_corruption_control_count == 3
    assert d.false_typing_rejected
    assert d.universal_overclaim_rejected


def test_stage14f_closes_only_frozen_criteria_44_through_47():
    d = stage14f_diagnostics()
    assert d.control_count == 14
    assert d.rejected_control_count == 14
    assert d.all_claims_not_licensed
    assert d.criteria_44_47_satisfied


def test_stage14f_summary_keeps_control_results_bounded():
    summary = stage14f_summary()
    assert summary["criteria_44_47_satisfied"]
    assert summary["bounded_result"] == STAGE14F_BOUNDED_RESULT
    assert summary["control_count"] == 14
    assert summary["rejected_control_count"] == 14
    guards = set(summary["guards"])
    for phrase in (
        "negative-control rejection != positive-family obstruction",
        "structure-function removal != evidence against the positive carrier",
        "missing-third-direction failure != physical time asymmetry",
        "wrong compensator failure != physical time asymmetry",
        "constraint-algebra anomaly != ontological becoming",
        "constraint-algebra anomaly != fundamental physical non-Abelianity",
        "control rejection != hypersurface-deformation algebra",
        "control rejection != general relativity",
        "two-clock incompleteness != physical time asymmetry",
        "cross-orbit rejection != spacetime causal separation",
        "singular-basis rejection != universal non-Abelianizability",
        "false typing rejection != empirical discovery",
    ):
        assert phrase in guards
    assert tuple(summary["guards"]) == STAGE14F_GUARDS
