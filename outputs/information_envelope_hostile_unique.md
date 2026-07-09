# Information Envelope: Hostile Unique World

This run attacks compressibility directly.

The synthetic world removes recurrence:

- every episode signature is unique
- every event label is sampled without replacement
- every context is unique
- every outcome is unique
- no canonical motif is expected to recur

## Result

The expected collapse occurred.

Key envelope values:

- active set unique count: `600`
- event label unique count: `600`
- event label redundancy fraction: `0.0`
- repeated event instance fraction: `0.0`
- transition unique count: `400`
- transition redundancy fraction: `0.0`
- episode signature unique count: `200`
- repeated episode instance fraction: `0.0`
- motif count: `0`
- motif support mass: `0`
- recurring length-3 window fraction: `0.0`
- compressibility index: `0.0`

## Interpretation

This is the desired failure.

The event-first representation should not invent motifs in a world designed not to repeat. Compression collapses because there is no recurrence to compress.

This separates two questions:

```text
Can the detector commit clean events?
Can the committed events support useful compression?
```

The hostile world answers the second question negatively by construction. Even with clean event commitment, there is no useful motif-level compression when episodes are unique.

## Methodological Update

The detector is part of the system.

The detector determines what information enters the event layer, what is excluded, what is merged, what is fragmented, and what later layers can compress. The operational envelope is therefore a coupled property of:

- detector dynamics
- event schema
- compression objective
- downstream prediction or retrieval objective

The useful regime is a narrow band:

```text
too little evidence -> undercapture
too much evidence   -> overcapture
right evidence      -> clean event commitment
```

The HEU is relevant because it is explicitly a temporal event-commitment system with interpretable dynamics and known expressivity limits. The next detector question is whether HEU-like independent temporal state can widen the useful event-commitment envelope without increasing overcapture.
