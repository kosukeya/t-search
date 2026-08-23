# Stage 12C notes — typed gauge atlas, quotient, and relational descent

## Incoming checkpoint

Stage 12B is externally validated at head `b3f618c2f08a88c26c6153d768149e2ba5f1543e` by GitHub Actions run **#1528**:

`973 passed in 677.85s (0:11:17)`.

That repository regression validates the Stage 12B implementation/documentation checkpoint; it is not new scientific evidence.

## Question

Stage 12C asks whether the Stage 12A/B finite multi-orbit carrier admits a typed constraint-generated gauge atlas whose quotient:

1. identifies all and only sampled representatives of one physical orbit;
2. preserves the four physically distinct canonical orbit classes;
3. supports representative-independent Dirac and relational observables;
4. keeps typed identity loss distinct from numerical reconstructibility;
5. rejects wrong-invariant purported gauge paths;
6. never identifies a constraint orbit with a modal continuation.

The target remains finite:

`finite gauge atlas != diffeomorphism invariance`.

## Typed node roles

The atlas explicitly contains distinct node roles for:

- physical orbit;
- gauge representative;
- external parameterization;
- relational event;
- internal clock `T`;
- modal continuation `h_L/h_R`.

In particular:

`physical orbit != gauge representative != external parameterization != relational event != internal clock`.

and

`constraint orbit != modal continuation`.

## Finite gauge groupoid

For each of the four canonical physical orbits, Stage 12A supplied five sampled representatives.

Stage 12C adds every ordered same-orbit arrow, including identities:

`5 x 5 = 25` arrows per orbit,

hence **100** typed `Phi` arrows in total.

The finite sample checks:

- **20 identity arrows**;
- **100 inverse checks**;
- **500 composition checks** (`4 x 5^3`).

For representatives `r_i,r_j,r_k` on one orbit, the sampled law is

`Phi_{j->k} o Phi_{i->j} = Phi_{i->k}`

with additive gauge displacement

`delta_s(i,j) + delta_s(j,k) = delta_s(i,k)`.

No licensed constructor accepts source and target representatives with different physical-orbit identities.

`same-orbit finite groupoid != general covariance`.

## Quotient construction

The quotient is not built by grouping on the predeclared `orbit_id` field.

Instead:

1. the 20 representative ids are graph vertices;
2. typed `Phi` arrows supply adjacency;
3. connected components define candidate gauge quotient classes;
4. only after the components are formed are their declared physical-orbit identities inspected.

The frozen positive target is exactly:

- **4 quotient classes**;
- **5 representatives per class**;
- **20 representatives covered once**;
- one and only one declared physical orbit represented in each class.

Thus the quotient must implement both

`same physical orbit -> one quotient class`

and

`different physical orbit -> distinct quotient classes`.

## Descent of relational/Dirac observables

For every quotient class, Stage 12C independently recomputes `Q_D,P_D` from each member representative using Stage 12B:

`Q_D=q-pT`,

`P_D=p`.

For every frozen `tau in {-1.25,-0.25,0.75,1.50}`, it then checks representative spread of

`q(T=tau)=Q_D+P_D tau`

and

`dq/dT=P_D`.

This gives **16 quotient-level descent evaluations** (`4 classes x 4 tau values`).

A positive result means these quantities are well defined on the sampled quotient classes. It does not mean relational change disappears:

`gauge quotient != elimination of physical change`.

## Orbit-identity ablation

Criterion 29 deliberately separates two questions.

When typed orbit identity/correspondence is removed:

- typed status is **`lost`**;
- the four groups may nevertheless be numerically reconstructed from the full independently computed `(Q_D,P_D)` pair in this frozen finite family, giving numerical status **`reconstructible`**.

Therefore:

`reconstructible != typed identity preserved`

and

`typed identity lost != metaphysically irreducible`.

This is only a finite-family reconstructibility diagnostic, not a universal theorem that orbit labels are redundant.

## Wrong-invariant controls

Two purported same-orbit gauge paths are corrupted independently:

1. a `q` corruption that changes reconstructed `Q_D`;
2. a `p` corruption that changes reconstructed `P_D` and also disturbs the constrained transport/constraint diagnostics.

Both must be classified **`numerically_refuted`**.

The check recomputes the invariants from phase-space values rather than trusting stored `Q_D,P_D` fields.

## Modal-continuation separation

`h_L` and `h_R` remain typed modal continuations inherited from Stage 10/11. They are represented by separate modal nodes and are never endpoints of `Phi` arrows or ids of quotient classes.

Hence:

`constraint orbit != modal continuation`.

This typing result does not establish any metaphysical identity or non-identity beyond the declared model architecture.

## Interpretation boundary

Stage 12C can establish a finite structural conjunction:

`gauge-representative redundancy + preserved physical-orbit plurality + quotient-level relational change`.

It does **not** establish:

- general covariance;
- diffeomorphism invariance;
- refoliation invariance;
- general relativity;
- eternalism;
- absence of ontological becoming.

In particular:

`operational quotient descent != modal/ontological identity`.

## Next step

If criteria 24–31 close, Stage 12D is next:

**Stage 12D — O/P/R/V/Xi and orbit-sensitive future-measurement descent.**

That stage must prevent a trivial success in which identical measurement payloads are merely copied to every physical orbit.