from engine.determinant_geometry import (
    area_example_det, area_example_matrix, closing_lines, orientation_determinants,
    singular_det, theorem_tex, signed_scale_tex, volume_scale, product_scaling_tex,
)


def test_core_geometry_statements() -> None:
    assert theorem_tex() == r"|\det(A)|=\text{area/volume scale factor}"
    assert signed_scale_tex() == r"\det(A)=\text{signed volume scale factor}"


def test_area_example_is_consistent() -> None:
    assert area_example_matrix() == ((2, 1), (0, 1))
    assert area_example_det() == 2


def test_orientation_and_singular_cases() -> None:
    assert orientation_determinants() == (1, -1)
    assert singular_det() == 0


def test_volume_and_product_scaling_content() -> None:
    assert volume_scale() == 3
    lines = product_scaling_tex()
    assert "det(B)" in lines[0]
    assert "det(A)" in lines[1]
    assert "det(AB)" in lines[2]


def test_closing_lines_cover_magnitude_sign_and_collapse() -> None:
    lines = closing_lines()
    assert "Magnitude" in lines[0]
    assert "Sign" in lines[1]
    assert "zero determinant" in lines[2]
