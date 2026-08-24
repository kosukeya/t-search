from collections import Counter

import pytest

from t_search.stage14_basis import (
    STAGE14D_ATOL,
    STAGE14D_BOUNDED_RESULT,
    STAGE14D_GUARDS,
    STAGE14D_METAPHYSICAL_CLAIM_STATUS,
    STAGE14D_SCALAR_FACTOR_FAMILIES,
    STAGE14D_SCALAR_OBSTRUCTED,
    STAGE14D_SIMPLE_SCALAR,
    STAGE14D_SINGULAR_REJECTED,
    STAGE14D_TRIANGULAR_BASIS_ID,
    STAGE14D_TRIANGULAR_EQUIVALENT,
    canonical_stage14d_basis_content_checks,
    canonical_stage14d_scalar_evaluations,
    canonical_stage14d_singular_controls,
    canonical_stage14d_triangular_probes,
    stage14d_diagnostics,
    stage14d_scalar_dprime_component,
    stage14d_scalar_transformation_admissible,
)
from t_search.stage14_structure_function import (
    STAGE14A_BASIS_ID,
    STAGE14A_KAPPA,
    Stage14PhaseSpacePoint,
)


def _probe_point(*, X: float) -> Stage14PhaseSpacePoint:
    return Stage14PhaseSpacePoint(
        T1=0.4,
        p_1=-0.5,
        T2=-0.2,
        p_2=-0.25,
        X=X,
        p_X=-0.5,
        q=0.7,
        p=1.0,
    )


def test_stage14d_criterion_32_simple_scalar_class_is_diagonal_and_invertible():
    evaluations = canonical_stage14d_scalar_evaluations()
    assert STAGE14D_SIMPLE_SCALAR == "simple_scalar_rescaling"
    assert len(STAGE14D_SCALAR_FACTOR_FAMILIES) == 3
    assert len(evaluations) == 324
    assert all(item.invertible for item in evaluations)
    assert all(abs(item.transformation_determinant) > STAGE14D_ATOL for item in evaluations)
    assert all(item.off_diagonal_norm <= STAGE14D_ATOL for item in evaluations)
    assert all(item.classification == STAGE14D_SCALAR_OBSTRUCTED for item in evaluations)


def test_stage14d_criterion_33_nonzero_Dprime_component_obstructs_all_X_nonzero_cases():
    evaluations = canonical_stage14d_scalar_evaluations()
    nonzero = [item for item in evaluations if item.x_nonzero]
    zero = [item for item in evaluations if not item.x_nonzero]
    assert len(nonzero) == 216
    assert len({item.representative_id for item in nonzero}) == 72
    assert all(item.obstructed for item in nonzero)
    assert all(abs(item.dprime_component) > STAGE14D_ATOL for item in nonzero)
    assert len(zero) == 108
    assert len({item.representative_id for item in zero}) == 36
    assert all(abs(item.dprime_component) <= STAGE14D_ATOL for item in zero)

    f_1, f_2, f_D = 1.2, 0.8, 2.0
    assert stage14d_scalar_transformation_admissible(f_1, f_2, f_D)
    expected = STAGE14A_KAPPA * f_1 * f_2 / f_D
    assert stage14d_scalar_dprime_component(_probe_point(X=1.0), f_1, f_2, f_D) == pytest.approx(-expected)
    assert stage14d_scalar_dprime_component(_probe_point(X=-1.0), f_1, f_2, f_D) == pytest.approx(expected)


def test_stage14d_criterion_34_singular_scalar_rescalings_are_rejected():
    controls = canonical_stage14d_singular_controls()
    assert len(controls) == 2
    assert {item.control_id for item in controls} == {
        "vanishing_diagonal_factor",
        "nonfinite_diagonal_factor",
    }
    assert all(item.classification == STAGE14D_SINGULAR_REJECTED for item in controls)
    assert all(item.rejected for item in controls)
    by_id = {item.control_id: item for item in controls}
    assert by_id["vanishing_diagonal_factor"].vanishing_witness_count == 36
    assert by_id["vanishing_diagonal_factor"].nonfinite_witness_count == 0
    assert by_id["nonfinite_diagonal_factor"].vanishing_witness_count == 0
    assert by_id["nonfinite_diagonal_factor"].nonfinite_witness_count == 36
    assert not stage14d_scalar_transformation_admissible(1.0, 1.0, 0.0)
    assert not stage14d_scalar_transformation_admissible(1.0, float("inf"), 1.0)
    with pytest.raises(ValueError):
        stage14d_scalar_dprime_component(_probe_point(X=1.0), 1.0, 1.0, 0.0)


def test_stage14d_criterion_35_triangular_transform_is_invertible_on_positive_family():
    probes = canonical_stage14d_triangular_probes()
    positive = [item for item in probes if item.surface_kind == "positive_constraint_surface"]
    off_surface = [item for item in probes if item.surface_kind == "off_surface_probe"]
    assert len(probes) == 216
    assert len(positive) == 108
    assert len(off_surface) == 108
    assert all(item.transformation_determinant == pytest.approx(1.0) for item in probes)
    assert max(item.inverse_identity_residual for item in probes) <= STAGE14D_ATOL
    assert max(item.forward_constraint_residual for item in probes) <= STAGE14D_ATOL
    assert max(item.inverse_constraint_residual for item in probes) <= STAGE14D_ATOL
    assert all(item.classification == STAGE14D_TRIANGULAR_EQUIVALENT for item in probes)


def test_stage14d_criterion_36_triangular_basis_is_strongly_commuting_off_surface_too():
    probes = canonical_stage14d_triangular_probes()
    assert max(item.H2_tilde_formula_residual for item in probes) <= STAGE14D_ATOL
    assert max(item.bracket_D_H1_residual for item in probes) <= STAGE14D_ATOL
    assert max(item.bracket_H1_H2_tilde_residual for item in probes) <= STAGE14D_ATOL
    assert max(item.bracket_H2_tilde_D_residual for item in probes) <= STAGE14D_ATOL
    assert any(item.surface_kind == "off_surface_probe" for item in probes)


def test_stage14d_criterion_37_typed_triangular_correspondence_preserves_public_content():
    checks = canonical_stage14d_basis_content_checks()
    assert len(checks) == 108
    assert all(item.original_basis_id == STAGE14A_BASIS_ID for item in checks)
    assert all(item.triangular_basis_id == STAGE14D_TRIANGULAR_BASIS_ID for item in checks)
    assert all(item.quotient_membership_preserved for item in checks)
    assert Counter(item.quotient_class_id for item in checks).values() == Counter({
        "q1": 27,
        "q2": 27,
        "q3": 27,
        "q4": 27,
    }).values()
    assert max(max(item.Q_D_residual, item.P_D_residual) for item in checks) <= STAGE14D_ATOL
    assert max(item.max_complete_relational_residual for item in checks) <= STAGE14D_ATOL
    assert max(item.max_triangular_dirac_bracket_residual for item in checks) <= STAGE14D_ATOL
    assert all(item.inherited_public_payload_equal for item in checks)
    assert all(item.public_payload_basis_provenance_absent for item in checks)


def test_stage14d_criterion_38_interpretation_is_bounded_and_all_diagnostics_close():
    diagnostics = stage14d_diagnostics()
    assert diagnostics.criteria_32_38_satisfied
    assert diagnostics.representative_count == 108
    assert diagnostics.scalar_evaluation_count == 324
    assert diagnostics.scalar_x_nonzero_obstructed_count == 216
    assert diagnostics.rejected_singular_control_count == 2
    assert diagnostics.triangular_probe_count == 216
    assert diagnostics.basis_content_check_count == 108
    assert diagnostics.basis_quotient_preserved_count == 108
    assert diagnostics.basis_public_payload_equal_count == 108
    assert diagnostics.public_basis_provenance_absent
    assert diagnostics.all_metaphysical_claims_not_licensed
    assert STAGE14D_BOUNDED_RESULT.endswith("= established")
    for guard in (
        "Stage-13-style scalar-rescaling obstruction != universal non-Abelianizability",
        "triangular basis equivalence != universal basis trivializability",
        "constraint-basis change != physical-orbit change",
        "basis-equivalent finite quotient != refoliation invariance",
        "basis equivalence != ontological becoming",
    ):
        assert guard in STAGE14D_GUARDS
    assert all(
        item.metaphysical_claim_status == STAGE14D_METAPHYSICAL_CLAIM_STATUS
        for item in (
            *canonical_stage14d_scalar_evaluations(),
            *canonical_stage14d_singular_controls(),
            *canonical_stage14d_triangular_probes(),
            *canonical_stage14d_basis_content_checks(),
        )
    )
