import numpy as np
import pytest

from engine.coefficient_sweep_path import CoefficientSweepPath
from engine.linear_combination import LinearCombination
from engine.linear_combination_geometry import LinearCombinationGeometrySnapshot
from engine.linear_combination_geometry_display import (
    LinearCombinationGeometryDisplayAdapter,
    LinearCombinationGeometryDisplaySnapshot,
)
from engine.linear_combination_geometry_path import LinearCombinationGeometryPath
from engine.rank_collapse_display import LinearDisplayProjector


def _path_2d() -> LinearCombinationGeometryPath:
    combination = LinearCombination([[2.0, 0.0], [0.0, 3.0]])
    return LinearCombinationGeometryPath(
        CoefficientSweepPath(
            combination,
            [0.0, 0.0],
            [2.0, -1.0],
        )
    )


def test_adapter_retains_exact_components_and_delegates_metadata() -> None:
    path = _path_2d()
    projector = LinearDisplayProjector([[1.0, 0.0], [0.0, 1.0]])

    adapter = LinearCombinationGeometryDisplayAdapter(path, projector)

    assert adapter.path is path
    assert adapter.projector is projector
    assert adapter.linear_combination is path.linear_combination
    assert adapter.vector_count == 2
    assert adapter.dimension == 2
    assert adapter.display_dimension == 2


def test_constructor_rejects_invalid_components() -> None:
    path = _path_2d()
    projector = LinearDisplayProjector(np.eye(2))

    with pytest.raises(TypeError, match="LinearCombinationGeometryPath"):
        LinearCombinationGeometryDisplayAdapter(object(), projector)  # type: ignore[arg-type]
    with pytest.raises(TypeError, match="LinearDisplayProjector"):
        LinearCombinationGeometryDisplayAdapter(path, object())  # type: ignore[arg-type]


def test_constructor_rejects_projector_input_dimension_mismatch() -> None:
    with pytest.raises(ValueError, match="mathematical dimension"):
        LinearCombinationGeometryDisplayAdapter(
            _path_2d(),
            LinearDisplayProjector(np.eye(3)),
        )


def test_identity_projection_preserves_all_segment_endpoints() -> None:
    adapter = LinearCombinationGeometryDisplayAdapter(
        _path_2d(),
        LinearDisplayProjector(np.eye(2)),
    )

    snapshot = adapter.snapshot(0.5)

    np.testing.assert_allclose(
        snapshot.display_term_segments,
        [
            [[0.0, 0.0], [2.0, 0.0]],
            [[2.0, 0.0], [2.0, -1.5]],
        ],
    )
    np.testing.assert_allclose(
        snapshot.display_resultant_segment,
        [[0.0, 0.0], [2.0, -1.5]],
    )


def test_axis_selector_projects_high_dimensional_geometry_to_two_dimensions() -> None:
    combination = LinearCombination(
        [
            [1.0, 10.0, 2.0, 100.0],
            [3.0, 20.0, -1.0, 200.0],
        ]
    )
    path = LinearCombinationGeometryPath(
        CoefficientSweepPath(combination, [0.0, 0.0], [2.0, -1.0])
    )
    projector = LinearDisplayProjector.from_axis_selector(4, [0, 2])

    snapshot = LinearCombinationGeometryDisplayAdapter(path, projector).snapshot(1.0)

    assert snapshot.mathematical_dimension == 4
    assert snapshot.display_dimension == 2
    assert snapshot.display_term_segments.shape == (2, 2, 2)
    np.testing.assert_allclose(
        snapshot.display_term_segments,
        [
            [[0.0, 0.0], [2.0, 4.0]],
            [[2.0, 4.0], [-1.0, 5.0]],
        ],
    )
    np.testing.assert_allclose(
        snapshot.display_resultant_segment,
        [[0.0, 0.0], [-1.0, 5.0]],
    )


def test_affine_offset_is_applied_to_each_endpoint_without_breaking_topology() -> None:
    projector = LinearDisplayProjector(
        [[2.0, 0.0], [0.0, -1.0]],
        offset=[5.0, 7.0],
    )
    snapshot = LinearCombinationGeometryDisplayAdapter(
        _path_2d(),
        projector,
    ).snapshot(0.5)

    np.testing.assert_allclose(
        snapshot.display_term_segments,
        [
            [[5.0, 7.0], [9.0, 7.0]],
            [[9.0, 7.0], [9.0, 8.5]],
        ],
    )
    np.testing.assert_allclose(
        snapshot.display_resultant_segment,
        [[5.0, 7.0], [9.0, 8.5]],
    )
    np.testing.assert_allclose(
        snapshot.display_term_ends[:-1],
        snapshot.display_term_starts[1:],
    )
    np.testing.assert_allclose(
        snapshot.display_resultant_start,
        snapshot.display_term_starts[0],
    )
    np.testing.assert_allclose(
        snapshot.display_resultant_end,
        snapshot.display_term_ends[-1],
    )


def test_nontrivial_projection_preserves_endpoint_order_and_resultant_tip() -> None:
    projector = LinearDisplayProjector([[1.0, 2.0], [-3.0, 1.0]])
    snapshot = LinearCombinationGeometryDisplayAdapter(
        _path_2d(),
        projector,
    ).snapshot(1.0)

    np.testing.assert_allclose(
        snapshot.display_term_segments,
        [
            [[0.0, 0.0], [4.0, -12.0]],
            [[4.0, -12.0], [-2.0, -15.0]],
        ],
    )
    np.testing.assert_allclose(
        snapshot.display_resultant_segment,
        [[0.0, 0.0], [-2.0, -15.0]],
    )


def test_snapshot_retains_exact_renderer_independent_geometry() -> None:
    path = _path_2d()
    adapter = LinearCombinationGeometryDisplayAdapter(
        path,
        LinearDisplayProjector(np.eye(2)),
    )

    snapshot = adapter.snapshot(0.25)

    assert isinstance(snapshot.geometry_snapshot, LinearCombinationGeometrySnapshot)
    assert snapshot.linear_combination_snapshot is (
        snapshot.geometry_snapshot.linear_combination_snapshot
    )
    np.testing.assert_allclose(
        snapshot.linear_combination_snapshot.coefficients,
        [0.5, -0.25],
    )
    np.testing.assert_allclose(
        snapshot.geometry_snapshot.term_segments,
        [
            [[0.0, 0.0], [1.0, 0.0]],
            [[1.0, 0.0], [1.0, -0.75]],
        ],
    )


def test_display_snapshot_arrays_are_owned_and_read_only() -> None:
    snapshot = LinearCombinationGeometryDisplayAdapter(
        _path_2d(),
        LinearDisplayProjector(np.eye(2)),
    ).snapshot(0.5)

    for array in (
        snapshot.display_term_segments,
        snapshot.display_resultant_segment,
        snapshot.projection_matrix,
        snapshot.display_offset,
    ):
        assert not array.flags.writeable

    with pytest.raises(ValueError):
        snapshot.display_term_segments[0, 0, 0] = 99.0


def test_display_snapshot_validates_projection_consistency() -> None:
    adapter = LinearCombinationGeometryDisplayAdapter(
        _path_2d(),
        LinearDisplayProjector(np.eye(2)),
    )
    valid = adapter.snapshot(0.5)

    invalid_terms = valid.display_term_segments.copy()
    invalid_terms[0, 1, 0] += 1.0

    with pytest.raises(ValueError, match="projected mathematical endpoints"):
        LinearCombinationGeometryDisplaySnapshot(
            geometry_snapshot=valid.geometry_snapshot,
            display_term_segments=invalid_terms,
            display_resultant_segment=valid.display_resultant_segment,
            projection_matrix=valid.projection_matrix,
            display_offset=valid.display_offset,
        )


def test_adapter_delegates_once_to_path_and_twice_to_projector() -> None:
    class RecordingPath(LinearCombinationGeometryPath):
        def __init__(self) -> None:
            super().__init__(
                CoefficientSweepPath(
                    LinearCombination([[1.0, 0.0], [0.0, 1.0]]),
                    [0.0, 0.0],
                    [2.0, 4.0],
                )
            )
            self.progress_calls: list[float] = []

        def snapshot(self, progress: float) -> LinearCombinationGeometrySnapshot:
            self.progress_calls.append(progress)
            return super().snapshot(progress)

    class RecordingProjector(LinearDisplayProjector):
        def __init__(self) -> None:
            super().__init__(np.eye(2))
            self.projected_shapes: list[tuple[int, ...]] = []

        def project(self, vectors: np.ndarray) -> np.ndarray:
            self.projected_shapes.append(np.asarray(vectors).shape)
            return super().project(vectors)

    path = RecordingPath()
    projector = RecordingProjector()

    output = LinearCombinationGeometryDisplayAdapter(path, projector).snapshot(0.25)

    assert path.progress_calls == [0.25]
    assert projector.projected_shapes == [(4, 2), (2, 2)]
    np.testing.assert_allclose(
        output.linear_combination_snapshot.coefficients,
        [0.5, 1.0],
    )


def test_snapshots_returns_immutable_sequence_in_requested_order() -> None:
    adapter = LinearCombinationGeometryDisplayAdapter(
        _path_2d(),
        LinearDisplayProjector(np.eye(2)),
    )

    snapshots = adapter.snapshots([0.0, 0.5, 1.0])

    assert isinstance(snapshots, tuple)
    assert len(snapshots) == 3
    np.testing.assert_allclose(
        [snapshot.linear_combination_snapshot.coefficients for snapshot in snapshots],
        [[0.0, 0.0], [1.0, -0.5], [2.0, -1.0]],
    )


def test_progress_validation_remains_owned_by_the_coefficient_path() -> None:
    adapter = LinearCombinationGeometryDisplayAdapter(
        _path_2d(),
        LinearDisplayProjector(np.eye(2)),
    )

    with pytest.raises(ValueError, match="scalar"):
        adapter.snapshot([0.5])  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="finite"):
        adapter.snapshot(np.nan)
    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        adapter.snapshot(1.01)


def test_call_is_shorthand_for_snapshot() -> None:
    adapter = LinearCombinationGeometryDisplayAdapter(
        _path_2d(),
        LinearDisplayProjector(np.eye(2)),
    )

    direct = adapter.snapshot(0.4)
    shorthand = adapter(0.4)

    np.testing.assert_allclose(
        shorthand.display_term_segments,
        direct.display_term_segments,
    )
    np.testing.assert_allclose(
        shorthand.display_resultant_segment,
        direct.display_resultant_segment,
    )
