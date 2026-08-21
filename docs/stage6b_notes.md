# Stage 6B Notes — Independence and Countermodel Matrix

Status: **completed**.

Stage 6B evaluates the ten implications frozen by `docs/stage6_protocol.md` using the executable W1--W5 inventory produced in Stage 6A. The classification is derived from measured case facts rather than from a hand-written answer table.

## 1. Evidence semantics

Each proposition in an evidence case receives one of three values:

- `true` — the declared witness measurements establish the proposition in that case;
- `false` — the declared witness measurements establish its negation in that case;
- `unknown` — the witness does not measure enough to decide it.

For an implication `A => B`, Stage 6B uses the frozen statuses:

- `refuted`: at least one executable case has `A=true` and `B=false`;
- `supported_in_declared_family`: at least one declared case has `A=true`, every such case has `B=true`, and none has `B=unknown`;
- `not_established`: the current evidence does not decide the implication, including cases where `A=true` but `B=unknown`, or where no declared case has `A=true`.

Thus:

`not_established != refuted`.

## 2. Case-level expansion

The Stage 6A inventory is expanded to nine evidence cases:

- `W1:global-vs-local`;
- `W2:matched-modal-operational`;
- `W3:forward`;
- `W3:reversed`;
- `W3:symmetric`;
- `W3:no-record`;
- `W3:uniform-memory`;
- `W4:same-clock-transition-family`;
- `W5:cross-clock-operational`.

The Stage 3 witness is deliberately expanded into five control-specific cases. Treating W3 as one undifferentiated row would erase the fact that neutral order and reversible microscopic dynamics are present across controls while the record-defined orientation appears or disappears.

## 3. Frozen implication matrix

| ID | Implication | Stage 6B status | Decisive executable evidence |
|---|---|---|---|
| I1 | `order => arrow` | `refuted` | `W3:symmetric`, `W3:no-record`, `W3:uniform-memory` |
| I2 | `reversible microdynamics => no record arrow` | `refuted` | `W3:forward`, `W3:reversed` |
| I3 | `perspective consistency => temporal arrow` | `not_established` | W4/W5 establish perspective/transition consistency but do not measure a temporal arrow |
| I4 | `operational equality => modal/ontological equivalence` | `refuted` | `W2:matched-modal-operational` |
| I5 | `global reconstructibility => local accessibility` | `refuted` | `W1:global-vs-local` |
| I6 | `perspective-dependent structure => operational inconsistency` | `refuted` | `W5:cross-clock-operational` |
| I7 | `physical clock change => temporal succession` | `not_established` | W5 establishes genuine physical clock change but does not measure cross-perspective succession |
| I8 | `record arrow => ontologically open future` | `not_established` | W3 establishes record orientation but carries no ontological-openness variable |
| I9 | `Potentiality => phenomenal passage` | `not_established` | W2 establishes multiple live extensions but carries no phenomenal-passage variable |
| I10 | `perspective consistency => modal equivalence` | `not_established` | W4/W5 establish perspective consistency but carry no modal-equivalence comparison |

Here the word `arrow` in I1 is operationalized only as the Stage 3 record-defined orientation. It is not phenomenal passage or a universal physical arrow.

## 4. Executable countermodels

### I1 — neutral order does not force record-defined direction

The Stage 3 symmetric, no-record, and uniform-memory controls retain a declared multi-position neutral order while the executable record diagnostic returns no record-defined orientation.

The forward and reversed controls show the complementary cases: the same broad ordered substrate can support either sign of record orientation.

This refutes the implication only in the frozen Stage 6B sense:

`neutral order => record-defined arrow`.

It does not establish that every possible notion of order is independent of every possible notion of temporal direction.

### I2 — reversible microscopic dynamics do not exclude a record arrow

For both `W3:forward` and `W3:reversed`, the declared microscopic update maps are bijective while the record diagnostic is nonzero and orientation is detected.

Therefore microscopic reversibility and record-defined informational direction can coexist in the tested family.

### I4 — operational equality does not force formal modal/model equivalence

W2 recomputes equal operational projections for the matched Stage 2 epistemic-history and ontic-extension models while their declared Potentiality runtime structures remain formally different.

Stage 6B therefore rejects the move:

`same tested operational output -> same modal/ontological model`.

The result is a formal/model-structure counterexample inside the declared Stage 2 comparison, not a general metaphysical theorem about ontology.

### I5 — global reconstructibility does not force one-interface local accessibility

W1 reconstructs the complete labeled block and its reachability relation from the full family of local views. Yet event `e`, although globally reachable from `a`, is absent from the declared one-hop local view at `a`.

Thus reconstruction using a family of views and information available to one local interface are distinct properties.

### I6 — perspective-dependent structure does not force operational inconsistency

W5 simultaneously exhibits:

- perspective-dependent reduced entanglement (`~1 bit / 0 / 0` across A/B/C clock perspectives);
- cross-clock composition consistency within tolerance;
- Born-prediction agreement within tolerance when corresponding observables are transported correctly.

Thus changing reduced structure across perspectives does not by itself imply operational contradiction.

## 5. Why five implications remain `not_established`

Stage 6B does not turn a missing variable into a negative result.

- I3 remains open because perspective consistency is measured while a separate temporal-arrow quantity is not.
- I7 remains open because genuine clock change is measured while cross-perspective temporal succession is not.
- I8 remains open because record orientation is measured while ontological future openness is not.
- I9 remains open because Potentiality/branching is measured while phenomenal passage is not.
- I10 remains open because perspective consistency is measured while modal equivalence is not.

These gaps identify cross-layer questions for later Stage 6 compatibility/transport work rather than licenses to infer non-implication automatically.

## 6. Controls against a hard-coded truth table

The implementation includes measurement perturbation controls.

### W1 accessibility flip

Changing only:

`remote_in_one_hop_view: false -> true`

removes the I5 countermodel and changes its classification from `refuted` to `supported_in_declared_family` for the modified inventory.

### W1 reconstruction removal

Changing only:

`family_labeled_equal: true -> false`

removes the true antecedent for I5 and changes its classification to `not_established`.

### W5 Born-consistency break

Changing only the maximum Born residual from within tolerance to above tolerance changes the W5 consequent from operational consistency to operational inconsistency. I6 therefore changes from `refuted` to `supported_in_declared_family` for that modified inventory.

These controls show that the matrix is calculated from witness measurements and tolerance rules rather than returned from an implication-name lookup table.

## 7. Implementation

Stage 6B adds:

- `src/t_search/stage6_independence.py` — three-valued fact layer, case adapters, implication evaluator, and JSON-friendly matrix rows;
- `experiments/stage6b_independence_matrix.py` — prints the nine evidence cases and ten implication assessments;
- `tests/test_stage6b_independence_matrix.py` — frozen-list, countermodel, unknown-consequent, provenance, serialization, and anti-hard-coding controls.

## 8. Interpretation boundary

Stage 6B supports several non-implications inside the declared toy-model families. It does **not** establish that the provisional layers `O`, `P`, `R`, `V`, and `Omega` are metaphysically fundamental or pairwise irreducible.

In particular:

- a countermodel to one implication does not prove full logical independence in every model;
- `not_established` does not mean false;
- the Stage 5 perspective atlas is still not identified with time itself;
- record orientation is still not identified with phenomenal passage;
- formal modal/model inequivalence is not automatically an experimentally distinguishable ontological difference.

## 9. Validation

The Stage 6B implementation commit passed the repository GitHub Actions `tests` workflow.

Stage 6B is therefore ready to serve as the input checkpoint for Stage 6C — partial perspective atlas.
