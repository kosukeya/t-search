"""Stage 16C Dirac pair, quotient, reachability, and four-clock relational audits."""
from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
from itertools import combinations, product
import numpy as np

from .stage16_local import (
    STAGE16A_ATOL, STAGE16A_C, STAGE16A_GRID_VALUES, STAGE16A_SMEARING_PAIRS,
    Stage16PhaseSpacePoint,
    canonical_stage16a_orbits, canonical_stage16a_representatives,
    canonical_stage16a_representatives_for_orbit, canonical_stage16a_off_surface_probes,
    stage16a_constraint_gradients, stage16a_dirac_data,
)
from .stage16_paths import (
    STAGE16B_LOCAL_STEP_PAIRS, STAGE16B_REFERENCE_CYCLE_WORD,
    STAGE16B_SMEARED_PARAMETER_PAIR,
    _newton_word, stage16b_apply_word, stage16b_local_raw_endpoints,
    stage16b_apply_smeared_flow, stage16b_seed_compensate,
)

STAGE16C_ATOL=1e-10
STAGE16C_QUOTIENT_CLASSIFICATION="four_class_physical_quotient_established"
STAGE16C_ORBIT_DISCRIMINATION="full_dirac_pair_orbit_discrimination_established"
STAGE16C_REACHABILITY="presented_generator_same_orbit_atlas_connected"
STAGE16C_LOCAL_DESCENT="local_compensated_complete_relational_descent_established"
STAGE16C_SMEARED_DESCENT="smeared_compensated_complete_relational_descent_established"
STAGE16C_OMITTED_CLASSIFICATION="relational_observable_incomplete"
STAGE16C_RAW_Q_CLASSIFICATION="raw_representative_coordinate_not_complete_relational"
STAGE16C_METAPHYSICAL_CLAIM_STATUS="not_licensed"
STAGE16C_GUARDS=(
    "complete relational observable != ontological becoming by definition",
    "Dirac-invariant data + relational change != proof of eternalism",
    "same-orbit reachability != ontological identity",
    "quotient class != ontological world",
    "compensated path descent != refoliation invariance",
    "repository validation != new scientific evidence",
)

@dataclass(frozen=True,slots=True)
class Stage16COrbitSummary:
    orbit_id:str; count:int; Q_D:float; P_D:float; Q_spread:float; P_spread:float

@dataclass(frozen=True,slots=True)
class Stage16CReachabilitySpoke:
    orbit_id:str; representative_id:str; success:bool; residual:float; inverse_residual:float; max_abs_parameter:float

@dataclass(frozen=True,slots=True)
class Stage16CDiagnostics:
    representative_count:int
    strong_commutation_point_count:int
    strong_commutation_bracket_count:int
    quotient_class_count:int
    min_class_size:int
    max_class_size:int
    orbit_pair_count:int
    physically_distinct_orbit_pair_count:int
    cross_orbit_ordered_pair_count:int
    cross_orbit_rejected_count:int
    reachability_spoke_count:int
    reachability_spoke_success_count:int
    derived_same_orbit_ordered_pair_count:int
    complete_relational_evaluation_count:int
    local_path_count:int
    local_relational_comparison_count:int
    smeared_path_count:int
    smeared_relational_comparison_count:int
    omitted_clock_evaluation_count:int
    omitted_clock_group_count:int
    omitted_clock_incomplete_group_count:int
    raw_q_evaluation_count:int
    raw_q_group_count:int
    raw_q_nondescending_group_count:int
    max_dirac_bracket_residual:float
    max_same_orbit_q_spread:float
    max_same_orbit_p_spread:float
    min_orbit_pair_separation:float
    max_reachability_residual:float
    max_reachability_inverse_residual:float
    max_reachability_parameter:float
    max_complete_target_residual:float
    min_complete_relational_spread:float
    max_complete_relational_spread:float
    max_local_dirac_residual:float
    max_local_relational_residual:float
    max_smeared_dirac_residual:float
    max_smeared_relational_residual:float
    omitted_clock_spreads:tuple[float,float,float,float]
    min_raw_q_spread:float
    max_raw_q_spread:float
    strong_dirac_invariance_established:bool
    quotient_exactly_four_by_eighty_one:bool
    orbit_discrimination_established:bool
    same_orbit_reachability_established:bool
    complete_relational_established:bool
    nontrivial_relational_change_established:bool
    local_path_descent_established:bool
    smeared_path_descent_established:bool
    omitted_clock_controls_rejected:bool
    raw_q_control_rejected:bool
    criteria_25_31_satisfied:bool


def _poisson(df,dg):
    return float(sum(df[q]*dg[p]-df[p]*dg[q] for q,p in ((0,1),(2,3),(4,5),(6,7),(8,9))))

def stage16c_dirac_bracket_residuals(point:Stage16PhaseSpacePoint)->tuple[float,...]:
    grad_q=np.asarray([1.,0.,-STAGE16A_C[0],0.,-STAGE16A_C[1],0.,-STAGE16A_C[2],0.,-STAGE16A_C[3],0.])
    grad_p=np.asarray([0.,1.,0.,0.,0.,0.,0.,0.,0.,0.])
    cg=stage16a_constraint_gradients(point)
    return tuple(abs(_poisson(g,row)) for g in (grad_q,grad_p) for row in cg)

def stage16c_complete_value(Q_D:float,tau:tuple[float,float,float,float])->float:
    return float(Q_D+sum(c*t for c,t in zip(STAGE16A_C,tau,strict=True)))

@lru_cache(maxsize=1)
def stage16c_orbit_summaries()->tuple[Stage16COrbitSummary,...]:
    result=[]
    for orbit in canonical_stage16a_orbits():
        vals=[stage16a_dirac_data(r.point()) for r in canonical_stage16a_representatives_for_orbit(orbit)]
        qs=[x[0] for x in vals]; ps=[x[1] for x in vals]
        result.append(Stage16COrbitSummary(orbit.orbit_id,len(vals),float(sum(qs)/len(qs)),float(sum(ps)/len(ps)),float(max(qs)-min(qs)),float(max(ps)-min(ps))))
    return tuple(result)

@lru_cache(maxsize=1)
def canonical_stage16c_reachability_spokes()->tuple[Stage16CReachabilitySpoke,...]:
    out=[]
    word=STAGE16B_REFERENCE_CYCLE_WORD
    invword=tuple(reversed(word))
    for orbit in canonical_stage16a_orbits():
        reps=canonical_stage16a_representatives_for_orbit(orbit)
        root=next(r for r in reps if r.point().clocks()==(0.,0.,0.,0.))
        for target in reps:
            if target.representative_id==root.representative_id: continue
            ok,params,res=_newton_word(root.point(),target.point(),word)
            if ok and params is not None:
                endpoint=stage16b_apply_word(root.point(),word,params)
                residual=float(max(abs(a-b) for a,b in zip(endpoint.vector(),target.point().vector(),strict=True)))
                invparams=tuple(-x for x in reversed(params))
                back=stage16b_apply_word(target.point(),invword,invparams)
                invres=float(max(abs(a-b) for a,b in zip(back.vector(),root.point().vector(),strict=True)))
                maxp=float(max(abs(x) for x in params))
            else:
                residual=float(res); invres=float('inf'); maxp=float('inf')
            out.append(Stage16CReachabilitySpoke(orbit.orbit_id,target.representative_id,bool(ok),residual,invres,maxp))
    return tuple(out)

def _dirac_residual(a,b):
    qa,pa=stage16a_dirac_data(a); qb,pb=stage16a_dirac_data(b)
    return float(max(abs(qa-qb),abs(pa-pb)))

def _relational_grid():
    return tuple(tuple(float(x) for x in tau) for tau in product(STAGE16A_GRID_VALUES,repeat=4))

@lru_cache(maxsize=1)
def stage16c_diagnostics()->Stage16CDiagnostics:
    reps=canonical_stage16a_representatives(); off=canonical_stage16a_off_surface_probes(); points=tuple(r.point() for r in reps)+off
    bracket=[x for p in points for x in stage16c_dirac_bracket_residuals(p)]
    summaries=stage16c_orbit_summaries()
    keys={}
    for r in reps:
        q,p=stage16a_dirac_data(r.point()); key=(round(q,12),round(p,12)); keys.setdefault(key,[]).append(r)
    pairseps=[]
    for a,b in combinations(summaries,2): pairseps.append(max(abs(a.Q_D-b.Q_D),abs(a.P_D-b.P_D)))
    cross=0; rejected=0
    for a in reps:
        qa,pa=stage16a_dirac_data(a.point())
        for b in reps:
            if a.orbit_id==b.orbit_id: continue
            cross+=1; qb,pb=stage16a_dirac_data(b.point())
            if max(abs(qa-qb),abs(pa-pb))>STAGE16C_ATOL: rejected+=1
    spokes=canonical_stage16c_reachability_spokes()
    taus=_relational_grid()
    max_target=0.; spreads=[]; complete_count=0
    for orbit in canonical_stage16a_orbits():
        ors=canonical_stage16a_representatives_for_orbit(orbit); lookup={r.point().clocks():r for r in ors}
        orbit_values=[]
        for source in ors:
            qd,_=stage16a_dirac_data(source.point())
            for tau in taus:
                val=stage16c_complete_value(qd,tau); target=lookup[tau]
                max_target=max(max_target,abs(val-target.Q)); orbit_values.append(val); complete_count+=1
        spreads.append(max(orbit_values)-min(orbit_values))
    max_ld=0.; max_lr=0.; local_count=0; local_rel_count=0
    for rep in reps:
        p=rep.point()
        for i,j in ((0,1),(1,2),(2,3),(3,0)):
            for s,u in STAGE16B_LOCAL_STEP_PAIRS:
                a,b=stage16b_local_raw_endpoints(p,i,j,s,u); comp=stage16b_seed_compensate(b,a)
                max_ld=max(max_ld,_dirac_residual(a,comp)); local_count+=1
                qa,_=stage16a_dirac_data(a); qc,_=stage16a_dirac_data(comp)
                for tau in taus:
                    max_lr=max(max_lr,abs(stage16c_complete_value(qa,tau)-stage16c_complete_value(qc,tau))); local_rel_count+=1
    max_sd=0.; max_sr=0.; smeared_count=0; smeared_rel_count=0
    alpha,beta=STAGE16B_SMEARED_PARAMETER_PAIR
    for rep in reps:
        p=rep.point()
        for N,M in STAGE16A_SMEARING_PAIRS:
            a=stage16b_apply_smeared_flow(stage16b_apply_smeared_flow(p,N,alpha),M,beta)
            b=stage16b_apply_smeared_flow(stage16b_apply_smeared_flow(p,M,beta),N,alpha)
            comp=stage16b_seed_compensate(b,a)
            max_sd=max(max_sd,_dirac_residual(a,comp)); smeared_count+=1
            qa,_=stage16a_dirac_data(a); qc,_=stage16a_dirac_data(comp)
            for tau in taus:
                max_sr=max(max_sr,abs(stage16c_complete_value(qa,tau)-stage16c_complete_value(qc,tau))); smeared_rel_count+=1
    omitted_spreads=[]; omitted_groups=0; omitted_bad=0; omitted_eval=0
    for idx,c in enumerate(STAGE16A_C):
        group_spreads=[]
        for orbit in canonical_stage16a_orbits():
            vals=[]
            for r in canonical_stage16a_representatives_for_orbit(orbit):
                qd,_=stage16a_dirac_data(r.point()); val=qd+c*r.point().clocks()[idx]
                vals.append(val); omitted_eval+=1
            spread=max(vals)-min(vals); group_spreads.append(spread); omitted_groups+=1
            if spread>STAGE16C_ATOL: omitted_bad+=1
        omitted_spreads.append(min(group_spreads))
    raw_sp=[]
    for orbit in canonical_stage16a_orbits():
        vals=[r.Q for r in canonical_stage16a_representatives_for_orbit(orbit)]; raw_sp.append(max(vals)-min(vals))
    strong=max(bracket)<=STAGE16C_ATOL
    quotient=len(keys)==4 and min(len(v) for v in keys.values())==81 and max(len(v) for v in keys.values())==81
    orbitdisc=len(pairseps)==6 and min(pairseps)>STAGE16C_ATOL and rejected==cross
    reach=len(spokes)==320 and all(x.success for x in spokes) and max(x.residual for x in spokes)<=STAGE16C_ATOL and max(x.inverse_residual for x in spokes)<=STAGE16C_ATOL
    complete=max_target<=STAGE16C_ATOL; nontriv=min(spreads)>STAGE16C_ATOL
    localok=max_ld<=STAGE16C_ATOL and max_lr<=STAGE16C_ATOL
    smearedok=max_sd<=STAGE16C_ATOL and max_sr<=STAGE16C_ATOL
    omitok=omitted_bad==16; rawok=all(x>STAGE16C_ATOL for x in raw_sp)
    return Stage16CDiagnostics(
        len(reps),len(points),len(bracket),len(keys),min(len(v) for v in keys.values()),max(len(v) for v in keys.values()),
        len(pairseps),sum(x>STAGE16C_ATOL for x in pairseps),cross,rejected,len(spokes),sum(x.success for x in spokes),4*81*81,
        complete_count,local_count,local_rel_count,smeared_count,smeared_rel_count,omitted_eval,omitted_groups,omitted_bad,len(reps),4,sum(x>STAGE16C_ATOL for x in raw_sp),
        max(bracket),max(x.Q_spread for x in summaries),max(x.P_spread for x in summaries),min(pairseps),max(x.residual for x in spokes),max(x.inverse_residual for x in spokes),max(x.max_abs_parameter for x in spokes),
        max_target,min(spreads),max(spreads),max_ld,max_lr,max_sd,max_sr,tuple(float(x) for x in omitted_spreads),min(raw_sp),max(raw_sp),
        strong,quotient,orbitdisc,reach,complete,nontriv,localok,smearedok,omitok,rawok,
        strong and quotient and orbitdisc and reach and complete and nontriv and localok and smearedok and omitok and rawok,
    )
