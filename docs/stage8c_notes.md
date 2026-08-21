# Stage 8C Notes — Operational Underdetermination and Explicit Update

Status: **completed for the declared canonical finite continuation family.**

## Question

Can the two type-distinct Stage 8B models on the same executable continuation carrier remain operationally indistinguishable under one fully specified ontology-neutral quantum interface when continuation weights are matched, while an explicit common piece of evidence updates them according to different internal semantics?

Stage 8C answers this finite-interface question and closes Stage 8 exit criteria **22–29**. Genuine clock-perspective transport remains Stage 8D.

## Full ontology-neutral interface O_Q

Stage 8C implements:

`O_Q = (D, rho_now, R_now, Next_Q(D), pi_Q(next|D), observed_outcome)`.

`QuantumOperationalView` contains the current anchor, normalized current reduced density matrix, target-memory joint readout distribution and mutual information, physically defined next outcomes and probabilities, and the explicit observed outcome after update. It deliberately excludes `h*`, selector/model type, typed Potentiality, and raw `q_E` / `K` bookkeeping.

## Physical future-signature measurement

The orthogonal Stage 8A canonical `e2` states define a fixed projective measurement. Its first two effects project onto the `h_L` and `h_R` future-state rays and a third remainder projector closes the ambient measurement.

Executable Born signatures are:

- `h_L -> future_signature_0` with probability one;
- `h_R -> future_signature_1` with probability one;
- remainder probability zero for both retained continuations.

The measurement checks physical differences already present in Stage 8A; continuation string labels themselves are not promoted to observables.

## Matched operational prediction

For each continuation `h`, Stage 8C computes `p(y|h,D)` from the projective measurement and then forms:

`pi_E(y|D) = sum_h q_E(h|D) p(y|h,D)`,

`pi_O(y|D) = sum_h K(h|D) p(y|h,D)`.

The hidden epistemic `h*` is not read by this computation.

With `q_E=K=(0.5,0.5)`, both typed models predict `(0.5,0.5)` and their complete declared `O_Q` views agree within tolerance. A separate privileged diagnostic still distinguishes whether a selected continuation is present.

`operational quantum equality != modal/ontological identity`.

## Hidden-selected-continuation swap

With carrier and weights fixed, changing `h*=h_L` to `h*=h_R` changes the privileged diagnostic but leaves the full `O_Q` view unchanged. Thus `h*` does not leak into the pre-evidence operational interface.

## Weight-mismatch control

Changing only the ontic weights to `K=(0.75,0.25)` leaves current Actuality and record fields unchanged but changes the future-signature prediction from `(0.5,0.5)` to `(0.75,0.25)`.

This positive control shows that operational equality is not hard-coded into the comparator.

## Explicit evidence update

The update API accepts explicit `QuantumEvidence(outcome)` and never samples a branch internally. The canonical common evidence is `future_signature_0`.

Epistemic update:

- retains pre-existing `h*=h_L`;
- conditions `q_E` to `(1,0)`;
- rejects deterministic evidence inconsistent with hidden `h*` rather than silently replacing it.

Ontic-extension update:

- conditions `K` to `(1,0)`;
- adds no selected-continuation, selector, seed, or singleton `QuantumContinuation` field;
- advances to terminal `e2`, where `QExt(e2)=empty`.

Both descriptions advance from `e1` to `e2` and their post-update `O_Q` views agree for the common evidence.

The evidence-conditioned singleton posterior support is public evidence-derived information about the completed continuation, not a hidden selector that existed before evidence.

## Superposition and density/Born controls

The shared current `e1` state contains multiple coherent amplitudes. The two modal types nevertheless share the same current density matrix and matched Born-mixture prediction while privileged modal structure remains different.

Therefore, within this canonical family, superposition, the current state/density representation, and matched Born output do not uniquely select the epistemic-selected or ontic-extension semantics.

This is finite-family underdetermination, not a theorem that quantum states can never constrain modal interpretations in other theories.

## Exit criteria

Stage 8C satisfies criteria **22–29**:

22. matched full operational views agree;
23. privileged diagnostics distinguish the modal structures;
24. a weight mismatch changes operational prediction;
25. explicit common evidence advances Actuality consistently;
26. epistemic update retains `h*` and conditions beliefs;
27. ontic-extension update prunes support without adding a hidden complete future;
28. superposition/Born randomness alone does not select ontic-extension semantics in the canonical family;
29. state/density representation alone does not silently decide the modal semantics in the canonical family.

Criteria 30–50 remain Stage 8D–G work.

## Validation

Stage 8C adds the focused suite `tests/test_stage8c_operational_update.py`. The implementation/full regression before final planning-document synchronization passed:

**`612 passed in 203.50s`**.

## Interpretation boundary

Stage 8C does not establish ontic openness of the real future, a hidden pre-existing future in nature, collapse as physical becoming, sampling as actualization, phenomenal passage, P-V covariance, or V independence from P/O/R.

Frozen guards:

- `matched numerical q_E and K != matched probability semantics`;
- `explicit evidence update != ontological becoming`;
- `random sampling != ontic actualization evidence`;
- `superposition != ontic Potentiality by definition`;
- `same density/Born data != unique modal semantics in this family`;
- `evidence-conditioned singleton support != pre-existing hidden selector`.

## Next

Stage 8D — genuine clock-change modal transport.
