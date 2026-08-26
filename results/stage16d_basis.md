# Stage 16D Result — Locality-Preserving Abelianization Pressure Test

Scientific implementation head: `16a26c4ea08b315af4581cbdc5550649703951d8`

Corrected validation head: `85b8312a958e66b17d5d0e11837de2d8f938dc01`

## Deterministic evidence

| Quantity | Result |
| --- | ---: |
| explicit equivalent candidates | 21 |
| L0 candidates | 3 |
| one-step L1 candidates | 16 |
| strongly commuting local candidates | 0 |
| unrestricted/global controls | 2 |
| strongly commuting unrestricted/global controls | 2 |
| minimum explicit-L1 all-point max bracket | 0.09375 = 3/32 |
| depth-1 compositions | 16 |
| depth-2 compositions | 256 |
| depth-3 compositions | 4,096 |
| depth-4 compositions | 65,536 |
| total depth<=4 compositions | 69,904 |
| depth<=4 strong witnesses | 0 |
| exact Lfinite witness clocks | (-1,-1,-1,-1) |
| minimum exact depth<=4 max bracket | 7/32 = 0.21875 |
| affine-L1 parameters | 12 |
| affine raw coefficient equations | 608 |
| affine sign-reduced equations | 137 |
| saturated Groebner basis | (1) |
| affine invertible strong solutions | 0 |
| explicit content audits preserved | 21 / 21 |
| minimum exhibited local Abelianization depth | none in declared local search |

## Result

The four-site closed cycle retains a known globally Abelian seed basis, but the frozen locality pressure test finds no local strongly commuting witness:

1. no L0 witness;
2. no one-step L1 witness in the 16 explicit elementary cyclic shears;
3. no witness in all 69,904 elementary L1 compositions through depth 4;
4. an exact saturation certificate excludes invertible strong solutions in the frozen 12-parameter translation-covariant affine L1 ansatz;
5. the known global seed and unrestricted full-matrix controls remain strongly commuting and preserve the same quotient/Dirac/relational content.

Bounded classification:

`only_nonlocal_abelianization_witness_found_in_frozen_search`.

This is intentionally weaker than a universal locality-obstruction theorem.

## CI correction note

CI #2032 gave `2 failed, 1308 passed in 946.87s (0:15:46)`. The two failures were a Stage 16C number-formatting mismatch and an overstated Stage 16D explicit-L1 residual lower bound. They are corrected on `85b8312a958e66b17d5d0e11837de2d8f938dc01`; the observed explicit-L1 minimum is `0.09375 = 3/32`.

## Corrected authoritative regression

- run #2036
- PR merge checkout `9471ae7170df65a20556200ab5207c1352afb3bf`
- **1310 passed in 700.22s (0:11:40)**

## Criteria state

**1–39 satisfied / 40–50 pending**.

Next after validation/docs sync:

**Stage 16E — typed O/P/R/V/Xi and future-measurement descent across cycle quotient, paths, and basis classes.**

## Guards

- `known global Abelianization != proof that all Abelianizations are nonlocal`;
- `no L1 witness in frozen search != no L1 Abelianization exists`;
- `only nonlocal witness found != fundamental physical non-Abelianity`;
- `global Abelianization != physical triviality`;
- `failure to Abelianize != ontological becoming`;
- `finite graph locality != relativistic locality`;
- `Stage 16D basis equivalence != refoliation invariance`;
- `repository validation != new scientific evidence`.

Bounded result:

> **Stage 16D closed-cycle locality-preserving Abelianization pressure test: only nonlocal Abelianization witnesses were found in the frozen search, with no L0/L1/depth<=4 local witness and an exact no-solution certificate for the frozen affine cyclic L1 ansatz.**
