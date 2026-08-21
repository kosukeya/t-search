# Stage 6E Notes — Record and Modality Transport

Status: **completed**.

Stage 6E adds the remaining cross-layer transport tests required before the Stage 6 minimality/ablation phase. It keeps record structure `R`, Potentiality/modality `V`, perspective labels `P`, and compatibility data `Xi` explicitly typed rather than collapsing them into one notion.

Implementation:

- `src/t_search/stage6_record_modality.py`
- `experiments/stage6e_record_modality_transport.py`
- `tests/test_stage6e_record_modality_transport.py`

## 1. Record transport uses explicit event and variable correspondence

The canonical perspective endpoints remain the Stage 6C/6D pair:

`C0 -> B2`.

Stage 6E declares separately which Stage 3 variables correspond:

- record variable: `M` at the current event;
- target variable: `X` at the compared event;
- current record event: `e1`.

No record sign is inferred from horizontal perspective-map direction.

The Stage 3 positions are connected to the Stage 6 event labels only by the explicit declaration:

- `e0 -> position 0`;
- `e1 -> position 1`;
- `e2 -> position 2`.

## 2. Orientation-preserving record covariance

For the canonical forward Stage 3 record ensemble, Stage 6E uses the explicit correspondence:

- `e0 -> e0`;
- `e1 -> e1`;
- `e2 -> e2`;
- orientation: `preserving`.

The source and target global record-information profiles and decoder-accessibility profiles agree under this correspondence. The signed record and accessibility contrasts also satisfy the preserving sign rule within the Stage 3 tolerance.

Thus the forward record orientation transports covariantly without identifying the record arrow with the perspective-map direction.

## 3. Orientation-reversing record covariance

The modeled history-reversal control uses the reversed Stage 3 ensemble together with inverse microscopic maps in reverse order. The explicit correspondence is:

- `e0 -> e2`;
- `e1 -> e1`;
- `e2 -> e0`;
- orientation: `reversing`.

Under this declaration:

- the source lower-index record orientation corresponds to the target upper-index orientation;
- the information profile transports after endpoint reversal;
- the accessibility profile transports after endpoint reversal;
- the signed record contrast changes sign as required;
- the signed accessibility contrast changes sign as required.

This is covariance of a declared record diagnostic under modeled history reversal. It is not phenomenal passage and does not establish an ontological arrow of time.

## 4. Record-orientation mismatch control

A negative control keeps the same source forward ensemble, reversed target ensemble, and endpoint-reversing event map, but falsely declares the correspondence `orientation="preserving"`.

The underlying event map remains bijective and the mapped information profile still matches. However, the declared sign rule is now wrong, so the record-score and accessibility-score transport residuals exceed tolerance.

This demonstrates that the orientation metadata in `chi` carries nontrivial compatibility content rather than being decorative.

## 5. Accessibility is perspective/interface dependent

Stage 6E preserves the Stage 3F distinction:

`global record structure != locally accessible record structure`.

Three target-interface controls hold the same global forward record block fixed:

### Exact target readout

The target exposes the record register without noise. Local record diagnostics remain available and agree with the source under the preserving correspondence.

### Hidden target record

The target does not expose `M`. Global record covariance still passes, but the target local record score and local accessibility score are represented as unavailable rather than as zero or false.

Thus:

`locally inaccessible != globally absent`.

### Maximally noisy target record

The target exposes `M` through a binary-symmetric channel with error probability `1/2`. The field is formally exposed, but its local record-information and decoder contrasts vanish. The underlying global record covariance remains unchanged.

This separates three statuses:

- globally present record structure;
- locally hidden record structure;
- locally exposed but informationally erased record readout.

## 6. Modal transport relation is explicitly a bijection

Stage 6E introduces a typed map on Stage 2 partial descriptions:

`F_{q<-p}: D_p -> D_q`.

The canonical map is an injective renaming of the Stage 2 events:

- `p -> q_p`;
- `n -> q_n`;
- `l1 -> q_l1`;
- `l2 -> q_l2`;
- `r1 -> q_r1`.

The target branching substrate is constructed by pushing the source tree through this mapping.

The frozen modal compatibility relation is not left as an unspecified `?~`. Stage 6E declares:

`F_*(Ext_p(D))` is in **bijection** with `Ext_q(F(D))`.

At the canonical prefix `('p','n')`, both the epistemic and ontic Stage 2 views have two live complete histories, and both typed extension carriers transport bijectively to the renamed target substrate.

## 7. Operational underdetermination is preserved

The Stage 2 epistemic-history and ontic-extension models are transported separately rather than merged.

Before transport:

- their ontology-neutral operational views agree;
- their Potentiality runtime types are distinct;
- the epistemic model contains a selected complete history;
- the ontic model contains no selected-future field.

After transport, all four properties remain true.

In addition, transporting each ontology-neutral operational view through `F` agrees with independently recomputing the corresponding target operational view.

Therefore Stage 6E preserves the Stage 2 boundary:

`operational equality != modal/ontological equivalence`.

Successful extension-set transport does not collapse epistemic Potentiality and ontic Potentiality into the same semantics.

## 8. Modal mismatch control

The negative control keeps the canonical target branching substrate fixed but changes the event map by swapping the target images of `l2` and `r1`.

The resulting map is still a bijection of the five event labels. Nevertheless, mapped complete histories fail to be valid target extensions, so the declared extension-set bijection fails for both epistemic and ontic Potentiality.

Hence:

`event-label bijection != modal-extension compatibility`.

The branch/extension structure matters.

## 9. Structural interpretation

Stage 6D established a positive compatibility relation between `P` and `O`. Stage 6E now adds two further compatibility patterns:

- `P / chi` can transport `R` covariantly, including the correct sign change under orientation reversal;
- a separately declared description map `F` can transport `V` by a specified extension-set relation.

At the same time, accessibility and modal semantics remain independent qualifications:

- record structure can be globally compatible while locally inaccessible;
- extension carriers can transport bijectively while epistemic and ontic semantics remain formally distinct.

This strengthens the case for treating `Xi` as explicit compatibility data in the provisional scaffold

`T6=(O,P,R,V,Omega;Xi)`

without yet claiming that `Xi` or any other layer is metaphysically fundamental or irreducible.

## 10. Interpretation guards

Stage 6E preserves:

`record transport != phenomenal passage`

and

`operational equality != modal/ontological equivalence`.

The implementation reports these as interpretation guards, not as newly measured physical variables.

## 11. Validation

Stage 6E adds **15 focused tests**.

Implementation-inclusive PR merge-ref checkpoint:

`410 passed in 22.26s`.

## 12. Next

Stage 6F — minimality / ablation.

The next substage should remove or neutralize each provisional layer `O`, `P`, `R`, `V`, and `Omega` in turn and classify each temporal-role diagnostic as:

- preserved;
- reconstructible;
- inaccessible;
- lost;
- not applicable;
- not established.

Stage 6F must distinguish failure of one software representation from evidence of structural irreducibility.
