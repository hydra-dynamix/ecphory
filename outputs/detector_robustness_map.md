# Detector Robustness Map

This maps detector family x hyperparameter variant x environment using the same downstream event-first representation.

The central metric is faithful operating envelope size, with hostile unique worlds expected to collapse rather than compress.

## Detector Family Status Counts

- `heu_like`: faithful=15 degraded=13 failed=22 expected_collapse=5 suspicious=0
- `hybrid_state_window`: faithful=1 degraded=27 failed=32 expected_collapse=6 suspicious=0
- `hysteresis`: faithful=27 degraded=10 failed=13 expected_collapse=5 suspicious=0
- `sliding_window`: faithful=11 degraded=11 failed=38 expected_collapse=6 suspicious=0
- `union_state_window`: faithful=15 degraded=27 failed=38 expected_collapse=8 suspicious=0

## Environment Status Counts

- `branch_clean`: faithful=18 degraded=6 failed=6 expected_collapse=0 suspicious=0
- `branch_dropout`: faithful=1 degraded=21 failed=8 expected_collapse=0 suspicious=0
- `branch_high_threshold`: faithful=3 degraded=0 failed=27 expected_collapse=0 suspicious=0
- `branch_low_threshold`: faithful=11 degraded=6 failed=13 expected_collapse=0 suspicious=0
- `branch_spurious`: faithful=0 degraded=5 failed=25 expected_collapse=0 suspicious=0
- `branch_window_blur`: faithful=9 degraded=9 failed=12 expected_collapse=0 suspicious=0
- `hostile_unique`: faithful=0 degraded=0 failed=0 expected_collapse=30 suspicious=0
- `overlap_clean`: faithful=18 degraded=6 failed=6 expected_collapse=0 suspicious=0
- `overlap_dropout`: faithful=0 degraded=21 failed=9 expected_collapse=0 suspicious=0
- `overlap_spurious`: faithful=0 degraded=5 failed=25 expected_collapse=0 suspicious=0
- `overlap_window_blur`: faithful=9 degraded=9 failed=12 expected_collapse=0 suspicious=0

## Variant Status Counts

- `heu_default`: faithful=5 degraded=2 failed=3 expected_collapse=1 suspicious=0
- `heu_fast_decay`: faithful=5 degraded=2 failed=3 expected_collapse=1 suspicious=0
- `heu_high_commit`: faithful=5 degraded=2 failed=3 expected_collapse=1 suspicious=0
- `heu_low_commit`: faithful=0 degraded=7 failed=3 expected_collapse=1 suspicious=0
- `heu_slow_decay`: faithful=0 degraded=0 failed=10 expected_collapse=1 suspicious=0
- `hybrid_default`: faithful=0 degraded=5 failed=5 expected_collapse=1 suspicious=0
- `hybrid_fast_consensus_pair`: faithful=0 degraded=5 failed=5 expected_collapse=1 suspicious=0
- `hybrid_fast_decay`: faithful=0 degraded=5 failed=5 expected_collapse=1 suspicious=0
- `hybrid_high_commit`: faithful=0 degraded=5 failed=5 expected_collapse=1 suspicious=0
- `hybrid_loose_local`: faithful=1 degraded=6 failed=3 expected_collapse=1 suspicious=0
- `hybrid_strict_local`: faithful=0 degraded=1 failed=9 expected_collapse=1 suspicious=0
- `hysteresis_default`: faithful=5 degraded=2 failed=3 expected_collapse=1 suspicious=0
- `hysteresis_high_threshold`: faithful=6 degraded=2 failed=2 expected_collapse=1 suspicious=0
- `hysteresis_loose`: faithful=5 degraded=2 failed=3 expected_collapse=1 suspicious=0
- `hysteresis_low_threshold`: faithful=6 degraded=2 failed=2 expected_collapse=1 suspicious=0
- `hysteresis_tight`: faithful=5 degraded=2 failed=3 expected_collapse=1 suspicious=0
- `sliding_low_consensus_pair`: faithful=0 degraded=2 failed=8 expected_collapse=1 suspicious=0
- `sliding_window_default`: faithful=2 degraded=2 failed=6 expected_collapse=1 suspicious=0
- `sliding_window_high_threshold`: faithful=4 degraded=2 failed=4 expected_collapse=1 suspicious=0
- `sliding_window_long`: faithful=0 degraded=0 failed=10 expected_collapse=1 suspicious=0
- `sliding_window_low_threshold`: faithful=0 degraded=2 failed=8 expected_collapse=1 suspicious=0
- `sliding_window_short`: faithful=5 degraded=3 failed=2 expected_collapse=1 suspicious=0
- `union_consensus_fast_decay`: faithful=2 degraded=4 failed=4 expected_collapse=1 suspicious=0
- `union_consensus_pair`: faithful=2 degraded=4 failed=4 expected_collapse=1 suspicious=0
- `union_default`: faithful=3 degraded=3 failed=4 expected_collapse=1 suspicious=0
- `union_fast_decay`: faithful=2 degraded=4 failed=4 expected_collapse=1 suspicious=0
- `union_frequent_subset_pair`: faithful=2 degraded=4 failed=4 expected_collapse=1 suspicious=0
- `union_high_commit`: faithful=2 degraded=4 failed=4 expected_collapse=1 suspicious=0
- `union_low_threshold`: faithful=0 degraded=0 failed=10 expected_collapse=1 suspicious=0
- `union_top_intensity_pair`: faithful=2 degraded=4 failed=4 expected_collapse=1 suspicious=0

## Hostile Controls

All hostile unique detector variants collapsed as expected.

## Interpretation

Detector families define different event vocabularies and operating regions. A useful family is not the one with the highest prediction alone, but the one that expands faithful compression while preserving hostile collapse.

If different families succeed on the same environments, evidence shifts toward the downstream event-first representation. If only one family succeeds, capability is localized to detector dynamics.
