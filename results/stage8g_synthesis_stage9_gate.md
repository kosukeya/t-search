# Stage 8G Results — Synthesis and Evidence-Selected Stage 9 Gate

Status: **synthesis implemented; final documentation-synchronized regression and merge-readiness review completed.**

## Synthesis result

Executable Stage 8A–F evidence selects:

`refined_layered`

The current finite-model candidate is retained at top level as:

`T8_candidate=(O,P,R,V;Xi)`

with candidate internal typing:

- `R=(R_content,R_direction,R_access)`;
- `V=(V_extension,V_semantics,V_weights)`.

This is a bookkeeping refinement supported by different finite-model role behavior, not a claim of fundamental primitive decomposition.

## Why the candidate is not reduced

Stage 8F does not reconstruct selected-vs-unselected modal semantics from retained public P/O/current-R structure. The same two-class carrier also admits different nontrivial weights with different predictions.

Therefore neither `V_semantics` nor nontrivial `V_weights` is reduced to the retained public carrier in the declared interface.

## Why the candidate is not broken

Stage 8E establishes positive finite-model compatibility for:

- `P-O(event effects)`;
- `P-R(current record)`;
- `P-V(class/weights)`;
- `O-V(extension)`.

Stage 8F further constructs a record-neutral, two-continuation constrained P/O/V witness with genuine clock transport and weight-sensitive prediction.

## Why the candidate is not merely inconclusive

The Stage 8F ablations discriminate distinct roles:

- current record can be lost while nontrivial V/P/O is preserved;
- QExt multiplicity can be lost while formal modal typing remains;
- singleton weight is reconstructible as 1;
- nontrivial two-class weights are underdetermined by the carrier;
- modal semantics can be removed without a unique reconstruction from public P/O/current-R;
- explicit P-V edge matrices are reconstructible;
- removing event/class correspondence makes P-V identification `not_established`;
- hiding record access makes the record inaccessible without globally erasing it.

These outcomes support a refined layered candidate strongly enough to distinguish it from a merely unresolved synthesis.

## Candidate refinements

### R

`R_content`, `R_direction`, and `R_access` remain distinct typed roles.

The canonical Stage 8 V carrier has record content but no directional record arrow. Hidden access preserves the global record while making the local interface inaccessible.

### V

`V_extension`, `V_semantics`, and `V_weights` show different ablation/reconstruction behavior.

`V_extension` is the executable continuation-class structure. `V_semantics` distinguishes hidden-selected from no-selected-continuation model roles. `V_weights` determines continuation weighting/prediction and is not fixed by the two-class carrier.

## Derived representation roles

The synthesis retains two derived roles in the declared representation:

- explicit P-V edge matrices are reconstructed from continuation-specific per-node coordinates;
- singleton continuation weight is reconstructed from normalization.

`P-V map reconstruction != P=V`.

## Project answers

1. Nontrivial V can coexist with P/O/current-R in the declared constrained family.
2. Current target-specific R is neither sufficient to determine V nor necessary for the Stage 8F nontrivial P/O/V witness.
3. Matched density/Born/public P/O/current-R data do not uniquely determine selected-vs-unselected modal semantics in the declared family.
4. V should be refined internally as a bookkeeping layer because multiplicity, semantics, and weights have different tested behavior.
5. Explicit P-V edge matrices are reconstructible, while event/class correspondence remains a required typing resource.
6. Full P/O/directional-R/V integration is not established, and full Stage 8C measurement-family covariance remains `not_established`.
7. The top-level layered candidate is retained and refined rather than collapsed.

## Evidence-selected Stage 9 ranking

1. `directional_record_potentiality` — score 9
2. `full_measurement_covariance` — score 6
3. `richer_causal_order` — score 5
4. `nonideal_povm_clocks` — score 3
5. `parametrized_covariance_precursor` — score 2

Selected Stage 9 gate:

> **Integrate directional record formation with nontrivial quantum Potentiality in one constrained continuation family.**

The selection is unique under the declared score function.

## Rationale for Stage 9

Stage 8's strongest remaining structural gap is not current-record/V compatibility but directional-record/V compatibility. The canonical V carrier has current record content with directional score 0; the Stage 7C control has directional score `+1` on the same current prefix. Stage 9 should bring these structures into one nontrivial continuation family and test the combined R_direction–V relation directly.

`directional record arrow != ontological future openness`.

The generally covariant/gravitational precursor remains deferred because introducing it before resolving the directional-R/V and measurement-family boundaries would add confounds rather than maximize discrimination.

## Unresolved implications

Still not established:

- `directional_record_structure <=> nontrivial_V_structure`;
- `record_defined_direction => ontological_future_openness`;
- selected-vs-unselected semantics as an empirical fact about nature;
- `Potentiality => phenomenal_passage`;
- `physical_clock_change => temporal_succession`;
- `P-V covariance => general covariance`;
- full Stage 8C measurement-family covariance;
- fundamental independence of V's internal roles;
- fundamental or unique status of the refined layered candidate.

`not_established != false`.

## Exit criteria

Criteria 48–49 are the Stage 8G executable synthesis/gate targets.

Criterion 50 is external and requires the final full repository regression plus merge-readiness review. It is satisfied externally and is not marked satisfied in code.

## Validation

Stage 8F final head before Stage 8G:

**`663 passed in 257.59s`**

head `f97b89100859a8f61483bbd969898befbbec4261`

Stage 8G source-level synthesis / exit-audit regression:

**`672 passed in 192.16s`**

source head `234b74559821ec5662d58f546e9d1ecd00507a17`

PR merge-ref `d392db357dfe68c221bbd3752910577af22d0c18`

The first documentation-synchronized Stage 8G run reached **671 passing tests / 2 documentation failures**. The scientific suite remained green; the failures were a historical Stage 7 roadmap assertion that still fixed gravity at Stage 9 and one missing exact openness guard. Both documentation issues were corrected before the final regression.

The corrected documentation-synchronized head then passed the complete repository suite in GitHub Actions run #918:

**`673 passed in 312.61s (0:05:12)`**

validated head `1adc43e03537dd050e5de4028db4277cae20bfc0`

validated PR merge-ref `f9c8d9d3c2bef845ac0f9f79c2d1da92513e9e99`

At that reviewed head, PR #9 was mergeable and had no unresolved review threads or submitted reviews. Criterion 50 is therefore closed as an external merge-readiness condition, not as an additional executable scientific criterion.

## Strongest bounded statement

**Within the declared finite Stage 8 family, the evidence favors retaining the top-level layered candidate `T=(O,P,R,V;Xi)` while refining R into record-content/direction/access roles and V into continuation-extension/modal-semantics/weight roles. Current record content can be removed while nontrivial constrained P/O/V structure remains; selected-vs-unselected semantics and nontrivial weights are not uniquely reconstructed from retained public structure; and explicit P-V edge matrices are reconstructible from per-node coordinates. The strongest unresolved compatibility link is directional R with nontrivial V, so that link is selected as the next finite-model gate ahead of generally covariant/gravitational extension. None of this establishes ontic openness, metaphysical irreducibility, phenomenal passage, or a fundamental/unique ontology of time.**
