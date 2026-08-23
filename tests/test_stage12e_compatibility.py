import pytest

from t_search.stage11_measurement import STAGE11D_REFERENCE_CLOCK, STAGE11D_REFERENCE_CLOCK_INDEX
from t_search.stage11_parametrized import STAGE11A_IDENTITY
from t_search.stage12_compatibility import (
    STAGE12E_ATOL if False else STAGE12E_CLOCK_TYPE,
)

# Import the public Stage 12E surface explicitly after the sentinel import above.
from t_search.stage12_compatibility import (  # noqa: E402
    STAGE12E_GAUGE_TYPE,
    STAGE12E_GUARD,
    STAGE12E_PATH_REJECTION,
    STAGE12E_REPARAMETERIZATION_TYPE,
    canonical_stage12e_clock_transports,
    canonical_stage12e_gauge_transports,
    canonical_stage12e_reparameterization_transports,
    canonical_stage12e_triple_spanning_gauge_transports,
    stage12e_apply_gauge,
    stage12e_clock_gauge_diagnostics,
    stage12e_controls,
    stage12e_diagnostics,
    stage12e_reparameterization_gauge_diagnostics,
    stage12e_state,
    stage12e_summary,
    stage12e_triple_diagnostics,
)
from t_search.stage12_multi_orbit import (
    STAGE12A_ATOL,
    canonical_stage12a_orbits,
    canonical_stage12a_representatives,
)


def test_stage12e_separately_types_C_G_and_Phi_transport_families() -> None:
    clocks = canonical_stage12e_clock_transports()
    reparams = canonical_stage12e_reparameterization_transports()
    gauges = canonical_stage12e_gauge_transports()
    spanning = canonical_stage12e_triple_spanning_gauge_transports()

    assert len(clocks) == 108
    assert len(reparams) == 12
    assert len(gauges) == 80
    assert len(spanning) == 4
    assert {item.transform_type for item in clocks} == {STAGE12E_CLOCK_TYPE}
    assert {item.transform_type for item in reparams} == {
        STAGE12E_REPARAMETERIZATION_TYPE
    }
    assert {item.transform_type for item in gauges} == {STAGE12E_GAUGE_TYPE}
    assert len(
        {
            STAGE12E_CLOCK_TYPE,
            STAGE12E_REPARAMETERIZATION_TYPE,
            STAGE12E_GAUGE_TYPE,
        }
    ) == 3
    assert all(item.valid for item in (*clocks, *reparams, *gauges))
    assert {item.orbit_id for item in spanning} == {
        item.orbit_id for item in canonical_stage12a_orbits()
    }
    assert all(abs(item.delta_s) == 2.0 for item in spanning)


def test_stage12e_operational_state_keeps_orbit_sensitive_and_representation_roles_separate() -> None:
    reps = canonical_stage12a_representatives()
    alpha = [item for item in reps if item.orbit_id == "omega_alpha"]
    beta = [item for item in reps if item.orbit_id == "omega_beta"]

    alpha_states = [
        stage12e_state(
            item.representative_id,
            STAGE11A_IDENTITY,
            STAGE11D_REFERENCE_CLOCK,
            STAGE11D_REFERENCE_CLOCK_INDEX,
            "h_L",
        )
        for item in alpha
    ]
    beta_state = stage12e_state(
        beta[0].representative_id,
        STAGE11A_IDENTITY,
        STAGE11D_REFERENCE_CLOCK,
        STAGE11D_REFERENCE_CLOCK_INDEX,
        "h_L",
    )

    assert len(alpha_states) == 5
    assert len({item.representative_id for item in alpha_states}) == 5
    assert len({item.gauge_parameter_s for item in alpha_states}) == 5
    assert len({item.anchor_relational_q for item in alpha_states}) == 1
    assert len({item.target_relational_q for item in alpha_states}) == 1
    assert len({item.measurement_probabilities for item in alpha_states}) == 1
    assert len({item.orbit_witness_probabilities for item in alpha_states}) == 1

    # The inherited Stage 11 measurement family itself is orbit-insensitive, while
    # relational O and the Stage 12D witness retain physical-orbit discrimination.
    assert alpha_states[0].measurement_probabilities == beta_state.measurement_probabilities
    assert alpha_states[0].target_relational_q != beta_state.target_relational_q
    assert alpha_states[0].orbit_witness_probabilities != beta_state.orbit_witness_probabilities


def test_stage12e_clock_x_gauge_paths_commute_on_all_positive_gauge_arrows() -> None:
    d = stage12e_clock_gauge_diagnostics()
    assert d.family_id == "C_x_Phi"
    assert d.object_count == 8640
    assert d.path_evaluation_count == 17280
    assert d.max_relational_residual <= STAGE12A_ATOL
    assert d.max_measurement_residual <= STAGE12A_ATOL
    assert d.max_orbit_witness_residual <= STAGE12A_ATOL
    assert d.compatible


def test_stage12e_reparameterization_x_gauge_paths_commute_on_all_positive_gauge_arrows() -> None:
    d = stage12e_reparameterization_gauge_diagnostics()
    assert d.family_id == "G_x_Phi"
    assert d.object_count == 1920
    assert d.path_evaluation_count == 3840
    assert d.max_total_residual <= STAGE12A_ATOL
    assert d.compatible


def test_stage12e_three_way_spanning_cubes_agree_for_all_six_orders() -> None:
    d = stage12e_triple_diagnostics()
    assert d.family_id == "C_x_G_x_Phi_spanning"
    assert d.object_count == 5184
    assert d.path_evaluation_count == 31104
    assert d.max_relational_residual <= STAGE12A_ATOL
    assert d.max_measurement_residual <= STAGE12A_ATOL
    assert d.max_orbit_witness_residual <= STAGE12A_ATOL
    assert d.compatible


def test_stage12e_mixed_orbit_and_untyped_paths_are_detectably_rejected() -> None:
    controls = stage12e_controls()
    assert len(controls) == 4
    assert all(item.rejected for item in controls)
    assert {item.classification for item in controls} == {STAGE12E_PATH_REJECTION}
    assert {item.control_id for item in controls} == {
        "mixed_orbit_phi",
        "clock_label_as_parameterization",
        "parameterization_label_as_clock",
        "gauge_type_relabelled_as_reparameterization",
    }

    # Construction-level cross-orbit protection remains active independently.
    gauges = canonical_stage12e_gauge_transports()
    reps = canonical_stage12a_representatives()
    alpha = next(item for item in reps if item.orbit_id == "omega_alpha")
    beta = next(item for item in reps if item.orbit_id == "omega_beta")
    state = stage12e_state(alpha.representative_id, "identity", "A", 0, "h_L")
    forged = gauges[0]
    forged = type(forged)(
        forged.transform_type,
        alpha.orbit_id,
        alpha.representative_id,
        beta.representative_id,
        forged.delta_s,
        True,
    )
    with pytest.raises(ValueError):
        stage12e_apply_gauge(state, forged)


def test_stage12e_diagnostics_close_criteria_39_through_43_and_keep_guards() -> None:
    d = stage12e_diagnostics()
    assert d.physical_orbit_count == 4
    assert d.representative_count == 20
    assert d.clock_transport_count == 108
    assert d.reparameterization_transport_count == 12
    assert d.gauge_transport_count == 80
    assert d.distinct_transform_type_count == 3
    assert d.clock_gauge_square_count == 8640
    assert d.reparameterization_gauge_square_count == 1920
    assert d.triple_spanning_gauge_count == 4
    assert d.triple_cube_count == 5184
    assert d.triple_path_evaluation_count == 31104
    assert d.max_clock_gauge_residual <= STAGE12A_ATOL
    assert d.max_reparameterization_gauge_residual <= STAGE12A_ATOL
    assert d.max_triple_residual <= STAGE12A_ATOL
    assert d.orbit_sensitive_signature_count == 4
    assert d.control_count == 4
    assert d.rejected_control_count == 4
    assert d.criteria_39_43_satisfied

    summary = stage12e_summary()
    assert summary["bounded_result"].endswith("= established")
    guards = set(summary["guards"])
    assert STAGE12E_GUARD in guards
    assert "constraint-generated gauge flow != internal-clock change" in guards
    assert "constraint-generated gauge flow != external reparameterization" in guards
    assert "path-independent future probabilities != future actuality" in guards
    assert "path-independent relational outputs != ontological becoming" in guards
