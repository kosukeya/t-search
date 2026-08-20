# Stage 4A — Finite Clock Kinematics

Status: **completed**.

Canonical fixture: `d_C=d_S=4`, `H_S=diag(0,1,2,3)`, `H_C=diag(0,-1,-2,-3)`, and `dim(H_kin)=16`.

The DFT clock basis

`|t_j>=(1/sqrt(d)) sum_n exp(i n t_j)|n>`

with `t_j=2*pi*j/d` is orthonormal within the frozen `1e-10` tolerance. Direct numerical cross-checks give a canonical Gram residual of about `1.17e-16`.

Clock translation satisfies

`exp(-i H_C Delta)|t_j>=|t_{j+1 mod d}>`, `Delta=2*pi/d`,

with canonical maximum one-step residual about `3.67e-16`. After `d` steps the unitary returns to identity; for `d=4` the maximum residual is about `7.35e-16`.

The same identities were checked for a non-grid origin shift and for `d=5`, with residuals below `1e-15`.

`tests/test_stage4a_clock_kinematics.py` contains 12 focused tests, including invalid-input guards.

Stage 4A establishes only a consistent finite periodic clock kinematics. It does not yet establish a Page--Wootters constraint, physical state, conditional dynamics, emergent time, or a temporal arrow.

Next: Stage 4B introduces `H_tot=H_C tensor I_S + I_C tensor H_S` and tests the constrained physical subspace.