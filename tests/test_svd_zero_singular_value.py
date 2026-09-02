import inspect

import numpy as np
import pytest

from engine.svd_zero_singular_value import ZeroSingularValueModel


def test_default_numerical_spine():
    model = ZeroSingularValueModel()
    root_two = np.sqrt(2)
    assert np.allclose(model.matrix, [[1, 1], [1, 1]])
    assert np.allclose(model.gram_matrix(), [[2, 2], [2, 2]])
    assert np.allclose(model.singular_values(), [2, 0])
    assert np.allclose(model.active_right_direction(), [1 / root_two, 1 / root_two])
    assert np.allclose(model.null_direction(), [1 / root_two, -1 / root_two])
    assert np.allclose(model.active_left_direction(), [1 / root_two, 1 / root_two])


def test_active_and_null_directions_have_expected_images():
    model = ZeroSingularValueModel()
    assert np.allclose(model.apply(model.active_right_direction()), 2 * model.active_left_direction())
    assert np.allclose(model.apply(model.null_direction()), [0, 0])


def test_rank_nullity_and_positive_singular_value_count_agree():
    model = ZeroSingularValueModel()
    assert model.rank() == 1
    assert model.nullity() == 1
    assert np.count_nonzero(model.singular_values() > 1e-12) == model.rank()


def test_unit_circle_maps_to_active_output_line_segment():
    model = ZeroSingularValueModel()
    mapped = model.mapped_circle_samples(64)
    active = model.active_left_direction()
    perpendicular = np.array([-active[1], active[0]])
    assert np.allclose(mapped @ perpendicular, 0)
    assert np.max(np.linalg.norm(mapped, axis=1)) == pytest.approx(2)


def test_reduced_factorization_reconstructs_rank_one_matrix():
    model = ZeroSingularValueModel()
    u, sigma, vt = model.reduced_factorization()
    assert u.shape == (2, 1)
    assert sigma.shape == (1, 1)
    assert vt.shape == (1, 2)
    assert np.allclose(u @ sigma @ vt, model.matrix)
    assert np.allclose(model.reduced_reconstruction(), model.matrix)


@pytest.mark.parametrize("matrix", ([[1, 0], [0, 1]], [[0, 0], [0, 0]]))
def test_model_requires_nonzero_rank_one_matrix(matrix):
    with pytest.raises(ValueError, match="rank one"):
        ZeroSingularValueModel(matrix)


@pytest.mark.parametrize("matrix", ([1, 1], [[1, 1, 1], [1, 1, 1]], [[1, np.inf], [1, 1]]))
def test_invalid_matrices_are_rejected(matrix):
    with pytest.raises(ValueError, match="matrix"):
        ZeroSingularValueModel(matrix)


@pytest.mark.parametrize("vector", ([1], [1, 2, 3], [1, np.inf]))
def test_invalid_vectors_are_rejected(vector):
    with pytest.raises(ValueError, match="vector"):
        ZeroSingularValueModel().apply(vector)


@pytest.mark.parametrize("count", (True, 7, 8.5))
def test_invalid_circle_sample_counts_are_rejected(count):
    with pytest.raises(ValueError, match="count"):
        ZeroSingularValueModel().circle_samples(count)


def test_engine_reuses_rank_collapse_and_has_no_renderer_dependency():
    module = inspect.getmodule(ZeroSingularValueModel)
    source = inspect.getsource(module)
    assert "from engine.rank_collapse import RankCollapse" in source
    assert "from manim" not in source
    assert "import manim" not in source
