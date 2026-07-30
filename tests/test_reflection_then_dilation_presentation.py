import inspect

from scenes.reflection_then_dilation_presentation import (
    ReflectionThenDilationPresentation,
)


def test_scene_has_two_explicit_routes():
    source = inspect.getsource(ReflectionThenDilationPresentation)
    assert "Path A: reflect first, then dilate." in source
    assert "Path B: dilate first, then reflect." in source
    assert r"D_c\!\left(r_m(\mathbf{v})\right)" in source
    assert r"r_m\!\left(D_c(\mathbf{v})\right)" in source


def test_scene_states_homogeneity():
    source = inspect.getsource(ReflectionThenDilationPresentation)
    assert r"r_m(c\mathbf{v})=c\,r_m(\mathbf{v})" in source
    assert "This is homogeneity" in source


def test_final_card_removes_geometry():
    source = inspect.getsource(
        ReflectionThenDilationPresentation._show_homogeneity_statement
    )
    assert "FadeOut(geometric_objects)" in source
