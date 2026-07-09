# Event-First Memory Prototype Report

## Question

When the same static graph is produced by different temporal processes, can the event graph distinguish them?

## Result

- Detected events: 452
- Detected transitions: 312
- Recurrent motifs: 45
- Event-first next-event accuracy, current event only: 0.667
- Event-first next-event accuracy, current event plus context: 0.886
- Event-first next-event accuracy, two-event history: 0.818
- Collapsed static next-event accuracy: 0.000
- Ambiguous {A,B} cases: 42
- Ambiguous {A,B} event-first accuracy: 0.500
- Ambiguous {A,B} collapsed-static accuracy: 0.000

The current-event model correctly treats `{A,B}` as ambiguous. Context-conditioned events and two-event histories resolve the branch, while the collapsed graph cannot represent either distinction.

The event view preserves temporal ordering and recovers the branches after `{A,B}`:

- `{B,C}` -> `{C,D}`: 58
- `{A,B}` -> `{B,C}`: 57
- `{A,B}` -> `{B,E}`: 54
- `{B,E}` -> `{E,F}`: 54
- `{B,C}` -> `{C,D,E}`: 2
- `{B,E}` -> `{A,F}`: 2
- `{A,B}` -> `{A,B,E}`: 2
- `{A,B,E}` -> `{B,E}`: 2

The collapsed graph contains unit co-occurrence edges, but it has no first-class representation of episode order, context, duration, or branch identity.

## Event Counts

- `{A,B}`: 117
- `{B,E}`: 64
- `{B,C}`: 62
- `{C,D}`: 60
- `{E,F}`: 59
- `{A,C}`: 5
- `{C,E}`: 4
- `{A,E}`: 4
- `{A,D}`: 4
- `{A,B,D}`: 4
- `{D,E}`: 4
- `{A,B,E}`: 4
- `{B,D}`: 3
- `{D,G}`: 3
- `{C,F}`: 3
- `{A,G}`: 3
- `{A,F}`: 3
- `{G,H}`: 3
- `{A,B,C}`: 3
- `{C,D,E}`: 2
- `{B,F}`: 2
- `{B,G}`: 2
- `{C,H}`: 2
- `{D,H}`: 2
- `{D,F}`: 2
- `{F,G}`: 2
- `{E,H}`: 2
- `{B,D,E}`: 2
- `{C,E,F}`: 2
- `{B,E,G}`: 2
- `{C,G}`: 1
- `{B,D,H}`: 1
- `{B,C,F}`: 1
- `{C,D,G}`: 1
- `{B,H}`: 1
- `{A,H}`: 1
- `{A,E,H}`: 1
- `{A,B,G}`: 1
- `{C,D,F}`: 1
- `{A,B,F}`: 1
- `{F,H}`: 1
- `{A,B,H}`: 1
- `{E,F,G}`: 1
- `{D,E,F}`: 1
- `{E,F,H}`: 1
- `{B,E,H}`: 1
- `{B,E,F}`: 1
- `{C,D,H}`: 1

## Top Motifs

- `{A,B}` support=117; next={B,C}, {B,E}, {A,B,E}, {A,B,C}, {B,D}, {B,E,H}, {B,E,G}; contexts=X:59, Z:57, N:1; outcomes=Y1:59, Y2:57, YN:1
- `{B,E}` support=64; next={E,F}, {A,F}, {B,D,E}, {E,H}, {B,E,G}, {A,B,E}, {C,E,F}; contexts=Z:62, N:2; outcomes=Y2:62, YN:2
- `{B,C}` support=62; next={C,D}, {C,D,E}; contexts=X:60, N:2; outcomes=Y1:60, YN:2
- `{C,D}` support=60; next=none; contexts=X:59, N:1; outcomes=Y1:59, YN:1
- `{E,F}` support=59; next={E,F,G}, {D,E,F}, {C,E,F}, {E,F,H}, {B,E}, {B,E,F}, {D,E}; contexts=Z:59; outcomes=Y2:59
- `{B,C} -> {C,D}` support=58; next=none; contexts=X:58; outcomes=Y1:58
- `{A,B} -> {B,C}` support=57; next={C,D}, {C,D,E}; contexts=X:57; outcomes=Y1:57
- `{A,B} -> {B,C} -> {C,D}` support=55; next=none; contexts=X:55; outcomes=Y1:55
- `{A,B} -> {B,E}` support=54; next={E,F}, {B,D,E}, {E,H}, {B,E,G}, {A,B,E}, {C,E,F}, {A,F}; contexts=Z:53, N:1; outcomes=Y2:53, YN:1
- `{B,E} -> {E,F}` support=54; next={E,F,G}, {D,E,F}, {C,E,F}, {E,F,H}, {B,E}, {B,E,F}, {D,E}; contexts=Z:54; outcomes=Y2:54

## Layer Information Loss

- `RawSignal` -> `Event` `record_count_ratio` = 0.026905: Event compression stores one detected coactivation object instead of every unit-time sample.
- `RawSignal` -> `Event` `active_signal_cell_coverage_ratio` = 1.272376: Ratio of event participant-duration cells to threshold-active unit-time cells; values above 1.0 indicate overcapture.
- `RawSignal` -> `Event` `active_signal_cell_overcapture_ratio` = 0.272376: Excess event participant-duration coverage beyond threshold-active unit-time cells.
- `RawSignal` -> `Event` `raw_sample_value_loss_fraction` = 0.764762: Fraction of original scalar sample positions not preserved as event participant-duration cells.
- `Event` -> `Transition` `record_count_ratio` = 0.690265: Transitions preserve adjacency pairs but drop standalone event payload unless joined back to events.
- `Event` -> `Transition` `event_payload_loss_fraction_without_join` = 0.555556: Transitions directly omit intensities, full participant set, source window, duration, and outcome.
- `Episode` -> `Motif` `recurring_three_event_window_retention` = 0.622093: Fraction of length-3 episode windows retained as recurrent motifs with support >= 2.
- `Event` -> `Motif` `motif_record_count_ratio` = 0.099558: Motifs are compressed recurring templates, not event-instance records.
- `Event` -> `StaticProjection` `node_count_ratio` = 0.017699: Static projection collapses event instances into participant unit nodes.
- `Event` -> `StaticProjection` `edge_count_ratio` = 0.089744: Static projection stores co-participant edges, not temporal event-transition edges.
- `Event` -> `StaticProjection` `event_instance_loss_fraction` = 1.000000: No event IDs, timestamps, durations, source windows, intensities, contexts, or outcomes survive as first-class static graph records.
- `Transition` -> `StaticProjection` `temporal_order_loss_fraction` = 1.000000: Directed temporal adjacency is absent from the collapsed undirected unit graph.
- `Event` -> `StaticProjection` `context_entropy_lost_bits` = 1.452956: Bits of event-context distribution that are not represented in the static projection.
- `Event` -> `StaticProjection` `outcome_entropy_lost_bits` = 1.452956: Bits of event-outcome distribution that are not represented in the static projection.
- `Event` -> `StaticProjection` `event_label_entropy_bits` = 3.569347: Entropy of event participant-set labels before static collapse.
- `Transition` -> `StaticProjection` `transition_entropy_lost_bits` = 4.100256: Bits of event-transition distribution erased by removing temporal adjacency.
- `EventHistory` -> `StaticProjection` `predictive_accuracy_delta` = 0.818182: Next-event accuracy lost when two-event temporal history is replaced by static co-occurrence.
- `EventContext` -> `StaticProjection` `contextual_predictive_accuracy_delta` = 0.886364: Next-event accuracy lost when event context is replaced by static co-occurrence.

## Information Envelope

- `RawSignal` `active_set_unique_count` = 112.000000: Distinct threshold-active unit sets observed directly in the signal stream.
- `RawSignal` `active_set_entropy_bits` = 5.032537: Entropy of threshold-active unit sets before event commitment.
- `Event` `event_label_unique_count` = 48.000000: Distinct first-class coactivation event labels.
- `Event` `event_label_entropy_bits` = 3.569347: Entropy of committed event participant sets.
- `Event` `event_label_redundancy_fraction` = 0.360900: How much event-label entropy falls below maximum entropy; higher values indicate recurrence and compression opportunity.
- `Event` `repeated_event_instance_fraction` = 0.960177: Fraction of event instances whose participant set appears more than once.
- `Transition` `transition_unique_count` = 87.000000: Distinct observed event-transition label pairs.
- `Transition` `transition_entropy_bits` = 4.100256: Entropy of temporal adjacency after event commitment.
- `Transition` `transition_redundancy_fraction` = 0.363605: How much transition entropy falls below maximum entropy; higher values indicate repeated temporal structure.
- `Episode` `episode_signature_unique_count` = 48.000000: Distinct ordered event-label sequences.
- `Episode` `episode_signature_entropy_bits` = 3.391859: Entropy of ordered episode signatures.
- `Episode` `repeated_episode_instance_fraction` = 0.671429: Fraction of episodes whose full event signature recurs.
- `Motif` `motif_count` = 45.000000: Number of recurring event patterns with support >= 2.
- `Motif` `motif_support_mass` = 776.000000: Total support represented by recurring motifs across all motif lengths.
- `Motif` `recurring_three_event_window_fraction` = 0.622093: Fraction of length-3 episode windows captured by recurring motifs.
- `StaticProjection` `static_node_count` = 8.000000: Participant nodes retained after collapsing event instances.
- `StaticProjection` `static_edge_count` = 28.000000: Co-participation edges retained after collapsing event instances.
- `System` `compressibility_index` = 0.448866: Composite recurrence signal across events, transitions, and length-3 motifs.

## Artifacts

- `raw_signals.csv`: generated temporal signal stream
- `events.csv`: detected coactivation hyperedges as first-class objects
- `transitions.csv`: temporal adjacency between detected events
- `episodes.csv`: ordered event sequences
- `motifs.csv`: recurrent event-transition patterns
- `layer_information_loss.csv`: compression and information-loss metrics by layer
- `information_envelope.csv`: entropy, redundancy, recurrence, and compressibility metrics
- `static_projection.graphml`: lossy collapsed unit co-occurrence graph
- `event_transition_graph.graphml`: event-level temporal graph
- `event_first_temporal_process_validation.md`: validation summary and interpretation
