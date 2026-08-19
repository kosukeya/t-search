# Stage 3D — Reversal and Symmetric Controls

Status: **completed; GitHub Actions full regression passed**.

## Purpose

Stage 3D tests whether the Stage 3C record-defined orientation survives, flips, or disappears under the protocol-frozen controls. No new orientation metric is introduced.

The canonical forward result carried into this checkpoint is:

`A_R=+1 bit`

`A_Acc=+1/2`

`orientation=lower-index`.

## 1. Exact history reversal

For:

`mu_rev = J_* mu_fwd`

with `J(z0,z1,z2)=(z2,z1,z0)`, the central-position information profile swaps sides:

`I(M_1;X_0): 1 -> 0`

`I(M_1;X_2): 0 -> 1`.

The decoder accessibility swaps likewise:

`Acc(M_1->X_0): 1 -> 1/2`

`Acc(M_1->X_2): 1/2 -> 1`.

Therefore:

`A_R(mu_rev)=-1 bit`

`A_Acc(mu_rev)=-1/2`

and:

`orientation=upper-index`.

Thus the Stage 3C diagnostic obeys the expected sign covariance under modeled history reversal.

## 2. Equal forward/reverse mixture

The exact mixture is:

`mu_sym = 1/2 mu_fwd + 1/2 mu_rev`.

The forward and reversed ensembles share one complete trajectory, so duplicate probability mass is merged. The resulting exact support contains seven distinct complete trajectories: six at probability `1/8` and the shared all-zero history at probability `1/4`.

The important result is that correlation remains while directional bias cancels:

`I(M_1;X_0)=I(M_1;X_2)≈0.188721875541 bit`

`Acc(M_1->X_0)=Acc(M_1->X_2)=0.75`.

Therefore:

`A_R=0`

`A_Acc=0`

`orientation=none`.

This is stronger than a trivial decorrelation control: the symmetric mixture retains nonzero record/target correlations but no signed preference between the two neutral sides.

## 3. Order-only / no-record control

The first update is replaced by the identity while the reversible scrambling map remains:

`z1=z0`

`z2=U_scr(z1)`.

The ensemble still has three ordered positions and trajectories in which `X` changes. The actual control maps `U_id` and `U_scr` are both bijective.

Because the blank register never couples to `X`:

`I(M_1;X_0)=0`

`I(M_1;X_2)=0`

`Acc(M_1->X_0)=Acc(M_1->X_2)=1/2`

so:

`A_R=0`

`A_Acc=0`

`orientation=none`.

This supports the project-level statement:

**mere ordered change is insufficient for the tested record-defined orientation.**

## 4. Independent uniform-memory boundary

The canonical reversible maps are restored, but the special boundary is replaced by independent uniform memory:

`X_0,M_0,N_0` independent uniform bits.

The exact initial ensemble contains all eight complete microstates at probability `1/8`. The full-state entropy profile is:

`H(Z_0)=H(Z_1)=H(Z_2)=3 bits`.

Because:

`M_1=M_0 XOR X_0`

and `M_0` is independent uniform noise, the accessible register carries no information about either comparison target:

`I(M_1;X_0)=0`

`I(M_1;X_2)=0`

`Acc(M_1->X_0)=Acc(M_1->X_2)=1/2`.

Therefore:

`A_R=0`

`A_Acc=0`

`orientation=none`.

Within the tested model family, the canonical orientation therefore depends on the special low-uncertainty memory boundary rather than following from reversible dynamics alone.

## Control table

| Ensemble | `A_R` | `A_Acc` | Orientation |
|---|---:|---:|---|
| canonical forward | `+1` | `+0.5` | `lower-index` |
| exact reversed | `-1` | `-0.5` | `upper-index` |
| 50/50 forward+reverse | `0` | `0` | `none` |
| no-record / identity first map | `0` | `0` | `none` |
| uniform initial memory | `0` | `0` | `none` |

## Strongest justified Stage 3D conclusion

The four controls jointly support:

**within this finite reversible toy model and the declared record/accessibility interface, the Stage 3C orientation is not a consequence of mere ordered positions or microscopic irreversibility. It reverses under modeled history reversal, cancels in an orientation-symmetric ensemble, disappears when the record coupling is removed, and disappears when the special blank-memory boundary is replaced by independent uniform memory.**

This makes the asymmetry attributable, within the tested construction, to the combination of record coupling and asymmetric boundary preparation more strongly than Stage 3C could.

## Limits

Stage 3D does not establish:

- a universal necessity of blank memories for records;
- a fundamental physical arrow of time;
- thermodynamic irreversibility;
- an empirical time-reversal violation;
- ontological becoming;
- phenomenal temporal passage.

The reversal result is covariance of this toy diagnostic under the declared modeled-history transformation. The symmetric result is a statement about an ensemble mixture, not a claim that the physical universe is a mixture of opposite arrows.

## Validation

The committed Stage 3D test file contains **9 focused tests** covering:

- reversal sign flip and profile swap;
- inverse-map validity of reversed histories;
- exact symmetric-mixture probability mass and duplicate merging;
- cancellation of signed bias while nonzero correlations remain;
- no-record control with reversible identity/scrambling maps;
- exact uniform-memory boundary and disappearance of the record contrast;
- global entropy preservation in the uniform-memory control;
- combined control classification;
- invalid mixture weights.

GitHub Actions clean PR merge-ref regression:

`137 passed in 3.11s`.

This includes Stage 1, Stage 2, and Stage 3A–3D tests.

## Next

Stage 3E defines the explicit record-bearing local view and global-to-local projection, then upgrades toward:

`G_k=(Records_k,Actuality_k,Potentiality_k)`.
