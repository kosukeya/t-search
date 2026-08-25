import numpy as np
import pytest

from t_search.stage16_local import (
    STAGE16A_ADJACENT_FORWARD_EDGES,
    STAGE16A_OPPOSITE_PAIRS,
    STAGE16A_SMEARING_PAIRS,
    canonical_stage16a_representatives,
    stage16a_constraints,
    stage16a_dirac_data,
)
from t_search.stage16_paths import (
    STAGE16B_ATOL,
    STAGE16B_ENDPOINT_TOL,
    STAGE16B_LOCAL_STEP_PAIRS,
    STAGE16B_PARAMETER_BOUND,
    STAGE16B_PRESENTED_COMPENSATION_KIND,
    STAGE16B_PRESENTED_SEARCH_ALL_FOUND,
    STAGE16B_INTERPRETATION_GUARDS,
    STAGE16B_PRESENTED_WORDS,
    STAGE16B_REFERENCE_CYCLE_WORD,
    STAGE16B_SEED_COMPENSATION_KIND,
    canonical_stage16b_cycle_probes,
    canonical_stage16b_local_probes,
    canonical_stage16b_smeared_probes,
    stage16b_apply_local_flow,
    stage16b_diagnostics,
    stage16b_local_oracle,
    stage16b_local_raw_endpoints,
)


def _phase_residual(a,b):
    return max(abs(x-y) for x,y in zip(a.vector(),b.vector(),strict=True))


def test_stage16b_exact_local_flows_preserve_surface_and_match_independent_oracle():
    reps=canonical_stage16a_representatives()
    oracle_reps=tuple(reps[orbit*81+offset] for orbit in range(4) for offset in (0,40,80))
    count=0
    for rep in oracle_reps:
        for i in range(4):
            for parameter in (-0.5,0.5):
                exact=stage16b_apply_local_flow(rep.point(),i,parameter)
                oracle=stage16b_local_oracle(rep.point(),i,parameter)
                assert max(abs(x) for x in stage16a_constraints(exact)) <= STAGE16B_ATOL
                assert stage16a_dirac_data(exact) == pytest.approx(stage16a_dirac_data(rep.point()),abs=STAGE16B_ATOL)
                assert _phase_residual(exact,oracle) <= STAGE16B_ENDPOINT_TOL
                count+=1
    assert count == 96


def test_stage16b_adjacent_defects_match_prediction_and_opposite_pairs_commute():
    probes=canonical_stage16b_local_probes()
    assert len(probes)==2592
    assert sum(abs(p.observed_defect)>STAGE16B_ATOL for p in probes)==2592
    assert max(abs(p.observed_defect-p.predicted_defect) for p in probes)==pytest.approx(0.0,abs=STAGE16B_ATOL)
    assert max(p.off_axis_residual for p in probes)==pytest.approx(0.0,abs=STAGE16B_ATOL)

    count=0
    for rep in canonical_stage16a_representatives():
        for i,j in STAGE16A_OPPOSITE_PAIRS:
            for s,u in STAGE16B_LOCAL_STEP_PAIRS:
                a,b=stage16b_local_raw_endpoints(rep.point(),i,j,s,u)
                assert _phase_residual(a,b)<=STAGE16B_ENDPOINT_TOL
                count+=1
    assert count==1296


def test_stage16b_seed_compensation_closes_but_missing_and_wrong_sign_are_rejected():
    probes=canonical_stage16b_local_probes()
    assert STAGE16B_SEED_COMPENSATION_KIND == 'global_seed_oracle'
    assert max(p.seed_compensated_residual for p in probes) <= STAGE16B_ENDPOINT_TOL
    assert max(p.payload_residual for p in probes) <= STAGE16B_ENDPOINT_TOL
    assert min(p.missing_residual for p in probes) == pytest.approx(0.015625,abs=STAGE16B_ATOL)
    assert min(p.wrong_sign_residual for p in probes) == pytest.approx(0.03125,abs=STAGE16B_ATOL)
    assert min(p.missing_residual for p in probes)>STAGE16B_ENDPOINT_TOL
    assert min(p.wrong_sign_residual for p in probes)>STAGE16B_ENDPOINT_TOL


def test_stage16b_presented_C_search_uses_frozen_family_and_finds_bounded_compensators():
    probes=canonical_stage16b_local_probes()
    assert len(STAGE16B_PRESENTED_WORDS)==24
    assert set(STAGE16B_PRESENTED_WORDS)==set(__import__('itertools').permutations(range(4)))
    assert STAGE16B_PARAMETER_BOUND==2.0
    assert STAGE16B_PRESENTED_COMPENSATION_KIND == 'presented_C_word_search'
    assert STAGE16B_PRESENTED_SEARCH_ALL_FOUND == 'presented_C_compensator_found_for_all_frozen_local_probes'
    assert all(p.presented_success for p in probes)
    assert all(p.presented_word==STAGE16B_REFERENCE_CYCLE_WORD for p in probes)
    assert max(p.presented_attempt_count for p in probes)==1
    assert max(p.presented_residual for p in probes)<=STAGE16B_ENDPOINT_TOL
    assert max(max(abs(x) for x in p.presented_parameters) for p in probes)<=0.103
    assert max(max(abs(x) for x in p.presented_parameters) for p in probes)<STAGE16B_PARAMETER_BOUND


def test_stage16b_smeared_matrix_exponential_ordering_and_seed_compensation():
    probes=canonical_stage16b_smeared_probes()
    assert len(STAGE16A_SMEARING_PAIRS)==8
    assert len(probes)==2592
    assert sum(p.raw_endpoint_residual>STAGE16B_ENDPOINT_TOL for p in probes)==2268
    assert sum(p.raw_endpoint_residual<=STAGE16B_ENDPOINT_TOL for p in probes)==324
    assert sum(p.zero_wedge_control for p in probes)==324
    assert all((p.raw_endpoint_residual<=STAGE16B_ENDPOINT_TOL) for p in probes if p.zero_wedge_control)
    assert max(p.seed_compensated_residual for p in probes)<=STAGE16B_ENDPOINT_TOL
    assert max(p.payload_residual for p in probes)<=STAGE16B_ENDPOINT_TOL


def test_stage16b_cycle_word_audit_exhibits_raw_ordering_dependence_and_seed_closure():
    probes=canonical_stage16b_cycle_probes()
    assert len(STAGE16B_PRESENTED_WORDS)==24
    assert len(probes)==7776
    assert sum(p.raw_endpoint_residual<=STAGE16B_ENDPOINT_TOL for p in probes)==324
    assert sum(p.raw_endpoint_residual>STAGE16B_ENDPOINT_TOL for p in probes)==7452
    assert all(p.raw_endpoint_residual<=STAGE16B_ENDPOINT_TOL for p in probes if p.word==STAGE16B_REFERENCE_CYCLE_WORD)
    assert max(p.seed_compensated_residual for p in probes)<=STAGE16B_ENDPOINT_TOL
    assert max(p.payload_residual for p in probes)<=STAGE16B_ENDPOINT_TOL


def test_stage16b_diagnostics_close_only_criteria_18_through_24():
    d=stage16b_diagnostics()
    assert d.representative_count==324
    assert d.local_probe_count==2592
    assert d.local_nonzero_defect_count==2592
    assert d.opposite_commuting_probe_count==1296
    assert d.presented_search_success_count==2592
    assert d.presented_search_failure_count==0
    assert d.presented_search_max_attempt_count==1
    assert d.smeared_probe_count==2592
    assert d.smeared_nonzero_defect_count==2268
    assert d.smeared_zero_defect_count==324
    assert d.cycle_probe_count==7776
    assert d.cycle_nonzero_word_count==7452
    assert d.single_local_oracle_probe_count==96
    assert d.single_smeared_oracle_probe_count==84
    assert d.max_local_prediction_residual<=STAGE16B_ENDPOINT_TOL
    assert d.max_seed_compensated_local_residual<=STAGE16B_ENDPOINT_TOL
    assert d.max_presented_compensated_local_residual<=STAGE16B_ENDPOINT_TOL
    assert d.max_single_local_oracle_residual<=STAGE16B_ENDPOINT_TOL
    assert d.max_single_smeared_oracle_residual<=STAGE16B_ENDPOINT_TOL
    assert d.max_presented_compensator_oracle_residual<=STAGE16B_ENDPOINT_TOL
    assert d.max_smeared_order_oracle_residual<=STAGE16B_ENDPOINT_TOL
    assert d.max_abs_presented_parameter<STAGE16B_PARAMETER_BOUND
    assert d.max_smeared_seed_compensated_residual<=STAGE16B_ENDPOINT_TOL
    assert d.max_cycle_seed_compensated_residual<=STAGE16B_ENDPOINT_TOL
    assert d.min_missing_compensator_residual>STAGE16B_ENDPOINT_TOL
    assert d.min_wrong_sign_compensator_residual>STAGE16B_ENDPOINT_TOL
    assert d.exact_local_flows_established
    assert d.local_defect_prediction_established
    assert d.seed_compensation_established
    assert d.presented_search_executed
    assert d.exact_smeared_flow_established
    assert d.smeared_compensation_established
    assert d.controls_rejected
    assert d.criteria_18_24_satisfied
    assert d.presented_search_classification == STAGE16B_PRESENTED_SEARCH_ALL_FOUND


def test_stage16b_interpretation_guards_do_not_promote_path_compensation_to_basis_or_metaphysics():
    guards=STAGE16B_INTERPRETATION_GUARDS
    assert guards == (
      'raw path-word inequality != physical path dependence',
      'seed-compensated closure != local presented-basis compensation',
      'presented compensator found != locality-preserving Abelianizing basis',
      'presented compensator not found in frozen word search != physical obstruction',
      'compensated cycle path closure != refoliation invariance',
      'cycle path defect != spacetime curvature',
      'finite constant smearing != continuum lapse/shift field',
      'Stage 16B path compensation != Stage 16D basis Abelianization',
      'repository validation != new scientific evidence',
    )
    assert len(guards)==9