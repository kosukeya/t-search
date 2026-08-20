import numpy as np
import pytest

from t_search.stage4_conditional import clock_probability_profile, physical_reduction
from t_search.stage4_controls import (
    global_conditional_born_probability,
    local_born_probability,
    plus01_projector,
)
from t_search.stage4_quantum import (
    DEFAULT_ATOL,
    equal_amplitude_physical_state,
    is_physical_state,
    physical_state_from_coefficients,
    tensor_basis_state,
)
from t_search.stage4_robustness import (
    ClockLabeling,
    global_phase_local_density_residual,
    global_phase_shift,
    ray_change_deficit_profile,
    relabeled_composition_residual,
    relabeled_transition_matrix,
    summarize_physical_state_robustness,
)
from t_search.stage4_transition import relational_transition_matrix


def _generic_coefficients(dimension: int, offset: float = 0.0) -> np.ndarray:
    values = np.array(
        [
            complex(n + 1.0 + offset, ((-1) ** n) * (n + 0.37 + offset))
            for n in range(dimension)
        ],
        dtype=np.complex128,
    )
    return values / np.linalg.norm(values)


def test_cross_stage4_summary_is_stable_across_dimensions_3_to_6():
    for d in (3, 4, 5, 6):
        state = physical_state_from_coefficients(_generic_coefficients(d), d)
        summary = summarize_physical_state_robustness(state, d)
        assert summary.max_structural_residual <= DEFAULT_ATOL


def test_cross_stage4_summary_is_stable_across_coefficient_families():
    d = 4
    families = [
        np.ones(d, dtype=np.complex128) / np.sqrt(d),
        _generic_coefficients(d),
        _generic_coefficients(d, offset=0.61),
        np.array([1.0, 1.0j, 0.0, 0.0], dtype=np.complex128) / np.sqrt(2.0),
    ]
    for coefficients in families:
        state = physical_state_from_coefficients(coefficients, d)
        summary = summarize_physical_state_robustness(state, d)
        assert summary.max_structural_residual <= DEFAULT_ATOL


def test_cross_stage4_summary_is_stable_under_multiple_clock_origins():
    d = 4
    state = physical_state_from_coefficients(_generic_coefficients(d), d)
    for origin in (-0.73, 0.0, 0.37, 5.2):
        summary = summarize_physical_state_robustness(state, d, origin=origin)
        assert summary.max_structural_residual <= DEFAULT_ATOL


def test_arbitrary_clock_label_rename_preserves_every_transition_matrix():
    labeling = ClockLabeling(("gamma", "alpha", "delta", "beta"))
    for source_label in labeling.labels:
        for target_label in labeling.labels:
            source = labeling.index_of(source_label)
            target = labeling.index_of(target_label)
            renamed = relabeled_transition_matrix(
                labeling, source_label, target_label
            )
            native = relational_transition_matrix(source, target, labeling.dimension)
            assert np.allclose(renamed, native, atol=DEFAULT_ATOL, rtol=0.0)


def test_clock_label_rename_preserves_composition_for_all_label_triples():
    labeling = ClockLabeling(("west", "north", "south", "east"))
    for source in labeling.labels:
        for middle in labeling.labels:
            for target in labeling.labels:
                assert (
                    relabeled_composition_residual(
                        labeling, source, middle, target
                    )
                    <= DEFAULT_ATOL
                )


def test_clock_labeling_rejects_duplicate_empty_and_unknown_labels():
    with pytest.raises(ValueError, match="unique"):
        ClockLabeling(("a", "a"))
    with pytest.raises(ValueError, match="nonempty"):
        ClockLabeling(("a", ""))
    labeling = ClockLabeling(("a", "b"))
    with pytest.raises(ValueError, match="unknown clock label"):
        labeling.index_of("c")


def test_global_phase_preserves_physicality_and_clock_probability_profile():
    d = 4
    state = physical_state_from_coefficients(_generic_coefficients(d), d)
    shifted = global_phase_shift(state, 1.234, d)
    assert is_physical_state(shifted, d)
    assert not np.allclose(shifted, state, atol=1e-6, rtol=0.0)
    assert np.allclose(
        clock_probability_profile(shifted, d),
        clock_probability_profile(state, d),
        atol=DEFAULT_ATOL,
        rtol=0.0,
    )


def test_global_phase_preserves_every_clock_relative_density_matrix():
    d = 4
    state = physical_state_from_coefficients(_generic_coefficients(d), d)
    for j in range(d):
        assert (
            global_phase_local_density_residual(state, j, -0.918, d)
            <= DEFAULT_ATOL
        )


def test_global_phase_preserves_global_and_local_born_probabilities():
    d = 4
    state = physical_state_from_coefficients(_generic_coefficients(d), d)
    shifted = global_phase_shift(state, 0.441, d)
    projector = plus01_projector(d)
    for j in range(d):
        assert abs(
            global_conditional_born_probability(state, j, projector, d)
            - global_conditional_born_probability(shifted, j, projector, d)
        ) <= DEFAULT_ATOL
        assert abs(
            local_born_probability(state, j, projector, d)
            - local_born_probability(shifted, j, projector, d)
        ) <= DEFAULT_ATOL


def test_two_sector_physical_state_has_nontrivial_ray_change():
    d = 4
    coefficients = np.array([1.0, 1.0, 0.0, 0.0], dtype=np.complex128) / np.sqrt(2.0)
    state = physical_state_from_coefficients(coefficients, d)
    deficits = ray_change_deficit_profile(state, d)
    assert deficits[0] <= DEFAULT_ATOL
    assert np.max(deficits) >= 1.0 - DEFAULT_ATOL


def test_single_sector_physical_state_has_no_ray_change_at_any_reading():
    d = 4
    state = tensor_basis_state(1, 1, d)
    deficits = ray_change_deficit_profile(state, d)
    assert np.max(np.abs(deficits)) <= DEFAULT_ATOL


def test_robustness_summary_rejects_nonphysical_kinematic_state():
    d = 4
    bad = (
        tensor_basis_state(0, 0, d) + tensor_basis_state(0, 1, d)
    ) / np.sqrt(2.0)
    with pytest.raises(ValueError, match="zero-constraint"):
        summarize_physical_state_robustness(bad, d)
