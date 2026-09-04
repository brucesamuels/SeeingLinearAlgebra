import inspect

import numpy as np
import pytest

from engine.pca_svd import PCASVD


def test_default_centered_dataset_and_gram_matrix_are_exact():
    model = PCASVD()
    assert model.shape == (6, 2)
    assert np.allclose(model.mean(), [0, 0])
    assert np.allclose(model.centered_data(), model.data())
    assert np.allclose(model.gram_matrix(), [[28, 26], [26, 28]])


def test_principal_directions_and_singular_values_are_exact():
    model = PCASVD()
    root_two = np.sqrt(2)
    assert np.allclose(model.singular_values(), [np.sqrt(54), np.sqrt(2)])
    assert np.allclose(model.principal_directions()[:, 0], [1 / root_two, 1 / root_two])
    assert np.allclose(model.principal_directions()[:, 1], [1 / root_two, -1 / root_two])


def test_covariance_and_explained_variance_use_sample_scaling():
    model = PCASVD()
    assert np.allclose(model.covariance_matrix(), model.gram_matrix() / 5)
    assert np.allclose(model.explained_variance(), [54 / 5, 2 / 5])
    assert model.explained_variance_ratio(1) == pytest.approx(54 / 56)
    assert model.explained_variance_ratio(2) == pytest.approx(1)


def test_scores_are_coordinates_along_principal_directions():
    model = PCASVD()
    scores = model.scores(1)
    assert scores.shape == (6, 1)
    assert np.allclose(scores, model.centered_data() @ model.principal_directions()[:, :1])
    assert np.linalg.norm(scores) == pytest.approx(model.singular_values()[0])


def test_rank_one_reconstruction_projects_every_point_onto_y_equals_x():
    model = PCASVD()
    reconstruction = model.reconstruction(1)
    assert np.allclose(reconstruction[:, 0], reconstruction[:, 1])
    assert np.allclose(reconstruction[:4], [[2.5, 2.5], [2.5, 2.5], [-2.5, -2.5], [-2.5, -2.5]])
    assert np.allclose(reconstruction[4:], [[1, 1], [-1, -1]])


def test_rank_one_error_matches_discarded_singular_value():
    model = PCASVD()
    assert model.frobenius_error(1) == pytest.approx(np.sqrt(2))
    assert model.relative_frobenius_error(1) == pytest.approx(np.sqrt(2 / 56))
    assert model.explained_variance_ratio(1) + model.relative_frobenius_error(1) ** 2 == pytest.approx(1)


def test_full_reconstruction_recovers_original_data_and_zero_rank_recovers_mean():
    model = PCASVD()
    assert np.allclose(model.reconstruction(2), model.data())
    assert np.allclose(model.reconstruction(0), np.zeros_like(model.data()))


def test_noncentered_custom_data_is_centered_and_mean_is_restored():
    shifted = PCASVD.example_data() + [10, -4]
    model = PCASVD(shifted)
    assert np.allclose(model.mean(), [10, -4])
    assert np.allclose(np.mean(model.centered_data(), axis=0), [0, 0])
    assert np.allclose(model.reconstruction(2), shifted)
    assert np.allclose(model.reconstruction(0), np.tile([10, -4], (6, 1)))


@pytest.mark.parametrize("data", ([], [[1, 2]], [1, 2], [[1, np.inf], [2, 3]], [[1, 1], [1, 1]]))
def test_invalid_datasets_are_rejected(data):
    with pytest.raises(ValueError, match="data"):
        PCASVD(data)


@pytest.mark.parametrize("components", (-1, 3, 1.5, True))
def test_invalid_component_counts_are_rejected(components):
    with pytest.raises(ValueError, match="components"):
        PCASVD().reconstruction(components)


def test_engine_composes_truncated_svd_and_has_no_renderer_dependency():
    source = inspect.getsource(inspect.getmodule(PCASVD))
    assert "from engine.truncated_svd_approximation import TruncatedSVDApproximation" in source
    assert "from manim" not in source
    assert "import manim" not in source
