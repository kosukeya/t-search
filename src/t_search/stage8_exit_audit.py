"""Executable Stage 8 exit audit.

Criteria 11--49 are recomputed from Stage 8A--G APIs. Criteria 1--10 are the
protocol/typing freeze and remain covered by documentation-consistency tests.
Criterion 50 is deliberately external: it is satisfied only after the final
Stage 8 head passes the full repository regression and merge-readiness review.

No criterion in this module is a hard-coded prose verdict.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .stage5_clock_change import DEFAULT_ATOL
from .stage8_ablation import (
    RoleStatus,
    mismatch_diagnostics,
    no_record_v_family_diagnostics,
    perspective_map_reconstruction_diagnostics,
    semantic_weight_reconstruction_diagnostics,
    singleton_qext_diagnostics,
    stage8f_ablation_matrix,
)
from .stage8_compatibility import stage8e_compatibility_diagnostics
from .stage8_continuations import stage8a_substrate_diagnostics
from .stage8_modal import stage8b_modal_diagnostics
from .stage8_modal_transport import stage8d_transport_diagnostics
from .stage8_operational import stage8c_operational_diagnostics
from .stage8_synthesis import Stage8SynthesisChoice, select_synthesis_choice, stage9_gate_candidates


@dataclass(frozen=True, slots=True)
class Stage8ExitAudit:
    criteria: tuple[tuple[int, bool], ...]

    @property
    def passed(self) -> int:
        return sum(value for _, value in self.criteria)

    @property
    def total(self) -> int:
        return len(self.criteria)

    @property
    def all_passed(self) -> bool:
        return all(value for _, value in self.criteria)

    def as_dict(self) -> dict[str, Any]:
        return {
            "criteria": {str(key): value for key, value in self.criteria},
            "passed": self.passed,
            "total": self.total,
            "all_passed": self.all_passed,
            "protocol_criteria_1_10": "validated by documentation-consistency tests",
            "criterion_50": "external final CI and merge-readiness review",
        }


def _case_by_id(ingredient: str):
    return next(case for case in stage8f_ablation_matrix() if case.ingredient == ingredient)


def pre_merge_exit_criteria(*, atol: float = DEFAULT_ATOL) -> dict[int, bool]:
    """Recompute scientific/current-execution criteria 11--49."""

    a = stage8a_substrate_diagnostics()
    b = stage8b_modal_diagnostics()
    c = stage8c_operational_diagnostics()
    d = stage8d_transport_diagnostics()
    e = stage8e_compatibility_diagnostics()
    no_record = no_record_v_family_diagnostics()
    singleton = singleton_qext_diagnostics()
    semantic_weight = semantic_weight_reconstruction_diagnostics()
    maps = perspective_map_reconstruction_diagnostics()
    ablations = stage8f_ablation_matrix()
    mismatches = mismatch_diagnostics()
    gates = stage9_gate_candidates()

    record_case = _case_by_id("record_coupling_neutralized")
    singleton_case = _case_by_id("qext_collapsed_singleton")
    semantics_case = _case_by_id("modal_semantics_removed")
    weights_case = _case_by_id("weights_unfixed")
    maps_case = _case_by_id("explicit_perspective_maps_removed")
    chi_case = _case_by_id("event_correspondence_removed")
    access_case = _case_by_id("current_record_access_hidden")

    criteria: dict[int, bool] = {
        # Stage 8A — criteria 11--16
        11: bool(a.qext_size >= 2 and a.physically_inequivalent),
        12: bool(a.future_operator_residual > atol and a.future_probe_difference > atol),
        13: bool(a.renamed_equivalent and a.deduplicated_size_with_rename == 2),
        14: bool(a.minimum_clock_reduction_rank == 14 and a.maximum_constraint_residual <= atol),
        15: bool(a.invalid_current_prefix_rejected),
        16: bool(a.terminal_qext_size == 0),
        # Stage 8B — criteria 17--21
        17: bool(b.potentiality_types_distinct and b.potentiality_members_match),
        18: bool(b.ontic_no_selected_complete_continuation_datum and b.ontic_full_weight_support),
        19: bool(b.shared_carrier_identity),
        20: bool(b.matched_weight_residual <= atol and b.selected_swap_weight_residual <= atol),
        21: bool(b.selected_swap_pre_view_equal and b.selected_hidden_from_pre_view_schema),
        # Stage 8C — criteria 22--29
        22: bool(c.hidden_selected_absent_from_operational_schema),
        23: bool(c.matched_operational_equal and c.privileged_structures_distinct),
        24: bool(c.selected_swap_operational_equal),
        25: bool(c.weight_mismatch_changes_prediction),
        26: bool(c.update_before_equal and c.update_after_equal),
        27: bool(c.update_anchor_advanced and c.update_outcome_equal),
        28: bool(
            c.epistemic_selected_preserved
            and c.ontic_posterior_pruned
            and c.ontic_no_selected_complete_continuation_datum
        ),
        29: bool(
            c.superposition_does_not_select_modal_semantics
            and c.state_and_born_data_do_not_select_modal_semantics
        ),
        # Stage 8D — criteria 30--35
        30: bool(d.qext_size == 2 and d.perspective_nodes_per_continuation == 9),
        31: bool(
            d.continuation_level_pv_covariance
            and d.max_state_transport_residual <= atol
            and d.max_inverse_residual <= atol
            and d.max_metric_covariance_residual <= 10 * atol
            and d.max_composition_residual <= atol
        ),
        32: bool(
            d.correct_chi_bijective
            and d.correct_chi_physical_classes_preserved
            and d.max_weight_transport_residual <= atol
        ),
        33: bool(d.matched_modal_views_all_nodes and d.selected_swap_modal_views_all_nodes),
        34: bool(
            d.wrong_class_correspondence_rejected
            and d.terminal_current_correspondence_rejected
            and d.wrong_continuation_map_rejected
        ),
        35: bool(
            not d.full_stage8c_measurement_covariance_established
            and not d.one_rederived_map_suffices_for_all_continuations
        ),
        # Stage 8E — criteria 36--41
        36: bool(e.p_o_event_effect_covariance and e.p_r_current_record_covariance),
        37: bool(e.p_v_class_weight_covariance and e.o_v_difference_after_current_anchor),
        38: bool(e.current_record_shared_across_v_classes and e.distinct_v_classes_with_same_current_record),
        39: bool(e.order_does_not_force_directional_r and e.record_scramble_control_directional_r_present),
        40: bool(
            e.same_por_carrier_distinct_v_semantics
            and e.privileged_modal_structures_distinct
            and e.weight_mismatch_control_detected
        ),
        41: bool(
            not e.full_directional_porv_integration_established
            and not e.full_stage8c_measurement_covariance_established
        ),
        # Stage 8F — criteria 42--47
        42: bool(
            no_record.current_record_lost
            and no_record.perspective_structure_preserved
            and no_record.physically_inequivalent
            and record_case.status("current_record_content") is RoleStatus.LOST
            and record_case.status("V_physical_multiplicity") is RoleStatus.PRESERVED
        ),
        43: bool(
            singleton.physical_multiplicity_lost
            and singleton.semantic_types_distinct
            and singleton.singleton_weight_reconstructible_from_normalization
            and singleton_case.status("V_physical_multiplicity") is RoleStatus.LOST
            and singleton_case.status("V_weights") is RoleStatus.RECONSTRUCTIBLE
        ),
        44: bool(
            semantic_weight.same_carrier_distinct_modal_semantics
            and not semantic_weight.modal_semantics_reconstructible_from_public_por
            and semantic_weight.same_carrier_admits_distinct_weights
            and semantic_weight.prediction_changes_with_weights
            and semantics_case.status("V_selected_vs_unselected_semantics") is RoleStatus.LOST
            and weights_case.status("V_weights") is RoleStatus.UNDERDETERMINED
        ),
        45: bool(maps.reconstructible and maps_case.status("P_V_class_transport") is RoleStatus.RECONSTRUCTIBLE),
        46: bool(chi_case.status("P_V_class_transport") is RoleStatus.NOT_ESTABLISHED),
        47: bool(
            all(item.detected for item in mismatches)
            and access_case.status("current_record_content") is RoleStatus.PRESERVED
            and access_case.status("local_record_access") is RoleStatus.INACCESSIBLE
            and len(ablations) == 7
        ),
        # Stage 8G — criteria 48--49
        48: bool(select_synthesis_choice() is Stage8SynthesisChoice.REFINED_LAYERED),
        49: bool(
            len(gates) >= 2
            and gates[0].gate_id == "directional_record_potentiality"
            and gates[0].score > gates[1].score
        ),
    }
    return criteria


def stage8_pre_merge_audit() -> Stage8ExitAudit:
    criteria = pre_merge_exit_criteria()
    return Stage8ExitAudit(tuple(sorted(criteria.items())))
