import math

import numpy as np
import pytest

from engine.positive_definite_cholesky import PositiveDefiniteCholesky


def test_default_upper_factor_has_expected_entries():
    model = PositiveDefiniteCholesky()
    expected = [
        [2, 1, 0],
        [0, math.sqrt(2), 1 / math.sqrt(2)],
        [0, 0, math.sqrt(3 / 2)],
    ]
    np.testing.assert_allclose(model.upper_factor(), expected, atol=1e-12)
    assert model.has_positive_diagonal()


def test_factorization_reconstructs_default_matrix():
    model = PositiveDefiniteCholesky()
    np.testing.assert_allclose(model.reconstruct(), model.matrix, atol=1e-12)


def test_construction_steps_cover_upper_triangle_in_algorithm_order():
    steps = PositiveDefiniteCholesky().construction_steps()
    assert [(step.row, step.column) for step in steps] == [
        (0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 2)
    ]
    assert [step.diagonal for step in steps] == [True, False, False, True, False, True]
    np.testing.assert_allclose(
        [step.value for step in steps],
        [2, 1, 0, math.sqrt(2), 1 / math.sqrt(2), math.sqrt(3 / 2)],
    )


def test_squared_norm_equals_direct_quadratic_energy():
    model = PositiveDefiniteCholesky()
    for vector in ([1, 0, 0], [2, -1, 4], [-0.5, 1.25, 3]):
        assert model.squared_norm_energy(vector) == pytest.approx(model.energy(vector))


def test_supports_general_symmetric_positive_definite_dimension():
    model = PositiveDefiniteCholesky([[2, 1], [1, 2]])
    np.testing.assert_allclose(model.reconstruct(), [[2, 1], [1, 2]])
    assert model.has_positive_diagonal()


@pytest.mark.parametrize(
    "bad_matrix",
    (
        [[1, 2, 3], [4, 5, 6]],
        [[1, 2], [0, 1]],
        [[1, np.inf], [np.inf, 1]],
        [],
        [[1, 0], [0, 0]],
        [[1, 0], [0, -1]],
    ),
)
def test_rejects_invalid_or_non_positive_definite_matrices(bad_matrix):
    with pytest.raises(ValueError):
        PositiveDefiniteCholesky(bad_matrix)


def test_rejects_bad_vectors_and_tolerances():
    with pytest.raises(ValueError):
        PositiveDefiniteCholesky(tolerance=-1)
    model = PositiveDefiniteCholesky()
    with pytest.raises(ValueError):
        model.energy([1, 2])
    with pytest.raises(ValueError):
        model.has_positive_diagonal(float("nan"))
