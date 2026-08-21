import json
from dataclasses import replace

import pytest

from t_search.stage6_independence import (
    FROZEN_IMPLICATIONS,
    ImplicationStatus,
    TruthValue,
    build_stage6b_cases,
    build_stage6b_matrix,
    stage6b_case_rows,
    stage6b_matrix_rows,
)
from t_search.stage6_inventory import WitnessRecord, build_stage6a_inventory


def _status_map(inventory=None):
    return {
        assessment.spec.implication_id: assessment
        for assessment in build_stage6b_matrix(inventory)
    }


def _replace_measurement(
    record: WitnessRecord,
    name: str,
    value,
) -> WitnessRecord:
    measurements = tuple(
        replace(item, value=value) if item.name == name else item
        for item in record.measurements
    )
    if measurements == record.measurements:
        raise AssertionError(f"measurement {name!r} not found")
    return replace(record, measurements=measurements)


def _replace_inventory_record(
    inventory: tuple[WitnessRecord, ...],
    replacement: WitnessRecord,
) -> tuple[WitnessRecord, ...]:
    return tuple(
        replacement if record.witness_id == replacement.witness_id else record
        for record in inventory
    )


def test_frozen_implication_matrix_contains_exact_protocol_list():
    assert tuple(spec.implication_id for spec in FROZEN_IMPLICATIONS) == tuple(
        f"I{index}" for index in range(1, 11)
    )
    assert tuple(spec.label for spec in FROZEN_IMPLICATIONS) == (
        "order => arrow",
        "reversible microdynamics => no record arrow",
        "perspective consistency => temporal arrow",
        "operational equality => modal/ontological equivalence",
        "global reconstructibility => local accessibility",
        "perspective-dependent structure => operational inconsistency",
        "physical clock change => temporal succession",
        "record arrow => ontologically open future",
        "Potentiality => phenomenal passage",
        "perspective consistency => modal equivalence",
    )


def test_w1_to_w5_expand_into_nine_case_level_evidence_records():
    cases = build_stage6b_cases()

    assert tuple(case.case_id for case in cases) == (
        "W1:global-vs-local",
        "W2:matched-modal-operational",
        "W3:forward",
        "W3:reversed",
        "W3:symmetric",
        "W3:no-record",
        "W3:uniform-memory",
        "W4:same-clock-transition-family",
        "W5:cross-clock-operational",
    )


def test_stage6b_expected_statuses_follow_executable_measurements():
    statuses = {key: value.status for key, value in _status_map().items()}

    assert statuses == {
        "I1": ImplicationStatus.REFUTED,
        "I2": ImplicationStatus.REFUTED,
        "I3": ImplicationStatus.NOT_ESTABLISHED,
        "I4": ImplicationStatus.REFUTED,
        "I5": ImplicationStatus.REFUTED,
        "I6": ImplicationStatus.REFUTED,
        "I7": ImplicationStatus.NOT_ESTABLISHED,
        "I8": ImplicationStatus.NOT_ESTABLISHED,
        "I9": ImplicationStatus.NOT_ESTABLISHED,
        "I10": ImplicationStatus.NOT_ESTABLISHED,
    }


def test_order_does_not_force_record_arrow_in_stage3_controls():
    assessment = _status_map()["I1"]

    assert assessment.status is ImplicationStatus.REFUTED
    assert set(assessment.countermodel_case_ids) == {
        "W3:symmetric",
        "W3:no-record",
        "W3:uniform-memory",
    }
    assert set(assessment.support_case_ids) >= {"W3:forward", "W3:reversed"}


def test_reversible_microdynamics_can_coexist_with_record_arrow():
    assessment = _status_map()["I2"]

    assert assessment.status is ImplicationStatus.REFUTED
    assert set(assessment.countermodel_case_ids) == {
        "W3:forward",
        "W3:reversed",
    }
    assert {
        "W3:symmetric",
        "W3:no-record",
        "W3:uniform-memory",
    }.issubset(set(assessment.support_case_ids))


def test_operational_equality_does_not_force_modal_model_equivalence():
    assessment = _status_map()["I4"]

    assert assessment.status is ImplicationStatus.REFUTED
    assert assessment.countermodel_case_ids == ("W2:matched-modal-operational",)
    evidence = assessment.evidence[0]
    assert evidence.antecedent.measurement_names == ("operational_equal",)
    assert evidence.consequent.measurement_names == (
        "potentiality_runtime_types_equal",
    )


def test_global_reconstruction_does_not_force_one_hop_local_access():
    assessment = _status_map()["I5"]

    assert assessment.status is ImplicationStatus.REFUTED
    assert assessment.countermodel_case_ids == ("W1:global-vs-local",)
    evidence = assessment.evidence[0]
    assert set(evidence.antecedent.measurement_names) == {
        "family_labeled_equal",
        "family_reachability_equal",
    }
    assert set(evidence.consequent.measurement_names) == {
        "remote_globally_reachable",
        "remote_in_one_hop_view",
    }


def test_perspective_dependent_entanglement_is_operationally_consistent():
    assessment = _status_map()["I6"]

    assert assessment.status is ImplicationStatus.REFUTED
    assert assessment.countermodel_case_ids == ("W5:cross-clock-operational",)
    evidence = assessment.evidence[0]
    assert "entanglement_perspective_dependent" in (
        evidence.antecedent.measurement_names
    )
    assert evidence.consequent.measurement_names == (
        "max_born_probability_residual",
    )


@pytest.mark.parametrize(
    ("implication_id", "expected_case"),
    (
        ("I3", "W4:same-clock-transition-family"),
        ("I7", "W5:cross-clock-operational"),
        ("I8", "W3:forward"),
        ("I9", "W2:matched-modal-operational"),
        ("I10", "W4:same-clock-transition-family"),
    ),
)
def test_unmeasured_consequents_remain_not_established(
    implication_id,
    expected_case,
):
    assessment = _status_map()[implication_id]

    assert assessment.status is ImplicationStatus.NOT_ESTABLISHED
    assert assessment.countermodel_case_ids == ()
    assert expected_case in assessment.undecided_case_ids
    for evidence in assessment.evidence:
        assert evidence.consequent.value is TruthValue.UNKNOWN


def test_negative_control_flipping_w1_accessibility_changes_i5_status():
    inventory = build_stage6a_inventory()
    w1 = next(record for record in inventory if record.witness_id == "W1")
    modified_w1 = _replace_measurement(w1, "remote_in_one_hop_view", True)
    modified_inventory = _replace_inventory_record(inventory, modified_w1)

    assessment = _status_map(modified_inventory)["I5"]

    assert assessment.status is ImplicationStatus.SUPPORTED_IN_DECLARED_FAMILY
    assert assessment.countermodel_case_ids == ()
    assert assessment.support_case_ids == ("W1:global-vs-local",)


def test_negative_control_disabling_w1_reconstruction_changes_i5_to_not_established():
    inventory = build_stage6a_inventory()
    w1 = next(record for record in inventory if record.witness_id == "W1")
    modified_w1 = _replace_measurement(w1, "family_labeled_equal", False)
    modified_inventory = _replace_inventory_record(inventory, modified_w1)

    assessment = _status_map(modified_inventory)["I5"]

    assert assessment.status is ImplicationStatus.NOT_ESTABLISHED
    assert assessment.premise_case_ids == ()


def test_negative_control_breaking_born_covariance_changes_i6_status():
    inventory = build_stage6a_inventory()
    w5 = next(record for record in inventory if record.witness_id == "W5")
    assert w5.tolerance is not None
    modified_w5 = _replace_measurement(
        w5,
        "max_born_probability_residual",
        10.0 * w5.tolerance,
    )
    modified_inventory = _replace_inventory_record(inventory, modified_w5)

    assessment = _status_map(modified_inventory)["I6"]

    assert assessment.status is ImplicationStatus.SUPPORTED_IN_DECLARED_FAMILY
    assert assessment.countermodel_case_ids == ()
    assert assessment.support_case_ids == ("W5:cross-clock-operational",)


def test_known_case_facts_retain_measurement_provenance():
    cases = build_stage6b_cases()

    for case in cases:
        for fact in case.facts:
            if fact.value is TruthValue.UNKNOWN:
                continue
            assert fact.measurement_names, (case.case_id, fact.name)


def test_case_and_matrix_rows_are_json_serializable():
    case_rows = stage6b_case_rows()
    matrix_rows = stage6b_matrix_rows()
    payload = json.dumps(
        {"cases": case_rows, "matrix": matrix_rows},
        sort_keys=True,
    )

    assert len(case_rows) == 9
    assert len(matrix_rows) == 10
    assert '"I1"' in payload
    assert '"W5:cross-clock-operational"' in payload
    for row in matrix_rows:
        assert row["status"] in {
            "refuted",
            "supported_in_declared_family",
            "not_established",
        }
