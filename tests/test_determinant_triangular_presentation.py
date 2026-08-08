from pathlib import Path

SCENE = Path("scenes/determinant_triangular_presentation.py")


def source() -> str:
    return SCENE.read_text(encoding="utf-8")


def test_scene_class_exists() -> None:
    assert "class DeterminantTriangularPresentation(Scene):" in source()


def test_scene_shows_upper_triangular_shortcut() -> None:
    text = source()
    assert "A triangular matrix gives us a shortcut" in text
    assert "upper_triangular_example()" in text
    assert "diagonal_product_tex()" in text
    assert "Everything below the diagonal is zero." in text


def test_scene_explains_diagonal_product_by_cofactor_expansion() -> None:
    text = source()
    assert "Why does the diagonal product work?" in text
    assert r"\det(T)=a\begin{vmatrix}d&e\\0&f\end{vmatrix}" in text
    assert r"=a(df)=adf" in text
    assert "triangular_explanation_lines()" in text


def test_scene_includes_lower_triangular_case() -> None:
    text = source()
    assert "The same rule holds below the diagonal" in text
    assert "lower_triangular_example()" in text
    assert "triangular_rule_tex()" in text


def test_scene_includes_block_triangular_extension() -> None:
    text = source()
    assert "The idea extends to blocks" in text
    assert "block_triangular_symbolic_tex()" in text
    assert "block_triangular_rule_tex()" in text
    assert "block_example_factorization_tex()" in text


def test_scene_ends_with_strategy() -> None:
    text = source()
    assert "Recognize structure before you compute" in text
    assert "strategy_lines()" in text
    assert "turn a long determinant computation into a glance" in text


def test_scene_uses_safe_clear_stage() -> None:
    text = source()
    assert "*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve]" in text
