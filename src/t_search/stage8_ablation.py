"""Stage 8F ablation / reconstruction / mismatch matrix.

Stage 8A--E placed executable quantum continuations, selected-vs-unselected
modal semantics, weighted operational predictions, genuine clock changes,
order/event structure, and current target-specific records into one finite
constrained model family.  Stage 8F neutralizes those ingredients one at a time
and classifies the represented *roles* that remain.

The status vocabulary is functional, not metaphysical:

- preserved: the role remains directly represented;
- reconstructible: the explicit ingredient is removed but an executable witness
  rebuilds the role from retained declared structure;
- inaccessible: the global role remains represented but the declared local
  interface cannot access it;
- lost: the represented role is deliberately removed and no retained direct
  representation remains;
- underdetermined: retained structure admits more than one incompatible value or
  semantic completion, so no unique reconstruction is licensed;
- not_established: the retained typing is insufficient to decide the role.

``lost`` does not mean metaphysically irreducible, ``reconstructible`` does not
mean universally redundant, and ``underdetermined`` does not prove ontological
openness.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from functools import lru_cache
from itertools import permutations, product
from typing import Any

import numpy as np

from .stage5_clock_change import DEFAULT_ATOL, SUBSYSTEMS
from .stage7_history import CURRENT_EVENT, UPPER_EVENT
from .stage8_compatibility import (
    continuation_record_profile,
    stage8e_compatibility_diagnostics,
)
from .stage8_continuations import (
    QuantumContinuation,
    canonical_continuation_left,
    canonical_continuation_right,
    continuation_clock_reduction_matrix,
    continuation_constraint_residual,
    continuation_current_record_information,
    continuation_equivalent,
    continuation_physical_basis,
    reduced_continuation_state,
)
from .stage8_modal import (
    QuantumContinuationCarrier,
    canonical_stage8b_models,
    make_epistemic_quantum_model,
    make_ontic_quantum_extension_model,
    make_quantum_continuation_carrier,
    ontic_selector_audit,
)
from .stage8_modal_transport import (
    continuation_clock_change_support_matrix,
    continuation_clock_coordinates,
    continuation_reduced_support_coordinates,
    continuation_support_metric,
    stage8d_transport_diagnostics,
)
from .stage8_operational import (
    compare_quantum_operational_views,
    privileged_quantum_modal_diagnostic,
    quantum_operational_view,
)

ROLE_IDS: tuple[str, ...] = (
    "V_physical_multiplicity",
    "V_selected_vs_unselected_semantics",
    "V_weights",
    "P_V_class_transport",
    "O_V_extension_relation",
    "current_record_content",
    "local_record_access",
)

ABLATION_IDS: tuple[str, ...] = (
    "record_coupling_neutralized",
    "qext_collapsed_singleton",
    "modal_semantics_removed",
    "weights_unfixed",
    "explicit_perspective_maps_removed",
    "event_correspondence_removed",
    "current_record_access_hidden",
)


class RoleStatus(str, Enum):
    PRESERVED = "preserved"
    RECONSTRUCTIBLE = "reconstructible"
    INACCESSIBLE = "inaccessible"
    LOST = "lost"
    UNDERDETERMINED = "underdetermined"
    NOT_ESTABLISHED = "not_established"


@dataclass(frozen=True, slots=True)
class RoleEvidence:
    role: str
    direct_available: bool = False
    reconstruction_available: bool = False
    globally_represented: bool | None = None
    locally_accessible: bool | None = None
    decisive_loss: bool = False
    underdetermined: bool = False
    measurements: tuple[tuple[str, Any], ...] = ()
    note: str = ""

    @property
    def status(self) -> RoleStatus:
        if self.direct_available:
            return RoleStatus.PRESERVED
        if self.reconstruction_available:
            return RoleStatus.RECONSTRUCTIBLE
        if self.globally_represented is True and self.locally_accessible is False:
            return RoleStatus.INACCESSIBLE
        if self.decisive_loss:
            return RoleStatus.LOST
        if self.underdetermined:
            return RoleStatus.UNDERDETERMINED
        return RoleStatus.NOT_ESTABLISHED

    def as_dict(self) -> dict[str, Any]:
        return {
            "role": self.role,
            "status": self.status.value,
            "direct_available": self.direct_available,
            "reconstruction_available": self.reconstruction_available,
            "globally_represented": self.globally_represented,
            "locally_accessible": self.locally_accessible,
            "decisive_loss": self.decisive_loss,
            "underdetermined": self.underdetermined,
            "measurements": dict(self.measurements),
            "note": self.note,
        }


@dataclass(frozen=True, slots=True)
class AblationCase:
    ingredient: str
    neutralization: str
    probes: tuple[RoleEvidence, ...]

    def __post_init__(self) -> None:
        if self.ingredient not in ABLATION_IDS:
            raise ValueError(f"unknown Stage 8F ablation: {self.ingredient!r}")
        if tuple(probe.role for probe in self.probes) != ROLE_IDS:
            raise ValueError("Stage 8F probes must follow the frozen role order")

    def status(self, role: str) -> RoleStatus:
        return next(probe.status for probe in self.probes if probe.role == role)

    def as_dict(self) -> dict[str, Any]:
        return {
            "ingredient": self.ingredient,
            "neutralization": self.neutralization,
            "probes": [probe.as_dict() for probe in self.probes],
        }


@dataclass(frozen=True, slots=True)
class NoRecordVFamilyDiagnostics:
    qext_size: int
    physical_dimension: int
    minimum_clock_reduction_rank: int
    max_constraint_residual: float
    common_current_state_residual: float
    future_overlap_squared: float
    future_state_distance: float
    physically_inequivalent: bool
    current_record_information_left: float
    current_record_information_right: float
    current_record_lost: bool
    matched_operational_views_equal: bool
    privileged_modal_structures_distinct: bool
    weight_mismatch_changes_prediction: bool
    distinct_clock_state_transports: int
    max_state_transport_residual: float
    max_inverse_residual: float
    max_metric_covariance_residual: float
    perspective_structure_preserved: bool


@dataclass(frozen=True, slots=True)
class PerspectiveMapReconstructionDiagnostics:
    comparisons: int
    max_reference_map_residual: float
    max_state_transport_residual: float
    max_inverse_residual: float
    max_metric_covariance_residual: float
    reconstructible: bool


@dataclass(frozen=True, slots=True)
class SingletonQExtDiagnostics:
    qext_size: int
    physical_multiplicity_lost: bool
    semantic_types_distinct: bool
    ontic_selector_absent: bool
    singleton_weight: float
    singleton_weight_reconstructible_from_normalization: bool
    current_record_information: float
    perspective_transport_preserved: bool
    future_extension_present: bool


@dataclass(frozen=True, slots=True)
class SemanticWeightReconstructionDiagnostics:
    same_carrier_distinct_modal_semantics: bool
    modal_semantics_reconstructible_from_public_por: bool
    uniform_weights: tuple[float, ...]
    alternative_weights: tuple[float, ...]
    same_carrier_admits_distinct_weights: bool
    prediction_density_residual: float
    prediction_changes_with_weights: bool
    weights_reconstructible_from_carrier: bool


@dataclass(frozen=True, slots=True)
class MismatchDiagnostic:
    mismatch: str
    affected_role: str
    detected: bool
    measurements: tuple[tuple[str, Any], ...]
    note: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "mismatch": self.mismatch,
            "affected_role": self.affected_role,
            "detected": self.detected,
            "measurements": dict(self.measurements),
            "note": self.note,
        }


def _normalized(vector: np.ndarray) -> np.ndarray:
    state = np.asarray(vector, dtype=np.complex128)
    norm = float(np.linalg.norm(state))
    if norm <= DEFAULT_ATOL:
        raise ValueError("state must have nonzero norm")
    return state / norm


def _preserved(role: str, measurements: tuple[tuple[str, Any], ...] = (), note: str = "") -> RoleEvidence:
    return RoleEvidence(
        role=role,
        direct_available=True,
        globally_represented=True,
        locally_accessible=True if role == "local_record_access" else None,
        measurements=measurements,
        note=note or "role remains directly represented after neutralization",
    )


def _reconstructible(role: str, measurements: tuple[tuple[str, Any], ...], note: str) -> RoleEvidence:
    return RoleEvidence(
        role=role,
        reconstruction_available=True,
        globally_represented=True,
        measurements=measurements,
        note=note,
    )


def _lost(role: str, measurements: tuple[tuple[str, Any], ...], note: str) -> RoleEvidence:
    return RoleEvidence(
        role=role,
        globally_represented=False,
        decisive_loss=True,
        measurements=measurements,
        note=note,
    )


def _inaccessible(role: str, measurements: tuple[tuple[str, Any], ...], note: str) -> RoleEvidence:
    return RoleEvidence(
        role=role,
        globally_represented=True,
        locally_accessible=False,
        measurements=measurements,
        note=note,
    )


def _underdetermined(role: str, measurements: tuple[tuple[str, Any], ...], note: str) -> RoleEvidence:
    return RoleEvidence(
        role=role,
        globally_represented=True,
        underdetermined=True,
        measurements=measurements,
        note=note,
    )


def _not_established(role: str, measurements: tuple[tuple[str, Any], ...], note: str) -> RoleEvidence:
    return RoleEvidence(role=role, measurements=measurements, note=note)


def _no_record_continuations() -> tuple[QuantumContinuation, QuantumContinuation]:
    return (
        QuantumContinuation("h_L^0", "identity", current_action="identity"),
        QuantumContinuation("h_R^0", "c-phase", current_action="identity"),
    )


def _direct_carrier(continuations: tuple[QuantumContinuation, ...]) -> QuantumContinuationCarrier:
    """Construct an ablation carrier without re-imposing canonical record-prefix validation."""

    return QuantumContinuationCarrier(
        current_anchor=CURRENT_EVENT,
        continuations=continuations,
    )


def _perspective_transport_diagnostics_for(
    continuations: tuple[QuantumContinuation, ...],
) -> tuple[int, float, float, float]:
    comparisons = 0
    max_state = 0.0
    max_inverse = 0.0
    max_metric = 0.0
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
                source = continuation_reduced_support_coordinates(
                    continuation, source_clock, source_index
                )
                target = continuation_reduced_support_coordinates(
                    continuation, target_clock, target_index
                )
                source_metric = continuation_support_metric(
                    continuation, source_clock, source_index
                )
                target_metric = continuation_support_metric(
                    continuation, target_clock, target_index
                )
                max_state = max(max_state, float(np.linalg.norm(transform @ source - target)))
                max_inverse = max(
                    max_inverse,
                    float(np.linalg.norm(inverse @ transform - np.eye(14, dtype=np.complex128))),
                )
                max_metric = max(
                    max_metric,
                    float(
                        np.linalg.norm(
                            transform.conj().T @ target_metric @ transform - source_metric
                        )
                    ),
                )
                comparisons += 1
    return comparisons, max_state, max_inverse, max_metric


@lru_cache(maxsize=1)
def no_record_v_family_diagnostics() -> NoRecordVFamilyDiagnostics:
    left, right = _no_record_continuations()
    continuations = (left, right)

    dimensions = tuple(continuation_physical_basis(item).shape[1] for item in continuations)
    ranks = tuple(
        int(
            np.linalg.matrix_rank(
                continuation_clock_reduction_matrix(item, clock, index),
                tol=DEFAULT_ATOL,
            )
        )
        for item in continuations
        for clock in SUBSYSTEMS
        for index in range(3)
    )
    constraints = tuple(continuation_constraint_residual(item) for item in continuations)

    left_current = reduced_continuation_state(left, CURRENT_EVENT)
    right_current = reduced_continuation_state(right, CURRENT_EVENT)
    left_future = _normalized(reduced_continuation_state(left, UPPER_EVENT))
    right_future = _normalized(reduced_continuation_state(right, UPPER_EVENT))
    overlap = float(abs(np.vdot(left_future, right_future)) ** 2)
    distance = float(np.linalg.norm(left_future - right_future))
    physically_inequivalent = bool(
        not continuation_equivalent(left, right)
        and overlap < 1.0 - 1e-9
        and distance > 1e-9
    )

    left_record = continuation_current_record_information(left)
    right_record = continuation_current_record_information(right)

    carrier = _direct_carrier(continuations)
    weights = (0.5, 0.5)
    epistemic = make_epistemic_quantum_model(carrier, left, weights)
    ontic = make_ontic_quantum_extension_model(carrier, weights)
    baseline_e = quantum_operational_view(epistemic)
    baseline_o = quantum_operational_view(ontic)
    matched = compare_quantum_operational_views(baseline_e, baseline_o).equal
    privileged_distinct = bool(
        privileged_quantum_modal_diagnostic(epistemic)
        != privileged_quantum_modal_diagnostic(ontic)
    )
    mismatched = make_ontic_quantum_extension_model(carrier, (0.75, 0.25))
    mismatch_view = quantum_operational_view(mismatched)
    weight_mismatch = not compare_quantum_operational_views(
        baseline_e, mismatch_view
    ).next_probabilities_equal

    comparisons, max_state, max_inverse, max_metric = _perspective_transport_diagnostics_for(
        continuations
    )
    perspective_preserved = bool(
        comparisons == 108
        and min(ranks) == 14
        and max_state <= 1e-9
        and max_inverse <= 1e-9
        and max_metric <= 1e-9
    )

    return NoRecordVFamilyDiagnostics(
        qext_size=2,
        physical_dimension=min(dimensions),
        minimum_clock_reduction_rank=min(ranks),
        max_constraint_residual=max(constraints),
        common_current_state_residual=float(np.linalg.norm(left_current - right_current)),
        future_overlap_squared=overlap,
        future_state_distance=distance,
        physically_inequivalent=physically_inequivalent,
        current_record_information_left=left_record,
        current_record_information_right=right_record,
        current_record_lost=bool(left_record <= 1e-9 and right_record <= 1e-9),
        matched_operational_views_equal=matched,
        privileged_modal_structures_distinct=privileged_distinct,
        weight_mismatch_changes_prediction=weight_mismatch,
        distinct_clock_state_transports=comparisons,
        max_state_transport_residual=max_state,
        max_inverse_residual=max_inverse,
        max_metric_covariance_residual=max_metric,
        perspective_structure_preserved=perspective_preserved,
    )


@lru_cache(maxsize=1)
def perspective_map_reconstruction_diagnostics() -> PerspectiveMapReconstructionDiagnostics:
    continuations = (canonical_continuation_left(), canonical_continuation_right())
    comparisons = 0
    max_reference = 0.0
    max_state = 0.0
    max_inverse = 0.0
    max_metric = 0.0

    for continuation in continuations:
        for source_clock, target_clock in permutations(SUBSYSTEMS, 2):
            for source_index, target_index in product(range(3), repeat=2):
                source_c = continuation_clock_coordinates(
                    continuation, source_clock, source_index
                )
                target_c = continuation_clock_coordinates(
                    continuation, target_clock, target_index
                )
                reconstructed = target_c @ np.linalg.inv(source_c)
                reverse = source_c @ np.linalg.inv(target_c)
                reference = continuation_clock_change_support_matrix(
                    continuation,
                    target_clock,
                    target_index,
                    source_clock,
                    source_index,
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
                max_reference = max(
                    max_reference, float(np.linalg.norm(reconstructed - reference))
                )
                max_state = max(
                    max_state,
                    float(np.linalg.norm(reconstructed @ source_state - target_state)),
                )
                max_inverse = max(
                    max_inverse,
                    float(np.linalg.norm(reverse @ reconstructed - np.eye(14))),
                )
                max_metric = max(
                    max_metric,
                    float(
                        np.linalg.norm(
                            reconstructed.conj().T @ target_metric @ reconstructed
                            - source_metric
                        )
                    ),
                )
                comparisons += 1

    reconstructible = bool(
        comparisons == 108
        and max_reference <= 1e-9
        and max_state <= 1e-9
        and max_inverse <= 1e-9
        and max_metric <= 1e-9
    )
    return PerspectiveMapReconstructionDiagnostics(
        comparisons=comparisons,
        max_reference_map_residual=max_reference,
        max_state_transport_residual=max_state,
        max_inverse_residual=max_inverse,
        max_metric_covariance_residual=max_metric,
        reconstructible=reconstructible,
    )


@lru_cache(maxsize=1)
def singleton_qext_diagnostics() -> SingletonQExtDiagnostics:
    left = canonical_continuation_left()
    carrier = make_quantum_continuation_carrier((left,))
    epistemic = make_epistemic_quantum_model(carrier, carrier.continuations[0], (1.0,))
    ontic = make_ontic_quantum_extension_model(carrier, (1.0,))
    semantic_distinct = bool(
        privileged_quantum_modal_diagnostic(epistemic)
        != privileged_quantum_modal_diagnostic(ontic)
    )
    audit = ontic_selector_audit(ontic)

    comparisons, max_state, max_inverse, max_metric = _perspective_transport_diagnostics_for(
        carrier.continuations
    )
    transport_preserved = bool(
        comparisons == 54
        and max_state <= 1e-9
        and max_inverse <= 1e-9
        and max_metric <= 1e-9
    )
    schedule = reduced_continuation_state(left, UPPER_EVENT)
    return SingletonQExtDiagnostics(
        qext_size=len(carrier.continuations),
        physical_multiplicity_lost=len(carrier.continuations) == 1,
        semantic_types_distinct=semantic_distinct,
        ontic_selector_absent=audit.no_selected_complete_continuation_datum,
        singleton_weight=ontic.extension_weights[0],
        singleton_weight_reconstructible_from_normalization=bool(
            ontic.extension_weights == (1.0,)
        ),
        current_record_information=continuation_current_record_information(left),
        perspective_transport_preserved=transport_preserved,
        future_extension_present=float(np.linalg.norm(schedule)) > DEFAULT_ATOL,
    )


@lru_cache(maxsize=1)
def semantic_weight_reconstruction_diagnostics() -> SemanticWeightReconstructionDiagnostics:
    epistemic, ontic = canonical_stage8b_models(selected_id="h_L")
    compatibility = stage8e_compatibility_diagnostics()
    alternative = make_ontic_quantum_extension_model(ontic.carrier, (0.75, 0.25))
    baseline_view = quantum_operational_view(ontic)
    alternative_view = quantum_operational_view(alternative)
    baseline_density = np.asarray(
        baseline_view.next_probabilities,
        dtype=object,
    )
    baseline_probabilities = np.array([value for _, value in baseline_view.next_probabilities])
    alternative_probabilities = np.array([value for _, value in alternative_view.next_probabilities])
    probability_residual = float(np.linalg.norm(baseline_probabilities - alternative_probabilities))
    same_carrier = alternative.carrier is ontic.carrier

    return SemanticWeightReconstructionDiagnostics(
        same_carrier_distinct_modal_semantics=compatibility.same_por_carrier_distinct_v_semantics,
        modal_semantics_reconstructible_from_public_por=False,
        uniform_weights=ontic.extension_weights,
        alternative_weights=alternative.extension_weights,
        same_carrier_admits_distinct_weights=bool(
            same_carrier and ontic.extension_weights != alternative.extension_weights
        ),
        prediction_density_residual=probability_residual,
        prediction_changes_with_weights=probability_residual > 1e-9,
        weights_reconstructible_from_carrier=False,
    )


def mismatch_diagnostics() -> tuple[MismatchDiagnostic, ...]:
    stage8d = stage8d_transport_diagnostics()
    stage8e = stage8e_compatibility_diagnostics()
    return (
        MismatchDiagnostic(
            mismatch="wrong_continuation_map",
            affected_role="P_V_class_transport",
            detected=stage8d.wrong_continuation_map_rejected,
            measurements=(("state_residual", stage8d.wrong_continuation_map_residual),),
            note="an h_L-derived clock map must not be reused on h_R",
        ),
        MismatchDiagnostic(
            mismatch="wrong_class_correspondence",
            affected_role="P_V_class_transport",
            detected=stage8d.wrong_class_correspondence_rejected,
            measurements=(),
            note="swapping physical continuation classes is not a valid chi",
        ),
        MismatchDiagnostic(
            mismatch="wrong_event_correspondence",
            affected_role="P_V_class_transport",
            detected=stage8d.terminal_current_correspondence_rejected,
            measurements=(),
            note="misdeclaring current e1 as terminal e2 is rejected",
        ),
        MismatchDiagnostic(
            mismatch="weight_mismatch",
            affected_role="V_weights",
            detected=stage8e.weight_mismatch_control_detected,
            measurements=(
                (
                    "transported_predictive_density_residual",
                    stage8e.transported_weight_mismatch_density_residual,
                ),
            ),
            note="same carrier with different K changes transported prediction",
        ),
        MismatchDiagnostic(
            mismatch="wrong_observable_coordinates",
            affected_role="current_record_content",
            detected=stage8e.bare_record_observable_rejected,
            measurements=(
                (
                    "bare_metric_self_adjoint_residual",
                    stage8e.bare_record_metric_self_adjoint_residual,
                ),
                (
                    "direct_record_interface_residual",
                    stage8e.max_current_record_direct_interface_residual,
                ),
            ),
            note="covariant transport of a wrongly typed observable is not semantic correctness",
        ),
    )


def _baseline_preserved_probes() -> dict[str, RoleEvidence]:
    compatibility = stage8e_compatibility_diagnostics()
    return {
        "V_physical_multiplicity": _preserved(
            "V_physical_multiplicity",
            (("qext_size", 2),),
        ),
        "V_selected_vs_unselected_semantics": _preserved(
            "V_selected_vs_unselected_semantics",
            (("distinct_semantics", compatibility.same_por_carrier_distinct_v_semantics),),
        ),
        "V_weights": _preserved("V_weights", (("weights", (0.5, 0.5)),)),
        "P_V_class_transport": _preserved(
            "P_V_class_transport",
            (("class_weight_covariance", compatibility.p_v_class_weight_covariance),),
        ),
        "O_V_extension_relation": _preserved(
            "O_V_extension_relation",
            (("first_difference_event", compatibility.o_v_first_difference_event),),
        ),
        "current_record_content": _preserved(
            "current_record_content",
            (("current_information", continuation_record_profile(canonical_continuation_left()).current_information),),
        ),
        "local_record_access": _preserved(
            "local_record_access",
            (("current_information", continuation_record_profile(canonical_continuation_left()).current_information),),
        ),
    }


@lru_cache(maxsize=1)
def stage8f_ablation_matrix() -> tuple[AblationCase, ...]:
    baseline = _baseline_preserved_probes()
    no_record = no_record_v_family_diagnostics()
    singleton = singleton_qext_diagnostics()
    reconstruction = perspective_map_reconstruction_diagnostics()
    semantic_weight = semantic_weight_reconstruction_diagnostics()

    record_neutralized = AblationCase(
        ingredient="record_coupling_neutralized",
        neutralization=(
            "replace canonical e1 record write by identity in both continuations, "
            "then re-derive their constrained physical states and clock maps"
        ),
        probes=(
            _preserved(
                "V_physical_multiplicity",
                (("qext_size", no_record.qext_size), ("future_overlap_squared", no_record.future_overlap_squared)),
                "two physically inequivalent future completions survive without the record write",
            ),
            _preserved(
                "V_selected_vs_unselected_semantics",
                (("privileged_structures_distinct", no_record.privileged_modal_structures_distinct),),
                "the same no-record carrier still supports the two typed modal semantics",
            ),
            _preserved(
                "V_weights",
                (("weight_mismatch_changes_prediction", no_record.weight_mismatch_changes_prediction),),
                "nontrivial continuation weights still affect the declared future prediction",
            ),
            _preserved(
                "P_V_class_transport",
                (("state_transports", no_record.distinct_clock_state_transports),),
                "continuation-specific perspective transport survives record neutralization",
            ),
            _preserved(
                "O_V_extension_relation",
                (("common_current_state_residual", no_record.common_current_state_residual),),
                "the pair still agrees through e1 and differs only in the represented future",
            ),
            _lost(
                "current_record_content",
                (
                    ("left_information", no_record.current_record_information_left),
                    ("right_information", no_record.current_record_information_right),
                ),
                "target-memory record information vanishes when the record write is neutralized",
            ),
            _lost(
                "local_record_access",
                (("global_record_present", False),),
                "there is no target-specific record left for the local interface to access",
            ),
        ),
    )

    singleton_case = AblationCase(
        ingredient="qext_collapsed_singleton",
        neutralization="retain only one admissible continuation class h_L",
        probes=(
            _lost(
                "V_physical_multiplicity",
                (("qext_size", singleton.qext_size),),
                "the multi-continuation role is removed by construction",
            ),
            _preserved(
                "V_selected_vs_unselected_semantics",
                (("semantic_types_distinct", singleton.semantic_types_distinct),),
                "selected-vs-unselected typing remains formally distinct even on singleton support",
            ),
            _reconstructible(
                "V_weights",
                (("singleton_weight", singleton.singleton_weight),),
                "normalization uniquely fixes the only continuation weight to one",
            ),
            _preserved(
                "P_V_class_transport",
                (("perspective_transport_preserved", singleton.perspective_transport_preserved),),
                "the remaining continuation still has a genuine re-derived perspective atlas",
            ),
            _preserved(
                "O_V_extension_relation",
                (("future_extension_present", singleton.future_extension_present),),
                "one future completion still extends the declared e1 actuality",
            ),
            baseline["current_record_content"],
            baseline["local_record_access"],
        ),
    )

    semantics_removed = AblationCase(
        ingredient="modal_semantics_removed",
        neutralization="retain the physical carrier and weights but discard selected-vs-unselected model typing",
        probes=(
            baseline["V_physical_multiplicity"],
            _lost(
                "V_selected_vs_unselected_semantics",
                (("same_public_por_supports_two_semantics", semantic_weight.same_carrier_distinct_modal_semantics),),
                "the semantic role is removed and cannot be uniquely reconstructed from retained P/O/current-R public data",
            ),
            baseline["V_weights"],
            baseline["P_V_class_transport"],
            baseline["O_V_extension_relation"],
            baseline["current_record_content"],
            baseline["local_record_access"],
        ),
    )

    weights_unfixed = AblationCase(
        ingredient="weights_unfixed",
        neutralization="retain carrier and modal typing but omit a declared q_E/K assignment",
        probes=(
            baseline["V_physical_multiplicity"],
            baseline["V_selected_vs_unselected_semantics"],
            _underdetermined(
                "V_weights",
                (
                    ("uniform", semantic_weight.uniform_weights),
                    ("alternative", semantic_weight.alternative_weights),
                    ("prediction_residual", semantic_weight.prediction_density_residual),
                ),
                "the same retained carrier admits distinct normalized weights with different predictions",
            ),
            baseline["P_V_class_transport"],
            baseline["O_V_extension_relation"],
            baseline["current_record_content"],
            baseline["local_record_access"],
        ),
    )

    maps_removed = AblationCase(
        ingredient="explicit_perspective_maps_removed",
        neutralization="remove stored/explicit edge maps but retain each continuation's per-node reduction coordinates",
        probes=(
            baseline["V_physical_multiplicity"],
            baseline["V_selected_vs_unselected_semantics"],
            baseline["V_weights"],
            _reconstructible(
                "P_V_class_transport",
                (
                    ("comparisons", reconstruction.comparisons),
                    ("max_map_residual", reconstruction.max_reference_map_residual),
                ),
                "S^h_{Y<-X}=C_{h,Y} C_{h,X}^{-1} reconstructs all tested explicit maps",
            ),
            baseline["O_V_extension_relation"],
            baseline["current_record_content"],
            baseline["local_record_access"],
        ),
    )

    chi_removed = AblationCase(
        ingredient="event_correspondence_removed",
        neutralization="retain local continuation atlases and V classes but remove the declared cross-perspective event/class chi",
        probes=(
            baseline["V_physical_multiplicity"],
            baseline["V_selected_vs_unselected_semantics"],
            baseline["V_weights"],
            _not_established(
                "P_V_class_transport",
                (("local_atlas_retained", True), ("class_correspondence_declared", False)),
                "without chi there is no typed claim that one source continuation/event corresponds to a target continuation/event",
            ),
            baseline["O_V_extension_relation"],
            baseline["current_record_content"],
            baseline["local_record_access"],
        ),
    )

    access_hidden = AblationCase(
        ingredient="current_record_access_hidden",
        neutralization="retain the global target-memory record but remove it from the declared local readout interface",
        probes=(
            baseline["V_physical_multiplicity"],
            baseline["V_selected_vs_unselected_semantics"],
            baseline["V_weights"],
            baseline["P_V_class_transport"],
            baseline["O_V_extension_relation"],
            _preserved(
                "current_record_content",
                (("global_information", continuation_record_profile(canonical_continuation_left()).current_information),),
                "the global target-specific record remains represented",
            ),
            _inaccessible(
                "local_record_access",
                (("global_information", continuation_record_profile(canonical_continuation_left()).current_information),),
                "the record exists globally but the ablated local interface does not expose it",
            ),
        ),
    )

    return (
        record_neutralized,
        singleton_case,
        semantics_removed,
        weights_unfixed,
        maps_removed,
        chi_removed,
        access_hidden,
    )


def stage8f_status_table() -> dict[str, dict[str, str]]:
    return {
        case.ingredient: {role: case.status(role).value for role in ROLE_IDS}
        for case in stage8f_ablation_matrix()
    }


def stage8f_summary() -> dict[str, object]:
    no_record = no_record_v_family_diagnostics()
    reconstruction = perspective_map_reconstruction_diagnostics()
    semantic_weight = semantic_weight_reconstruction_diagnostics()
    return {
        "stage": "8F",
        "status_vocabulary": tuple(status.value for status in RoleStatus),
        "roles": ROLE_IDS,
        "ablations": [case.as_dict() for case in stage8f_ablation_matrix()],
        "mismatches": [item.as_dict() for item in mismatch_diagnostics()],
        "diagnostics": {
            "no_record_v_family": asdict(no_record),
            "perspective_map_reconstruction": asdict(reconstruction),
            "semantic_weight_reconstruction": asdict(semantic_weight),
        },
        "current_execution_criteria": {
            "42": "typed Stage 8F role/status matrix with preserved/reconstructible/inaccessible/lost/underdetermined/not_established kept distinct",
            "43": "record-neutral constrained continuation pair retains nontrivial V/P/O structure while current R is lost",
            "44": "singleton-QExt ablation separates physical continuation multiplicity from selected-vs-unselected typing and makes its sole weight reconstructible",
            "45": "modal semantics and nontrivial weights are not uniquely reconstructed from retained public carrier structure",
            "46": "explicit P-V edge maps are reconstructible from per-node coordinates while removal of event/class chi makes cross-perspective P-V correspondence not established",
            "47": "hidden record access and controlled map/class/event/weight/observable mismatches distinguish inaccessible/lost/underdetermined/not_established outcomes",
        },
        "next": "Stage 8G — synthesis and evidence-selected next gate",
        "guards": (
            "lost != metaphysically irreducible",
            "reconstructible != universally redundant",
            "underdetermined != ontically open",
            "inaccessible != globally absent",
            "not_established != false",
            "singleton support != absence of a formal selected-vs-unselected type distinction",
            "record-neutral V witness != universal R-V independence theorem",
            "P-V map reconstruction != P=V",
            "covariance of a wrongly typed observable != semantic correctness",
            "full Stage 8C measurement covariance remains not_established",
        ),
    }
