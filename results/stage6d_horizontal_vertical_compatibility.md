# Stage 6D Results — Horizontal / Vertical Compatibility

Status: **completed**.

## Main result

Stage 6D constructs one executable model containing both:

- horizontal Stage 6C perspective maps `M_{q<-p}`;
- vertical order/conditioning maps `D_p(e2<-e1)`.

The two arrow types are defined separately and connected only through an explicit event correspondence `chi`.

For the canonical event correspondence, the commuting-square condition

`M_{q<-p} D_p = D_q M_{q<-p}`

holds within `1e-10` across the declared canonical family.

## Canonical case

Perspective endpoints:

`C0 -> B2`.

The direct primitive endpoint edge remains absent, as in Stage 6C. Horizontal transport is reconstructed through:

- `C0 -> A0 -> B2`;
- `C0 -> A1 -> B2`;
- `C0 -> A2 -> B2`.

The vertical event domain is:

`e0(0) < e1(1) < e2(3)`.

The explicit canonical correspondence maps each event label to the same event label in the target perspective.

Three horizontal paths times three forward event relations produce **9 commuting squares**. All commute within `1e-10`, and all three order relations are preserved.

## Exhaustive family result

Across all distinct-clock endpoint/readout choices:

- endpoint cases: `54`;
- indirect Stage 6C horizontal paths: `162`;
- explicit forward order-covariance checks: `162`;
- horizontal/vertical commuting squares: `486`;
- order-covariance violations: `0`;
- maximum horizontal bridge residual: `< 1e-10`;
- maximum commuting-square residual: `< 1e-10`.

This establishes compatibility in the declared ideal qutrit family even though the horizontal atlas is partial rather than a complete primitive map table.

## Mismatch control

The canonical `C0 -> A1 -> B2` horizontal path is held fixed.

Only `chi` is changed by swapping target event labels `e1` and `e2` while still declaring the correspondence orientation-preserving.

The horizontal topology is unchanged, but the diagnostics detect the mismatch:

- canonical square residuals remain within tolerance;
- at least one mismatched square residual exceeds tolerance;
- at least one declared order relation fails covariance.

Thus explicit event correspondence contains compatibility information that cannot be recovered from horizontal graph connectivity alone.

## Strongest supported Stage 6D statement

**Within the canonical ideal three-clock qutrit family, the partial perspective atlas of Stage 6C can be combined with a separately typed reversible vertical conditioning structure such that all 486 declared horizontal/vertical squares commute within tolerance under an explicit orientation-preserving event correspondence, with zero order-covariance violations. A deliberately wrong event correspondence breaks square and order covariance without changing the horizontal atlas, showing that cross-perspective event identification is an independent compatibility datum rather than something determined merely by the existence or connectivity of perspective maps.**

This is a bounded structural covariance result for the toy model, not an identification of perspective change with temporal succession.

## Structural consequence for T6

Stage 6B supplied non-implications between several temporal roles. Stage 6C showed that the perspective layer can be partial yet reconstructible. Stage 6D now adds a positive relation:

`P` and `O` need not collapse into one notion in order to satisfy a strong compatibility condition.

The current evidence therefore favors treating `Xi` — compatibility data among typed layers — as substantive rather than decorative in the provisional container:

`T6=(O,P,R,V,Omega;Xi)`.

This still does not establish that `Xi` is metaphysically fundamental or irreducible. Stage 6F must test redundancy and reconstructibility before such a conclusion could be considered.

## Interpretation boundary

Stage 6D does not establish:

- `perspective change = temporal succession`;
- `physical clock change = phenomenal passage`;
- that the chosen vertical unitary family is a fundamental law of nature;
- that an explicit `chi` is unique;
- that every nonideal or interacting clock system admits such commuting squares.

## Validation

Stage 6D focused tests: **14**.

PR merge-ref checkpoint:

`395 passed in 29.42s`.

## Next pressure test

Stage 6E — record and modality transport.

Stage 6E should test how record orientation, accessibility, and Potentiality/extension structure transform under explicit perspective/event correspondence while preserving the Stage 2 underdetermination boundary and the guard:

`record transport != phenomenal passage`.
