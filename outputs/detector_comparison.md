# Detector Comparison

This compares the original sliding-window detector against a simple HEU-like stateful event-commitment detector.

The HEU-like detector is intentionally minimal: bounded envelope accumulation, recovery/leak, and thresholded event commitment. It is not the full HEU paper implementation.

## Case Results

### branch_baseline

- `heu_like` status=faithful modes=within_useful_manifold events=420 motifs=25 motif_recovery=1.0 coverage=1.0 overcapture=0.0 history_acc=1.0 compressibility=0.553351
- `sliding_window` status=faithful modes=within_useful_manifold events=420 motifs=25 motif_recovery=1.0 coverage=1.0 overcapture=0.0 history_acc=1.0 compressibility=0.553351

### branch_dropout_005

- `heu_like` status=degraded modes=coverage_degradation;motif_degradation;history_prediction_degradation events=447 motifs=36 motif_recovery=0.866667 coverage=0.943301 overcapture=0.0 history_acc=0.849057 compressibility=0.53869
- `sliding_window` status=failed modes=coverage_degradation;motif_loss events=302 motifs=21 motif_recovery=0.366667 coverage=0.761025 overcapture=0.0 history_acc=1.0 compressibility=0.506664

### branch_spurious_005

- `heu_like` status=failed modes=coverage_degradation;motif_loss;history_prediction_failure events=898 motifs=230 motif_recovery=0.066667 coverage=0.931328 overcapture=0.0 history_acc=0.356061 compressibility=0.227644
- `sliding_window` status=degraded modes=coverage_degradation events=420 motifs=31 motif_recovery=1.0 coverage=0.765725 overcapture=0.0 history_acc=1.0 compressibility=0.550197

### branch_threshold_high

- `heu_like` status=failed modes=overcapture events=420 motifs=28 motif_recovery=1.0 coverage=6.364557 overcapture=5.364557 history_acc=1.0 compressibility=0.551015
- `sliding_window` status=failed modes=no_events_detected;undercapture;motif_loss;history_prediction_failure;no_event_advantage_over_static events=0 motifs=0 motif_recovery=0.0 coverage=0.0 overcapture=0.0 history_acc=0.0 compressibility=0.0

### branch_threshold_low

- `heu_like` status=faithful modes=within_useful_manifold events=420 motifs=26 motif_recovery=1.0 coverage=1.0 overcapture=0.0 history_acc=1.0 compressibility=0.554386
- `sliding_window` status=failed modes=overcapture events=418 motifs=25 motif_recovery=1.0 coverage=1.554762 overcapture=0.554762 history_acc=1.0 compressibility=0.560449

### branch_window_blur

- `heu_like` status=faithful modes=within_useful_manifold events=420 motifs=26 motif_recovery=1.0 coverage=1.0 overcapture=0.0 history_acc=1.0 compressibility=0.553563
- `sliding_window` status=failed modes=undercapture;motif_loss events=163 motifs=14 motif_recovery=0.0 coverage=0.590476 overcapture=0.0 history_acc=1.0 compressibility=0.487366

### hostile_unique_baseline

- `heu_like` status=expected_collapse modes=noncompressible_as_expected events=600 motifs=0 motif_recovery=0.0 coverage=1.0 overcapture=0.0 history_acc=0.0 compressibility=0.0
- `sliding_window` status=expected_collapse modes=noncompressible_as_expected events=600 motifs=0 motif_recovery=0.0 coverage=1.0 overcapture=0.0 history_acc=0.0 compressibility=0.0

### overlap_baseline

- `heu_like` status=faithful modes=within_useful_manifold events=600 motifs=30 motif_recovery=1.0 coverage=1.0 overcapture=0.0 history_acc=1.0 compressibility=0.571007
- `sliding_window` status=faithful modes=within_useful_manifold events=600 motifs=30 motif_recovery=1.0 coverage=1.0 overcapture=0.0 history_acc=1.0 compressibility=0.571007

### overlap_dropout_005

- `heu_like` status=degraded modes=coverage_degradation;motif_degradation;history_prediction_degradation events=658 motifs=47 motif_recovery=0.783333 coverage=0.946843 overcapture=0.0 history_acc=0.85 compressibility=0.559876
- `sliding_window` status=failed modes=coverage_degradation;motif_loss events=432 motifs=22 motif_recovery=0.3 coverage=0.761233 overcapture=0.0 history_acc=1.0 compressibility=0.534532

### overlap_spurious_005

- `heu_like` status=failed modes=coverage_degradation;motif_loss;history_prediction_failure events=1218 motifs=307 motif_recovery=0.166667 coverage=0.929645 overcapture=0.0 history_acc=0.234637 compressibility=0.266019
- `sliding_window` status=degraded modes=coverage_degradation events=600 motifs=29 motif_recovery=1.0 coverage=0.785014 overcapture=0.0 history_acc=1.0 compressibility=0.570552

### overlap_window_blur

- `heu_like` status=faithful modes=within_useful_manifold events=600 motifs=34 motif_recovery=1.0 coverage=1.0 overcapture=0.0 history_acc=1.0 compressibility=0.567534
- `sliding_window` status=failed modes=undercapture;motif_loss events=244 motifs=22 motif_recovery=0.066667 coverage=0.619444 overcapture=0.0 history_acc=1.0 compressibility=0.480359

## Interpretation

A detector improves the system only if it widens the faithful compression envelope without inventing recurrence in the hostile unique world.

Prediction alone is insufficient. Cases that preserve prediction while overcapturing event cells still degrade the representation.
