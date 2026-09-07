import inspect

import numpy as np
import pytest

from engine.graph_laplacian_spectrum import GraphLaplacianSpectrum
from engine.simple_undirected_graph import SimpleUndirectedGraph, triangle_with_tail_graph
from engine.spectral_graph_partition import SpectralGraphPartition


def test_default_fiedler_vector_has_exact_recurring_direction():
    model = SpectralGraphPartition()
    expected = np.array([1, 1, 0, -2], dtype=float) / np.sqrt(6)
    assert model.vertex_order == (1, 2, 3, 4)
    assert model.fiedler_vector() == pytest.approx(expected, abs=1e-12)


def test_zero_threshold_gives_triangle_and_tail_partition():
    model = SpectralGraphPartition()
    assert model.sign_partition() == ((1, 2, 3), (4,))
    assert model.threshold_partition([1, 1, 0, -2]) == ((1, 2, 3), (4,))
    assert model.threshold_partition([1, 1, 0, -2], equal_to_upper=False) == ((1, 2), (3, 4))


def test_sign_flip_only_swaps_the_two_groups_when_zero_is_assigned_consistently():
    model = SpectralGraphPartition()
    positive, negative = model.threshold_partition([1, 1, 0.1, -2])
    flipped_positive, flipped_negative = model.threshold_partition([-1, -1, -0.1, 2])
    assert (positive, negative) == (flipped_negative, flipped_positive)


def test_fiedler_cut_crosses_only_the_bridge():
    model = SpectralGraphPartition()
    assert model.cut_edges((1, 2, 3)) == ((3, 4),)
    assert model.cut_size((1, 2, 3)) == 1
    assert model.cut_edges((4,)) == ((3, 4),)


def test_alternative_two_two_cut_crosses_two_edges():
    model = SpectralGraphPartition()
    assert model.cut_edges((1, 2)) == ((2, 3), (1, 3))
    assert model.cut_size((1, 2)) == 2


def test_ratio_cut_scores_include_group_sizes():
    model = SpectralGraphPartition()
    assert model.ratio_cut_score((1, 2, 3)) == pytest.approx(4 / 3)
    assert model.ratio_cut_score((1, 2)) == pytest.approx(2)
    assert model.ratio_cut_score((1,)) == pytest.approx(8 / 3)


def test_balanced_partition_signal_is_mean_zero():
    model = SpectralGraphPartition()
    signal = model.balanced_partition_signal((1, 2, 3))
    assert signal == pytest.approx([1 / 3, 1 / 3, 1 / 3, -1])
    assert signal.sum() == pytest.approx(0)


@pytest.mark.parametrize("first_side", ((1, 2, 3), (1, 2), (1,), (3, 4)))
def test_partition_signal_rayleigh_quotient_equals_ratio_cut(first_side):
    model = SpectralGraphPartition()
    assert model.partition_rayleigh_quotient(first_side) == pytest.approx(
        model.ratio_cut_score(first_side)
    )


def test_sweep_partitions_follow_ordered_fiedler_coordinates():
    model = SpectralGraphPartition()
    assert model.sweep_partitions() == (
        ((4,), (1, 2, 3)),
        ((3, 4), (1, 2)),
    )
    assert model.sweep_scores() == pytest.approx((4 / 3, 2))


def test_best_sweep_cut_recovers_bridge_partition():
    model = SpectralGraphPartition()
    assert model.best_sweep_partition() == ((4,), (1, 2, 3))


@pytest.mark.parametrize(
    "side",
    ((), (1, 2, 3, 4), (1, 1), (1, 5), ([1],)),
)
def test_invalid_partitions_are_rejected(side):
    model = SpectralGraphPartition()
    with pytest.raises(ValueError, match="partition"):
        model.cut_edges(side)


@pytest.mark.parametrize("values", ((1, 2, 3), (1, 2, 3, 4, 5), (1, np.nan, 3, 4)))
def test_invalid_threshold_values_are_rejected(values):
    with pytest.raises(ValueError, match="values"):
        SpectralGraphPartition().threshold_partition(values)


def test_invalid_threshold_is_rejected():
    with pytest.raises(ValueError, match="threshold"):
        SpectralGraphPartition().threshold_partition([1, 1, 0, -2], np.inf)


def test_invalid_spectrum_is_rejected():
    with pytest.raises(ValueError, match="GraphLaplacianSpectrum"):
        SpectralGraphPartition(spectrum=object())


def test_disconnected_graph_is_rejected_because_second_mode_is_not_unique():
    graph = triangle_with_tail_graph().without_edge((3, 4))
    with pytest.raises(ValueError, match="connected graph"):
        SpectralGraphPartition(GraphLaplacianSpectrum(graph))


def test_one_vertex_graph_is_rejected():
    graph = SimpleUndirectedGraph((1,), ())
    with pytest.raises(ValueError, match="at least two"):
        SpectralGraphPartition(GraphLaplacianSpectrum(graph))


def test_engine_composes_spectrum_model_and_has_no_renderer_dependency():
    module = inspect.getmodule(SpectralGraphPartition)
    source = inspect.getsource(module)
    assert "from engine.graph_laplacian_spectrum import GraphLaplacianSpectrum" in source
    assert "from manim" not in source
    assert "import manim" not in source
