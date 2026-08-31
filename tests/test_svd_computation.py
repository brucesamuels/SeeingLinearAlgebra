import numpy as np
import pytest

from engine.svd_computation import SingularValueDecompositionComputation


def test_default_matrix_and_gram_matrix_are_exact():
    model = SingularValueDecompositionComputation()
    assert np.allclose(model.matrix, [[1, 1], [1, -1], [1, 1]])
    assert np.allclose(model.gram_matrix(), [[3, 1], [1, 3]])


def test_gram_eigenpairs_and_singular_values_are_ordered():
    model = SingularValueDecompositionComputation()
    values, vectors = model.gram_eigenpairs()
    expected_vectors = np.array([[1.0, 1.0], [1.0, -1.0]]) / np.sqrt(2.0)
    assert np.allclose(values, [4.0, 2.0])
    assert np.allclose(vectors, expected_vectors)
    assert np.allclose(model.singular_values(), [2.0, np.sqrt(2.0)])


def test_left_singular_vectors_follow_u_equals_av_over_sigma():
    model = SingularValueDecompositionComputation()
    expected_u = np.array(
        [[1 / np.sqrt(2), 0.0], [0.0, 1.0], [1 / np.sqrt(2), 0.0]]
    )
    assert np.allclose(model.left_singular_vectors(), expected_u)
    assert np.allclose(expected_u.T @ expected_u, np.eye(2))
    assert np.allclose(
        model.matrix @ model.right_singular_vectors(),
        expected_u @ np.diag(model.singular_values()),
    )


def test_thin_factorization_dimensions_and_reconstruction():
    model = SingularValueDecompositionComputation()
    u, sigma, vt = model.factorization()
    assert model.thin_dimensions() == ((3, 2), (2, 2), (2, 2))
    assert u.shape == (3, 2)
    assert sigma.shape == (2, 2)
    assert vt.shape == (2, 2)
    assert np.allclose(model.reconstruction(), model.matrix)


@pytest.mark.parametrize("component", [0, 1])
def test_paired_sign_flip_does_not_change_factorization(component):
    model = SingularValueDecompositionComputation()
    u, sigma, vt = model.sign_flipped_factorization(component)
    assert np.allclose(u @ sigma @ vt, model.matrix)


@pytest.mark.parametrize(
    "matrix",
    [[], [1.0, 2.0], [[1.0, np.inf]], [[1.0, 0.0]]],
)
def test_invalid_or_unsupported_matrices_are_rejected(matrix):
    with pytest.raises(ValueError):
        SingularValueDecompositionComputation(matrix)


def test_dependent_columns_and_invalid_component_are_rejected():
    with pytest.raises(ValueError, match="independent columns"):
        SingularValueDecompositionComputation([[1.0, 2.0], [2.0, 4.0]])
    model = SingularValueDecompositionComputation()
    with pytest.raises(ValueError, match="component_index"):
        model.sign_flipped_factorization(2)
