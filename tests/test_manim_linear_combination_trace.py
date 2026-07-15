from dataclasses import dataclass

import numpy as np
import pytest

from engine.linear_combination_trace import LinearCombinationTraceSnapshot
from engine.linear_combination_trace_display import (
    LinearCombinationTraceDisplaySnapshot,
)
from engine.manim_linear_combination_trace import ManimLinearCombinationTrace


@dataclass
class TraceDisplaySnapshot:
    display_resultant_segments: np.ndarray


def make_snapshot(segments) -> TraceDisplaySnapshot:
    return TraceDisplaySnapshot(np.asarray(segments, dtype=float))


def line_endpoints(line) -> tuple[np.ndarray, np.ndarray]:
    return np.asarray(line.get_start()), np.asarray(line.get_end())


def test_adapter_consumes_actual_checkpoint_17_display_snapshot() -> None:
    coefficients = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 2.0]])
    resultant_points = np.array([[0.0, 0.0], [1.0, 0.0], [1.0, 2.0]])
    resultant_segments = np.array(
        [
            [[0.0, 0.0], [1.0, 0.0]],
            [[1.0, 0.0], [1.0, 2.0]],
        ]
    )
    trace_snapshot = LinearCombinationTraceSnapshot(
        coefficients=coefficients,
        resultant_points=resultant_points,
        resultant_segments=resultant_segments,
    )
    display_snapshot = LinearCombinationTraceDisplaySnapshot(
        trace_snapshot=trace_snapshot,
        display_resultant_points=resultant_points,
        display_resultant_segments=resultant_segments,
        projection_matrix=np.eye(2),
        display_offset=np.zeros(2),
    )

    adapter = ManimLinearCombinationTrace(display_snapshot)

    assert adapter.snapshot is display_snapshot
    assert adapter.segment_count == 2
    second_start, second_end = line_endpoints(adapter.segment_lines[1])
    np.testing.assert_allclose(second_start, [1.0, 0.0, 0.0])
    np.testing.assert_allclose(second_end, [1.0, 2.0, 0.0])


def test_adapter_builds_one_line_per_trace_segment_in_order() -> None:
    snapshot = make_snapshot(
        [
            [[0.0, 0.0], [1.0, 2.0]],
            [[1.0, 2.0], [-2.0, 3.0]],
        ]
    )

    adapter = ManimLinearCombinationTrace(snapshot)

    assert adapter.segment_count == 2
    assert len(adapter.segment_lines) == 2
    assert len(adapter) == 2

    first_start, first_end = line_endpoints(adapter.segment_lines[0])
    second_start, second_end = line_endpoints(adapter.segment_lines[1])
    np.testing.assert_allclose(first_start, [0.0, 0.0, 0.0])
    np.testing.assert_allclose(first_end, [1.0, 2.0, 0.0])
    np.testing.assert_allclose(second_start, [1.0, 2.0, 0.0])
    np.testing.assert_allclose(second_end, [-2.0, 3.0, 0.0])


def test_adapter_retains_exact_snapshot_and_is_its_root_mobject() -> None:
    snapshot = make_snapshot([[[0.0, 0.0], [1.0, 0.0]]])

    adapter = ManimLinearCombinationTrace(snapshot)

    assert adapter.snapshot is snapshot
    assert adapter.mobject is adapter


@pytest.mark.parametrize(
    "segments, expected_start, expected_end",
    [
        (
            [[[1.5], [-2.0]]],
            [1.5, 0.0, 0.0],
            [-2.0, 0.0, 0.0],
        ),
        (
            [[[1.5, -4.0], [-2.0, 3.0]]],
            [1.5, -4.0, 0.0],
            [-2.0, 3.0, 0.0],
        ),
        (
            [[[1.5, -4.0, 2.0], [-2.0, 3.0, 7.0]]],
            [1.5, -4.0, 2.0],
            [-2.0, 3.0, 7.0],
        ),
    ],
)
def test_one_two_and_three_dimensional_points_are_manim_compatible(
    segments,
    expected_start,
    expected_end,
) -> None:
    adapter = ManimLinearCombinationTrace(make_snapshot(segments))

    start, end = line_endpoints(adapter.segment_lines[0])
    np.testing.assert_allclose(start, expected_start)
    np.testing.assert_allclose(end, expected_end)


def test_single_sample_empty_trace_creates_empty_group() -> None:
    snapshot = TraceDisplaySnapshot(np.empty((0, 2, 2), dtype=float))

    adapter = ManimLinearCombinationTrace(snapshot)

    assert adapter.segment_count == 0
    assert adapter.segment_lines == ()
    assert len(adapter) == 0


def test_segment_mobjects_are_created_once() -> None:
    snapshot = make_snapshot(
        [
            [[0.0, 0.0], [1.0, 0.0]],
            [[1.0, 0.0], [1.0, 1.0]],
        ]
    )

    adapter = ManimLinearCombinationTrace(snapshot)
    identities = tuple(id(line) for line in adapter.segment_lines)

    assert tuple(id(line) for line in adapter.segment_lines) == identities
    assert tuple(adapter.segment_lines) == tuple(adapter)


def test_zero_length_trace_segment_preserves_display_endpoints() -> None:
    adapter = ManimLinearCombinationTrace(
        make_snapshot([[[2.0, -1.0], [2.0, -1.0]]])
    )

    start, end = line_endpoints(adapter.segment_lines[0])
    np.testing.assert_allclose(start, [2.0, -1.0, 0.0])
    np.testing.assert_allclose(end, [2.0, -1.0, 0.0])


def test_style_arguments_cannot_override_snapshot_endpoints() -> None:
    snapshot = make_snapshot([[[0.0, 0.0], [1.0, 0.0]]])

    with pytest.raises(ValueError, match="start and end"):
        ManimLinearCombinationTrace(
            snapshot,
            segment_kwargs={"start": [8.0, 8.0, 8.0]},
        )

    with pytest.raises(ValueError, match="start and end"):
        ManimLinearCombinationTrace(
            snapshot,
            segment_kwargs={"end": [8.0, 8.0, 8.0]},
        )


def test_nonzero_line_buff_is_rejected() -> None:
    snapshot = make_snapshot([[[0.0, 0.0], [1.0, 0.0]]])

    with pytest.raises(ValueError, match="buff must be zero"):
        ManimLinearCombinationTrace(snapshot, segment_kwargs={"buff": 0.1})


def test_missing_canonical_snapshot_field_is_rejected() -> None:
    with pytest.raises(TypeError, match="display_resultant_segments"):
        ManimLinearCombinationTrace(object())


@pytest.mark.parametrize(
    "segments",
    [
        np.array([0.0, 1.0]),
        np.zeros((2, 3, 2)),
        np.zeros((2, 2, 0)),
        np.zeros((2, 2, 4)),
    ],
)
def test_invalid_segment_shapes_or_display_dimensions_are_rejected(
    segments,
) -> None:
    with pytest.raises(ValueError):
        ManimLinearCombinationTrace(TraceDisplaySnapshot(segments))


@pytest.mark.parametrize("bad_value", [np.nan, np.inf, -np.inf])
def test_nonfinite_display_coordinates_are_rejected(bad_value: float) -> None:
    segments = np.array([[[0.0, 0.0], [1.0, bad_value]]])

    with pytest.raises(ValueError, match="finite"):
        ManimLinearCombinationTrace(TraceDisplaySnapshot(segments))
