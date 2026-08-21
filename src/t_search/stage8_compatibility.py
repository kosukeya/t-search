"""Stage 8E compatibility and underdetermination for P/O/R/V.

Stage 8D established continuation-aware P-V class/weight transport, but it also
showed that a shared A/e1 current ray need not remain one identical conditional
pure ray in B/C perspectives.  Stage 8E therefore keeps the layers typed and
asks which compatibility claims can actually be witnessed on the same finite
constrained carrier.

The executable checks are deliberately split into:

* P-O: covariance of the A-clock event-effect family under each continuation's
  re-derived physical-clock atlas;
* P-R(current): covariance of the declared target-memory record readout with
  transported observables, plus wrong-target and bare-observable controls;
* P-V: the continuation-class/weight covariance already established by Stage
  8D;
* O-V: canonical continuation classes agree through e1 and first differ only at
  the later e2 event; current-prefix and terminal controls remain explicit;
* R(current)-V: h_L/h_R have the same current target-specific record while
  remaining physically inequivalent future continuations;
* O-R(direction): a contrast with the Stage 7C record-scrambling completion
  keeps the same e0<e1<e2 event skeleton and the same A/e1 current state but
  changes the directional record score.  Thus order does not force directional
  R in this declared family;
* modal underdetermination: the same P/O/current-R physical carrier hosts the
  epistemic selected-h* and ontic no-selected-continuation semantics while
  their public transported views remain matched under equal weights.

The canonical Stage 8 h_L/h_R future operations preserve the recorded target,
so their lower and upper record information are equal and directional R is not
present.  This is a result, not a software failure.  Stage 8E therefore does
not claim full P/O/directional-R/V co-realization.

Compatibility here is finite-model compatibility, not metaphysical identity or
fundamentality.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import permutations, product
from typing import Literal

import numpy as np

from .stage3_asymmetry import orientation_from_scores
from .stage5_clock_change import DEFAULT_ATOL, SUBSYSTEMS
from .stage7_history import (
    CURRENT_EVENT,
    LOWER_EVENT,
    UPPER_EVENT,
    assess_relational_record,
    canonical_physical_history_state,
    clock_reading_projector,
    reduced_history_state,
)
from .stage7_record import (
    canonical_target_pair_projector,
    canonical_wrong_target_pair_projector,
)
from .stage7_spectator import MEMORY_DIMENSION, memory_identity
from .stage8_continuations import (
    QuantumContinuation,
    assess_continuation_admissibility,
    canonical_continuation_left,
    canonical_continuation_right,
    continuation_physical_basis,
    continuation_schedule_rest_operators,
    quantum_extension_set,
    reduced_continuation_state,
    stage8a_substrate_diagnostics,
)
from .stage8_modal import (
    canonical_stage8b_models,
    make_ontic_quantum_extension_model,
)
from .stage8_modal_transport import (
    continuation_clock_change_support_matrix,
    continuation_clock_coordinates,
    continuation_reduced_support_coordinates,
    continuation_support_metric,
    perspective_modal_view,
    stage8d_transport_diagnostics,
)
from .stage8_operational import privileged_quantum_modal_diagnostic

CompatibilityStatus = Literal[
    "compatible",
    "underdetermined",
    "implication_refuted",
    "partial",
    "not_established",
]


@dataclass(frozen=True, slots=True)
class ContinuationRecordProfile:
    continuation_id: str
    clock: str
    clock_index: int
    lower_information: float
    current_information: float
    upper_information: float
    lower_accuracy: float
    current_accuracy: float
    upper_accuracy: float
    record_score: float
    accessibility_score: float
    orientation: str
    current_record_present: bool
    directional_record_defined: bool


@dataclass(frozen=True, slots=True)
class CompatibilityEntry:
    relation: str
    status: CompatibilityStatus
    evidence: str


@dataclass(frozen=True, slots=True)
class Stage8ECompatibilityDiagnostics:
    p_o_event_effect_covariance: bool
    max_p_o_operator_transport_residual: float
    max_p_o_probability_residual: float
    max_event_effect_completeness_residual: float
    max_event_effect_metric_self_adjoint_residual: float
    p_r_current_record_covariance: bool
    max_current_record_joint_residual: float
    max_current_record_information_residual: float
    max_wrong_target_information: float
    bare_record_metric_self_adjoint_residual: float
    bare_record_observable_rejected: bool
    p_v_class_weight_covariance: bool
    o_v_first_difference_event: int
    o_v_difference_after_current_anchor: bool
    o_v_invalid_current_prefix_rejected: bool
    o_v_terminal_qext_empty: bool
    current_record_shared_across_v_classes: bool
    current_record_class_joint_residual: float
    distinct_v_classes_with_same_current_record: bool
    baseline_left_record_score: float
    baseline_right_record_score: float
    baseline_directional_r_absent: bool
    record_scramble_control_current_state_residual: float
    record_scramble_control_record_score: float
    record_scramble_control_directional_r_present: bool
    order_does_not_force_directional_r: bool
    same_por_carrier_distinct_v_semantics: bool
    matched_public_modal_views_all_nodes: bool
    privileged_modal_structures_distinct: bool
    transported_weight_mismatch_density_residual: float
    weight_mismatch_control_detected: bool
    full_stage8c_measurement_covariance_established: bool
    full_directional_porv_integration_established: bool


def _target_support_projector(*, wrong_target: bool = False) -> np.ndarray:
    pair = (
        canonical_wrong_target_pair_projector()
        if wrong_target
        else canonical_target_pair_projector()
    )
    return np.kron(pair, memory_identity())


def _memory_support_projector(bit: int) -> np.ndarray:
    if bit not in (0, 1):
        raise ValueError("memory bit must be 0 or 1")
    pair_dimension = canonical_target_pair_projector().shape[0]
    memory = np.zeros((MEMORY_DIMENSION, MEMORY_DIMENSION), dtype=np.complex128)
    memory[bit, bit] = 1.0
    return np.kron(np.eye(pair_dimension, dtype=np.complex128), memory)


def _physical_from_a_support(
    continuation: QuantumContinuation,
    event_index: int,
    support_operator: np.ndarray,
) -> np.ndarray:
    coordinates = continuation_clock_coordinates(
        continuation, "A", event_index
    )
    return np.linalg.inv(coordinates) @ support_operator @ coordinates


def _represent_physical_operator(
    continuation: QuantumContinuation,
    physical_operator: np.ndarray,
    clock: str,
    index: int,
) -> np.ndarray:
    coordinates = continuation_clock_coordinates(continuation, clock, index)
    return coordinates @ physical_operator @ np.linalg.inv(coordinates)


def _metric_self_adjoint_residual(
    operator: np.ndarray,
    metric: np.ndarray,
) -> float:
    return float(np.linalg.norm(metric @ operator - operator.conj().T @ metric))


def _metric_expectation(
    state: np.ndarray,
    metric: np.ndarray,
    operator: np.ndarray,
) -> complex:
    denominator = np.vdot(state, metric @ state)
    if abs(denominator.imag) > 1e-9 or denominator.real <= DEFAULT_ATOL:
        raise RuntimeError("invalid induced-metric norm in Stage 8E")
    return np.vdot(state, metric @ operator @ state) / denominator


def _mutual_information(joint: np.ndarray) -> float:
    probabilities = np.asarray(joint, dtype=float)
    probabilities = probabilities / np.sum(probabilities)
    px = np.sum(probabilities, axis=1, keepdims=True)
    pm = np.sum(probabilities, axis=0, keepdims=True)
    independent = px @ pm
    mask = probabilities > DEFAULT_ATOL
    if not np.any(mask):
        return 0.0
    return float(
        np.sum(
            probabilities[mask]
            * np.log2(probabilities[mask] / independent[mask])
        )
    )


def _decoder_accuracy(joint: np.ndarray) -> float:
    return float(sum(np.max(joint[:, memory_bit]) for memory_bit in (0, 1)))


def continuation_record_joint_distribution(
    continuation: QuantumContinuation,
    clock: str,
    index: int,
    target_event: int,
    *,
    wrong_target: bool = False,
) -> tuple[np.ndarray, float, float, float]:
    """Read the e1 memory against a declared target event in one perspective.

    The target operator is anchored at the declared A-clock event and the memory
    readout at current e1.  Both are converted to physical coefficients and then
    represented in the requested continuation-specific perspective chart.
    """

    if target_event not in (LOWER_EVENT, CURRENT_EVENT, UPPER_EVENT):
        raise ValueError("target event must be e0, e1, or e2")

    state = continuation_reduced_support_coordinates(continuation, clock, index)
    metric = continuation_support_metric(continuation, clock, index)
    target_physical = _physical_from_a_support(
        continuation,
        target_event,
        _target_support_projector(wrong_target=wrong_target),
    )
    target = _represent_physical_operator(
        continuation, target_physical, clock, index
    )
    memories = tuple(
        _represent_physical_operator(
            continuation,
            _physical_from_a_support(
                continuation,
                CURRENT_EVENT,
                _memory_support_projector(bit),
            ),
            clock,
            index,
        )
        for bit in (0, 1)
    )

    identity = np.eye(target.shape[0], dtype=np.complex128)
    joint = np.zeros((2, 2), dtype=float)
    max_self_adjoint = _metric_self_adjoint_residual(target, metric)
    max_projector = float(np.linalg.norm(target @ target - target))
    max_commutator = 0.0

    for target_bit, target_projector in (
        (1, target),
        (0, identity - target),
    ):
        for memory_bit, memory in enumerate(memories):
            max_self_adjoint = max(
                max_self_adjoint,
                _metric_self_adjoint_residual(memory, metric),
            )
            max_projector = max(
                max_projector,
                float(np.linalg.norm(memory @ memory - memory)),
            )
            max_commutator = max(
                max_commutator,
                float(
                    np.linalg.norm(
                        target_projector @ memory - memory @ target_projector
                    )
                ),
            )
            value = _metric_expectation(
                state,
                metric,
                target_projector @ memory,
            )
            if abs(value.imag) > 1e-8:
                raise RuntimeError("record readout acquired an imaginary probability")
            joint[target_bit, memory_bit] = float(value.real)

    joint[np.abs(joint) <= DEFAULT_ATOL] = 0.0
    if np.min(joint) < -1e-9:
        raise RuntimeError("record joint distribution acquired a negative probability")
    joint = np.clip(joint, 0.0, None)
    joint = joint / np.sum(joint)
    return joint, max_self_adjoint, max_projector, max_commutator


def continuation_record_profile(
    continuation: QuantumContinuation,
    clock: str = "A",
    index: int = CURRENT_EVENT,
    *,
    tolerance: float = 1e-10,
) -> ContinuationRecordProfile:
    lower, *_ = continuation_record_joint_distribution(
        continuation, clock, index, LOWER_EVENT
    )
    current, *_ = continuation_record_joint_distribution(
        continuation, clock, index, CURRENT_EVENT
    )
    upper, *_ = continuation_record_joint_distribution(
        continuation, clock, index, UPPER_EVENT
    )
    lower_information = _mutual_information(lower)
    current_information = _mutual_information(current)
    upper_information = _mutual_information(upper)
    lower_accuracy = _decoder_accuracy(lower)
    current_accuracy = _decoder_accuracy(current)
    upper_accuracy = _decoder_accuracy(upper)
    record_score = lower_information - upper_information
    accessibility_score = lower_accuracy - upper_accuracy
    orientation = orientation_from_scores(
        record_score, accessibility_score, tolerance=tolerance
    )
    return ContinuationRecordProfile(
        continuation_id=continuation.continuation_id,
        clock=clock,
        clock_index=index,
        lower_information=lower_information,
        current_information=current_information,
        upper_information=upper_information,
        lower_accuracy=lower_accuracy,
        current_accuracy=current_accuracy,
        upper_accuracy=upper_accuracy,
        record_score=record_score,
        accessibility_score=accessibility_score,
        orientation=orientation,
        current_record_present=current_information > tolerance,
        directional_record_defined=orientation != "none",
    )


def _event_effect_physical_operator(
    continuation: QuantumContinuation,
    event_index: int,
) -> np.ndarray:
    if event_index not in (LOWER_EVENT, CURRENT_EVENT, UPPER_EVENT):
        raise ValueError("event index must be e0, e1, or e2")
    event = np.kron(
        clock_reading_projector(event_index),
        np.eye(18, dtype=np.complex128),
    )
    physical = continuation_physical_basis(continuation)
    return physical.conj().T @ event @ physical


def _event_effect_diagnostics(
    continuations: tuple[QuantumContinuation, ...],
) -> tuple[float, float, float, float]:
    max_operator_transport = 0.0
    max_probability = 0.0
    max_completeness = 0.0
    max_self_adjoint = 0.0

    for continuation in continuations:
        physical_effects = tuple(
            _event_effect_physical_operator(continuation, event)
            for event in (LOWER_EVENT, CURRENT_EVENT, UPPER_EVENT)
        )
        reference_state = continuation_reduced_support_coordinates(
            continuation, "A", CURRENT_EVENT
        )
        reference_metric = continuation_support_metric(
            continuation, "A", CURRENT_EVENT
        )
        reference_probabilities = []
        for effect in physical_effects:
            local = _represent_physical_operator(
                continuation, effect, "A", CURRENT_EVENT
            )
            reference_probabilities.append(
                float(_metric_expectation(reference_state, reference_metric, local).real)
            )

        for clock in SUBSYSTEMS:
            for index in range(3):
                state = continuation_reduced_support_coordinates(
                    continuation, clock, index
                )
                metric = continuation_support_metric(continuation, clock, index)
                locals_ = tuple(
                    _represent_physical_operator(
                        continuation, effect, clock, index
                    )
                    for effect in physical_effects
                )
                max_completeness = max(
                    max_completeness,
                    float(
                        np.linalg.norm(
                            sum(locals_) - np.eye(14, dtype=np.complex128)
                        )
                    ),
                )
                for event, local in enumerate(locals_):
                    max_self_adjoint = max(
                        max_self_adjoint,
                        _metric_self_adjoint_residual(local, metric),
                    )
                    probability = float(
                        _metric_expectation(state, metric, local).real
                    )
                    max_probability = max(
                        max_probability,
                        abs(probability - reference_probabilities[event]),
                    )

        for source_clock, target_clock in permutations(SUBSYSTEMS, 2):
            for source_index, target_index in product(range(3), repeat=2):
                transform = continuation_clock_change_support_matrix(
                    continuation,
                    target_clock,
                    target_index,
                    source_clock,
                    source_index,
                )
                inverse = np.linalg.inv(transform)
                for effect in physical_effects:
                    source = _represent_physical_operator(
                        continuation,
                        effect,
                        source_clock,
                        source_index,
                    )
                    target = _represent_physical_operator(
                        continuation,
                        effect,
                        target_clock,
                        target_index,
                    )
                    max_operator_transport = max(
                        max_operator_transport,
                        float(np.linalg.norm(transform @ source @ inverse - target)),
                    )

    return (
        max_operator_transport,
        max_probability,
        max_completeness,
        max_self_adjoint,
    )


def _record_covariance_diagnostics(
    continuations: tuple[QuantumContinuation, ...],
) -> tuple[float, float, float, float]:
    max_joint = 0.0
    max_information = 0.0
    max_wrong_target_information = 0.0
    max_bare_self_adjoint = 0.0
    bare_target = _target_support_projector()
    bare_memory = _memory_support_projector(0)

    for continuation in continuations:
        reference_joint, *_ = continuation_record_joint_distribution(
            continuation, "A", CURRENT_EVENT, CURRENT_EVENT
        )
        reference_information = _mutual_information(reference_joint)
        for clock in SUBSYSTEMS:
            for index in range(3):
                joint, *_ = continuation_record_joint_distribution(
                    continuation, clock, index, CURRENT_EVENT
                )
                max_joint = max(max_joint, float(np.linalg.norm(joint - reference_joint)))
                max_information = max(
                    max_information,
                    abs(_mutual_information(joint) - reference_information),
                )
                wrong, *_ = continuation_record_joint_distribution(
                    continuation,
                    clock,
                    index,
                    CURRENT_EVENT,
                    wrong_target=True,
                )
                max_wrong_target_information = max(
                    max_wrong_target_information,
                    _mutual_information(wrong),
                )

                if clock in ("B", "C"):
                    metric = continuation_support_metric(
                        continuation, clock, index
                    )
                    max_bare_self_adjoint = max(
                        max_bare_self_adjoint,
                        _metric_self_adjoint_residual(bare_target, metric),
                        _metric_self_adjoint_residual(bare_memory, metric),
                    )

    return (
        max_joint,
        max_information,
        max_wrong_target_information,
        max_bare_self_adjoint,
    )


def _first_schedule_difference_event(
    left: QuantumContinuation,
    right: QuantumContinuation,
    *,
    atol: float = DEFAULT_ATOL,
) -> int:
    for event, (left_operator, right_operator) in enumerate(
        zip(
            continuation_schedule_rest_operators(left),
            continuation_schedule_rest_operators(right),
            strict=True,
        )
    ):
        if np.linalg.norm(left_operator - right_operator) > atol:
            return event
    return -1


def _transported_weight_mismatch_residual() -> float:
    epistemic, _ = canonical_stage8b_models(selected_id="h_L")
    mismatch = make_ontic_quantum_extension_model(
        epistemic.carrier, (0.75, 0.25)
    )
    residuals = []
    for clock in ("B", "C"):
        for index in range(3):
            baseline = perspective_modal_view(epistemic, clock, index)
            changed = perspective_modal_view(mismatch, clock, index)
            residuals.append(
                float(
                    np.linalg.norm(
                        np.asarray(baseline.predictive_density, dtype=np.complex128)
                        - np.asarray(changed.predictive_density, dtype=np.complex128)
                    )
                )
            )
    return max(residuals)


def stage8e_compatibility_diagnostics(
    *,
    atol: float = DEFAULT_ATOL,
) -> Stage8ECompatibilityDiagnostics:
    epistemic, ontic = canonical_stage8b_models(selected_id="h_L")
    carrier = epistemic.carrier
    continuations = carrier.continuations
    left = canonical_continuation_left()
    right = canonical_continuation_right()

    (
        max_event_operator,
        max_event_probability,
        max_event_completeness,
        max_event_self_adjoint,
    ) = _event_effect_diagnostics(continuations)
    p_o = bool(
        max_event_operator <= atol
        and max_event_probability <= atol
        and max_event_completeness <= atol
        and max_event_self_adjoint <= atol
    )

    (
        max_record_joint,
        max_record_information,
        max_wrong_target_information,
        bare_record_self_adjoint,
    ) = _record_covariance_diagnostics(continuations)
    p_r = bool(
        max_record_joint <= atol
        and max_record_information <= atol
        and max_wrong_target_information <= atol
        and bare_record_self_adjoint > atol
    )

    stage8d = stage8d_transport_diagnostics(atol=atol)
    stage8a = stage8a_substrate_diagnostics(atol=atol)

    first_difference = _first_schedule_difference_event(left, right, atol=atol)
    invalid = QuantumContinuation(
        continuation_id="invalid-current-prefix-stage8e",
        future_action="identity",
        current_action="identity",
    )
    invalid_rejected = not assess_continuation_admissibility(invalid, atol=atol).admissible
    terminal_empty = len(quantum_extension_set(UPPER_EVENT)) == 0

    left_current_joint, *_ = continuation_record_joint_distribution(
        left, "A", CURRENT_EVENT, CURRENT_EVENT
    )
    right_current_joint, *_ = continuation_record_joint_distribution(
        right, "A", CURRENT_EVENT, CURRENT_EVENT
    )
    current_class_joint_residual = float(
        np.linalg.norm(left_current_joint - right_current_joint)
    )
    current_record_shared = bool(
        current_class_joint_residual <= atol
        and _mutual_information(left_current_joint) > atol
        and _mutual_information(right_current_joint) > atol
    )

    left_profile = continuation_record_profile(left)
    right_profile = continuation_record_profile(right)
    baseline_direction_absent = bool(
        left_profile.current_record_present
        and right_profile.current_record_present
        and not left_profile.directional_record_defined
        and not right_profile.directional_record_defined
    )

    scramble_assessment = assess_relational_record("forward")
    scramble_current = reduced_history_state(
        canonical_physical_history_state("forward"),
        "forward",
        CURRENT_EVENT,
    )
    left_current = reduced_continuation_state(left, CURRENT_EVENT)
    scramble_current_residual = float(np.linalg.norm(scramble_current - left_current))
    scramble_direction_present = bool(
        scramble_assessment.record_defined
        and scramble_assessment.orientation != "none"
        and abs(scramble_assessment.record_score) > atol
    )
    order_does_not_force_direction = bool(
        baseline_direction_absent
        and scramble_direction_present
        and scramble_current_residual <= atol
    )

    privileged_distinct = bool(
        privileged_quantum_modal_diagnostic(epistemic)
        != privileged_quantum_modal_diagnostic(ontic)
    )
    same_por_distinct_v = bool(
        epistemic.carrier is ontic.carrier
        and p_o
        and p_r
        and stage8d.class_weight_pv_covariance
        and stage8d.matched_modal_views_all_nodes
        and privileged_distinct
    )
    weight_mismatch = _transported_weight_mismatch_residual()

    full_directional = bool(
        same_por_distinct_v
        and not baseline_direction_absent
        and stage8d.full_stage8c_measurement_covariance_established
    )

    return Stage8ECompatibilityDiagnostics(
        p_o_event_effect_covariance=p_o,
        max_p_o_operator_transport_residual=max_event_operator,
        max_p_o_probability_residual=max_event_probability,
        max_event_effect_completeness_residual=max_event_completeness,
        max_event_effect_metric_self_adjoint_residual=max_event_self_adjoint,
        p_r_current_record_covariance=p_r,
        max_current_record_joint_residual=max_record_joint,
        max_current_record_information_residual=max_record_information,
        max_wrong_target_information=max_wrong_target_information,
        bare_record_metric_self_adjoint_residual=bare_record_self_adjoint,
        bare_record_observable_rejected=bare_record_self_adjoint > atol,
        p_v_class_weight_covariance=stage8d.class_weight_pv_covariance,
        o_v_first_difference_event=first_difference,
        o_v_difference_after_current_anchor=first_difference > CURRENT_EVENT,
        o_v_invalid_current_prefix_rejected=invalid_rejected,
        o_v_terminal_qext_empty=terminal_empty,
        current_record_shared_across_v_classes=current_record_shared,
        current_record_class_joint_residual=current_class_joint_residual,
        distinct_v_classes_with_same_current_record=bool(
            current_record_shared and stage8a.physically_inequivalent
        ),
        baseline_left_record_score=left_profile.record_score,
        baseline_right_record_score=right_profile.record_score,
        baseline_directional_r_absent=baseline_direction_absent,
        record_scramble_control_current_state_residual=scramble_current_residual,
        record_scramble_control_record_score=scramble_assessment.record_score,
        record_scramble_control_directional_r_present=scramble_direction_present,
        order_does_not_force_directional_r=order_does_not_force_direction,
        same_por_carrier_distinct_v_semantics=same_por_distinct_v,
        matched_public_modal_views_all_nodes=stage8d.matched_modal_views_all_nodes,
        privileged_modal_structures_distinct=privileged_distinct,
        transported_weight_mismatch_density_residual=weight_mismatch,
        weight_mismatch_control_detected=weight_mismatch > atol,
        full_stage8c_measurement_covariance_established=(
            stage8d.full_stage8c_measurement_covariance_established
        ),
        full_directional_porv_integration_established=full_directional,
    )


def stage8e_compatibility_matrix(
    *,
    atol: float = DEFAULT_ATOL,
) -> tuple[CompatibilityEntry, ...]:
    d = stage8e_compatibility_diagnostics(atol=atol)
    o_v = bool(
        d.o_v_difference_after_current_anchor
        and d.o_v_invalid_current_prefix_rejected
        and d.o_v_terminal_qext_empty
    )
    return (
        CompatibilityEntry(
            "P-O(event effects)",
            "compatible" if d.p_o_event_effect_covariance else "not_established",
            "ordered A-event effect family is transported covariantly through continuation-specific clock atlases",
        ),
        CompatibilityEntry(
            "P-R(current record)",
            "compatible" if d.p_r_current_record_covariance else "not_established",
            "target-memory statistics agree only with corresponding observable transport; bare local reuse is rejected",
        ),
        CompatibilityEntry(
            "P-V(class/weights)",
            "compatible" if d.p_v_class_weight_covariance else "not_established",
            "Stage 8D continuation-class and weight covariance",
        ),
        CompatibilityEntry(
            "O-V(extension)",
            "compatible" if o_v else "not_established",
            "canonical V alternatives share the frozen prefix and first differ only after current e1",
        ),
        CompatibilityEntry(
            "R(current)-V",
            (
                "underdetermined"
                if d.distinct_v_classes_with_same_current_record
                else "not_established"
            ),
            "physically inequivalent V classes share the same target-specific current record",
        ),
        CompatibilityEntry(
            "O=>R(direction)",
            (
                "implication_refuted"
                if d.order_does_not_force_directional_r
                else "not_established"
            ),
            "same e0<e1<e2 skeleton/current state supports zero-direction baseline and directional scramble control",
        ),
        CompatibilityEntry(
            "P/O/current-R=>V semantics",
            (
                "underdetermined"
                if d.same_por_carrier_distinct_v_semantics
                else "not_established"
            ),
            "same physical carrier/public P-O-R data hosts selected-h* and no-selected-continuation semantics",
        ),
        CompatibilityEntry(
            "full P/O/directional-R/V",
            (
                "compatible"
                if d.full_directional_porv_integration_established
                else "partial"
            ),
            "directional R is absent in canonical h_L/h_R and full Stage 8C measurement covariance remains not_established",
        ),
    )


def stage8e_summary() -> dict[str, object]:
    diagnostics = stage8e_compatibility_diagnostics()
    return {
        "stage": "8E",
        "diagnostics": asdict(diagnostics),
        "compatibility_matrix": [
            asdict(entry) for entry in stage8e_compatibility_matrix()
        ],
        "current_execution_criteria": {
            "36": "P-O event-effect covariance in continuation-aware physical-clock atlases",
            "37": "P-R current target-specific record covariance with wrong-target and bare-observable controls",
            "38": "O-V future-only extension compatibility with prefix and terminal controls",
            "39": "R(current)-V underdetermination across physically inequivalent continuation classes",
            "40": "O does not force directional R: canonical zero-direction baseline versus record-scramble contrast",
            "41": "same P/O/current-R carrier supports distinct V semantics while stronger directional/full-measurement integration remains explicit",
        },
        "guards": [
            "event-effect covariance != temporal succession",
            "current record covariance != directional record arrow",
            "record content != unique future continuation",
            "order != directional record arrow",
            "R-V compatibility != R=V",
            "O-V compatibility != O=V",
            "P-V covariance != P=V",
            "same P/O/current-R public data != modal identity",
            "directional R absent in canonical Stage 8 V carrier != universal R-V incompatibility",
            "full Stage 8C measurement covariance not established != false class-level P-V covariance",
            "not_established != false",
        ],
        "next": "Stage 8F — ablation / reconstruction / mismatch matrix",
    }
