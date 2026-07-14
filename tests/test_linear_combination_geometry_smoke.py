from __future__ import annotations

import numpy as np
import pytest

pytest.importorskip("manim")

from manim import Scene

from engine.manim_linear_combination_geometry import (
    ManimLinearCombinationGeometry,
)
from scenes.linear_combination_geometry_smoke import (
    LinearCombinationGeometrySmoke,
    SMOKE_END_COEFFICIENTS,
    SMOKE_START_COEFFICIENTS,
    SMOKE_VECTORS,
    build_linear_combination_smoke_pipeline,
    update_linear_combination_mobject,
)


def test_smoke_scene_is_a_manim_scene() -> None:
    assert issubclass(LinearCombinationGeometrySmoke, Scene)


def test_smoke_inputs_have_consistent_two_term_shapes() -> None:
    assert SMOKE_VECTORS.shape == (2, 2)
    assert SMOKE_START_COEFFICIENTS.shape == (2,)
    assert SMOKE_END_COEFFICIENTS.shape == (2,)
    assert np.all(np.isfinite(SMOKE_VECTORS))
    assert np.all(np.isfinite(SMOKE_START_COEFFICIENTS))
    assert np.all(np.isfinite(SMOKE_END_COEFFICIENTS))


def test_pipeline_produces_display_snapshots_consumable_by_manim_adapter() -> None:
    pipeline = build_linear_combination_smoke_pipeline()

    initial_snapshot = pipeline.display_path.snapshot(0.0)
    final_snapshot = pipeline.display_path.snapshot(1.0)
    adapter = ManimLinearCombinationGeometry(initial_snapshot)

    adapter.update_from_snapshot(final_snapshot)

    assert adapter.term_count == 2
    np.testing.assert_allclose(
        adapter.term_arrows[0].get_start(),
        (0.0, 0.0, 0.0),
    )
    np.testing.assert_allclose(
        adapter.term_arrows[0].get_end(),
        (2.5, 1.25, 0.0),
    )
    np.testing.assert_allclose(
        adapter.term_arrows[1].get_start(),
        (2.5, 1.25, 0.0),
    )
    np.testing.assert_allclose(
        adapter.term_arrows[1].get_end(),
        (3.25, -0.25, 0.0),
    )
    np.testing.assert_allclose(
        adapter.resultant_arrow.get_start(),
        (0.0, 0.0, 0.0),
    )
    np.testing.assert_allclose(
        adapter.resultant_arrow.get_end(),
        (3.25, -0.25, 0.0),
    )


def test_scene_update_helper_preserves_all_mobject_identities() -> None:
    pipeline = build_linear_combination_smoke_pipeline()
    adapter = ManimLinearCombinationGeometry(pipeline.display_path.snapshot(0.0))
    root_id = id(adapter)
    term_ids = tuple(id(arrow) for arrow in adapter.term_arrows)
    resultant_id = id(adapter.resultant_arrow)

    returned = update_linear_combination_mobject(
        adapter,
        pipeline.display_path,
        1.0,
    )

    assert returned is adapter
    assert id(adapter) == root_id
    assert tuple(id(arrow) for arrow in adapter.term_arrows) == term_ids
    assert id(adapter.resultant_arrow) == resultant_id


def test_scene_update_helper_requests_exact_progress_value() -> None:
    sentinel_snapshot = object()

    class DisplayPathSpy:
        def __init__(self) -> None:
            self.received_progress: float | None = None

        def snapshot(self, progress: float) -> object:
            self.received_progress = progress
            return sentinel_snapshot

    class MobjectSpy:
        def __init__(self) -> None:
            self.received_snapshot: object | None = None

        def update_from_snapshot(self, snapshot: object) -> MobjectSpy:
            self.received_snapshot = snapshot
            return self

    display_path = DisplayPathSpy()
    mobject = MobjectSpy()

    returned = update_linear_combination_mobject(  # type: ignore[arg-type]
        mobject,
        display_path,  # type: ignore[arg-type]
        0.375,
    )

    assert returned is mobject
    assert display_path.received_progress == pytest.approx(0.375)
    assert mobject.received_snapshot is sentinel_snapshot
