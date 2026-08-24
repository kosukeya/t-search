from __future__ import annotations

import pytest

from t_search.stage13_multi_constraint import (
    STAGE13A_ATOL,
    canonical_stage13a_orbits,
    canonical_stage13a_representatives_for_orbit,
)
from t_search.stage13_paths import (
    STAGE13B_CLASSIFICATION,
    STAGE13B_CROSS_ORBIT_CLASSIFICATION,
    STAGE13B_METAPHYSICAL_CLAIM_STATUS,
    STAGE13B_PATH_ORDER_ROLE,
    STAGE13B_PATH_WORD_ROLE,
    STAGE13B_SAME_RAW_CLASSIFICATION,
    STAGE13B_TEMPORAL_ORDER_STATUS,
    STAGE13B_WRONG_COMPENSATOR_CLASSIFICATION,
    canonical_stage13b_mixed_path_comparisons,
    stage13b_cross_orbit_control_rejected,
    stage13b_diagnostics,
    stage13b_mixed_path_comparison,
    stage13b_summary,
)


def test_stage13b_uses_all_144_nontrivial_mixed_pairs() -> None:
    comparisons = canonical_stage13b_mixed_path_comparisons()

    assert len(comparisons) == 144
    assert all(abs(item.s) > STAGE13A_ATOL for item in comparisons)
    assert all(abs(item.delta_X) > STAGE13A_ATOL for item in comparisons)
    assert all(abs(item.u_TX - item.u_XT) > STAGE13A_ATOL for item in comparisons)


def test_stage13b_same_raw_u_reordering_is_detectably_noncommuting_for_every_mixed_pair() -> None:
    comparisons = canonical_stage13b_mixed_path_comparisons()

    assert all(item.same_raw_endpoint_separation > STAGE13A_ATOL for item in comparisons)
    assert all(item.same_raw_TX_target_residual <= STAGE13A_ATOL for item in comparisons)
    assert all(item.same_raw_XT_target_residual > STAGE13A_ATOL for item in comparisons)
    assert {item.same_raw_classification for item in comparisons} == {
        STAGE13B_SAME_RAW_CLASSIFICATION
    }


def test_stage13b_exact_compensator_closes_both_path_orders_onto_same_target() -> None:
    comparisons = canonical_stage13b_mixed_path_comparisons()

    for item in comparisons:
        assert item.compensator_law_residual <= STAGE13A_ATOL
        assert item.compensated_endpoint_separation <= STAGE13A_ATOL
        assert item.compensated_TX_target_residual <= STAGE13A_ATOL
        assert item.compensated_XT_target_residual <= STAGE13A_ATOL
        assert item.compensated_classification == STAGE13B_CLASSIFICATION


def test_stage13b_compensated_paths_preserve_constraints_and_declared_orbit_identity() -> None:
    comparisons = canonical_stage13b_mixed_path_comparisons()

    assert all(item.compensated_constraint_residual <= STAGE13A_ATOL for item in comparisons)
    assert all(item.physical_orbit_identity_preserved for item in comparisons)
    assert all(item.orbit_id in {orbit.orbit_id for orbit in canonical_stage13a_orbits()} for item in comparisons)


def test_stage13b_wrong_compensator_is_detected_for_every_mixed_pair() -> None:
    comparisons = canonical_stage13b_mixed_path_comparisons()

    assert all(item.wrong_compensator_parameter_residual > STAGE13A_ATOL for item in comparisons)
    assert all(item.wrong_compensator_target_residual > STAGE13A_ATOL for item in comparisons)
    assert {item.wrong_compensator_classification for item in comparisons} == {
        STAGE13B_WRONG_COMPENSATOR_CLASSIFICATION
    }


def test_stage13b_path_order_metadata_is_not_typed_as_physical_temporal_order() -> None:
    comparisons = canonical_stage13b_mixed_path_comparisons()

    assert all(item.path_word_role == STAGE13B_PATH_WORD_ROLE for item in comparisons)
    assert all(item.path_order_role == STAGE13B_PATH_ORDER_ROLE for item in comparisons)
    assert all(item.temporal_order_status == STAGE13B_TEMPORAL_ORDER_STATUS for item in comparisons)
    assert all(item.metaphysical_claim_status == STAGE13B_METAPHYSICAL_CLAIM_STATUS for item in comparisons)
    assert all(item.path_word_TX != item.path_word_XT for item in comparisons)


def test_stage13b_rejects_cross_orbit_path_instead_of_compensating_it() -> None:
    alpha = canonical_stage13a_representatives_for_orbit(canonical_stage13a_orbits()[0])
    beta = canonical_stage13a_representatives_for_orbit(canonical_stage13a_orbits()[1])
    source = alpha[0]
    target = next(
        item
        for item in beta
        if abs(item.T - source.T) > STAGE13A_ATOL and abs(item.X - source.X) > STAGE13A_ATOL
    )

    with pytest.raises(ValueError, match="distinct physical orbits"):
        stage13b_mixed_path_comparison(source, target)
    assert stage13b_cross_orbit_control_rejected()
    assert STAGE13B_CROSS_ORBIT_CLASSIFICATION == "cross_orbit_path_rejected"


def test_stage13b_diagnostics_close_exactly_criteria_17_23() -> None:
    diagnostics = stage13b_diagnostics()
    summary = stage13b_summary()

    assert diagnostics.mixed_pair_count == 144
    assert diagnostics.nontrivial_two_generator_pair_count == 144
    assert diagnostics.same_raw_noncommuting_count == 144
    assert diagnostics.compensated_closure_count == 144
    assert diagnostics.compensated_surface_preservation_count == 144
    assert diagnostics.wrong_compensator_detected_count == 144
    assert diagnostics.typed_path_semantics_count == 144
    assert diagnostics.cross_orbit_control_rejected
    assert diagnostics.minimum_same_raw_endpoint_separation > STAGE13A_ATOL
    assert diagnostics.maximum_compensator_law_residual <= STAGE13A_ATOL
    assert diagnostics.maximum_compensated_endpoint_separation <= STAGE13A_ATOL
    assert diagnostics.maximum_compensated_target_residual <= STAGE13A_ATOL
    assert diagnostics.maximum_compensated_constraint_residual <= STAGE13A_ATOL
    assert diagnostics.minimum_wrong_compensator_target_residual > STAGE13A_ATOL
    assert diagnostics.physical_orbit_identity_preserved
    assert diagnostics.path_order_temporal_distinction_explicit
    assert diagnostics.criteria_17_23_satisfied

    assert summary["criteria_17_23_satisfied"] is True
    assert summary["next"].startswith("Stage 13C")
    joined_guards = " ".join(summary["guards"])
    assert "raw gauge-path commutativity" in joined_guards
    assert "physical temporal history" in joined_guards
    assert "refoliation invariance" in joined_guards
