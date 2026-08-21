# Stage 6F Notes — Minimality / Ablation

Status: **completed**.

Stage 6F tests whether the provisional Stage 6 scaffold

`T6=(O,P,R,V,Omega;Xi)`

contains role-redundant layers inside the declared toy-model interfaces.

Implementation:

- `src/t_search/stage6_ablation.py`
- `experiments/stage6f_minimality_ablation.py`
- `tests/test_stage6f_ablation.py`

The purpose is not to maximize the number of retained layers. It is to ask which tested roles survive when one layer is removed or neutralized, and whether a lost primitive can be reconstructed from retained structure.

## 1. Frozen status semantics

Stage 6F uses six statuses:

- `preserved`: the role remains directly represented and its retained diagnostic passes;
- `reconstructible`: the removed primitive is absent, but an executable reconstruction witness recovers the role from retained structure;
- `inaccessible`: the role remains globally represented but the declared local interface cannot access it;
- `lost`: the baseline role was represented, and the declared ablation removes the current representation without an executable reconstruction witness;
- `not_applicable`: the diagnostic requires an endpoint/layer that has been removed;
- `not_established`: the current evidence does not decide the claim.

Important boundary:

`lost in declared interface != metaphysically irreducible`.

Every layer-level irreducibility assessment remains `not_established` in Stage 6F.

## 2. Frozen roles

The six protocol roles are evaluated explicitly:

- succession/order;
- perspective transport;
- record-defined direction;
- modal branching/extension semantics;
- cross-perspective operational consistency;
- local record accessibility.

Stage 6F also keeps the Stage 6D/E compatibility roles visible:

- `P_O_compatibility`;
- `P_R_compatibility`;
- `P_V_compatibility`.

This distinguishes a role that is lost from a compatibility test that becomes meaningless because one endpoint is absent.

## 3. Baseline

Before any ablation, Stage 6F recomputes the retained Stage 6 diagnostics rather than assuming them from prose:

- the canonical Stage 6D event family has three strict order relations;
- the Stage 6C `C0 -> B2` partial atlas has three valid indirect paths and reconstructs the missing direct map within tolerance;
- the Stage 6E forward record transport is globally compatible and record-defined;
- epistemic and ontic Potentiality extension carriers both transport while remaining distinct semantic/runtime types;
- local exact record access retains a nonzero record contrast;
- Stage 6D `P-O` compatibility passes;
- Stage 6E `P-R` and `P-V` compatibility pass;
- Stage 5 operational consistency is reproduced under the corresponding-observable transport rule.

All frozen baseline roles therefore classify as `preserved`.

## 4. O ablation

Neutralization:

- remove the explicit Stage 6 event-order relations and vertical conditioning family;
- retain Stage 3 neutral bookkeeping positions inside the independent record witness, but do not silently reinterpret those indices as `O`.

Result:

- succession/order: `lost`;
- perspective transport: `preserved`;
- record-defined direction: `preserved`;
- modal branching semantics: `preserved`;
- cross-perspective operational consistency: `preserved`;
- local record accessibility: `preserved`;
- `P-O` compatibility: `not_applicable`;
- `P-R` and `P-V` compatibility: `preserved`.

Thus the explicit Stage 6 order layer can be removed without erasing the independently typed perspective, record, modal, or operational witnesses. This does not establish that no richer reconstruction of order is possible.

## 5. P ablation

Neutralization:

- remove the perspective atlas vertices/maps from the declared Stage 6 interface.

Result:

- perspective transport: `lost`;
- succession/order: `preserved`;
- record-defined direction: `preserved`;
- modal branching semantics: `preserved`;
- local record accessibility: `preserved`;
- cross-perspective operational consistency: `not_applicable`;
- all `P-*` compatibility checks: `not_applicable`.

This is deliberately stronger than the Stage 6C missing-edge control. Stage 6C removed one primitive edge while retaining `P`; Stage 6F removes the perspective layer itself. No indirect atlas path is therefore available.

## 6. R ablation

Neutralization:

- replace the Stage 3 recording interaction with the reversible no-record control;
- keep the neutral ordered positions and the other Stage 6 layers fixed.

Executable result:

- `record_defined = false`;
- orientation becomes `none`;
- record score becomes zero within tolerance;
- accessibility-arrow score becomes zero within tolerance.

Classification:

- record-defined direction: `lost`;
- local record accessibility: `lost` for the record-specific temporal role;
- succession/order, perspective transport, modal semantics, and cross-perspective operational consistency: `preserved`;
- `P-R` compatibility: `not_applicable`;
- `P-O` and `P-V` compatibility: `preserved`.

This reuses the Stage 3 non-implication witness: ordered positions and reversible dynamics can remain while record-defined direction disappears.

## 7. V ablation

Neutralization:

- remove the typed `EpistemicPotentiality` / `OnticPotentiality` extension carriers and their extension semantics;
- do not reconstruct them from ontology-neutral operational equality.

Result:

- modal branching/extension semantics: `lost`;
- succession/order: `preserved`;
- perspective transport: `preserved`;
- record-defined direction: `preserved`;
- cross-perspective operational consistency: `preserved`;
- local record accessibility: `preserved`;
- `P-V` compatibility: `not_applicable`;
- `P-O` and `P-R` compatibility: `preserved`.

The Stage 2 underdetermination result is crucial here: operational agreement is not treated as a reconstruction of the removed modal semantics.

## 8. Omega ablation — reconstruction witness

This is the distinctive Stage 6F result.

Neutralization:

- remove the explicit cross-perspective corresponding-observable rule from `Omega`.

Two alternatives are then compared over all ordered distinct-clock endpoint/readout pairs in the canonical qutrit family: `6 * 3^2 = 54` comparisons.

### Bare-matrix control

The source projector is used unchanged as a bare matrix in the target perspective.

At least one comparison exceeds the frozen tolerance, and the maximum bare-matrix probability residual is greater than `1e-10`.

Thus raw matrix identity is not a valid replacement for operational correspondence.

### Reconstruction from retained P

Using the retained perspective map `M`, Stage 6F reconstructs the corresponding target observable as

`O_q = M O_p M^dagger`.

All 54 source/target Born-probability comparisons then match within tolerance.

Therefore, in this declared finite-dimensional quantum operator interface:

- the explicit `Omega` primitive is removed;
- cross-perspective operational consistency is `reconstructible` from retained `P` plus the standard adjoint action on operators.

This is **not** a universal proof that operational correspondence is always redundant. The reconstruction assumes the declared quantum representation and the rule that observables transform by the adjoint action of the perspective map.

A conservative Stage 6 interpretation is therefore:

`Omega is a candidate derived layer from P/Xi in the current quantum interface`.

## 9. Inaccessible is not lost

Stage 6F also carries an interface-only control from Stage 6E.

The global record structure and global record-transport compatibility are retained while the target record field is hidden.

The local record role is classified as:

`inaccessible`,

not `lost`.

This keeps the distinction:

`locally inaccessible != globally absent`.

## 10. Ablation matrix

| removed layer | O role | P role | R role | V role | Omega role | local record access |
| --- | --- | --- | --- | --- | --- | --- |
| `O` | lost | preserved | preserved | preserved | preserved | preserved |
| `P` | preserved | lost | preserved | preserved | not_applicable | preserved |
| `R` | preserved | preserved | lost | preserved | preserved | lost |
| `V` | preserved | preserved | preserved | lost | preserved | preserved |
| `Omega` | preserved | preserved | preserved | preserved | reconstructible | preserved |

Compatibility tests become `not_applicable` when their required endpoint is ablated rather than being mislabeled as a failed compatibility relation.

## 11. Minimality interpretation

Within the declared Stage 6 interfaces:

- `O`, `P`, `R`, and `V` each lose their named role when that layer is removed, with no executable reconstruction witness currently supplied;
- `Omega` does not behave the same way: its tested operational role is reconstructible from retained `P` in the canonical quantum operator interface;
- local inaccessibility can occur without global loss;
- no layer has been shown to be metaphysically fundamental or universally irreducible.

So Stage 6F weakens the need for a five-primitive-layer reading of

`T6=(O,P,R,V,Omega;Xi)`.

A better Stage 6G candidate is now a layered structure in which `O`, `P`, `R`, and `V` remain explicitly typed, while the tested `Omega` role may be represented as derived compatibility/action data associated with `P` and `Xi`.

That remains a Stage 6G synthesis question rather than a Stage 6F ontology claim.

## 12. Interpretation guards

Stage 6F freezes:

- `lost != metaphysically irreducible`;
- `software dependency != fundamentality`;
- `inaccessible != globally absent`;
- `Omega reconstructible here != Omega universally redundant`;
- `record direction != phenomenal passage`.

## 13. Validation

Stage 6F adds **13 focused tests**.

Implementation-inclusive PR merge-ref checkpoint:

`423 passed in 31.81s`.

## 14. Next

Stage 6G — synthesis and Stage 7 gate.

Stage 6G should now compare the four frozen outcome classes:

- A: one minimal common temporal structure;
- B: layered temporal structure;
- C: complementary family of structures;
- D: inconclusive.

It should incorporate the Stage 6F result that the tested `Omega` role is reconstructible in the canonical quantum interface, while preserving every `not_established` boundary from Stages 6B–6F. It should then choose the most discriminating Stage 7 physical extension, run full regression, and perform merge-readiness review without overstating the toy-model evidence.
