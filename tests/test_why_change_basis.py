import numpy as np
import pytest

from engine.why_change_basis import WhyChangeBasisLesson


def test_default_example_has_two_coordinate_descriptions() -> None:
    lesson = WhyChangeBasisLesson()
    assert np.allclose(lesson.vector, [4.0, 2.0])
    assert np.allclose(lesson.basis_coordinates(), [3.0, 1.0])


def test_basis_coordinates_reconstruct_same_vector() -> None:
    lesson = WhyChangeBasisLesson()
    assert np.allclose(lesson.reconstruct(), lesson.vector)
    assert np.allclose(lesson.basis @ lesson.basis_coordinates(), lesson.vector)


def test_description_keeps_geometric_vector_distinct_from_coordinates() -> None:
    description = WhyChangeBasisLesson().description()
    assert np.allclose(description.standard_coordinates, [4.0, 2.0])
    assert np.allclose(description.basis_coordinates, [3.0, 1.0])
    assert not np.allclose(description.standard_coordinates, description.basis_coordinates)


def test_dependent_basis_is_rejected() -> None:
    with pytest.raises(ValueError, match="linearly independent"):
        WhyChangeBasisLesson(basis=np.array([[1.0, 2.0], [2.0, 4.0]]))


def test_invalid_shapes_are_rejected() -> None:
    with pytest.raises(ValueError, match="vector must have shape"):
        WhyChangeBasisLesson(vector=np.array([[4.0], [2.0]]))
    with pytest.raises(ValueError, match="basis must have shape"):
        WhyChangeBasisLesson(basis=np.eye(3))

