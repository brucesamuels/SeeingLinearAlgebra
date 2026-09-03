import inspect

import numpy as np
import pytest

from engine.svd_conditioning import SVDConditioning


def test_default_matrix_has_expected_singular_values_and_inverse():
    model = SVDConditioning()
    assert np.allclose(model.matrix, [[4, 0], [0, 0.25]])
    assert np.allclose(model.singular_values(), [4, 0.25])
    assert np.allclose(model.inverse_singular_values(), [0.25, 4])
    assert np.allclose(model.inverse(), [[0.25, 0], [0, 4]])


def test_default_map_is_invertible_but_ill_conditioned():
    model = SVDConditioning()
    assert model.is_invertible()
    assert model.condition_number() == pytest.approx(16)
    assert model.condition_number() == pytest.approx(np.linalg.cond(model.matrix, 2))


def test_forward_and_inverse_maps_round_trip():
    model = SVDConditioning()
    vector = np.array([1.5, -2.0])
    assert np.allclose(model.solve(model.apply(vector)), vector)


def test_equal_output_perturbations_have_unequal_inverse_responses():
    model = SVDConditioning()
    epsilon = 0.08
    assert model.inverse_response_norm("strong", epsilon) == pytest.approx(epsilon / 4)
    assert model.inverse_response_norm("weak", epsilon) == pytest.approx(4 * epsilon)
    assert model.sensitivity_ratio() == pytest.approx(16)


def test_singular_directions_match_coordinate_axes_up_to_sign():
    model = SVDConditioning()
    assert np.allclose(np.abs(model.strongest_input_direction()), [1, 0])
    assert np.allclose(np.abs(model.weakest_input_direction()), [0, 1])
    assert np.allclose(np.abs(model.strongest_output_direction()), [1, 0])
    assert np.allclose(np.abs(model.weakest_output_direction()), [0, 1])


def test_relative_error_bound_holds_for_representative_perturbations():
    model = SVDConditioning()
    for perturbation in ([0.01, 0], [0, 0.01], [0.01, -0.02]):
        assert model.satisfies_relative_error_bound([4, 0.25], perturbation)


def test_singular_matrix_has_infinite_condition_number_and_no_inverse():
    model = SVDConditioning([[4, 0], [0, 0]])
    assert not model.is_invertible()
    assert np.isinf(model.condition_number())
    assert np.allclose(model.inverse_singular_values()[0], 0.25)
    assert np.isinf(model.inverse_singular_values()[1])
    with pytest.raises(ValueError, match="singular"):
        model.inverse()


@pytest.mark.parametrize(
    "matrix, message",
    (([1, 2], "two by two"), ([[1, 2, 3], [4, 5, 6]], "two by two"), ([[1, 0], [0, np.inf]], "finite")),
)
def test_invalid_matrices_are_rejected(matrix, message):
    with pytest.raises(ValueError, match=message):
        SVDConditioning(matrix)


@pytest.mark.parametrize("tolerance", (-1, np.inf, np.nan))
def test_invalid_tolerances_are_rejected(tolerance):
    with pytest.raises(ValueError, match="tolerance"):
        SVDConditioning(tolerance=tolerance)


@pytest.mark.parametrize("vector", ([1], [1, 2, 3], [1, np.inf]))
def test_invalid_input_vectors_are_rejected(vector):
    with pytest.raises(ValueError, match="input vector"):
        SVDConditioning().apply(vector)


@pytest.mark.parametrize("lane", ("middle", "", None))
def test_invalid_lanes_are_rejected(lane):
    with pytest.raises(ValueError, match="lane"):
        SVDConditioning().inverse_response_norm(lane)


@pytest.mark.parametrize("magnitude", (-1, np.inf, np.nan, [1]))
def test_invalid_magnitudes_are_rejected(magnitude):
    with pytest.raises(ValueError, match="magnitude"):
        SVDConditioning().inverse_response_norm("weak", magnitude)


def test_engine_has_no_renderer_dependency():
    source = inspect.getsource(inspect.getmodule(SVDConditioning))
    assert "from manim" not in source
    assert "import manim" not in source
