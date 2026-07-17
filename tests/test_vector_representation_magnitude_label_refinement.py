from __future__ import annotations

import inspect

from scenes.vector_representation_presentation import (
    VectorRepresentationPresentation,
)


def test_scene_names_pythagorean_distance_formula() -> None:
    source = inspect.getsource(
        VectorRepresentationPresentation.construct
    )

    assert "Use the Pythagorean distance formula" in source


def test_scene_computes_magnitude_in_successive_forms() -> None:
    source = inspect.getsource(
        VectorRepresentationPresentation.construct
    )

    assert r"\|\mathbf{v}\|=\sqrt{3^2+2^2}" in source
    assert r"\|\mathbf{v}\|=\sqrt{13}" in source
    assert r"\|\mathbf{v}\|\approx 3.6" in source
    assert "magnitude_formula," in source
    assert "magnitude_exact," in source
    assert "magnitude_decimal," in source
    assert source.count("ReplacementTransform(") >= 3


def test_final_magnitude_label_matches_shared_typography() -> None:
    source = inspect.getsource(
        VectorRepresentationPresentation.construct
    )

    assert "ThemedText.body(" in source
    assert "display_snapshot.magnitude_text" in source
    assert "theme=self.THEME" in source
    assert "display.style.vertical_gap" in source
    assert "aligned_edge=[-1.0, 0.0, 0.0]" in source


def test_computation_transforms_into_final_magnitude_label() -> None:
    source = inspect.getsource(
        VectorRepresentationPresentation.construct
    )

    decimal_position = source.index("magnitude_decimal,")
    label_position = source.index("magnitude_label,", decimal_position)

    assert decimal_position < label_position
    assert "ReplacementTransform(" in source[
        source.rfind("ReplacementTransform(", 0, decimal_position):
        label_position
    ]
