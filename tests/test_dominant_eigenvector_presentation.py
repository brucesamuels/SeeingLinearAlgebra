from pathlib import Path

SCENE = Path("scenes/dominant_eigenvector_presentation.py")

def source() -> str:
    return SCENE.read_text(encoding="utf-8")


def test_title_and_power_identity_are_present() -> None:
    text = source()
    assert 'LESSON_TITLE = "Dynamics and the Dominant Eigenvector"' in text
    assert r"A^k=QD^kQ^T" in text


def test_example_eigenvalues_are_four_and_two() -> None:
    text = source()
    assert r"\lambda_1=4" in text
    assert r"\lambda_2=2" in text


def test_component_ratio_is_shown() -> None:
    text = source()
    assert r"\left(\frac12\right)^k" in text
    assert r"\longrightarrow 0" in text


def test_geometry_tracks_normalized_iterates() -> None:
    text = source()
    assert "normalized_power_direction" in text
    assert "k=4" in text
    assert r"\mathbf q_1" in text


def test_general_dominance_statement_and_caveat_are_present() -> None:
    text = source()
    assert r"|\lambda_1|>|\lambda_2|" in text
    assert "nonzero component in the dominant eigendirection" in text


def test_student_scene_omits_checkpoint_number() -> None:
    assert "CP180" not in source()


def test_general_tex_separator_does_not_merge_with_A() -> None:
    text = source()
    assert r"\quadA" not in text
    assert r"\quad " in text
