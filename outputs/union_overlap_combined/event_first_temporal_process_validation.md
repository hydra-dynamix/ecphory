# Event-First Memory Prototype Report

## Question

When the same static graph is produced by different temporal processes, can the event graph distinguish them?

## Result

- Detected events: 1135
- Detected transitions: 935
- Recurrent motifs: 273
- Event-first next-event accuracy, current event only: 0.267
- Event-first next-event accuracy, current event plus context: 0.328
- Event-first next-event accuracy, two-event history: 0.233
- Collapsed static next-event accuracy: 0.000
- Ambiguous {A,B} cases: 63
- Ambiguous {A,B} event-first accuracy: 0.127
- Ambiguous {A,B} collapsed-static accuracy: 0.000

The current-event model correctly treats `{A,B}` as ambiguous. Context-conditioned events and two-event histories resolve the branch, while the collapsed graph cannot represent either distinction.

The event view preserves temporal ordering and recovers the branches after `{A,B}`:

- `{B,E}` -> `{E,F}`: 25
- `{A,B}` -> `{B,C}`: 25
- `{A,B}` -> `{B,E}`: 25
- `{B,C}` -> `{E,F}`: 24
- `{A,B}` -> `{B,G}`: 23
- `{B,G}` -> `{E,F}`: 19
- `{E,F}` -> `{D,E,F}`: 18
- `{E,F}` -> `{B,E,F}`: 16

The collapsed graph contains unit co-occurrence edges, but it has no first-class representation of episode order, context, duration, or branch identity.

## Event Counts

- `{E,F}`: 189
- `{A,B}`: 186
- `{B,E}`: 72
- `{B,C}`: 70
- `{B,G}`: 69
- `{B,E,F}`: 30
- `{A,B,E}`: 29
- `{A,B,H}`: 27
- `{A,B,C}`: 24
- `{D,E,F}`: 22
- `{A,B,G}`: 21
- `{E,F,G}`: 19
- `{A,E,F}`: 18
- `{A,B,D}`: 18
- `{B,C,E}`: 17
- `{A,B,F}`: 17
- `{E,F,H}`: 17
- `{D,E}`: 12
- `{B,C,D}`: 11
- `{E,G}`: 11
- `{C,E,F}`: 11
- `{B,D,G}`: 9
- `{A,F}`: 9
- `{B,G,H}`: 9
- `{B,C,G}`: 9
- `{B,F,G}`: 8
- `{A,G}`: 8
- `{F,H}`: 8
- `{B,C,F}`: 8
- `{D,G}`: 7
- `{B,E,G}`: 7
- `{B,D}`: 7
- `{B,H}`: 6
- `{C,E}`: 6
- `{C,H}`: 6
- `{B,C,H}`: 6
- `{D,H}`: 5
- `{C,G}`: 5
- `{B,D,E}`: 5
- `{B,F}`: 5
- `{A,E}`: 5
- `{F,G}`: 5
- `{C,F}`: 5
- `{A,E,G}`: 4
- `{B,E,H}`: 4
- `{A,H}`: 4
- `{C,D}`: 4
- `{A,D}`: 4
- `{D,F}`: 4
- `{G,H}`: 3
- `{A,C}`: 3
- `{C,E,G}`: 3
- `{C,F,H}`: 3
- `{A,B,D,E}`: 3
- `{A,G,H}`: 2
- `{C,F,G}`: 2
- `{B,E,G,H}`: 2
- `{A,B,E,H}`: 2
- `{E,H}`: 2
- `{A,D,E}`: 2
- `{A,C,H}`: 2
- `{B,E,F,G}`: 2
- `{A,B,C,H}`: 2
- `{A,E,F,G}`: 2
- `{A,B,E,F}`: 2
- `{B,C,E,H}`: 2
- `{D,E,F,G}`: 2
- `{A,B,E,G}`: 1
- `{A,D,G}`: 1
- `{A,D,E,F}`: 1
- `{B,C,D,H}`: 1
- `{B,D,F}`: 1
- `{A,B,F,H}`: 1
- `{A,C,E}`: 1
- `{A,F,H}`: 1
- `{A,B,D,E,H}`: 1
- `{A,E,H}`: 1
- `{A,B,C,G}`: 1
- `{B,D,E,H}`: 1
- `{D,E,H}`: 1
- `{A,B,E,G,H}`: 1
- `{A,B,D,E,F}`: 1
- `{D,E,G}`: 1
- `{B,D,E,F}`: 1
- `{B,C,D,F}`: 1
- `{A,B,G,H}`: 1
- `{A,C,D}`: 1
- `{C,E,F,G}`: 1
- `{A,B,C,E}`: 1
- `{D,E,F,H}`: 1
- `{A,B,D,G,H}`: 1
- `{B,C,D,E,F}`: 1
- `{A,B,C,F}`: 1
- `{B,C,D,F,H}`: 1
- `{A,F,G}`: 1
- `{C,E,F,H}`: 1
- `{B,F,G,H}`: 1
- `{B,C,F,H}`: 1
- `{B,C,G,H}`: 1

## Top Motifs

- `{E,F}` support=189; next={D,E,F}, {B,E,F}, {A,E,F}, {E,F,G}, {C,E,F}, {E,F}, {E,F,H}, {A,F}, {A,B}, {F,H}, {A,D,E,F}, {C,G}, {E,G}, {C,D}, {A,G}, {C,H}, {A,H}, {D,E}, {B,C,D,E,F}, {D,F}, {A,E,F,G}, {D,E,F,G}, {C,E,F,H}, {C,F}, {E,H}; contexts=X:63, Z:62, W:61, N:3; outcomes=Y1:63, Y2:62, Y3:61, YN:3
- `{A,B}` support=186; next={B,C}, {B,E}, {B,G}, {A,B,E}, {A,B,F}, {A,B,D}, {A,B,H}, {A,B,C}, {A,B}, {A,B,G}, {B,D}, {B,G,H}, {B,C,E}, {B,E,H}, {B,D,G}, {A,G}, {C,F}, {C,H}, {E,F}, {B,D,E}, {A,B,F,H}, {F,H}, {D,H}, {B,D,E,H}, {A,B,D,E,F}, {D,G}, {A,B,D,E}, {B,F,G}, {B,C,F}, {A,F}, {A,E}, {A,B,D,G,H}, {A,B,C,F}, {B,C,D,F,H}, {D,F}, {B,C,D}, {C,G}, {A,C}, {B,F}, {B,C,G}, {A,B,C,H}; contexts=Z:63, X:61, W:60, N:2; outcomes=Y2:63, Y1:61, Y3:60, YN:2
- `{B,E}` support=72; next={E,F}, {B,C,E}, {B,E,F}, {A,B,E}, {B,D,E}, {D,G}, {B,E,G}, {B,E}, {B,G}, {B,E,F,G}, {E,F,G}, {D,E,F}, {E,F,H}, {C,E}, {A,F,H}, {E,G}, {A,B}, {A,B,E,H}, {B,F}, {A,E}, {C,E,F,G}, {A,B,C,E}, {D,E,F,H}, {A,B,E,F}, {A,B,D,E}, {B,E,H}, {B,D}; contexts=Z:66, N:3, W:2, X:1; outcomes=Y2:66, YN:3, Y3:2, Y1:1
- `{B,C}` support=70; next={E,F}, {B,C,D}, {B,C,E}, {A,B,C}, {B,C,F}, {B,H}, {C,E}, {E,F,G}, {B,E,F}, {B,C,G}, {B,C,H}, {A,E,F}, {C,E,G}, {B,F}, {B,C}, {D,E}, {E,F,H}, {A,B,C,H}, {B,C,E,H}, {C,E,F}, {B,C,F,H}, {B,D}, {B,E}; contexts=X:61, N:7, Z:2; outcomes=Y1:61, YN:7, Y2:2
- `{B,G}` support=69; next={E,F}, {B,D,G}, {B,E,G}, {B,F,G}, {B,G,H}, {B,E}, {A,B,G}, {E,F,G}, {C,G}, {B,E,G,H}, {B,E,F}, {B,C,G}, {B,G}, {A,B,E,G,H}, {A,E,F}, {A,E,F,G}, {D,E,F}, {A,H}, {E,G}, {A,F}, {C,E,F}, {B,F,G,H}, {E,F,H}, {B,C,G,H}, {D,E}, {A,B}; contexts=W:64, N:3, Z:2; outcomes=Y3:64, YN:3, Y2:2
- `{B,E,F}` support=30; next={E,F}, {D,E}, {B,E}, {C,E}, {E,F,H}, {C,F}, {A,E,F}; contexts=Z:16, X:7, W:7; outcomes=Y2:16, Y1:7, Y3:7
- `{A,B,E}` support=29; next={A,B}, {B,E}, {B,C}, {E,F}, {B,G}, {A,B,H}, {B,E,F}, {E,G}, {A,C,D}, {B,D}, {B,C,H}; contexts=Z:16, X:7, W:6; outcomes=Y2:16, Y1:7, Y3:6
- `{A,B,H}` support=27; next={A,B}, {B,G}, {B,E}, {B,C}, {A,B,E}, {D,F}, {A,B,G}, {B,H}, {B,F,G}, {B,C,E}, {B,G,H}, {B,C,F}; contexts=X:11, W:9, Z:6, N:1; outcomes=Y1:11, Y3:9, Y2:6, YN:1
- `{B,E} -> {E,F}` support=25; next={D,E,F}, {B,E,F}, {E,F}, {C,E,F}, {A,F}, {E,F,G}, {D,F}, {A,E,F,G}, {C,E,F,H}, {A,E,F}; contexts=Z:24, W:1; outcomes=Y2:24, Y3:1
- `{A,B} -> {B,C}` support=25; next={E,F}, {B,C,E}, {B,C,D}, {A,B,C}, {E,F,G}, {B,E,F}, {B,C,G}, {E,F,H}, {B,C,F}, {B,C,H}, {B,E}; contexts=X:24, Z:1; outcomes=Y1:24, Y2:1

## Layer Information Loss

- `RawSignal` -> `Event` `record_count_ratio` = 0.047292: Event compression stores one detected coactivation object instead of every unit-time sample.
- `RawSignal` -> `Event` `active_signal_cell_coverage_ratio` = 1.059448: Ratio of event participant-duration cells to threshold-active unit-time cells; values above 1.0 indicate overcapture.
- `RawSignal` -> `Event` `active_signal_cell_overcapture_ratio` = 0.059448: Excess event participant-duration coverage beyond threshold-active unit-time cells.
- `RawSignal` -> `Event` `raw_sample_value_loss_fraction` = 0.804708: Fraction of original scalar sample positions not preserved as event participant-duration cells.
- `Event` -> `Transition` `record_count_ratio` = 0.823789: Transitions preserve adjacency pairs but drop standalone event payload unless joined back to events.
- `Event` -> `Transition` `event_payload_loss_fraction_without_join` = 0.555556: Transitions directly omit intensities, full participant set, source window, duration, and outcome.
- `Episode` -> `Motif` `recurring_three_event_window_retention` = 0.284354: Fraction of length-3 episode windows retained as recurrent motifs with support >= 2.
- `Event` -> `Motif` `motif_record_count_ratio` = 0.240529: Motifs are compressed recurring templates, not event-instance records.
- `Event` -> `StaticProjection` `node_count_ratio` = 0.007048: Static projection collapses event instances into participant unit nodes.
- `Event` -> `StaticProjection` `edge_count_ratio` = 0.029947: Static projection stores co-participant edges, not temporal event-transition edges.
- `Event` -> `StaticProjection` `event_instance_loss_fraction` = 1.000000: No event IDs, timestamps, durations, source windows, intensities, contexts, or outcomes survive as first-class static graph records.
- `Transition` -> `StaticProjection` `temporal_order_loss_fraction` = 1.000000: Directed temporal adjacency is absent from the collapsed undirected unit graph.
- `Event` -> `StaticProjection` `context_entropy_lost_bits` = 1.901528: Bits of event-context distribution that are not represented in the static projection.
- `Event` -> `StaticProjection` `outcome_entropy_lost_bits` = 1.901528: Bits of event-outcome distribution that are not represented in the static projection.
- `Event` -> `StaticProjection` `event_label_entropy_bits` = 4.906364: Entropy of event participant-set labels before static collapse.
- `Transition` -> `StaticProjection` `transition_entropy_lost_bits` = 7.924518: Bits of event-transition distribution erased by removing temporal adjacency.
- `EventHistory` -> `StaticProjection` `predictive_accuracy_delta` = 0.233333: Next-event accuracy lost when two-event temporal history is replaced by static co-occurrence.
- `EventContext` -> `StaticProjection` `contextual_predictive_accuracy_delta` = 0.328063: Next-event accuracy lost when event context is replaced by static co-occurrence.

## Information Envelope

- `RawSignal` `active_set_unique_count` = 107.000000: Distinct threshold-active unit sets observed directly in the signal stream.
- `RawSignal` `active_set_entropy_bits` = 4.788075: Entropy of threshold-active unit sets before event commitment.
- `Event` `event_label_unique_count` = 99.000000: Distinct first-class coactivation event labels.
- `Event` `event_label_entropy_bits` = 4.906364: Entropy of committed event participant sets.
- `Event` `event_label_redundancy_fraction` = 0.259903: How much event-label entropy falls below maximum entropy; higher values indicate recurrence and compression opportunity.
- `Event` `repeated_event_instance_fraction` = 0.971806: Fraction of event instances whose participant set appears more than once.
- `Transition` `transition_unique_count` = 418.000000: Distinct observed event-transition label pairs.
- `Transition` `transition_entropy_bits` = 7.924518: Entropy of temporal adjacency after event commitment.
- `Transition` `transition_redundancy_fraction` = 0.089906: How much transition entropy falls below maximum entropy; higher values indicate repeated temporal structure.
- `Episode` `episode_signature_unique_count` = 196.000000: Distinct ordered event-label sequences.
- `Episode` `episode_signature_entropy_bits` = 7.603856: Entropy of ordered episode signatures.
- `Episode` `repeated_episode_instance_fraction` = 0.040000: Fraction of episodes whose full event signature recurs.
- `Motif` `motif_count` = 273.000000: Number of recurring event patterns with support >= 2.
- `Motif` `motif_support_mass` = 1960.000000: Total support represented by recurring motifs across all motif lengths.
- `Motif` `recurring_three_event_window_fraction` = 0.284354: Fraction of length-3 episode windows captured by recurring motifs.
- `StaticProjection` `static_node_count` = 8.000000: Participant nodes retained after collapsing event instances.
- `StaticProjection` `static_edge_count` = 28.000000: Co-participation edges retained after collapsing event instances.
- `System` `compressibility_index` = 0.211388: Composite recurrence signal across events, transitions, and length-3 motifs.

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
