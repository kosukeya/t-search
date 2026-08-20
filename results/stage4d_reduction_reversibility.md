# Stage 4D — Reduction-Map Reversibility

Status: **completed**.

Canonical `d=4` result:

`P_j^kin=(<t_j| tensor I): H_kin -> H_S`

has shape `4 x 16`, rank `4`, and nullity `12` for every ideal clock reading. It is therefore non-injective on the full kinematic Hilbert space.

An explicit nonzero kernel vector is:

`(|0>_C|2>_S-|1>_C|2>_S)/sqrt(2)`

at `j=0`. Adding this kernel vector to another kinematic vector leaves the clock projection unchanged, giving a constructive many-to-one witness.

By contrast, the normalized physical reduction:

`R_j=sqrt(d) P_j^kin restricted to H_phys`

is unitary in orthonormal physical-basis coordinates:

`R_j^dagger R_j=R_j R_j^dagger=I`.

The explicit reconstruction:

`E_j|phi>=sum_n exp(+i n t_j) phi_n |n>_C|n>_S`

satisfies:

`R_j E_j=I_S`

and:

`E_j R_j=I_phys`.

Generic complex physical-state round trips, system-state round trips, norm preservation, and inner-product preservation all pass within the frozen `1e-10` tolerance.

The full-space composition `E_j sqrt(d) P_j^kin` is not an inverse on `H_kin`: it has rank `4`, not `16`. It becomes identity only after restriction to `H_phys`.

The same structure is checked at `d=5`, where the kinematic projection has rank `5`, nullity `20`, while the physical reduction remains isometric/invertible.

Focused Stage 4D tests: **12**.

Clean PR merge-ref checkpoint after Stage 4D code/tests:

`219 passed in 3.59s`.

Strongest supported Stage 4D statement:

**in the ideal finite matched-energy Page--Wootters-style model, clock conditioning is lossy on the unrestricted kinematic space but becomes information-preserving and explicitly reversible when restricted and normalized on the zero-constraint physical subspace.**

This does not establish that all physical projections are reversible, that no physical information is ever lost, or that time has been shown to fundamentally emerge.

Next: Stage 4E — relational transition structure.
