import numpy as np
import pytest

from engine.gram_matrix_definiteness import GramMatrixDefiniteness


def test_default_rectangular_matrix_has_original_positive_definite_gram_matrix():
    model = GramMatrixDefiniteness()
    np.testing.assert_allclose(model.gram_matrix(), [[2, 1], [1, 2]])
    assert model.rank() == 2
    assert model.has_independent_columns()
    assert model.gram_is_positive_semidefinite()
    assert model.gram_is_positive_definite()


def test_gram_energy_equals_squared_image_norm():
    model = GramMatrixDefiniteness()
    for vector in ([1, 0], [0, 1], [2, -3], [-0.25, 1.5]):
        assert model.gram_energy(vector) == pytest.approx(
            model.squared_norm_energy(vector)
        )


def test_dependent_columns_create_nonzero_zero_energy_direction():
    model = GramMatrixDefiniteness([[1, 2], [1, 2], [0, 0]])
    vector = [-2, 1]
    np.testing.assert_allclose(model.image(vector), [0, 0, 0])
    assert model.gram_energy(vector) == pytest.approx(0.0)
    np.testing.assert_allclose(model.gram_matrix(), [[2, 4], [4, 8]])
    assert model.gram_is_positive_semidefinite()
    assert not model.gram_is_positive_definite()


def test_gram_energy_is_never_negative_for_rectangular_examples():
    matrices = (
        [[1, 2, 3]],
        [[1], [-2], [3]],
        [[1, 0], [0, 0], [0, 1]],
    )
    for matrix in matrices:
        model = GramMatrixDefiniteness(matrix)
        assert model.gram_is_positive_semidefinite()


@pytest.mark.parametrize("bad_matrix", ([], [[]], [1, 2, 3], [[1, np.inf]]))
def test_rejects_invalid_matrices(bad_matrix):
    with pytest.raises(ValueError):
        GramMatrixDefiniteness(bad_matrix)


def test_rejects_bad_vectors_and_tolerances():
    model = GramMatrixDefiniteness()
    with pytest.raises(ValueError):
        model.gram_energy([1, 2, 3])
    with pytest.raises(ValueError):
        model.rank(-1)
    with pytest.raises(ValueError):
        model.gram_is_positive_semidefinite(float("nan"))
