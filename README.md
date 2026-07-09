# Ecphory

Event-first memory experiments for testing whether repeated imperfect event observations consolidate into stable reusable temporal motifs.

The current prototype asks a narrow question:

> Can an event-first hierarchy preserve reusable temporal structure more reliably than exact event recovery alone?

## Core Result

The strongest current metric is **Representation Gain**:

```text
Representation Gain =
  canonical length-3 motif support fraction
  - exact canonical motif recovery
```

Positive gain means recurrence across episodes concentrates support around canonical temporal motifs beyond what exact event recovery predicts.

In the useful regimes, Representation Gain is positive. In the over-entropic union detector regime, it is negative. Null controls collapse or sharply reduce the gain.

That supports the bounded claim:

```text
too little recall             -> undercapture
too much candidate entropy    -> negative Representation Gain
stable imperfect recurrence   -> positive Representation Gain
```

## Pipeline

```text
raw signals
  -> event detector
  -> discrete event decoder
  -> event transitions
  -> episodes
  -> motifs
  -> static projections only afterward
```

The detector and event identity are intentionally separated. Detectors produce candidate event envelopes. Decoders canonicalize event identity. Motifs are mined afterward as recurring temporal structure.

## Run

```bash
python -m pip install -r requirements.txt
python event_graph_experiment.py --motif-fault-tolerance-sweep
python event_graph_experiment.py --null-ablation-package
```

Important experiment modes:

```bash
python event_graph_experiment.py --dropout-spurious-pareto
python event_graph_experiment.py --temporal-decoder-seed-sweep
python event_graph_experiment.py --motif-fault-tolerance-sweep
python event_graph_experiment.py --null-ablation-package
```

## Key Artifacts

- `event_graph_experiment.py`: synthetic signal generation, detectors, decoders, motif mining, nulls, and reports.
- `docs/ldgr-research-methodology.md`: falsification-first methodology.
- `docs/detector-interface-hypothesis.md`: detector/representation interface framing.
- `outputs/representation_gain_findings.md`: Representation Gain summary.
- `outputs/motif_fault_tolerance_findings.md`: motif-layer fault tolerance results.
- `outputs/null_ablation_findings.md`: stronger nulls and hierarchy ablations.
- `outputs/null_ablation_package.csv`: raw null/ablation metrics.
- `outputs/motif_fault_tolerance_sweep.csv`: raw Representation Gain and motif support metrics.

## Current Interpretation

This is not a claim about general machine knowledge.

The current claim is narrower:

> Under controlled combined dropout and spurious corruption, an event-first hierarchy can concentrate recurring motif support beyond exact event recovery, provided the detector produces a stable but imperfect event stream rather than an over-entropic candidate envelope.

The hierarchy appears to act like an error-correcting mechanism at the representation level, but no coding-theoretic model is claimed yet.
