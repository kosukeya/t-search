# Stage 12F Notes — Ablation / Wrong-Orbit / False-Positive Controls

Stage 12F pressure-tests the Stage 12A–E positive family rather than adding a new positive dynamics. The central rule is to keep numerical reconstructibility, typed identification, covariance status, and metaphysical interpretation separate.

Incoming repository checkpoint: Stage 12E final head `b035e0a107a6d64b0c17acd8c197aa630ffc13a6`, GitHub Actions run **#1592**, **`1002 passed in 887.98s (0:14:47)`**.

## Ablation classifications

Two explicit orbit-resource ablations are tested.

1. **Remove typed orbit identity/correspondence.** The declared orbit labels are removed, while the independently reconstructed full Dirac pair still recovers four numerical classes of five representatives. Expected classification:

   `orbit_identity_reconstructible_but_typed_correspondence_lost`

2. **Corrupt Xi orbit/quotient correspondence on one representative.** The typed Stage 12D validator must reject the corrupted claim, while the representative phase-space payload still uniquely reconstructs its original physical orbit from `(Q_D,P_D)`. Expected classification:

   `corrupted_orbit_correspondence_numerically_reconstructible_but_typed_claim_lost`

Both are required to have:

- numerical payload: `reconstructible`;
- typed identification: `lost`;
- covariance status: `not_established`.

`numerical reconstructibility != typed operational identification`.

`reconstructible != universally redundant`.

## Consolidated false-positive matrix

Stage 12F consolidates prior controls with explicit evidence-source metadata and adds representative-dependent descent corruptions.

Expected matrix size: **27 controls**, all rejected.

The matrix includes:

- same-`P_D` / different-`Q_D` and same-`Q_D` / different-`P_D` controls;
- equal `T`, equal `q`, and equal raw external-label cross-orbit matches;
- `wrong_Q_D_path`, `wrong_P_D_path`, and forced cross-orbit `Phi`;
- constraint-orbit / modal-continuation conflation;
- Stage 12D wrong orbit/event/class/outcome/normalization controls;
- `orbit_insensitive_measurement_clone`;
- representative-dependent **O/P/R/V/measurement** corruption, one representative at a time;
- Stage 12E mixed-orbit / untyped transport controls;
- inherited orientation-reversal and noninjective external-relabeling controls;
- the false reading `different physical orbit = later temporal succession`.

The three equal-label witness counts carried forward from Stage 12B are expected to remain **30 equal-T**, **2 equal-q**, and **312 equal-raw-lambda** cross-orbit coincidences.

## Representative-dependent descent controls

Stage 12D established same-orbit descent across five representatives. Stage 12F therefore corrupts only one representative while leaving its same-orbit peers canonical:

- O: perturb one relational `q` value;
- P: reverse the `QExt` id ordering;
- R: perturb one directional record score;
- V: perturb one continuation weight;
- measurement: shift the two-outcome probabilities by `±0.05` while preserving total normalization.

The control succeeds only if the corruption is detected as representative-dependent inconsistency. This prevents a positive result from being obtained merely because every representative was generated from one shared payload without an explicit corruption test.

## Interpretation boundary

Every ablation/control carries `metaphysical_claim_status = not_licensed`.

Required guards:

- `numerical reconstructibility != typed operational identification`;
- `reconstructible != universally redundant`;
- `lost != metaphysically irreducible`;
- `missing typing != metaphysical absence`;
- `wrong-gauge failure != ontological becoming`;
- `cross-orbit mismatch != temporal succession or ontological becoming`;
- `finite-model ablation != fundamental ontology`;
- `false-positive rejection != proof of eternalism`;
- `not_established != false`.

A successful Stage 12F therefore licenses only a bounded statement about the frozen finite typed model.

## Stage 12F boundary

Stage 12F closes criteria **44–47** only. It does not select the overall Stage 12 status. That remains the task of **Stage 12G — executable synthesis and evidence-selected next gate**.
