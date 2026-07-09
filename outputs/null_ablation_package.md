# Null And Ablation Package

This tests whether Representation Gain disappears when temporal recurrence or event identity is selectively broken after detection.

Nulls transform the detected event stream before transitions, episodes, and motifs are rebuilt.

## Stronger Nulls

### branch

#### sliding_low_temporal_consensus_pair

- `observed` exact_mean=0.894444 support_fraction_mean=0.982036 gain_mean=0.087591 gain_min=0.080631
- `within_episode_permuted` exact_mean=0.144444 support_fraction_mean=0.175090 gain_mean=0.030645 gain_min=0.016667
- `episode_boundaries_permuted` exact_mean=0.000000 support_fraction_mean=0.028790 gain_mean=0.028790 gain_min=0.000000
- `global_label_permuted` exact_mean=0.000000 support_fraction_mean=0.000000 gain_mean=0.000000 gain_min=0.000000

#### sliding_window_low_threshold

- `observed` exact_mean=0.755556 support_fraction_mean=0.894300 gain_mean=0.138744 gain_min=0.068182
- `within_episode_permuted` exact_mean=0.111111 support_fraction_mean=0.164291 gain_mean=0.053180 gain_min=0.036478
- `episode_boundaries_permuted` exact_mean=0.000000 support_fraction_mean=0.024828 gain_mean=0.024828 gain_min=0.000000
- `global_label_permuted` exact_mean=0.000000 support_fraction_mean=0.000000 gain_mean=0.000000 gain_min=0.000000

#### union_temporal_consensus_pair

- `observed` exact_mean=0.661111 support_fraction_mean=0.542557 gain_mean=-0.118554 gain_min=-0.133664
- `within_episode_permuted` exact_mean=0.122222 support_fraction_mean=0.124959 gain_mean=0.002736 gain_min=-0.016291
- `episode_boundaries_permuted` exact_mean=0.011111 support_fraction_mean=0.025247 gain_mean=0.014136 gain_min=0.000000
- `global_label_permuted` exact_mean=0.000000 support_fraction_mean=0.000000 gain_mean=0.000000 gain_min=0.000000

### overlap

#### sliding_low_temporal_consensus_pair

- `observed` exact_mean=0.888889 support_fraction_mean=0.988321 gain_mean=0.099432 gain_min=0.060344
- `within_episode_permuted` exact_mean=0.116667 support_fraction_mean=0.175744 gain_mean=0.059077 gain_min=0.038235
- `episode_boundaries_permuted` exact_mean=0.011111 support_fraction_mean=0.030965 gain_mean=0.019854 gain_min=0.012469
- `global_label_permuted` exact_mean=0.000000 support_fraction_mean=0.000000 gain_mean=0.000000 gain_min=0.000000

#### sliding_window_low_threshold

- `observed` exact_mean=0.750000 support_fraction_mean=0.930974 gain_mean=0.180974 gain_min=0.160828
- `within_episode_permuted` exact_mean=0.116667 support_fraction_mean=0.184803 gain_mean=0.068137 gain_min=0.046078
- `episode_boundaries_permuted` exact_mean=0.011111 support_fraction_mean=0.025670 gain_mean=0.014560 gain_min=0.000000
- `global_label_permuted` exact_mean=0.000000 support_fraction_mean=0.000000 gain_mean=0.000000 gain_min=0.000000

#### union_temporal_consensus_pair

- `observed` exact_mean=0.666667 support_fraction_mean=0.589167 gain_mean=-0.077500 gain_min=-0.085599
- `within_episode_permuted` exact_mean=0.105556 support_fraction_mean=0.121667 gain_mean=0.016112 gain_min=0.007143
- `episode_boundaries_permuted` exact_mean=0.022222 support_fraction_mean=0.047035 gain_mean=0.024813 gain_min=0.017514
- `global_label_permuted` exact_mean=0.000000 support_fraction_mean=0.000000 gain_mean=0.000000 gain_min=0.000000

## Layer Ablations

### branch observed streams

- `sliding_low_temporal_consensus_pair` event_fraction=0.858485 transition_fraction=0.797979 motif_fraction=0.982036 motif_over_event=0.123550 motif_over_transition=0.184057
- `sliding_window_low_threshold` event_fraction=0.791354 transition_fraction=0.674778 motif_fraction=0.894300 motif_over_event=0.102945 motif_over_transition=0.219522
- `union_temporal_consensus_pair` event_fraction=0.776684 transition_fraction=0.498056 motif_fraction=0.542557 motif_over_event=-0.234128 motif_over_transition=0.044500

### overlap observed streams

- `sliding_low_temporal_consensus_pair` event_fraction=0.904144 transition_fraction=0.847495 motif_fraction=0.988321 motif_over_event=0.084177 motif_over_transition=0.140826
- `sliding_window_low_threshold` event_fraction=0.839832 transition_fraction=0.714397 motif_fraction=0.930974 motif_over_event=0.091143 motif_over_transition=0.216577
- `union_temporal_consensus_pair` event_fraction=0.808439 transition_fraction=0.541843 motif_fraction=0.589167 motif_over_event=-0.219272 motif_over_transition=0.047324

## Interpretation

A strong result requires positive Representation Gain in observed recurring streams and collapse of that gain under selective temporal or identity nulls.

Layer ablations compare whether canonical support is already present at the event/transition layer or is concentrated specifically by motifs.
