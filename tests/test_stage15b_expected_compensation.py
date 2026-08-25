import pytest

from t_search.stage15_local import (
    STAGE15A_ATOL,
    canonical_stage15a_representatives,
)
from t_search.stage15_paths import (
    STAGE15B_SMEARED_CASES,
    stage15b_apply_local_flow,
    stage15b_apply_smeared_flow,
    stage15b_expected_smeared_c2_defect,
)


def _residual(a, b):
    return max(abs(x - y) for x, y in zip(a.vector(), b.vector(), strict=True))


def _coefficient_support(smearing):
    return {index for index, value in enumerate(smearing) if abs(value) > STAGE15A_ATOL}


def test_stage15b_predicted_smeared_compensator_closes_all_frozen_cases():
    comparisons = 0
    nonzero = 0
    zero = 0
    max_residual = 0.0

    for rep in canonical_stage15a_representatives():
        source = rep.point()
        for _, N, M, alpha, beta, _ in STAGE15B_SMEARED_CASES:
            path_nm = stage15b_apply_smeared_flow(
                stage15b_apply_smeared_flow(source, N, alpha), M, beta
            )
            path_mn = stage15b_apply_smeared_flow(
                stage15b_apply_smeared_flow(source, M, beta), N, alpha
            )
            predicted = stage15b_expected_smeared_c2_defect(
                source, N, M, alpha, beta
            )
            compensated = stage15b_apply_local_flow(path_mn, 2, predicted)
            comparisons += 1
            max_residual = max(max_residual, _residual(compensated, path_nm))
            if abs(predicted) > STAGE15A_ATOL:
                nonzero += 1
            else:
                zero += 1

    assert comparisons == 540
    assert nonzero == 432
    assert zero == 108
    assert max_residual <= STAGE15A_ATOL


def test_stage15b_frozen_smearing_cases_include_declared_site_index_supports():
    cases = {case[0]: case for case in STAGE15B_SMEARED_CASES}

    _, N01, M12, _, _, _ = cases["compact01_vs_compact12"]
    assert _coefficient_support(N01) == {0, 1}
    assert _coefficient_support(M12) == {1, 2}

    for case_id in ("compact01_vs_full", "compact12_vs_full", "full_vs_full"):
        _, N, M, _, _, _ = cases[case_id]
        assert {0, 1, 2} in (_coefficient_support(N), _coefficient_support(M))

    _, N, M, _, _, expected_nontrivial = cases["parallel_plus_c2_zero_wedge"]
    assert N[0] * M[1] - N[1] * M[0] == pytest.approx(0.0, abs=STAGE15A_ATOL)
    assert not expected_nontrivial
