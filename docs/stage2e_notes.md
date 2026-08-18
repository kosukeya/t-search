# Stage 2E — Update Comparison Notes

Status: **completed**.

## Question

Stage 2D established that two internally different model families can have the same pre-observation operational view under matched weights:

`O(G_E(D_0)) = O(G_O(D_0))`.

Stage 2E asks whether that equality survives a common explicit observation while the internal semantic difference remains.

Baseline observation:

`l1`.

## Comparison rule

Stage 2E does not introduce a new dynamics or random branch selector.

It applies the already-fixed update rules:

- epistemic: `condition_epistemic_model`;
- ontic: `update_ontic_model`;

and compares the resulting local views through the Stage 2D operational interface.

The two models must begin from the same current Actuality/prefix.

## Expected epistemic update

Starting from:

`D_0 = (p,n)`

with:

`h* = h_L`

and equal beliefs, observation `l1` produces:

`D_1 = (p,n,l1)`.

The belief distribution conditions to the left history, while:

`h*` remains unchanged.

## Expected ontic update

Starting from the same `D_0`, observation `l1` produces the same updated Actuality:

`D_1 = (p,n,l1)`.

The incompatible right extension is removed and the remaining extension weight is renormalized.

No selected complete future field is created.

## Operational comparison after update

Both models should operationalize to:

`A_now = (p,n,l1)`

`Next = {l2}`

`pi(l2) = 1`.

Thus Stage 2E tests:

`O(G_E(D_1)) = O(G_O(D_1))`.

This equality is checked after running the two distinct update rules rather than being inserted as a shared post-update object.

## Internal distinction after update

Operational equality does not erase the model-level contrast:

- epistemic: the complete selected history existed before the observation and is preserved by the update;
- ontic: there is still no selected complete future field after the update.

The typed Potentiality carriers also remain different Python types even when both contain only `h_L` after the observation.

## Update-domain contrast

The canonical epistemic actual-run fixture stores `h*=h_L`, so observation `r1` is rejected as contradicting the selected history.

The canonical ontic state, by contrast, can update through `r1` because both branches initially have positive weight and neither is preselected.

This does not by itself give an empirical discriminator between the two *model families*: an epistemic model with `h*=h_R` can represent an actual right-branch run. The result only shows that one fixed epistemic global state has a narrower compatible actual-run update domain than the unselected ontic baseline state.

## Guards

`explicit observation != simulated creation of physical becoming`

`post-update operational equality != ontological equality`

`a difference in privileged update semantics != automatically an observable physical difference`

`simulation order != modeled temporal order`.

## Validation

A clean GitHub clone remains unavailable in the current execution environment because `github.com` cannot be resolved by the container network path.

The committed Stage 2E test file contains 9 focused tests. A compact semantic reconstruction of the Stage 2A–E contracts passed:

`9/9 checks`.

A full repository regression remains mandatory before Stage 2 merge review.
