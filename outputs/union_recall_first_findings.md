# Union Recall-First Detector Findings

## Question

Does combining stateful detection with sliding-window detection by union pick up the wanted events before pruning?

## Detector Change

`union_state_window` admits an event if either detector finds it:

- sliding-window detector
- HEU-like stateful detector

Events are merged only when they have the same episode, the same participant set, and overlapping or adjacent time spans. Everything else is preserved.

This is intentionally recall-first. It tests detection coverage before any pruning or validation layer removes unwanted events.

## Combined Dropout + Spurious Result

The union detector does not undercapture by active-cell coverage:

| world | variant | status | coverage | overcapture | motif recovery | history accuracy |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| branch | union_default | failed | 1.030480 | 0.030480 | 0.066667 | 0.224719 |
| branch | union_fast_decay | failed | 1.047742 | 0.047742 | 0.066667 | 0.244898 |
| branch | union_high_commit | failed | 1.049460 | 0.049460 | 0.116667 | 0.295918 |
| overlap | union_default | failed | 1.059973 | 0.059973 | 0.066667 | 0.188811 |
| overlap | union_fast_decay | failed | 1.042193 | 0.042193 | 0.116667 | 0.190789 |
| overlap | union_high_commit | failed | 1.058850 | 0.058850 | 0.100000 | 0.315789 |

By contrast, the best sliding-window low-threshold combined cases were degraded rather than failed:

| world | variant | status | coverage | overcapture | motif recovery | history accuracy |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| branch | sliding_window_low_threshold | degraded | 1.265645 | 0.265645 | 0.733333 | 0.853659 |
| overlap | sliding_window_low_threshold | degraded | 1.258201 | 0.258201 | 0.733333 | 0.786885 |

## Interpretation

The union detector answers the immediate recall question partially:

```text
Are active cells being missed? mostly no.
Are canonical event sequences preserved? no.
```

The failure moved from undercapture to fragmentation and contamination. Union admits enough signal mass, but it creates extra participant-set variants and temporal subdivisions that break the canonical motif identity used by the downstream motif miner.

That means the next problem is not simply "remove extra events." The pruning layer must preserve equivalence between noisy event variants and the intended canonical event, or motif recovery will remain low.

## Hostile Unique Control

The hostile unique world still collapses as expected under union:

| detector | detected events | event labels | recurring length-3 fraction | compressibility |
| --- | ---: | ---: | ---: | ---: |
| union_state_window | 2733 | 2413 | 0.000000 | 0.002268 |
| sliding_window_low_threshold | 899 | 819 | 0.000000 | 0.001600 |

Union overcaptures heavily in hostile conditions, but it does not manufacture reusable episode-level structure in this control.

## Boundary Found

Recall-first union expands event-cell coverage but contracts motif recoverability.

The compression boundary is therefore not only detector recall. It is the stability of event identity under noise:

```text
raw signal coverage
    can be sufficient
while
canonical event identity
    is still destroyed
```

The next adversarial mechanism should test pruning or canonicalization after recall-first union, with motif recovery and hostile-collapse preservation as the acceptance criteria.
