from pathlib import Path
SCENE_PATH=Path("scenes/first_order_system_eigenvectors_presentation.py")

def source()->str: return SCENE_PATH.read_text(encoding="utf-8")

def test_title_and_system_are_explicit()->None:
    t=source(); assert 'LESSON_TITLE="Solving a First-Order System with Eigenvectors"' in t
    assert r"\mathbf x'(t)=A\mathbf x(t)" in t

def test_ansatz_derives_eigenvalue_equation()->None:
    t=source(); assert r"\mathbf x(t)=e^{\lambda t}\mathbf v" in t; assert r"A\mathbf v=\lambda\mathbf v" in t

def test_general_solution_and_initial_condition_are_shown()->None:
    t=source(); assert r"\mathbf x(t)=c_1e^{4t}\mathbf q_1+c_2e^{2t}\mathbf q_2" in t
    assert r"\mathbf x(0)=\begin{bmatrix}2\\0\end{bmatrix}" in t
    assert r"c_1=c_2=\sqrt2" in t

def test_closed_form_solution_is_shown()->None:
    assert r"\begin{bmatrix}e^{4t}+e^{2t}\\e^{4t}-e^{2t}\end{bmatrix}" in source()

def test_long_term_ratio_and_decoupling_are_shown()->None:
    t=source(); assert r"e^{-2t}\longrightarrow0" in t
    assert r"\mathbf y'(t)=D\mathbf y(t)" in t
    assert r"y_1'=4y_1,\qquad y_2'=2y_2" in t

def test_no_checkpoint_number_in_student_scene()->None:
    assert "CP181" not in source()

def test_no_known_latex_concatenation_hazards()->None:
    t=source(); assert r"\quadA" not in t; assert r"\qquadA" not in t


def test_card_four_initial_condition_block_is_shifted_lower() -> None:
    text = source()
    assert "ivp=VGroup(ic,decomp,coeffs,sol1,sol2).arrange(DOWN,buff=0.36).scale(0.96).shift(DOWN*0.42)" in text
