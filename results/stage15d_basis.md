# Stage 15D Result — Locality-Preserving Basis Pressure Test

Status: **criteria 32–38 satisfied by validated executable evidence. Stage 15E is next.**

Validated scientific checkpoint: `1c24fe88f0bec2d6d557fa21d353eb9385019436`; GitHub Actions run #1968: **`1217 passed in 551.47s (0:09:11)`**.

## Deterministic evidence

- basis candidates audited: **14**;
- points per candidate: **216 = 108 positive + 108 off-surface**;
- L0 candidates: **3**, strongly commuting: **0**;
- strict L1 candidates: **7**, strongly commuting: **2**;
- one-step local candidates including L0: **10**, strongly commuting: **2**;
- one-step L1 Abelianizing witness: `C_0_tilde=C_0`, `C_1_tilde=C_1-kappa T_1 C_2=K_1`, `C_2_tilde=C_2=K_2`;
- known full seed reconstruction: direct one-step L1 **false**, exact Lfinite depth **2**;
- minimum exhibited local Abelianization depth: **1**;
- equivalent-basis physical-content checks: **14/14** preserve the sampled `4 x 27` quotient, Dirac pair, and complete relational family;
- transformed unsmeared first-class closure reconstructions: **9072**;
- transformed smeared first-class closure reconstructions: **18144**.

Bounded classification:

`local_abelianization_persists`.

Bounded result:

`Stage 15D locality-preserving basis pressure test on the frozen three-site carrier = local_abelianization_persists`.

This establishes only that at least one admissible one-step L1 Abelianizing basis exists on the declared finite carrier. It does not prove that every local basis Abelianizes, that the original local algebra is physically trivial, that finite graph locality is relativistic locality, or that general relativity/refoliation structure is captured.

Criteria **32–38** are satisfied. Criteria **39–50 remain pending at the Stage 15D checkpoint**.

Persistent guards:

- `basis locality != physical causal locality`;
- `finite graph locality != relativistic microcausality`;
- `locality-preserving basis map != gauge transformation`;
- `local Abelianization != absence of meaningful local constraint structure`;
- `known nonlocal seed reconstruction != proof that all Abelianizations are nonlocal`;
- `constraint-basis change != physical-orbit change`;
- `strongly commuting finite basis != refoliation invariance`;
- `Stage 15D basis equivalence != general relativity`;
- `Stage 15D basis result != eternalism or ontological becoming`;
- `repository validation != new scientific evidence`.
