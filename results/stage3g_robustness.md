# Stage 3G — Robustness Results

Status: **robustness controls passed; final Stage 3 synthesis and final-head regression follow**.

## Summary

Stage 3G stress-tests the Stage 3A--3F claims without adding a new temporal model.

The 12 focused robustness tests passed at the code/test checkpoint, with the full repository suite reporting:

`171 passed in 3.28s`.

## Bookkeeping relabeling

Arbitrary unique symbolic names for positions preserve the numerical record profile. The selected neutral side follows the corresponding renamed structural side rather than any literal name.

Bijective bit-value relabelings of the record/target variables also preserve mutual information and Bayes-optimal decoding.

Supported conclusion:

`bookkeeping representation != measured information content`.

## Repeated-value control

The all-zero trajectory repeats the same complete state value at all three positions. Position-tagged occurrences nevertheless remain distinct, and repeated local `(X,M)` values do not collapse coverage information.

Two repeated-value views can remain ambiguous, while adding the third position uniquely identifies the all-zero history.

Supported conclusion:

`state-value equality != occurrence identity`.

## Boundary sweep

Let:

`p=P(M_0=0)`.

With unchanged reversible maps and independent uniform `X_0,N_0`:

| `p` | `A_R` | `A_Acc` | orientation |
|---:|---:|---:|---|
| `1` | `1` | `0.5` | lower-index |
| `3/4` | `~0.188721875541` | `0.25` | lower-index |
| `1/2` | `0` | `0` | none |
| `1/4` | `~0.188721875541` | `0.25` | lower-index |
| `0` | `1` | `0.5` | lower-index |

Thus the literal value `M_0=0` is not the robust explanatory ingredient. A deterministic `M_0=1` boundary gives an equally strong, anti-correlated but perfectly decodable record.

The refined toy-model statement is:

**record strength depends on non-maximal uncertainty/nonuniform preparation of the memory boundary, not on which deterministic bit value is designated blank.**

## Forward/reverse balance

For:

`mu_w=w mu_fwd+(1-w)mu_rev`,

the controls verify:

- forward-biased mixture -> lower-index orientation;
- exact 50/50 balance -> no signed orientation;
- reverse-biased mixture -> upper-index orientation;
- signed record/accessibility scores are antisymmetric under `w -> 1-w`.

This strengthens the Stage 3D equal-mixture control: the sign tracks ensemble orientation balance and crosses zero at symmetry.

## Boundary uncertainty versus readout uncertainty

Two distinct constructions produce the same reduced information value `~0.188721875541` bit:

1. globally uncertain memory boundary `P(M_0=0)=3/4`, where true global `I(M_1;X_0)` is reduced;
2. canonical globally perfect record plus local readout noise `epsilon=1/4`, where true global `I(M_1;X_0)=1` bit but accessible `I(M_obs;X_0)` is reduced.

Therefore:

`same local/accessibility statistic != same global information structure`.

## Stage 2 integration review

Swapping the epistemic hidden selected history `h*` while holding the Stage 2 local projection fixed does not change the complete Stage 3 product local view.

Epistemic and ontic product views retain:

- identical Stage 3 record layer;
- equal matched modal Actuality/next probabilities in the canonical fixture;
- distinct typed Potentiality semantics.

No hidden selected history is reintroduced by the Stage 3 adapter.

This is construction-level modularity, not a physical theorem about the independence of record arrows from future ontology.

## Strongest supported Stage 3G robustness statement

Within the declared finite toy-model family:

**the Stage 3 record-defined orientation is not an artifact of literal position names, binary value naming, or the special convention that the blank register equals zero. It survives non-maximal memory-boundary bias, changes sign with forward/reverse ensemble balance, vanishes at the relevant symmetric limits, and remains formally separable from local-access degradation and from the Stage 2 Potentiality type distinction.**

## Limits

This does not establish:

- a fundamental physical temporal arrow;
- a generally covariant time observable;
- thermodynamic irreversibility or a Past Hypothesis;
- empirical T violation;
- ontological becoming;
- phenomenal passage.

The canonical `X_1=X_0` redundancy also remains a known limitation: current system state itself carries lower-side information independently of the explicit memory readout.
