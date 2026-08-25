"""Stage 16B finite local/smeared/cycle path defects and compensation audits."""
from __future__ import annotations
from dataclasses import dataclass
from functools import lru_cache
from itertools import permutations
import math
import numpy as np

from .stage16_local import (
    STAGE16A_ATOL, STAGE16A_C, STAGE16A_KAPPA,
    STAGE16A_ADJACENT_FORWARD_EDGES, STAGE16A_OPPOSITE_PAIRS,
    STAGE16A_SMEARING_PAIRS,
    Stage16PhaseSpacePoint, Stage16Representative,
    canonical_stage16a_representatives,
    stage16a_constraints, stage16a_dirac_data, stage16a_frame_matrix,
    stage16a_generator_vectors,
)

STAGE16B_ATOL = 1e-10
STAGE16B_LOCAL_STEP_PAIRS = ((0.5,0.5),(-0.5,0.5))
STAGE16B_PRESENTED_WORDS = tuple(permutations(range(4)))
STAGE16B_PARAMETER_BOUND = 2.0
STAGE16B_ENDPOINT_TOL = 1e-10
STAGE16B_SMEARED_PARAMETER_PAIR = (0.5,0.5)
STAGE16B_CYCLE_PARAMETER = 0.25
STAGE16B_REFERENCE_CYCLE_WORD = (0,1,2,3)
STAGE16B_SEED_COMPENSATION_KIND = "global_seed_oracle"
STAGE16B_PRESENTED_COMPENSATION_KIND = "presented_C_word_search"
STAGE16B_PRESENTED_SEARCH_ALL_FOUND = "presented_C_compensator_found_for_all_frozen_local_probes"
STAGE16B_PRESENTED_SEARCH_PARTIAL = "presented_C_compensator_search_partial_on_frozen_local_probes"
STAGE16B_PRESENTED_SEARCH_NONE = "presented_C_compensator_not_found_in_frozen_word_search"
STAGE16B_INTERPRETATION_GUARDS = (
    "raw path-word inequality != physical path dependence",
    "seed-compensated closure != local presented-basis compensation",
    "presented compensator found != locality-preserving Abelianizing basis",
    "presented compensator not found in frozen word search != physical obstruction",
    "compensated cycle path closure != refoliation invariance",
    "cycle path defect != spacetime curvature",
    "finite constant smearing != continuum lapse/shift field",
    "Stage 16B path compensation != Stage 16D basis Abelianization",
    "repository validation != new scientific evidence",
)

@dataclass(frozen=True, slots=True)
class Stage16BLocalProbe:
    representative_id: str
    edge: tuple[int,int]
    s: float
    u: float
    observed_defect: float
    predicted_defect: float
    off_axis_residual: float
    seed_compensated_residual: float
    payload_residual: float
    presented_success: bool
    presented_word: tuple[int,int,int,int] | None
    presented_parameters: tuple[float,float,float,float] | None
    presented_residual: float
    presented_attempt_count: int
    missing_residual: float
    wrong_sign_residual: float

@dataclass(frozen=True, slots=True)
class Stage16BSmearedProbe:
    representative_id: str
    pair_index: int
    raw_endpoint_residual: float
    seed_compensated_residual: float
    payload_residual: float
    zero_wedge_control: bool

@dataclass(frozen=True, slots=True)
class Stage16BCycleProbe:
    representative_id: str
    word: tuple[int,int,int,int]
    raw_endpoint_residual: float
    seed_compensated_residual: float
    payload_residual: float

@dataclass(frozen=True, slots=True)
class Stage16BDiagnostics:
    representative_count: int
    local_probe_count: int
    local_nonzero_defect_count: int
    opposite_commuting_probe_count: int
    presented_search_success_count: int
    presented_search_failure_count: int
    presented_search_max_attempt_count: int
    smeared_probe_count: int
    smeared_nonzero_defect_count: int
    smeared_zero_defect_count: int
    cycle_probe_count: int
    cycle_nonzero_word_count: int
    single_local_oracle_probe_count: int
    single_smeared_oracle_probe_count: int
    max_local_prediction_residual: float
    max_local_off_axis_residual: float
    max_seed_compensated_local_residual: float
    max_presented_compensated_local_residual: float
    max_local_payload_residual: float
    max_single_local_oracle_residual: float
    max_single_smeared_oracle_residual: float
    max_presented_compensator_oracle_residual: float
    max_smeared_order_oracle_residual: float
    max_abs_presented_parameter: float
    max_smeared_seed_compensated_residual: float
    max_smeared_payload_residual: float
    max_cycle_seed_compensated_residual: float
    max_cycle_payload_residual: float
    min_missing_compensator_residual: float
    min_wrong_sign_compensator_residual: float
    exact_local_flows_established: bool
    local_defect_prediction_established: bool
    seed_compensation_established: bool
    presented_search_executed: bool
    exact_smeared_flow_established: bool
    smeared_compensation_established: bool
    controls_rejected: bool
    criteria_18_24_satisfied: bool
    presented_search_classification: str


def _constraint_residual(point):
    return max(abs(x) for x in stage16a_constraints(point))

def _require_on_surface(point):
    if _constraint_residual(point)>STAGE16B_ATOL:
        raise ValueError('Stage 16B finite flow formulas require an on-surface source')

def _point_with_clocks(source, clocks):
    QD,PD=stage16a_dirac_data(source)
    q=QD+sum(c*t for c,t in zip(STAGE16A_C,clocks,strict=True))
    return Stage16PhaseSpacePoint(q,PD, clocks[0],-STAGE16A_C[0]*PD,
                                  clocks[1],-STAGE16A_C[1]*PD,
                                  clocks[2],-STAGE16A_C[2]*PD,
                                  clocks[3],-STAGE16A_C[3]*PD)

def _clock_residual(a,b):
    return float(max(abs(x-y) for x,y in zip(a.clocks(),b.clocks(),strict=True)))

def _phase_residual(a,b):
    return float(max(abs(x-y) for x,y in zip(a.vector(),b.vector(),strict=True)))

def _payload_residual(a,b):
    qa,pa=stage16a_dirac_data(a); qb,pb=stage16a_dirac_data(b)
    return float(max(abs(qa-qb),abs(pa-pb)))

def stage16b_apply_local_flow(point, generator_index, parameter):
    _require_on_surface(point)
    clocks=list(point.clocks()); i=int(generator_index); j=(i+1)%4; s=float(parameter)
    old=clocks[i]
    clocks[i]=old+s
    clocks[j]=clocks[j]+STAGE16A_KAPPA*(old*s+0.5*s*s)
    return _point_with_clocks(point, tuple(clocks))

def stage16b_apply_seed_flow(point, seed_index, parameter):
    _require_on_surface(point)
    clocks=list(point.clocks()); clocks[int(seed_index)]+=float(parameter)
    return _point_with_clocks(point, tuple(clocks))

def stage16b_apply_word(point, word, parameters):
    out=point
    for g,p in zip(word,parameters,strict=True): out=stage16b_apply_local_flow(out,g,p)
    return out

def stage16b_local_raw_endpoints(point,i,j,s,u):
    a=stage16b_apply_local_flow(stage16b_apply_local_flow(point,i,s),j,u)
    b=stage16b_apply_local_flow(stage16b_apply_local_flow(point,j,u),i,s)
    return a,b

def stage16b_predicted_adjacent_defect(point,i,s,u):
    return float((STAGE16A_KAPPA**2)*u*(point.clocks()[i]*s+0.5*s*s))

def stage16b_seed_compensate(source,target):
    out=source
    for i,(a,b) in enumerate(zip(source.clocks(),target.clocks(),strict=True)):
        out=stage16b_apply_seed_flow(out,i,b-a)
    return out

# matrix exponential via scaling/squaring Taylor; deterministic and independent of ODE oracle
def _matrix_exponential(matrix):
    A=np.asarray(matrix,dtype=float)
    norm=float(np.linalg.norm(A,ord=np.inf))
    scale=0 if norm<=0.5 else int(math.ceil(math.log2(norm/0.5)))
    B=A/(2**scale)
    result=np.eye(A.shape[0]); term=np.eye(A.shape[0])
    for k in range(1,80):
        term=(term@B)/float(k); result=result+term
        if np.linalg.norm(term,ord=np.inf)<1e-17: break
    for _ in range(scale): result=result@result
    return result

@lru_cache(maxsize=None)
def _smeared_affine_map(smearing, parameter):
    N=np.asarray(smearing,dtype=float); B=np.zeros((4,4),dtype=float)
    for i in range(4): B[(i+1)%4,i]=STAGE16A_KAPPA*N[i]
    aug=np.zeros((5,5),dtype=float); aug[:4,:4]=B; aug[:4,4]=N
    return _matrix_exponential(float(parameter)*aug)

def stage16b_apply_smeared_flow(point,smearing,parameter):
    _require_on_surface(point)
    smearing=tuple(float(x) for x in smearing)
    vec=np.concatenate([np.asarray(point.clocks(),dtype=float),[1.0]])
    clocks=(_smeared_affine_map(smearing,float(parameter))@vec)[:4]
    return _point_with_clocks(point, tuple(float(x) for x in clocks))

def _full_vector(point,weights):
    gens=stage16a_generator_vectors(point)
    return np.asarray(weights,dtype=float)@gens

def _point_from_vector(v):
    return Stage16PhaseSpacePoint(*[float(x) for x in v])

def stage16b_direct_ode_oracle(point,weights,parameter,steps=32):
    v=point.vector().astype(float); h=float(parameter)/steps
    for _ in range(steps):
        p1=_point_from_vector(v); k1=_full_vector(p1,weights)
        p2=_point_from_vector(v+0.5*h*k1); k2=_full_vector(p2,weights)
        p3=_point_from_vector(v+0.5*h*k2); k3=_full_vector(p3,weights)
        p4=_point_from_vector(v+h*k3); k4=_full_vector(p4,weights)
        v=v+(h/6.0)*(k1+2*k2+2*k3+k4)
    return _point_from_vector(v)

def stage16b_local_oracle(point,i,parameter):
    w=np.zeros(4); w[i]=1.0
    return stage16b_direct_ode_oracle(point,tuple(w),parameter,steps=8)

def _newton_word(start,target,word):
    delta=np.asarray(target.clocks())-np.asarray(start.clocks())
    V=stage16a_frame_matrix(start).T
    by_label=np.linalg.solve(V,delta)
    x=np.asarray([by_label[g] for g in word],dtype=float)
    x=np.clip(x,-STAGE16B_PARAMETER_BOUND,STAGE16B_PARAMETER_BOUND)
    def f(z):
        out=stage16b_apply_word(start,word,tuple(float(q) for q in z))
        return np.asarray(out.clocks())-np.asarray(target.clocks())
    for _ in range(15):
        y=f(x)
        if np.linalg.norm(y,ord=np.inf)<=STAGE16B_ENDPOINT_TOL:
            return True,tuple(float(q) for q in x),float(np.linalg.norm(y,ord=np.inf))
        J=np.zeros((4,4)); eps=1e-7
        for c in range(4):
            xp=x.copy(); xm=x.copy(); xp[c]+=eps; xm[c]-=eps
            J[:,c]=(f(xp)-f(xm))/(2*eps)
        try: step=np.linalg.solve(J,-y)
        except np.linalg.LinAlgError: return False,None,float(np.linalg.norm(y,ord=np.inf))
        accepted=False
        for fac in (1.0,0.5,0.25,0.125,0.0625):
            trial=x+fac*step
            if np.any(np.abs(trial)>STAGE16B_PARAMETER_BOUND): continue
            if np.linalg.norm(f(trial),ord=np.inf)<np.linalg.norm(y,ord=np.inf):
                x=trial; accepted=True; break
        if not accepted: return False,None,float(np.linalg.norm(y,ord=np.inf))
    y=f(x); return np.linalg.norm(y,ord=np.inf)<=STAGE16B_ENDPOINT_TOL, tuple(float(q) for q in x), float(np.linalg.norm(y,ord=np.inf))

def stage16b_presented_search_classification(success_count: int, total_count: int) -> str:
    if success_count == total_count:
        return STAGE16B_PRESENTED_SEARCH_ALL_FOUND
    if success_count == 0:
        return STAGE16B_PRESENTED_SEARCH_NONE
    return STAGE16B_PRESENTED_SEARCH_PARTIAL

def stage16b_presented_compensator_search(start,target):
    best=float('inf')
    for attempt,word in enumerate(STAGE16B_PRESENTED_WORDS,1):
        ok,params,res=_newton_word(start,target,word); best=min(best,res)
        if ok:
            return True,word,params,res,attempt
    return False,None,None,best,len(STAGE16B_PRESENTED_WORDS)

@lru_cache(maxsize=1)
def canonical_stage16b_local_probes():
    out=[]
    for rep in canonical_stage16a_representatives():
      p=rep.point()
      for i,j in STAGE16A_ADJACENT_FORWARD_EDGES:
       for s,u in STAGE16B_LOCAL_STEP_PAIRS:
        a,b=stage16b_local_raw_endpoints(p,i,j,s,u)
        k=(i+2)%4
        observed=a.clocks()[k]-b.clocks()[k]
        predicted=stage16b_predicted_adjacent_defect(p,i,s,u)
        off=max(abs((a.clocks()[q]-b.clocks()[q])) for q in range(4) if q!=k)
        seed=stage16b_apply_seed_flow(b,k,observed)
        ok,word,params,res,attempts=stage16b_presented_compensator_search(b,a)
        if ok and word is not None and params is not None:
            presented_endpoint=stage16b_apply_word(b,word,params)
            res=_phase_residual(presented_endpoint,a)
        miss=_clock_residual(b,a)
        wrong=_clock_residual(stage16b_apply_seed_flow(b,k,-observed),a)
        out.append(Stage16BLocalProbe(rep.representative_id,(i,j),s,u,observed,predicted,off,
             _phase_residual(seed,a),_payload_residual(seed,a),ok,word,params,res,attempts,miss,wrong))
    return tuple(out)

@lru_cache(maxsize=1)
def canonical_stage16b_smeared_probes():
    out=[]; alpha,beta=STAGE16B_SMEARED_PARAMETER_PAIR
    for rep in canonical_stage16a_representatives():
      p=rep.point()
      for idx,(N,M) in enumerate(STAGE16A_SMEARING_PAIRS):
        a=stage16b_apply_smeared_flow(stage16b_apply_smeared_flow(p,N,alpha),M,beta)
        b=stage16b_apply_smeared_flow(stage16b_apply_smeared_flow(p,M,beta),N,alpha)
        seed=stage16b_seed_compensate(b,a)
        zero=all(abs(N[q]*M[(q+1)%4]-N[(q+1)%4]*M[q])<=STAGE16B_ATOL for q in range(4))
        out.append(Stage16BSmearedProbe(rep.representative_id,idx,_clock_residual(a,b),_phase_residual(seed,a),_payload_residual(seed,a),zero))
    return tuple(out)

@lru_cache(maxsize=1)
def canonical_stage16b_cycle_probes():
    out=[]
    params=(STAGE16B_CYCLE_PARAMETER,)*4
    for rep in canonical_stage16a_representatives():
      p=rep.point(); ref=stage16b_apply_word(p,STAGE16B_REFERENCE_CYCLE_WORD,params)
      for word in STAGE16B_PRESENTED_WORDS:
        raw=stage16b_apply_word(p,word,params); seed=stage16b_seed_compensate(raw,ref)
        out.append(Stage16BCycleProbe(rep.representative_id,word,_clock_residual(raw,ref),_phase_residual(seed,ref),_payload_residual(seed,ref)))
    return tuple(out)

@lru_cache(maxsize=1)
def stage16b_diagnostics():
    reps=canonical_stage16a_representatives(); local=canonical_stage16b_local_probes(); smeared=canonical_stage16b_smeared_probes(); cycle=canonical_stage16b_cycle_probes()
    opposite=0
    for rep in reps:
      for i,j in STAGE16A_OPPOSITE_PAIRS:
       for s,u in STAGE16B_LOCAL_STEP_PAIRS:
        a,b=stage16b_local_raw_endpoints(rep.point(),i,j,s,u)
        if _phase_residual(a,b)<=STAGE16B_ATOL: opposite+=1
    oracle_reps=tuple(reps[orbit*81+offset] for orbit in range(4) for offset in (0,40,80))
    local_oracle=[]
    for rep in oracle_reps:
      for i in range(4):
       for par in (-0.5,0.5):
        exact=stage16b_apply_local_flow(rep.point(),i,par); oracle=stage16b_local_oracle(rep.point(),i,par)
        local_oracle.append(_phase_residual(exact,oracle))
    unique=[]
    for pair in STAGE16A_SMEARING_PAIRS:
      for N in pair:
       if N not in unique: unique.append(N)
    smeared_oracle=[]
    for rep in oracle_reps:
      for N in unique:
        exact=stage16b_apply_smeared_flow(rep.point(),N,0.5); oracle=stage16b_direct_ode_oracle(rep.point(),N,0.5,steps=48)
        smeared_oracle.append(_phase_residual(exact,oracle))
    # Independently validate composed presented compensators on the deterministic oracle subset.
    local_lookup={(q.representative_id,q.edge,q.s,q.u):q for q in local}
    presented_oracle=[]
    for rep in oracle_reps:
      p=rep.point()
      for i,j in STAGE16A_ADJACENT_FORWARD_EDGES:
       for s0,u in STAGE16B_LOCAL_STEP_PAIRS:
        q=local_lookup[(rep.representative_id,(i,j),s0,u)]
        a,b=stage16b_local_raw_endpoints(p,i,j,s0,u)
        if not q.presented_success or q.presented_word is None or q.presented_parameters is None:
            presented_oracle.append(float("inf"))
            continue
        out=b
        for g,par in zip(q.presented_word,q.presented_parameters,strict=True):
            weights=[0.0]*4; weights[g]=1.0
            out=stage16b_direct_ode_oracle(out,tuple(weights),par,steps=8)
        presented_oracle.append(_phase_residual(out,a))

    # Independently validate finite smeared ordering defects on the same oracle subset.
    smeared_order_oracle=[]
    alpha,beta=STAGE16B_SMEARED_PARAMETER_PAIR
    for rep in oracle_reps:
      p=rep.point()
      for N,M in STAGE16A_SMEARING_PAIRS:
        exact_a=stage16b_apply_smeared_flow(stage16b_apply_smeared_flow(p,N,alpha),M,beta)
        exact_b=stage16b_apply_smeared_flow(stage16b_apply_smeared_flow(p,M,beta),N,alpha)
        ode_a=stage16b_direct_ode_oracle(stage16b_direct_ode_oracle(p,N,alpha,steps=48),M,beta,steps=48)
        ode_b=stage16b_direct_ode_oracle(stage16b_direct_ode_oracle(p,M,beta,steps=48),N,alpha,steps=48)
        exact_delta=np.asarray(exact_a.clocks())-np.asarray(exact_b.clocks())
        ode_delta=np.asarray(ode_a.clocks())-np.asarray(ode_b.clocks())
        smeared_order_oracle.append(float(np.linalg.norm(exact_delta-ode_delta,ord=np.inf)))

    nonzero_s=sum(p.raw_endpoint_residual>STAGE16B_ATOL for p in smeared)
    zero_s=len(smeared)-nonzero_s
    success=sum(p.presented_success for p in local)
    return Stage16BDiagnostics(
      len(reps),len(local),sum(abs(p.observed_defect)>STAGE16B_ATOL for p in local),opposite,
      success,len(local)-success,max(p.presented_attempt_count for p in local),
      len(smeared),nonzero_s,zero_s,len(cycle),sum(p.raw_endpoint_residual>STAGE16B_ATOL for p in cycle),
      len(local_oracle),len(smeared_oracle),
      max(abs(p.observed_defect-p.predicted_defect) for p in local),max(p.off_axis_residual for p in local),
      max(p.seed_compensated_residual for p in local),max(p.presented_residual for p in local),max(p.payload_residual for p in local),
      max(local_oracle),max(smeared_oracle),max(presented_oracle),max(smeared_order_oracle),
      max((max(abs(x) for x in p.presented_parameters) for p in local if p.presented_parameters is not None), default=0.0),
      max(p.seed_compensated_residual for p in smeared),max(p.payload_residual for p in smeared),
      max(p.seed_compensated_residual for p in cycle),max(p.payload_residual for p in cycle),
      min(p.missing_residual for p in local),min(p.wrong_sign_residual for p in local),
      max(local_oracle)<=STAGE16B_ENDPOINT_TOL,
      max(abs(p.observed_defect-p.predicted_defect) for p in local)<=STAGE16B_ENDPOINT_TOL and max(p.off_axis_residual for p in local)<=STAGE16B_ENDPOINT_TOL,
      max(p.seed_compensated_residual for p in local)<=STAGE16B_ENDPOINT_TOL,
      success+len(local)-success==len(local) and all(p.presented_attempt_count<=24 for p in local),
      max(smeared_oracle)<=STAGE16B_ENDPOINT_TOL and max(smeared_order_oracle)<=STAGE16B_ENDPOINT_TOL,
      max(p.seed_compensated_residual for p in smeared)<=STAGE16B_ENDPOINT_TOL,
      min(p.missing_residual for p in local)>STAGE16B_ENDPOINT_TOL and min(p.wrong_sign_residual for p in local)>STAGE16B_ENDPOINT_TOL,
      (max(local_oracle)<=STAGE16B_ENDPOINT_TOL
       and max(abs(p.observed_defect-p.predicted_defect) for p in local)<=STAGE16B_ENDPOINT_TOL
       and max(p.seed_compensated_residual for p in local)<=STAGE16B_ENDPOINT_TOL
       and success==len(local) and max(p.presented_residual for p in local)<=STAGE16B_ENDPOINT_TOL
       and max(presented_oracle)<=STAGE16B_ENDPOINT_TOL
       and max(smeared_oracle)<=STAGE16B_ENDPOINT_TOL
       and max(smeared_order_oracle)<=STAGE16B_ENDPOINT_TOL
       and max(p.seed_compensated_residual for p in smeared)<=STAGE16B_ENDPOINT_TOL
       and min(p.missing_residual for p in local)>STAGE16B_ENDPOINT_TOL
       and min(p.wrong_sign_residual for p in local)>STAGE16B_ENDPOINT_TOL),
      stage16b_presented_search_classification(success, len(local)))