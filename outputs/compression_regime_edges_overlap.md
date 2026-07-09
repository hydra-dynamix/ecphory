# Compression Regime Edges: overlap

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
- `no_events_detected`: 6
- `coverage_degradation`: 5
- `overcapture`: 4
- `overcapture_degradation`: 4
- `motif_degradation`: 3
- `history_prediction_degradation`: 1

### active_dropout

- faithful values: [0.0]
- degraded values: none
- failed values: [0.05, 0.1, 0.2, 0.35, 0.5]
- `dropout_0.00` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `dropout_0.05` status=failed modes=coverage_degradation;motif_loss motif_recovery=0.35 active_coverage=0.774081 overcapture=0.0 history_acc=1.0 delta=1.0
- `dropout_0.10` status=failed modes=undercapture;motif_loss motif_recovery=0.166667 active_coverage=0.601295 overcapture=0.0 history_acc=1.0 delta=1.0
- `dropout_0.20` status=failed modes=undercapture;motif_loss;history_prediction_failure;no_event_advantage_over_static motif_recovery=0.0 active_coverage=0.290323 overcapture=0.0 history_acc=0.0 delta=0.0
- `dropout_0.35` status=failed modes=undercapture;motif_loss;history_prediction_failure;no_event_advantage_over_static motif_recovery=0.0 active_coverage=0.118252 overcapture=0.0 history_acc=0.0 delta=0.0
- `dropout_0.50` status=failed modes=undercapture;motif_loss;history_prediction_failure;no_event_advantage_over_static motif_recovery=0.0 active_coverage=0.036125 overcapture=0.0 history_acc=0.0 delta=0.0

### active_variance

- faithful values: [0.02, 0.05, 0.1]
- degraded values: [0.2]
- failed values: [0.35]
- `active_std_0.02` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `active_std_0.05` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `active_std_0.10` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.004464 overcapture=0.004464 history_acc=1.0 delta=1.0
- `active_std_0.20` status=degraded modes=overcapture_degradation;motif_degradation motif_recovery=0.866667 active_coverage=1.116656 overcapture=0.116656 history_acc=1.0 delta=1.0
- `active_std_0.35` status=failed modes=overcapture_degradation;motif_loss motif_recovery=0.516667 active_coverage=1.156036 overcapture=0.156036 history_acc=1.0 delta=1.0

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
- `baseline_mean_0.15` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.005556 overcapture=0.005556 history_acc=1.0 delta=1.0
- `baseline_mean_0.30` status=degraded modes=overcapture_degradation motif_recovery=1.0 active_coverage=1.316667 overcapture=0.316667 history_acc=1.0 delta=1.0
- `baseline_mean_0.45` status=failed modes=overcapture motif_recovery=1.0 active_coverage=1.550556 overcapture=0.550556 history_acc=1.0 delta=1.0
- `baseline_mean_0.60` status=failed modes=overcapture motif_recovery=1.0 active_coverage=1.571667 overcapture=0.571667 history_acc=1.0 delta=1.0

### baseline_variance

- faithful values: [0.01, 0.05, 0.1, 0.2]
- degraded values: [0.35]
- failed values: none
- `baseline_std_0.01` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `baseline_std_0.05` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `baseline_std_0.10` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.000556 overcapture=0.000556 history_acc=1.0 delta=1.0
- `baseline_std_0.20` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.011105 overcapture=0.011105 history_acc=1.0 delta=1.0
- `baseline_std_0.35` status=degraded modes=coverage_degradation motif_recovery=0.983333 active_coverage=0.937359 overcapture=0.0 history_acc=1.0 delta=1.0

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
- `spurious_0.01` status=degraded modes=coverage_degradation motif_recovery=1.0 active_coverage=0.948367 overcapture=0.0 history_acc=1.0 delta=1.0
- `spurious_0.03` status=degraded modes=coverage_degradation motif_recovery=1.0 active_coverage=0.859394 overcapture=0.0 history_acc=1.0 delta=1.0
- `spurious_0.05` status=degraded modes=coverage_degradation motif_recovery=1.0 active_coverage=0.774388 overcapture=0.0 history_acc=1.0 delta=1.0
- `spurious_0.10` status=failed modes=undercapture;motif_degradation motif_recovery=0.933333 active_coverage=0.645344 overcapture=0.0 history_acc=1.0 delta=1.0
- `spurious_0.20` status=failed modes=undercapture;motif_degradation;history_prediction_degradation motif_recovery=0.783333 active_coverage=0.506909 overcapture=0.0 history_acc=0.894737 delta=0.886607

### noise

- faithful values: [0.0, 10.0, 20.0, 40.0, 60.0]
- degraded values: none
- failed values: none
- `noise_00` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `noise_10` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `noise_20` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `noise_40` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `noise_60` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=0.985714

### participant_cardinality

- faithful values: [1.0, 2.0]
- degraded values: none
- failed values: [3.0]
- `min_participants_1` status=faithful modes=within_useful_manifold motif_recovery=0.983333 active_coverage=1.0025 overcapture=0.0025 history_acc=1.0 delta=1.0
- `min_participants_2` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `min_participants_3` status=failed modes=no_events_detected;undercapture;motif_loss;history_prediction_failure;no_event_advantage_over_static motif_recovery=0.0 active_coverage=0.0 overcapture=0.0 history_acc=0.0 delta=0.0

### signal_separation

- faithful values: [0.85, 1.0]
- degraded values: [1.15]
- failed values: [0.55, 0.7]
- `signal_0.55` status=failed modes=no_events_detected;undercapture;motif_loss;history_prediction_failure;no_event_advantage_over_static motif_recovery=0.0 active_coverage=0.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `signal_0.70` status=failed modes=no_events_detected;undercapture;motif_loss;history_prediction_failure;no_event_advantage_over_static motif_recovery=0.0 active_coverage=0.0 overcapture=0.0 history_acc=0.0 delta=0.0
- `signal_0.85` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.023309 overcapture=0.023309 history_acc=1.0 delta=1.0
- `signal_1.00` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `signal_1.15` status=degraded modes=overcapture_degradation motif_recovery=1.0 active_coverage=1.413889 overcapture=0.413889 history_acc=1.0 delta=1.0

### temporal_resolution

- faithful values: [1.0, 2.0, 3.0]
- degraded values: none
- failed values: [4.0, 5.0]
- `window_1` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `window_2` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `window_3` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.0 overcapture=0.0 history_acc=1.0 delta=1.0
- `window_4` status=failed modes=undercapture;motif_loss motif_recovery=0.0 active_coverage=0.640556 overcapture=0.0 history_acc=1.0 delta=1.0
- `window_5` status=failed modes=no_events_detected;undercapture;motif_loss;history_prediction_failure;no_event_advantage_over_static motif_recovery=0.0 active_coverage=0.0 overcapture=0.0 history_acc=0.0 delta=0.0

### temporal_separation

- faithful values: [0.0, 1.0, 2.0, 3.0, 5.0]
- degraded values: none
- failed values: none
- `gap_0` status=faithful modes=within_useful_manifold motif_recovery=1.0 active_coverage=1.000556 overcapture=0.000556 history_acc=1.0 delta=1.0
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
- `threshold_0.90` status=faithful modes=within_useful_manifold motif_recovery=0.966667 active_coverage=1.021931 overcapture=0.021931 history_acc=1.0 delta=1.0
- `threshold_1.05` status=failed modes=undercapture;motif_loss;history_prediction_failure;no_event_advantage_over_static motif_recovery=0.0 active_coverage=0.021467 overcapture=0.0 history_acc=0.0 delta=0.0

## Interpretation

The edge of this compression regime is where detected event objects stop preserving the task-relevant temporal branch structure. In this prototype, that edge is operationally visible as a drop in canonical motif recovery or event-history prediction before static graph metrics become useful.

Static projection remains a deliberately lossy lower layer: event instance identity and temporal order loss stay at 1.0 by design. The question is therefore not whether static projection loses information, but which upstream event-detection settings keep enough event structure before that projection is requested.

## Overlap Stress Result

The overlap world uses three motifs with the same prefix `{A,B}` and the same suffix `{E,F}`. The middle event is the discriminating state: `{B,C}`, `{B,E}`, or `{B,G}`.

A faithful event representation should therefore show low current-event certainty at the shared prefix, high recovery for all three full motifs, and high two-event-history prediction into the shared suffix.
