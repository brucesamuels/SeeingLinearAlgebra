from engine.determinant_jacobian_preview import (
    closing_lines,
    jacobian_matrix_tex,
    linear_area_tex,
    linear_example_tex,
    local_area_tex,
    polar_area_tex,
    polar_jacobian_tex,
)


def test_linear_area_formula_uses_absolute_determinant() -> None:
    assert r"|\det(A)|" in linear_area_tex()


def test_jacobian_matrix_contains_partial_derivatives() -> None:
    text = jacobian_matrix_tex()
    assert r"\frac{\partial x}{\partial u}" in text
    assert r"\frac{\partial y}{\partial v}" in text


def test_local_area_formula_uses_jacobian_determinant() -> None:
    text = local_area_tex()
    assert r"|\det J_F(u,v)|" in text
    assert r"dA_{uv}" in text


def test_linear_example_has_constant_jacobian_and_scale_six() -> None:
    lines = linear_example_tex()
    assert r"F(u,v)=(2u,\,u+3v)" == lines[0]
    assert r"\begin{bmatrix}2&0\\1&3\end{bmatrix}" in lines[1]
    assert lines[2] == r"\det(J_F)=6"


def test_polar_jacobian_has_determinant_r() -> None:
    lines = polar_jacobian_tex()
    assert r"x=r\cos\theta" in lines[0]
    assert r"\det(J)=r" == lines[2]
    assert polar_area_tex() == r"dA=r\,dr\,d\theta"


def test_closing_lines_connect_linear_and_nonlinear_scaling() -> None:
    lines = closing_lines()
    assert "linear map" in lines[0]
    assert "Jacobian determinant" in lines[1]
    assert "geometric measure" in lines[2]
