from pathlib import Path


SCENE_PATH = Path(__file__).parents[1] / "scenes" / "markov_long_term_behavior_presentation.py"
TEXT = SCENE_PATH.read_text()


def test_scene_has_established_chrome_and_steady_state_title():
    assert 'CHAPTER_BANNER = "GRAPHS, NETWORKS, AND THE LAPLACIAN"' in TEXT
    assert 'LESSON_TITLE = "Long-Term Probabilities and Steady States"' in TEXT
    assert r"\textbf{Long-Term Probabilities and Steady States}" in TEXT


def test_scene_uses_four_state_model_and_exact_spine():
    assert "MarkovLongTermBehavior.mixing_chain()" in TEXT
    assert "MarkovLongTermBehavior.branching_chain()" in TEXT
    assert 'RuntimeError("unexpected first probability step")' in TEXT
    assert 'RuntimeError("unexpected second probability step")' in TEXT
    assert 'RuntimeError("unexpected third probability step")' in TEXT
    assert 'RuntimeError("unexpected steady state")' in TEXT
    assert 'RuntimeError("unexpected regularity")' in TEXT


def test_scene_defines_probability_vectors_in_r4():
    assert "probability vector in R⁴" in TEXT
    assert r"x_i\ge0" in TEXT
    assert r"x_1+x_2+x_3+x_4=1" in TEXT
    assert r"x_k=A^k x_0" in TEXT


def test_scene_explains_transition_rule_before_matrix():
    assert "stay with probability one half" in TEXT
    assert '"STAY"' in TEXT
    assert '"CHOOSE UNIFORMLY"' in TEXT
    assert r"\frac12\cdot\frac14=\frac18" in TEXT
    assert r"\Pr(i\to i)=\frac12+\frac18=\frac58" in TEXT


def test_scene_displays_structural_four_by_four_matrix():
    assert "Markov matrix maps probability vectors" in TEXT
    assert TEXT.count(r"\frac58") >= 5
    assert TEXT.count(r"\frac18") >= 12
    assert "v_buff=1.50" in TEXT
    assert '"MARKOV MATRIX"' in TEXT
    assert r"x_{k+1}=Ax_k" in TEXT
    assert "entries ≥ 0; column j starts at state j" in TEXT
    assert '"COLUMN-STOCHASTIC"' in TEXT
    assert "not the earlier adjacency matrix" in TEXT


def test_scene_computes_first_step_as_first_column():
    assert r"x_0=e_1=(1,0,0,0)^T" in TEXT
    assert r"x_1=Ax_0=Ae_1" in TEXT
    assert r"\operatorname{column}_1(A)" in TEXT
    assert r"\left(\frac58,\frac18,\frac18,\frac18\right)^T" in TEXT


def test_scene_computes_second_power_coordinate_by_coordinate():
    assert r"x_2=A x_1=A^2x_0" in TEXT
    assert r"(x_2)_1=\frac58\frac58+3\left(\frac18\frac18\right)" in TEXT
    assert r"\frac{28}{64}=\frac7{16}" in TEXT
    assert r"(x_2)_2=\frac18\frac58+\frac58\frac18" in TEXT
    assert r"\frac{12}{64}=\frac3{16}" in TEXT


def test_scene_animates_successive_powers():
    assert r"x_2=\left(\frac7{16},\frac3{16},\frac3{16},\frac3{16}\right)^T" in TEXT
    assert r"x_3=\left(\frac{11}{32},\frac7{32},\frac7{32},\frac7{32}\right)^T" in TEXT
    assert "Transform(marks" in TEXT
    assert "rise toward one fourth" in TEXT


def test_scene_derives_power_formula_and_limit():
    assert "Regular means some power is entirely positive" in TEXT
    assert r"U=\frac14\mathbf1\mathbf1^T" in TEXT
    assert r"A=U+\frac12(I-U)" in TEXT
    assert r"A^k=U+2^{-k}(I-U)" in TEXT
    assert r"A^k\to U" in TEXT
    assert r"x_k=\frac14\mathbf1+2^{-k}\left(e_1-\frac14\mathbf1\right)" in TEXT
    assert r"(x_k)_{2,3,4}=\frac14-\frac{1}{4\cdot2^k}" in TEXT
    assert r"x_k\longrightarrow\left(\frac14,\frac14,\frac14,\frac14\right)^T" in TEXT
    assert "initial imbalance is halved" in TEXT


def test_scene_solves_ax_equals_x_directly():
    assert "normalized solution of Ax=x" in TEXT
    assert r"A=\frac12I+\frac18\mathbf1\mathbf1^T" in TEXT
    assert r"\mathbf1^Tx=1" in TEXT
    assert r"x=\frac14\mathbf1" in TEXT
    assert "individual transitions continue" in TEXT


def test_scene_contrasts_absorbing_steady_states():
    assert "Absorbing states are a contrasting source of steady states" in TEXT
    assert r"Be_3=e_3,\qquad Be_4=e_4" in TEXT
    assert r"x=(0,0,t,1-t)^T" in TEXT
    assert r"B^2e_1=\left(0,0,\frac12,\frac12\right)^T" in TEXT
    assert "depends on the starting probabilities" in TEXT


def test_scene_distinguishes_steady_state_from_convergence():
    assert "Ax=x identifies steady states" in TEXT
    assert '"REGULAR"' in TEXT
    assert '"ABSORBING"' in TEXT
    assert '"PERIODIC"' in TEXT
    assert r"Ce_1=e_2,\ Ce_2=e_1" in TEXT
    assert r"(A-I)x=0" in TEXT
    assert "normalized eigenvectors with eigenvalue 1" in TEXT
    assert "PageRank modifies a directed walk" in TEXT


def test_vertex_numerals_are_high_contrast_and_bottom_text_is_safe():
    assert "font_size=29, color=BLACK" in TEXT
    assert "font_size=30, color=BLACK" in TEXT
    assert "to_edge(DOWN, buff=0.70)" in TEXT
