"""Stage 8B typed quantum Potentiality models on one shared continuation carrier.

Stage 8A established a physically executable continuation substrate

    QExt(e1) = {h_L, h_R}

inside the Stage 7 constrained construction.  Stage 8B keeps that physical
substrate fixed and gives it two distinct global model roles:

    M_E^Q = (QCarrier, D, h*, q_E)

with one globally selected complete continuation h* hidden from the
pre-discriminating interface, and

    M_O^Q(D) = (QCarrier, D, QExt(D), K)

with no selected complete continuation datum or equivalent selector field.

This module intentionally stops short of the full Stage 8C operational/update
interface.  Its public projection is only the minimal pre-discriminating view
needed to test that changing h* alone cannot affect declared current data or
matched continuation weights.

Formal selected-vs-unselected model structure is not evidence that nature is
eternalistic or ontically open.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, fields
from math import isclose, isfinite
from typing import Sequence

import numpy as np

from .stage5_clock_change import DEFAULT_ATOL
from .stage8_continuations import (
    CANONICAL_ANCHOR,
    QuantumContinuation,
    continuation_current_record_information,
    continuation_equivalent,
    quantum_extension_set,
    reduced_continuation_state,
)


@dataclass(frozen=True, slots=True)
class QuantumContinuationCarrier:
    """Validated physical continuation-equivalence representatives at one anchor."""

    current_anchor: int
    continuations: tuple[QuantumContinuation, ...]


@dataclass(frozen=True, slots=True)
class EpistemicQuantumPotentiality:
    """Live hypotheses about which already-selected continuation is actual."""

    continuations: tuple[QuantumContinuation, ...]


@dataclass(frozen=True, slots=True)
class OnticExtensionQuantumPotentiality:
    """All represented admissible continuations, with no selected future datum."""

    continuations: tuple[QuantumContinuation, ...]


@dataclass(frozen=True, slots=True)
class EpistemicQuantumModel:
    """M_E^Q=(QCarrier,D,h*,q_E)."""

    carrier: QuantumContinuationCarrier
    selected_continuation: QuantumContinuation
    belief_weights: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class OnticQuantumExtensionModel:
    """M_O^Q(D)=(QCarrier,D,QExt(D),K), without a selected continuation field."""

    carrier: QuantumContinuationCarrier
    extension_weights: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class PreDiscriminatingQuantumView:
    """Minimal Stage 8B public projection, deliberately excluding h* and model type.

    Stage 8C will define the full frozen O_Q interface and update semantics.
    """

    current_anchor: int
    qext_size: int
    current_state: tuple[complex, ...]
    current_record_information: float
    continuation_weights: tuple[float, ...]


@dataclass(frozen=True, slots=True)
class OnticSelectorAudit:
    field_names: tuple[str, ...]
    forbidden_selector_fields: tuple[str, ...]
    direct_continuation_fields: tuple[str, ...]
    arbitrary_instance_dict_present: bool
    all_qext_members_represented: bool
    full_weight_support: bool
    no_selected_complete_continuation_datum: bool


@dataclass(frozen=True, slots=True)
class Stage8BModalDiagnostics:
    qext_size: int
    epistemic_selected_left: str
    epistemic_selected_right: str
    privileged_selected_swap_detected: bool
    potentiality_types_distinct: bool
    potentiality_members_match: bool
    shared_carrier_identity: bool
    matched_weight_residual: float
    selected_swap_weight_residual: float
    matched_pre_view_equal: bool
    selected_swap_pre_view_equal: bool
    selected_hidden_from_pre_view_schema: bool
    ontic_no_selected_complete_continuation_datum: bool
    ontic_full_weight_support: bool
    current_record_information: float
    current_state_norm: float


def make_quantum_continuation_carrier(
    continuations: Sequence[QuantumContinuation] | None = None,
    *,
    current_anchor: int = CANONICAL_ANCHOR,
    atol: float = DEFAULT_ATOL,
) -> QuantumContinuationCarrier:
    proposed = None if continuations is None else tuple(continuations)
    normalized = quantum_extension_set(
        current_anchor,
        candidates=proposed,
        atol=atol,
    )
    if not normalized:
        raise ValueError("Stage 8B carrier requires at least one admissible continuation")
    if proposed is not None and len(normalized) != len(proposed):
        raise ValueError("Stage 8B carrier must contain one representative per continuation class")
    ids = tuple(item.continuation_id for item in normalized)
    if len(set(ids)) != len(ids):
        raise ValueError("continuation representative ids must be unique")
    return QuantumContinuationCarrier(current_anchor=current_anchor, continuations=normalized)


def canonical_quantum_continuation_carrier() -> QuantumContinuationCarrier:
    return make_quantum_continuation_carrier()


def continuation_ids(carrier: QuantumContinuationCarrier) -> tuple[str, ...]:
    return tuple(item.continuation_id for item in carrier.continuations)


def _equivalent_index(
    carrier: QuantumContinuationCarrier,
    continuation: QuantumContinuation,
    *,
    atol: float = DEFAULT_ATOL,
) -> int:
    matches = [
        index
        for index, representative in enumerate(carrier.continuations)
        if continuation_equivalent(representative, continuation, atol=atol)
    ]
    if len(matches) != 1:
        raise ValueError("selected continuation must belong to exactly one QExt equivalence class")
    return matches[0]


def _validate_weights(
    carrier: QuantumContinuationCarrier,
    weights: Sequence[float],
    *,
    name: str,
) -> tuple[float, ...]:
    frozen = tuple(float(weight) for weight in weights)
    if len(frozen) != len(carrier.continuations):
        raise ValueError(f"{name} must provide one weight per QExt continuation class")
    if any(not isfinite(weight) or weight < 0.0 for weight in frozen):
        raise ValueError(f"{name} must be finite and non-negative")
    total = sum(frozen)
    if not isclose(total, 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError(f"{name} must sum to 1; got {total}")
    return frozen


def matched_uniform_weights(carrier: QuantumContinuationCarrier) -> tuple[float, ...]:
    """Return matched q_E/K weights without taking or consulting any h*."""

    count = len(carrier.continuations)
    return tuple(1.0 / count for _ in carrier.continuations)


def make_epistemic_quantum_model(
    carrier: QuantumContinuationCarrier,
    selected_continuation: QuantumContinuation,
    belief_weights: Sequence[float],
    *,
    atol: float = DEFAULT_ATOL,
) -> EpistemicQuantumModel:
    weights = _validate_weights(carrier, belief_weights, name="q_E")
    selected_index = _equivalent_index(carrier, selected_continuation, atol=atol)
    if weights[selected_index] <= 0.0:
        raise ValueError("selected continuation must retain positive epistemic support")
    selected_representative = carrier.continuations[selected_index]
    return EpistemicQuantumModel(
        carrier=carrier,
        selected_continuation=selected_representative,
        belief_weights=weights,
    )


def make_ontic_quantum_extension_model(
    carrier: QuantumContinuationCarrier,
    extension_weights: Sequence[float],
) -> OnticQuantumExtensionModel:
    weights = _validate_weights(carrier, extension_weights, name="K")
    return OnticQuantumExtensionModel(carrier=carrier, extension_weights=weights)


def continuation_by_id(
    carrier: QuantumContinuationCarrier,
    continuation_id: str,
) -> QuantumContinuation:
    matches = [item for item in carrier.continuations if item.continuation_id == continuation_id]
    if len(matches) != 1:
        raise ValueError(f"unknown or ambiguous continuation id {continuation_id!r}")
    return matches[0]


def canonical_stage8b_models(
    *,
    selected_id: str = "h_L",
) -> tuple[EpistemicQuantumModel, OnticQuantumExtensionModel]:
    """Return canonical typed models sharing the exact same carrier object."""

    carrier = canonical_quantum_continuation_carrier()
    weights = matched_uniform_weights(carrier)
    epistemic = make_epistemic_quantum_model(
        carrier,
        continuation_by_id(carrier, selected_id),
        weights,
    )
    ontic = make_ontic_quantum_extension_model(carrier, weights)
    return epistemic, ontic


def epistemic_quantum_potentiality(
    model: EpistemicQuantumModel,
) -> EpistemicQuantumPotentiality:
    live = tuple(
        continuation
        for continuation, weight in zip(
            model.carrier.continuations,
            model.belief_weights,
            strict=True,
        )
        if weight > 0.0
    )
    return EpistemicQuantumPotentiality(live)


def ontic_extension_quantum_potentiality(
    model: OnticQuantumExtensionModel,
) -> OnticExtensionQuantumPotentiality:
    return OnticExtensionQuantumPotentiality(model.carrier.continuations)


def selected_quantum_continuation(model: EpistemicQuantumModel) -> QuantumContinuation:
    """Privileged Stage 8B diagnostic.  This is not part of the public view."""

    return model.selected_continuation


def ontic_selector_audit(
    model: OnticQuantumExtensionModel,
) -> OnticSelectorAudit:
    """Audit the declared ontic model schema for selector-like stored state.

    The audit is intentionally structural and bounded to this dataclass schema.
    It does not prove that nature lacks a selected future.
    """

    names = tuple(field.name for field in fields(model))
    forbidden_tokens = (
        "selected",
        "selector",
        "seed",
        "precomputed",
        "outcome",
        "latent_branch",
    )
    forbidden = tuple(
        name
        for name in names
        if any(token in name.lower() for token in forbidden_tokens)
    )
    direct = tuple(
        name
        for name in names
        if isinstance(getattr(model, name), QuantumContinuation)
    )
    arbitrary_dict = hasattr(model, "__dict__")
    represented = ontic_extension_quantum_potentiality(model).continuations
    all_represented = bool(
        len(represented) == len(model.carrier.continuations)
        and all(
            any(continuation_equivalent(item, candidate) for candidate in represented)
            for item in model.carrier.continuations
        )
    )
    full_support = all(weight > 0.0 for weight in model.extension_weights)
    no_selector = bool(
        not forbidden
        and not direct
        and not arbitrary_dict
        and all_represented
        and not hasattr(model, "selected_continuation")
        and not hasattr(model, "selected_history")
        and not hasattr(model, "selector")
        and not hasattr(model, "seed")
    )
    return OnticSelectorAudit(
        field_names=names,
        forbidden_selector_fields=forbidden,
        direct_continuation_fields=direct,
        arbitrary_instance_dict_present=arbitrary_dict,
        all_qext_members_represented=all_represented,
        full_weight_support=full_support,
        no_selected_complete_continuation_datum=no_selector,
    )


def _weights_for_pre_view(
    model: EpistemicQuantumModel | OnticQuantumExtensionModel,
) -> tuple[float, ...]:
    if isinstance(model, EpistemicQuantumModel):
        return model.belief_weights
    if isinstance(model, OnticQuantumExtensionModel):
        return model.extension_weights
    raise TypeError("unsupported Stage 8B model type")


def pre_discriminating_quantum_view(
    model: EpistemicQuantumModel | OnticQuantumExtensionModel,
    *,
    atol: float = DEFAULT_ATOL,
) -> PreDiscriminatingQuantumView:
    """Project only shared current data and declared continuation weights.

    The function never reads ``selected_continuation``.  It uses the first
    carrier representative only as a model-neutral representative of the common
    current Actuality and verifies that every continuation gives the same current
    reduced state before returning the view.
    """

    carrier = model.carrier
    current_states = tuple(
        reduced_continuation_state(item, carrier.current_anchor)
        for item in carrier.continuations
    )
    reference = current_states[0]
    for state in current_states[1:]:
        if np.linalg.norm(state - reference) > atol:
            raise ValueError("carrier continuations do not share the declared current Actuality")
    current_record_values = tuple(
        continuation_current_record_information(item)
        for item in carrier.continuations
    )
    if max(current_record_values) - min(current_record_values) > atol:
        raise ValueError("carrier continuations do not share the declared current record interface")
    return PreDiscriminatingQuantumView(
        current_anchor=carrier.current_anchor,
        qext_size=len(carrier.continuations),
        current_state=tuple(complex(value) for value in reference),
        current_record_information=float(current_record_values[0]),
        continuation_weights=_weights_for_pre_view(model),
    )


def stage8b_modal_diagnostics(*, atol: float = DEFAULT_ATOL) -> Stage8BModalDiagnostics:
    carrier = canonical_quantum_continuation_carrier()
    weights = matched_uniform_weights(carrier)
    left = continuation_by_id(carrier, "h_L")
    right = continuation_by_id(carrier, "h_R")
    epistemic_left = make_epistemic_quantum_model(carrier, left, weights, atol=atol)
    epistemic_right = make_epistemic_quantum_model(carrier, right, weights, atol=atol)
    ontic = make_ontic_quantum_extension_model(carrier, weights)

    epot = epistemic_quantum_potentiality(epistemic_left)
    opot = ontic_extension_quantum_potentiality(ontic)
    audit = ontic_selector_audit(ontic)
    view_left = pre_discriminating_quantum_view(epistemic_left, atol=atol)
    view_right = pre_discriminating_quantum_view(epistemic_right, atol=atol)
    view_ontic = pre_discriminating_quantum_view(ontic, atol=atol)

    current = np.asarray(view_left.current_state, dtype=np.complex128)
    matched_weight_residual = max(
        abs(a - b)
        for a, b in zip(epistemic_left.belief_weights, ontic.extension_weights, strict=True)
    )
    selected_swap_weight_residual = max(
        abs(a - b)
        for a, b in zip(epistemic_left.belief_weights, epistemic_right.belief_weights, strict=True)
    )
    members_match = bool(
        len(epot.continuations) == len(opot.continuations)
        and all(
            any(continuation_equivalent(item, candidate, atol=atol) for candidate in opot.continuations)
            for item in epot.continuations
        )
    )
    return Stage8BModalDiagnostics(
        qext_size=len(carrier.continuations),
        epistemic_selected_left=selected_quantum_continuation(epistemic_left).continuation_id,
        epistemic_selected_right=selected_quantum_continuation(epistemic_right).continuation_id,
        privileged_selected_swap_detected=not continuation_equivalent(left, right, atol=atol),
        potentiality_types_distinct=type(epot) is not type(opot),
        potentiality_members_match=members_match,
        shared_carrier_identity=bool(
            epistemic_left.carrier is epistemic_right.carrier
            and epistemic_left.carrier is ontic.carrier
        ),
        matched_weight_residual=float(matched_weight_residual),
        selected_swap_weight_residual=float(selected_swap_weight_residual),
        matched_pre_view_equal=view_left == view_ontic,
        selected_swap_pre_view_equal=view_left == view_right,
        selected_hidden_from_pre_view_schema=bool(
            "selected_continuation" not in {field.name for field in fields(PreDiscriminatingQuantumView)}
            and "model_type" not in {field.name for field in fields(PreDiscriminatingQuantumView)}
        ),
        ontic_no_selected_complete_continuation_datum=audit.no_selected_complete_continuation_datum,
        ontic_full_weight_support=audit.full_weight_support,
        current_record_information=view_left.current_record_information,
        current_state_norm=float(np.linalg.norm(current)),
    )


def stage8b_summary() -> dict[str, object]:
    diagnostics = stage8b_modal_diagnostics()
    epistemic, ontic = canonical_stage8b_models()
    return {
        "stage": "8B",
        "status": "typed quantum modal models established on shared Stage 8A carrier",
        "current_anchor": "e1",
        "qext": continuation_ids(epistemic.carrier),
        "epistemic_type": type(epistemic_quantum_potentiality(epistemic)).__name__,
        "ontic_type": type(ontic_extension_quantum_potentiality(ontic)).__name__,
        "diagnostics": asdict(diagnostics),
        "ontic_selector_audit": asdict(ontic_selector_audit(ontic)),
        "exit_criteria_satisfied": (17, 18, 19, 20, 21),
        "next": "Stage 8C — operational underdetermination and explicit update",
        "guards": (
            "formal selected-vs-unselected difference != empirical physical difference",
            "no selected continuation field != proof of ontic openness in nature",
            "matched numerical q_E and K != matched probability semantics",
            "hidden h* diagnostic != operational access to h*",
            "Stage 8B pre-discriminating view != full Stage 8C O_Q interface",
        ),
    }
