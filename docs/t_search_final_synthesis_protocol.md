# t-search Final Synthesis Protocol

## Purpose

This protocol freezes how the t-search final synthesis will be produced after the Stage 16 closure decision.

The finalization phase is **documentation/synthesis only**. It is not a new numbered scientific Stage and must not be used to generate new Stage 17 evidence.

Primary companion decision record:

`docs/t_search_closure_decision.md`

Finalization baseline:

`main` merge commit `477a8e940bfcfaab377d618f7512027bacb5b5dd` after PR #17.

`final synthesis != new experiment`.

`repository validation != new scientific evidence`.

## Frozen objectives

The finalization must answer five questions without overclaiming:

1. What was t-search trying to discriminate about blockness and becoming?
2. What did Stages 1–16 actually establish on their declared models and finite families?
3. Which apparently becoming-like signatures were shown to be insufficient, representation-dependent, basis-dependent, gauge-dependent, clock-dependent, or otherwise non-diagnostic on the tested families?
4. Which claims remain genuinely unresolved or underdetermined?
5. Why does the current method no longer provide enough additional discrimination to justify continuing the same bounded-search trajectory?

The finalization must not attempt to force a winner between blockness and becoming.

## Evidence freeze

### Authoritative evidence base

Only evidence already present in the merged Stage 1–16 history may support scientific claims in the final synthesis.

Evidence may be drawn from:

- merged scientific implementation and tests on `main`;
- merged stage protocols and notes;
- merged `results/` artifacts;
- criterion-50 merge-readiness reports;
- recorded GitHub Actions regressions associated with the historical checkpoints;
- historical README/roadmap statements when they accurately summarize the underlying merged evidence.

### Evidence priority

When wording differs across artifacts, use this priority:

1. executable implementation/tests and exact validated diagnostics;
2. stage result artifacts recording the scientific synthesis;
3. frozen stage protocols/notes defining the tested claim and its scope;
4. criterion-50 reports for repository-validation state;
5. top-level README/roadmap summaries.

A later finalization document may clarify scope but may not silently strengthen a historical claim.

### Historical-state rule

Historical checkpoint artifacts must remain historical.

For example, a Stage 16G artifact that says criterion 50 was pending at that checkpoint is not retroactively rewritten merely because criterion 50 later completed. Likewise, the Stage 16G selection of Stage 17 remains historically valid even though the closure review later decides not to pursue Stage 17.

`later closure decision != rewrite of earlier evidence-selected gate`.

## Claim-status vocabulary

Every substantive final claim must be classified using one of the following statuses.

### `established_on_declared_family`

Use only when the relevant merged tests/results positively establish the claim on the explicitly declared finite/model family.

This status must include the scope in prose. It must never be shortened into an unqualified universal statement.

Example form:

> Established on the declared Stage 15 finite carrier: a one-step L1 local strongly commuting witness exists.

### `bounded_negative_result`

Use when an exhaustive or deterministic search/certificate applies to a declared but restricted class and reports no witness or a restricted nonexistence result.

Example form:

> Bounded negative result: no local strongly commuting witness was found in the declared Stage 16D search families.

This status may be strengthened to class-level nonexistence only when the historical artifact itself contains a genuine completeness/nonexistence certificate for that exact class.

### `not_established`

Use when the repository evidence does not establish the claim.

This status is epistemic, not a negation.

`not_established != false`.

### `underdetermined`

Use when multiple live interpretations remain compatible with the merged evidence and the project cannot discriminate among them.

The final synthesis should prefer `underdetermined` over speculative resolution when the evidence leaves multiple alternatives open.

### `methodological_judgment`

Use for the closure decision itself and other project-governance conclusions, such as the judgment that further bounded search has insufficient expected discriminating gain.

A methodological judgment must never be counted as new evidence for blockness, becoming, local obstruction, or any other physical claim.

## Central synthesis axes

The final synthesis must organize Stage 1–16 evidence by conceptual discriminator, not merely replay the chronological history.

At minimum, audit these axes:

1. reconstruction and accessibility;
2. records and continuation structure;
3. modality/potentiality and future-measurement content;
4. clock covariance and reparameterization;
5. gauge/constraint quotient structure;
6. multi-constraint path ordering and compensation;
7. phase-space-dependent structure functions;
8. local/smeared constraint structure;
9. basis equivalence and Abelianization;
10. locality pressure and closed-cycle topology;
11. typed O/P/R/V/Xi descent and provenance;
12. operational-to-ontological inference limits.

For each axis, the final synthesis must state:

- what phenomenon was constructed;
- what invariant/quotient/public content survived;
- what control or alternate representation weakened a naive ontological reading;
- the strongest licensed claim;
- the strongest explicitly unlicensed claim.

## Candidate-becoming audit

The final synthesis must explicitly audit whether each of the following can serve as a sufficient criterion for ontological becoming on the evidence obtained:

- relational change;
- future-measurement probabilities or potentiality;
- record directionality;
- path ordering;
- raw path-word inequality;
- constraint noncommutativity;
- nontrivial structure functions;
- failure of scalar trivialization;
- failure of a declared local Abelianization search;
- closed-cycle topology;
- typed operational descent.

For each candidate, record one of:

- `insufficient_on_project_evidence`;
- `not_established_as_sufficient`;
- `underdetermined`.

Do not use `refuted_as_becoming` unless the evidence genuinely proves impossibility, which the current closure decision does not assume.

## Blockness audit

The same asymmetry discipline applies to blockness.

The final synthesis must not infer block ontology merely from:

- existence of Dirac observables;
- quotient invariance;
- complete relational observables;
- covariance across clocks/gauges;
- existence of a strongly commuting basis;
- successful reconstruction of multiple temporal perspectives.

At minimum preserve:

`Dirac-invariant data + relational change != proof of eternalism`.

`global Abelianization != proof of block ontology`.

`reconstructible multiple perspectives != proof that all events are equally actual`.

## Required final artifacts

After this protocol is reviewed, the closure branch should produce the following artifacts.

### 1. `results/t_search_final_synthesis.md`

A research-level synthesis organized around the central question, conceptual axes, main findings, failed/insufficient candidate criteria, remaining anomaly, methodological boundary, and final conclusion.

### 2. `results/t_search_final_claim_ledger.md`

A compact claim ledger with columns or sections for:

- claim;
- status;
- scope;
- primary evidence artifact(s);
- interpretation guard;
- whether it bears on blockness, becoming, both, or neither.

### 3. `docs/t_search_methodological_limits.md`

A focused analysis of:

- admissibility/equivalence-class dependence;
- finite-model extrapolation;
- operational/ontological gap;
- missing bridge criterion for ontological becoming;
- search-family regress and why more bounded search is not automatically more discriminating.

### 4. README/roadmap final synchronization

Update only top-level current-state wording needed to record:

- Stage 16 completed and merged via PR #17;
- finalization entered after Stage 16;
- Stage 17 was historically selected but not pursued after methodological review;
- project closure/final synthesis status.

Do not rewrite historical stage checkpoint sections beyond factual merge-status synchronization where necessary.

### 5. Final closure audit

Run a full-repository regression on the final documentation-synchronized branch and perform a changed-file/consistency review before the final closure PR is declared merge-ready.

This validation establishes repository consistency only.

`final closure CI != new scientific evidence`.

## Final synthesis structure

`results/t_search_final_synthesis.md` should use approximately the following structure:

1. **Research question**
2. **Methodological strategy**
3. **Evidence trajectory across conceptual axes**
4. **What the project established**
5. **What apparently becoming-like signatures failed to establish**
6. **What block-like reconstructions failed to establish**
7. **Stage 16 residual issue: closed-cycle locality pressure**
8. **Why the residual issue remains underdetermined**
9. **Methodological boundary reached**
10. **Final conclusion**
11. **Possible reopening directions, without commitment**
12. **Interpretation guards**

## Final conclusion constraints

The final conclusion must satisfy all of the following.

It may say:

- t-search progressively separated representational/operational effects from stronger ontological claims;
- several intuitive signatures of becoming were insufficient on the tested families;
- block-like and becoming-like descriptions can coexist with the same quotient/public content in multiple tested constructions;
- Stage 16 leaves a bounded closed-cycle locality-pressure result;
- the project reaches an underdetermination/methodological boundary rather than a proof of either ontology.

It may not say, without new independent evidence:

- block universe is true;
- becoming is false;
- becoming is true;
- future events are actual;
- future events are unreal;
- closed cycles fundamentally obstruct local Abelianization;
- local non-Abelianizability is ontological becoming;
- finite precursor behavior establishes GR or continuum spacetime ontology.

## No-new-science rule

During finalization, changes to `src/` or scientific test logic are forbidden unless required solely to repair an accidental repository regression introduced by finalization itself.

If a substantive scientific implementation change becomes necessary, finalization must stop and the change must be treated as a reopened research program rather than silently incorporated into closure.

Documentation-consistency tests may be added or updated only to protect finalization-state wording and must not create new physical claims.

## Closure acceptance criteria

The project can be marked finalized only when all of the following are satisfied:

1. the closure decision remains explicit and outcome-neutral about blockness/becoming;
2. all final claims are traceable to merged Stage 1–16 evidence;
3. claim statuses use the frozen vocabulary consistently;
4. the final synthesis distinguishes finite/model-bounded claims from universal claims;
5. Stage 16 residual local-obstruction questions remain bounded/underdetermined unless the historical evidence already establishes more;
6. Stage 17 remains recorded as historically selected but not scientifically executed;
7. no historical Stage 1–16 result artifact is rewritten to manufacture a cleaner retrospective narrative;
8. README and roadmap accurately state the merged Stage 16 and finalization status;
9. the final full-repository regression passes;
10. an external merge-readiness review finds no remaining closure-documentation inconsistency.

## Reopening boundary

Future work is outside this finalization protocol unless it supplies a materially new discriminator as defined in `docs/t_search_closure_decision.md`.

Simple expansion of candidate count, search depth, polynomial degree, or sampled families is not part of finalization.

## Persistent interpretation guards

- `final synthesis != new experiment`;
- `repository validation != new scientific evidence`;
- `project closure decision != physical theorem`;
- `Stage 17 not pursued != Stage 17 refuted`;
- `bounded negative search != universal obstruction`;
- `not_established != false`;
- `operational equivalence != ontological equivalence`;
- `future-measurement covariance != future actuality`;
- `failure to Abelianize != ontological becoming`;
- `global Abelianization != proof of block ontology`;
- `Dirac-invariant data + relational change != proof of eternalism`;
- `finite graph locality != relativistic locality`;
- `finite constraint precursor != general relativity`.
