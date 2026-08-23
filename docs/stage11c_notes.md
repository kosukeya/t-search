# Stage 11C Notes — Typed O/P/R/V/Xi Lift

Status: **Stage 11C implementation complete; criteria 24–31 are decided by executable diagnostics, with repository-level regression tracked separately.**

Stage 11B baseline: run #1335 — **`891 passed in 652.53s (0:10:52)`**.

## Question

Stage 11C asks whether the layered Stage 10 candidate

`T10_candidate=(O,P,R,V;Xi)`

with

`R=(R_content,R_direction,R_access)`

and

`V=(V_extension,V_semantics,V_weights)`

can be represented across the four frozen positive external parameterizations without making the raw external parameter a physical field.

The stage does **not** yet transport the Stage 10 future-measurement matrices/probabilities. That is reserved for Stage 11D.

## Construction

The Stage 11C lift is a typed product construction between:

1. the existing Stage 9/10 physical/modal/record payload; and
2. the Stage 11A/B parameterization carrier.

The physical O/P/R/V payload is held fixed at corresponding physical event roles. Representation-specific data are placed in `Xi`.

### O

The public O layer contains:

- the common Stage 9/10 current `e1` reduced density matrix;
- a typed Stage 11 prediction-anchor event;
- a typed Stage 11 measurement-target event;
- the corresponding relational `T` and `q(T)` values.

Raw `lambda_rho` values are not part of O.

### P

The Stage 9/10 extension carrier is retained exactly:

`QExt(e1)={h_L,h_R}`.

The continuation ids are paired with their already-defined physical continuation classes (`identity` / `c-phase`) rather than treated as bare branch labels.

### R

The Stage 9 directional record diagnostics are retained in three separately typed components:

- `R_content`: lower/upper record information and decoder accuracy;
- `R_direction`: record score and orientation;
- `R_access`: accessibility score.

`R_direction` is inherited from the physical Stage 9 record diagnostic; it is not defined by increasing external `lambda`.

### V

The public V layer retains:

- `V_extension=(h_L,h_R)`;
- matched continuation-class weights `(0.5,0.5)`;
- explicit continuation-to-weight alignment;
- public weight semantics that do not encode a hidden selected continuation.

The privileged modal roles remain distinct in the source models: epistemic semantics still contain a hidden selected complete continuation, while ontic-extension semantics do not. Stage 11C verifies that distinction privately while keeping it out of the public O/P/R/V/Xi schema.

### Xi

For each positive parameterization, Xi carries:

- parameterization identity;
- raw parameter value at the Stage 11 anchor and target roles;
- transformed positive lapse at those roles;
- the typed Stage 10 event-role bridge `e1/e2 -> Stage 11 physical event id`;
- identity continuation/class correspondence for `h_L/h_R`;
- identity outcome correspondence for `future_signature_left/future_signature_other`;
- event, lapse, and continuation-weight semantics.

The event-role bridge is a typing association between the Stage 10 architecture and the Stage 11 precursor. It is not a claim that the finite classical precursor and the Stage 10 quantum carrier are dynamically identical theories.

`Stage 10 event-role bridge != dynamical identification of quantum and classical carriers`.

## Positive family

The positive family contains the frozen four parameterizations:

- identity;
- positive affine;
- nonlinear cubic;
- nonlinear hyperbolic/sinh.

Across them, O/P/R/V must agree at corresponding typed physical roles, while Xi is allowed—and required—to carry different raw parameter/lapse representation data.

Matched epistemic and ontic-extension public projections are compared at all four parameterizations. A hidden `h*` swap from `h_L` to `h_R` is also checked and must not change the public projection.

## Negative controls

Stage 11C adds executable controls for:

1. wrong continuation/class correspondence in Xi;
2. parameter-dependent corruption of O;
3. parameter-dependent corruption of P;
4. parameter-dependent corruption of R;
5. parameter-dependent corruption of V.

The O/P/R/V corruption cases are intentionally type-specific so the validator must identify the corrupted layer rather than merely reject an opaque object.

Expected executable classification for each O/P/R/V corruption:

`parameter_dependent_oprv_corruption_detected`.

## Interpretation

A successful Stage 11C result means only that the existing typed architecture can be lifted consistently onto the finite positive parameterization family with representation-specific information isolated in Xi.

It does not yet establish future-measurement covariance under reparameterization.

`typed O/P/R/V/Xi lift != full future-measurement covariance`.

`typed product lift feasibility != independent dynamical covariance evidence`.

`same typed architecture across parameterizations != modal/ontological identity`.

`selector-free public projection != absence of privileged modal semantics`.

`parameter orientation != physical record direction by definition`.

`finite typed parametrized covariance != general covariance`.

`parametrized covariance precursor != general relativity`.

`absence of preferred external parameterization != absence of ontological becoming`.

`repository validation != new scientific evidence`.

Next checkpoint: **Stage 11D — future-measurement reparameterization covariance.**
