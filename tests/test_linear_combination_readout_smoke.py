from __future__ import annotations

import numpy as np
import pytest

pytest.importorskip("manim")

from manim import DecimalNumber, Scene, VGroup

from engine.manim_linear_combination_geometry import (
    ManimLinearCombinationGeometry,
)
from engine.manim_linear_combination_readout import (
    ManimLinearCombinationReadout,
)
from scenes.linear_combination_readout_smoke import (
    LinearCombinationReadoutSmoke,
    SMOKE_END_COEFFICIENTS,
    SMOKE_START_COEFFICIENTS,
    SMOKE_VECTORS,
    build_linear_combination_readout_smoke_pipeline,
    update_linear_combination_mobjects,
)


def entry_values(entries: tuple[DecimalNumber, ...]) -> np.ndarray:
    return np.array([entry.get_value() for entry in entries], dtype=float)


def test_smoke_scene_is_a_manim_scene() -> None:
    assert issubclass(LinearCombinationReadoutSmoke, Scene)


def test_smoke_inputs_are_finite_and_structurally_compatible() -> None:
    assert SMOKE_VECTORS.shape == (2, 2)
    assert SMOKE_START_COEFFICIENTS.shape == (2,)
    assert SMOKE_END_COEFFICIENTS.shape == (2,)
    assert np.all(np.isfinite(SMOKE_VECTORS))
    assert np.all(np.isfinite(SMOKE_START_COEFFICIENTS))
    assert np.all(np.isfinite(SMOKE_END_COEFFICIENTS))


def test_pipeline_shares_exact_upstream_components() -> None:
    pipeline = build_linear_combination_readout_smoke_pipeline()

    assert pipeline.coefficient_path.linear_combination is pipeline.combination
    assert pipeline.geometry_path.coefficient_sweep_path is pipeline.coefficient_path
    assert pipeline.geometry_path.geometry is pipeline.geometry
    assert pipeline.display_path.path is pipeline.geometry_path
    assert pipeline.display_path.projector is pipeline.projector


def test_readout_and_arrows_can_start_from_one_exact_display_snapshot() -> None:
    pipeline = build_linear_combination_readout_smoke_pipeline()
    display_snapshot = pipeline.display_path.snapshot(0.0)

    arrows = ManimLinearCombinationGeometry(display_snapshot)
    readout = ManimLinearCombinationReadout(
        display_snapshot.linear_combination_snapshot
    )

    assert readout.snapshot is display_snapshot.linear_combination_snapshot
    assert arrows.term_count == pipeline.combination.vector_count
    np.testing.assert_allclose(
        entry_values(readout.coefficient_entries),
        SMOKE_START_COEFFICIENTS,
    )
    np.testing.assert_allclose(
        entry_values(readout.result_entries),
        display_snapshot.display_resultant_end,
    )


def test_shared_update_keeps_readout_result_synchronized_with_arrow_tip() -> None:
    pipeline = build_linear_combination_readout_smoke_pipeline()
    initial_snapshot = pipeline.display_path.snapshot(0.0)
    arrows = ManimLinearCombinationGeometry(initial_snapshot)
    readout = ManimLinearCombinationReadout(
        initial_snapshot.linear_combination_snapshot
    )
    group = VGroup(arrows, readout)

    returned = update_linear_combination_mobjects(
        group,
        arrows,
        readout,
        pipeline.display_path,
        1.0,
    )
    final_snapshot = pipeline.display_path.snapshot(1.0)

    assert returned is group
    np.testing.assert_allclose(
        entry_values(readout.coefficient_entries),
        SMOKE_END_COEFFICIENTS,
    )
    np.testing.assert_allclose(
        entry_values(readout.result_entries),
        final_snapshot.linear_combination_snapshot.result,
    )
    np.testing.assert_allclose(
        arrows.resultant_arrow.get_end(),
        [*final_snapshot.display_resultant_end, 0.0],
    )
    np.testing.assert_allclose(
        entry_values(readout.result_entries),
        arrows.resultant_arrow.get_end()[:2],
    )


def test_shared_update_preserves_all_mobject_identities() -> None:
    pipeline = build_linear_combination_readout_smoke_pipeline()
    initial_snapshot = pipeline.display_path.snapshot(0.0)
    arrows = ManimLinearCombinationGeometry(initial_snapshot)
    readout = ManimLinearCombinationReadout(
        initial_snapshot.linear_combination_snapshot
    )
    group = VGroup(arrows, readout)

    identities = {
        "group": id(group),
        "arrows": id(arrows),
        "terms": tuple(id(arrow) for arrow in arrows.term_arrows),
        "resultant": id(arrows.resultant_arrow),
        "readout": id(readout),
        "coefficient_label": id(readout.coefficient_label_mobject),
        "result_label": id(readout.result_label_mobject),
        "coefficient_matrix": id(readout.coefficient_matrix),
        "result_matrix": id(readout.result_matrix),
        "coefficient_entries": tuple(
            id(entry) for entry in readout.coefficient_entries
        ),
        "result_entries": tuple(id(entry) for entry in readout.result_entries),
    }

    update_linear_combination_mobjects(
        group,
        arrows,
        readout,
        pipeline.display_path,
        0.625,
    )

    assert id(group) == identities["group"]
    assert id(arrows) == identities["arrows"]
    assert tuple(id(arrow) for arrow in arrows.term_arrows) == identities["terms"]
    assert id(arrows.resultant_arrow) == identities["resultant"]
    assert id(readout) == identities["readout"]
    assert id(readout.coefficient_label_mobject) == identities["coefficient_label"]
    assert id(readout.result_label_mobject) == identities["result_label"]
    assert id(readout.coefficient_matrix) == identities["coefficient_matrix"]
    assert id(readout.result_matrix) == identities["result_matrix"]
    assert tuple(id(entry) for entry in readout.coefficient_entries) == identities[
        "coefficient_entries"
    ]
    assert tuple(id(entry) for entry in readout.result_entries) == identities[
        "result_entries"
    ]


def test_shared_update_queries_display_path_exactly_once() -> None:
    mathematical_snapshot = object()

    class DisplaySnapshot:
        linear_combination_snapshot = mathematical_snapshot

    display_snapshot = DisplaySnapshot()

    class DisplayPathSpy:
        def __init__(self) -> None:
            self.received_progress: list[float] = []

        def snapshot(self, progress: float) -> DisplaySnapshot:
            self.received_progress.append(progress)
            return display_snapshot

    class AdapterSpy:
        def __init__(self) -> None:
            self.received_snapshot: object | None = None

        def update_from_snapshot(self, snapshot: object) -> AdapterSpy:
            self.received_snapshot = snapshot
            return self

    group = VGroup()
    arrows = AdapterSpy()
    readout = AdapterSpy()
    display_path = DisplayPathSpy()

    returned = update_linear_combination_mobjects(
        group,
        arrows,  # type: ignore[arg-type]
        readout,  # type: ignore[arg-type]
        display_path,  # type: ignore[arg-type]
        0.375,
    )

    assert returned is group
    assert display_path.received_progress == [pytest.approx(0.375)]
    assert arrows.received_snapshot is display_snapshot
    assert readout.received_snapshot is mathematical_snapshot


def test_shared_update_uses_same_intermediate_mathematical_state() -> None:
    pipeline = build_linear_combination_readout_smoke_pipeline()
    initial_snapshot = pipeline.display_path.snapshot(0.0)
    arrows = ManimLinearCombinationGeometry(initial_snapshot)
    readout = ManimLinearCombinationReadout(
        initial_snapshot.linear_combination_snapshot
    )
    group = VGroup(arrows, readout)

    progress = 0.4
    update_linear_combination_mobjects(
        group,
        arrows,
        readout,
        pipeline.display_path,
        progress,
    )
    expected = pipeline.display_path.snapshot(progress)

    np.testing.assert_allclose(
        entry_values(readout.coefficient_entries),
        expected.linear_combination_snapshot.coefficients,
    )
    np.testing.assert_allclose(
        entry_values(readout.result_entries),
        expected.linear_combination_snapshot.result,
    )
    np.testing.assert_allclose(
        arrows.resultant_arrow.get_end(),
        [*expected.display_resultant_end, 0.0],
    )
