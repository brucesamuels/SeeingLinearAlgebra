import numpy as np
import pytest

from engine.pivot_columns import PivotColumns

MATRIX = np.array([
    [1.0, 2.0, 1.0],
    [0.0, 1.0, 1.0],
    [1.0, 3.0, 2.0],
])


def _model() -> PivotColumns:
    return PivotColumns(MATRIX)


def test_snapshot_reports_rank_two() -> None:
    assert _model().snapshot().rank == 2


def test_echelon_form_has_expected_pivot_columns() -> None:
    snapshot = _model().snapshot()
    assert np.allclose(snapshot.echelon_matrix, np.array([[1.0, 2.0, 1.0], [0.0, 1.0, 1.0], [0.0, 0.0, 0.0]]))
    assert snapshot.pivot_column_indices == (0, 1)
    assert snapshot.nonpivot_column_indices == (2,)


def test_nonpivot_column_is_combination_of_original_pivot_columns() -> None:
    coefficients = _model().express_nonpivot_column_in_pivot_columns()
    assert np.allclose(coefficients, np.array([-1.0, 1.0]), atol=1e-9)


def test_spans_match_after_removing_nonpivot_column() -> None:
    assert _model().spans_match()


def test_sample_column_space_has_shape_n_by_three() -> None:
    coeffs = np.array([(-1.0, 0.0), (0.0, 1.0), (1.0, 1.0)], dtype=float)
    samples = _model().sample_column_space(coeffs)
    assert samples.shape == (3, 3)


def test_invalid_matrix_shape_is_rejected() -> None:
    with pytest.raises(ValueError):
        PivotColumns(np.eye(2))


def test_rank_three_matrix_is_rejected() -> None:
    with pytest.raises(ValueError):
        PivotColumns(np.eye(3))
