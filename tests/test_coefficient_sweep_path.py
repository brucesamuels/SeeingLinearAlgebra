import numpy as np
import pytest

from engine.coefficient_sweep_path import CoefficientSweepPath
from engine.linear_combination import LinearCombination, LinearCombinationSnapshot


def test_endpoints_return_start_and_end_states() -> None:
    combination = LinearCombination([[1.0, 0.0], [0.0, 2.0]])
    path = CoefficientSweepPath(combination, [1.0, -2.0], [3.0, 4.0])

    start = path.snapshot(0.0)
    end = path.snapshot(1.0)

    np.testing.assert_array_equal(start.coefficients, [1.0, -2.0])
    np.testing.assert_array_equal(end.coefficients, [3.0, 4.0])
    np.testing.assert_allclose(start.result, [1.0, -4.0])
    np.testing.assert_allclose(end.result, [3.0, 8.0])


def test_midpoint_interpolates_each_coefficient_linearly() -> None:
    combination = LinearCombination([[2.0, 1.0], [-1.0, 3.0]])
    path = CoefficientSweepPath(combination, [-2.0, 4.0], [6.0, -2.0])

    snapshot = path.snapshot(0.5)

    np.testing.assert_allclose(snapshot.coefficients, [2.0, 1.0])
    np.testing.assert_allclose(snapshot.result, [3.0, 5.0])


def test_quarter_progress_preserves_full_tip_to_tail_snapshot() -> None:
    combination = LinearCombination(
        [[1.0, 2.0], [3.0, -1.0], [-2.0, 4.0]]
    )
    path = CoefficientSweepPath(
        combination,
        [0.0, 2.0, -2.0],
        [4.0, -2.0, 2.0],
    )

    snapshot = path.snapshot(0.25)

    np.testing.assert_allclose(snapshot.coefficients, [1.0, 1.0, -1.0])
    np.testing.assert_allclose(
        snapshot.terms,
        [[1.0, 2.0], [3.0, -1.0], [2.0, -4.0]],
    )
    np.testing.assert_allclose(
        snapshot.partial_sums,
        [[0.0, 0.0], [1.0, 2.0], [4.0, 1.0], [6.0, -3.0]],
    )
    np.testing.assert_allclose(snapshot.result, [6.0, -3.0])


def test_vector_count_and_ambient_dimension_remain_independent() -> None:
    combination = LinearCombination(
        [
            [1.0, 0.0, 2.0, -1.0],
            [0.0, 3.0, 1.0, 2.0],
            [2.0, -1.0, 0.0, 1.0],
        ]
    )
    path = CoefficientSweepPath(combination, [0.0, 0.0, 0.0], [2.0, -1.0, 0.5])

    snapshot = path.snapshot(1.0)

    assert path.vector_count == 3
    assert path.dimension == 4
    assert snapshot.vector_count == 3
    assert snapshot.dimension == 4
    np.testing.assert_allclose(snapshot.result, [3.0, -3.5, 3.0, -3.5])


def test_single_vector_sweep_accepts_scalar_endpoints() -> None:
    combination = LinearCombination([2.0, -3.0, 4.0])
    path = CoefficientSweepPath(combination, -1.0, 3.0)

    snapshot = path.snapshot(0.25)

    np.testing.assert_allclose(snapshot.coefficients, [0.0])
    np.testing.assert_allclose(snapshot.result, [0.0, 0.0, 0.0])


def test_path_delegates_snapshot_construction_to_linear_combination() -> None:
    class RecordingLinearCombination(LinearCombination):
        def __init__(self) -> None:
            super().__init__([[1.0, 0.0], [0.0, 1.0]])
            self.calls: list[np.ndarray] = []

        def snapshot(self, coefficients: object) -> LinearCombinationSnapshot:
            self.calls.append(np.array(coefficients, dtype=float, copy=True))
            return super().snapshot(coefficients)

    combination = RecordingLinearCombination()
    path = CoefficientSweepPath(combination, [0.0, 2.0], [4.0, -2.0])
    combination.calls.clear()

    snapshot = path.snapshot(0.75)

    assert path.linear_combination is combination
    assert len(combination.calls) == 1
    np.testing.assert_allclose(combination.calls[0], [3.0, -1.0])
    np.testing.assert_allclose(snapshot.coefficients, [3.0, -1.0])


def test_endpoint_validation_is_owned_by_linear_combination() -> None:
    combination = LinearCombination([[1.0, 0.0], [0.0, 1.0]])

    with pytest.raises(ValueError, match="coefficient count"):
        CoefficientSweepPath(combination, [1.0], [2.0, 3.0])

    with pytest.raises(ValueError, match="finite"):
        CoefficientSweepPath(combination, [1.0, 2.0], [np.inf, 3.0])


def test_progress_must_be_a_finite_scalar_in_the_unit_interval() -> None:
    path = CoefficientSweepPath(
        LinearCombination([[1.0, 0.0]]),
        [0.0],
        [1.0],
    )

    with pytest.raises(ValueError, match="scalar"):
        path.snapshot([0.5])
    with pytest.raises(ValueError, match="finite"):
        path.snapshot(np.nan)
    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        path.snapshot(-0.01)
    with pytest.raises(ValueError, match=r"\[0, 1\]"):
        path.snapshot(1.01)


def test_constructor_copies_endpoints_and_public_arrays_are_read_only() -> None:
    start = np.array([1.0, 2.0])
    end = np.array([3.0, -4.0])
    path = CoefficientSweepPath(
        LinearCombination([[1.0, 0.0], [0.0, 1.0]]),
        start,
        end,
    )

    start[:] = 99.0
    end[:] = 99.0

    np.testing.assert_allclose(path.start_coefficients, [1.0, 2.0])
    np.testing.assert_allclose(path.end_coefficients, [3.0, -4.0])
    np.testing.assert_allclose(path.coefficient_delta, [2.0, -6.0])

    for array in (
        path.start_coefficients,
        path.end_coefficients,
        path.coefficient_delta,
        path.coefficients_at(0.5),
    ):
        assert not array.flags.writeable


def test_coefficients_at_returns_an_independent_array() -> None:
    path = CoefficientSweepPath(
        LinearCombination([[1.0], [2.0]]),
        [0.0, 1.0],
        [2.0, 3.0],
    )

    first = path.coefficients_at(0.5)
    second = path.coefficients_at(0.5)

    assert first is not second
    np.testing.assert_allclose(first, second)
    assert not np.shares_memory(first, path.start_coefficients)
    assert not np.shares_memory(first, path.end_coefficients)


def test_call_is_shorthand_for_snapshot() -> None:
    path = CoefficientSweepPath(
        LinearCombination([[1.0, 2.0], [3.0, 4.0]]),
        [0.0, 0.0],
        [2.0, -1.0],
    )

    direct = path.snapshot(0.4)
    shorthand = path(0.4)

    np.testing.assert_allclose(shorthand.coefficients, direct.coefficients)
    np.testing.assert_allclose(shorthand.terms, direct.terms)
    np.testing.assert_allclose(shorthand.partial_sums, direct.partial_sums)
    np.testing.assert_allclose(shorthand.result, direct.result)
