from __future__ import annotations

import numpy as np
import pytest

pytest.importorskip("manim")

from manim import Scene

from engine.manim_linear_combination_geometry import (
    ManimLinearCombinationGeometry,
)
from engine.manim_linear_combination_trace import ManimLinearCombinationTrace
from scenes.linear_combination_trace_smoke import (
    LinearCombinationTraceSmoke,
    SMOKE_END_COEFFICIENTS,
    SMOKE_START_COEFFICIENTS,
    SMOKE_VECTORS,
    TRACE_PROGRESS_VALUES,
    TRACE_SAMPLE_COUNT,
    build_linear_combination_trace_smoke_pipeline,
    update_linear_combination_mobject,
)


def test_smoke_scene_is_a_manim_scene() -> None:
    assert issubclass(LinearCombinationTraceSmoke, Scene)


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
    pipeline = build_linear_combination_trace_smoke_pipeline()

    assert pipeline.coefficient_path.linear_combination is pipeline.combination
    assert pipeline.geometry_path.coefficient_sweep_path is pipeline.coefficient_path
    assert pipeline.geometry_path.geometry is pipeline.geometry
    assert pipeline.display_path.path is pipeline.geometry_path
    assert pipeline.display_path.projector is pipeline.projector
    assert pipeline.trace_display_adapter.trace is pipeline.trace
    assert pipeline.trace_display_adapter.projector is pipeline.projector


def test_trace_samples_exact_geometry_path_coefficients_and_resultant_tips() -> None:
    pipeline = build_linear_combination_trace_smoke_pipeline()
    trace_snapshot = pipeline.trace.snapshot()

    expected_coefficients = np.stack(
        [
            pipeline.coefficient_path.coefficients_at(float(progress))
            for progress in TRACE_PROGRESS_VALUES
        ],
        axis=0,
    )
    expected_resultant_points = np.stack(
        [
            pipeline.geometry_path.snapshot(float(progress)).resultant_segment[1]
            for progress in TRACE_PROGRESS_VALUES
        ],
        axis=0,
    )

    assert trace_snapshot.sample_count == TRACE_SAMPLE_COUNT
    np.testing.assert_allclose(trace_snapshot.coefficients, expected_coefficients)
    np.testing.assert_allclose(
        trace_snapshot.resultant_points,
        expected_resultant_points,
    )


def test_trace_and_moving_geometry_use_consistent_display_endpoints() -> None:
    pipeline = build_linear_combination_trace_smoke_pipeline()
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


def test_actual_manim_adapters_consume_pipeline_outputs() -> None:
    pipeline = build_linear_combination_trace_smoke_pipeline()

    trace_display = pipeline.trace_display_adapter.snapshot()
    trace_mobject = ManimLinearCombinationTrace(trace_display)
    arrows = ManimLinearCombinationGeometry(pipeline.display_path.snapshot(0.0))
    arrows.update_from_snapshot(pipeline.display_path.snapshot(1.0))

    assert trace_mobject.segment_count == TRACE_SAMPLE_COUNT - 1
    assert arrows.term_count == 2
    np.testing.assert_allclose(
        trace_mobject.segment_lines[0].get_start(),
        [*trace_display.display_resultant_points[0], 0.0],
    )
    np.testing.assert_allclose(
        trace_mobject.segment_lines[-1].get_end(),
        [*trace_display.display_resultant_points[-1], 0.0],
    )
    np.testing.assert_allclose(
        arrows.resultant_arrow.get_end(),
        [*trace_display.display_resultant_points[-1], 0.0],
    )


def test_scene_update_helper_preserves_all_arrow_mobject_identities() -> None:
    pipeline = build_linear_combination_trace_smoke_pipeline()
    arrows = ManimLinearCombinationGeometry(pipeline.display_path.snapshot(0.0))

    root_id = id(arrows)
    term_ids = tuple(id(arrow) for arrow in arrows.term_arrows)
    resultant_id = id(arrows.resultant_arrow)

    returned = update_linear_combination_mobject(
        arrows,
        pipeline.display_path,
        1.0,
    )

    assert returned is arrows
    assert id(arrows) == root_id
    assert tuple(id(arrow) for arrow in arrows.term_arrows) == term_ids
    assert id(arrows.resultant_arrow) == resultant_id


def test_scene_update_helper_requests_exact_progress_value() -> None:
    sentinel_snapshot = object()

    class DisplayPathSpy:
        def __init__(self) -> None:
            self.received_progress: float | None = None

        def snapshot(self, progress: float) -> object:
            self.received_progress = progress
            return sentinel_snapshot

    class MobjectSpy:
        def __init__(self) -> None:
            self.received_snapshot: object | None = None

        def update_from_snapshot(self, snapshot: object) -> MobjectSpy:
            self.received_snapshot = snapshot
            return self

    display_path = DisplayPathSpy()
    mobject = MobjectSpy()

    returned = update_linear_combination_mobject(
        mobject,  # type: ignore[arg-type]
        display_path,  # type: ignore[arg-type]
        0.375,
    )

    assert returned is mobject
    assert display_path.received_progress == pytest.approx(0.375)
    assert mobject.received_snapshot is sentinel_snapshot
