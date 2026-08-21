# Stage 8D Results — Genuine Clock-Change Modal Transport

Status: **completed for the declared canonical finite continuation family at the continuation/class-transport level.**

## Scope

Stage 8D tests whether `QExt(e1)={h_L,h_R}` and the Stage 8B selected-vs-unselected modal models survive genuine A/B/C physical-clock changes when each continuation is allowed to carry its own physically re-derived perspective atlas.

Because `h_L` and `h_R` define different modified constraints, no single inherited clock-change matrix is assumed to apply to both continuations.

## Re-derived continuation-specific atlas

For every continuation `h` and perspective node `(X,j)`:

`D_X(j)B_h = Q_{h,X,j}C_{h,X,j}`,

`G_{h,X,j}=C_{h,X,j}^{-dagger}C_{h,X,j}^{-1}`,

`S^h_{Y,k<-X,j}=C_{h,Y,k}C_{h,X,j}^{-1}`.

All 18 continuation/perspective charts have rank 14.

Executable positive checks:

- 108 distinct-clock state transports;
- 108 inverse checks embedded in those transports;
- induced-metric covariance for all tested maps;
- 324 three-clock compositions.

Maximum residuals:

- state transport = `7.406835737661463e-16`;
- inverse = `8.865498249943151e-16`;
- metric covariance = `3.627704160496353e-15`;
- composition = `7.676816844782384e-16`.

Thus the continuation-specific physical perspective atlases are internally consistent to numerical precision.

## Explicit modal correspondence

The canonical positive correspondence is declared rather than inferred from equal clock readings:

`e1 -> e1`,

`h_L -> h_L`,

`h_R -> h_R`.

It is bijective and preserves the physical continuation-equivalence classes. Continuation-class matching uses `continuation_equivalent`, so a renamed representative may be mapped to the same canonical physical class.

The public `PerspectiveModalView` keeps relational event identity separate from local clock/readout index and does not expose `h*`, model type, or selector data.

## Transported modal underdetermination

With matched:

`q_E=K=(0.5,0.5)`,

all nine public transported epistemic and ontic-extension modal views agree.

Swapping only epistemic `h*=h_L -> h*=h_R` leaves all nine public transported modal views unchanged.

Maximum continuation-weight residual = `0`.

Changing only ontic `K` to `(0.75,0.25)` remains detectable in B/C transported predictive densities. Hence equality is not imposed by the perspective-modal projection.

## Negative controls

### Wrong continuation map

Using the `h_L` support-coordinate map on `h_R` gives maximum state-transport residual:

`1.0000000000000002`.

The positive covariance result therefore requires the continuation-appropriate re-derived map.

The maximum direct QR-coordinate matrix difference between the `h_L` and `h_R` atlas representations is `8.615466962951768`; because this quantity is coordinate/basis-sensitive it is not interpreted as a representation-independent impossibility theorem.

### Wrong class correspondence

The bijective label swap `h_L<->h_R` fails physical continuation-equivalence and is rejected.

### Wrong current-event correspondence

Misdeclaring `e1 -> e2` fails because the source carrier has two current classes while terminal `QExt(e2)=empty`.

### Renaming control

A source representative named `renamed-left` can be mapped to target `h_L` when the two are physically continuation-equivalent. The class transport therefore does not define physics by string labels.

## Perspective-relative refinement of shared Actuality

The canonical Stage 8A A/e1 current pure-state density remains shared:

`||rho_L^(A,e1)-rho_R^(A,e1)|| = 7.099525387436241e-16`.

However, across the six B/C same-readout charts, the normalized `h_L/h_R` conditional pure-state density residual is:

- minimum = `0.9128709291752769`;
- maximum = `1.1547005383792515`.

Therefore the Stage 8A statement that the continuations share one A/e1 current ray does not transport into the stronger claim that they are represented by the same normalized pure conditional ray in every physical-clock perspective.

This does not spoil per-continuation perspective covariance. Instead it shows that the modal carrier requires continuation-aware transport and that “shared current Actuality” is itself perspective/event typed in this construction.

## Full Stage 8C measurement covariance

Stage 8D does not construct a single declared `h`-independent transport for the Stage 8C cross-continuation future-signature measurement.

Accordingly:

`full Stage 8C measurement covariance = not_established`.

This is intentionally not reported as false. Continuation-level physical covariance and class/weight `P-V` covariance are both positive while the stronger measurement-family claim remains open.

## Exit-criteria ledger

Stage 8.0 originally recorded only that criteria 30–50 remained future work; it did not freeze their detailed substage allocation. In the current execution ledger, Stage 8D closes criteria **30–35**:

30. continuation-specific full-rank supports/metrics;
31. genuine state/inverse/metric/composition covariance;
32. explicit event/class correspondence and weight preservation;
33. transported matched-modal equality plus hidden-`h*` swap control;
34. wrong-map / wrong-class / wrong-event / renaming controls;
35. explicit separation of established class transport from not-established full Stage 8C measurement covariance.

Criteria **36–50** remain Stage 8E–G work.

## Validation

Final scientific regression before documentation synchronization:

**`634 passed in 131.34s`**

on branch head `ad9293d31c6879b0271d7b9e77876c64f55f0f7b` / PR merge-ref `d080f5915b56ac69ed80efc8a7759088e02ed532`.

A final documentation-synchronized regression follows after propagating this checkpoint to the protocol, concepts, README, roadmap, and documentation audit.

## Strongest bounded statement

**Within the canonical finite continuation family, each represented continuation admits its own re-derived full-rank A/B/C physical-clock atlas whose state transport, inverse structure, induced metric, and three-clock composition are consistent to about `1e-15`. With an explicit `e1->e1` physical continuation-class correspondence, matched epistemic and ontic-extension weights give equal public transported modal views at all nine perspective nodes, and changing the hidden epistemic `h*` alone remains operationally invisible. Wrong continuation maps, wrong physical-class correspondence, and a misdeclared terminal-current correspondence fail. At the same time, the shared A/e1 current pure ray does not remain an identical normalized pure conditional ray across B/C perspectives, and a single transport of the Stage 8C cross-continuation measurement family has not been established. This supports continuation/class-level `P-V` covariance in the declared finite model, not `P=V`, ontic openness, universal quantum covariance, or a perspective-independent ontology of the future.**

## Next

Stage 8E — P/O/R/V compatibility and underdetermination.
