import inspect

import numpy as np
import pytest

from engine.svd_image_compression import SVDImageCompression


def test_default_image_is_deterministic_grayscale_landscape():
    first = SVDImageCompression()
    second = SVDImageCompression()
    assert first.shape == (32, 32)
    assert np.allclose(first.original(), second.original())
    assert np.min(first.original()) >= 0
    assert np.max(first.original()) <= 1
    assert np.std(first.original()) > 0.1


def test_singular_values_are_nonnegative_and_descending():
    values = SVDImageCompression().singular_values()
    assert len(values) == 32
    assert np.all(values >= 0)
    assert np.all(values[:-1] >= values[1:])


@pytest.mark.parametrize("rank", (0, 1, 4, 8, 32))
def test_reconstructions_have_image_shape_and_finite_values(rank):
    model = SVDImageCompression()
    reconstruction = model.reconstruction(rank)
    assert reconstruction.shape == model.shape
    assert np.all(np.isfinite(reconstruction))
    clipped = model.reconstruction(rank, clip=True)
    assert np.min(clipped) >= 0
    assert np.max(clipped) <= 1


def test_full_rank_reconstructs_original_image():
    model = SVDImageCompression()
    assert np.allclose(model.reconstruction(model.maximum_rank), model.original())
    assert model.frobenius_error(model.maximum_rank) == pytest.approx(0, abs=1e-12)
    assert model.retained_energy(model.maximum_rank) == pytest.approx(1)


def test_error_decreases_and_energy_increases_with_rank():
    model = SVDImageCompression()
    ranks = (0, 1, 4, 8, model.maximum_rank)
    errors = [model.frobenius_error(rank) for rank in ranks]
    energies = [model.retained_energy(rank) for rank in ranks]
    assert all(left >= right for left, right in zip(errors, errors[1:]))
    assert all(left <= right for left, right in zip(energies, energies[1:]))
    assert energies[0] == pytest.approx(0)


@pytest.mark.parametrize("rank", (1, 4, 8))
def test_energy_and_relative_error_obey_pythagorean_identity(rank):
    model = SVDImageCompression()
    error_fraction = model.relative_frobenius_error(rank) ** 2
    assert model.retained_energy(rank) + error_fraction == pytest.approx(1)


def test_storage_counts_for_thirty_two_square_image():
    model = SVDImageCompression()
    assert model.original_storage() == 1024
    assert model.compressed_storage(4) == 260
    assert model.storage_fraction(4) == pytest.approx(260 / 1024)
    assert model.compression_ratio(4) == pytest.approx(1024 / 260)


def test_custom_rectangular_image_uses_correct_storage_formula():
    model = SVDImageCompression(np.full((12, 20), 0.5))
    assert model.maximum_rank == 12
    assert model.original_storage() == 240
    assert model.compressed_storage(3) == 3 * (12 + 20 + 1)


@pytest.mark.parametrize("image", ([], [0.2, 0.4], [[np.inf]], [[-0.1]], [[1.1]], [[0.0]]))
def test_invalid_images_are_rejected(image):
    with pytest.raises(ValueError, match="image"):
        SVDImageCompression(image)


@pytest.mark.parametrize("size", (7, 8.5, True))
def test_invalid_synthetic_image_sizes_are_rejected(size):
    with pytest.raises(ValueError, match="size"):
        SVDImageCompression.synthetic_landscape(size)


@pytest.mark.parametrize("rank", (-1, 33, 1.5, True))
def test_invalid_ranks_are_rejected(rank):
    with pytest.raises(ValueError, match="rank"):
        SVDImageCompression().reconstruction(rank)


def test_zero_rank_has_no_compressed_storage_representation():
    with pytest.raises(ValueError, match="positive"):
        SVDImageCompression().compressed_storage(0)


def test_engine_composes_cp220_model_and_has_no_renderer_dependency():
    source = inspect.getsource(inspect.getmodule(SVDImageCompression))
    assert "from engine.truncated_svd_approximation import TruncatedSVDApproximation" in source
    assert "from manim" not in source
    assert "import manim" not in source
