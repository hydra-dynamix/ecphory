# Representation Gain Findings

## Metric

```text
Representation Gain =
  canonical length-3 motif support fraction
  - exact canonical motif recovery
```

Positive gain means the motif layer concentrates support around the true reusable sequences more strongly than exact event recovery alone suggests.

## Result

Representation Gain is consistently positive for the useful imperfect-event regimes.

| world | variant | exact recovery mean | motif support fraction mean | gain mean | gain min |
| --- | --- | ---: | ---: | ---: | ---: |
| branch | sliding_window_low_threshold | 0.753333 | 0.912253 | 0.158920 | 0.068182 |
| branch | sliding_low_consensus_pair | 0.880000 | 0.968523 | 0.088523 | 0.046552 |
| branch | sliding_low_temporal_consensus_pair | 0.886667 | 0.989221 | 0.102555 | 0.080631 |
| overlap | sliding_window_low_threshold | 0.750000 | 0.900398 | 0.150398 | 0.077643 |
| overlap | sliding_low_consensus_pair | 0.873333 | 0.969078 | 0.095745 | 0.037571 |
| overlap | sliding_low_temporal_consensus_pair | 0.886667 | 0.978915 | 0.092248 | 0.060344 |

This supports the claim that the hierarchy is more reliable than the individual event observations in these regimes.

## Negative Controls

Union variants show negative gain.

| world | variant | exact recovery mean | motif support fraction mean | gain mean | gain min |
| --- | --- | ---: | ---: | ---: | ---: |
| branch | union_temporal_consensus_pair | 0.643333 | 0.556135 | -0.087198 | -0.133664 |
| overlap | union_temporal_consensus_pair | 0.653333 | 0.567290 | -0.086044 | -0.111111 |

This is useful: the metric does not automatically flatter the hierarchy. It distinguishes useful recurrence from unstable candidate envelopes.

## Interpretation

The detector does not need perfect event recovery for the hierarchy to preserve useful temporal structure.

In the useful regimes:

```text
imperfect events
  -> noisy transitions
  -> repeated episodes
  -> motif support concentrates around true reusable sequences
```

That is evidence for recurrence acting as an error-correcting mechanism at the representation level.

The boundary remains:

```text
too little recall      -> undercapture
too much candidate entropy -> negative Representation Gain
stable recurrence      -> positive Representation Gain
```
