import json

import numpy as np
import pytest

from t_search.stage1 import canonical_block, project_local_view, transitive_closure
from t_search.stage2_epistemic import canonical_epistemic_model, project_epistemic_view
from t_search.stage2_ontic import canonical_ontic_model, project_ontic_view
from t_search.stage2_operational import (
    compare_operational_views,
    operationalize_epistemic_view,
    operationalize_ontic_view,
)
from t_search.stage3_controls import stage3d_control_assessments
from t_search.stage4_transition import transition_composition_residual
from t_search.stage6_inventory import (
    build_stage6a_inventory,
    stage1_reconstruction_accessibility_witness,
    stage2_modal_operational_witness,
    stage3_order_record_witness,
    stage4_same_clock_transition_witness,
    stage5_cross_clock_operational_witness,
    stage6a_inventory_rows,
)

ATOL = 1e-10


def test_w1_recomputes_family_reconstruction_and_local_inaccessibility():
    witness = stage1_reconstruction_accessibility_witness()

    assert witness.witness_id == "W1"
    assert witness.measurement("family_labeled_equal") is True
    assert witness.measurement("family_reachability_equal") is True
    assert witness.measurement("remote_globally_reachable") is True
    assert witness.measurement("remote_in_one_hop_view") is False


def test_w1_measurements_match_direct_stage1_api_calls():
    witness = stage1_reconstruction_accessibility_witness()
    block = canonical_block()
    closure = transitive_closure(block)
    local = project_local_view(block, "a")

    assert witness.measurement("global_reachability_pair_count") == len(closure)
    assert witness.measurement("local_successor_count") == len(local.successors)
    assert ("a", "e") in closure
    assert "e" not in local.successors


def test_w2_recomputes_operational_equality_with_modal_type_difference():
    witness = stage2_modal_operational_witness()

    assert witness.witness_id == "W2"
    assert witness.measurement("operational_equal") is True
    assert witness.measurement("actuality_equal") is True
    assert witness.measurement("next_events_equal") is True
    assert witness.measurement("probabilities_equal") is True
    assert witness.measurement("potentiality_runtime_types_equal") is False
    assert witness.measurement("ontic_selected_future_field_count") == 0


def test_w2_operational_result_matches_direct_stage2_api_calls():
    prefix = ("p", "n")
    epistemic = canonical_epistemic_model()
    ontic = canonical_ontic_model(actuality=prefix)
    direct = compare_operational_views(
        operationalize_epistemic_view(project_epistemic_view(epistemic, prefix)),
        operationalize_ontic_view(project_ontic_view(ontic)),
    )
    witness = stage2_modal_operational_witness()

    assert witness.measurement("operational_equal") == direct.equal
    assert witness.measurement("epistemic_live_history_count") == 2
    assert witness.measurement("ontic_live_history_count") == 2


def test_w3_recomputes_forward_reverse_and_neutral_record_controls():
    witness = stage3_order_record_witness()

    assert witness.witness_id == "W3"
    assert witness.measurement("forward_orientation") == "lower-index"
    assert witness.measurement("reversed_orientation") == "upper-index"
    for name in ("symmetric", "no-record", "uniform-memory"):
        assert witness.measurement(f"{name}_orientation") == "none"
        assert witness.measurement(f"{name}_record_defined") is False
    for name in ("forward", "reversed", "symmetric", "no-record", "uniform-memory"):
        assert witness.measurement(f"{name}_declared_microdynamics_reversible") is True


def test_w3_signed_scores_match_direct_stage3_control_assessments():
    witness = stage3_order_record_witness()
    direct = stage3d_control_assessments()

    assert witness.measurement("forward_record_score") == pytest.approx(
        direct["forward"].record_score
    )
    assert witness.measurement("reversed_record_score") == pytest.approx(
        direct["reversed"].record_score
    )
    assert witness.measurement("forward_accessibility_score") == pytest.approx(0.5)
    assert witness.measurement("reversed_accessibility_score") == pytest.approx(-0.5)
    assert witness.measurement("symmetric_record_score") == pytest.approx(0.0)
    assert witness.measurement("forward_declared_position_count") == 3


def test_w4_recomputes_same_clock_identity_inverse_composition_and_unitarity():
    witness = stage4_same_clock_transition_witness()

    assert witness.witness_id == "W4"
    assert witness.measurement("clock_reading_count") == 4
    for name in (
        "max_identity_residual",
        "max_inverse_residual",
        "max_composition_residual",
        "max_expected_transition_residual",
        "max_unitarity_residual",
    ):
        assert float(witness.measurement(name)) <= ATOL


def test_w4_composition_inventory_is_tied_to_direct_stage4_api():
    witness = stage4_same_clock_transition_witness()
    direct = transition_composition_residual(0, 2, 3, 4)

    assert direct <= float(witness.measurement("max_composition_residual")) + 1e-15
    assert direct <= ATOL


def test_w5_recomputes_all_cross_clock_routes_and_operational_covariance():
    witness = stage5_cross_clock_operational_witness()

    assert witness.witness_id == "W5"
    assert witness.measurement("three_clock_route_count") == 162
    assert float(witness.measurement("max_cross_clock_composition_residual")) <= ATOL
    assert float(witness.measurement("max_born_probability_residual")) <= ATOL


def test_w5_recomputes_perspective_dependent_entanglement_control():
    witness = stage5_cross_clock_operational_witness()

    assert float(witness.measurement("entanglement_A_bits")) == pytest.approx(1.0, abs=ATOL)
    assert float(witness.measurement("entanglement_B_bits")) == pytest.approx(0.0, abs=ATOL)
    assert float(witness.measurement("entanglement_C_bits")) == pytest.approx(0.0, abs=ATOL)
    assert witness.measurement("entanglement_perspective_dependent") is True


def test_inventory_contains_exactly_one_typed_witness_per_prior_stage():
    inventory = build_stage6a_inventory()

    assert tuple(record.witness_id for record in inventory) == ("W1", "W2", "W3", "W4", "W5")
    assert tuple(record.source_stage for record in inventory) == (1, 2, 3, 4, 5)
    assert len({record.witness_id for record in inventory}) == 5
    for record in inventory:
        assert record.domain
        assert record.assumptions
        assert record.roles
        assert record.measurements


def test_inventory_rows_are_json_serializable_and_preserve_measurement_metadata():
    rows = stage6a_inventory_rows()
    payload = json.dumps(rows, sort_keys=True)

    assert "W1" in payload and "W5" in payload
    assert len(rows) == 5
    for row in rows:
        assert isinstance(row["measurements"], dict)
        for measurement in row["measurements"].values():
            assert set(measurement) == {"value", "unit"}


def test_measurement_lookup_rejects_unknown_names():
    witness = build_stage6a_inventory()[0]
    with pytest.raises(KeyError):
        witness.measurement("not-a-measurement")
