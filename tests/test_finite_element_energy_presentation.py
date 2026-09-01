from pathlib import Path


SOURCE = Path(__file__).parents[1] / "scenes" / "finite_element_energy_presentation.py"
TEXT = SOURCE.read_text()


def test_scene_uses_structural_matrix_objects():
    assert "Matrix(entries" in TEXT
    assert r"\begin{bmatrix}" not in TEXT


def test_scene_defines_the_problem_and_continuous_energy():
    assert r"-u''(x)=1,\qquad 0<x<1" in TEXT
    assert r"u(0)=0" in TEXT
    assert r"u(1)=0" in TEXT
    assert r"J(u)=\frac12\int_0^1" in TEXT
    assert "Finite elements replace the unknown function" in TEXT


def test_scene_explains_the_physics_and_boundary_conditions():
    assert "downward displacement" in TEXT
    assert r"-T\,u''(x)=q(x)" in TEXT
    assert "string tension" in TEXT
    assert "downward load per unit length" in TEXT
    assert "concave down" in TEXT
    assert r"T=1,\quad q(x)=1\quad\Longrightarrow\quad -u''(x)=1" in TEXT
    assert "left end fixed at zero displacement" in TEXT
    assert "right end fixed at zero displacement" in TEXT
    assert "boundary conditions in space, not initial conditions in time" in TEXT


def test_scene_defines_mesh_hat_functions_and_approximation():
    assert "Divide the interval into three finite elements." in TEXT
    assert r"\phi_1" in TEXT
    assert r"\phi_2" in TEXT
    assert r"u_h(x)=c_1\phi_1(x)+c_2\phi_2(x)" in TEXT
    assert "Each hat equals 1 at its own node" in TEXT


def test_scene_assembles_stiffness_matrix_and_load_vector():
    assert r"K^{(e)}=\frac1h" in TEXT
    assert '[["3", "-3", "0", "0"], ["-3", "6", "-3", "0"]' in TEXT
    assert '[["6", "-3"], ["-3", "6"]]' in TEXT
    assert r"f_i=\int_0^1\phi_i(x)\,dx" in TEXT
    assert '[[r"\\frac13"], [r"\\frac13"]]' in TEXT


def test_scene_connects_positive_energy_to_unique_minimizer():
    assert r"J(c)=\frac12c^TKc-f^Tc" in TEXT
    assert r"c^TKc=\int_0^1" in TEXT
    assert "Positive definiteness guarantees one unique minimizer." in TEXT


def test_scene_has_prediction_solve_and_piecewise_linear_result():
    assert "Pause: what equation must the minimizing coefficients satisfy?" in TEXT
    assert r"\nabla J(c)=Kc-f=0" in TEXT
    assert r"\boxed{Kc=f}" in TEXT
    assert r"c_1=c_2=\frac19" in TEXT
    assert "model.nodal_values()" in TEXT


def test_scene_finishes_with_four_step_recipe_and_preserves_scope():
    for step in range(1, 5):
        assert f"self._recipe_card({step}," in TEXT
    assert "positive energy  →  positive definite matrix  →  unique approximation" in TEXT
    forbidden = ("weak form", "integration by parts", "convergence rate", "Galerkin")
    assert not any(word.lower() in TEXT.lower() for word in forbidden)


def test_scene_is_standalone_without_checkpoint_references():
    assert "CP211" not in TEXT
    assert "CP210" not in TEXT
    assert "checkpoint" not in TEXT.lower()
