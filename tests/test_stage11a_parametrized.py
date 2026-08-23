import numpy as np
import pytest

from t_search.stage11_parametrized import (
    STAGE11A_AFFINE,
    STAGE11A_ATOL,
    STAGE11A_CUBIC,
    STAGE11A_HYPERBOLIC,
    STAGE11A_IDENTITY,
    STAGE11A_NONINJECTIVE,
    STAGE11A_POSITIVE_PARAMETERIZATION_IDS,
    STAGE11A_REVERSE,
    canonical_stage11a_parameterizations,
    canonical_stage11a_positive_family,
    canonical_stage11a_trajectory,
    stage11a_diagnostics,
    stage11a_event_correspondence,
    stage11a_excluded_parameterizations,
    stage11a_lapse_chain_rule_residual,
    stage11a_seed_lapse,
)


def test_stage11a_minimal_constrained_trajectory_has_positive_lapse() -> None:
    for trajectory in canonical_stage11a_positive_family():
        assert np.all(trajectory.lapse_values > 0.0)
        assert np.max(np.abs(trajectory.constraint_values)) <= STAGE11A_ATOL
        assert np.allclose(
            trajectory.p_T_values + 0.5 * trajectory.p_values**2,
            0.0,
            atol=STAGE11A_ATOL,
            rtol=0.0,
        )


def test_stage11a_frozen_positive_parameterization_family_is_implemented() -> None:
    specs = canonical_stage11a_parameterizations()
    assert tuple(item.parameterization_id for item in specs) == STAGE11A_POSITIVE_PARAMETERIZATION_IDS
    assert STAGE11A_POSITIVE_PARAMETERIZATION_IDS == (
        STAGE11A_IDENTITY,
        STAGE11A_AFFINE,
        STAGE11A_CUBIC,
        STAGE11A_HYPERBOLIC,
    )
    assert all(item.admissible for item in specs)
    assert all(item.orientation_preserving for item in specs)
    assert all(item.injective_on_test_domain for item in specs)

    family = {item.parameterization_id: item for item in canonical_stage11a_positive_family()}
    x = family[STAGE11A_IDENTITY].source_labels
    assert np.allclose(family[STAGE11A_IDENTITY].parameter_labels, x)
    assert np.allclose(family[STAGE11A_AFFINE].parameter_labels, 2.0 * x + 1.0)
    assert np.allclose(family[STAGE11A_CUBIC].parameter_labels, x + x**3 / 4.0)
    assert np.allclose(family[STAGE11A_HYPERBOLIC].parameter_labels, np.sinh(x))


def test_stage11a_corresponding_events_can_have_different_raw_parameter_values() -> None:
    family = canonical_stage11a_positive_family()
    reference = family[0]
    differing = 0
    for target in family[1:]:
        correspondence = stage11a_event_correspondence(reference, target)
        assert tuple(item.event_id for item in correspondence) == reference.event_ids
        for item in correspondence:
            if abs(item.source_parameter_value - item.target_parameter_value) > STAGE11A_ATOL:
                differing += 1
    assert differing == 36


def test_stage11a_chain_rule_lapse_transformation_is_verified() -> None:
    for trajectory in canonical_stage11a_positive_family():
        assert stage11a_lapse_chain_rule_residual(trajectory) <= STAGE11A_ATOL

    reference = canonical_stage11a_trajectory(STAGE11A_IDENTITY)
    affine = canonical_stage11a_trajectory(STAGE11A_AFFINE)
    assert np.allclose(
        affine.lapse_values,
        stage11a_seed_lapse(reference.source_labels) / 2.0,
        atol=STAGE11A_ATOL,
        rtol=0.0,
    )


def test_stage11a_constraint_orbit_is_preserved_across_positive_family() -> None:
    family = canonical_stage11a_positive_family()
    reference = family[0]
    for target in family[1:]:
        stage11a_event_correspondence(reference, target)
        assert target.event_ids == reference.event_ids
        assert np.allclose(target.clock_values, reference.clock_values, atol=STAGE11A_ATOL, rtol=0.0)
        assert np.allclose(target.q_values, reference.q_values, atol=STAGE11A_ATOL, rtol=0.0)
        assert np.allclose(target.p_values, reference.p_values, atol=STAGE11A_ATOL, rtol=0.0)
        assert np.allclose(target.p_T_values, reference.p_T_values, atol=STAGE11A_ATOL, rtol=0.0)


def test_stage11a_orientation_reverse_and_noninjective_maps_are_excluded() -> None:
    controls = {item.parameterization_id: item for item in stage11a_excluded_parameterizations()}
    assert not controls[STAGE11A_REVERSE].admissible
    assert not controls[STAGE11A_REVERSE].orientation_preserving
    assert controls[STAGE11A_REVERSE].injective_on_test_domain

    assert not controls[STAGE11A_NONINJECTIVE].admissible
    assert not controls[STAGE11A_NONINJECTIVE].injective_on_test_domain

    with pytest.raises(ValueError, match="boundary/control"):
        canonical_stage11a_trajectory(STAGE11A_REVERSE)
    with pytest.raises(ValueError, match="boundary/control"):
        canonical_stage11a_trajectory(STAGE11A_NONINJECTIVE)


def test_stage11a_diagnostics_close_criteria_11_through_16() -> None:
    diagnostics = stage11a_diagnostics()
    assert diagnostics.event_count == 13
    assert diagnostics.positive_parameterization_count == 4
    assert diagnostics.minimum_positive_lapse > 0.0
    assert diagnostics.max_constraint_residual <= STAGE11A_ATOL
    assert diagnostics.max_lapse_chain_rule_residual <= STAGE11A_ATOL
    assert diagnostics.differing_parameter_event_pairs == 36
    assert diagnostics.nonlinear_raw_rate_difference_count > 0
    assert diagnostics.positive_family_admissible
    assert diagnostics.constraint_orbit_preserved
    assert diagnostics.orientation_reverse_excluded
    assert diagnostics.noninjective_excluded
    assert diagnostics.criteria_11_16_satisfied
