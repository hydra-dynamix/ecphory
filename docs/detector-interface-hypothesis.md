# Detector Interface Hypothesis

## L0 Observations

- Neither the sliding-window detector nor the HEU-like detector dominates.
- Each expands performance in some regions and contracts it in others.
- Both correctly collapse on the hostile unique world.
- The representation is still constrained by the information envelope rather than detector choice alone.

## L1 Inference

The results are inconsistent with:

```text
HEU-like detector is a strictly better detector.
```

The results are consistent with:

```text
Detector choice changes the operating region.
```

This is a weaker and better-supported claim.

## L2 Framing

The detector is a front-end transducer.

```text
continuous signal
    -> event detector
    -> discrete events
    -> event-first representation
    -> motif / retrieval / compression
```

Different transducers bias what becomes a discrete event commitment. If the downstream representation is robust, detector families should be swappable without changing the core event, transition, motif, retrieval, and compression machinery.

The tradeoff becomes environmental:

```text
Which detector family favors which operating region?
```

## Robustness Map

Detector evaluation should sweep:

- detector family
- detector hyperparameters
- environment

The metric is:

```text
faithful operating envelope size
```

subject to:

```text
hostile controls must still collapse
compression must not invent recurrence
target / compatible structure must be preserved where recurrence exists
```

## Capability Localization

If multiple unrelated detector families show similar envelope boundaries, that is evidence that the downstream event-first representation carries the result.

If only one detector family succeeds, the capability has been localized to that detector.

If detector choice changes the induced event vocabulary but downstream compression/retrieval remains stable, the interface decomposition is supported.

If downstream behavior changes radically with small detector changes, the decomposition is weaker than expected and the detector-representation boundary needs revision.

## Current Status

The rejected claim is:

```text
HEU-like detector is a strictly better detector.
```

The supported claim is:

```text
Detector choice changes the operating region.
```

More precisely:

```text
Across the environments tested, the downstream event-first representation remains stable under multiple detector implementations. Detector choice primarily changes the operating envelope, the range of signal conditions under which events are recovered faithfully, rather than the behavior of the downstream motif-discovery pipeline.
```

This does not prove detector independence in general. It only states what the current experiments demonstrate.

## Detector Priors

Detector families encode priors about temporal continuity:

| Detector | Prior about the world | Strength | Weakness |
| --- | --- | --- | --- |
| Sliding window | Events are local and instantaneous | Rejects noise | Misses fragmented events |
| HEU-like | Events have temporal persistence | Bridges gaps | Integrates false activity |
| Hysteresis | Events should be stable before committing | Good compromise | Still remembers persistent noise |

The next experiment should map detector-family by hyperparameter by environment, not optimize a single detector in isolation.

## Pareto Framing

Dropout and spurious activity are opposing adversaries:

```text
missing evidence -> favors longer temporal integration
false evidence   -> favors shorter temporal integration
```

The combined adversary should be interpreted as a Pareto-frontier problem. For each detector variant, measure:

- dropout robustness
- spurious robustness
- combined-environment robustness
- hostile-control collapse

Detector variants on the upper-right frontier are genuinely better under the current objective. Dominated variants should not be defended by cherry-picking one environment.

## Current Pareto Result

The combined dropout+spurious adversary is stronger than the one-axis detector maps.

Current tested variants show:

```text
no faithful detector in the combined environment
```

Low-threshold sliding-window variants are the only tested variants that degrade rather than fail under combined corruption. Stateful detectors remain better at dropout alone but are more vulnerable to spurious activity.

This supports a temporal bias-variance interpretation:

```text
longer memory -> survives missing evidence, remembers noise
shorter memory -> rejects noise, misses fragmented evidence
```

The next detector mechanisms should target this exact conflict before adding architectural complexity:

1. refractory suppression
2. minimum-duration hysteresis
3. explicit duration validation
4. multi-voice detectors only after simpler mechanisms fail
