import pytest

from engine.orthogonal_sets import OrthogonalSetExample, OrthogonalSetsLesson


def test_orthogonal_example_has_all_zero_pairwise_dots() -> None:
    snapshot = OrthogonalSetsLesson().orthogonal_example()
    assert snapshot.is_orthogonal
    assert snapshot.pairwise_dots == (
        (0, 1, pytest.approx(0.0)),
        (0, 2, pytest.approx(0.0)),
        (1, 2, pytest.approx(0.0)),
    )


def test_nonexample_has_exactly_one_offending_pair() -> None:
    snapshot = OrthogonalSetsLesson().nonexample()
    nonzero_pairs = [(i, j, value) for i, j, value in snapshot.pairwise_dots if not pytest.approx(0.0) == value]
    assert len(nonzero_pairs) == 1
    assert nonzero_pairs[0][0:2] == (0, 2)
    assert nonzero_pairs[0][2] == pytest.approx(3.0)
    assert not snapshot.is_orthogonal


def test_lesson_contains_definition_theorem_and_bridge() -> None:
    lesson = OrthogonalSetsLesson()
    assert "is orthogonal if" in lesson.DEFINITION
    assert "linearly independent" in lesson.THEOREM
    assert lesson.bridge_to_orthonormal == (
        r"\mathbf{v}_i\cdot\mathbf{v}_j=0\quad (i\ne j)",
        r"\|\mathbf{v}_i\|=1",
    )


def test_example_rejects_mismatched_dimensions() -> None:
    with pytest.raises(ValueError, match="same dimension"):
        OrthogonalSetExample(((1, 0), (0, 1, 0)))


def test_example_rejects_zero_vector() -> None:
    with pytest.raises(ValueError, match="nonzero"):
        OrthogonalSetExample(((1, 0, 0), (0, 0, 0)))
