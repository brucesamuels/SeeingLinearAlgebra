import numpy as np
import pytest

from engine.fundamental_subspaces import FundamentalSubspaces

MATRIX = np.array([
    [1.0, 2.0, 1.0],
    [0.0, 1.0, 1.0],
    [1.0, 3.0, 2.0],
])


def _model() -> FundamentalSubspaces:
    return FundamentalSubspaces(MATRIX)


def test_snapshot_reports_expected_dimensions() -> None:
    snapshot = _model().snapshot()
    assert snapshot.rank == 2
    assert snapshot.nullity == 1
    assert snapshot.left_nullity == 1


def test_pivot_columns_are_first_two_columns() -> None:
    snapshot = _model().snapshot()
    assert snapshot.pivot_column_indices == (0, 1)
    assert len(snapshot.column_basis) == 2


def test_row_space_is_orthogonal_to_null_space() -> None:
    assert _model().row_null_are_orthogonal()


def test_column_space_is_orthogonal_to_left_null_space() -> None:
    assert _model().col_left_null_are_orthogonal()


def test_null_vector_maps_to_zero() -> None:
    model = _model()
    snapshot = model.snapshot()
    assert np.allclose(model.apply(snapshot.null_basis[0]), np.zeros(3), atol=1e-9)


def test_invalid_shape_is_rejected() -> None:
    with pytest.raises(ValueError):
        FundamentalSubspaces(np.eye(2))


def test_rank_three_matrix_is_rejected() -> None:
    with pytest.raises(ValueError):
        FundamentalSubspaces(np.eye(3))
