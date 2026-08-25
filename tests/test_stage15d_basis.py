import pytest

from t_search.stage15_basis import (
    STAGE15D_CLASSIFICATION,
    STAGE15D_GUARDS,
    STAGE15D_KNOWN_SEED_ID,
    STAGE15D_L0,
    STAGE15D_L1,
    STAGE15D_L1_SCALED_WITNESS_ID,
    STAGE15D_L1_WITNESS_ID,
    STAGE15D_LFINITE,
    STAGE15D_METAPHYSICAL_CLAIM_STATUS,
    STAGE15D_NONLOCAL,
    STAGE15D_TYPED_STATUS,
    STAGE15D_UNRESTRICTED_ID,
    canonical_stage15d_candidate_audits,
    canonical_stage15d_candidates,
    canonical_stage15d_content_audits,
    stage15d_diagnostics,
    stage15d_locality_audit,
    stage15d_seed_factorization_audit,
    stage15d_transformed_values_and_gradients,
)
from t_search.stage15_local import (
    STAGE15A_ATOL,
    canonical_stage15a_off_surface_probes,
    stage15a_constraints,
    stage15a_seed_constraints,
)


def _candidate(candidate_id):
    return next(
        item for item in canonical_stage15d_candidates()
        if item.candidate_id == candidate_id
    )


def _audit(candidate_id):
    return next(
        item for item in canonical_stage15d_candidate_audits()
        if item.candidate_id == candidate_id
    )


def test_stage15d_criterion_32_l0_and_locality_classes_remain_frozen():
    candidates = canonical_stage15d_candidates()
    locality = [stage15d_locality_audit(item) for item in candidates]
    assert len(candidates) == 14

    l0 = [item for item in locality if item.locality_class == STAGE15D_L0]
    strict_l1 = [item for item in locality if item.locality_class == STAGE15D_L1]
    assert len(l0) == 3
    assert len(strict_l1) == 7
    assert {item.family_id for item in l0} == {"diagonal_scalar_rescaling"}
    assert all(item.forward_l1_ok and item.inverse_l1_ok for item in (*l0, *strict_l1))


def test_stage15d_criterion_33_one_step_l1_tail_witness_is_distinct_from_full_seed_reconstruction():
    witness = _candidate(STAGE15D_L1_WITNESS_ID)
    locality = stage15d_locality_audit(witness)
    assert locality.locality_class == STAGE15D_L1
    assert locality.one_step_l1
    assert not locality.l0

    point = canonical_stage15a_off_surface_probes()[0]
    _, transformed, _ = stage15d_transformed_values_and_gradients(witness, point)
    C0, _, _ = stage15a_constraints(point)
    _, K1, K2 = stage15a_seed_constraints(point)
    assert transformed[0] == pytest.approx(C0, abs=STAGE15A_ATOL)
    assert transformed[1] == pytest.approx(K1, abs=STAGE15A_ATOL)
    assert transformed[2] == pytest.approx(K2, abs=STAGE15A_ATOL)

    seed_locality = stage15d_locality_audit(_candidate(STAGE15D_KNOWN_SEED_ID))
    assert not seed_locality.one_step_l1
    assert seed_locality.locality_class == STAGE15D_LFINITE
    assert seed_locality.nonlocal_for_stage15_L1


def test_stage15d_criterion_34_l1_witness_strongly_commutes_on_and_off_surface_and_under_smearing():
    audits = canonical_stage15d_candidate_audits()
    assert len(audits) == 14
    assert all(item.point_count == 216 for item in audits)
    assert all(item.positive_point_count == 108 for item in audits)
    assert all(item.off_surface_point_count == 108 for item in audits)
    assert all(item.invertible_equivalent_on_tested_family for item in audits)
    assert all(item.first_class_on_positive_family for item in audits)

    witness = _audit(STAGE15D_L1_WITNESS_ID)
    scaled = _audit(STAGE15D_L1_SCALED_WITNESS_ID)
    for item in (witness, scaled):
        assert item.locality_class == STAGE15D_L1
        assert item.strongly_commuting_unsmeared
        assert item.strongly_commuting_smeared
        assert item.strongly_commuting
        assert item.max_all_unsmeared_bracket <= STAGE15A_ATOL
        assert item.max_all_smeared_bracket <= STAGE15A_ATOL
        assert item.max_dirac_bracket <= STAGE15A_ATOL

    l0 = [item for item in audits if item.locality_class == STAGE15D_L0]
    assert len(l0) == 3
    assert all(not item.strongly_commuting for item in l0)
    assert all(item.max_all_unsmeared_bracket > STAGE15A_ATOL for item in l0)


def test_stage15d_criterion_35_known_seed_is_exactly_depth_two_lfinite_not_one_step_l1():
    audit = stage15d_seed_factorization_audit()
    assert not audit.direct_seed_one_step_l1
    assert audit.direct_seed_nonlocal_for_stage15_L1
    assert audit.step1_l1
    assert audit.step2_l1_on_intermediate_basis
    assert audit.composition_depth == 2
    assert audit.max_composition_matrix_residual <= STAGE15A_ATOL
    assert audit.max_seed_constraint_formula_residual <= STAGE15A_ATOL
    assert audit.strongly_commuting_seed


def test_stage15d_criterion_36_every_audited_equivalent_basis_preserves_stage15c_physical_content():
    checks = canonical_stage15d_content_audits()
    assert len(checks) == 14
    assert all(item.representative_count == 108 for item in checks)
    assert all(item.quotient_class_count == 4 for item in checks)
    assert all(item.minimum_quotient_class_size == 27 for item in checks)
    assert all(item.maximum_quotient_class_size == 27 for item in checks)
    assert all(item.quotient_preserved for item in checks)
    assert all(item.dirac_pair_preserved for item in checks)
    assert all(item.complete_relational_preserved for item in checks)
    assert max(item.max_transformed_constraint_residual for item in checks) <= STAGE15A_ATOL
    assert max(item.max_Q_D_residual for item in checks) <= STAGE15A_ATOL
    assert max(item.max_P_D_residual for item in checks) <= STAGE15A_ATOL
    assert max(item.max_complete_relational_target_residual for item in checks) <= STAGE15A_ATOL


def test_stage15d_criterion_37_locality_false_positives_and_stage15e_boundary_are_explicit():
    head = stage15d_locality_audit(_candidate("head_shear_support_expansion_control"))
    chain = stage15d_locality_audit(_candidate("same_orientation_chain_inverse_locality_control"))
    seed = stage15d_locality_audit(_candidate(STAGE15D_KNOWN_SEED_ID))
    unrestricted = stage15d_locality_audit(_candidate(STAGE15D_UNRESTRICTED_ID))

    assert head.locality_class == STAGE15D_NONLOCAL
    assert "forward_L1_rule_failed" in head.failure_reasons
    assert chain.locality_class == STAGE15D_NONLOCAL
    assert "inverse_L1_rule_failed" in chain.failure_reasons
    assert seed.locality_class == STAGE15D_LFINITE
    assert unrestricted.locality_class == STAGE15D_NONLOCAL

    assert all(
        item.typed_status == STAGE15D_TYPED_STATUS
        for item in (
            *canonical_stage15d_candidate_audits(),
            *canonical_stage15d_content_audits(),
        )
    )
    assert all(
        item.metaphysical_claim_status == STAGE15D_METAPHYSICAL_CLAIM_STATUS
        for item in (
            *canonical_stage15d_candidate_audits(),
            *canonical_stage15d_content_audits(),
        )
    )


def test_stage15d_criterion_38_classifies_local_abelianization_persists_without_overclaiming():
    diagnostics = stage15d_diagnostics()
    assert diagnostics.criteria_32_38_satisfied
    assert diagnostics.classification == STAGE15D_CLASSIFICATION == "local_abelianization_persists"
    assert diagnostics.candidate_count == 14
    assert diagnostics.l0_candidate_count == 3
    assert diagnostics.l0_strong_commuting_count == 0
    assert diagnostics.strict_l1_candidate_count == 7
    assert diagnostics.strict_l1_strong_commuting_count == 2
    assert diagnostics.one_step_local_candidate_count == 10
    assert diagnostics.one_step_local_strong_commuting_count == 2
    assert diagnostics.known_seed_one_step_l1 is False
    assert diagnostics.known_seed_lfinite_depth == 2
    assert diagnostics.minimum_local_abelianization_depth == 1
    assert not diagnostics.l0_offdiagonal_mixing_available
    assert diagnostics.local_abelianization_established
    assert diagnostics.lfinite_seed_factorization_established
    assert diagnostics.physical_content_preserved
    assert diagnostics.typed_stage_deferred
    assert diagnostics.all_metaphysical_claims_not_licensed

    for guard in (
        "basis locality != physical causal locality",
        "finite graph locality != relativistic microcausality",
        "locality-preserving basis map != gauge transformation",
        "local Abelianization != absence of meaningful local constraint structure",
        "known nonlocal seed reconstruction != proof that all Abelianizations are nonlocal",
        "constraint-basis change != physical-orbit change",
        "strongly commuting finite basis != refoliation invariance",
    ):
        assert guard in STAGE15D_GUARDS
