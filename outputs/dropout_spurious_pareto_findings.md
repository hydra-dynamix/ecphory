# Dropout-Spurious Pareto Findings

This adversary combines two opposing pressures:

```text
dropout  -> missing true evidence
spurious -> false inactive evidence
```

The goal is not to pick a detector by one environment. The goal is to locate the Pareto frontier across:

- dropout robustness
- spurious robustness
- combined robustness

## Result

No detector variant is faithful in the combined dropout+spurious environment.

Combined-environment status counts:

- `sliding_window`: 2 degraded, 8 failed
- `heu_like`: 10 failed
- `hysteresis`: 10 failed

The only degraded combined cases are:

- `branch / sliding_window_low_threshold`
- `overlap / sliding_window_low_threshold`

All other combined cases fail.

## Pareto Frontier

The frontier contains two broad kinds of detector:

1. Stateful detectors with better dropout robustness but poor spurious robustness.
2. Sliding-window detectors with better spurious robustness but weaker dropout robustness.

This is consistent with a temporal bias-variance tradeoff:

```text
longer memory -> survives missing evidence, remembers noise
shorter memory -> rejects noise, misses fragmented evidence
```

## Current Interpretation

The combined adversary is stronger than the previous one-axis maps.

It shows that widening one side of the envelope can contract the other. Hysteresis had the broadest one-axis envelope, but under simultaneous dropout and spurious activity it did not dominate.

The detector interface hypothesis remains intact, but the faithful region under mixed corruption is currently empty for tested variants.

## Next Mechanisms to Test

The next mechanisms should specifically target:

```text
bridge gaps without remembering false activity
```

Priority order:

1. refractory suppression
2. minimum-duration hysteresis
3. explicit duration validation
4. multi-voice detector only after simpler mechanisms fail

The objective remains compression fidelity, not detector elegance.
