from pathlib import Path

SCENE = Path("scenes/determinant_elimination_presentation.py")


def source() -> str:
    return SCENE.read_text(encoding="utf-8")


def test_scene_class_exists() -> None:
    assert "class DeterminantEliminationPresentation(Scene):" in source()


def test_scene_has_context_banner() -> None:
    text = source()
    assert "Methods of Computation" in text
    assert "Using elimination to compute determinants" in text


def test_scene_has_overview_card() -> None:
    text = source()
    assert "Determinants and elimination" in text
    assert "overview_rule_lines" in text
    assert "the pivot product gives det(U)" in text


def test_scene_has_example_setup() -> None:
    text = source()
    assert "Example: track determinant changes during elimination" in text
    assert "Use elimination to reach a triangular matrix U." in text
    assert 'MathTex(r"A"' in text
    assert "matrix.move_to(np.array([-4.1, 0.25, 0.0]))" in text
    assert "goal.move_to(np.array([2.95, 0.0, 0.0]))" in text


def test_scene_has_relaid_out_step_card() -> None:
    text = source()
    assert 'label.move_to(np.array([0.0, 3.02, 0.0]))' in text
    assert '("Start", example.initial_matrix, WHITE, np.array([-5.25, 1.56, 0.0]))' in text
    assert '("Step 1", example.steps[0].matrix, ORANGE, np.array([-1.55, 1.56, 0.0]))' in text
    assert '("Step 2", example.steps[1].matrix, BLUE, np.array([2.40, 1.56, 0.0]))' in text
    assert '("Step 3", example.steps[2].matrix, GREEN, np.array([2.15, -1.46, 0.0]))' in text
    assert '("Step 4", example.steps[3].matrix, RED, np.array([-1.55, -1.46, 0.0]))' in text



def test_scene_has_single_arrows_in_gaps() -> None:
    text = source()
    assert 'top_left_arrow = Arrow(' in text
    assert 'top_right_arrow = Arrow(' in text
    assert 'vertical_arrow = Arrow(' in text
    assert 'bottom_arrow = Arrow(' in text
    assert 'np.array([-4.20, 1.56, 0.0])' in text
    assert 'np.array([-0.45, 1.56, 0.0])' in text
    assert 'np.array([2.88, 0.82, 0.0])' in text
    assert 'np.array([0.95, -1.46, 0.0])' in text


def test_scene_has_compact_matrix_helper() -> None:
    text = source()
    assert 'def matrix_mobject(matrix: np.ndarray, font_size: int, h_buff: float = 0.9, v_buff: float = 0.68) -> Matrix:' in text
    assert 'h_buff=h_buff' in text
    assert 'v_buff=v_buff' in text


def test_scene_has_final_recovery() -> None:
    text = source()
    assert "Recover det(A) from the triangular matrix" in text
    assert r"\det(U)=1\cdot 1 \cdot \tfrac72 = \tfrac72" in text
    assert r"\det(U)=-\tfrac12\det(A)" in text
    assert "The pivot product gives det(U). Accounting for the swap and the scaling recovers det(A)." in text
    assert r"\det(A)=-7" in text


def test_scene_clears_stage_individually() -> None:
    text = source()
    assert "*[FadeOut(mob) for mob in list(self.mobjects) if mob not in preserve]" in text
    assert "VGroup(*self.mobjects)" not in text


def test_scene_r14_larger_directional_nudges() -> None:
    text = source()
    assert "top_left_op.move_to(np.array([-3.35, 1.98, 0.0]))" in text
    assert "top_left_det.move_to(np.array([-3.35, 1.00, 0.0]))" in text
    assert "top_right_op.move_to(np.array([0.45, 1.98, 0.0]))" in text
    assert "top_right_det.move_to(np.array([0.45, 0.93, 0.0]))" in text
    assert "bottom_op.move_to(np.array([0.30, -0.98, 0.0]))" in text
    assert "bottom_det.move_to(np.array([0.30, -1.88, 0.0]))" in text
    assert "vertical_op.move_to(np.array([2.05, 0.55, 0.0]))" in text
    assert "vertical_det.move_to(np.array([2.05, -0.20, 0.0]))" in text


def test_scene_r15_larger_elements_keep_r14_spacing() -> None:
    text = source()
    assert 'label = Text("Step-by-step elimination", font_size=34, color=YELLOW)' in text
    assert 'title_mob = Text(title, font_size=22, color=color)' in text
    assert 'matrix_mob = self.matrix_mobject(mat, font_size=17, h_buff=0.56, v_buff=0.42)' in text
    assert 'top_left_op = MathTex(r"r_1 \\leftrightarrow r_2", font_size=25, color=ORANGE)' in text
    assert 'top_left_det = MathTex(r"\\det(S_1)=-\\det(A)", font_size=19, color=ORANGE)' in text
    assert 'top_right_op = MathTex(r"r_2 \\to \\tfrac12 r_2", font_size=25, color=BLUE)' in text
    assert 'vertical_op = MathTex(r"r_3 \\to r_3-2r_1", font_size=25, color=GREEN)' in text
    assert 'bottom_op = MathTex(r"r_3 \\to r_3-r_2", font_size=25, color=RED)' in text
    assert 'stroke_width=5' in text
    assert 'top_left_op.move_to(np.array([-3.35, 1.98, 0.0]))' in text
    assert 'top_right_op.move_to(np.array([0.45, 1.98, 0.0]))' in text
    assert 'bottom_op.move_to(np.array([0.30, -0.98, 0.0]))' in text


def test_scene_r16_nudges_step2_cluster_right() -> None:
    text = source()
    assert '("Step 2", example.steps[1].matrix, BLUE, np.array([2.40, 1.56, 0.0]))' in text
    assert 'title_mob.move_to(pos + np.array([0.0, 0.98, 0.0]))' in text
    assert 'vertical_op.move_to(np.array([2.05, 0.55, 0.0]))' in text
    assert 'vertical_det.move_to(np.array([2.05, -0.20, 0.0]))' in text
