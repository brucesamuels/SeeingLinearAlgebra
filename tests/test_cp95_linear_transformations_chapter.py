from pathlib import Path
import ast

BUILD = Path("scripts/build_cp95_linear_transformations_chapter.py")
CARDS = Path("scenes/linear_transformations_chapter_cards.py")


def test_chapter_files_exist():
    assert BUILD.exists()
    assert CARDS.exists()


def test_opening_and_reflection_classes_exist():
    source = CARDS.read_text(encoding="utf-8")
    tree = ast.parse(source)
    classes = {
        node.name
        for node in tree.body
        if isinstance(node, ast.ClassDef)
    }

    assert "LinearTransformationsChapterOpening" in classes
    assert "LinearTransformationsChapterReflection" in classes


def test_chapter_order_ends_at_basis_images_to_matrix():
    source = BUILD.read_text(encoding="utf-8")

    expected_order = [
        "Chapter opening",
        "What a linear transformation does",
        "Which transformations are linear",
        "Reflection then dilation",
        "Reflection preserves addition",
        "Linearity preserves linear combinations",
        "Composition of transformations",
        "A basis determines the transformation",
        "Basis images become matrix columns",
        "Chapter reflection",
    ]

    positions = [source.index(f'"{label}"') for label in expected_order]
    assert positions == sorted(positions)


def test_cp94_is_not_in_linear_transformations_assembly():
    source = BUILD.read_text(encoding="utf-8")

    assert "matrix_vector_column_combination" not in source
    assert "MatrixVectorColumnCombinationPresentation" not in source


def test_reflection_states_basis_determines_everything():
    source = CARDS.read_text(encoding="utf-8")

    assert "what else remains to be determined?" in source
    assert "Nothing." in source
    assert "Every vector is a linear combination of the basis vectors." in source
    assert "T(x) = x₁T(e₁) + x₂T(e₂)" in source


def test_output_path_is_stable():
    source = BUILD.read_text(encoding="utf-8")

    assert 'LinearTransformationsChapter.mp4' in source
    assert '"linear_transformations_chapter"' in source
