import numpy as np
import pytest

from engine.linear_combination import LinearCombination, LinearCombinationSnapshot
from engine.linear_combination_geometry import (
    LinearCombinationGeometry,
    LinearCombinationGeometrySnapshot,
)


def test_two_term_geometry_is_placed_tip_to_tail() -> None:
    mathematical = LinearCombination([[2.0, 1.0], [-1.0, 3.0]]).snapshot(
        [2.0, -1.0]
    )

    geometry = LinearCombinationGeometry().snapshot(mathematical)

    np.testing.assert_allclose(
        geometry.term_segments,
        [
            [[0.0, 0.0], [4.0, 2.0]],
            [[4.0, 2.0], [5.0, -1.0]],
        ],
    )
    np.testing.assert_allclose(
        geometry.resultant_segment,
        [[0.0, 0.0], [5.0, -1.0]],
    )


def test_term_segment_displacements_equal_scaled_terms() -> None:
    mathematical = LinearCombination(
        [[1.0, 2.0, -1.0], [3.0, 0.0, 4.0], [-2.0, 1.0, 2.0]]
    ).snapshot([2.0, -1.0, 0.5])

    geometry = LinearCombinationGeometry()(mathematical)

    displacements = geometry.term_ends - geometry.term_starts
    np.testing.assert_allclose(displacements, mathematical.terms)


def test_negative_and_zero_terms_preserve_exact_segment_geometry() -> None:
    mathematical = LinearCombination([[1.0, 0.0], [0.0, 2.0], [3.0, -1.0]]).snapshot(
        [-2.0, 0.0, 1.0]
    )

    geometry = LinearCombinationGeometry()(mathematical)

    np.testing.assert_allclose(
        geometry.term_segments,
        [
            [[0.0, 0.0], [-2.0, 0.0]],
            [[-2.0, 0.0], [-2.0, 0.0]],
            [[-2.0, 0.0], [1.0, -1.0]],
        ],
    )


def test_resultant_always_runs_from_origin_to_final_sum() -> None:
    mathematical = LinearCombination(
        [[1.0, -2.0, 3.0, 0.0], [0.5, 1.0, -1.0, 2.0]]
    ).snapshot([-2.0, 4.0])

    geometry = LinearCombinationGeometry()(mathematical)

    np.testing.assert_array_equal(geometry.resultant_start, np.zeros(4))
    np.testing.assert_allclose(geometry.resultant_end, mathematical.result)


def test_vector_count_and_dimension_are_independent() -> None:
    mathematical = LinearCombination(
        [
            [1.0, 0.0, 2.0, -1.0, 3.0],
            [0.0, 3.0, 1.0, 2.0, -2.0],
            [2.0, -1.0, 0.0, 1.0, 4.0],
        ]
    ).snapshot([2.0, -1.0, 0.5])

    geometry = LinearCombinationGeometry()(mathematical)

    assert geometry.vector_count == 3
    assert geometry.dimension == 5
    assert geometry.term_segments.shape == (3, 2, 5)
    assert geometry.resultant_segment.shape == (2, 5)


def test_single_vector_geometry_has_one_term_segment() -> None:
    mathematical = LinearCombination([2.0, -3.0, 4.0]).snapshot(-2.0)

    geometry = LinearCombinationGeometry()(mathematical)

    assert geometry.term_segments.shape == (1, 2, 3)
    np.testing.assert_allclose(
        geometry.term_segments[0],
        [[0.0, 0.0, 0.0], [-4.0, 6.0, -8.0]],
    )
    np.testing.assert_allclose(geometry.resultant_end, [-4.0, 6.0, -8.0])


def test_geometry_snapshot_retains_the_exact_mathematical_snapshot() -> None:
    mathematical = LinearCombination([[1.0, 0.0], [0.0, 1.0]]).snapshot([3.0, 4.0])

    geometry = LinearCombinationGeometry()(mathematical)

    assert geometry.linear_combination_snapshot is mathematical
    np.testing.assert_array_equal(
        geometry.linear_combination_snapshot.coefficients,
        [3.0, 4.0],
    )


def test_geometry_converter_rejects_non_snapshot_input() -> None:
    converter = LinearCombinationGeometry()

    with pytest.raises(TypeError, match="LinearCombinationSnapshot"):
        converter.snapshot(np.zeros(2))  # type: ignore[arg-type]


def test_public_geometry_arrays_are_owned_and_read_only() -> None:
    mathematical = LinearCombination([[1.0, 2.0], [3.0, 4.0]]).snapshot([2.0, -1.0])
    geometry = LinearCombinationGeometry()(mathematical)

    for array in (
        geometry.term_segments,
        geometry.resultant_segment,
        geometry.term_starts,
        geometry.term_ends,
        geometry.resultant_start,
        geometry.resultant_end,
    ):
        assert not array.flags.writeable

    assert not np.shares_memory(geometry.term_segments, mathematical.partial_sums)
    assert not np.shares_memory(geometry.resultant_segment, mathematical.result)


def test_snapshot_validation_rejects_inconsistent_term_segments() -> None:
    mathematical = LinearCombination([[1.0, 0.0], [0.0, 1.0]]).snapshot([1.0, 2.0])
    bad_segments = np.array(
        [
            [[0.0, 0.0], [1.0, 0.0]],
            [[9.0, 9.0], [1.0, 2.0]],
        ]
    )

    with pytest.raises(ValueError, match="tails"):
        LinearCombinationGeometrySnapshot(
            linear_combination_snapshot=mathematical,
            term_segments=bad_segments,
            resultant_segment=[[0.0, 0.0], [1.0, 2.0]],
        )


def test_snapshot_validation_rejects_inconsistent_resultant() -> None:
    mathematical = LinearCombination([[1.0, 0.0], [0.0, 1.0]]).snapshot([1.0, 2.0])
    term_segments = np.stack(
        (mathematical.partial_sums[:-1], mathematical.partial_sums[1:]),
        axis=1,
    )

    with pytest.raises(ValueError, match="final sum"):
        LinearCombinationGeometrySnapshot(
            linear_combination_snapshot=mathematical,
            term_segments=term_segments,
            resultant_segment=[[0.0, 0.0], [99.0, 99.0]],
        )


def test_call_is_shorthand_for_snapshot() -> None:
    mathematical = LinearCombination([[2.0, 1.0], [-1.0, 3.0]]).snapshot([0.5, 2.0])
    converter = LinearCombinationGeometry()

    direct = converter.snapshot(mathematical)
    shorthand = converter(mathematical)

    np.testing.assert_allclose(shorthand.term_segments, direct.term_segments)
    np.testing.assert_allclose(shorthand.resultant_segment, direct.resultant_segment)
    assert shorthand.linear_combination_snapshot is mathematical
