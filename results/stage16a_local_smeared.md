# Stage 16A Result — Four-Site Cyclic First-Class Carrier, Exact Local/Smeared Algebra, Support Audits, and Finite Representative Family

Status: **established on the frozen Stage 16A finite carrier; criteria 11–17 satisfied. Criteria 18–50 remain pending.**

Scientific source/test checkpoint:

`20f448e676499ecdab87b890bef79c9e19302832`

PR run #2014 validates merge checkout `bc7b18714841751bf0107646298003059ff4ce70` with

**`1276 passed in 716.34s (0:11:56)`**.

`repository validation != new scientific evidence`.

## Carrier

The implementation `src/t_search/stage16_local.py` realizes the frozen four-cycle

`0~1~2~3~0`

with

`K_i=pi_i+c_i P`, `c=(1.0,0.5,-0.25,0.75)`,

`C_i=K_i+0.5 T_i K_{i+1 mod 4}`.

The cyclic frame determinant takes exactly

`{0.9375,1.0,1.0625}`

on the positive grid, so its minimum absolute value is **0.9375** and the frame is nonsingular on all 324 positive representatives.

The four declared physical payload classes are represented by **81 representatives each, 324 total**, with **324** deterministic off-surface probes used for algebra/Jacobi diagnostics.

Both constraint gradients and Hamiltonian generator vectors have minimum rank **4** throughout the positive family.

## Exact unsmeared algebra

An independent exact sparse-polynomial oracle in `tests/test_stage16a_local_smeared.py` certifies the frozen identities with rational coefficients. Direct canonical evaluation independently agrees with

`{C_i,C_{i+1}}=-0.25 T_i K_{i+2}`

and the antisymmetric/zero opposite-pair cases.

Sampled structure factors: **`{-0.25,0.0,0.25}`**.

Among the 324 off-surface probes and four adjacent forward edges, **864** brackets are nonzero.

Maximum residuals:

- direct vs seed formula: **0.0**;
- direct vs exact presented-`C` reconstruction: approximately **`1.3877787807814457e-17`**;
- Jacobi over **2592** probes: **0.0**.

## Support separation

Canonical-function support remains inside the union of the input generator supports.

At the same time, exact expansion of adjacent brackets in presented `C` coordinates reaches support size **4** on **768** positive/off-surface adjacent-forward probes.

Therefore the finite evidence explicitly realizes

`local canonical support != local closure-coordinate support`.

This does not license the interpretation

`cycle-spanning closure coordinates = physical nonlocality`.

Nor does it establish a Stage 16D locality obstruction.

## Exact finite smeared algebra

The same exact sparse-polynomial oracle certifies all **8** frozen smearing-pair identities. Direct analytic-gradient evaluation on all 648 positive/off-surface source points yields **5184** smeared probes.

Maximum residuals:

- direct vs seed formula: **0.0**;
- direct vs exact presented-`C` reconstruction: approximately **`2.7755575615628914e-17`**;
- antisymmetry: **0.0**.

The parallel zero-wedge family contributes **648** exactly vanishing direct brackets, and Kronecker smearings recover the unsmeared relations.

## Criteria 11–17

- **11** — 324 positive representatives, 324 off-surface probes, and nonsingular cyclic frame established;
- **12** — rank-four constraint/generator directions established;
- **13** — exact unsmeared algebra and nontrivial signed structure-factor sampling established;
- **14** — on/off direct brackets agree with seed and exact presented-basis first-class reconstruction;
- **15** — Jacobi plus separate canonical-function/closure-coordinate support audits established;
- **16** — exact/direct smeared algebra, antisymmetry, Kronecker recovery, zero-wedge, and support checks established;
- **17** — deterministic carrier diagnostics preserve the declared payload embedding without importing later-stage claims.

Criteria **18–50 remain pending**.

## Bounded Stage 16A result

`Stage 16A four-site cyclic first-class carrier, exact local/smeared algebra, support audits, and finite representative family = established`

This is a finite-carrier first-class consistency result. It does **not** establish compensated path covariance, a quotient theorem, locality-preserving Abelianization or obstruction, refoliation invariance, general relativity, physical nonlocality, eternalism, or ontological becoming.

Guards:

`four-site cycle != spatial topology of the universe`.

`cyclic first-class closure != hypersurface-deformation algebra`.

`cycle-spanning closure coordinates != physical nonlocality by definition`.

`local canonical support != local closure-coordinate support`.

`declared Dirac-payload consistency != full Dirac-observable descent`.

`local/smeared closure != compensated cycle-path closure`.

`Stage 16A support audit != Stage 16D locality obstruction`.

`known global Abelianization != proof that all Abelianizations are nonlocal`.

`failure to Abelianize != ontological becoming`.

`repository validation != new scientific evidence`.

## Next

Stage 16B — local/smeared/cycle path defects, seed compensation, presented-basis compensation search, and independent flow oracle.
