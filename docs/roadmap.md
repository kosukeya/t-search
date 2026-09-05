# Research Roadmap

This roadmap is provisional and evidence-selected. Historical checkpoints and superseded planning labels are retained where documentation regressions depend on them; current scientific status is stated separately from those historical labels.

## Current track — R1 preflight completed (2026-09-05)

The user has authorized research redesign in this repository. The [redesign protocol](t_search_redesign_protocol.md) separates same-experiment covariance from the preservation of physically available intervention classes under clock changes, with explicit records and resource budgets.

- **R0:** redesign protocol prepared; no new scientific evidence.
- **R1 — completed with blockers:** [literature and implementability audit](t_search_r1_preflight.md), [reproducible diagnostic](../experiments/r1_intervention_preflight.py), and [results](../results/r1_intervention_preflight.json). Bare memory readout fails fixed-constraint support preservation; a lifted instrument's covariance does not establish its timed physical implementation.
- **Pilot:** `pilot_gate = blocked`; RQ2 closure and RQ3 control experiments have not started. Novelty remains unestablished.
- **R1b — proposed next:** specify one finite readout apparatus and its constraint family, common preparation and periodic boundary conditions; reassess physical event correspondence and novelty before opening a pilot.
- **Historical Stage 17:** selected but not started; the Stage 16 bounded basis-search expansion remains frozen.

PR #18 merged on 2026-08-26 at `d1384a2071bc954c9fcfa2e1559d6721ce1f1ec3`. The historical closure limits and Stage 1–16 evidence remain in force as interpretation boundaries; the new discriminator's novelty and physical adequacy are not yet established.

## Historical refined candidate and Stage 1–16 status

`T_candidate=(O,P,R,V;Xi)` with `R=(R_content,R_direction,R_access)` and `V=(V_extension,V_semantics,V_weights)` remains the carried typed architecture.

Stage 10G selects `measurement_covariant`; Stage 10 criteria 1–50 are completed and Stage 10 is merged via PR #11 at `4a322634a5b83e416d374ee18e96ac6c7a5c88ba`.

Stage 11G selects `parametrized_covariant`; Stage 11 criteria 1–50 are completed and Stage 11 is merged via PR #12 at `d5fdc899a72b6a983c03b1f960c65cda948c8fb8`. PR #12 was subsequently merged into `main`.

Stage 12G selects `multi_orbit_gauge_covariant`; Stage 12 criteria 1–50 are completed and Stage 12 is merged via PR #13.

Stage 13G selects `multi_constraint_path_covariant`; Stage 13 criteria 1–50 are completed and Stage 13 is merged via PR #14.

Stage 14G selects `structure_function_path_covariant_scalar_obstructed`. Stage 14 criterion 50 reviewed head `ab500148975ecea6e03fe8678ba1e8dcc50cb666`; run #1922 passed **`1166 passed in 709.02s (0:11:49)`**. PR #15 was subsequently merged into `main` at `041dce7af2a8990d6ca759dd668d9a53323bccff`. Stage 14 criteria 1–50 are completed.

Stage 15G selects `spatial_local_path_covariant_local_abelianizable`; Stage 15 criteria 1–50 are completed and PR #16 was subsequently merged into `main` at `cca49e37b3d4171ea74fd6c15fa119fcd4392e2d`.

Stage 16G selects `closed_cycle_local_path_covariant_nonlocal_only_in_declared_search`; Stage 16 criteria 1–50 are completed and PR #17 was subsequently merged into `main` at `477a8e940bfcfaab377d618f7512027bacb5b5dd`. Stage 16G historically evidence-selected `admissible_basis_transformation_completeness_audit` for Stage 17, but Finalization later froze new bounded scientific search after Stage 16. Stage 17 is therefore selected historically but not started and not pursued in the current program.

At the Finalization checkpoint, the project entered a documentation/synthesis-only closure state on PR #18. Finalization introduces no new scientific Stage or scientific evidence. Its current artifacts are `docs/t_search_closure_decision.md`, `docs/t_search_final_synthesis_protocol.md`, `results/t_search_final_claim_ledger.md`, `results/t_search_final_synthesis.md`, and `docs/t_search_methodological_limits.md`. README / roadmap synchronization and the final closure audit were completed before PR #18 was merged.

Validated criterion-50 checkpoints:

- Stage 10: `11b4357fccb0b73b7b7b80bc13e34f904290107b`, run #1271, **`868 passed in 345.59s`**.
- Stage 11: `6b5ae9ffb2f1fe784080d9d2a02e349430d4f01a`, run #1469, **`938 passed in 682.23s (0:11:22)`**.
- Stage 12F: **`1011 passed in 692.53s (0:11:32)`**; Stage 12 criterion 50 `549eed786b36aa458470ef7e858b515117816ac7`, run #1642, **`1024 passed in 896.22s (0:14:56)`**.
- Stage 13 criterion-50 reviewed head `5b6b4641f082f6554cf14ce6f55eba1ce5905ad0`, run #1815, **`1098 passed in 695.62s (0:11:35)`**; branch **ahead 83 / behind 0**, PR #14 `mergeable = true`; PR #14 was subsequently merged.
- Stage 14 criterion-50 reviewed head `ab500148975ecea6e03fe8678ba1e8dcc50cb666`, run #1922, **`1166 passed in 709.02s (0:11:49)`**; PR #15 was subsequently merged.
- Stage 15 criterion-50 reviewed head `42d3efdeecb04c76b7b49774ceb9c7afafbb0d3a`; push run #2001 **`1261 passed in 486.79s (0:08:06)`**; PR run #2002 **`1261 passed in 906.83s (0:15:06)`**; PR #16 was subsequently merged.
- Stage 16 criterion-50 reviewed head `5fd4ee8e95d2773335e8ac01f7669cd87b688f41`; PR run #2074 **`1342 passed in 944.90s (0:15:44)`**; audit `results/stage16_criterion50_merge_readiness.md`; PR #17 was subsequently merged at `477a8e940bfcfaab377d618f7512027bacb5b5dd`.

`repository validation != new scientific evidence`.

`merge-ready != merged`.

`project closure decision != new scientific evidence`.

`Stage 17 not pursued != Stage 17 refuted`.

## Historical selected gates through Stage 17

The gates below retain the evidence-selected historical trajectory. The Stage 17 gate remains a correct Stage 16G checkpoint, but Finalization records the later methodological decision not to execute it in the current program.

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

Evidence-selected Stage 16 gate:

> **Construct a minimal four-site closed-cycle spatially indexed first-class constraint-algebra precursor with no terminal seed generator, retain explicit local/smeared structure-function dependence, test whether one-step L1 or finite-depth locality-preserving Abelianization still exists, and retest compensated paths, the physical quotient, complete relational observables, and typed O/P/R/V/Xi descent without assuming general relativity or refoliation invariance.**

Stage 16 selector id: `four_site_closed_cycle_constraint_algebra_precursor`.

Selection rationale: the Stage 15 one-step L1 witness peels the terminal `C2=K2` tail of an acyclic open chain. A three-site cycle would make every one-step neighbourhood contain every site, so the locality audit would degenerate. A four-site cycle is the smallest closed carrier for which `N1(i)` remains a genuine restriction while removing the terminal-seed loophole.

Evidence-selected Stage 17 gate:

> **Audit a broader admissible locality-preserving basis-transformation class on the validated four-site closed-cycle carrier beyond the frozen affine cyclic one-step L1 ansatz and depth<=4 elementary-shear compositions; seek either a constructive local strongly commuting witness or a bounded completeness/nonexistence certificate, while preserving invertibility, the four-class quotient, the Dirac pair, complete four-clock relational observables, and typed O/P/R/V/Xi content, without promoting search failure to a universal physical locality obstruction.**

Stage 17 selector id: `admissible_basis_transformation_completeness_audit`.

Current Finalization disposition: **historically selected, not started, and not pursued after methodological closure review**.

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

## Stage 14 — phase-space-dependent structure-function / hypersurface-deformation precursor — completed and merged

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

The validated synthesis is `structure_function_path_covariant_scalar_obstructed`.

Source/test head `c109d1ed1c9a1f043ed741a934c32b139ca15e09`; run #1910 passed **`1168 passed in 891.95s (0:14:51)`**. Documentation-synchronized head `70adbf1355581f159544ff200f45d5a2b007d80e`; run #1918 passed **`1166 passed in 902.17s (0:15:02)`**.

### Stage 14 criterion 50 — completed and subsequently merged

Reviewed head `ab500148975ecea6e03fe8678ba1e8dcc50cb666`; run #1922 passed **`1166 passed in 709.02s (0:11:49)`**. PR #15 was merge-ready, Draft, open, and unmerged at that historical checkpoint and was subsequently merged into `main` at `041dce7af2a8990d6ca759dd668d9a53323bccff`.

Stage 14 criteria **1–50** are completed.

## Stage 15 — spatially indexed constraint-algebra precursor — completed and merged

### Stage 15A — local/smeared first-class carrier — completed

The open three-site carrier has 108 positive representatives in four physical orbits, three independent constraint directions, and a nontrivial phase-space-dependent local structure coefficient.

### Stage 15B — compensated local/smeared paths and Jacobi — completed

All 864 canonical local pairs and 540 smeared ordering probes satisfy the exact predicted compensation; off-surface Jacobi and an independent Hamiltonian flow oracle are retained.

### Stage 15C — Dirac / complete relational / physical quotient — completed

The full Dirac pair yields exactly four classes of 27 representatives; same-orbit sampled pairs are constraint-flow reachable, all six orbit pairs are separated, and complete three-clock relational observables descend while omitted-clock/raw-coordinate controls fail.

### Stage 15D — locality-preserving basis pressure — completed

A distinct one-step L1 nearest-neighbour shear `C1 -> C1-kappa*T1*C2=K1` gives a strongly commuting basis and preserves the tested physical content. The full seed reconstruction itself remains non-one-step-L1 and factors at exact Lfinite depth 2.

Classification: `local_abelianization_persists`.

### Stage 15E — typed O/P/R/V/Xi descent — completed

108 representative architectures descend to four public payloads; 864 local checks, 540 smeared checks, 1080 independent non-grid endpoint reconstructions, and 1512 basis correspondences preserve the declared public/future payloads while provenance remains in Xi.

### Stage 15F — destructive controls — completed

All **15/15** frozen destructive controls are rejected as intended. Scientific run #1982 passed **`1242 passed in 489.65s (0:08:09)`**.

### Stage 15G — executable synthesis and evidence-selected Stage 16 gate — completed

The validated executable selector chooses `spatial_local_path_covariant_local_abelianizable` and ranks `four_site_closed_cycle_constraint_algebra_precursor` first. Push run #1995 passed **`1255 passed in 886.65s (0:14:46)`** and PR run #1996 passed **`1255 passed in 553.80s (0:09:13)`**.

The closed-cycle gate is selected to remove the open-chain terminal-seed/triangular-elimination loophole without importing GR or refoliation assumptions.

### Stage 15 criterion 50 — external final repository validation / merge-readiness review — completed

Reviewed head `42d3efdeecb04c76b7b49774ceb9c7afafbb0d3a`; push run #2001 passed **`1261 passed in 486.79s (0:08:06)`** and PR run #2002 passed **`1261 passed in 906.83s (0:15:06)`**. The external review found no remaining repository-level blocker. The audit is recorded in `results/stage15_criterion50_merge_readiness.md`.

Stage 15 criteria **1–50** are completed and PR #16 was subsequently merged into `main` at `cca49e37b3d4171ea74fd6c15fa119fcd4392e2d`.

## Stage 16 — four-site closed-cycle locality pressure test — completed and merged

### Stage 16A — closed-cycle local/smeared first-class carrier — completed

The four-site cyclic carrier validates the exact first-class local/smeared algebra, rank-4 constraint/generator structure, 324 positive representatives, and the distinction among canonical-function support, closure-coordinate support, and basis-map locality.

### Stage 16B — compensated local/smeared paths — completed

All **2,592 / 2,592** frozen adjacent local path probes admit the declared presented-basis compensator; raw ordering defects remain nontrivial and quotient/Dirac equality is independently preserved.

### Stage 16C — Dirac / complete relational / physical quotient — completed

The Dirac pair yields exactly four physical quotient classes of 81 representatives and complete four-clock relational observables descend while omitted-clock/raw-coordinate controls fail.

### Stage 16D — locality-preserving Abelianization pressure test — completed

A global strongly commuting seed basis exists. No local strongly commuting witness is found in the declared L0 / explicit one-step L1 / depth<=4 elementary-shear / frozen translation-covariant affine cyclic L1 searches. This is a bounded search result, not a universal locality obstruction.

Classification: `only_nonlocal_abelianization_witness_found_in_frozen_search`.

### Stage 16E — typed O/P/R/V/Xi descent — completed

Typed public and future-measurement content descends to four quotient payloads across representative, path, and basis choices while provenance remains explicit in Xi.

### Stage 16F — destructive and topology controls — completed

All **20/20** frozen controls reject/detect as intended. Topology controls exhibit local Abelianization depth **1** for projected open C3 and depth **2** for wrap-open C4, while the closed C4 has no local strong witness in the declared Stage 16D search.

### Stage 16G — executable synthesis and evidence-selected Stage 17 gate — completed

The executable selector chooses `closed_cycle_local_path_covariant_nonlocal_only_in_declared_search`. Scientific implementation head `e1a559abc2488e6ef23bda7c7dbb50bc43bd030d`; PR run #2060 passed **`1338 passed in 738.18s (0:12:18)`**.

The selected Stage 17 gate is `admissible_basis_transformation_completeness_audit`, targeting the principal uncertainty left by Stage 16D: whether the negative local-witness result reflects the frozen search class or survives a broader declared admissible class. This remains the historical Stage 16G selection; it was not started and is not pursued by Finalization.

### Stage 16 criterion 50 — external final full-repository regression / merge-readiness review — completed

Reviewed head `5fd4ee8e95d2773335e8ac01f7669cd87b688f41`; PR run #2074 passed **`1342 passed in 944.90s (0:15:44)`** on merge checkout `b9b457a3baa4c52c124ce9ab9ea329185cdcfbdf`. The external review found no repository-level merge blocker. The audit is recorded in `results/stage16_criterion50_merge_readiness.md`.

Stage 16 criteria **1–50** are completed. PR #17 was subsequently merged into `main` at `477a8e940bfcfaab377d618f7512027bacb5b5dd`.

## Finalization — documentation/synthesis-only closure phase — completed and merged (historical)

Finalization starts from merged Stage 16 baseline `477a8e940bfcfaab377d618f7512027bacb5b5dd`. It is not Stage 17 and introduces no new scientific carrier, search family, or physical evidence.

Completed artifacts on PR #18:

- `docs/t_search_closure_decision.md`;
- `docs/t_search_final_synthesis_protocol.md`;
- `results/t_search_final_claim_ledger.md`;
- `results/t_search_final_synthesis.md`;
- `docs/t_search_methodological_limits.md`.

The current final synthesis classifies ontological becoming and blockness/eternalism as `not_established`, decisive discrimination between them as `underdetermined`, and the decision not to continue the same bounded-search trajectory as a `methodological_judgment` rather than a new physical result.

README / roadmap synchronization and the final closure audit were completed before PR #18 merged on 2026-08-26 at `d1384a2071bc954c9fcfa2e1559d6721ce1f1ec3`. The audit establishes repository/documentation readiness only; it adds no new scientific evidence.

`final synthesis != new scientific evidence`.

`Stage 17 not pursued != Stage 17 refuted`.

`project closure decision != physical theorem`.

## Persistent interpretation guards

- `repository validation != new scientific evidence`;
- `merge-ready != merged`;
- `project closure decision != physical theorem`;
- `final synthesis != new scientific evidence`;
- `Stage 17 not pursued != Stage 17 refuted`;
- `not_established != false`;
- `one-step L1 Abelianization on an open three-site chain != universal local Abelianizability`;
- `local Abelianization != absence of meaningful local constraint structure`;
- `finite graph locality != relativistic locality`;
- `finite smeared constraint algebra != hypersurface-deformation algebra`;
- `compensated local/smeared operational descent != refoliation invariance`;
- `nonlocal_only_in_declared_search != universal locality obstruction`;
- `no L1 witness in frozen search != no L1 Abelianization exists`;
- `global Abelianization != physical triviality`;
- `cycle opening changes graph topology != proof that topology is ontic`;
- `failure to Abelianize != ontological becoming`;
- `Dirac-invariant data + relational change != proof of eternalism`;
- `complete relational observable != ontological becoming by definition`;
- `future-measurement covariance != future actuality`;
- `typed operational descent != ontological equivalence`;
- `Stage 17 completeness audit selection != predicted locality obstruction`.
