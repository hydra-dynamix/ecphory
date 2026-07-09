# Useful Compression Manifold

This artifact summarizes the expanded non-scaling stress sweep for the event-first memory prototype.

Worlds tested:

- `branch`: two motifs share prefix `{A,B}` and diverge.
- `overlap`: three motifs share prefix `{A,B}` and suffix `{E,F}` with different middle events.

Both worlds produced the same status distribution across the expanded sweep:

- faithful: 34
- degraded: 7
- failed: 20

## Useful Region

The current useful manifold is defined by:

- activation threshold near the active signal band: `0.75` to `0.90`
- window size less than or equal to true event duration: `1` to `3` when event duration is `3`
- event duration at least as long as the detector window
- active signal mean at or above roughly `0.85` when threshold is `0.75`
- active standard deviation up to about `0.10` faithful, around `0.20` degraded
- baseline mean up to about `0.15` faithful, around `0.30` degraded, `0.45+` failed
- baseline standard deviation up to about `0.20` faithful, `0.35` degraded
- inactive spurious probability up to `0.05` degraded but still predictive, `0.10+` failed
- active dropout must be near zero; even `0.05` caused motif loss in this detector
- participant cardinality threshold must not exceed the true event cardinality

## Failure Categories

Observed failure modes:

- `overcapture`: threshold too permissive or baseline too high; motif prediction may remain good while compression is no longer faithful.
- `undercapture`: threshold/window/cardinality settings miss active event structure.
- `motif_loss`: canonical event sequences are not recovered even if some prediction cases remain easy.
- `history_prediction_failure`: event history no longer predicts future events.
- `no_event_advantage_over_static`: the event representation loses its measurable predictive advantage.
- `coverage_degradation`: event coverage remains usable but slips outside the faithful band.
- `overcapture_degradation`: event coverage expands beyond faithful compression while staying below outright failure.

## Current Disproof Pressure

The strongest falsifying axes so far are:

- active dropout
- window size greater than event duration
- activation threshold too low or too high
- active signal too close to threshold
- baseline elevation
- spurious inactive activity
- participant cardinality threshold above true event size

The overlap topology did not break the representation under clean detection. Shared prefix and shared suffix motifs remained recoverable because the middle event stayed detectable.

## Interpretation

The theory is not disproven yet, but the useful manifold is not broad in every direction. It is highly sensitive to detector fidelity. The event-first representation works when compression creates clean event objects; it fails when compression either erases event cells or absorbs too much non-event activity.

Static projection remains deliberately lossy in all cases. The central question is now whether a better event detector can widen the useful manifold without increasing overcapture.
