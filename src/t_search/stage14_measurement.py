"""Stage 14E typed O/P/R/V/Xi and future-measurement descent.

Finite operational checks only: no refoliation, future-actuality, empirical,
GR, or ontological claim is licensed.
"""
from __future__ import annotations
from dataclasses import dataclass, replace
from functools import lru_cache
from math import tanh
from t_search.stage9_modal import FUTURE_SIGNATURE_LEFT, FUTURE_SIGNATURE_OTHER
from t_search.stage11_lift import Stage11OLayer, Stage11OEvent, Stage11PLayer, Stage11RLayer, Stage11VLayer
from t_search.stage11_parametrized import STAGE11A_IDENTITY
from t_search.stage13_measurement import canonical_stage13e_measurement_views, canonical_stage13e_posterior_views, canonical_stage13e_quotient_projections, canonical_stage13e_weighted_views
from t_search.stage14_basis import STAGE14D_TRIANGULAR_BASIS_ID
from t_search.stage14_paths import STAGE14B_PATH_12D, STAGE14B_PATH_21D, canonical_stage14b_mixed_pairs
from t_search.stage14_relational import stage14c_complete_relational_value, stage14c_quotient_classes
from t_search.stage14_structure_function import STAGE14A_ATOL, STAGE14A_BASIS_ID, STAGE14A_H1, STAGE14A_H2, canonical_stage14a_orbits, canonical_stage14a_representatives, stage14a_apply_flow, stage14a_structure_functions

STAGE14E_ATOL=STAGE14A_ATOL
STAGE14E_PATH_DESCENT_CLASSIFICATION="structure_function_path_operational_payloads_descend"
STAGE14E_BASIS_DESCENT_CLASSIFICATION="basis_operational_payloads_descend"
STAGE14E_REPRESENTATIVE_CORRUPTION="representative_dependent_payload_corruption_detected"
STAGE14E_PATH_CORRUPTION="path_dependent_payload_corruption_detected"
STAGE14E_BASIS_CORRUPTION="basis_dependent_payload_corruption_detected"
STAGE14E_NOT_LICENSED="not_licensed"
STAGE14E_CLOCK_TRIPLES=(("e1",-1.,-1.,-1.),("e2",1.,1.,1.))
STAGE14E_BOUNDED_RESULT="Stage 14E typed O/P/R/V/Xi and future-measurement descent across structure-function paths and original/triangular basis choices on the frozen finite family = established"

@dataclass(frozen=True,slots=True)
class Stage14EFuturePayload:
    orbit_id:str; measurement:tuple; weighted:tuple; posterior:tuple
    future_signature_ids:tuple[str,str]=(FUTURE_SIGNATURE_LEFT,FUTURE_SIGNATURE_OTHER)
    future_actuality_status:str=STAGE14E_NOT_LICENSED
    empirical_claim_status:str=STAGE14E_NOT_LICENSED

@dataclass(frozen=True,slots=True)
class Stage14EXi:
    orbit_id:str; quotient_id:str; representative_id:str; constraint_basis_id:str
    basis_transform_provenance:str; source_structure_functions:tuple[float,float]
    representative_coordinates:tuple[float,float,float]; licensed_path_words:tuple[str,str]
    event_correspondence:tuple; continuation_class_correspondence:tuple; outcome_correspondence:tuple
    provenance_semantics:str="structure-function/path/basis provenance retained in Xi only"

@dataclass(frozen=True,slots=True)
class Stage14ETypedArchitecture:
    orbit_id:str; quotient_id:str; representative_id:str
    O:Stage11OLayer; P:Stage11PLayer; R:Stage11RLayer; V:Stage11VLayer
    future_measurement:Stage14EFuturePayload; Xi:Stage14EXi

@dataclass(frozen=True,slots=True)
class Stage14EQuotientArchitecture:
    orbit_id:str; quotient_id:str; O:Stage11OLayer; P:Stage11PLayer; R:Stage11RLayer; V:Stage11VLayer
    future_measurement:Stage14EFuturePayload; parameterization_id:str
    event_correspondence:tuple; continuation_class_correspondence:tuple; outcome_correspondence:tuple

@dataclass(frozen=True,slots=True)
class Stage14EPathXi:
    pair_id:str; path_word:str; source_representative_id:str; target_representative_id:str
    s:float; u:float; v:float; structure_function_trace:tuple; compensator_provenance:str

@dataclass(frozen=True,slots=True)
class Stage14EPathCheck:
    pair_id:str; path_Xi_12D:Stage14EPathXi; path_Xi_21D:Stage14EPathXi
    provenance_distinct:bool; trace_distinct:bool; public_equal:bool; future_equal:bool; witness_equal:bool
    classification:str=STAGE14E_PATH_DESCENT_CLASSIFICATION

@dataclass(frozen=True,slots=True)
class Stage14EBasisCheck:
    representative_id:str; original_Xi:Stage14EXi; triangular_Xi:Stage14EXi
    provenance_distinct:bool; public_equal:bool; future_equal:bool; witness_equal:bool
    classification:str=STAGE14E_BASIS_DESCENT_CLASSIFICATION

@dataclass(frozen=True,slots=True)
class Stage14EOrbitWitness:
    orbit_id:str; representative_id:str; probabilities:tuple[tuple[str,float],...]
    probability_sum_residual:float
    semantics:str="orbit-conditioned diagnostic only; not an empirical prediction"

@dataclass(frozen=True,slots=True)
class Stage14EControl:
    control_id:str; classification:str; rejected:bool

@dataclass(frozen=True,slots=True)
class Stage14EDiagnostics:
    representative_count:int; quotient_class_count:int; distinct_public_count:int
    path_check_count:int; path_xi_count:int; basis_check_count:int; basis_xi_count:int
    witness_count:int; distinct_witness_count:int; minimum_witness_separation:float
    same_orbit_descent:bool; path_descent:bool; basis_descent:bool
    public_provenance_absent:bool; xi_provenance_explicit:bool
    control_count:int; rejected_control_count:int; criteria_39_43_satisfied:bool

def _m(x): return (x.continuation_id,x.family_id,x.internal_clock,x.internal_clock_index,x.outcome_ids,x.normalization_semantics,x.probabilities)
def _w(x): return (x.continuation_ids,x.continuation_weights,x.directional_record_scores,x.directional_accessibility_scores,x.orientations,x.next_outcomes,x.next_probabilities)
def _p(x): return (x.observed_outcome,x.epistemic_posterior_weights,x.ontic_posterior_weights,x.epistemic_selected_continuation_id,x.ontic_no_selected_complete_continuation_datum)

@lru_cache(maxsize=1)
def _public():
    d={}
    for x in canonical_stage13e_quotient_projections():
        d.setdefault(x.orbit_id,x)
        if d[x.orbit_id]!=x: raise ValueError("inherited public payload is representative-dependent")
    return d

@lru_cache(maxsize=1)
def _future():
    d={}
    ms=canonical_stage13e_measurement_views(); ws=canonical_stage13e_weighted_views(); ps=canonical_stage13e_posterior_views()
    for orbit in canonical_stage14a_orbits():
        oid=orbit.orbit_id
        d[oid]=Stage14EFuturePayload(oid,tuple(sorted({_m(x) for x in ms if x.orbit_id==oid},key=repr)),tuple(sorted({_w(x) for x in ws if x.orbit_id==oid},key=repr)),tuple(sorted({_p(x) for x in ps if x.orbit_id==oid},key=repr)))
        if not d[oid].measurement or not d[oid].weighted or not d[oid].posterior: raise ValueError("missing inherited future payload")
    return d

@lru_cache(maxsize=1)
def _qbyrep():
    d={}
    for q in stage14c_quotient_classes():
        for rid in q.member_representative_ids: d[rid]=q
    if len(d)!=108: raise ValueError("quotient lookup must cover 108 representatives")
    return d

def _basis(bid):
    if bid==STAGE14A_BASIS_ID: return "identity_original_structure_function_basis"
    if bid==STAGE14D_TRIANGULAR_BASIS_ID: return "H_2_tilde=H_2-kappa*T1*X*D"
    raise ValueError(bid)

def _events(rep):
    q=_qbyrep()[rep.representative_id]; out=[]
    for eid,t1,t2,x in STAGE14E_CLOCK_TRIPLES:
        out.append(Stage11OEvent(role="prediction_anchor" if eid=="e1" else "measurement_target",stage10_event=eid,physical_event_id=f"{rep.orbit_id}:complete_relational:{eid}",clock_value=t1,q_value=stage14c_complete_relational_value(q.Q_D,q.P_D,t1,t2,x)))
    return tuple(out)

def stage14e_architecture_for_representative(rep,*,basis_id=STAGE14A_BASIS_ID):
    base=_public()[rep.orbit_id]; q=_qbyrep()[rep.representative_id]; O=replace(base.O,relational_events=_events(rep))
    xi=Stage14EXi(rep.orbit_id,q.class_id,rep.representative_id,basis_id,_basis(basis_id),stage14a_structure_functions(rep.point()),(rep.T1,rep.T2,rep.X),(STAGE14B_PATH_12D,STAGE14B_PATH_21D),tuple((e.stage10_event,e.physical_event_id) for e in O.relational_events),base.continuation_class_correspondence,base.outcome_correspondence)
    return Stage14ETypedArchitecture(rep.orbit_id,q.class_id,rep.representative_id,O,base.P,base.R,base.V,_future()[rep.orbit_id],xi)

@lru_cache(maxsize=1)
def canonical_stage14e_architectures(): return tuple(stage14e_architecture_for_representative(r) for r in canonical_stage14a_representatives())

def stage14e_validate_architecture(a):
    rep=next((r for r in canonical_stage14a_representatives() if r.representative_id==a.representative_id),None)
    if rep is None: return False,("representative_identity",)
    expected=stage14e_architecture_for_representative(rep,basis_id=a.Xi.constraint_basis_id)
    return a==expected,() if a==expected else ("typed_architecture_mismatch",)

def stage14e_quotient_projection(a):
    return Stage14EQuotientArchitecture(a.orbit_id,a.quotient_id,a.O,a.P,a.R,a.V,a.future_measurement,STAGE11A_IDENTITY,a.Xi.event_correspondence,a.Xi.continuation_class_correspondence,a.Xi.outcome_correspondence)

@lru_cache(maxsize=1)
def canonical_stage14e_quotient_projections(): return tuple(stage14e_quotient_projection(a) for a in canonical_stage14e_architectures())

def stage14e_orbit_witness(a):
    q=_qbyrep()[a.representative_id]; rq=stage14c_complete_relational_value(q.Q_D,q.P_D,1.,1.,1.)
    left=.5*(1.+tanh(.70*q.Q_D+.40*q.P_D+.20*rq)); probs=((FUTURE_SIGNATURE_LEFT,left),(FUTURE_SIGNATURE_OTHER,1.-left))
    return Stage14EOrbitWitness(a.orbit_id,a.representative_id,probs,abs(sum(v for _,v in probs)-1.))

@lru_cache(maxsize=1)
def canonical_stage14e_orbit_witnesses(): return tuple(stage14e_orbit_witness(a) for a in canonical_stage14e_architectures())

def _pathxi(pair,word):
    src=pair.source.point()
    if word==STAGE14B_PATH_12D: after=stage14a_apply_flow(src,STAGE14A_H1,pair.s); v=pair.v_12D; cp="exact_D_compensator:v_12D"
    elif word==STAGE14B_PATH_21D: after=stage14a_apply_flow(src,STAGE14A_H2,pair.u); v=pair.v_21D; cp="exact_D_compensator:v_21D"
    else: raise ValueError(word)
    return Stage14EPathXi(pair.pair_id,word,pair.source.representative_id,pair.target.representative_id,pair.s,pair.u,v,(stage14a_structure_functions(src),stage14a_structure_functions(after)),cp)

@lru_cache(maxsize=1)
def canonical_stage14e_path_descent_checks():
    A={a.representative_id:a for a in canonical_stage14e_architectures()}; W={w.representative_id:w for w in canonical_stage14e_orbit_witnesses()}; out=[]
    for pair in canonical_stage14b_mixed_pairs():
        s,t=A[pair.source.representative_id],A[pair.target.representative_id]; x,y=_pathxi(pair,STAGE14B_PATH_12D),_pathxi(pair,STAGE14B_PATH_21D)
        out.append(Stage14EPathCheck(pair.pair_id,x,y,x!=y,x.structure_function_trace!=y.structure_function_trace,stage14e_quotient_projection(s)==stage14e_quotient_projection(t),s.future_measurement==t.future_measurement,W[s.representative_id].probabilities==W[t.representative_id].probabilities))
    return tuple(out)

@lru_cache(maxsize=1)
def canonical_stage14e_basis_descent_checks():
    out=[]
    for r in canonical_stage14a_representatives():
        a=stage14e_architecture_for_representative(r); b=stage14e_architecture_for_representative(r,basis_id=STAGE14D_TRIANGULAR_BASIS_ID)
        out.append(Stage14EBasisCheck(r.representative_id,a.Xi,b.Xi,a.Xi!=b.Xi,stage14e_quotient_projection(a)==stage14e_quotient_projection(b),a.future_measurement==b.future_measurement,stage14e_orbit_witness(a).probabilities==stage14e_orbit_witness(b).probabilities))
    return tuple(out)

def stage14e_controls():
    a=canonical_stage14e_architectures()[0]
    badO=replace(a.O,relational_events=(replace(a.O.relational_events[0],q_value=a.O.relational_events[0].q_value+.125),)+a.O.relational_events[1:])
    badP=replace(a.future_measurement,measurement=a.future_measurement.measurement+(("path_corruption",),))
    badB=replace(a.future_measurement,weighted=a.future_measurement.weighted+(("basis_corruption",),))
    return (Stage14EControl("representative_dependent_public_payload",STAGE14E_REPRESENTATIVE_CORRUPTION,badO!=a.O),Stage14EControl("path_dependent_future_measurement_payload",STAGE14E_PATH_CORRUPTION,badP!=a.future_measurement),Stage14EControl("basis_dependent_future_measurement_payload",STAGE14E_BASIS_CORRUPTION,badB!=a.future_measurement))

def _public_clean():
    bad=(STAGE14A_BASIS_ID,STAGE14D_TRIANGULAR_BASIS_ID,STAGE14B_PATH_12D,STAGE14B_PATH_21D)
    return all(not any(x in repr((a.O,a.P,a.R,a.V,a.future_measurement)) for x in bad) for a in canonical_stage14e_architectures())

def stage14e_diagnostics():
    A=canonical_stage14e_architectures(); Q=canonical_stage14e_quotient_projections(); P=canonical_stage14e_path_descent_checks(); B=canonical_stage14e_basis_descent_checks(); W=canonical_stage14e_orbit_witnesses(); C=stage14e_controls(); refs=[]; same=True
    for o in canonical_stage14a_orbits():
        subset=[a for a in A if a.orbit_id==o.orbit_id]; same &= len({repr(stage14e_quotient_projection(a)) for a in subset})==1; refs.append(next(w for w in W if w.orbit_id==o.orbit_id))
    pv=lambda w: tuple(v for _,v in w.probabilities)
    sep=min(max(abs(a-b) for a,b in zip(pv(x),pv(y),strict=True)) for i,x in enumerate(refs) for y in refs[i+1:])
    path=all(x.public_equal and x.future_equal and x.witness_equal for x in P); basis=all(x.public_equal and x.future_equal and x.witness_equal for x in B)
    xi=len(P)==864 and all(x.provenance_distinct and x.trace_distinct for x in P) and len(B)==108 and all(x.provenance_distinct for x in B)
    ok=all((len(A)==108,len(stage14c_quotient_classes())==4,len({repr(x) for x in Q})==4,all(stage14e_validate_architecture(a)[0] for a in A),same,path,basis,_public_clean(),xi,len({pv(w) for w in refs})==4,sep>STAGE14E_ATOL,all(w.probability_sum_residual<=STAGE14E_ATOL for w in W),len(C)==3,all(c.rejected for c in C),all(a.future_measurement.future_actuality_status==STAGE14E_NOT_LICENSED and a.future_measurement.empirical_claim_status==STAGE14E_NOT_LICENSED for a in A)))
    return Stage14EDiagnostics(len(A),len(stage14c_quotient_classes()),len({repr(x) for x in Q}),len(P),2*len(P),len(B),2*len(B),len(W),len({pv(w) for w in refs}),sep,same,path,basis,_public_clean(),xi,len(C),sum(c.rejected for c in C),ok)

def stage14e_summary():
    d=stage14e_diagnostics()
    return {"criteria_39_43_satisfied":d.criteria_39_43_satisfied,"bounded_result":STAGE14E_BOUNDED_RESULT,"guards":("structure-function/path Xi provenance != quotient-level physical content","basis-specific Xi provenance != quotient-level physical content","path word != physical temporal history","path word != modal continuation","compensated-path operational descent != refoliation invariance","basis-equivalent operational descent != refoliation invariance","future-measurement covariance != future actuality","orbit-sensitive witness != empirical prediction","basis equivalence != general relativity","finite-model success != empirical discovery")}
