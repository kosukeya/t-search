# Stage 4B — Constrained Global Physical State

Status: **completed at the implementation/focused-test checkpoint**.

Canonical dimensions:

`d_C=d_S=4`, `dim(H_kin)=16`.

The total constraint is:

`H_tot=H_C tensor I_S + I_C tensor H_S`.

With the frozen spectra, the tensor-basis eigenvalue of `|c>_C|s>_S` is `s-c`. The zero-eigenvalue sector is therefore the matched-energy subspace:

`H_phys=span{|0,0>,|1,1>,|2,2>,|3,3>}`.

The numerical zero-eigenspace extracted independently with `numpy.linalg.eigh` has dimension `4`, and its projector agrees with the analytic matched-energy projector at machine precision.

Both the equal-amplitude baseline and a generic normalized complex coefficient state:

`|Psi_c>=sum_n c_n |n>_C|n>_S`

have constraint residual:

`||H_tot|Psi_c>||=0`

within the frozen `1e-10` tolerance.

They are also stationary under the constraint-generated external parameter evolution:

`exp(-i H_tot tau)|Psi_c>=|Psi_c>`

for the tested positive and negative values of `tau`.

Negative control:

`|0>_C|1>_S`

has constraint residual exactly `1` for the canonical spectra and is not stationary. At `tau=0.37`, its stationarity residual is about `0.368`.

The matched-energy kernel structure is also checked at `d=5`, where `dim(H_kin)=25` and `dim(H_phys)=5`.

`tests/test_stage4b_constrained_physical_state.py` contains 12 focused tests, including invalid-input guards.

Stage 4B establishes only:

**a finite global kinematic space containing an explicitly identified constrained physical subspace whose states are stationary under the declared constraint generator.**

It does not yet establish clock-relative conditional dynamics, physical reduction maps, an arrow of time, ontological becoming, or fundamental emergent time.

Next: Stage 4C implements ideal clock conditioning and tests normalized conditional Schrödinger dynamics.
