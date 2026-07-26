import numpy as np
import pytest

from engine.column_space import ColumnSpace


MATRIX = np.array([
    [2.0, -0.5, 1.5],
    [0.5, 1.8, 2.3],
    [0.5, 0.8, 1.3],
])


def test_snapshot_computes_matrix_vector_product() -> None:
    model = ColumnSpace(MATRIX)
    snapshot = model.snapshot([1.0, -2.0, 0.5])
    assert np.allclose(snapshot.output, MATRIX @ np.array([1.0, -2.0, 0.5]))


def test_columns_are_stored_as_vectors() -> None:
    model = ColumnSpace(MATRIX)
    assert np.allclose(model.columns[0], MATRIX[:, 0])
    assert np.allclose(model.columns[1], MATRIX[:, 1])
    assert np.allclose(model.columns[2], MATRIX[:, 2])


def test_rank_two_matrix_has_two_independent_columns() -> None:
    model = ColumnSpace(MATRIX)
    assert model.rank == 2
    assert model.independent_columns() == (0, 1)


def test_third_column_is_sum_of_first_two() -> None:
    model = ColumnSpace(MATRIX)
    assert np.allclose(model.columns[2], model.columns[0] + model.columns[1])


def test_sample_outputs_remain_in_column_plane() -> None:
    model = ColumnSpace(MATRIX)
    coefficients = np.array([(a, b, c) for a in (-1, 0, 1) for b in (-1, 0, 1) for c in (-1, 0, 1)], dtype=float)
    outputs = model.sample_outputs(coefficients)
    assert np.linalg.matrix_rank(outputs, tol=1e-9) == 2


def test_invalid_matrix_shape_is_rejected() -> None:
    with pytest.raises(ValueError):
        ColumnSpace(np.eye(2))
