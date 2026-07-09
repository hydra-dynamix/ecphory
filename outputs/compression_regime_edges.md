# Compression Regime Edges

This sweep estimates where event-first compression remains faithful, becomes degraded, or fails for the synthetic branch-disambiguation task.

Status criteria:

- `faithful`: active coverage is between 0.95 and 1.10, canonical motif recovery >= 0.95, event-history accuracy >= 0.95, and predictive delta over static >= 0.50.
- `degraded`: active coverage is between 0.70 and 1.50, canonical motif recovery >= 0.70, event-history accuracy >= 0.70, and predictive delta remains positive.
- `failed`: one or more degraded criteria are not met.

## Boundary Summary

### baseline

- faithful values: [0.0]
- degraded values: none
- failed values: none
- `baseline` status=faithful motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0

### event_duration

- faithful values: [3.0, 4.0, 5.0]
- degraded values: none
- failed values: [1.0, 2.0]
- `duration_1` status=failed motif_recovery=0.0 active_coverage=0.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `duration_2` status=failed motif_recovery=0.0 active_coverage=0.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `duration_3` status=faithful motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `duration_4` status=faithful motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `duration_5` status=faithful motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0

### noise

- faithful values: [0.0, 10.0, 20.0, 40.0, 60.0]
- degraded values: none
- failed values: none
- `noise_00` status=faithful motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `noise_10` status=faithful motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `noise_20` status=faithful motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `noise_40` status=faithful motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `noise_60` status=faithful motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0

### signal_separation

- faithful values: [0.85, 1.0]
- degraded values: [1.15]
- failed values: [0.55, 0.7]
- `signal_0.55` status=failed motif_recovery=0.0 active_coverage=0.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `signal_0.70` status=failed motif_recovery=0.0 active_coverage=0.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `signal_0.85` status=faithful motif_recovery=0.983333 active_coverage=1.028642 overcapture=0.028642 history_acc=1.0 delta=1.0
- `signal_1.00` status=faithful motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `signal_1.15` status=degraded motif_recovery=1.0 active_coverage=1.412698 overcapture=0.412698 history_acc=1.0 delta=1.0

### temporal_resolution

- faithful values: [1.0, 2.0, 3.0]
- degraded values: none
- failed values: [4.0, 5.0]
- `window_1` status=faithful motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `window_2` status=faithful motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `window_3` status=faithful motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `window_4` status=failed motif_recovery=0.066667 active_coverage=0.674603 overcapture=0.0 history_acc=1.0 delta=1.0
- `window_5` status=failed motif_recovery=0.0 active_coverage=0.0 overcapture=0.0 history_acc=0.0 delta=0.0

### threshold

- faithful values: [0.75, 0.9]
- degraded values: none
- failed values: [0.45, 0.6, 1.05]
- `threshold_0.45` status=failed motif_recovery=1.0 active_coverage=1.555556 overcapture=0.555556 history_acc=1.0 delta=1.0
- `threshold_0.60` status=failed motif_recovery=1.0 active_coverage=1.554762 overcapture=0.554762 history_acc=1.0 delta=1.0
- `threshold_0.75` status=faithful motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `threshold_0.90` status=faithful motif_recovery=0.983333 active_coverage=1.015758 overcapture=0.015758 history_acc=1.0 delta=1.0
- `threshold_1.05` status=failed motif_recovery=0.0 active_coverage=0.0 overcapture=0.0 history_acc=0.0 delta=0.0

## Interpretation

The edge of this compression regime is where detected event objects stop preserving the task-relevant temporal branch structure. In this prototype, that edge is operationally visible as a drop in canonical motif recovery or event-history prediction before static graph metrics become useful.

Static projection remains a deliberately lossy lower layer: event instance identity and temporal order loss stay at 1.0 by design. The question is therefore not whether static projection loses information, but which upstream event-detection settings keep enough event structure before that projection is requested.
