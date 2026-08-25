from t_search.stage15_local import (
    STAGE15A_ATOL,
    STAGE15A_KAPPA,
    canonical_stage15a_orbits,
    canonical_stage15a_representatives_for_orbit,
    stage15a_dirac_data,
)
from t_search.stage15_paths import stage15b_apply_local_flow


def _residual(a, b):
    return max(abs(x - y) for x, y in zip(a.vector(), b.vector(), strict=True))


def test_stage15c_every_sampled_same_orbit_pair_is_reachable_by_a_canonical_local_word():
    comparisons = 0
    nonidentity = 0
    max_endpoint_residual = 0.0
    max_payload_residual = 0.0

    for orbit in canonical_stage15a_orbits():
        reps = canonical_stage15a_representatives_for_orbit(orbit)
        for source in reps:
            for target in reps:
                s = float(target.T0 - source.T0)
                delta_01 = float(
                    STAGE15A_KAPPA
                    * (source.T0 * s + 0.5 * s**2)
                )
                u = float(target.T1 - source.T1 - delta_01)

                after_0 = stage15b_apply_local_flow(source.point(), 0, s)
                after_1 = stage15b_apply_local_flow(after_0, 1, u)
                v = float(target.T2 - after_1.T2)
                endpoint = stage15b_apply_local_flow(after_1, 2, v)

                comparisons += 1
                if source.representative_id != target.representative_id:
                    nonidentity += 1
                max_endpoint_residual = max(
                    max_endpoint_residual, _residual(endpoint, target.point())
                )
                qd_endpoint, pd_endpoint = stage15a_dirac_data(endpoint)
                qd_target, pd_target = stage15a_dirac_data(target.point())
                max_payload_residual = max(
                    max_payload_residual,
                    abs(qd_endpoint - qd_target),
                    abs(pd_endpoint - pd_target),
                )

    assert comparisons == 2916
    assert nonidentity == 2808
    assert max_endpoint_residual <= STAGE15A_ATOL
    assert max_payload_residual <= STAGE15A_ATOL
