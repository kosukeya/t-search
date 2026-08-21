import json

import pytest

from t_search.stage6_ablation import (
    AblationStatus,
    LAYERS,
    ROLE_IDS,
    RoleEvidence,
    accessibility_inaccessibility_control,
    baseline_role_evidence,
    build_stage6f_ablation_matrix,
    omega_reconstruction_diagnostics,
    stage6f_minimality_summary,
    stage6f_rows,
)


def _case(layer: str):
    return next(
        case for case in build_stage6f_ablation_matrix()
        if case.removed_layer == layer
    )


def test_status_evaluator_preserves_frozen_priority_order() -> None:
    assert RoleEvidence(role="x", applicable=False).status is AblationStatus.NOT_APPLICABLE
    assert (
        RoleEvidence(
            role="x",
            direct_available=True,
            reconstruction_available=True,
            globally_represented=True,
            locally_accessible=False,
            decisive_loss=True,
        ).status
        is AblationStatus.PRESERVED
    )
    assert (
        RoleEvidence(role="x", reconstruction_available=True, decisive_loss=True).status
        is AblationStatus.RECONSTRUCTIBLE
    )
    assert (
        RoleEvidence(
            role="x",
            globally_represented=True,
            locally_accessible=False,
            decisive_loss=True,
        ).status
        is AblationStatus.INACCESSIBLE
    )
    assert RoleEvidence(role="x", decisive_loss=True).status is AblationStatus.LOST
    assert RoleEvidence(role="x").status is AblationStatus.NOT_ESTABLISHED


def test_baseline_recomputes_all_frozen_roles_as_preserved() -> None:
    baseline = baseline_role_evidence()
    assert tuple(probe.role for probe in baseline) == ROLE_IDS
    assert all(probe.status is AblationStatus.PRESERVED for probe in baseline)


def test_ablation_matrix_contains_exactly_five_frozen_layer_cases() -> None:
    cases = build_stage6f_ablation_matrix()
    assert tuple(case.removed_layer for case in cases) == LAYERS
    assert all(case.irreducibility_status is AblationStatus.NOT_ESTABLISHED for case in cases)


def test_o_ablation_loses_explicit_order_but_preserves_independent_roles() -> None:
    case = _case("O")
    assert case.status("succession_order") is AblationStatus.LOST
    assert case.status("perspective_transport") is AblationStatus.PRESERVED
    assert case.status("record_defined_direction") is AblationStatus.PRESERVED
    assert case.status("modal_branching_semantics") is AblationStatus.PRESERVED
    assert case.status("cross_perspective_operational_consistency") is AblationStatus.PRESERVED
    assert case.status("local_record_accessibility") is AblationStatus.PRESERVED
    assert case.status("P_O_compatibility") is AblationStatus.NOT_APPLICABLE


def test_p_ablation_loses_perspective_transport_and_makes_cross_perspective_tests_not_applicable() -> None:
    case = _case("P")
    assert case.status("succession_order") is AblationStatus.PRESERVED
    assert case.status("perspective_transport") is AblationStatus.LOST
    assert case.status("record_defined_direction") is AblationStatus.PRESERVED
    assert case.status("modal_branching_semantics") is AblationStatus.PRESERVED
    assert (
        case.status("cross_perspective_operational_consistency")
        is AblationStatus.NOT_APPLICABLE
    )
    assert case.status("P_O_compatibility") is AblationStatus.NOT_APPLICABLE
    assert case.status("P_R_compatibility") is AblationStatus.NOT_APPLICABLE
    assert case.status("P_V_compatibility") is AblationStatus.NOT_APPLICABLE


def test_r_ablation_uses_no_record_control_and_loses_record_roles_only() -> None:
    case = _case("R")
    direction = next(
        probe for probe in case.probes if probe.role == "record_defined_direction"
    )
    measurements = dict(direction.measurements)
    assert case.status("record_defined_direction") is AblationStatus.LOST
    assert case.status("local_record_accessibility") is AblationStatus.LOST
    assert measurements["no_record_record_defined"] is False
    assert measurements["no_record_orientation"] == "none"
    assert measurements["no_record_record_score"] == pytest.approx(0.0, abs=1e-12)
    assert measurements["no_record_accessibility_score"] == pytest.approx(0.0, abs=1e-12)
    assert case.status("succession_order") is AblationStatus.PRESERVED
    assert case.status("perspective_transport") is AblationStatus.PRESERVED
    assert case.status("P_R_compatibility") is AblationStatus.NOT_APPLICABLE


def test_v_ablation_loses_typed_modal_semantics_without_collapsing_operational_role() -> None:
    case = _case("V")
    assert case.status("modal_branching_semantics") is AblationStatus.LOST
    assert case.status("cross_perspective_operational_consistency") is AblationStatus.PRESERVED
    assert case.status("record_defined_direction") is AblationStatus.PRESERVED
    assert case.status("P_V_compatibility") is AblationStatus.NOT_APPLICABLE


def test_omega_ablation_reconstructs_operational_consistency_from_retained_p() -> None:
    case = _case("Omega")
    probe = next(
        probe
        for probe in case.probes
        if probe.role == "cross_perspective_operational_consistency"
    )
    assert probe.status is AblationStatus.RECONSTRUCTIBLE
    measurements = dict(probe.measurements)
    assert measurements["bare_matrix_mismatch_count"] > 0
    assert measurements["max_bare_matrix_probability_residual"] > 1e-10
    assert measurements["max_reconstructed_probability_residual"] <= 1e-10
    assert measurements["reconstructed_match_count"] == measurements["comparison_count"]


def test_omega_reconstruction_diagnostic_distinguishes_bare_and_transported_observables() -> None:
    diagnostics = omega_reconstruction_diagnostics()
    assert diagnostics.comparison_count == 54
    assert diagnostics.raw_correspondence_fails
    assert diagnostics.bare_matrix_mismatch_count > 0
    assert diagnostics.reconstructed_correspondence_holds
    assert diagnostics.max_reconstructed_probability_residual <= diagnostics.tolerance


def test_hidden_record_control_is_inaccessible_not_lost() -> None:
    control = accessibility_inaccessibility_control()
    assert control.status is AblationStatus.INACCESSIBLE
    assert control.globally_represented is True
    assert control.locally_accessible is False
    measurements = dict(control.measurements)
    assert measurements["global_record_transport_compatible"] is True
    assert measurements["target_record_exposed"] is False
    assert measurements["target_record_score"] is None


def test_lost_status_changes_when_reconstruction_witness_is_supplied() -> None:
    evidence = RoleEvidence(role="synthetic", decisive_loss=True)
    assert evidence.status is AblationStatus.LOST
    reconstructed = RoleEvidence(
        role="synthetic",
        reconstruction_available=True,
        decisive_loss=True,
    )
    assert reconstructed.status is AblationStatus.RECONSTRUCTIBLE


def test_minimality_summary_is_bounded_and_does_not_claim_irreducibility() -> None:
    summary = stage6f_minimality_summary()
    assert summary["own_role_status_after_ablation"] == {
        "O": "lost",
        "P": "lost",
        "R": "lost",
        "V": "lost",
        "Omega": "reconstructible",
    }
    assert summary["layers_lost_in_declared_interface"] == ["O", "P", "R", "V"]
    assert summary["layers_reconstructible_in_declared_interface"] == ["Omega"]
    assert summary["metaphysical_irreducibility_established"] is False


def test_stage6f_rows_are_json_serializable_and_preserve_interpretation_guards() -> None:
    rows = stage6f_rows()
    json.dumps(rows)
    assert rows["status_vocabulary"] == [
        "preserved",
        "reconstructible",
        "inaccessible",
        "lost",
        "not_applicable",
        "not_established",
    ]
    assert rows["interpretation_guards"]["lost_means_metaphysically_irreducible"] is False
    assert rows["interpretation_guards"]["software_dependency_proves_fundamentality"] is False
    assert rows["interpretation_guards"]["inaccessible_means_globally_absent"] is False
    assert (
        rows["interpretation_guards"]["omega_reconstructible_here_means_universally_redundant"]
        is False
    )
