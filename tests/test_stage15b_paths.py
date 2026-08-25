import math

import pytest

from t_search.stage15_local import (
    STAGE15A_ATOL,
    canonical_stage15a_off_surface_probes,
    canonical_stage15a_representatives,
)
from t_search.stage15_paths import (
    STAGE15B_JACOBI_SMEARINGS,
    STAGE15B_PATH_012,
    STAGE15B_PATH_102,
    STAGE15B_SMEARED_CASES,
    canonical_stage15b_local_pairs,
    canonical_stage15b_local_path_results,
    canonical_stage15b_smeared_order_probes,
    stage15b_apply_local_flow,
    stage15b_apply_local_path,
    stage15b_apply_smeared_flow,
    stage15b_diagnostics,
    stage15b_expected_smeared_c2_defect,
    stage15b_smeared_jacobi_residual,
    stage15b_smeared_nested_bracket,
)


def _residual(a, b):
    return max(abs(x - y) for x, y in zip(a.vector(), b.vector(), strict=True))


def test_stage15b_exact_finite_local_and_smeared_flows_preserve_tested_surface_payload():
    diag = stage15b_diagnostics()
    assert diag.single_local_flow_probe_count == 648
    assert diag.single_smeared_flow_probe_count == 864
    assert diag.max_single_flow_constraint_residual <= STAGE15A_ATOL
    assert diag.max_single_flow_payload_residual <= STAGE15A_ATOL
    assert diag.exact_finite_flows_established

    # The positive-path implementation is deliberately not an off-surface
    # integration rule; Stage 15B only licenses these exact finite formulas
    # on the frozen positive surface.
    off_surface = canonical_stage15a_off_surface_probes()[0]
    with pytest.raises(ValueError, match="on-surface"):
        stage15b_apply_local_flow(off_surface, 0, 0.5)
    with pytest.raises(ValueError, match="on-surface"):
        stage15b_apply_smeared_flow(off_surface, (1.0, 0.0, 0.0), 0.5)


def test_stage15b_constructs_exact_864_local_source_target_pair_family():
    pairs = canonical_stage15b_local_pairs()
    assert len(pairs) == 864
    assert len({pair.pair_id for pair in pairs}) == 864
    assert all(pair.source.orbit_id == pair.target.orbit_id for pair in pairs)
    assert all(abs(pair.source.T0 - pair.target.T0) > STAGE15A_ATOL for pair in pairs)
    assert all(abs(pair.source.T1 - pair.target.T1) > STAGE15A_ATOL for pair in pairs)
    assert all(abs(pair.source.T2 - pair.target.T2) > STAGE15A_ATOL for pair in pairs)
    assert all(abs(pair.s) > STAGE15A_ATOL for pair in pairs)
    assert all(abs(pair.u) > STAGE15A_ATOL for pair in pairs)


def test_stage15b_two_local_orderings_match_raw_formulas_and_close_with_path_specific_c2_compensation():
    results = canonical_stage15b_local_path_results()
    assert len(results) == 1728
    assert {result.path_word for result in results} == {
        STAGE15B_PATH_012,
        STAGE15B_PATH_102,
    }
    assert max(result.raw_formula_residual for result in results) <= STAGE15A_ATOL
    assert max(result.final_endpoint_residual for result in results) <= STAGE15A_ATOL
    assert max(result.final_payload_residual for result in results) <= STAGE15A_ATOL
    assert max(result.final_relational_residual for result in results) <= STAGE15A_ATOL


def test_stage15b_local_compensator_identity_has_nontrivial_and_zero_subfamilies():
    pairs = canonical_stage15b_local_pairs()
    nonzero = [pair for pair in pairs if abs(pair.compensator_difference) > STAGE15A_ATOL]
    zero = [pair for pair in pairs if abs(pair.compensator_difference) <= STAGE15A_ATOL]
    assert len(nonzero) == 576
    assert len(zero) == 288

    for pair in pairs:
        assert math.isclose(
            pair.compensator_difference,
            pair.expected_compensator_difference,
            rel_tol=0.0,
            abs_tol=STAGE15A_ATOL,
        )

    pair = nonzero[0]
    result_012 = stage15b_apply_local_path(pair, STAGE15B_PATH_012)
    result_102 = stage15b_apply_local_path(pair, STAGE15B_PATH_102)
    assert abs(result_012.compensator - result_102.compensator) > STAGE15A_ATOL
    assert result_012.final_endpoint_residual <= STAGE15A_ATOL
    assert result_102.final_endpoint_residual <= STAGE15A_ATOL


def test_stage15b_wrong_missing_and_shared_local_compensators_are_detected():
    diag = stage15b_diagnostics()
    assert diag.local_wrong_sign_rejected_count == 1728
    assert diag.local_wrong_half_rejected_count == 1728
    assert diag.local_missing_rejected_count == 1728
    assert diag.local_shared_compensator_rejected_count == 576
    assert diag.local_shared_compensator_zero_defect_compatible_count == 288
    assert diag.local_controls_detected


def test_stage15b_smeared_order_defects_are_c2_only_and_match_integrated_structure_function():
    probes = canonical_stage15b_smeared_order_probes()
    assert len(STAGE15B_SMEARED_CASES) == 5
    assert len(probes) == 540

    case_ids = {case[0] for case in STAGE15B_SMEARED_CASES}
    assert {probe.case_id for probe in probes} == case_ids

    nonzero = [probe for probe in probes if abs(probe.observed_c2_defect) > STAGE15A_ATOL]
    zero = [probe for probe in probes if abs(probe.observed_c2_defect) <= STAGE15A_ATOL]
    assert len(nonzero) == 432
    assert len(zero) == 108
    assert all(probe.nontrivial_expected for probe in nonzero)
    assert all(not probe.nontrivial_expected for probe in zero)

    assert max(
        abs(probe.observed_c2_defect - probe.expected_c2_defect)
        for probe in probes
    ) <= STAGE15A_ATOL
    assert max(probe.c2_only_residual for probe in probes) <= STAGE15A_ATOL
    assert max(probe.compensated_endpoint_residual for probe in probes) <= STAGE15A_ATOL
    assert max(probe.payload_residual for probe in probes) <= STAGE15A_ATOL

    rep = canonical_stage15a_representatives()[0]
    case_id, N, M, alpha, beta, _ = STAGE15B_SMEARED_CASES[0]
    expected = stage15b_expected_smeared_c2_defect(rep.point(), N, M, alpha, beta)
    matching = next(
        probe
        for probe in probes
        if probe.representative_id == rep.representative_id and probe.case_id == case_id
    )
    assert matching.expected_c2_defect == pytest.approx(expected, abs=STAGE15A_ATOL)


def test_stage15b_smeared_controls_and_zero_wedge_case_discriminate_ordering():
    diag = stage15b_diagnostics()
    assert diag.smeared_wrong_sign_rejected_count == 432
    assert diag.smeared_missing_rejected_count == 432
    assert diag.smeared_nonzero_order_defect_count == 432
    assert diag.smeared_zero_order_defect_count == 108
    assert diag.smeared_order_defect_detected
    assert diag.smeared_zero_wedge_control_exact

    zero_case = next(case for case in STAGE15B_SMEARED_CASES if not case[-1])
    _, N, M, _, _, _ = zero_case
    assert N[0] * M[1] - N[1] * M[0] == pytest.approx(0.0, abs=STAGE15A_ATOL)


def test_stage15b_off_surface_smeared_jacobi_is_nontrivial_but_cancels():
    off_surface = canonical_stage15a_off_surface_probes()
    assert len(STAGE15B_JACOBI_SMEARINGS) == 4

    residuals = []
    terms = []
    for point in off_surface:
        for L in STAGE15B_JACOBI_SMEARINGS:
            for N in STAGE15B_JACOBI_SMEARINGS:
                for M in STAGE15B_JACOBI_SMEARINGS:
                    if L in (N, M) or N == M:
                        continue
                    residuals.append(abs(stage15b_smeared_jacobi_residual(point, L, N, M)))
                    terms.extend(
                        (
                            abs(stage15b_smeared_nested_bracket(point, L, N, M)),
                            abs(stage15b_smeared_nested_bracket(point, N, M, L)),
                            abs(stage15b_smeared_nested_bracket(point, M, L, N)),
                        )
                    )

    assert len(residuals) == 2592
    assert max(residuals) <= STAGE15A_ATOL
    assert max(terms) > STAGE15A_ATOL


def test_stage15b_diagnostics_close_only_frozen_criteria_18_through_24():
    diag = stage15b_diagnostics()
    assert diag.orbit_count == 4
    assert diag.representative_count == 108
    assert diag.single_local_flow_probe_count == 648
    assert diag.single_smeared_flow_probe_count == 864
    assert diag.local_pair_count == 864
    assert diag.local_path_result_count == 1728
    assert diag.local_nonzero_order_defect_count == 576
    assert diag.local_zero_order_defect_count == 288
    assert diag.smeared_order_probe_count == 540
    assert diag.smeared_nonzero_order_defect_count == 432
    assert diag.smeared_zero_order_defect_count == 108
    assert diag.smeared_jacobi_probe_count == 2592
    assert diag.max_local_endpoint_residual <= STAGE15A_ATOL
    assert diag.max_smeared_endpoint_residual <= STAGE15A_ATOL
    assert diag.max_smeared_jacobi_residual <= STAGE15A_ATOL
    assert diag.max_smeared_jacobi_term_magnitude > STAGE15A_ATOL
    assert diag.local_compensated_path_closure_established
    assert diag.local_order_defect_detected
    assert diag.smeared_compensated_path_closure_established
    assert diag.smeared_jacobi_established_off_surface
    assert diag.criteria_18_24_satisfied
