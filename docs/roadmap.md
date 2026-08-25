# Research Roadmap

This roadmap is provisional and evidence-selected. Historical checkpoints and superseded planning labels are retained where documentation regressions depend on them; current scientific status is stated separately from those historical labels.

## Current refined candidate and status

`T12_candidate=(O,P,R,V;Xi)` with `R=(R_content,R_direction,R_access)` and `V=(V_extension,V_semantics,V_weights)` remains the carried typed architecture.

Stage 10G selects `measurement_covariant`. **Stage 10 criteria 1–50 are completed and Stage 10 is merged** into `main` via PR #11 at `4a322634a5b83e416d374ee18e96ac6c7a5c88ba`.

Stage 11G selects `parametrized_covariant`; Stage 11 criteria 1–50 were completed and **PR #12 was subsequently merged into `main`** at `d5fdc899a72b6a983c03b1f960c65cda948c8fb8`.

Stage 12G selects `multi_orbit_gauge_covariant`; Stage 12 criteria 1–50 were completed and PR #13 was subsequently merged into `main` at `ee4baec55fa994217b275f9f2451e25fc6736787`.

Stage 13 criteria **1–50** are completed. At its criterion-50 checkpoint PR #14 was merge-ready, open, Draft, and unmerged; it was subsequently merged into `main` at `468fe6667ec6484fbe9e402135cd75f5d69420cf`. The validated Stage 13 synthesis is `multi_constraint_path_covariant`.

Stage 14A–G are completed on Draft PR #15. The validated Stage 14 synthesis is `structure_function_path_covariant_scalar_obstructed`; criteria **1–49** are satisfied and criterion **50** is the current external final full-repository / merge-readiness review.

Validated criterion-50 checkpoints:

- Stage 10: `11b4357fccb0b73b7b7b80bc13e34f904290107b`, run #1271, **`868 passed in 345.59s`**.
- Stage 11: `6b5ae9ffb2f1fe784080d9d2a02e349430d4f01a`, run #1469, **`938 passed in 682.23s (0:11:22)`**.
- Stage 12F: **`1011 passed in 692.53s (0:11:32)`**; Stage 12 criterion 50 `549eed786b36aa458470ef7e858b515117816ac7`, run #1642, **`1024 passed in 896.22s (0:14:56)`**.
- Stage 13 criterion-50 reviewed head `5b6b4641f082f6554cf14ce6f55eba1ce5905ad0`, run #1815, **`1098 passed in 695.62s (0:11:35)`**; branch **ahead 83 / behind 0**, PR #14 `mergeable = true`, no repository-level blocker found. This is a historical merge-readiness marker; PR #14 was subsequently merged.

`repository validation != new scientific evidence`.

`merge-ready != merged`.

## Selected gates through Stage 15

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

Evidence-selected Stage 15 gate:

> **Construct a minimal spatially indexed first-class constraint-algebra precursor with explicit local/smeared generators and nontrivial structure-function dependence, test whether the Stage 14 triangular Abelianization persists under the declared locality-preserving basis class, and retest the physical quotient, relational observables, and typed O/P/R/V measurement architecture without assuming general relativity or refoliation invariance.**

Stage 15 selector id: `spatially_indexed_constraint_algebra_precursor`.

## Historical Stage 7–9 checkpoints

## Stage 7 — Quantum records inside a constrained multi-clock model

Earlier roadmap versions assigned Stage 7 directly to a generally covariant / gravitational extension. The Stage 6G evidence selection superseded that chronology and inserted the more discriminating record gate first.

Gravity/general covariance is deferred, not abandoned.

## Stage 8 — Quantum Potentiality inside the shared constrained construction

Stage 8 integrated explicit Potentiality/extension semantics in the shared constrained construction. Stage 8G completed criteria **48–49**, kept criterion **50** external, and selected the directional-record Stage 9 gate while gravity/general covariance remained deferred.

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

Stage 9G executable synthesis selected `refined_layered`, retained/ranked `full_measurement_covariance`, and selected the fully typed future-measurement covariance program.

`finite-family bidirectional countermodels != universal R-V independence theorem`.

`P edge reconstruction != P layer universally redundant`.

`finite clock covariance != general covariance`.

### Historical planning labels retained for regression context

Before Stage 10G closed its synthesis and before Stage 11 became active, planning documents used the following historical labels. They do not describe the current state.

## Stage 10 — Fully typed future-measurement covariance — in progress

Selected Stage 10 gate remained the fully typed cross-continuation future-measurement family above until Stage 10G closed it.

## Stage 11 — Parametrized / generally covariant / gravitational extension — deferred gate

At that historical checkpoint, Gravity/general covariance is deferred, not abandoned. Stage 10G later reranked the finite precursor and selected the narrower parametrized-covariance gate implemented below.

## Stage 10 — Fully typed future-measurement covariance — completed and merged

Stage 10A through Stage 10G are completed. Stage 10G selected `measurement_covariant`. Stage 10 criteria 1–50 are completed and Stage 10 is merged into `main`. Criterion 50 validated head `11b4357fccb0b73b7b7b80bc13e34f904290107b`; run #1271 passed **`868 passed in 345.59s`**.

`finite clock covariance != general covariance`.

`parametrized covariance precursor != general relativity`.

## Stage 11 — Parametrized covariance precursor — completed and merged

Stage 11A through Stage 11G are completed. Stage 11G selected `parametrized_covariant` and `multi_orbit_constraint_gauge_atlas`; Stage 11 criteria 1–50 are completed.

Frozen distinctions:

`parameter label != internal clock reading`.

`parameter label != event identity`.

`internal clock perspective != external parameterization`.

`parametrized covariance precursor != general relativity`.

### Stage 11A — minimal parametrized constrained carrier and admissible family — completed

Historical evidence includes **36** corresponding-event views, **24** nonlinear raw-rate differences, and minimum positive lapse **0.5**.

`same constraint orbit != established general covariance`.

### Stage 11B — relational observables and relational derivatives — completed

Historical evidence retains **52** relational evaluations, **24** raw-rate comparisons, **7** correspondence classes, **6** negative-control families, and momentum value **1.25**. The `invalid_equal_raw_parameter_event_rule` control remains explicit.

`relational covariance on one finite orbit != general covariance`.

### Stage 11C — typed O/P/R/V/Xi lift — completed

`QExt(e1)={h_L,h_R}`.

`typed O/P/R/V/Xi lift != full future-measurement covariance`.

`typed product lift feasibility != independent dynamical covariance evidence`.

`Stage 10 event-role bridge != dynamical identification of quantum and classical carriers`.

### Stage 11D — future-measurement reparameterization covariance — completed

`Stage 11D future-measurement reparameterization covariance on the frozen positive family = established`.

`future-measurement reparameterization covariance != clock-change x reparameterization compatibility`.

`typed Stage 10/11 bridge != dynamical derivation of quantum measurement from the classical precursor`.

### Stage 11E — clock-change × parameterization compatibility — completed

`Stage 11E clock-change x parameterization compatibility on the frozen finite family = established`.

Historical exhaustive evidence retains **12**, **108**, **648**, and **1296** comparison counts together with `noncommuting_wrong_clock_path_detected`.

`commuting typed product square != independent interaction law`.

`commuting typed diagram != general covariance`.

`path-independent future probabilities != future actuality`.

`path-independent evidence update != ontological becoming`.

### Stage 11F — ablation / wrong-gauge / false-positive controls — completed

`Stage 11F typed-resource ablation and wrong-gauge false-positive controls = established on the frozen finite family`.

The historical matrix retains **12** typed-resource/ablation cases, **6** control groups, **4 / 4** reconstruction checks, and **7 / 7** rejected controls including `invalid_equal_raw_parameter_event_rule` and `parameter_dependent_oprv_corruption_detected`.

- `event_correspondence_reconstructible_but_typed_identity_lost`;
- `lapse_semantics_missing_typed_claim_not_established`;
- `wrong_lapse_jacobian_numerically_refuted`;
- `reconstructible != universally redundant`;
- `lost != metaphysically irreducible`;
- `wrong-gauge failure != ontological becoming`;
- `finite-model ablation != fundamental ontology`.

### Stage 11G — synthesis and evidence-selected next gate — completed

`Stage 11 finite typed parametrized covariance status = parametrized_covariant`.

`multi_orbit_constraint_gauge_atlas` was selected for Stage 12. Criterion 50 validated head `6b5ae9ffb2f1fe784080d9d2a02e349430d4f01a`; run #1469 passed **`938 passed in 682.23s (0:11:22)`**.

`finite typed parametrized covariance != general covariance`.

`parametrized_covariant finite family != general covariance`.

`one-orbit covariance != multi-orbit gauge covariance`.

`external parameterization independence != diffeomorphism invariance`.

`constraint-generated gauge precursor != general relativity`.

## Stage 12 — Multi-orbit constraint-generated gauge atlas — completed and merged

### Stage 12A — multi-orbit constrained carrier and explicit gauge-flow representatives — completed

Four physically distinct physical orbits are represented by same-orbit gauge families.

### Stage 12B — Dirac/relational observables and physical-orbit discrimination — completed

The full Dirac pair separates the physical orbits while relational change remains nontrivial.

### Stage 12C — typed gauge atlas, quotient, and descent — completed

The finite gauge groupoid descends to four physical quotient classes without licensed cross-orbit arrows.

### Stage 12D — O/P/R/V/Xi and orbit-sensitive future-measurement descent — completed

The inherited typed architecture descends over the gauge quotient.

### Stage 12E — internal clock × external parameterization × gauge-flow compatibility — completed

The declared finite C x Phi, G x Phi, and C x G x Phi path families are compatible.

### Stage 12F — ablation / wrong-orbit / false-positive controls — completed

Stage 12F checkpoint passed **`1011 passed in 692.53s (0:11:32)`**.

### Stage 12G — executable synthesis and evidence-selected next gate — completed

Stage 12G selects `multi_orbit_gauge_covariant` and `multi_constraint_refoliation_precursor`.

Stage 12 criteria 1–50 are completed. Criterion 50 reviewed head `549eed786b36aa458470ef7e858b515117816ac7`; run #1642 passed **`1024 passed in 896.22s (0:14:56)`**.

`multi_orbit_gauge_covariant finite family != general covariance`.

`finite C x G x Phi compatibility != refoliation invariance`.

## Stage 13 — Multi-constraint constraint-algebra / refoliation precursor — completed and merged

### Stage 13A — two-constraint first-class carrier and finite representative family — completed

The 36 positive representatives have two independent first-class constraint/generator directions and 144 licensed single-generator arrows.

### Stage 13B — noncommuting gauge paths and compensated closure — completed

All **144 / 144** mixed paths close under the exact compensator and wrong compensators are detected.

### Stage 13C — Dirac / two-clock complete relational observables — completed

The Dirac pair remains representative-independent inside each physical orbit and complete-relational change remains nontrivial.

### Stage 13D — typed multi-constraint gauge atlas / quotient — completed

The atlas has 87 typed nodes, 144 arrows, zero licensed cross-orbit arrows, and four quotient classes of nine representatives.

### Stage 13E — O/P/R/V/Xi and future-measurement descent — completed

All 144 compensated paths preserve the declared operational payloads; 10 / 10 controls are rejected. Run #1801: **`1084 passed in 703.45s (0:11:43)`**.

### Stage 13F — basis / ablation / anomaly controls — completed

The equivalent commuting presentation `K_X_tilde=exp(-T)K_X=p_X+0.5p` reconstructs the same finite quotient-level content. All 144 / 144 commuting mixed paths close and 6 / 6 controls are rejected. Run #1809: **`1085 passed in 562.97s (0:09:22)`**; follow-up #1811: **`1087 passed in 867.22s (0:14:27)`**.

### Stage 13G — executable synthesis and evidence-selected next gate — completed

The executable selector chooses exactly `multi_constraint_path_covariant`. Implementation head `013f90303ededbf769aaeef11a0336a480b02e2b`; run #1813 passed **`1099 passed in 878.58s (0:14:38)`**. It selects `phase_space_structure_function_precursor` for Stage 14.

### Stage 13 criterion 50 — external final repository validation / merge-readiness review — completed

Reviewed head `5b6b4641f082f6554cf14ce6f55eba1ce5905ad0`; run #1815 passed **`1098 passed in 695.62s (0:11:35)`**. The branch was **ahead 83 / behind 0**, PR #14 was `mergeable = true`, and no repository-level blocker was found. At this historical checkpoint PR #14 was merge-ready, Draft, open, and unmerged; it was subsequently merged into `main` at `468fe6667ec6484fbe9e402135cd75f5d69420cf`.

Stage 13 criteria **1–50** are completed and Stage 13 is merged into `main` via PR #14.

## Stage 14 — phase-space-dependent structure-function / hypersurface-deformation precursor — criteria 1–49 completed

### Stage 14A — three-constraint first-class structure-function carrier — completed

The 108 positive representatives have three independent first-class constraint/generator directions, with phase-space-dependent structure functions sampling negative, zero, and positive values and off-surface closure/Jacobi checks.

### Stage 14B — mixed paths and third-direction compensation — completed

All **864/864** canonical same-orbit mixed pairs close for both `12D` and `21D` under the exact third-direction compensator. The nontrivial `X_0 != 0` subfamily contains **576** compensator differences and the `X_0=0` subfamily contains **288** exact zero differences.

### Stage 14C — Dirac / complete relational / quotient descent — completed

The raw Dirac pair reconstructs exactly **4 classes × 27 representatives**, separates all **6/6** physical-orbit pairs, preserves **23328** compensated-path complete-relational comparisons, and retains nontrivial three-condition relational change.

### Stage 14D — scalar obstruction vs triangular basis equivalence — completed

All **216/216** required `X != 0` finite/nonzero diagonal `simple_scalar_rescaling` evaluations retain the nonzero `D'` component, while the determinant-one triangular transformation `H_2_tilde=H_2-kappa T1 X D=p_2+b p` gives an equivalent strongly commuting tested basis preserving sampled quotient/Dirac/relational/public content.

### Stage 14E — typed O/P/R/V/Xi and future-measurement descent — completed

All **864** path checks and **108** original/triangular basis checks preserve quotient-level public/future payloads while path, structure-function, compensator, and basis provenance remain explicit in Xi.

### Stage 14F — destructive controls — completed

The frozen matrix rejects **14/14** ablation/anomaly/false-positive controls in their intended layers, including the rebuilt `H_2_bad` anomaly surface.

### Stage 14G — executable synthesis and evidence-selected Stage 15 gate — completed

The validated synthesis is

`structure_function_path_covariant_scalar_obstructed`.

Source/test head `c109d1ed1c9a1f043ed741a934c32b139ca15e09`; run #1910 passed **`1168 passed in 891.95s (0:14:51)`**. Documentation-synchronized head `70adbf1355581f159544ff200f45d5a2b007d80e`; run #1918 passed **`1166 passed in 902.17s (0:15:02)`**.

The Stage 15 ranking selects `spatially_indexed_constraint_algebra_precursor` before gravitational minisuperspace because spatial indexing/local smearing is the sharper missing algebraic structure and minisuperspace suppresses it.

### Stage 14 criterion 50 — external final full-repository regression / merge-readiness review — in progress

Stage 14 criteria **1–49** are satisfied. Criterion 50 reviews the complete Stage 14A–G repository delta, synchronizes top-level planning/status documents, checks review blockers and branch/base state, and performs the final full regression before merge-readiness is declared.

`structure_function_path_covariant_scalar_obstructed finite family != refoliation invariance`.

`diagonal scalar-rescaling obstruction != fundamental physical non-Abelianity`.

`triangular basis equivalence != universal basis trivializability`.

`spatially indexed constraint precursor != hypersurface-deformation algebra by definition`.

`spatially indexed constraint precursor != general relativity`.

## Persistent interpretation guards

- `repository validation != new scientific evidence`;
- `merge-ready != merged`;
- `not_established != false`.
