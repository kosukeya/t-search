"""Stage 8D genuine clock-change transport for quantum Potentiality.

Stage 8A continuations define different modified constraints.  Consequently a
single Stage 7D/Stage 5 clock-change matrix must not be reused for every member
of QExt.  Stage 8D re-derives the perspective support, induced metric, and
clock-change map separately for each physical continuation h:

    C_{h,X,j} = coordinates of D_X(j) B_h,
    G_{h,X,j} = C^{-dagger} C^{-1},
    S^h_{Y,k<-X,j} = C_{h,Y,k} C_{h,X,j}^{-1}.

The modal carrier is then transported by an explicit correspondence between
continuation equivalence classes and an explicit relational-event
correspondence.  The canonical positive correspondence preserves e1 and maps
h_L->h_L and h_R->h_R.  Controls deliberately swap continuation classes or
misdeclare terminal e2 as the current event.

This module distinguishes three claims:

1. continuation-level physical perspective covariance;
2. class/weight covariance of the represented Potentiality carrier;
3. transport of the full Stage 8C cross-continuation measurement interface.

The first two are executable Stage 8D targets.  The third is not inferred merely
because the first two work: the canonical continuations generally require
different re-derived perspective maps, so a single h-independent transport of
the Stage 8C A/e2 future-signature measurement needs an additional declared
construction.

P-V covariance in this finite modal atlas does not imply P=V and does not imply
that the represented continuations are ontically real futures.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from itertools import permutations, product
from typing import Literal, Sequence

import numpy as np

from .stage5_clock_change import DEFAULT_ATOL, SUBSYSTEMS
from .stage7_history import CURRENT_EVENT, UPPER_EVENT
from .stage8_continuations import (
    QuantumContinuation,
    canonical_continuation_left,
    canonical_continuation_physical_state,
    canonical_continuation_right,
    continuation_clock_reduction_matrix,
    continuation_clock_reduction_operator,
    continuation_equivalent,
    quantum_extension_set,
)
from .stage8_modal import (
    EpistemicQuantumModel,
    OnticQuantumExtensionModel,
    QuantumContinuationCarrier,
    canonical_stage8b_models,
    continuation_by_id,
    make_epistemic_quantum_model,
    make_ontic_quantum_extension_model,
    matched_uniform_weights,
)

ModalChiKind = Literal[
    "preserving",
    "swapped-classes",
    "misdeclared-terminal-preserving",
]
Stage8DModel = EpistemicQuantumModel | OnticQuantumExtensionModel


@dataclass(frozen=True, slots=True)
class ModalEventCorrespondence:
    name: ModalChiKind
    source_current_event: int
    target_current_event: int
    declared_orientation: str
    class_map: tuple[tuple[str, str], ...]


@dataclass(frozen=True, slots=True)
class ModalCorrespondenceAudit:
    bijective: bool
    current_event_preserved: bool
    physical_classes_preserved: bool
    source_qext_size: int
    target_qext_size: int
    valid: bool


@dataclass(frozen=True, slots=True)
class PerspectiveModalView:
    """Model-neutral local representation of a transported modal carrier.

    ``current_event`` and ``clock_index`` are intentionally separate fields:
    equal numeric clock readings are not used as event identity.  The view does
    not expose h*, selected-history data, or a model-type label.
    """

    current_event: int
    clock: str
    clock_index: int
    continuation_ids: tuple[str, ...]
    continuation_weights: tuple[float, ...]
    predictive_density: tuple[complex, ...]


@dataclass(frozen=True, slots=True)
class Stage8DTransportDiagnostics:
    qext_size: int
    perspective_nodes_per_continuation: int
    distinct_clock_state_transports: int
    three_clock_compositions: int
    max_state_transport_residual: float
    max_inverse_residual: float
    max_metric_covariance_residual: float
    max_composition_residual: float
    max_weight_transport_residual: float
    correct_chi_bijective: bool
    correct_chi_physical_classes_preserved: bool
    matched_modal_views_all_nodes: bool
    selected_swap_modal_views_all_nodes: bool
    hidden_selected_absent_from_modal_view_schema: bool
    wrong_class_correspondence_rejected: bool
    terminal_current_correspondence_rejected: bool
    wrong_continuation_map_residual: float
    wrong_continuation_map_rejected: bool
    max_cross_continuation_map_difference: float
    one_rederived_map_suffices_for_all_continuations: bool
    a_e1_shared_current_density_residual: float
    min_non_a_same_reading_density_residual: float
    max_non_a_same_reading_density_residual: float
    continuation_level_pv_covariance: bool
    class_weight_pv_covariance: bool
    full_stage8c_measurement_covariance_established: bool


def _validate_clock(clock: str) -> str:
    if clock not in SUBSYSTEMS:
        raise ValueError("clock must be one of A, B, or C")
    return clock


def _validate_index(index: int) -> int:
    if isinstance(index, bool) or not isinstance(index, int) or index not in (0, 1, 2):
        raise ValueError("clock index must be 0, 1, or 2")
    return index


def continuation_clock_support_qr(
    continuation: QuantumContinuation,
    clock: str,
    index: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Re-derive one continuation-specific reduced support and coordinates."""

    _validate_clock(clock)
    _validate_index(index)
    reduction = continuation_clock_reduction_matrix(continuation, clock, index)
    q, r = np.linalg.qr(reduction, mode="reduced")
    if reduction.shape != (18, 14) or np.linalg.matrix_rank(r, tol=DEFAULT_ATOL) != 14:
        raise ValueError("continuation clock reading is not an injective perspective")
    return q, r


def continuation_clock_support_basis(
    continuation: QuantumContinuation,
    clock: str,
    index: int,
) -> np.ndarray:
    return continuation_clock_support_qr(continuation, clock, index)[0]


def continuation_clock_coordinates(
    continuation: QuantumContinuation,
    clock: str,
    index: int,
) -> np.ndarray:
    return continuation_clock_support_qr(continuation, clock, index)[1]


def continuation_support_metric(
    continuation: QuantumContinuation,
    clock: str,
    index: int,
) -> np.ndarray:
    coordinates = continuation_clock_coordinates(continuation, clock, index)
    inverse = np.linalg.inv(coordinates)
    return inverse.conj().T @ inverse


def continuation_clock_change_support_matrix(
    continuation: QuantumContinuation,
    target_clock: str,
    target_index: int,
    source_clock: str,
    source_index: int,
) -> np.ndarray:
    """Return S^h_{Y<-X}=C_{h,Y} C_{h,X}^{-1}."""

    _validate_clock(source_clock)
    _validate_clock(target_clock)
    _validate_index(source_index)
    _validate_index(target_index)
    if source_clock == target_clock:
        raise ValueError("Stage 8D genuine clock change requires distinct clocks")
    source = continuation_clock_coordinates(continuation, source_clock, source_index)
    target = continuation_clock_coordinates(continuation, target_clock, target_index)
    return target @ np.linalg.inv(source)


def continuation_reduced_support_coordinates(
    continuation: QuantumContinuation,
    clock: str,
    index: int,
) -> np.ndarray:
    """Reduce the canonical global continuation state into one local support chart."""

    physical = canonical_continuation_physical_state(continuation)
    support = continuation_clock_support_basis(continuation, clock, index)
    reduced = continuation_clock_reduction_operator(clock, index) @ physical
    return support.conj().T @ reduced


def continuation_reduced_ambient_state(
    continuation: QuantumContinuation,
    clock: str,
    index: int,
) -> np.ndarray:
    physical = canonical_continuation_physical_state(continuation)
    return continuation_clock_reduction_operator(clock, index) @ physical


def _normalized_density(state: np.ndarray) -> np.ndarray:
    vector = np.asarray(state, dtype=np.complex128)
    norm = float(np.linalg.norm(vector))
    if norm <= DEFAULT_ATOL:
        raise ValueError("reduced continuation state has zero norm")
    vector = vector / norm
    return np.outer(vector, vector.conj())


def _model_weights(model: Stage8DModel) -> tuple[float, ...]:
    if isinstance(model, EpistemicQuantumModel):
        return model.belief_weights
    if isinstance(model, OnticQuantumExtensionModel):
        return model.extension_weights
    raise TypeError("unsupported Stage 8D model type")


def modal_event_correspondence(
    carrier: QuantumContinuationCarrier,
    kind: ModalChiKind = "preserving",
) -> ModalEventCorrespondence:
    ids = tuple(item.continuation_id for item in carrier.continuations)
    if kind == "preserving":
        mapping = tuple((item, item) for item in ids)
        return ModalEventCorrespondence(
            name=kind,
            source_current_event=carrier.current_anchor,
            target_current_event=carrier.current_anchor,
            declared_orientation="preserving",
            class_map=mapping,
        )
    if kind == "swapped-classes":
        if len(ids) != 2:
            raise ValueError("canonical swapped-class control requires exactly two QExt classes")
        return ModalEventCorrespondence(
            name=kind,
            source_current_event=carrier.current_anchor,
            target_current_event=carrier.current_anchor,
            declared_orientation="preserving",
            class_map=((ids[0], ids[1]), (ids[1], ids[0])),
        )
    if kind == "misdeclared-terminal-preserving":
        mapping = tuple((item, item) for item in ids)
        return ModalEventCorrespondence(
            name=kind,
            source_current_event=carrier.current_anchor,
            target_current_event=UPPER_EVENT,
            declared_orientation="preserving",
            class_map=mapping,
        )
    raise ValueError("unknown Stage 8D modal correspondence kind")


def audit_modal_correspondence(
    carrier: QuantumContinuationCarrier,
    correspondence: ModalEventCorrespondence,
    *,
    atol: float = DEFAULT_ATOL,
) -> ModalCorrespondenceAudit:
    source = carrier.continuations
    source_ids = tuple(item.continuation_id for item in source)
    mapped_sources = tuple(pair[0] for pair in correspondence.class_map)
    mapped_targets = tuple(pair[1] for pair in correspondence.class_map)
    bijective = bool(
        len(mapped_sources) == len(source_ids)
        and set(mapped_sources) == set(source_ids)
        and len(set(mapped_targets)) == len(mapped_targets)
    )

    try:
        target_qext = quantum_extension_set(correspondence.target_current_event)
    except ValueError:
        target_qext = ()
    target_ids = tuple(item.continuation_id for item in target_qext)
    current_preserved = correspondence.target_current_event == carrier.current_anchor

    physical_classes_preserved = False
    if bijective and current_preserved and set(mapped_targets) == set(target_ids):
        physical_classes_preserved = all(
            continuation_equivalent(
                continuation_by_id(carrier, source_id),
                next(item for item in target_qext if item.continuation_id == target_id),
                atol=atol,
            )
            for source_id, target_id in correspondence.class_map
        )

    valid = bool(bijective and current_preserved and physical_classes_preserved)
    return ModalCorrespondenceAudit(
        bijective=bijective,
        current_event_preserved=current_preserved,
        physical_classes_preserved=physical_classes_preserved,
        source_qext_size=len(source),
        target_qext_size=len(target_qext),
        valid=valid,
    )


def perspective_modal_view(
    model: Stage8DModel,
    clock: str,
    index: int,
    *,
    correspondence: ModalEventCorrespondence | None = None,
    atol: float = DEFAULT_ATOL,
) -> PerspectiveModalView:
    """Represent the same modal carrier in one genuine physical-clock chart.

    The predictive density is the model's uncertainty/extension-weighted mixture
    of continuation-specific conditional states.  The hidden epistemic h* is not
    consulted.  Numerical q_E/K equality does not identify their semantics.
    """

    _validate_clock(clock)
    _validate_index(index)
    chi = correspondence or modal_event_correspondence(model.carrier, "preserving")
    audit = audit_modal_correspondence(model.carrier, chi, atol=atol)
    if not audit.valid:
        raise ValueError("modal correspondence does not preserve current QExt physical classes")

    weights = _model_weights(model)
    density = np.zeros((18, 18), dtype=np.complex128)
    for weight, continuation in zip(weights, model.carrier.continuations, strict=True):
        density += float(weight) * _normalized_density(
            continuation_reduced_ambient_state(continuation, clock, index)
        )
    density = density / np.trace(density)
    return PerspectiveModalView(
        current_event=chi.target_current_event,
        clock=clock,
        clock_index=index,
        continuation_ids=tuple(target for _, target in chi.class_map),
        continuation_weights=tuple(float(value) for value in weights),
        predictive_density=tuple(complex(value) for value in density.reshape(-1)),
    )


def _views_close(
    left: PerspectiveModalView,
    right: PerspectiveModalView,
    *,
    atol: float = DEFAULT_ATOL,
) -> bool:
    if (
        left.current_event != right.current_event
        or left.clock != right.clock
        or left.clock_index != right.clock_index
        or left.continuation_ids != right.continuation_ids
        or len(left.continuation_weights) != len(right.continuation_weights)
    ):
        return False
    return bool(
        np.allclose(left.continuation_weights, right.continuation_weights, atol=atol, rtol=0.0)
        and np.allclose(left.predictive_density, right.predictive_density, atol=atol, rtol=0.0)
    )


def continuation_family_density_residual(clock: str, index: int) -> float:
    """Phase-invariant difference between h_L/h_R local conditional pure states."""

    left = _normalized_density(
        continuation_reduced_ambient_state(canonical_continuation_left(), clock, index)
    )
    right = _normalized_density(
        continuation_reduced_ambient_state(canonical_continuation_right(), clock, index)
    )
    return float(np.linalg.norm(left - right))


def _wrong_continuation_map_residual(*, atol: float = DEFAULT_ATOL) -> float:
    """Use h_L's re-derived map on h_R and measure failure against h_R target state."""

    left = canonical_continuation_left()
    right = canonical_continuation_right()
    residuals: list[float] = []
    for target_clock in ("B", "C"):
        for source_index, target_index in product(range(3), repeat=2):
            wrong_map = continuation_clock_change_support_matrix(
                left, target_clock, target_index, "A", source_index
            )
            source = continuation_reduced_support_coordinates(right, "A", source_index)
            target = continuation_reduced_support_coordinates(right, target_clock, target_index)
            residuals.append(float(np.linalg.norm(wrong_map @ source - target)))
    value = max(residuals)
    if value <= atol:
        return 0.0
    return value


def stage8d_transport_diagnostics(
    *,
    atol: float = DEFAULT_ATOL,
) -> Stage8DTransportDiagnostics:
    epistemic, ontic = canonical_stage8b_models(selected_id="h_L")
    carrier = epistemic.carrier
    continuations = carrier.continuations

    max_state = 0.0
    max_inverse = 0.0
    max_metric = 0.0
    state_comparisons = 0
    map_differences: list[float] = []

    for continuation in continuations:
        for source_clock, target_clock in permutations(SUBSYSTEMS, 2):
            for source_index, target_index in product(range(3), repeat=2):
                transform = continuation_clock_change_support_matrix(
                    continuation,
                    target_clock,
                    target_index,
                    source_clock,
                    source_index,
                )
                inverse = continuation_clock_change_support_matrix(
                    continuation,
                    source_clock,
                    source_index,
                    target_clock,
                    target_index,
                )
                source_state = continuation_reduced_support_coordinates(
                    continuation, source_clock, source_index
                )
                target_state = continuation_reduced_support_coordinates(
                    continuation, target_clock, target_index
                )
                source_metric = continuation_support_metric(
                    continuation, source_clock, source_index
                )
                target_metric = continuation_support_metric(
                    continuation, target_clock, target_index
                )
                max_state = max(max_state, float(np.linalg.norm(transform @ source_state - target_state)))
                max_inverse = max(
                    max_inverse,
                    float(np.linalg.norm(inverse @ transform - np.eye(14, dtype=np.complex128))),
                )
                max_metric = max(
                    max_metric,
                    float(np.linalg.norm(transform.conj().T @ target_metric @ transform - source_metric)),
                )
                state_comparisons += 1

    # Measure whether the two continuation-specific atlases actually coincide.
    left, right = continuations
    for source_clock, target_clock in permutations(SUBSYSTEMS, 2):
        for source_index, target_index in product(range(3), repeat=2):
            left_map = continuation_clock_change_support_matrix(
                left, target_clock, target_index, source_clock, source_index
            )
            right_map = continuation_clock_change_support_matrix(
                right, target_clock, target_index, source_clock, source_index
            )
            map_differences.append(float(np.linalg.norm(left_map - right_map)))

    max_composition = 0.0
    composition_count = 0
    for continuation in continuations:
        for source_clock, middle_clock, target_clock in permutations(SUBSYSTEMS, 3):
            for source_index, middle_index, target_index in product(range(3), repeat=3):
                first = continuation_clock_change_support_matrix(
                    continuation,
                    middle_clock,
                    middle_index,
                    source_clock,
                    source_index,
                )
                second = continuation_clock_change_support_matrix(
                    continuation,
                    target_clock,
                    target_index,
                    middle_clock,
                    middle_index,
                )
                direct = continuation_clock_change_support_matrix(
                    continuation,
                    target_clock,
                    target_index,
                    source_clock,
                    source_index,
                )
                max_composition = max(
                    max_composition,
                    float(np.linalg.norm(second @ first - direct)),
                )
                composition_count += 1

    preserving = modal_event_correspondence(carrier, "preserving")
    preserving_audit = audit_modal_correspondence(carrier, preserving, atol=atol)
    wrong_class = audit_modal_correspondence(
        carrier, modal_event_correspondence(carrier, "swapped-classes"), atol=atol
    )
    terminal = audit_modal_correspondence(
        carrier,
        modal_event_correspondence(carrier, "misdeclared-terminal-preserving"),
        atol=atol,
    )

    weights = matched_uniform_weights(carrier)
    swapped_epistemic = make_epistemic_quantum_model(
        carrier, continuation_by_id(carrier, "h_R"), weights, atol=atol
    )
    matched_all = True
    selected_swap_all = True
    max_weight_residual = 0.0
    for clock in SUBSYSTEMS:
        for index in range(3):
            e_view = perspective_modal_view(epistemic, clock, index, correspondence=preserving, atol=atol)
            o_view = perspective_modal_view(ontic, clock, index, correspondence=preserving, atol=atol)
            s_view = perspective_modal_view(
                swapped_epistemic, clock, index, correspondence=preserving, atol=atol
            )
            matched_all = matched_all and _views_close(e_view, o_view, atol=atol)
            selected_swap_all = selected_swap_all and _views_close(e_view, s_view, atol=atol)
            max_weight_residual = max(
                max_weight_residual,
                max(
                    abs(a - b)
                    for a, b in zip(
                        e_view.continuation_weights,
                        o_view.continuation_weights,
                        strict=True,
                    )
                ),
            )

    schema = {field.name for field in fields(PerspectiveModalView)}
    hidden_absent = bool(
        "selected_continuation" not in schema
        and "selected_history" not in schema
        and "selector" not in schema
        and "model_type" not in schema
    )

    wrong_map = _wrong_continuation_map_residual(atol=atol)
    a_current = continuation_family_density_residual("A", CURRENT_EVENT)
    non_a = [
        continuation_family_density_residual(clock, index)
        for clock in ("B", "C")
        for index in range(3)
    ]
    max_map_difference = max(map_differences)
    one_map = max_map_difference <= atol

    continuation_covariance = bool(
        state_comparisons == 108
        and max_state <= atol
        and max_inverse <= atol
        and max_metric <= atol
        and composition_count == 324
        and max_composition <= atol
    )
    class_weight_covariance = bool(
        preserving_audit.valid
        and max_weight_residual <= atol
        and matched_all
        and selected_swap_all
    )

    # A single transported Stage 8C measurement would require an explicitly
    # declared h-independent measurement/map construction.  The current
    # re-derived atlas provides no such construction when the h-specific maps
    # differ, so this claim is computed as established only in the degenerate
    # case where both atlases coincide.
    full_measurement_covariance = bool(
        continuation_covariance and class_weight_covariance and one_map
    )

    return Stage8DTransportDiagnostics(
        qext_size=len(continuations),
        perspective_nodes_per_continuation=9,
        distinct_clock_state_transports=state_comparisons,
        three_clock_compositions=composition_count,
        max_state_transport_residual=max_state,
        max_inverse_residual=max_inverse,
        max_metric_covariance_residual=max_metric,
        max_composition_residual=max_composition,
        max_weight_transport_residual=max_weight_residual,
        correct_chi_bijective=preserving_audit.bijective,
        correct_chi_physical_classes_preserved=preserving_audit.physical_classes_preserved,
        matched_modal_views_all_nodes=matched_all,
        selected_swap_modal_views_all_nodes=selected_swap_all,
        hidden_selected_absent_from_modal_view_schema=hidden_absent,
        wrong_class_correspondence_rejected=not wrong_class.valid,
        terminal_current_correspondence_rejected=not terminal.valid,
        wrong_continuation_map_residual=wrong_map,
        wrong_continuation_map_rejected=wrong_map > atol,
        max_cross_continuation_map_difference=max_map_difference,
        one_rederived_map_suffices_for_all_continuations=one_map,
        a_e1_shared_current_density_residual=a_current,
        min_non_a_same_reading_density_residual=min(non_a),
        max_non_a_same_reading_density_residual=max(non_a),
        continuation_level_pv_covariance=continuation_covariance,
        class_weight_pv_covariance=class_weight_covariance,
        full_stage8c_measurement_covariance_established=full_measurement_covariance,
    )


def stage8d_summary() -> dict[str, object]:
    diagnostics = stage8d_transport_diagnostics()
    return {
        "stage": "8D",
        "transport": "continuation-aware P-V atlas",
        "diagnostics": asdict(diagnostics),
        "current_execution_criteria": {
            "30": "continuation-specific full-rank perspective supports and induced metrics",
            "31": "state/inverse/metric/composition covariance for re-derived genuine clock changes",
            "32": "explicit QExt class/event correspondence and weight preservation",
            "33": "matched typed modal views and h* swap remain public-transport invariant",
            "34": "wrong class/event/continuation-map controls are rejected",
            "35": "full Stage 8C measurement covariance is reported separately and not inferred from class transport",
        },
        "guards": [
            "equal numeric clock readings != event identity",
            "continuation-aware P-V transport != one universal h-independent linear map",
            "branch-specific perspective map != hidden branch selection",
            "P-V covariance != P=V",
            "QExt represented != ontically real futures by definition",
            "matched transported modal views != matched probability semantics",
            "full Stage 8C measurement covariance not established != false P-V class transport",
        ],
        "next": "Stage 8E — P/O/R/V compatibility and underdetermination",
    }
