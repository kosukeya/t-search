# Stage 11F Result — Ablation / Wrong-Gauge / False-Positive Controls

Status: **criteria 44–47 satisfied by executable diagnostics; Stage 11F source/unit-test checkpoint completed.**

Stage 11E final repository baseline: run #1421 — **`916 passed in 589.69s (0:09:49)`**.

Stage 11F source/unit-test checkpoint: run #1425 — **`924 passed in 586.95s (0:09:46)`**.

## Executable classifications

Stage 11F separates numerical payload, typed identification, and the status of the covariance claim.

### Parameter-event correspondence removed

Classification:

`event_correspondence_reconstructible_but_typed_identity_lost`.

Observed structure:

- numerical payload: `reconstructible`;
- typed identification: `lost`;
- covariance status: `not_established`;
- unchanged O relational-q residual: **0.0**.

O still carries the `e1/e2` role-to-physical-event rows after Xi event correspondence is removed, so the mapping can be reconstructed from the retained public payload. Stage 11C/11D validators nevertheless reject the ablated architecture as a well-typed cross-representation context.

Therefore

`numerical reconstructibility != typed operational identification`.

`reconstructible != universally redundant`.

### Lapse/Jacobian semantics removed

Classification:

`lapse_semantics_missing_typed_claim_not_established`.

The correct cubic numerical lapse remains stored. The relational derivative remains

`dq/dT = p = 1.25`

with numerical derivative residual **0.0**, while the Xi transformation semantics are absent and Stage 11D rejects the typed lapse/Jacobian context.

Observed structure:

- numerical payload: `preserved`;
- typed identification: `underdetermined`;
- covariance status: `not_established`.

### Wrong lapse/Jacobian value

Classification:

`wrong_lapse_jacobian_numerically_refuted`.

At the frozen Stage 11B target event the source label is `lambda=1`. Hence

- seed/identity lapse: `1.25`;
- cubic Jacobian: `1.75`;
- correct cubic lapse: `1.25/1.75 = 0.7142857142857143`;
- deliberately reused identity lapse: `1.25`;
- lapse-value residual: approximately **0.5357142857142857**.

Using the wrong lapse with the unchanged cubic raw rate changes the reconstructed `dq/dT` from `1.25` to approximately `0.7142857142857143`, giving relational-derivative residual approximately **0.5357142857142857**.

Observed structure:

- numerical payload: `corrupted`;
- typed identification: `lost`;
- covariance status: `refuted` for this tested construction.

Thus

`missing semantics != wrong numerical gauge data`.

`not_established != refuted`.

## Consolidated false-positive controls

The executable Stage 11F control family contains **7** members, and **7 / 7** are rejected:

1. orientation reversal `f_rev(lambda)=-lambda` — classified `orientation_reversal_outside_positive_family`; all **12** raw-label steps of the 13-event sample decrease;
2. non-injective square `f_noninj(lambda)=lambda^2` — classified `noninjective_relabeling_rejected`; **6** collisions occur among the 13 both-sign source labels;
3. raw-equal-parameter event matching — retains Stage 11B classification `invalid_equal_raw_parameter_event_rule`; **6** equal-label matches are false physical-event identifications;
4. parameter-dependent O corruption — detected;
5. parameter-dependent P corruption — detected;
6. parameter-dependent R corruption — detected;
7. parameter-dependent V corruption — detected.

The four O/P/R/V controls remain **4 / 4** detected and classified

`parameter_dependent_oprv_corruption_detected`.

These witnesses prevent the control family from reducing to metadata flags alone.

## Criteria 44–47

44. Removing parameter-event correspondence is classified separately from numerical reconstructibility — **satisfied**.
45. Missing/wrong lapse-Jacobian semantics are classified separately and have explicit witnesses — **satisfied**.
46. Orientation reversal, non-injective relabeling, raw-lambda matching, and parameter-dependent corruption have explicit false-positive controls — **satisfied**.
47. Ablation/control results are not promoted to metaphysical fundamentality or ontological becoming — **satisfied**.

Bounded Stage 11F result:

`Stage 11F typed-resource ablation and wrong-gauge false-positive controls = established on the frozen finite family`.

## Interpretation boundary

- `numerical reconstructibility != typed operational identification`;
- `reconstructible != universally redundant`;
- `lost != metaphysically irreducible`;
- `missing typing != metaphysical absence`;
- `wrong-gauge failure != ontological becoming`;
- `typed-resource necessity in this finite family != metaphysical fundamentality`;
- `finite-model ablation != fundamental ontology`;
- `finite-model ablation != theorem about reality in general`;
- `not_established != false`;
- `repository validation != new scientific evidence`.

Next checkpoint: **Stage 11G — synthesis and evidence-selected next gate.**
