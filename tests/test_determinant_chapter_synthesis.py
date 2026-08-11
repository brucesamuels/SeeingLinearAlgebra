from engine.determinant_chapter_synthesis import (
    algebraic_rules,
    closing_words,
    computation_methods,
    geometric_lines,
    invertibility_chain,
    jacobian_bridge,
    singular_chain,
    system_formulas,
)


def test_computation_methods_cover_three_viewpoints() -> None:
    methods = computation_methods()
    assert len(methods) == 3
    assert "Elimination" in methods[0]
    assert "Cofactors" in methods[1]
    assert "Big Formula" in methods[2]


def test_invertibility_chain_contains_core_equivalences() -> None:
    tex = invertibility_chain()
    assert r"\det(A)\ne0" in tex
    assert r"\operatorname{rank}(A)=n" in tex
    assert r"\mathcal N(A)=\{\mathbf 0\}" in tex
    assert r"A^{-1}\text{ exists}" in tex


def test_singular_chain_contains_zero_determinant_case() -> None:
    tex = singular_chain()
    assert r"\det(A)=0" in tex
    assert r"\operatorname{rank}(A)<n" in tex
    assert r"A\text{ is singular}" in tex


def test_geometry_summary_contains_scale_orientation_and_collapse() -> None:
    lines = geometric_lines()
    assert "scale factor" in lines[0]
    assert "orientation" in lines[1]
    assert "collapse" in lines[2]


def test_algebraic_rules_include_product_transpose_inverse() -> None:
    lines = algebraic_rules()
    assert r"\det(AB)=\det(A)\det(B)" == lines[0]
    assert r"\det(A^T)=\det(A)" == lines[1]
    assert r"\det(A^{-1})" in lines[2]


def test_system_formulas_include_cramer_and_adjugate() -> None:
    cramer, inverse = system_formulas()
    assert r"x_k=" in cramer
    assert r"\operatorname{adj}(A)" in inverse


def test_jacobian_bridge_distinguishes_global_and_local() -> None:
    linear, nonlinear = jacobian_bridge()
    assert "global area scale" in linear
    assert "local area scale" in nonlinear


def test_closing_words() -> None:
    assert closing_words() == ("Computation", "Structure", "Geometry")
