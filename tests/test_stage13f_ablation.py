from t_search.stage13_multi_constraint import (
    STAGE13A_BASIS_ID,
    STAGE13A_K_T,
    canonical_stage13a_representatives,
)
from t_search.stage13_ablation import (
    STAGE13F_ANOMALY_DETECTED,
    STAGE13F_ATOL,
    STAGE13F_BASIS_EQUIVALENT,
    STAGE13F_COMMUTING_BASIS_ID,
    STAGE13F_COMMUTING_PATH_CLASSIFICATION,
    STAGE13F_CROSS_ORBIT_REJECTED,
    STAGE13F_DECOUPLED_REJECTED,
    STAGE13F_GUARDS,
    STAGE13F_K_X_TILDE,
    STAGE13F_NOT_LICENSED,
    STAGE13F_ONE_CLOCK_INCOMPLETE,
    STAGE13F_RANK_DEFICIENT_REJECTED,
    canonical_stage13f_basis_equivalence_checks,
    canonical_stage13f_commuting_arrows,
    canonical_stage13f_commuting_mixed_path_checks,
    canonical_stage13f_commuting_quotient_classes,
    canonical_stage13f_false_positive_controls,
    stage13f_K_X_tilde,
    stage13f_diagnostics,
    stage13f_poisson_KT_KX_tilde,
    stage13f_summary,
)


def _controls_by_id():
    return {item.control_id: item for item in canonical_stage13f_false_positive_controls()}


def test_stage13f_equivalent_commuting_basis_closes_on_all_representatives_and_arrows():
    representatives = canonical_stage13a_representatives()
    assert len(representatives) == 36
    assert max(abs(stage13f_K_X_tilde(item.point())) for item in representatives) <= STAGE13F_ATOL
    assert max(abs(stage13f_poisson_KT_KX_tilde(item.point())) for item in representatives) <= STAGE13F_ATOL

    arrows = canonical_stage13f_commuting_arrows()
    assert len(arrows) == 144
    assert sum(item.generator_id == STAGE13A_K_T for item in arrows) == 72
    assert sum(item.generator_id == STAGE13F_K_X_TILDE for item in arrows) == 72
    assert all(item.basis_id == STAGE13F_COMMUTING_BASIS_ID for item in arrows)
    assert all(item.classification == STAGE13F_BASIS_EQUIVALENT for item in arrows)
    assert max(item.endpoint_residual for item in arrows) <= STAGE13F_ATOL
    assert max(item.constraint_residual for item in arrows) <= STAGE13F_ATOL


def test_stage13f_commuting_basis_recovers_same_four_quotient_classes_and_public_payload():
    quotients = canonical_stage13f_commuting_quotient_classes()
    assert len(quotients) == 4
    assert tuple(sorted(len(item.representative_ids) for item in quotients)) == (9, 9, 9, 9)
    assert all(len(item.inferred_orbit_ids) == 1 for item in quotients)
    assert all(item.matches_stage13d_quotient for item in quotients)
    assert all(item.classification == STAGE13F_BASIS_EQUIVALENT for item in quotients)
    assert max(item.max_Q_D_spread for item in quotients) <= STAGE13F_ATOL
    assert max(item.max_P_D_spread for item in quotients) <= STAGE13F_ATOL

    checks = canonical_stage13f_basis_equivalence_checks()
    assert len(checks) == 36
    assert all(item.noncommuting_basis_id == STAGE13A_BASIS_ID for item in checks)
    assert all(item.commuting_basis_id == STAGE13F_COMMUTING_BASIS_ID for item in checks)
    assert all(item.public_payload_equal for item in checks)
    assert all(item.classification == STAGE13F_BASIS_EQUIVALENT for item in checks)
    assert all(item.metaphysical_claim_status == STAGE13F_NOT_LICENSED for item in checks)
    assert max(item.dirac_residual for item in checks) <= STAGE13F_ATOL
    assert max(item.relational_residual for item in checks) <= STAGE13F_ATOL


def test_stage13f_equivalent_commuting_basis_needs_no_order_compensator():
    checks = canonical_stage13f_commuting_mixed_path_checks()
    assert len(checks) == 144
    assert all(item.classification == STAGE13F_COMMUTING_PATH_CLASSIFICATION for item in checks)
    assert all(item.metaphysical_claim_status == STAGE13F_NOT_LICENSED for item in checks)
    assert max(item.endpoint_separation for item in checks) <= STAGE13F_ATOL
    assert max(item.tx_target_residual for item in checks) <= STAGE13F_ATOL
    assert max(item.xt_target_residual for item in checks) <= STAGE13F_ATOL
    assert max(item.constraint_residual for item in checks) <= STAGE13F_ATOL


def test_stage13f_rank_decoupled_wrong_compensator_one_clock_and_cross_orbit_controls_are_rejected():
    controls = _controls_by_id()
    assert len(controls) == 6
    assert controls["rank_deficient_constraint_pair"].classification == STAGE13F_RANK_DEFICIENT_REJECTED
    assert controls["rank_deficient_constraint_pair"].witness_count == 36
    assert controls["decoupled_second_constraint"].classification == STAGE13F_DECOUPLED_REJECTED
    assert controls["decoupled_second_constraint"].witness_count == 72
    assert controls["wrong_compensator"].classification == "wrong_compensator_detected"
    assert controls["wrong_compensator"].witness_count == 144
    assert controls["one_clock_incomplete"].classification == STAGE13F_ONE_CLOCK_INCOMPLETE
    assert controls["one_clock_incomplete"].witness_count == 12
    assert controls["cross_orbit_single_invariant_false_match"].classification == STAGE13F_CROSS_ORBIT_REJECTED
    assert controls["cross_orbit_single_invariant_false_match"].witness_count == 2
    for control_id in (
        "rank_deficient_constraint_pair",
        "decoupled_second_constraint",
        "wrong_compensator",
        "one_clock_incomplete",
        "cross_orbit_single_invariant_false_match",
    ):
        assert controls[control_id].rejected
        assert controls[control_id].residual > STAGE13F_ATOL
        assert controls[control_id].metaphysical_claim_status == STAGE13F_NOT_LICENSED


def test_stage13f_non_first_class_deformation_is_detected_as_anomaly():
    control = _controls_by_id()["non_first_class_K_X_bad"]
    assert control.classification == STAGE13F_ANOMALY_DETECTED
    assert control.rejected
    assert control.witness_count == 36
    assert control.residual > STAGE13F_ATOL
    assert control.metaphysical_claim_status == STAGE13F_NOT_LICENSED


def test_stage13f_diagnostics_close_criteria_44_through_47_in_source_evidence():
    d = stage13f_diagnostics()
    assert d.representative_count == 36
    assert d.commuting_constraint_surface_count == 36
    assert d.commuting_arrow_count == 144
    assert d.commuting_phi_T_arrow_count == 72
    assert d.commuting_phi_X_arrow_count == 72
    assert d.commuting_quotient_class_count == 4
    assert d.commuting_quotient_class_sizes == (9, 9, 9, 9)
    assert d.stage13d_membership_match_count == 4
    assert d.basis_equivalence_check_count == 36
    assert d.basis_equivalent_count == 36
    assert d.commuting_mixed_path_check_count == 144
    assert d.commuting_mixed_path_closed_count == 144
    assert d.max_K_X_tilde_constraint_residual <= STAGE13F_ATOL
    assert d.max_KT_KX_tilde_bracket_residual <= STAGE13F_ATOL
    assert d.max_commuting_arrow_endpoint_residual <= STAGE13F_ATOL
    assert d.max_commuting_arrow_constraint_residual <= STAGE13F_ATOL
    assert d.max_commuting_mixed_endpoint_separation <= STAGE13F_ATOL
    assert d.max_commuting_mixed_target_residual <= STAGE13F_ATOL
    assert d.max_commuting_mixed_constraint_residual <= STAGE13F_ATOL
    assert d.max_basis_dirac_residual <= STAGE13F_ATOL
    assert d.max_basis_relational_residual <= STAGE13F_ATOL
    assert d.false_positive_control_count == 6
    assert d.rejected_false_positive_control_count == 6
    assert d.rank_deficient_rejected
    assert d.decoupled_rejected
    assert d.wrong_compensator_rejected
    assert d.one_clock_incomplete_rejected
    assert d.cross_orbit_false_positive_rejected
    assert d.anomaly_detected
    assert d.all_metaphysical_claims_not_licensed
    assert d.criteria_44_47_satisfied


def test_stage13f_summary_keeps_basis_and_metaphysical_boundaries_explicit():
    summary = stage13f_summary()
    assert summary["bounded_result"].endswith("= established")
    assert summary["basis_classification"] == STAGE13F_BASIS_EQUIVALENT
    assert tuple(summary["guards"]) == STAGE13F_GUARDS
    assert summary["next"].startswith("Stage 13G")
    for phrase in (
        "noncommuting constraint presentation != fundamental physical non-Abelianity",
        "constraint-basis change != physical-orbit change",
        "basis-equivalent finite quotient != refoliation invariance",
        "wrong compensator failure != physical time asymmetry",
        "constraint-algebra anomaly != ontological becoming",
        "constraint-algebra/refoliation precursor != general relativity",
        "Dirac-invariant data + relational change != proof of eternalism",
        "complete relational observable != ontological becoming by definition",
    ):
        assert phrase in summary["guards"]
