# Stage 11F Result — Ablation / Wrong-Gauge / False-Positive Controls

Status: **executable diagnostics implemented; criteria 44–47 awaiting source/unit-test checkpoint before final closure.**

Stage 11E final repository baseline: run #1421 — **`916 passed in 589.69s (0:09:49)`**.

## Declared classifications

Stage 11F distinguishes numerical payload, typed identification, and covariance status.

### Parameter-event correspondence removed

Target classification:

`event_correspondence_reconstructible_but_typed_identity_lost`.

Expected structure:

- numerical payload: `reconstructible`;
- typed identification: `lost`;
- covariance status: `not_established`.

The intended witness is that O still carries the e1/e2 role-to-physical-event rows even after Xi correspondence is removed, while Stage 11C/11D validators reject the resulting typed context.

### Lapse/Jacobian semantics removed

Target classification:

`lapse_semantics_missing_typed_claim_not_established`.

The numerical Stage 11A/B trajectory and correct stored lapse values remain available, so `dq/dT` should remain numerically reconstructible. The typed transformation claim is nevertheless unavailable.

### Wrong lapse/Jacobian value

Target classification:

`wrong_lapse_jacobian_numerically_refuted`.

The cubic target receives the identity target lapse. The test requires both typed rejection and a nonzero `dq/dT` witness.

## Consolidated false-positive controls

The executable control set contains **7** members:

- orientation reversal;
- non-injective square relabeling;
- raw-lambda event matching;
- parameter-dependent O corruption;
- parameter-dependent P corruption;
- parameter-dependent R corruption;
- parameter-dependent V corruption.

The run must establish explicit numerical/count witnesses for reversal, noninjectivity, and raw-lambda false matching, and must retain **4 / 4** detected O/P/R/V corruption controls.

## Pending source/unit-test result

Criteria 44–47 remain **pending** until the Stage 11F source/unit-test checkpoint succeeds.

No scientific conclusion will be promoted from CI status alone:

`repository validation != new scientific evidence`.

Interpretation guards:

- `numerical reconstructibility != typed operational identification`;
- `reconstructible != universally redundant`;
- `lost != metaphysically irreducible`;
- `missing typing != metaphysical absence`;
- `wrong-gauge failure != ontological becoming`;
- `finite-model ablation != fundamental ontology`;
- `not_established != false`.

Next checkpoint after criteria 44–47 close: **Stage 11G — synthesis and evidence-selected next gate.**
