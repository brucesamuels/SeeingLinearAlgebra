import numpy as np
import pytest

from engine.rank_collapse import RankCollapse


def test_endpoints_are_original_and_truncated_svd():
    matrix = np.diag([4.0, 2.0, 1.0])
    collapse = RankCollapse(matrix, target_rank=1)

    np.testing.assert_allclose(collapse.matrix_at(0.0), matrix)
    np.testing.assert_allclose(
        collapse.matrix_at(1.0),
        np.diag([4.0, 0.0, 0.0]),
        atol=1e-12,
    )


def test_intermediate_progress_scales_discarded_singular_values():
    collapse = RankCollapse(np.diag([4.0, 2.0, 1.0]), target_rank=1)

    np.testing.assert_allclose(
        collapse.singular_values_at(0.25),
        np.array([4.0, 1.5, 0.75]),
    )


def test_rank_and_nullity_at_end():
    collapse = RankCollapse(
        [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
        target_rank=2,
    )

    assert collapse.initial_rank == 3
    assert collapse.target_rank == 2
    assert collapse.initial_nullity == 0
    assert collapse.final_nullity == 1
    assert collapse.rank_at(1.0) == 2
    assert collapse.nullity_at(1.0) == 1


def test_apply_uses_requested_progress():
    collapse = RankCollapse(np.diag([3.0, 2.0]), target_rank=1)
    vector = np.array([1.0, 1.0])

    np.testing.assert_allclose(collapse.apply(vector, 0.0), [3.0, 2.0])
    np.testing.assert_allclose(collapse.apply(vector, 1.0), [3.0, 0.0])


def test_image_and_kernel_bases_are_correct_at_end():
    collapse = RankCollapse(np.diag([5.0, 2.0, 1.0]), target_rank=1)

    image = collapse.image_basis()
    kernel = collapse.kernel_basis()

    assert image.shape == (3, 1)
    assert kernel.shape == (3, 2)
    np.testing.assert_allclose(image.T @ image, np.eye(1), atol=1e-12)
    np.testing.assert_allclose(kernel.T @ kernel, np.eye(2), atol=1e-12)
    np.testing.assert_allclose(
        collapse.matrix_at(1.0) @ kernel,
        np.zeros((3, 2)),
        atol=1e-12,
    )


def test_wide_matrix_includes_automatic_kernel_directions():
    matrix = np.array([[1.0, 0.0, 0.0], [0.0, 2.0, 0.0]])
    collapse = RankCollapse(matrix, target_rank=1)

    kernel = collapse.kernel_basis()

    assert kernel.shape == (3, 2)
    np.testing.assert_allclose(
        collapse.matrix_at(1.0) @ kernel,
        np.zeros((2, 2)),
        atol=1e-12,
    )


def test_snapshot_is_consistent():
    collapse = RankCollapse(np.diag([3.0, 2.0]), target_rank=1)
    snapshot = collapse.snapshot(1.0)

    assert snapshot.progress == 1.0
    assert snapshot.rank == 1
    assert snapshot.nullity == 1
    np.testing.assert_allclose(snapshot.matrix, collapse.matrix_at(1.0))
    np.testing.assert_allclose(
        snapshot.singular_values,
        collapse.singular_values_at(1.0),
    )


@pytest.mark.parametrize("progress", [-0.01, 1.01, np.inf])
def test_invalid_progress_raises(progress):
    collapse = RankCollapse(np.eye(2), target_rank=1)

    with pytest.raises(ValueError):
        collapse.matrix_at(progress)


def test_invalid_target_rank_raises():
    with pytest.raises(ValueError):
        RankCollapse(np.eye(2), target_rank=3)


def test_vector_dimension_must_match_domain():
    collapse = RankCollapse(np.eye(3), target_rank=2)

    with pytest.raises(ValueError):
        collapse.apply([1.0, 2.0])
