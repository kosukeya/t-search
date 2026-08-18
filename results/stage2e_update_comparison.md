# Stage 2E — Update Comparison

Status: **completed**.

## Purpose

Stage 2E compares the Stage 2B epistemic-history model and Stage 2C ontic-extension model after the same explicit observation.

Stage 2D established pre-observation operational equality under matched weights. Stage 2E asks whether that equality survives update while the privileged internal distinction remains.

## Baseline

Common current Actuality:

`D_0 = (p,n)`.

Common explicit observation:

`l1`.

Epistemic model:

`M_E = (T,h*,q_E)`

with:

`h* = h_L = (p,n,l1,l2)`

and:

`q_E(h_L)=q_E(h_R)=1/2`.

Ontic model:

`M_O(D_0) = (D_0,Ext_T(D_0),K)`

with:

`K(h_L)=K(h_R)=1/2`.

## Before-update result

As established in Stage 2D:

`O(G_E(D_0)) = O(G_O(D_0))`.

Both expose:

- Actuality `(p,n)`;
- Next `{l1,r1}`;
- probabilities `1/2,1/2`.

## Common observation update

### Epistemic

Observation `l1` changes the evidence prefix:

`(p,n) -> (p,n,l1)`.

Beliefs condition to:

`q_E(h_L)=1`

`q_E(h_R)=0`.

The selected complete history remains:

`h*=h_L`.

### Ontic

Observation `l1` extends Actuality:

`(p,n) -> (p,n,l1)`.

The incompatible right extension is removed:

`OPot(D_1)={h_L}`

and:

`K(h_L)=1`.

No selected complete future field is created.

## After-update operational result

Both updated models operationalize to:

`A_now = (p,n,l1)`

`Next = {l2}`

`pi(l2)=1`.

Therefore:

`O(G_E(D_1)) = O(G_O(D_1))`.

The Stage 2D operational indistinguishability persists through this matched common update.

## Internal distinction persists

The post-update operational equality does not make the model states identical.

Epistemic:

- the selected complete history was present before observation;
- the same `h*` remains after observation;
- beliefs changed.

Ontic:

- there was no selected complete future before observation;
- there is still no selected complete future field after observation;
- Actuality lengthened and the extension set was pruned.

Typed Potentiality remains distinct:

`EpistemicPotentiality != OnticPotentiality`

although after `l1` both carriers contain only `h_L`.

Thus:

`internal semantic difference persists`

while:

`tested operational outputs remain equal`.

## Terminal continuation control

Applying the next common observation:

`l2`

to the updated left-branch states gives the same terminal operational view:

`A_now=(p,n,l1,l2)`

`Next=empty`

`pi=empty`.

The epistemic selected history remains unchanged, while the ontic model still has no selected-future field.

## Update-domain contrast

The unselected ontic baseline can accept observation `r1` because the right branch has positive weight.

The canonical epistemic actual-run fixture with `h*=h_L` rejects the same observation as inconsistent with its already-selected history.

This is a real formal distinction between those two specific global states.

However, it is **not yet an operational discriminator between the model families**, because an epistemic model with `h*=h_R` can represent a right-branch actual run. Stage 2E therefore does not claim that observing `r1` would empirically favor the ontic family.

## Classification

### Operationally shared after the matched update

- updated Actuality/prefix;
- immediate next alternatives;
- immediate-next predictive probabilities.

### Internal/formal and not in the operational interface

- epistemic selected complete history `h*` and its preservation;
- ontic absence of a selected complete future;
- epistemic versus ontic Potentiality semantics.

### Not a strict physical invariant

Post-update equality of `A_now`, `Next`, and `pi` is a shared operational structure under the chosen interface and matched parameters. It is not yet a fundamental invariant of physical time.

## Validation

The committed Stage 2E test file contains 9 focused tests covering:

1. operational equality before and after common `l1` update;
2. expected post-update Actuality/Next/probabilities;
3. preservation of epistemic `h*`;
4. continued absence of ontic selected-future fields;
5. distinct typed Potentiality after update;
6. common `l2` update to the same terminal operational view;
7. rejection of mismatched starting Actualities;
8. `r1` update-domain contrast for the canonical `h*=h_L` fixture;
9. continued erasure of modal semantics by the operational interface.

A compact semantic reconstruction passed:

`9/9 checks`.

A clean-checkout/full-repository pytest run remains required before Stage 2 merge review because the current container cannot resolve `github.com`.

## Interpretation

The strongest justified Stage 2E statement is:

`M_E and M_O update differently internally, but under the matched left-branch observation they remain operationally indistinguishable through O`.

This supports a formal separation between hidden/global semantics and the tested local operational description. It does not decide whether physical time is fundamentally fixed or open.

## Next step

Stage 2F will run the remaining controls and produce the Stage 2 synthesis:

- event renaming / isomorphism;
- repeated state labels;
- weight mismatch consolidation;
- terminal and invalid-input controls;
- information/invariance classification;
- answers to the six fixed questions.
