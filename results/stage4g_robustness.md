# Stage 4G — Robustness Results

Status: **completed**.

Stage 4G applies the Stage 4A--F identities jointly rather than adding a new mechanism.

## Dimension sweep

For generic normalized complex physical states, the combined structural residual suite passes at:

`d=3,4,5,6`.

The suite includes constraint satisfaction, ideal clock probability `1/d`, physical round-trip reconstruction, expected unitary transitions, transition composition, and global/local Born consistency.

All tested residuals remain within the frozen `1e-10` tolerance.

## Coefficient-family sweep

At `d=4`, the same joint suite passes for:

- equal-amplitude coefficients;
- two distinct generic complex coefficient families;
- a sparse coherent two-sector state.

Thus the equal-amplitude full-spectrum state is not required for the Stage 4 structural identities.

The two-sector state:

`(|0,0>+|1,1>)/sqrt(2)`

shows nontrivial ray evolution over the finite clock cycle, while the single-sector physical state `|1,1>` remains the same ray at every reading.

This supports the narrower toy-family distinction:

`multi-sector coherent support can yield nontrivial relative ray change`

while:

`single-sector support yields only phase change`.

## Origin shifts

The combined suite passes for common clock origins:

`-0.73`, `0`, `0.37`, and `5.2`.

Local vector representatives change, but the relative transition structure and operational consistency survive.

## Bookkeeping relabeling

Arbitrary unique labels are attached to fixed clock indices without changing the physical clock states. The relabeled transition matrices match the native matrices for every ordered pair, and the composition law remains valid for every relabeled triple.

Therefore:

`bookkeeping clock label != physical relational content`.

This is not a change of physical clock subsystem.

## Global phase

For:

`|Psi'>=exp(i theta)|Psi>`,

Stage 4G verifies that:

- the shifted state remains physical;
- the DFT clock probability profile is unchanged;
- all clock-relative density matrices are unchanged;
- tested global conditional Born probabilities are unchanged;
- tested local Born probabilities are unchanged.

Thus vector representatives are not themselves the invariant operational object.

## Validation

Focused Stage 4G tests: **12**.

Clean PR merge-ref code/test checkpoint:

`255 passed in 4.46s`.

## Strongest supported Stage 4G result

**within the tested finite matched-energy Page--Wootters-style family, the constrained physical structure and its reversible DFT-clock-relative transition/operational relations are stable under the tested finite-dimension changes, generic and sparse coefficient choices, common clock-origin changes, global phase, and pure bookkeeping relabeling.**

The strongest surviving candidate is therefore relational and map-based rather than an absolute clock value or a particular ket representative.

This does not establish a fundamental invariant of physical time. An actual change of the physical clock subsystem is deferred to Stage 5.
