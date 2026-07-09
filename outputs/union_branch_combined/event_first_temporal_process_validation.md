# Event-First Memory Prototype Report

## Question

When the same static graph is produced by different temporal processes, can the event graph distinguish them?

## Result

- Detected events: 811
- Detected transitions: 671
- Recurrent motifs: 224
- Event-first next-event accuracy, current event only: 0.240
- Event-first next-event accuracy, current event plus context: 0.315
- Event-first next-event accuracy, two-event history: 0.267
- Collapsed static next-event accuracy: 0.000
- Ambiguous {A,B} cases: 44
- Ambiguous {A,B} event-first accuracy: 0.159
- Ambiguous {A,B} collapsed-static accuracy: 0.000

The current-event model correctly treats `{A,B}` as ambiguous. Context-conditioned events and two-event histories resolve the branch, while the collapsed graph cannot represent either distinction.

The event view preserves temporal ordering and recovers the branches after `{A,B}`:

- `{A,B}` -> `{B,E}`: 25
- `{B,C}` -> `{C,D}`: 23
- `{A,B}` -> `{B,C}`: 22
- `{B,E}` -> `{E,F}`: 21
- `{A,B,C}` -> `{B,C}`: 10
- `{A,B}` -> `{A,B,C}`: 10
- `{A,B}` -> `{A,B,F}`: 9
- `{A,B}` -> `{A,B,E}`: 9

The collapsed graph contains unit co-occurrence edges, but it has no first-class representation of episode order, context, duration, or branch identity.

## Event Counts

- `{A,B}`: 123
- `{B,C}`: 71
- `{B,E}`: 69
- `{E,F}`: 67
- `{C,D}`: 64
- `{A,B,C}`: 24
- `{A,B,E}`: 20
- `{A,B,D}`: 16
- `{B,C,E}`: 14
- `{A,B,F}`: 14
- `{A,B,G}`: 12
- `{C,D,G}`: 12
- `{B,E,F}`: 10
- `{D,E}`: 10
- `{C,E}`: 9
- `{B,D,E}`: 9
- `{B,C,F}`: 9
- `{E,F,H}`: 9
- `{B,C,G}`: 8
- `{C,H}`: 8
- `{A,B,H}`: 8
- `{B,E,H}`: 8
- `{D,E,F}`: 8
- `{C,D,E}`: 7
- `{D,H}`: 7
- `{C,D,H}`: 7
- `{A,H}`: 7
- `{A,E,F}`: 7
- `{A,C}`: 7
- `{B,C,D}`: 7
- `{B,E,G}`: 7
- `{B,G}`: 6
- `{C,F}`: 6
- `{G,H}`: 6
- `{B,D}`: 5
- `{C,D,F}`: 5
- `{A,D}`: 5
- `{A,C,D}`: 5
- `{D,G}`: 4
- `{A,G}`: 4
- `{A,E}`: 4
- `{E,G}`: 4
- `{E,H}`: 4
- `{A,B,E,G}`: 4
- `{C,E,F}`: 4
- `{D,F}`: 4
- `{B,C,H}`: 4
- `{E,F,G}`: 4
- `{B,C,E,F}`: 3
- `{B,C,D,F}`: 3
- `{B,H}`: 3
- `{A,F}`: 3
- `{F,G}`: 3
- `{B,D,E,G}`: 3
- `{C,E,G}`: 2
- `{C,G}`: 2
- `{A,E,H}`: 2
- `{A,B,C,D}`: 2
- `{A,C,D,H}`: 2
- `{A,C,E,F}`: 2
- `{A,C,D,E}`: 2
- `{C,D,E,H}`: 1
- `{B,D,H}`: 1
- `{B,F}`: 1
- `{D,E,F,G}`: 1
- `{B,F,H}`: 1
- `{B,C,E,G}`: 1
- `{C,G,H}`: 1
- `{A,G,H}`: 1
- `{A,C,H}`: 1
- `{A,E,F,H}`: 1
- `{D,F,H}`: 1
- `{A,D,H}`: 1
- `{A,E,G}`: 1
- `{A,D,F}`: 1
- `{C,D,F,G}`: 1
- `{C,F,G}`: 1
- `{A,C,D,F}`: 1
- `{A,D,E}`: 1
- `{A,B,C,D,E,H}`: 1
- `{A,B,C,G}`: 1
- `{D,G,H}`: 1
- `{F,G,H}`: 1
- `{F,H}`: 1
- `{A,F,H}`: 1
- `{B,D,G}`: 1
- `{A,B,E,F}`: 1
- `{B,E,F,H}`: 1
- `{A,C,E}`: 1
- `{A,C,F,H}`: 1
- `{A,B,E,H}`: 1
- `{A,B,G,H}`: 1
- `{B,D,E,F}`: 1
- `{A,B,D,F}`: 1
- `{A,B,D,H}`: 1
- `{A,E,G,H}`: 1
- `{A,B,C,H}`: 1
- `{B,C,D,E}`: 1
- `{A,B,D,G}`: 1
- `{B,E,F,G}`: 1
- `{D,E,F,H}`: 1
- `{A,B,D,G,H}`: 1
- `{A,B,F,G}`: 1
- `{C,D,E,G}`: 1

## Top Motifs

- `{A,B}` support=123; next={B,E}, {B,C}, {A,B,C}, {A,B,F}, {A,B,E}, {A,B,D}, {A,B,G}, {A,B,H}, {B,C,G}, {A,B,E,G}, {C,H}, {B,D,E}, {B,E,H}, {A,B}, {B,C,E}, {E,G}, {A,C}, {A,F}, {C,E}, {B,C,D}, {A,B,E,F}, {G,H}, {A,H}, {A,B,D,F}, {A,B,D,H}, {A,E,G,H}, {A,B,C,H}, {D,G}, {C,F}, {A,E,H}, {A,B,D,G,H}; contexts=X:61, Z:59, N:3; outcomes=Y1:61, Y2:59, YN:3
- `{B,C}` support=71; next={C,D}, {B,C,F}, {B,C}, {A,B,C}, {B,C,H}, {B,C,E}, {B,C,D}, {B,C,G}, {E,F}, {A,H}, {D,H}, {C,D,G}, {C,D,E,H}, {C,D,H}, {B,H}, {C,D,F,G}, {A,C,D,F}, {C,H}, {B,E}, {A,C,D,E}, {A,D}, {A,B,G}, {B,E,F}; contexts=X:66, N:3, Z:2; outcomes=Y1:66, YN:3, Y2:2
- `{B,E}` support=69; next={E,F}, {B,E,F}, {B,D,E}, {B,E,G}, {B,C,E}, {A,B,E}, {B,E,H}, {B,E}, {A,E,F}, {A,B,E,G}, {B,G}, {B,C,E,G}, {C,E}, {B,D,E,G}, {B,C,E,F}, {C,D}, {A,B,C}, {B,C,D,E}, {A,B}, {B,E,F,G}, {B,C}, {E,F,H}, {D,E}, {E,G}, {A,F}; contexts=Z:65, N:2, X:2; outcomes=Y2:65, YN:2, Y1:2
- `{E,F}` support=67; next={D,E,F}, {E,F,H}, {E,F}, {C,E,F}, {A,E,F}, {D,E}, {A,C,E,F}, {E,F,G}, {B,E,F}, {A,B}, {C,E}, {A,H}, {B,E}, {D,E,F,H}, {C,D}; contexts=Z:65, N:1, X:1; outcomes=Y2:65, YN:1, Y1:1
- `{C,D}` support=64; next={C,D,E}, {C,D,H}, {C,D,G}, {C,D,F}, {A,C,D}, {D,H}, {B,D}, {B,C,D}, {C,D}, {A,C,D,H}, {B,E,F}, {D,F}, {A,B,C,D}, {C,F}, {D,E}, {C,D,E,G}; contexts=X:62, N:2; outcomes=Y1:62, YN:2
- `{A,B} -> {B,E}` support=25; next={E,F}, {B,E}, {B,D,E}, {B,C,E}, {A,B,E}, {B,E,H}, {B,E,G}, {B,E,F}, {C,E}, {A,B,C}, {B,C}, {A,B,E,G}; contexts=Z:24, N:1; outcomes=Y2:24, YN:1
- `{A,B,C}` support=24; next={B,C}, {C,D}, {A,B}, {B,E}, {A,B,F}, {A,B,C}, {B,C,E}, {A,B,E}; contexts=X:17, Z:7; outcomes=Y1:17, Y2:7
- `{B,C} -> {C,D}` support=23; next={C,D,H}, {D,H}, {C,D,G}, {A,B,C,D}, {C,D}, {A,C,D,H}, {C,D,F}, {B,C,D}, {C,D,E}, {D,E}, {B,D}; contexts=X:23; outcomes=Y1:23
- `{A,B} -> {B,C}` support=22; next={C,D}, {B,C,G}, {B,C,H}, {B,C,E}, {C,D,H}, {A,B,C}, {A,C,D,F}, {A,H}, {C,H}, {B,C,D}, {B,E}, {D,H}, {B,C}, {C,D,G}, {B,C,F}; contexts=X:22; outcomes=Y1:22
- `{B,E} -> {E,F}` support=21; next={D,E,F}, {C,E,F}, {B,E,F}, {A,E,F}, {D,E}, {E,F,H}, {D,E,F,H}, {E,F}; contexts=Z:21; outcomes=Y2:21

## Layer Information Loss

- `RawSignal` -> `Event` `record_count_ratio` = 0.048274: Event compression stores one detected coactivation object instead of every unit-time sample.
- `RawSignal` -> `Event` `active_signal_cell_coverage_ratio` = 1.072118: Ratio of event participant-duration cells to threshold-active unit-time cells; values above 1.0 indicate overcapture.
- `RawSignal` -> `Event` `active_signal_cell_overcapture_ratio` = 0.072118: Excess event participant-duration coverage beyond threshold-active unit-time cells.
- `RawSignal` -> `Event` `raw_sample_value_loss_fraction` = 0.801786: Fraction of original scalar sample positions not preserved as event participant-duration cells.
- `Event` -> `Transition` `record_count_ratio` = 0.827374: Transitions preserve adjacency pairs but drop standalone event payload unless joined back to events.
- `Event` -> `Transition` `event_payload_loss_fraction_without_join` = 0.555556: Transitions directly omit intensities, full participant set, source window, duration, and outcome.
- `Episode` -> `Motif` `recurring_three_event_window_retention` = 0.293785: Fraction of length-3 episode windows retained as recurrent motifs with support >= 2.
- `Event` -> `Motif` `motif_record_count_ratio` = 0.276202: Motifs are compressed recurring templates, not event-instance records.
- `Event` -> `StaticProjection` `node_count_ratio` = 0.009864: Static projection collapses event instances into participant unit nodes.
- `Event` -> `StaticProjection` `edge_count_ratio` = 0.041729: Static projection stores co-participant edges, not temporal event-transition edges.
- `Event` -> `StaticProjection` `event_instance_loss_fraction` = 1.000000: No event IDs, timestamps, durations, source windows, intensities, contexts, or outcomes survive as first-class static graph records.
- `Transition` -> `StaticProjection` `temporal_order_loss_fraction` = 1.000000: Directed temporal adjacency is absent from the collapsed undirected unit graph.
- `Event` -> `StaticProjection` `context_entropy_lost_bits` = 1.456388: Bits of event-context distribution that are not represented in the static projection.
- `Event` -> `StaticProjection` `outcome_entropy_lost_bits` = 1.456388: Bits of event-outcome distribution that are not represented in the static projection.
- `Event` -> `StaticProjection` `event_label_entropy_bits` = 5.189002: Entropy of event participant-set labels before static collapse.
- `Transition` -> `StaticProjection` `transition_entropy_lost_bits` = 7.789230: Bits of event-transition distribution erased by removing temporal adjacency.
- `EventHistory` -> `StaticProjection` `predictive_accuracy_delta` = 0.267327: Next-event accuracy lost when two-event temporal history is replaced by static co-occurrence.
- `EventContext` -> `StaticProjection` `contextual_predictive_accuracy_delta` = 0.315217: Next-event accuracy lost when event context is replaced by static co-occurrence.

## Information Envelope

- `RawSignal` `active_set_unique_count` = 112.000000: Distinct threshold-active unit sets observed directly in the signal stream.
- `RawSignal` `active_set_entropy_bits` = 5.032537: Entropy of threshold-active unit sets before event commitment.
- `Event` `event_label_unique_count` = 104.000000: Distinct first-class coactivation event labels.
- `Event` `event_label_entropy_bits` = 5.189002: Entropy of committed event participant sets.
- `Event` `event_label_redundancy_fraction` = 0.225573: How much event-label entropy falls below maximum entropy; higher values indicate recurrence and compression opportunity.
- `Event` `repeated_event_instance_fraction` = 0.946979: Fraction of event instances whose participant set appears more than once.
- `Transition` `transition_unique_count` = 343.000000: Distinct observed event-transition label pairs.
- `Transition` `transition_entropy_bits` = 7.789230: Entropy of temporal adjacency after event commitment.
- `Transition` `transition_redundancy_fraction` = 0.075140: How much transition entropy falls below maximum entropy; higher values indicate repeated temporal structure.
- `Episode` `episode_signature_unique_count` = 139.000000: Distinct ordered event-label sequences.
- `Episode` `episode_signature_entropy_bits` = 7.114997: Entropy of ordered episode signatures.
- `Episode` `repeated_episode_instance_fraction` = 0.014286: Fraction of episodes whose full event signature recurs.
- `Motif` `motif_count` = 224.000000: Number of recurring event patterns with support >= 2.
- `Motif` `motif_support_mass` = 1357.000000: Total support represented by recurring motifs across all motif lengths.
- `Motif` `recurring_three_event_window_fraction` = 0.293785: Fraction of length-3 episode windows captured by recurring motifs.
- `StaticProjection` `static_node_count` = 8.000000: Participant nodes retained after collapsing event instances.
- `StaticProjection` `static_edge_count` = 28.000000: Co-participation edges retained after collapsing event instances.
- `System` `compressibility_index` = 0.198166: Composite recurrence signal across events, transitions, and length-3 motifs.

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
