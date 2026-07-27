import numpy as np
import pytest

from engine.row_space import RowSpace

MATRIX = np.array([
    [1.0, 2.0, 1.0],
    [0.0, 1.0, 1.0],
    [1.0, 3.0, 2.0],
])


def _model() -> RowSpace:
    return RowSpace(MATRIX)


def test_snapshot_reports_rank_two() -> None:
    assert _model().snapshot().rank == 2


def test_echelon_form_has_zero_third_row() -> None:
    snapshot = _model().snapshot()
    assert np.allclose(snapshot.echelon_matrix[2], np.zeros(3))


def test_pivot_rows_are_nonzero_rows_of_echelon_form() -> None:
    snapshot = _model().snapshot()
    assert snapshot.pivot_row_indices == (0, 1)
    assert snapshot.pivot_rows.shape == (2, 3)


def test_row_spaces_match_before_and_after_reduction() -> None:
    assert _model().row_spaces_match()


def test_sample_spaces_have_same_rank() -> None:
    model = _model()
    coeffs = np.array([(-1.0, 0.0), (0.0, 1.0), (1.0, 1.0)], dtype=float)
    initial = model.sample_initial_row_space(coeffs)
    pivot = model.sample_pivot_row_space(coeffs)
    assert np.linalg.matrix_rank(initial) == np.linalg.matrix_rank(pivot) == 2


def test_invalid_matrix_shape_is_rejected() -> None:
    with pytest.raises(ValueError):
        RowSpace(np.eye(2))


def test_rank_three_matrix_is_rejected() -> None:
    with pytest.raises(ValueError):
        RowSpace(np.eye(3))
