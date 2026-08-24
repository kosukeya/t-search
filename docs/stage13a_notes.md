# Stage 13A Notes — Two-Constraint First-Class Carrier and Finite Representative Family

Status: **implementation complete; criteria 11–16 close only after the Stage 13A executable/test family passes repository CI.**

Incoming Stage 13.0 checkpoint: head `898f36682b3cadac4abd953ba1bac8e32f17103e`, GitHub Actions run #1672, **`1039 passed in 542.21s (0:09:02)`**.

## Question

Stage 13A asks whether the Stage 13.0 frozen six-dimensional carrier can actually be realized as a finite two-constraint first-class system with two independent gauge directions while retaining the four Stage 12 physical initial-data classes.

It does **not** yet test reordered two-generator paths or the compensator law. Those are Stage 13B questions.

## Implemented positive carrier

Canonical coordinates are

`(T,p_T; X,p_X; q,p)`.

The frozen constraints are implemented as

`K_T = p_T + p^2/2`,

`K_X = exp(T)(p_X + 0.5p)`.

The 36 positive representatives use

`p=P_D`,

`q=Q_D+P_D T+0.5X`,

`p_T=-P_D^2/2`,

`p_X=-0.5P_D`,

for the four Stage 12 `(Q_D,P_D)` classes and the `3 x 3` grid

`T,X in {-1,0,1}`.

This gives exactly **9 representatives per orbit / 36 total**.

## Independent constraint / generator directions

The implementation evaluates both the two constraint gradients and the two Hamiltonian generator vectors at every positive representative.

In coordinate order `(T,p_T,X,p_X,q,p)`, the gradients are

`grad K_T = (0,1,0,0,0,p)`,

`grad K_X = (K_X,0,0,exp(T),0,0.5exp(T))`.

On the positive surface `K_X=0`, the second row still has a nonzero `p_X` component `exp(T)`, while the first row has a unit `p_T` component. The executable test therefore requires rank **2** everywhere rather than inferring independence merely from two different constraint labels.

The minimum singular value over the frozen finite family is approximately **0.3778026573**, comfortably above the Stage 13A tolerance `1e-10`.

`two constraint labels != two independent gauge directions`.

## First-class bracket

The canonical Poisson bracket is evaluated directly from analytic gradients and must satisfy

`{K_T,K_X} = -K_X`.

Testing only the positive surface would reduce this to the weak identity `0=0`, so Stage 13A also creates **36 off-surface bracket probes** by perturbing `p_T`, `p_X`, and `q`. Every probe has nonzero `K_X`, allowing the same bracket identity to be checked with a nonzero right-hand side.

This is still a finite toy-carrier closure test:

`first-class closure on this toy carrier != hypersurface-deformation algebra`.

## Single-generator licensed transports

Stage 13A tests each generator separately.

### `Phi_T`

A licensed `Phi_T` path keeps `X` fixed and changes `T` by

`s=T_target-T_source`.

It checks

`T' = T+s`,

`q' = q+ps`,

with `X,p,p_T,p_X` unchanged on the positive surface.

There are **72** ordered nonidentity `Phi_T` transports.

### `Phi_X`

A licensed `Phi_X` path keeps `T` fixed and uses

`u=(X_target-X_source)/exp(T)`.

It checks

`X' = X+exp(T)u`,

`q' = q+0.5exp(T)u`,

and the full Hamiltonian expression

`p_T' = p_T-u K_X`.

Because licensed sources satisfy `K_X=0`, `p_T` remains unchanged on the positive family. There are **72** ordered nonidentity `Phi_X` transports.

Thus Stage 13A checks **144 single-generator transports total**.

The deterministic implementation gives maximum endpoint residuals of approximately **2.22e-16** for both generator families and zero positive-surface constraint residual within floating precision.

## Stage 13B family reserved but not yet tested

The source enumerates the protocol-frozen **144 ordered mixed pairs** for which both `T` and `X` change. It does not yet construct or compare the two reordered path words.

That boundary is explicit:

`Stage 13A single-generator surface preservation != compensated multi-generator path closure`.

The 144 mixed pairs become the canonical positive family in Stage 13B.

## Four physical initial-data classes retained

Stage 13A retains the declared Stage 12 pairs

- `omega_alpha: (-0.35,1.25)`;
- `omega_beta: (0.40,1.25)`;
- `omega_gamma: (-0.35,0.75)`;
- `omega_delta: (0.20,1.75)`.

The same-P/different-Q and same-Q/different-P anti-triviality structure therefore remains present. Stage 13A checks that each class has exactly nine representatives and that no declared initial-data class is accidentally collapsed.

Independent reconstruction and full physical-orbit discrimination from representative data remain Stage 13C work.

## Typed provenance

The carrier keeps distinct roles for

- physical orbit identity;
- gauge representative identity;
- sampled event identity;
- `T` clock coordinate;
- `X` clock coordinate;
- constraint-generator identity;
- constraint-basis presentation.

The generator id is recorded on each transport, while basis and clock roles remain separately typed on each representative.

`constraint-generator identity != physical-event identity`.

`constraint-generator identity != internal-clock perspective`.

## Stage boundary

A successful Stage 13A establishes only a bounded two-constraint first-class carrier and single-generator surface preservation.

It does not yet establish

- noncommuting reordered path behavior;
- correct compensated closure;
- path-word quotient descent;
- two-clock relational covariance;
- O/P/R/V measurement descent;
- refoliation invariance or GR.

## Interpretation guards

- `two constraint labels != two independent gauge directions`;
- `first-class closure on this toy carrier != hypersurface-deformation algebra`;
- `Stage 13A single-generator surface preservation != compensated multi-generator path closure`;
- `constraint-generator identity != physical-event identity`;
- `constraint-generator identity != internal-clock perspective`;
- `multi-constraint carrier != refoliation invariance`;
- `constraint-algebra/refoliation precursor != general relativity`;
- `finite-model success != empirical discovery`.
