# Stage 9G Notes — Synthesis and Evidence-Selected Stage 10 Gate

Status: **Stage 9G synthesis and final Stage 9 external validation are completed; criteria 48–50 are closed.**

## 1. Input evidence

Stage 9G introduces no new physical carrier. It synthesizes the executable Stage 9A–F evidence:

- Stage 9A: common constrained `QExt(e1)={h_L,h_R}` with nonzero per-continuation directional R;
- Stage 9B: forward/reversed/balanced/no-record directional controls;
- Stage 9C: selected-vs-unselected modal underdetermination on the same directional carrier;
- Stage 9D: continuation-aware clock transport with typed record/class/weight covariance;
- Stage 9E: P/O/R_direction/V compatibility classification;
- Stage 9F: ablation/reconstruction/accessibility matrix.

The Stage 9F documentation-synchronized current-head regression completed in run #1095:

**`755 passed in 348.67s`**.

## 2. Executable synthesis choice

`select_synthesis_choice()` returns:

`refined_layered`

The retained finite-model candidate is:

`T9_candidate=(O,P,R,V;Xi)`

with:

`R=(R_content,R_direction,R_access)`

`V=(V_extension,V_semantics,V_weights)`.

This choice requires all of the following executable evidence simultaneously:

1. positive P/O/R_direction/V structural compatibility;
2. separation of `R_content`, `R_direction`, and `R_access` under Stage 9F ablations;
3. separation of `V_extension`, `V_semantics`, and `V_weights` by loss/reconstruction/underdetermination behavior;
4. finite-family countermodels in both directions between directional R and nontrivial V multiplicity;
5. reconstruction of explicit P edge matrices from per-node coordinates;
6. continued necessity of explicit event/class/observable typing after the P-edge reconstruction;
7. rejection of wrongly typed record-observable coordinate reuse.

If these conditions were not jointly satisfied, the synthesis would fall to `broken`, `reduced`, or `inconclusive` rather than selecting `refined_layered` by declaration.

## 3. What Stage 9 adds to the layered candidate

Stage 8G retained the layered candidate while directional R and nontrivial V had not yet been integrated in one continuation family.

Stage 9 closes that specific gap and then pressure-tests it.

The strongest new finite-family evidence is not merely coexistence. Stage 9F supplies:

- nontrivial V multiplicity without directional R;
- directional R without nontrivial V multiplicity;
- record content without directional asymmetry;
- globally represented record/direction/V with local record access hidden.

Therefore the Stage 9 evidence supports keeping R and V as distinct top-level bookkeeping layers while retaining their internal refinements.

`finite-family bidirectional countermodels != universal R-V independence theorem`.

## 4. Xi after Stage 9

Stage 9 does **not** justify a new direct value law:

`Xi_RV : R_direction -> V`

or its converse.

The explicit Xi-like resources that remain necessary are typed correspondences among:

- relational events/current anchors;
- continuation classes;
- clock-perspective representations;
- record-target and memory observables;
- continuation weights.

Removing event/class correspondence leaves local P transport executable but makes typed cross-perspective P-R-V identification `not_established`.

Thus:

`typed Xi correspondence retained != direct Xi_RV value law established`.

`absence of an established direct Xi_RV value law != proof that no R-V constraint can exist in a broader theory`.

## 5. P after Stage 9

All 108 canonical explicit P edge matrices are reconstructible from retained per-node continuation coordinates:

`S^h_{Y<-X}=C_{h,Y} C_{h,X}^{-1}`.

This makes the stored edge matrices a derived representation role in the tested atlas.

It does **not** eliminate the P layer, because:

- the per-node perspective structure remains part of the model;
- event/class correspondence is not reconstructed merely from the matrices;
- typed observable semantics remain required.

`P edge reconstruction != P layer universally redundant`.

## 6. Remaining operational boundary

Stage 9D established covariance for:

- continuation-specific states;
- induced metrics;
- typed directional record observables;
- continuation classes;
- continuation weights;
- matched modal public views.

However, it deliberately did **not** construct one fully typed cross-continuation transport law for the Stage 9C future-signature measurement family.

`full Stage 9C future-measurement covariance remains not_established`.

This is the sharpest explicit operational boundary left after Stage 9.

## 7. Evidence-selected Stage 10 ranking

The completed `directional_record_potentiality` gate is removed from the future candidate set.

Remaining candidates are re-ranked from current evidence:

1. `full_measurement_covariance` — **9**
2. `richer_causal_order` — **6**
3. `parametrized_covariance_precursor` — **5**
4. `nonideal_povm_clocks` — **4**

Selected Stage 10 gate:

> **Construct and validate a fully typed cross-continuation future-measurement family under genuine continuation-aware clock changes.**

The selection is unique under the declared score function.

## 8. Why measurement covariance comes first

This gate is selected because Stage 9 has already made the surrounding structure unusually well isolated:

- continuation-specific state/metric transport works;
- directional record observables transport;
- V classes and weights transport;
- event/class/observable typing is explicit;
- P edge reconstruction is understood;
- the full future-signature measurement-family transport is still explicitly missing.

That makes measurement covariance a narrower and more discriminating next experiment than simultaneously changing the causal-order layer, clock ideality, or covariance class.

## 9. Why covariance/gravity rises but remains third

The parametrized/general-covariance precursor rises from Stage 8G's score 2 to Stage 9G's score 5 because the finite O/P/R/V architecture is substantially more mature and the directional-R/V blocker is now resolved in the declared family.

It is not selected first because:

`finite clock covariance != general covariance`.

Moving to a parametrized or gravitational model before closing the known future-measurement transport boundary would combine two changes at once and reduce diagnostic clarity.

Gravity/general covariance is therefore **deferred, not abandoned**.

## 10. Unresolved implications retained

Stage 9G explicitly keeps the following open:

- finite-family R/V separation => universal R-V independence;
- record-defined direction => ontological future openness;
- record-defined direction => ontological becoming;
- selected-vs-unselected modal semantics => ontic openness in nature;
- Potentiality => phenomenal passage;
- physical clock change => temporal succession;
- finite clock covariance => general covariance;
- full Stage 9C future-measurement-family covariance;
- direct Xi_RV value law;
- P-edge reconstructibility => universal P redundancy;
- refined O/P/R/V/Xi candidate => fundamental or unique ontology of time.

`not_established != false`.

## 11. Validation

Stage 9G source-level synthesis / gate-selection regression, GitHub Actions run #1099:

**`765 passed in 248.81s (0:04:08)`**

validated source head:

`e570a2b8e08d73bfa14db87c4faa71499d28dfad`

The first documentation-synchronized Stage 9G run (#1117) reached **764 passing tests / 2 historical documentation failures**. The Stage 9 scientific suite remained green. Both failures were stale Stage 7/8 roadmap assertions that still fixed gravity at Stage 10 after Stage 9G had selected the measurement-covariance gate for Stage 10. Those historical assertions were updated without changing the Stage 9G synthesis.

The corrected documentation-synchronized head then passed GitHub Actions run #1121:

**`766 passed in 459.00s (0:07:38)`**

validated branch head:

`1bcdc83a9dd5261f3d0de8d152534afda89667d7`

validated PR merge-ref:

`b53906446fd6970e3cfb03f110690ea9b5ce97b2`

At that reviewed checkpoint:

- the branch was ahead of `main` and behind by 0 commits;
- PR #10 was `mergeable=true`;
- unresolved review threads: 0;
- submitted reviews: 0;
- repository search found no TODO/FIXME/HACK markers or obvious credential/absolute-path artifacts.

Criterion 50 is therefore satisfied externally. It remains deliberately outside the executable Stage 9G selector.

## 12. Final validation interpretation

Closing criterion 50 does not add a new scientific claim. It records that the already-synthesized Stage 9 evidence is documentation-synchronized, regression-clean, based on the current `main`, mergeable, and free of known review blockers at the reviewed head.

It does **not** alter these boundaries:

- `full Stage 9C future-measurement covariance remains not_established`;
- `finite-family bidirectional countermodels != universal R-V independence theorem`;
- `finite clock covariance != general covariance`;
- `refined layered candidate != fundamental ontology`.

## 13. Strongest bounded statement

**Within the declared finite constrained Stage 9 family, the evidence strengthens the refined layered candidate `T=(O,P,R,V;Xi)`: directional R and nontrivial V are jointly realizable, finite-family ablations refute their mutual necessity in both directions, R_content/R_direction/R_access and V_extension/V_semantics/V_weights exhibit distinct functional behavior, and explicit P edge matrices are reconstructible while typed event/class/observable correspondence remains necessary. No direct Xi_RV value law is established. The strongest explicit operational boundary left is the full cross-continuation Stage 9C future-measurement-family covariance, so that boundary is selected as the Stage 10 gate ahead of richer order, parametrized/general covariance, and nonideal clocks. Criterion 50 is closed by the external final regression and merge-readiness review without adding a scientific claim. None of this establishes universal R-V independence, ontic openness, ontological becoming, empirical novelty, or general covariance.**
