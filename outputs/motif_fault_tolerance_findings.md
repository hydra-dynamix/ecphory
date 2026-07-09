# Motif Layer Fault Tolerance

This experiment stops repairing the detector and asks whether the motif layer can stabilize reusable temporal structure from imperfect events.

All recurring-world cases use combined dropout+spurious corruption. Hostile unique controls use the same corruption.

## Recurring Worlds

### branch

- `sliding_window_low_threshold` statuses={'degraded': 5} exact_recovery_mean=0.753333 exact_recovery_min=0.716667 canonical_support_fraction_mean=0.912253 representation_gain_mean=0.158920 representation_gain_min=0.068182 worst_rank_max=2 top5_jaccard_mean=0.264286
- `sliding_low_consensus_pair` statuses={'degraded': 5} exact_recovery_mean=0.880000 exact_recovery_min=0.850000 canonical_support_fraction_mean=0.968523 representation_gain_mean=0.088523 representation_gain_min=0.046552 worst_rank_max=2 top5_jaccard_mean=0.515238
- `sliding_low_temporal_consensus_pair` statuses={'degraded': 5} exact_recovery_mean=0.886667 exact_recovery_min=0.866667 canonical_support_fraction_mean=0.989221 representation_gain_mean=0.102555 representation_gain_min=0.080631 worst_rank_max=2 top5_jaccard_mean=0.690000
- `hybrid_fast_temporal_consensus_pair` statuses={'failed': 5} exact_recovery_mean=0.886667 exact_recovery_min=0.866667 canonical_support_fraction_mean=0.929054 representation_gain_mean=0.042387 representation_gain_min=0.008333 worst_rank_max=2 top5_jaccard_mean=1.000000
- `union_temporal_consensus_pair` statuses={'failed': 5} exact_recovery_mean=0.643333 exact_recovery_min=0.566667 canonical_support_fraction_mean=0.556135 representation_gain_mean=-0.087198 representation_gain_min=-0.133664 worst_rank_max=2 top5_jaccard_mean=0.521429

### overlap

- `sliding_window_low_threshold` statuses={'degraded': 5} exact_recovery_mean=0.750000 exact_recovery_min=0.733333 canonical_support_fraction_mean=0.900398 representation_gain_mean=0.150398 representation_gain_min=0.077643 worst_rank_max=3 top5_jaccard_mean=0.428571
- `sliding_low_consensus_pair` statuses={'degraded': 5} exact_recovery_mean=0.873333 exact_recovery_min=0.833333 canonical_support_fraction_mean=0.969078 representation_gain_mean=0.095745 representation_gain_min=0.037571 worst_rank_max=3 top5_jaccard_mean=0.656667
- `sliding_low_temporal_consensus_pair` statuses={'degraded': 5} exact_recovery_mean=0.886667 exact_recovery_min=0.866667 canonical_support_fraction_mean=0.978915 representation_gain_mean=0.092248 representation_gain_min=0.060344 worst_rank_max=3 top5_jaccard_mean=0.563571
- `hybrid_fast_temporal_consensus_pair` statuses={'failed': 5} exact_recovery_mean=0.890000 exact_recovery_min=0.866667 canonical_support_fraction_mean=0.899658 representation_gain_mean=0.009658 representation_gain_min=-0.009890 worst_rank_max=3 top5_jaccard_mean=0.766667
- `union_temporal_consensus_pair` statuses={'failed': 5} exact_recovery_mean=0.653333 exact_recovery_min=0.600000 canonical_support_fraction_mean=0.567290 representation_gain_mean=-0.086044 representation_gain_min=-0.111111 worst_rank_max=3 top5_jaccard_mean=0.571429

## Hostile Unique Controls

- `sliding_window_low_threshold` compressibility_max=0.001832 motif_count_max=96 length3_support_mass_max=0.000000 recurring_len3_max=0.000000
- `sliding_low_consensus_pair` compressibility_max=0.006886 motif_count_max=166 length3_support_mass_max=0.000000 recurring_len3_max=0.000000
- `sliding_low_temporal_consensus_pair` compressibility_max=0.004864 motif_count_max=148 length3_support_mass_max=0.000000 recurring_len3_max=0.000000
- `hybrid_fast_temporal_consensus_pair` compressibility_max=0.006000 motif_count_max=141 length3_support_mass_max=0.000000 recurring_len3_max=0.000000
- `union_temporal_consensus_pair` compressibility_max=0.009738 motif_count_max=532 length3_support_mass_max=4.000000 recurring_len3_max=0.003147

## Interpretation

If the event-first hierarchy is fault tolerant, exact event recovery can be degraded while canonical motifs remain high-rank, high-support, and stable across seeds.

`representation_gain = canonical_support_fraction - exact_recovery`. Positive gain means recurrence across episodes recovered more stable motif structure than exact event recovery alone exposed.

If hostile unique worlds accumulate motif count or support mass, recurrence is being induced by event identity collapse rather than discovered in the world.
