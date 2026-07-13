import numpy as np
import pytest

from engine.rank_collapse import RankCollapse
from engine.rank_collapse_path import RankCollapsePath
from engine.rank_collapse_display import (
    LinearDisplayProjector,
    RankCollapseDisplayAdapter,
)
from engine.visuals.rank_collapse_manim import (
    ManimRankCollapsePointCloud,
    to_manim_coordinates,
)


class FakePoint:
    def __init__(self, *, point, **kwargs):
        self.position = np.asarray(point, dtype=float)
        self.kwargs = kwargs
        self.move_count = 0

    def move_to(self, point):
        self.position = np.asarray(point, dtype=float)
        self.move_count += 1
        return self


class FakeGroup:
    def __init__(self, *mobjects):
        self.mobjects = list(mobjects)
        self.updaters = []

    def __iter__(self):
        return iter(self.mobjects)

    def __len__(self):
        return len(self.mobjects)

    def add_updater(self, updater):
        self.updaters.append(updater)
        return self

    def run_updaters(self):
        for updater in self.updaters:
            updater(self)


class FakeTracker:
    def __init__(self, value=0.0):
        self.value = float(value)

    def get_value(self):
        return self.value


def make_renderer(display_dimension=2):
    collapse = RankCollapse(np.diag([4.0, 2.0, 1.0]), target_rank=1)
    path = RankCollapsePath(collapse, [[1.0, 1.0, 1.0], [2.0, -1.0, 0.5]])
    projector = LinearDisplayProjector.from_axis_selector(
        3,
        list(range(display_dimension)),
    )
    display = RankCollapseDisplayAdapter(path, projector)
    return ManimRankCollapsePointCloud(display)


@pytest.mark.parametrize(
    "coordinates, expected",
    [
        ([2.0], [2.0, 0.0, 0.0]),
        ([2.0, -1.0], [2.0, -1.0, 0.0]),
        ([2.0, -1.0, 4.0], [2.0, -1.0, 4.0]),
    ],
)
def test_single_vector_is_converted_to_manim_coordinates(coordinates, expected):
    np.testing.assert_allclose(to_manim_coordinates(coordinates), expected)


def test_point_collection_is_padded_row_wise():
    result = to_manim_coordinates([[1.0, 2.0], [-3.0, 4.0]])

    np.testing.assert_allclose(result, [[1.0, 2.0, 0.0], [-3.0, 4.0, 0.0]])


@pytest.mark.parametrize(
    "coordinates",
    [
        [],
        np.empty((2, 0)),
        [1.0, 2.0, 3.0, 4.0],
        [[[1.0, 2.0]]],
        [1.0, np.inf],
    ],
)
def test_invalid_manim_coordinate_inputs_raise(coordinates):
    with pytest.raises(ValueError):
        to_manim_coordinates(coordinates)


def test_scene_points_are_padded_from_display_space():
    renderer = make_renderer(display_dimension=2)

    np.testing.assert_allclose(
        renderer.scene_points_at(0.0),
        [[4.0, 2.0, 0.0], [8.0, -2.0, 0.0]],
    )
    np.testing.assert_allclose(
        renderer.scene_points_at(1.0),
        [[4.0, 0.0, 0.0], [8.0, 0.0, 0.0]],
        atol=1e-12,
    )


def test_scene_basis_images_are_manim_compatible():
    renderer = make_renderer(display_dimension=2)

    result = renderer.scene_basis_images_at(0.0)

    assert result.shape == (3, 3)
    np.testing.assert_allclose(
        result,
        [[4.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 0.0]],
    )


def test_build_point_cloud_uses_injected_factories_and_kwargs():
    renderer = make_renderer(display_dimension=2)

    group = renderer.build_point_cloud(
        0.0,
        point_factory=FakePoint,
        group_factory=FakeGroup,
        point_kwargs={"radius": 0.07, "label": "sample"},
    )

    assert isinstance(group, FakeGroup)
    assert len(group) == renderer.point_count
    assert all(point.kwargs["radius"] == 0.07 for point in group)
    assert all(point.kwargs["label"] == "sample" for point in group)
    np.testing.assert_allclose(group.mobjects[0].position, [4.0, 2.0, 0.0])


def test_update_point_cloud_preserves_point_identity():
    renderer = make_renderer(display_dimension=2)
    group = renderer.build_point_cloud(
        0.0,
        point_factory=FakePoint,
        group_factory=FakeGroup,
    )
    identities = [id(point) for point in group]

    returned = renderer.update_point_cloud(group, 1.0)

    assert returned is group
    assert [id(point) for point in group] == identities
    assert all(point.move_count == 1 for point in group)
    np.testing.assert_allclose(group.mobjects[0].position, [4.0, 0.0, 0.0], atol=1e-12)


def test_update_rejects_wrong_point_count():
    renderer = make_renderer(display_dimension=2)
    group = FakeGroup(FakePoint(point=[0.0, 0.0, 0.0]))

    with pytest.raises(ValueError):
        renderer.update_point_cloud(group, 0.5)


def test_bind_to_tracker_adds_working_updater():
    renderer = make_renderer(display_dimension=2)
    group = renderer.build_point_cloud(
        0.0,
        point_factory=FakePoint,
        group_factory=FakeGroup,
    )
    tracker = FakeTracker(0.0)

    returned = renderer.bind_to_tracker(group, tracker)
    tracker.value = 1.0
    group.run_updaters()

    assert returned is group
    assert len(group.updaters) == 1
    np.testing.assert_allclose(group.mobjects[0].position, [4.0, 0.0, 0.0], atol=1e-12)


def test_sampled_frames_preserve_order_and_shape():
    renderer = make_renderer(display_dimension=1)

    frames = renderer.sampled_scene_frames([1.0, 0.0, 0.5])

    assert len(frames) == 3
    assert all(frame.shape == (2, 3) for frame in frames)
    np.testing.assert_allclose(frames[0][0], [4.0, 0.0, 0.0])
    np.testing.assert_allclose(frames[1][0], [4.0, 0.0, 0.0])


def test_three_dimensional_display_passes_through_all_coordinates():
    renderer = make_renderer(display_dimension=3)

    np.testing.assert_allclose(
        renderer.scene_points_at(0.0),
        [[4.0, 2.0, 1.0], [8.0, -2.0, 0.5]],
    )


def test_renderer_rejects_display_dimension_above_three():
    collapse = RankCollapse(np.eye(4), target_rank=2)
    path = RankCollapsePath(collapse, np.eye(4))
    projector = LinearDisplayProjector(np.eye(4))
    display = RankCollapseDisplayAdapter(path, projector)

    with pytest.raises(ValueError):
        ManimRankCollapsePointCloud(display)


def test_renderer_type_validation():
    with pytest.raises(TypeError):
        ManimRankCollapsePointCloud(np.eye(2))


def test_bind_validation_for_group_and_tracker():
    renderer = make_renderer(display_dimension=2)

    with pytest.raises(TypeError):
        renderer.bind_to_tracker(object(), FakeTracker())

    group = renderer.build_point_cloud(
        0.0,
        point_factory=FakePoint,
        group_factory=FakeGroup,
    )
    with pytest.raises(TypeError):
        renderer.bind_to_tracker(group, object())
