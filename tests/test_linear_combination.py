import numpy as np
import pytest

from engine.linear_combination import LinearCombination, LinearCombinationSnapshot


def test_two_vector_combination_in_r2() -> None:
    combination = LinearCombination([[1.0, 2.0], [3.0, -1.0]])

    snapshot = combination.snapshot([2.0, -1.0])

    np.testing.assert_allclose(snapshot.terms, [[2.0, 4.0], [-3.0, 1.0]])
    np.testing.assert_allclose(snapshot.result, [-1.0, 5.0])
    assert snapshot.vector_count == 2
    assert snapshot.dimension == 2


def test_dimension_and_vector_count_are_independent() -> None:
    combination = LinearCombination(
        [
            [1.0, 0.0, 2.0, -1.0],
            [0.0, 3.0, 1.0, 2.0],
            [2.0, -1.0, 0.0, 1.0],
        ]
    )

    result = combination.evaluate([2.0, -1.0, 0.5])

    np.testing.assert_allclose(result, [3.0, -3.5, 3.0, -3.5])
    assert combination.vector_count == 3
    assert combination.dimension == 4


def test_partial_sums_include_origin_and_tip_to_tail_states() -> None:
    combination = LinearCombination([[2.0, 0.0], [0.0, 3.0], [-1.0, 1.0]])

    snapshot = combination.snapshot([0.5, 2.0, -1.0])

    np.testing.assert_allclose(
        snapshot.partial_sums,
        [
            [0.0, 0.0],
            [1.0, 0.0],
            [1.0, 6.0],
            [2.0, 5.0],
        ],
    )
    np.testing.assert_allclose(snapshot.result, snapshot.partial_sums[-1])


def test_zero_coefficients_produce_zero_terms_and_result() -> None:
    combination = LinearCombination([[1.0, 2.0, 3.0], [-4.0, 5.0, 6.0]])

    snapshot = combination.snapshot([0.0, 0.0])

    np.testing.assert_allclose(snapshot.terms, np.zeros((2, 3)))
    np.testing.assert_allclose(snapshot.partial_sums, np.zeros((3, 3)))
    np.testing.assert_allclose(snapshot.result, np.zeros(3))


def test_single_vector_accepts_scalar_coefficient() -> None:
    combination = LinearCombination([2.0, -3.0, 4.0])

    snapshot = combination.snapshot(-0.5)

    np.testing.assert_allclose(snapshot.coefficients, [-0.5])
    np.testing.assert_allclose(snapshot.result, [-1.0, 1.5, -2.0])


def test_coefficient_count_must_match_vector_count() -> None:
    combination = LinearCombination([[1.0, 0.0], [0.0, 1.0]])

    with pytest.raises(ValueError, match="coefficient count"):
        combination.snapshot([1.0])


def test_invalid_vector_shapes_are_rejected() -> None:
    with pytest.raises(ValueError, match="one- or two-dimensional"):
        LinearCombination(np.zeros((2, 2, 2)))

    with pytest.raises(ValueError, match="at least one vector"):
        LinearCombination(np.empty((0, 2)))

    with pytest.raises(ValueError, match="dimension at least 1"):
        LinearCombination(np.empty((2, 0)))


def test_nonfinite_values_are_rejected() -> None:
    with pytest.raises(ValueError, match="finite"):
        LinearCombination([[1.0, np.inf]])

    combination = LinearCombination([[1.0, 2.0]])
    with pytest.raises(ValueError, match="finite"):
        combination.snapshot([np.nan])


def test_inputs_are_copied_and_public_arrays_are_read_only() -> None:
    source_vectors = np.array([[1.0, 2.0], [3.0, 4.0]])
    source_coefficients = np.array([2.0, -1.0])
    combination = LinearCombination(source_vectors)
    snapshot = combination.snapshot(source_coefficients)

    source_vectors[0, 0] = 99.0
    source_coefficients[0] = 99.0

    np.testing.assert_allclose(combination.vectors, [[1.0, 2.0], [3.0, 4.0]])
    np.testing.assert_allclose(snapshot.coefficients, [2.0, -1.0])

    for array in (
        combination.vectors,
        snapshot.coefficients,
        snapshot.terms,
        snapshot.partial_sums,
        snapshot.result,
    ):
        assert not array.flags.writeable


def test_snapshot_rejects_inconsistent_mathematical_state() -> None:
    with pytest.raises(ValueError, match="cumulative sums"):
        LinearCombinationSnapshot(
            coefficients=np.array([1.0, 2.0]),
            terms=np.array([[1.0, 0.0], [0.0, 2.0]]),
            partial_sums=np.array(
                [
                    [0.0, 0.0],
                    [1.0, 0.0],
                    [9.0, 9.0],
                ]
            ),
            result=np.array([9.0, 9.0]),
        )
