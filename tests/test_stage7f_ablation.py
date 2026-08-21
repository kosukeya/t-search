import json

import pytest

from t_search.stage7_ablation import (
    ABLATION_IDS,
    ROLE_IDS,
    RoleEvidence,
    RoleStatus,
    baseline_role_evidence,
    build_stage7f_ablation_matrix,
    memory_removal_diagnostics,
    no_record_perspective_diagnostics,
    perspective_reconstruction_diagnostics,
    r_reconstruction_from_p_o_diagnostics,
    stage7f_mismatch_matrix,
    stage7f_summary,
)

ATOL = 1e-9


def _case(name):
    return next(c for c in build_stage7f_ablation_matrix() if c.ingredient == name)


def test_status_priority():
    assert RoleEvidence(role="x", direct_available=True, decisive_loss=True).status is RoleStatus.PRESERVED
    assert RoleEvidence(role="x", reconstruction_available=True, decisive_loss=True).status is RoleStatus.RECONSTRUCTIBLE
    assert RoleEvidence(role="x", globally_represented=True, locally_accessible=False).status is RoleStatus.INACCESSIBLE
    assert RoleEvidence(role="x", decisive_loss=True).status is RoleStatus.LOST
    assert RoleEvidence(role="x").status is RoleStatus.NOT_ESTABLISHED


def test_baseline_and_frozen_matrix_shape():
    baseline = baseline_role_evidence()
    assert tuple(x.role for x in baseline) == ROLE_IDS
    assert all(x.status is RoleStatus.PRESERVED for x in baseline)
    cases = build_stage7f_ablation_matrix()
    assert tuple(c.ingredient for c in cases) == ABLATION_IDS
    assert all(tuple(p.role for p in c.probes) == ROLE_IDS for c in cases)


def test_memory_removal_loses_record_not_clock_role():
    d = memory_removal_diagnostics()
    c = _case("memory_removed")
    assert d.baseline_lower_information == pytest.approx(1.0, abs=ATOL)
    assert d.baseline_upper_information == pytest.approx(0.0, abs=ATOL)
    assert d.removed_lower_information == pytest.approx(0.0, abs=ATOL)
    assert d.removed_upper_information == pytest.approx(0.0, abs=ATOL)
    assert d.removed_record_score == pytest.approx(0.0, abs=ATOL)
    assert d.removed_accessibility_score == pytest.approx(0.0, abs=ATOL)
    assert d.removed_orientation == "none"
    assert not d.record_survives_removal
    assert c.status("target_specific_record") is RoleStatus.LOST
    assert c.status("record_defined_direction") is RoleStatus.LOST
    assert c.status("local_record_readout") is RoleStatus.LOST
    assert c.status("perspective_transport") is RoleStatus.PRESERVED
    assert c.status("P_R_covariance") is RoleStatus.NOT_ESTABLISHED


def test_no_record_retains_p_and_anchor_without_r():
    d = no_record_perspective_diagnostics()
    c = _case("record_coupling_neutralized")
    assert d.comparisons == 54 and d.min_rank == 14
    assert d.max_state_transport_residual <= ATOL
    assert d.max_inverse_residual <= ATOL
    assert d.max_metric_covariance_residual <= ATOL
    assert d.perspective_structure_preserved and d.internally_anchored
    assert not d.record_defined
    assert d.record_score == pytest.approx(0.0, abs=ATOL)
    assert d.accessibility_score == pytest.approx(0.0, abs=ATOL)
    assert c.status("perspective_transport") is RoleStatus.PRESERVED
    assert c.status("internal_history_anchor") is RoleStatus.PRESERVED
    assert c.status("target_specific_record") is RoleStatus.LOST
    assert c.status("record_defined_direction") is RoleStatus.LOST
    assert c.status("P_R_covariance") is RoleStatus.NOT_ESTABLISHED


def test_anchor_removal_keeps_correlation_but_not_direction():
    c = _case("history_anchor_removed")
    assert c.status("target_specific_record") is RoleStatus.PRESERVED
    assert c.status("local_record_readout") is RoleStatus.PRESERVED
    assert c.status("record_defined_direction") is RoleStatus.NOT_ESTABLISHED
    assert c.status("P_R_covariance") is RoleStatus.NOT_ESTABLISHED
    assert c.status("internal_history_anchor") is RoleStatus.LOST


def test_explicit_maps_are_reconstructible_from_reductions():
    d = perspective_reconstruction_diagnostics()
    c = _case("explicit_perspective_maps_removed")
    assert d.comparisons == 54
    assert d.max_reference_map_residual <= ATOL
    assert d.max_state_transport_residual <= ATOL
    assert d.max_inverse_residual <= ATOL
    assert d.max_metric_covariance_residual <= ATOL
    assert d.max_record_score_residual <= ATOL
    assert d.max_accessibility_residual <= ATOL
    assert d.reconstructible
    assert c.status("perspective_transport") is RoleStatus.RECONSTRUCTIBLE
    assert c.status("P_R_covariance") is RoleStatus.RECONSTRUCTIBLE


def test_missing_chi_is_not_established_not_false():
    c = _case("event_correspondence_removed")
    assert c.status("target_specific_record") is RoleStatus.PRESERVED
    assert c.status("record_defined_direction") is RoleStatus.PRESERVED
    assert c.status("perspective_transport") is RoleStatus.PRESERVED
    assert c.status("P_R_covariance") is RoleStatus.NOT_ESTABLISHED


@pytest.mark.parametrize("name", ("local_access_hidden", "local_access_maximally_noisy"))
def test_hidden_and_noisy_are_inaccessible_not_lost(name):
    c = _case(name)
    assert c.status("target_specific_record") is RoleStatus.PRESERVED
    assert c.status("record_defined_direction") is RoleStatus.PRESERVED
    assert c.status("local_record_readout") is RoleStatus.INACCESSIBLE
    assert c.status("perspective_transport") is RoleStatus.PRESERVED
    assert c.status("P_R_covariance") is RoleStatus.PRESERVED


def test_mismatch_controls_detect_wrong_chi_and_local_edge():
    rows = {m.mismatch: m for m in stage7f_mismatch_matrix()}
    wrong = rows["wrong_or_misdeclared_chi"]
    assert wrong.detected
    wm = dict(wrong.measurements)
    assert wm["record_score_residual"] == pytest.approx(2.0, abs=ATOL)
    assert wm["accessibility_score_residual"] == pytest.approx(1.0, abs=ATOL)
    assert wm["source_orientation"] == "lower-index"
    assert wm["wrong_orientation"] == "upper-index"
    edge = rows["perturbed_local_perspective_edge"]
    assert edge.detected
    em = dict(edge.measurements)
    assert em["map_residual"] > 1e-3
    assert em["state_residual"] > 1e-3
    assert em["metric_residual"] > 1e-3
    assert em["record_score_residual"] > 1e-4
    assert em["unaffected_paths_consistent"] is True
    assert em["observable_residual"] <= ATOL


def test_p_plus_o_countermodel_does_not_reconstruct_r():
    d = r_reconstruction_from_p_o_diagnostics()
    assert d.perspective_structure_preserved
    assert d.history_anchor_preserved
    assert not d.no_record_record_defined
    assert d.no_record_record_score == pytest.approx(0.0, abs=ATOL)
    assert d.no_record_accessibility_score == pytest.approx(0.0, abs=ATOL)
    assert d.p_and_o_retained_without_r
    assert not d.reconstruction_witness_found


def test_summary_is_bounded_and_serializable():
    s = stage7f_summary()
    json.dumps(s)
    assert s["status_vocabulary"] == ["preserved", "reconstructible", "inaccessible", "lost", "not_established"]
    assert s["own_role_status_after_neutralization"] == {
        "memory_record_resource": "lost",
        "record_coupling": "lost",
        "history_anchor": "lost",
        "explicit_perspective_maps": "reconstructible",
        "event_correspondence_for_P_R": "not_established",
        "hidden_local_access": "inaccessible",
    }
    b = s["bounded_interpretation"]
    assert b["P_plus_O_implies_R_in_declared_stage7_family"] is False
    assert b["explicit_cross_clock_edge_matrices_are_primitive_in_declared_interface"] is False
    assert b["R_metaphysically_irreducible"] is False
    assert b["P_universally_redundant"] is False
    assert b["inaccessible_means_globally_absent"] is False
    assert b["not_established_means_false"] is False
    g = s["guards"]
    assert "lost != metaphysically irreducible" in g
    assert "reconstructible != universally redundant" in g
    assert "explicit perspective-map reconstruction != elimination of the perspective layer" in g
    assert "not_established != false" in g
