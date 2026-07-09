# Temporal Decoder Seed Sweep

This tests one-step temporal decoding under combined dropout+spurious corruption across three seeds.

The temporal decoder can use the previous decoded event and the next candidate envelope, but it is not a general sequence model.

## Combined Recurring Worlds

### branch

- `sliding_low_consensus_pair` statuses={'degraded': 3} motif_mean=0.883333 motif_min=0.850000 history_mean=0.951994 coverage_mean=1.206072
- `sliding_low_temporal_consensus_pair` statuses={'degraded': 3} motif_mean=0.894444 motif_min=0.883333 history_mean=0.951984 coverage_mean=1.200735
- `sliding_low_temporal_high_penalty` statuses={'degraded': 3} motif_mean=0.894444 motif_min=0.883333 history_mean=0.951984 coverage_mean=1.203747
- `sliding_low_temporal_weak_recurrence` statuses={'degraded': 3} motif_mean=0.861111 motif_min=0.850000 history_mean=0.943439 coverage_mean=1.206949
- `hybrid_fast_temporal_consensus_pair` statuses={'failed': 3} motif_mean=0.900000 motif_min=0.883333 history_mean=0.922613 coverage_mean=0.558093
- `union_temporal_consensus_pair` statuses={'failed': 3} motif_mean=0.661111 motif_min=0.633333 history_mean=0.634431 coverage_mean=0.801615
- `union_temporal_high_penalty` statuses={'failed': 3} motif_mean=0.611111 motif_min=0.550000 history_mean=0.611613 coverage_mean=0.803533
- `union_temporal_weak_recurrence` statuses={'failed': 3} motif_mean=0.577778 motif_min=0.533333 history_mean=0.584533 coverage_mean=0.818954
- `union_temporal_consensus_fast_decay` statuses={'failed': 3} motif_mean=0.661111 motif_min=0.633333 history_mean=0.634431 coverage_mean=0.801615

### overlap

- `sliding_low_consensus_pair` statuses={'degraded': 3} motif_mean=0.883333 motif_min=0.850000 history_mean=0.954385 coverage_mean=1.206143
- `sliding_low_temporal_consensus_pair` statuses={'degraded': 3} motif_mean=0.888889 motif_min=0.866667 history_mean=0.949103 coverage_mean=1.203889
- `sliding_low_temporal_high_penalty` statuses={'degraded': 3} motif_mean=0.883333 motif_min=0.850000 history_mean=0.943638 coverage_mean=1.208690
- `sliding_low_temporal_weak_recurrence` statuses={'degraded': 3} motif_mean=0.855556 motif_min=0.816667 history_mean=0.932540 coverage_mean=1.212288
- `hybrid_fast_temporal_consensus_pair` statuses={'failed': 3} motif_mean=0.894444 motif_min=0.883333 history_mean=0.883402 coverage_mean=0.560352
- `union_temporal_consensus_pair` statuses={'failed': 3} motif_mean=0.666667 motif_min=0.633333 history_mean=0.585138 coverage_mean=0.801390
- `union_temporal_high_penalty` statuses={'failed': 3} motif_mean=0.622222 motif_min=0.533333 history_mean=0.574860 coverage_mean=0.802433
- `union_temporal_weak_recurrence` statuses={'failed': 3} motif_mean=0.572222 motif_min=0.533333 history_mean=0.550993 coverage_mean=0.816373
- `union_temporal_consensus_fast_decay` statuses={'failed': 3} motif_mean=0.661111 motif_min=0.616667 history_mean=0.583536 coverage_mean=0.801390

## Hostile Mixed Controls

- `sliding_low_consensus_pair` statuses={'expected_collapse': 3} compressibility_max=0.006155 motif_count_max=166 motif_support_mass_max=406.000000 recurring_len3_max=0.000000
- `sliding_low_temporal_consensus_pair` statuses={'expected_collapse': 3} compressibility_max=0.004654 motif_count_max=148 motif_support_mass_max=336.000000 recurring_len3_max=0.000000
- `sliding_low_temporal_high_penalty` statuses={'expected_collapse': 3} compressibility_max=0.003689 motif_count_max=139 motif_support_mass_max=300.000000 recurring_len3_max=0.000000
- `sliding_low_temporal_weak_recurrence` statuses={'expected_collapse': 3} compressibility_max=0.003017 motif_count_max=135 motif_support_mass_max=277.000000 recurring_len3_max=0.000000
- `hybrid_fast_temporal_consensus_pair` statuses={'expected_collapse': 3} compressibility_max=0.006000 motif_count_max=141 motif_support_mass_max=334.000000 recurring_len3_max=0.000000
- `union_temporal_consensus_pair` statuses={'expected_collapse': 3} compressibility_max=0.009738 motif_count_max=521 motif_support_mass_max=1574.000000 recurring_len3_max=0.002996
- `union_temporal_high_penalty` statuses={'expected_collapse': 3} compressibility_max=0.007720 motif_count_max=545 motif_support_mass_max=1581.000000 recurring_len3_max=0.001541
- `union_temporal_weak_recurrence` statuses={'expected_collapse': 3} compressibility_max=0.006982 motif_count_max=555 motif_support_mass_max=1576.000000 recurring_len3_max=0.000000
- `union_temporal_consensus_fast_decay` statuses={'expected_collapse': 3} compressibility_max=0.009762 motif_count_max=523 motif_support_mass_max=1580.000000 recurring_len3_max=0.002990

## Interpretation

A temporal decoder is useful only if it improves recurring-world motif recovery across seeds without turning hostile unique episodes into reusable motifs.

Passing hostile collapse requires more than low length-3 recurrence: motif count and motif support mass are tracked here because lower-level identity collapse can appear before full episode recurrence.
