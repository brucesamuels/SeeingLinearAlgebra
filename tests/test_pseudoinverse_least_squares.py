import inspect

import numpy as np
import pytest

from engine.pseudoinverse_least_squares import PseudoinverseLeastSquares


def test_default_target_is_inconsistent_and_projects_to_image():
    model = PseudoinverseLeastSquares()
    assert np.allclose(model.target, [3, 1, 2])
    assert not model.is_consistent()
    assert np.allclose(model.closest_output(), [2, 2, 0])
    assert np.allclose(model.residual(), [1, -1, 2])


def test_pseudoinverse_selects_expected_preimage():
    model = PseudoinverseLeastSquares()
    assert np.allclose(model.solution(), [1, 1])
    assert np.allclose(model.matrix @ model.solution(), model.closest_output())
    assert np.allclose(model.normal_equation_residual(), [0, 0])


@pytest.mark.parametrize("parameter", (-3, -0.5, 0, 2.5))
def test_solution_family_has_same_closest_output_and_error(parameter):
    model = PseudoinverseLeastSquares()
    expected = [1 + parameter, 1 - parameter]
    assert np.allclose(model.solution_family(parameter), expected)
    assert np.allclose(model.family_output(parameter), [2, 2, 0])
    assert model.squared_residual_norm(expected) == pytest.approx(6.0)


@pytest.mark.parametrize("parameter", (-3, -0.5, 0, 2.5))
def test_pseudoinverse_solution_is_unique_minimum_norm_family_member(parameter):
    model = PseudoinverseLeastSquares()
    assert model.squared_solution_norm(parameter) == pytest.approx(2 + 2 * parameter**2)
    assert model.squared_solution_norm(parameter) >= model.squared_solution_norm(0)
    if parameter != 0:
        assert model.squared_solution_norm(parameter) > model.squared_solution_norm(0)


def test_consistent_target_still_selects_row_space_preimage():
    model = PseudoinverseLeastSquares(target=[4, 4, 0])
    assert model.is_consistent()
    assert np.allclose(model.solution(), [2, 2])
    assert np.allclose(model.solution_family(3), [5, -1])
    assert np.allclose(model.family_output(3), [4, 4, 0])


@pytest.mark.parametrize("target", ([1], [1, 2], [1, 2, 3, 4], [1, 2, np.inf]))
def test_invalid_targets_are_rejected(target):
    with pytest.raises(ValueError, match="target"):
        PseudoinverseLeastSquares(target=target)


@pytest.mark.parametrize("parameter", ([1], np.inf, np.nan))
def test_invalid_parameters_are_rejected(parameter):
    with pytest.raises(ValueError, match="parameter"):
        PseudoinverseLeastSquares().solution_family(parameter)


@pytest.mark.parametrize("candidate", ([1], [1, 2, 3], [1, np.inf]))
def test_invalid_candidates_are_rejected(candidate):
    with pytest.raises(ValueError, match="candidate"):
        PseudoinverseLeastSquares().squared_residual_norm(candidate)


def test_engine_composes_cp217_model_and_has_no_renderer_dependency():
    source = inspect.getsource(inspect.getmodule(PseudoinverseLeastSquares))
    assert "from engine.svd_pseudoinverse import SVDPseudoinverse" in source
    assert "from manim" not in source
    assert "import manim" not in source
