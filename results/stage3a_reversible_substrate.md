# Stage 3A — Reversible Record Substrate

Status: **completed**.

## Purpose

Stage 3A establishes only the reversible finite substrate required for later record diagnostics. It does **not** measure or claim a temporal arrow.

The canonical complete microstate is:

`Z=(X,M,N)`

with three bits and therefore eight total microstates.

## Reversible maps

The protocol-frozen maps are:

`U_rec(X,M,N)=(X,M XOR X,N)`

and:

`U_scr(X,M,N)=(X XOR N,M,N)`.

Both maps are permutations of the full eight-state microstate space and are self-inverse:

`U_rec^{-1}=U_rec`

`U_scr^{-1}=U_scr`.

A non-bijective erasure-map control is rejected when reversibility is claimed.

## Exact canonical ensemble

The Stage 3 boundary distribution is represented exactly using rational weights:

`X_0=a`

`M_0=0`

`N_0=b`

with independent uniform bits `a,b`.

Thus the initial support contains four complete microstates, each with probability `1/4`.

Stage 3A treats this only as a declared boundary ensemble. The blank-memory condition is not yet interpreted as a record arrow; that interpretation is reserved for Stage 3C after the diagnostics are defined.

## Forward trajectories

Each initial microstate generates:

`z_1=U_rec(z_0)`

`z_2=U_scr(z_1)`.

The canonical ensemble therefore contains four equiprobable complete trajectories. Every trajectory satisfies the declared forward dynamics.

Representative trajectories are:

- `(0,0,0) -> (0,0,0) -> (0,0,0)`
- `(0,0,1) -> (0,0,1) -> (1,0,1)`
- `(1,0,0) -> (1,1,0) -> (1,1,0)`
- `(1,0,1) -> (1,1,1) -> (0,1,1)`

where each triple denotes `(X,M,N)`.

## Modeled history reversal

History reversal is:

`J(z_0,z_1,z_2)=(z_2,z_1,z_0)`.

The reversed ensemble is constructed as the exact pushforward `J_* mu_fwd`.

Every reversed trajectory satisfies the inverse dynamics in reverse map order:

`z_1=U_scr^{-1}(z_2)`

`z_0=U_rec^{-1}(z_1)`.

Because both maps are self-inverse, this condition is checked directly. Applying `J` twice returns the original trajectory and applying ensemble reversal twice returns the original exact ensemble.

This is a modeled-history transformation, not Python loop reversal.

## Full-state information preservation

At every neutral trajectory position, the exact full-state marginal contains four states with probability `1/4` each.

Therefore:

`H(Z_0)=2 bits`

`H(Z_1)=2 bits`

`H(Z_2)=2 bits`.

Thus:

`H(Z_0)=H(Z_1)=H(Z_2)`.

The reversed ensemble carries the corresponding reversed entropy profile, which is also `(2,2,2)`.

This verifies full-state Shannon entropy preservation for the canonical exact ensemble under the reversible maps. It does **not** yet analyze subsystem entropies or record correlations; those belong to Stage 3B.

## Validation

The committed Stage 3A test file contains **10 focused tests** covering:

1. exact eight-state microstate space and bit validation;
2. `U_rec` bijectivity and self-inverse behavior;
3. `U_scr` bijectivity and self-inverse behavior;
4. rejection of a non-bijective map when reversibility is claimed;
5. exact four-state canonical boundary distribution;
6. four equiprobable dynamically valid forward trajectories;
7. involutive history reversal and inverse-map reverse dynamics;
8. full-state probability-mass and entropy preservation;
9. reversed-ensemble entropy preservation;
10. invalid ensemble weights and position indices.

The Stage 3 branch will be checked by GitHub Actions after the Stage 3 tracking PR is opened.

## Interpretation

The strongest justified Stage 3A conclusion is:

**the canonical Stage 3 substrate is a closed finite model with explicitly reversible microscopic maps and exact forward/reversed trajectory ensembles.**

Stage 3A does not establish:

- a record relation;
- a preferred temporal orientation;
- entropy production;
- a thermodynamic arrow;
- phenomenal passage.

The next step, Stage 3B, adds exact information-theoretic and decoder-based record diagnostics without yet assuming that the lower-index side is the past.
