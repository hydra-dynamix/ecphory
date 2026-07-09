# Adversarial Falsification Battery

This battery tries to break the event-first hierarchy after event identity has already been discretized. That means failures here are not detector failures; they are representation, novelty-gate, or metric failures.

Classifier mode: `evidence_index`.

## Summary

### small length 3

- `unique_triplets` expectation=no_recurrence naive_failures=0/3 evidence_index_failures=0/3 len3_mean=0.000000 full_sequence_mean=0.000000 compressibility_mean=0.000000 history_accuracy_mean=0.000000 outcome_purity_max_mean=0.000000 failure_modes={} evidence_failure_modes={} len3_index_statuses={} full_index_statuses={}
- `shared_edges_unique_middle` expectation=partial_recurrence_only naive_failures=0/3 evidence_index_failures=0/3 len3_mean=0.000000 full_sequence_mean=0.000000 compressibility_mean=0.134374 history_accuracy_mean=0.000000 outcome_purity_max_mean=0.000000 failure_modes={} evidence_failure_modes={} len3_index_statuses={} full_index_statuses={}
- `near_miss_drift` expectation=partial_recurrence_only naive_failures=0/3 evidence_index_failures=0/3 len3_mean=0.000000 full_sequence_mean=0.000000 compressibility_mean=0.067254 history_accuracy_mean=0.000000 outcome_purity_max_mean=0.000000 failure_modes={} evidence_failure_modes={} len3_index_statuses={} full_index_statuses={}
- `hidden_novelty_alias_collision` expectation=hidden_novelty naive_failures=3/3 evidence_index_failures=0/3 len3_mean=1.000000 full_sequence_mean=1.000000 compressibility_mean=0.333333 history_accuracy_mean=1.000000 outcome_purity_max_mean=0.016667 failure_modes={'compressed_hidden_or_contradictory_novelty': 3, 'low_outcome_purity': 3} evidence_failure_modes={} len3_index_statuses={'ambiguous_evidence': 3} full_index_statuses={'ambiguous_evidence': 3}
- `contradictory_outcomes` expectation=outcome_contradiction naive_failures=3/3 evidence_index_failures=0/3 len3_mean=1.000000 full_sequence_mean=1.000000 compressibility_mean=0.333333 history_accuracy_mean=1.000000 outcome_purity_max_mean=0.150000 failure_modes={'compressed_hidden_or_contradictory_novelty': 3, 'low_outcome_purity': 3} evidence_failure_modes={} len3_index_statuses={'ambiguous_evidence': 3} full_index_statuses={'ambiguous_evidence': 3}
- `random_small_vocab` expectation=chance_recurrence naive_failures=2/3 evidence_index_failures=3/3 len3_mean=0.150000 full_sequence_mean=0.150000 compressibility_mean=0.067460 history_accuracy_mean=0.158333 outcome_purity_max_mean=0.500000 failure_modes={'chance_full_sequence_recurrence_overcompressed': 2} evidence_failure_modes={'chance_subsequence_promoted_as_resolved': 3, 'chance_full_sequence_promoted_as_resolved': 3} len3_index_statuses={'episode_template_index': 12, 'ambiguous_evidence': 1} full_index_statuses={'episode_template_index': 12, 'ambiguous_evidence': 1}
- `uniform_branching` expectation=high_branch_entropy naive_failures=0/3 evidence_index_failures=0/3 len3_mean=0.755555 full_sequence_mean=0.755555 compressibility_mean=0.329659 history_accuracy_mean=0.185185 outcome_purity_max_mean=0.888889 failure_modes={'low_predictive_utility': 3} evidence_failure_modes={} len3_index_statuses={'ambiguous_evidence': 13, 'episode_template_index': 34} full_index_statuses={'ambiguous_evidence': 13, 'episode_template_index': 34}

### small length 5

- `unique_triplets` expectation=no_recurrence naive_failures=0/3 evidence_index_failures=0/3 len3_mean=0.000000 full_sequence_mean=0.000000 compressibility_mean=0.000000 history_accuracy_mean=0.000000 outcome_purity_max_mean=0.000000 failure_modes={} evidence_failure_modes={} len3_index_statuses={} full_index_statuses={}
- `shared_edges_unique_middle` expectation=partial_recurrence_only naive_failures=0/3 evidence_index_failures=0/3 len3_mean=0.000000 full_sequence_mean=0.000000 compressibility_mean=0.072890 history_accuracy_mean=0.000000 outcome_purity_max_mean=0.000000 failure_modes={} evidence_failure_modes={} len3_index_statuses={} full_index_statuses={}
- `near_miss_drift` expectation=partial_recurrence_only naive_failures=0/3 evidence_index_failures=0/3 len3_mean=0.000000 full_sequence_mean=0.000000 compressibility_mean=0.036457 history_accuracy_mean=0.000000 outcome_purity_max_mean=0.000000 failure_modes={} evidence_failure_modes={} len3_index_statuses={} full_index_statuses={}
- `hidden_novelty_alias_collision` expectation=hidden_novelty naive_failures=3/3 evidence_index_failures=0/3 len3_mean=1.000000 full_sequence_mean=1.000000 compressibility_mean=0.333333 history_accuracy_mean=1.000000 outcome_purity_max_mean=0.016667 failure_modes={'compressed_hidden_or_contradictory_novelty': 3, 'low_outcome_purity': 3} evidence_failure_modes={} len3_index_statuses={'ambiguous_evidence': 9} full_index_statuses={'ambiguous_evidence': 3}
- `contradictory_outcomes` expectation=outcome_contradiction naive_failures=3/3 evidence_index_failures=0/3 len3_mean=1.000000 full_sequence_mean=1.000000 compressibility_mean=0.333333 history_accuracy_mean=1.000000 outcome_purity_max_mean=0.150000 failure_modes={'compressed_hidden_or_contradictory_novelty': 3, 'low_outcome_purity': 3} evidence_failure_modes={} len3_index_statuses={'ambiguous_evidence': 9} full_index_statuses={'ambiguous_evidence': 3}
- `random_small_vocab` expectation=chance_recurrence naive_failures=0/3 evidence_index_failures=3/3 len3_mean=0.298148 full_sequence_mean=0.000000 compressibility_mean=0.111569 history_accuracy_mean=0.098019 outcome_purity_max_mean=0.722222 failure_modes={} evidence_failure_modes={'chance_subsequence_promoted_as_resolved': 3} len3_index_statuses={'ambiguous_evidence': 7, 'branching_fragment': 5, 'retrieval_index': 64} full_index_statuses={}
- `uniform_branching` expectation=high_branch_entropy naive_failures=0/3 evidence_index_failures=0/3 len3_mean=0.411111 full_sequence_mean=0.000000 compressibility_mean=0.167815 history_accuracy_mean=0.116983 outcome_purity_max_mean=0.833333 failure_modes={'low_predictive_utility': 3} evidence_failure_modes={} len3_index_statuses={'ambiguous_evidence': 19, 'branching_fragment': 23, 'retrieval_index': 49} full_index_statuses={}

### small length 8

- `unique_triplets` expectation=no_recurrence naive_failures=0/3 evidence_index_failures=0/3 len3_mean=0.000000 full_sequence_mean=0.000000 compressibility_mean=0.000000 history_accuracy_mean=0.000000 outcome_purity_max_mean=0.000000 failure_modes={} evidence_failure_modes={} len3_index_statuses={} full_index_statuses={}
- `shared_edges_unique_middle` expectation=partial_recurrence_only naive_failures=0/3 evidence_index_failures=0/3 len3_mean=0.000000 full_sequence_mean=0.000000 compressibility_mean=0.041949 history_accuracy_mean=0.000000 outcome_purity_max_mean=0.000000 failure_modes={} evidence_failure_modes={} len3_index_statuses={} full_index_statuses={}
- `near_miss_drift` expectation=partial_recurrence_only naive_failures=0/3 evidence_index_failures=0/3 len3_mean=0.000000 full_sequence_mean=0.000000 compressibility_mean=0.020997 history_accuracy_mean=0.000000 outcome_purity_max_mean=0.000000 failure_modes={} evidence_failure_modes={} len3_index_statuses={} full_index_statuses={}
- `hidden_novelty_alias_collision` expectation=hidden_novelty naive_failures=3/3 evidence_index_failures=0/3 len3_mean=1.000000 full_sequence_mean=1.000000 compressibility_mean=0.333333 history_accuracy_mean=1.000000 outcome_purity_max_mean=0.016667 failure_modes={'compressed_hidden_or_contradictory_novelty': 3, 'low_outcome_purity': 3} evidence_failure_modes={} len3_index_statuses={'ambiguous_evidence': 18} full_index_statuses={'ambiguous_evidence': 3}
- `contradictory_outcomes` expectation=outcome_contradiction naive_failures=3/3 evidence_index_failures=0/3 len3_mean=1.000000 full_sequence_mean=1.000000 compressibility_mean=0.333333 history_accuracy_mean=1.000000 outcome_purity_max_mean=0.150000 failure_modes={'compressed_hidden_or_contradictory_novelty': 3, 'low_outcome_purity': 3} evidence_failure_modes={} len3_index_statuses={'ambiguous_evidence': 18} full_index_statuses={'ambiguous_evidence': 3}
- `random_small_vocab` expectation=chance_recurrence naive_failures=3/3 evidence_index_failures=3/3 len3_mean=0.524074 full_sequence_mean=0.000000 compressibility_mean=0.182812 history_accuracy_mean=0.146296 outcome_purity_max_mean=0.722222 failure_modes={'chance_subsequence_recurrence_overcompressed': 3} evidence_failure_modes={'chance_subsequence_promoted_as_resolved': 3} len3_index_statuses={'ambiguous_evidence': 51, 'branching_fragment': 5, 'retrieval_index': 197} full_index_statuses={}
- `uniform_branching` expectation=high_branch_entropy naive_failures=0/3 evidence_index_failures=0/3 len3_mean=0.539815 full_sequence_mean=0.000000 compressibility_mean=0.193221 history_accuracy_mean=0.182497 outcome_purity_max_mean=1.000000 failure_modes={'low_predictive_utility': 3} evidence_failure_modes={} len3_index_statuses={'ambiguous_evidence': 62, 'branching_fragment': 8, 'retrieval_index': 174} full_index_statuses={}

### scaled length 3

- `unique_triplets` expectation=no_recurrence naive_failures=0/3 evidence_index_failures=0/3 len3_mean=0.000000 full_sequence_mean=0.000000 compressibility_mean=0.000000 history_accuracy_mean=0.000000 outcome_purity_max_mean=0.000000 failure_modes={} evidence_failure_modes={} len3_index_statuses={} full_index_statuses={}
- `shared_edges_unique_middle` expectation=partial_recurrence_only naive_failures=0/3 evidence_index_failures=0/3 len3_mean=0.000000 full_sequence_mean=0.000000 compressibility_mean=0.165063 history_accuracy_mean=0.000000 outcome_purity_max_mean=0.000000 failure_modes={} evidence_failure_modes={} len3_index_statuses={} full_index_statuses={}
- `near_miss_drift` expectation=partial_recurrence_only naive_failures=0/3 evidence_index_failures=0/3 len3_mean=0.000000 full_sequence_mean=0.000000 compressibility_mean=0.081216 history_accuracy_mean=0.000000 outcome_purity_max_mean=0.000000 failure_modes={} evidence_failure_modes={} len3_index_statuses={} full_index_statuses={}
- `hidden_novelty_alias_collision` expectation=hidden_novelty naive_failures=3/3 evidence_index_failures=0/3 len3_mean=1.000000 full_sequence_mean=1.000000 compressibility_mean=0.333333 history_accuracy_mean=1.000000 outcome_purity_max_mean=0.001667 failure_modes={'compressed_hidden_or_contradictory_novelty': 3, 'low_outcome_purity': 3} evidence_failure_modes={} len3_index_statuses={'ambiguous_evidence': 3} full_index_statuses={'ambiguous_evidence': 3}
- `contradictory_outcomes` expectation=outcome_contradiction naive_failures=3/3 evidence_index_failures=0/3 len3_mean=1.000000 full_sequence_mean=1.000000 compressibility_mean=0.333333 history_accuracy_mean=1.000000 outcome_purity_max_mean=0.041667 failure_modes={'compressed_hidden_or_contradictory_novelty': 3, 'low_outcome_purity': 3} evidence_failure_modes={} len3_index_statuses={'ambiguous_evidence': 3} full_index_statuses={'ambiguous_evidence': 3}
- `random_small_vocab` expectation=chance_recurrence naive_failures=3/3 evidence_index_failures=3/3 len3_mean=0.677778 full_sequence_mean=0.677778 compressibility_mean=0.228645 history_accuracy_mean=0.114815 outcome_purity_max_mean=0.500000 failure_modes={'chance_subsequence_recurrence_overcompressed': 3, 'chance_full_sequence_recurrence_overcompressed': 3} evidence_failure_modes={'chance_subsequence_promoted_as_resolved': 3, 'chance_full_sequence_promoted_as_resolved': 3} len3_index_statuses={'ambiguous_evidence': 181, 'episode_template_index': 312} full_index_statuses={'ambiguous_evidence': 181, 'episode_template_index': 312}
- `uniform_branching` expectation=high_branch_entropy naive_failures=0/3 evidence_index_failures=0/3 len3_mean=1.000000 full_sequence_mean=1.000000 compressibility_mean=0.402493 history_accuracy_mean=0.142593 outcome_purity_max_mean=0.542592 failure_modes={'low_predictive_utility': 3} evidence_failure_modes={} len3_index_statuses={'ambiguous_evidence': 105, 'episode_template_index': 3} full_index_statuses={'ambiguous_evidence': 105, 'episode_template_index': 3}

### scaled length 5

- `unique_triplets` expectation=no_recurrence naive_failures=0/3 evidence_index_failures=0/3 len3_mean=0.000000 full_sequence_mean=0.000000 compressibility_mean=0.000000 history_accuracy_mean=0.000000 outcome_purity_max_mean=0.000000 failure_modes={} evidence_failure_modes={} len3_index_statuses={} full_index_statuses={}
- `shared_edges_unique_middle` expectation=partial_recurrence_only naive_failures=0/3 evidence_index_failures=0/3 len3_mean=0.000000 full_sequence_mean=0.000000 compressibility_mean=0.091110 history_accuracy_mean=0.000000 outcome_purity_max_mean=0.000000 failure_modes={} evidence_failure_modes={} len3_index_statuses={} full_index_statuses={}
- `near_miss_drift` expectation=partial_recurrence_only naive_failures=0/3 evidence_index_failures=0/3 len3_mean=0.000000 full_sequence_mean=0.000000 compressibility_mean=0.045251 history_accuracy_mean=0.000000 outcome_purity_max_mean=0.000000 failure_modes={} evidence_failure_modes={} len3_index_statuses={} full_index_statuses={}
- `hidden_novelty_alias_collision` expectation=hidden_novelty naive_failures=3/3 evidence_index_failures=0/3 len3_mean=1.000000 full_sequence_mean=1.000000 compressibility_mean=0.333333 history_accuracy_mean=1.000000 outcome_purity_max_mean=0.001667 failure_modes={'compressed_hidden_or_contradictory_novelty': 3, 'low_outcome_purity': 3} evidence_failure_modes={} len3_index_statuses={'ambiguous_evidence': 9} full_index_statuses={'ambiguous_evidence': 3}
- `contradictory_outcomes` expectation=outcome_contradiction naive_failures=3/3 evidence_index_failures=0/3 len3_mean=1.000000 full_sequence_mean=1.000000 compressibility_mean=0.333333 history_accuracy_mean=1.000000 outcome_purity_max_mean=0.041667 failure_modes={'compressed_hidden_or_contradictory_novelty': 3, 'low_outcome_purity': 3} evidence_failure_modes={} len3_index_statuses={'ambiguous_evidence': 9} full_index_statuses={'ambiguous_evidence': 3}
- `random_small_vocab` expectation=chance_recurrence naive_failures=3/3 evidence_index_failures=3/3 len3_mean=0.970370 full_sequence_mean=0.017778 compressibility_mean=0.324803 history_accuracy_mean=0.124074 outcome_purity_max_mean=0.500000 failure_modes={'chance_subsequence_recurrence_overcompressed': 3} evidence_failure_modes={'chance_full_sequence_promoted_as_resolved': 3} len3_index_statuses={'ambiguous_evidence': 1049, 'background_recurrence': 282} full_index_statuses={'episode_template_index': 16}
- `uniform_branching` expectation=high_branch_entropy naive_failures=0/3 evidence_index_failures=0/3 len3_mean=0.958334 full_sequence_mean=0.360000 compressibility_mean=0.344700 history_accuracy_mean=0.157407 outcome_purity_max_mean=1.000000 failure_modes={'low_predictive_utility': 3} evidence_failure_modes={} len3_index_statuses={'ambiguous_evidence': 618, 'branching_fragment': 307, 'retrieval_index': 175} full_index_statuses={'ambiguous_evidence': 28, 'episode_template_index': 273}

### scaled length 8

- `unique_triplets` expectation=no_recurrence naive_failures=0/3 evidence_index_failures=0/3 len3_mean=0.000000 full_sequence_mean=0.000000 compressibility_mean=0.000000 history_accuracy_mean=0.000000 outcome_purity_max_mean=0.000000 failure_modes={} evidence_failure_modes={} len3_index_statuses={} full_index_statuses={}
- `shared_edges_unique_middle` expectation=partial_recurrence_only naive_failures=0/3 evidence_index_failures=0/3 len3_mean=0.000000 full_sequence_mean=0.000000 compressibility_mean=0.053408 history_accuracy_mean=0.000000 outcome_purity_max_mean=0.000000 failure_modes={} evidence_failure_modes={} len3_index_statuses={} full_index_statuses={}
- `near_miss_drift` expectation=partial_recurrence_only naive_failures=0/3 evidence_index_failures=0/3 len3_mean=0.000000 full_sequence_mean=0.000000 compressibility_mean=0.026622 history_accuracy_mean=0.000000 outcome_purity_max_mean=0.000000 failure_modes={} evidence_failure_modes={} len3_index_statuses={} full_index_statuses={}
- `hidden_novelty_alias_collision` expectation=hidden_novelty naive_failures=3/3 evidence_index_failures=0/3 len3_mean=1.000000 full_sequence_mean=1.000000 compressibility_mean=0.333333 history_accuracy_mean=1.000000 outcome_purity_max_mean=0.001667 failure_modes={'compressed_hidden_or_contradictory_novelty': 3, 'low_outcome_purity': 3} evidence_failure_modes={} len3_index_statuses={'ambiguous_evidence': 18} full_index_statuses={'ambiguous_evidence': 3}
- `contradictory_outcomes` expectation=outcome_contradiction naive_failures=3/3 evidence_index_failures=0/3 len3_mean=1.000000 full_sequence_mean=1.000000 compressibility_mean=0.333333 history_accuracy_mean=1.000000 outcome_purity_max_mean=0.041667 failure_modes={'compressed_hidden_or_contradictory_novelty': 3, 'low_outcome_purity': 3} evidence_failure_modes={} len3_index_statuses={'ambiguous_evidence': 18} full_index_statuses={'ambiguous_evidence': 3}
- `random_small_vocab` expectation=chance_recurrence naive_failures=3/3 evidence_index_failures=0/3 len3_mean=0.999074 full_sequence_mean=0.000000 compressibility_mean=0.333886 history_accuracy_mean=0.134259 outcome_purity_max_mean=0.555556 failure_modes={'chance_subsequence_recurrence_overcompressed': 3} evidence_failure_modes={} len3_index_statuses={'ambiguous_evidence': 1490, 'background_recurrence': 35} full_index_statuses={}
- `uniform_branching` expectation=high_branch_entropy naive_failures=0/3 evidence_index_failures=0/3 len3_mean=0.998889 full_sequence_mean=0.002222 compressibility_mean=0.338764 history_accuracy_mean=0.173457 outcome_purity_max_mean=0.777778 failure_modes={'low_predictive_utility': 3} evidence_failure_modes={} len3_index_statuses={'ambiguous_evidence': 1331, 'background_recurrence': 1, 'branching_fragment': 9, 'retrieval_index': 48} full_index_statuses={'episode_template_index': 2}

## Failure Interpretation

- `hidden_novelty_alias_collision` is an information-theoretic failure: if distinct latent episodes project to the same event identity, the current representation compresses them as one motif.
- `contradictory_outcomes` shows that recurrence alone is insufficient; a motif can be structurally stable while carrying low outcome purity.
- `random_small_vocab` attacks support-count novelty gating. At scale, chance recurrence becomes expected and support >= 2 is not a sufficient motif criterion.
- `shared_edges_unique_middle` and `near_miss_drift` check whether partial overlap is incorrectly promoted to full length-3 recurrence.
- `unique_triplets` remains the clean hostile control: any length-3 recurrence there is invented by the representation itself.

## Layer Decomposition

### small length 3

| case | event redundancy | transition redundancy | repeated episodes | length-3 recurrence | full-sequence recurrence | outcome purity max | history accuracy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `unique_triplets` | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| `shared_edges_unique_middle` | 0.403122 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| `near_miss_drift` | 0.201763 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| `hidden_novelty_alias_collision` | 0.000000 | 0.000000 | 1.000000 | 1.000000 | 1.000000 | 0.016667 | 1.000000 |
| `contradictory_outcomes` | 0.000000 | 0.000000 | 1.000000 | 1.000000 | 1.000000 | 0.150000 | 1.000000 |
| `random_small_vocab` | 0.014520 | 0.037861 | 0.150000 | 0.150000 | 0.150000 | 0.500000 | 0.158333 |
| `uniform_branching` | 0.120885 | 0.112538 | 0.755555 | 0.755555 | 0.755555 | 0.888889 | 0.185185 |

### small length 5

| case | event redundancy | transition redundancy | repeated episodes | length-3 recurrence | full-sequence recurrence | outcome purity max | history accuracy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `unique_triplets` | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| `shared_edges_unique_middle` | 0.218670 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| `near_miss_drift` | 0.109372 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| `hidden_novelty_alias_collision` | 0.000000 | 0.000000 | 1.000000 | 1.000000 | 1.000000 | 0.016667 | 1.000000 |
| `contradictory_outcomes` | 0.000000 | 0.000000 | 1.000000 | 1.000000 | 1.000000 | 0.150000 | 1.000000 |
| `random_small_vocab` | 0.006179 | 0.030380 | 0.000000 | 0.298148 | 0.000000 | 0.722222 | 0.098019 |
| `uniform_branching` | 0.036532 | 0.055804 | 0.000000 | 0.411111 | 0.000000 | 0.833333 | 0.116983 |

### small length 8

| case | event redundancy | transition redundancy | repeated episodes | length-3 recurrence | full-sequence recurrence | outcome purity max | history accuracy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `unique_triplets` | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| `shared_edges_unique_middle` | 0.125847 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| `near_miss_drift` | 0.062992 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| `hidden_novelty_alias_collision` | 0.000000 | 0.000000 | 1.000000 | 1.000000 | 1.000000 | 0.016667 | 1.000000 |
| `contradictory_outcomes` | 0.000000 | 0.000000 | 1.000000 | 1.000000 | 1.000000 | 0.150000 | 1.000000 |
| `random_small_vocab` | 0.004533 | 0.019830 | 0.000000 | 0.524074 | 0.000000 | 0.722222 | 0.146296 |
| `uniform_branching` | 0.013421 | 0.026427 | 0.000000 | 0.539815 | 0.000000 | 1.000000 | 0.182497 |

### scaled length 3

| case | event redundancy | transition redundancy | repeated episodes | length-3 recurrence | full-sequence recurrence | outcome purity max | history accuracy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `unique_triplets` | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| `shared_edges_unique_middle` | 0.495189 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| `near_miss_drift` | 0.243647 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| `hidden_novelty_alias_collision` | 0.000000 | 0.000000 | 1.000000 | 1.000000 | 1.000000 | 0.001667 | 1.000000 |
| `contradictory_outcomes` | 0.000000 | 0.000000 | 1.000000 | 1.000000 | 1.000000 | 0.041667 | 1.000000 |
| `random_small_vocab` | 0.001208 | 0.006950 | 0.677778 | 0.677778 | 0.677778 | 0.500000 | 0.114815 |
| `uniform_branching` | 0.107429 | 0.100050 | 1.000000 | 1.000000 | 1.000000 | 0.542592 | 0.142593 |

### scaled length 5

| case | event redundancy | transition redundancy | repeated episodes | length-3 recurrence | full-sequence recurrence | outcome purity max | history accuracy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `unique_triplets` | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| `shared_edges_unique_middle` | 0.273330 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| `near_miss_drift` | 0.135754 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| `hidden_novelty_alias_collision` | 0.000000 | 0.000000 | 1.000000 | 1.000000 | 1.000000 | 0.001667 | 1.000000 |
| `contradictory_outcomes` | 0.000000 | 0.000000 | 1.000000 | 1.000000 | 1.000000 | 0.041667 | 1.000000 |
| `random_small_vocab` | 0.000641 | 0.003397 | 0.017778 | 0.970370 | 0.017778 | 0.500000 | 0.124074 |
| `uniform_branching` | 0.030623 | 0.045144 | 0.360000 | 0.958334 | 0.360000 | 1.000000 | 0.157407 |

### scaled length 8

| case | event redundancy | transition redundancy | repeated episodes | length-3 recurrence | full-sequence recurrence | outcome purity max | history accuracy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `unique_triplets` | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| `shared_edges_unique_middle` | 0.160223 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| `near_miss_drift` | 0.079865 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 | 0.000000 |
| `hidden_novelty_alias_collision` | 0.000000 | 0.000000 | 1.000000 | 1.000000 | 1.000000 | 0.001667 | 1.000000 |
| `contradictory_outcomes` | 0.000000 | 0.000000 | 1.000000 | 1.000000 | 1.000000 | 0.041667 | 1.000000 |
| `random_small_vocab` | 0.000470 | 0.002115 | 0.000000 | 0.999074 | 0.000000 | 0.555556 | 0.134259 |
| `uniform_branching` | 0.009481 | 0.007921 | 0.002222 | 0.998889 | 0.002222 | 0.777778 | 0.173457 |

## Sequence-Length Effects

### small

| case | len3 recurrence at 3/5/8 | full recurrence at 3/5/8 |
| --- | --- | --- |
| `unique_triplets` | 0.000000 / 0.000000 / 0.000000 | 0.000000 / 0.000000 / 0.000000 |
| `shared_edges_unique_middle` | 0.000000 / 0.000000 / 0.000000 | 0.000000 / 0.000000 / 0.000000 |
| `near_miss_drift` | 0.000000 / 0.000000 / 0.000000 | 0.000000 / 0.000000 / 0.000000 |
| `hidden_novelty_alias_collision` | 1.000000 / 1.000000 / 1.000000 | 1.000000 / 1.000000 / 1.000000 |
| `contradictory_outcomes` | 1.000000 / 1.000000 / 1.000000 | 1.000000 / 1.000000 / 1.000000 |
| `random_small_vocab` | 0.150000 / 0.298148 / 0.524074 | 0.150000 / 0.000000 / 0.000000 |
| `uniform_branching` | 0.755555 / 0.411111 / 0.539815 | 0.755555 / 0.000000 / 0.000000 |

### scaled

| case | len3 recurrence at 3/5/8 | full recurrence at 3/5/8 |
| --- | --- | --- |
| `unique_triplets` | 0.000000 / 0.000000 / 0.000000 | 0.000000 / 0.000000 / 0.000000 |
| `shared_edges_unique_middle` | 0.000000 / 0.000000 / 0.000000 | 0.000000 / 0.000000 / 0.000000 |
| `near_miss_drift` | 0.000000 / 0.000000 / 0.000000 | 0.000000 / 0.000000 / 0.000000 |
| `hidden_novelty_alias_collision` | 1.000000 / 1.000000 / 1.000000 | 1.000000 / 1.000000 / 1.000000 |
| `contradictory_outcomes` | 1.000000 / 1.000000 / 1.000000 | 1.000000 / 1.000000 / 1.000000 |
| `random_small_vocab` | 0.677778 / 0.970370 / 0.999074 | 0.677778 / 0.017778 / 0.000000 |
| `uniform_branching` | 1.000000 / 0.958334 / 0.998889 | 1.000000 / 0.360000 / 0.002222 |

## Scale Effects

- `unique_triplets` length3_delta=0.000000 compressibility_delta=0.000000
- `shared_edges_unique_middle` length3_delta=0.000000 compressibility_delta=0.030689
- `near_miss_drift` length3_delta=0.000000 compressibility_delta=0.013962
- `hidden_novelty_alias_collision` length3_delta=0.000000 compressibility_delta=0.000000
- `contradictory_outcomes` length3_delta=0.000000 compressibility_delta=0.000000
- `random_small_vocab` length3_delta=0.527778 compressibility_delta=0.161185
- `uniform_branching` length3_delta=0.244445 compressibility_delta=0.072833
