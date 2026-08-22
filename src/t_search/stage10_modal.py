"""Stage 10E weighted/modal/evidence-update covariance.

Stage 10D established the fully typed future-signature measurement family at
per-continuation / pre-weighting level.  Stage 10E restores the Stage 9C modal
roles and continuation weights without changing their semantics.

The key rule is deliberately simple: at each A/B/C chart, use the Stage 10D
per-continuation likelihoods as the likelihood table and then apply the same
weighting/Bayes operations already used by Stage 9C.

This stage tests:
- weighted future-prediction covariance;
- matched epistemic/ontic-extension public measurement-view equality;
- hidden epistemic h* swap invariance;
- perspective-stable visibility of a weight mismatch;
- perspective-consistent common evidence conditioning/posteriors while the
  updated ontic-extension state remains selector-free.

None of these operational results identifies epistemic and ontic modal
semantics or promotes evidence update to ontological becoming.
"""

from __future__ import annotations

from dataclasses import dataclass, fields
from math import isclose
from typing import Sequence

import numpy as np

from .stage5_clock_change import DEFAULT_ATOL, SUBSYSTEMS
from .stage9_modal import (
    FUTURE_SIGNATURE_LEFT,
    Stage9CModel,
    Stage9EpistemicModel,
    Stage9Evidence,
    Stage9OnticExtensionModel,
    canonical_stage9c_models,
    continuation_by_id,
    make_stage9_epistemic_model,
    make_stage9_ontic_model,
    matched_uniform_weights,
    ontic_selector_audit,
    update_stage9_epistemic_model,
    update_stage9_ontic_model,
    updated_ontic_selector_audit,
)
from .stage9_transport import (
    Stage9PerspectiveQRView,
    class_correspondence,
    perspective_qr_view,
)
from .stage10_probability import stage10d_chart_probabilities
from .stage10_transport import Stage10ChartMeasurement, canonical_stage10c_charts


@dataclass(frozen=True, slots=True)
class Stage10EPublicMeasurementView:
    current_event: int
    clock: str
    clock_index: int
    continuation_ids: tuple[str, ...]
    continuation_weights: tuple[float, ...]
    predictive_density: tuple[complex, ...]
    directional_record_scores: tuple[float, ...]
    directional_accessibility_scores: tuple[float, ...]
    orientations: tuple[str, ...]
    next_outcomes: tuple[str, ...]
    next_probabilities: tuple[tuple[str, float], ...]


@dataclass(frozen=True, slots=True)
class Stage10EPosteriorView:
    clock: str
    clock_index: int
    observed_outcome: str
    epistemic_posterior_weights: tuple[float, ...]
    ontic_posterior_weights: tuple[float, ...]
    epistemic_selected_continuation_id: str
    ontic_no_selected_complete_continuation_datum: bool


@dataclass(frozen=True, slots=True)
class Stage10EModalDiagnostics:
    chart_count: int
    weighted_prediction_evaluations: int
    max_weighted_prediction_covariance_residual: float
    matched_epistemic_ontic_views_all_nodes: bool
    hidden_selected_absent_from_public_schema: bool
    hidden_hstar_swap_views_all_nodes: bool
    privileged_modal_roles_still_distinct: bool
    weight_mismatch_visible_all_nodes: bool
    max_weight_mismatch_covariance_residual: float
    minimum_weight_mismatch_prediction_difference: float
    evidence_outcome: str
    posterior_chart_count: int
    max_epistemic_posterior_covariance_residual: float
    max_ontic_posterior_covariance_residual: float
    max_epistemic_ontic_posterior_residual: float
    stage9c_epistemic_posterior_residual: float
    stage9c_ontic_posterior_residual: float
    epistemic_hidden_selection_preserved: bool
    ontic_updated_selector_free_all_nodes: bool
    weighted_prediction_covariance: bool
    matched_modal_public_view_covariance: bool
    hidden_hstar_swap_invariant: bool
    weight_mismatch_transport_covariance: bool
    evidence_update_covariance: bool
    weighted_modal_update_covariance_established: bool


def _chart_lookup() -> dict[tuple[str, str, int], Stage10ChartMeasurement]:
    return {
        (chart.continuation_id, chart.clock, chart.clock_index): chart
        for chart in canonical_stage10c_charts()
    }


def _weights(model: Stage9CModel) -> tuple[float, ...]:
    if isinstance(model, Stage9EpistemicModel):
        return model.belief_weights
    if isinstance(model, Stage9OnticExtensionModel):
        return model.extension_weights
    raise TypeError("unsupported Stage 10E model")


def _validate_weight_alignment(model: Stage9CModel, weights: Sequence[float]) -> tuple[float, ...]:
    frozen = tuple(float(value) for value in weights)
    if len(frozen) != len(model.carrier.continuations):
        raise ValueError("Stage 10E requires one weight per continuation class")
    if any(value < 0.0 or not np.isfinite(value) for value in frozen):
        raise ValueError("Stage 10E weights must be finite and non-negative")
    if not isclose(sum(frozen), 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError("Stage 10E weights must sum to one")
    return frozen


def stage10e_continuation_likelihoods(
    model: Stage9CModel,
    clock: str,
    index: int,
    *,
    atol: float = DEFAULT_ATOL,
) -> tuple[tuple[str, tuple[tuple[str, float], ...]], ...]:
    if clock not in SUBSYSTEMS or index not in (0, 1, 2):
        raise ValueError("Stage 10E chart must be one declared A/B/C clock/readout")
    charts = _chart_lookup()
    result: list[tuple[str, tuple[tuple[str, float], ...]]] = []
    for continuation in model.carrier.continuations:
        key = (continuation.continuation_id, clock, index)
        chart = charts[key]
        result.append(
            (
                continuation.continuation_id,
                stage10d_chart_probabilities(continuation, chart, atol=atol),
            )
        )
    return tuple(result)


def stage10e_weighted_prediction(
    model: Stage9CModel,
    clock: str,
    index: int,
    *,
    atol: float = DEFAULT_ATOL,
) -> tuple[tuple[str, float], ...]:
    weights = _validate_weight_alignment(model, _weights(model))
    likelihood_rows = stage10e_continuation_likelihoods(
        model, clock, index, atol=atol
    )
    likelihoods = tuple(dict(row) for _, row in likelihood_rows)
    names = tuple(name for name, _ in likelihood_rows[0][1])
    prediction = tuple(
        (
            name,
            float(
                sum(
                    weight * likelihood[name]
                    for weight, likelihood in zip(weights, likelihoods, strict=True)
                )
            ),
        )
        for name in names
    )
    if not isclose(sum(value for _, value in prediction), 1.0, rel_tol=0.0, abs_tol=10 * atol):
        raise ValueError("Stage 10E weighted prediction must sum to one")
    return prediction


def stage10e_public_measurement_view(
    model: Stage9CModel,
    clock: str,
    index: int,
    *,
    atol: float = DEFAULT_ATOL,
) -> Stage10EPublicMeasurementView:
    correspondence = class_correspondence(model.carrier, "preserving")
    base: Stage9PerspectiveQRView = perspective_qr_view(
        model, clock, index, correspondence=correspondence, atol=atol
    )
    prediction = stage10e_weighted_prediction(model, clock, index, atol=atol)
    return Stage10EPublicMeasurementView(
        current_event=base.current_event,
        clock=base.clock,
        clock_index=base.clock_index,
        continuation_ids=base.continuation_ids,
        continuation_weights=base.continuation_weights,
        predictive_density=base.predictive_density,
        directional_record_scores=base.directional_record_scores,
        directional_accessibility_scores=base.directional_accessibility_scores,
        orientations=base.orientations,
        next_outcomes=tuple(name for name, _ in prediction),
        next_probabilities=prediction,
    )


def _public_views_close(
    left: Stage10EPublicMeasurementView,
    right: Stage10EPublicMeasurementView,
    *,
    atol: float,
) -> bool:
    if (
        left.current_event != right.current_event
        or left.clock != right.clock
        or left.clock_index != right.clock_index
        or left.continuation_ids != right.continuation_ids
        or left.orientations != right.orientations
        or left.next_outcomes != right.next_outcomes
    ):
        return False
    arrays = (
        (left.continuation_weights, right.continuation_weights),
        (left.predictive_density, right.predictive_density),
        (left.directional_record_scores, right.directional_record_scores),
        (
            left.directional_accessibility_scores,
            right.directional_accessibility_scores,
        ),
    )
    if not all(
        np.allclose(np.asarray(a), np.asarray(b), atol=atol, rtol=0.0)
        for a, b in arrays
    ):
        return False
    lp = dict(left.next_probabilities)
    rp = dict(right.next_probabilities)
    return bool(
        set(lp) == set(rp)
        and all(isclose(lp[name], rp[name], rel_tol=0.0, abs_tol=atol) for name in lp)
    )


def _probability_residual(
    left: tuple[tuple[str, float], ...],
    right: tuple[tuple[str, float], ...],
) -> float:
    lhs = dict(left)
    rhs = dict(right)
    if set(lhs) != set(rhs):
        return float("inf")
    return max(abs(lhs[name] - rhs[name]) for name in lhs)


def _posterior(
    prior: Sequence[float],
    likelihoods: Sequence[float],
    *,
    atol: float,
) -> tuple[float, ...]:
    raw = tuple(
        float(weight) * float(likelihood)
        for weight, likelihood in zip(prior, likelihoods, strict=True)
    )
    total = sum(raw)
    if total <= atol:
        raise ValueError("Stage 10E evidence has zero predictive support")
    return tuple(value / total for value in raw)


def stage10e_posterior_view(
    epistemic: Stage9EpistemicModel,
    ontic: Stage9OnticExtensionModel,
    evidence: Stage9Evidence,
    clock: str,
    index: int,
    *,
    atol: float = DEFAULT_ATOL,
) -> Stage10EPosteriorView:
    if epistemic.carrier is not ontic.carrier:
        raise ValueError("Stage 10E common evidence requires the exact same carrier")
    likelihood_rows = stage10e_continuation_likelihoods(
        epistemic, clock, index, atol=atol
    )
    likelihood_tables = tuple(dict(row) for _, row in likelihood_rows)
    if evidence.outcome not in likelihood_tables[0]:
        raise ValueError("Stage 10E evidence outcome is outside the typed measurement family")
    likelihoods = tuple(table[evidence.outcome] for table in likelihood_tables)
    selected_index = next(
        i
        for i, item in enumerate(epistemic.carrier.continuations)
        if item.continuation_id == epistemic.selected_continuation.continuation_id
    )
    if likelihoods[selected_index] <= atol:
        raise ValueError("Stage 10E evidence contradicts the hidden selected continuation")
    posterior_e = _posterior(epistemic.belief_weights, likelihoods, atol=atol)
    posterior_o = _posterior(ontic.extension_weights, likelihoods, atol=atol)

    # The Stage 9C update objects remain the semantic authority for selector
    # behavior; chart-local likelihoods must reproduce their posterior values.
    updated_e = update_stage9_epistemic_model(epistemic, evidence, atol=atol)
    updated_o = update_stage9_ontic_model(ontic, evidence, atol=atol)
    if not np.allclose(posterior_e, updated_e.posterior_weights, atol=10 * atol, rtol=0.0):
        raise RuntimeError("Stage 10E epistemic posterior disagrees with Stage 9C semantics")
    if not np.allclose(posterior_o, updated_o.posterior_weights, atol=10 * atol, rtol=0.0):
        raise RuntimeError("Stage 10E ontic posterior disagrees with Stage 9C semantics")

    return Stage10EPosteriorView(
        clock=clock,
        clock_index=index,
        observed_outcome=evidence.outcome,
        epistemic_posterior_weights=posterior_e,
        ontic_posterior_weights=posterior_o,
        epistemic_selected_continuation_id=updated_e.selected_continuation.continuation_id,
        ontic_no_selected_complete_continuation_datum=updated_ontic_selector_audit(updated_o),
    )


def stage10e_modal_diagnostics(*, atol: float = DEFAULT_ATOL) -> Stage10EModalDiagnostics:
    epistemic, ontic = canonical_stage9c_models(selected_id="h_L")
    carrier = epistemic.carrier
    uniform = matched_uniform_weights(carrier)
    swapped_epistemic = make_stage9_epistemic_model(
        carrier,
        continuation_by_id(carrier, "h_R"),
        uniform,
        atol=atol,
    )
    mismatch = make_stage9_ontic_model(carrier, (0.75, 0.25))

    matched_all = True
    selected_swap_all = True
    weighted_predictions: list[tuple[tuple[str, float], ...]] = []
    mismatch_predictions: list[tuple[tuple[str, float], ...]] = []
    weight_mismatch_visible_all = True
    minimum_mismatch_difference = float("inf")

    for clock in SUBSYSTEMS:
        for index in range(3):
            view_e = stage10e_public_measurement_view(epistemic, clock, index, atol=atol)
            view_o = stage10e_public_measurement_view(ontic, clock, index, atol=atol)
            view_swap = stage10e_public_measurement_view(
                swapped_epistemic, clock, index, atol=atol
            )
            view_mismatch = stage10e_public_measurement_view(
                mismatch, clock, index, atol=atol
            )
            matched_all = matched_all and _public_views_close(view_e, view_o, atol=atol)
            selected_swap_all = selected_swap_all and _public_views_close(
                view_e, view_swap, atol=atol
            )
            weighted_predictions.append(view_e.next_probabilities)
            mismatch_predictions.append(view_mismatch.next_probabilities)
            difference = _probability_residual(
                view_e.next_probabilities, view_mismatch.next_probabilities
            )
            minimum_mismatch_difference = min(minimum_mismatch_difference, difference)
            weight_mismatch_visible_all = weight_mismatch_visible_all and difference > 10 * atol

    reference_prediction = weighted_predictions[0]
    reference_mismatch = mismatch_predictions[0]
    max_weighted_covariance = max(
        _probability_residual(reference_prediction, item)
        for item in weighted_predictions
    )
    max_mismatch_covariance = max(
        _probability_residual(reference_mismatch, item)
        for item in mismatch_predictions
    )

    public_schema = {field.name for field in fields(Stage10EPublicMeasurementView)}
    hidden_absent = all(
        name not in public_schema
        for name in (
            "selected_continuation",
            "selected_continuation_id",
            "selector",
            "model_type",
            "modal_type",
            "belief_weights",
            "extension_weights",
        )
    )
    privileged_distinct = bool(
        hasattr(epistemic, "selected_continuation")
        and not hasattr(ontic, "selected_continuation")
        and ontic_selector_audit(ontic).no_selected_complete_continuation_datum
    )

    evidence = Stage9Evidence(FUTURE_SIGNATURE_LEFT)
    posterior_views: list[Stage10EPosteriorView] = []
    for clock in SUBSYSTEMS:
        for index in range(3):
            posterior_views.append(
                stage10e_posterior_view(
                    epistemic, ontic, evidence, clock, index, atol=atol
                )
            )
    reference_posterior = posterior_views[0]
    max_e_cov = max(
        float(np.max(np.abs(
            np.asarray(item.epistemic_posterior_weights)
            - np.asarray(reference_posterior.epistemic_posterior_weights)
        )))
        for item in posterior_views
    )
    max_o_cov = max(
        float(np.max(np.abs(
            np.asarray(item.ontic_posterior_weights)
            - np.asarray(reference_posterior.ontic_posterior_weights)
        )))
        for item in posterior_views
    )
    max_eo = max(
        float(np.max(np.abs(
            np.asarray(item.epistemic_posterior_weights)
            - np.asarray(item.ontic_posterior_weights)
        )))
        for item in posterior_views
    )

    updated_e = update_stage9_epistemic_model(epistemic, evidence, atol=atol)
    updated_o = update_stage9_ontic_model(ontic, evidence, atol=atol)
    stage9_e_residual = float(np.max(np.abs(
        np.asarray(reference_posterior.epistemic_posterior_weights)
        - np.asarray(updated_e.posterior_weights)
    )))
    stage9_o_residual = float(np.max(np.abs(
        np.asarray(reference_posterior.ontic_posterior_weights)
        - np.asarray(updated_o.posterior_weights)
    )))
    selection_preserved = all(
        item.epistemic_selected_continuation_id
        == epistemic.selected_continuation.continuation_id
        for item in posterior_views
    )
    ontic_selector_free_all = all(
        item.ontic_no_selected_complete_continuation_datum
        for item in posterior_views
    )

    tolerance = 1e-9
    weighted_covariance = max_weighted_covariance <= tolerance
    matched_covariance = matched_all
    hstar_invariant = bool(selected_swap_all and hidden_absent)
    mismatch_covariance = bool(
        weight_mismatch_visible_all
        and minimum_mismatch_difference > tolerance
        and max_mismatch_covariance <= tolerance
    )
    update_covariance = bool(
        max_e_cov <= tolerance
        and max_o_cov <= tolerance
        and max_eo <= tolerance
        and stage9_e_residual <= tolerance
        and stage9_o_residual <= tolerance
        and selection_preserved
        and ontic_selector_free_all
    )

    return Stage10EModalDiagnostics(
        chart_count=9,
        weighted_prediction_evaluations=9 * 2,
        max_weighted_prediction_covariance_residual=max_weighted_covariance,
        matched_epistemic_ontic_views_all_nodes=matched_all,
        hidden_selected_absent_from_public_schema=hidden_absent,
        hidden_hstar_swap_views_all_nodes=selected_swap_all,
        privileged_modal_roles_still_distinct=privileged_distinct,
        weight_mismatch_visible_all_nodes=weight_mismatch_visible_all,
        max_weight_mismatch_covariance_residual=max_mismatch_covariance,
        minimum_weight_mismatch_prediction_difference=minimum_mismatch_difference,
        evidence_outcome=evidence.outcome,
        posterior_chart_count=len(posterior_views),
        max_epistemic_posterior_covariance_residual=max_e_cov,
        max_ontic_posterior_covariance_residual=max_o_cov,
        max_epistemic_ontic_posterior_residual=max_eo,
        stage9c_epistemic_posterior_residual=stage9_e_residual,
        stage9c_ontic_posterior_residual=stage9_o_residual,
        epistemic_hidden_selection_preserved=selection_preserved,
        ontic_updated_selector_free_all_nodes=ontic_selector_free_all,
        weighted_prediction_covariance=weighted_covariance,
        matched_modal_public_view_covariance=matched_covariance,
        hidden_hstar_swap_invariant=hstar_invariant,
        weight_mismatch_transport_covariance=mismatch_covariance,
        evidence_update_covariance=update_covariance,
        weighted_modal_update_covariance_established=bool(
            weighted_covariance
            and matched_covariance
            and hstar_invariant
            and privileged_distinct
            and mismatch_covariance
            and update_covariance
        ),
    )


def stage10e_summary(*, atol: float = DEFAULT_ATOL) -> dict[str, object]:
    d = stage10e_modal_diagnostics(atol=atol)
    return {
        "stage": "10E",
        "weighted_modal_update_covariance_established": d.weighted_modal_update_covariance_established,
        "chart_count": d.chart_count,
        "max_weighted_prediction_covariance_residual": d.max_weighted_prediction_covariance_residual,
        "matched_epistemic_ontic_views_all_nodes": d.matched_epistemic_ontic_views_all_nodes,
        "hidden_hstar_swap_views_all_nodes": d.hidden_hstar_swap_views_all_nodes,
        "minimum_weight_mismatch_prediction_difference": d.minimum_weight_mismatch_prediction_difference,
        "max_weight_mismatch_covariance_residual": d.max_weight_mismatch_covariance_residual,
        "max_epistemic_posterior_covariance_residual": d.max_epistemic_posterior_covariance_residual,
        "max_ontic_posterior_covariance_residual": d.max_ontic_posterior_covariance_residual,
        "ontic_updated_selector_free_all_nodes": d.ontic_updated_selector_free_all_nodes,
        "next": "Stage 10F — ablation / wrong-typing / false-positive controls",
    }
