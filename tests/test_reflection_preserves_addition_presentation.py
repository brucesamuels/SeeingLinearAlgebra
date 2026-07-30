import inspect

from scenes.reflection_preserves_addition_presentation import (
    ReflectionPreservesAdditionPresentation,
)


def test_scene_uses_retained_result_sequence():
    source = inspect.getsource(ReflectionPreservesAdditionPresentation)

    assert "_reflect_and_retain_sum" in source
    assert "_erase_everything_except_result" in source
    assert "_redraw_and_reflect_components" in source
    assert "_show_sum_of_reflections" in source


def test_reflected_sum_is_retained_when_original_vectors_clear():
    source = inspect.getsource(
        ReflectionPreservesAdditionPresentation._erase_everything_except_result
    )

    assert "FadeOut(original_group)" in source
    assert "FadeOut(retained_result[0])" in source
    assert "FadeOut(retained_result[1])" not in source
    assert "FadeOut(retained_result[2])" not in source


def test_u_and_v_are_redrawn_and_reflected_separately():
    source = inspect.getsource(
        ReflectionPreservesAdditionPresentation._redraw_and_reflect_components
    )

    assert r"\mathbf{u}" in source
    assert r"r_m(\mathbf{u})" in source
    assert r"\mathbf{v}" in source
    assert r"r_m(\mathbf{v})" in source
    assert "TransformFromCopy(u_arrow, reflected_u)" in source
    assert "TransformFromCopy(v_arrow, reflected_v_origin)" in source


def test_sum_of_reflections_is_shown():
    source = inspect.getsource(
        ReflectionPreservesAdditionPresentation._show_sum_of_reflections
    )

    assert r"r_m(\mathbf{u})+r_m(\mathbf{v})" in source
    assert "GrowArrow(sum_of_reflections)" in source
    assert "coincides with the retained reflected sum" in source


def test_scene_states_additivity():
    source = inspect.getsource(ReflectionPreservesAdditionPresentation)

    assert r"r_m(\mathbf{u}+\mathbf{v})" in source
    assert r"r_m(\mathbf{u})+r_m(\mathbf{v})" in source
    assert "This is additivity" in source
