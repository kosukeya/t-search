"""Stage 13D typed multi-constraint gauge atlas, quotient, and descent.

This module consumes the Stage 13A single-generator transports, Stage 13B
compensated mixed paths, and Stage 13C Dirac / two-clock relational data.  It
closes only the Stage 13D questions frozen in ``docs/stage13_protocol.md``:

* keep physical orbit, representative, generator/basis, path word, event,
  clock, and modal roles explicitly typed;
* build the sampled multi-constraint atlas from licensed ``Phi_T`` / ``Phi_X``
  connectivity rather than using stored orbit labels to construct classes;
* recover exactly four quotient classes of nine representatives;
* verify quotient-level Dirac / two-clock relational descent;
* verify that the two compensated mixed path words descend to the same
  quotient-level payload;
* keep physically distinct Dirac data separated under connectivity;
* separate loss of path-word / compensator typing from finite numerical
  reconstructibility; and
* keep path words distinct from modal continuations and physical temporal
  history.

The result is finite and typed.  It is not refoliation invariance, a
hypersurface-deformation algebra, general covariance, general relativity, or a
metaphysical result about becoming / eternalism.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

from t_search.stage13_multi_constraint import (
    STAGE13A_ATOL,
    STAGE13A_BASIS_ID,
    STAGE13A_K_T,
    STAGE13A_K_X,
    Stage13PhaseSpacePoint,
    Stage13Representative,
    Stage13SingleGeneratorTransport,
    canonical_stage13a_grid_values,
    canonical_stage13a_orbits,
    canonical_stage13a_phi_T_transports,
    canonical_stage13a_phi_X_transports,
    canonical_stage13a_representatives,
)
from t_search.stage13_paths import (
    STAGE13B_PATH_WORD_ROLE,
    STAGE13B_PHI_T,
    STAGE13B_PHI_X,
    STAGE13B_TEMPORAL_ORDER_STATUS,
    canonical_stage13b_mixed_path_comparisons,
)
from t_search.stage13_relational import (
    canonical_stage13c_compensated_relational_comparisons,
    stage13c_complete_relational_value,
    stage13c_reconstruct_dirac_from_point,
)

STAGE13D_NODE_PHYSICAL_ORBIT = "physical_orbit"
STAGE13D_NODE_REPRESENTATIVE = "gauge_representative"
STAGE13D_NODE_GENERATOR = "constraint_generator"
STAGE13D_NODE_BASIS = "constraint_basis"
STAGE13D_NODE_PATH_WORD = "gauge_path_word"
STAGE13D_NODE_EVENT = "relational_event"
STAGE13D_NODE_CLOCK = "relational_clock"
STAGE13D_NODE_MODAL = "modal_continuation"

STAGE13D_ATLAS_ARROW_ROLE = "typed_single_generator_atlas_arrow"
STAGE13D_QUOTIENT_ROLE = "connectivity_generated_physical_quotient"
STAGE13D_DESCENT_ROLE = "quotient_level_dirac_two_clock_relational_payload"
STAGE13D_COMPENSATED_DESCENT_CLASSIFICATION = "compensated_path_words_descend_to_same_quotient_payload"
STAGE13D_TYPED_STATUS_LOST = "lost"
STAGE13D_NUMERICAL_STATUS_RECONSTRUCTIBLE = "reconstructible"
STAGE13D_PATH_ABLATION_CLASSIFICATION = "path_word_compensator_provenance_lost_numerically_reconstructible"
STAGE13D_MODAL_STATUS = "not_modal_continuation"
STAGE13D_METAPHYSICAL_CLAIM_STATUS = "not_licensed"
STAGE13D_MODAL_CONTINUATIONS = ("h_L", "h_R")


@dataclass(frozen=True, slots=True)
class Stage13DTypedNode:
    node_id: str
    node_type: str
    orbit_id: str | None
    role: str
    provenance: str


@dataclass(frozen=True, slots=True)
class Stage13DAtlasArrow:
    arrow_id: str
    source_representative_id: str
    target_representative_id: str
    generator_id: str
    basis_id: str
    path_word: tuple[str, ...]
    path_word_role: str
    declared_orbit_id: str
    phase_space_residual: float
    constraint_residual: float
    role: str
    provenance: str


@dataclass(frozen=True, slots=True)
class Stage13DQuotientClass:
    quotient_id: str
    representative_ids: tuple[str, ...]
    inferred_orbit_ids: tuple[str, ...]
    Q_D: float
    P_D: float
    max_Q_D_spread: float
    max_P_D_spread: float
    internal_arrow_count: int
    role: str
    provenance: str


@dataclass(frozen=True, slots=True)
class Stage13DQuotientDescentEvaluation:
    quotient_id: str
    inferred_orbit_id: str
    tau: float
    chi: float
    Q_D: float
    P_D: float
    relational_q: float
    max_Q_D_spread: float
    max_P_D_spread: float
    max_relational_q_spread: float
    role: str


@dataclass(frozen=True, slots=True)
class Stage13DCompensatedDescentCheck:
    comparison_id: str
    quotient_id: str
    source_representative_id: str
    target_representative_id: str
    path_word_TX: tuple[str, str]
    path_word_XT: tuple[str, str]
    path_word_role: str
    temporal_order_status: str
    modal_role_status: str
    Q_TX: float
    P_TX: float
    Q_XT: float
    P_XT: float
    quotient_Q_D: float
    quotient_P_D: float
    max_dirac_payload_residual: float
    relational_evaluation_count: int
    max_relational_payload_residual: float
    classification: str
    metaphysical_claim_status: str


@dataclass(frozen=True, slots=True)
class Stage13DPathProvenanceAblation:
    removed_resource: str
    typed_status: str
    numerical_status: str
    comparison_count: int
    uniquely_reconstructed_target_count: int
    classification: str
    provenance: str


@dataclass(frozen=True, slots=True)
class Stage13DDiagnostics:
    typed_node_count: int
    node_types: tuple[str, ...]
    atlas_arrow_count: int
    phi_T_arrow_count: int
    phi_X_arrow_count: int
    cross_orbit_arrow_count: int
    quotient_class_count: int
    quotient_member_count: int
    quotient_class_sizes: tuple[int, ...]
    mixed_orbit_quotient_count: int
    quotient_descent_evaluation_count: int
    compensated_descent_check_count: int
    compensated_relational_evaluation_count: int
    distinct_quotient_dirac_pair_count: int
    max_quotient_Q_D_spread: float
    max_quotient_P_D_spread: float
    max_quotient_relational_q_spread: float
    max_compensated_dirac_payload_residual: float
    max_compensated_relational_payload_residual: float
    path_ablation_typed_status: str
    path_ablation_numerical_status: str
    path_ablation_reconstructed_target_count: int
    path_word_modal_separation_explicit: bool
    path_word_temporal_separation_explicit: bool
    quotient_partition_exact: bool
    physical_dirac_data_not_collapsed: bool
    criteria_32_38_satisfied: bool


def _representative_lookup() -> dict[str, Stage13Representative]:
    return {item.representative_id: item for item in canonical_stage13a_representatives()}


def _point_residual(left: Stage13PhaseSpacePoint, right: Stage13PhaseSpacePoint) -> float:
    return float(
        max(
            abs(left.T - right.T),
            abs(left.p_T - right.p_T),
            abs(left.X - right.X),
            abs(left.p_X - right.p_X),
            abs(left.q - right.q),
            abs(left.p - right.p),
        )
    )


def canonical_stage13d_typed_nodes() -> tuple[Stage13DTypedNode, ...]:
    """Return the explicitly typed Stage 13D node vocabulary."""

    nodes: dict[str, Stage13DTypedNode] = {}

    for orbit in canonical_stage13a_orbits():
        nodes[f"orbit::{orbit.orbit_id}"] = Stage13DTypedNode(
            node_id=f"orbit::{orbit.orbit_id}",
            node_type=STAGE13D_NODE_PHYSICAL_ORBIT,
            orbit_id=orbit.orbit_id,
            role="physical orbit identity",
            provenance="Stage 12-carried canonical physical initial-data class",
        )

    for representative in canonical_stage13a_representatives():
        nodes[f"representative::{representative.representative_id}"] = Stage13DTypedNode(
            node_id=f"representative::{representative.representative_id}",
            node_type=STAGE13D_NODE_REPRESENTATIVE,
            orbit_id=representative.orbit_id,
            role=representative.representative_role,
            provenance=representative.provenance,
        )
        nodes[f"event::{representative.event_id}"] = Stage13DTypedNode(
            node_id=f"event::{representative.event_id}",
            node_type=STAGE13D_NODE_EVENT,
            orbit_id=representative.orbit_id,
            role=representative.event_role,
            provenance="sampled carrier event; not identified with a path word",
        )

    for generator in (STAGE13A_K_T, STAGE13A_K_X):
        nodes[f"generator::{generator}"] = Stage13DTypedNode(
            node_id=f"generator::{generator}",
            node_type=STAGE13D_NODE_GENERATOR,
            orbit_id=None,
            role="constraint generator identity",
            provenance="Stage 13 frozen noncommuting constraint presentation",
        )

    nodes[f"basis::{STAGE13A_BASIS_ID}"] = Stage13DTypedNode(
        node_id=f"basis::{STAGE13A_BASIS_ID}",
        node_type=STAGE13D_NODE_BASIS,
        orbit_id=None,
        role="constraint basis presentation",
        provenance="basis metadata is representation provenance rather than quotient physical content",
    )

    for node_id, word in (
        ("single_Phi_T", (STAGE13B_PHI_T,)),
        ("single_Phi_X", (STAGE13B_PHI_X,)),
        ("composite_TX", (STAGE13B_PHI_T, STAGE13B_PHI_X)),
        ("composite_XT", (STAGE13B_PHI_X, STAGE13B_PHI_T)),
    ):
        nodes[f"path_word::{node_id}"] = Stage13DTypedNode(
            node_id=f"path_word::{node_id}",
            node_type=STAGE13D_NODE_PATH_WORD,
            orbit_id=None,
            role=STAGE13B_PATH_WORD_ROLE,
            provenance=f"typed gauge path word {word}; not a physical temporal history",
        )

    for clock_id, role in (
        ("clock_T", "relational / gauge-coordinate clock T"),
        ("clock_X", "relational / gauge-coordinate clock X"),
    ):
        nodes[f"clock::{clock_id}"] = Stage13DTypedNode(
            node_id=f"clock::{clock_id}",
            node_type=STAGE13D_NODE_CLOCK,
            orbit_id=None,
            role=role,
            provenance="clock role remains distinct from generator and path-word identity",
        )

    for continuation in STAGE13D_MODAL_CONTINUATIONS:
        nodes[f"continuation::{continuation}"] = Stage13DTypedNode(
            node_id=f"continuation::{continuation}",
            node_type=STAGE13D_NODE_MODAL,
            orbit_id=None,
            role="modal continuation",
            provenance="inherited Stage 10/11 modal role; not a constraint-generated gauge path",
        )

    return tuple(nodes[key] for key in sorted(nodes))


def stage13d_atlas_arrow(transport: Stage13SingleGeneratorTransport) -> Stage13DAtlasArrow:
    """Lift one licensed Stage 13A transport into the Stage 13D typed atlas."""

    lookup = _representative_lookup()
    source = lookup[transport.source_representative_id]
    target = lookup[transport.target_representative_id]
    if source.orbit_id != target.orbit_id:
        raise ValueError("Stage 13D atlas cannot admit a cross-orbit generator edge")
    if transport.constraint_basis_id != STAGE13A_BASIS_ID:
        raise ValueError("Stage 13D atlas requires the frozen Stage 13 positive basis")
    if transport.generator_id == STAGE13A_K_T:
        word = (STAGE13B_PHI_T,)
    elif transport.generator_id == STAGE13A_K_X:
        word = (STAGE13B_PHI_X,)
    else:
        raise ValueError("Stage 13D atlas received an unknown generator identity")

    return Stage13DAtlasArrow(
        arrow_id=f"atlas::{transport.transport_id}",
        source_representative_id=transport.source_representative_id,
        target_representative_id=transport.target_representative_id,
        generator_id=transport.generator_id,
        basis_id=transport.constraint_basis_id,
        path_word=word,
        path_word_role=STAGE13B_PATH_WORD_ROLE,
        declared_orbit_id=source.orbit_id,
        phase_space_residual=transport.phase_space_residual,
        constraint_residual=max(
            transport.source_constraint_residual,
            transport.predicted_constraint_residual,
            transport.target_constraint_residual,
        ),
        role=STAGE13D_ATLAS_ARROW_ROLE,
        provenance="licensed typed single-generator edge; orbit label is diagnostic only and not used for union",
    )


def canonical_stage13d_atlas_arrows() -> tuple[Stage13DAtlasArrow, ...]:
    transports = canonical_stage13a_phi_T_transports() + canonical_stage13a_phi_X_transports()
    return tuple(stage13d_atlas_arrow(item) for item in transports)


def _connectivity_components() -> tuple[tuple[str, ...], ...]:
    """Build components from typed arrow endpoints without consulting orbit ids."""

    representative_ids = tuple(item.representative_id for item in canonical_stage13a_representatives())
    adjacency: dict[str, set[str]] = {item: set() for item in representative_ids}
    for arrow in canonical_stage13d_atlas_arrows():
        adjacency[arrow.source_representative_id].add(arrow.target_representative_id)
        adjacency[arrow.target_representative_id].add(arrow.source_representative_id)

    unseen = set(adjacency)
    components: list[tuple[str, ...]] = []
    while unseen:
        seed = min(unseen)
        stack = [seed]
        component: set[str] = set()
        while stack:
            current = stack.pop()
            if current in component:
                continue
            component.add(current)
            stack.extend(sorted(adjacency[current] - component))
        unseen -= component
        components.append(tuple(sorted(component)))
    return tuple(sorted(components, key=lambda items: items[0]))


def canonical_stage13d_quotient_classes() -> tuple[Stage13DQuotientClass, ...]:
    """Recover the quotient from connectivity, using orbit labels only afterward for validation."""

    lookup = _representative_lookup()
    arrows = canonical_stage13d_atlas_arrows()
    result: list[Stage13DQuotientClass] = []
    for index, component in enumerate(_connectivity_components()):
        dirac_values = [stage13c_reconstruct_dirac_from_point(lookup[item].point()) for item in component]
        q_values = [item[0] for item in dirac_values]
        p_values = [item[1] for item in dirac_values]
        q_mean = float(sum(q_values) / len(q_values))
        p_mean = float(sum(p_values) / len(p_values))
        inferred_orbit_ids = tuple(sorted({lookup[item].orbit_id for item in component}))
        component_set = set(component)
        internal_arrow_count = sum(
            1
            for arrow in arrows
            if arrow.source_representative_id in component_set
            and arrow.target_representative_id in component_set
        )
        result.append(
            Stage13DQuotientClass(
                quotient_id=f"stage13_multi_constraint_quotient_{index:02d}",
                representative_ids=component,
                inferred_orbit_ids=inferred_orbit_ids,
                Q_D=q_mean,
                P_D=p_mean,
                max_Q_D_spread=max(abs(value - q_mean) for value in q_values),
                max_P_D_spread=max(abs(value - p_mean) for value in p_values),
                internal_arrow_count=internal_arrow_count,
                role=STAGE13D_QUOTIENT_ROLE,
                provenance="connected component of typed Phi_T/Phi_X arrows; stored orbit labels not used to construct component",
            )
        )
    return tuple(result)


def _representative_to_quotient() -> dict[str, Stage13DQuotientClass]:
    mapping: dict[str, Stage13DQuotientClass] = {}
    for quotient in canonical_stage13d_quotient_classes():
        for representative_id in quotient.representative_ids:
            mapping[representative_id] = quotient
    return mapping


def canonical_stage13d_quotient_descent_evaluations() -> tuple[Stage13DQuotientDescentEvaluation, ...]:
    lookup = _representative_lookup()
    result: list[Stage13DQuotientDescentEvaluation] = []
    for quotient in canonical_stage13d_quotient_classes():
        if len(quotient.inferred_orbit_ids) != 1:
            raise ValueError("Stage 13D quotient mixes distinct declared physical orbits")
        points = [lookup[item].point() for item in quotient.representative_ids]
        dirac_values = [stage13c_reconstruct_dirac_from_point(point) for point in points]
        q_values = [item[0] for item in dirac_values]
        p_values = [item[1] for item in dirac_values]
        q_mean = float(sum(q_values) / len(q_values))
        p_mean = float(sum(p_values) / len(p_values))
        for tau in canonical_stage13a_grid_values():
            for chi in canonical_stage13a_grid_values():
                relational_values = [
                    stage13c_complete_relational_value(Q_D, P_D, float(tau), float(chi))
                    for Q_D, P_D in dirac_values
                ]
                relational_mean = float(sum(relational_values) / len(relational_values))
                result.append(
                    Stage13DQuotientDescentEvaluation(
                        quotient_id=quotient.quotient_id,
                        inferred_orbit_id=quotient.inferred_orbit_ids[0],
                        tau=float(tau),
                        chi=float(chi),
                        Q_D=q_mean,
                        P_D=p_mean,
                        relational_q=relational_mean,
                        max_Q_D_spread=max(abs(value - q_mean) for value in q_values),
                        max_P_D_spread=max(abs(value - p_mean) for value in p_values),
                        max_relational_q_spread=max(
                            abs(value - relational_mean) for value in relational_values
                        ),
                        role=STAGE13D_DESCENT_ROLE,
                    )
                )
    return tuple(result)


def canonical_stage13d_compensated_descent_checks() -> tuple[Stage13DCompensatedDescentCheck, ...]:
    quotient_by_rep = _representative_to_quotient()
    quotient_lookup = {item.quotient_id: item for item in canonical_stage13d_quotient_classes()}
    relational_by_comparison: dict[str, list[object]] = {}
    for item in canonical_stage13c_compensated_relational_comparisons():
        relational_by_comparison.setdefault(item.comparison_id, []).append(item)

    result: list[Stage13DCompensatedDescentCheck] = []
    for comparison in canonical_stage13b_mixed_path_comparisons():
        source_quotient = quotient_by_rep[comparison.source_representative_id]
        target_quotient = quotient_by_rep[comparison.target_representative_id]
        if source_quotient.quotient_id != target_quotient.quotient_id:
            raise ValueError("Stage 13D compensated path endpoints do not descend to one quotient")
        quotient = quotient_lookup[source_quotient.quotient_id]
        Q_TX, P_TX = stage13c_reconstruct_dirac_from_point(comparison.compensated_TX_endpoint)
        Q_XT, P_XT = stage13c_reconstruct_dirac_from_point(comparison.compensated_XT_endpoint)
        dirac_residual = max(
            abs(Q_TX - Q_XT),
            abs(P_TX - P_XT),
            abs(Q_TX - quotient.Q_D),
            abs(P_TX - quotient.P_D),
            abs(Q_XT - quotient.Q_D),
            abs(P_XT - quotient.P_D),
        )
        relational_items = relational_by_comparison[comparison.comparison_id]
        relational_residuals: list[float] = []
        for item in relational_items:
            quotient_q = stage13c_complete_relational_value(
                quotient.Q_D, quotient.P_D, item.tau, item.chi
            )
            relational_residuals.extend(
                (
                    abs(item.q_TX - item.q_XT),
                    abs(item.q_TX - quotient_q),
                    abs(item.q_XT - quotient_q),
                    abs(item.q_target - quotient_q),
                )
            )
        result.append(
            Stage13DCompensatedDescentCheck(
                comparison_id=comparison.comparison_id,
                quotient_id=quotient.quotient_id,
                source_representative_id=comparison.source_representative_id,
                target_representative_id=comparison.target_representative_id,
                path_word_TX=comparison.path_word_TX,
                path_word_XT=comparison.path_word_XT,
                path_word_role=comparison.path_word_role,
                temporal_order_status=comparison.temporal_order_status,
                modal_role_status=STAGE13D_MODAL_STATUS,
                Q_TX=Q_TX,
                P_TX=P_TX,
                Q_XT=Q_XT,
                P_XT=P_XT,
                quotient_Q_D=quotient.Q_D,
                quotient_P_D=quotient.P_D,
                max_dirac_payload_residual=float(dirac_residual),
                relational_evaluation_count=len(relational_items),
                max_relational_payload_residual=float(max(relational_residuals)),
                classification=STAGE13D_COMPENSATED_DESCENT_CLASSIFICATION,
                metaphysical_claim_status=STAGE13D_METAPHYSICAL_CLAIM_STATUS,
            )
        )
    return tuple(result)


def stage13d_path_provenance_ablation() -> Stage13DPathProvenanceAblation:
    """Remove typed path-word/compensator provenance and test finite numerical reconstruction.

    The numerical check matches compensated endpoints to raw representatives
    without using path-word, compensator, or orbit labels.  A successful match
    does not restore the removed typed provenance.
    """

    representatives = canonical_stage13a_representatives()
    reconstructed = 0
    comparisons = canonical_stage13b_mixed_path_comparisons()
    for comparison in comparisons:
        matches = [
            representative
            for representative in representatives
            if _point_residual(comparison.compensated_TX_endpoint, representative.point())
            <= STAGE13A_ATOL
        ]
        if len(matches) == 1:
            reconstructed += 1

    numerical_status = (
        STAGE13D_NUMERICAL_STATUS_RECONSTRUCTIBLE
        if reconstructed == len(comparisons)
        else "not_established"
    )
    return Stage13DPathProvenanceAblation(
        removed_resource="typed path word + compensator provenance",
        typed_status=STAGE13D_TYPED_STATUS_LOST,
        numerical_status=numerical_status,
        comparison_count=len(comparisons),
        uniquely_reconstructed_target_count=reconstructed,
        classification=STAGE13D_PATH_ABLATION_CLASSIFICATION,
        provenance=(
            "path-word/compensator fields removed by construction; finite endpoint coordinates used only to test numerical reconstructibility"
        ),
    )


def stage13d_diagnostics() -> Stage13DDiagnostics:
    nodes = canonical_stage13d_typed_nodes()
    arrows = canonical_stage13d_atlas_arrows()
    quotients = canonical_stage13d_quotient_classes()
    descent = canonical_stage13d_quotient_descent_evaluations()
    compensated = canonical_stage13d_compensated_descent_checks()
    ablation = stage13d_path_provenance_ablation()
    lookup = _representative_lookup()

    phi_T_count = sum(1 for item in arrows if item.path_word == (STAGE13B_PHI_T,))
    phi_X_count = sum(1 for item in arrows if item.path_word == (STAGE13B_PHI_X,))
    cross_orbit_count = sum(
        1
        for item in arrows
        if lookup[item.source_representative_id].orbit_id
        != lookup[item.target_representative_id].orbit_id
    )
    class_sizes = tuple(sorted(len(item.representative_ids) for item in quotients))
    mixed_quotients = sum(1 for item in quotients if len(item.inferred_orbit_ids) != 1)

    distinct_pairs = 0
    for left, right in combinations(quotients, 2):
        if max(abs(left.Q_D - right.Q_D), abs(left.P_D - right.P_D)) > STAGE13A_ATOL:
            distinct_pairs += 1

    node_types = tuple(sorted({item.node_type for item in nodes}))
    path_word_nodes = [item for item in nodes if item.node_type == STAGE13D_NODE_PATH_WORD]
    modal_nodes = [item for item in nodes if item.node_type == STAGE13D_NODE_MODAL]
    modal_separation = (
        len(path_word_nodes) == 4
        and len(modal_nodes) == 2
        and not ({item.node_id for item in path_word_nodes} & {item.node_id for item in modal_nodes})
        and all(item.modal_role_status == STAGE13D_MODAL_STATUS for item in compensated)
    )
    temporal_separation = all(
        item.temporal_order_status == STAGE13B_TEMPORAL_ORDER_STATUS
        and item.metaphysical_claim_status == STAGE13D_METAPHYSICAL_CLAIM_STATUS
        for item in compensated
    )

    quotient_exact = (
        len(quotients) == 4
        and class_sizes == (9, 9, 9, 9)
        and sum(class_sizes) == 36
        and mixed_quotients == 0
    )
    dirac_not_collapsed = distinct_pairs == 6

    max_q_spread = max(item.max_Q_D_spread for item in quotients)
    max_p_spread = max(item.max_P_D_spread for item in quotients)
    max_relational_spread = max(item.max_relational_q_spread for item in descent)
    max_comp_dirac = max(item.max_dirac_payload_residual for item in compensated)
    max_comp_relational = max(item.max_relational_payload_residual for item in compensated)
    relational_evaluation_count = sum(item.relational_evaluation_count for item in compensated)

    required_node_types = {
        STAGE13D_NODE_PHYSICAL_ORBIT,
        STAGE13D_NODE_REPRESENTATIVE,
        STAGE13D_NODE_GENERATOR,
        STAGE13D_NODE_BASIS,
        STAGE13D_NODE_PATH_WORD,
        STAGE13D_NODE_EVENT,
        STAGE13D_NODE_CLOCK,
        STAGE13D_NODE_MODAL,
    }
    typed_roles_complete = required_node_types.issubset(set(node_types))
    compensated_descends = (
        len(compensated) == 144
        and relational_evaluation_count == 1296
        and max_comp_dirac <= STAGE13A_ATOL
        and max_comp_relational <= STAGE13A_ATOL
        and all(item.path_word_TX != item.path_word_XT for item in compensated)
    )
    quotient_descent_established = (
        len(descent) == 36
        and max_q_spread <= STAGE13A_ATOL
        and max_p_spread <= STAGE13A_ATOL
        and max_relational_spread <= STAGE13A_ATOL
    )
    path_ablation_separated = (
        ablation.typed_status == STAGE13D_TYPED_STATUS_LOST
        and ablation.numerical_status == STAGE13D_NUMERICAL_STATUS_RECONSTRUCTIBLE
        and ablation.uniquely_reconstructed_target_count == 144
    )
    criteria = (
        typed_roles_complete
        and len(arrows) == 144
        and phi_T_count == 72
        and phi_X_count == 72
        and cross_orbit_count == 0
        and quotient_exact
        and quotient_descent_established
        and compensated_descends
        and dirac_not_collapsed
        and path_ablation_separated
        and modal_separation
        and temporal_separation
    )

    return Stage13DDiagnostics(
        typed_node_count=len(nodes),
        node_types=node_types,
        atlas_arrow_count=len(arrows),
        phi_T_arrow_count=phi_T_count,
        phi_X_arrow_count=phi_X_count,
        cross_orbit_arrow_count=cross_orbit_count,
        quotient_class_count=len(quotients),
        quotient_member_count=sum(class_sizes),
        quotient_class_sizes=class_sizes,
        mixed_orbit_quotient_count=mixed_quotients,
        quotient_descent_evaluation_count=len(descent),
        compensated_descent_check_count=len(compensated),
        compensated_relational_evaluation_count=relational_evaluation_count,
        distinct_quotient_dirac_pair_count=distinct_pairs,
        max_quotient_Q_D_spread=float(max_q_spread),
        max_quotient_P_D_spread=float(max_p_spread),
        max_quotient_relational_q_spread=float(max_relational_spread),
        max_compensated_dirac_payload_residual=float(max_comp_dirac),
        max_compensated_relational_payload_residual=float(max_comp_relational),
        path_ablation_typed_status=ablation.typed_status,
        path_ablation_numerical_status=ablation.numerical_status,
        path_ablation_reconstructed_target_count=ablation.uniquely_reconstructed_target_count,
        path_word_modal_separation_explicit=modal_separation,
        path_word_temporal_separation_explicit=temporal_separation,
        quotient_partition_exact=quotient_exact,
        physical_dirac_data_not_collapsed=dirac_not_collapsed,
        criteria_32_38_satisfied=criteria,
    )
