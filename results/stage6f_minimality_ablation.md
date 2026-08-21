# Stage 6F Results — Minimality / Ablation

Status: **completed**.

## Main result

Stage 6F neutralizes `O`, `P`, `R`, `V`, and `Omega` one at a time and derives role statuses from executable evidence rather than a hard-coded classification table.

The own-role result is:

- remove `O` -> succession/order is `lost`;
- remove `P` -> perspective transport is `lost`;
- remove `R` -> record-defined direction is `lost`;
- remove `V` -> modal branching/extension semantics are `lost`;
- remove `Omega` -> cross-perspective operational consistency is `reconstructible`.

For every layer, metaphysical irreducibility remains `not_established`.

## Status matrix

| ablation | succession/order | perspective transport | record direction | modal semantics | cross-perspective operational consistency | local record accessibility |
| --- | --- | --- | --- | --- | --- | --- |
| `O` | lost | preserved | preserved | preserved | preserved | preserved |
| `P` | preserved | lost | preserved | preserved | not_applicable | preserved |
| `R` | preserved | preserved | lost | preserved | preserved | lost |
| `V` | preserved | preserved | preserved | lost | preserved | preserved |
| `Omega` | preserved | preserved | preserved | preserved | reconstructible | preserved |

Compatibility checks involving an ablated endpoint are classified `not_applicable`, not as failed covariance.

## O, P, R, and V

The named roles of `O`, `P`, `R`, and `V` disappear under the declared ablations while the other independent toy-model roles remain available where meaningful.

The `R` result is especially diagnostic: replacing the recording interaction by the reversible no-record control leaves neutral ordered positions in place but drives both record and accessibility contrasts to zero and removes the record-defined orientation.

The `V` result preserves the Stage 2 boundary: ontology-neutral operational equality is not used to recreate the removed epistemic/ontic Potentiality semantics.

These are losses in the declared Stage 6 representation. They are not proofs that the four layers are universally irreducible.

## Omega reconstruction

Removing explicit `Omega` produces a different result.

Across all `54` ordered distinct-clock endpoint/readout comparisons in the canonical qutrit family:

- using the same bare source projector matrix in the target perspective produces at least one Born-probability mismatch above `1e-10`;
- reconstructing the target observable from the retained perspective map by

`O_q = M O_p M^dagger`

restores all 54 comparisons within the frozen tolerance.

Therefore the tested `Omega` role is `reconstructible` from retained `P` in the declared quantum operator interface.

The supported statement is limited:

**The explicit operational-correspondence layer is not required as an independent primitive for the Stage 5/6 canonical quantum witness once the perspective transformation and its standard adjoint action on operators are retained.**

This does not show that every operational semantics is derivable from perspective structure in general.

## Accessibility control

When the global `R` structure is retained but the target record readout is hidden, the local record role classifies as `inaccessible`, not `lost`.

Hence Stage 6F explicitly distinguishes:

`inaccessible != globally absent`.

## Minimality consequence

The Stage 6 evidence no longer supports treating all five symbols in

`T6=(O,P,R,V,Omega;Xi)`

as equally primitive in the tested architecture.

A more economical candidate for Stage 6G is:

- explicit typed layers `O`, `P`, `R`, and `V`;
- explicit compatibility data `Xi`;
- the tested quantum `Omega` role represented as derived from `P`/`Xi` rather than necessarily primitive.

This is a candidate minimal representation for the declared toy-model family, not a final ontology of time.

## Strongest supported Stage 6F statement

**Within the declared Stage 1–6 toy-model interfaces, removing `O`, `P`, `R`, or `V` eliminates that layer's named temporal role without an available reconstruction witness while leaving several other typed roles intact; removing the explicit `Omega` correspondence rule is different, because the tested cross-perspective Born consistency can be reconstructed from the retained perspective map through the standard adjoint action on observables. Local record information can separately become inaccessible without global record loss. None of these finite ablations establishes metaphysical fundamentality or universal irreducibility.**

## Guards

- `lost != metaphysically irreducible`;
- `software dependency != fundamentality`;
- `inaccessible != globally absent`;
- `Omega reconstructible here != Omega universally redundant`;
- `record direction != phenomenal passage`.

## Validation

Stage 6F focused tests: **13**.

Implementation-inclusive PR merge-ref checkpoint:

`423 passed in 31.81s`.

## Next pressure test

Stage 6G — synthesis and Stage 7 gate.

The synthesis should choose among:

- A — single minimal structure;
- B — layered temporal structure;
- C — complementary family;
- D — inconclusive.

The choice must preserve all `not_established` boundaries and use Stage 6F's partial minimality result rather than simply counting surviving software modules.
