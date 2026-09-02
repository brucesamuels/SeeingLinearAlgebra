import inspect

import numpy as np
import pytest

from engine.svd_pseudoinverse import SVDPseudoinverse


def test_default_singular_values_and_reciprocal_rule():
    model = SVDPseudoinverse()
    assert np.allclose(model.singular_values(), [2, 0])
    assert np.allclose(model.reciprocal_singular_values(), [0.5, 0])
    assert np.allclose(model.sigma_pseudoinverse(), [[0.5, 0, 0], [0, 0, 0]])


def test_default_pseudoinverse_has_expected_values_and_shape():
    model = SVDPseudoinverse()
    expected = [[0.25, 0.25, 0], [0.25, 0.25, 0]]
    assert model.pseudoinverse().shape == (2, 3)
    assert np.allclose(model.pseudoinverse(), expected)
    assert np.allclose(model.pseudoinverse(), np.linalg.pinv(model.matrix))


def test_pseudoinverse_reverses_active_direction_and_not_null_direction():
    model = SVDPseudoinverse()
    v_one = model.active_right_direction()
    v_two = model.null_direction()
    u_one = model.active_left_direction()
    assert np.allclose(model.apply(v_one), 2 * u_one)
    assert np.allclose(model.apply_pseudoinverse(u_one), 0.5 * v_one)
    assert np.allclose(model.domain_round_trip(v_one), v_one)
    assert np.allclose(model.domain_round_trip(v_two), 0)


def test_domain_round_trip_is_row_space_projection():
    model = SVDPseudoinverse()
    expected = np.array([[0.5, 0.5], [0.5, 0.5]])
    projector = model.row_projection()
    assert np.allclose(projector, expected)
    assert np.allclose(projector.T, projector)
    assert np.allclose(projector @ projector, projector)
    assert np.allclose(model.domain_round_trip([3, -1]), expected @ [3, -1])


def test_output_round_trip_is_column_space_projection():
    model = SVDPseudoinverse()
    expected = np.array([[0.5, 0.5, 0], [0.5, 0.5, 0], [0, 0, 0]])
    projector = model.column_projection()
    assert np.allclose(projector, expected)
    assert np.allclose(projector.T, projector)
    assert np.allclose(projector @ projector, projector)
    assert np.allclose(model.output_round_trip([2, -1, 3]), expected @ [2, -1, 3])


def test_round_trips_satisfy_reconstruction_identities():
    model = SVDPseudoinverse()
    a = model.matrix
    plus = model.pseudoinverse()
    assert np.allclose(a @ plus @ a, a)
    assert np.allclose(plus @ a @ plus, plus)


@pytest.mark.parametrize("vector", ([1], [1, 2, 3], [1, np.inf]))
def test_invalid_domain_vectors_are_rejected(vector):
    with pytest.raises(ValueError, match="domain vector"):
        SVDPseudoinverse().domain_round_trip(vector)


@pytest.mark.parametrize("vector", ([1], [1, 2], [1, 2, np.inf]))
def test_invalid_output_vectors_are_rejected(vector):
    with pytest.raises(ValueError, match="output vector"):
        SVDPseudoinverse().output_round_trip(vector)


def test_engine_composes_cp216_structure_and_has_no_renderer_dependency():
    source = inspect.getsource(inspect.getmodule(SVDPseudoinverse))
    assert "from engine.svd_fundamental_subspaces import SVDFundamentalSubspaces" in source
    assert "from manim" not in source
    assert "import manim" not in source
