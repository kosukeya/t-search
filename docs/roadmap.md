# Research Roadmap

This roadmap is provisional and evidence-selected.

## Current refined candidate

`T12_candidate=(O,P,R,V;Xi)` with `R=(R_content,R_direction,R_access)` and `V=(V_extension,V_semantics,V_weights)`, equipped on the frozen finite Stage 12 family with a typed physical-orbit quotient `Q_Phi` and separately typed internal-clock `C`, external-reparameterization `G`, and constraint-generated gauge `Phi` transport families.

Stage 10G selects `measurement_covariant`. **Stage 10 criteria 1–50 are completed and Stage 10 is merged into `main` via PR #11 at `4a322634a5b83e416d374ee18e96ac6c7a5c88ba`.** Stage 11G selects `parametrized_covariant`; Stage 11 criteria 1–50 were completed and PR #12 was subsequently merged into `main` at `d5fdc899a72b6a983c03b1f960c65cda948c8fb8`. Stage 12G selects `multi_orbit_gauge_covariant`; Stage 12.0 and Stage 12A–G are completed on Draft PR #13, criteria 1–49 are satisfied and criterion 50 is next.

Selected Stage 10 gate:

> **Construct and validate a fully typed cross-continuation future-measurement family under genuine continuation-aware clock changes.**

Selected Stage 11 gate:

> **Construct a parametrized covariance precursor that preserves the typed O/P/R/V measurement architecture without assuming a preferred external time parameterization.**

Selected Stage 12 gate:

> **Construct a multi-orbit constraint-generated gauge atlas that separates gauge-related parameterizations from physically distinct orbits and tests whether relational/Dirac observables and the typed O/P/R/V measurement architecture descend consistently across that atlas.**

Selected Stage 13 gate:

> **Construct a minimal multi-constraint constraint-algebra/refoliation precursor with at least two nontrivially related first-class constraint directions, and test whether the Stage 12 physical-orbit quotient, relational observables, and typed O/P/R/V measurement architecture remain compatible under the resulting constraint-generated path structure without assuming general relativity.**

## Stages 0–9 — completed and merged

Stages 0–6 established the reconstruction/accessibility, modal, record, constrained relational, multi-clock, and layered O/P/R/V/Xi foundations. Stage 7 integrated quantum records, Stage 8 explicit Potentiality, and Stage 9 directional records with nontrivial Potentiality. Stage 9G selected the fully typed future-measurement covariance gate and criterion 50 later closed with final Stage 9 validation **`766 passed in 459.00s`**.

`Potentiality != quantum randomness by definition`.

`finite clock covariance != general covariance`.

## Stage 10 — Fully typed future-measurement covariance — completed and merged

Stage 10A–B established the typed reference family and continuation-specific normalization. Stage 10C implemented 18 typed charts, 108 genuine ordered distinct-clock transports, and 324 three-clock compositions. Stage 10D used 196 Hermitian-tomography-complete probes and 7056 probe outcome evaluations. Stage 10E transported weights/modal models/evidence updates; Stage 10F pressure-tested typing and false positives; Stage 10G selected `measurement_covariant`.

Bounded result:

`fully typed finite future-measurement covariance = established`.

Documentation-synchronized head `11b4357fccb0b73b7b7b80bc13e34f904290107b` passed run #1271 with **`868 passed in 345.59s`**; final run #1275 passed **`868 passed in 402.52s`** before merge.

`repository validation != new scientific evidence`.

`merge-ready != merged`.

## Stage 11 — Parametrized covariance precursor — completed and merged

Frozen distinctions include:

`parameter label != internal clock reading`.

`parameter label != event identity`.

`internal clock perspective != external parameterization`.

`orientation-preserving reparameterization != time reversal`.

`parametrized covariance precursor != general relativity`.

### Stage 11A — minimal parametrized constrained carrier and admissible family — completed

Criteria **11–16** satisfied. `C = p_T + p^2/2 = 0` was implemented with positive nonconstant lapse and the identity/affine/cubic/sinh family. Evidence includes minimum positive lapse **0.5**, **36** corresponding-event raw-label differences, and **24** nonlinear raw-rate differences.

`minimal Stage 11A constraint orbit preservation = established`.

`same constraint orbit != established general covariance`.

### Stage 11B — relational observables and relational derivatives — completed

Criteria **17–23** satisfied. Stage 11B evaluated **52** `q(T=tau)` observables and **52** `dq/dT` derivatives, reconstructed `dq/dT=1.25`, retained **24** nonlinear raw-rate differences, and found **7** identity/affine equal-label overlaps of which **6** pair different events. The weak rule is `invalid_equal_raw_parameter_event_rule`.

`Stage 11B relational observable/derivative covariance on the frozen positive family = established`.

`equal raw lambda != physical-event correspondence`.

`relational covariance on one finite orbit != general covariance`.

### Stage 11C — typed O/P/R/V/Xi lift — completed

Criteria **24–31** satisfied. The Stage 9/10 architecture was lifted across the four external parameterizations while representation metadata stayed in Xi. `QExt(e1)={h_L,h_R}` remained explicit. Parameter-dependent O/P/R/V corruption controls were **4 / 4** detected as `parameter_dependent_oprv_corruption_detected`.

`Stage 11C typed O/P/R/V/Xi lift on the frozen positive family = established`.

`typed O/P/R/V/Xi lift != full future-measurement covariance`.

`typed product lift feasibility != independent dynamical covariance evidence`.

`Stage 10 event-role bridge != dynamical identification of quantum and classical carriers`.

### Stage 11D — future-measurement reparameterization covariance — completed

Criteria **32–38** satisfied. At fixed A/e2, `QExt(e1)={h_L,h_R}` and the frozen two-outcome future measurement were transported across four external parameterizations.

`Stage 11D future-measurement reparameterization covariance on the frozen positive family = established`.

`external lapse != quantum measurement normalization form`.

`typed Stage 10/11 bridge != dynamical derivation of quantum measurement from the classical precursor`.

`future-measurement reparameterization covariance != clock-change x reparameterization compatibility`.

### Stage 11E — clock-change × parameterization compatibility — completed

Criteria **39–43** satisfied. The finite family used **12** external `G` transports and **108** genuine clock transports, yielding **648** event/O squares, **1296** measurement/probability squares, **648** weighted/modal squares, and **648** posterior squares. The wrong path is `noncommuting_wrong_clock_path_detected`.

`Stage 11E clock-change x parameterization compatibility on the frozen finite family = established`.

`internal-clock covariance != reparameterization covariance`.

`commuting typed product square != independent interaction law`.

`commuting typed diagram != general covariance`.

`path-independent future probabilities != future actuality`.

`path-independent evidence update != ontological becoming`.

### Stage 11F — ablation / wrong-gauge / false-positive controls — completed

Criteria **44–47** satisfied. The classifications include `event_correspondence_reconstructible_but_typed_identity_lost`, `lapse_semantics_missing_typed_claim_not_established`, and `wrong_lapse_jacobian_numerically_refuted`. The wrong lapse changes the tested value/derivative by approximately **0.5357142857142857**.

The consolidated family retains orientation reversal (**12** decreasing steps), non-injective square (**6** collisions), the `invalid_equal_raw_parameter_event_rule`, parameter-dependent O/P/R/V corruption (**4 / 4**), and **7 / 7** rejected controls.

`Stage 11F typed-resource ablation and wrong-gauge false-positive controls = established on the frozen finite family`.

`reconstructible != universally redundant`.

`lost != metaphysically irreducible`.

`wrong-gauge failure != ontological becoming`.

`finite-model ablation != fundamental ontology`.

### Stage 11G — synthesis and evidence-selected next gate — completed

Criteria **48–49** satisfied. The complete Stage 11A–F evidence selects `parametrized_covariant`.

`Stage 11 finite typed parametrized covariance status = parametrized_covariant`.

Stage 12 candidate ranking was:

| rank | gate | score |
| --- | --- | ---: |
| 1 | `multi_orbit_constraint_gauge_atlas` | **10** |
| 2 | `richer_causal_order` | **7** |
| 3 | `nonideal_povm_clocks` | **6** |
| 4 | `gravitational_minisuperspace_extension` | **5** |

Selected Stage 12 gate:

> **Construct a multi-orbit constraint-generated gauge atlas that separates gauge-related parameterizations from physically distinct orbits and tests whether relational/Dirac observables and the typed O/P/R/V measurement architecture descend consistently across that atlas.**

`one-orbit covariance != multi-orbit gauge covariance`.

`external parameterization independence != diffeomorphism invariance`.

`constraint-generated gauge precursor != general relativity`.

### Stage 11 criterion 50 — external final repository validation / merge-readiness review — completed

Criterion 50 was satisfied at reviewed head `6b5ae9ffb2f1fe784080d9d2a02e349430d4f01a`. GitHub Actions run **#1469** passed **`938 passed in 682.23s (0:11:22)`**. PR #12 was mergeable at the reviewed checkpoint and was subsequently merged into `main` at `d5fdc899a72b6a983c03b1f960c65cda948c8fb8`.

Stage 11 criteria **1–50** are completed.

`finite typed parametrized covariance != general covariance`.

`absence of preferred external parameterization != absence of ontological becoming`.

`repository validation != new scientific evidence`.

`merge-ready != merged`.

## Stage 12 — Multi-orbit constraint-generated gauge atlas — in progress

### Stage 12.0 — protocol freeze — completed

The freeze separates physical orbit, gauge representative/flow, external parameterization, event, internal clock, modal continuation, and measurement roles. It fixes four canonical orbit controls and the rule

`quotient invariance without physical-orbit discrimination != successful multi-orbit gauge atlas`.

### Stage 12A — multi-orbit constrained carrier and explicit gauge-flow representatives — completed

Criteria **11–16** satisfied. Four physical orbits × five sampled representatives give **20 representatives** and **80** ordered nonidentity same-orbit `Phi_s` transports; the Stage 11 four-parameterization family gives **16** external views. Run #1508 passed **`963 passed in 680.97s (0:11:20)`**.

`constraint-generated gauge flow != external reparameterization by definition`.

### Stage 12B — Dirac/relational observables and physical-orbit discrimination — completed

Criteria **17–23** satisfied. Independent `Q_D=q-pT`, `P_D=p` reconstruction gives 20 representative and 16 external estimates; all six distinct orbit pairs remain distinct under the full pair. There are **144** relational `q(T=tau)` and **232** derivative evaluations; **30 equal-T**, **2 equal-q**, and **312 equal-raw-lambda** cross-orbit coincidences are rejected. Run #1528 passed **`973 passed in 677.85s (0:11:17)`**.

`Dirac invariant != timeless ontology by definition`.

`Dirac-invariant data + relational change != proof of eternalism`.

`relational change != ontological becoming by definition`.

### Stage 12C — typed gauge atlas, quotient, and descent of relational structure — completed

Criteria **24–31** satisfied. The finite groupoid has **100 typed `Phi` arrows**, **20 identities**, **100 inverse checks**, **500 composition checks**, and **0** licensed cross-orbit arrows. Connectivity yields **4 quotient classes** of size 5, with **16** quotient-level relational/Dirac descent evaluations. Run #1548 passed **`984 passed in 680.36s (0:11:20)`**.

`gauge-representative redundancy + physical-orbit plurality + nontrivial relational change`.

`gauge quotient != elimination of physical change`.

`constraint orbit != modal continuation`.

`finite gauge atlas != diffeomorphism invariance`.

### Stage 12D — O/P/R/V/Xi and orbit-sensitive future-measurement descent — completed

Criteria **32–38** satisfied. All 20 representatives receive typed O/P/R/V/Xi views; quotient projection yields four physical-orbit architectures. The inherited family has **40** per-continuation measurement views / **80** outcome evaluations, 20 weighted views, 20 posterior views, and 20 bounded orbit-sensitive witnesses with **4** signatures. Minimum canonical witness separation is about **0.0057933319**. Run #1570 passed **`994 passed in 562.97s (0:09:22)`**.

`typed bridge to orbit data != dynamical derivation of quantum measurement from the classical constraint`.

`orbit-sensitive witness != empirical prediction`.

### Stage 12E — internal clock × external parameterization × gauge-flow compatibility — completed

Criteria **39–43** satisfied. Stage 12E keeps **108** `C`, **12** `G`, and **80** nonidentity `Phi` transports distinct. It checks **8,640 C × Phi** squares / **17,280** paths, **1,920 G × Phi** squares / **3,840** paths, and **5,184 C × G × Phi** cubes / **31,104** order paths. Run #1592 passed **`1002 passed in 887.98s (0:14:47)`**.

`internal-clock covariance != external-reparameterization covariance`.

`constraint-generated gauge flow != internal-clock change`.

`constraint-generated gauge flow != external reparameterization`.

`path-independent future probabilities != future actuality`.

`finite three-way compatibility != diffeomorphism invariance`.

### Stage 12F — ablation / wrong-orbit / false-positive controls — completed

Criteria **44–47** satisfied. Two orbit-resource ablations remain numerically `reconstructible` while typed identification is `lost` and covariance is `not_established`. The consolidated matrix has **27 / 27** rejected controls, including **5** representative-dependent O/P/R/V/measurement corruptions and an orbit-insensitive measurement clone.

Source run #1596 produced **`1 failed, 1009 passed in 696.32s (0:11:36)`** only because of exact float equality in one test. The Stage 12F source was unchanged when that assertion was made tolerance-aware. Final Stage 12F checkpoint head `68f50acacc4b18f7f646ddc912a8e2791e24cded`, run **#1612**, passed **`1011 passed in 692.53s (0:11:32)`** and supersedes #1596.

`numerical reconstructibility != typed operational identification`.

`reconstructible != universally redundant`.

`lost != metaphysically irreducible`.

`wrong-gauge failure != ontological becoming`.

`cross-orbit mismatch != temporal succession or ontological becoming`.

`false-positive rejection != proof of eternalism`.

### Stage 12G — executable synthesis and evidence-selected next gate — completed

Criteria **48–49** satisfied. The full Stage 12A–F diagnostic snapshot selects exactly one frozen status:

`multi_orbit_gauge_covariant`.

Bounded structural synthesis:

`gauge-representative redundancy + physical-orbit plurality + Dirac-invariant orbit data + nontrivial relational change + quotient-level typed operational descent`.

This result does not identify gauge quotienting with elimination of change and does not decide eternalism/blockness versus ontological becoming.

Stage 13 candidate ranking:

| rank | gate | score |
| --- | --- | ---: |
| 1 | `multi_constraint_refoliation_precursor` | **10** |
| 2 | `gravitational_minisuperspace_extension` | **7** |
| 2 | `richer_causal_order` | **7** |
| 4 | `nonideal_povm_clocks` | **6** |

Selected Stage 13 gate:

> **Construct a minimal multi-constraint constraint-algebra/refoliation precursor with at least two nontrivially related first-class constraint directions, and test whether the Stage 12 physical-orbit quotient, relational observables, and typed O/P/R/V measurement architecture remain compatible under the resulting constraint-generated path structure without assuming general relativity.**

The nearest unresolved assumption is the single Hamiltonian constraint. The selected gate isolates nontrivial constraint-algebra effects before introducing a dynamical gravitational carrier.

Stage 12 criteria **1–49 are satisfied and criterion 50 is next**.

`multi_orbit_gauge_covariant finite family != general covariance`.

`finite constraint-generated gauge atlas != diffeomorphism invariance`.

`finite C x G x Phi compatibility != refoliation invariance`.

`single Hamiltonian constraint != hypersurface-deformation algebra`.

`constraint-algebra/refoliation precursor != general relativity`.

### Next: Stage 12 criterion 50 — external final repository validation / merge-readiness review

Criterion 50 must review the final current head, full-repository regression, branch/base state, PR mergeability, and review blockers. A successful criterion-50 review is repository evidence, not new scientific evidence.

## Later directions

After the selected Stage 13 constraint-algebra/refoliation precursor, a gravitational/minisuperspace extension, richer causal order, and nonideal/POVM clocks remain live candidates rather than rejected directions. Empirical relevance should be pursued only if a genuinely discriminating prediction emerges beyond the chosen representation.

## Cautions

- `operational quantum equality != modal/ontological identity`;
- `directional record arrow != ontological becoming`;
- `future-measurement covariance != future actuality`;
- `measurement covariance != modal/ontological identity`;
- `perspective-invariant future probabilities != proof of eternalism`;
- `measurement covariance != refutation of ontological becoming`;
- `typed-resource necessity != metaphysical fundamentality`;
- `parameter label != internal clock reading`;
- `parameter label != event identity`;
- `internal clock perspective != external parameterization`;
- `orientation-preserving reparameterization != time reversal`;
- `equal raw lambda != physical-event correspondence`;
- `same relational orbit != same metaphysics`;
- `same constraint orbit != established general covariance`;
- `relational covariance on one finite orbit != general covariance`;
- `typed O/P/R/V/Xi lift != full future-measurement covariance`;
- `typed product lift feasibility != independent dynamical covariance evidence`;
- `Stage 10 event-role bridge != dynamical identification of quantum and classical carriers`;
- `selector-free public projection != absence of privileged modal semantics`;
- `external lapse != quantum measurement normalization form`;
- `typed Stage 10/11 bridge != dynamical derivation of quantum measurement from the classical precursor`;
- `future-measurement reparameterization covariance != clock-change x reparameterization compatibility`;
- `internal-clock covariance != reparameterization covariance`;
- `commuting typed product square != independent interaction law`;
- `commuting typed diagram != general covariance`;
- `path-independent future probabilities != future actuality`;
- `path-independent evidence update != ontological becoming`;
- `numerical reconstructibility != typed operational identification`;
- `reconstructible != universally redundant`;
- `lost != metaphysically irreducible`;
- `missing typing != metaphysical absence`;
- `wrong-gauge failure != ontological becoming`;
- `typed-resource necessity in this finite family != metaphysical fundamentality`;
- `finite-model ablation != fundamental ontology`;
- `parametrized_covariant finite family != general covariance`;
- `external parameterization independence != diffeomorphism invariance`;
- `one-orbit covariance != multi-orbit gauge covariance`;
- `constraint-generated gauge precursor != general relativity`;
- `parameterization-covariant future probabilities != future actuality`;
- `parameterization-covariant future probabilities != proof of eternalism`;
- `absence of preferred external parameterization != absence of ontological becoming`;
- `finite clock covariance != general covariance`;
- `finite typed parametrized covariance != general covariance`;
- `parametrized covariance precursor != general relativity`;
- `constraint-generated gauge flow != ontological becoming`;
- `different physical orbit != later event on one orbit`;
- `Dirac invariant != timeless ontology by definition`;
- `Dirac-invariant data + relational change != proof of eternalism`;
- `relational change != ontological becoming by definition`;
- `gauge quotient != elimination of physical change`;
- `constraint orbit != modal continuation`;
- `operational quotient descent != modal/ontological identity`;
- `same gauge-invariant probability within an orbit != all physical orbits operationally identical`;
- `typed bridge to orbit data != dynamical derivation of quantum measurement from the classical constraint`;
- `orbit-sensitive witness != empirical prediction`;
- `commuting finite gauge/clock diagrams != general covariance`;
- `internal-clock covariance != external-reparameterization covariance`;
- `constraint-generated gauge flow != internal-clock change`;
- `constraint-generated gauge flow != external reparameterization`;
- `path-independent relational outputs != ontological becoming`;
- `finite three-way compatibility != diffeomorphism invariance`;
- `cross-orbit mismatch != temporal succession or ontological becoming`;
- `false-positive rejection != proof of eternalism`;
- `finite gauge atlas != diffeomorphism invariance`;
- `multi-orbit gauge covariance != general covariance`;
- `multi_orbit_gauge_covariant finite family != general covariance`;
- `finite constraint-generated gauge atlas != diffeomorphism invariance`;
- `finite C x G x Phi compatibility != refoliation invariance`;
- `single Hamiltonian constraint != hypersurface-deformation algebra`;
- `constraint-algebra/refoliation precursor != general relativity`;
- `finite-model success != empirical discovery`;
- `repository validation != new scientific evidence`;
- `merge-ready != merged`.
