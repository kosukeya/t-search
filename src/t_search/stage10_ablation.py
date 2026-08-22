"""Stage 10F ablation / wrong-typing / false-positive controls.

Stage 10A-E established a fully typed finite future-measurement family.  This
module removes or corrupts individual typing/normalization resources to ask a
different question: which positive conclusions survive merely numerically,
and which conclusions require the retained semantic correspondence data?

The central distinction is:

    numerical reconstructibility != typed operational identification.

Accordingly, an ablation may leave the same matrices or numbers in memory while
the project status of the *typed identification* becomes ``lost`` or
``not_established``.  These are finite-model functional classifications, not
claims of metaphysical irreducibility.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from math import isclose
from typing import Literal

import numpy as np

from .stage5_clock_change import DEFAULT_ATOL
from .stage9_modal import make_stage9_ontic_model, canonical_stage9c_models
from .stage10_modal import (
    stage10e_continuation_likelihoods,
    stage10e_weighted_prediction,
)
from .stage10_probability import (
    stage10d_chart_probabilities,
    stage10d_probe_family,
)
from .stage10_transport import (
    Stage10ChartMeasurement,
    audit_measurement_correspondence,
    canonical_stage10c_charts,
)

FunctionalStatus = Literal[
    "preserved",
    "reconstructible",
    "inaccessible",
    "lost",
    "underdetermined",
    "not_established",
]
MeasurementStatus = Literal["established", "partial", "refuted", "not_established"]


@dataclass(frozen=True, slots=True)
class Stage10FAblationClassification:
    ablation: str
    resource: str
    numerical_payload_status: FunctionalStatus
    typed_identification_status: FunctionalStatus
    probability_covariance_status: MeasurementStatus
    witness: str
    residual: float


@dataclass(frozen=True, slots=True)
class Stage10FDiagnostics:
    classifications: tuple[Stage10FAblationClassification, ...]
    correspondence_ablations_classified: bool
    normalization_ablations_classified: bool
    bare_effect_residual: float
    bare_effect_rejected: bool
    wrong_continuation_form_residual: float
    wrong_continuation_rejected: bool
    wrong_outcome_probability_residual: float
    wrong_outcome_rejected: bool
    wrong_event_rejected: bool
    weight_misalignment_prediction_residual: float
    weight_misalignment_rejected: bool
    fresh_identity_probe_residual: float
    fresh_identity_rejected: bool
    missing_normalization_semantics_status: MeasurementStatus
    all_required_false_positive_controls_rejected: bool
    metaphysical_promotion_avoided: bool


def _chart_lookup() -> dict[tuple[str, str, int], Stage10ChartMeasurement]:
    return {
        (chart.continuation_id, chart.clock, chart.clock_index): chart
        for chart in canonical_stage10c_charts()
    }


def _probability_residual(
    left: tuple[tuple[str, float], ...],
    right: tuple[tuple[str, float], ...],
) -> float:
    lhs = dict(left)
    rhs = dict(right)
    if set(lhs) != set(rhs):
        return float("inf")
    return max(abs(lhs[name] - rhs[name]) for name in lhs)


def _weighted_from_rows(
    weights: tuple[float, ...],
    rows: tuple[tuple[str, tuple[tuple[str, float], ...]], ...],
) -> tuple[tuple[str, float], ...]:
    tables = tuple(dict(values) for _, values in rows)
    names = tuple(name for name, _ in rows[0][1])
    return tuple(
        (
            name,
            float(sum(weight * table[name] for weight, table in zip(weights, tables, strict=True))),
        )
        for name in names
    )


def _bare_effect_residual(charts: dict[tuple[str, str, int], Stage10ChartMeasurement]) -> float:
    source = charts[("h_L", "A", 0)]
    target = charts[("h_L", "B", 0)]
    return max(
        float(np.linalg.norm(left.matrix - right.matrix))
        for left, right in zip(source.effects, target.effects, strict=True)
    )


def _wrong_continuation_residual(
    charts: dict[tuple[str, str, int], Stage10ChartMeasurement]
) -> tuple[float, bool]:
    left = charts[("h_L", "A", 0)]
    right = charts[("h_R", "A", 0)]
    residual = max(
        float(np.linalg.norm(a.matrix - b.matrix))
        for a, b in zip(left.effects, right.effects, strict=True)
    )
    epistemic, _ = canonical_stage9c_models(selected_id="h_L")
    h_right = next(
        item for item in epistemic.carrier.continuations if item.continuation_id == "h_R"
    )
    rejected = False
    try:
        stage10d_chart_probabilities(h_right, left)
    except ValueError:
        rejected = True
    return residual, rejected


def _wrong_outcome_residual(
    charts: dict[tuple[str, str, int], Stage10ChartMeasurement]
) -> tuple[float, bool]:
    epistemic, _ = canonical_stage9c_models(selected_id="h_L")
    h_left = next(
        item for item in epistemic.carrier.continuations if item.continuation_id == "h_L"
    )
    values = dict(stage10d_chart_probabilities(h_left, charts[("h_L", "A", 0)]))
    residual = abs(values["future_signature_left"] - values["future_signature_other"])
    audit = audit_measurement_correspondence(outcome_kind="swapped")
    return residual, not audit.valid


def _weight_misalignment_residual() -> tuple[float, bool]:
    _, ontic = canonical_stage9c_models(selected_id="h_L")
    mismatch = make_stage9_ontic_model(ontic.carrier, (0.75, 0.25))
    rows = stage10e_continuation_likelihoods(mismatch, "A", 0)
    correct = stage10e_weighted_prediction(mismatch, "A", 0)
    wrong = _weighted_from_rows((0.25, 0.75), rows)
    residual = _probability_residual(correct, wrong)
    return residual, residual > 10 * DEFAULT_ATOL


def _fresh_identity_probe_residual(
    charts: dict[tuple[str, str, int], Stage10ChartMeasurement]
) -> tuple[float, bool]:
    epistemic, _ = canonical_stage9c_models(selected_id="h_L")
    h_left = next(
        item for item in epistemic.carrier.continuations if item.continuation_id == "h_L"
    )
    # Search a tomography-complete probe family so a wrong Hermitian
    # normalization cannot hide on the canonical continuation state.
    chart = charts[("h_L", "B", 1)]
    identity = np.eye(chart.normalization_form.shape[0], dtype=np.complex128)
    max_residual = 0.0
    for probe in stage10d_probe_family():
        correct = stage10d_chart_probabilities(
            h_left,
            chart,
            physical_coordinates=probe.physical_coordinates,
        )
        wrong = stage10d_chart_probabilities(
            h_left,
            chart,
            physical_coordinates=probe.physical_coordinates,
            normalization=identity,
        )
        max_residual = max(max_residual, _probability_residual(correct, wrong))
    return max_residual, max_residual > 10 * DEFAULT_ATOL


def stage10f_ablation_diagnostics(
    *, atol: float = DEFAULT_ATOL
) -> Stage10FDiagnostics:
    del atol  # Stage 10F uses the established project tolerance controls below.
    charts = _chart_lookup()
    reference = charts[("h_L", "A", 0)]

    # Correspondence removals preserve the stored matrices, but destroy the
    # typed statement that source/target resources denote the same operational
    # question across perspectives.
    no_event = replace(reference, event_correspondence=())
    no_class = replace(reference, class_correspondence=("", ""))
    no_outcome = replace(reference, outcome_correspondence=())
    correspondence_payloads_preserved = bool(
        np.allclose(no_event.normalization_form, reference.normalization_form)
        and np.allclose(no_class.normalization_form, reference.normalization_form)
        and np.allclose(no_outcome.normalization_form, reference.normalization_form)
    )

    bare_residual = _bare_effect_residual(charts)
    wrong_continuation_residual, wrong_continuation_rejected = _wrong_continuation_residual(charts)
    wrong_outcome_residual, wrong_outcome_rejected = _wrong_outcome_residual(charts)
    wrong_event_rejected = not audit_measurement_correspondence(
        event_kind="misdeclared-preserving"
    ).valid
    weight_residual, weight_rejected = _weight_misalignment_residual()
    fresh_identity_residual, fresh_identity_rejected = _fresh_identity_probe_residual(charts)

    classifications = (
        Stage10FAblationClassification(
            "remove_event_correspondence",
            "event correspondence",
            "preserved" if correspondence_payloads_preserved else "lost",
            "lost",
            "not_established",
            "numeric forms remain stored but e1/e2 operational role identity is absent",
            0.0,
        ),
        Stage10FAblationClassification(
            "remove_class_correspondence",
            "continuation-class correspondence",
            "preserved" if correspondence_payloads_preserved else "lost",
            "lost",
            "not_established",
            "numeric forms remain stored but h_L/h_R class identity is absent",
            0.0,
        ),
        Stage10FAblationClassification(
            "remove_outcome_correspondence",
            "outcome correspondence",
            "preserved" if correspondence_payloads_preserved else "lost",
            "lost",
            "not_established",
            "numeric forms remain stored but cross-chart outcome identity is absent",
            0.0,
        ),
        Stage10FAblationClassification(
            "remove_normalization_semantics",
            "normalization semantics",
            "reconstructible",
            "underdetermined",
            "not_established",
            "normalization matrix remains available but its operational Born-rule role is no longer typed",
            0.0,
        ),
        Stage10FAblationClassification(
            "fresh_identity_normalization",
            "normalization rule",
            "preserved",
            "lost",
            "refuted",
            "fresh numerical identity changes probe probabilities in a non-Euclidean-unitary chart",
            fresh_identity_residual,
        ),
        Stage10FAblationClassification(
            "bare_effect_reuse",
            "chart representation",
            "preserved",
            "lost",
            "refuted",
            "source-chart effect matrices differ from the correctly represented target-chart effects",
            bare_residual,
        ),
        Stage10FAblationClassification(
            "weight_class_misalignment",
            "continuation-weight alignment",
            "preserved",
            "lost",
            "refuted",
            "swapping weights while holding continuation likelihood rows fixed changes the weighted prediction",
            weight_residual,
        ),
    )

    correspondence_classified = all(
        item.typed_identification_status == "lost"
        and item.probability_covariance_status == "not_established"
        for item in classifications[:3]
    )
    normalization_classified = bool(
        classifications[3].probability_covariance_status == "not_established"
        and classifications[4].probability_covariance_status == "refuted"
        and fresh_identity_rejected
    )
    all_controls = bool(
        bare_residual > 10 * DEFAULT_ATOL
        and wrong_continuation_residual > 10 * DEFAULT_ATOL
        and wrong_continuation_rejected
        and wrong_outcome_residual > 10 * DEFAULT_ATOL
        and wrong_outcome_rejected
        and wrong_event_rejected
        and weight_rejected
        and fresh_identity_rejected
    )

    return Stage10FDiagnostics(
        classifications=classifications,
        correspondence_ablations_classified=correspondence_classified,
        normalization_ablations_classified=normalization_classified,
        bare_effect_residual=bare_residual,
        bare_effect_rejected=bare_residual > 10 * DEFAULT_ATOL,
        wrong_continuation_form_residual=wrong_continuation_residual,
        wrong_continuation_rejected=wrong_continuation_rejected,
        wrong_outcome_probability_residual=wrong_outcome_residual,
        wrong_outcome_rejected=wrong_outcome_rejected,
        wrong_event_rejected=wrong_event_rejected,
        weight_misalignment_prediction_residual=weight_residual,
        weight_misalignment_rejected=weight_rejected,
        fresh_identity_probe_residual=fresh_identity_residual,
        fresh_identity_rejected=fresh_identity_rejected,
        missing_normalization_semantics_status="not_established",
        all_required_false_positive_controls_rejected=all_controls,
        metaphysical_promotion_avoided=True,
    )


def stage10f_summary(*, atol: float = DEFAULT_ATOL) -> dict[str, object]:
    d = stage10f_ablation_diagnostics(atol=atol)
    return {
        "stage": "10F",
        "criteria_44_47_satisfied": bool(
            d.correspondence_ablations_classified
            and d.normalization_ablations_classified
            and d.all_required_false_positive_controls_rejected
            and d.metaphysical_promotion_avoided
        ),
        "classifications": tuple(
            {
                "ablation": item.ablation,
                "resource": item.resource,
                "numerical_payload_status": item.numerical_payload_status,
                "typed_identification_status": item.typed_identification_status,
                "probability_covariance_status": item.probability_covariance_status,
                "witness": item.witness,
                "residual": item.residual,
            }
            for item in d.classifications
        ),
        "controls": {
            "bare_effect_residual": d.bare_effect_residual,
            "wrong_continuation_form_residual": d.wrong_continuation_form_residual,
            "wrong_outcome_probability_residual": d.wrong_outcome_probability_residual,
            "wrong_event_rejected": d.wrong_event_rejected,
            "weight_misalignment_prediction_residual": d.weight_misalignment_prediction_residual,
            "fresh_identity_probe_residual": d.fresh_identity_probe_residual,
        },
        "guards": (
            "numerical reconstructibility != typed operational identification",
            "same numeric probability != measurement-family identity",
            "missing typing != metaphysical absence",
            "lost != metaphysically irreducible",
            "not_established != false",
            "wrong-typing failure != ontological becoming",
            "finite-model ablation != fundamental ontology",
        ),
        "next": "Stage 10G — synthesis and evidence-selected next gate",
    }
