from engine.determinant_invertibility import (
    closing_lines, geometric_lines, invertible_chain_tex, invertible_determinant,
    homogeneous_system_statement_tex, invertible_example, null_vector_equation_tex,
    nullspace_invertibility_theorem_tex, singular_chain_tex,
    singular_determinant, singular_example, singular_null_vector,
)


def test_invertible_example_is_triangular_and_nonzero_determinant() -> None:
    assert invertible_example() == ((2, 1, 0), (0, 3, 1), (0, 0, 4))
    assert invertible_determinant() == 24


def test_singular_example_has_dependent_rows_and_zero_determinant() -> None:
    B = singular_example()
    assert B[1] == tuple(2 * x for x in B[0])
    assert singular_determinant() == 0


def test_null_vector_is_nonzero_and_correct() -> None:
    B, v = singular_example(), singular_null_vector()
    assert v != (0, 0, 0)
    assert tuple(sum(B[i][j] * v[j] for j in range(3)) for i in range(3)) == (0, 0, 0)


def test_null_vector_equation_contains_matrix_vector_and_zero() -> None:
    tex = null_vector_equation_tex()
    assert r"\begin{bmatrix}-1\\-1\\1\end{bmatrix}" in tex
    assert r"=\begin{bmatrix}0\\0\\0\end{bmatrix}" in tex


def test_invertible_chain_links_core_equivalences() -> None:
    joined = " ".join(invertible_chain_tex())
    assert r"\det(A)\neq 0" in joined
    assert r"\operatorname{rank}(A)=n" in joined
    assert r"\mathcal N(A)=\{\mathbf 0\}" in joined
    assert "invertible" in joined


def test_singular_chain_links_core_equivalences() -> None:
    joined = " ".join(singular_chain_tex())
    assert r"\det(A)=0" in joined
    assert r"\operatorname{rank}(A)<n" in joined
    assert r"\mathcal N(A)\neq\{\mathbf 0\}" in joined
    assert "singular" in joined


def test_geometric_lines_connect_zero_determinant_to_collapse() -> None:
    lines = geometric_lines()
    assert "no dimension is lost" in lines[0]
    assert "signed volume" in lines[1]
    assert "collapses dimension" in lines[2]


def test_closing_lines_state_invertibility_test() -> None:
    lines = closing_lines()
    assert "square matrix" in lines[0]
    assert "invertible" in lines[1]
    assert "singular" in lines[2]


def test_formal_nullspace_invertibility_theorem() -> None:
    theorem = nullspace_invertibility_theorem_tex()
    assert r"A\text{ is invertible}" in theorem
    assert r"\Longleftrightarrow" in theorem
    assert r"\mathcal N(A)=\{\mathbf 0\}" in theorem
    statement = homogeneous_system_statement_tex()
    assert r"A\mathbf x=\mathbf 0" in statement
    assert "only the trivial solution" in statement
