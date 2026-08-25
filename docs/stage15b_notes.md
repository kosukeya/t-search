# Stage 15B Notes — Local/Smeared Path Closure and Compensation

Status: **validated Stage 15B scientific checkpoint; criteria 18–24 satisfied. Stage 15C follows.**

Incoming Stage 15A checkpoint: `e53dadffbf94257ef15d37b2a817cfa4caa05913`.

Validated Stage 15B scientific checkpoint: `54d508ea432953e966809677c736253ab9930d0d`, GitHub Actions run #1956, **`1193 passed in 890.90s`**.

## Question tested

Stage 15B asks whether the finite local and constant-smeared Hamiltonian flows of the frozen three-site carrier preserve the positive constraint surface and physical payload, and whether different noncommuting orderings close after the algebraically required `C_2` compensation.

The tested presented algebra remains

`{C_0,C_1}=-0.25 T_0 C_2`,

`{C_0,C_2}=0`,

`{C_1,C_2}=0`.

## Finite local flows

The executable implementation is `src/t_search/stage15_paths.py`.

Across the 108 positive representatives:

- single local-flow probes: **648**;
- single constant-smeared-flow probes: **864**;
- canonical same-orbit mixed local pairs: **864**;
- ordered local path results (`012` and `102`): **1728**.

All tested exact finite flows remain on the frozen positive constraint surface and preserve the carried `(Q_D,P_D)` payload within the declared tolerance.

## Local ordering defect and compensation

Among the 864 canonical local mixed pairs:

- nonzero compensator-difference cases: **576**;
- exact zero-defect cases: **288**.

The two path words are not identified at the raw word level. Instead, each ordering receives its own algebraically derived final `C_2` compensation and is compared with the same declared target representative.

Wrong-sign, half-strength, missing, and unjustified shared-compensator controls are rejected on the nonzero-defect family, while the zero-defect family remains explicitly compatible with a shared compensator.

`raw local path-word inequality != physical path dependence`.

## Constant-smeared ordering

The frozen smearing family includes compact `{0,1}`, compact `{1,2}`, full-support, and zero-wedge controls.

Across all positive representatives:

- smeared ordering probes: **540**;
- nonzero predicted `C_2` defects: **432**;
- exact zero-wedge controls: **108**.

The predicted integrated `C_2` defect closes the tested orderings rather than being inferred from the endpoint after the fact.

The off-surface smeared Jacobi audit contains **2592** ordered probes and retains nonzero individual nested-bracket terms while the cyclic residual cancels within tolerance.

## Criteria 18–24

Stage 15B closes only criteria **18–24**:

18. exact positive-surface local flows;
19. exact constant-smeared flows;
20. canonical local ordering defects and algebraic compensators;
21. local wrong-compensator controls;
22. compact/full smeared ordering defects and predicted compensation;
23. zero-wedge and off-surface smeared Jacobi controls;
24. bounded path interpretation without importing Stage 15C quotient or Stage 15D basis claims.

Criteria **25–50 remain pending at the Stage 15B checkpoint**.

## Bounded result

`Stage 15B local/smeared finite compensated-path closure on the frozen three-site carrier = established`.

This does not establish a physical quotient theorem, a complete Dirac-observable descent theorem, locality-protected non-Abelianity, refoliation invariance, a continuum hypersurface-deformation algebra, general relativity, eternalism, or ontological becoming.

Guards:

- `compensated local-path closure != refoliation invariance`;
- `finite smeared path closure != continuum hypersurface-deformation algebra`;
- `raw path-word inequality != physical path dependence`;
- `payload preservation != complete quotient descent`;
- `Stage 15B path closure != Stage 15D locality obstruction`;
- `repository validation != new scientific evidence`.
