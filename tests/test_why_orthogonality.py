import numpy as np
import pytest

from engine.why_orthogonality import BasisExample, WhyOrthogonalityLesson


def test_determinant_bridge_preserves_expected_area_scale() -> None:
    s = WhyOrthogonalityLesson().determinant_bridge()
    assert s.matrix.shape == (2, 2)
    assert s.reference_square.shape == (4, 2)
    assert s.transformed_region.shape == (4, 2)
    assert s.area_scale == pytest.approx(2.0)


def test_skew_and_orthogonal_examples_reconstruct_same_target() -> None:
    lesson = WhyOrthogonalityLesson()
    skew = lesson.skew_basis()
    ortho = lesson.orthogonal_basis()
    np.testing.assert_allclose(skew.target, [2.0, 1.0])
    np.testing.assert_allclose(ortho.target, [2.0, 1.0])


def test_examples_are_bases_but_have_different_geometry() -> None:
    lesson = WhyOrthogonalityLesson()
    skew = lesson.skew_basis()
    ortho = lesson.orthogonal_basis()
    assert skew.is_independent
    assert ortho.is_independent
    assert not skew.is_perpendicular
    assert ortho.is_perpendicular


def test_basis_example_rejects_dependent_vectors() -> None:
    with pytest.raises(ValueError, match="linearly independent"):
        BasisExample((1, 2), (2, 4), (1, 1))


def test_chapter_preview_topics_make_projection_the_next_spine() -> None:
    assert WhyOrthogonalityLesson().preview_topics == (
        "Projection",
        "Orthogonal decomposition",
        "Gram-Schmidt",
        "QR factorization",
        "Least squares",
    )
