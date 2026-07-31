import inspect

from scenes.cross_product_computation_presentation import (
    CrossProductComputationPresentation,
)


def test_construct_removes_subtitle_before_cofactor_section() -> None:
    source = inspect.getsource(CrossProductComputationPresentation.construct)

    assert "We know what it represents. Now let us calculate it." in source
    assert "FadeOut(subtitle)" in source
    assert "remove_fixed_in_frame_mobjects(subtitle)" in source
    assert "self.remove(subtitle)" in source
    assert source.index("FadeOut(subtitle)") < source.index("self._show_cross_hatch_shortcut(s)")


def test_manual_grid_helper_builds_aligned_rows() -> None:
    source = inspect.getsource(CrossProductComputationPresentation._manual_grid)

    assert "MathTex(value, font_size=38)" in source
    assert "return grid, entry_rows" in source


def test_cofactor_section_uses_manual_layout_and_lowered_heading() -> None:
    source = inspect.getsource(
        CrossProductComputationPresentation._show_cofactor_derivation
    )

    assert "Where Do the Cofactors Come From?" in source
    assert ".to_edge(UP).shift(DOWN * 0.65)" in source
    assert "left_bar = Line(" in source
    assert "right_bar = Line(" in source
    assert "Matrix(" not in source
    assert "TransformFromCopy(surviving_group,minor_grid)" in source


def test_cofactor_section_shows_expected_signed_results() -> None:
    source = inspect.getsource(
        CrossProductComputationPresentation._show_cofactor_derivation
    )

    assert r"(1)(2)-(3)(4)=-10" in source
    assert r"-\big((2)(2)-(3)(1)\big)=-1" in source
    assert r"(2)(4)-(1)(1)=7" in source
    assert r"-10\mathbf{i}" in source
    assert r"-\mathbf{j}" in source
    assert r"7\mathbf{k}" in source


def test_symbolic_vector_form_is_lowered_below_cofactor_expansion() -> None:
    source = inspect.getsource(
        CrossProductComputationPresentation._show_cofactor_derivation
    )

    assert r"-10\mathbf{i}-\mathbf{j}+7\mathbf{k}" in source
    assert ".shift(DOWN*1.00)" in source
    assert ".shift(DOWN*0.30)" not in source


def test_cross_hatch_section_uses_manual_layout_and_lowered_heading() -> None:
    source = inspect.getsource(
        CrossProductComputationPresentation._show_cross_hatch_computation
    )

    assert "The Cross-Hatch Shortcut" in source
    assert ".to_edge(UP).shift(DOWN*1.05)" in source
    assert "shortcut,entry_rows=self._manual_grid(" in source
    assert "Matrix(" not in source
    assert "return entry_rows[r][c].get_center()" in source


def test_cross_hatch_pairs_and_subtractions_are_correct() -> None:
    source = inspect.getsource(
        CrossProductComputationPresentation._show_cross_hatch_computation
    )

    for pair in [
        "(1,1,2,2)",
        "(1,2,2,1)",
        "(1,2,2,3)",
        "(1,3,2,2)",
        "(1,3,2,4)",
        "(1,4,2,3)",
    ]:
        assert pair in source

    assert r"2-12=-10" in source
    assert r"3-4=-1" in source
    assert r"8-1=7" in source


def test_vector_and_coordinate_forms_are_sequential() -> None:
    source = inspect.getsource(
        CrossProductComputationPresentation._show_cross_hatch_computation
    )

    assert "FadeOut(vf)" in source
    assert "self.remove(vf,vh)" in source
    assert "self.wait(0.25)" in source
    assert "FadeIn(ch),FadeIn(cf)" in source
