import numpy as np
import pytest

from engine.svd_introduction import SingularValueDecompositionIntroduction


def test_default_gram_matrix_and_eigenpairs_are_exact():
    model = SingularValueDecompositionIntroduction()
    eigenvalues, vectors = model.gram_eigendecomposition()
    expected_vectors = np.array([[1.0, 1.0], [1.0, -1.0]]) / np.sqrt(2.0)
    assert np.allclose(model.gram_matrix(), [[2.0, 1.0], [1.0, 2.0]])
    assert np.allclose(eigenvalues, [3.0, 1.0])
    assert np.allclose(vectors, expected_vectors)


def test_singular_values_are_square_roots_of_gram_eigenvalues():
    model = SingularValueDecompositionIntroduction()
    assert np.allclose(model.singular_values(), [np.sqrt(3.0), 1.0])
    assert np.allclose(model.sigma_matrix(), [[np.sqrt(3.0), 0.0], [0.0, 1.0]])


def test_right_directions_map_to_scaled_orthonormal_left_directions():
    model = SingularValueDecompositionIntroduction()
    expected_u = np.array(
        [[1 / np.sqrt(6), 1 / np.sqrt(2)],
         [2 / np.sqrt(6), 0.0],
         [1 / np.sqrt(6), -1 / np.sqrt(2)]]
    )
    assert np.allclose(model.left_singular_vectors(), expected_u)
    assert np.allclose(expected_u.T @ expected_u, np.eye(2))
    assert model.mapped_directions_are_orthogonal()
    assert np.allclose(
        model.mapped_right_directions(),
        expected_u @ model.sigma_matrix(),
    )


def test_thin_svd_reconstructs_rectangular_matrix():
    model = SingularValueDecompositionIntroduction()
    u, sigma, vt = model.factorization()
    assert u.shape == (3, 2)
    assert sigma.shape == (2, 2)
    assert vt.shape == (2, 2)
    assert np.allclose(model.reconstruction(), model.matrix)


@pytest.mark.parametrize(
    "matrix",
    [[], [1.0, 2.0], [[1.0, np.inf]], [[1.0, 0.0]]],
)
def test_invalid_or_unsupported_matrix_is_rejected(matrix):
    with pytest.raises(ValueError):
        SingularValueDecompositionIntroduction(matrix)


def test_dependent_columns_are_deferred_from_this_introductory_model():
    with pytest.raises(ValueError, match="independent columns"):
        SingularValueDecompositionIntroduction([[1.0, 2.0], [2.0, 4.0]])


def test_invalid_orthogonality_tolerance_is_rejected():
    model = SingularValueDecompositionIntroduction()
    with pytest.raises(ValueError, match="tolerance"):
        model.mapped_directions_are_orthogonal(-1.0)
