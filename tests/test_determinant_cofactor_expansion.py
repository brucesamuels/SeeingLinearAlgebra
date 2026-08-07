from engine.determinant_cofactor_expansion import (
    bridge_lines,
    checkerboard_signs,
    cofactor_definition_tex,
    first_row_cofactor_tex,
    general_column_expansion_tex,
    general_row_expansion_tex,
    grouped_by_first_row_tex,
    minor_definition_tex,
    sign_origin_tex,
    row_one_expansion_tex,
    row_one_minor_determinants_tex,
    six_term_formula_lines,
)


def test_six_term_formula_keeps_all_terms() -> None:
    line1, line2 = six_term_formula_lines()
    assert r"a_{11}a_{22}a_{33}" in line1
    assert r"a_{12}a_{23}a_{31}" in line1
    assert r"a_{13}a_{21}a_{32}" in line1
    assert r"-a_{11}a_{23}a_{32}" in line2
    assert r"-a_{12}a_{21}a_{33}" in line2
    assert r"-a_{13}a_{22}a_{31}" in line2


def test_grouping_by_first_row_is_algebraically_correct() -> None:
    tex = grouped_by_first_row_tex()
    assert r"a_{11}(a_{22}a_{33}-a_{23}a_{32})" in tex
    assert r"-a_{12}(a_{21}a_{33}-a_{23}a_{31})" in tex
    assert r"+a_{13}(a_{21}a_{32}-a_{22}a_{31})" in tex


def test_first_row_minor_determinants_are_correct() -> None:
    m11, m12, m13 = row_one_minor_determinants_tex()
    assert r"a_{22}&a_{23}" in m11 and r"a_{32}&a_{33}" in m11
    assert r"a_{21}&a_{23}" in m12 and r"a_{31}&a_{33}" in m12
    assert r"a_{21}&a_{22}" in m13 and r"a_{31}&a_{32}" in m13


def test_row_one_expansion_has_alternating_signs() -> None:
    tex = row_one_expansion_tex()
    assert tex.startswith(r"\det(A)=a_{11}")
    assert r"-a_{12}" in tex
    assert r"+a_{13}" in tex


def test_checkerboard_sign_pattern() -> None:
    assert checkerboard_signs() == (
        ("+", "-", "+"),
        ("-", "+", "-"),
        ("+", "-", "+"),
    )


def test_cofactor_definition_and_general_expansions() -> None:
    assert cofactor_definition_tex() == r"C_{ij}=(-1)^{i+j}M_{ij}"
    assert first_row_cofactor_tex() == r"\det(A)=a_{11}C_{11}+a_{12}C_{12}+a_{13}C_{13}"
    assert general_row_expansion_tex() == r"\det(A)=\sum_{j=1}^{n}a_{ij}C_{ij}"
    assert general_column_expansion_tex() == r"\det(A)=\sum_{i=1}^{n}a_{ij}C_{ij}"


def test_bridge_lines_no_longer_reference_cp136() -> None:
    lines = bridge_lines()
    assert lines[0] == "Begin with the six-term determinant formula."
    assert all("CP136" not in line for line in lines)


def test_minor_and_sign_origin_definitions() -> None:
    assert r"Minor " in minor_definition_tex()
    assert r"delete row }i" in minor_definition_tex()
    assert r"then take the determinant" in minor_definition_tex()
    assert r"(-1)^{i+j}" in sign_origin_tex()
    assert "permutation signs" in sign_origin_tex()
    assert r"Negative signs come from " in sign_origin_tex()
