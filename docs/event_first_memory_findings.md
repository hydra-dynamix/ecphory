# Event-First Memory Findings

Status: frozen interpretation after synthetic adversarial sweeps.

## Core Method

The system is event-first, not graph-first.

```text
RawSignal
  -> Event
  -> Transition
  -> Episode
  -> CandidatePattern / Motif View
  -> Structural Signature Index Payload
```

The durable object is evidence. Static graphs, motifs, classifiers, and labels are views.

## Architecture Commitments

Structural signatures are the only retrieval keys.

```json
{
  "signature": ["{A,B}", "{B,C}", "{C,D}"],
  "signature_length": 3
}
```

Context, outcome, predicted next events, entropy, classifier status, and interpretation labels live inside the payload.

```json
{
  "support": 60,
  "contexts": [],
  "outcomes": [],
  "predicted_next_events": [],
  "annotations": {}
}
```

No semantic annotation participates in signature identity. No semantic annotation suppresses storage of evidence.

## Primary Result

The event-first hierarchy preserves reusable temporal structure better than exact event recovery in useful imperfect-detector regimes.

Representative combined dropout/spurious results:

```text
branch:
  exact recovery ~= 0.887
  motif support ~= 0.989
  Representation Gain ~= +0.103

overlap:
  exact recovery ~= 0.887
  motif support ~= 0.979
  Representation Gain ~= +0.092
```

The metric is discriminative. Over-entropic union detector variants show negative gain, and hostile unique worlds collapse as expected.

```text
too little recall          -> undercapture
too much candidate entropy -> identity collapse / hostile leak
stable imperfect recurrence -> positive Representation Gain
```

## Detector Result

The detector is part of the operating envelope, but not the whole explanation.

The strongest detector conclusion is negative:

```text
HEU-like detector is not strictly better.
```

The supported claim is:

```text
Detector choice changes the operating region.
```

Useful decomposition:

```text
continuous signal
  -> event detector
  -> discrete events
  -> event-first representation
  -> transitions / episodes / motifs / retrieval
```

Permissive detectors need enough recall, but too much candidate entropy destabilizes identity. Under-admitting evidence cannot be repaired downstream.

## Adversarial Findings

The strongest failures came from exact-event adversarial streams, which bypass the detector and therefore test the representation/index layer directly.

### Clean Unique Control

Unique triplets did not hallucinate recurrence.

```text
length-3 recurrence = 0
compressibility = 0
```

This means the system is not inventing arbitrary recurrence in a fully unique world.

### Hidden Novelty Alias

Same visible sequence, unique latent context/outcome.

```text
visible recurrence = 1.0
outcome purity ~= 0
```

Old interpretation: false compression.

Frozen interpretation: valid structural retrieval key with ambiguous payload. The system should retrieve all counterfactual evidence, not choose a meaning.

### Contradictory Outcomes

Same event sequence, conflicting outcomes.

```text
visible recurrence = 1.0
history accuracy = 1.0
outcome purity low
```

This is not a memory failure if the payload preserves contradiction. It is a failure only if a downstream layer treats the pattern as outcome-determinate.

### Chance Recurrence At Scale

Small vocabularies generate cheap short-window recurrence.

Scaled random-small-vocabulary world:

```text
sequence length 8:
  full-sequence recurrence = 0.0
  length-3 recurrence      = 0.999074
```

Longer full signatures fix full-sequence chance collision. They do not fix short-window chance recurrence.

## Signature-Length Boundary

Current boundary:

```text
length 2-3:
  useful local fragments
  high chance-collision risk
  should not be treated as resolved memories

length 4+ / full episode:
  better retrieval anchors
  lower chance collision
  still vulnerable to hidden variables
```

Short patterns are evidence fragments. Longer signature families are safer retrieval anchors.

## Novelty Status

There is no principled novelty model in the core system yet.

Current core behavior:

```text
Novel      = not previously seen
Recurring  = support >= 2
Interesting / worth indexing = not formally defined
```

The optional evidence-index classifier is not core. It is a view.

It helps reframe hidden novelty and contradictory outcomes as ambiguous evidence, but it does not solve chance recurrence promotion in small-vocabulary worlds. It has not earned a core retrieval role.

## HEU Novelty-Gate Inspection

The later HEU novelty gate was inspected in:

```text
gb10:/home/bakobi/repos/bako/research/heu/heu-campaign-worktrees/near-family-mitigation/multiscale-prototype/experiments/near_family_threshold_novelty_gate.py
```

Its mechanism was token novelty against the best prototype:

```text
novelty_fraction = unseen_tokens / incoming_tokens
if novelty_fraction >= novelty_gate:
  create new prototype
```

Result:

```text
384 cases
48 settings
viable settings = 0
best setting used novelty_gate=None
```

Do not port that gate directly.

The useful HEU lesson is split/merge and coverage diagnostics:

```text
assignment margin
top-two gap
coverage
split/merge detection
ambiguous retrieval margins
abstain rather than false commitment
```

Profile coverage was the important result:

```text
strict passes   = 18/24
coverage passes = 24/24
```

This supports the Ecphory rule: preserve evidence and measure useful coverage, rather than forcing a single canonical interpretation.

## Structural Index Payload

Two payload dump modes were generated:

```text
signature_index_payloads_naive.jsonl
signature_index_payloads_evidence_index.jsonl
```

Boundary validation:

```text
naive:
  records = 246016
  bad_keys = 0
  annotations = 0

evidence_index:
  records = 246016
  bad_keys = 0
  annotations = 246016
```

Both modes keep keys purely structural. Classifier output is only payload annotation.

The JSONL dumps are large generated artifacts and are intentionally excluded from git. CSV and Markdown summaries are committed instead.

## Current Claim

Supported:

```text
An event-first evidence store can preserve temporal structure that static projection loses.
Repeated imperfect event streams can consolidate into stable reusable signature families in a bounded operating envelope.
Contradictory and negative evidence remain useful if stored as payload evidence instead of collapsed into semantic meaning.
```

Not supported:

```text
The current system has semantic memory.
Support count alone is a novelty model.
Short recurring subsequences are reliable memories at scale.
The optional classifier should select or suppress core evidence.
The HEU token-novelty gate should be ported directly.
```

## Next Work

The next useful phase is a real-world retrieval example.

Recommended structure:

```text
collect real event stream
derive structural signatures
store payload evidence
retrieve by partial/full signature family
inspect payload contradictions and variants
measure retrieval utility
```

Primary metrics should move from compression to retrieval:

```text
true family recall
candidate set size
counterexample inclusion
false confidence
payload entropy surfaced
downstream continuation utility
```

The core question becomes:

```text
Does structural signature retrieval surface the right evidence without prematurely deciding what it means?
```
