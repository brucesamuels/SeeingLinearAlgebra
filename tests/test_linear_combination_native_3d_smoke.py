from __future__ import annotations

import numpy as np
import pytest

pytest.importorskip("manim")

from scenes.linear_combination_native_3d_smoke import (
    SMOKE_COEFFICIENTS,
    SMOKE_VECTORS,
    VECTOR_DRAW_RUN_TIME,
    LinearCombinationNative3DSmoke,
    _parallelepiped_edges,
    build_native_3d_full_rank_pipeline,
)


def test_scene_is_native_three_d() -> None:
    from manim import ThreeDScene

    assert issubclass(LinearCombinationNative3DSmoke, ThreeDScene)


def test_vectors_are_full_rank() -> None:
    assert SMOKE_VECTORS.shape == (3, 3)
    assert np.linalg.matrix_rank(SMOKE_VECTORS) == 3
    assert abs(float(np.linalg.det(SMOKE_VECTORS))) > 1.0e-8


def test_pipeline_result_is_sum_of_three_vectors() -> None:
    pipeline = build_native_3d_full_rank_pipeline()
    snapshot = pipeline.final_snapshot

    np.testing.assert_allclose(SMOKE_COEFFICIENTS, np.ones(3))
    np.testing.assert_allclose(
        snapshot.linear_combination_snapshot.result,
        SMOKE_VECTORS.sum(axis=0),
    )


def test_parallelepiped_has_twelve_edges() -> None:
    edges = _parallelepiped_edges(*SMOKE_VECTORS)
    assert len(edges) == 12


def test_scene_uses_common_origin_vectors() -> None:
    from pathlib import Path
    import scenes.linear_combination_native_3d_smoke as smoke_module

    source = Path(smoke_module.__file__).read_text(encoding="utf-8")

    assert "axes_origin = axes.c2p(0.0, 0.0, 0.0)" in source
    assert "vector_points = tuple(" in source
    assert "axes.c2p(*vector)" in source
    assert "axes_origin," in source
    assert "vector_point," in source
    assert "terms =" not in source


def test_vector_draws_are_intentionally_slow() -> None:
    assert VECTOR_DRAW_RUN_TIME >= 2.0


def test_box_is_drawn_after_all_three_vectors() -> None:
    from pathlib import Path
    import scenes.linear_combination_native_3d_smoke as smoke_module

    source = Path(smoke_module.__file__).read_text(encoding="utf-8")

    vector_loop_index = source.index(
        "for vector_point, color in zip("
    )
    box_index = source.index("box = VGroup(")
    result_index = source.index("resultant = _arrow(")

    assert vector_loop_index < box_index < result_index


def test_scene_maps_all_display_geometry_through_axes() -> None:
    from pathlib import Path
    import scenes.linear_combination_native_3d_smoke as smoke_module

    source = Path(smoke_module.__file__).read_text(encoding="utf-8")

    assert "axes_origin = axes.c2p(0.0, 0.0, 0.0)" in source
    assert "axes.c2p(*vector)" in source
    assert "start=axes.c2p(*start)" in source
    assert "end=axes.c2p(*end)" in source
    assert "result_point = axes.c2p(*result)" in source
