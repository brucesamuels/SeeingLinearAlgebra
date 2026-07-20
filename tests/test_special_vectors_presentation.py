from __future__ import annotations

import inspect

from scenes.special_vectors_presentation import SpecialVectorsPresentation


def test_scene_reuses_renderer_independent_snapshot() -> None:
    source = inspect.getsource(SpecialVectorsPresentation)

    assert "SNAPSHOT: SpecialVectorSnapshot = SPECIAL_VECTORS_SNAPSHOT" in source
    assert "self.SNAPSHOT.source" in source
    assert "self.SNAPSHOT.unit" in source


def test_scene_uses_shared_visual_identity() -> None:
    source = inspect.getsource(SpecialVectorsPresentation)

    assert "ThemedText.lesson_title" in source
    assert "LessonLayout()" in source
    assert "SEEING_LINEAR_ALGEBRA_THEME" in source


def test_scene_introduces_zero_vector_and_normalization() -> None:
    source = inspect.getsource(SpecialVectorsPresentation.construct)

    assert r"\mathbf 0=\begin{bmatrix}0\\0\end{bmatrix}" in source
    assert r"\widehat{\mathbf v}=\frac{\mathbf v}{\|\mathbf v\|}" in source
    assert r"\|\widehat{\mathbf v}\|=1" in source


def test_scene_uses_unit_circle_as_geometric_confirmation() -> None:
    source = inspect.getsource(SpecialVectorsPresentation.construct)

    assert "unit_circle = Circle(" in source
    assert "TracedPath(" in source
    assert "angle=TAU" in source
    assert "Every point on this circle is a unit vector." in source


def test_scene_remains_independently_renderable() -> None:
    assert issubclass(SpecialVectorsPresentation, __import__("manim").Scene)



def test_scene_positions_vector_labels_clear_of_the_arrow() -> None:
    source = inspect.getsource(SpecialVectorsPresentation.construct)

    assert "source_label.next_to(source_arrow.get_end(), UP, buff=0.32)" in source
    assert "restored_label.next_to(restored_arrow.get_end(), UP, buff=0.32)" in source
    assert "source_label.shift(RIGHT * 0.22)" in source
    assert "restored_label.shift(RIGHT * 0.22)" in source


def test_magnitude_heading_is_replaced_before_the_next_prompt() -> None:
    source = inspect.getsource(SpecialVectorsPresentation.construct)

    assert '"Computing the Magnitude"' in source
    assert "ReplacementTransform(magnitude_heading, question)" in source
    assert "FadeIn(question)" not in source
