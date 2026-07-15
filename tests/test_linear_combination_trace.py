from __future__ import annotations

from dataclasses import fields
from types import SimpleNamespace

import numpy as np
import pytest

from engine.linear_combination import LinearCombinationSnapshot
from engine.linear_combination_geometry import LinearCombinationGeometrySnapshot
from engine.linear_combination_trace import LinearCombinationTrace


def _geometry_snapshot(
    coefficients: list[float],
    result: list[float],
):
    result_array = np.asarray(result, dtype=float)
    return SimpleNamespace(
        linear_combination_snapshot=SimpleNamespace(
            coefficients=np.asarray(coefficients, dtype=float)
        ),
        resultant_segment=np.stack(
            (np.zeros_like(result_array), result_array),
            axis=0,
        ),
    )


def test_established_snapshot_fields_used_by_trace_exist() -> None:
    linear_combination_fields = {
        field.name for field in fields(LinearCombinationSnapshot)
    }
    geometry_fields = {
        field.name for field in fields(LinearCombinationGeometrySnapshot)
    }

    assert "coefficients" in linear_combination_fields
    assert "linear_combination_snapshot" in geometry_fields
    assert "resultant_segment" in geometry_fields


def test_trace_collects_coefficients_and_resultant_tips() -> None:
    trace = LinearCombinationTrace(
        [
            _geometry_snapshot([0.0, 0.0], [0.0, 0.0]),
            _geometry_snapshot([0.5, -0.25], [1.25, 0.75]),
            _geometry_snapshot([1.0, -0.5], [2.5, 1.5]),
        ]
    )

    snapshot = trace.snapshot()

    np.testing.assert_allclose(
        snapshot.coefficients,
        [[0.0, 0.0], [0.5, -0.25], [1.0, -0.5]],
    )
    np.testing.assert_allclose(
        snapshot.resultant_points,
        [[0.0, 0.0], [1.25, 0.75], [2.5, 1.5]],
    )


def test_trace_connects_consecutive_resultant_points() -> None:
    snapshot = LinearCombinationTrace(
        [
            _geometry_snapshot([0.0], [0.0, 0.0]),
            _geometry_snapshot([1.0], [1.0, 2.0]),
            _geometry_snapshot([2.0], [3.0, 5.0]),
        ]
    ).snapshot()

    np.testing.assert_allclose(
        snapshot.resultant_segments,
        [
            [[0.0, 0.0], [1.0, 2.0]],
            [[1.0, 2.0], [3.0, 5.0]],
        ],
    )


def test_single_sample_has_empty_segment_array_with_stable_shape() -> None:
    snapshot = LinearCombinationTrace(
        [_geometry_snapshot([2.0, -1.0], [4.0, 3.0, -2.0])]
    ).snapshot()

    assert snapshot.resultant_segments.shape == (0, 2, 3)
    assert snapshot.sample_count == 1
    assert snapshot.coefficient_dimension == 2
    assert snapshot.ambient_dimension == 3


@pytest.mark.parametrize("ambient_dimension", [1, 2, 3, 5])
def test_trace_is_ambient_dimension_independent(ambient_dimension: int) -> None:
    first = np.arange(ambient_dimension, dtype=float)
    second = first + 1.0

    snapshot = LinearCombinationTrace(
        [
            _geometry_snapshot([0.0, 1.0], first.tolist()),
            _geometry_snapshot([1.0, 0.0], second.tolist()),
        ]
    ).snapshot()

    assert snapshot.resultant_points.shape == (2, ambient_dimension)
    assert snapshot.resultant_segments.shape == (1, 2, ambient_dimension)


def test_trace_owns_its_arrays_and_exposes_read_only_outputs() -> None:
    coefficients = np.array([0.25, -0.75])
    result = np.array([2.0, -1.0])
    source = SimpleNamespace(
        linear_combination_snapshot=SimpleNamespace(coefficients=coefficients),
        resultant_segment=np.stack((np.zeros(2), result), axis=0),
    )

    snapshot = LinearCombinationTrace([source]).snapshot()
    coefficients[:] = 99.0
    result[:] = 99.0
    source.resultant_segment[:] = 99.0

    np.testing.assert_allclose(snapshot.coefficients, [[0.25, -0.75]])
    np.testing.assert_allclose(snapshot.resultant_points, [[2.0, -1.0]])
    assert not snapshot.coefficients.flags.writeable
    assert not snapshot.resultant_points.flags.writeable
    assert not snapshot.resultant_segments.flags.writeable

    with pytest.raises(ValueError):
        snapshot.coefficients[0, 0] = 5.0


def test_trace_rejects_empty_snapshot_sequence() -> None:
    with pytest.raises(ValueError, match="at least one"):
        LinearCombinationTrace([])


def test_trace_rejects_inconsistent_coefficient_dimensions() -> None:
    with pytest.raises(ValueError, match="coefficient dimension"):
        LinearCombinationTrace(
            [
                _geometry_snapshot([1.0], [1.0, 2.0]),
                _geometry_snapshot([1.0, 2.0], [3.0, 4.0]),
            ]
        )


def test_trace_rejects_inconsistent_ambient_dimensions() -> None:
    with pytest.raises(ValueError, match="ambient dimension"):
        LinearCombinationTrace(
            [
                _geometry_snapshot([1.0], [1.0, 2.0]),
                _geometry_snapshot([2.0], [3.0, 4.0, 5.0]),
            ]
        )


def test_trace_rejects_malformed_resultant_segment() -> None:
    malformed = SimpleNamespace(
        linear_combination_snapshot=SimpleNamespace(
            coefficients=np.array([1.0])
        ),
        resultant_segment=np.array([1.0, 2.0]),
    )

    with pytest.raises(ValueError, match=r"shape \(2, dimension\)"):
        LinearCombinationTrace([malformed])


@pytest.mark.parametrize(
    "snapshot",
    [
        SimpleNamespace(
            linear_combination_snapshot=SimpleNamespace(
                coefficients=np.array([np.nan])
            ),
            resultant_segment=np.array([[0.0], [1.0]]),
        ),
        SimpleNamespace(
            linear_combination_snapshot=SimpleNamespace(
                coefficients=np.array([1.0])
            ),
            resultant_segment=np.array([[0.0], [np.inf]]),
        ),
    ],
)
def test_trace_rejects_nonfinite_values(snapshot) -> None:
    with pytest.raises(ValueError, match="finite"):
        LinearCombinationTrace([snapshot])


def test_trace_rejects_objects_without_checkpoint_15_fields() -> None:
    with pytest.raises(TypeError, match="linear_combination_snapshot"):
        LinearCombinationTrace([SimpleNamespace()])
