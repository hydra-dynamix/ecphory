# Dropout-Spurious Pareto Frontier

This adversary treats missing evidence and false evidence as opposing pressures.

Scores combine status, motif recovery, coverage fidelity, event-history accuracy, and predictive delta. They are diagnostic, not final truth.

## Frontier Variants

- `branch` `sliding_low_consensus_pair` dropout=0.538788 spurious=0.746998 combined=0.746334 statuses=failed/degraded/degraded
- `branch` `hybrid_fast_consensus_pair` dropout=0.73192 spurious=0.563379 combined=0.519018 statuses=degraded/failed/failed
- `branch` `hybrid_high_commit` dropout=0.749169 spurious=0.510288 combined=0.483352 statuses=degraded/failed/failed
- `branch` `hybrid_default` dropout=0.754656 spurious=0.493785 combined=0.481503 statuses=degraded/failed/failed
- `branch` `hybrid_loose_local` dropout=0.753663 spurious=0.494199 combined=0.472901 statuses=degraded/failed/failed
- `branch` `sliding_window_high_threshold` dropout=0.451429 spurious=0.782455 combined=0.425999 statuses=failed/degraded/failed
- `branch` `union_consensus_pair` dropout=0.767977 spurious=0.456474 combined=0.39353 statuses=degraded/failed/failed
- `branch` `union_frequent_subset_pair` dropout=0.774646 spurious=0.467669 combined=0.392231 statuses=degraded/failed/failed
- `branch` `hysteresis_high_threshold` dropout=0.779807 spurious=0.280397 combined=0.263879 statuses=degraded/failed/failed
- `branch` `heu_fast_decay` dropout=0.777581 spurious=0.282316 combined=0.247731 statuses=degraded/failed/failed
- `branch` `hysteresis_low_threshold` dropout=0.776449 spurious=0.29264 combined=0.235799 statuses=degraded/failed/failed
- `overlap` `sliding_low_consensus_pair` dropout=0.528055 spurious=0.772657 combined=0.753256 statuses=failed/degraded/degraded
- `overlap` `hybrid_fast_consensus_pair` dropout=0.736268 spurious=0.555421 combined=0.519138 statuses=degraded/failed/failed
- `overlap` `sliding_window_short` dropout=0.548029 spurious=0.759692 combined=0.501788 statuses=failed/degraded/failed

## Dominated Variants

- `branch` `heu_default` dropout=0.770401 spurious=0.263018 combined=0.246513
- `branch` `heu_high_commit` dropout=0.764609 spurious=0.281853 combined=0.279884
- `branch` `heu_low_commit` dropout=0.757996 spurious=0.16258 combined=0.170729
- `branch` `heu_slow_decay` dropout=0.506238 spurious=0.106461 combined=0.088744
- `branch` `hybrid_fast_decay` dropout=0.730839 spurious=0.487857 combined=0.48846
- `branch` `hybrid_strict_local` dropout=0.407565 spurious=0.514123 combined=0.350983
- `branch` `hysteresis_default` dropout=0.774441 spurious=0.280394 combined=0.239775
- `branch` `hysteresis_loose` dropout=0.756279 spurious=0.257082 combined=0.269033
- `branch` `hysteresis_tight` dropout=0.76639 spurious=0.278687 combined=0.250044
- `branch` `sliding_window_default` dropout=0.44255 spurious=0.781339 combined=0.403176
- `branch` `sliding_window_long` dropout=0.101839 spurious=0.318336 combined=0.295524
- `branch` `sliding_window_low_threshold` dropout=0.523399 spurious=0.694815 combined=0.675936
- `branch` `sliding_window_short` dropout=0.54385 spurious=0.755205 combined=0.487966
- `branch` `union_consensus_fast_decay` dropout=0.732838 spurious=0.451032 combined=0.401167
- `branch` `union_default` dropout=0.751537 spurious=0.250198 combined=0.255515
- `branch` `union_fast_decay` dropout=0.77481 spurious=0.257349 combined=0.256098
- `branch` `union_high_commit` dropout=0.757653 spurious=0.245638 combined=0.277924
- `branch` `union_low_threshold` dropout=0.544615 spurious=0.204006 combined=0.173644
- `branch` `union_top_intensity_pair` dropout=0.765335 spurious=0.435732 combined=0.380018
- `overlap` `heu_default` dropout=0.760413 spurious=0.265426 combined=0.242965
- `overlap` `heu_fast_decay` dropout=0.761677 spurious=0.275143 combined=0.259772
- `overlap` `heu_high_commit` dropout=0.752044 spurious=0.282637 combined=0.259662
- `overlap` `heu_low_commit` dropout=0.759466 spurious=0.16732 combined=0.170577
- `overlap` `heu_slow_decay` dropout=0.510449 spurious=0.120434 combined=0.089416
- `overlap` `hybrid_default` dropout=0.743367 spurious=0.505964 combined=0.4445
- `overlap` `hybrid_fast_decay` dropout=0.731535 spurious=0.482144 combined=0.448826
- `overlap` `hybrid_high_commit` dropout=0.711308 spurious=0.467 combined=0.453264
- `overlap` `hybrid_loose_local` dropout=0.738252 spurious=0.49528 combined=0.447052
- `overlap` `hybrid_strict_local` dropout=0.409476 spurious=0.517962 combined=0.396031
- `overlap` `hysteresis_default` dropout=0.768785 spurious=0.274857 combined=0.24746
- `overlap` `hysteresis_high_threshold` dropout=0.750894 spurious=0.281696 combined=0.274588
- `overlap` `hysteresis_loose` dropout=0.762425 spurious=0.277259 combined=0.244476
- `overlap` `hysteresis_low_threshold` dropout=0.743841 spurious=0.274086 combined=0.258141
- `overlap` `hysteresis_tight` dropout=0.747346 spurious=0.273375 combined=0.240659
- `overlap` `sliding_window_default` dropout=0.449878 spurious=0.77303 combined=0.386187
- `overlap` `sliding_window_high_threshold` dropout=0.431065 spurious=0.776596 combined=0.421406
- `overlap` `sliding_window_long` dropout=0.106597 spurious=0.320622 combined=0.285252
- `overlap` `sliding_window_low_threshold` dropout=0.537402 spurious=0.685499 combined=0.66407
- `overlap` `union_consensus_fast_decay` dropout=0.757124 spurious=0.444381 combined=0.373488
- `overlap` `union_consensus_pair` dropout=0.758095 spurious=0.444311 combined=0.364651
- `overlap` `union_default` dropout=0.740464 spurious=0.248899 combined=0.242434
- `overlap` `union_fast_decay` dropout=0.77465 spurious=0.254166 combined=0.258886
- `overlap` `union_frequent_subset_pair` dropout=0.750671 spurious=0.429231 combined=0.390147
- `overlap` `union_high_commit` dropout=0.746803 spurious=0.265469 combined=0.276027
- `overlap` `union_low_threshold` dropout=0.547345 spurious=0.159939 combined=0.146595
- `overlap` `union_top_intensity_pair` dropout=0.761264 spurious=0.418261 combined=0.337548

## Interpretation

A detector on the frontier is not globally best; it is not dominated across dropout robustness, spurious robustness, and combined robustness under this scoring function.

The expected hard case is a detector that must bridge gaps without remembering false activity.
