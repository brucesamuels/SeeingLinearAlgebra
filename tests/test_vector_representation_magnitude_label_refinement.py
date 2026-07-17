from __future__ import annotations

import inspect

from scenes.vector_representation_presentation import (
    VectorRepresentationPresentation,
)


def test_scene_names_pythagorean_distance_formula() -> None:
    source = inspect.getsource(VectorRepresentationPresentation.construct)

    assert "Use the Pythagorean distance formula" in source


def test_scene_computes_magnitude_in_successive_forms() -> None:
    source = inspect.getsource(VectorRepresentationPresentation.construct)

    assert r"\|\mathbf{v}\|=\sqrt{3^2+2^2}" in source
    assert r"\|\mathbf{v}\|=\sqrt{13}" in source
    assert r"\|\mathbf{v}\|\approx 3.6" in source
    assert "ReplacementTransform(magnitude_formula, magnitude_exact)" in source
    assert "ReplacementTransform(magnitude_exact, magnitude_decimal)" in source


def test_final_magnitude_label_matches_dimension_label_typography() -> None:
    source = inspect.getsource(VectorRepresentationPresentation.construct)

    assert "Text(display_snapshot.magnitude_text)" in source
    assert "display.style.label_scale" in source
    assert "display.style.vertical_gap" in source
    assert "aligned_edge=LEFT" in source


def test_computation_transforms_into_final_magnitude_label() -> None:
    source = inspect.getsource(VectorRepresentationPresentation.construct)

    assert (
        "ReplacementTransform(magnitude_decimal, magnitude_label)"
        in source
    )
