from __future__ import annotations

import numpy as np
import pytest

from engine.coefficient_sweep_path import CoefficientSweepPath
from engine.linear_combination import LinearCombination
from engine.linear_combination_geometry_path import LinearCombinationGeometryPath
from engine.linear_combination_trace import (
    LinearCombinationTrace,
    LinearCombinationTraceSnapshot,
)
from engine.linear_combination_trace_display import (
    LinearCombinationTraceDisplayAdapter,
    LinearCombinationTraceDisplaySnapshot,
)
from engine.rank_collapse_display import LinearDisplayProjector


def _trace_2d(
    progress_values: tuple[float, ...] = (0.0, 0.5, 1.0),
) -> LinearCombinationTrace:
    combination = LinearCombination([[2.0, 0.0], [0.0, 3.0]])
    path = LinearCombinationGeometryPath(
        CoefficientSweepPath(
            combination,
            [0.0, 0.0],
            [2.0, -1.0],
        )
    )
    return LinearCombinationTrace(
        path.snapshot(progress) for progress in progress_values
    )


def test_adapter_retains_exact_components_and_delegates_metadata() -> None:
    trace = _trace_2d()
    projector = LinearDisplayProjector(np.eye(2))
    adapter = LinearCombinationTraceDisplayAdapter(trace, projector)

    assert adapter.trace is trace
    assert adapter.projector is projector
    assert adapter.sample_count == 3
    assert adapter.coefficient_dimension == 2
    assert adapter.mathematical_dimension == 2
    assert adapter.display_dimension == 2


def test_constructor_rejects_invalid_components() -> None:
    trace = _trace_2d()
    projector = LinearDisplayProjector(np.eye(2))

    with pytest.raises(TypeError, match="LinearCombinationTrace"):
        LinearCombinationTraceDisplayAdapter(object(), projector)  # type: ignore[arg-type]

    with pytest.raises(TypeError, match="LinearDisplayProjector"):
        LinearCombinationTraceDisplayAdapter(trace, object())  # type: ignore[arg-type]


def test_constructor_rejects_projector_input_dimension_mismatch() -> None:
    with pytest.raises(ValueError, match="trace mathematical dimension"):
        LinearCombinationTraceDisplayAdapter(
            _trace_2d(),
            LinearDisplayProjector(np.eye(3)),
        )


def test_identity_projection_preserves_trace_points_and_segments() -> None:
    trace = _trace_2d()
    display = LinearCombinationTraceDisplayAdapter(
        trace,
        LinearDisplayProjector(np.eye(2)),
    ).snapshot()

    mathematical = trace.snapshot()
    assert display.trace_snapshot is mathematical
    np.testing.assert_allclose(
        display.display_resultant_points,
        mathematical.resultant_points,
    )
    np.testing.assert_allclose(
        display.display_resultant_segments,
        mathematical.resultant_segments,
    )


def test_axis_selector_projects_high_dimensional_trace_to_two_dimensions() -> None:
    combination = LinearCombination(
        [
            [1.0, 10.0, 2.0, 100.0],
            [3.0, 20.0, -1.0, 200.0],
        ]
    )
    path = LinearCombinationGeometryPath(
        CoefficientSweepPath(
            combination,
            [0.0, 0.0],
            [2.0, -1.0],
        )
    )
    trace = LinearCombinationTrace(
        path.snapshot(progress) for progress in (0.0, 0.5, 1.0)
    )
    projector = LinearDisplayProjector.from_axis_selector(4, [0, 2])
    display = LinearCombinationTraceDisplayAdapter(
        trace,
        projector,
    ).snapshot()

    assert display.mathematical_dimension == 4
    assert display.display_dimension == 2
    assert display.display_resultant_points.shape == (3, 2)
    assert display.display_resultant_segments.shape == (2, 2, 2)
    np.testing.assert_allclose(
        display.display_resultant_points,
        [[0.0, 0.0], [-0.5, 2.5], [-1.0, 5.0]],
    )
    np.testing.assert_allclose(
        display.display_resultant_segments,
        [
            [[0.0, 0.0], [-0.5, 2.5]],
            [[-0.5, 2.5], [-1.0, 5.0]],
        ],
    )


def test_affine_offset_is_applied_without_breaking_trace_topology() -> None:
    projector = LinearDisplayProjector(
        [[2.0, 0.0], [0.0, -1.0]],
        offset=[5.0, 7.0],
    )
    display = LinearCombinationTraceDisplayAdapter(
        _trace_2d(),
        projector,
    ).snapshot()

    np.testing.assert_allclose(
        display.display_resultant_points,
        [[5.0, 7.0], [9.0, 8.5], [13.0, 10.0]],
    )
    np.testing.assert_allclose(
        display.display_resultant_starts,
        display.display_resultant_points[:-1],
    )
    np.testing.assert_allclose(
        display.display_resultant_ends,
        display.display_resultant_points[1:],
    )


def test_snapshot_retains_coefficients_and_exact_mathematical_trace() -> None:
    trace = _trace_2d()
    mathematical = trace.snapshot()
    display = LinearCombinationTraceDisplayAdapter(
        trace,
        LinearDisplayProjector(np.eye(2)),
    ).snapshot()

    assert display.trace_snapshot is mathematical
    np.testing.assert_allclose(
        display.coefficients,
        [[0.0, 0.0], [1.0, -0.5], [2.0, -1.0]],
    )
    assert display.sample_count == 3
    assert display.coefficient_dimension == 2


def test_single_sample_preserves_stable_empty_segment_shape() -> None:
    display = LinearCombinationTraceDisplayAdapter(
        _trace_2d((0.25,)),
        LinearDisplayProjector.from_axis_selector(2, [1]),
    ).snapshot()

    assert display.display_resultant_points.shape == (1, 1)
    assert display.display_resultant_segments.shape == (0, 2, 1)
    np.testing.assert_allclose(display.display_resultant_points, [[-0.75]])


def test_display_snapshot_arrays_are_owned_and_read_only() -> None:
    display = LinearCombinationTraceDisplayAdapter(
        _trace_2d(),
        LinearDisplayProjector(np.eye(2)),
    ).snapshot()

    for array in (
        display.display_resultant_points,
        display.display_resultant_segments,
        display.projection_matrix,
        display.display_offset,
    ):
        assert not array.flags.writeable

    with pytest.raises(ValueError):
        display.display_resultant_points[0, 0] = 99.0


def test_display_snapshot_validates_projection_consistency() -> None:
    valid = LinearCombinationTraceDisplayAdapter(
        _trace_2d(),
        LinearDisplayProjector(np.eye(2)),
    ).snapshot()
    invalid_points = valid.display_resultant_points.copy()
    invalid_points[1, 0] += 1.0

    with pytest.raises(ValueError, match="projected mathematical trace points"):
        LinearCombinationTraceDisplaySnapshot(
            trace_snapshot=valid.trace_snapshot,
            display_resultant_points=invalid_points,
            display_resultant_segments=valid.display_resultant_segments,
            projection_matrix=valid.projection_matrix,
            display_offset=valid.display_offset,
        )


def test_display_snapshot_rejects_wrong_trace_snapshot_type() -> None:
    with pytest.raises(TypeError, match="LinearCombinationTraceSnapshot"):
        LinearCombinationTraceDisplaySnapshot(
            trace_snapshot=object(),  # type: ignore[arg-type]
            display_resultant_points=np.zeros((1, 2)),
            display_resultant_segments=np.empty((0, 2, 2)),
            projection_matrix=np.eye(2),
            display_offset=np.zeros(2),
        )


def test_adapter_delegates_once_for_output_and_twice_to_projector() -> None:
    class RecordingTrace(LinearCombinationTrace):
        def __init__(self) -> None:
            source = _trace_2d().snapshot()
            self._snapshot = source
            self.snapshot_calls = 0

        def snapshot(self) -> LinearCombinationTraceSnapshot:
            self.snapshot_calls += 1
            return self._snapshot

    class RecordingProjector(LinearDisplayProjector):
        def __init__(self) -> None:
            super().__init__(np.eye(2))
            self.projected_shapes: list[tuple[int, ...]] = []

        def project(self, vectors: np.ndarray) -> np.ndarray:
            self.projected_shapes.append(np.asarray(vectors).shape)
            return super().project(vectors)

    trace = RecordingTrace()
    projector = RecordingProjector()
    adapter = LinearCombinationTraceDisplayAdapter(trace, projector)
    constructor_calls = trace.snapshot_calls
    output = adapter.snapshot()

    assert constructor_calls == 1
    assert trace.snapshot_calls == 2
    assert projector.projected_shapes == [(3, 2), (4, 2)]
    np.testing.assert_allclose(output.coefficients[1], [1.0, -0.5])


def test_call_is_shorthand_for_snapshot() -> None:
    adapter = LinearCombinationTraceDisplayAdapter(
        _trace_2d(),
        LinearDisplayProjector(np.eye(2)),
    )

    direct = adapter.snapshot()
    shorthand = adapter()

    np.testing.assert_allclose(
        shorthand.display_resultant_points,
        direct.display_resultant_points,
    )
    np.testing.assert_allclose(
        shorthand.display_resultant_segments,
        direct.display_resultant_segments,
    )
