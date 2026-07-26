import numpy as np
import pytest

from engine.rank_collapse_3d import RankCollapse3D


def _model() -> RankCollapse3D:
    triples = np.array([(a,b,c) for a in (-1,0,1) for b in (-1,0,1) for c in (-1,0,1)], dtype=float)
    return RankCollapse3D([2.1,0.15,0.15], [0.25,1.75,0.35], [0.2,-0.3,1.75], triples)


def test_states_have_expected_ranks() -> None:
    model = _model()
    assert model.space_to_plane(0).rank == 3
    assert model.space_to_plane(1).rank == 2
    assert model.plane_to_line(1).rank == 1


def test_determinant_collapses_to_zero_at_rank_two() -> None:
    model = _model()
    assert abs(model.space_to_plane(0).determinant) > 0.1
    assert model.space_to_plane(1).determinant == pytest.approx(0.0, abs=1e-10)


def test_rank_one_endpoints_are_collinear() -> None:
    snapshot = _model().plane_to_line(1)
    assert np.linalg.matrix_rank(snapshot.endpoints, tol=1e-9) == 1


def test_snapshots_are_read_only() -> None:
    snapshot = _model().space_to_plane(0.5)
    assert not snapshot.endpoints.flags.writeable
    assert not snapshot.parallelepiped_corners.flags.writeable


def test_progress_must_lie_in_unit_interval() -> None:
    model = _model()
    with pytest.raises(ValueError):
        model.space_to_plane(1.1)


def test_space_to_plane_moves_along_an_arc_not_a_straight_blend() -> None:
    model = _model()
    start = model.space_to_plane(0.0).generator_w
    end = model.space_to_plane(1.0).generator_w
    midpoint = model.space_to_plane(0.5).generator_w
    linear_midpoint = 0.5 * (start + end)
    assert np.linalg.norm(midpoint - linear_midpoint) > 0.05


def test_plane_to_line_uses_curved_direction_changes() -> None:
    model = _model()
    start = model.plane_to_line(0.0).generator_v
    end = model.plane_to_line(1.0).generator_v
    midpoint = model.plane_to_line(0.5).generator_v
    linear_midpoint = 0.5 * (start + end)
    assert np.linalg.norm(midpoint - linear_midpoint) > 0.03
