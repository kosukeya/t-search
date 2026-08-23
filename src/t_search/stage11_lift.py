"""Stage 11C typed O/P/R/V/Xi lift across external parameterizations.

Stage 11A-B established a shared finite constraint orbit and relational
q(T=tau)/dq/dT covariance under four admissible orientation-preserving external
parameterizations.  Stage 11C does not redesign the Stage 9-10 modal/record
architecture.  Instead, it projects the already-tested O/P/R/V content onto the
Stage 11 parameterized carrier while keeping all representation-specific data
inside Xi.

The public architecture is intentionally selector-free.  An epistemic model may
retain a privileged hidden h* in its private semantic object, but that field is
not copied into O/P/R/V/Xi.  This stage therefore tests typed reconstruction and
schema discipline, not modal identity or ontological becoming.
"""

from __future__ import annotations

from dataclasses import dataclass, fields, is_dataclass, replace
from functools import lru_cache

import numpy as np

from .stage5_clock_change import DEFAULT_ATOL
from .stage7_history import CURRENT_EVENT, UPPER_EVENT
from .stage9_modal import (
    FUTURE_SIGNATURE_LEFT,
    FUTURE_SIGNATURE_OTHER,
    Stage9CModel,
    Stage9EpistemicModel,
    Stage9OnticExtensionModel,
    canonical_stage9c_models,
    continuation_by_id,
    make_stage9_epistemic_model,
    matched_uniform_weights,
    privileged_stage9_modal_diagnostic,
)
from .stage9_substrate import assess_stage9_direction, reduced_stage9_state
from .stage11_parametrized import (
    STAGE11A_ATOL,
    STAGE11A_IDENTITY,
    Stage11ParametrizedTrajectory,
    canonical_stage11a_positive_family,
)
from .stage11_relational import (
    STAGE11B_ANCHOR_INDEX,
    STAGE11B_TARGET_INDEX,
)

STAGE11C_EVENT_BRIDGE_SEMANTICS = (
    "Stage 10 event-role bridge to Stage 11 precursor physical event ids; "
    "raw external parameter labels are representation metadata only"
)
STAGE11C_LAPSE_SEMANTICS = (
    "N_rho=dT/dlambda_rho with N_sigma=N_rho d(lambda_rho)/d(lambda_sigma)"
)
STAGE11C_WEIGHT_SEMANTICS = (
    "matched continuation-class weights over QExt(e1); public V does not encode hidden h*"
)
STAGE11C_CORRUPTION_CLASSIFICATION = "parameter_dependent_oprv_corruption_detected"


@dataclass(frozen=True, slots=True)
class Stage11OEvent:
    role: str
    stage10_event: str
    physical_event_id: str
    clock_value: float
    q_value: float


@dataclass(frozen=True, slots=True)
class Stage11OLayer:
    stage10_current_anchor: int
    current_density_matrix: tuple[complex, ...]
    relational_events: tuple[Stage11OEvent, ...]


@dataclass(frozen=True, slots=True)
class Stage11PLayer:
    current_anchor: int
    qext_ids: tuple[str, ...]
    continuation_classes: tuple[tuple[str, str], ...]


@dataclass(frozen=True, slots=True)
class Stage11RContentRow:
    continuation_id: str
    lower_information: float
    upper_information: float
    lower_accuracy: float
    upper_accuracy: float


@dataclass(frozen=True, slots=True)
class Stage11RDirectionRow:
    continuation_id: str
    record_score: float
    orientation: str


@dataclass(frozen=True, slots=True)
class Stage11RAccessRow:
    continuation_id: str
    accessibility_score: float


@dataclass(frozen=True, slots=True)
class Stage11RLayer:
    R_content: tuple[Stage11RContentRow, ...]
    R_direction: tuple[Stage11RDirectionRow, ...]
    R_access: tuple[Stage11RAccessRow, ...]


@dataclass(frozen=True, slots=True)
class Stage11VLayer:
    V_extension: tuple[str, ...]
    V_semantics: str
    V_weights: tuple[float, ...]
    continuation_weight_alignment: tuple[tuple[str, float], ...]


@dataclass(frozen=True, slots=True)
class Stage11XiLayer:
    parameterization_id: str
    anchor_parameter_value: float
    target_parameter_value: float
    anchor_lapse: float
    target_lapse: float
    event_correspondence: tuple[tuple[str, str], ...]
    continuation_class_correspondence: tuple[tuple[str, str], ...]
    outcome_correspondence: tuple[tuple[str, str], ...]
    event_correspondence_semantics: str
    lapse_semantics: str
    continuation_weight_semantics: str


@dataclass(frozen=True, slots=True)
class Stage11TypedArchitecture:
    O: Stage11OLayer
    P: Stage11PLayer
    R: Stage11RLayer
    V: Stage11VLayer
    Xi: Stage11XiLayer


@dataclass(frozen=True, slots=True)
class Stage11ArchitectureValidation:
    parameterization_id: str
    O_valid: bool
    P_valid: bool
    R_valid: bool
    V_valid: bool
    Xi_valid: bool
    continuation_correspondence_valid: bool
    outcome_correspondence_valid: bool
    valid: bool
    corrupted_layers: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Stage11SelectorSchemaAudit:
    public_field_names: tuple[str, ...]
    forbidden_public_fields: tuple[str, ...]
    selector_free: bool


@dataclass(frozen=True, slots=True)
class Stage11CCorruptionControl:
    layer: str
    classification: str
    detected: bool
    validator_corrupted_layers: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class Stage11CDiagnostics:
    parameterization_count: int
    matched_modal_public_projection_count: int
    qext_size: int
    directional_content_rows: int
    directional_direction_rows: int
    directional_access_rows: int
    xi_view_count: int
    continuation_correspondence_entries: int
    outcome_correspondence_entries: int
    max_current_density_residual: float
    max_relational_O_residual: float
    max_R_residual: float
    max_V_weight_residual: float
    all_positive_architectures_valid: bool
    matched_epistemic_ontic_public_equal: bool
    hidden_hstar_swap_public_invariant: bool
    privileged_modal_roles_distinct: bool
    public_schema_selector_free: bool
    corruption_control_count: int
    corruption_detected_count: int
    criteria_24_31_satisfied: bool


def _trajectory_by_id(parameterization_id: str) -> Stage11ParametrizedTrajectory:
    matches = [
        item
        for item in canonical_stage11a_positive_family()
        if item.parameterization_id == parameterization_id
    ]
    if len(matches) != 1:
        raise ValueError(f"unknown Stage 11C positive parameterization {parameterization_id!r}")
    return matches[0]


def _model_weights(model: Stage9CModel) -> tuple[float, ...]:
    if isinstance(model, Stage9EpistemicModel):
        return tuple(float(value) for value in model.belief_weights)
    if isinstance(model, Stage9OnticExtensionModel):
        return tuple(float(value) for value in model.extension_weights)
    raise TypeError("unsupported Stage 11C modal model")


@lru_cache(maxsize=1)
def _canonical_stage10_physical_payload() -> tuple[
    tuple[complex, ...], Stage11PLayer, Stage11RLayer
]:
    epistemic, _ = canonical_stage9c_models(selected_id="h_L")
    carrier = epistemic.carrier

    current_states: list[np.ndarray] = []
    for continuation in carrier.continuations:
        state = np.asarray(
            reduced_stage9_state(continuation, CURRENT_EVENT), dtype=np.complex128
        )
        norm = float(np.linalg.norm(state))
        if norm <= DEFAULT_ATOL:
            raise ValueError("Stage 11C current Stage 10 state has zero norm")
        current_states.append(state / norm)
    reference = current_states[0]
    if any(
        np.linalg.norm(state - reference) > 10 * DEFAULT_ATOL
        for state in current_states[1:]
    ):
        raise ValueError("Stage 11C requires the Stage 9 current prefix to be common")
    density = np.outer(reference, reference.conj()).reshape(-1)

    qext_ids = tuple(item.continuation_id for item in carrier.continuations)
    classes = tuple(
        (item.continuation_id, item.future_action) for item in carrier.continuations
    )
    P = Stage11PLayer(
        current_anchor=carrier.current_anchor,
        qext_ids=qext_ids,
        continuation_classes=classes,
    )

    content_rows: list[Stage11RContentRow] = []
    direction_rows: list[Stage11RDirectionRow] = []
    access_rows: list[Stage11RAccessRow] = []
    for continuation in carrier.continuations:
        assessment = assess_stage9_direction(continuation)
        content_rows.append(
            Stage11RContentRow(
                continuation.continuation_id,
                float(assessment.lower_information),
                float(assessment.upper_information),
                float(assessment.lower_accuracy),
                float(assessment.upper_accuracy),
            )
        )
        direction_rows.append(
            Stage11RDirectionRow(
                continuation.continuation_id,
                float(assessment.record_score),
                assessment.orientation,
            )
        )
        access_rows.append(
            Stage11RAccessRow(
                continuation.continuation_id,
                float(assessment.accessibility_score),
            )
        )
    R = Stage11RLayer(tuple(content_rows), tuple(direction_rows), tuple(access_rows))
    return tuple(complex(value) for value in density), P, R


def _stage11c_relational_O(trajectory: Stage11ParametrizedTrajectory) -> Stage11OLayer:
    density, _, _ = _canonical_stage10_physical_payload()
    anchor_event_id = trajectory.event_ids[STAGE11B_ANCHOR_INDEX]
    target_event_id = trajectory.event_ids[STAGE11B_TARGET_INDEX]
    relational_events = (
        Stage11OEvent(
            "prediction_anchor",
            "e1",
            anchor_event_id,
            float(trajectory.clock_values[STAGE11B_ANCHOR_INDEX]),
            float(trajectory.q_values[STAGE11B_ANCHOR_INDEX]),
        ),
        Stage11OEvent(
            "measurement_target",
            "e2",
            target_event_id,
            float(trajectory.clock_values[STAGE11B_TARGET_INDEX]),
            float(trajectory.q_values[STAGE11B_TARGET_INDEX]),
        ),
    )
    return Stage11OLayer(CURRENT_EVENT, density, relational_events)


def _stage11c_V(model: Stage9CModel) -> Stage11VLayer:
    ids = tuple(item.continuation_id for item in model.carrier.continuations)
    weights = _model_weights(model)
    if len(ids) != len(weights):
        raise ValueError("Stage 11C V requires one weight per continuation class")
    return Stage11VLayer(
        V_extension=ids,
        V_semantics=STAGE11C_WEIGHT_SEMANTICS,
        V_weights=weights,
        continuation_weight_alignment=tuple(zip(ids, weights, strict=True)),
    )


def _stage11c_Xi(
    model: Stage9CModel,
    trajectory: Stage11ParametrizedTrajectory,
) -> Stage11XiLayer:
    ids = tuple(item.continuation_id for item in model.carrier.continuations)
    return Stage11XiLayer(
        parameterization_id=trajectory.parameterization_id,
        anchor_parameter_value=float(
            trajectory.parameter_labels[STAGE11B_ANCHOR_INDEX]
        ),
        target_parameter_value=float(
            trajectory.parameter_labels[STAGE11B_TARGET_INDEX]
        ),
        anchor_lapse=float(trajectory.lapse_values[STAGE11B_ANCHOR_INDEX]),
        target_lapse=float(trajectory.lapse_values[STAGE11B_TARGET_INDEX]),
        event_correspondence=(
            ("e1", trajectory.event_ids[STAGE11B_ANCHOR_INDEX]),
            ("e2", trajectory.event_ids[STAGE11B_TARGET_INDEX]),
        ),
        continuation_class_correspondence=tuple((item, item) for item in ids),
        outcome_correspondence=(
            (FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_LEFT),
            (FUTURE_SIGNATURE_OTHER, FUTURE_SIGNATURE_OTHER),
        ),
        event_correspondence_semantics=STAGE11C_EVENT_BRIDGE_SEMANTICS,
        lapse_semantics=STAGE11C_LAPSE_SEMANTICS,
        continuation_weight_semantics=STAGE11C_WEIGHT_SEMANTICS,
    )


def stage11c_public_architecture(
    model: Stage9CModel,
    parameterization_id: str,
) -> Stage11TypedArchitecture:
    trajectory = _trajectory_by_id(parameterization_id)
    _, P, R = _canonical_stage10_physical_payload()
    if model.carrier.current_anchor != CURRENT_EVENT:
        raise ValueError("Stage 11C model must retain the Stage 10 e1 current anchor")
    model_ids = tuple(item.continuation_id for item in model.carrier.continuations)
    if model_ids != P.qext_ids:
        raise ValueError("Stage 11C model continuation carrier drifted from canonical QExt(e1)")
    return Stage11TypedArchitecture(
        O=_stage11c_relational_O(trajectory),
        P=P,
        R=R,
        V=_stage11c_V(model),
        Xi=_stage11c_Xi(model, trajectory),
    )


def canonical_stage11c_public_architectures() -> tuple[Stage11TypedArchitecture, ...]:
    _, ontic = canonical_stage9c_models(selected_id="h_L")
    return tuple(
        stage11c_public_architecture(ontic, trajectory.parameterization_id)
        for trajectory in canonical_stage11a_positive_family()
    )


def _nested_field_names(value: object) -> tuple[str, ...]:
    names: list[str] = []

    def visit(item: object) -> None:
        if is_dataclass(item) and not isinstance(item, type):
            for field in fields(item):
                names.append(field.name)
                visit(getattr(item, field.name))
        elif isinstance(item, tuple):
            for element in item:
                visit(element)

    visit(value)
    return tuple(dict.fromkeys(names))


def stage11c_selector_schema_audit(
    architecture: Stage11TypedArchitecture,
) -> Stage11SelectorSchemaAudit:
    public_fields = _nested_field_names(architecture)
    forbidden_tokens = (
        "selected_continuation",
        "selected_continuation_id",
        "selector",
        "hidden_selector",
        "modal_type",
        "model_type",
        "privileged_modal_type",
    )
    forbidden = tuple(
        name
        for name in public_fields
        if any(token == name.lower() for token in forbidden_tokens)
    )
    return Stage11SelectorSchemaAudit(public_fields, forbidden, not forbidden)


def _tuple_numeric_residual(left: tuple[object, ...], right: tuple[object, ...]) -> float:
    a = np.asarray(left, dtype=np.complex128)
    b = np.asarray(right, dtype=np.complex128)
    if a.shape != b.shape:
        return float("inf")
    return float(np.max(np.abs(a - b))) if a.size else 0.0


def _R_residual(left: Stage11RLayer, right: Stage11RLayer) -> float:
    if (
        tuple(item.continuation_id for item in left.R_content)
        != tuple(item.continuation_id for item in right.R_content)
        or tuple(item.continuation_id for item in left.R_direction)
        != tuple(item.continuation_id for item in right.R_direction)
        or tuple(item.continuation_id for item in left.R_access)
        != tuple(item.continuation_id for item in right.R_access)
        or tuple(item.orientation for item in left.R_direction)
        != tuple(item.orientation for item in right.R_direction)
    ):
        return float("inf")
    values_left = tuple(
        value
        for row in left.R_content
        for value in (
            row.lower_information,
            row.upper_information,
            row.lower_accuracy,
            row.upper_accuracy,
        )
    ) + tuple(row.record_score for row in left.R_direction) + tuple(
        row.accessibility_score for row in left.R_access
    )
    values_right = tuple(
        value
        for row in right.R_content
        for value in (
            row.lower_information,
            row.upper_information,
            row.lower_accuracy,
            row.upper_accuracy,
        )
    ) + tuple(row.record_score for row in right.R_direction) + tuple(
        row.accessibility_score for row in right.R_access
    )
    return _tuple_numeric_residual(values_left, values_right)


def _O_residual(left: Stage11OLayer, right: Stage11OLayer) -> tuple[float, float]:
    density = _tuple_numeric_residual(left.current_density_matrix, right.current_density_matrix)
    if (
        left.stage10_current_anchor != right.stage10_current_anchor
        or tuple((item.role, item.stage10_event, item.physical_event_id) for item in left.relational_events)
        != tuple((item.role, item.stage10_event, item.physical_event_id) for item in right.relational_events)
    ):
        return float("inf"), float("inf")
    relational = max(
        max(abs(a.clock_value - b.clock_value), abs(a.q_value - b.q_value))
        for a, b in zip(left.relational_events, right.relational_events, strict=True)
    )
    return density, float(relational)


def stage11c_validate_architecture(
    architecture: Stage11TypedArchitecture,
    *,
    atol: float = STAGE11A_ATOL,
) -> Stage11ArchitectureValidation:
    _, ontic = canonical_stage9c_models(selected_id="h_L")
    expected = stage11c_public_architecture(ontic, architecture.Xi.parameterization_id)
    density_residual, relational_residual = _O_residual(architecture.O, expected.O)
    O_valid = density_residual <= atol and relational_residual <= atol
    P_valid = architecture.P == expected.P
    R_valid = _R_residual(architecture.R, expected.R) <= atol
    V_valid = (
        architecture.V.V_extension == expected.V.V_extension
        and architecture.V.V_semantics == expected.V.V_semantics
        and architecture.V.continuation_weight_alignment
        == expected.V.continuation_weight_alignment
        and _tuple_numeric_residual(architecture.V.V_weights, expected.V.V_weights) <= atol
    )
    Xi_valid = architecture.Xi == expected.Xi
    continuation_valid = architecture.Xi.continuation_class_correspondence == tuple(
        (item, item) for item in expected.P.qext_ids
    )
    outcome_valid = architecture.Xi.outcome_correspondence == (
        (FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_LEFT),
        (FUTURE_SIGNATURE_OTHER, FUTURE_SIGNATURE_OTHER),
    )
    flags = {
        "O": O_valid,
        "P": P_valid,
        "R": R_valid,
        "V": V_valid,
        "Xi": Xi_valid,
    }
    corrupted = tuple(name for name, valid in flags.items() if not valid)
    valid = bool(
        all(flags.values()) and continuation_valid and outcome_valid
    )
    return Stage11ArchitectureValidation(
        parameterization_id=architecture.Xi.parameterization_id,
        O_valid=O_valid,
        P_valid=P_valid,
        R_valid=R_valid,
        V_valid=V_valid,
        Xi_valid=Xi_valid,
        continuation_correspondence_valid=continuation_valid,
        outcome_correspondence_valid=outcome_valid,
        valid=valid,
        corrupted_layers=corrupted,
    )


def stage11c_corruption_controls() -> tuple[Stage11CCorruptionControl, ...]:
    _, ontic = canonical_stage9c_models(selected_id="h_L")
    base = stage11c_public_architecture(ontic, "cubic")

    target = base.O.relational_events[1]
    corrupted_O = replace(
        base,
        O=replace(
            base.O,
            relational_events=(
                base.O.relational_events[0],
                replace(target, q_value=target.q_value + 0.125),
            ),
        ),
    )
    corrupted_P = replace(
        base,
        P=replace(
            base.P,
            qext_ids=(base.P.qext_ids[0],),
            continuation_classes=(base.P.continuation_classes[0],),
        ),
    )
    first_direction = base.R.R_direction[0]
    corrupted_R = replace(
        base,
        R=replace(
            base.R,
            R_direction=(
                replace(first_direction, orientation="corrupted-parameter-direction"),
                *base.R.R_direction[1:],
            ),
        ),
    )
    corrupted_weights = (0.75, 0.25)
    corrupted_V = replace(
        base,
        V=replace(
            base.V,
            V_weights=corrupted_weights,
            continuation_weight_alignment=tuple(
                zip(base.V.V_extension, corrupted_weights, strict=True)
            ),
        ),
    )

    result: list[Stage11CCorruptionControl] = []
    for layer, candidate in (
        ("O", corrupted_O),
        ("P", corrupted_P),
        ("R", corrupted_R),
        ("V", corrupted_V),
    ):
        validation = stage11c_validate_architecture(candidate)
        detected = layer in validation.corrupted_layers and not validation.valid
        result.append(
            Stage11CCorruptionControl(
                layer=layer,
                classification=(
                    STAGE11C_CORRUPTION_CLASSIFICATION if detected else "inconclusive"
                ),
                detected=detected,
                validator_corrupted_layers=validation.corrupted_layers,
            )
        )
    return tuple(result)


def stage11c_diagnostics(*, atol: float = STAGE11A_ATOL) -> Stage11CDiagnostics:
    epistemic_left, ontic = canonical_stage9c_models(selected_id="h_L")
    carrier = epistemic_left.carrier
    uniform = matched_uniform_weights(carrier)
    epistemic_right = make_stage9_epistemic_model(
        carrier,
        continuation_by_id(carrier, "h_R"),
        uniform,
        atol=DEFAULT_ATOL,
    )

    trajectories = canonical_stage11a_positive_family()
    ontic_views = [
        stage11c_public_architecture(ontic, item.parameterization_id)
        for item in trajectories
    ]
    epistemic_left_views = [
        stage11c_public_architecture(epistemic_left, item.parameterization_id)
        for item in trajectories
    ]
    epistemic_right_views = [
        stage11c_public_architecture(epistemic_right, item.parameterization_id)
        for item in trajectories
    ]

    validations = [stage11c_validate_architecture(item, atol=atol) for item in ontic_views]
    all_valid = all(item.valid for item in validations)
    matched_modal = all(
        left == right
        for left, right in zip(epistemic_left_views, ontic_views, strict=True)
    )
    hidden_swap = all(
        left == right
        for left, right in zip(epistemic_left_views, epistemic_right_views, strict=True)
    )

    privileged_left = privileged_stage9_modal_diagnostic(epistemic_left)
    privileged_ontic = privileged_stage9_modal_diagnostic(ontic)
    privileged_distinct = bool(
        privileged_left.selected_complete_continuation_present
        and not privileged_ontic.selected_complete_continuation_present
        and privileged_left.semantic_type != privileged_ontic.semantic_type
    )
    schema_free = all(stage11c_selector_schema_audit(item).selector_free for item in ontic_views)

    reference = next(
        item for item in ontic_views if item.Xi.parameterization_id == STAGE11A_IDENTITY
    )
    max_density = 0.0
    max_relational_O = 0.0
    max_R = 0.0
    max_V = 0.0
    for item in ontic_views:
        density, relational = _O_residual(reference.O, item.O)
        max_density = max(max_density, density)
        max_relational_O = max(max_relational_O, relational)
        max_R = max(max_R, _R_residual(reference.R, item.R))
        max_V = max(
            max_V,
            _tuple_numeric_residual(reference.V.V_weights, item.V.V_weights),
        )
        if item.P != reference.P:
            all_valid = False

    controls = stage11c_corruption_controls()
    corruption_detected_count = sum(item.detected for item in controls)
    _, P, R = _canonical_stage10_physical_payload()
    criteria = bool(
        len(trajectories) == 4
        and len(P.qext_ids) == 2
        and P.qext_ids == ("h_L", "h_R")
        and max_density <= atol
        and max_relational_O <= atol
        and max_R <= atol
        and max_V <= atol
        and all_valid
        and matched_modal
        and hidden_swap
        and privileged_distinct
        and schema_free
        and corruption_detected_count == 4
        and all(
            item.Xi.continuation_class_correspondence
            == (("h_L", "h_L"), ("h_R", "h_R"))
            for item in ontic_views
        )
        and all(
            item.Xi.outcome_correspondence
            == (
                (FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_LEFT),
                (FUTURE_SIGNATURE_OTHER, FUTURE_SIGNATURE_OTHER),
            )
            for item in ontic_views
        )
    )

    return Stage11CDiagnostics(
        parameterization_count=len(trajectories),
        matched_modal_public_projection_count=len(trajectories) * 2,
        qext_size=len(P.qext_ids),
        directional_content_rows=len(R.R_content),
        directional_direction_rows=len(R.R_direction),
        directional_access_rows=len(R.R_access),
        xi_view_count=len(ontic_views),
        continuation_correspondence_entries=sum(
            len(item.Xi.continuation_class_correspondence) for item in ontic_views
        ),
        outcome_correspondence_entries=sum(
            len(item.Xi.outcome_correspondence) for item in ontic_views
        ),
        max_current_density_residual=max_density,
        max_relational_O_residual=max_relational_O,
        max_R_residual=max_R,
        max_V_weight_residual=max_V,
        all_positive_architectures_valid=all_valid,
        matched_epistemic_ontic_public_equal=matched_modal,
        hidden_hstar_swap_public_invariant=hidden_swap,
        privileged_modal_roles_distinct=privileged_distinct,
        public_schema_selector_free=schema_free,
        corruption_control_count=len(controls),
        corruption_detected_count=corruption_detected_count,
        criteria_24_31_satisfied=criteria,
    )


def stage11c_summary(*, atol: float = STAGE11A_ATOL) -> dict[str, object]:
    diagnostics = stage11c_diagnostics(atol=atol)
    return {
        "status": (
            "Stage 11C completed; criteria 24-31 satisfied"
            if diagnostics.criteria_24_31_satisfied
            else "Stage 11C incomplete"
        ),
        "parameterizations": diagnostics.parameterization_count,
        "matched_modal_public_projections": diagnostics.matched_modal_public_projection_count,
        "qext_size": diagnostics.qext_size,
        "qext_ids": ("h_L", "h_R"),
        "xi_views": diagnostics.xi_view_count,
        "continuation_correspondence_entries": diagnostics.continuation_correspondence_entries,
        "outcome_correspondence_entries": diagnostics.outcome_correspondence_entries,
        "max_current_density_residual": diagnostics.max_current_density_residual,
        "max_relational_O_residual": diagnostics.max_relational_O_residual,
        "max_R_residual": diagnostics.max_R_residual,
        "max_V_weight_residual": diagnostics.max_V_weight_residual,
        "public_schema_selector_free": diagnostics.public_schema_selector_free,
        "hidden_hstar_swap_public_invariant": diagnostics.hidden_hstar_swap_public_invariant,
        "corruption_controls_detected": (
            diagnostics.corruption_detected_count,
            diagnostics.corruption_control_count,
        ),
        "bounded_result": "Stage 11C typed O/P/R/V/Xi lift on the frozen positive family = established",
        "guard": "typed O/P/R/V/Xi lift != full future-measurement covariance",
    }
