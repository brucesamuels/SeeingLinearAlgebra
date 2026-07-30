import numpy as np
import pytest

from engine.planar_affine_transformation import (
    PlanarAffineTransformation,
    PlanarTransformationGeometry,
)


def test_rotation_by_quarter_turn() -> None:
    transform = PlanarAffineTransformation.rotation(np.pi / 2)
    assert np.allclose(transform.apply((1.0, 0.0)), (0.0, 1.0))


def test_reflection_through_x_axis() -> None:
    transform = PlanarAffineTransformation.reflection((1.0, 0.0))
    assert np.allclose(transform.apply((2.0, 3.0)), (2.0, -3.0))


def test_projection_onto_x_axis_collapses_y_coordinate() -> None:
    transform = PlanarAffineTransformation.projection((1.0, 0.0))
    assert np.allclose(transform.apply((2.0, 3.0)), (2.0, 0.0))


def test_translation_moves_origin_and_is_not_linear() -> None:
    transform = PlanarAffineTransformation.translation((1.25, -0.5))
    assert np.allclose(transform.apply((0.0, 0.0)), (1.25, -0.5))
    assert not transform.fixes_origin
    assert not transform.is_linear


def test_zero_offset_affine_map_is_linear() -> None:
    transform = PlanarAffineTransformation.shear_x(0.75)
    assert transform.fixes_origin
    assert transform.is_linear


def test_interpolation_begins_at_identity_and_ends_at_target() -> None:
    transform = PlanarAffineTransformation.translation((2.0, 1.0))
    assert np.allclose(transform.interpolate(0).apply((3.0, 4.0)), (3.0, 4.0))
    assert np.allclose(transform.interpolate(1).apply((3.0, 4.0)), (5.0, 5.0))


def test_geometry_snapshot_transforms_every_stage_element() -> None:
    geometry = PlanarTransformationGeometry(
        vector_endpoints=((2.0, 1.0),),
        polygon_vertices=((0.0, 0.0), (1.0, 0.0), (0.0, 1.0)),
        grid_extent=2,
    )
    transform = PlanarAffineTransformation.translation((1.0, 2.0))
    snapshot = geometry.snapshot(transform)

    assert np.allclose(snapshot.origin, (1.0, 2.0))
    assert np.allclose(snapshot.basis_endpoints, ((2.0, 2.0), (1.0, 3.0)))
    assert np.allclose(snapshot.vector_endpoints, ((3.0, 3.0),))
    assert np.allclose(snapshot.polygon_vertices[0], (1.0, 2.0))
    assert snapshot.grid_segments.ndim == 3
    assert snapshot.grid_segments.shape[1:] == (2, 2)


@pytest.mark.parametrize("progress", [-0.01, 1.01, np.nan])
def test_interpolation_rejects_invalid_progress(progress: float) -> None:
    with pytest.raises(ValueError):
        PlanarAffineTransformation(np.eye(2)).interpolate(progress)
