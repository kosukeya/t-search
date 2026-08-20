# Stage 4G — Robustness and Synthesis Notes

Status: **robustness implementation complete; Stage 4 synthesis / exit review in progress**.

## Purpose

Stage 4G does not introduce a new Page--Wootters mechanism. It applies the Stage 4A--F identities as a joint cross-check suite and asks which structures survive modest changes of finite dimension, physical coefficient family, clock-origin convention, global phase, and bookkeeping labels.

The principal guard is:

`robust under tested representation changes != fundamental invariant of physical time`.

A change of the physical clock subsystem is still deferred to Stage 5.

## Cross-check summary

`Stage4RobustnessSummary` combines the following residuals for one normalized physical state:

- zero-constraint residual;
- deviation of every ideal DFT clock probability from `1/d`;
- maximum physical reduction/reconstruction round-trip residual;
- maximum residual between `T_{k<-j}` and `exp[-i H_S(t_k-t_j)]`;
- maximum transition-composition residual;
- maximum global/local conditional Born residual for `Pi_+=|+><+|`.

All are required to remain below the frozen `1e-10` tolerance.

## Dimension robustness

The joint summary passes for generic complex physical states at:

`d=3,4,5,6`.

Thus the principal Stage 4 identities are not artifacts of the canonical `d=4` choice within this modest finite family.

This does not establish a continuum-clock limit or realistic clock quality.

## Coefficient-family robustness

At `d=4`, the joint summary passes for:

- equal-amplitude coefficients;
- multiple generic complex coefficient vectors;
- a sparse two-sector coherent state.

The equal-amplitude full-spectrum state is therefore a convenient baseline, not a necessary ingredient for the tested structural identities.

The two-sector state:

`(|0,0>+|1,1>)/sqrt(2)`

has nontrivial clock-relative ray change. In the canonical `d=4` cycle its reference-ray deficit reaches `1` at an opposite reading.

By contrast, the single-sector state `|1,1>` has zero ray-change deficit at every reading.

The supported refinement is:

`single-sector support -> phase-only local vector change`

while:

`multi-sector coherent support can produce nontrivial relational ray change`.

Do not generalize this pure matched-energy toy-family statement into a universal claim that entanglement creates physical time.

## Clock-origin robustness

The joint summary passes for multiple origins, including negative and non-grid shifts:

`alpha in {-0.73, 0, 0.37, 5.2}`.

Individual local vector representatives change under a common origin shift, while the local-to-local transition family continues to depend only on relative clock separation.

## Bookkeeping relabeling

`ClockLabeling` attaches arbitrary unique strings to the fixed neutral clock indices without changing their physical order or clock states.

Examples intentionally use labels whose lexical order differs from neutral index order.

For every source/target pair:

`T'_{rho(k)<-rho(j)} = T_{k<-j}`

when the relabeling is applied consistently.

Composition also remains:

`T'_{rho(l)<-rho(k)} T'_{rho(k)<-rho(j)} = T'_{rho(l)<-rho(j)}`.

This is bookkeeping covariance only. It is not a physical clock change or a quantum-reference-frame transformation.

## Global phase robustness

For:

`|Psi'>=exp(i theta)|Psi>`,

physicality and clock-outcome probabilities are unchanged. Each local vector acquires the same global phase, so all local density matrices and tested Born probabilities remain unchanged.

Therefore:

`global vector representative != physical ray / operational content`.

This extends the Stage 4F vector/ray guard from local phase-only evolution to the global constrained description itself.

## Robustness checkpoint

Focused Stage 4G tests: **12**.

Clean PR merge-ref after Stage 4G code/tests:

`255 passed in 4.46s`.

## Strongest Stage 4G robustness statement

**within the tested finite matched-energy family, the zero-constraint physical structure, reversible DFT-clock reduction, relative unitary transition family, composition consistency, uniform ideal clock probabilities, and global/local Born agreement survive modest changes of finite dimension, generic/sparse physical coefficients, common clock-origin convention, global phase, and pure bookkeeping labels.**

The robust object is therefore not an absolute clock label or a particular vector representative. The strongest surviving candidate is the relational family of maps and operational predictions tied consistently to the constrained physical subspace.

This remains a toy-model representation result. Stage 5 must still test whether an analogous structure survives an actual change of physical clock subsystem.
