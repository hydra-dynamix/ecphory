# HEU-Like Detector Comparison Summary

This comparison treats the detector as part of the event-first representation system.

Detectors compared:

- `sliding_window`: original mean-threshold coactivation detector.
- `heu_like`: bounded envelope accumulation with recovery/leak and thresholded event commitment.

The HEU-like detector is not the full HEU paper implementation. It is a minimal stateful event-commitment adversary.

## Result

The HEU-like detector widens some parts of the useful envelope and narrows others.

It helps when the problem is temporal undercommitment:

- dropout at `0.05`: failed -> degraded
- low threshold `0.60`: failed by overcapture -> faithful
- window size `4`: failed by undercapture/motif loss -> faithful

It hurts when the problem is spurious inactive activity:

- spurious `0.05`: degraded -> failed

It preserves the expected hostile-world collapse:

- `hostile_unique`: expected collapse under both detectors
- motif count remains `0`
- compressibility index remains `0`

## Interpretation

The detector is part of the representation.

The HEU-like stateful detector can bridge short missing evidence and avoid some sliding-window threshold artifacts, but the same temporal memory makes it vulnerable to spurious activity. It converts some undercapture failures into usable degraded/faithful cases, while converting some noisy cases into motif loss.

This supports the narrow-band reading:

```text
too little temporal persistence -> undercapture
too much persistence/noise memory -> spurious commitment
useful regime -> stateful commitment with controlled decay
```

The next adversary should not ask whether HEU-like dynamics are better in general. They are not. It should ask which detector parameters trace the useful envelope:

- attack rate
- recovery rate
- leak rate
- commitment threshold
- refractory or hysteresis behavior
- per-unit independent state versus globally coupled detector settings

The compression target remains unchanged: widen the faithful envelope without inventing recurrence in hostile worlds.
