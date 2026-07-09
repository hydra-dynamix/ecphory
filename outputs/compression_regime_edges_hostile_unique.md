# Compression Regime Edges: hostile_unique

This sweep attacks compressibility directly by removing recurrence from the synthetic temporal motif task.

Status criteria:

- `expected_collapse`: compressibility index <= 0.05, repeated episode fraction = 0, and recurring length-3 window fraction <= 0.05.
- `partial_collapse`: compressibility remains low but some recurrence leaks through.
- `suspicious_compression`: the system appears to compress a world designed not to repeat.

## Boundary Summary

## Failure Mode Counts

- `noncompressible_as_expected`: 61

### active_dropout

- expected collapse values: [0.0, 0.05, 0.1, 0.2, 0.35, 0.5]
- `dropout_0.00` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `dropout_0.05` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=0.775439 overcapture=0.0 history_acc=0.0 delta=0.0
- `dropout_0.10` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=0.618785 overcapture=0.0 history_acc=0.0 delta=0.0
- `dropout_0.20` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=0.317757 overcapture=0.0 history_acc=0.0 delta=0.0
- `dropout_0.35` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=0.116949 overcapture=0.0 history_acc=0.0 delta=0.0
- `dropout_0.50` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=0.020607 overcapture=0.0 history_acc=0.0 delta=0.0

### active_variance

- expected collapse values: [0.02, 0.05, 0.1, 0.2, 0.35]
- `active_std_0.02` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `active_std_0.05` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `active_std_0.10` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.008939 overcapture=0.008939 history_acc=0.0 delta=0.0
- `active_std_0.20` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.113103 overcapture=0.113103 history_acc=0.0 delta=0.0
- `active_std_0.35` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.150985 overcapture=0.150985 history_acc=0.0 delta=0.0

### baseline

- expected collapse values: [0.0]
- `baseline` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0

### baseline_elevation

- expected collapse values: [0.03, 0.15, 0.3, 0.45, 0.6]
- `baseline_mean_0.03` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `baseline_mean_0.15` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.005556 overcapture=0.005556 history_acc=0.0 delta=0.0
- `baseline_mean_0.30` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.321111 overcapture=0.321111 history_acc=0.0 delta=0.0
- `baseline_mean_0.45` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.555 overcapture=0.555 history_acc=0.0 delta=0.0
- `baseline_mean_0.60` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.57 overcapture=0.57 history_acc=0.0 delta=0.0

### baseline_variance

- expected collapse values: [0.01, 0.05, 0.1, 0.2, 0.35]
- `baseline_std_0.01` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `baseline_std_0.05` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `baseline_std_0.10` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `baseline_std_0.20` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.008301 overcapture=0.008301 history_acc=0.0 delta=0.0
- `baseline_std_0.35` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=0.647491 overcapture=0.0 history_acc=0.0 delta=0.0

### event_duration

- expected collapse values: [1.0, 2.0, 3.0, 4.0, 5.0]
- `duration_1` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=0.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `duration_2` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=0.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `duration_3` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `duration_4` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `duration_5` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0

### inactive_spurious_activity

- expected collapse values: [0.0, 0.01, 0.03, 0.05, 0.1, 0.2]
- `spurious_0.00` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `spurious_0.01` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=0.758955 overcapture=0.0 history_acc=0.0 delta=0.0
- `spurious_0.03` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=0.515061 overcapture=0.0 history_acc=0.0 delta=0.0
- `spurious_0.05` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=0.382158 overcapture=0.0 history_acc=0.0 delta=0.0
- `spurious_0.10` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=0.244406 overcapture=0.0 history_acc=0.0 delta=0.0
- `spurious_0.20` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=0.199554 overcapture=0.0 history_acc=0.0 delta=0.0

### noise

- expected collapse values: [0.0, 10.0, 20.0, 40.0, 60.0]
- `noise_00` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `noise_10` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `noise_20` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `noise_40` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `noise_60` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0

### participant_cardinality

- expected collapse values: [1.0, 2.0, 3.0]
- `min_participants_1` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.000833 overcapture=0.000833 history_acc=0.0 delta=0.0
- `min_participants_2` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `min_participants_3` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=0.0 overcapture=0.0 history_acc=0.0 delta=0.0

### signal_separation

- expected collapse values: [0.55, 0.7, 0.85, 1.0, 1.15]
- `signal_0.55` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=0.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `signal_0.70` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=0.010969 overcapture=0.0 history_acc=0.0 delta=0.0
- `signal_0.85` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.023018 overcapture=0.023018 history_acc=0.0 delta=0.0
- `signal_1.00` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `signal_1.15` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.419444 overcapture=0.419444 history_acc=0.0 delta=0.0

### temporal_resolution

- expected collapse values: [1.0, 2.0, 3.0, 4.0, 5.0]
- `window_1` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `window_2` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `window_3` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `window_4` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=0.654444 overcapture=0.0 history_acc=0.0 delta=0.0
- `window_5` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=0.0 overcapture=0.0 history_acc=0.0 delta=0.0

### temporal_separation

- expected collapse values: [0.0, 1.0, 2.0, 3.0, 5.0]
- `gap_0` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `gap_1` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `gap_2` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `gap_3` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `gap_5` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0

### threshold

- expected collapse values: [0.45, 0.6, 0.75, 0.9, 1.05]
- `threshold_0.45` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.555556 overcapture=0.555556 history_acc=0.0 delta=0.0
- `threshold_0.60` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.554444 overcapture=0.554444 history_acc=0.0 delta=0.0
- `threshold_0.75` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `threshold_0.90` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=1.018388 overcapture=0.018388 history_acc=0.0 delta=0.0
- `threshold_1.05` status=expected_collapse modes=noncompressible_as_expected motif_recovery=0.0 active_coverage=0.010969 overcapture=0.0 history_acc=0.0 delta=0.0

## Interpretation

The edge of this compression regime is where detected event objects stop preserving the task-relevant temporal branch structure. In recurring worlds, that edge is operationally visible as a drop in canonical motif recovery or event-history prediction before static graph metrics become useful.

Static projection remains a deliberately lossy lower layer: event instance identity and temporal order loss stay at 1.0 by design. The question is therefore not whether static projection loses information, but which upstream event-detection settings keep enough event structure before that projection is requested.

## Hostile Compressibility Result

The hostile world intentionally removes recurrence: every episode signature is unique, contexts and outcomes are unique, and event labels are sampled without replacement.

The expected result is collapse of motif support and compressibility. Suspicious compression in this world would indicate that the detector or projection is inventing structure rather than preserving real recurrence.
