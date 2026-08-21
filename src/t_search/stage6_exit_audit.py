"""Evidence-driven audit for Stage 6 protocol exit criteria 1--31.

Criteria 32--34 depend on the Stage 6G synthesis/gate choice and are completed in
``stage6_synthesis.pre_merge_exit_criteria``. Criterion 35 is intentionally
external because it depends on final GitHub CI and PR review state.
"""

from __future__ import annotations

from .stage5_clock_change import DEFAULT_ATOL
from .stage6_ablation import (
    AblationStatus,
    LAYERS,
    accessibility_inaccessibility_control,
    build_stage6f_ablation_matrix,
    stage6f_minimality_summary,
)
from .stage6_compatibility import stage6d_rows
from .stage6_independence import ImplicationStatus, build_stage6b_matrix
from .stage6_inventory import build_stage6a_inventory
from .stage6_partial_atlas import stage6c_summary_rows
from .stage6_record_modality import stage6e_rows


def _inventory_checks() -> dict[int, bool]:
    inventory = build_stage6a_inventory()
    by_id = {item.witness_id: item for item in inventory}
    expected_ids = ("W1", "W2", "W3", "W4", "W5")
    complete = tuple(item.witness_id for item in inventory) == expected_ids
    metadata_complete = all(
        item.domain
        and item.assumptions
        and item.measurements
        and (item.tolerance is not None or item.source_stage in {1, 2, 3})
        for item in inventory
    )
    return {
        5: complete and "W1" in by_id,
        6: complete and "W2" in by_id,
        7: complete and "W3" in by_id,
        8: complete and "W4" in by_id,
        9: complete and "W5" in by_id,
        10: complete and metadata_complete,
    }


def _independence_checks() -> dict[int, bool]:
    matrix = build_stage6b_matrix()
    by_id = {item.spec.implication_id: item for item in matrix}
    statuses_machine_readable = len(matrix) == 10 and all(
        isinstance(item.status, ImplicationStatus) for item in matrix
    )
    provenance_complete = all(
        item.evidence and all(evidence.witness_id for evidence in item.evidence)
        for item in matrix
    )
    status_values = {item.status for item in matrix}
    return {
        11: statuses_machine_readable and provenance_complete,
        12: by_id["I1"].status is ImplicationStatus.REFUTED,
        13: by_id["I4"].status is ImplicationStatus.REFUTED,
        14: by_id["I5"].status is ImplicationStatus.REFUTED,
        15: by_id["I6"].status is ImplicationStatus.REFUTED,
        16: (
            ImplicationStatus.REFUTED in status_values
            and ImplicationStatus.NOT_ESTABLISHED in status_values
            and ImplicationStatus.REFUTED is not ImplicationStatus.NOT_ESTABLISHED
        ),
    }


def _partial_atlas_checks() -> dict[int, bool]:
    rows = stage6c_summary_rows()
    canonical = rows["canonical_diagnostics"]
    family = rows["family_scan"]
    perturbed = rows["perturbed_diagnostics"]
    return {
        17: (
            canonical["target_present"]
            and not canonical["direct_edge_present"]
            and canonical["path_count"] > 0
            and canonical["max_indirect_direct_residual"] <= DEFAULT_ATOL
        ),
        18: family["max_pairwise_path_residual"] <= DEFAULT_ATOL,
        19: family["max_loop_residual"] <= DEFAULT_ATOL,
        20: (
            perturbed["max_pairwise_path_residual"] > DEFAULT_ATOL
            or perturbed["max_loop_residual"] > DEFAULT_ATOL
        ),
        21: canonical["target_present"] and not canonical["direct_edge_present"],
    }


def _compatibility_checks() -> dict[int, bool]:
    rows = stage6d_rows()
    canonical = rows["canonical"]
    mismatch = rows["mismatch_control"]
    guards = rows["guards"]
    return {
        22: canonical["path_count"] > 0 and canonical["event_relation_count"] > 0,
        23: (
            canonical["max_square_residual"] <= DEFAULT_ATOL
            and canonical["order_violation_count"] == 0
        ),
        24: (
            mismatch["mismatch_failed_square_count"] > 0
            and mismatch["mismatch_order_violation_count"] > 0
        ),
        25: not guards["horizontal_vertical_identity_claimed"],
    }


def _record_modal_checks() -> dict[int, bool]:
    rows = stage6e_rows()
    preserving = rows["record_transport"]["orientation_preserving"]
    reversing = rows["record_transport"]["orientation_reversing"]
    hidden = rows["record_transport"]["accessibility_controls"]["target-hidden"]
    modal = rows["modality_transport"]
    return {
        26: (
            preserving["correspondence_orientation"] == "preserving"
            and preserving["globally_compatible"]
            and reversing["correspondence_orientation"] == "reversing"
            and reversing["globally_compatible"]
        ),
        27: (
            hidden["globally_compatible"]
            and not hidden["target_local"]["record_exposed"]
            and hidden["target_local"]["record_score"] is None
        ),
        28: (
            modal["epistemic_extensions"]["relation"] == "bijection"
            and modal["epistemic_extensions"]["relation_holds"]
            and modal["ontic_extensions"]["relation"] == "bijection"
            and modal["ontic_extensions"]["relation_holds"]
        ),
        29: modal["underdetermination_preserved"],
    }


def _minimality_checks() -> dict[int, bool]:
    cases = build_stage6f_ablation_matrix()
    summary = stage6f_minimality_summary()
    hidden = accessibility_inaccessibility_control()
    own = summary["own_role_status_after_ablation"]
    return {
        30: len(cases) >= 3 and tuple(case.removed_layer for case in cases) == LAYERS,
        31: (
            AblationStatus.LOST.value in own.values()
            and AblationStatus.RECONSTRUCTIBLE.value in own.values()
            and hidden.status is AblationStatus.INACCESSIBLE
        ),
    }


def audit_exit_criteria_1_to_31() -> dict[int, bool]:
    """Recompute protocol criteria 1--31 from Stage 6 APIs."""

    d_rows = stage6d_rows()
    implications = build_stage6b_matrix()
    inventory = build_stage6a_inventory()

    checks: dict[int, bool] = {
        1: set(LAYERS) == {"O", "P", "R", "V", "Omega"},
        2: (
            not d_rows["guards"]["horizontal_vertical_identity_claimed"]
            and not d_rows["guards"]["perspective_change_is_temporal_succession"]
        ),
        3: (
            not d_rows["guards"]["clock_coordinate_defines_event_correspondence"]
            and d_rows["canonical"]["event_relation_count"] > 0
        ),
        4: (
            len(inventory) == 5
            and len(implications) == 10
            and all(isinstance(item.status, ImplicationStatus) for item in implications)
        ),
    }
    checks.update(_inventory_checks())
    checks.update(_independence_checks())
    checks.update(_partial_atlas_checks())
    checks.update(_compatibility_checks())
    checks.update(_record_modal_checks())
    checks.update(_minimality_checks())

    if tuple(sorted(checks)) != tuple(range(1, 32)):
        raise RuntimeError("Stage 6 exit audit does not cover criteria 1--31 exactly")
    return checks
