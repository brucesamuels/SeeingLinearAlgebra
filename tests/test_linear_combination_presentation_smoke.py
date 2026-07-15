from __future__ import annotations

import numpy as np
import pytest

pytest.importorskip("manim")

from manim import DecimalNumber, Scene, VGroup

from engine.manim_linear_combination_geometry import (
    ManimLinearCombinationGeometry,
)
from engine.manim_linear_combination_readout import (
    ManimLinearCombinationReadout,
)
from engine.manim_linear_combination_trace import ManimLinearCombinationTrace
from scenes.linear_combination_presentation_smoke import (
    LinearCombinationPresentationSmoke,
    SMOKE_END_COEFFICIENTS,
    SMOKE_START_COEFFICIENTS,
    SMOKE_VECTORS,
    TRACE_PROGRESS_VALUES,
    TRACE_SAMPLE_COUNT,
    build_linear_combination_presentation_smoke_pipeline,
    update_linear_combination_presentation,
)


def entry_values(entries: tuple[DecimalNumber, ...]) -> np.ndarray:
    return np.array([entry.get_value() for entry in entries], dtype=float)


def test_smoke_scene_is_a_manim_scene() -> None:
    assert issubclass(LinearCombinationPresentationSmoke, Scene)


def test_smoke_inputs_and_trace_samples_are_well_formed() -> None:
    assert SMOKE_VECTORS.shape == (2, 2)
    assert SMOKE_START_COEFFICIENTS.shape == (2,)
    assert SMOKE_END_COEFFICIENTS.shape == (2,)
    assert TRACE_SAMPLE_COUNT >= 2
    assert TRACE_PROGRESS_VALUES.shape == (TRACE_SAMPLE_COUNT,)
    assert not TRACE_PROGRESS_VALUES.flags.writeable
    assert TRACE_PROGRESS_VALUES[0] == pytest.approx(0.0)
    assert TRACE_PROGRESS_VALUES[-1] == pytest.approx(1.0)
    assert np.all(np.diff(TRACE_PROGRESS_VALUES) > 0.0)
    assert np.all(np.isfinite(SMOKE_VECTORS))
    assert np.all(np.isfinite(SMOKE_START_COEFFICIENTS))
    assert np.all(np.isfinite(SMOKE_END_COEFFICIENTS))


def test_pipeline_shares_exact_upstream_components() -> None:
    pipeline = build_linear_combination_presentation_smoke_pipeline()

    assert pipeline.coefficient_path.linear_combination is pipeline.combination
    assert pipeline.geometry_path.coefficient_sweep_path is pipeline.coefficient_path
    assert pipeline.geometry_path.geometry is pipeline.geometry
    assert pipeline.display_path.path is pipeline.geometry_path
    assert pipeline.display_path.projector is pipeline.projector
    assert pipeline.trace_display_adapter.trace is pipeline.trace
    assert pipeline.trace_display_adapter.projector is pipeline.projector


def test_trace_uses_actual_geometry_path_samples() -> None:
    pipeline = build_linear_combination_presentation_smoke_pipeline()
    trace_snapshot = pipeline.trace.snapshot()

    expected_coefficients = np.stack(
        [
            pipeline.coefficient_path.coefficients_at(float(progress))
            for progress in TRACE_PROGRESS_VALUES
        ],
        axis=0,
    )
    expected_points = np.stack(
        [
            pipeline.geometry_path.snapshot(float(progress)).resultant_end
            for progress in TRACE_PROGRESS_VALUES
        ],
        axis=0,
    )

    assert trace_snapshot.sample_count == TRACE_SAMPLE_COUNT
    np.testing.assert_allclose(trace_snapshot.coefficients, expected_coefficients)
    np.testing.assert_allclose(trace_snapshot.resultant_points, expected_points)


def test_trace_endpoints_match_moving_display_path_endpoints() -> None:
    pipeline = build_linear_combination_presentation_smoke_pipeline()
    trace_display = pipeline.trace_display_adapter.snapshot()
    initial_display = pipeline.display_path.snapshot(0.0)
    final_display = pipeline.display_path.snapshot(1.0)

    np.testing.assert_allclose(
        trace_display.display_resultant_points[0],
        initial_display.display_resultant_end,
    )
    np.testing.assert_allclose(
        trace_display.display_resultant_points[-1],
        final_display.display_resultant_end,
    )
    np.testing.assert_allclose(
        trace_display.projection_matrix,
        initial_display.projection_matrix,
    )
    np.testing.assert_allclose(
        trace_display.display_offset,
        initial_display.display_offset,
    )


def test_all_actual_manim_adapters_consume_one_pipeline() -> None:
    pipeline = build_linear_combination_presentation_smoke_pipeline()
    trace_display = pipeline.trace_display_adapter.snapshot()
    initial_display = pipeline.display_path.snapshot(0.0)

    trace = ManimLinearCombinationTrace(trace_display)
    arrows = ManimLinearCombinationGeometry(initial_display)
    readout = ManimLinearCombinationReadout(
        initial_display.linear_combination_snapshot
    )

    assert trace.snapshot is trace_display
    assert trace.segment_count == TRACE_SAMPLE_COUNT - 1
    assert arrows.term_count == pipeline.combination.vector_count
    assert readout.snapshot is initial_display.linear_combination_snapshot
    np.testing.assert_allclose(
        entry_values(readout.coefficient_entries),
        SMOKE_START_COEFFICIENTS,
    )
    np.testing.assert_allclose(
        trace.segment_lines[0].get_start(),
        [*initial_display.display_resultant_end, 0.0],
    )


def test_shared_update_synchronizes_arrows_and_readout() -> None:
    pipeline = build_linear_combination_presentation_smoke_pipeline()
    initial_display = pipeline.display_path.snapshot(0.0)
    arrows = ManimLinearCombinationGeometry(initial_display)
    readout = ManimLinearCombinationReadout(
        initial_display.linear_combination_snapshot
    )
    group = VGroup(arrows, readout)

    returned = update_linear_combination_presentation(
        group,
        arrows,
        readout,
        pipeline.display_path,
        1.0,
    )
    final_display = pipeline.display_path.snapshot(1.0)

    assert returned is group
    np.testing.assert_allclose(
        entry_values(readout.coefficient_entries),
        SMOKE_END_COEFFICIENTS,
    )
    np.testing.assert_allclose(
        entry_values(readout.result_entries),
        final_display.linear_combination_snapshot.result,
    )
    np.testing.assert_allclose(
        arrows.resultant_arrow.get_end(),
        [*final_display.display_resultant_end, 0.0],
    )


def test_shared_update_queries_display_path_exactly_once() -> None:
    mathematical_snapshot = object()

    class DisplaySnapshot:
        linear_combination_snapshot = mathematical_snapshot

    display_snapshot = DisplaySnapshot()

    class DisplayPathSpy:
        def __init__(self) -> None:
            self.received_progress: list[float] = []

        def snapshot(self, progress: float) -> DisplaySnapshot:
            self.received_progress.append(progress)
            return display_snapshot

    class AdapterSpy:
        def __init__(self) -> None:
            self.received_snapshot: object | None = None

        def update_from_snapshot(self, snapshot: object) -> AdapterSpy:
            self.received_snapshot = snapshot
            return self

    group = VGroup()
    arrows = AdapterSpy()
    readout = AdapterSpy()
    display_path = DisplayPathSpy()

    returned = update_linear_combination_presentation(
        group,
        arrows,  # type: ignore[arg-type]
        readout,  # type: ignore[arg-type]
        display_path,  # type: ignore[arg-type]
        0.375,
    )

    assert returned is group
    assert display_path.received_progress == [pytest.approx(0.375)]
    assert arrows.received_snapshot is display_snapshot
    assert readout.received_snapshot is mathematical_snapshot


def test_shared_update_preserves_all_moving_mobject_identities() -> None:
    pipeline = build_linear_combination_presentation_smoke_pipeline()
    initial_display = pipeline.display_path.snapshot(0.0)
    arrows = ManimLinearCombinationGeometry(initial_display)
    readout = ManimLinearCombinationReadout(
        initial_display.linear_combination_snapshot
    )
    group = VGroup(arrows, readout)

    identities = {
        "group": id(group),
        "arrows": id(arrows),
        "terms": tuple(id(arrow) for arrow in arrows.term_arrows),
        "resultant": id(arrows.resultant_arrow),
        "readout": id(readout),
        "coefficient_entries": tuple(
            id(entry) for entry in readout.coefficient_entries
        ),
        "result_entries": tuple(id(entry) for entry in readout.result_entries),
    }

    update_linear_combination_presentation(
        group,
        arrows,
        readout,
        pipeline.display_path,
        0.625,
    )

    assert id(group) == identities["group"]
    assert id(arrows) == identities["arrows"]
    assert tuple(id(arrow) for arrow in arrows.term_arrows) == identities["terms"]
    assert id(arrows.resultant_arrow) == identities["resultant"]
    assert id(readout) == identities["readout"]
    assert tuple(id(entry) for entry in readout.coefficient_entries) == identities[
        "coefficient_entries"
    ]
    assert tuple(id(entry) for entry in readout.result_entries) == identities[
        "result_entries"
    ]


def test_moving_updates_leave_completed_trace_unchanged() -> None:
    pipeline = build_linear_combination_presentation_smoke_pipeline()
    trace = ManimLinearCombinationTrace(
        pipeline.trace_display_adapter.snapshot()
    )
    initial_display = pipeline.display_path.snapshot(0.0)
    arrows = ManimLinearCombinationGeometry(initial_display)
    readout = ManimLinearCombinationReadout(
        initial_display.linear_combination_snapshot
    )
    group = VGroup(arrows, readout)

    line_ids = tuple(id(line) for line in trace.segment_lines)
    starts = tuple(line.get_start().copy() for line in trace.segment_lines)
    ends = tuple(line.get_end().copy() for line in trace.segment_lines)

    update_linear_combination_presentation(
        group,
        arrows,
        readout,
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


def test_intermediate_state_uses_one_exact_mathematical_snapshot() -> None:
    pipeline = build_linear_combination_presentation_smoke_pipeline()
    initial_display = pipeline.display_path.snapshot(0.0)
    arrows = ManimLinearCombinationGeometry(initial_display)
    readout = ManimLinearCombinationReadout(
        initial_display.linear_combination_snapshot
    )
    group = VGroup(arrows, readout)
    progress = 0.4

    update_linear_combination_presentation(
        group,
        arrows,
        readout,
        pipeline.display_path,
        progress,
    )
    expected = pipeline.display_path.snapshot(progress)

    assert readout.snapshot is not initial_display.linear_combination_snapshot
    np.testing.assert_allclose(
        entry_values(readout.coefficient_entries),
        expected.linear_combination_snapshot.coefficients,
    )
    np.testing.assert_allclose(
        entry_values(readout.result_entries),
        expected.linear_combination_snapshot.result,
    )
    np.testing.assert_allclose(
        arrows.resultant_arrow.get_end(),
        [*expected.display_resultant_end, 0.0],
    )
