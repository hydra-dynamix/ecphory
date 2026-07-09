# Discrete Event Decoder Findings

## Question

Can a post-detector discrete event decoder recover the event symbols needed by the event-first memory pipeline?

The decoder sits between detection and event-transition construction:

```text
raw signals
  -> detector
  -> noisy event candidates
  -> discrete event decoder
  -> transitions
  -> episodes
  -> motifs
```

This keeps detectors and event identity separate. Detectors decide when something happened. Decoders decide which discrete event symbol the candidate should commit to.

## Implemented Decoders

- `none`: preserve detected participant set.
- `top_intensity_pair`: map larger participant sets to the two highest-intensity units.
- `frequent_subset_pair`: map larger participant sets to their most recurrent pair subset.
- `consensus_pair`: map larger participant sets using recurrence plus event-local intensity.

All current decoders are pair decoders. That matches the current synthetic worlds, whose canonical events are pair coactivations.

## Combined Dropout + Spurious Results

The strongest result was not union. It was low-threshold sliding-window detection plus consensus pair decoding.

| world | variant | status | motif recovery | coverage | overcapture | history accuracy | score |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| branch | sliding_window_low_threshold | degraded | 0.733333 | 1.265645 | 0.265645 | 0.853659 | 0.675936 |
| branch | sliding_low_consensus_pair | degraded | 0.883333 | 1.198716 | 0.198716 | 0.951220 | 0.746334 |
| overlap | sliding_window_low_threshold | degraded | 0.733333 | 1.258201 | 0.258201 | 0.786885 | 0.664070 |
| overlap | sliding_low_consensus_pair | degraded | 0.900000 | 1.199821 | 0.199821 | 0.966102 | 0.753256 |

Consensus decoding improved motif recovery, reduced overcapture, and restored high event-history prediction in both branch and overlap worlds.

## Union Result

Union plus decoding improved over undecoded union, but still failed combined corruption.

| world | variant | decoder | status | motif recovery | coverage | history accuracy | score |
| --- | --- | --- | --- | ---: | ---: | ---: | ---: |
| branch | union_default | none | failed | 0.066667 | 1.030480 | 0.224719 | 0.255515 |
| branch | union_consensus_pair | consensus_pair | failed | 0.533333 | 0.812318 | 0.516667 | 0.393530 |
| branch | union_frequent_subset_pair | frequent_subset_pair | failed | 0.516667 | 0.818827 | 0.527027 | 0.392231 |
| overlap | union_default | none | failed | 0.066667 | 1.059973 | 0.188811 | 0.242434 |
| overlap | union_frequent_subset_pair | frequent_subset_pair | failed | 0.500000 | 0.811509 | 0.546392 | 0.390147 |
| overlap | union_consensus_pair | consensus_pair | failed | 0.433333 | 0.801880 | 0.525862 | 0.364651 |

Interpretation: union captures too many plausible candidates. Pair decoding can repair some event identity, but it also drops below the coverage envelope. The union detector is still not the best front end for this decoder.

## Hybrid Result

Hybrid plus consensus decoding improved motif recovery and history accuracy, but remains undercapturing.

| world | variant | status | motif recovery | coverage | history accuracy | score |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| branch | hybrid_fast_decay | failed | 0.800000 | 0.564251 | 0.878049 | 0.488460 |
| branch | hybrid_fast_consensus_pair | failed | 0.900000 | 0.568860 | 0.906977 | 0.519018 |
| overlap | hybrid_fast_decay | failed | 0.766667 | 0.580667 | 0.705128 | 0.448826 |
| overlap | hybrid_fast_consensus_pair | failed | 0.866667 | 0.564615 | 0.967742 | 0.519138 |

This says the decoder can stabilize event identity, but it cannot restore signal mass that the detector never admitted.

## Hostile Mixed Control

Mixed dropout+spurious hostile-unique controls still collapsed under decoded variants:

| variant | event labels | recurring length-3 fraction | repeated episode fraction | compressibility |
| --- | ---: | ---: | ---: | ---: |
| sliding_low_consensus_pair | 569 | 0.000000 | 0.000000 | 0.005887 |
| union_consensus_pair | 642 | 0.000000 | 0.000000 | 0.023101 |
| hybrid_fast_consensus_pair | 590 | 0.000000 | 0.000000 | 0.008218 |

The decoder did not manufacture episode-level recurrence in the hostile unique world.

## Current Boundary

The useful architecture is now more specific:

```text
detector = candidate generator
decoder = event identity stabilizer
event graph = temporal memory substrate
motifs = compression over stable event identities
```

The failure boundary is no longer just detector recall. It is the joint envelope:

```text
candidate recall
  must be high enough
event identity entropy
  must be low enough
hostile compressibility
  must remain near zero
```

The current best tested point is:

```text
sliding_window_low_threshold + consensus_pair decoder
```

It is still degraded, not faithful, because overcapture remains above the faithful range and motif recovery is below 0.95. But it expands the useful manifold without violating hostile controls.

## Next Test

The next decoder should not only choose pair identity per event. It should decode using local temporal consistency:

```text
candidate event
  + previous decoded event
  + next candidate event
  -> chosen discrete event symbol
```

Acceptance criteria:

- branch and overlap combined motif recovery >= 0.95
- event-history accuracy >= 0.95
- active-cell coverage between 0.95 and 1.10
- hostile unique recurring length-3 fraction <= 0.05
