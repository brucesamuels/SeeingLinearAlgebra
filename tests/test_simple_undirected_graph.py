import inspect

import pytest

from engine.simple_undirected_graph import SimpleUndirectedGraph, triangle_with_tail_graph


def test_triangle_with_tail_has_expected_vertices_edges_neighbors_and_degrees():
    graph = triangle_with_tail_graph()
    assert graph.vertices == (1, 2, 3, 4)
    assert graph.edges == ((1, 2), (2, 3), (1, 3), (3, 4))
    assert graph.neighbors(1) == (2, 3)
    assert graph.neighbors(3) == (1, 2, 4)
    assert graph.degree_sequence() == (2, 2, 3, 1)


def test_adjacency_is_symmetric_and_absent_edges_remain_absent():
    graph = triangle_with_tail_graph()
    assert graph.is_adjacent(1, 3)
    assert graph.is_adjacent(3, 1)
    assert not graph.is_adjacent(1, 4)


def test_walk_may_repeat_vertices_and_edges_but_path_may_not():
    graph = triangle_with_tail_graph()
    repeated = (4, 3, 1, 2, 3, 1)
    path = (4, 3, 1, 2)
    assert graph.is_walk(repeated)
    assert graph.walk_length(repeated) == 5
    assert not graph.is_path(repeated)
    assert graph.is_path(path)
    assert graph.walk_length(path) == 3


def test_invalid_route_is_not_a_walk_and_has_no_walk_length():
    graph = triangle_with_tail_graph()
    assert not graph.is_walk((1, 4))
    assert not graph.is_walk(())
    assert not graph.is_walk((1, 99))
    with pytest.raises(ValueError, match="walk"):
        graph.walk_length((1, 4))


def test_bridge_removal_reveals_two_connected_components():
    graph = triangle_with_tail_graph()
    assert graph.is_connected()
    assert graph.connected_components() == ((1, 2, 3, 4),)
    separated = graph.without_edge((4, 3))
    assert not separated.is_connected()
    assert separated.connected_components() == ((1, 2, 3), (4,))
    assert separated.degree_sequence() == (2, 2, 2, 0)


@pytest.mark.parametrize(
    "vertices, edges, message",
    (
        ((), (), "nonempty"),
        ((1, 1), (), "unique"),
        ((1, 2), ((1, 1),), "loops"),
        ((1, 2), ((1, 2), (2, 1)), "repeated"),
        ((1, 2), ((1, 3),), "endpoints"),
        ((1, 2), ((1,),), "two endpoints"),
    ),
)
def test_invalid_simple_graph_data_is_rejected(vertices, edges, message):
    with pytest.raises(ValueError, match=message):
        SimpleUndirectedGraph(vertices, edges)


def test_unknown_vertex_and_missing_edge_are_rejected():
    graph = triangle_with_tail_graph()
    with pytest.raises(ValueError, match="unknown vertex"):
        graph.neighbors(8)
    with pytest.raises(ValueError, match="not present"):
        graph.without_edge((1, 4))


def test_engine_has_no_renderer_dependency():
    module = inspect.getmodule(SimpleUndirectedGraph)
    source = inspect.getsource(module)
    assert "from manim" not in source
    assert "import manim" not in source
