from __future__ import annotations

import numpy as np
import pytest

from t_search.stage13_multi_constraint import (
    STAGE13A_ATOL,
    STAGE13A_BASIS_ID,
    STAGE13A_BASIS_ROLE,
    STAGE13A_CLOCK_T_ROLE,
    STAGE13A_CLOCK_X_ROLE,
    STAGE13A_EVENT_ROLE,
    STAGE13A_GENERATOR_ROLE,
    STAGE13A_K_T,
    STAGE13A_K_X,
    STAGE13A_ORBIT_ROLE,
    STAGE13A_REPRESENTATIVE_ROLE,
    canonical_stage13a_mixed_pairs,
    canonical_stage13a_off_surface_bracket_probes,
    canonical_stage13a_orbits,
    canonical_stage13a_phi_T_transports,
    canonical_stage13a_phi_X_transports,
    canonical_stage13a_representatives,
    canonical_stage13a_representatives_for_orbit,
    stage13a_K_X,
    stage13a_constraint_gradients,
    stage13a_diagnostics,
    stage13a_generator_vectors,
    stage13a_phi_T_transport,
    stage13a_phi_X_transport,
    stage13a_poisson_KT_KX,
    stage13a_summary,
)


def test_stage13a_builds_exact_36_representative_positive_family() -> None:
    orbits = canonical_stage13a_orbits()
    representatives = canonical_stage13a_representatives()

    assert len(orbits) == 4
    assert len(representatives) == 36
    assert len({rep.representative_id for rep in representatives}) == 36
    assert len({rep.event_id for rep in representatives}) == 36
    assert all(abs(rep.K_T_value) <= STAGE13A_ATOL for rep in representatives)
    assert all(abs(rep.K_X_value) <= STAGE13A_ATOL for rep in representatives)
    assert all(len(canonical_stage13a_representatives_for_orbit(orbit)) == 9 for orbit in orbits)


def test_stage13a_two_constraint_and_generator_directions_are_independent_everywhere() -> None:
    for representative in canonical_stage13a_representatives():
        gradients = stage13a_constraint_gradients(representative.point())
        generators = stage13a_generator_vectors(representative.point())

        assert np.linalg.matrix_rank(gradients, tol=STAGE13A_ATOL) == 2
        assert np.linalg.matrix_rank(generators, tol=STAGE13A_ATOL) == 2
        assert np.linalg.svd(gradients, compute_uv=False)[-1] > STAGE13A_ATOL
        assert np.linalg.svd(generators, compute_uv=False)[-1] > STAGE13A_ATOL


def test_stage13a_first_class_bracket_identity_is_nontrivially_checked_off_surface() -> None:
    positive_points = tuple(rep.point() for rep in canonical_stage13a_representatives())
    probes = canonical_stage13a_off_surface_bracket_probes()

    assert len(probes) == 36
    assert all(abs(stage13a_K_X(point)) > STAGE13A_ATOL for point in probes)

    for point in positive_points + probes:
        assert abs(stage13a_poisson_KT_KX(point) + stage13a_K_X(point)) <= STAGE13A_ATOL


def test_stage13a_phi_T_and_phi_X_each_preserve_the_positive_surface() -> None:
    phi_T = canonical_stage13a_phi_T_transports()
    phi_X = canonical_stage13a_phi_X_transports()

    assert len(phi_T) == 72
    assert len(phi_X) == 72
    assert {item.generator_id for item in phi_T} == {STAGE13A_K_T}
    assert {item.generator_id for item in phi_X} == {STAGE13A_K_X}

    for item in phi_T + phi_X:
        assert item.phase_space_residual <= STAGE13A_ATOL
        assert item.source_constraint_residual <= STAGE13A_ATOL
        assert item.predicted_constraint_residual <= STAGE13A_ATOL
        assert item.target_constraint_residual <= STAGE13A_ATOL


def test_stage13a_mixed_family_is_enumerated_but_not_yet_promoted_to_path_closure() -> None:
    mixed = canonical_stage13a_mixed_pairs()

    assert len(mixed) == 144
    assert all(source.orbit_id == target.orbit_id for source, target in mixed)
    assert all(abs(source.T - target.T) > STAGE13A_ATOL for source, target in mixed)
    assert all(abs(source.X - target.X) > STAGE13A_ATOL for source, target in mixed)

    summary = stage13a_summary()
    assert summary["mixed_ordered_pair_count_reserved_for_stage13b"] == 144
    assert summary["next"] == "Stage 13B — noncommuting gauge paths and compensated closure"


def test_stage13a_retains_four_declared_initial_data_classes_without_collapse() -> None:
    orbits = canonical_stage13a_orbits()
    pairs = {(orbit.Q_D, orbit.P_D) for orbit in orbits}

    assert len(pairs) == 4
    assert orbits[0].P_D == orbits[1].P_D
    assert orbits[0].Q_D != orbits[1].Q_D
    assert orbits[0].Q_D == orbits[2].Q_D
    assert orbits[0].P_D != orbits[2].P_D

    for orbit in orbits:
        reps = canonical_stage13a_representatives_for_orbit(orbit)
        assert {(rep.declared_Q_D, rep.declared_P_D) for rep in reps} == {(orbit.Q_D, orbit.P_D)}


def test_stage13a_keeps_orbit_representative_event_clock_generator_and_basis_typing_separate() -> None:
    representatives = canonical_stage13a_representatives()
    transports = canonical_stage13a_phi_T_transports() + canonical_stage13a_phi_X_transports()

    roles = {
        STAGE13A_ORBIT_ROLE,
        STAGE13A_REPRESENTATIVE_ROLE,
        STAGE13A_EVENT_ROLE,
        STAGE13A_CLOCK_T_ROLE,
        STAGE13A_CLOCK_X_ROLE,
        STAGE13A_BASIS_ROLE,
        STAGE13A_GENERATOR_ROLE,
    }
    assert len(roles) == 7
    assert all(rep.orbit_role == STAGE13A_ORBIT_ROLE for rep in representatives)
    assert all(rep.representative_role == STAGE13A_REPRESENTATIVE_ROLE for rep in representatives)
    assert all(rep.event_role == STAGE13A_EVENT_ROLE for rep in representatives)
    assert all(rep.clock_T_role == STAGE13A_CLOCK_T_ROLE for rep in representatives)
    assert all(rep.clock_X_role == STAGE13A_CLOCK_X_ROLE for rep in representatives)
    assert all(rep.constraint_basis_id == STAGE13A_BASIS_ID for rep in representatives)
    assert all(rep.constraint_basis_role == STAGE13A_BASIS_ROLE for rep in representatives)
    assert all(item.generator_role == STAGE13A_GENERATOR_ROLE for item in transports)


def test_stage13a_rejects_unlicensed_single_generator_transport_shapes() -> None:
    alpha = canonical_stage13a_representatives_for_orbit(canonical_stage13a_orbits()[0])
    beta = canonical_stage13a_representatives_for_orbit(canonical_stage13a_orbits()[1])

    with pytest.raises(ValueError, match="distinct physical orbits"):
        stage13a_phi_T_transport(alpha[0], beta[3])

    mixed_target = next(
        target
        for target in alpha
        if abs(target.T - alpha[0].T) > STAGE13A_ATOL
        and abs(target.X - alpha[0].X) > STAGE13A_ATOL
    )
    with pytest.raises(ValueError, match="fixed X"):
        stage13a_phi_T_transport(alpha[0], mixed_target)
    with pytest.raises(ValueError, match="fixed T"):
        stage13a_phi_X_transport(alpha[0], mixed_target)


def test_stage13a_diagnostics_close_only_criteria_11_16() -> None:
    diagnostics = stage13a_diagnostics()
    summary = stage13a_summary()

    assert diagnostics.orbit_count == 4
    assert diagnostics.representative_count == 36
    assert diagnostics.representatives_per_orbit == 9
    assert diagnostics.phi_T_transport_count == 72
    assert diagnostics.phi_X_transport_count == 72
    assert diagnostics.single_generator_transport_count == 144
    assert diagnostics.mixed_ordered_pair_count == 144
    assert diagnostics.off_surface_bracket_probe_count == 36
    assert diagnostics.distinct_declared_initial_data_count == 4
    assert diagnostics.minimum_constraint_gradient_rank == 2
    assert diagnostics.minimum_generator_vector_rank == 2
    assert diagnostics.canonical_orbits_distinct
    assert diagnostics.representative_family_complete
    assert diagnostics.independent_constraint_directions
    assert diagnostics.first_class_closure_established
    assert diagnostics.individual_flows_preserve_surface
    assert diagnostics.physical_initial_data_preserved
    assert diagnostics.typed_provenance_explicit
    assert diagnostics.criteria_11_16_satisfied

    assert summary["criteria_11_16_satisfied"] is True
    assert "hypersurface-deformation algebra" in " ".join(summary["guards"])
    assert "compensated multi-generator path closure" in " ".join(summary["guards"])
