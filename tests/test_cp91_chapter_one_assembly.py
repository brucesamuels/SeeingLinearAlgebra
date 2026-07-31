import ast
from pathlib import Path

from engine.chapter_one_lesson_manifest import (
    CHAPTER_ONE_LESSONS,
    locate_scene_file,
)
from scripts.build_cp91_chapter_one import discover_scene_class


EXPECTED_KEYS = (
    "why_vectors",
    "vector_representation",
    "free_vector_equality",
    "placing_vector_at_origin",
    "special_vectors",
    "scalar_multiplication",
    "unit_vector",
    "vector_addition",
    "vector_addition_commutativity",
    "vector_subtraction",
    "three_vector_addition_3d",
    "infinite_possibilities",
    "inner_product_dot_product",
    "cross_product",
    "cross_product_computation",
)


def test_manifest_contains_complete_revised_chapter_one_sequence() -> None:
    assert tuple(lesson.key for lesson in CHAPTER_ONE_LESSONS) == EXPECTED_KEYS


def test_dot_and_cross_product_lessons_follow_vector_foundations() -> None:
    keys = tuple(lesson.key for lesson in CHAPTER_ONE_LESSONS)

    assert keys[-3:] == (
        "inner_product_dot_product",
        "cross_product",
        "cross_product_computation",
    )
    assert keys.index("infinite_possibilities") < keys.index("inner_product_dot_product")


def test_product_lesson_scene_filenames_are_explicit() -> None:
    by_key = {lesson.key: lesson for lesson in CHAPTER_ONE_LESSONS}

    assert by_key["inner_product_dot_product"].filename_candidates == (
        "inner_product_dot_product_presentation.py",
    )
    assert by_key["cross_product"].filename_candidates == (
        "cross_product_presentation.py",
    )
    assert by_key["cross_product_computation"].filename_candidates == (
        "cross_product_computation_presentation.py",
    )


def test_locator_prefers_exact_candidate(tmp_path: Path) -> None:
    spec = CHAPTER_ONE_LESSONS[0]
    expected = tmp_path / spec.filename_candidates[0]
    expected.write_text("class Example: pass", encoding="utf-8")
    assert locate_scene_file(tmp_path, spec) == expected


def test_scene_class_discovery_finds_presentation(tmp_path: Path) -> None:
    scene = tmp_path / "sample_presentation.py"
    scene.write_text(
        """from manim import Scene

class SamplePresentation(Scene):
    pass
""",
        encoding="utf-8",
    )
    assert discover_scene_class(scene) == "SamplePresentation"


def test_title_card_is_a_valid_scene() -> None:
    source = Path("scenes/chapter_one_title_card.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    classes = [node.name for node in tree.body if isinstance(node, ast.ClassDef)]

    assert "ChapterOneTitleCard" in classes
    assert "Chapter 1" in source
    assert "Vectors" in source


def test_render_script_builds_individual_lessons_not_legacy_combined_scene() -> None:
    source = Path("scripts/build_cp91_chapter_one.py").read_text(encoding="utf-8")

    assert "for index, lesson in enumerate(CHAPTER_ONE_LESSONS" in source
    assert "locate_scene_file" in source
    assert "discover_scene_class" in source
    assert "chapter_one_opening_presentation.py" not in source
    assert "ChapterOneOpeningPresentation" not in source


def test_render_output_path_is_dedicated_chapter_assembly() -> None:
    source = Path("scripts/build_cp91_chapter_one.py").read_text(encoding="utf-8")

    assert '"chapter_one_assembly"' in source
    assert '"ChapterOneAssembly.mp4"' in source


def test_focused_check_script_runs_only_cp91_tests() -> None:
    source = Path("scripts/check_cp91_chapter_one_assembly.zsh").read_text(
        encoding="utf-8"
    )

    assert "tests/test_cp91_chapter_one_assembly.py" in source
    assert "python -m pytest -q" in source
    assert "tests/test_linearity_preserves_linear_combinations_presentation.py" not in source


def test_locator_accepts_unit_vector_lesson_filename(tmp_path: Path) -> None:
    spec = next(
        lesson for lesson in CHAPTER_ONE_LESSONS if lesson.key == "unit_vector"
    )
    expected = tmp_path / "unit_vector_lesson.py"
    expected.write_text("from manim import Scene\n", encoding="utf-8")

    assert locate_scene_file(tmp_path, spec) == expected


def test_locator_fallback_searches_all_python_scene_files() -> None:
    source = Path(
        "engine/chapter_one_lesson_manifest.py"
    ).read_text(encoding="utf-8")

    assert 'scenes_dir.glob("*.py")' in source
    assert 'scenes_dir.glob("*_presentation.py")' not in source



def test_normalized_words_accepts_simple_plural_titles() -> None:
    from engine.chapter_one_lesson_manifest import _normalized_words

    words = _normalized_words("Unit Vectors")
    assert "unit" in words
    assert "vector" in words
    assert "vectors" in words

def test_locator_finds_unit_vector_scene_by_class_and_title(tmp_path: Path) -> None:
    scene_file = tmp_path / "magnitude_and_direction_scene.py"
    scene_file.write_text(
        """from manim import Scene

class UnitVectorMagnitudePresentation(Scene):
    TITLE = \"Unit Vectors\"

    def construct(self):
        pass
""",
        encoding="utf-8",
    )

    lesson = next(spec for spec in CHAPTER_ONE_LESSONS if spec.key == "unit_vector")
    assert locate_scene_file(tmp_path, lesson) == scene_file


def test_locator_failure_reports_available_scene_files(tmp_path: Path) -> None:
    scene_file = tmp_path / "unrelated_scene.py"
    scene_file.write_text(
        """from manim import Scene

class UnrelatedPresentation(Scene):
    def construct(self):
        pass
""",
        encoding="utf-8",
    )

    lesson = next(spec for spec in CHAPTER_ONE_LESSONS if spec.key == "unit_vector")
    try:
        locate_scene_file(tmp_path, lesson)
    except FileNotFoundError as error:
        message = str(error)
        assert "Available scene files" in message
        assert "unrelated_scene.py" in message
    else:
        raise AssertionError("Expected semantic scene discovery to fail")
