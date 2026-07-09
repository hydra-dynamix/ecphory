# Compression Regime Edges: branch

This sweep estimates where event-first compression remains faithful, becomes degraded, or fails for the selected synthetic temporal motif task.

Status criteria:

- `faithful`: active coverage is between 0.95 and 1.10, canonical motif recovery >= 0.95, event-history accuracy >= 0.95, and predictive delta over static >= 0.50.
- `degraded`: active coverage is between 0.70 and 1.50, canonical motif recovery >= 0.70, event-history accuracy >= 0.70, and predictive delta remains positive.
- `failed`: one or more degraded criteria are not met.

## Boundary Summary

## Failure Mode Counts

- `within_useful_manifold`: 34
- `undercapture`: 14
- `motif_loss`: 14
- `history_prediction_failure`: 10
- `no_event_advantage_over_static`: 10
- `no_events_detected`: 7
- `coverage_degradation`: 5
- `overcapture`: 4
- `overcapture_degradation`: 3
- `motif_degradation`: 2
- `history_prediction_degradation`: 1

### active_dropout

- faithful values: [0.0]
- degraded values: none
- failed values: [0.05, 0.1, 0.2, 0.35, 0.5]
- `dropout_0.00` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `dropout_0.05` status=failed modes=coverage_degradation;motif_loss motif_recovery=0.383333 active_coverage=0.797342 overcapture=0.0 history_acc=1.0 delta=1.0
- `dropout_0.10` status=failed modes=undercapture;motif_loss motif_recovery=0.116667 active_coverage=0.579876 overcapture=0.0 history_acc=1.0 delta=1.0
- `dropout_0.20` status=failed modes=undercapture;motif_loss;history_prediction_failure;no_event_advantage_over_static motif_recovery=0.0 active_coverage=0.331198 overcapture=0.0 history_acc=0.0 delta=0.0
- `dropout_0.35` status=failed modes=undercapture;motif_loss;history_prediction_failure;no_event_advantage_over_static motif_recovery=0.0 active_coverage=0.116334 overcapture=0.0 history_acc=0.0 delta=0.0
- `dropout_0.50` status=failed modes=undercapture;motif_loss;history_prediction_failure;no_event_advantage_over_static motif_recovery=0.0 active_coverage=0.02915 overcapture=0.0 history_acc=0.0 delta=0.0

### active_variance

- faithful values: [0.02, 0.05, 0.1]
- degraded values: [0.2]
- failed values: [0.35]
- `active_std_0.02` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `active_std_0.05` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `active_std_0.10` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.008786 overcapture=0.008786 history_acc=1.0 delta=1.0
- `active_std_0.20` status=degraded modes=overcapture_degradation;motif_degradation motif_recovery=0.883333 active_coverage=1.132712 overcapture=0.132712 history_acc=1.0 delta=1.0
- `active_std_0.35` status=failed modes=motif_loss motif_recovery=0.35 active_coverage=1.084906 overcapture=0.084906 history_acc=1.0 delta=1.0

### baseline

- faithful values: [0.0]
- degraded values: none
- failed values: none
- `baseline` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0

### baseline_elevation

- faithful values: [0.03, 0.15]
- degraded values: [0.3]
- failed values: [0.45, 0.6]
- `baseline_mean_0.03` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `baseline_mean_0.15` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.000794 overcapture=0.000794 history_acc=1.0 delta=1.0
- `baseline_mean_0.30` status=degraded modes=overcapture_degradation motif_recovery=1.0 active_coverage=1.323016 overcapture=0.323016 history_acc=1.0 delta=1.0
- `baseline_mean_0.45` status=failed modes=overcapture motif_recovery=1.0 active_coverage=1.553175 overcapture=0.553175 history_acc=1.0 delta=1.0
- `baseline_mean_0.60` status=failed modes=overcapture motif_recovery=1.0 active_coverage=1.569841 overcapture=0.569841 history_acc=1.0 delta=1.0

### baseline_variance

- faithful values: [0.01, 0.05, 0.1, 0.2]
- degraded values: [0.35]
- failed values: none
- `baseline_std_0.01` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `baseline_std_0.05` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.000794 overcapture=0.000794 history_acc=1.0 delta=1.0
- `baseline_std_0.10` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.000794 overcapture=0.000794 history_acc=1.0 delta=1.0
- `baseline_std_0.20` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.00595 overcapture=0.00595 history_acc=1.0 delta=1.0
- `baseline_std_0.35` status=degraded modes=coverage_degradation motif_recovery=1.0 active_coverage=0.941134 overcapture=0.0 history_acc=1.0 delta=1.0

### event_duration

- faithful values: [3.0, 4.0, 5.0]
- degraded values: none
- failed values: [1.0, 2.0]
- `duration_1` status=failed modes=no_events_detected;undercapture;motif_loss;history_prediction_failure;no_event_advantage_over_static motif_recovery=0.0 active_coverage=0.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `duration_2` status=failed modes=no_events_detected;undercapture;motif_loss;history_prediction_failure;no_event_advantage_over_static motif_recovery=0.0 active_coverage=0.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `duration_3` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `duration_4` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `duration_5` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0

### inactive_spurious_activity

- faithful values: [0.0]
- degraded values: [0.01, 0.03, 0.05]
- failed values: [0.1, 0.2]
- `spurious_0.00` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `spurious_0.01` status=degraded modes=coverage_degradation motif_recovery=1.0 active_coverage=0.942056 overcapture=0.0 history_acc=1.0 delta=1.0
- `spurious_0.03` status=degraded modes=coverage_degradation motif_recovery=1.0 active_coverage=0.862517 overcapture=0.0 history_acc=1.0 delta=1.0
- `spurious_0.05` status=degraded modes=coverage_degradation motif_recovery=0.983333 active_coverage=0.784429 overcapture=0.0 history_acc=1.0 delta=1.0
- `spurious_0.10` status=failed modes=undercapture motif_recovery=0.966667 active_coverage=0.635636 overcapture=0.0 history_acc=1.0 delta=1.0
- `spurious_0.20` status=failed modes=undercapture;motif_degradation;history_prediction_degradation motif_recovery=0.733333 active_coverage=0.524967 overcapture=0.0 history_acc=0.888889 delta=0.888889

### noise

- faithful values: [0.0, 10.0, 20.0, 40.0, 60.0]
- degraded values: none
- failed values: none
- `noise_00` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `noise_10` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `noise_20` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `noise_40` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=0.989583
- `noise_60` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=0.990909

### participant_cardinality

- faithful values: [1.0, 2.0]
- degraded values: none
- failed values: [3.0]
- `min_participants_1` status=faithful modes=within_useful_manifold motif_recovery=0.983333 active_coverage=1.00119 overcapture=0.00119 history_acc=1.0 delta=1.0
- `min_participants_2` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `min_participants_3` status=failed modes=no_events_detected;undercapture;motif_loss;history_prediction_failure;no_event_advantage_over_static motif_recovery=0.0 active_coverage=0.0 overcapture=0.0 history_acc=0.0 delta=0.0

### signal_separation

- faithful values: [0.85, 1.0]
- degraded values: [1.15]
- failed values: [0.55, 0.7]
- `signal_0.55` status=failed modes=no_events_detected;undercapture;motif_loss;history_prediction_failure;no_event_advantage_over_static motif_recovery=0.0 active_coverage=0.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `signal_0.70` status=failed modes=no_events_detected;undercapture;motif_loss;history_prediction_failure;no_event_advantage_over_static motif_recovery=0.0 active_coverage=0.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `signal_0.85` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.020243 overcapture=0.020243 history_acc=1.0 delta=1.0
- `signal_1.00` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `signal_1.15` status=degraded modes=overcapture_degradation motif_recovery=1.0 active_coverage=1.414286 overcapture=0.414286 history_acc=1.0 delta=1.0

### temporal_resolution

- faithful values: [1.0, 2.0, 3.0]
- degraded values: none
- failed values: [4.0, 5.0]
- `window_1` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `window_2` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `window_3` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `window_4` status=failed modes=undercapture;motif_loss motif_recovery=0.083333 active_coverage=0.64127 overcapture=0.0 history_acc=1.0 delta=1.0
- `window_5` status=failed modes=no_events_detected;undercapture;motif_loss;history_prediction_failure;no_event_advantage_over_static motif_recovery=0.0 active_coverage=0.0 overcapture=0.0 history_acc=0.0 delta=0.0

### temporal_separation

- faithful values: [0.0, 1.0, 2.0, 3.0, 5.0]
- degraded values: none
- failed values: none
- `gap_0` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `gap_1` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `gap_2` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `gap_3` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `gap_5` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0

### threshold

- faithful values: [0.75, 0.9]
- degraded values: none
- failed values: [0.45, 0.6, 1.05]
- `threshold_0.45` status=failed modes=overcapture motif_recovery=1.0 active_coverage=1.555556 overcapture=0.555556 history_acc=1.0 delta=1.0
- `threshold_0.60` status=failed modes=overcapture motif_recovery=1.0 active_coverage=1.555556 overcapture=0.555556 history_acc=1.0 delta=1.0
- `threshold_0.75` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `threshold_0.90` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.021484 overcapture=0.021484 history_acc=1.0 delta=1.0
- `threshold_1.05` status=failed modes=no_events_detected;undercapture;motif_loss;history_prediction_failure;no_event_advantage_over_static motif_recovery=0.0 active_coverage=0.0 overcapture=0.0 history_acc=0.0 delta=0.0

## Interpretation

The edge of this compression regime is where detected event objects stop preserving the task-relevant temporal branch structure. In this prototype, that edge is operationally visible as a drop in canonical motif recovery or event-history prediction before static graph metrics become useful.

Static projection remains a deliberately lossy lower layer: event instance identity and temporal order loss stay at 1.0 by design. The question is therefore not whether static projection loses information, but which upstream event-detection settings keep enough event structure before that projection is requested.
