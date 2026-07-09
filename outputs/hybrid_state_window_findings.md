# Hybrid Stateful-Window Detector Findings

Question:

```text
What happens if a stateful detector is combined with a sliding-window evidence gate?
```

Hypothesis:

```text
State bridges dropout, local window evidence rejects spurious activity.
```

## Result

The hybrid partially works, but does not solve the combined adversary.

Hybrid variants improve the spurious robustness of pure stateful detectors:

- pure HEU-like spurious scores are roughly `0.26-0.28`
- hybrid spurious scores are roughly `0.48-0.51`

Hybrid variants preserve much of the dropout robustness of pure stateful detectors:

- hybrid dropout scores are roughly `0.71-0.75`
- pure HEU-like dropout scores are roughly `0.75-0.78`

But the combined dropout+spurious environment still fails:

- all hybrid variants fail in the combined environment
- low-threshold sliding-window remains the only tested variant that degrades rather than fails under combined corruption

## Interpretation

The hybrid moves the Pareto point toward the middle:

```text
better spurious rejection than pure stateful detectors
better dropout robustness than most sliding-window detectors
```

But it does not reach the useful region for simultaneous missing and false evidence.

The local evidence gate appears to suppress some false stateful commitments, but it also reintroduces undercapture when true evidence is fragmented. The hybrid therefore inherits both sides of the tradeoff:

```text
state helps bridge gaps
local confirmation rejects noise
local confirmation also blocks some gap bridging
```

## Current Status

The combined adversary remains unsolved.

This result argues for mechanisms that distinguish isolated false activity from valid fragmented event evidence, rather than simply requiring both state and local evidence at the same instant.

Next candidates:

1. refractory suppression after event commitment
2. minimum-duration hysteresis
3. duration validation over candidate events
4. delayed commitment: accumulate first, validate event duration/shape after the fact
