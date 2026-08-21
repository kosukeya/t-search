"""Stage 6A structural inventory and executable witness adapters.

The adapters in this module do not copy prose conclusions from Stages 1--5.
Each witness recomputes quantities through the existing stage APIs and returns a
uniform typed record that Stage 6B can consume without erasing source-domain or
tolerance metadata.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations, product
from typing import Any

import numpy as np

from .stage1 import (
    canonical_block,
    compare_blocks,
    glue_views,
    project_all_views,
    project_local_view,
    transitive_closure,
)
from .stage2_epistemic import (
    canonical_epistemic_model,
    project_epistemic_view,
    selected_history,
)
from .stage2_ontic import canonical_ontic_model, project_ontic_view
from .stage2_operational import (
    compare_operational_views,
    operationalize_epistemic_view,
    operationalize_ontic_view,
)
from .stage2_update import ontic_selected_future_fields
from .stage3 import is_bijective, u_scr
from .stage3_controls import stage3d_control_assessments, u_identity
from .stage4_transition import (
    transition_composition_residual,
    transition_expected_residual,
    transition_identity_residual,
    transition_inverse_residual,
    transition_unitarity_residual,
)
from .stage5_clock_change import (
    SUBSYSTEMS,
    physical_state_from_coefficients,
    tensor_basis_state,
)
from .stage5_cross_clock_composition import (
    cross_clock_composition_support_matrices,
    ordered_distinct_clock_triples,
)
from .stage5_operational import (
    perspective_entanglement_entropy,
    reduced_born_probability,
    transform_reduced_observable,
)
from .stage5_reductions import clock_relative_support_basis, physical_clock_reduction

Scalar = bool | int | float | str | None


@dataclass(frozen=True)
class Measurement:
    """One machine-readable measured quantity from an executable witness."""

    name: str
    value: Scalar
    unit: str | None = None


@dataclass(frozen=True)
class WitnessRecord:
    """Typed Stage 6 witness retaining source-domain and tolerance metadata."""

    witness_id: str
    source_stage: int
    domain: str
    assumptions: tuple[str, ...]
    roles: tuple[str, ...]
    measurements: tuple[Measurement, ...]
    tolerance: float | None = None

    def measurement(self, name: str) -> Scalar:
        matches = [item.value for item in self.measurements if item.name == name]
        if len(matches) != 1:
            raise KeyError(f"expected exactly one measurement named {name!r}")
        return matches[0]

    def as_dict(self) -> dict[str, Any]:
        return {
            "witness_id": self.witness_id,
            "source_stage": self.source_stage,
            "domain": self.domain,
            "assumptions": list(self.assumptions),
            "roles": list(self.roles),
            "measurements": {
                item.name: {"value": item.value, "unit": item.unit}
                for item in self.measurements
            },
            "tolerance": self.tolerance,
        }


def _measurement(name: str, value: Scalar, unit: str | None = None) -> Measurement:
    if isinstance(value, np.bool_):
        value = bool(value)
    elif isinstance(value, np.integer):
        value = int(value)
    elif isinstance(value, np.floating):
        value = float(value)
    return Measurement(name=name, value=value, unit=unit)


def stage1_reconstruction_accessibility_witness() -> WitnessRecord:
    """W1: recompute global reconstruction and one-hop local inaccessibility."""

    block = canonical_block()
    views = project_all_views(block)
    reconstructed = glue_views(views)
    comparison = compare_blocks(block, reconstructed)
    closure = transitive_closure(block)

    local_event = "a"
    remote_event = "e"
    local_view = project_local_view(block, local_event)
    remote_globally_reachable = (local_event, remote_event) in closure
    remote_in_one_hop_view = (
        remote_event in local_view.predecessors
        or remote_event in local_view.successors
        or remote_event == local_view.event_id
    )

    return WitnessRecord(
        witness_id="W1",
        source_stage=1,
        domain="canonical six-event DAG; complete labeled one-hop view family plus one local one-hop interface",
        assumptions=(
            "event IDs are retained by the complete Stage 1A view family",
            "local accessibility means membership in the declared one-hop view interface",
            "reachability is the transitive closure of the directed edge relation",
        ),
        roles=("order", "reconstructibility", "accessibility"),
        measurements=(
            _measurement("family_labeled_equal", comparison.labeled_equal),
            _measurement("family_reachability_equal", comparison.reachability_equal),
            _measurement("global_reachability_pair_count", len(closure)),
            _measurement("local_event", local_event),
            _measurement("remote_event", remote_event),
            _measurement("remote_globally_reachable", remote_globally_reachable),
            _measurement("remote_in_one_hop_view", remote_in_one_hop_view),
            _measurement("local_successor_count", len(local_view.successors)),
        ),
    )


def stage2_modal_operational_witness() -> WitnessRecord:
    """W2: recompute matched operational outputs with distinct modal semantics."""

    prefix = ("p", "n")
    epistemic_model = canonical_epistemic_model()
    ontic_model = canonical_ontic_model(actuality=prefix)
    epistemic_view = project_epistemic_view(epistemic_model, prefix)
    ontic_view = project_ontic_view(ontic_model)

    epistemic_operational = operationalize_epistemic_view(epistemic_view)
    ontic_operational = operationalize_ontic_view(ontic_view)
    comparison = compare_operational_views(epistemic_operational, ontic_operational)

    selected = selected_history(epistemic_model)
    ontic_selector_fields = ontic_selected_future_fields(ontic_model)

    return WitnessRecord(
        witness_id="W2",
        source_stage=2,
        domain="canonical Stage 2 branching substrate at Actuality prefix ('p','n') with matched 1/2-1/2 live support",
        assumptions=(
            "epistemic model contains one selected complete history with positive support",
            "ontic-extension model contains no selected-future field",
            "comparison uses only the ontology-neutral OperationalView interface",
        ),
        roles=("modality", "operational-correspondence", "underdetermination"),
        measurements=(
            _measurement("operational_equal", comparison.equal),
            _measurement("actuality_equal", comparison.actuality_equal),
            _measurement("next_events_equal", comparison.next_events_equal),
            _measurement("probabilities_equal", comparison.probabilities_equal),
            _measurement("epistemic_selected_history", repr(selected)),
            _measurement("ontic_selected_future_field_count", len(ontic_selector_fields)),
            _measurement(
                "potentiality_runtime_types_equal",
                type(epistemic_view.potentiality) is type(ontic_view.potentiality),
            ),
            _measurement(
                "epistemic_live_history_count", len(epistemic_view.potentiality.histories)
            ),
            _measurement("ontic_live_history_count", len(ontic_view.potentiality.histories)),
        ),
        tolerance=1e-12,
    )


def stage3_order_record_witness() -> WitnessRecord:
    """W3: recompute record orientation under the frozen Stage 3D controls."""

    assessments = stage3d_control_assessments()
    order = ("forward", "reversed", "symmetric", "no-record", "uniform-memory")
    measurements: list[Measurement] = []
    for name in order:
        assessment = assessments[name]
        if name == "no-record":
            declared_reversible = is_bijective(u_identity) and is_bijective(u_scr)
        else:
            # These controls retain the canonical U_rec/U_scr microscopic maps;
            # the assessment computes their bijectivity through the Stage 3 API.
            declared_reversible = assessment.microscopic_maps_reversible
        measurements.extend(
            (
                _measurement(f"{name}_orientation", assessment.orientation),
                _measurement(f"{name}_record_defined", assessment.record_defined),
                _measurement(f"{name}_record_score", assessment.record_score, "bits"),
                _measurement(
                    f"{name}_accessibility_score", assessment.accessibility_score
                ),
                _measurement(
                    f"{name}_declared_microdynamics_reversible",
                    declared_reversible,
                ),
                _measurement(
                    f"{name}_declared_position_count",
                    assessment.upper_position - assessment.lower_position + 1,
                ),
            )
        )

    return WitnessRecord(
        witness_id="W3",
        source_stage=3,
        domain="canonical reversible three-position record model plus reversed, symmetric-mixture, no-record, and uniform-memory controls",
        assumptions=(
            "position indices are neutral bookkeeping labels",
            "record-defined orientation requires nonzero agreeing information and accessibility diagnostics",
            "record orientation is not identified with phenomenal passage or modal openness",
        ),
        roles=("order", "record-direction", "accessibility", "reversibility"),
        measurements=tuple(measurements),
        tolerance=1e-12,
    )


def stage4_same_clock_transition_witness() -> WitnessRecord:
    """W4: recompute Stage 4E same-clock transition consistency."""

    d = 4
    identity = [transition_identity_residual(j, d) for j in range(d)]
    inverse = [
        transition_inverse_residual(source, target, d)
        for source, target in product(range(d), repeat=2)
    ]
    composition = [
        transition_composition_residual(source, middle, target, d)
        for source, middle, target in product(range(d), repeat=3)
    ]
    expected = [
        transition_expected_residual(source, target, d)
        for source, target in product(range(d), repeat=2)
    ]
    unitarity = [
        transition_unitarity_residual(source, target, d)
        for source, target in product(range(d), repeat=2)
    ]

    return WitnessRecord(
        witness_id="W4",
        source_stage=4,
        domain="canonical d=4 matched-energy finite Page-Wootters-style physical clock family",
        assumptions=(
            "transition maps are normalized physical reduction/reconstruction maps on the declared physical sector",
            "one fixed physical clock subsystem is used",
            "clock-relative transition consistency is not interpreted as a temporal arrow",
        ),
        roles=("perspective", "same-clock-transition", "composition", "reversibility"),
        measurements=(
            _measurement("clock_reading_count", d),
            _measurement("max_identity_residual", max(identity)),
            _measurement("max_inverse_residual", max(inverse)),
            _measurement("max_composition_residual", max(composition)),
            _measurement("max_expected_transition_residual", max(expected)),
            _measurement("max_unitarity_residual", max(unitarity)),
        ),
        tolerance=1e-10,
    )


def _stage5_generic_physical_state() -> np.ndarray:
    raw = np.array(
        [
            1.0 + 0.2j,
            -0.4 + 0.7j,
            0.3 - 0.1j,
            0.8 + 0.5j,
            -0.2 - 0.6j,
            0.9 - 0.3j,
            0.1 + 0.4j,
        ],
        dtype=np.complex128,
    )
    return physical_state_from_coefficients(raw, normalize=True)


def _stage5_support_projector(clock: str) -> np.ndarray:
    basis = clock_relative_support_basis(clock)
    coordinates = np.array(
        [1.0, 0.4j, -0.3 + 0.2j, 0.5, -0.1j, 0.25, -0.45],
        dtype=np.complex128,
    )
    coordinates /= np.linalg.norm(coordinates)
    ket = basis @ coordinates
    return np.outer(ket, ket.conj())


def _stage5_entanglement_control_state() -> np.ndarray:
    return (
        tensor_basis_state(+1, -1, 0) + tensor_basis_state(+1, 0, -1)
    ) / np.sqrt(2.0)


def stage5_cross_clock_operational_witness() -> WitnessRecord:
    """W5: recompute genuine clock composition, Born covariance, and entanglement."""

    d = 3
    composition_residuals: list[float] = []
    for source, middle, target in ordered_distinct_clock_triples():
        for source_index, middle_index, target_index in product(range(d), repeat=3):
            composed, direct = cross_clock_composition_support_matrices(
                target,
                target_index,
                middle,
                middle_index,
                source,
                source_index,
                d,
            )
            composition_residuals.append(float(np.linalg.norm(composed - direct)))

    physical_state = _stage5_generic_physical_state()
    born_residuals: list[float] = []
    for source, target in permutations(SUBSYSTEMS, 2):
        source_projector = _stage5_support_projector(source)
        for source_index, target_index in product(range(d), repeat=2):
            source_state = physical_clock_reduction(
                physical_state, source, source_index, d
            )
            target_state = physical_clock_reduction(
                physical_state, target, target_index, d
            )
            target_projector = transform_reduced_observable(
                source_projector,
                target,
                target_index,
                source,
                source_index,
                d,
            )
            source_probability = reduced_born_probability(
                source_state, source_projector, d
            )
            target_probability = reduced_born_probability(
                target_state, target_projector, d
            )
            born_residuals.append(abs(source_probability - target_probability))

    entanglement_state = _stage5_entanglement_control_state()
    entropies = {
        clock: perspective_entanglement_entropy(entanglement_state, clock, 0, d)
        for clock in SUBSYSTEMS
    }

    return WitnessRecord(
        witness_id="W5",
        source_stage=5,
        domain="canonical symmetric three-qutrit constrained model with all distinct clock routes and transformed support observables",
        assumptions=(
            "clock changes act only on declared physical support subspaces",
            "corresponding observables are transported with the clock-change map",
            "reduced bipartite entanglement is allowed to be perspective-dependent",
        ),
        roles=(
            "perspective",
            "cross-clock-composition",
            "operational-correspondence",
            "perspective-dependent-structure",
        ),
        measurements=(
            _measurement("three_clock_route_count", 6 * d**3),
            _measurement(
                "max_cross_clock_composition_residual", max(composition_residuals)
            ),
            _measurement("max_born_probability_residual", max(born_residuals)),
            _measurement("entanglement_A_bits", entropies["A"], "bits"),
            _measurement("entanglement_B_bits", entropies["B"], "bits"),
            _measurement("entanglement_C_bits", entropies["C"], "bits"),
            _measurement(
                "entanglement_perspective_dependent",
                max(entropies.values()) - min(entropies.values()) > 1e-10,
            ),
        ),
        tolerance=1e-10,
    )


def build_stage6a_inventory() -> tuple[WitnessRecord, ...]:
    """Recompute and return the complete Stage 6A W1--W5 inventory."""

    inventory = (
        stage1_reconstruction_accessibility_witness(),
        stage2_modal_operational_witness(),
        stage3_order_record_witness(),
        stage4_same_clock_transition_witness(),
        stage5_cross_clock_operational_witness(),
    )
    ids = tuple(record.witness_id for record in inventory)
    if ids != ("W1", "W2", "W3", "W4", "W5"):
        raise RuntimeError("Stage 6A witness inventory is incomplete or misordered")
    return inventory


def stage6a_inventory_rows() -> tuple[dict[str, Any], ...]:
    """Return JSON-friendly rows without collapsing measurements to prose labels."""

    return tuple(record.as_dict() for record in build_stage6a_inventory())
