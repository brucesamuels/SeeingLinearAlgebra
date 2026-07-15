"""Focused tests for Checkpoint 26 labeled presentation integration."""

from __future__ import annotations

import numpy as np
import pytest

pytest.importorskip("manim")

from manim import DecimalNumber, Scene, VGroup, ValueTracker

from engine.manim_linear_combination_labels import ManimLinearCombinationLabels
from engine.manim_linear_combination_presentation import (
    ManimLinearCombinationPresentation,
)
from engine.manim_linear_combination_trace import ManimLinearCombinationTrace
from scenes.linear_combination_presentation_smoke import (
    LinearCombinationPresentationSmoke,
    SMOKE_RESULTANT_LABEL,
    SMOKE_RESULTANT_LABEL_OFFSET,
    SMOKE_TERM_LABELS,
    SMOKE_TERM_LABEL_OFFSETS,
    SMOKE_VECTORS,
    build_linear_combination_presentation_smoke_pipeline,
    update_labeled_linear_combination_from_tracker,
    update_labeled_linear_combination_presentation,
)


def _entry_values(entries: tuple[DecimalNumber, ...]) -> np.ndarray:
    return np.array([entry.get_value() for entry in entries], dtype=float)


def _label_centers(
    labels: ManimLinearCombinationLabels,
) -> tuple[np.ndarray, ...]:
    return tuple(
        np.asarray(label.get_center(), dtype=float)
        for label in (
            *labels.term_label_mobjects,
            labels.resultant_label_mobject,
        )
    )


def _embedded_midpoint(segment: np.ndarray) -> np.ndarray:
    midpoint = np.mean(np.asarray(segment, dtype=float), axis=0)
    result = np.zeros(3, dtype=float)
    result[: midpoint.size] = midpoint
    return result


def test_labeled_smoke_scene_remains_a_manim_scene() -> None:
    assert issubclass(LinearCombinationPresentationSmoke, Scene)


def test_scene_label_configuration_matches_the_smoke_vector_count() -> None:
    assert len(SMOKE_TERM_LABELS) == SMOKE_VECTORS.shape[0]
    assert all(isinstance(source, str) and source.strip() for source in SMOKE_TERM_LABELS)
    assert len(SMOKE_TERM_LABEL_OFFSETS) == SMOKE_VECTORS.shape[0]
    assert all(len(offset) in (2, 3) for offset in SMOKE_TERM_LABEL_OFFSETS)
    assert isinstance(SMOKE_RESULTANT_LABEL, str)
    assert SMOKE_RESULTANT_LABEL.strip()
    assert len(SMOKE_RESULTANT_LABEL_OFFSET) in (2, 3)


def test_actual_presentation_and_labels_consume_one_initial_snapshot() -> None:
    pipeline = build_linear_combination_presentation_smoke_pipeline()
    initial = pipeline.display_path.snapshot(0.0)

    presentation = ManimLinearCombinationPresentation(initial)
    labels = ManimLinearCombinationLabels(
        initial,
        term_labels=SMOKE_TERM_LABELS,
        resultant_label=SMOKE_RESULTANT_LABEL,
    )

    assert presentation.snapshot is initial
    assert labels.snapshot is initial
    assert labels.term_count == presentation.vector_count
    assert labels.display_dimension == presentation.display_dimension
    assert labels.term_label_sources == SMOKE_TERM_LABELS
    assert labels.resultant_label_source == SMOKE_RESULTANT_LABEL


def test_labeled_update_queries_display_path_exactly_once_and_shares_snapshot() -> None:
    display_snapshot = object()

    class DisplayPathSpy:
        def __init__(self) -> None:
            self.received_progress: list[float] = []

        def snapshot(self, progress: float) -> object:
            self.received_progress.append(progress)
            return display_snapshot

    class AdapterSpy:
        def __init__(self) -> None:
            self.received_snapshots: list[object] = []

        def update_from_snapshot(self, snapshot: object) -> AdapterSpy:
            self.received_snapshots.append(snapshot)
            return self

    presentation = AdapterSpy()
    labels = AdapterSpy()
    display_path = DisplayPathSpy()

    returned = update_labeled_linear_combination_presentation(
        presentation,  # type: ignore[arg-type]
        labels,  # type: ignore[arg-type]
        display_path,  # type: ignore[arg-type]
        0.375,
    )

    assert returned is presentation
    assert display_path.received_progress == [pytest.approx(0.375)]
    assert presentation.received_snapshots == [display_snapshot]
    assert labels.received_snapshots == [display_snapshot]


def test_labeled_update_synchronizes_geometry_readout_and_label_positions() -> None:
    pipeline = build_linear_combination_presentation_smoke_pipeline()
    initial = pipeline.display_path.snapshot(0.0)
    presentation = ManimLinearCombinationPresentation(initial)
    labels = ManimLinearCombinationLabels(
        initial,
        term_labels=SMOKE_TERM_LABELS,
        resultant_label=SMOKE_RESULTANT_LABEL,
        term_label_offsets=SMOKE_TERM_LABEL_OFFSETS,
        resultant_label_offset=SMOKE_RESULTANT_LABEL_OFFSET,
    )
    returned = update_labeled_linear_combination_presentation(
        presentation,
        labels,
        pipeline.display_path,
        1.0,
    )

    final = presentation.snapshot
    assert returned is presentation
    assert labels.snapshot is final
    assert presentation.readout.snapshot is final.linear_combination_snapshot

    np.testing.assert_allclose(
        presentation.geometry.resultant_arrow.get_end(),
        [*final.display_resultant_end, 0.0],
    )
    np.testing.assert_allclose(
        _entry_values(presentation.readout.coefficient_entries),
        final.linear_combination_snapshot.coefficients,
    )
    np.testing.assert_allclose(
        _entry_values(presentation.readout.result_entries),
        final.linear_combination_snapshot.result,
    )

    expected_term_centers = tuple(
        _embedded_midpoint(segment) + offset
        for segment, offset in zip(
            final.display_term_segments,
            labels.term_label_offsets,
            strict=True,
        )
    )
    expected_resultant_center = (
        _embedded_midpoint(final.display_resultant_segment)
        + labels.resultant_label_offset
    )
    expected_centers = (*expected_term_centers, expected_resultant_center)

    for actual, expected in zip(
        _label_centers(labels),
        expected_centers,
        strict=True,
    ):
        np.testing.assert_allclose(actual, expected)


def test_labeled_update_preserves_all_moving_mobject_identities() -> None:
    pipeline = build_linear_combination_presentation_smoke_pipeline()
    initial = pipeline.display_path.snapshot(0.0)
    presentation = ManimLinearCombinationPresentation(initial)
    labels = ManimLinearCombinationLabels(
        initial,
        term_labels=SMOKE_TERM_LABELS,
        resultant_label=SMOKE_RESULTANT_LABEL,
    )
    identities = {
        "presentation": id(presentation),
        "geometry": id(presentation.geometry),
        "term_arrows": tuple(
            id(arrow) for arrow in presentation.geometry.term_arrows
        ),
        "resultant_arrow": id(presentation.geometry.resultant_arrow),
        "readout": id(presentation.readout),
        "coefficient_entries": tuple(
            id(entry) for entry in presentation.readout.coefficient_entries
        ),
        "result_entries": tuple(
            id(entry) for entry in presentation.readout.result_entries
        ),
        "labels": id(labels),
        "term_labels": tuple(id(label) for label in labels.term_label_mobjects),
        "resultant_label": id(labels.resultant_label_mobject),
    }

    update_labeled_linear_combination_presentation(
        presentation,
        labels,
        pipeline.display_path,
        0.625,
    )

    assert id(presentation) == identities["presentation"]
    assert id(presentation.geometry) == identities["geometry"]
    assert tuple(
        id(arrow) for arrow in presentation.geometry.term_arrows
    ) == identities["term_arrows"]
    assert id(presentation.geometry.resultant_arrow) == identities["resultant_arrow"]
    assert id(presentation.readout) == identities["readout"]
    assert tuple(
        id(entry) for entry in presentation.readout.coefficient_entries
    ) == identities["coefficient_entries"]
    assert tuple(
        id(entry) for entry in presentation.readout.result_entries
    ) == identities["result_entries"]
    assert id(labels) == identities["labels"]
    assert tuple(id(label) for label in labels.term_label_mobjects) == identities[
        "term_labels"
    ]
    assert id(labels.resultant_label_mobject) == identities["resultant_label"]


def test_labeled_updates_leave_the_completed_trace_unchanged() -> None:
    pipeline = build_linear_combination_presentation_smoke_pipeline()
    trace = ManimLinearCombinationTrace(
        pipeline.trace_display_adapter.snapshot()
    )
    initial = pipeline.display_path.snapshot(0.0)
    presentation = ManimLinearCombinationPresentation(initial)
    labels = ManimLinearCombinationLabels(initial)
    line_ids = tuple(id(line) for line in trace.segment_lines)
    starts = tuple(line.get_start().copy() for line in trace.segment_lines)
    ends = tuple(line.get_end().copy() for line in trace.segment_lines)

    update_labeled_linear_combination_presentation(
        presentation,
        labels,
        pipeline.display_path,
        0.8,
    )

    assert tuple(id(line) for line in trace.segment_lines) == line_ids
    for line, expected_start, expected_end in zip(
        trace.segment_lines,
        starts,
        ends,
        strict=True,
    ):
        np.testing.assert_allclose(line.get_start(), expected_start)
        np.testing.assert_allclose(line.get_end(), expected_end)


def test_tracker_update_reads_progress_and_updates_both_siblings_once() -> None:
    display_snapshot = object()

    class DisplayPathSpy:
        def __init__(self) -> None:
            self.received_progress: list[float] = []

        def snapshot(self, progress: float) -> object:
            self.received_progress.append(progress)
            return display_snapshot

    class AdapterSpy:
        def __init__(self) -> None:
            self.received_snapshots: list[object] = []

        def update_from_snapshot(self, snapshot: object) -> AdapterSpy:
            self.received_snapshots.append(snapshot)
            return self

    moving_group = VGroup()
    presentation = AdapterSpy()
    labels = AdapterSpy()
    display_path = DisplayPathSpy()
    tracker = ValueTracker(0.625)

    returned = update_labeled_linear_combination_from_tracker(
        moving_group,
        presentation,  # type: ignore[arg-type]
        labels,  # type: ignore[arg-type]
        display_path,  # type: ignore[arg-type]
        tracker,
    )

    assert returned is moving_group
    assert display_path.received_progress == [pytest.approx(0.625)]
    assert presentation.received_snapshots == [display_snapshot]
    assert labels.received_snapshots == [display_snapshot]
