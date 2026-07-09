# Detector Robustness Findings

This run maps detector family x hyperparameter x environment using the same downstream event-first pipeline.

Detector families:

- `sliding_window`
- `heu_like`
- `hysteresis`

Worlds/environments:

- branch clean
- overlap clean
- hostile unique
- dropout
- spurious inactive activity
- low threshold
- high threshold
- window blur

## Family-Level Envelope

Excluding hostile controls:

- `hysteresis`: 27 faithful, 10 degraded, 13 failed
- `heu_like`: 15 faithful, 13 degraded, 22 failed
- `sliding_window`: 11 faithful, 9 degraded, 30 failed

Including hostile controls, all detector variants collapsed correctly:

- `sliding_window`: 5 expected collapses
- `heu_like`: 5 expected collapses
- `hysteresis`: 5 expected collapses

No detector invented recurrence in the hostile unique world.

## Environment-Level Findings

Clean branch and overlap worlds are easy. Most detector variants are faithful.

Window blur favors stateful or onset/offset detectors:

- `heu_like` default / fast decay / high commit are faithful.
- all hysteresis variants are faithful.
- sliding window only succeeds when the detector window is shortened.

Dropout remains hard:

- no variant is faithful.
- `heu_like` and `hysteresis` variants often degrade instead of failing.
- sliding-window default fails.

Spurious inactive activity exposes the opposite weakness:

- no variant is faithful.
- sliding-window variants degrade.
- `heu_like` and `hysteresis` mostly fail.

This is the clearest detector tradeoff so far:

```text
stateful persistence helps missing evidence
stateful persistence hurts spurious evidence
stateless locality helps avoid remembering noise
```

## Current Best Interpretation

The detector interface hypothesis is supported.

The downstream event-first machinery remains stable across detector families, but detector choice changes which environments enter the faithful or degraded envelope.

The result does not support a universal detector winner. It supports a detector-family x environment map.

## Next Adversary

The next useful experiment should combine dropout and spurious activity in the same environment.

That tests whether any detector can preserve recurrence under simultaneous missing evidence and false evidence. It directly targets the apparent tradeoff:

```text
bridge gaps without remembering noise
```

Candidate detector mechanisms:

- refractory suppression
- hysteresis with minimum duration
- HEU-like envelope with faster recovery
- multi-voice detector with transient and sustain channels
- explicit event-duration validation
