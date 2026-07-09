# LDGR Research Methodology

LDGR Research exists to destroy hypotheses as quickly as possible while preserving any surviving evidence.

The method is not designed to prove a theory. A theory only survives because repeated attempts to kill it fail.

## Core Thesis

Research proceeds by adversarial model construction:

```text
Hypothesis
    -> strongest adversary
    -> counterexample search
    -> boundary characterization
    -> theory refinement
```

There is no step called "prove the hypothesis."

Positive evidence extends confidence. Negative evidence reduces the search space. Both are useful only when the evidence is frozen and the interpretation remains revisable.

## Principles

### 1. State the Smallest Possible Claim

Never claim more than the experiment actually measures.

Prefer:

```text
Event-first representations preserve temporal information destroyed by static projection.
```

Avoid:

```text
Event-first memory is the substrate of cognition.
```

The larger theory waits until smaller claims survive repeated destructive tests.

### 2. Define Success Before Execution

No moving the goalposts.

Every experiment must declare:

- hypothesis
- null
- acceptance criteria
- rejection criteria
- measured variables
- expected artifacts

Criteria must be concrete enough that a failed run cannot be reinterpreted into success after the fact.

### 3. Assume the Hypothesis Is Wrong

The purpose of an experiment is to find the smallest counterexample.

The default posture is:

```text
This representation is probably discarding something important.
This mechanism is probably overfit to the easy case.
This result probably fails under a cleaner adversary.
```

### 4. Prefer Destructive Experiments

Every experiment should attempt to answer:

```text
Where does this fail?
```

Failure boundaries are first-class results. A boundary is more valuable than a broad positive claim because it constrains the theory.

### 5. Separate Mechanism From Interpretation

Measure mechanisms:

- prediction
- compression
- retrieval
- generalization
- scaling

Do not prematurely rename them as:

- memory
- reasoning
- intelligence
- understanding
- subjective time

Interpretation can be layered on later, after the mechanism survives.

### 6. Distinguish Representation From Computation

Static representations are views.

The underlying computation or process is the primary object of study. Whenever possible, preserve the process rather than its projection.

For event-first memory work:

```text
raw signals -> events -> transitions -> motifs -> derived views
```

Static graphs, embeddings, labels, and summaries are projections. They must not replace the process unless they have been shown to preserve the information required by the computation under study.

### 6.1 Treat the Detector as Part of the System

The detector is not an external preprocessing detail.

If a representation depends on a detector, then the detector and representation are coupled. The detector defines what can enter the representation, what is excluded, what is merged, what is fragmented, and what becomes available for later compression.

Evaluate:

- detector dynamics
- representation schema
- compression behavior
- downstream predictive or retrieval behavior

as one system.

The operational envelope is usually bounded on both sides:

```text
too little evidence -> undercapture
too much evidence   -> overcapture
useful regime       -> narrow band of sufficient event commitment
```

This mirrors the HEU lesson: globally coupled temporal parameters can impose strict expressivity limits, and independent state or adaptive dynamics may be required when temporal regimes conflict.

### 6.2 Define Detector Interfaces, Not Detector Winners

The current evidence does not support:

```text
HEU-like detectors are strictly better.
```

It supports the weaker claim:

```text
Detector choice changes the operating region.
```

Treat the detector as a front-end transducer:

```text
continuous signal
    -> detector family and detector parameters
    -> discrete event commitments
    -> event-first representation
    -> motif, retrieval, and compression views
```

Different detector families induce different event vocabularies and therefore different representative sequences. The downstream machinery should remain the same wherever possible; the detector changes which environments enter the faithful region.

The scientific question is not:

```text
Is detector X biologically plausible?
```

It is:

```text
Which detector maximizes the faithful region of the operating envelope while preserving hostile controls?
```

Detector research should be mapped across three axes:

- detector family
- detector hyperparameters
- environment

If multiple unrelated detector families produce similar envelope boundaries, the downstream event-first representation is likely carrying the result. If only one detector family succeeds, the capability has been localized to the detector.

### 7. Representations Are Guilty Until Proven Sufficient

Every representation must justify itself.

The central question is:

```text
What information did this representation throw away?
```

Do not trust a representation because it works on a benchmark. Ask what it destroys:

- temporal order
- event identity
- participant sets
- duration
- context
- branch structure
- outcome distributions
- uncertainty
- rare variants
- causal sequence

A representation is sufficient only for a specified computation under specified conditions.

### 8. Compress Only After Validation

Do not invent abstractions first.

Allow abstractions to emerge from repeated successful observations. Compression must be evaluated against task-relevant information, not aesthetics or convenience.

Compression analysis should separate:

- intended loss
- harmless loss
- harmful loss
- overcapture
- undercapture
- prediction-preserving but evidence-destroying compression

### 9. Treat Negative Results as Progress

A rejected hypothesis is an asset.

It removes part of the search space and forces the theory to become smaller, sharper, or false.

The correct response to failure is not rescue. It is classification:

- What failed?
- Under what condition?
- Which measurement detected it?
- Did the mechanism fail, or did the representation fail?
- Did compression erase necessary information?

### 10. Freeze Evidence

Artifacts are immutable.

Interpretation may change. Evidence does not.

Every durable claim should point to frozen evidence:

- source files
- generated data
- reports
- command outputs
- validation records
- LDGR observations
- LDGR artifacts
- LDGR decisions

When interpretation changes, create a new interpretation artifact. Do not rewrite evidence to match the current theory.

### 11. Build Only What the Evidence Demands

Do not add mechanisms because they sound plausible.

Do not add:

- attention
- novelty
- subjective time
- semantics
- hierarchy
- agents
- memory claims

unless experiments demonstrate that the current mechanism cannot explain the observations.

The happy path is built first. Additional mechanisms are admitted only when the evidence forces them.

## Required Experiment Record

Every LDGR Research experiment should create or reference a record with:

```text
claim:
null:
adversary:
acceptance_criteria:
rejection_criteria:
measures:
artifacts:
validation:
failure_modes:
decision:
```

Minimal example:

```text
claim:
  Event-first representations preserve branch-disambiguating temporal structure lost in static projection.

null:
  Static projection predicts future events as well as event history.

adversary:
  Overlapping motifs with shared prefixes and shared suffixes.

acceptance_criteria:
  Canonical motif recovery >= 0.95.
  Event-history prediction accuracy >= 0.95.
  Event-history predictive delta over static projection >= 0.50.
  Active event coverage remains in the faithful compression band.

rejection_criteria:
  Motif recovery < 0.70.
  Event-history prediction accuracy < 0.70.
  Predictive delta <= 0.
  Compression undercaptures or overcaptures task-relevant signal.
```

## Compression Discipline

Compression is not an implementation detail. It is a central object of study.

For every compression step, record:

- source layer
- target layer
- intended retained information
- intended discarded information
- observed retained information
- observed discarded information
- task-relevant loss
- compression ratio
- coverage ratio
- overcapture ratio
- predictive delta

Example layer questions:

```text
RawSignal -> Event:
  Did event extraction preserve threshold-active coactivation cells?
  Did it overcapture inactive cells?
  Did it fragment or merge events?

Event -> Transition:
  Did adjacency preserve branch structure?
  What event payload is lost without joining back to events?

Episode -> Motif:
  Which recurring sequences survived?
  Which variants were erased?

Event -> StaticProjection:
  Which temporal, contextual, and outcome information disappeared?
```

Prediction without compression fidelity is not enough. A representation can predict while destroying evidence needed for later explanation, replay, or theory refinement.

## Failure Taxonomy

Failure modes should be named, not hand-waved.

Current event-first compression failure categories:

- `no_events_detected`
- `undercapture`
- `coverage_degradation`
- `overcapture`
- `overcapture_degradation`
- `motif_loss`
- `motif_degradation`
- `history_prediction_failure`
- `history_prediction_degradation`
- `no_event_advantage_over_static`

These names are provisional. They should be revised when new experiments expose sharper distinctions.

## Boundary Characterization

A successful experiment does not end with "it worked."

It should produce a boundary statement:

```text
The mechanism survives under conditions A, B, C.
It degrades under D and E.
It fails under F and G.
The likely cause of failure is H.
The next adversary should test I.
```

Boundary characterization is the useful output. It defines the manifold where the mechanism is currently justified.

## LDGR Usage

LDGR is the continuity layer.

Every research slice should:

1. Run `ldgr status`.
2. Start one bounded work item.
3. Record observations only when they add durable continuity.
4. Attach artifacts as evidence.
5. Record validation.
6. Close the run with a decision.
7. Queue the next adversarial slice when needed.

The chat is transient. LDGR is the causal record.

## Build Discipline

Build only what the current experiment requires.

Do not add scaling tests until the mechanism has survived local boundary characterization. Do not add visualizations until the data and compression metrics are stable. Do not add semantic layers until non-semantic mechanisms fail in a way that demands them.

The system should remain small enough that failures are interpretable.

## Current Methodological Summary

The methodology is falsification-first, but more specifically:

```text
adversarial model construction with frozen evidence
```

The operating rule is:

```text
Representations are guilty until proven sufficient.
```

The research loop is:

```text
state the smallest claim
define failure before execution
construct the strongest adversary
run the destructive experiment
measure mechanism and compression separately
freeze artifacts
classify failures
map the useful manifold
refine or reject the theory
```
