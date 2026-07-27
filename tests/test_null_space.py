import numpy as np
import pytest

from engine.null_space import NullSpace


MATRIX = np.array([
    [2.0, -0.5, 1.5],
    [0.5, 1.8, 2.3],
    [0.5, 0.8, 1.3],
])


def test_null_vector_maps_to_zero() -> None:
    model = NullSpace(MATRIX)
    snapshot = model.snapshot(model.null_vector)
    assert np.allclose(snapshot.output_vector, np.zeros(3), atol=1e-9)


def test_scalar_multiples_of_null_vector_map_to_zero() -> None:
    model = NullSpace(MATRIX)
    inputs = model.scalar_multiples(np.array([-2.0, -1.0, 0.0, 1.0, 2.0]))
    outputs = model.sample_outputs(inputs)
    assert np.allclose(outputs, 0.0, atol=1e-9)


def test_rank_and_nullity_match_rank_nullity_theorem() -> None:
    model = NullSpace(MATRIX)
    assert model.rank == 2
    assert model.nullity == 1
    assert model.rank + model.nullity == 3


def test_generic_input_is_not_in_null_space() -> None:
    model = NullSpace(MATRIX)
    assert not model.is_in_null_space(np.array([1.0, 0.0, 0.0]))


def test_snapshot_computes_matrix_vector_product() -> None:
    model = NullSpace(MATRIX)
    vector = np.array([1.1, -0.6, 0.7])
    snapshot = model.snapshot(vector)
    assert np.allclose(snapshot.output_vector, MATRIX @ vector)


def test_invalid_matrix_shape_is_rejected() -> None:
    with pytest.raises(ValueError):
        NullSpace(np.eye(2))


def test_invertible_matrix_is_rejected() -> None:
    with pytest.raises(ValueError):
        NullSpace(np.eye(3))
