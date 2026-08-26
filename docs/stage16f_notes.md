# Stage 16F Notes — Topology / Locality / Anomaly / False-Positive Controls

Status: **Stage 16F scientifically validated. Criteria 1–47 satisfied; criteria 48–50 remain pending.**

Scientific implementation head: `38559933e42111efb241b764881684b978804aec`

Corrected validation head: `217a201c3f7cf5bd9b37db31ef58cd18ef6b8525`

Authoritative PR regression:

- run #2052
- PR merge checkout `116806864f52a5bc8626cb1a82ffa859b9bac236`
- `1329 passed in 964.64s (0:16:04)`

Historical note: run #2050 reached `1 failed, 1328 passed in 628.95s (0:10:28)`; the sole failure was a Stage 16E documentation literal mismatch (`Criteria 1–44 are satisfied` vs `criteria 1–44 satisfied`). No Stage 16F scientific test failed. Commit `217a201c3f7cf5bd9b37db31ef58cd18ef6b8525` corrected only that documentation wording.

## Frozen control inventory

Stage 16F implements **20 control records** covering all **16 frozen control classifications**. All 20 are rejected/detected as intended, and all 16 required vocabulary entries are covered.

Key controls include:

- `kappa=0` structure-function removal;
- wrap-edge opening of C4, yielding an explicit local strong basis at exhibited depth **2**;
- three-site projection, recovering the validated Stage 15 one-step L1 witness at exhibited depth **1**;
- C3 radius-1 locality degeneracy;
- disconnected-component path false positive;
- support expansion, opposite-site coefficient dependence, forward-local/inverse-nonlocal maps, and the known global seed anti-L1 control;
- singular `kappa=1`, all-clocks-one cycle frame;
- smearing-sign corruption and Jacobi anomaly;
- missing/wrong-sign compensator rejection across the frozen local path family;
- cross-orbit false-positive rejection;
- incomplete four-clock relational observable rejection;
- representative/path/basis/depth-conditioned O/P/R/V corruption controls;
- numerical-only commuting false-positive rejection.

## Topology sensitivity control

The frozen evidence now distinguishes three bounded cases:

| carrier/control | exhibited local Abelianization status |
| --- | --- |
| open three-site projection | depth 1 witness recovered |
| wrap-open four-site chain | explicit depth 2 witness |
| closed C4 | no witness in the declared L0 / explicit L1 / depth<=4 / affine cyclic L1 search |

This is evidence that the tested locality cost is sensitive to opening/closing the finite graph under the declared search classes. It is **not** a theorem that topology is ontically fundamental and it is **not** a proof of universal local non-Abelianizability on the closed cycle.

## Criteria 45–47

45. Frozen topology/locality-breaking controls detect cycle opening, C3 locality degeneracy, disconnected paths, support/coefficient/inverse nonlocality, global-seed non-L1 status, and the singular cycle frame — **satisfied**.
46. Frozen algebra/path/quotient/relational false-positive controls detect smearing/Jacobi corruption, missing/wrong compensation, numerical-only commuting claims, cross-orbit paths, and incomplete relational observables — **satisfied**.
47. Typed O/P/R/V provenance-corruption controls are rejected, all 20 control records reject as intended, and all 16 required classifications are covered — **satisfied**.

## Guards

- `negative-control rejection != proof of continuum correctness`;
- `cycle opening changes graph topology != proof that topology is ontic`;
- `three-cycle L1 label != nontrivial locality evidence`;
- `locality-breaking detection != physical causal locality`;
- `constraint-algebra anomaly detection != quantum anomaly theorem`;
- `cross-orbit rejection != ontological superselection`;
- `incomplete relational rejection != ontological becoming`;
- `typed corruption detection != ontological equivalence`;
- `numerical-only commuting rejection != universal non-Abelianity`;
- `four-site constraint precursor != general relativity`;
- `repository validation != new scientific evidence`.

Bounded result:

> **Stage 16F frozen topology/locality-breaking, algebra/path anomaly, false-positive, relational, and typed-payload controls on the Stage 16 finite four-cycle carrier = all declared controls rejected as intended.**

Next: **Stage 16G — synthesis, bounded classification, and evidence-selected next gate.**
