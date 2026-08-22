"""Stage 9E P/O/R_direction/V compatibility matrix.

Stage 9E introduces no new physical carrier.  It classifies the six frozen
compatibility questions from the Stage 9 protocol using executable evidence
already accumulated in Stages 9A--9D.

The matrix distinguishes compatibility from determination.  In particular,
coexistence of directional records with nontrivial quantum Potentiality does
not identify R with V, and matched public views do not identify selected and
unselected modal semantics.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from functools import lru_cache
from typing import Literal

from .stage5_clock_change import DEFAULT_ATOL
from .stage9_controls import stage9b_control_diagnostics
from .stage9_modal import stage9c_modal_diagnostics
from .stage9_substrate import stage9a_substrate_diagnostics
from .stage9_transport import stage9d_transport_diagnostics

CompatibilityStatus = Literal[
    "compatible",
    "preserved",
    "reconstructible",
    "inaccessible",
    "lost",
    "underdetermined",
    "not_established",
    "implication_refuted",
]


@dataclass(frozen=True, slots=True)
class Stage9ECompatibilityEntry:
    relation: str
    status: CompatibilityStatus
    evidence: str


@dataclass(frozen=True, slots=True)
class Stage9ECompatibilityDiagnostics:
    qext_nontrivial: bool
    coherent_direction_on_canonical_carrier: bool
    direction_v_extension_coexistence: bool
    direction_controls_retain_v_extension: bool
    r_direction_v_extension_compatible: bool
    v_extension_identity_does_not_determine_direction: bool
    direction_does_not_determine_v_extension_identity: bool
    weight_change_detected: bool
    weight_change_preserves_current_direction: bool
    r_direction_v_weights_compatible: bool
    matched_directional_public_views: bool
    privileged_modal_structures_distinct: bool
    hidden_selector_swap_publicly_invariant: bool
    r_direction_v_semantics_underdetermined: bool
    positive_access_shared_across_continuations: bool
    access_covariant_across_clock_atlas: bool
    r_access_v_compatible: bool
    p_transport_covariant: bool
    p_direction_v_compatible: bool
    same_order_skeleton_supports_positive_negative_and_zero_direction: bool
    o_direction_v_compatible: bool
    o_does_not_determine_r_direction: bool
    full_future_measurement_covariance_established: bool
    direct_xi_rv_value_constraint_established: bool


def _scores_by_control() -> dict[str, tuple[float, ...]]:
    controls = stage9b_control_diagnostics()
    return {
        "forward": tuple(value for _, value in controls.forward_scores),
        "reversed": tuple(value for _, value in controls.reversed_scores),
        "balanced": tuple(value for _, value in controls.balanced_scores),
        "no-record": tuple(value for _, value in controls.no_record_scores),
    }


@lru_cache(maxsize=4)
def stage9e_compatibility_diagnostics(
    *, atol: float = DEFAULT_ATOL
) -> Stage9ECompatibilityDiagnostics:
    a = stage9a_substrate_diagnostics(atol=atol)
    b = stage9b_control_diagnostics()
    c = stage9c_modal_diagnostics(atol=atol)
    d = stage9d_transport_diagnostics(atol=atol)
    scores = _scores_by_control()

    qext_nontrivial = bool(a.qext_size >= 2 and a.physically_inequivalent)
    coherent_direction = bool(
        a.coherent_direction
        and a.minimum_record_score > atol
        and a.continuation_identity_separated_from_record_channel
    )
    direction_extension_coexistence = bool(qext_nontrivial and coherent_direction)

    controls_retain_v = bool(
        b.all_controls_retain_nontrivial_v
        and b.all_pure_controls_valid_constrained_carriers
        and b.minimum_clock_reduction_rank == 14
    )
    direction_extension_compatible = bool(
        direction_extension_coexistence and controls_retain_v
    )

    positive = all(value > atol for value in scores["forward"])
    negative = all(value < -atol for value in scores["reversed"])
    balanced_zero = all(abs(value) <= atol for value in scores["balanced"])
    no_record_zero = all(abs(value) <= atol for value in scores["no-record"])
    order_direction_variation = bool(
        positive
        and negative
        and balanced_zero
        and no_record_zero
        and b.common_reversal_is_interaction_reversal
        and controls_retain_v
    )

    # h_L and h_R are physically inequivalent V classes with the same canonical
    # direction, while the same h_L/h_R V distinction survives +, -, and zero
    # directional controls.  Neither side therefore uniquely determines the
    # other in this declared finite family.
    v_identity_not_determine_direction = bool(
        direction_extension_coexistence
        and len({round(value, 12) for value in scores["forward"]}) == 1
        and order_direction_variation
    )
    direction_not_determine_v_identity = bool(
        direction_extension_coexistence
        and controls_retain_v
        and a.qext_size >= 2
    )

    weight_change = bool(c.weight_mismatch_changes_prediction)
    weight_preserves_direction = bool(
        c.weight_mismatch_preserves_current_directional_data
        and c.directional_interface_present
        and c.directional_interface_shared_across_continuations
    )
    direction_weights_compatible = bool(weight_change and weight_preserves_direction)

    matched_public = bool(c.matched_operational_equal and c.directional_interface_present)
    privileged_distinct = bool(c.privileged_structures_distinct)
    hidden_swap = bool(c.selected_swap_operational_equal)
    direction_semantics_underdetermined = bool(
        matched_public and privileged_distinct and hidden_swap
    )

    positive_access_shared = bool(
        a.minimum_accessibility_score > atol
        and c.directional_accessibility_score > atol
        and c.directional_interface_shared_across_continuations
    )
    access_covariant = bool(
        d.directional_record_covariance
        and d.max_preserving_accessibility_residual <= atol
        and d.matched_modal_views_all_nodes
        and d.class_weight_transport_covariance
    )
    access_v_compatible = bool(
        qext_nontrivial
        and positive_access_shared
        and access_covariant
        and c.privileged_structures_distinct
    )

    p_covariant = bool(
        d.continuation_level_transport_covariance
        and d.directional_record_covariance
        and d.class_weight_transport_covariance
        and d.correct_class_correspondence_valid
        and d.observable_typing_fields_present
    )
    p_direction_v_compatible = bool(
        p_covariant
        and direction_extension_compatible
        and d.matched_modal_views_all_nodes
        and d.selected_swap_modal_views_all_nodes
    )

    o_direction_v_compatible = bool(
        qext_nontrivial
        and a.common_e1_state_residual <= atol
        and a.invalid_current_prefix_rejected
        and a.terminal_qext_size == 0
        and order_direction_variation
    )
    o_not_determine_direction = bool(o_direction_v_compatible and order_direction_variation)

    # Stages 9A--9D support coexistence, controlled separation, weight variation,
    # and semantic underdetermination.  They do not establish a new direct value
    # constraint Xi_RV.  Existing event/class/observable correspondence remains a
    # typing/transport resource and is not collapsed into a direct R-V law.
    direct_xi_rv = False

    return Stage9ECompatibilityDiagnostics(
        qext_nontrivial=qext_nontrivial,
        coherent_direction_on_canonical_carrier=coherent_direction,
        direction_v_extension_coexistence=direction_extension_coexistence,
        direction_controls_retain_v_extension=controls_retain_v,
        r_direction_v_extension_compatible=direction_extension_compatible,
        v_extension_identity_does_not_determine_direction=v_identity_not_determine_direction,
        direction_does_not_determine_v_extension_identity=direction_not_determine_v_identity,
        weight_change_detected=weight_change,
        weight_change_preserves_current_direction=weight_preserves_direction,
        r_direction_v_weights_compatible=direction_weights_compatible,
        matched_directional_public_views=matched_public,
        privileged_modal_structures_distinct=privileged_distinct,
        hidden_selector_swap_publicly_invariant=hidden_swap,
        r_direction_v_semantics_underdetermined=direction_semantics_underdetermined,
        positive_access_shared_across_continuations=positive_access_shared,
        access_covariant_across_clock_atlas=access_covariant,
        r_access_v_compatible=access_v_compatible,
        p_transport_covariant=p_covariant,
        p_direction_v_compatible=p_direction_v_compatible,
        same_order_skeleton_supports_positive_negative_and_zero_direction=order_direction_variation,
        o_direction_v_compatible=o_direction_v_compatible,
        o_does_not_determine_r_direction=o_not_determine_direction,
        full_future_measurement_covariance_established=(
            d.full_stage9c_future_measurement_covariance_established
        ),
        direct_xi_rv_value_constraint_established=direct_xi_rv,
    )


def stage9e_compatibility_matrix(
    *, atol: float = DEFAULT_ATOL
) -> tuple[Stage9ECompatibilityEntry, ...]:
    d = stage9e_compatibility_diagnostics(atol=atol)
    return (
        Stage9ECompatibilityEntry(
            "R_direction-V_extension",
            "compatible" if d.r_direction_v_extension_compatible else "not_established",
            "two physically inequivalent V extensions share the same nonzero canonical direction, while +/−/0 directional controls retain nontrivial QExt",
        ),
        Stage9ECompatibilityEntry(
            "R_direction-V_weights",
            "compatible" if d.r_direction_v_weights_compatible else "not_established",
            "changing only continuation weights changes future prediction while preserving the current directional record interface",
        ),
        Stage9ECompatibilityEntry(
            "R_direction-V_semantics",
            (
                "underdetermined"
                if d.r_direction_v_semantics_underdetermined
                else "not_established"
            ),
            "matched directional public views and hidden-selector swap invariance coexist with distinct privileged selected-vs-unselected modal structures",
        ),
        Stage9ECompatibilityEntry(
            "R_access-V",
            "compatible" if d.r_access_v_compatible else "not_established",
            "positive local accessibility is shared by both V classes and transports covariantly with continuation classes/weights across the declared clock atlas",
        ),
        Stage9ECompatibilityEntry(
            "P-R_direction-V",
            "compatible" if d.p_direction_v_compatible else "not_established",
            "continuation-specific P transport covariantly carries directional record observables, V classes/weights, and matched modal public views",
        ),
        Stage9ECompatibilityEntry(
            "O-R_direction-V",
            "compatible" if d.o_direction_v_compatible else "not_established",
            "the common e0<e1<e2 order/current anchor supports nontrivial V together with positive, negative, balanced-zero, and no-record-zero directional controls",
        ),
    )


def stage9e_constraint_assessment(
    *, atol: float = DEFAULT_ATOL
) -> tuple[Stage9ECompatibilityEntry, ...]:
    """Return determination/constraint statements that qualify the six-row matrix."""

    d = stage9e_compatibility_diagnostics(atol=atol)
    return (
        Stage9ECompatibilityEntry(
            "V_extension=>R_direction",
            (
                "implication_refuted"
                if d.v_extension_identity_does_not_determine_direction
                else "not_established"
            ),
            "the same nontrivial h_L/h_R V distinction survives positive, negative, balanced-zero, and no-record-zero directional controls",
        ),
        Stage9ECompatibilityEntry(
            "R_direction=>V_extension identity",
            (
                "implication_refuted"
                if d.direction_does_not_determine_v_extension_identity
                else "not_established"
            ),
            "physically inequivalent h_L/h_R V classes carry the same canonical nonzero direction",
        ),
        Stage9ECompatibilityEntry(
            "O=>R_direction",
            (
                "implication_refuted"
                if d.o_does_not_determine_r_direction
                else "not_established"
            ),
            "one declared order/current-anchor skeleton supports positive, negative, and zero directional diagnostics while V remains nontrivial",
        ),
        Stage9ECompatibilityEntry(
            "direct Xi_RV value constraint",
            (
                "compatible"
                if d.direct_xi_rv_value_constraint_established
                else "not_established"
            ),
            "no new direct R_direction-V value law is required or established by Stages 9A-D; explicit event/class/observable correspondence remains a separate typing resource",
        ),
        Stage9ECompatibilityEntry(
            "full future-measurement covariance",
            (
                "compatible"
                if d.full_future_measurement_covariance_established
                else "not_established"
            ),
            "successful state/record/class/weight transport does not by itself construct the full cross-continuation Stage 9C future-signature measurement family",
        ),
    )


def stage9e_summary() -> dict[str, object]:
    diagnostics = stage9e_compatibility_diagnostics()
    return {
        "stage": "9E",
        "status": "P/O/R_direction/V compatibility matrix classified from Stage 9A-D executable evidence",
        "diagnostics": asdict(diagnostics),
        "compatibility_matrix": [
            asdict(entry) for entry in stage9e_compatibility_matrix()
        ],
        "constraint_assessment": [
            asdict(entry) for entry in stage9e_constraint_assessment()
        ],
        "exit_criteria_satisfied": tuple(range(37, 43)),
        "guards": (
            "R-V compatibility != R=V",
            "R_direction-V_extension compatibility != universal R-V independence",
            "weight-direction compatibility != weight-direction identity",
            "operational directional equality != modal/ontological identity",
            "accessible canonical R_access-V compatibility != accessibility independence",
            "P-R_direction-V covariance != ontic openness",
            "O-R_direction-V compatibility != O determines R_direction",
            "absence of an established direct Xi_RV value constraint != proof that no such constraint exists",
            "full Stage 9C future-measurement covariance remains not_established",
            "directional record arrow != ontological future openness",
            "directional record arrow != ontological becoming",
            "not_established != false",
        ),
        "next": "Stage 9F — ablation / reconstruction / accessibility matrix",
    }
