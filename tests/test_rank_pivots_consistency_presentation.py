from pathlib import Path

SCENE_PATH = Path("scenes/rank_pivots_consistency_presentation.py")


def scene_source() -> str:
    return SCENE_PATH.read_text(encoding="utf-8")


def test_scene_introduces_rank_as_pivot_count() -> None:
    source = scene_source()
    assert "Rank, Pivots, and Consistency" in source
    assert "Pivots determine rank" in source
    assert "Rank is the number of pivot rows" in source
    assert "self._pivot_boxes(matrix, ((0, 0), (1, 1)), color=BLUE)" in source


def test_scene_compares_coefficient_and_augmented_rank() -> None:
    source = scene_source()
    assert "Consistency is a comparison of two ranks" in source
    assert "Equal ranks" in source
    assert "An augmented-column pivot" in source
    assert r"\operatorname{rank}(A)=2<3=\operatorname{rank}([A\mid\mathbf b])" in source
    assert "inconsistent" in source


def test_scene_contains_pause_and_predict_without_overlaying_a_matrix_card() -> None:
    source = scene_source()
    assert "Pause and Predict" in source
    assert "Which matrix represents a solvable system?" in source
    prompt_index = source.index("prompt = VGroup")
    assert "FadeOut(consistent_card)" in source[prompt_index:]
    assert "FadeOut(inconsistent_card)" in source[prompt_index:]


def test_scene_presents_unique_solution_case() -> None:
    source = scene_source()
    assert "Equal ranks and a pivot in every variable column" in source
    assert "no free variables" in source
    assert "one solution" in source
    assert "((0, 0), (1, 1), (2, 2))" in source


def test_scene_presents_infinite_solution_case() -> None:
    source = scene_source()
    assert "Equal ranks but fewer pivots than variables" in source
    assert "one free variable" in source
    assert "infinitely many solutions" in source
    assert "SurroundingRectangle(infinite_matrix.get_columns()[2]" in source


def test_scene_presents_inconsistent_case_and_contradiction() -> None:
    source = scene_source()
    assert "An augmented-column pivot destroys consistency" in source
    assert "((2, 3),)" in source
    assert r"0=3\quad\Longrightarrow\quad\text{no solution}" in source
    assert "contradictory row" in source


def test_scene_ends_with_rank_decision_tree() -> None:
    source = scene_source()
    assert "Read the solution type from rank and pivots" in source
    assert r"\operatorname{rank}(A)=\operatorname{rank}([A\mid\mathbf b])?" in source
    assert "Unique solution" in source
    assert "Infinitely many solutions" in source
    assert "No solution" in source
    assert r"\#\text{ free variables}=n-\operatorname{rank}(A)" in source


def test_scene_headings_and_content_are_vertically_separated() -> None:
    source = scene_source()
    assert 'heading = Text("Pivots determine rank", font_size=29).move_to(UP * 1.92)' in source
    assert 'compare_heading = Text("Consistency is a comparison of two ranks", font_size=29).move_to(UP * 1.96)' in source
    assert 'unique_heading = Text("Equal ranks and a pivot in every variable column", font_size=28).move_to(UP * 1.96)' in source
    assert 'display.move_to(LEFT * 3.08 + DOWN * 0.30)' in source
    assert 'unique_display.move_to(LEFT * 3.08 + DOWN * 0.28)' in source


def test_matrix_labels_align_to_all_four_columns() -> None:
    source = scene_source()
    assert 'MathTex("b", font_size=29, color=GREEN)' in source
    assert "zip(labels, matrix.get_columns(), strict=True)" in source
    assert "matrix.get_top()[1] + 0.23" in source


def test_student_facing_scene_omits_checkpoint_language() -> None:
    student_lines = [line for line in scene_source().splitlines() if "Text(" in line or "MathTex(" in line]
    assert all("checkpoint" not in line.lower() for line in student_lines)
