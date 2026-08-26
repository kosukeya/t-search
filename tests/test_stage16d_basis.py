from fractions import Fraction

from t_search.stage16_basis import (
    STAGE16D_AFFINE_CERTIFICATE,
    STAGE16D_CLASSIFICATION,
    STAGE16D_GUARDS,
    STAGE16D_KNOWN_SEED_ID,
    STAGE16D_L0,
    STAGE16D_L1,
    STAGE16D_NONLOCAL,
    STAGE16D_UNRESTRICTED_ID,
    canonical_stage16d_candidate_audits,
    canonical_stage16d_candidates,
    canonical_stage16d_content_audits,
    stage16d_affine_ansatz_audit,
    stage16d_diagnostics,
    stage16d_known_seed_locality_audit,
    stage16d_lfinite_search_audit,
)


def test_stage16d_known_global_seed_is_strong_but_not_one_step_l1():
    audits = {item.candidate_id: item for item in canonical_stage16d_candidate_audits()}
    known = audits[STAGE16D_KNOWN_SEED_ID]
    locality = stage16d_known_seed_locality_audit()
    assert known.locality_class == STAGE16D_NONLOCAL
    assert not known.one_step_l1
    assert known.strongly_commuting
    assert known.invertible_equivalent_on_tested_family
    assert known.max_all_unsmeared_bracket <= 1e-10
    assert known.max_all_smeared_bracket <= 1e-10
    assert locality.opposite_generator_nonzero_row_count == 4
    assert locality.determinant_clock_dependence_count == 4
    assert not locality.forward_map_l1
    assert locality.inverse_map_l1
    assert locality.transformed_seed_support_same_site


def test_stage16d_l0_and_one_step_l1_explicit_candidate_families_have_no_strong_witness():
    audits = canonical_stage16d_candidate_audits()
    l0 = [item for item in audits if item.locality_class == STAGE16D_L0]
    l1 = [item for item in audits if item.locality_class == STAGE16D_L1]
    assert len(l0) == 3
    assert len(l1) == 16
    assert all(item.first_class_on_positive_family for item in (*l0, *l1))
    assert not any(item.strongly_commuting for item in l0)
    assert not any(item.strongly_commuting for item in l1)
    assert all(item.invertible_equivalent_on_tested_family for item in (*l0, *l1))
    # The full positive + off-surface explicit L1 family has a strictly
    # positive minimum strong-commutation defect.  Pin the observed exact
    # dyadic value instead of overstating the lower bound.
    assert min(item.max_all_unsmeared_bracket for item in l1) == 0.09375


def test_stage16d_depth_four_elementary_l1_composition_search_is_exact_and_witness_free():
    audit = stage16d_lfinite_search_audit()
    assert audit.elementary_operation_count == 16
    assert audit.max_depth == 4
    assert audit.depth_candidate_counts == (16, 256, 4096, 65536)
    assert audit.total_candidate_count == 69904
    assert audit.strongly_commuting_witness_count == 0
    assert audit.exact_witness_clocks == (-1.0, -1.0, -1.0, -1.0)
    assert audit.minimum_exact_max_bracket == Fraction(7, 32)
    assert len(audit.minimum_exact_max_bracket_sequence) == 4
    assert audit.all_candidates_invertible_by_unit_shear
    assert audit.all_candidates_content_equivalent_by_invertible_basis_change
    assert audit.classification == "no_witness_in_frozen_depth_le_4_composition_search"


def test_stage16d_affine_cyclic_l1_ansatz_has_exact_invertibility_saturation_certificate():
    audit = stage16d_affine_ansatz_audit()
    assert audit.parameter_count == 12
    assert audit.raw_coefficient_equation_count == 608
    assert audit.sign_reduced_equation_count == 137
    assert audit.saturated_groebner_basis == ("1",)
    assert not audit.invertible_solution_exists
    assert audit.certificate == STAGE16D_AFFINE_CERTIFICATE
    assert "b0c" in audit.determinant_at_origin
    assert "bmc" in audit.determinant_at_origin
    assert "bpc" in audit.determinant_at_origin


def test_stage16d_all_explicit_equivalent_candidates_preserve_quotient_dirac_and_relational_content():
    candidates = canonical_stage16d_candidates()
    contents = canonical_stage16d_content_audits()
    assert len(candidates) == 21
    assert len(contents) == 21
    assert all(item.quotient_class_count == 4 for item in contents)
    assert all(item.min_quotient_class_size == 81 for item in contents)
    assert all(item.max_quotient_class_size == 81 for item in contents)
    assert all(item.quotient_preserved for item in contents)
    assert all(item.dirac_pair_preserved for item in contents)
    assert all(item.complete_relational_preserved for item in contents)


def test_stage16d_only_unrestricted_controls_are_strong_in_explicit_candidate_table():
    audits = canonical_stage16d_candidate_audits()
    strong = {item.candidate_id for item in audits if item.strongly_commuting}
    assert strong == {STAGE16D_KNOWN_SEED_ID, STAGE16D_UNRESTRICTED_ID}
    assert all(item.locality_class == STAGE16D_NONLOCAL for item in audits if item.candidate_id in strong)


def test_stage16d_diagnostics_issue_bounded_nonlocal_only_classification():
    d = stage16d_diagnostics()
    assert d.candidate_count == 21
    assert d.l0_candidate_count == 3
    assert d.one_step_l1_candidate_count == 16
    assert d.one_step_l1_strong_count == 0
    assert d.nonlocal_candidate_count == 2
    assert d.nonlocal_strong_count == 2
    assert d.content_audit_count == 21
    assert d.content_preserved_count == 21
    assert d.lfinite_candidate_count == 69904
    assert d.lfinite_strong_count == 0
    assert d.lfinite_minimum_exact_max_bracket == 0.21875
    assert d.affine_raw_equation_count == 608
    assert d.affine_sign_reduced_equation_count == 137
    assert not d.affine_invertible_strong_solution_exists
    assert not d.known_seed_one_step_l1
    assert d.known_seed_strongly_commuting
    assert d.minimum_exhibited_locality_depth is None
    assert d.global_abelianization_established
    assert not d.local_witness_found_in_frozen_search
    assert d.classification == STAGE16D_CLASSIFICATION
    assert d.criteria_32_39_satisfied


def test_stage16d_interpretation_guards_remain_explicit():
    guards = set(STAGE16D_GUARDS)
    for expected in (
        "known global Abelianization != proof that all Abelianizations are nonlocal",
        "no L1 witness in frozen search != no L1 Abelianization exists",
        "only nonlocal witness found != fundamental physical non-Abelianity",
        "global Abelianization != physical triviality",
        "failure to Abelianize != ontological becoming",
        "repository validation != new scientific evidence",
    ):
        assert expected in guards
