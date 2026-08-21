import json

import numpy as np
import pytest

from t_search.stage5_clock_change import DEFAULT_ATOL
from t_search.stage6_partial_atlas import (
    DirectMapUnavailableError,
    PerspectiveNode,
    UnknownPerspectiveError,
    canonical_partial_clock_atlas,
    diagnose_partial_atlas,
    external_direct_reference,
    indirect_paths,
    perturb_direct_edge,
    scan_partial_clock_atlas_family,
    stage6c_summary_rows,
)


def test_canonical_partial_atlas_omits_direct_edge_but_retains_target():
    atlas, source, target = canonical_partial_clock_atlas()

    assert source == PerspectiveNode("C", 0)
    assert target == PerspectiveNode("B", 2)
    assert atlas.has_perspective(source)
    assert atlas.has_perspective(target)
    assert not atlas.has_direct_map(source, target)
    assert len(atlas.perspectives) == 5
    assert len(atlas.edges) == 7

    with pytest.raises(DirectMapUnavailableError, match="no primitive direct map"):
        atlas.direct_map(source, target)


def test_absent_direct_edge_is_distinct_from_absent_perspective():
    atlas, source, target = canonical_partial_clock_atlas()
    absent = PerspectiveNode("A", 99)

    assert atlas.has_perspective(target)
    assert not atlas.has_direct_map(source, target)
    assert not atlas.has_perspective(absent)

    with pytest.raises(DirectMapUnavailableError):
        atlas.direct_map(source, target)
    with pytest.raises(UnknownPerspectiveError, match="unknown target perspective"):
        atlas.direct_map(source, absent)


def test_missing_c0_to_b2_map_is_reconstructed_by_three_two_hop_paths():
    atlas, source, target = canonical_partial_clock_atlas()
    paths = indirect_paths(atlas, source, target)
    reference = external_direct_reference(source, target, 3)

    assert len(paths) == 3
    assert {path[1] for path in paths} == {
        PerspectiveNode("A", 0),
        PerspectiveNode("A", 1),
        PerspectiveNode("A", 2),
    }
    for path in paths:
        assert np.allclose(
            atlas.compose_path(path),
            reference,
            atol=DEFAULT_ATOL,
            rtol=0.0,
        )


def test_alternative_indirect_paths_are_consistent_on_common_endpoints():
    atlas, source, target = canonical_partial_clock_atlas()
    paths = indirect_paths(atlas, source, target)

    for first_index in range(len(paths)):
        for second_index in range(first_index + 1, len(paths)):
            assert atlas.path_residual(
                paths[first_index], paths[second_index]
            ) <= DEFAULT_ATOL


def test_each_available_reconstruction_path_closes_to_identity_loop():
    atlas, source, target = canonical_partial_clock_atlas()
    paths = indirect_paths(atlas, source, target)

    for path in paths:
        loop = path + (source,)
        assert atlas.loop_residual(loop) <= DEFAULT_ATOL


def test_canonical_partial_atlas_diagnostics_meet_frozen_stage6c_conditions():
    atlas, source, target = canonical_partial_clock_atlas()
    reference = external_direct_reference(source, target, 3)
    diagnostic = diagnose_partial_atlas(atlas, source, target, reference)

    assert diagnostic.target_present is True
    assert diagnostic.direct_edge_present is False
    assert diagnostic.path_count == 3
    assert diagnostic.max_indirect_direct_residual <= DEFAULT_ATOL
    assert diagnostic.max_pairwise_path_residual <= DEFAULT_ATOL
    assert diagnostic.max_loop_residual <= DEFAULT_ATOL


def test_exhaustive_partial_atlas_scan_covers_all_ordered_endpoints_and_routes():
    scan = scan_partial_clock_atlas_family(3)

    assert scan.endpoint_case_count == 6 * 3**2 == 54
    assert scan.indirect_path_count == 6 * 3**3 == 162
    assert scan.closed_loop_count == 162
    assert scan.missing_direct_edge_count == 54
    assert scan.present_target_count == 54
    assert scan.max_indirect_direct_residual <= DEFAULT_ATOL
    assert scan.max_pairwise_path_residual <= DEFAULT_ATOL
    assert scan.max_loop_residual <= DEFAULT_ATOL


def test_deliberate_single_edge_perturbation_breaks_path_and_loop_consistency():
    atlas, source, target = canonical_partial_clock_atlas()
    reference = external_direct_reference(source, target, 3)
    corrupted = perturb_direct_edge(
        atlas,
        source,
        PerspectiveNode("A", 1),
        epsilon=1e-4,
    )
    diagnostic = diagnose_partial_atlas(corrupted, source, target, reference)

    assert diagnostic.target_present is True
    assert diagnostic.direct_edge_present is False
    assert diagnostic.path_count == 3
    assert diagnostic.max_indirect_direct_residual > 100 * DEFAULT_ATOL
    assert diagnostic.max_pairwise_path_residual > 100 * DEFAULT_ATOL
    assert diagnostic.max_loop_residual > 100 * DEFAULT_ATOL


def test_perturbation_is_local_to_routes_using_the_changed_edge():
    atlas, source, target = canonical_partial_clock_atlas()
    corrupted = perturb_direct_edge(
        atlas,
        source,
        PerspectiveNode("A", 1),
        epsilon=1e-4,
    )

    path_a0 = (source, PerspectiveNode("A", 0), target)
    path_a1 = (source, PerspectiveNode("A", 1), target)
    path_a2 = (source, PerspectiveNode("A", 2), target)

    assert corrupted.path_residual(path_a0, path_a2) <= DEFAULT_ATOL
    assert corrupted.path_residual(path_a0, path_a1) > 100 * DEFAULT_ATOL
    assert corrupted.loop_residual(path_a0 + (source,)) <= DEFAULT_ATOL
    assert corrupted.loop_residual(path_a1 + (source,)) > 100 * DEFAULT_ATOL


def test_partial_atlas_rejects_invalid_path_and_perturbation_requests():
    atlas, source, target = canonical_partial_clock_atlas()

    with pytest.raises(ValueError, match="at least one edge"):
        atlas.compose_path((source,))
    with pytest.raises(ValueError, match="common source and target"):
        atlas.path_residual(
            (source, PerspectiveNode("A", 0), target),
            (PerspectiveNode("A", 0), target),
        )
    with pytest.raises(ValueError, match="close at its source"):
        atlas.loop_residual((source, PerspectiveNode("A", 0), target))
    with pytest.raises(DirectMapUnavailableError):
        perturb_direct_edge(atlas, source, target, epsilon=1e-4)
    with pytest.raises(ValueError, match="nonzero"):
        perturb_direct_edge(
            atlas,
            source,
            PerspectiveNode("A", 0),
            epsilon=0.0,
        )


def test_stage6c_summary_is_json_serializable_and_reports_perturbation_detection():
    summary = stage6c_summary_rows()
    payload = json.dumps(summary, sort_keys=True)

    assert '"canonical_diagnostics"' in payload
    assert '"family_scan"' in payload
    assert summary["canonical_diagnostics"]["direct_edge_present"] is False
    assert summary["canonical_diagnostics"]["max_loop_residual"] <= DEFAULT_ATOL
    assert summary["perturbed_diagnostics"]["max_loop_residual"] > 100 * DEFAULT_ATOL
