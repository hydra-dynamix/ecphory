from __future__ import annotations

import argparse
import csv
import json
import math
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from statistics import mean
from typing import Iterable

import networkx as nx
import numpy as np


UnitId = str
EventLabel = str


@dataclass(frozen=True)
class RawSignal:
    unit_id: UnitId
    t: int
    value: float
    episode_id: str
    context: str


@dataclass(frozen=True)
class Event:
    event_id: str
    episode_id: str
    t_start: int
    t_end: int
    participants: tuple[UnitId, ...]
    intensities: dict[UnitId, float]
    context: str
    source_window: str
    outcome: str

    @property
    def label(self) -> EventLabel:
        return event_label(self.participants)


@dataclass(frozen=True)
class Transition:
    from_event: str
    to_event: str
    delta_t: int
    shared_participants: tuple[UnitId, ...]
    changed_participants: tuple[UnitId, ...]
    weight: int
    episode_id: str
    context: str
    from_label: EventLabel
    to_label: EventLabel


@dataclass(frozen=True)
class Episode:
    episode_id: str
    context: str
    outcome: str
    ordered_events: tuple[str, ...]


@dataclass(frozen=True)
class Motif:
    pattern: tuple[EventLabel, ...]
    support: int
    variants: tuple[str, ...]
    predicted_next_events: tuple[str, ...]
    contexts: tuple[str, ...]
    outcomes: tuple[str, ...]


@dataclass(frozen=True)
class PatternEvidence:
    pattern: tuple[EventLabel, ...]
    support: int
    expected_support: float
    lift: float
    context_entropy_bits: float
    outcome_entropy_bits: float
    context_purity: float
    outcome_purity: float
    next_entropy_bits: float
    next_purity: float
    evidence_episode_ids: tuple[str, ...]
    contexts: tuple[str, ...]
    outcomes: tuple[str, ...]
    predicted_next_events: tuple[str, ...]
    index_status: str
    index_reason: str


@dataclass(frozen=True)
class LayerLoss:
    from_layer: str
    to_layer: str
    metric: str
    value: float
    interpretation: str


@dataclass(frozen=True)
class InformationEnvelope:
    layer: str
    measure: str
    value: float
    interpretation: str


@dataclass(frozen=True)
class ExperimentResult:
    raw_signals: list[RawSignal]
    events: list[Event]
    transitions: list[Transition]
    episodes: list[Episode]
    motifs: list[Motif]
    metrics: dict[str, float | int]
    layer_losses: list[LayerLoss]
    information_envelope: list[InformationEnvelope]


@dataclass(frozen=True)
class SweepCase:
    case_id: str
    axis: str
    parameter: str
    value: float
    event_duration: int
    event_gap: int
    window_size: int
    activation_threshold: float
    noise_episodes: int
    min_participants: int
    active_mean: float
    active_std: float
    baseline_mean: float
    baseline_std: float
    dropout_probability: float
    spurious_probability: float


def event_label(participants: Iterable[UnitId]) -> EventLabel:
    return "{" + ",".join(sorted(participants)) + "}"


def shannon_entropy(counter: Counter[object]) -> float:
    total = sum(counter.values())
    if total == 0:
        return 0.0
    entropy = 0.0
    for count in counter.values():
        probability = count / total
        entropy -= probability * math.log2(probability)
    return entropy


def generate_synthetic_signals(
    rng: np.random.Generator,
    motif_repetitions: int,
    noise_episodes: int,
    event_duration: int,
    event_gap: int,
    active_mean: float,
    active_std: float,
    baseline_mean: float,
    baseline_std: float,
    world: str,
    dropout_probability: float,
    spurious_probability: float,
) -> tuple[list[RawSignal], list[dict[str, str]]]:
    units = tuple(f"U{index:02d}" for index in range(40)) if world == "hostile_unique" else tuple("ABCDEFGH")
    if world == "branch":
        motifs: tuple[tuple[str, str, tuple[tuple[str, ...], ...], str], ...] = (
            ("motif_1", "X", (("A", "B"), ("B", "C"), ("C", "D")), "Y1"),
            ("motif_2", "Z", (("A", "B"), ("B", "E"), ("E", "F")), "Y2"),
        )
    elif world == "overlap":
        motifs = (
            ("motif_1", "X", (("A", "B"), ("B", "C"), ("E", "F")), "Y1"),
            ("motif_2", "Z", (("A", "B"), ("B", "E"), ("E", "F")), "Y2"),
            ("motif_3", "W", (("A", "B"), ("B", "G"), ("E", "F")), "Y3"),
        )
    elif world != "hostile_unique":
        raise ValueError(f"unknown synthetic world: {world}")
    raw_signals: list[RawSignal] = []
    episode_specs: list[dict[str, str]] = []
    episode_index = 0
    base_t = 0

    def append_episode(
        motif_id: str,
        context: str,
        events: tuple[tuple[str, ...], ...],
        outcome: str,
    ) -> None:
        nonlocal episode_index, base_t
        episode_id = f"episode_{episode_index:04d}"
        episode_specs.append(
            {
                "episode_id": episode_id,
                "motif_id": motif_id,
                "context": context,
                "outcome": outcome,
            }
        )
        episode_start = base_t
        episode_end = episode_start + len(events) * (event_duration + event_gap)
        event_starts = [
            episode_start + index * (event_duration + event_gap)
            for index in range(len(events))
        ]

        active_by_t: dict[int, tuple[str, ...]] = {}
        for event_index, participants in enumerate(events):
            event_start = event_starts[event_index]
            for offset in range(event_duration):
                active_by_t[event_start + offset] = participants

        for t in range(episode_start, episode_end):
            active_units = set(active_by_t.get(t, ()))
            for unit_id in units:
                baseline = float(rng.normal(baseline_mean, baseline_std))
                value = baseline
                if unit_id in active_units:
                    if rng.random() >= dropout_probability:
                        value = float(rng.normal(active_mean, active_std))
                elif rng.random() < spurious_probability:
                    value = float(rng.normal(active_mean, active_std))
                raw_signals.append(
                    RawSignal(
                        unit_id=unit_id,
                        t=t,
                        value=max(0.0, value),
                        episode_id=episode_id,
                        context=context,
                    )
                )

        episode_index += 1
        base_t = episode_end + event_gap

    if world == "hostile_unique":
        pair_pool = [
            (left, right)
            for left_index, left in enumerate(units)
            for right in units[left_index + 1 :]
        ]
        rng.shuffle(pair_pool)
        total_episodes = motif_repetitions * 3 + noise_episodes
        required_pairs = total_episodes * 3
        if required_pairs > len(pair_pool):
            raise ValueError(
                f"hostile_unique needs {required_pairs} unique event labels, "
                f"but only {len(pair_pool)} are available"
            )
        for episode_number in range(total_episodes):
            events = tuple(pair_pool[episode_number * 3 : episode_number * 3 + 3])
            append_episode(
                motif_id=f"unique_{episode_number:04d}",
                context=f"CTX_{episode_number:04d}",
                events=events,
                outcome=f"OUT_{episode_number:04d}",
            )
        return raw_signals, episode_specs

    for repetition in range(motif_repetitions):
        ordered_motifs = list(motifs)
        rng.shuffle(ordered_motifs)
        for motif_id, context, events, outcome in ordered_motifs:
            append_episode(motif_id, context, events, outcome)

        if repetition < noise_episodes:
            noise_events = tuple(
                tuple(sorted(rng.choice(units, size=2, replace=False)))
                for _ in range(3)
            )
            append_episode("noise", "N", noise_events, "YN")

    return raw_signals, episode_specs


def detect_coactivation_events(
    raw_signals: list[RawSignal],
    episode_specs: list[dict[str, str]],
    window_size: int,
    activation_threshold: float,
    min_participants: int,
) -> list[Event]:
    by_episode: dict[str, list[RawSignal]] = defaultdict(list)
    spec_by_episode = {spec["episode_id"]: spec for spec in episode_specs}
    for signal in raw_signals:
        by_episode[signal.episode_id].append(signal)

    events: list[Event] = []
    event_index = 0

    for episode_id in sorted(by_episode):
        signals = by_episode[episode_id]
        values: dict[tuple[int, UnitId], float] = {
            (signal.t, signal.unit_id): signal.value for signal in signals
        }
        units = sorted({signal.unit_id for signal in signals})
        times = sorted({signal.t for signal in signals})
        if not times:
            continue

        active_windows: list[tuple[int, int, tuple[UnitId, ...], dict[UnitId, float]]] = []
        for t_start in range(min(times), max(times) - window_size + 2):
            intensities: dict[UnitId, float] = {}
            for unit_id in units:
                window_values = [
                    values.get((t, unit_id), 0.0)
                    for t in range(t_start, t_start + window_size)
                ]
                window_mean = mean(window_values)
                if window_mean >= activation_threshold:
                    intensities[unit_id] = window_mean
            if len(intensities) >= min_participants:
                participants = tuple(sorted(intensities))
                active_windows.append(
                    (t_start, t_start + window_size - 1, participants, intensities)
                )

        segment_start: int | None = None
        segment_end: int | None = None
        segment_participants: tuple[UnitId, ...] | None = None
        segment_intensities: dict[UnitId, list[float]] = defaultdict(list)

        def flush_segment() -> None:
            nonlocal event_index, segment_start, segment_end, segment_participants
            if (
                segment_start is None
                or segment_end is None
                or segment_participants is None
            ):
                return
            spec = spec_by_episode[episode_id]
            averaged_intensities = {
                unit_id: round(mean(segment_intensities[unit_id]), 4)
                for unit_id in segment_participants
            }
            event_id = f"event_{event_index:05d}"
            events.append(
                Event(
                    event_id=event_id,
                    episode_id=episode_id,
                    t_start=segment_start,
                    t_end=segment_end,
                    participants=segment_participants,
                    intensities=averaged_intensities,
                    context=spec["context"],
                    source_window=f"{segment_start}:{segment_end}",
                    outcome=spec["outcome"],
                )
            )
            event_index += 1
            segment_start = None
            segment_end = None
            segment_participants = None
            segment_intensities.clear()

        for t_start, t_end, participants, intensities in active_windows:
            contiguous = segment_end is not None and t_start <= segment_end + 1
            same_participants = participants == segment_participants
            if segment_participants is not None and (not contiguous or not same_participants):
                flush_segment()
            if segment_participants is None:
                segment_start = t_start
                segment_participants = participants
            segment_end = t_end
            for unit_id, intensity in intensities.items():
                segment_intensities[unit_id].append(intensity)
        flush_segment()

    return sorted(events, key=lambda event: (event.episode_id, event.t_start, event.event_id))


def detect_heu_like_coactivation_events(
    raw_signals: list[RawSignal],
    episode_specs: list[dict[str, str]],
    activation_threshold: float,
    min_participants: int,
    attack_rate: float,
    recovery_rate: float,
    leak_rate: float,
    commitment_threshold: float,
) -> list[Event]:
    by_episode: dict[str, list[RawSignal]] = defaultdict(list)
    spec_by_episode = {spec["episode_id"]: spec for spec in episode_specs}
    for signal in raw_signals:
        by_episode[signal.episode_id].append(signal)

    events: list[Event] = []
    event_index = 0

    for episode_id in sorted(by_episode):
        signals = by_episode[episode_id]
        values: dict[tuple[int, UnitId], float] = {
            (signal.t, signal.unit_id): signal.value for signal in signals
        }
        units = sorted({signal.unit_id for signal in signals})
        times = sorted({signal.t for signal in signals})
        if not times:
            continue

        envelopes = {unit_id: 0.0 for unit_id in units}
        active_points: list[tuple[int, int, tuple[UnitId, ...], dict[UnitId, float]]] = []

        for t in range(min(times), max(times) + 1):
            intensities: dict[UnitId, float] = {}
            for unit_id in units:
                raw_value = values.get((t, unit_id), 0.0)
                excitation = min(1.0, max(0.0, raw_value / activation_threshold))
                envelope = envelopes[unit_id]
                growth = attack_rate * excitation * (1.0 - envelope)
                recovery = recovery_rate * (1.0 - excitation) * envelope
                leak = leak_rate * envelope
                envelope = min(1.0, max(0.0, envelope + growth - recovery - leak))
                envelopes[unit_id] = envelope
                if envelope >= commitment_threshold:
                    intensities[unit_id] = envelope
            if len(intensities) >= min_participants:
                participants = tuple(sorted(intensities))
                active_points.append((t, t, participants, intensities))

        segment_start: int | None = None
        segment_end: int | None = None
        segment_participants: tuple[UnitId, ...] | None = None
        segment_intensities: dict[UnitId, list[float]] = defaultdict(list)

        def flush_segment() -> None:
            nonlocal event_index, segment_start, segment_end, segment_participants
            if (
                segment_start is None
                or segment_end is None
                or segment_participants is None
            ):
                return
            spec = spec_by_episode[episode_id]
            averaged_intensities = {
                unit_id: round(mean(segment_intensities[unit_id]), 4)
                for unit_id in segment_participants
            }
            event_id = f"event_{event_index:05d}"
            events.append(
                Event(
                    event_id=event_id,
                    episode_id=episode_id,
                    t_start=segment_start,
                    t_end=segment_end,
                    participants=segment_participants,
                    intensities=averaged_intensities,
                    context=spec["context"],
                    source_window=f"heu:{segment_start}:{segment_end}",
                    outcome=spec["outcome"],
                )
            )
            event_index += 1
            segment_start = None
            segment_end = None
            segment_participants = None
            segment_intensities.clear()

        for t_start, t_end, participants, intensities in active_points:
            contiguous = segment_end is not None and t_start <= segment_end + 1
            same_participants = participants == segment_participants
            if segment_participants is not None and (not contiguous or not same_participants):
                flush_segment()
            if segment_participants is None:
                segment_start = t_start
                segment_participants = participants
            segment_end = t_end
            for unit_id, intensity in intensities.items():
                segment_intensities[unit_id].append(intensity)
        flush_segment()

    return sorted(events, key=lambda event: (event.episode_id, event.t_start, event.event_id))


def detect_hysteresis_coactivation_events(
    raw_signals: list[RawSignal],
    episode_specs: list[dict[str, str]],
    activation_threshold: float,
    min_participants: int,
    off_threshold_ratio: float,
) -> list[Event]:
    by_episode: dict[str, list[RawSignal]] = defaultdict(list)
    spec_by_episode = {spec["episode_id"]: spec for spec in episode_specs}
    for signal in raw_signals:
        by_episode[signal.episode_id].append(signal)

    events: list[Event] = []
    event_index = 0
    off_threshold = activation_threshold * off_threshold_ratio

    for episode_id in sorted(by_episode):
        signals = by_episode[episode_id]
        values: dict[tuple[int, UnitId], float] = {
            (signal.t, signal.unit_id): signal.value for signal in signals
        }
        units = sorted({signal.unit_id for signal in signals})
        times = sorted({signal.t for signal in signals})
        if not times:
            continue

        active_units = {unit_id: False for unit_id in units}
        active_points: list[tuple[int, int, tuple[UnitId, ...], dict[UnitId, float]]] = []
        for t in range(min(times), max(times) + 1):
            intensities: dict[UnitId, float] = {}
            for unit_id in units:
                value = values.get((t, unit_id), 0.0)
                if active_units[unit_id]:
                    if value <= off_threshold:
                        active_units[unit_id] = False
                elif value >= activation_threshold:
                    active_units[unit_id] = True
                if active_units[unit_id]:
                    intensities[unit_id] = value
            if len(intensities) >= min_participants:
                participants = tuple(sorted(intensities))
                active_points.append((t, t, participants, intensities))

        segment_start: int | None = None
        segment_end: int | None = None
        segment_participants: tuple[UnitId, ...] | None = None
        segment_intensities: dict[UnitId, list[float]] = defaultdict(list)

        def flush_segment() -> None:
            nonlocal event_index, segment_start, segment_end, segment_participants
            if (
                segment_start is None
                or segment_end is None
                or segment_participants is None
            ):
                return
            spec = spec_by_episode[episode_id]
            averaged_intensities = {
                unit_id: round(mean(segment_intensities[unit_id]), 4)
                for unit_id in segment_participants
            }
            event_id = f"event_{event_index:05d}"
            events.append(
                Event(
                    event_id=event_id,
                    episode_id=episode_id,
                    t_start=segment_start,
                    t_end=segment_end,
                    participants=segment_participants,
                    intensities=averaged_intensities,
                    context=spec["context"],
                    source_window=f"hysteresis:{segment_start}:{segment_end}",
                    outcome=spec["outcome"],
                )
            )
            event_index += 1
            segment_start = None
            segment_end = None
            segment_participants = None
            segment_intensities.clear()

        for t_start, t_end, participants, intensities in active_points:
            contiguous = segment_end is not None and t_start <= segment_end + 1
            same_participants = participants == segment_participants
            if segment_participants is not None and (not contiguous or not same_participants):
                flush_segment()
            if segment_participants is None:
                segment_start = t_start
                segment_participants = participants
            segment_end = t_end
            for unit_id, intensity in intensities.items():
                segment_intensities[unit_id].append(intensity)
        flush_segment()

    return sorted(events, key=lambda event: (event.episode_id, event.t_start, event.event_id))


def detect_hybrid_state_window_events(
    raw_signals: list[RawSignal],
    episode_specs: list[dict[str, str]],
    activation_threshold: float,
    min_participants: int,
    attack_rate: float,
    recovery_rate: float,
    leak_rate: float,
    commitment_threshold: float,
    window_size: int,
    local_threshold_ratio: float,
) -> list[Event]:
    by_episode: dict[str, list[RawSignal]] = defaultdict(list)
    spec_by_episode = {spec["episode_id"]: spec for spec in episode_specs}
    for signal in raw_signals:
        by_episode[signal.episode_id].append(signal)

    events: list[Event] = []
    event_index = 0
    local_threshold = activation_threshold * local_threshold_ratio

    for episode_id in sorted(by_episode):
        signals = by_episode[episode_id]
        values: dict[tuple[int, UnitId], float] = {
            (signal.t, signal.unit_id): signal.value for signal in signals
        }
        units = sorted({signal.unit_id for signal in signals})
        times = sorted({signal.t for signal in signals})
        if not times:
            continue

        envelopes = {unit_id: 0.0 for unit_id in units}
        active_points: list[tuple[int, int, tuple[UnitId, ...], dict[UnitId, float]]] = []
        first_t = min(times)
        last_t = max(times)

        for t in range(first_t, last_t + 1):
            intensities: dict[UnitId, float] = {}
            for unit_id in units:
                raw_value = values.get((t, unit_id), 0.0)
                excitation = min(1.0, max(0.0, raw_value / activation_threshold))
                envelope = envelopes[unit_id]
                growth = attack_rate * excitation * (1.0 - envelope)
                recovery = recovery_rate * (1.0 - excitation) * envelope
                leak = leak_rate * envelope
                envelope = min(1.0, max(0.0, envelope + growth - recovery - leak))
                envelopes[unit_id] = envelope

                local_start = max(first_t, t - window_size + 1)
                local_values = [
                    values.get((local_t, unit_id), 0.0)
                    for local_t in range(local_start, t + 1)
                ]
                local_mean = mean(local_values)
                has_local_support = local_mean >= local_threshold
                if envelope >= commitment_threshold and has_local_support:
                    intensities[unit_id] = (envelope + min(1.0, local_mean)) / 2.0
            if len(intensities) >= min_participants:
                participants = tuple(sorted(intensities))
                active_points.append((t, t, participants, intensities))

        segment_start: int | None = None
        segment_end: int | None = None
        segment_participants: tuple[UnitId, ...] | None = None
        segment_intensities: dict[UnitId, list[float]] = defaultdict(list)

        def flush_segment() -> None:
            nonlocal event_index, segment_start, segment_end, segment_participants
            if (
                segment_start is None
                or segment_end is None
                or segment_participants is None
            ):
                return
            spec = spec_by_episode[episode_id]
            averaged_intensities = {
                unit_id: round(mean(segment_intensities[unit_id]), 4)
                for unit_id in segment_participants
            }
            event_id = f"event_{event_index:05d}"
            events.append(
                Event(
                    event_id=event_id,
                    episode_id=episode_id,
                    t_start=segment_start,
                    t_end=segment_end,
                    participants=segment_participants,
                    intensities=averaged_intensities,
                    context=spec["context"],
                    source_window=f"hybrid:{segment_start}:{segment_end}",
                    outcome=spec["outcome"],
                )
            )
            event_index += 1
            segment_start = None
            segment_end = None
            segment_participants = None
            segment_intensities.clear()

        for t_start, t_end, participants, intensities in active_points:
            contiguous = segment_end is not None and t_start <= segment_end + 1
            same_participants = participants == segment_participants
            if segment_participants is not None and (not contiguous or not same_participants):
                flush_segment()
            if segment_participants is None:
                segment_start = t_start
                segment_participants = participants
            segment_end = t_end
            for unit_id, intensity in intensities.items():
                segment_intensities[unit_id].append(intensity)
        flush_segment()

    return sorted(events, key=lambda event: (event.episode_id, event.t_start, event.event_id))


def merge_detector_events(
    event_sets: list[tuple[str, list[Event]]],
) -> list[Event]:
    merged_events: list[Event] = []

    def intervals_touch(left_event: Event, right_event: Event) -> bool:
        return (
            left_event.episode_id == right_event.episode_id
            and left_event.participants == right_event.participants
            and left_event.t_start <= right_event.t_end + 1
            and right_event.t_start <= left_event.t_end + 1
        )

    for detector_name, detector_events in event_sets:
        for event in sorted(
            detector_events,
            key=lambda item: (item.episode_id, item.t_start, item.t_end, item.participants),
        ):
            matching_index: int | None = None
            for candidate_index, candidate_event in enumerate(merged_events):
                if intervals_touch(candidate_event, event):
                    matching_index = candidate_index
                    break

            source_window = f"{detector_name}:{event.source_window}"
            if matching_index is None:
                merged_events.append(
                    Event(
                        event_id=event.event_id,
                        episode_id=event.episode_id,
                        t_start=event.t_start,
                        t_end=event.t_end,
                        participants=event.participants,
                        intensities=event.intensities,
                        context=event.context,
                        source_window=source_window,
                        outcome=event.outcome,
                    )
                )
                continue

            previous_event = merged_events[matching_index]
            averaged_intensities = {}
            for unit_id in previous_event.participants:
                averaged_intensities[unit_id] = round(
                    mean(
                        [
                            previous_event.intensities.get(unit_id, 0.0),
                            event.intensities.get(unit_id, 0.0),
                        ]
                    ),
                    4,
                )
            merged_events[matching_index] = Event(
                event_id=previous_event.event_id,
                episode_id=previous_event.episode_id,
                t_start=min(previous_event.t_start, event.t_start),
                t_end=max(previous_event.t_end, event.t_end),
                participants=previous_event.participants,
                intensities=averaged_intensities,
                context=previous_event.context,
                source_window=f"{previous_event.source_window}|{source_window}",
                outcome=previous_event.outcome,
            )

    renumbered_events = []
    for event_index, event in enumerate(
        sorted(merged_events, key=lambda item: (item.episode_id, item.t_start, item.t_end, item.participants))
    ):
        renumbered_events.append(
            Event(
                event_id=f"event_{event_index:05d}",
                episode_id=event.episode_id,
                t_start=event.t_start,
                t_end=event.t_end,
                participants=event.participants,
                intensities=event.intensities,
                context=event.context,
                source_window=f"union:{event.source_window}",
                outcome=event.outcome,
            )
        )
    return renumbered_events


def detect_union_state_window_events(
    raw_signals: list[RawSignal],
    episode_specs: list[dict[str, str]],
    window_size: int,
    activation_threshold: float,
    min_participants: int,
    attack_rate: float,
    recovery_rate: float,
    leak_rate: float,
    commitment_threshold: float,
) -> list[Event]:
    sliding_events = detect_coactivation_events(
        raw_signals=raw_signals,
        episode_specs=episode_specs,
        window_size=window_size,
        activation_threshold=activation_threshold,
        min_participants=min_participants,
    )
    heu_events = detect_heu_like_coactivation_events(
        raw_signals=raw_signals,
        episode_specs=episode_specs,
        activation_threshold=activation_threshold,
        min_participants=min_participants,
        attack_rate=attack_rate,
        recovery_rate=recovery_rate,
        leak_rate=leak_rate,
        commitment_threshold=commitment_threshold,
    )
    return merge_detector_events(
        [
            ("sliding_window", sliding_events),
            ("heu_like", heu_events),
        ]
    )


def participant_subsets(
    participants: tuple[UnitId, ...],
    subset_size: int,
) -> list[tuple[UnitId, ...]]:
    if len(participants) < subset_size:
        return []
    if subset_size == len(participants):
        return [participants]
    if subset_size != 2:
        raise ValueError("only pair decoders are currently implemented")
    return [
        (left_unit, right_unit)
        for left_index, left_unit in enumerate(participants)
        for right_unit in participants[left_index + 1 :]
    ]


def decode_events(
    events: list[Event],
    decoder: str,
    subset_size: int,
    temporal_intensity_weight: float,
    temporal_recurrence_weight: float,
    temporal_prev_transition_weight: float,
    temporal_next_transition_weight: float,
    temporal_next_overlap_weight: float,
    temporal_overcommon_penalty_weight: float,
) -> list[Event]:
    if decoder == "none":
        return events

    subset_frequency: Counter[tuple[UnitId, ...]] = Counter()
    subset_episode_count: Counter[tuple[UnitId, ...]] = Counter()
    candidate_pairs_by_event_id: dict[str, tuple[tuple[UnitId, ...], ...]] = {}
    for event in events:
        candidates = tuple(participant_subsets(event.participants, subset_size))
        candidate_pairs_by_event_id[event.event_id] = candidates
        for subset in candidates:
            subset_frequency[subset] += 1
        for subset in set(candidates):
            subset_episode_count[subset] += 1

    max_frequency = max(subset_frequency.values()) if subset_frequency else 1
    max_episode_count = max(subset_episode_count.values()) if subset_episode_count else 1

    by_episode: dict[str, list[Event]] = defaultdict(list)
    for event in events:
        by_episode[event.episode_id].append(event)

    transition_frequency: Counter[tuple[tuple[UnitId, ...], tuple[UnitId, ...]]] = Counter()
    for episode_events in by_episode.values():
        ordered_events = sorted(
            episode_events,
            key=lambda item: (item.t_start, item.t_end, item.event_id),
        )
        for previous_event, next_event in zip(ordered_events, ordered_events[1:]):
            for previous_pair in candidate_pairs_by_event_id[previous_event.event_id]:
                for next_pair in candidate_pairs_by_event_id[next_event.event_id]:
                    transition_frequency[(previous_pair, next_pair)] += 1

    max_outgoing_by_pair: dict[tuple[UnitId, ...], int] = defaultdict(int)
    for (from_pair, _to_pair), count in transition_frequency.items():
        max_outgoing_by_pair[from_pair] = max(max_outgoing_by_pair[from_pair], count)

    def decoded_event(event: Event, decoded_participants: tuple[UnitId, ...]) -> Event:
        return Event(
            event_id=event.event_id,
            episode_id=event.episode_id,
            t_start=event.t_start,
            t_end=event.t_end,
            participants=decoded_participants,
            intensities={
                unit_id: event.intensities.get(unit_id, 0.0)
                for unit_id in decoded_participants
            },
            context=event.context,
            source_window=f"decoder:{decoder}:{event.source_window}",
            outcome=event.outcome,
        )

    def choose_participants(event: Event) -> tuple[UnitId, ...]:
        if len(event.participants) <= subset_size:
            return event.participants

        candidates = participant_subsets(event.participants, subset_size)
        if not candidates:
            return event.participants

        if decoder == "top_intensity_pair":
            ranked_units = sorted(
                event.participants,
                key=lambda unit_id: (-event.intensities.get(unit_id, 0.0), unit_id),
            )
            return tuple(sorted(ranked_units[:subset_size]))

        if decoder == "frequent_subset_pair":
            return max(
                candidates,
                key=lambda subset: (
                    subset_frequency[subset],
                    sum(event.intensities.get(unit_id, 0.0) for unit_id in subset),
                    subset,
                ),
            )

        if decoder == "consensus_pair":
            return max(
                candidates,
                key=lambda subset: (
                    subset_frequency[subset] / max_frequency
                    + sum(event.intensities.get(unit_id, 0.0) for unit_id in subset)
                    / subset_size,
                    subset_frequency[subset],
                    subset,
                ),
            )

        raise ValueError(f"unknown event decoder: {decoder}")

    def temporal_score(
        event: Event,
        candidate: tuple[UnitId, ...],
        previous_decoded: tuple[UnitId, ...] | None,
        next_event: Event | None,
    ) -> float:
        intensity_score = (
            sum(event.intensities.get(unit_id, 0.0) for unit_id in candidate)
            / subset_size
        )
        recurrence_score = subset_frequency[candidate] / max_frequency

        previous_transition_score = 0.0
        if previous_decoded is not None:
            previous_max = max_outgoing_by_pair.get(previous_decoded, 0)
            if previous_max:
                previous_transition_score = (
                    transition_frequency[(previous_decoded, candidate)] / previous_max
                )

        next_transition_score = 0.0
        next_overlap_score = 0.0
        if next_event is not None:
            next_candidates = candidate_pairs_by_event_id[next_event.event_id]
            candidate_max = max_outgoing_by_pair.get(candidate, 0)
            if candidate_max:
                next_transition_score = max(
                    (
                        transition_frequency[(candidate, next_candidate)] / candidate_max
                        for next_candidate in next_candidates
                    ),
                    default=0.0,
                )
            next_overlap_score = max(
                (
                    len(set(candidate) & set(next_candidate)) / subset_size
                    for next_candidate in next_candidates
                ),
                default=0.0,
            )

        overcommon_penalty = (
            subset_episode_count[candidate] / max_episode_count
        ) ** 2
        return (
            temporal_intensity_weight * intensity_score
            + temporal_recurrence_weight * recurrence_score
            + temporal_prev_transition_weight * previous_transition_score
            + temporal_next_transition_weight * next_transition_score
            + temporal_next_overlap_weight * next_overlap_score
            - temporal_overcommon_penalty_weight * overcommon_penalty
        )

    if decoder == "temporal_consensus_pair":
        decoded_events: list[Event] = []
        for episode_id in sorted(by_episode):
            previous_decoded: tuple[UnitId, ...] | None = None
            episode_events = sorted(
                by_episode[episode_id],
                key=lambda item: (item.t_start, item.t_end, item.event_id),
            )
            for event_index, event in enumerate(episode_events):
                candidates = candidate_pairs_by_event_id[event.event_id]
                if len(event.participants) <= subset_size or not candidates:
                    decoded_participants = event.participants
                else:
                    next_event = (
                        episode_events[event_index + 1]
                        if event_index + 1 < len(episode_events)
                        else None
                    )
                    decoded_participants = max(
                        candidates,
                        key=lambda candidate: (
                            temporal_score(
                                event,
                                candidate,
                                previous_decoded,
                                next_event,
                            ),
                            subset_frequency[candidate],
                            candidate,
                        ),
                    )
                previous_decoded = decoded_participants
                decoded_events.append(decoded_event(event, decoded_participants))
        return merge_detector_events([(decoder, decoded_events)])

    decoded_events: list[Event] = []
    for event in events:
        decoded_participants = choose_participants(event)
        decoded_events.append(decoded_event(event, decoded_participants))

    return merge_detector_events([(decoder, decoded_events)])


def assemble_episodes(events: list[Event]) -> list[Episode]:
    by_episode: dict[str, list[Event]] = defaultdict(list)
    for event in events:
        by_episode[event.episode_id].append(event)

    episodes: list[Episode] = []
    for episode_id, episode_events in sorted(by_episode.items()):
        ordered_events = tuple(
            event.event_id for event in sorted(episode_events, key=lambda item: item.t_start)
        )
        first_event = episode_events[0]
        episodes.append(
            Episode(
                episode_id=episode_id,
                context=first_event.context,
                outcome=first_event.outcome,
                ordered_events=ordered_events,
            )
        )
    return episodes


def build_transitions(events: list[Event], episodes: list[Episode]) -> list[Transition]:
    event_by_id = {event.event_id: event for event in events}
    transitions: list[Transition] = []
    for episode in episodes:
        for from_event_id, to_event_id in zip(episode.ordered_events, episode.ordered_events[1:]):
            from_event = event_by_id[from_event_id]
            to_event = event_by_id[to_event_id]
            from_participants = set(from_event.participants)
            to_participants = set(to_event.participants)
            transitions.append(
                Transition(
                    from_event=from_event.event_id,
                    to_event=to_event.event_id,
                    delta_t=to_event.t_start - from_event.t_end,
                    shared_participants=tuple(sorted(from_participants & to_participants)),
                    changed_participants=tuple(sorted(from_participants ^ to_participants)),
                    weight=1,
                    episode_id=episode.episode_id,
                    context=episode.context,
                    from_label=from_event.label,
                    to_label=to_event.label,
                )
            )
    return transitions


def mine_motifs(events: list[Event], episodes: list[Episode], motif_lengths: tuple[int, ...]) -> list[Motif]:
    event_by_id = {event.event_id: event for event in events}
    counts: Counter[tuple[EventLabel, ...]] = Counter()
    contexts: dict[tuple[EventLabel, ...], Counter[str]] = defaultdict(Counter)
    outcomes: dict[tuple[EventLabel, ...], Counter[str]] = defaultdict(Counter)
    next_events: dict[tuple[EventLabel, ...], Counter[EventLabel]] = defaultdict(Counter)

    for episode in episodes:
        labels = tuple(event_by_id[event_id].label for event_id in episode.ordered_events)
        for motif_length in motif_lengths:
            for index in range(0, len(labels) - motif_length + 1):
                pattern = labels[index : index + motif_length]
                counts[pattern] += 1
                contexts[pattern][episode.context] += 1
                outcomes[pattern][episode.outcome] += 1
                if index + motif_length < len(labels):
                    next_events[pattern][labels[index + motif_length]] += 1

    motifs: list[Motif] = []
    for pattern, support in counts.most_common():
        if support < 2:
            continue
        predicted = tuple(
            label for label, _count in next_events[pattern].most_common()
        )
        variant_labels = tuple(
            f"{label}:{count}" for label, count in next_events[pattern].most_common()
        )
        motifs.append(
            Motif(
                pattern=pattern,
                support=support,
                variants=variant_labels,
                predicted_next_events=predicted,
                contexts=tuple(
                    f"{context}:{count}" for context, count in contexts[pattern].most_common()
                ),
                outcomes=tuple(
                    f"{outcome}:{count}" for outcome, count in outcomes[pattern].most_common()
                ),
            )
        )
    return motifs


def counter_purity(counter: Counter[str]) -> float:
    total = sum(counter.values())
    if total == 0:
        return 0.0
    return max(counter.values()) / total


def classify_pattern_evidence(
    support: int,
    expected_support: float,
    lift: float,
    context_purity: float,
    outcome_purity: float,
    next_purity: float,
    full_sequence: bool,
) -> tuple[str, str]:
    if support <= 1:
        return "singleton_evidence", "observed_once_preserve_as_episode_evidence"
    if outcome_purity < 0.50:
        return "ambiguous_evidence", "same_signature_family_has_conflicting_outcomes"
    if context_purity < 0.10 and outcome_purity < 0.75:
        return "latent_alias_candidate", "same_signature_family_spans_many_contexts_and_outcomes"
    if lift < 1.25 and not full_sequence:
        return "background_recurrence", "recurrence_is_near_chance_for_local_vocabulary"
    if next_purity < 0.50 and not full_sequence:
        return "branching_fragment", "signature_retrieves_multiple_continuations"
    if full_sequence and support >= 2:
        return "episode_template_index", "full_sequence_repeats_and_is_worth_retrieving"
    return "retrieval_index", "recurrence_is_distinct_enough_to_index_as_evidence"


def mine_pattern_evidence(
    events: list[Event],
    episodes: list[Episode],
    pattern_lengths: tuple[int, ...],
) -> list[PatternEvidence]:
    event_by_id = {event.event_id: event for event in events}
    event_label_counter = Counter(event.label for event in events)
    event_total = sum(event_label_counter.values())
    event_probabilities = {
        label: count / event_total for label, count in event_label_counter.items()
    }
    counts: Counter[tuple[EventLabel, ...]] = Counter()
    contexts: dict[tuple[EventLabel, ...], Counter[str]] = defaultdict(Counter)
    outcomes: dict[tuple[EventLabel, ...], Counter[str]] = defaultdict(Counter)
    next_events: dict[tuple[EventLabel, ...], Counter[EventLabel]] = defaultdict(Counter)
    evidence_episode_ids: dict[tuple[EventLabel, ...], set[str]] = defaultdict(set)
    window_counts_by_length: Counter[int] = Counter()

    for episode in episodes:
        labels = tuple(event_by_id[event_id].label for event_id in episode.ordered_events)
        for pattern_length in pattern_lengths:
            for index in range(0, len(labels) - pattern_length + 1):
                pattern = labels[index : index + pattern_length]
                counts[pattern] += 1
                contexts[pattern][episode.context] += 1
                outcomes[pattern][episode.outcome] += 1
                evidence_episode_ids[pattern].add(episode.episode_id)
                window_counts_by_length[pattern_length] += 1
                if index + pattern_length < len(labels):
                    next_events[pattern][labels[index + pattern_length]] += 1

    evidence_rows: list[PatternEvidence] = []
    max_pattern_length = max(pattern_lengths) if pattern_lengths else 0
    for pattern, support in counts.most_common():
        expected_probability = 1.0
        for label in pattern:
            expected_probability *= event_probabilities.get(label, 0.0)
        expected_support = window_counts_by_length[len(pattern)] * expected_probability
        lift = support / expected_support if expected_support > 0.0 else 0.0
        context_counter = contexts[pattern]
        outcome_counter = outcomes[pattern]
        next_counter = next_events[pattern]
        context_purity = counter_purity(context_counter)
        outcome_purity = counter_purity(outcome_counter)
        next_purity = counter_purity(next_counter)
        index_status, index_reason = classify_pattern_evidence(
            support=support,
            expected_support=expected_support,
            lift=lift,
            context_purity=context_purity,
            outcome_purity=outcome_purity,
            next_purity=next_purity,
            full_sequence=len(pattern) == max_pattern_length,
        )
        evidence_rows.append(
            PatternEvidence(
                pattern=pattern,
                support=support,
                expected_support=expected_support,
                lift=lift,
                context_entropy_bits=shannon_entropy(context_counter),
                outcome_entropy_bits=shannon_entropy(outcome_counter),
                context_purity=context_purity,
                outcome_purity=outcome_purity,
                next_entropy_bits=shannon_entropy(next_counter),
                next_purity=next_purity,
                evidence_episode_ids=tuple(sorted(evidence_episode_ids[pattern])),
                contexts=tuple(
                    f"{context}:{count}" for context, count in context_counter.most_common()
                ),
                outcomes=tuple(
                    f"{outcome}:{count}" for outcome, count in outcome_counter.most_common()
                ),
                predicted_next_events=tuple(
                    f"{label}:{count}" for label, count in next_counter.most_common()
                ),
                index_status=index_status,
                index_reason=index_reason,
            )
        )
    return evidence_rows


def pattern_evidence_payload_records(
    case_id: str,
    scale_id: str,
    sequence_length: int,
    classifier_mode: str,
    seed: int,
    pattern_evidence: list[PatternEvidence],
    include_annotations: bool,
) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    for evidence in pattern_evidence:
        key = {
            "signature": list(evidence.pattern),
            "signature_length": len(evidence.pattern),
        }
        payload: dict[str, object] = {
            "case_id": case_id,
            "scale_id": scale_id,
            "sequence_length": sequence_length,
            "classifier_mode": classifier_mode,
            "seed": seed,
            "support": evidence.support,
            "expected_support": round(evidence.expected_support, 6),
            "lift": round(evidence.lift, 6),
            "evidence_episode_ids": list(evidence.evidence_episode_ids),
            "contexts": list(evidence.contexts),
            "outcomes": list(evidence.outcomes),
            "predicted_next_events": list(evidence.predicted_next_events),
            "context_entropy_bits": round(evidence.context_entropy_bits, 6),
            "outcome_entropy_bits": round(evidence.outcome_entropy_bits, 6),
            "context_purity": round(evidence.context_purity, 6),
            "outcome_purity": round(evidence.outcome_purity, 6),
            "next_entropy_bits": round(evidence.next_entropy_bits, 6),
            "next_purity": round(evidence.next_purity, 6),
        }
        if include_annotations:
            payload["annotations"] = {
                "index_status": evidence.index_status,
                "index_reason": evidence.index_reason,
            }
        records.append({"key": key, "payload": payload})
    return records


def write_jsonl(path: Path, rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def split_episodes(episodes: list[Episode], train_fraction: float) -> tuple[set[str], set[str]]:
    train_count = math.floor(len(episodes) * train_fraction)
    train_ids = {episode.episode_id for episode in episodes[:train_count]}
    test_ids = {episode.episode_id for episode in episodes[train_count:]}
    return train_ids, test_ids


def build_event_predictor(
    events: list[Event],
    episodes: list[Episode],
    train_episode_ids: set[str],
) -> dict[EventLabel, Counter[EventLabel]]:
    event_by_id = {event.event_id: event for event in events}
    predictor: dict[EventLabel, Counter[EventLabel]] = defaultdict(Counter)
    for episode in episodes:
        if episode.episode_id not in train_episode_ids:
            continue
        labels = tuple(event_by_id[event_id].label for event_id in episode.ordered_events)
        for current_label, next_label in zip(labels, labels[1:]):
            predictor[current_label][next_label] += 1
    return predictor


def build_context_event_predictor(
    events: list[Event],
    episodes: list[Episode],
    train_episode_ids: set[str],
) -> dict[tuple[str, EventLabel], Counter[EventLabel]]:
    event_by_id = {event.event_id: event for event in events}
    predictor: dict[tuple[str, EventLabel], Counter[EventLabel]] = defaultdict(Counter)
    for episode in episodes:
        if episode.episode_id not in train_episode_ids:
            continue
        labels = tuple(event_by_id[event_id].label for event_id in episode.ordered_events)
        for current_label, next_label in zip(labels, labels[1:]):
            predictor[(episode.context, current_label)][next_label] += 1
    return predictor


def build_event_history_predictor(
    events: list[Event],
    episodes: list[Episode],
    train_episode_ids: set[str],
) -> dict[tuple[EventLabel, EventLabel], Counter[EventLabel]]:
    event_by_id = {event.event_id: event for event in events}
    predictor: dict[tuple[EventLabel, EventLabel], Counter[EventLabel]] = defaultdict(Counter)
    for episode in episodes:
        if episode.episode_id not in train_episode_ids:
            continue
        labels = tuple(event_by_id[event_id].label for event_id in episode.ordered_events)
        for index in range(0, len(labels) - 2):
            predictor[(labels[index], labels[index + 1])][labels[index + 2]] += 1
    return predictor


def build_static_projection(events: list[Event], train_episode_ids: set[str] | None = None) -> nx.Graph:
    graph = nx.Graph()
    for event in events:
        if train_episode_ids is not None and event.episode_id not in train_episode_ids:
            continue
        for unit_id in event.participants:
            graph.add_node(unit_id, kind="unit")
        for left_index, left_unit in enumerate(event.participants):
            for right_unit in event.participants[left_index + 1 :]:
                if graph.has_edge(left_unit, right_unit):
                    graph[left_unit][right_unit]["weight"] += 1
                else:
                    graph.add_edge(left_unit, right_unit, weight=1)
    return graph


def static_predict_next_event(
    static_graph: nx.Graph,
    current_label: EventLabel,
    candidate_labels: set[EventLabel],
) -> EventLabel | None:
    current_units = parse_event_label(current_label)
    scored_candidates: list[tuple[float, EventLabel]] = []
    for candidate_label in candidate_labels:
        candidate_units = parse_event_label(candidate_label)
        score = 0.0
        for current_unit in current_units:
            for candidate_unit in candidate_units:
                if current_unit == candidate_unit:
                    score += 0.25
                elif static_graph.has_edge(current_unit, candidate_unit):
                    score += float(static_graph[current_unit][candidate_unit]["weight"])
        scored_candidates.append((score, candidate_label))
    if not scored_candidates:
        return None
    scored_candidates.sort(key=lambda item: (-item[0], item[1]))
    return scored_candidates[0][1]


def parse_event_label(label: EventLabel) -> tuple[UnitId, ...]:
    stripped = label.strip("{}")
    if not stripped:
        return ()
    return tuple(stripped.split(","))


def evaluate_prediction(
    events: list[Event],
    episodes: list[Episode],
    train_episode_ids: set[str],
    test_episode_ids: set[str],
) -> dict[str, float | int]:
    event_by_id = {event.event_id: event for event in events}
    event_predictor = build_event_predictor(events, episodes, train_episode_ids)
    context_event_predictor = build_context_event_predictor(events, episodes, train_episode_ids)
    history_predictor = build_event_history_predictor(events, episodes, train_episode_ids)
    static_graph = build_static_projection(events, train_episode_ids)
    candidate_labels = {
        event.label for event in events if event.episode_id in train_episode_ids
    }

    event_correct = 0
    static_correct = 0
    total = 0
    ambiguous_total = 0
    ambiguous_event_correct = 0
    ambiguous_static_correct = 0
    context_total = 0
    context_correct = 0
    history_total = 0
    history_correct = 0

    for episode in episodes:
        if episode.episode_id not in test_episode_ids:
            continue
        labels = tuple(event_by_id[event_id].label for event_id in episode.ordered_events)
        for current_label, actual_next_label in zip(labels, labels[1:]):
            if not event_predictor[current_label]:
                continue
            event_prediction = event_predictor[current_label].most_common(1)[0][0]
            static_prediction = static_predict_next_event(
                static_graph, current_label, candidate_labels
            )
            event_hit = event_prediction == actual_next_label
            static_hit = static_prediction == actual_next_label
            event_correct += int(event_hit)
            static_correct += int(static_hit)
            total += 1
            if current_label == "{A,B}":
                ambiguous_total += 1
                ambiguous_event_correct += int(event_hit)
                ambiguous_static_correct += int(static_hit)

        for current_label, actual_next_label in zip(labels, labels[1:]):
            context_key = (episode.context, current_label)
            if not context_event_predictor[context_key]:
                continue
            context_prediction = context_event_predictor[context_key].most_common(1)[0][0]
            context_correct += int(context_prediction == actual_next_label)
            context_total += 1

        for index in range(0, len(labels) - 2):
            history_key = (labels[index], labels[index + 1])
            if not history_predictor[history_key]:
                continue
            history_prediction = history_predictor[history_key].most_common(1)[0][0]
            history_correct += int(history_prediction == labels[index + 2])
            history_total += 1

    return {
        "prediction_cases": total,
        "event_first_accuracy": event_correct / total if total else 0.0,
        "event_context_accuracy": context_correct / context_total if context_total else 0.0,
        "event_context_cases": context_total,
        "event_history_accuracy": history_correct / history_total if history_total else 0.0,
        "event_history_cases": history_total,
        "collapsed_static_accuracy": static_correct / total if total else 0.0,
        "ambiguous_ab_cases": ambiguous_total,
        "ambiguous_ab_event_first_accuracy": (
            ambiguous_event_correct / ambiguous_total if ambiguous_total else 0.0
        ),
        "ambiguous_ab_static_accuracy": (
            ambiguous_static_correct / ambiguous_total if ambiguous_total else 0.0
        ),
    }


def quantify_layer_information_loss(
    raw_signals: list[RawSignal],
    events: list[Event],
    transitions: list[Transition],
    episodes: list[Episode],
    motifs: list[Motif],
    metrics: dict[str, float | int],
    activation_threshold: float,
) -> list[LayerLoss]:
    static_graph = build_static_projection(events)
    active_raw_cells = sum(1 for signal in raw_signals if signal.value >= activation_threshold)
    event_participant_time_cells = sum(
        (event.t_end - event.t_start + 1) * len(event.participants) for event in events
    )
    total_sequence_windows = sum(
        max(0, len(episode.ordered_events) - 2) for episode in episodes
    )
    recurrent_three_event_windows = sum(
        motif.support for motif in motifs if len(motif.pattern) == 3
    )
    event_label_entropy = shannon_entropy(Counter(event.label for event in events))
    transition_entropy = shannon_entropy(
        Counter((transition.from_label, transition.to_label) for transition in transitions)
    )
    context_entropy = shannon_entropy(Counter(event.context for event in events))
    outcome_entropy = shannon_entropy(Counter(event.outcome for event in events))

    rows = [
        LayerLoss(
            "RawSignal",
            "Event",
            "record_count_ratio",
            len(events) / len(raw_signals) if raw_signals else 0.0,
            "Event compression stores one detected coactivation object instead of every unit-time sample.",
        ),
        LayerLoss(
            "RawSignal",
            "Event",
            "active_signal_cell_coverage_ratio",
            event_participant_time_cells / active_raw_cells if active_raw_cells else 0.0,
            "Ratio of event participant-duration cells to threshold-active unit-time cells; values above 1.0 indicate overcapture.",
        ),
        LayerLoss(
            "RawSignal",
            "Event",
            "active_signal_cell_overcapture_ratio",
            max(
                0.0,
                (event_participant_time_cells / active_raw_cells if active_raw_cells else 0.0)
                - 1.0,
            ),
            "Excess event participant-duration coverage beyond threshold-active unit-time cells.",
        ),
        LayerLoss(
            "RawSignal",
            "Event",
            "raw_sample_value_loss_fraction",
            1.0 - (event_participant_time_cells / len(raw_signals) if raw_signals else 0.0),
            "Fraction of original scalar sample positions not preserved as event participant-duration cells.",
        ),
        LayerLoss(
            "Event",
            "Transition",
            "record_count_ratio",
            len(transitions) / len(events) if events else 0.0,
            "Transitions preserve adjacency pairs but drop standalone event payload unless joined back to events.",
        ),
        LayerLoss(
            "Event",
            "Transition",
            "event_payload_loss_fraction_without_join",
            5.0 / 9.0,
            "Transitions directly omit intensities, full participant set, source window, duration, and outcome.",
        ),
        LayerLoss(
            "Episode",
            "Motif",
            "recurring_three_event_window_retention",
            recurrent_three_event_windows / total_sequence_windows if total_sequence_windows else 0.0,
            "Fraction of length-3 episode windows retained as recurrent motifs with support >= 2.",
        ),
        LayerLoss(
            "Event",
            "Motif",
            "motif_record_count_ratio",
            len(motifs) / len(events) if events else 0.0,
            "Motifs are compressed recurring templates, not event-instance records.",
        ),
        LayerLoss(
            "Event",
            "StaticProjection",
            "node_count_ratio",
            static_graph.number_of_nodes() / len(events) if events else 0.0,
            "Static projection collapses event instances into participant unit nodes.",
        ),
        LayerLoss(
            "Event",
            "StaticProjection",
            "edge_count_ratio",
            static_graph.number_of_edges() / len(transitions) if transitions else 0.0,
            "Static projection stores co-participant edges, not temporal event-transition edges.",
        ),
        LayerLoss(
            "Event",
            "StaticProjection",
            "event_instance_loss_fraction",
            1.0,
            "No event IDs, timestamps, durations, source windows, intensities, contexts, or outcomes survive as first-class static graph records.",
        ),
        LayerLoss(
            "Transition",
            "StaticProjection",
            "temporal_order_loss_fraction",
            1.0,
            "Directed temporal adjacency is absent from the collapsed undirected unit graph.",
        ),
        LayerLoss(
            "Event",
            "StaticProjection",
            "context_entropy_lost_bits",
            context_entropy,
            "Bits of event-context distribution that are not represented in the static projection.",
        ),
        LayerLoss(
            "Event",
            "StaticProjection",
            "outcome_entropy_lost_bits",
            outcome_entropy,
            "Bits of event-outcome distribution that are not represented in the static projection.",
        ),
        LayerLoss(
            "Event",
            "StaticProjection",
            "event_label_entropy_bits",
            event_label_entropy,
            "Entropy of event participant-set labels before static collapse.",
        ),
        LayerLoss(
            "Transition",
            "StaticProjection",
            "transition_entropy_lost_bits",
            transition_entropy,
            "Bits of event-transition distribution erased by removing temporal adjacency.",
        ),
        LayerLoss(
            "EventHistory",
            "StaticProjection",
            "predictive_accuracy_delta",
            float(metrics["event_history_accuracy"])
            - float(metrics["collapsed_static_accuracy"]),
            "Next-event accuracy lost when two-event temporal history is replaced by static co-occurrence.",
        ),
        LayerLoss(
            "EventContext",
            "StaticProjection",
            "contextual_predictive_accuracy_delta",
            float(metrics["event_context_accuracy"])
            - float(metrics["collapsed_static_accuracy"]),
            "Next-event accuracy lost when event context is replaced by static co-occurrence.",
        ),
    ]
    return rows


def normalized_redundancy(counter: Counter[object]) -> float:
    total = sum(counter.values())
    unique_count = len(counter)
    if total == 0 or unique_count <= 1:
        return 0.0
    max_entropy = math.log2(unique_count)
    if max_entropy == 0.0:
        return 0.0
    return max(0.0, 1.0 - shannon_entropy(counter) / max_entropy)


def quantify_information_envelope(
    raw_signals: list[RawSignal],
    events: list[Event],
    transitions: list[Transition],
    episodes: list[Episode],
    motifs: list[Motif],
    activation_threshold: float,
) -> list[InformationEnvelope]:
    event_by_id = {event.event_id: event for event in events}
    active_units_by_time: dict[tuple[str, int], list[str]] = defaultdict(list)
    for signal in raw_signals:
        if signal.value >= activation_threshold:
            active_units_by_time[(signal.episode_id, signal.t)].append(signal.unit_id)

    raw_active_set_counter: Counter[str] = Counter(
        event_label(unit_ids)
        for unit_ids in active_units_by_time.values()
        if len(unit_ids) >= 1
    )
    event_label_counter: Counter[str] = Counter(event.label for event in events)
    transition_counter: Counter[tuple[str, str]] = Counter(
        (transition.from_label, transition.to_label) for transition in transitions
    )
    episode_signature_counter: Counter[tuple[str, ...]] = Counter(
        tuple(event_by_id[event_id].label for event_id in episode.ordered_events)
        for episode in episodes
    )
    motif_support_mass = sum(motif.support for motif in motifs)
    total_three_event_windows = sum(
        max(0, len(episode.ordered_events) - 2) for episode in episodes
    )
    recurring_three_event_mass = sum(
        motif.support for motif in motifs if len(motif.pattern) == 3
    )
    repeated_event_instances = sum(
        count for count in event_label_counter.values() if count > 1
    )
    repeated_episode_instances = sum(
        count for count in episode_signature_counter.values() if count > 1
    )
    static_graph = build_static_projection(events)

    rows = [
        InformationEnvelope(
            "RawSignal",
            "active_set_unique_count",
            float(len(raw_active_set_counter)),
            "Distinct threshold-active unit sets observed directly in the signal stream.",
        ),
        InformationEnvelope(
            "RawSignal",
            "active_set_entropy_bits",
            shannon_entropy(raw_active_set_counter),
            "Entropy of threshold-active unit sets before event commitment.",
        ),
        InformationEnvelope(
            "Event",
            "event_label_unique_count",
            float(len(event_label_counter)),
            "Distinct first-class coactivation event labels.",
        ),
        InformationEnvelope(
            "Event",
            "event_label_entropy_bits",
            shannon_entropy(event_label_counter),
            "Entropy of committed event participant sets.",
        ),
        InformationEnvelope(
            "Event",
            "event_label_redundancy_fraction",
            normalized_redundancy(event_label_counter),
            "How much event-label entropy falls below maximum entropy; higher values indicate recurrence and compression opportunity.",
        ),
        InformationEnvelope(
            "Event",
            "repeated_event_instance_fraction",
            repeated_event_instances / len(events) if events else 0.0,
            "Fraction of event instances whose participant set appears more than once.",
        ),
        InformationEnvelope(
            "Transition",
            "transition_unique_count",
            float(len(transition_counter)),
            "Distinct observed event-transition label pairs.",
        ),
        InformationEnvelope(
            "Transition",
            "transition_entropy_bits",
            shannon_entropy(transition_counter),
            "Entropy of temporal adjacency after event commitment.",
        ),
        InformationEnvelope(
            "Transition",
            "transition_redundancy_fraction",
            normalized_redundancy(transition_counter),
            "How much transition entropy falls below maximum entropy; higher values indicate repeated temporal structure.",
        ),
        InformationEnvelope(
            "Episode",
            "episode_signature_unique_count",
            float(len(episode_signature_counter)),
            "Distinct ordered event-label sequences.",
        ),
        InformationEnvelope(
            "Episode",
            "episode_signature_entropy_bits",
            shannon_entropy(episode_signature_counter),
            "Entropy of ordered episode signatures.",
        ),
        InformationEnvelope(
            "Episode",
            "repeated_episode_instance_fraction",
            repeated_episode_instances / len(episodes) if episodes else 0.0,
            "Fraction of episodes whose full event signature recurs.",
        ),
        InformationEnvelope(
            "Motif",
            "motif_count",
            float(len(motifs)),
            "Number of recurring event patterns with support >= 2.",
        ),
        InformationEnvelope(
            "Motif",
            "motif_support_mass",
            float(motif_support_mass),
            "Total support represented by recurring motifs across all motif lengths.",
        ),
        InformationEnvelope(
            "Motif",
            "recurring_three_event_window_fraction",
            recurring_three_event_mass / total_three_event_windows
            if total_three_event_windows
            else 0.0,
            "Fraction of length-3 episode windows captured by recurring motifs.",
        ),
        InformationEnvelope(
            "StaticProjection",
            "static_node_count",
            float(static_graph.number_of_nodes()),
            "Participant nodes retained after collapsing event instances.",
        ),
        InformationEnvelope(
            "StaticProjection",
            "static_edge_count",
            float(static_graph.number_of_edges()),
            "Co-participation edges retained after collapsing event instances.",
        ),
        InformationEnvelope(
            "System",
            "compressibility_index",
            (
                normalized_redundancy(event_label_counter)
                + normalized_redundancy(transition_counter)
                + (
                    recurring_three_event_mass / total_three_event_windows
                    if total_three_event_windows
                    else 0.0
                )
            )
            / 3.0,
            "Composite recurrence signal across events, transitions, and length-3 motifs.",
        ),
    ]
    return rows


def build_event_transition_graph(events: list[Event], transitions: list[Transition]) -> nx.DiGraph:
    graph = nx.DiGraph()
    for event in events:
        graph.add_node(
            event.event_id,
            kind="event",
            label=event.label,
            participants=",".join(event.participants),
            context=event.context,
            outcome=event.outcome,
            t_start=event.t_start,
            t_end=event.t_end,
            duration=event.t_end - event.t_start + 1,
            intensities=json.dumps(event.intensities, sort_keys=True),
            source_window=event.source_window,
            episode_id=event.episode_id,
        )
    for transition in transitions:
        graph.add_edge(
            transition.from_event,
            transition.to_event,
            delta_t=transition.delta_t,
            shared_participants=",".join(transition.shared_participants),
            changed_participants=",".join(transition.changed_participants),
            weight=transition.weight,
            context=transition.context,
            from_label=transition.from_label,
            to_label=transition.to_label,
        )
    return graph


def write_csv(path: Path, rows: Iterable[dict[str, object]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_outputs(
    output_dir: Path,
    raw_signals: list[RawSignal],
    events: list[Event],
    transitions: list[Transition],
    episodes: list[Episode],
    motifs: list[Motif],
    metrics: dict[str, float | int],
    layer_losses: list[LayerLoss],
    information_envelope: list[InformationEnvelope],
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    write_csv(
        output_dir / "raw_signals.csv",
        (
            {
                "unit_id": signal.unit_id,
                "t": signal.t,
                "value": round(signal.value, 5),
                "episode_id": signal.episode_id,
                "context": signal.context,
            }
            for signal in raw_signals
        ),
        ["unit_id", "t", "value", "episode_id", "context"],
    )
    write_csv(
        output_dir / "events.csv",
        (
            {
                "event_id": event.event_id,
                "episode_id": event.episode_id,
                "t_start": event.t_start,
                "t_end": event.t_end,
                "participants": ",".join(event.participants),
                "label": event.label,
                "intensities": json.dumps(event.intensities, sort_keys=True),
                "context": event.context,
                "source_window": event.source_window,
                "outcome": event.outcome,
            }
            for event in events
        ),
        [
            "event_id",
            "episode_id",
            "t_start",
            "t_end",
            "participants",
            "label",
            "intensities",
            "context",
            "source_window",
            "outcome",
        ],
    )
    write_csv(
        output_dir / "transitions.csv",
        (
            {
                "from_event": transition.from_event,
                "to_event": transition.to_event,
                "delta_t": transition.delta_t,
                "shared_participants": ",".join(transition.shared_participants),
                "changed_participants": ",".join(transition.changed_participants),
                "weight": transition.weight,
                "episode_id": transition.episode_id,
                "context": transition.context,
                "from_label": transition.from_label,
                "to_label": transition.to_label,
            }
            for transition in transitions
        ),
        [
            "from_event",
            "to_event",
            "delta_t",
            "shared_participants",
            "changed_participants",
            "weight",
            "episode_id",
            "context",
            "from_label",
            "to_label",
        ],
    )
    write_csv(
        output_dir / "episodes.csv",
        (
            {
                "episode_id": episode.episode_id,
                "context": episode.context,
                "outcome": episode.outcome,
                "ordered_events": ",".join(episode.ordered_events),
            }
            for episode in episodes
        ),
        ["episode_id", "context", "outcome", "ordered_events"],
    )
    write_csv(
        output_dir / "motifs.csv",
        (
            {
                "pattern": " -> ".join(motif.pattern),
                "support": motif.support,
                "variants": ";".join(motif.variants),
                "predicted_next_events": ";".join(motif.predicted_next_events),
                "contexts": ";".join(motif.contexts),
                "outcomes": ";".join(motif.outcomes),
            }
            for motif in motifs
        ),
        ["pattern", "support", "variants", "predicted_next_events", "contexts", "outcomes"],
    )
    write_csv(
        output_dir / "layer_information_loss.csv",
        (
            {
                "from_layer": loss.from_layer,
                "to_layer": loss.to_layer,
                "metric": loss.metric,
                "value": round(loss.value, 6),
                "interpretation": loss.interpretation,
            }
            for loss in layer_losses
        ),
        ["from_layer", "to_layer", "metric", "value", "interpretation"],
    )
    write_csv(
        output_dir / "information_envelope.csv",
        (
            {
                "layer": item.layer,
                "measure": item.measure,
                "value": round(item.value, 6),
                "interpretation": item.interpretation,
            }
            for item in information_envelope
        ),
        ["layer", "measure", "value", "interpretation"],
    )

    static_graph = build_static_projection(events)
    event_transition_graph = build_event_transition_graph(events, transitions)
    nx.write_graphml(static_graph, output_dir / "static_projection.graphml")
    nx.write_graphml(event_transition_graph, output_dir / "event_transition_graph.graphml")
    write_report(
        output_dir / "event_first_temporal_process_validation.md",
        events,
        transitions,
        motifs,
        metrics,
        layer_losses,
        information_envelope,
    )


def write_report(
    path: Path,
    events: list[Event],
    transitions: list[Transition],
    motifs: list[Motif],
    metrics: dict[str, float | int],
    layer_losses: list[LayerLoss],
    information_envelope: list[InformationEnvelope],
) -> None:
    event_counts = Counter(event.label for event in events)
    transition_counts = Counter(
        (transition.from_label, transition.to_label) for transition in transitions
    )
    top_motifs = motifs[:10]

    lines = [
        "# Event-First Memory Prototype Report",
        "",
        "## Question",
        "",
        "When the same static graph is produced by different temporal processes, can the event graph distinguish them?",
        "",
        "## Result",
        "",
        f"- Detected events: {len(events)}",
        f"- Detected transitions: {len(transitions)}",
        f"- Recurrent motifs: {len(motifs)}",
        f"- Event-first next-event accuracy, current event only: {metrics['event_first_accuracy']:.3f}",
        f"- Event-first next-event accuracy, current event plus context: {metrics['event_context_accuracy']:.3f}",
        f"- Event-first next-event accuracy, two-event history: {metrics['event_history_accuracy']:.3f}",
        f"- Collapsed static next-event accuracy: {metrics['collapsed_static_accuracy']:.3f}",
        f"- Ambiguous {{A,B}} cases: {metrics['ambiguous_ab_cases']}",
        f"- Ambiguous {{A,B}} event-first accuracy: {metrics['ambiguous_ab_event_first_accuracy']:.3f}",
        f"- Ambiguous {{A,B}} collapsed-static accuracy: {metrics['ambiguous_ab_static_accuracy']:.3f}",
        "",
        "The current-event model correctly treats `{A,B}` as ambiguous. Context-conditioned events and two-event histories resolve the branch, while the collapsed graph cannot represent either distinction.",
        "",
        "The event view preserves temporal ordering and recovers the branches after `{A,B}`:",
        "",
    ]
    for (from_label, to_label), count in transition_counts.most_common(8):
        lines.append(f"- `{from_label}` -> `{to_label}`: {count}")

    lines.extend(
        [
            "",
            "The collapsed graph contains unit co-occurrence edges, but it has no first-class representation of episode order, context, duration, or branch identity.",
            "",
            "## Event Counts",
            "",
        ]
    )
    for label, count in event_counts.most_common():
        lines.append(f"- `{label}`: {count}")

    lines.extend(["", "## Top Motifs", ""])
    for motif in top_motifs:
        predicted = ", ".join(motif.predicted_next_events) or "none"
        contexts = ", ".join(motif.contexts)
        outcomes = ", ".join(motif.outcomes)
        lines.append(
            f"- `{' -> '.join(motif.pattern)}` support={motif.support}; "
            f"next={predicted}; contexts={contexts}; outcomes={outcomes}"
        )

    lines.extend(["", "## Layer Information Loss", ""])
    for loss in layer_losses:
        lines.append(
            f"- `{loss.from_layer}` -> `{loss.to_layer}` `{loss.metric}` = "
            f"{loss.value:.6f}: {loss.interpretation}"
        )

    lines.extend(["", "## Information Envelope", ""])
    for item in information_envelope:
        lines.append(
            f"- `{item.layer}` `{item.measure}` = {item.value:.6f}: "
            f"{item.interpretation}"
        )

    lines.extend(
        [
            "",
            "## Artifacts",
            "",
            "- `raw_signals.csv`: generated temporal signal stream",
            "- `events.csv`: detected coactivation hyperedges as first-class objects",
            "- `transitions.csv`: temporal adjacency between detected events",
            "- `episodes.csv`: ordered event sequences",
            "- `motifs.csv`: recurrent event-transition patterns",
            "- `layer_information_loss.csv`: compression and information-loss metrics by layer",
            "- `information_envelope.csv`: entropy, redundancy, recurrence, and compressibility metrics",
            "- `static_projection.graphml`: lossy collapsed unit co-occurrence graph",
            "- `event_transition_graph.graphml`: event-level temporal graph",
            "- `event_first_temporal_process_validation.md`: validation summary and interpretation",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def execute_experiment(args: argparse.Namespace) -> ExperimentResult:
    rng = np.random.default_rng(args.seed)
    raw_signals, episode_specs = generate_synthetic_signals(
        rng=rng,
        motif_repetitions=args.motif_repetitions,
        noise_episodes=args.noise_episodes,
        event_duration=args.event_duration,
        event_gap=args.event_gap,
        active_mean=args.active_mean,
        active_std=args.active_std,
        baseline_mean=args.baseline_mean,
        baseline_std=args.baseline_std,
        world=args.world,
        dropout_probability=args.dropout_probability,
        spurious_probability=args.spurious_probability,
    )
    if args.detector == "sliding_window":
        events = detect_coactivation_events(
            raw_signals=raw_signals,
            episode_specs=episode_specs,
            window_size=args.window_size,
            activation_threshold=args.activation_threshold,
            min_participants=args.min_participants,
        )
    elif args.detector == "heu_like":
        events = detect_heu_like_coactivation_events(
            raw_signals=raw_signals,
            episode_specs=episode_specs,
            activation_threshold=args.activation_threshold,
            min_participants=args.min_participants,
            attack_rate=args.heu_attack_rate,
            recovery_rate=args.heu_recovery_rate,
            leak_rate=args.heu_leak_rate,
            commitment_threshold=args.heu_commitment_threshold,
        )
    elif args.detector == "hysteresis":
        events = detect_hysteresis_coactivation_events(
            raw_signals=raw_signals,
            episode_specs=episode_specs,
            activation_threshold=args.activation_threshold,
            min_participants=args.min_participants,
            off_threshold_ratio=args.hysteresis_off_ratio,
        )
    elif args.detector == "hybrid_state_window":
        events = detect_hybrid_state_window_events(
            raw_signals=raw_signals,
            episode_specs=episode_specs,
            activation_threshold=args.activation_threshold,
            min_participants=args.min_participants,
            attack_rate=args.heu_attack_rate,
            recovery_rate=args.heu_recovery_rate,
            leak_rate=args.heu_leak_rate,
            commitment_threshold=args.heu_commitment_threshold,
            window_size=args.window_size,
            local_threshold_ratio=args.hybrid_local_threshold_ratio,
        )
    elif args.detector == "union_state_window":
        events = detect_union_state_window_events(
            raw_signals=raw_signals,
            episode_specs=episode_specs,
            window_size=args.window_size,
            activation_threshold=args.activation_threshold,
            min_participants=args.min_participants,
            attack_rate=args.heu_attack_rate,
            recovery_rate=args.heu_recovery_rate,
            leak_rate=args.heu_leak_rate,
            commitment_threshold=args.heu_commitment_threshold,
        )
    else:
        raise ValueError(f"unknown detector: {args.detector}")
    events = decode_events(
        events=events,
        decoder=args.event_decoder,
        subset_size=args.decoder_subset_size,
        temporal_intensity_weight=args.temporal_decoder_intensity_weight,
        temporal_recurrence_weight=args.temporal_decoder_recurrence_weight,
        temporal_prev_transition_weight=args.temporal_decoder_prev_transition_weight,
        temporal_next_transition_weight=args.temporal_decoder_next_transition_weight,
        temporal_next_overlap_weight=args.temporal_decoder_next_overlap_weight,
        temporal_overcommon_penalty_weight=args.temporal_decoder_overcommon_penalty_weight,
    )
    episodes = assemble_episodes(events)
    transitions = build_transitions(events, episodes)
    motifs = mine_motifs(events, episodes, motif_lengths=(1, 2, 3))
    train_episode_ids, test_episode_ids = split_episodes(episodes, args.train_fraction)
    metrics = evaluate_prediction(events, episodes, train_episode_ids, test_episode_ids)
    layer_losses = quantify_layer_information_loss(
        raw_signals=raw_signals,
        events=events,
        transitions=transitions,
        episodes=episodes,
        motifs=motifs,
        metrics=metrics,
        activation_threshold=args.activation_threshold,
    )
    information_envelope = quantify_information_envelope(
        raw_signals=raw_signals,
        events=events,
        transitions=transitions,
        episodes=episodes,
        motifs=motifs,
        activation_threshold=args.activation_threshold,
    )
    return ExperimentResult(
        raw_signals=raw_signals,
        events=events,
        transitions=transitions,
        episodes=episodes,
        motifs=motifs,
        metrics=metrics,
        layer_losses=layer_losses,
        information_envelope=information_envelope,
    )


def run_experiment(args: argparse.Namespace) -> Path:
    result = execute_experiment(args)
    output_dir = Path(args.output_dir)
    write_outputs(
        output_dir,
        result.raw_signals,
        result.events,
        result.transitions,
        result.episodes,
        result.motifs,
        result.metrics,
        result.layer_losses,
        result.information_envelope,
    )
    if args.sweep:
        run_compression_sweep(args, output_dir)
    if args.compare_detectors:
        run_detector_comparison(args, output_dir)
    if args.detector_robustness_map:
        run_detector_robustness_map(args, output_dir)
    if args.dropout_spurious_pareto:
        run_dropout_spurious_pareto(args, output_dir)
    if args.temporal_decoder_seed_sweep:
        run_temporal_decoder_seed_sweep(args, output_dir)
    if args.motif_fault_tolerance_sweep:
        run_motif_fault_tolerance_sweep(args, output_dir)
    if args.null_ablation_package:
        run_null_ablation_package(args, output_dir)
    if args.representation_gain_noise_grid:
        run_representation_gain_noise_grid(args, output_dir)
    if args.adversarial_falsification_battery:
        run_adversarial_falsification_battery(args, output_dir)
    return output_dir


def make_case_args(args: argparse.Namespace, case: SweepCase, seed_offset: int) -> argparse.Namespace:
    case_args = argparse.Namespace(**vars(args))
    case_args.seed = args.seed + seed_offset
    case_args.event_duration = case.event_duration
    case_args.event_gap = case.event_gap
    case_args.window_size = case.window_size
    case_args.activation_threshold = case.activation_threshold
    case_args.noise_episodes = case.noise_episodes
    case_args.min_participants = case.min_participants
    case_args.active_mean = case.active_mean
    case_args.active_std = case.active_std
    case_args.baseline_mean = case.baseline_mean
    case_args.baseline_std = case.baseline_std
    case_args.dropout_probability = case.dropout_probability
    case_args.spurious_probability = case.spurious_probability
    case_args.sweep = False
    return case_args


def build_sweep_cases(args: argparse.Namespace) -> list[SweepCase]:
    base = {
        "event_duration": args.event_duration,
        "event_gap": args.event_gap,
        "window_size": args.window_size,
        "activation_threshold": args.activation_threshold,
        "noise_episodes": args.noise_episodes,
        "min_participants": args.min_participants,
        "active_mean": args.active_mean,
        "active_std": args.active_std,
        "baseline_mean": args.baseline_mean,
        "baseline_std": args.baseline_std,
        "dropout_probability": args.dropout_probability,
        "spurious_probability": args.spurious_probability,
    }
    cases: list[SweepCase] = [
        SweepCase("baseline", "baseline", "none", 0.0, **base),
    ]

    for noise_episodes in (0, 10, 20, 40, 60):
        case_base = dict(base)
        case_base["noise_episodes"] = noise_episodes
        cases.append(
            SweepCase(
                f"noise_{noise_episodes:02d}",
                "noise",
                "noise_episodes",
                float(noise_episodes),
                **case_base,
            )
        )

    for threshold in (0.45, 0.60, 0.75, 0.90, 1.05):
        case_base = dict(base)
        case_base["activation_threshold"] = threshold
        cases.append(
            SweepCase(
                f"threshold_{threshold:.2f}",
                "threshold",
                "activation_threshold",
                threshold,
                **case_base,
            )
        )

    for window_size in (1, 2, 3, 4, 5):
        case_base = dict(base)
        case_base["window_size"] = window_size
        cases.append(
            SweepCase(
                f"window_{window_size}",
                "temporal_resolution",
                "window_size",
                float(window_size),
                **case_base,
            )
        )

    for event_duration in (1, 2, 3, 4, 5):
        case_base = dict(base)
        case_base["event_duration"] = event_duration
        cases.append(
            SweepCase(
                f"duration_{event_duration}",
                "event_duration",
                "event_duration",
                float(event_duration),
                **case_base,
            )
        )

    for event_gap in (0, 1, 2, 3, 5):
        case_base = dict(base)
        case_base["event_gap"] = event_gap
        cases.append(
            SweepCase(
                f"gap_{event_gap}",
                "temporal_separation",
                "event_gap",
                float(event_gap),
                **case_base,
            )
        )

    for active_mean in (0.55, 0.70, 0.85, 1.00, 1.15):
        case_base = dict(base)
        case_base["active_mean"] = active_mean
        cases.append(
            SweepCase(
                f"signal_{active_mean:.2f}",
                "signal_separation",
                "active_mean",
                active_mean,
                **case_base,
            )
        )

    for active_std in (0.02, 0.05, 0.10, 0.20, 0.35):
        case_base = dict(base)
        case_base["active_std"] = active_std
        cases.append(
            SweepCase(
                f"active_std_{active_std:.2f}",
                "active_variance",
                "active_std",
                active_std,
                **case_base,
            )
        )

    for baseline_mean in (0.03, 0.15, 0.30, 0.45, 0.60):
        case_base = dict(base)
        case_base["baseline_mean"] = baseline_mean
        cases.append(
            SweepCase(
                f"baseline_mean_{baseline_mean:.2f}",
                "baseline_elevation",
                "baseline_mean",
                baseline_mean,
                **case_base,
            )
        )

    for baseline_std in (0.01, 0.05, 0.10, 0.20, 0.35):
        case_base = dict(base)
        case_base["baseline_std"] = baseline_std
        cases.append(
            SweepCase(
                f"baseline_std_{baseline_std:.2f}",
                "baseline_variance",
                "baseline_std",
                baseline_std,
                **case_base,
            )
        )

    for dropout_probability in (0.0, 0.05, 0.10, 0.20, 0.35, 0.50):
        case_base = dict(base)
        case_base["dropout_probability"] = dropout_probability
        cases.append(
            SweepCase(
                f"dropout_{dropout_probability:.2f}",
                "active_dropout",
                "dropout_probability",
                dropout_probability,
                **case_base,
            )
        )

    for spurious_probability in (0.0, 0.01, 0.03, 0.05, 0.10, 0.20):
        case_base = dict(base)
        case_base["spurious_probability"] = spurious_probability
        cases.append(
            SweepCase(
                f"spurious_{spurious_probability:.2f}",
                "inactive_spurious_activity",
                "spurious_probability",
                spurious_probability,
                **case_base,
            )
        )

    for min_participants in (1, 2, 3):
        case_base = dict(base)
        case_base["min_participants"] = min_participants
        cases.append(
            SweepCase(
                f"min_participants_{min_participants}",
                "participant_cardinality",
                "min_participants",
                float(min_participants),
                **case_base,
            )
        )

    return cases


def layer_loss_value(layer_losses: list[LayerLoss], metric: str) -> float:
    for loss in layer_losses:
        if loss.metric == metric:
            return loss.value
    return 0.0


def envelope_value(envelope: list[InformationEnvelope], measure: str) -> float:
    for item in envelope:
        if item.measure == measure:
            return item.value
    return 0.0


def motif_support(motifs: list[Motif], pattern: tuple[EventLabel, ...]) -> int:
    for motif in motifs:
        if motif.pattern == pattern:
            return motif.support
    return 0


def length_three_motif_counter(motifs: list[Motif]) -> Counter[tuple[EventLabel, ...]]:
    return Counter(
        {motif.pattern: motif.support for motif in motifs if len(motif.pattern) == 3}
    )


def canonical_motif_metrics(
    motifs: list[Motif],
    canonical_motifs: tuple[tuple[EventLabel, ...], ...],
) -> dict[str, float | int | str]:
    length_three_counter = length_three_motif_counter(motifs)
    total_length_three_support = sum(length_three_counter.values())
    canonical_supports = [
        length_three_counter.get(canonical_motif, 0)
        for canonical_motif in canonical_motifs
    ]
    canonical_support_mass = sum(canonical_supports)
    ranked_patterns = [
        pattern
        for pattern, _support in length_three_counter.most_common()
    ]
    ranks: list[int] = []
    for canonical_motif in canonical_motifs:
        try:
            ranks.append(ranked_patterns.index(canonical_motif) + 1)
        except ValueError:
            ranks.append(0)
    return {
        "canonical_length3_supports": ";".join(str(item) for item in canonical_supports),
        "canonical_length3_support_min": min(canonical_supports) if canonical_supports else 0,
        "canonical_length3_support_mass": canonical_support_mass,
        "canonical_length3_support_fraction": (
            canonical_support_mass / total_length_three_support
            if total_length_three_support
            else 0.0
        ),
        "canonical_length3_ranks": ";".join(str(item) for item in ranks),
        "canonical_length3_rank_worst": max(ranks) if ranks else 0,
        "length3_motif_support_mass": total_length_three_support,
        "length3_motif_count": len(length_three_counter),
        "top5_length3_patterns": " | ".join(
            " -> ".join(pattern)
            for pattern, _support in length_three_counter.most_common(5)
        ),
    }


def canonical_layer_support_metrics(
    events: list[Event],
    transitions: list[Transition],
    canonical_motifs: tuple[tuple[EventLabel, ...], ...],
) -> dict[str, float | int]:
    canonical_event_labels = {
        label for motif in canonical_motifs for label in motif
    }
    canonical_transition_labels = {
        (from_label, to_label)
        for motif in canonical_motifs
        for from_label, to_label in zip(motif, motif[1:])
    }
    event_label_counter = Counter(event.label for event in events)
    transition_label_counter = Counter(
        (transition.from_label, transition.to_label) for transition in transitions
    )
    total_event_support = sum(event_label_counter.values())
    total_transition_support = sum(transition_label_counter.values())
    canonical_event_support = sum(
        event_label_counter[label] for label in canonical_event_labels
    )
    canonical_transition_support = sum(
        transition_label_counter[label_pair]
        for label_pair in canonical_transition_labels
    )
    return {
        "canonical_event_support_fraction": (
            canonical_event_support / total_event_support
            if total_event_support
            else 0.0
        ),
        "canonical_transition_support_fraction": (
            canonical_transition_support / total_transition_support
            if total_transition_support
            else 0.0
        ),
        "canonical_event_support_mass": canonical_event_support,
        "canonical_transition_support_mass": canonical_transition_support,
    }


def jaccard_similarity(left: set[tuple[EventLabel, ...]], right: set[tuple[EventLabel, ...]]) -> float:
    if not left and not right:
        return 1.0
    union = left | right
    if not union:
        return 0.0
    return len(left & right) / len(union)


def relabeled_event(
    event: Event,
    participants: tuple[UnitId, ...],
    source_prefix: str,
    episode_id: str | None = None,
    context: str | None = None,
    outcome: str | None = None,
) -> Event:
    return Event(
        event_id=event.event_id,
        episode_id=episode_id if episode_id is not None else event.episode_id,
        t_start=event.t_start,
        t_end=event.t_end,
        participants=participants,
        intensities={
            unit_id: event.intensities.get(unit_id, 1.0)
            for unit_id in participants
        },
        context=context if context is not None else event.context,
        source_window=f"{source_prefix}:{event.source_window}",
        outcome=outcome if outcome is not None else event.outcome,
    )


def transform_event_stream_null(
    events: list[Event],
    null_model: str,
    rng: np.random.Generator,
) -> list[Event]:
    if null_model == "observed":
        return events

    if null_model == "within_episode_permuted":
        transformed_events: list[Event] = []
        by_episode: dict[str, list[Event]] = defaultdict(list)
        for event in events:
            by_episode[event.episode_id].append(event)
        for episode_id in sorted(by_episode):
            episode_events = sorted(
                by_episode[episode_id],
                key=lambda item: (item.t_start, item.t_end, item.event_id),
            )
            participant_sets = [event.participants for event in episode_events]
            rng.shuffle(participant_sets)
            for event, participants in zip(episode_events, participant_sets):
                transformed_events.append(
                    relabeled_event(event, participants, "null:within_episode_permuted")
                )
        return sorted(
            transformed_events,
            key=lambda item: (item.episode_id, item.t_start, item.event_id),
        )

    if null_model == "global_label_permuted":
        unique_participant_sets = sorted({event.participants for event in events})
        permuted_sets = list(unique_participant_sets)
        rng.shuffle(permuted_sets)
        label_map = dict(zip(unique_participant_sets, permuted_sets))
        return [
            relabeled_event(
                event,
                label_map[event.participants],
                "null:global_label_permuted",
            )
            for event in events
        ]

    if null_model == "episode_boundaries_permuted":
        by_episode: dict[str, list[Event]] = defaultdict(list)
        for event in events:
            by_episode[event.episode_id].append(event)
        episode_ids = sorted(by_episode)
        episode_specs = []
        flattened_events: list[Event] = []
        for episode_id in episode_ids:
            ordered_events = sorted(
                by_episode[episode_id],
                key=lambda item: (item.t_start, item.t_end, item.event_id),
            )
            first_event = ordered_events[0]
            episode_specs.append(
                (
                    episode_id,
                    first_event.context,
                    first_event.outcome,
                    len(ordered_events),
                )
            )
            flattened_events.extend(ordered_events)
        rng.shuffle(flattened_events)
        transformed_events = []
        cursor = 0
        for episode_id, context, outcome, episode_length in episode_specs:
            chunk = flattened_events[cursor : cursor + episode_length]
            cursor += episode_length
            for event_index, event in enumerate(chunk):
                transformed_events.append(
                    relabeled_event(
                        event,
                        event.participants,
                        "null:episode_boundaries_permuted",
                        episode_id=episode_id,
                        context=context,
                        outcome=outcome,
                    )
                )
        return sorted(
            transformed_events,
            key=lambda item: (item.episode_id, item.t_start, item.event_id),
        )

    raise ValueError(f"unknown null model: {null_model}")


def rebuild_result_from_events(
    base_result: ExperimentResult,
    events: list[Event],
    args: argparse.Namespace,
) -> ExperimentResult:
    episodes = assemble_episodes(events)
    transitions = build_transitions(events, episodes)
    motifs = mine_motifs(events, episodes, motif_lengths=(1, 2, 3))
    train_episode_ids, test_episode_ids = split_episodes(episodes, args.train_fraction)
    metrics = evaluate_prediction(events, episodes, train_episode_ids, test_episode_ids)
    layer_losses = quantify_layer_information_loss(
        raw_signals=base_result.raw_signals,
        events=events,
        transitions=transitions,
        episodes=episodes,
        motifs=motifs,
        metrics=metrics,
        activation_threshold=args.activation_threshold,
    )
    information_envelope = quantify_information_envelope(
        raw_signals=base_result.raw_signals,
        events=events,
        transitions=transitions,
        episodes=episodes,
        motifs=motifs,
        activation_threshold=args.activation_threshold,
    )
    return ExperimentResult(
        raw_signals=base_result.raw_signals,
        events=events,
        transitions=transitions,
        episodes=episodes,
        motifs=motifs,
        metrics=metrics,
        layer_losses=layer_losses,
        information_envelope=information_envelope,
    )


def canonical_motifs_for_world(world: str) -> tuple[tuple[EventLabel, ...], ...]:
    if world == "branch":
        return (
            ("{A,B}", "{B,C}", "{C,D}"),
            ("{A,B}", "{B,E}", "{E,F}"),
        )
    if world == "overlap":
        return (
            ("{A,B}", "{B,C}", "{E,F}"),
            ("{A,B}", "{B,E}", "{E,F}"),
            ("{A,B}", "{B,G}", "{E,F}"),
        )
    if world == "hostile_unique":
        return ()
    raise ValueError(f"unknown synthetic world: {world}")


def classify_regime(
    active_coverage: float,
    motif_recovery: float,
    event_history_accuracy: float,
    predictive_delta: float,
) -> str:
    if (
        0.95 <= active_coverage <= 1.10
        and motif_recovery >= 0.95
        and event_history_accuracy >= 0.95
        and predictive_delta >= 0.50
    ):
        return "faithful"
    if (
        0.70 <= active_coverage <= 1.50
        and motif_recovery >= 0.70
        and event_history_accuracy >= 0.70
        and predictive_delta > 0.0
    ):
        return "degraded"
    return "failed"


def classify_hostile_compressibility(
    compressibility_index: float,
    repeated_episode_fraction: float,
    recurring_window_fraction: float,
) -> str:
    if (
        compressibility_index <= 0.05
        and repeated_episode_fraction == 0.0
        and recurring_window_fraction <= 0.05
    ):
        return "expected_collapse"
    if compressibility_index <= 0.15 and repeated_episode_fraction <= 0.05:
        return "partial_collapse"
    return "suspicious_compression"


def categorize_failure_modes(
    active_coverage: float,
    overcapture: float,
    motif_recovery: float,
    event_history_accuracy: float,
    predictive_delta: float,
    event_count: int,
) -> tuple[str, ...]:
    modes: list[str] = []
    if event_count == 0:
        modes.append("no_events_detected")
    if active_coverage < 0.70:
        modes.append("undercapture")
    elif active_coverage < 0.95:
        modes.append("coverage_degradation")
    if active_coverage > 1.50 or overcapture > 0.50:
        modes.append("overcapture")
    elif active_coverage > 1.10 or overcapture > 0.10:
        modes.append("overcapture_degradation")
    if motif_recovery < 0.70:
        modes.append("motif_loss")
    elif motif_recovery < 0.95:
        modes.append("motif_degradation")
    if event_history_accuracy < 0.70:
        modes.append("history_prediction_failure")
    elif event_history_accuracy < 0.95:
        modes.append("history_prediction_degradation")
    if predictive_delta <= 0.0:
        modes.append("no_event_advantage_over_static")
    if not modes:
        modes.append("within_useful_manifold")
    return tuple(modes)


def run_compression_sweep(args: argparse.Namespace, output_dir: Path) -> None:
    rows: list[dict[str, object]] = []
    cases = build_sweep_cases(args)
    canonical_motifs = canonical_motifs_for_world(args.world)

    for index, case in enumerate(cases):
        result = execute_experiment(make_case_args(args, case, index + 1))
        canonical_supports = [
            motif_support(result.motifs, motif) for motif in canonical_motifs
        ]
        motif_recovery = (
            min(canonical_supports) / args.motif_repetitions
            if canonical_supports
            else 0.0
        )
        active_coverage = layer_loss_value(
            result.layer_losses, "active_signal_cell_coverage_ratio"
        )
        predictive_delta = layer_loss_value(
            result.layer_losses, "predictive_accuracy_delta"
        )
        overcapture = layer_loss_value(
            result.layer_losses, "active_signal_cell_overcapture_ratio"
        )
        event_history_accuracy = float(result.metrics["event_history_accuracy"])
        compressibility_index = envelope_value(
            result.information_envelope, "compressibility_index"
        )
        repeated_episode_fraction = envelope_value(
            result.information_envelope, "repeated_episode_instance_fraction"
        )
        recurring_window_fraction = envelope_value(
            result.information_envelope, "recurring_three_event_window_fraction"
        )
        if args.world == "hostile_unique":
            status = classify_hostile_compressibility(
                compressibility_index,
                repeated_episode_fraction,
                recurring_window_fraction,
            )
            failure_modes = (
                ("noncompressible_as_expected",)
                if status == "expected_collapse"
                else ("unexpected_recurrence",)
            )
        else:
            status = classify_regime(
                active_coverage,
                motif_recovery,
                event_history_accuracy,
                predictive_delta,
            )
            failure_modes = categorize_failure_modes(
                active_coverage,
                overcapture,
                motif_recovery,
                event_history_accuracy,
                predictive_delta,
                len(result.events),
            )
        rows.append(
            {
                "case_id": case.case_id,
                "axis": case.axis,
                "parameter": case.parameter,
                "value": case.value,
                "status": status,
                "failure_modes": ";".join(failure_modes),
                "event_count": len(result.events),
                "transition_count": len(result.transitions),
                "motif_count": len(result.motifs),
                "canonical_motif_supports": ";".join(
                    str(support) for support in canonical_supports
                ),
                "canonical_motif_recovery": round(motif_recovery, 6),
                "active_signal_cell_coverage_ratio": round(active_coverage, 6),
                "active_signal_cell_overcapture_ratio": round(
                    overcapture, 6
                ),
                "raw_sample_value_loss_fraction": round(
                    layer_loss_value(result.layer_losses, "raw_sample_value_loss_fraction"),
                    6,
                ),
                "event_history_accuracy": round(event_history_accuracy, 6),
                "event_context_accuracy": round(
                    float(result.metrics["event_context_accuracy"]), 6
                ),
                "collapsed_static_accuracy": round(
                    float(result.metrics["collapsed_static_accuracy"]), 6
                ),
                "predictive_accuracy_delta": round(predictive_delta, 6),
                "compressibility_index": round(compressibility_index, 6),
                "repeated_episode_instance_fraction": round(
                    repeated_episode_fraction, 6
                ),
                "recurring_three_event_window_fraction": round(
                    recurring_window_fraction, 6
                ),
                "event_instance_loss_fraction": round(
                    layer_loss_value(result.layer_losses, "event_instance_loss_fraction"),
                    6,
                ),
                "temporal_order_loss_fraction": round(
                    layer_loss_value(result.layer_losses, "temporal_order_loss_fraction"),
                    6,
                ),
                "event_duration": case.event_duration,
                "event_gap": case.event_gap,
                "window_size": case.window_size,
                "activation_threshold": case.activation_threshold,
                "noise_episodes": case.noise_episodes,
                "min_participants": case.min_participants,
                "active_mean": case.active_mean,
                "active_std": case.active_std,
                "baseline_mean": case.baseline_mean,
                "baseline_std": case.baseline_std,
                "dropout_probability": case.dropout_probability,
                "spurious_probability": case.spurious_probability,
            }
        )

    sweep_path = output_dir / f"compression_regime_sweep_{args.world}.csv"
    report_path = output_dir / f"compression_regime_edges_{args.world}.md"
    write_csv(
        sweep_path,
        rows,
        [
            "case_id",
            "axis",
            "parameter",
            "value",
            "status",
            "failure_modes",
            "event_count",
            "transition_count",
            "motif_count",
            "canonical_motif_supports",
            "canonical_motif_recovery",
            "active_signal_cell_coverage_ratio",
            "active_signal_cell_overcapture_ratio",
            "raw_sample_value_loss_fraction",
            "event_history_accuracy",
            "event_context_accuracy",
            "collapsed_static_accuracy",
            "predictive_accuracy_delta",
            "compressibility_index",
            "repeated_episode_instance_fraction",
            "recurring_three_event_window_fraction",
            "event_instance_loss_fraction",
            "temporal_order_loss_fraction",
            "event_duration",
            "event_gap",
            "window_size",
            "activation_threshold",
            "noise_episodes",
            "min_participants",
            "active_mean",
            "active_std",
            "baseline_mean",
            "baseline_std",
            "dropout_probability",
            "spurious_probability",
        ],
    )
    write_compression_regime_report(report_path, rows, args.world)


def write_compression_regime_report(
    path: Path, rows: list[dict[str, object]], world: str
) -> None:
    by_axis: dict[str, list[dict[str, object]]] = defaultdict(list)
    failure_mode_counts: Counter[str] = Counter()
    for row in rows:
        by_axis[str(row["axis"])].append(row)
        for mode in str(row["failure_modes"]).split(";"):
            failure_mode_counts[mode] += 1

    lines = [
        f"# Compression Regime Edges: {world}",
        "",
        "This sweep estimates where event-first compression remains faithful, becomes degraded, or fails for the selected synthetic temporal motif task.",
        "",
        "## Boundary Summary",
        "",
    ]
    if world == "hostile_unique":
        lines[2] = "This sweep attacks compressibility directly by removing recurrence from the synthetic temporal motif task."
        lines[4:4] = [
            "Status criteria:",
            "",
            "- `expected_collapse`: compressibility index <= 0.05, repeated episode fraction = 0, and recurring length-3 window fraction <= 0.05.",
            "- `partial_collapse`: compressibility remains low but some recurrence leaks through.",
            "- `suspicious_compression`: the system appears to compress a world designed not to repeat.",
            "",
        ]
    else:
        lines[4:4] = [
            "Status criteria:",
            "",
            "- `faithful`: active coverage is between 0.95 and 1.10, canonical motif recovery >= 0.95, event-history accuracy >= 0.95, and predictive delta over static >= 0.50.",
            "- `degraded`: active coverage is between 0.70 and 1.50, canonical motif recovery >= 0.70, event-history accuracy >= 0.70, and predictive delta remains positive.",
            "- `failed`: one or more degraded criteria are not met.",
            "",
        ]

    lines.extend(["## Failure Mode Counts", ""])
    for mode, count in failure_mode_counts.most_common():
        lines.append(f"- `{mode}`: {count}")
    lines.append("")

    for axis in sorted(by_axis):
        axis_rows = sorted(by_axis[axis], key=lambda item: float(item["value"]))
        faithful_values = [
            row["value"] for row in axis_rows if row["status"] == "faithful"
        ]
        degraded_values = [
            row["value"] for row in axis_rows if row["status"] == "degraded"
        ]
        failed_values = [row["value"] for row in axis_rows if row["status"] == "failed"]
        expected_collapse_values = [
            row["value"] for row in axis_rows if row["status"] == "expected_collapse"
        ]
        lines.append(f"### {axis}")
        lines.append("")
        if world == "hostile_unique":
            lines.append(
                f"- expected collapse values: {expected_collapse_values or 'none'}"
            )
        else:
            lines.append(f"- faithful values: {faithful_values or 'none'}")
            lines.append(f"- degraded values: {degraded_values or 'none'}")
            lines.append(f"- failed values: {failed_values or 'none'}")
        for row in axis_rows:
            lines.append(
                f"- `{row['case_id']}` status={row['status']} "
                f"modes={row['failure_modes']} "
                f"motif_recovery={row['canonical_motif_recovery']} "
                f"active_coverage={row['active_signal_cell_coverage_ratio']} "
                f"overcapture={row['active_signal_cell_overcapture_ratio']} "
                f"history_acc={row['event_history_accuracy']} "
                f"delta={row['predictive_accuracy_delta']}"
            )
        lines.append("")

    lines.extend(
        [
            "## Interpretation",
            "",
            "The edge of this compression regime is where detected event objects stop preserving the task-relevant temporal branch structure. In recurring worlds, that edge is operationally visible as a drop in canonical motif recovery or event-history prediction before static graph metrics become useful.",
            "",
            "Static projection remains a deliberately lossy lower layer: event instance identity and temporal order loss stay at 1.0 by design. The question is therefore not whether static projection loses information, but which upstream event-detection settings keep enough event structure before that projection is requested.",
        ]
    )
    if world == "overlap":
        lines.extend(
            [
                "",
                "## Overlap Stress Result",
                "",
                "The overlap world uses three motifs with the same prefix `{A,B}` and the same suffix `{E,F}`. The middle event is the discriminating state: `{B,C}`, `{B,E}`, or `{B,G}`.",
                "",
                "A faithful event representation should therefore show low current-event certainty at the shared prefix, high recovery for all three full motifs, and high two-event-history prediction into the shared suffix.",
            ]
        )
    if world == "hostile_unique":
        lines.extend(
            [
                "",
                "## Hostile Compressibility Result",
                "",
                "The hostile world intentionally removes recurrence: every episode signature is unique, contexts and outcomes are unique, and event labels are sampled without replacement.",
                "",
                "The expected result is collapse of motif support and compressibility. Suspicious compression in this world would indicate that the detector or projection is inventing structure rather than preserving real recurrence.",
            ]
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def summarize_detector_result(
    result: ExperimentResult,
    world: str,
    motif_repetitions: int,
) -> dict[str, float | int | str]:
    canonical_motifs = canonical_motifs_for_world(world)
    canonical_supports = [
        motif_support(result.motifs, motif) for motif in canonical_motifs
    ]
    motif_recovery = (
        min(canonical_supports) / motif_repetitions if canonical_supports else 0.0
    )
    active_coverage = layer_loss_value(
        result.layer_losses, "active_signal_cell_coverage_ratio"
    )
    overcapture = layer_loss_value(
        result.layer_losses, "active_signal_cell_overcapture_ratio"
    )
    compressibility_index = envelope_value(
        result.information_envelope, "compressibility_index"
    )
    recurring_window_fraction = envelope_value(
        result.information_envelope, "recurring_three_event_window_fraction"
    )
    repeated_episode_fraction = envelope_value(
        result.information_envelope, "repeated_episode_instance_fraction"
    )
    event_history_accuracy = float(result.metrics["event_history_accuracy"])
    predictive_delta = layer_loss_value(result.layer_losses, "predictive_accuracy_delta")
    if world == "hostile_unique":
        status = classify_hostile_compressibility(
            compressibility_index,
            repeated_episode_fraction,
            recurring_window_fraction,
        )
        failure_modes = (
            "noncompressible_as_expected"
            if status == "expected_collapse"
            else "unexpected_recurrence"
        )
    else:
        status = classify_regime(
            active_coverage,
            motif_recovery,
            event_history_accuracy,
            predictive_delta,
        )
        failure_modes = ";".join(
            categorize_failure_modes(
                active_coverage,
                overcapture,
                motif_recovery,
                event_history_accuracy,
                predictive_delta,
                len(result.events),
            )
        )
    return {
        "status": status,
        "failure_modes": failure_modes,
        "event_count": len(result.events),
        "transition_count": len(result.transitions),
        "motif_count": len(result.motifs),
        "canonical_motif_supports": ";".join(str(item) for item in canonical_supports),
        "canonical_motif_recovery": round(motif_recovery, 6),
        "active_signal_cell_coverage_ratio": round(active_coverage, 6),
        "active_signal_cell_overcapture_ratio": round(overcapture, 6),
        "event_history_accuracy": round(event_history_accuracy, 6),
        "event_context_accuracy": round(float(result.metrics["event_context_accuracy"]), 6),
        "collapsed_static_accuracy": round(float(result.metrics["collapsed_static_accuracy"]), 6),
        "predictive_accuracy_delta": round(predictive_delta, 6),
        "compressibility_index": round(compressibility_index, 6),
        "recurring_three_event_window_fraction": round(recurring_window_fraction, 6),
        "repeated_episode_instance_fraction": round(repeated_episode_fraction, 6),
    }


def detector_comparison_cases(args: argparse.Namespace) -> list[tuple[str, str, dict[str, object]]]:
    return [
        ("branch_baseline", "branch", {}),
        ("overlap_baseline", "overlap", {}),
        ("hostile_unique_baseline", "hostile_unique", {}),
        ("branch_dropout_005", "branch", {"dropout_probability": 0.05}),
        ("overlap_dropout_005", "overlap", {"dropout_probability": 0.05}),
        ("branch_spurious_005", "branch", {"spurious_probability": 0.05}),
        ("overlap_spurious_005", "overlap", {"spurious_probability": 0.05}),
        ("branch_threshold_low", "branch", {"activation_threshold": 0.60}),
        ("branch_threshold_high", "branch", {"activation_threshold": 1.05}),
        ("branch_window_blur", "branch", {"window_size": 4}),
        ("overlap_window_blur", "overlap", {"window_size": 4}),
    ]


def run_detector_comparison(args: argparse.Namespace, output_dir: Path) -> None:
    rows: list[dict[str, object]] = []
    for case_index, (case_id, world, overrides) in enumerate(detector_comparison_cases(args)):
        for detector in ("sliding_window", "heu_like", "hysteresis"):
            case_args = argparse.Namespace(**vars(args))
            case_args.seed = args.seed + case_index + 100
            case_args.world = world
            case_args.detector = detector
            case_args.sweep = False
            case_args.compare_detectors = False
            for key, value in overrides.items():
                setattr(case_args, key, value)
            result = execute_experiment(case_args)
            summary = summarize_detector_result(result, world, case_args.motif_repetitions)
            rows.append(
                {
                    "case_id": case_id,
                    "world": world,
                    "detector": detector,
                    **summary,
                    "window_size": case_args.window_size,
                    "activation_threshold": case_args.activation_threshold,
                    "dropout_probability": case_args.dropout_probability,
                    "spurious_probability": case_args.spurious_probability,
                    "heu_attack_rate": case_args.heu_attack_rate,
                    "heu_recovery_rate": case_args.heu_recovery_rate,
                    "heu_leak_rate": case_args.heu_leak_rate,
                    "heu_commitment_threshold": case_args.heu_commitment_threshold,
                    "hysteresis_off_ratio": case_args.hysteresis_off_ratio,
                    "hybrid_local_threshold_ratio": case_args.hybrid_local_threshold_ratio,
                    "event_decoder": case_args.event_decoder,
                    "decoder_subset_size": case_args.decoder_subset_size,
                }
            )

    fieldnames = [
        "case_id",
        "world",
        "detector",
        "status",
        "failure_modes",
        "event_count",
        "transition_count",
        "motif_count",
        "canonical_motif_supports",
        "canonical_motif_recovery",
        "active_signal_cell_coverage_ratio",
        "active_signal_cell_overcapture_ratio",
        "event_history_accuracy",
        "event_context_accuracy",
        "collapsed_static_accuracy",
        "predictive_accuracy_delta",
        "compressibility_index",
        "recurring_three_event_window_fraction",
        "repeated_episode_instance_fraction",
        "window_size",
        "activation_threshold",
        "dropout_probability",
        "spurious_probability",
        "heu_attack_rate",
        "heu_recovery_rate",
        "heu_leak_rate",
        "heu_commitment_threshold",
        "hysteresis_off_ratio",
        "hybrid_local_threshold_ratio",
        "event_decoder",
        "decoder_subset_size",
    ]
    write_csv(output_dir / "detector_comparison.csv", rows, fieldnames)
    write_detector_comparison_report(output_dir / "detector_comparison.md", rows)


def write_detector_comparison_report(path: Path, rows: list[dict[str, object]]) -> None:
    by_case: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        by_case[str(row["case_id"])].append(row)

    lines = [
        "# Detector Comparison",
        "",
        "This compares the original sliding-window detector against a simple HEU-like stateful event-commitment detector.",
        "",
        "The HEU-like detector is intentionally minimal: bounded envelope accumulation, recovery/leak, and thresholded event commitment. It is not the full HEU paper implementation.",
        "",
        "## Case Results",
        "",
    ]
    for case_id in sorted(by_case):
        lines.append(f"### {case_id}")
        lines.append("")
        for row in sorted(by_case[case_id], key=lambda item: str(item["detector"])):
            lines.append(
                f"- `{row['detector']}` status={row['status']} modes={row['failure_modes']} "
                f"events={row['event_count']} motifs={row['motif_count']} "
                f"motif_recovery={row['canonical_motif_recovery']} "
                f"coverage={row['active_signal_cell_coverage_ratio']} "
                f"overcapture={row['active_signal_cell_overcapture_ratio']} "
                f"history_acc={row['event_history_accuracy']} "
                f"compressibility={row['compressibility_index']}"
            )
        lines.append("")

    lines.extend(
        [
            "## Interpretation",
            "",
            "A detector improves the system only if it widens the faithful compression envelope without inventing recurrence in the hostile unique world.",
            "",
            "Prediction alone is insufficient. Cases that preserve prediction while overcapturing event cells still degrade the representation.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def detector_variant_specs() -> list[tuple[str, str, dict[str, object]]]:
    return [
        ("sliding_window_default", "sliding_window", {}),
        ("sliding_window_short", "sliding_window", {"window_size": 2}),
        ("sliding_window_long", "sliding_window", {"window_size": 4}),
        ("sliding_window_low_threshold", "sliding_window", {"activation_threshold": 0.60}),
        ("sliding_window_high_threshold", "sliding_window", {"activation_threshold": 0.90}),
        ("heu_default", "heu_like", {}),
        ("heu_fast_decay", "heu_like", {"heu_recovery_rate": 0.60, "heu_leak_rate": 0.05}),
        ("heu_slow_decay", "heu_like", {"heu_recovery_rate": 0.15, "heu_leak_rate": 0.00}),
        ("heu_high_commit", "heu_like", {"heu_commitment_threshold": 0.80}),
        ("heu_low_commit", "heu_like", {"heu_commitment_threshold": 0.50}),
        ("hysteresis_default", "hysteresis", {}),
        ("hysteresis_tight", "hysteresis", {"hysteresis_off_ratio": 0.85}),
        ("hysteresis_loose", "hysteresis", {"hysteresis_off_ratio": 0.35}),
        ("hysteresis_low_threshold", "hysteresis", {"activation_threshold": 0.60}),
        ("hysteresis_high_threshold", "hysteresis", {"activation_threshold": 0.90}),
        ("hybrid_default", "hybrid_state_window", {}),
        ("hybrid_strict_local", "hybrid_state_window", {"hybrid_local_threshold_ratio": 0.95}),
        ("hybrid_loose_local", "hybrid_state_window", {"hybrid_local_threshold_ratio": 0.55}),
        ("hybrid_fast_decay", "hybrid_state_window", {"heu_recovery_rate": 0.60, "heu_leak_rate": 0.05}),
        ("hybrid_high_commit", "hybrid_state_window", {"heu_commitment_threshold": 0.80}),
        ("union_default", "union_state_window", {}),
        ("union_fast_decay", "union_state_window", {"heu_recovery_rate": 0.60, "heu_leak_rate": 0.05}),
        ("union_high_commit", "union_state_window", {"heu_commitment_threshold": 0.80}),
        ("union_low_threshold", "union_state_window", {"activation_threshold": 0.60}),
        ("union_top_intensity_pair", "union_state_window", {"event_decoder": "top_intensity_pair"}),
        ("union_frequent_subset_pair", "union_state_window", {"event_decoder": "frequent_subset_pair"}),
        ("union_consensus_pair", "union_state_window", {"event_decoder": "consensus_pair"}),
        (
            "union_consensus_fast_decay",
            "union_state_window",
            {"event_decoder": "consensus_pair", "heu_recovery_rate": 0.60, "heu_leak_rate": 0.05},
        ),
        (
            "sliding_low_consensus_pair",
            "sliding_window",
            {"activation_threshold": 0.60, "event_decoder": "consensus_pair"},
        ),
        (
            "sliding_low_temporal_consensus_pair",
            "sliding_window",
            {"activation_threshold": 0.60, "event_decoder": "temporal_consensus_pair"},
        ),
        (
            "hybrid_fast_consensus_pair",
            "hybrid_state_window",
            {"event_decoder": "consensus_pair", "heu_recovery_rate": 0.60, "heu_leak_rate": 0.05},
        ),
        (
            "hybrid_fast_temporal_consensus_pair",
            "hybrid_state_window",
            {"event_decoder": "temporal_consensus_pair", "heu_recovery_rate": 0.60, "heu_leak_rate": 0.05},
        ),
        (
            "union_temporal_consensus_pair",
            "union_state_window",
            {"event_decoder": "temporal_consensus_pair"},
        ),
        (
            "union_temporal_consensus_fast_decay",
            "union_state_window",
            {"event_decoder": "temporal_consensus_pair", "heu_recovery_rate": 0.60, "heu_leak_rate": 0.05},
        ),
    ]


def detector_environment_specs() -> list[tuple[str, str, dict[str, object]]]:
    return [
        ("branch_clean", "branch", {}),
        ("branch_dropout", "branch", {"dropout_probability": 0.05}),
        ("branch_spurious", "branch", {"spurious_probability": 0.05}),
        ("branch_window_blur", "branch", {"window_size": 4}),
        ("branch_low_threshold", "branch", {"activation_threshold": 0.60}),
        ("branch_high_threshold", "branch", {"activation_threshold": 1.05}),
        ("overlap_clean", "overlap", {}),
        ("overlap_dropout", "overlap", {"dropout_probability": 0.05}),
        ("overlap_spurious", "overlap", {"spurious_probability": 0.05}),
        ("overlap_window_blur", "overlap", {"window_size": 4}),
        ("hostile_unique", "hostile_unique", {}),
    ]


def run_detector_robustness_map(args: argparse.Namespace, output_dir: Path) -> None:
    rows: list[dict[str, object]] = []
    variants = detector_variant_specs()
    environments = detector_environment_specs()
    for env_index, (environment_id, world, environment_overrides) in enumerate(environments):
        for variant_index, (variant_id, detector, detector_overrides) in enumerate(variants):
            case_args = argparse.Namespace(**vars(args))
            case_args.seed = args.seed + 1000 + env_index * 100 + variant_index
            case_args.world = world
            case_args.detector = detector
            case_args.sweep = False
            case_args.compare_detectors = False
            case_args.detector_robustness_map = False
            for key, value in environment_overrides.items():
                setattr(case_args, key, value)
            for key, value in detector_overrides.items():
                setattr(case_args, key, value)
            result = execute_experiment(case_args)
            summary = summarize_detector_result(result, world, case_args.motif_repetitions)
            rows.append(
                {
                    "environment_id": environment_id,
                    "world": world,
                    "detector_variant": variant_id,
                    "detector": detector,
                    **summary,
                    "window_size": case_args.window_size,
                    "activation_threshold": case_args.activation_threshold,
                    "dropout_probability": case_args.dropout_probability,
                    "spurious_probability": case_args.spurious_probability,
                    "heu_attack_rate": case_args.heu_attack_rate,
                    "heu_recovery_rate": case_args.heu_recovery_rate,
                    "heu_leak_rate": case_args.heu_leak_rate,
                    "heu_commitment_threshold": case_args.heu_commitment_threshold,
                    "hysteresis_off_ratio": case_args.hysteresis_off_ratio,
                    "hybrid_local_threshold_ratio": case_args.hybrid_local_threshold_ratio,
                    "event_decoder": case_args.event_decoder,
                    "decoder_subset_size": case_args.decoder_subset_size,
                }
            )

    fieldnames = [
        "environment_id",
        "world",
        "detector_variant",
        "detector",
        "status",
        "failure_modes",
        "event_count",
        "transition_count",
        "motif_count",
        "canonical_motif_supports",
        "canonical_motif_recovery",
        "active_signal_cell_coverage_ratio",
        "active_signal_cell_overcapture_ratio",
        "event_history_accuracy",
        "event_context_accuracy",
        "collapsed_static_accuracy",
        "predictive_accuracy_delta",
        "compressibility_index",
        "recurring_three_event_window_fraction",
        "repeated_episode_instance_fraction",
        "window_size",
        "activation_threshold",
        "dropout_probability",
        "spurious_probability",
        "heu_attack_rate",
        "heu_recovery_rate",
        "heu_leak_rate",
        "heu_commitment_threshold",
        "hysteresis_off_ratio",
        "hybrid_local_threshold_ratio",
        "event_decoder",
        "decoder_subset_size",
    ]
    write_csv(output_dir / "detector_robustness_map.csv", rows, fieldnames)
    write_detector_robustness_report(output_dir / "detector_robustness_map.md", rows)


def robustness_score(row: dict[str, object]) -> float:
    status = str(row["status"])
    if status in ("faithful", "expected_collapse"):
        status_score = 1.0
    elif status in ("degraded", "partial_collapse"):
        status_score = 0.5
    else:
        status_score = 0.0
    motif_recovery = float(row["canonical_motif_recovery"])
    coverage = float(row["active_signal_cell_coverage_ratio"])
    coverage_score = max(0.0, 1.0 - abs(1.0 - coverage))
    event_history_accuracy = float(row["event_history_accuracy"])
    predictive_delta = max(0.0, float(row["predictive_accuracy_delta"]))
    return round(
        0.35 * status_score
        + 0.25 * motif_recovery
        + 0.20 * coverage_score
        + 0.10 * event_history_accuracy
        + 0.10 * min(1.0, predictive_delta),
        6,
    )


def pareto_dominated(
    candidate: dict[str, object],
    others: list[dict[str, object]],
    axes: tuple[str, ...],
) -> bool:
    candidate_values = tuple(float(candidate[axis]) for axis in axes)
    for other in others:
        if other is candidate:
            continue
        other_values = tuple(float(other[axis]) for axis in axes)
        at_least_as_good = all(
            other_value >= candidate_value
            for other_value, candidate_value in zip(other_values, candidate_values)
        )
        strictly_better = any(
            other_value > candidate_value
            for other_value, candidate_value in zip(other_values, candidate_values)
        )
        if at_least_as_good and strictly_better:
            return True
    return False


def run_dropout_spurious_pareto(args: argparse.Namespace, output_dir: Path) -> None:
    environments = [
        ("dropout", {"dropout_probability": 0.05, "spurious_probability": 0.0}),
        ("spurious", {"dropout_probability": 0.0, "spurious_probability": 0.05}),
        ("combined", {"dropout_probability": 0.05, "spurious_probability": 0.05}),
    ]
    worlds = ("branch", "overlap")
    variants = detector_variant_specs()
    per_environment_rows: list[dict[str, object]] = []
    aggregate: dict[tuple[str, str, str], dict[str, object]] = {}

    for world_index, world in enumerate(worlds):
        for environment_index, (environment_id, environment_overrides) in enumerate(environments):
            for variant_index, (variant_id, detector, detector_overrides) in enumerate(variants):
                case_args = argparse.Namespace(**vars(args))
                case_args.seed = args.seed + 2000 + world_index * 1000 + environment_index * 100 + variant_index
                case_args.world = world
                case_args.detector = detector
                case_args.sweep = False
                case_args.compare_detectors = False
                case_args.detector_robustness_map = False
                case_args.dropout_spurious_pareto = False
                for key, value in environment_overrides.items():
                    setattr(case_args, key, value)
                for key, value in detector_overrides.items():
                    setattr(case_args, key, value)
                result = execute_experiment(case_args)
                summary = summarize_detector_result(result, world, case_args.motif_repetitions)
                row = {
                    "world": world,
                    "environment": environment_id,
                    "detector_variant": variant_id,
                    "detector": detector,
                    "event_decoder": case_args.event_decoder,
                    "decoder_subset_size": case_args.decoder_subset_size,
                    **summary,
                    "score": 0.0,
                }
                row["score"] = robustness_score(row)
                per_environment_rows.append(row)

                key = (variant_id, detector, world)
                if key not in aggregate:
                    aggregate[key] = {
                        "detector_variant": variant_id,
                        "detector": detector,
                        "world": world,
                        "dropout_score": 0.0,
                        "spurious_score": 0.0,
                        "combined_score": 0.0,
                        "dropout_status": "",
                        "spurious_status": "",
                        "combined_status": "",
                    }
                aggregate_row = aggregate[key]
                aggregate_row[f"{environment_id}_score"] = row["score"]
                aggregate_row[f"{environment_id}_status"] = row["status"]

    aggregate_rows = list(aggregate.values())
    axes = ("dropout_score", "spurious_score", "combined_score")
    for row in aggregate_rows:
        row["pareto_dominated"] = pareto_dominated(row, aggregate_rows, axes)
        row["frontier"] = not row["pareto_dominated"]

    env_fieldnames = [
        "world",
        "environment",
        "detector_variant",
        "detector",
        "event_decoder",
        "decoder_subset_size",
        "status",
        "failure_modes",
        "score",
        "event_count",
        "motif_count",
        "canonical_motif_recovery",
        "active_signal_cell_coverage_ratio",
        "active_signal_cell_overcapture_ratio",
        "event_history_accuracy",
        "event_context_accuracy",
        "collapsed_static_accuracy",
        "predictive_accuracy_delta",
        "compressibility_index",
        "transition_count",
        "canonical_motif_supports",
        "event_context_accuracy",
        "collapsed_static_accuracy",
        "recurring_three_event_window_fraction",
        "repeated_episode_instance_fraction",
    ]
    write_csv(
        output_dir / "dropout_spurious_environment_scores.csv",
        per_environment_rows,
        env_fieldnames,
    )

    aggregate_fieldnames = [
        "world",
        "detector_variant",
        "detector",
        "dropout_score",
        "spurious_score",
        "combined_score",
        "dropout_status",
        "spurious_status",
        "combined_status",
        "frontier",
        "pareto_dominated",
    ]
    write_csv(
        output_dir / "dropout_spurious_pareto.csv",
        aggregate_rows,
        aggregate_fieldnames,
    )
    write_dropout_spurious_pareto_report(
        output_dir / "dropout_spurious_pareto.md",
        aggregate_rows,
    )


def write_dropout_spurious_pareto_report(
    path: Path,
    rows: list[dict[str, object]],
) -> None:
    lines = [
        "# Dropout-Spurious Pareto Frontier",
        "",
        "This adversary treats missing evidence and false evidence as opposing pressures.",
        "",
        "Scores combine status, motif recovery, coverage fidelity, event-history accuracy, and predictive delta. They are diagnostic, not final truth.",
        "",
        "## Frontier Variants",
        "",
    ]
    frontier_rows = [row for row in rows if row["frontier"]]
    for row in sorted(
        frontier_rows,
        key=lambda item: (
            str(item["world"]),
            -float(item["combined_score"]),
            str(item["detector_variant"]),
        ),
    ):
        lines.append(
            f"- `{row['world']}` `{row['detector_variant']}` "
            f"dropout={row['dropout_score']} spurious={row['spurious_score']} "
            f"combined={row['combined_score']} statuses="
            f"{row['dropout_status']}/{row['spurious_status']}/{row['combined_status']}"
        )

    lines.extend(["", "## Dominated Variants", ""])
    for row in sorted(
        [row for row in rows if row["pareto_dominated"]],
        key=lambda item: (str(item["world"]), str(item["detector_variant"])),
    ):
        lines.append(
            f"- `{row['world']}` `{row['detector_variant']}` "
            f"dropout={row['dropout_score']} spurious={row['spurious_score']} "
            f"combined={row['combined_score']}"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "A detector on the frontier is not globally best; it is not dominated across dropout robustness, spurious robustness, and combined robustness under this scoring function.",
            "",
            "The expected hard case is a detector that must bridge gaps without remembering false activity.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def temporal_decoder_seed_variant_specs() -> list[tuple[str, str, dict[str, object]]]:
    return [
        (
            "sliding_low_consensus_pair",
            "sliding_window",
            {"activation_threshold": 0.60, "event_decoder": "consensus_pair"},
        ),
        (
            "sliding_low_temporal_consensus_pair",
            "sliding_window",
            {"activation_threshold": 0.60, "event_decoder": "temporal_consensus_pair"},
        ),
        (
            "sliding_low_temporal_high_penalty",
            "sliding_window",
            {
                "activation_threshold": 0.60,
                "event_decoder": "temporal_consensus_pair",
                "temporal_decoder_overcommon_penalty_weight": 0.60,
            },
        ),
        (
            "sliding_low_temporal_weak_recurrence",
            "sliding_window",
            {
                "activation_threshold": 0.60,
                "event_decoder": "temporal_consensus_pair",
                "temporal_decoder_recurrence_weight": 0.20,
                "temporal_decoder_overcommon_penalty_weight": 0.60,
            },
        ),
        (
            "hybrid_fast_temporal_consensus_pair",
            "hybrid_state_window",
            {
                "event_decoder": "temporal_consensus_pair",
                "heu_recovery_rate": 0.60,
                "heu_leak_rate": 0.05,
            },
        ),
        (
            "union_temporal_consensus_pair",
            "union_state_window",
            {"event_decoder": "temporal_consensus_pair"},
        ),
        (
            "union_temporal_high_penalty",
            "union_state_window",
            {
                "event_decoder": "temporal_consensus_pair",
                "temporal_decoder_overcommon_penalty_weight": 0.60,
            },
        ),
        (
            "union_temporal_weak_recurrence",
            "union_state_window",
            {
                "event_decoder": "temporal_consensus_pair",
                "temporal_decoder_recurrence_weight": 0.20,
                "temporal_decoder_overcommon_penalty_weight": 0.60,
            },
        ),
        (
            "union_temporal_consensus_fast_decay",
            "union_state_window",
            {
                "event_decoder": "temporal_consensus_pair",
                "heu_recovery_rate": 0.60,
                "heu_leak_rate": 0.05,
            },
        ),
    ]


def run_temporal_decoder_seed_sweep(args: argparse.Namespace, output_dir: Path) -> None:
    seeds = (args.seed, args.seed + 101, args.seed + 202)
    worlds = ("branch", "overlap", "hostile_unique")
    variants = temporal_decoder_seed_variant_specs()
    rows: list[dict[str, object]] = []

    for seed_index, seed in enumerate(seeds):
        for world in worlds:
            for variant_id, detector, overrides in variants:
                case_args = argparse.Namespace(**vars(args))
                case_args.seed = seed
                case_args.world = world
                case_args.detector = detector
                case_args.dropout_probability = 0.05
                case_args.spurious_probability = 0.05
                case_args.sweep = False
                case_args.compare_detectors = False
                case_args.detector_robustness_map = False
                case_args.dropout_spurious_pareto = False
                case_args.temporal_decoder_seed_sweep = False
                for key, value in overrides.items():
                    setattr(case_args, key, value)
                result = execute_experiment(case_args)
                summary = summarize_detector_result(
                    result,
                    world,
                    case_args.motif_repetitions,
                )
                rows.append(
                    {
                        "seed_index": seed_index,
                        "seed": seed,
                        "world": world,
                        "detector_variant": variant_id,
                        "detector": detector,
                        "event_decoder": case_args.event_decoder,
                        "decoder_subset_size": case_args.decoder_subset_size,
                        **summary,
                        "motif_support_mass": round(
                            envelope_value(
                                result.information_envelope,
                                "motif_support_mass",
                            ),
                            6,
                        ),
                    }
                )

    fieldnames = [
        "seed_index",
        "seed",
        "world",
        "detector_variant",
        "detector",
        "event_decoder",
        "decoder_subset_size",
        "status",
        "failure_modes",
        "event_count",
        "transition_count",
        "motif_count",
        "motif_support_mass",
        "canonical_motif_supports",
        "canonical_motif_recovery",
        "active_signal_cell_coverage_ratio",
        "active_signal_cell_overcapture_ratio",
        "event_history_accuracy",
        "event_context_accuracy",
        "collapsed_static_accuracy",
        "predictive_accuracy_delta",
        "compressibility_index",
        "recurring_three_event_window_fraction",
        "repeated_episode_instance_fraction",
    ]
    write_csv(output_dir / "temporal_decoder_seed_sweep.csv", rows, fieldnames)
    write_temporal_decoder_seed_report(
        output_dir / "temporal_decoder_seed_sweep.md",
        rows,
    )


def write_temporal_decoder_seed_report(
    path: Path,
    rows: list[dict[str, object]],
) -> None:
    rows_by_world_variant: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        rows_by_world_variant[(str(row["world"]), str(row["detector_variant"]))].append(row)

    lines = [
        "# Temporal Decoder Seed Sweep",
        "",
        "This tests one-step temporal decoding under combined dropout+spurious corruption across three seeds.",
        "",
        "The temporal decoder can use the previous decoded event and the next candidate envelope, but it is not a general sequence model.",
        "",
        "## Combined Recurring Worlds",
        "",
    ]
    for world in ("branch", "overlap"):
        lines.append(f"### {world}")
        lines.append("")
        for variant_id, _detector, _overrides in temporal_decoder_seed_variant_specs():
            variant_rows = rows_by_world_variant[(world, variant_id)]
            if not variant_rows:
                continue
            motif_values = [float(row["canonical_motif_recovery"]) for row in variant_rows]
            history_values = [float(row["event_history_accuracy"]) for row in variant_rows]
            coverage_values = [
                float(row["active_signal_cell_coverage_ratio"])
                for row in variant_rows
            ]
            statuses = Counter(str(row["status"]) for row in variant_rows)
            lines.append(
                f"- `{variant_id}` statuses={dict(statuses)} "
                f"motif_mean={mean(motif_values):.6f} motif_min={min(motif_values):.6f} "
                f"history_mean={mean(history_values):.6f} "
                f"coverage_mean={mean(coverage_values):.6f}"
            )
        lines.append("")

    lines.extend(["## Hostile Mixed Controls", ""])
    for variant_id, _detector, _overrides in temporal_decoder_seed_variant_specs():
        variant_rows = rows_by_world_variant[("hostile_unique", variant_id)]
        if not variant_rows:
            continue
        compressibility_values = [
            float(row["compressibility_index"]) for row in variant_rows
        ]
        motif_counts = [int(row["motif_count"]) for row in variant_rows]
        support_values = [float(row["motif_support_mass"]) for row in variant_rows]
        recurring_values = [
            float(row["recurring_three_event_window_fraction"])
            for row in variant_rows
        ]
        statuses = Counter(str(row["status"]) for row in variant_rows)
        lines.append(
            f"- `{variant_id}` statuses={dict(statuses)} "
            f"compressibility_max={max(compressibility_values):.6f} "
            f"motif_count_max={max(motif_counts)} "
            f"motif_support_mass_max={max(support_values):.6f} "
            f"recurring_len3_max={max(recurring_values):.6f}"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "A temporal decoder is useful only if it improves recurring-world motif recovery across seeds without turning hostile unique episodes into reusable motifs.",
            "",
            "Passing hostile collapse requires more than low length-3 recurrence: motif count and motif support mass are tracked here because lower-level identity collapse can appear before full episode recurrence.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def motif_fault_tolerance_variant_specs() -> list[tuple[str, str, dict[str, object]]]:
    return [
        (
            "sliding_window_low_threshold",
            "sliding_window",
            {"activation_threshold": 0.60},
        ),
        (
            "sliding_low_consensus_pair",
            "sliding_window",
            {"activation_threshold": 0.60, "event_decoder": "consensus_pair"},
        ),
        (
            "sliding_low_temporal_consensus_pair",
            "sliding_window",
            {"activation_threshold": 0.60, "event_decoder": "temporal_consensus_pair"},
        ),
        (
            "hybrid_fast_temporal_consensus_pair",
            "hybrid_state_window",
            {
                "event_decoder": "temporal_consensus_pair",
                "heu_recovery_rate": 0.60,
                "heu_leak_rate": 0.05,
            },
        ),
        (
            "union_temporal_consensus_pair",
            "union_state_window",
            {"event_decoder": "temporal_consensus_pair"},
        ),
    ]


def run_motif_fault_tolerance_sweep(args: argparse.Namespace, output_dir: Path) -> None:
    seeds = (args.seed, args.seed + 101, args.seed + 202, args.seed + 303, args.seed + 404)
    worlds = ("branch", "overlap", "hostile_unique")
    variants = motif_fault_tolerance_variant_specs()
    rows: list[dict[str, object]] = []

    for seed_index, seed in enumerate(seeds):
        for world in worlds:
            for variant_id, detector, overrides in variants:
                case_args = argparse.Namespace(**vars(args))
                case_args.seed = seed
                case_args.world = world
                case_args.detector = detector
                case_args.dropout_probability = 0.05
                case_args.spurious_probability = 0.05
                case_args.sweep = False
                case_args.compare_detectors = False
                case_args.detector_robustness_map = False
                case_args.dropout_spurious_pareto = False
                case_args.temporal_decoder_seed_sweep = False
                case_args.motif_fault_tolerance_sweep = False
                for key, value in overrides.items():
                    setattr(case_args, key, value)

                result = execute_experiment(case_args)
                summary = summarize_detector_result(
                    result,
                    world,
                    case_args.motif_repetitions,
                )
                canonical_metrics = canonical_motif_metrics(
                    result.motifs,
                    canonical_motifs_for_world(world),
                )
                representation_gain = (
                    float(canonical_metrics["canonical_length3_support_fraction"])
                    - float(summary["canonical_motif_recovery"])
                )
                rows.append(
                    {
                        "seed_index": seed_index,
                        "seed": seed,
                        "world": world,
                        "detector_variant": variant_id,
                        "detector": detector,
                        "event_decoder": case_args.event_decoder,
                        **summary,
                        **canonical_metrics,
                        "representation_gain": round(representation_gain, 6),
                    }
                )

    fieldnames = [
        "seed_index",
        "seed",
        "world",
        "detector_variant",
        "detector",
        "event_decoder",
        "status",
        "failure_modes",
        "event_count",
        "transition_count",
        "motif_count",
        "canonical_motif_supports",
        "canonical_motif_recovery",
        "canonical_length3_supports",
        "canonical_length3_support_min",
        "canonical_length3_support_mass",
        "canonical_length3_support_fraction",
        "representation_gain",
        "canonical_length3_ranks",
        "canonical_length3_rank_worst",
        "length3_motif_support_mass",
        "length3_motif_count",
        "top5_length3_patterns",
        "active_signal_cell_coverage_ratio",
        "active_signal_cell_overcapture_ratio",
        "event_history_accuracy",
        "event_context_accuracy",
        "collapsed_static_accuracy",
        "predictive_accuracy_delta",
        "compressibility_index",
        "recurring_three_event_window_fraction",
        "repeated_episode_instance_fraction",
    ]
    write_csv(output_dir / "motif_fault_tolerance_sweep.csv", rows, fieldnames)
    write_motif_fault_tolerance_report(
        output_dir / "motif_fault_tolerance_findings.md",
        rows,
    )


def write_motif_fault_tolerance_report(
    path: Path,
    rows: list[dict[str, object]],
) -> None:
    rows_by_world_variant: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    top_sets_by_world_variant: dict[tuple[str, str], list[set[tuple[EventLabel, ...]]]] = defaultdict(list)
    for row in rows:
        key = (str(row["world"]), str(row["detector_variant"]))
        rows_by_world_variant[key].append(row)
        top_patterns = set()
        for pattern_text in str(row["top5_length3_patterns"]).split(" | "):
            if pattern_text:
                top_patterns.add(tuple(pattern_text.split(" -> ")))
        top_sets_by_world_variant[key].append(top_patterns)

    lines = [
        "# Motif Layer Fault Tolerance",
        "",
        "This experiment stops repairing the detector and asks whether the motif layer can stabilize reusable temporal structure from imperfect events.",
        "",
        "All recurring-world cases use combined dropout+spurious corruption. Hostile unique controls use the same corruption.",
        "",
        "## Recurring Worlds",
        "",
    ]

    for world in ("branch", "overlap"):
        lines.append(f"### {world}")
        lines.append("")
        for variant_id, _detector, _overrides in motif_fault_tolerance_variant_specs():
            variant_rows = rows_by_world_variant[(world, variant_id)]
            if not variant_rows:
                continue
            motif_recovery_values = [
                float(row["canonical_motif_recovery"]) for row in variant_rows
            ]
            support_fraction_values = [
                float(row["canonical_length3_support_fraction"])
                for row in variant_rows
            ]
            representation_gain_values = [
                float(row["representation_gain"]) for row in variant_rows
            ]
            rank_values = [
                int(row["canonical_length3_rank_worst"])
                for row in variant_rows
                if int(row["canonical_length3_rank_worst"]) > 0
            ]
            top_sets = top_sets_by_world_variant[(world, variant_id)]
            pairwise_jaccards = [
                jaccard_similarity(left, right)
                for left_index, left in enumerate(top_sets)
                for right in top_sets[left_index + 1 :]
            ]
            status_counts = Counter(str(row["status"]) for row in variant_rows)
            lines.append(
                f"- `{variant_id}` statuses={dict(status_counts)} "
                f"exact_recovery_mean={mean(motif_recovery_values):.6f} "
                f"exact_recovery_min={min(motif_recovery_values):.6f} "
                f"canonical_support_fraction_mean={mean(support_fraction_values):.6f} "
                f"representation_gain_mean={mean(representation_gain_values):.6f} "
                f"representation_gain_min={min(representation_gain_values):.6f} "
                f"worst_rank_max={max(rank_values) if rank_values else 0} "
                f"top5_jaccard_mean={mean(pairwise_jaccards) if pairwise_jaccards else 0.0:.6f}"
            )
        lines.append("")

    lines.extend(["## Hostile Unique Controls", ""])
    for variant_id, _detector, _overrides in motif_fault_tolerance_variant_specs():
        variant_rows = rows_by_world_variant[("hostile_unique", variant_id)]
        if not variant_rows:
            continue
        compressibility_values = [
            float(row["compressibility_index"]) for row in variant_rows
        ]
        motif_count_values = [int(row["motif_count"]) for row in variant_rows]
        support_mass_values = [
            float(row["length3_motif_support_mass"]) for row in variant_rows
        ]
        len3_values = [
            float(row["recurring_three_event_window_fraction"])
            for row in variant_rows
        ]
        lines.append(
            f"- `{variant_id}` compressibility_max={max(compressibility_values):.6f} "
            f"motif_count_max={max(motif_count_values)} "
            f"length3_support_mass_max={max(support_mass_values):.6f} "
            f"recurring_len3_max={max(len3_values):.6f}"
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "If the event-first hierarchy is fault tolerant, exact event recovery can be degraded while canonical motifs remain high-rank, high-support, and stable across seeds.",
            "",
            "`representation_gain = canonical_support_fraction - exact_recovery`. Positive gain means recurrence across episodes recovered more stable motif structure than exact event recovery alone exposed.",
            "",
            "If hostile unique worlds accumulate motif count or support mass, recurrence is being induced by event identity collapse rather than discovered in the world.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def run_null_ablation_package(args: argparse.Namespace, output_dir: Path) -> None:
    seeds = (args.seed, args.seed + 101, args.seed + 202)
    worlds = ("branch", "overlap")
    variants = (
        (
            "sliding_low_temporal_consensus_pair",
            "sliding_window",
            {"activation_threshold": 0.60, "event_decoder": "temporal_consensus_pair"},
        ),
        (
            "sliding_window_low_threshold",
            "sliding_window",
            {"activation_threshold": 0.60},
        ),
        (
            "union_temporal_consensus_pair",
            "union_state_window",
            {"event_decoder": "temporal_consensus_pair"},
        ),
    )
    null_models = (
        "observed",
        "within_episode_permuted",
        "episode_boundaries_permuted",
        "global_label_permuted",
    )
    rows: list[dict[str, object]] = []

    for seed_index, seed in enumerate(seeds):
        for world in worlds:
            canonical_motifs = canonical_motifs_for_world(world)
            for variant_id, detector, overrides in variants:
                case_args = argparse.Namespace(**vars(args))
                case_args.seed = seed
                case_args.world = world
                case_args.detector = detector
                case_args.dropout_probability = 0.05
                case_args.spurious_probability = 0.05
                case_args.sweep = False
                case_args.compare_detectors = False
                case_args.detector_robustness_map = False
                case_args.dropout_spurious_pareto = False
                case_args.temporal_decoder_seed_sweep = False
                case_args.motif_fault_tolerance_sweep = False
                case_args.null_ablation_package = False
                for key, value in overrides.items():
                    setattr(case_args, key, value)
                base_result = execute_experiment(case_args)

                for null_index, null_model in enumerate(null_models):
                    rng = np.random.default_rng(seed + null_index * 10_000)
                    null_events = transform_event_stream_null(
                        base_result.events,
                        null_model,
                        rng,
                    )
                    result = (
                        base_result
                        if null_model == "observed"
                        else rebuild_result_from_events(base_result, null_events, case_args)
                    )
                    summary = summarize_detector_result(
                        result,
                        world,
                        case_args.motif_repetitions,
                    )
                    motif_metrics = canonical_motif_metrics(
                        result.motifs,
                        canonical_motifs,
                    )
                    layer_metrics = canonical_layer_support_metrics(
                        result.events,
                        result.transitions,
                        canonical_motifs,
                    )
                    representation_gain = (
                        float(motif_metrics["canonical_length3_support_fraction"])
                        - float(summary["canonical_motif_recovery"])
                    )
                    motif_over_event_gain = (
                        float(motif_metrics["canonical_length3_support_fraction"])
                        - float(layer_metrics["canonical_event_support_fraction"])
                    )
                    motif_over_transition_gain = (
                        float(motif_metrics["canonical_length3_support_fraction"])
                        - float(layer_metrics["canonical_transition_support_fraction"])
                    )
                    rows.append(
                        {
                            "seed_index": seed_index,
                            "seed": seed,
                            "world": world,
                            "detector_variant": variant_id,
                            "detector": detector,
                            "event_decoder": case_args.event_decoder,
                            "null_model": null_model,
                            **summary,
                            **motif_metrics,
                            **layer_metrics,
                            "representation_gain": round(representation_gain, 6),
                            "motif_over_event_gain": round(motif_over_event_gain, 6),
                            "motif_over_transition_gain": round(
                                motif_over_transition_gain,
                                6,
                            ),
                        }
                    )

    fieldnames = [
        "seed_index",
        "seed",
        "world",
        "detector_variant",
        "detector",
        "event_decoder",
        "null_model",
        "status",
        "failure_modes",
        "event_count",
        "transition_count",
        "motif_count",
        "canonical_motif_supports",
        "canonical_motif_recovery",
        "canonical_length3_supports",
        "canonical_length3_support_min",
        "canonical_length3_support_mass",
        "canonical_length3_support_fraction",
        "representation_gain",
        "canonical_length3_ranks",
        "canonical_event_support_fraction",
        "canonical_transition_support_fraction",
        "canonical_event_support_mass",
        "canonical_transition_support_mass",
        "motif_over_event_gain",
        "motif_over_transition_gain",
        "canonical_length3_rank_worst",
        "length3_motif_support_mass",
        "length3_motif_count",
        "top5_length3_patterns",
        "active_signal_cell_coverage_ratio",
        "active_signal_cell_overcapture_ratio",
        "event_history_accuracy",
        "event_context_accuracy",
        "collapsed_static_accuracy",
        "predictive_accuracy_delta",
        "compressibility_index",
        "recurring_three_event_window_fraction",
        "repeated_episode_instance_fraction",
    ]
    write_csv(output_dir / "null_ablation_package.csv", rows, fieldnames)
    write_null_ablation_report(output_dir / "null_ablation_package.md", rows)


def write_null_ablation_report(path: Path, rows: list[dict[str, object]]) -> None:
    grouped: dict[tuple[str, str, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[
            (
                str(row["world"]),
                str(row["detector_variant"]),
                str(row["null_model"]),
            )
        ].append(row)

    lines = [
        "# Null And Ablation Package",
        "",
        "This tests whether Representation Gain disappears when temporal recurrence or event identity is selectively broken after detection.",
        "",
        "Nulls transform the detected event stream before transitions, episodes, and motifs are rebuilt.",
        "",
        "## Stronger Nulls",
        "",
    ]
    for world in ("branch", "overlap"):
        lines.append(f"### {world}")
        lines.append("")
        for variant_id in (
            "sliding_low_temporal_consensus_pair",
            "sliding_window_low_threshold",
            "union_temporal_consensus_pair",
        ):
            lines.append(f"#### {variant_id}")
            lines.append("")
            for null_model in (
                "observed",
                "within_episode_permuted",
                "episode_boundaries_permuted",
                "global_label_permuted",
            ):
                null_rows = grouped[(world, variant_id, null_model)]
                if not null_rows:
                    continue
                recovery_values = [
                    float(row["canonical_motif_recovery"]) for row in null_rows
                ]
                support_values = [
                    float(row["canonical_length3_support_fraction"])
                    for row in null_rows
                ]
                gain_values = [float(row["representation_gain"]) for row in null_rows]
                lines.append(
                    f"- `{null_model}` exact_mean={mean(recovery_values):.6f} "
                    f"support_fraction_mean={mean(support_values):.6f} "
                    f"gain_mean={mean(gain_values):.6f} "
                    f"gain_min={min(gain_values):.6f}"
                )
            lines.append("")

    lines.extend(["## Layer Ablations", ""])
    for world in ("branch", "overlap"):
        lines.append(f"### {world} observed streams")
        lines.append("")
        for variant_id in (
            "sliding_low_temporal_consensus_pair",
            "sliding_window_low_threshold",
            "union_temporal_consensus_pair",
        ):
            observed_rows = grouped[(world, variant_id, "observed")]
            if not observed_rows:
                continue
            event_values = [
                float(row["canonical_event_support_fraction"])
                for row in observed_rows
            ]
            transition_values = [
                float(row["canonical_transition_support_fraction"])
                for row in observed_rows
            ]
            motif_values = [
                float(row["canonical_length3_support_fraction"])
                for row in observed_rows
            ]
            motif_over_event_values = [
                float(row["motif_over_event_gain"]) for row in observed_rows
            ]
            motif_over_transition_values = [
                float(row["motif_over_transition_gain"]) for row in observed_rows
            ]
            lines.append(
                f"- `{variant_id}` event_fraction={mean(event_values):.6f} "
                f"transition_fraction={mean(transition_values):.6f} "
                f"motif_fraction={mean(motif_values):.6f} "
                f"motif_over_event={mean(motif_over_event_values):.6f} "
                f"motif_over_transition={mean(motif_over_transition_values):.6f}"
            )
        lines.append("")

    lines.extend(
        [
            "## Interpretation",
            "",
            "A strong result requires positive Representation Gain in observed recurring streams and collapse of that gain under selective temporal or identity nulls.",
            "",
            "Layer ablations compare whether canonical support is already present at the event/transition layer or is concentrated specifically by motifs.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def noise_grid_variant_specs() -> list[tuple[str, str, dict[str, object]]]:
    return [
        (
            "sliding_window_low_threshold",
            "sliding_window",
            {"activation_threshold": 0.60},
        ),
        (
            "sliding_low_temporal_consensus_pair",
            "sliding_window",
            {"activation_threshold": 0.60, "event_decoder": "temporal_consensus_pair"},
        ),
        (
            "union_temporal_consensus_pair",
            "union_state_window",
            {"event_decoder": "temporal_consensus_pair"},
        ),
    ]


def classify_noise_region(row: dict[str, object]) -> str:
    world = str(row["world"])
    if world == "hostile_unique":
        compressibility = float(row["compressibility_index"])
        support_mass = float(row["length3_motif_support_mass"])
        recurring_length3 = float(row["recurring_three_event_window_fraction"])
        if compressibility <= 0.05 and support_mass <= 0.0 and recurring_length3 <= 0.05:
            return "hostile_collapse"
        return "hostile_leak"

    coverage = float(row["active_signal_cell_coverage_ratio"])
    gain = float(row["representation_gain"])
    motif_fraction = float(row["canonical_length3_support_fraction"])
    event_fraction = float(row["canonical_event_support_fraction"])

    if coverage < 0.70:
        return "undercapture"
    if gain < 0.0 and event_fraction > motif_fraction:
        return "identity_collapse"
    if gain < 0.0:
        return "negative_gain"
    if motif_fraction < 0.50:
        return "identity_collapse"
    if gain > 0.0:
        return "positive_gain"
    return "borderline"


def run_representation_gain_noise_grid(args: argparse.Namespace, output_dir: Path) -> None:
    seeds = (args.seed, args.seed + 101, args.seed + 202)
    worlds = ("branch", "overlap", "hostile_unique")
    variants = noise_grid_variant_specs()
    dropout_values = (0.0, 0.05, 0.10, 0.15, 0.20)
    spurious_values = (0.0, 0.05, 0.10, 0.15, 0.20)
    rows: list[dict[str, object]] = []

    for seed_index, seed in enumerate(seeds):
        for world in worlds:
            canonical_motifs = canonical_motifs_for_world(world)
            for dropout_probability in dropout_values:
                for spurious_probability in spurious_values:
                    for variant_id, detector, overrides in variants:
                        case_args = argparse.Namespace(**vars(args))
                        case_args.seed = seed
                        case_args.world = world
                        case_args.detector = detector
                        case_args.dropout_probability = dropout_probability
                        case_args.spurious_probability = spurious_probability
                        case_args.sweep = False
                        case_args.compare_detectors = False
                        case_args.detector_robustness_map = False
                        case_args.dropout_spurious_pareto = False
                        case_args.temporal_decoder_seed_sweep = False
                        case_args.motif_fault_tolerance_sweep = False
                        case_args.null_ablation_package = False
                        case_args.representation_gain_noise_grid = False
                        for key, value in overrides.items():
                            setattr(case_args, key, value)

                        result = execute_experiment(case_args)
                        summary = summarize_detector_result(
                            result,
                            world,
                            case_args.motif_repetitions,
                        )
                        motif_metrics = canonical_motif_metrics(
                            result.motifs,
                            canonical_motifs,
                        )
                        layer_metrics = canonical_layer_support_metrics(
                            result.events,
                            result.transitions,
                            canonical_motifs,
                        )
                        representation_gain = (
                            float(motif_metrics["canonical_length3_support_fraction"])
                            - float(summary["canonical_motif_recovery"])
                        )
                        row = {
                            "seed_index": seed_index,
                            "seed": seed,
                            "world": world,
                            "detector_variant": variant_id,
                            "detector": detector,
                            "event_decoder": case_args.event_decoder,
                            "dropout_probability": dropout_probability,
                            "spurious_probability": spurious_probability,
                            **summary,
                            **motif_metrics,
                            **layer_metrics,
                            "representation_gain": round(representation_gain, 6),
                        }
                        row["noise_region"] = classify_noise_region(row)
                        rows.append(row)

    fieldnames = [
        "seed_index",
        "seed",
        "world",
        "detector_variant",
        "detector",
        "event_decoder",
        "dropout_probability",
        "spurious_probability",
        "noise_region",
        "status",
        "failure_modes",
        "event_count",
        "transition_count",
        "motif_count",
        "canonical_motif_supports",
        "canonical_motif_recovery",
        "canonical_length3_supports",
        "canonical_length3_support_min",
        "canonical_length3_support_mass",
        "canonical_length3_support_fraction",
        "representation_gain",
        "canonical_length3_ranks",
        "canonical_length3_rank_worst",
        "canonical_event_support_fraction",
        "canonical_transition_support_fraction",
        "canonical_event_support_mass",
        "canonical_transition_support_mass",
        "length3_motif_support_mass",
        "length3_motif_count",
        "top5_length3_patterns",
        "active_signal_cell_coverage_ratio",
        "active_signal_cell_overcapture_ratio",
        "event_history_accuracy",
        "event_context_accuracy",
        "collapsed_static_accuracy",
        "predictive_accuracy_delta",
        "compressibility_index",
        "recurring_three_event_window_fraction",
        "repeated_episode_instance_fraction",
    ]
    write_csv(output_dir / "representation_gain_noise_grid.csv", rows, fieldnames)
    write_representation_gain_noise_report(
        output_dir / "representation_gain_noise_envelope.md",
        rows,
        dropout_values,
        spurious_values,
    )


def aggregate_noise_rows(rows: list[dict[str, object]]) -> dict[str, object]:
    gain_values = [float(row["representation_gain"]) for row in rows]
    recovery_values = [float(row["canonical_motif_recovery"]) for row in rows]
    support_values = [
        float(row["canonical_length3_support_fraction"]) for row in rows
    ]
    coverage_values = [
        float(row["active_signal_cell_coverage_ratio"]) for row in rows
    ]
    region_counts = Counter(str(row["noise_region"]) for row in rows)
    return {
        "representation_gain_mean": mean(gain_values) if gain_values else 0.0,
        "representation_gain_min": min(gain_values) if gain_values else 0.0,
        "exact_recovery_mean": mean(recovery_values) if recovery_values else 0.0,
        "canonical_support_fraction_mean": (
            mean(support_values) if support_values else 0.0
        ),
        "coverage_mean": mean(coverage_values) if coverage_values else 0.0,
        "region": region_counts.most_common(1)[0][0] if region_counts else "none",
        "region_counts": dict(region_counts),
    }


def noise_region_symbol(region: str) -> str:
    symbols = {
        "positive_gain": "+",
        "negative_gain": "-",
        "identity_collapse": "I",
        "undercapture": "U",
        "hostile_collapse": "H",
        "hostile_leak": "L",
        "borderline": "B",
    }
    return symbols.get(region, "?")


def write_noise_grid_table(
    lines: list[str],
    rows: list[dict[str, object]],
    world: str,
    variant_id: str,
    dropout_values: tuple[float, ...],
    spurious_values: tuple[float, ...],
) -> None:
    lines.append(f"#### {world} / {variant_id}")
    lines.append("")
    lines.append("| dropout \\ spurious | " + " | ".join(f"{value:.2f}" for value in spurious_values) + " |")
    lines.append("| --- | " + " | ".join("---" for _ in spurious_values) + " |")
    for dropout_probability in dropout_values:
        cells: list[str] = []
        for spurious_probability in spurious_values:
            cell_rows = [
                row
                for row in rows
                if str(row["world"]) == world
                and str(row["detector_variant"]) == variant_id
                and float(row["dropout_probability"]) == dropout_probability
                and float(row["spurious_probability"]) == spurious_probability
            ]
            aggregate = aggregate_noise_rows(cell_rows)
            cells.append(noise_region_symbol(str(aggregate["region"])))
        lines.append(f"| {dropout_probability:.2f} | " + " | ".join(cells) + " |")
    lines.append("")


def write_representation_gain_noise_report(
    path: Path,
    rows: list[dict[str, object]],
    dropout_values: tuple[float, ...],
    spurious_values: tuple[float, ...],
) -> None:
    grouped: dict[tuple[str, str], list[dict[str, object]]] = defaultdict(list)
    cell_grouped: dict[tuple[str, str, float, float], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        key = (str(row["world"]), str(row["detector_variant"]))
        grouped[key].append(row)
        cell_grouped[
            (
                str(row["world"]),
                str(row["detector_variant"]),
                float(row["dropout_probability"]),
                float(row["spurious_probability"]),
            )
        ].append(row)

    lines = [
        "# Representation Gain Noise Envelope",
        "",
        "This grid varies dropout and spurious activation while holding the downstream event-first hierarchy fixed.",
        "",
        "Region symbols: `+` positive gain, `-` negative gain, `I` identity collapse, `U` undercapture, `H` hostile collapse, `L` hostile leak, `B` borderline.",
        "",
        "## Region Counts",
        "",
    ]

    for world in ("branch", "overlap", "hostile_unique"):
        lines.append(f"### {world}")
        lines.append("")
        for variant_id, _detector, _overrides in noise_grid_variant_specs():
            variant_rows = grouped[(world, variant_id)]
            if not variant_rows:
                continue
            aggregate = aggregate_noise_rows(variant_rows)
            lines.append(
                f"- `{variant_id}` region_counts={aggregate['region_counts']} "
                f"gain_mean={float(aggregate['representation_gain_mean']):.6f} "
                f"gain_min={float(aggregate['representation_gain_min']):.6f} "
                f"exact_mean={float(aggregate['exact_recovery_mean']):.6f} "
                f"support_mean={float(aggregate['canonical_support_fraction_mean']):.6f} "
                f"coverage_mean={float(aggregate['coverage_mean']):.6f}"
            )
        lines.append("")

    lines.extend(["## Envelope Maps", ""])
    for world in ("branch", "overlap", "hostile_unique"):
        lines.append(f"### {world}")
        lines.append("")
        for variant_id, _detector, _overrides in noise_grid_variant_specs():
            write_noise_grid_table(
                lines,
                rows,
                world,
                variant_id,
                dropout_values,
                spurious_values,
            )

    lines.extend(["## Cell Metrics", ""])
    for world in ("branch", "overlap"):
        lines.append(f"### {world}")
        lines.append("")
        for variant_id, _detector, _overrides in noise_grid_variant_specs():
            lines.append(f"#### {variant_id}")
            lines.append("")
            for dropout_probability in dropout_values:
                for spurious_probability in spurious_values:
                    cell_rows = cell_grouped[
                        (
                            world,
                            variant_id,
                            dropout_probability,
                            spurious_probability,
                        )
                    ]
                    aggregate = aggregate_noise_rows(cell_rows)
                    lines.append(
                        f"- dropout={dropout_probability:.2f} spurious={spurious_probability:.2f} "
                        f"region={aggregate['region']} "
                        f"gain_mean={float(aggregate['representation_gain_mean']):.6f} "
                        f"exact_mean={float(aggregate['exact_recovery_mean']):.6f} "
                        f"support_mean={float(aggregate['canonical_support_fraction_mean']):.6f} "
                        f"coverage_mean={float(aggregate['coverage_mean']):.6f}"
                    )
            lines.append("")

    lines.extend(
        [
            "## Interpretation",
            "",
            "The useful envelope is the region where exact event recovery degrades before canonical motif support does. Negative gain marks over-entropic identity collapse rather than useful compression.",
            "",
            "Hostile unique worlds are expected to remain in hostile collapse across the grid; hostile leak indicates recurrence induced by the detector/decoder rather than by the world.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def pair_label(prefix: str, index: int) -> tuple[UnitId, UnitId]:
    return (f"{prefix}{index:04d}a", f"{prefix}{index:04d}b")


def adversarial_case_sequences(
    case_id: str,
    episode_count: int,
    sequence_length: int,
    rng: np.random.Generator,
) -> tuple[list[tuple[tuple[UnitId, ...], ...]], list[str], list[str], str]:
    sequences: list[tuple[tuple[UnitId, ...], ...]] = []
    contexts: list[str] = []
    outcomes: list[str] = []

    if case_id == "unique_triplets":
        for episode_index in range(episode_count):
            sequences.append(
                tuple(
                    pair_label("A", episode_index * sequence_length + offset)
                    for offset in range(sequence_length)
                )
            )
            contexts.append(f"CTX_{episode_index:04d}")
            outcomes.append(f"OUT_{episode_index:04d}")
        return sequences, contexts, outcomes, "no_recurrence"

    if case_id == "shared_edges_unique_middle":
        for episode_index in range(episode_count):
            sequences.append(
                (("A", "B"),)
                + tuple(
                    pair_label("M", episode_index * sequence_length + offset)
                    for offset in range(max(0, sequence_length - 2))
                )
                + (("C", "D"),)
            )
            contexts.append(f"CTX_{episode_index:04d}")
            outcomes.append(f"OUT_{episode_index:04d}")
        return sequences, contexts, outcomes, "partial_recurrence_only"

    if case_id == "near_miss_drift":
        for episode_index in range(episode_count):
            sequence: list[tuple[UnitId, ...]] = [("A", "B")]
            previous_right = "B"
            for offset in range(max(0, sequence_length - 1)):
                next_right = f"C{episode_index:04d}_{offset:02d}"
                sequence.append((previous_right, next_right))
                previous_right = next_right
            sequences.append(tuple(sequence[:sequence_length]))
            contexts.append(f"CTX_{episode_index:04d}")
            outcomes.append(f"OUT_{episode_index:04d}")
        return sequences, contexts, outcomes, "partial_recurrence_only"

    if case_id == "hidden_novelty_alias_collision":
        base_sequence = tuple(
            (chr(ord("A") + offset), chr(ord("B") + offset))
            for offset in range(sequence_length)
        )
        for episode_index in range(episode_count):
            sequences.append(base_sequence)
            contexts.append(f"LATENT_CTX_{episode_index:04d}")
            outcomes.append(f"LATENT_OUT_{episode_index:04d}")
        return sequences, contexts, outcomes, "hidden_novelty"

    if case_id == "contradictory_outcomes":
        outcome_count = max(4, int(math.sqrt(episode_count)))
        base_sequence = tuple(
            (chr(ord("A") + offset), chr(ord("B") + offset))
            for offset in range(sequence_length)
        )
        for episode_index in range(episode_count):
            sequences.append(base_sequence)
            contexts.append("CTX_SHARED")
            outcomes.append(f"OUT_{episode_index % outcome_count:04d}")
        return sequences, contexts, outcomes, "outcome_contradiction"

    if case_id == "random_small_vocab":
        vocabulary = (
            ("A", "B"),
            ("B", "C"),
            ("C", "D"),
            ("D", "E"),
            ("E", "F"),
            ("F", "G"),
            ("G", "H"),
            ("H", "A"),
        )
        for episode_index in range(episode_count):
            sampled_indices = rng.integers(0, len(vocabulary), size=sequence_length)
            sequences.append(tuple(vocabulary[int(index)] for index in sampled_indices))
            contexts.append(f"CTX_{episode_index:04d}")
            outcomes.append(f"OUT_{episode_index:04d}")
        return sequences, contexts, outcomes, "chance_recurrence"

    if case_id == "uniform_branching":
        branch_events = (
            ("B", "C"),
            ("B", "E"),
            ("B", "G"),
            ("B", "I"),
            ("B", "K"),
            ("B", "M"),
        )
        suffix_events = (
            ("C", "D"),
            ("E", "F"),
            ("G", "H"),
            ("I", "J"),
            ("K", "L"),
            ("M", "N"),
        )
        for episode_index in range(episode_count):
            sequence = [("A", "B")]
            branch_index = 0
            suffix_index = 0
            for offset in range(max(0, sequence_length - 1)):
                branch_index = int(rng.integers(0, len(branch_events)))
                suffix_index = int(rng.integers(0, len(suffix_events)))
                sequence.append(
                    branch_events[branch_index]
                    if offset % 2 == 0
                    else suffix_events[suffix_index]
                )
            sequences.append(tuple(sequence[:sequence_length]))
            contexts.append("CTX_BRANCH")
            outcomes.append(f"OUT_{branch_index}_{suffix_index}")
        return sequences, contexts, outcomes, "high_branch_entropy"

    raise ValueError(f"unknown adversarial case: {case_id}")


def events_from_sequences(
    sequences: list[tuple[tuple[UnitId, ...], ...]],
    contexts: list[str],
    outcomes: list[str],
    event_duration: int,
    event_gap: int,
) -> list[Event]:
    events: list[Event] = []
    event_index = 0
    for episode_index, sequence in enumerate(sequences):
        episode_id = f"episode_{episode_index:05d}"
        for sequence_index, participants in enumerate(sequence):
            t_start = sequence_index * (event_duration + event_gap)
            event_index += 1
            events.append(
                Event(
                    event_id=f"event_{event_index:08d}",
                    episode_id=episode_id,
                    t_start=t_start,
                    t_end=t_start + event_duration,
                    participants=tuple(sorted(participants)),
                    intensities={unit_id: 1.0 for unit_id in participants},
                    context=contexts[episode_index],
                    source_window="adversarial:exact_event_stream",
                    outcome=outcomes[episode_index],
                )
            )
    return events


def motif_count_entropy(encoded_counts: tuple[str, ...]) -> float:
    counter: Counter[str] = Counter()
    for encoded in encoded_counts:
        if ":" not in encoded:
            continue
        label, count_text = encoded.rsplit(":", 1)
        counter[label] += int(count_text)
    return shannon_entropy(counter)


def motif_max_purity(encoded_counts: tuple[str, ...], support: int) -> float:
    counts: list[int] = []
    for encoded in encoded_counts:
        if ":" not in encoded:
            continue
        _label, count_text = encoded.rsplit(":", 1)
        counts.append(int(count_text))
    if support <= 0 or not counts:
        return 0.0
    return max(counts) / support


def summarize_adversarial_event_stream(
    case_id: str,
    scale_id: str,
    sequence_length: int,
    expectation: str,
    seed: int,
    events: list[Event],
    use_evidence_index_classifier: bool,
    args: argparse.Namespace,
) -> dict[str, object]:
    episodes = assemble_episodes(events)
    transitions = build_transitions(events, episodes)
    motif_lengths = tuple(sorted({1, 2, 3, sequence_length}))
    motifs = mine_motifs(events, episodes, motif_lengths=motif_lengths)
    pattern_evidence = (
        mine_pattern_evidence(
            events,
            episodes,
            pattern_lengths=motif_lengths,
        )
        if use_evidence_index_classifier
        else []
    )
    train_episode_ids, test_episode_ids = split_episodes(episodes, args.train_fraction)
    metrics = evaluate_prediction(events, episodes, train_episode_ids, test_episode_ids)
    envelope = quantify_information_envelope(
        raw_signals=[],
        events=events,
        transitions=transitions,
        episodes=episodes,
        motifs=motifs,
        activation_threshold=args.activation_threshold,
    )
    envelope_by_measure = {item.measure: item.value for item in envelope}
    length_three_motifs = [motif for motif in motifs if len(motif.pattern) == 3]
    full_sequence_motifs = [
        motif for motif in motifs if len(motif.pattern) == sequence_length
    ]
    length_three_evidence = [
        row for row in pattern_evidence if len(row.pattern) == 3 and row.support >= 2
    ]
    full_sequence_evidence = [
        row
        for row in pattern_evidence
        if len(row.pattern) == sequence_length and row.support >= 2
    ]
    length_three_status_counts = Counter(
        row.index_status for row in length_three_evidence
    )
    full_sequence_status_counts = Counter(
        row.index_status for row in full_sequence_evidence
    )
    total_length_three_windows = sum(
        max(0, len(episode.ordered_events) - 2) for episode in episodes
    )
    length_three_support_mass = sum(motif.support for motif in length_three_motifs)
    length_three_top_support = (
        max((motif.support for motif in length_three_motifs), default=0)
    )
    full_sequence_support_mass = sum(motif.support for motif in full_sequence_motifs)
    full_sequence_top_support = (
        max((motif.support for motif in full_sequence_motifs), default=0)
    )
    length_three_top_support_fraction = (
        length_three_top_support / total_length_three_windows
        if total_length_three_windows
        else 0.0
    )
    full_sequence_top_support_fraction = (
        full_sequence_top_support / len(episodes) if episodes else 0.0
    )
    recurring_full_sequence_fraction = (
        full_sequence_support_mass / len(episodes) if episodes else 0.0
    )
    outcome_purities = [
        motif_max_purity(motif.outcomes, motif.support)
        for motif in length_three_motifs
    ]
    context_purities = [
        motif_max_purity(motif.contexts, motif.support)
        for motif in length_three_motifs
    ]
    outcome_entropies = [
        motif_count_entropy(motif.outcomes) for motif in length_three_motifs
    ]
    context_entropies = [
        motif_count_entropy(motif.contexts) for motif in length_three_motifs
    ]
    recurring_length_three_fraction = (
        length_three_support_mass / total_length_three_windows
        if total_length_three_windows
        else 0.0
    )
    top_patterns = " | ".join(
        " -> ".join(motif.pattern)
        for motif in sorted(length_three_motifs, key=lambda item: item.support, reverse=True)[:5]
    )
    top_indexed_patterns = " | ".join(
        f"{' -> '.join(row.pattern)} [{row.index_status}]"
        for row in sorted(
            full_sequence_evidence,
            key=lambda item: (item.support, item.lift),
            reverse=True,
        )[:5]
    )

    novelty_failure = False
    failure_modes: list[str] = []
    if expectation == "no_recurrence" and recurring_length_three_fraction > 0.0:
        novelty_failure = True
        failure_modes.append("invented_length3_recurrence")
    if expectation == "no_recurrence" and recurring_full_sequence_fraction > 0.0:
        novelty_failure = True
        failure_modes.append("invented_full_sequence_recurrence")
    if expectation in {"hidden_novelty", "outcome_contradiction"}:
        if recurring_full_sequence_fraction >= 0.95:
            novelty_failure = True
            failure_modes.append("compressed_hidden_or_contradictory_novelty")
        if outcome_purities and max(outcome_purities) < 0.50:
            failure_modes.append("low_outcome_purity")
    if expectation == "chance_recurrence" and recurring_length_three_fraction > 0.50:
        novelty_failure = True
        failure_modes.append("chance_subsequence_recurrence_overcompressed")
    if expectation == "chance_recurrence" and recurring_full_sequence_fraction > 0.10:
        novelty_failure = True
        failure_modes.append("chance_full_sequence_recurrence_overcompressed")
    if expectation == "high_branch_entropy" and float(metrics["event_history_accuracy"]) < 0.40:
        failure_modes.append("low_predictive_utility")
    if expectation == "partial_recurrence_only" and length_three_top_support_fraction > 0.10:
        novelty_failure = True
        failure_modes.append("near_miss_or_partial_recurrence_overcompressed")

    evidence_index_failure = False
    evidence_failure_modes: list[str] = []
    resolved_statuses = {"retrieval_index", "episode_template_index"}
    if expectation in {"hidden_novelty", "outcome_contradiction"}:
        if any(row.index_status in resolved_statuses for row in full_sequence_evidence):
            evidence_index_failure = True
            evidence_failure_modes.append("ambiguous_signature_promoted_as_resolved")
    if expectation == "chance_recurrence":
        if any(row.index_status in resolved_statuses for row in length_three_evidence):
            evidence_index_failure = True
            evidence_failure_modes.append("chance_subsequence_promoted_as_resolved")
        if any(row.index_status in resolved_statuses for row in full_sequence_evidence):
            evidence_index_failure = True
            evidence_failure_modes.append("chance_full_sequence_promoted_as_resolved")

    return {
        "case_id": case_id,
        "scale_id": scale_id,
        "sequence_length": sequence_length,
        "classifier_mode": (
            "evidence_index" if use_evidence_index_classifier else "naive_recurrence"
        ),
        "seed": seed,
        "expectation": expectation,
        "episode_count": len(episodes),
        "event_count": len(events),
        "transition_count": len(transitions),
        "motif_count": len(motifs),
        "length3_motif_count": len(length_three_motifs),
        "length3_support_mass": length_three_support_mass,
        "length3_top_support": length_three_top_support,
        "length3_top_support_fraction": round(length_three_top_support_fraction, 6),
        "recurring_length3_fraction": round(recurring_length_three_fraction, 6),
        "full_sequence_motif_count": len(full_sequence_motifs),
        "full_sequence_support_mass": full_sequence_support_mass,
        "full_sequence_top_support": full_sequence_top_support,
        "full_sequence_top_support_fraction": round(full_sequence_top_support_fraction, 6),
        "recurring_full_sequence_fraction": round(recurring_full_sequence_fraction, 6),
        "length3_index_status_counts": ";".join(
            f"{status}:{count}" for status, count in sorted(length_three_status_counts.items())
        ),
        "full_sequence_index_status_counts": ";".join(
            f"{status}:{count}" for status, count in sorted(full_sequence_status_counts.items())
        ),
        "length3_background_recurrence_count": length_three_status_counts["background_recurrence"],
        "length3_ambiguous_evidence_count": length_three_status_counts["ambiguous_evidence"],
        "full_sequence_background_recurrence_count": full_sequence_status_counts[
            "background_recurrence"
        ],
        "full_sequence_ambiguous_evidence_count": full_sequence_status_counts[
            "ambiguous_evidence"
        ],
        "repeated_episode_instance_fraction": round(
            float(envelope_by_measure.get("repeated_episode_instance_fraction", 0.0)),
            6,
        ),
        "event_label_redundancy_fraction": round(
            float(envelope_by_measure.get("event_label_redundancy_fraction", 0.0)),
            6,
        ),
        "transition_redundancy_fraction": round(
            float(envelope_by_measure.get("transition_redundancy_fraction", 0.0)),
            6,
        ),
        "compressibility_index": round(
            float(envelope_by_measure.get("compressibility_index", 0.0)),
            6,
        ),
        "event_history_accuracy": round(float(metrics["event_history_accuracy"]), 6),
        "collapsed_static_accuracy": round(float(metrics["collapsed_static_accuracy"]), 6),
        "predictive_accuracy_delta": round(
            float(metrics["event_first_accuracy"])
            - float(metrics["collapsed_static_accuracy"]),
            6,
        ),
        "length3_outcome_purity_max": round(max(outcome_purities, default=0.0), 6),
        "length3_outcome_purity_mean": round(mean(outcome_purities) if outcome_purities else 0.0, 6),
        "length3_context_purity_max": round(max(context_purities, default=0.0), 6),
        "length3_context_purity_mean": round(mean(context_purities) if context_purities else 0.0, 6),
        "length3_outcome_entropy_max": round(max(outcome_entropies, default=0.0), 6),
        "length3_context_entropy_max": round(max(context_entropies, default=0.0), 6),
        "novelty_failure": novelty_failure,
        "failure_modes": ";".join(failure_modes),
        "evidence_index_failure": evidence_index_failure,
        "evidence_failure_modes": ";".join(evidence_failure_modes),
        "top5_length3_patterns": top_patterns,
        "top5_full_sequence_indexed_patterns": top_indexed_patterns,
    }


def run_adversarial_falsification_battery(args: argparse.Namespace, output_dir: Path) -> None:
    case_ids = (
        "unique_triplets",
        "shared_edges_unique_middle",
        "near_miss_drift",
        "hidden_novelty_alias_collision",
        "contradictory_outcomes",
        "random_small_vocab",
        "uniform_branching",
    )
    scales = (("small", 60), ("scaled", 600))
    sequence_lengths = (3, 5, 8)
    seeds = (args.seed, args.seed + 101, args.seed + 202)
    rows: list[dict[str, object]] = []
    signature_payload_records: list[dict[str, object]] = []
    classifier_mode = "evidence_index" if args.evidence_index_classifier else "naive_recurrence"

    for scale_id, episode_count in scales:
        for sequence_length in sequence_lengths:
            for case_id in case_ids:
                for seed in seeds:
                    rng = np.random.default_rng(seed)
                    sequences, contexts, outcomes, expectation = adversarial_case_sequences(
                        case_id,
                        episode_count,
                        sequence_length,
                        rng,
                    )
                    events = events_from_sequences(
                        sequences,
                        contexts,
                        outcomes,
                        args.event_duration,
                        args.event_gap,
                    )
                    motif_lengths = tuple(sorted({1, 2, 3, sequence_length}))
                    signature_payload_records.extend(
                        pattern_evidence_payload_records(
                            case_id=case_id,
                            scale_id=scale_id,
                            sequence_length=sequence_length,
                            classifier_mode=classifier_mode,
                            seed=seed,
                            pattern_evidence=mine_pattern_evidence(
                                events,
                                assemble_episodes(events),
                                motif_lengths,
                            ),
                            include_annotations=args.evidence_index_classifier,
                        )
                    )
                    rows.append(
                        summarize_adversarial_event_stream(
                            case_id,
                            scale_id,
                            sequence_length,
                            expectation,
                            seed,
                            events,
                            args.evidence_index_classifier,
                            args,
                        )
                    )

    fieldnames = [
        "case_id",
        "scale_id",
        "sequence_length",
        "classifier_mode",
        "seed",
        "expectation",
        "episode_count",
        "event_count",
        "transition_count",
        "motif_count",
        "length3_motif_count",
        "length3_support_mass",
        "length3_top_support",
        "length3_top_support_fraction",
        "recurring_length3_fraction",
        "full_sequence_motif_count",
        "full_sequence_support_mass",
        "full_sequence_top_support",
        "full_sequence_top_support_fraction",
        "recurring_full_sequence_fraction",
        "length3_index_status_counts",
        "full_sequence_index_status_counts",
        "length3_background_recurrence_count",
        "length3_ambiguous_evidence_count",
        "full_sequence_background_recurrence_count",
        "full_sequence_ambiguous_evidence_count",
        "repeated_episode_instance_fraction",
        "event_label_redundancy_fraction",
        "transition_redundancy_fraction",
        "compressibility_index",
        "event_history_accuracy",
        "collapsed_static_accuracy",
        "predictive_accuracy_delta",
        "length3_outcome_purity_max",
        "length3_outcome_purity_mean",
        "length3_context_purity_max",
        "length3_context_purity_mean",
        "length3_outcome_entropy_max",
        "length3_context_entropy_max",
        "novelty_failure",
        "failure_modes",
        "evidence_index_failure",
        "evidence_failure_modes",
        "top5_length3_patterns",
        "top5_full_sequence_indexed_patterns",
    ]
    output_suffix = "evidence_index" if args.evidence_index_classifier else "naive"
    write_csv(
        output_dir / f"adversarial_falsification_battery_{output_suffix}.csv",
        rows,
        fieldnames,
    )
    write_jsonl(
        output_dir / f"signature_index_payloads_{output_suffix}.jsonl",
        signature_payload_records,
    )
    write_adversarial_falsification_report(
        output_dir / f"adversarial_falsification_findings_{output_suffix}.md",
        rows,
        classifier_mode=output_suffix,
    )


def write_adversarial_falsification_report(
    path: Path,
    rows: list[dict[str, object]],
    classifier_mode: str,
) -> None:
    grouped: dict[tuple[str, int, str], list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        grouped[
            (
                str(row["scale_id"]),
                int(row["sequence_length"]),
                str(row["case_id"]),
            )
        ].append(row)

    lines = [
        "# Adversarial Falsification Battery",
        "",
        "This battery tries to break the event-first hierarchy after event identity has already been discretized. That means failures here are not detector failures; they are representation, novelty-gate, or metric failures.",
        "",
        f"Classifier mode: `{classifier_mode}`.",
        "",
        "## Summary",
        "",
    ]
    for scale_id in ("small", "scaled"):
        for sequence_length in (3, 5, 8):
            lines.append(f"### {scale_id} length {sequence_length}")
            lines.append("")
            for case_id in (
                "unique_triplets",
                "shared_edges_unique_middle",
                "near_miss_drift",
                "hidden_novelty_alias_collision",
                "contradictory_outcomes",
                "random_small_vocab",
                "uniform_branching",
            ):
                case_rows = grouped[(scale_id, sequence_length, case_id)]
                if not case_rows:
                    continue
                failure_count = sum(1 for row in case_rows if str(row["novelty_failure"]) == "True")
                evidence_failure_count = sum(
                    1 for row in case_rows if str(row["evidence_index_failure"]) == "True"
                )
                recurring_values = [float(row["recurring_length3_fraction"]) for row in case_rows]
                full_recurring_values = [
                    float(row["recurring_full_sequence_fraction"]) for row in case_rows
                ]
                compressibility_values = [float(row["compressibility_index"]) for row in case_rows]
                history_values = [float(row["event_history_accuracy"]) for row in case_rows]
                outcome_purity_values = [float(row["length3_outcome_purity_max"]) for row in case_rows]
                failure_modes = Counter(
                    mode
                    for row in case_rows
                    for mode in str(row["failure_modes"]).split(";")
                    if mode
                )
                evidence_failure_modes = Counter(
                    mode
                    for row in case_rows
                    for mode in str(row["evidence_failure_modes"]).split(";")
                    if mode
                )
                full_status_counts = Counter()
                length_three_status_counts = Counter()
                for row in case_rows:
                    for encoded_count in str(row["full_sequence_index_status_counts"]).split(";"):
                        if ":" not in encoded_count:
                            continue
                        status, count_text = encoded_count.rsplit(":", 1)
                        full_status_counts[status] += int(count_text)
                    for encoded_count in str(row["length3_index_status_counts"]).split(";"):
                        if ":" not in encoded_count:
                            continue
                        status, count_text = encoded_count.rsplit(":", 1)
                        length_three_status_counts[status] += int(count_text)
                lines.append(
                    f"- `{case_id}` expectation={case_rows[0]['expectation']} "
                    f"naive_failures={failure_count}/{len(case_rows)} "
                    f"evidence_index_failures={evidence_failure_count}/{len(case_rows)} "
                    f"len3_mean={mean(recurring_values):.6f} "
                    f"full_sequence_mean={mean(full_recurring_values):.6f} "
                    f"compressibility_mean={mean(compressibility_values):.6f} "
                    f"history_accuracy_mean={mean(history_values):.6f} "
                    f"outcome_purity_max_mean={mean(outcome_purity_values):.6f} "
                    f"failure_modes={dict(failure_modes)} "
                    f"evidence_failure_modes={dict(evidence_failure_modes)} "
                    f"len3_index_statuses={dict(length_three_status_counts)} "
                    f"full_index_statuses={dict(full_status_counts)}"
                )
            lines.append("")

    lines.extend(["## Failure Interpretation", ""])
    lines.extend(
        [
            "- `hidden_novelty_alias_collision` is an information-theoretic failure: if distinct latent episodes project to the same event identity, the current representation compresses them as one motif.",
            "- `contradictory_outcomes` shows that recurrence alone is insufficient; a motif can be structurally stable while carrying low outcome purity.",
            "- `random_small_vocab` attacks support-count novelty gating. At scale, chance recurrence becomes expected and support >= 2 is not a sufficient motif criterion.",
            "- `shared_edges_unique_middle` and `near_miss_drift` check whether partial overlap is incorrectly promoted to full length-3 recurrence.",
            "- `unique_triplets` remains the clean hostile control: any length-3 recurrence there is invented by the representation itself.",
        ]
    )
    lines.extend(["", "## Layer Decomposition", ""])
    for scale_id in ("small", "scaled"):
        for sequence_length in (3, 5, 8):
            lines.append(f"### {scale_id} length {sequence_length}")
            lines.append("")
            lines.append(
                "| case | event redundancy | transition redundancy | repeated episodes | length-3 recurrence | full-sequence recurrence | outcome purity max | history accuracy |"
            )
            lines.append("| --- | --- | --- | --- | --- | --- | --- | --- |")
            for case_id in (
                "unique_triplets",
                "shared_edges_unique_middle",
                "near_miss_drift",
                "hidden_novelty_alias_collision",
                "contradictory_outcomes",
                "random_small_vocab",
                "uniform_branching",
            ):
                case_rows = grouped[(scale_id, sequence_length, case_id)]
                if not case_rows:
                    continue
                event_redundancy = mean(
                    float(row["event_label_redundancy_fraction"]) for row in case_rows
                )
                transition_redundancy = mean(
                    float(row["transition_redundancy_fraction"]) for row in case_rows
                )
                repeated_episodes = mean(
                    float(row["repeated_episode_instance_fraction"]) for row in case_rows
                )
                length_three_recurrence = mean(
                    float(row["recurring_length3_fraction"]) for row in case_rows
                )
                full_sequence_recurrence = mean(
                    float(row["recurring_full_sequence_fraction"]) for row in case_rows
                )
                outcome_purity = mean(
                    float(row["length3_outcome_purity_max"]) for row in case_rows
                )
                history_accuracy = mean(
                    float(row["event_history_accuracy"]) for row in case_rows
                )
                lines.append(
                    f"| `{case_id}` | {event_redundancy:.6f} | {transition_redundancy:.6f} | "
                    f"{repeated_episodes:.6f} | {length_three_recurrence:.6f} | "
                    f"{full_sequence_recurrence:.6f} | {outcome_purity:.6f} | "
                    f"{history_accuracy:.6f} |"
                )
            lines.append("")

    lines.extend(["## Sequence-Length Effects", ""])
    for scale_id in ("small", "scaled"):
        lines.append(f"### {scale_id}")
        lines.append("")
        lines.append(
            "| case | len3 recurrence at 3/5/8 | full recurrence at 3/5/8 |"
        )
        lines.append("| --- | --- | --- |")
        for case_id in (
            "unique_triplets",
            "shared_edges_unique_middle",
            "near_miss_drift",
            "hidden_novelty_alias_collision",
            "contradictory_outcomes",
            "random_small_vocab",
            "uniform_branching",
        ):
            len3_values: list[str] = []
            full_values: list[str] = []
            for sequence_length in (3, 5, 8):
                case_rows = grouped[(scale_id, sequence_length, case_id)]
                if not case_rows:
                    continue
                len3_values.append(
                    f"{mean(float(row['recurring_length3_fraction']) for row in case_rows):.6f}"
                )
                full_values.append(
                    f"{mean(float(row['recurring_full_sequence_fraction']) for row in case_rows):.6f}"
                )
            lines.append(
                f"| `{case_id}` | {' / '.join(len3_values)} | {' / '.join(full_values)} |"
            )
        lines.append("")

    lines.extend(["## Scale Effects", ""])
    for case_id in (
        "unique_triplets",
        "shared_edges_unique_middle",
        "near_miss_drift",
        "hidden_novelty_alias_collision",
        "contradictory_outcomes",
        "random_small_vocab",
        "uniform_branching",
    ):
        small_rows = grouped[("small", 3, case_id)]
        scaled_rows = grouped[("scaled", 3, case_id)]
        if not small_rows or not scaled_rows:
            continue
        small_recurrence = mean(
            float(row["recurring_length3_fraction"]) for row in small_rows
        )
        scaled_recurrence = mean(
            float(row["recurring_length3_fraction"]) for row in scaled_rows
        )
        small_compressibility = mean(
            float(row["compressibility_index"]) for row in small_rows
        )
        scaled_compressibility = mean(
            float(row["compressibility_index"]) for row in scaled_rows
        )
        lines.append(
            f"- `{case_id}` length3_delta={scaled_recurrence - small_recurrence:.6f} "
            f"compressibility_delta={scaled_compressibility - small_compressibility:.6f}"
        )

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_detector_robustness_report(path: Path, rows: list[dict[str, object]]) -> None:
    detector_counts: dict[str, Counter[str]] = defaultdict(Counter)
    environment_counts: dict[str, Counter[str]] = defaultdict(Counter)
    variant_counts: dict[str, Counter[str]] = defaultdict(Counter)
    hostile_rows: list[dict[str, object]] = []
    for row in rows:
        detector_counts[str(row["detector"])][str(row["status"])] += 1
        environment_counts[str(row["environment_id"])][str(row["status"])] += 1
        variant_counts[str(row["detector_variant"])][str(row["status"])] += 1
        if row["world"] == "hostile_unique":
            hostile_rows.append(row)

    lines = [
        "# Detector Robustness Map",
        "",
        "This maps detector family x hyperparameter variant x environment using the same downstream event-first representation.",
        "",
        "The central metric is faithful operating envelope size, with hostile unique worlds expected to collapse rather than compress.",
        "",
        "## Detector Family Status Counts",
        "",
    ]
    for detector in sorted(detector_counts):
        counts = detector_counts[detector]
        lines.append(
            f"- `{detector}`: faithful={counts['faithful']} degraded={counts['degraded']} "
            f"failed={counts['failed']} expected_collapse={counts['expected_collapse']} "
            f"suspicious={counts['suspicious_compression']}"
        )

    lines.extend(["", "## Environment Status Counts", ""])
    for environment_id in sorted(environment_counts):
        counts = environment_counts[environment_id]
        lines.append(
            f"- `{environment_id}`: faithful={counts['faithful']} degraded={counts['degraded']} "
            f"failed={counts['failed']} expected_collapse={counts['expected_collapse']} "
            f"suspicious={counts['suspicious_compression']}"
        )

    lines.extend(["", "## Variant Status Counts", ""])
    for variant_id in sorted(variant_counts):
        counts = variant_counts[variant_id]
        lines.append(
            f"- `{variant_id}`: faithful={counts['faithful']} degraded={counts['degraded']} "
            f"failed={counts['failed']} expected_collapse={counts['expected_collapse']} "
            f"suspicious={counts['suspicious_compression']}"
        )

    lines.extend(["", "## Hostile Controls", ""])
    suspicious = [
        row for row in hostile_rows if row["status"] != "expected_collapse"
    ]
    if suspicious:
        lines.append("Hostile controls did not all collapse:")
        for row in suspicious:
            lines.append(
                f"- `{row['detector_variant']}` status={row['status']} "
                f"compressibility={row['compressibility_index']}"
            )
    else:
        lines.append("All hostile unique detector variants collapsed as expected.")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "Detector families define different event vocabularies and operating regions. A useful family is not the one with the highest prediction alone, but the one that expands faithful compression while preserving hostile collapse.",
            "",
            "If different families succeed on the same environments, evidence shifts toward the downstream event-first representation. If only one family succeeds, capability is localized to detector dynamics.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Event-first memory experiment over synthetic coactivation traces."
    )
    parser.add_argument("--output-dir", default="outputs")
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument(
        "--detector",
        choices=(
            "sliding_window",
            "heu_like",
            "hysteresis",
            "hybrid_state_window",
            "union_state_window",
        ),
        default="sliding_window",
    )
    parser.add_argument(
        "--world",
        choices=("branch", "overlap", "hostile_unique"),
        default="branch",
    )
    parser.add_argument("--motif-repetitions", type=int, default=60)
    parser.add_argument("--noise-episodes", type=int, default=20)
    parser.add_argument("--event-duration", type=int, default=3)
    parser.add_argument("--event-gap", type=int, default=2)
    parser.add_argument("--window-size", type=int, default=3)
    parser.add_argument("--activation-threshold", type=float, default=0.75)
    parser.add_argument("--active-mean", type=float, default=1.0)
    parser.add_argument("--active-std", type=float, default=0.05)
    parser.add_argument("--baseline-mean", type=float, default=0.03)
    parser.add_argument("--baseline-std", type=float, default=0.01)
    parser.add_argument("--dropout-probability", type=float, default=0.0)
    parser.add_argument("--spurious-probability", type=float, default=0.0)
    parser.add_argument("--heu-attack-rate", type=float, default=0.80)
    parser.add_argument("--heu-recovery-rate", type=float, default=0.35)
    parser.add_argument("--heu-leak-rate", type=float, default=0.02)
    parser.add_argument("--heu-commitment-threshold", type=float, default=0.65)
    parser.add_argument("--hysteresis-off-ratio", type=float, default=0.55)
    parser.add_argument("--hybrid-local-threshold-ratio", type=float, default=0.75)
    parser.add_argument(
        "--event-decoder",
        choices=(
            "none",
            "top_intensity_pair",
            "frequent_subset_pair",
            "consensus_pair",
            "temporal_consensus_pair",
        ),
        default="none",
    )
    parser.add_argument("--decoder-subset-size", type=int, default=2)
    parser.add_argument("--temporal-decoder-intensity-weight", type=float, default=1.0)
    parser.add_argument("--temporal-decoder-recurrence-weight", type=float, default=0.8)
    parser.add_argument("--temporal-decoder-prev-transition-weight", type=float, default=1.2)
    parser.add_argument("--temporal-decoder-next-transition-weight", type=float, default=0.8)
    parser.add_argument("--temporal-decoder-next-overlap-weight", type=float, default=0.4)
    parser.add_argument("--temporal-decoder-overcommon-penalty-weight", type=float, default=0.15)
    parser.add_argument("--min-participants", type=int, default=2)
    parser.add_argument("--train-fraction", type=float, default=0.7)
    parser.add_argument("--sweep", action="store_true")
    parser.add_argument("--compare-detectors", action="store_true")
    parser.add_argument("--detector-robustness-map", action="store_true")
    parser.add_argument("--dropout-spurious-pareto", action="store_true")
    parser.add_argument("--temporal-decoder-seed-sweep", action="store_true")
    parser.add_argument("--motif-fault-tolerance-sweep", action="store_true")
    parser.add_argument("--null-ablation-package", action="store_true")
    parser.add_argument("--representation-gain-noise-grid", action="store_true")
    parser.add_argument("--adversarial-falsification-battery", action="store_true")
    parser.add_argument("--evidence-index-classifier", action="store_true")
    return parser.parse_args()


def main() -> None:
    output_dir = run_experiment(parse_args())
    print(f"Wrote event-first experiment artifacts to {output_dir.resolve()}")


if __name__ == "__main__":
    main()
