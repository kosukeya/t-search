# Stage 9G Results — Synthesis and Evidence-Selected Stage 10 Gate

Status: **Stage 9 executable synthesis and final external validation completed; criteria 48–50 satisfied.**

## Synthesis result

Executable Stage 9A–F evidence selects:

`refined_layered`

The retained finite-model candidate is:

`T9_candidate=(O,P,R,V;Xi)`

with:

- `R=(R_content,R_direction,R_access)`;
- `V=(V_extension,V_semantics,V_weights)`.

The result strengthens rather than collapses the Stage 8G architecture.

## Why the candidate is retained

Stage 9E establishes typed finite-model compatibility among P/O/R_direction/V, while Stage 9F gives discriminating ablations rather than mere coexistence:

- nontrivial V multiplicity survives removal of directional R;
- directional R survives collapse to singleton QExt;
- one-bit R_content survives scrambler removal while R_direction vanishes;
- global record/direction/V survive removal of local R_access;
- V_semantics can be erased without unique reconstruction from the retained public carrier;
- V_weights can remain underdetermined on the same carrier;
- explicit P edges are reconstructible from per-node coordinates;
- event/class correspondence remains a separate typed resource;
- wrong observable-coordinate reuse is rejected.

These outcomes are jointly sufficient for the executable selector to choose `refined_layered` rather than `reduced`, `broken`, or `inconclusive`.

## R/V relation after Stage 9

The declared finite family now contains countermodels in both directions:

`nontrivial V multiplicity without R_direction`

and

`R_direction without nontrivial V multiplicity`.

Therefore mutual necessity is refuted in this family.

`finite-family bidirectional countermodels != universal R-V independence theorem`.

## Xi relation after Stage 9

Stage 9 does not establish or require a new direct `Xi_RV` value law.

The retained Xi-like resources are typed event/current-anchor, continuation-class, clock-perspective, weight, and record-observable correspondences.

`typed Xi correspondence retained != direct Xi_RV value law established`.

`no direct Xi_RV law established != no possible R-V constraint`.

## P representation after Stage 9

The tested atlas reconstructs all 108 canonical explicit P edge matrices from per-node coordinates:

`S^h_{Y<-X}=C_{h,Y} C_{h,X}^{-1}`.

However, event/class correspondence and semantic observable typing are not thereby eliminated.

`P edge reconstruction != P layer universally redundant`.

## Evidence-selected Stage 10 ranking

The completed Stage 9 gate is removed from the future ranking.

1. `full_measurement_covariance` — score **9**
2. `richer_causal_order` — score **6**
3. `parametrized_covariance_precursor` — score **5**
4. `nonideal_povm_clocks` — score **4**

Selected Stage 10 gate:

> **Construct and validate a fully typed cross-continuation future-measurement family under genuine continuation-aware clock changes.**

The selection is unique under the declared score function.

## Why this gate is selected

Stage 9D already establishes continuation-specific state, metric, directional-record observable, continuation-class, and weight covariance. Stage 9E shows the surrounding P/R/V structure is compatible, and Stage 9F shows explicit P edges are reconstructible while correspondence typing remains necessary.

`full Stage 9C future-measurement covariance remains not_established`.

Closing that boundary therefore changes one known missing operational layer at a time and is more discriminating than simultaneously changing order structure, clock ideality, or covariance class.

## Why general covariance is not selected yet

The parametrized/general-covariance precursor rises substantially in priority after Stage 9 because the finite architecture is more mature and the directional-R/V gate is now resolved in the declared family.

It remains below measurement covariance because:

`finite clock covariance != general covariance`.

A covariance/gravity extension before the known future-measurement boundary is closed would add an additional structural change before the current finite operational interface is fully pressure-tested.

Gravity/general covariance remains deferred, not discarded.

## Exit criteria

- criterion **48** — executable Stage 9 synthesis selects/refines the finite-model candidate — **satisfied**;
- criterion **49** — remaining gates are evidence-ranked and one Stage 10 gate is uniquely selected — **satisfied**;
- criterion **50** — external final full-repository regression and merge-readiness review — **satisfied externally**.

## Validation

Stage 9F documentation-synchronized current-head regression, run #1095:

**`755 passed in 348.67s (0:05:48)`**

Stage 9G source-level synthesis/gate-selection regression, run #1099:

**`765 passed in 248.81s (0:04:08)`**

source head:

`e570a2b8e08d73bfa14db87c4faa71499d28dfad`

The first Stage 9G documentation-synchronized regression, run #1117, reached **764 passing tests / 2 historical documentation failures**. The scientific suite remained green; both failures were stale Stage 7/8 assertions that still fixed the generally covariant/gravitational extension at Stage 10 after Stage 9G had evidence-selected measurement covariance for Stage 10. Those historical assertions were updated without changing the Stage 9G scientific synthesis.

The corrected documentation-synchronized head then passed the complete repository suite in GitHub Actions run #1121:

**`766 passed in 459.00s (0:07:38)`**

validated branch head:

`1bcdc83a9dd5261f3d0de8d152534afda89667d7`

validated PR merge-ref:

`b53906446fd6970e3cfb03f110690ea9b5ce97b2`

At that reviewed checkpoint, the Stage 9 branch was ahead of `main` and **behind by 0 commits**, PR #10 was `mergeable=true`, and there were **no unresolved review threads and no submitted reviews**. A repository search also found no TODO/FIXME/HACK markers or obvious credential/absolute-path artifacts in the reviewed Stage 9 repository content.

Criterion 50 is therefore closed as an **external merge-readiness condition**, not as an additional executable scientific criterion. Closing it adds no new scientific claim.

## Final validation interpretation

The external criterion confirms that the already-synthesized Stage 9 evidence is documentation-synchronized, regression-clean, based on the current `main`, mergeable at the reviewed checkpoint, and free of known review blockers. It does not upgrade any `not_established` scientific relation.

In particular:

- `full Stage 9C future-measurement covariance remains not_established`;
- `finite-family bidirectional countermodels != universal R-V independence theorem`;
- `finite clock covariance != general covariance`;
- `refined layered candidate != fundamental ontology`.

## Unresolved implications

Still not established:

- finite-family R_direction/V separation => universal R-V independence;
- record-defined direction => ontological future openness;
- record-defined direction => ontological becoming;
- selected-vs-unselected V_semantics as an empirical fact about nature;
- Potentiality => phenomenal passage;
- physical clock change => temporal succession;
- finite clock covariance => general covariance;
- full Stage 9C future-measurement-family covariance;
- a direct Xi_RV value law;
- universal redundancy of P from edge reconstruction;
- fundamental or unique status of the refined O/P/R/V/Xi candidate.

`not_established != false`.

## Strongest bounded statement

**Within the declared finite constrained Stage 9 family, executable compatibility, transport, modal, and ablation evidence favors retaining the refined layered candidate `T=(O,P,R,V;Xi)`. Directional R and nontrivial V coexist and are not mutually necessary in the tested family; R and V subroles display distinct functional behavior; explicit P edge matrices are reconstructible while semantic correspondence remains explicit; and no new direct Xi_RV value law is established. The strongest remaining operational boundary is full cross-continuation future-measurement-family covariance, which is selected as the Stage 10 gate. The final external regression and merge-readiness review closes criterion 50 without adding a scientific claim. These results do not establish universal R-V independence, ontic future openness, ontological becoming, general covariance, or a fundamental ontology of time.**
