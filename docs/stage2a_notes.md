# Stage 2A Implementation Notes

This note records one implementation choice that is mathematically compatible with the Stage 2 protocol but worth keeping explicit.

The protocol writes the neutral substrate as:

`T = (E,C,H)`.

In code, `BranchingStructure` stores only:

- `E` (`events`);
- `C` (`direct_edges`);
- the distinguished root.

`H` is exposed as a derived property computed from the unique root-to-leaf paths of the validated outward rooted tree.

Reason: independently storing both `C` and `H` would create duplicated model state and permit accidental inconsistency between the edge structure and the declared history family.

This is an implementation normalization, not a change in the mathematical content of Stage 2A.

The current Stage 2A baseline deliberately remains a rooted tree rather than a general DAG. Generalized merge/reconvergence structures can be tested later as robustness/generalization cases if Stage 2 conclusions depend on tree-specific properties.
