"""Stage 6E record and modality transport utilities.

Stage 6E adds two further compatibility questions to the typed Stage 6 scaffold:

- how record orientation and locally accessible record information transform under
  explicit event correspondence;
- how Stage 2 Potentiality/extension structures transport under an explicit map on
  partial descriptions.

The module deliberately keeps record transport, modal transport, operational
correspondence, and phenomenal passage distinct.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Iterable

from .stage2 import (
    BranchingStructure,
    EventId,
    History,
    Prefix,
    canonical_stage2_substrate,
    make_branching_structure,
)
from .stage2_epistemic import (
    EpistemicHistoryModel,
    make_epistemic_history_model,
    canonical_epistemic_model,
    project_epistemic_view,
)
from .stage2_ontic import (
    OnticExtensionModel,
    make_ontic_extension_model,
    canonical_ontic_model,
    project_ontic_view,
)
from .stage2_operational import (
    OperationalView,
    compare_operational_views,
    operationalize_epistemic_view,
    operationalize_ontic_view,
)
from .stage3 import (
    all_microstates,
    canonical_reversed_ensemble,
    u_rec,
    u_scr,
)
from .stage3_accessibility import (
    LocalAccessPolicy,
    make_local_observation_ensemble,
    record_readout_accessibility_arrow_score,
    record_readout_arrow_score,
)
from .stage3_asymmetry import AsymmetricRecordModel, assess_record_orientation
from .stage3_diagnostics import accessibility_profile, record_profile
from .stage3_local import Stage3RecordBlock, canonical_record_block
from .stage6_compatibility import EventCorrespondence
from .stage6_partial_atlas import PerspectiveNode


RECORD_EVENT_TO_POSITION: dict[str, int] = {"e0": 0, "e1": 1, "e2": 2}
CANONICAL_SOURCE_PERSPECTIVE = PerspectiveNode("C", 0)
CANONICAL_TARGET_PERSPECTIVE = PerspectiveNode("B", 2)


@dataclass(frozen=True)
class RecordVariableCorrespondence:
    """Declare which Stage 3 variables count as corresponding record variables."""

    source_record_component: str = "m"
    target_record_component: str = "m"
    source_target_component: str = "x"
    target_target_component: str = "x"
    source_current_event: str = "e1"

    def as_dict(self) -> dict[str, Any]:
        return {
            "source_record_component": self.source_record_component,
            "target_record_component": self.target_record_component,
            "source_target_component": self.source_target_component,
            "target_target_component": self.target_target_component,
            "source_current_event": self.source_current_event,
        }


@dataclass(frozen=True)
class LocalRecordAccessDiagnostics:
    """What the declared local interface can access about the record arrow."""

    record_exposed: bool
    record_error_probability: float
    record_score: float | None
    accessibility_score: float | None

    def as_dict(self) -> dict[str, Any]:
        return {
            "record_exposed": self.record_exposed,
            "record_error_probability": self.record_error_probability,
            "record_score": self.record_score,
            "accessibility_score": self.accessibility_score,
        }


@dataclass(frozen=True)
class RecordTransportDiagnostics:
    """Global record covariance plus perspective-specific accessibility metadata."""

    source: PerspectiveNode
    target: PerspectiveNode
    correspondence_orientation: str
    variable_correspondence: RecordVariableCorrespondence
    source_orientation: str
    target_orientation: str
    max_information_profile_residual: float
    max_accessibility_profile_residual: float
    record_score_transport_residual: float
    accessibility_score_transport_residual: float
    globally_compatible: bool
    source_local: LocalRecordAccessDiagnostics
    target_local: LocalRecordAccessDiagnostics

    def as_dict(self) -> dict[str, Any]:
        return {
            "source": self.source.label,
            "target": self.target.label,
            "correspondence_orientation": self.correspondence_orientation,
            "variable_correspondence": self.variable_correspondence.as_dict(),
            "source_orientation": self.source_orientation,
            "target_orientation": self.target_orientation,
            "max_information_profile_residual": self.max_information_profile_residual,
            "max_accessibility_profile_residual": self.max_accessibility_profile_residual,
            "record_score_transport_residual": self.record_score_transport_residual,
            "accessibility_score_transport_residual": self.accessibility_score_transport_residual,
            "globally_compatible": self.globally_compatible,
            "source_local": self.source_local.as_dict(),
            "target_local": self.target_local.as_dict(),
        }


@dataclass(frozen=True)
class ModalDescriptionMap:
    """Explicit event renaming F_{q<-p} used to transport Stage 2 descriptions."""

    source: PerspectiveNode
    target: PerspectiveNode
    event_mapping: tuple[tuple[EventId, EventId], ...]

    def __post_init__(self) -> None:
        source_events = [source for source, _ in self.event_mapping]
        target_events = [target for _, target in self.event_mapping]
        if len(set(source_events)) != len(source_events):
            raise ValueError("modal description map contains duplicate source events")
        if len(set(target_events)) != len(target_events):
            raise ValueError("modal description map must be injective on declared events")

    def event(self, source_event: EventId) -> EventId:
        matches = [target for source, target in self.event_mapping if source == source_event]
        if not matches:
            raise KeyError(f"modal description map has no image for {source_event!r}")
        return matches[0]

    def prefix(self, prefix: Prefix) -> Prefix:
        return tuple(self.event(event) for event in prefix)

    def history(self, history: History) -> History:
        return tuple(self.event(event) for event in history)

    def as_dict(self) -> dict[str, Any]:
        return {
            "source": self.source.label,
            "target": self.target.label,
            "event_mapping": dict(self.event_mapping),
        }


@dataclass(frozen=True)
class ExtensionTransportDiagnostics:
    """Check the declared relation F_*(Ext_p(D)) ~= Ext_q(F(D))."""

    relation: str
    source_extension_count: int
    target_extension_count: int
    mapped_extension_count: int
    invalid_mapped_extension_count: int
    missing_target_extension_count: int
    duplicate_mapped_extension_count: int
    relation_holds: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "relation": self.relation,
            "source_extension_count": self.source_extension_count,
            "target_extension_count": self.target_extension_count,
            "mapped_extension_count": self.mapped_extension_count,
            "invalid_mapped_extension_count": self.invalid_mapped_extension_count,
            "missing_target_extension_count": self.missing_target_extension_count,
            "duplicate_mapped_extension_count": self.duplicate_mapped_extension_count,
            "relation_holds": self.relation_holds,
        }


@dataclass(frozen=True)
class ModalTransportDiagnostics:
    """Typed modal transport plus Stage 2 operational-underdetermination guard."""

    source: PerspectiveNode
    target: PerspectiveNode
    epistemic_extensions: ExtensionTransportDiagnostics
    ontic_extensions: ExtensionTransportDiagnostics
    source_operational_equal: bool
    target_operational_equal: bool
    epistemic_operational_transport_equal: bool
    ontic_operational_transport_equal: bool
    source_potentiality_types_distinct: bool
    target_potentiality_types_distinct: bool
    epistemic_selected_history_present: bool
    ontic_selected_future_field_present: bool
    underdetermination_preserved: bool

    def as_dict(self) -> dict[str, Any]:
        return {
            "source": self.source.label,
            "target": self.target.label,
            "epistemic_extensions": self.epistemic_extensions.as_dict(),
            "ontic_extensions": self.ontic_extensions.as_dict(),
            "source_operational_equal": self.source_operational_equal,
            "target_operational_equal": self.target_operational_equal,
            "epistemic_operational_transport_equal": self.epistemic_operational_transport_equal,
            "ontic_operational_transport_equal": self.ontic_operational_transport_equal,
            "source_potentiality_types_distinct": self.source_potentiality_types_distinct,
            "target_potentiality_types_distinct": self.target_potentiality_types_distinct,
            "epistemic_selected_history_present": self.epistemic_selected_history_present,
            "ontic_selected_future_field_present": self.ontic_selected_future_field_present,
            "underdetermination_preserved": self.underdetermination_preserved,
        }


@dataclass(frozen=True)
class ModalMismatchDiagnostics:
    """Negative control: event bijection that does not preserve extension structure."""

    event_map_is_bijective: bool
    epistemic_relation_holds: bool
    ontic_relation_holds: bool
    epistemic_invalid_mapped_extension_count: int
    ontic_invalid_mapped_extension_count: int

    def as_dict(self) -> dict[str, Any]:
        return {
            "event_map_is_bijective": self.event_map_is_bijective,
            "epistemic_relation_holds": self.epistemic_relation_holds,
            "ontic_relation_holds": self.ontic_relation_holds,
            "epistemic_invalid_mapped_extension_count": self.epistemic_invalid_mapped_extension_count,
            "ontic_invalid_mapped_extension_count": self.ontic_invalid_mapped_extension_count,
        }


def preserving_record_correspondence(
    source: PerspectiveNode = CANONICAL_SOURCE_PERSPECTIVE,
    target: PerspectiveNode = CANONICAL_TARGET_PERSPECTIVE,
) -> EventCorrespondence:
    """Identity-on-event-labels, explicitly orientation-preserving."""

    return EventCorrespondence(
        source=source,
        target=target,
        mapping=(("e0", "e0"), ("e1", "e1"), ("e2", "e2")),
        orientation="preserving",
    )


def reversing_record_correspondence(
    source: PerspectiveNode = CANONICAL_SOURCE_PERSPECTIVE,
    target: PerspectiveNode = CANONICAL_TARGET_PERSPECTIVE,
) -> EventCorrespondence:
    """Reverse the modeled history orientation while keeping e1 as the center."""

    return EventCorrespondence(
        source=source,
        target=target,
        mapping=(("e0", "e2"), ("e1", "e1"), ("e2", "e0")),
        orientation="reversing",
    )


def misdeclared_record_correspondence(
    source: PerspectiveNode = CANONICAL_SOURCE_PERSPECTIVE,
    target: PerspectiveNode = CANONICAL_TARGET_PERSPECTIVE,
) -> EventCorrespondence:
    """Same event reversal as the valid control, but falsely declared preserving."""

    return EventCorrespondence(
        source=source,
        target=target,
        mapping=(("e0", "e2"), ("e1", "e1"), ("e2", "e0")),
        orientation="preserving",
    )


def reversed_record_block() -> Stage3RecordBlock:
    """Represent the Stage 3 reversed ensemble with inverse maps in reverse order."""

    return Stage3RecordBlock(
        state_space=all_microstates(),
        first_update=u_scr,
        second_update=u_rec,
        ensemble=canonical_reversed_ensemble(),
    )


def _event_position(label: str) -> int:
    try:
        return RECORD_EVENT_TO_POSITION[label]
    except KeyError as exc:
        raise KeyError(f"record transport has no declared Stage 3 position for {label!r}") from exc


def _local_access(
    block: Stage3RecordBlock,
    policy: LocalAccessPolicy,
    *,
    current_position: int,
) -> LocalRecordAccessDiagnostics:
    if not policy.expose_m:
        return LocalRecordAccessDiagnostics(
            record_exposed=False,
            record_error_probability=float(policy.record_error_probability),
            record_score=None,
            accessibility_score=None,
        )

    observation = make_local_observation_ensemble(
        block,
        policy,
        position=current_position,
    )
    return LocalRecordAccessDiagnostics(
        record_exposed=True,
        record_error_probability=float(policy.record_error_probability),
        record_score=record_readout_arrow_score(observation),
        accessibility_score=record_readout_accessibility_arrow_score(observation),
    )


def record_transport_diagnostics(
    source_block: Stage3RecordBlock,
    target_block: Stage3RecordBlock,
    correspondence: EventCorrespondence,
    *,
    source_policy: LocalAccessPolicy = LocalAccessPolicy(expose_x=False, expose_m=True),
    target_policy: LocalAccessPolicy = LocalAccessPolicy(expose_x=False, expose_m=True),
    variable_correspondence: RecordVariableCorrespondence = RecordVariableCorrespondence(),
    tolerance: float = 1e-12,
) -> RecordTransportDiagnostics:
    """Test record/profile covariance under an explicit event correspondence.

    The global covariance calculation uses the complete Stage 3 ensembles.
    Local access diagnostics are reported separately and never used to infer
    global absence when a local record field is hidden or noisy.
    """

    source_current_label = variable_correspondence.source_current_event
    target_current_label = correspondence.target_label(source_current_label)
    source_current = _event_position(source_current_label)
    target_current = _event_position(target_current_label)

    source_profile = record_profile(
        source_block.ensemble,
        current_position=source_current,
        record_component=variable_correspondence.source_record_component,
        target_component=variable_correspondence.source_target_component,
    )
    target_profile = record_profile(
        target_block.ensemble,
        current_position=target_current,
        record_component=variable_correspondence.target_record_component,
        target_component=variable_correspondence.target_target_component,
    )
    source_access_profile = accessibility_profile(
        source_block.ensemble,
        current_position=source_current,
        record_component=variable_correspondence.source_record_component,
        target_component=variable_correspondence.source_target_component,
    )
    target_access_profile = accessibility_profile(
        target_block.ensemble,
        current_position=target_current,
        record_component=variable_correspondence.target_record_component,
        target_component=variable_correspondence.target_target_component,
    )

    information_residuals: list[float] = []
    accessibility_residuals: list[float] = []
    for source_event, source_position in RECORD_EVENT_TO_POSITION.items():
        target_event = correspondence.target_label(source_event)
        target_position = _event_position(target_event)
        information_residuals.append(
            abs(source_profile[source_position] - target_profile[target_position])
        )
        accessibility_residuals.append(
            abs(source_access_profile[source_position] - target_access_profile[target_position])
        )

    source_assessment = assess_record_orientation(
        AsymmetricRecordModel(ensemble=source_block.ensemble, current_position=source_current)
    )
    target_assessment = assess_record_orientation(
        AsymmetricRecordModel(ensemble=target_block.ensemble, current_position=target_current)
    )

    expected_sign = 1.0 if correspondence.orientation == "preserving" else -1.0
    record_score_residual = abs(
        target_assessment.record_score - expected_sign * source_assessment.record_score
    )
    accessibility_score_residual = abs(
        target_assessment.accessibility_score
        - expected_sign * source_assessment.accessibility_score
    )

    max_information_residual = max(information_residuals, default=0.0)
    max_accessibility_residual = max(accessibility_residuals, default=0.0)
    globally_compatible = (
        max_information_residual <= tolerance
        and max_accessibility_residual <= tolerance
        and record_score_residual <= tolerance
        and accessibility_score_residual <= tolerance
    )

    return RecordTransportDiagnostics(
        source=correspondence.source,
        target=correspondence.target,
        correspondence_orientation=correspondence.orientation,
        variable_correspondence=variable_correspondence,
        source_orientation=source_assessment.orientation,
        target_orientation=target_assessment.orientation,
        max_information_profile_residual=max_information_residual,
        max_accessibility_profile_residual=max_accessibility_residual,
        record_score_transport_residual=record_score_residual,
        accessibility_score_transport_residual=accessibility_score_residual,
        globally_compatible=globally_compatible,
        source_local=_local_access(source_block, source_policy, current_position=source_current),
        target_local=_local_access(target_block, target_policy, current_position=target_current),
    )


def canonical_preserving_record_transport() -> RecordTransportDiagnostics:
    return record_transport_diagnostics(
        canonical_record_block(),
        canonical_record_block(),
        preserving_record_correspondence(),
    )


def canonical_reversing_record_transport() -> RecordTransportDiagnostics:
    return record_transport_diagnostics(
        canonical_record_block(),
        reversed_record_block(),
        reversing_record_correspondence(),
    )


def record_orientation_mismatch_control() -> RecordTransportDiagnostics:
    """Keep source/reversed target fixed but misdeclare the reversal as preserving."""

    return record_transport_diagnostics(
        canonical_record_block(),
        reversed_record_block(),
        misdeclared_record_correspondence(),
    )


def record_accessibility_controls() -> dict[str, RecordTransportDiagnostics]:
    """Hold global record structure fixed while varying the target local interface."""

    source = canonical_record_block()
    target = canonical_record_block()
    chi = preserving_record_correspondence()
    exact = LocalAccessPolicy(expose_x=False, expose_m=True)
    hidden = LocalAccessPolicy(expose_x=False, expose_m=False)
    maximally_noisy = LocalAccessPolicy(
        expose_x=False,
        expose_m=True,
        record_error_probability=Fraction(1, 2),
    )
    return {
        "exact": record_transport_diagnostics(
            source,
            target,
            chi,
            source_policy=exact,
            target_policy=exact,
        ),
        "target-hidden": record_transport_diagnostics(
            source,
            target,
            chi,
            source_policy=exact,
            target_policy=hidden,
        ),
        "target-maximally-noisy": record_transport_diagnostics(
            source,
            target,
            chi,
            source_policy=exact,
            target_policy=maximally_noisy,
        ),
    }


def canonical_modal_description_map(
    source: PerspectiveNode = CANONICAL_SOURCE_PERSPECTIVE,
    target: PerspectiveNode = CANONICAL_TARGET_PERSPECTIVE,
) -> ModalDescriptionMap:
    return ModalDescriptionMap(
        source=source,
        target=target,
        event_mapping=(
            ("p", "q_p"),
            ("n", "q_n"),
            ("l1", "q_l1"),
            ("l2", "q_l2"),
            ("r1", "q_r1"),
        ),
    )


def mismatched_modal_description_map(
    source: PerspectiveNode = CANONICAL_SOURCE_PERSPECTIVE,
    target: PerspectiveNode = CANONICAL_TARGET_PERSPECTIVE,
) -> ModalDescriptionMap:
    """Bijective event renaming that does not preserve the target branch structure."""

    return ModalDescriptionMap(
        source=source,
        target=target,
        event_mapping=(
            ("p", "q_p"),
            ("n", "q_n"),
            ("l1", "q_l1"),
            ("l2", "q_r1"),
            ("r1", "q_l2"),
        ),
    )


def renamed_modal_substrate(
    source_substrate: BranchingStructure,
    description_map: ModalDescriptionMap,
) -> BranchingStructure:
    """Push the neutral Stage 2 branching substrate through an event renaming."""

    return make_branching_structure(
        events={description_map.event(event) for event in source_substrate.events},
        direct_edges={
            (description_map.event(source), description_map.event(target))
            for source, target in source_substrate.direct_edges
        },
        root=description_map.event(source_substrate.root),
    )


def transport_epistemic_model(
    source_model: EpistemicHistoryModel,
    target_substrate: BranchingStructure,
    description_map: ModalDescriptionMap,
) -> EpistemicHistoryModel:
    mapped_weights = {
        description_map.history(history): weight
        for history, weight in source_model.belief_weights
    }
    return make_epistemic_history_model(
        target_substrate,
        description_map.history(source_model.selected_history),
        mapped_weights,
    )


def transport_ontic_model(
    source_model: OnticExtensionModel,
    target_substrate: BranchingStructure,
    description_map: ModalDescriptionMap,
) -> OnticExtensionModel:
    mapped_weights = {
        description_map.history(history): weight
        for history, weight in source_model.extension_weights
    }
    return make_ontic_extension_model(
        target_substrate,
        description_map.prefix(source_model.actuality),
        mapped_weights,
    )


def extension_transport_diagnostics(
    source_histories: Iterable[History],
    target_histories: Iterable[History],
    description_map: ModalDescriptionMap,
) -> ExtensionTransportDiagnostics:
    """Test the explicitly declared relation: bijection of complete extensions."""

    source_tuple = tuple(source_histories)
    target_tuple = tuple(target_histories)
    mapped = tuple(description_map.history(history) for history in source_tuple)
    target_set = set(target_tuple)
    mapped_set = set(mapped)
    invalid = [history for history in mapped if history not in target_set]
    missing = [history for history in target_tuple if history not in mapped_set]
    duplicate_count = len(mapped) - len(mapped_set)
    relation_holds = (
        not invalid
        and not missing
        and duplicate_count == 0
        and len(source_tuple) == len(target_tuple) == len(mapped)
    )
    return ExtensionTransportDiagnostics(
        relation="bijection",
        source_extension_count=len(source_tuple),
        target_extension_count=len(target_tuple),
        mapped_extension_count=len(mapped),
        invalid_mapped_extension_count=len(invalid),
        missing_target_extension_count=len(missing),
        duplicate_mapped_extension_count=duplicate_count,
        relation_holds=relation_holds,
    )


def transport_operational_view(
    view: OperationalView,
    description_map: ModalDescriptionMap,
) -> OperationalView:
    return OperationalView(
        actuality=description_map.prefix(view.actuality),
        next_events=tuple(sorted(description_map.event(event) for event in view.next_events)),
        next_probabilities=tuple(
            sorted(
                (description_map.event(event), probability)
                for event, probability in view.next_probabilities
            )
        ),
    )


def canonical_modal_transport() -> ModalTransportDiagnostics:
    """Transport both Stage 2 semantics while preserving their formal distinction."""

    source_substrate = canonical_stage2_substrate()
    description_map = canonical_modal_description_map()
    target_substrate = renamed_modal_substrate(source_substrate, description_map)

    source_epistemic = canonical_epistemic_model()
    source_ontic = canonical_ontic_model()
    source_epistemic_view = project_epistemic_view(source_epistemic, ("p", "n"))
    source_ontic_view = project_ontic_view(source_ontic)

    target_epistemic = transport_epistemic_model(
        source_epistemic, target_substrate, description_map
    )
    target_ontic = transport_ontic_model(
        source_ontic, target_substrate, description_map
    )
    target_epistemic_view = project_epistemic_view(
        target_epistemic, description_map.prefix(("p", "n"))
    )
    target_ontic_view = project_ontic_view(target_ontic)

    source_ep_op = operationalize_epistemic_view(source_epistemic_view)
    source_on_op = operationalize_ontic_view(source_ontic_view)
    target_ep_op = operationalize_epistemic_view(target_epistemic_view)
    target_on_op = operationalize_ontic_view(target_ontic_view)

    source_operational_equal = compare_operational_views(source_ep_op, source_on_op).equal
    target_operational_equal = compare_operational_views(target_ep_op, target_on_op).equal

    epistemic_operational_transport_equal = compare_operational_views(
        transport_operational_view(source_ep_op, description_map),
        target_ep_op,
    ).equal
    ontic_operational_transport_equal = compare_operational_views(
        transport_operational_view(source_on_op, description_map),
        target_on_op,
    ).equal

    epistemic_extensions = extension_transport_diagnostics(
        source_epistemic_view.potentiality.histories,
        target_epistemic_view.potentiality.histories,
        description_map,
    )
    ontic_extensions = extension_transport_diagnostics(
        source_ontic_view.potentiality.histories,
        target_ontic_view.potentiality.histories,
        description_map,
    )

    source_types_distinct = (
        type(source_epistemic_view.potentiality)
        is not type(source_ontic_view.potentiality)
    )
    target_types_distinct = (
        type(target_epistemic_view.potentiality)
        is not type(target_ontic_view.potentiality)
    )
    epistemic_selected_history_present = hasattr(target_epistemic, "selected_history")
    ontic_selected_future_field_present = hasattr(target_ontic, "selected_history")

    underdetermination_preserved = (
        source_operational_equal
        and target_operational_equal
        and epistemic_operational_transport_equal
        and ontic_operational_transport_equal
        and source_types_distinct
        and target_types_distinct
        and epistemic_selected_history_present
        and not ontic_selected_future_field_present
    )

    return ModalTransportDiagnostics(
        source=description_map.source,
        target=description_map.target,
        epistemic_extensions=epistemic_extensions,
        ontic_extensions=ontic_extensions,
        source_operational_equal=source_operational_equal,
        target_operational_equal=target_operational_equal,
        epistemic_operational_transport_equal=epistemic_operational_transport_equal,
        ontic_operational_transport_equal=ontic_operational_transport_equal,
        source_potentiality_types_distinct=source_types_distinct,
        target_potentiality_types_distinct=target_types_distinct,
        epistemic_selected_history_present=epistemic_selected_history_present,
        ontic_selected_future_field_present=ontic_selected_future_field_present,
        underdetermination_preserved=underdetermination_preserved,
    )


def modal_mismatch_control() -> ModalMismatchDiagnostics:
    """Keep the canonical target substrate fixed and use a branch-breaking event map."""

    source_substrate = canonical_stage2_substrate()
    canonical_map = canonical_modal_description_map()
    target_substrate = renamed_modal_substrate(source_substrate, canonical_map)

    source_epistemic = canonical_epistemic_model()
    source_ontic = canonical_ontic_model()
    source_ep_view = project_epistemic_view(source_epistemic, ("p", "n"))
    source_on_view = project_ontic_view(source_ontic)

    target_epistemic = transport_epistemic_model(
        source_epistemic, target_substrate, canonical_map
    )
    target_ontic = transport_ontic_model(source_ontic, target_substrate, canonical_map)
    target_ep_view = project_epistemic_view(
        target_epistemic, canonical_map.prefix(("p", "n"))
    )
    target_on_view = project_ontic_view(target_ontic)

    bad_map = mismatched_modal_description_map()
    ep_diag = extension_transport_diagnostics(
        source_ep_view.potentiality.histories,
        target_ep_view.potentiality.histories,
        bad_map,
    )
    on_diag = extension_transport_diagnostics(
        source_on_view.potentiality.histories,
        target_on_view.potentiality.histories,
        bad_map,
    )

    source_targets = [target for _, target in bad_map.event_mapping]
    return ModalMismatchDiagnostics(
        event_map_is_bijective=len(set(source_targets)) == len(source_targets),
        epistemic_relation_holds=ep_diag.relation_holds,
        ontic_relation_holds=on_diag.relation_holds,
        epistemic_invalid_mapped_extension_count=ep_diag.invalid_mapped_extension_count,
        ontic_invalid_mapped_extension_count=on_diag.invalid_mapped_extension_count,
    )


def stage6e_rows() -> dict[str, Any]:
    """Return JSON-friendly Stage 6E diagnostics."""

    record_controls = record_accessibility_controls()
    return {
        "record_transport": {
            "orientation_preserving": canonical_preserving_record_transport().as_dict(),
            "orientation_reversing": canonical_reversing_record_transport().as_dict(),
            "misdeclared_orientation_control": record_orientation_mismatch_control().as_dict(),
            "accessibility_controls": {
                name: diagnostics.as_dict()
                for name, diagnostics in record_controls.items()
            },
        },
        "modality_transport": canonical_modal_transport().as_dict(),
        "modality_mismatch_control": modal_mismatch_control().as_dict(),
        "interpretation_guards": {
            "record_transport_is_phenomenal_passage": False,
            "operational_equality_implies_modal_equivalence": False,
        },
    }
