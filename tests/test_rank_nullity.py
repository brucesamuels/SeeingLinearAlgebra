import numpy as np
import pytest

from engine.rank_nullity import RankNullity

MATRIX = np.array([
    [1.0, 2.0, 1.0],
    [0.0, 1.0, 1.0],
    [1.0, 3.0, 2.0],
])
INPUT_VECTOR = np.array([1.5, 0.2, 0.8])


def _model() -> RankNullity:
    return RankNullity(MATRIX)


def test_rank_and_nullity_are_two_and_one() -> None:
    model = _model()
    assert model.rank == 2
    assert model.nullity == 1


def test_decomposition_components_sum_to_input_vector() -> None:
    decomposition = _model().decompose(INPUT_VECTOR)
    assert np.allclose(
        decomposition.row_component + decomposition.null_component,
        decomposition.input_vector,
        atol=1e-9,
    )


def test_null_component_lies_in_null_space() -> None:
    model = _model()
    decomposition = model.decompose(INPUT_VECTOR)
    assert model.is_in_null_space(decomposition.null_component)
    assert np.allclose(model.apply(decomposition.null_component), np.zeros(3), atol=1e-9)


def test_row_component_and_full_input_have_same_output() -> None:
    model = _model()
    decomposition = model.decompose(INPUT_VECTOR)
    assert np.allclose(model.apply(decomposition.input_vector), model.apply(decomposition.row_component), atol=1e-9)


def test_row_component_is_orthogonal_to_null_direction() -> None:
    model = _model()
    decomposition = model.decompose(INPUT_VECTOR)
    assert abs(np.dot(decomposition.row_component, model.null_direction)) <= 1e-9


def test_sample_row_space_has_shape_n_by_three() -> None:
    coeffs = np.array([(-1.0, 0.0), (0.0, 1.0), (1.0, 1.0)], dtype=float)
    samples = _model().sample_row_space(coeffs)
    assert samples.shape == (3, 3)


def test_invalid_matrix_shape_is_rejected() -> None:
    with pytest.raises(ValueError):
        RankNullity(np.eye(2))
