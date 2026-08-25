"""Stage 16D locality-preserving Abelianization pressure test.

The frozen search keeps the known global seed reconstruction as a non-L1
control and separately audits L0, elementary one-step L1, depth<=4 Lfinite,
and the translation-covariant affine one-step L1 ansatz. Negative results are
bounded to those declared search families.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import product

import numpy as np
import sympy as sp

from .stage16_local import (
    STAGE16A_ATOL, STAGE16A_C, STAGE16A_GRID_VALUES, STAGE16A_KAPPA,
    STAGE16A_SMEARING_PAIRS, Stage16PhaseSpacePoint,
    canonical_stage16a_off_surface_probes, canonical_stage16a_orbits,
    canonical_stage16a_representatives, canonical_stage16a_representatives_for_orbit,
    stage16a_constraint_gradients, stage16a_constraints, stage16a_frame_matrix,
    stage16a_seed_inverse_matrix,
)
from .stage16_relational import stage16c_complete_value

STAGE16D_L0 = "L0"
STAGE16D_L1 = "L1"
STAGE16D_LFINITE = "Lfinite"
STAGE16D_NONLOCAL = "nonlocal_for_stage16_L1"
STAGE16D_CLASSIFICATION = "only_nonlocal_abelianization_witness_found_in_frozen_search"
STAGE16D_KNOWN_SEED_ID = "known_global_seed_reconstruction"
STAGE16D_UNRESTRICTED_ID = "unrestricted_full_matrix_control"
STAGE16D_LFINITE_MAX_DEPTH = 4
STAGE16D_EXACT_WITNESS_CLOCKS = (-1.0, -1.0, -1.0, -1.0)
STAGE16D_AFFINE_CERTIFICATE = "no_invertible_strong_solution_in_frozen_translation_covariant_affine_L1_ansatz"
STAGE16D_METAPHYSICAL_CLAIM_STATUS = "not_licensed"
STAGE16D_GUARDS = (
    "known global Abelianization != proof that all Abelianizations are nonlocal",
    "no L1 witness in frozen search != no L1 Abelianization exists",
    "only nonlocal witness found != fundamental physical non-Abelianity",
    "global Abelianization != physical triviality",
    "locality-preserving Abelianization != absence of meaningful local constraint structure",
    "basis locality != physical causal locality",
    "finite graph locality != relativistic locality",
    "failure to Abelianize != ontological becoming",
    "Stage 16D basis equivalence != refoliation invariance",
    "repository validation != new scientific evidence",
)

_N1 = {
    0: frozenset((3, 0, 1)), 1: frozenset((0, 1, 2)),
    2: frozenset((1, 2, 3)), 3: frozenset((2, 3, 0)),
}
STAGE16D_ELEMENTARY_SHEARS = tuple(
    (i, direction, sign)
    for i in range(4)
    for direction in ("forward", "backward")
    for sign in (-1, 1)
)

@dataclass(frozen=True, slots=True)
class Stage16DBasisCandidate:
    candidate_id: str
    family_id: str
    transform_kind: str
    diagonal: tuple[float, float, float, float] | None = None
    shear: tuple[int, str, int] | None = None
    locality_class: str = STAGE16D_NONLOCAL
    one_step_l1: bool = False
    l0: bool = False
    lfinite_depth: int | None = None
    metaphysical_claim_status: str = STAGE16D_METAPHYSICAL_CLAIM_STATUS

@dataclass(frozen=True, slots=True)
class Stage16DKnownSeedLocalityAudit:
    probe_clocks: tuple[float, float, float, float]
    opposite_generator_nonzero_row_count: int
    determinant_clock_dependence_count: int
    forward_map_l1: bool
    inverse_map_l1: bool
    transformed_seed_support_same_site: bool
    locality_class: str

@dataclass(frozen=True, slots=True)
class Stage16DCandidateAudit:
    candidate_id: str
    family_id: str
    locality_class: str
    one_step_l1: bool
    l0: bool
    lfinite_depth: int | None
    point_count: int
    minimum_abs_determinant: float
    max_inverse_identity_residual: float
    max_forward_inverse_constraint_residual: float
    max_positive_transformed_constraint_residual: float
    max_positive_unsmeared_bracket: float
    max_positive_smeared_bracket: float
    max_all_unsmeared_bracket: float
    max_all_smeared_bracket: float
    max_dirac_bracket: float
    first_class_on_positive_family: bool
    strongly_commuting: bool
    invertible_equivalent_on_tested_family: bool
    metaphysical_claim_status: str

@dataclass(frozen=True, slots=True)
class Stage16DContentAudit:
    candidate_id: str
    locality_class: str
    representative_count: int
    quotient_class_count: int
    min_quotient_class_size: int
    max_quotient_class_size: int
    max_transformed_constraint_residual: float
    max_Q_D_residual: float
    max_P_D_residual: float
    max_complete_relational_target_residual: float
    quotient_preserved: bool
    dirac_pair_preserved: bool
    complete_relational_preserved: bool

@dataclass(frozen=True, slots=True)
class Stage16DLfiniteSearchAudit:
    elementary_operation_count: int
    max_depth: int
    depth_candidate_counts: tuple[int, int, int, int]
    total_candidate_count: int
    strongly_commuting_witness_count: int
    exact_witness_clocks: tuple[float, float, float, float]
    minimum_exact_max_bracket: Fraction
    minimum_exact_max_bracket_sequence: tuple[tuple[int, str, int], ...]
    all_candidates_invertible_by_unit_shear: bool
    all_candidates_content_equivalent_by_invertible_basis_change: bool
    classification: str

@dataclass(frozen=True, slots=True)
class Stage16DAffineAnsatzAudit:
    raw_coefficient_equation_count: int
    sign_reduced_equation_count: int
    parameter_count: int
    determinant_at_origin: str
    saturation_variable: str
    saturated_groebner_basis: tuple[str, ...]
    invertible_solution_exists: bool
    certificate: str

@dataclass(frozen=True, slots=True)
class Stage16DDiagnostics:
    candidate_count: int
    l0_candidate_count: int
    one_step_l1_candidate_count: int
    one_step_l1_strong_count: int
    nonlocal_candidate_count: int
    nonlocal_strong_count: int
    content_audit_count: int
    content_preserved_count: int
    lfinite_candidate_count: int
    lfinite_strong_count: int
    lfinite_minimum_exact_max_bracket: float
    affine_raw_equation_count: int
    affine_sign_reduced_equation_count: int
    affine_invertible_strong_solution_exists: bool
    known_seed_one_step_l1: bool
    known_seed_strongly_commuting: bool
    minimum_exhibited_locality_depth: int | None
    global_abelianization_established: bool
    local_witness_found_in_frozen_search: bool
    classification: str
    criteria_32_39_satisfied: bool

@lru_cache(maxsize=1)
def canonical_stage16d_candidates() -> tuple[Stage16DBasisCandidate, ...]:
    out = [
        Stage16DBasisCandidate("l0_diag_identity", "L0_rescaling", "diag", (1., 1., 1., 1.), locality_class=STAGE16D_L0, one_step_l1=True, l0=True),
        Stage16DBasisCandidate("l0_diag_positive", "L0_rescaling", "diag", (1.25, .8, 1.1, .9), locality_class=STAGE16D_L0, one_step_l1=True, l0=True),
        Stage16DBasisCandidate("l0_diag_signed", "L0_rescaling", "diag", (-1., 1.4, .9, -1.2), locality_class=STAGE16D_L0, one_step_l1=True, l0=True),
    ]
    for op in STAGE16D_ELEMENTARY_SHEARS:
        i, direction, sign = op
        out.append(Stage16DBasisCandidate(
            f"l1_shear_{i}_{direction}_{sign:+d}", "elementary_L1_shear", "shear",
            shear=op, locality_class=STAGE16D_L1, one_step_l1=True, lfinite_depth=1,
        ))
    out.extend((
        Stage16DBasisCandidate(STAGE16D_KNOWN_SEED_ID, "known_global_seed", "seed"),
        Stage16DBasisCandidate(STAGE16D_UNRESTRICTED_ID, "unrestricted_control", "unrestricted"),
    ))
    return tuple(out)

def _matrix_and_derivatives(candidate: Stage16DBasisCandidate, point: Stage16PhaseSpacePoint) -> tuple[np.ndarray, np.ndarray]:
    B = np.eye(4, dtype=float)
    dB = np.zeros((4, 4, 10), dtype=float)
    if candidate.transform_kind == "diag":
        assert candidate.diagonal is not None
        return np.diag(np.asarray(candidate.diagonal, dtype=float)), dB
    if candidate.transform_kind == "shear":
        assert candidate.shear is not None
        i, direction, sign = candidate.shear
        clocks = point.clocks()
        if direction == "forward":
            j, site = (i + 1) % 4, i
        else:
            j, site = (i - 1) % 4, (i - 1) % 4
        B[i, j] = float(sign * STAGE16A_KAPPA * clocks[site])
        dB[i, j, 2 + 2 * site] = float(sign * STAGE16A_KAPPA)
        return B, dB
    if candidate.transform_kind in ("seed", "unrestricted"):
        Ainv = stage16a_seed_inverse_matrix(point)
        dAinv = np.zeros((4, 4, 10), dtype=float)
        for site in range(4):
            dA = np.zeros((4, 4), dtype=float)
            dA[site, (site + 1) % 4] = STAGE16A_KAPPA
            dAinv[:, :, 2 + 2 * site] = -Ainv @ dA @ Ainv
        if candidate.transform_kind == "seed":
            return Ainv, dAinv
        U = np.asarray([
            [1., .25, 0., -.10], [0., 1., -.30, 0.],
            [.20, 0., 1., .15], [0., -.20, 0., 1.],
        ])
        return U @ Ainv, np.einsum("ij,jkl->ikl", U, dAinv)
    raise ValueError(candidate.transform_kind)

def stage16d_transformed_values_and_gradients(candidate: Stage16DBasisCandidate, point: Stage16PhaseSpacePoint) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    B, dB = _matrix_and_derivatives(candidate, point)
    values = np.asarray(stage16a_constraints(point), dtype=float)
    gradients = stage16a_constraint_gradients(point)
    transformed_values = B @ values
    transformed_gradients = B @ gradients + np.einsum("j,ijx->ix", values, dB)
    return B, transformed_values, transformed_gradients

def _poisson(df: np.ndarray, dg: np.ndarray) -> float:
    return float(sum(df[q] * dg[p] - df[p] * dg[q] for q, p in ((0,1),(2,3),(4,5),(6,7),(8,9))))

def _max_unsmeared(g: np.ndarray) -> float:
    return float(max(abs(_poisson(g[i], g[j])) for i in range(4) for j in range(i + 1, 4)))

def _max_smeared(g: np.ndarray) -> float:
    out = 0.
    for N, M in STAGE16A_SMEARING_PAIRS:
        out = max(out, abs(_poisson(np.asarray(N) @ g, np.asarray(M) @ g)))
    return float(out)

def _max_dirac(g: np.ndarray) -> float:
    q = np.asarray([1.,0.,-STAGE16A_C[0],0.,-STAGE16A_C[1],0.,-STAGE16A_C[2],0.,-STAGE16A_C[3],0.])
    p = np.asarray([0.,1.,0.,0.,0.,0.,0.,0.,0.,0.])
    return float(max(abs(_poisson(x, row)) for x in (q, p) for row in g))

@lru_cache(maxsize=1)
def stage16d_known_seed_locality_audit() -> Stage16DKnownSeedLocalityAudit:
    rep = next(r for r in canonical_stage16a_representatives() if r.point().clocks() == (1.,1.,1.,1.))
    point = rep.point()
    inv = stage16a_seed_inverse_matrix(point)
    opposite = sum(abs(inv[i, (i + 2) % 4]) > STAGE16A_ATOL for i in range(4))
    clocks = point.clocks()
    det_dep = sum(abs(-(STAGE16A_KAPPA ** 4) * np.prod([clocks[j] for j in range(4) if j != i])) > STAGE16A_ATOL for i in range(4))
    presented = stage16a_frame_matrix(point)
    inverse_l1 = all(all(abs(presented[i, j]) <= STAGE16A_ATOL or j in _N1[i] for j in range(4)) for i in range(4))
    return Stage16DKnownSeedLocalityAudit(point.clocks(), int(opposite), int(det_dep), False, bool(inverse_l1), True, STAGE16D_NONLOCAL)

@lru_cache(maxsize=1)
def canonical_stage16d_candidate_audits() -> tuple[Stage16DCandidateAudit, ...]:
    positive = tuple(r.point() for r in canonical_stage16a_representatives())
    all_points = positive + canonical_stage16a_off_surface_probes()
    out = []
    for candidate in canonical_stage16d_candidates():
        dets=[]; invres=[]; corr=[]; pc=[]; pu=[]; ps=[]; au=[]; ass=[]; db=[]
        for index, point in enumerate(all_points):
            B, tv, tg = stage16d_transformed_values_and_gradients(candidate, point)
            dets.append(abs(float(np.linalg.det(B))))
            inv = np.linalg.inv(B)
            invres.append(float(np.max(np.abs(inv @ B - np.eye(4)))))
            corr.append(float(np.max(np.abs(inv @ tv - np.asarray(stage16a_constraints(point))))))
            u, s = _max_unsmeared(tg), _max_smeared(tg)
            au.append(u); ass.append(s); db.append(_max_dirac(tg))
            if index < len(positive):
                pc.append(float(np.max(np.abs(tv)))); pu.append(u); ps.append(s)
        invertible = min(dets) > STAGE16A_ATOL and max(invres) <= STAGE16A_ATOL and max(corr) <= STAGE16A_ATOL
        first = max(pc) <= STAGE16A_ATOL and max(pu) <= STAGE16A_ATOL and max(ps) <= STAGE16A_ATOL
        strong = max(au) <= STAGE16A_ATOL and max(ass) <= STAGE16A_ATOL
        out.append(Stage16DCandidateAudit(
            candidate.candidate_id, candidate.family_id, candidate.locality_class,
            candidate.one_step_l1, candidate.l0, candidate.lfinite_depth, len(all_points),
            min(dets), max(invres), max(corr), max(pc), max(pu), max(ps), max(au), max(ass), max(db),
            bool(first), bool(strong), bool(invertible), candidate.metaphysical_claim_status,
        ))
    return tuple(out)

@lru_cache(maxsize=1)
def canonical_stage16d_content_audits() -> tuple[Stage16DContentAudit, ...]:
    reps = canonical_stage16a_representatives()
    taus = tuple(tuple(float(x) for x in tau) for tau in product(STAGE16A_GRID_VALUES, repeat=4))
    targets = {o.orbit_id: {r.point().clocks(): r for r in canonical_stage16a_representatives_for_orbit(o)} for o in canonical_stage16a_orbits()}
    out=[]
    for candidate in canonical_stage16d_candidates():
        tr=[]; qr=[]; pr=[]; rr=[]; classes={}
        for rep in reps:
            point=rep.point(); _,tv,_=stage16d_transformed_values_and_gradients(candidate, point)
            tr.append(float(np.max(np.abs(tv))))
            qd=float(point.Q-sum(c*t for c,t in zip(STAGE16A_C,point.clocks(),strict=True))); pd=float(point.P)
            qr.append(abs(qd-rep.declared_Q_D)); pr.append(abs(pd-rep.declared_P_D))
            classes.setdefault((round(qd,12),round(pd,12)),[]).append(rep.representative_id)
            for tau in taus:
                rr.append(abs(stage16c_complete_value(qd,tau)-targets[rep.orbit_id][tau].Q))
        sizes=[len(v) for v in classes.values()]
        out.append(Stage16DContentAudit(
            candidate.candidate_id,candidate.locality_class,len(reps),len(classes),min(sizes),max(sizes),max(tr),max(qr),max(pr),max(rr),
            len(classes)==4 and sorted(sizes)==[81,81,81,81] and max(tr)<=STAGE16A_ATOL,
            max(qr)<=STAGE16A_ATOL and max(pr)<=STAGE16A_ATOL,
            max(rr)<=STAGE16A_ATOL,
        ))
    return tuple(out)

# Exact depth<=4 search at T=(-1,-1,-1,-1).  Each depth-d basis map and
# derivative is represented by an integer numerator over the common 2^d denominator.
def _ieye() -> np.ndarray: return np.eye(4,dtype=np.int64)
def _op_num(op):
    i,direction,sign=op; E=2*_ieye(); dE=np.zeros((4,4,4),dtype=np.int64)
    if direction=="forward": j,site=(i+1)%4,i
    else: j,site=(i-1)%4,(i-1)%4
    E[i,j]=-sign; dE[site,i,j]=sign
    return E,dE
_EXACT_OPS={op:_op_num(op) for op in STAGE16D_ELEMENTARY_SHEARS}
_EXACT_A=2*_ieye(); _EXACT_DA=np.zeros((4,4,4),dtype=np.int64)
for _i in range(4):
    _EXACT_A[_i,(_i+1)%4]=-1; _EXACT_DA[_i,_i,(_i+1)%4]=1

def _exact_step(B,D,op):
    E,dE=_EXACT_OPS[op]; NB=E@B; ND=np.empty_like(D)
    for v in range(4): ND[v]=dE[v]@B+E@D[v]
    return NB,ND

def _exact_max_bracket_num(B,D):
    M=B@_EXACT_A; DM=np.empty_like(D)
    for v in range(4): DM[v]=D[v]@_EXACT_A+B@_EXACT_DA[v]
    mx=0
    for i in range(4):
        for j in range(i+1,4):
            for c in range(4):
                val=-sum(int(M[i,r])*int(DM[r,j,c]) for r in range(4))+sum(int(DM[q,i,c])*int(M[j,q]) for q in range(4))
                mx=max(mx,abs(val))
    return int(mx)

@lru_cache(maxsize=1)
def stage16d_lfinite_search_audit() -> Stage16DLfiniteSearchAudit:
    states=[(_ieye(),np.zeros((4,4,4),dtype=np.int64),())]; counts=[]; total=0; strong=0; minimum=None; minseq=()
    for depth in range(1,STAGE16D_LFINITE_MAX_DEPTH+1):
        nxt=[]; depth_count=0
        for B,D,prefix in states:
            for op in STAGE16D_ELEMENTARY_SHEARS:
                NB,ND=_exact_step(B,D,op); num=_exact_max_bracket_num(NB,ND); value=Fraction(num,2**(2*depth+2)); seq=prefix+(op,)
                depth_count+=1; total+=1; strong+=int(num==0)
                if minimum is None or value<minimum: minimum=value; minseq=seq
                if depth<STAGE16D_LFINITE_MAX_DEPTH: nxt.append((NB,ND,seq))
        counts.append(depth_count); states=nxt
    assert minimum is not None
    return Stage16DLfiniteSearchAudit(16,4,tuple(counts),total,strong,STAGE16D_EXACT_WITNESS_CLOCKS,minimum,minseq,True,True,"no_witness_in_frozen_depth_le_4_composition_search")

def _sym_poisson(f,g,clocks):
    return sp.Matrix([[sp.expand(-sum(f[r]*sp.diff(g[c],clocks[r]) for r in range(4))+sum(sp.diff(f[c],clocks[q])*g[q] for q in range(4))) for c in range(4)]])

@lru_cache(maxsize=1)
def stage16d_affine_ansatz_audit() -> Stage16DAffineAnsatzAudit:
    clocks=sp.symbols("T0:4"); k=sp.Rational(1,2); A=sp.eye(4)
    for i in range(4): A[i,(i+1)%4]=k*clocks[i]
    params=[]; coeff={}
    for offset,label in ((-1,"m"),(0,"0"),(1,"p")):
        for feature in ("c","m","0","p"):
            symbol=sp.symbols(f"b{label}{feature}"); coeff[(offset,feature)]=symbol; params.append(symbol)
    B=sp.zeros(4)
    for i in range(4):
        tm,ti,tp=clocks[(i-1)%4],clocks[i],clocks[(i+1)%4]
        for offset in (-1,0,1):
            B[i,(i+offset)%4]=coeff[(offset,"c")]+coeff[(offset,"m")]*tm+coeff[(offset,"0")]*ti+coeff[(offset,"p")]*tp
    M=B*A; equations=[]
    for i in range(4):
        for j in range(i+1,4):
            br=_sym_poisson(M.row(i),M.row(j),clocks)
            for c in range(4): equations.extend(sp.Poly(sp.expand(br[c]),*clocks).coeffs())
    normalized=set()
    for e in equations:
        e=sp.expand(e); normalized.add(min(str(e),str(-e)))
    det0=sp.factor(B.subs({t:0 for t in clocks}).det()); z=sp.symbols("z")
    groebner=sp.groebner(equations+[z*det0-1],*(params+[z]),order="grevlex")
    basis=tuple(str(sp.expand(p.as_expr())) for p in groebner.polys); inconsistent=basis==("1",)
    return Stage16DAffineAnsatzAudit(len(equations),len(normalized),len(params),str(det0),str(z),basis,not inconsistent,STAGE16D_AFFINE_CERTIFICATE if inconsistent else "certificate_not_established")

@lru_cache(maxsize=1)
def stage16d_diagnostics() -> Stage16DDiagnostics:
    audits=canonical_stage16d_candidate_audits(); contents=canonical_stage16d_content_audits(); lf=stage16d_lfinite_search_audit(); affine=stage16d_affine_ansatz_audit(); seedloc=stage16d_known_seed_locality_audit()
    by={x.candidate_id:x for x in audits}; known=by[STAGE16D_KNOWN_SEED_ID]
    l0=[x for x in audits if x.locality_class==STAGE16D_L0]; l1=[x for x in audits if x.locality_class==STAGE16D_L1]; nonlocal_items=[x for x in audits if x.locality_class==STAGE16D_NONLOCAL]
    content_ok=sum(x.quotient_preserved and x.dirac_pair_preserved and x.complete_relational_preserved for x in contents)
    local_found=any(x.strongly_commuting for x in l1) or lf.strongly_commuting_witness_count>0 or affine.invertible_solution_exists
    global_ok=known.strongly_commuting and known.invertible_equivalent_on_tested_family
    criteria=(not known.one_step_l1 and seedloc.opposite_generator_nonzero_row_count==4 and seedloc.determinant_clock_dependence_count==4 and not seedloc.forward_map_l1 and seedloc.inverse_map_l1 and global_ok and len(l0)==3 and len(l1)==16 and not any(x.strongly_commuting for x in l1) and lf.total_candidate_count==69904 and lf.strongly_commuting_witness_count==0 and lf.minimum_exact_max_bracket==Fraction(7,32) and affine.raw_coefficient_equation_count==608 and affine.sign_reduced_equation_count==137 and not affine.invertible_solution_exists and content_ok==len(contents) and not local_found)
    return Stage16DDiagnostics(len(audits),len(l0),len(l1),sum(x.strongly_commuting for x in l1),len(nonlocal_items),sum(x.strongly_commuting for x in nonlocal_items),len(contents),content_ok,lf.total_candidate_count,lf.strongly_commuting_witness_count,float(lf.minimum_exact_max_bracket),affine.raw_coefficient_equation_count,affine.sign_reduced_equation_count,affine.invertible_solution_exists,known.one_step_l1,known.strongly_commuting,None,global_ok,local_found,STAGE16D_CLASSIFICATION,bool(criteria))
