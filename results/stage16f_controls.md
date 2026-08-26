# Stage 16F Result — Topology / Locality / Anomaly / False-Positive Controls

Scientific implementation head: `38559933e42111efb241b764881684b978804aec`

Corrected validation head: `217a201c3f7cf5bd9b37db31ef58cd18ef6b8525`

Authoritative PR regression: run #2052, merge checkout `116806864f52a5bc8626cb1a82ffa859b9bac236`, **1329 passed in 964.64s (0:16:04)**.

Historical validation note: run #2050 had **1 failed, 1328 passed in 628.95s (0:10:28)** because `docs/stage16e_notes.md` used semantically equivalent wording that did not match a literal documentation assertion. The Stage 16F scientific controls themselves passed in that run; commit `217a201c3f7cf5bd9b37db31ef58cd18ef6b8525` changed only that Stage 16E wording.

## Result

- control records: **20**;
- controls rejected/detected as intended: **20 / 20**;
- frozen required classifications: **16**;
- frozen vocabulary covered: **16 / 16**;
- wrap-open C4 local strong witness: exhibited depth **2**;
- three-site projection: validated one-step L1 witness recovered at depth **1**;
- typed O/P/R/V provenance corruption controls: **4 / 4 detected**;
- cross-orbit false-positive ordered pairs remain rejected by the Stage 16C quotient audit;
- all 16 single-clock-omission groups remain incomplete;
- all frozen local path probes reject missing and wrong-sign compensation;
- a zero-clock numerical commuting sample is rejected as a certificate of strong commutation because another off-surface sample is noncommuting.

The bounded topology comparison is therefore:

`open C3: exhibited depth 1` → `wrap-open C4: exhibited depth 2` → `closed C4: no local strong witness found in the declared Stage 16D search through depth 4 / affine cyclic L1 certificate`.

This comparison is a control on the declared finite search and locality definitions; it is not a universal obstruction theorem.

## Criteria state

**criteria 1–47 satisfied / criteria 48–50 pending**.

## Guards

`cycle opening changes graph topology != proof that topology is ontic`;
`three-cycle L1 label != nontrivial locality evidence`;
`locality-breaking detection != physical causal locality`;
`only nonlocal witness found != fundamental physical non-Abelianity`;
`failure to Abelianize != ontological becoming`;
`constraint-algebra anomaly detection != quantum anomaly theorem`;
`typed corruption detection != ontological equivalence`;
`numerical-only commuting rejection != universal non-Abelianity`;
`four-site constraint precursor != general relativity`;
`repository validation != new scientific evidence`.

Bounded result:

> **Stage 16F frozen topology/locality-breaking, algebra/path anomaly, false-positive, relational, and typed-payload controls on the Stage 16 finite four-cycle carrier = all declared controls rejected as intended.**
