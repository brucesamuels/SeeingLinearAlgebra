import inspect

import numpy as np
import pytest

from engine.svd_fundamental_subspaces import SVDFundamentalSubspaces


def test_default_matrix_and_dimensions():
    model = SVDFundamentalSubspaces()
    assert np.allclose(model.matrix, [[1, 1], [1, 1], [0, 0]])
    assert model.domain_dimension == 2
    assert model.codomain_dimension == 3
    assert model.rank() == 1
    assert model.nullity() == 1
    assert model.left_nullity() == 2
    assert np.allclose(model.singular_values(), [2, 0])


def test_full_bases_are_orthonormal_and_have_expected_shapes():
    model = SVDFundamentalSubspaces()
    assert model.row_basis().shape == (2, 1)
    assert model.null_basis().shape == (2, 1)
    assert model.column_basis().shape == (3, 1)
    assert model.left_null_basis().shape == (3, 2)
    assert np.allclose(model.full_v().T @ model.full_v(), np.eye(2))
    assert np.allclose(model.full_u().T @ model.full_u(), np.eye(3))


def test_default_pedagogical_bases_are_deterministic():
    model = SVDFundamentalSubspaces()
    root_two = np.sqrt(2)
    assert np.allclose(model.row_basis()[:, 0], [1 / root_two, 1 / root_two])
    assert np.allclose(model.null_basis()[:, 0], [1 / root_two, -1 / root_two])
    assert np.allclose(model.column_basis()[:, 0], [1 / root_two, 1 / root_two, 0])
    assert np.allclose(
        model.left_null_basis(),
        [[1 / root_two, 0], [-1 / root_two, 0], [0, 1]],
    )


def test_basis_columns_span_the_four_fundamental_subspaces():
    model = SVDFundamentalSubspaces()
    assert np.allclose(model.apply(model.null_basis()[:, 0]), 0)
    assert np.allclose(model.matrix.T @ model.left_null_basis(), 0)
    assert np.allclose(
        model.apply(model.row_basis()[:, 0]),
        2 * model.column_basis()[:, 0],
    )


def test_full_factorization_has_rectangular_dimensions_and_reconstructs():
    model = SVDFundamentalSubspaces()
    u, sigma, vt = model.full_factorization()
    assert u.shape == (3, 3)
    assert sigma.shape == (3, 2)
    assert vt.shape == (2, 2)
    assert np.allclose(sigma, [[2, 0], [0, 0], [0, 0]])
    assert np.allclose(u @ sigma @ vt, model.matrix)
    assert np.allclose(model.reconstruction(), model.matrix)


def test_domain_decomposition_splits_row_and_null_components():
    model = SVDFundamentalSubspaces()
    vector = np.array([3.0, -1.0])
    row, null = model.domain_decomposition(vector)
    assert np.allclose(row + null, vector)
    assert np.dot(row, null) == pytest.approx(0)
    assert np.allclose(model.apply(vector), model.apply(row))
    assert np.allclose(model.apply(null), 0)


def test_output_decomposition_splits_column_and_left_null_components():
    model = SVDFundamentalSubspaces()
    vector = np.array([2.0, -1.0, 3.0])
    column, left_null = model.output_decomposition(vector)
    assert np.allclose(column + left_null, vector)
    assert np.dot(column, left_null) == pytest.approx(0)
    assert np.allclose(model.matrix.T @ left_null, 0)


@pytest.mark.parametrize("matrix", ([[1, 0], [0, 1], [0, 0]], np.zeros((3, 2))))
def test_model_requires_nonzero_rank_one_matrix(matrix):
    with pytest.raises(ValueError, match="rank one"):
        SVDFundamentalSubspaces(matrix)


@pytest.mark.parametrize("matrix", ([1, 2], [[1, 1], [1, 1]], [[1, np.inf], [1, 1], [0, 0]]))
def test_invalid_matrices_are_rejected(matrix):
    with pytest.raises(ValueError, match="matrix"):
        SVDFundamentalSubspaces(matrix)


@pytest.mark.parametrize("vector", ([1], [1, 2, 3], [1, np.inf]))
def test_invalid_domain_vectors_are_rejected(vector):
    with pytest.raises(ValueError, match="vector"):
        SVDFundamentalSubspaces().domain_decomposition(vector)


@pytest.mark.parametrize("vector", ([1], [1, 2], [1, 2, np.inf]))
def test_invalid_output_vectors_are_rejected(vector):
    with pytest.raises(ValueError, match="output vector"):
        SVDFundamentalSubspaces().output_decomposition(vector)


def test_engine_reuses_rank_collapse_and_has_no_renderer_dependency():
    source = inspect.getsource(inspect.getmodule(SVDFundamentalSubspaces))
    assert "from engine.rank_collapse import RankCollapse" in source
    assert "from manim" not in source
    assert "import manim" not in source
