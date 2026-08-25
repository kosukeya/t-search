import pytest

from t_search.stage15_flow_oracle import (
    stage15b_direct_local_flow,
    stage15b_direct_smeared_flow,
)
from t_search.stage15_local import (
    STAGE15A_ATOL,
    canonical_stage15a_representatives,
    stage15a_constraints,
    stage15a_dirac_data,
)
from t_search.stage15_paths import (
    STAGE15B_FLOW_PARAMETERS,
    STAGE15B_SMEAR_01,
    STAGE15B_SMEAR_12,
    STAGE15B_SMEAR_FULL_A,
    STAGE15B_SMEAR_FULL_B,
    stage15b_apply_local_flow,
    stage15b_apply_smeared_flow,
)


def _residual(a, b):
    return max(abs(x - y) for x, y in zip(a.vector(), b.vector(), strict=True))


def test_stage15b_chart_local_flows_match_independent_hamiltonian_oracle():
    comparisons = 0
    max_residual = 0.0
    for rep in canonical_stage15a_representatives():
        point = rep.point()
        for generator_index in range(3):
            for parameter in STAGE15B_FLOW_PARAMETERS:
                chart = stage15b_apply_local_flow(point, generator_index, parameter)
                direct = stage15b_direct_local_flow(point, generator_index, parameter)
                comparisons += 1
                max_residual = max(max_residual, _residual(chart, direct))
    assert comparisons == 648
    assert max_residual <= STAGE15A_ATOL


def test_stage15b_chart_smeared_flows_match_independent_hamiltonian_oracle():
    smearings = (
        STAGE15B_SMEAR_01,
        STAGE15B_SMEAR_12,
        STAGE15B_SMEAR_FULL_A,
        STAGE15B_SMEAR_FULL_B,
    )
    comparisons = 0
    max_residual = 0.0
    for rep in canonical_stage15a_representatives():
        point = rep.point()
        for smearing in smearings:
            for parameter in STAGE15B_FLOW_PARAMETERS:
                chart = stage15b_apply_smeared_flow(point, smearing, parameter)
                direct = stage15b_direct_smeared_flow(point, smearing, parameter)
                comparisons += 1
                max_residual = max(max_residual, _residual(chart, direct))
    assert comparisons == 864
    assert max_residual <= STAGE15A_ATOL


def test_stage15b_direct_hamiltonian_oracle_preserves_surface_and_payload_as_a_result():
    max_constraint = 0.0
    max_payload = 0.0
    for rep in canonical_stage15a_representatives():
        source = rep.point()
        source_payload = stage15a_dirac_data(source)
        for generator_index in range(3):
            target = stage15b_direct_local_flow(source, generator_index, 0.5)
            max_constraint = max(
                max_constraint,
                max(abs(value) for value in stage15a_constraints(target)),
            )
            target_payload = stage15a_dirac_data(target)
            max_payload = max(
                max_payload,
                max(abs(a - b) for a, b in zip(source_payload, target_payload, strict=True)),
            )
    assert max_constraint <= STAGE15A_ATOL
    assert max_payload <= STAGE15A_ATOL
