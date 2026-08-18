# Stage 1 Synthesis — Classical Global/Local Reconstruction

Status: **Stage 1 synthesis complete; ready for Stage 1 exit review**.

## 1. Purpose of this report

Stage 1 tested a deliberately small classical question before introducing Potentiality, records, entropy, or quantum structure:

> Given a finite global directed relational structure, what can be recovered from families of local or perspective-like descriptions as privileged information is removed or transformed?

The baseline global object was:

`B_1 = (E, C)`

with canonical event set:

`E = {a,b,c,d,e,f}`

and direct edges:

`C = {(a,b),(a,c),(b,d),(c,d),(d,e),(d,f)}`.

The induced non-reflexive reachability relation is:

`prec = TC(C)`.

Stage 1 is an infrastructure and information-preservation study. It is **not** yet a physical model of becoming and does not decide eternalism versus ontic becoming.

## 2. Stage 1 experiment sequence

Stage 1A established the information-rich round-trip baseline:

`B_1 -> {V_e} -> B_1_hat`.

Stage 1B then changed one major information assumption at a time:

1. B1 — outgoing-only;
2. B2 — incoming-only;
3. B3 — missing local views;
4. B4 — reachability-only;
5. B5 — state-label collision;
6. B6 — anonymous / global-ID-free views.

This ordering separated redundancy, coverage, representational detail, state identity, and global naming rather than changing them all at once.

## 3. Information-preservation map

| Stage / variant | Retained local information | Removed / transformed information | Global result | Classification |
|---|---|---|---|---|
| Stage 1A baseline | shared event ID + predecessors + successors | nothing in baseline | exact labeled graph and reachability recovered | reconstructible baseline |
| B1 outgoing-only | shared ID + successors | predecessor channel | exact `E`, `C`, `prec` recovered | predecessor channel redundant for reconstruction; cross-check lost |
| B2 incoming-only | shared ID + predecessors | successor channel | exact `E`, `C`, `prec` recovered | successor channel redundant for reconstruction; cross-check lost |
| B3 Case A | full views except `V_d`; shared IDs | one event-owned perspective | latent policy recovers `d` and all edges exactly | missing perspective reconstructible |
| B3 Case B | full views except `V_b`,`V_d`; shared IDs | two adjacent perspectives | `b`,`d` identities recoverable but their relation has 3 compatible completions | relation ambiguous |
| B3 Case C | full views except `V_d`,`V_e`; shared IDs | coverage removes all surviving references to `e` | `e` absent from reconstructible universe | event lost |
| B4 canonical | shared ID + all ancestors/descendants | direct one-hop edge encoding | `prec` and unique minimal cover relation recovered | order/cover reconstructible |
| B4 shortcut control | same reachability-only data | whether redundant shortcut `a->d` existed | canonical and 7-edge input observationally identical | redundant edge encoding not identifiable |
| B5 correct | shared ID + state + predecessors + successors | state no longer assumed unique | 6 events and state map recovered despite `s(b)=s(c)` | state equality separated from event identity |
| B5 naive control | state value used as identity | event multiplicity | 6 events collapse to 5 state-nodes and graph structure changes | identity information lost |
| B6a anonymous degree stars | multiset of `(in_degree,out_degree)` | all shared IDs and cross-view identity links | 3 non-isomorphic compatible global DAGs | global structure ambiguous |
| B6b refined anonymous neighborhoods | anonymous star type + predecessor/successor star-type multisets | shared global IDs remain absent | exactly 1 compatible global DAG up to isomorphism in the six-event search class | global structure reconstructible up to relabeling |

The strongest qualitative progression is:

`redundant -> reconstructible -> ambiguous -> lost`

as local information is weakened in different ways.

## 4. What was actually local?

Stage 1 makes the term "local" representation-dependent.

Examples:

- Stage 1A: own ID, immediate predecessor IDs, immediate successor IDs;
- B1/B2: one oriented one-hop adjacency channel;
- B4: all ancestor/descendant IDs, which is relational but not one-hop local in graph distance;
- B6a: anonymous in-degree/out-degree only;
- B6b: anonymous one-step neighborhood types.

Therefore Stage 1 does **not** support one universal notion of locality. Each reconstruction claim must state exactly which local data are permitted.

## 5. Directional redundancy was not structurally essential

B1 and B2 gave symmetric results.

With shared IDs and complete view coverage, either:

`V_e^+ = (id_e, Succ_1(e))`

or:

`V_e^- = (id_e, Pred_1(e))`

was sufficient to reconstruct the canonical labeled DAG exactly.

The discarded opposite-direction channel was useful as an independent consistency check, but not necessary for reconstructing the graph.

Therefore the Stage 1A success did not depend on having two copies of every edge report.

## 6. Coverage mattered more than direction

B3 was the first experiment to produce qualitatively different reconstruction states.

### 6.1 Reconstructible missing perspective

Removing only `V_d` did not destroy the canonical structure under the referenced-latent-node policy because surviving neighbors still referred to `d` and every incident edge retained at least one surviving endpoint report.

### 6.2 Reconstructible events but ambiguous relation

Removing both `V_b` and `V_d` preserved references to both event IDs, but the relation between them lost all surviving endpoint evidence.

Three labeled DAG completions remained compatible:

1. no edge between `b` and `d`;
2. `b -> d`;
3. `d -> b`.

This is Stage 1's first explicit example of:

`event identity reconstructible`

while:

`relation not uniquely reconstructible`.

### 6.3 Completely lost event

Removing both `V_d` and `V_e` made `e` neither a surviving owner nor a surviving reference. Under the stated closed-world reconstruction policy, `e` disappeared entirely.

Thus reconstruction depends not only on what each perspective contains but on whether the family of perspectives leaves a relational trace of the target at all.

## 7. Compatible completions are not ontic Potentiality

B3 produced multiple compatible global completions, but Stage 1 assigns them no modal ontology.

The crucial guard is:

`compatible global completions != ontic future possibilities`.

At Stage 1 they are only model-theoretic / information-theoretic alternatives consistent with incomplete data.

This distinction is essential for Stage 2. The same mathematical set of alternatives can later support two different models:

- epistemic: one complete history is already selected but hidden;
- ontic: no complete future history is preselected in the model state.

Stage 1 therefore supplies a neutral ambiguity structure without deciding its metaphysical interpretation in advance.

## 8. Reachability survived representational redundancy better than arbitrary edge lists

B4 tested whether the global description should be identified with an arbitrary direct-edge encoding or with the induced order.

For the canonical graph:

`TR(TC(C)) = C`

because the canonical `C` is already the minimal cover relation.

But adding the transitive shortcut:

`a -> d`

left all reachability-only views unchanged.

Therefore:

`different direct-edge encodings -> same reachability order`

when redundant shortcut edges are allowed.

Within the finite-DAG setting, the more stable reconstructible object is:

`(E, prec)`

plus its unique minimal cover relation, not an arbitrary input edge list.

This is a representation-level result. It does **not** establish that physical time is fundamentally a partial order.

## 9. State equality is not an identity criterion

B5 introduced:

`s: E -> Sigma`

with:

`b != c`

but:

`s(b) = s(c) = X`.

Correct ID-based reconstruction preserved both event occurrences and the complete graph.

A deliberately incorrect state-as-identity quotient collapsed:

- 6 events to 5 state-nodes;
- 6 event edges to 4 distinct state-edges.

Therefore Stage 1 establishes the implementation and conceptual guard:

`state equality != event identity`.

This will matter whenever later models revisit the same physical, latent, or observational state at different relational positions.

However, B5 does not make global event IDs fundamental. B6 explicitly removes them.

## 10. Global IDs were sufficient, but not necessary

B6 is the strongest Stage 1 test of privileged naming.

Shared event IDs were removed from the observable local data, and the reconstruction target changed from labeled equality to directed graph isomorphism.

### 10.1 B6a — anonymous one-hop degree stars

Each local description retained only:

`A_e^(0) = (in_degree(e), out_degree(e))`.

For exactly six-event DAGs, exhaustive enumeration scanned:

`2^15 = 32768`

forward-edge subsets.

The canonical anonymous degree multiset admitted:

- 5 topological-label matches;
- 3 non-isomorphic compatible global DAGs.

Thus:

`N_compatible^(0) = 3`.

This ambiguity is not merely relabeling. The candidates are genuinely non-isomorphic, and one candidate even has a different reachability-pair count.

Therefore bare anonymous local shape is too weak to identify the global world.

### 10.2 B6b — one-step anonymous relational refinement

Define:

`t_0(e) = (in_degree(e), out_degree(e))`

and retain:

`A_e^(1) = (t_0(e), multiset{t_0(pred)}, multiset{t_0(succ)})`.

No shared event names are restored.

Under the same exhaustive six-event DAG search:

`N_compatible^(1) = 1`.

The unique compatible isomorphism class is the canonical graph.

Therefore, in this toy search class:

`shared global IDs are sufficient but not necessary for unique global reconstruction`.

What matters is whether the anonymous relational context is rich enough to eliminate non-isomorphic alternatives.

## 11. Strongest justified Stage 1 conclusions

The following conclusions are supported by the implemented experiments.

### 11.1 Reconstruction is conditional on an information interface

There is no context-free statement that "the global structure is reconstructible from local views." Reconstruction depends on:

- which relational data each view contains;
- coverage of the view family;
- whether identities are shared or anonymous;
- which equivalence relation defines "same global structure";
- background assumptions such as finite DAG, event count, and closed-world reconstruction.

### 11.2 Relational context can substitute for privileged naming

B6b shows, within the six-event DAG search class, that enough anonymous relational information can identify the global graph up to isomorphism without shared global IDs.

This is the Stage 1 result most directly aligned with the project's motivating idea that objectivity may be associated with consistency/reconstructibility across perspectives rather than a privileged naming frame.

### 11.3 Weak locality can underdetermine the global world

B3 and B6a independently produce multiple compatible global structures:

- B3 through missing coverage;
- B6a through insufficient anonymous relational detail.

Thus local/perspectival data do not generically determine a unique global structure.

### 11.4 Some representation details are less stable than relational order

B4 shows that redundant direct-edge details can vary while reachability remains fixed.

This identifies `(E,prec)` or its cover relation as a **candidate representation-stable structure within this toy setting**, not as an established fundamental temporal object.

### 11.5 Event occurrence cannot be reduced to state value

B5 shows that state equality can erase relational multiplicity if used as an identity rule.

Any later temporal model must retain some criterion that distinguishes repeated or relationally distinct occurrences even when state descriptions coincide.

## 12. What Stage 1 does not justify

Stage 1 does **not** establish that:

- block-like and becoming-like descriptions are physically equivalent;
- a global block exists ontologically;
- local becoming is more fundamental than a block;
- reachability or partial order is the fundamental nature of time;
- B6b's anonymous signature is a physical observable;
- objectivity in real physics is literally graph reconstruction;
- compatible completions are ontic possibilities;
- Future Potential is real rather than epistemic;
- records create time;
- entropy explains temporal passage;
- quantum reference-frame changes preserve the same structures;
- the same results survive general covariance, relativity, or quantum theory;
- a new physical law or novel theorem about time has been discovered.

The Stage 1 results are conditional finite classical combinatorial results.

## 13. Strict invariant assessment

Stage 1 intentionally reserved the term **strict invariant** for structures preserved under a genuine representation equivalence or reversible description change.

No non-trivial **physical** strict invariant has been established.

Two weaker but useful candidates emerged:

1. **reachability / cover structure** is stable under adding or removing transitively redundant direct-edge shortcuts;
2. **global graph isomorphism class** can be uniquely reconstructible from the B6b anonymous family without global names.

These should be called:

- representation-stable structures;
- reconstructible structures;
- candidate invariants for later tests;

not yet fundamental invariants of time.

## 14. Optional combined restrictions — decision

Stage 1 originally allowed optional combinations such as:

- hide IDs + remove one direction;
- hide IDs + delete views;
- anonymous neighborhoods + state collisions;
- varying graph size/topology.

### Decision for Stage 1 exit

**Do not make these combined restrictions prerequisites for Stage 1 completion.**

Reason:

B1–B6 already isolate the six intended mechanisms:

- directional redundancy;
- coverage;
- adjacency versus order representation;
- state versus event identity;
- shared identity removal;
- anonymous relational refinement.

Combining them now would primarily test robustness and interactions rather than answer a missing Stage 1 foundational question.

They should be retained as a future robustness suite, especially if Stage 2 conclusions later depend strongly on one Stage 1 reconstruction assumption.

The highest-value future combined controls would be:

1. B6b anonymous views + missing coverage;
2. B6b anonymous views + repeated state labels;
3. B6b signature across larger and structurally different DAGs.

These are valuable generalization tests, but they are not required for the first clean Stage 1 exit.

## 15. Stage 1 exit criteria review

The protocol defined seven exit conditions.

### Criterion 1 — reproducible Stage 1A round trip

Satisfied.

The canonical information-rich family reconstructs the labeled graph exactly.

### Criterion 2 — adjacency and reachability kept distinct

Satisfied.

B4 directly tests and separates them.

### Criterion 3 — B1–B6 individually run or justified omission

Satisfied.

All planned variants B1–B6 were implemented and recorded.

### Criterion 4 — local / reconstructible / invariant / ambiguous / lost classification

Satisfied.

Each variant records its classification, and this report integrates them.

### Criterion 5 — dependence on global IDs and privileged encodings explicit

Satisfied.

B5 states the limits of ID-based identity; B6 removes shared IDs and changes the equivalence criterion to graph isomorphism.

### Criterion 6 — simulation order not interpreted as physical time

Satisfied.

`simulation order != modeled temporal order`

remains a project-wide guard.

### Criterion 7 — state what Stage 1 teaches before Potentiality

Satisfied by this synthesis.

### Stage 1 exit judgment

`Stage 1 exit criteria: satisfied`.

Stage 1 can be considered conceptually complete after review of this synthesis and PR contents.

## 16. What should be carried into Stage 2

Stage 2 should not replace the Stage 1 machinery. It should reuse the structural distinctions that Stage 1 made explicit.

### 16.1 Carry forward: compatible-completion set

Use a representation like:

`Comp(D_now) = {B^(1), B^(2), ...}`

for global continuations/histories compatible with current relational data.

Stage 1 shows that such sets can arise from incomplete information without any ontic interpretation.

### 16.2 Add an explicit epistemic model

Represent a complete hidden actual history:

`(T, h*)`

where local/current data do not reveal all of `h*`.

Alternatives in `Comp(D_now)` represent uncertainty about which already-complete history is actual.

### 16.3 Add a distinct ontic-Potentiality model

Represent only current structure plus admissible extensions:

`(D_now, Ext(D_now))`

without storing a hidden preselected complete future history `h*`.

This gives a formal difference between:

- unknown future;
- not-yet-selected future in the model ontology.

### 16.4 Keep event occurrence separate from state value

Stage 2 must preserve:

`state equality != event identity`.

Potential branches may revisit identical state values without representing the same event occurrence.

### 16.5 Keep equivalence criteria explicit

Stage 2 must state whether alternatives differing only by labels are distinct possibilities.

The default should compare physical/relational structures up to the relevant isomorphism or reference-frame equivalence, not count mere renamings as different worlds.

### 16.6 Keep epistemic ambiguity separate from ontic openness

A Stage 2 success criterion must require more than multiple compatible completions.

To represent ontic openness, the code/state representation must differ from the epistemic model in whether a complete future history is already selected or stored.

If both models produce the same observable predictions in the toy experiment, the correct conclusion is:

`operationally indistinguishable under the tested observables`,

not a metaphysical proof for either ontology.

## 17. Recommended Stage 2 starting point

The cleanest next experiment is a small branching temporal structure in which the same present/local data admit multiple future extensions.

Construct two explicit model classes over the same graph family:

### Epistemic-history model

- generate/select a complete history `h*` at initialization;
- expose only a current-prefix/local perspective;
- retain alternative histories only as hypotheses about hidden `h*`.

### Ontic-extension model

- store only the current prefix/structure;
- store admissible next extensions;
- do not select a complete future history until an extension event/update occurs.

Then compare:

- current observables;
- predictions over next outcomes;
- internal state representation;
- counterfactual alternatives;
- whether any operational test distinguishes the two.

This is the appropriate place to introduce Potentiality. Stage 1 should remain free of that ontology.

## 18. Stage 1 answer to the project's motivating question

Stage 1 cannot yet answer whether time itself is a perspective-invariant relational structure.

It does establish a narrower methodological result:

> In a finite classical toy model, global relational structure can sometimes be reconstructed from families of local descriptions without a privileged global naming frame, but only when the anonymous relational information is sufficiently rich; weaker or incomplete local data can leave genuinely non-isomorphic global alternatives.

A second useful result is:

> Some lower-level graph encodings can vary while a more abstract reachability/cover structure remains unchanged.

These results justify carrying relational reconstruction and equivalence-class reasoning forward as **tools** for the project.

They do not yet justify treating the surviving graph structures as the ontology of physical time.

## 19. Final Stage 1 classification

### Established infrastructure

- explicit global object `B_1`;
- explicit local-view families;
- projection and reconstruction machinery;
- labeled equality and directed graph isomorphism diagnostics;
- reachability diagnostics;
- ambiguity enumeration;
- separation of event identity from state value;
- anonymous reconstruction search.

### Strongest candidate structures for later testing

- relational reachability / cover structure under redundant-edge representation changes;
- graph isomorphism class reconstructed from sufficiently rich anonymous local relational context.

### Explicitly unresolved

- physical significance of those structures;
- block versus becoming ontology;
- ontic versus epistemic openness;
- records and temporal arrow;
- quantum / reference-frame / relativistic robustness.

## 20. Conclusion

Stage 1 has completed its intended role.

It did not discover a theory of time. It established a disciplined reconstruction framework and located several information boundaries:

- redundant information can be removed without changing reconstruction;
- missing coverage can create ambiguity or complete loss;
- state equality cannot replace event identity;
- arbitrary edge encodings contain details not preserved by reachability;
- anonymous locality may underdetermine the global graph;
- richer anonymous relational context can restore unique global structure up to isomorphism in the tested finite class.

The central methodological lesson is:

`global reconstruction depends on relational information and equivalence assumptions, not merely on the presence of global labels`.

Stage 1 should now be closed after PR review, and Stage 2 should begin by implementing **epistemic-history versus ontic-extension Potentiality as explicitly different internal model structures**.
