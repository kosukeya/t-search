# Stage 2D Design Notes — Operational Equivalence

Status: **completed**.

## Design goal

Stage 2D must compare the epistemic and ontic models without cheating by inspecting their Python class names or privileged internal fields.

The protocol therefore fixes an ontology-neutral operational erasure:

`O(G) = (A_now, Next(D), pi(next|D))`.

The implementation follows that interface literally.

## Why the typed local views are not compared directly

`EpistemicLocalView` and `OnticLocalView` intentionally contain different typed Potentiality wrappers:

- `EpistemicPotentiality`;
- `OnticPotentiality`.

Direct dataclass equality would therefore answer only whether the semantic/type encodings are identical, which is not the Stage 2D question.

Instead, both are mapped to the shared `OperationalView` type.

## OperationalView

`OperationalView` contains only:

- current Actuality/prefix;
- canonical immediate next-event tuple;
- canonical immediate-next probability tuple.

It does not retain:

- Potentiality type;
- complete-history semantic role;
- epistemic selected history `h*`;
- ontic absence-of-selector metadata.

The erasure is deliberate and fixed before observing the result.

## Structural alternatives versus probability support

`Next(D)` is derived from the live Potentiality histories rather than inferred only from positive probability entries.

This matters because Stage 2C permits a structurally admissible extension to have zero weight.

The operational probability tuple is required to contain exactly the same next-event keys as the structural `Next(D)` set, including zero-valued entries when applicable.

This preserves the distinction:

`admissibility structure != probability assignment`.

## Baseline equality

For the canonical matched fixture:

- epistemic `q_E = (1/2,1/2)`;
- ontic `K = (1/2,1/2)`;

both operational views are exactly:

`((p,n), (l1,r1), ((l1,1/2),(r1,1/2)))`.

This is an intentionally constructed control.

## Negative control

Changing only one probability assignment, for example:

`q_E = (3/4,1/4)`

while leaving:

`K = (1/2,1/2)`,

keeps Actuality and Next equal but makes the probability component unequal.

This demonstrates that operational equality is conditional on matched predictions rather than forced by the epistemic/ontic labels.

## Interpretation guard

Use:

`operationally indistinguishable under the tested observables`

not:

- "the two models are the same";
- "ontic and epistemic Potentiality are physically equivalent";
- "no future experiment could distinguish them".

Stage 2D tests only the declared finite operational interface of the canonical toy model.

## Stage 2E handoff

Stage 2E should reuse the same `OperationalView` after a common explicit observation.

Baseline observation:

`l1`.

The interesting question is whether the two updated operational views remain equal even though their privileged internal semantics continue to differ.
