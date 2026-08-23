import numpy as np
import pytest

from t_search.stage11_parametrized import STAGE11A_POSITIVE_PARAMETERIZATION_IDS
from t_search.stage12_multi_orbit import (
    STAGE12A_ATOL,
    STAGE12A_CANONICAL_ORBIT_IDS,
    STAGE12A_CONSTRAINT_ID,
    STAGE12A_EVENT_ROLE,
    STAGE12A_EXTERNAL_REPARAM_TYPE,
    STAGE12A_GAUGE_FLOW_TYPE,
    STAGE12A_OMEGA_ALPHA,
    STAGE12A_OMEGA_BETA,
    STAGE12A_OMEGA_DELTA,
    STAGE12A_OMEGA_GAMMA,
    canonical_stage12a_external_views,
    canonical_stage12a_gauge_parameters,
    canonical_stage12a_gauge_transports,
    canonical_stage12a_orbits,
    canonical_stage12a_representatives,
    canonical_stage12a_representatives_for_orbit,
    stage12a_diagnostics,
    stage12a_gauge_transport,
)


def test_stage12a_four_canonical_physical_orbits_match_frozen_dirac_data() -> None:
    orbits = canonical_stage12a_orbits()
    assert tuple(orbit.orbit_id for orbit in orbits) == STAGE12A_CANONICAL_ORBIT_IDS
    assert STAGE12A_CANONICAL_ORBIT_IDS == (
        STAGE12A_OMEGA_ALPHA,
        STAGE12A_OMEGA_BETA,
        STAGE12A_OMEGA_GAMMA,
        STAGE12A_OMEGA_DELTA,
    )
    assert {(orbit.Q_D, orbit.P_D) for orbit in orbits} == {
        (-0.35, 1.25),
        (0.40, 1.25),
        (-0.35, 0.75),
        (0.20, 1.75),
    }
    assert {orbit.constraint_id for orbit in orbits} == {STAGE12A_CONSTRAINT_ID}

    by_id = {orbit.orbit_id: orbit for orbit in orbits}
    assert by_id[STAGE12A_OMEGA_ALPHA].P_D == by_id[STAGE12A_OMEGA_BETA].P_D
    assert by_id[STAGE12A_OMEGA_ALPHA].Q_D != by_id[STAGE12A_OMEGA_BETA].Q_D
    assert by_id[STAGE12A_OMEGA_ALPHA].Q_D == by_id[STAGE12A_OMEGA_GAMMA].Q_D
    assert by_id[STAGE12A_OMEGA_ALPHA].P_D != by_id[STAGE12A_OMEGA_GAMMA].P_D


def test_stage12a_samples_multiple_explicit_gauge_representatives_per_orbit() -> None:
    assert canonical_stage12a_gauge_parameters() == (-1.0, -0.5, 0.0, 0.5, 1.0)

    for orbit in canonical_stage12a_orbits():
        representatives = canonical_stage12a_representatives_for_orbit(orbit)
        assert len(representatives) == 5
        assert tuple(rep.gauge_parameter_s for rep in representatives) == canonical_stage12a_gauge_parameters()
        assert len({rep.representative_id for rep in representatives}) == 5
        assert len({rep.event_id for rep in representatives}) == 5
        for rep in representatives:
            assert rep.orbit_id == orbit.orbit_id
            assert rep.event_role == STAGE12A_EVENT_ROLE
            assert rep.gauge_flow_type == STAGE12A_GAUGE_FLOW_TYPE
            assert rep.provenance
            assert np.isclose(rep.T, rep.gauge_parameter_s, atol=STAGE12A_ATOL, rtol=0.0)
            assert np.isclose(rep.q, orbit.Q_D + orbit.P_D * rep.T, atol=STAGE12A_ATOL, rtol=0.0)


def test_stage12a_all_positive_representatives_stay_on_constraint_surface() -> None:
    representatives = canonical_stage12a_representatives()
    assert len(representatives) == 20
    for rep in representatives:
        assert abs(rep.constraint_value) <= STAGE12A_ATOL
        assert np.isclose(rep.p_T + 0.5 * rep.p**2, 0.0, atol=STAGE12A_ATOL, rtol=0.0)
        assert np.isclose(rep.Q_D, rep.q - rep.p * rep.T, atol=STAGE12A_ATOL, rtol=0.0)
        assert np.isclose(rep.P_D, rep.p, atol=STAGE12A_ATOL, rtol=0.0)


def test_stage12a_explicit_same_orbit_gauge_transports_follow_hamiltonian_flow() -> None:
    transports = canonical_stage12a_gauge_transports()
    # Five representatives give 5*4 ordered non-identity transports per orbit.
    assert len(transports) == 4 * 5 * 4
    assert all(item.transform_type == STAGE12A_GAUGE_FLOW_TYPE for item in transports)
    assert all(item.phase_space_residual <= STAGE12A_ATOL for item in transports)
    assert all(item.Q_D_drift <= STAGE12A_ATOL for item in transports)
    assert all(item.P_D_drift <= STAGE12A_ATOL for item in transports)
    assert all(item.max_constraint_residual <= STAGE12A_ATOL for item in transports)
    assert all(item.source_event_id != item.target_event_id for item in transports)
    assert all(item.provenance for item in transports)


def test_stage12a_cross_orbit_gauge_transport_is_not_licensed() -> None:
    orbits = canonical_stage12a_orbits()
    alpha = canonical_stage12a_representatives_for_orbit(orbits[0])[0]
    beta = canonical_stage12a_representatives_for_orbit(orbits[1])[0]
    with pytest.raises(ValueError, match="distinct physical orbits"):
        stage12a_gauge_transport(alpha, beta)


def test_stage12a_stage11_positive_external_parameterizations_exist_on_every_orbit() -> None:
    views = canonical_stage12a_external_views()
    assert len(views) == 4 * len(STAGE11A_POSITIVE_PARAMETERIZATION_IDS)

    by_orbit: dict[str, list] = {orbit_id: [] for orbit_id in STAGE12A_CANONICAL_ORBIT_IDS}
    for view in views:
        by_orbit[view.orbit_id].append(view)
        assert view.transform_type == STAGE12A_EXTERNAL_REPARAM_TYPE
        assert view.transform_type != STAGE12A_GAUGE_FLOW_TYPE
        assert view.source_parameter_type == "external_seed_label_lambda"
        assert view.parameter_label_type == "external_parameter_label_lambda_rho"
        assert view.source_parameter_type != view.parameter_label_type
        assert np.all(view.lapse_values > 0.0)
        assert np.max(np.abs(view.constraint_values)) <= STAGE12A_ATOL
        assert view.lapse_chain_rule_residual <= STAGE12A_ATOL
        assert all(event_id.startswith(f"{view.orbit_id}:") for event_id in view.event_ids)

    for orbit_id, orbit_views in by_orbit.items():
        assert {view.parameterization_id for view in orbit_views} == set(
            STAGE11A_POSITIVE_PARAMETERIZATION_IDS
        ), orbit_id


def test_stage12a_external_views_preserve_each_orbits_dirac_pair() -> None:
    orbit_by_id = {orbit.orbit_id: orbit for orbit in canonical_stage12a_orbits()}
    for view in canonical_stage12a_external_views():
        orbit = orbit_by_id[view.orbit_id]
        Q_values = view.q_values - view.p_values * view.clock_values
        assert np.allclose(Q_values, orbit.Q_D, atol=STAGE12A_ATOL, rtol=0.0)
        assert np.allclose(view.p_values, orbit.P_D, atol=STAGE12A_ATOL, rtol=0.0)


def test_stage12a_orbit_gauge_event_and_external_parameter_provenance_remain_typed() -> None:
    representatives = canonical_stage12a_representatives()
    assert len({rep.event_id for rep in representatives}) == len(representatives)
    assert len({rep.representative_id for rep in representatives}) == len(representatives)
    for rep in representatives:
        assert rep.orbit_id in rep.representative_id
        assert rep.orbit_id in rep.event_id
        assert rep.event_role == STAGE12A_EVENT_ROLE
        assert rep.gauge_flow_type == STAGE12A_GAUGE_FLOW_TYPE

    for view in canonical_stage12a_external_views():
        assert view.transform_type == STAGE12A_EXTERNAL_REPARAM_TYPE
        assert view.parameter_label_type != STAGE12A_GAUGE_FLOW_TYPE


def test_stage12a_diagnostics_close_criteria_11_through_16() -> None:
    diagnostics = stage12a_diagnostics()
    assert diagnostics.orbit_count == 4
    assert diagnostics.representative_count == 20
    assert diagnostics.representatives_per_orbit == 5
    assert diagnostics.gauge_transport_count == 80
    assert diagnostics.external_parameterization_view_count == 16
    assert diagnostics.external_parameterized_event_count == 208
    assert diagnostics.distinct_dirac_pair_count == 4
    assert diagnostics.max_constraint_residual <= STAGE12A_ATOL
    assert diagnostics.max_representative_Q_D_residual <= STAGE12A_ATOL
    assert diagnostics.max_representative_P_D_residual <= STAGE12A_ATOL
    assert diagnostics.max_gauge_transport_residual <= STAGE12A_ATOL
    assert diagnostics.max_gauge_Q_D_drift <= STAGE12A_ATOL
    assert diagnostics.max_gauge_P_D_drift <= STAGE12A_ATOL
    assert diagnostics.max_external_constraint_residual <= STAGE12A_ATOL
    assert diagnostics.max_external_Q_D_residual <= STAGE12A_ATOL
    assert diagnostics.max_external_P_D_residual <= STAGE12A_ATOL
    assert diagnostics.max_external_lapse_chain_rule_residual <= STAGE12A_ATOL
    assert diagnostics.minimum_external_positive_lapse > 0.0
    assert diagnostics.canonical_orbits_distinct
    assert diagnostics.gauge_representatives_complete
    assert diagnostics.gauge_invariants_preserved
    assert diagnostics.external_parameterization_family_complete
    assert diagnostics.typed_provenance_explicit
    assert diagnostics.criteria_11_16_satisfied
