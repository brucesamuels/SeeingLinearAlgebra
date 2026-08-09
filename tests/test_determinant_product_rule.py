from engine.determinant_product_rule import (
    elementary_cases,
    elementary_conclusion_tex,
    factorization_tex,
    invertible_chain_tex,
    inverse_consequence_tex,
    many_factors_tex,
    power_consequence_tex,
    product_factorization_tex,
    singular_case_tex,
    theorem_tex,
)


def test_main_theorem() -> None:
    assert theorem_tex() == r"\det(AB)=\det(A)\det(B)"


def test_elementary_cases_cover_all_three_row_operations() -> None:
    cases = elementary_cases()
    assert len(cases) == 3
    assert cases[0] == (r"R_i\leftrightarrow R_j", r"\det(E)=-1", r"\det(EB)=-\det(B)")
    assert cases[1] == (r"R_i\to cR_i", r"\det(E)=c", r"\det(EB)=c\det(B)")
    assert cases[2] == (r"R_i\to R_i+cR_j", r"\det(E)=1", r"\det(EB)=\det(B)")
    assert elementary_conclusion_tex() == r"\det(EB)=\det(E)\det(B)"


def test_invertible_factorization_and_chain() -> None:
    assert factorization_tex() == r"A=E_mE_{m-1}\cdots E_1"
    assert product_factorization_tex() == r"AB=E_mE_{m-1}\cdots E_1B"
    chain = invertible_chain_tex()
    assert r"\det(E_m)\cdots\det(E_1)\det(B)" in chain[0]
    assert r"\det(A)" in chain[1]
    assert r"\det(AB)=\det(A)\det(B)" in chain[2]


def test_singular_case_uses_rank_argument() -> None:
    lines = singular_case_tex()
    assert r"\det(A)=0" in lines[0]
    assert r"\operatorname{rank}(AB)\leq\operatorname{rank}(A)<n" == lines[1]
    assert r"AB\text{ singular}" in lines[2]
    assert r"\det(AB)=0=\det(A)\det(B)" == lines[3]


def test_consequences() -> None:
    inv = inverse_consequence_tex()
    assert inv[0] == r"AA^{-1}=I"
    assert inv[2] == r"\det(A^{-1})=\frac{1}{\det(A)}"
    assert power_consequence_tex() == r"\det(A^k)=\det(A)^k"
    assert many_factors_tex() == r"\det(A_1A_2\cdots A_m)=\det(A_1)\det(A_2)\cdots\det(A_m)"
