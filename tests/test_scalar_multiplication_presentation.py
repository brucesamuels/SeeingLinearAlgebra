import inspect

from scenes.scalar_multiplication_presentation import ScalarMultiplicationPresentation


def test_scene_reuses_renderer_independent_stages() -> None:
    source = inspect.getsource(ScalarMultiplicationPresentation)
    assert "LESSON_STAGES = SCALAR_MULTIPLICATION_STAGES" in source
    assert "for stage in self.LESSON_STAGES" in source
    assert "scaled_vector(stage.scalar)" in source


def test_scene_uses_shared_visual_identity() -> None:
    source = inspect.getsource(ScalarMultiplicationPresentation)
    assert "ThemedText.lesson_title" in source
    assert "LessonLayout()" in source
    assert "SEEING_LINEAR_ALGEBRA_THEME" in source


def test_scene_prepares_vector_subtraction() -> None:
    source = inspect.getsource(ScalarMultiplicationPresentation.construct)
    assert r"(-1)\mathbf{v}=-\mathbf{v}" in source
    assert "stage.scalar < 0" in source
