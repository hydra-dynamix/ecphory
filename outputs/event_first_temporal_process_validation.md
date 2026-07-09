# Event-First Memory Prototype Report

## Question

When the same static graph is produced by different temporal processes, can the event graph distinguish them?

## Result

- Detected events: 420
- Detected transitions: 280
- Recurrent motifs: 25
- Event-first next-event accuracy, current event only: 0.750
- Event-first next-event accuracy, current event plus context: 1.000
- Event-first next-event accuracy, two-event history: 1.000
- Collapsed static next-event accuracy: 0.000
- Ambiguous {A,B} cases: 42
- Ambiguous {A,B} event-first accuracy: 0.500
- Ambiguous {A,B} collapsed-static accuracy: 0.000

The current-event model correctly treats `{A,B}` as ambiguous. Context-conditioned events and two-event histories resolve the branch, while the collapsed graph cannot represent either distinction.

The event view preserves temporal ordering and recovers the branches after `{A,B}`:

- `{A,B}` -> `{B,C}`: 60
- `{B,C}` -> `{C,D}`: 60
- `{A,B}` -> `{B,E}`: 60
- `{B,E}` -> `{E,F}`: 60
- `{B,E}` -> `{A,H}`: 1
- `{A,H}` -> `{C,G}`: 1
- `{B,C}` -> `{B,D}`: 1
- `{B,D}` -> `{A,F}`: 1

The collapsed graph contains unit co-occurrence edges, but it has no first-class representation of episode order, context, duration, or branch identity.

## Event Counts

- `{A,B}`: 125
- `{C,D}`: 63
- `{B,E}`: 63
- `{E,F}`: 63
- `{B,C}`: 61
- `{A,G}`: 5
- `{A,F}`: 4
- `{A,H}`: 3
- `{C,G}`: 3
- `{B,D}`: 3
- `{C,F}`: 3
- `{F,G}`: 3
- `{D,G}`: 2
- `{A,C}`: 2
- `{A,D}`: 2
- `{C,H}`: 2
- `{G,H}`: 2
- `{D,F}`: 2
- `{D,E}`: 2
- `{D,H}`: 1
- `{E,H}`: 1
- `{A,E}`: 1
- `{C,E}`: 1
- `{B,G}`: 1
- `{F,H}`: 1
- `{E,G}`: 1

## Top Motifs

- `{A,B}` support=125; next={B,C}, {B,E}, {C,G}, {A,B}, {F,H}; contexts=X:60, Z:60, N:5; outcomes=Y1:60, Y2:60, YN:5
- `{C,D}` support=63; next={A,F}; contexts=X:60, N:3; outcomes=Y1:60, YN:3
- `{B,E}` support=63; next={E,F}, {A,H}, {C,D}, {F,G}; contexts=Z:60, N:3; outcomes=Y2:60, YN:3
- `{E,F}` support=63; next={F,G}; contexts=Z:60, N:3; outcomes=Y2:60, YN:3
- `{B,C}` support=61; next={C,D}, {B,D}; contexts=X:60, N:1; outcomes=Y1:60, YN:1
- `{A,B} -> {B,C}` support=60; next={C,D}; contexts=X:60; outcomes=Y1:60
- `{B,C} -> {C,D}` support=60; next=none; contexts=X:60; outcomes=Y1:60
- `{A,B} -> {B,C} -> {C,D}` support=60; next=none; contexts=X:60; outcomes=Y1:60
- `{A,B} -> {B,E}` support=60; next={E,F}; contexts=Z:60; outcomes=Y2:60
- `{B,E} -> {E,F}` support=60; next=none; contexts=Z:60; outcomes=Y2:60

## Layer Information Loss

- `RawSignal` -> `Event` `record_count_ratio` = 0.025000: Event compression stores one detected coactivation object instead of every unit-time sample.
- `RawSignal` -> `Event` `active_signal_cell_coverage_ratio` = 1.000000: Ratio of event participant-duration cells to threshold-active unit-time cells; values above 1.0 indicate overcapture.
- `RawSignal` -> `Event` `active_signal_cell_overcapture_ratio` = 0.000000: Excess event participant-duration coverage beyond threshold-active unit-time cells.
- `RawSignal` -> `Event` `raw_sample_value_loss_fraction` = 0.850000: Fraction of original scalar sample positions not preserved as event participant-duration cells.
- `Event` -> `Transition` `record_count_ratio` = 0.666667: Transitions preserve adjacency pairs but drop standalone event payload unless joined back to events.
- `Event` -> `Transition` `event_payload_loss_fraction_without_join` = 0.555556: Transitions directly omit intensities, full participant set, source window, duration, and outcome.
- `Episode` -> `Motif` `recurring_three_event_window_retention` = 0.857143: Fraction of length-3 episode windows retained as recurrent motifs with support >= 2.
- `Event` -> `Motif` `motif_record_count_ratio` = 0.059524: Motifs are compressed recurring templates, not event-instance records.
- `Event` -> `StaticProjection` `node_count_ratio` = 0.019048: Static projection collapses event instances into participant unit nodes.
- `Event` -> `StaticProjection` `edge_count_ratio` = 0.092857: Static projection stores co-participant edges, not temporal event-transition edges.
- `Event` -> `StaticProjection` `event_instance_loss_fraction` = 1.000000: No event IDs, timestamps, durations, source windows, intensities, contexts, or outcomes survive as first-class static graph records.
- `Transition` -> `StaticProjection` `temporal_order_loss_fraction` = 1.000000: Directed temporal adjacency is absent from the collapsed undirected unit graph.
- `Event` -> `StaticProjection` `context_entropy_lost_bits` = 1.448816: Bits of event-context distribution that are not represented in the static projection.
- `Event` -> `StaticProjection` `outcome_entropy_lost_bits` = 1.448816: Bits of event-outcome distribution that are not represented in the static projection.
- `Event` -> `StaticProjection` `event_label_entropy_bits` = 2.953322: Entropy of event participant-set labels before static collapse.
- `Transition` -> `StaticProjection` `transition_entropy_lost_bits` = 3.066234: Bits of event-transition distribution erased by removing temporal adjacency.
- `EventHistory` -> `StaticProjection` `predictive_accuracy_delta` = 1.000000: Next-event accuracy lost when two-event temporal history is replaced by static co-occurrence.
- `EventContext` -> `StaticProjection` `contextual_predictive_accuracy_delta` = 1.000000: Next-event accuracy lost when event context is replaced by static co-occurrence.

## Information Envelope

- `RawSignal` `active_set_unique_count` = 26.000000: Distinct threshold-active unit sets observed directly in the signal stream.
- `RawSignal` `active_set_entropy_bits` = 2.953322: Entropy of threshold-active unit sets before event commitment.
- `Event` `event_label_unique_count` = 26.000000: Distinct first-class coactivation event labels.
- `Event` `event_label_entropy_bits` = 2.953322: Entropy of committed event participant sets.
- `Event` `event_label_redundancy_fraction` = 0.371692: How much event-label entropy falls below maximum entropy; higher values indicate recurrence and compression opportunity.
- `Event` `repeated_event_instance_fraction` = 0.983333: Fraction of event instances whose participant set appears more than once.
- `Transition` `transition_unique_count` = 44.000000: Distinct observed event-transition label pairs.
- `Transition` `transition_entropy_bits` = 3.066234: Entropy of temporal adjacency after event commitment.
- `Transition` `transition_redundancy_fraction` = 0.438360: How much transition entropy falls below maximum entropy; higher values indicate repeated temporal structure.
- `Episode` `episode_signature_unique_count` = 22.000000: Distinct ordered event-label sequences.
- `Episode` `episode_signature_entropy_bits` = 2.066234: Entropy of ordered episode signatures.
- `Episode` `repeated_episode_instance_fraction` = 0.857143: Fraction of episodes whose full event signature recurs.
- `Motif` `motif_count` = 25.000000: Number of recurring event patterns with support >= 2.
- `Motif` `motif_support_mass` = 773.000000: Total support represented by recurring motifs across all motif lengths.
- `Motif` `recurring_three_event_window_fraction` = 0.857143: Fraction of length-3 episode windows captured by recurring motifs.
- `StaticProjection` `static_node_count` = 8.000000: Participant nodes retained after collapsing event instances.
- `StaticProjection` `static_edge_count` = 26.000000: Co-participation edges retained after collapsing event instances.
- `System` `compressibility_index` = 0.555732: Composite recurrence signal across events, transitions, and length-3 motifs.

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
