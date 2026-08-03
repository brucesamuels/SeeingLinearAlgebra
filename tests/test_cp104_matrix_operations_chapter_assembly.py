import ast
from pathlib import Path

BUILD_PATH = Path("scripts/build_cp104_matrix_operations_chapter.py")
CARDS_PATH = Path("scenes/matrix_operations_chapter_cards.py")


def build_source() -> str:
    return BUILD_PATH.read_text(encoding="utf-8")


def cards_source() -> str:
    return CARDS_PATH.read_text(encoding="utf-8")


def test_build_script_is_valid_python() -> None:
    ast.parse(build_source())


def test_cards_scene_is_valid_python() -> None:
    ast.parse(cards_source())


def test_chapter_contains_opening_and_reflection_cards() -> None:
    text = cards_source()
    assert "class MatrixOperationsChapterTitleCard(Scene)" in text
    assert "class MatrixOperationsChapterReflectionCard(Scene)" in text
    assert "How do matrices combine, act, and preserve structure?" in text
    assert "Chapter Reflection" in text


def test_chapter_manifest_contains_all_lessons_in_order() -> None:
    text = build_source()
    ordered_labels = [
        "Opening card",
        "Matrix addition and subtraction",
        "Scalar multiplication of matrices",
        "Matrix-vector multiplication as a column combination",
        "The row-column rule",
        "Matrix-matrix multiplication",
        "Matrix multiplication as composition",
        "The trace of a matrix",
        "Matrix transposition",
        "Order, identity, and undoing",
        "Closing reflection",
    ]

    positions = [text.index(label) for label in ordered_labels]
    assert positions == sorted(positions)


def test_manifest_references_known_scene_files_and_classes() -> None:
    text = build_source()
    expected = [
        "matrix_addition_subtraction_presentation.py",
        "MatrixAdditionSubtractionPresentation",
        "matrix_scalar_multiplication_presentation.py",
        "MatrixScalarMultiplicationPresentation",
        "row_column_rule_presentation.py",
        "RowColumnRulePresentation",
        "matrix_matrix_multiplication_presentation.py",
        "MatrixMatrixMultiplicationPresentation",
        "matrix_multiplication_composition_presentation.py",
        "MatrixMultiplicationCompositionPresentation",
        "matrix_trace_presentation.py",
        "MatrixTracePresentation",
        "matrix_transposition_presentation.py",
        "MatrixTranspositionPresentation",
        "matrix_order_identity_undoing_presentation.py",
        "MatrixOrderIdentityUndoingPresentation",
    ]
    for item in expected:
        assert item in text


def test_cp94_scene_is_discovered_robustly() -> None:
    text = build_source()
    assert "discovery_terms" in text
    assert '"column combination"' in text
    assert '"matrix-vector"' in text
    assert "discover_scene" in text


def test_builder_renders_and_concatenates_with_ffmpeg() -> None:
    text = build_source()
    assert '"-m",' in text
    assert '"manim",' in text
    assert '"ffmpeg",' in text
    assert '"concat",' in text
    assert "MatrixOperationsChapter.mp4" in text


def test_title_and_reflection_text_fit_width() -> None:
    text = cards_source()
    assert "question.scale_to_fit_width(11.0)" in text
    assert "prompt.scale_to_fit_width(11.0)" in text
    assert "final.scale_to_fit_width(11.2)" in text


def test_reuse_mode_always_rerenders_chapter_cards() -> None:
    text = build_source()
    assert "always_rerender = class_name in" in text
    assert '"MatrixOperationsChapterTitleCard"' in text
    assert '"MatrixOperationsChapterReflectionCard"' in text
    assert "if args.reuse_existing and not always_rerender:" in text
