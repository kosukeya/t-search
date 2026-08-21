import json

import numpy as np
import pytest

from t_search.stage5_clock_change import DEFAULT_ATOL
from t_search.stage5_reductions import support_coordinate_reduction_matrix
from t_search.stage6_compatibility import (
    CANONICAL_EVENTS,
    VERTICAL_GENERATOR_SCALE,
    canonical_stage6d_diagnostics,
    common_vertical_conditioning_matrix,
    compatibility_square_residual,
    horizontal_bridge_reference,
    identity_event_correspondence,
    mapped_event,
    mismatch_control_diagnostics,
    mismatched_event_correspondence,
    order_covariant,
    ordered_event_relations,
    perspective_vertical_map,
    scan_horizontal_vertical_compatibility,
    square_residual_for_correspondence,
    stage6d_rows,
)
from t_search.stage6_partial_atlas import (
    PerspectiveNode,
    build_partial_clock_atlas,
    indirect_paths,
)


def test_canonical_event_family_has_nonuniform_strict_order():
    assert tuple((event.label, event.coordinate) for event in CANONICAL_EVENTS) == (
        ("e0", 0.0),
        ("e1", 1.0),
        ("e2", 3.0),
    )
    assert tuple(
        (source.label, target.label)
        for source, target in ordered_event_relations()
    ) == (("e0", "e1"), ("e0", "e2"), ("e1", "e2"))
    assert VERTICAL_GENERATOR_SCALE > 0.0


def test_event_correspondence_is_explicit_and_not_derived_from_clock_readings():
    source = PerspectiveNode("C", 0)
    target = PerspectiveNode("B", 2)
    chi = identity_event_correspondence(source, target)

    assert source.index != target.index
    assert chi.target_label("e0") == "e0"
    assert chi.target_label("e1") == "e1"
    assert mapped_event(chi, CANONICAL_EVENTS[2]) == CANONICAL_EVENTS[2]


def test_common_vertical_conditioning_family_is_identity_inverse_and_compositional():
    e0, e1, e2 = CANONICAL_EVENTS
    d = 7
    identity = common_vertical_conditioning_matrix(e0, e0, d)
    forward = common_vertical_conditioning_matrix(e0, e1, d)
    backward = common_vertical_conditioning_matrix(e1, e0, d)
    second = common_vertical_conditioning_matrix(e1, e2, d)
    direct = common_vertical_conditioning_matrix(e0, e2, d)

    assert np.allclose(identity, np.eye(d), atol=DEFAULT_ATOL, rtol=0.0)
    assert np.allclose(backward @ forward, np.eye(d), atol=DEFAULT_ATOL, rtol=0.0)
    assert np.allclose(second @ forward, direct, atol=DEFAULT_ATOL, rtol=0.0)


def test_perspective_vertical_map_is_common_vertical_structure_in_local_coordinates():
    node = PerspectiveNode("A", 1)
    e0, e1, _e2 = CANONICAL_EVENTS
    reduction = support_coordinate_reduction_matrix("A", 1, 3)
    expected = (
        reduction
        @ common_vertical_conditioning_matrix(e0, e1, reduction.shape[1])
        @ reduction.conj().T
    )

    actual = perspective_vertical_map(node, e0, e1)

    assert actual.shape == expected.shape == (7, 7)
    assert np.allclose(actual, expected, atol=DEFAULT_ATOL, rtol=0.0)


def test_stage6c_indirect_horizontal_maps_match_common_physical_bridge():
    source = PerspectiveNode("C", 0)
    target = PerspectiveNode("B", 2)
    atlas = build_partial_clock_atlas(source, target)
    paths = indirect_paths(atlas, source, target)
    bridge = horizontal_bridge_reference(source, target)

    assert len(paths) == 3
    assert not atlas.has_direct_map(source, target)
    for path in paths:
        assert np.allclose(
            atlas.compose_path(path),
            bridge,
            atol=DEFAULT_ATOL,
            rtol=0.0,
        )


def test_canonical_horizontal_vertical_squares_commute_for_all_paths_and_relations():
    source = PerspectiveNode("C", 0)
    target = PerspectiveNode("B", 2)
    atlas = build_partial_clock_atlas(source, target)
    chi = identity_event_correspondence(source, target)

    for path in indirect_paths(atlas, source, target):
        horizontal = atlas.compose_path(path)
        for source_event, target_event in ordered_event_relations():
            residual = square_residual_for_correspondence(
                horizontal,
                source,
                target,
                source_event,
                target_event,
                chi,
            )
            assert residual <= DEFAULT_ATOL


def test_low_level_square_residual_detects_noncommuting_target_vertical_map():
    source = PerspectiveNode("C", 0)
    target = PerspectiveNode("B", 2)
    atlas = build_partial_clock_atlas(source, target)
    horizontal = atlas.compose_path(indirect_paths(atlas, source, target)[0])
    e0, e1, e2 = CANONICAL_EVENTS
    source_vertical = perspective_vertical_map(source, e0, e1)
    target_vertical_good = perspective_vertical_map(target, e0, e1)
    target_vertical_bad = perspective_vertical_map(target, e0, e2)

    assert compatibility_square_residual(
        horizontal, source_vertical, target_vertical_good
    ) <= DEFAULT_ATOL
    assert compatibility_square_residual(
        horizontal, source_vertical, target_vertical_bad
    ) > DEFAULT_ATOL


def test_identity_correspondence_preserves_all_declared_order_relations():
    source = PerspectiveNode("A", 2)
    target = PerspectiveNode("C", 0)
    chi = identity_event_correspondence(source, target)

    assert all(
        order_covariant(chi, source_event, target_event)
        for source_event, target_event in ordered_event_relations()
    )


def test_mismatched_correspondence_breaks_order_and_commuting_squares_without_topology_change():
    diagnostics = mismatch_control_diagnostics()

    assert diagnostics.topology_unchanged is True
    assert diagnostics.path == ("C0", "A1", "B2")
    assert diagnostics.canonical_max_square_residual <= DEFAULT_ATOL
    assert diagnostics.mismatch_max_square_residual > DEFAULT_ATOL
    assert diagnostics.mismatch_failed_square_count >= 1
    assert diagnostics.canonical_order_violation_count == 0
    assert diagnostics.mismatch_order_violation_count >= 1


def test_wrong_chi_is_explicitly_different_from_identity_chi():
    source = PerspectiveNode("C", 0)
    target = PerspectiveNode("B", 2)
    good = identity_event_correspondence(source, target)
    bad = mismatched_event_correspondence(source, target)

    assert good.mapping != bad.mapping
    assert bad.orientation == "preserving"
    assert bad.target_label("e1") == "e2"
    assert bad.target_label("e2") == "e1"
    assert not order_covariant(bad, CANONICAL_EVENTS[1], CANONICAL_EVENTS[2])


def test_canonical_diagnostics_cover_three_paths_and_nine_squares():
    diagnostics = canonical_stage6d_diagnostics()

    assert diagnostics.source == PerspectiveNode("C", 0)
    assert diagnostics.target == PerspectiveNode("B", 2)
    assert diagnostics.path_count == 3
    assert diagnostics.event_relation_count == 3
    assert diagnostics.square_count == 9
    assert diagnostics.max_horizontal_bridge_residual <= DEFAULT_ATOL
    assert diagnostics.max_square_residual <= DEFAULT_ATOL
    assert diagnostics.order_violation_count == 0


def test_exhaustive_family_scan_covers_all_endpoint_paths_and_relations():
    scan = scan_horizontal_vertical_compatibility()

    assert scan.endpoint_case_count == 6 * 3**2 == 54
    assert scan.indirect_path_count == 54 * 3 == 162
    assert scan.event_relation_count == 54 * 3 == 162
    assert scan.square_count == 54 * 3 * 3 == 486
    assert scan.max_horizontal_bridge_residual <= DEFAULT_ATOL
    assert scan.max_square_residual <= DEFAULT_ATOL
    assert scan.order_violation_count == 0


def test_stage6d_rows_are_json_serializable_and_preserve_type_guards():
    rows = stage6d_rows()
    payload = json.dumps(rows, sort_keys=True)

    assert '"square_count": 486' in payload
    assert rows["guards"] == {
        "horizontal_vertical_identity_claimed": False,
        "clock_coordinate_defines_event_correspondence": False,
        "perspective_change_is_temporal_succession": False,
    }


def test_correspondence_endpoint_mismatch_is_rejected():
    source = PerspectiveNode("C", 0)
    target = PerspectiveNode("B", 2)
    wrong_target = PerspectiveNode("A", 0)
    chi = identity_event_correspondence(source, wrong_target)
    atlas = build_partial_clock_atlas(source, target)
    horizontal = atlas.compose_path(indirect_paths(atlas, source, target)[0])

    with pytest.raises(ValueError, match="endpoints"):
        square_residual_for_correspondence(
            horizontal,
            source,
            target,
            CANONICAL_EVENTS[0],
            CANONICAL_EVENTS[1],
            chi,
        )
