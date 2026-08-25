from math import tanh

from t_search.stage15_local import (
    STAGE15A_ATOL,
    canonical_stage15a_representatives,
    stage15a_dirac_data,
)
from t_search.stage15_measurement import (
    STAGE15E_CLOCK_TRIPLES,
    canonical_stage15e_architectures,
    stage15e_orbit_witness,
)
from t_search.stage15_paths import (
    canonical_stage15b_smeared_order_probes,
    stage15b_apply_local_flow,
    stage15b_apply_smeared_flow,
)
from t_search.stage15_relational import stage15c_complete_relational_value
from t_search.stage9_modal import FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_OTHER


def _endpoint_witness(q_d: float, p_d: float):
    relational_target = stage15c_complete_relational_value(q_d, 1.0, 1.0, 1.0)
    left = 0.5 * (
        1.0 + tanh(0.70 * q_d + 0.40 * p_d + 0.20 * relational_target)
    )
    return (
        (FUTURE_SIGNATURE_LEFT, left),
        (FUTURE_SIGNATURE_OTHER, 1.0 - left),
    )


def test_stage15e_all_540_smeared_non_grid_endpoints_reconstruct_the_same_public_O_and_witness():
    representatives = {
        item.representative_id: item for item in canonical_stage15a_representatives()
    }
    architectures = {
        item.representative_id: item for item in canonical_stage15e_architectures()
    }

    comparisons = 0
    max_dirac_residual = 0.0
    max_relational_residual = 0.0
    max_witness_residual = 0.0

    for probe in canonical_stage15b_smeared_order_probes():
        representative = representatives[probe.representative_id]
        architecture = architectures[probe.representative_id]
        source = representative.point()

        after_n = stage15b_apply_smeared_flow(source, probe.N, probe.alpha)
        endpoint_nm = stage15b_apply_smeared_flow(after_n, probe.M, probe.beta)
        after_m = stage15b_apply_smeared_flow(source, probe.M, probe.beta)
        endpoint_mn = stage15b_apply_smeared_flow(after_m, probe.N, probe.alpha)
        endpoint_mn_compensated = stage15b_apply_local_flow(
            endpoint_mn, 2, probe.observed_c2_defect
        )

        source_qd, source_pd = stage15a_dirac_data(source)
        source_witness = stage15e_orbit_witness(architecture).probabilities

        for endpoint in (endpoint_nm, endpoint_mn_compensated):
            q_d, p_d = stage15a_dirac_data(endpoint)
            max_dirac_residual = max(
                max_dirac_residual,
                abs(q_d - source_qd),
                abs(p_d - source_pd),
            )

            for event, (_, tau0, tau1, tau2) in zip(
                architecture.O.relational_events, STAGE15E_CLOCK_TRIPLES, strict=True
            ):
                expected = stage15c_complete_relational_value(
                    q_d, tau0, tau1, tau2
                )
                max_relational_residual = max(
                    max_relational_residual, abs(event.q_value - expected)
                )

            endpoint_witness = _endpoint_witness(q_d, p_d)
            max_witness_residual = max(
                max_witness_residual,
                max(
                    abs(left_value - right_value)
                    for (_, left_value), (_, right_value) in zip(
                        source_witness, endpoint_witness, strict=True
                    )
                ),
            )
            comparisons += 1

    assert comparisons == 1080
    assert max_dirac_residual <= STAGE15A_ATOL
    assert max_relational_residual <= STAGE15A_ATOL
    assert max_witness_residual <= STAGE15A_ATOL


def test_stage15e_inherited_future_payload_is_orbit_level_not_smeared_path_level():
    architectures = canonical_stage15e_architectures()
    for orbit_id in {item.orbit_id for item in architectures}:
        subset = [item for item in architectures if item.orbit_id == orbit_id]
        assert len(subset) == 27
        assert len({repr(item.future_measurement) for item in subset}) == 1
        payload_repr = repr(subset[0].future_measurement)
        assert "ordered_smeared_path" not in payload_repr
        assert "observed_C2_compensator" not in payload_repr
