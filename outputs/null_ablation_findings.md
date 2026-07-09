# Null And Ablation Findings

## Question

Does Representation Gain disappear when temporal recurrence or event identity is selectively broken?

## Result

The large positive gain appears only in observed recurring streams.

### Observed Useful Streams

| world | variant | exact mean | motif support fraction mean | gain mean |
| --- | --- | ---: | ---: | ---: |
| branch | sliding_low_temporal_consensus_pair | 0.894444 | 0.982036 | 0.087591 |
| overlap | sliding_low_temporal_consensus_pair | 0.888889 | 0.988321 | 0.099432 |
| branch | sliding_window_low_threshold | 0.755556 | 0.894300 | 0.138744 |
| overlap | sliding_window_low_threshold | 0.750000 | 0.930974 | 0.180974 |

### Selective Nulls

| world | variant | null | exact mean | motif support fraction mean | gain mean |
| --- | --- | --- | ---: | ---: | ---: |
| branch | sliding_low_temporal_consensus_pair | within episode permuted | 0.144444 | 0.175090 | 0.030645 |
| branch | sliding_low_temporal_consensus_pair | episode boundaries permuted | 0.000000 | 0.028790 | 0.028790 |
| branch | sliding_low_temporal_consensus_pair | global labels permuted | 0.000000 | 0.000000 | 0.000000 |
| overlap | sliding_low_temporal_consensus_pair | within episode permuted | 0.116667 | 0.175744 | 0.059077 |
| overlap | sliding_low_temporal_consensus_pair | episode boundaries permuted | 0.011111 | 0.030965 | 0.019854 |
| overlap | sliding_low_temporal_consensus_pair | global labels permuted | 0.000000 | 0.000000 | 0.000000 |

The nulls do not merely reduce exact recovery. They reduce motif support concentration itself.

Within-episode permutation leaves a small residual positive gain. That is expected: it destroys ordered motifs but preserves per-episode event composition and event frequencies. It is a weaker null, not a full hostile control.

## Negative Control

Union remains negative in observed streams:

| world | variant | exact mean | motif support fraction mean | gain mean |
| --- | --- | ---: | ---: | ---: |
| branch | union_temporal_consensus_pair | 0.661111 | 0.542557 | -0.118554 |
| overlap | union_temporal_consensus_pair | 0.666667 | 0.589167 | -0.077500 |

This keeps Representation Gain discriminative: it rewards stable imperfect recurrence, not all hierarchy outputs.

## Layer Ablation

The motif layer concentrates canonical support beyond events and transitions in useful streams.

| world | variant | event fraction | transition fraction | motif fraction | motif over event | motif over transition |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| branch | sliding_low_temporal_consensus_pair | 0.858485 | 0.797979 | 0.982036 | 0.123550 | 0.184057 |
| overlap | sliding_low_temporal_consensus_pair | 0.904144 | 0.847495 | 0.988321 | 0.084177 | 0.140826 |
| branch | sliding_window_low_threshold | 0.791354 | 0.674778 | 0.894300 | 0.102945 | 0.219522 |
| overlap | sliding_window_low_threshold | 0.839832 | 0.714397 | 0.930974 | 0.091143 | 0.216577 |

This is evidence that the gain is not already fully present at the event or transition layer. Motif recurrence concentrates support further.

## Interpretation

The null package strengthens the claim:

```text
observed temporal recurrence
  -> large positive Representation Gain

temporal order disrupted
  -> gain sharply reduced

episode boundaries disrupted
  -> gain nearly eliminated

event identity randomized
  -> gain eliminated

over-entropic union envelope
  -> negative gain
```

This makes the result harder to dismiss as a metric artifact or detector artifact. The hierarchy is doing useful consolidation specifically when stable temporal recurrence exists.
