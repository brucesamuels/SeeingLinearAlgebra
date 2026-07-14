import numpy as np
import pytest

from engine.coefficient_sweep_path import CoefficientSweepPath
from engine.linear_combination import LinearCombination, LinearCombinationSnapshot
from engine.linear_combination_geometry import (
    LinearCombinationGeometry,
    LinearCombinationGeometrySnapshot,
)
from engine.linear_combination_geometry_path import LinearCombinationGeometryPath


def _two_vector_path() -> LinearCombinationGeometryPath:
    combination = LinearCombination([[2.0, 0.0], [0.0, 3.0]])
    coefficient_path = CoefficientSweepPath(
        combination,
        [0.0, 0.0],
        [2.0, -1.0],
    )
    return LinearCombinationGeometryPath(coefficient_path)


def test_start_snapshot_uses_start_coefficients_and_geometry() -> None:
    snapshot = _two_vector_path().snapshot(0.0)

    np.testing.assert_allclose(
        snapshot.linear_combination_snapshot.coefficients,
        [0.0, 0.0],
    )
    np.testing.assert_allclose(
        snapshot.term_segments,
        [
            [[0.0, 0.0], [0.0, 0.0]],
            [[0.0, 0.0], [0.0, 0.0]],
        ],
    )
    np.testing.assert_allclose(snapshot.resultant_segment, [[0.0, 0.0], [0.0, 0.0]])


def test_midpoint_snapshot_composes_interpolation_with_tip_to_tail_geometry() -> None:
    snapshot = _two_vector_path().snapshot(0.5)

    np.testing.assert_allclose(
        snapshot.linear_combination_snapshot.coefficients,
        [1.0, -0.5],
    )
    np.testing.assert_allclose(
        snapshot.term_segments,
        [
            [[0.0, 0.0], [2.0, 0.0]],
            [[2.0, 0.0], [2.0, -1.5]],
        ],
    )
    np.testing.assert_allclose(
        snapshot.resultant_segment,
        [[0.0, 0.0], [2.0, -1.5]],
    )


def test_end_snapshot_uses_end_coefficients_and_geometry() -> None:
    snapshot = _two_vector_path().snapshot(1.0)

    np.testing.assert_allclose(
        snapshot.linear_combination_snapshot.coefficients,
        [2.0, -1.0],
    )
    np.testing.assert_allclose(
        snapshot.term_segments,
        [
            [[0.0, 0.0], [4.0, 0.0]],
            [[4.0, 0.0], [4.0, -3.0]],
        ],
    )
    np.testing.assert_allclose(snapshot.resultant_end, [4.0, -3.0])


def test_path_delegates_once_to_each_existing_layer() -> None:
    class RecordingCoefficientSweepPath(CoefficientSweepPath):
        def __init__(self) -> None:
            super().__init__(
                LinearCombination([[1.0, 0.0], [0.0, 1.0]]),
                [0.0, 0.0],
                [2.0, 4.0],
            )
            self.progress_calls: list[float] = []

        def snapshot(self, progress: float) -> LinearCombinationSnapshot:
            self.progress_calls.append(progress)
            return super().snapshot(progress)

    class RecordingGeometry(LinearCombinationGeometry):
        def __init__(self) -> None:
            self.snapshot_calls: list[LinearCombinationSnapshot] = []

        def snapshot(
            self,
            linear_combination_snapshot: LinearCombinationSnapshot,
        ) -> LinearCombinationGeometrySnapshot:
            self.snapshot_calls.append(linear_combination_snapshot)
            return super().snapshot(linear_combination_snapshot)

    coefficient_path = RecordingCoefficientSweepPath()
    geometry = RecordingGeometry()
    path = LinearCombinationGeometryPath(coefficient_path, geometry)

    output = path.snapshot(0.25)

    assert coefficient_path.progress_calls == [0.25]
    assert len(geometry.snapshot_calls) == 1
    assert output.linear_combination_snapshot is geometry.snapshot_calls[0]
    np.testing.assert_allclose(
        output.linear_combination_snapshot.coefficients,
        [0.5, 1.0],
    )


def test_path_retains_exact_components_and_delegates_metadata() -> None:
    combination = LinearCombination(
        [[1.0, 0.0, 2.0], [0.0, 3.0, -1.0], [2.0, 1.0, 0.0]]
    )
    coefficient_path = CoefficientSweepPath(
        combination,
        [0.0, 0.0, 0.0],
        [1.0, -2.0, 0.5],
    )
    geometry = LinearCombinationGeometry()
    path = LinearCombinationGeometryPath(coefficient_path, geometry)

    assert path.coefficient_sweep_path is coefficient_path
    assert path.geometry is geometry
    assert path.linear_combination is combination
    assert path.vector_count == 3
    assert path.dimension == 3


def test_default_geometry_converter_is_created_when_omitted() -> None:
    coefficient_path = CoefficientSweepPath(
        LinearCombination([[1.0, 0.0]]),
        [0.0],
        [1.0],
    )

    path = LinearCombinationGeometryPath(coefficient_path)

    assert isinstance(path.geometry, LinearCombinationGeometry)


def test_vector_count_and_dimension_remain_independent() -> None:
    combination = LinearCombination(
        [
            [1.0, 0.0, 2.0, -1.0, 3.0],
            [0.0, 3.0, 1.0, 2.0, -2.0],
            [2.0, -1.0, 0.0, 1.0, 4.0],
        ]
    )
    path = LinearCombinationGeometryPath(
        CoefficientSweepPath(
            combination,
            [0.0, 0.0, 0.0],
            [2.0, -1.0, 0.5],
        )
    )

    snapshot = path.snapshot(0.75)

    assert path.vector_count == 3
    assert path.dimension == 5
    assert snapshot.term_segments.shape == (3, 2, 5)
    assert snapshot.resultant_segment.shape == (2, 5)


def test_single_vector_scalar_sweep_is_supported() -> None:
    path = LinearCombinationGeometryPath(
        CoefficientSweepPath(
            LinearCombination([2.0, -3.0, 4.0]),
            -1.0,
            3.0,
        )
    )

    snapshot = path.snapshot(0.25)

    assert snapshot.term_segments.shape == (1, 2, 3)
    np.testing.assert_allclose(snapshot.resultant_end, [0.0, 0.0, 0.0])


def test_constructor_rejects_invalid_components() -> None:
    coefficient_path = CoefficientSweepPath(
        LinearCombination([[1.0, 0.0]]),
        [0.0],
        [1.0],
    )

    with pytest.raises(TypeError, match="CoefficientSweepPath"):
        LinearCombinationGeometryPath(object())  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="LinearCombinationGeometry"):
        LinearCombinationGeometryPath(
            coefficient_path,
            object(),  # type: ignore[arg-type]
        )


def test_progress_validation_is_left_to_coefficient_sweep_path() -> None:
    path = _two_vector_path()

    with pytest.raises(ValueError, match="scalar"):
        path.snapshot([0.5])  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="finite"):
        path.snapshot(np.nan)
    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        path.snapshot(1.01)


def test_call_is_shorthand_for_snapshot() -> None:
    path = _two_vector_path()

    direct = path.snapshot(0.4)
    shorthand = path(0.4)

    np.testing.assert_allclose(shorthand.term_segments, direct.term_segments)
    np.testing.assert_allclose(shorthand.resultant_segment, direct.resultant_segment)
    np.testing.assert_allclose(
        shorthand.linear_combination_snapshot.coefficients,
        direct.linear_combination_snapshot.coefficients,
    )
