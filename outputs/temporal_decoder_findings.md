# Temporal Consistency Decoder Findings

## Question

Can a one-step temporal decoder stabilize event identity better than per-event consensus decoding?

The tested decoder scores candidate pair symbols using:

```text
local intensity
+ recurrence prior
+ previous decoded transition compatibility
+ next candidate transition compatibility
+ next candidate overlap
- overcommon pair penalty
```

It only sees:

- the current candidate event
- the previous decoded event
- the next candidate envelope

It is not a sequence model.

## Three-Seed Combined Corruption Result

Combined corruption means:

```text
dropout_probability = 0.05
spurious_probability = 0.05
```

The best temporal variant was `sliding_low_temporal_consensus_pair`.

| world | variant | statuses | motif mean | motif min | history mean | coverage mean |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| branch | sliding_low_consensus_pair | degraded/degraded/degraded | 0.883333 | 0.850000 | 0.951994 | 1.206072 |
| branch | sliding_low_temporal_consensus_pair | degraded/degraded/degraded | 0.894444 | 0.883333 | 0.951984 | 1.200735 |
| overlap | sliding_low_consensus_pair | degraded/degraded/degraded | 0.883333 | 0.850000 | 0.954385 | 1.206143 |
| overlap | sliding_low_temporal_consensus_pair | degraded/degraded/degraded | 0.888889 | 0.866667 | 0.949103 | 1.203889 |

Temporal decoding improves motif recovery slightly and consistently, but does not reach faithful criteria.

## Suppression Variants

Increasing the overcommon-pair penalty reduced hostile compressibility pressure, but did not improve recurring-world recovery.

| world | variant | motif mean | motif min | history mean | coverage mean |
| --- | --- | ---: | ---: | ---: | ---: |
| branch | sliding_low_temporal_high_penalty | 0.894444 | 0.883333 | 0.951984 | 1.203747 |
| branch | sliding_low_temporal_weak_recurrence | 0.861111 | 0.850000 | 0.943439 | 1.206949 |
| overlap | sliding_low_temporal_high_penalty | 0.883333 | 0.850000 | 0.943638 | 1.208690 |
| overlap | sliding_low_temporal_weak_recurrence | 0.855556 | 0.816667 | 0.932540 | 1.212288 |

The weak-recurrence variant is safer but less useful. The high-penalty variant is not clearly better than baseline temporal consensus.

## Union Result

Union temporal decoding still fails.

| world | variant | motif mean | motif min | history mean | coverage mean |
| --- | --- | ---: | ---: | ---: | ---: |
| branch | union_temporal_consensus_pair | 0.661111 | 0.633333 | 0.634431 | 0.801615 |
| branch | union_temporal_weak_recurrence | 0.577778 | 0.533333 | 0.584533 | 0.818954 |
| overlap | union_temporal_consensus_pair | 0.666667 | 0.633333 | 0.585138 | 0.801390 |
| overlap | union_temporal_weak_recurrence | 0.572222 | 0.533333 | 0.550993 | 0.816373 |

More candidate sources remain harmful. Union is not failing because the decoder lacks recurrence awareness; it is failing because the candidate envelope has too much identity entropy and too little clean coverage after canonicalization.

## Hostile Mixed Controls

All variants still pass the old hostile-collapse classifier, but the stricter motif-count/support check reveals residual lower-level recurrence.

| variant | compressibility max | motif count max | motif support mass max | recurring length-3 max |
| --- | ---: | ---: | ---: | ---: |
| sliding_low_consensus_pair | 0.006155 | 166 | 406 | 0.000000 |
| sliding_low_temporal_consensus_pair | 0.004654 | 148 | 336 | 0.000000 |
| sliding_low_temporal_high_penalty | 0.003689 | 139 | 300 | 0.000000 |
| sliding_low_temporal_weak_recurrence | 0.003017 | 135 | 277 | 0.000000 |
| union_temporal_consensus_pair | 0.009738 | 521 | 1574 | 0.002996 |
| union_temporal_weak_recurrence | 0.006982 | 555 | 1576 | 0.000000 |

The length-3 hostile criterion is insufficient by itself. Motif count and motif support mass expose lower-level identity collapse even when full episode recurrence remains absent.

## Interpretation

The decomposition still holds:

```text
detector = candidate envelope
decoder = identity stabilization
event graph = temporal memory substrate
motif miner = compression over stable event identity
```

But the temporal decoder did not solve the envelope. It found a narrow improvement:

```text
sliding_low_temporal_consensus_pair
```

This is currently the best tested point, but it is still degraded:

- motif recovery remains below 0.95
- active coverage remains above the faithful range
- hostile motif support mass is not near zero

The useful manifold appears to require two simultaneous constraints:

```text
enough permissive detection to avoid undercapture
enough identity discipline to avoid hostile motif support mass
```

One-step temporal context helps, but not enough. The next adversary should test whether duration-aware event validation can reduce overcapture without losing recall.
