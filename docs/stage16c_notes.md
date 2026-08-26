# Stage 16C Notes — Dirac Pair, Four-Clock Relational Observables, Quotient, and Reachability

Status: **Stage 16C scientifically validated. Criteria 1–31 are satisfied; criteria 32–50 remain pending.**

Scientific checkpoint:

`04deb0ae259cee8cf40ec606b77d2972f5c0ab17`

Authoritative PR regression:

- run #2028
- PR merge checkout `3c488d6d4dab310a423d30dcd255c7c626377a4e`
- `1299 passed in 922.38s (0:15:22)`

## Scope

Stage 16C consumes the validated four-site cyclic carrier from Stage 16A and the path/compensation atlas from Stage 16B. It closes only the relational/quotient questions frozen as criteria 25–31:

- strong Dirac invariance of `Q_D,P_D`;
- exact sampled quotient `4 x 81`;
- all six physical-orbit pair discriminations;
- same-orbit reachability under the presented-`C` generator atlas;
- exhaustive four-clock complete relational observable evaluation;
- local/smeared compensated path descent of Dirac and complete-relational content;
- rejection of all omitted-clock controls and raw `Q`.

Stage 16C does **not** perform the Stage 16D locality-preserving Abelianization search.

## Dirac pair

The frozen pair is

`P_D=P`

and

`Q_D=Q-sum_i c_i T_i`.

Across 324 positive representatives plus 324 deterministic off-surface probes, both functions are checked against all four presented constraints. This gives

`648 points x 2 Dirac functions x 4 constraints = 5,184`

strong-commutation checks, with maximum residual `0.0`.

The finite sampled quotient is exactly four classes of 81 representatives.

All 6/6 orbit pairs are separated by the full Dirac pair. The minimum full-pair separation is `0.5`.

All `78,732` ordered cross-orbit representative pairs are rejected as same-class candidates.

## Presented-generator reachability

For each physical orbit, the representative with clocks `(0,0,0,0)` is used as a root. The frozen presented word `(0,1,2,3)` is solved to each of the other 80 representatives, and the inverse flow is independently checked.

- nonidentity root spokes: `320/320`;
- maximum forward endpoint residual: `5.55e-16`;
- maximum inverse-flow residual: `4.44e-16`;
- maximum absolute solved parameter: `1.3906053272633412 < 2`.

Thus each of the four 81-node representative classes is connected under the declared presented-generator atlas. Connectivity yields

`4 x 81^2 = 26,244`

ordered same-orbit reachable pairs.

This count is **derived from the verified star atlases and inverse flows**. It is not a claim that all 26,244 ordered pairs were independently root-solved.

`same-orbit reachability != ontological identity`.

## Complete four-clock relational observable

The complete observable is

`Q(tau_0,tau_1,tau_2,tau_3)=Q_D+sum_i c_i tau_i`.

Every one of the 324 source representatives is evaluated at all 81 frozen target clock quadruples:

`324 x 81 = 26,244` evaluations.

Maximum canonical-target residual is `2.22e-16`.

The relational spread is `5.0` on each orbit, so representative-independent Dirac data coexist with nontrivial relational change.

`complete relational observable != ontological becoming by definition`.

`Dirac-invariant data + relational change != proof of eternalism`.

## Local and smeared path descent

For all 2,592 Stage 16B local path probes, the complete relational observable is compared over all 81 frozen target clock quadruples:

`2,592 x 81 = 209,952` local relational comparisons.

Maximum residuals are:

- Dirac-pair descent: `2.22e-16`;
- complete-relational descent: `2.22e-16`.

The same audit is applied to all 2,592 Stage 16B smeared ordering probes:

`2,592 x 81 = 209,952` smeared relational comparisons.

Maximum residuals are:

- Dirac-pair descent: `8.88e-16`;
- complete-relational descent: `8.88e-16`.

`compensated path descent != refoliation invariance`.

## Incomplete controls

All four one-clock omissions are tested.

- omitted-clock evaluations: `1,296`;
- orbit/omission groups: `16`;
- incomplete groups: `16 / 16`;
- minimum residual representative spreads by omitted clock: approximately `(2.0, 1.0, 0.5, 1.5)`.

Raw `Q` is also grouped by physical orbit and fails quotient descent in `4 / 4` groups, with spread `5.0`.

The bounded negative result is therefore explicit:

`relational_observable_incomplete`

for every single-clock omission, while raw `Q` remains a representative coordinate rather than a complete quotient observable.

## Criteria 25–31

25. `Q_D,P_D` strong Dirac invariance — **satisfied**.
26. Exactly four quotient classes of 81 representatives — **satisfied**.
27. All six physical-orbit pairs separated — **satisfied**.
28. Same-orbit reachability/path connectivity under the declared presented-generator atlas — **satisfied**.
29. Exhaustive four-clock complete relational observable with nontrivial relational change — **satisfied**.
30. Local/smeared path descent of Dirac and complete-relational content where licensed — **satisfied**.
31. Omitted-clock/raw-coordinate controls rejected and Stage 16C documentation synchronized — **satisfied**.

Stage 16 protocol state after this checkpoint:

**criteria 1–31 satisfied / criteria 32–50 pending**.

Next stage:

**Stage 16D — locality-preserving Abelianization pressure test and minimal exhibited locality depth.**

## Interpretation boundary

Persistent guards:

- `complete relational observable != ontological becoming by definition`;
- `Dirac-invariant data + relational change != proof of eternalism`;
- `same-orbit reachability != ontological identity`;
- `quotient class != ontological world`;
- `compensated path descent != refoliation invariance`;
- `Stage 16C relational descent != Stage 16D basis Abelianization`;
- `repository validation != new scientific evidence`.

Bounded result:

> **Stage 16C Dirac pair, four-clock complete relational observables, physical quotient, reachability, and orbit discrimination = established.**
