# Research Roadmap

This roadmap is provisional and evidence-selected. Historical checkpoints and superseded planning labels are retained where documentation regressions depend on them; current scientific status is stated separately from those historical labels.

## Current refined candidate and status

The typed architecture carried from Stage 12 is

`T12_candidate=(O,P,R,V;Xi)`

with `R=(R_content,R_direction,R_access)` and `V=(V_extension,V_semantics,V_weights)`.

Stage 10G selects `measurement_covariant`. **Stage 10 criteria 1–50 are completed and Stage 10 is merged into `main` via PR #11 at `4a322634a5b83e416d374ee18e96ac6c7a5c88ba`.**

Stage 11G selects `parametrized_covariant`; Stage 11 criteria 1–50 were completed and **PR #12 was subsequently merged into `main`** at `d5fdc899a72b6a983c03b1f960c65cda948c8fb8`.

Stage 12G selects `multi_orbit_gauge_covariant`; Stage 12 criteria 1–50 were completed and PR #13 was subsequently merged into `main` at `ee4baec55fa994217b275f9f2451e25fc6736787`.

**Stage 13 criteria **1–50** are completed on Draft PR #14 at the criterion-50 merge-readiness checkpoint. The validated Stage 13 synthesis is `multi_constraint_path_covariant`; PR #14 is merge-ready, open, Draft, and unmerged.**

Validated checkpoint chain:

- Stage 10 criterion 50 head `11b4357fccb0b73b7b7b80bc13e34f904290107b`; run #1271: **`868 passed in 345.59s`**.
- Stage 11 criterion 50 head `6b5ae9ffb2f1fe784080d9d2a02e349430d4f01a`; run #1469: **`938 passed in 682.23s (0:11:22)`**.
- Stage 12F: **`1011 passed in 692.53s (0:11:32)`**; Stage 12 criterion 50 head `549eed786b36aa458470ef7e858b515117816ac7`, run #1642: **`1024 passed in 896.22s (0:14:56)`**; final pre-merge run #1654: **`1025 passed in 693.84s (0:11:33)`**.
- Stage 13G implementation head `013f90303ededbf769aaeef11a0336a480b02e2b`, run #1813: **`1099 passed in 878.58s (0:14:38)`**.
- Stage 13 criterion-50 reviewed head `5b6b4641f082f6554cf14ce6f55eba1ce5905ad0`, run #1815: **`1098 passed in 695.62s (0:11:35)`**; branch **ahead 83 / behind 0**, PR #14 `mergeable = true`, no review blocker found.

`repository validation != new scientific evidence`.

`merge-ready != merged`.

## Selected gates through Stage 14

Selected Stage 10 gate:

> **Construct and validate a fully typed cross-continuation future-measurement family under genuine continuation-aware clock changes.**

Selected Stage 11 gate:

> **Construct a parametrized covariance precursor that preserves the typed O/P/R/V measurement architecture without assuming a preferred external time parameterization.**

Selected Stage 12 gate:

> **Construct a multi-orbit constraint-generated gauge atlas that separates gauge-related parameterizations from physically distinct orbits and tests whether relational/Dirac observables and the typed O/P/R/V measurement architecture descend consistently across that atlas.**

Selected Stage 13 gate:

> **Construct a minimal multi-constraint constraint-algebra/refoliation precursor with at least two nontrivially related first-class constraint directions, and test whether the Stage 12 physical-orbit quotient, relational observables, and typed O/P/R/V measurement architecture remain compatible under the resulting constraint-generated path structure without assuming general relativity.**

Evidence-selected Stage 14 gate:

> **Construct a minimal phase-space-dependent structure-function / hypersurface-deformation precursor designed to test whether the Stage 13F simple commuting-basis trivialization persists, and retest the physical quotient, relational observables, and typed O/P/R/V measurement architecture without assuming general relativity or refoliation invariance.**

Stage 14 selector id: `phase_space_structure_function_precursor`.

The Stage 14 ranking at the Stage 13G checkpoint is:

1. `phase_space_structure_function_precursor` — 12;
2. `gravitational_minisuperspace_extension` — 8;
3. `richer_causal_order` — 8;
4. `nonideal_povm_clocks` — 7.

The first gate is selected because Stage 13F explicitly showed that the present noncommuting presentation admits the simple equivalent commuting rescaling `K_X_tilde=exp(-T)K_X`. The next clean pressure test is whether such basis trivialization persists under phase-space-dependent structure-function dependence before adding gravitational field degrees of freedom.

`constraint-basis equivalence != universal basis trivializability`.

`phase-space-dependent structure-function precursor != hypersurface-deformation algebra by definition`.

`structure-function precursor != general relativity`.

## Historical Stage 7–9 checkpoints

## Stage 7 — Quantum records inside a constrained multi-clock model

Earlier roadmap versions assigned Stage 7 directly to a generally covariant / gravitational extension. The Stage 6G evidence selection superseded that chronology and inserted the more discriminating record gate first.

Gravity/general covariance is deferred, not abandoned.

## Stage 8 — Quantum Potentiality inside the shared constrained construction

Stage 8 integrated explicit Potentiality/extension semantics in the shared constrained construction. Stage 8G completed criteria 48–49, kept criterion 50 external, and selected the directional-record Stage 9 gate while gravity/general covariance remained deferred.

`Potentiality != quantum randomness by definition`.

## Stage 9 — Directional records with nontrivial quantum Potentiality

- Stage 9A — common directional-R/V continuation substrate — completed.
- Stage 9B — directional diagnostics and controls — completed.
- Stage 9C — typed modal models and directional operational underdetermination — completed.
- Stage 9D — continuation-aware clock transport — completed.
- Stage 9E — P/O/R_direction/V compatibility matrix — completed.
- Stage 9F — ablation / reconstruction / accessibility matrix — completed.
- Stage 9G — synthesis and evidence-selected next gate — completed.
- Stage 9 criterion 50 — external final validation — completed.

At the **Stage 9 checkpoint**, Stage 9C future-measurement covariance remained `not_established`; Stage 10 subsequently closed that bounded operational gap.

Stage 9G selected `refined_layered` and the fully typed future-measurement covariance program.

`finite-family bidirectional countermodels != universal R-V independence theorem`.

`P edge reconstruction != P layer universally redundant`.

`finite clock covariance != general covariance`.

### Historical planning labels retained for regression context

Before Stage 10G closed its synthesis and before Stage 11 became the active gate, planning documents used the historical labels below. They do not describe the current state.

## Stage 10 — Fully typed future-measurement covariance — in progress

Selected Stage 10 gate remained the fully typed cross-continuation future-measurement family above until Stage 10G closed it.

## Stage 11 — Parametrized / generally covariant / gravitational extension — deferred gate

At that historical checkpoint, Gravity/general covariance is deferred, not abandoned. Stage 10G later reranked the finite precursor and selected the narrower parametrized-covariance gate implemented below.

## Stages 0–9 — completed and merged

Stages 0–6 established the reconstruction/accessibility, modal, record, constrained relational, multi-clock, and layered O/P/R/V/Xi foundations. Stage 7 integrated quantum records, Stage 8 explicit Potentiality, and Stage 9 directional records with nontrivial Potentiality.

## Stage 10 — Fully typed future-measurement covariance — completed and merged

Stage 10A–B established the typed reference family and continuation-specific normalization. Stage 10C implemented the continuation-aware transport; Stage 10D established the bounded probability covariance; Stage 10E transported weights/modal models/evidence updates; Stage 10F pressure-tested typing and false positives; Stage 10G completed synthesis and selected `measurement_covariant`.

Stage 10 criteria 1–50 are completed. Criterion 50 validated head `11b4357fccb0b73b7b7b80bc13e34f904290107b`; run #1271 passed **`868 passed in 345.59s`**.

`parametrized covariance precursor != general relativity`.

`repository validation != new scientific evidence`.

`merge-ready != merged`.

## Stage 11 — Parametrized covariance precursor — completed and merged

Frozen distinctions retained throughout Stage 11:

`parameter label != internal clock reading`.

`parameter label != event identity`.

`internal clock perspective != external parameterization`.

`orientation-preserving reparameterization != time reversal`.

`parametrized covariance precursor != general relativity`.

Stage 11A–G are completed. Stage 11G selected `parametrized_covariant`; criterion 50 validated head `6b5ae9ffb2f1fe784080d9d2a02e349430d4f01a`, run #1469: **`938 passed in 682.23s (0:11:22)`**.

`parametrized_covariant finite family != general covariance`.

`one-orbit covariance != multi-orbit gauge covariance`.

`external parameterization independence != diffeomorphism invariance`.

`constraint-generated gauge precursor != general relativity`.

## Stage 12 — Multi-orbit constraint-generated gauge atlas — completed and merged

### Stage 12A — multi-orbit constrained carrier and explicit gauge-flow representatives — completed

Four physically distinct canonical orbits are retained while same-orbit gauge representatives are related by the declared constraint-generated flow.

### Stage 12B — Dirac/relational observables and physical-orbit discrimination — completed

The full Dirac pair separates all distinct canonical physical orbits while relational change remains nontrivial.

### Stage 12C — typed gauge atlas, quotient, and descent — completed

The finite same-orbit gauge groupoid descends to four physical quotient classes without licensed cross-orbit arrows.

### Stage 12D — O/P/R/V/Xi and orbit-sensitive future-measurement descent — completed

The inherited typed architecture descends over the quotient while retaining orbit-sensitive operational witnesses.

### Stage 12E — internal clock × external parameterization × gauge-flow compatibility — completed

The declared finite C x Phi, G x Phi, and C x G x Phi typed path families are compatible.

### Stage 12F — ablation / wrong-orbit / false-positive controls — completed

Stage 12F rejects the frozen false-positive family. The validated checkpoint passed **`1011 passed in 692.53s (0:11:32)`**.

### Stage 12G — executable synthesis and evidence-selected next gate — completed

Stage 12G selects `multi_orbit_gauge_covariant` and `multi_constraint_refoliation_precursor`.

Stage 12 criteria 1–50 are completed. Criterion 50 reviewed head `549eed786b36aa458470ef7e858b515117816ac7`, run #1642: **`1024 passed in 896.22s (0:14:56)`**. Final pre-merge run #1654: **`1025 passed in 693.84s (0:11:33)`**.

`multi_orbit_gauge_covariant finite family != general covariance`.

`finite constraint-generated gauge atlas != diffeomorphism invariance`.

`finite C x G x Phi compatibility != refoliation invariance`.

## Stage 13 — Multi-constraint constraint-algebra / refoliation precursor — completed at merge-readiness checkpoint

### Stage 13.0 — protocol freeze — completed

The six-dimensional carrier, two first-class constraint directions, compensated mixed-path semantics, complete-relational data, equivalent-basis controls, typed O/P/R/V/Xi carry-over, and interpretation guards were frozen before the positive experiments.

### Stage 13A — two-constraint first-class carrier and finite representative family — completed

The 36 positive representatives satisfy two independent constraint/generator directions with `{K_T,K_X}=-K_X` and 144 licensed single-generator arrows.

### Stage 13B — noncommuting gauge paths and compensated closure — completed

All **144 / 144** mixed pairs close under the exact compensator; same-raw reordered paths differ and wrong compensators are detected.

### Stage 13C — Dirac / two-clock complete relational observables and physical-orbit discrimination — completed

`Q_D=q-pT-0.5X`, `P_D=p` descend across representatives, all six distinct orbit pairs remain separated, and complete-relational change remains nontrivial.

### Stage 13D — typed multi-constraint gauge atlas, path words, quotient, and descent — completed

The atlas contains 87 typed nodes and 144 arrows, no licensed cross-orbit arrows, and exactly four quotient classes of nine representatives.

### Stage 13E — O/P/R/V/Xi and future-measurement descent across compensated path choices — completed

The operational architecture descends over all 144 compensated path choices; 10 / 10 negative controls are rejected. Run #1801: **`1084 passed in 703.45s (0:11:43)`**.

### Stage 13F — basis / ablation / anomaly / false-positive controls — completed

The equivalent commuting presentation `K_X_tilde=exp(-T)K_X=p_X+0.5p` reconstructs the same finite quotient-level content. All 144 / 144 commuting mixed paths close and 6 / 6 required controls are rejected. Run #1809: **`1085 passed in 562.97s (0:09:22)`**; follow-up #1811: **`1087 passed in 867.22s (0:14:27)`**.

`noncommuting constraint presentation != fundamental physical non-Abelianity`.

`basis-equivalent finite quotient != refoliation invariance`.

### Stage 13G — executable synthesis and evidence-selected next gate — completed

The executable A–F selector chooses exactly `multi_constraint_path_covariant`; run #1813 passed **`1099 passed in 878.58s (0:14:38)`**. It evidence-selects `phase_space_structure_function_precursor` for Stage 14.

### Stage 13 criterion 50 — external final repository validation / merge-readiness review — completed

Reviewed head `5b6b4641f082f6554cf14ce6f55eba1ce5905ad0`; run #1815 passed **`1098 passed in 695.62s (0:11:35)`**. The branch was **ahead 83 / behind 0**, PR #14 was `mergeable = true`, and no unresolved review blocker was found.

Stage 13 criteria **1–50** are completed at this merge-readiness checkpoint. PR #14 remains Draft, open, and unmerged.

## Stage 14 — phase-space-dependent structure-function / hypersurface-deformation precursor — selected next gate

Stage 14 should alter the constraint algebra before adding full gravitational dynamics. The first discriminating question is whether Stage 13F's simple commuting-basis trivialization survives a deliberately phase-space-dependent structure-function construction while the physical quotient, relational observables, and typed operational architecture are retested.

The selected gate is a precursor only. It does not presuppose a hypersurface-deformation algebra, refoliation invariance, diffeomorphism invariance, general covariance, or general relativity.

## Persistent interpretation guards

- `operational quantum equality != modal/ontological identity`;
- `Potentiality != quantum randomness by definition`;
- `parameter label != internal clock reading`;
- `parameter label != event identity`;
- `internal clock perspective != external parameterization`;
- `finite clock covariance != general covariance`;
- `parametrized_covariant finite family != general covariance`;
- `one-orbit covariance != multi-orbit gauge covariance`;
- `external parameterization independence != diffeomorphism invariance`;
- `constraint-generated gauge precursor != general relativity`;
- `multi_orbit_gauge_covariant finite family != general covariance`;
- `Dirac-invariant data + relational change != proof of eternalism`;
- `gauge quotient != elimination of physical change`;
- `noncommuting constraint presentation != fundamental physical non-Abelianity`;
- `constraint-basis equivalence != universal basis trivializability`;
- `multi_constraint_path_covariant finite family != refoliation invariance`;
- `finite first-class constraint algebra != hypersurface-deformation algebra`;
- `phase-space-dependent structure-function precursor != hypersurface-deformation algebra by definition`;
- `structure-function precursor != general relativity`;
- `future-measurement covariance != future actuality`;
- `finite-model success != empirical discovery`;
- `repository validation != new scientific evidence`;
- `merge-ready != merged`;
- `not_established != false`.
