import inspect

import numpy as np
import pytest

from engine.directed_page_rank import DirectedPageRank


def test_default_directed_graph_preserves_recurring_skeleton_and_directions():
    model = DirectedPageRank()
    assert model.vertices == (1, 2, 3, 4)
    assert model.directed_edges == ((1, 2), (2, 3), (3, 1), (3, 4))
    assert model.out_neighbors(3) == (1, 4)
    assert model.in_neighbors(3) == (2,)
    assert model.out_degree_vector().tolist() == [1, 1, 2, 0]
    assert model.dangling_vertices() == (4,)


def test_adjacency_uses_columns_as_sources():
    model = DirectedPageRank()
    assert model.adjacency_matrix().tolist() == [
        [0, 0, 1, 0],
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
    ]


def test_raw_link_matrix_has_zero_dangling_column():
    model = DirectedPageRank()
    expected = np.array(
        [
            [0, 0, 1 / 2, 0],
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1 / 2, 0],
        ]
    )
    assert model.raw_link_matrix() == pytest.approx(expected)
    assert model.raw_link_matrix().sum(axis=0) == pytest.approx([1, 1, 1, 0])


def test_dangling_repair_replaces_column_four_uniformly():
    model = DirectedPageRank()
    repaired = model.repaired_link_matrix()
    assert repaired[:, 3] == pytest.approx([1 / 4] * 4)
    assert repaired.sum(axis=0) == pytest.approx(np.ones(4))


def test_uniform_teleportation_matrix_has_identical_columns():
    model = DirectedPageRank()
    assert model.uniform_distribution() == pytest.approx([1 / 4] * 4)
    assert model.teleportation_matrix() == pytest.approx(np.full((4, 4), 1 / 4))


def test_google_matrix_is_exact_for_one_half_damping():
    model = DirectedPageRank()
    expected = np.array(
        [
            [1 / 8, 1 / 8, 3 / 8, 1 / 4],
            [5 / 8, 1 / 8, 1 / 8, 1 / 4],
            [1 / 8, 5 / 8, 1 / 8, 1 / 4],
            [1 / 8, 1 / 8, 3 / 8, 1 / 4],
        ]
    )
    assert model.google_matrix() == pytest.approx(expected)
    assert model.column_sums() == pytest.approx(np.ones(4))
    assert np.all(model.google_matrix() > 0)


def test_first_two_updates_from_uniform_are_exact():
    model = DirectedPageRank()
    p0, p1, p2 = model.trajectory(model.uniform_distribution(), 2)
    assert p0 == pytest.approx([1 / 4] * 4)
    assert p1 == pytest.approx([7 / 32, 9 / 32, 9 / 32, 7 / 32])
    assert p2 == pytest.approx([57 / 256, 67 / 256, 75 / 256, 57 / 256])


def test_exact_page_rank_is_stationary_and_normalized():
    model = DirectedPageRank()
    rank = model.page_rank()
    assert rank == pytest.approx([11 / 49, 13 / 49, 2 / 7, 11 / 49])
    assert rank.sum() == pytest.approx(1)
    assert model.stationary_residual() == pytest.approx(np.zeros(4), abs=1e-12)


def test_rank_order_preserves_exact_tie():
    assert DirectedPageRank().rank_order() == ((3,), (2,), (1, 4))


def test_trajectory_converges_to_page_rank():
    model = DirectedPageRank()
    trajectory = model.trajectory(model.uniform_distribution(), 14)
    distances = [model.total_variation_distance(state, model.page_rank()) for state in trajectory]
    assert distances[-1] < 1e-6
    assert distances[-1] < distances[0]


@pytest.mark.parametrize("damping", (-0.1, 1, 1.1, np.inf, np.nan, True, "half"))
def test_invalid_damping_is_rejected(damping):
    with pytest.raises(ValueError, match="damping"):
        DirectedPageRank().google_matrix(damping)


@pytest.mark.parametrize(
    "distribution",
    (
        (1, 0, 0),
        (1, 0, 0, 0, 0),
        (0.5, 0.5, 0, np.nan),
        (1.1, -0.1, 0, 0),
        (0.2, 0.2, 0.2, 0.2),
    ),
)
def test_invalid_distributions_are_rejected(distribution):
    with pytest.raises(ValueError, match="distribution"):
        DirectedPageRank().next_distribution(distribution)


@pytest.mark.parametrize("steps", (-1, 1.5, True))
def test_invalid_step_counts_are_rejected(steps):
    with pytest.raises(ValueError, match="nonnegative integer"):
        DirectedPageRank().trajectory([1 / 4] * 4, steps)


@pytest.mark.parametrize(
    ("vertices", "edges", "message"),
    (
        ((), (), "nonempty"),
        ((1, 1), (), "unique"),
        ((1, 2), ((1, 3),), "known vertices"),
        ((1, 2), ((1, 1),), "loops"),
        ((1, 2), ((1, 2), (1, 2)), "unique"),
        ((1, 2), ((1, 2, 3),), "source and destination"),
    ),
)
def test_invalid_directed_graphs_are_rejected(vertices, edges, message):
    with pytest.raises(ValueError, match=message):
        DirectedPageRank(vertices, edges)


def test_unknown_vertex_queries_are_rejected():
    model = DirectedPageRank()
    with pytest.raises(ValueError, match="unknown vertex"):
        model.out_neighbors(9)
    with pytest.raises(ValueError, match="unknown vertex"):
        model.in_neighbors(9)


def test_model_has_no_renderer_dependency():
    module = inspect.getmodule(DirectedPageRank)
    source = inspect.getsource(module)
    assert "from manim" not in source
    assert "import manim" not in source
