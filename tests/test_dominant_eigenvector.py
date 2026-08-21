import numpy as np
from engine.dominant_eigenvector import DominantEigenvectorLesson


def test_example_has_both_eigen_components() -> None:
    ex = DominantEigenvectorLesson().example()
    assert np.allclose(ex.eigen_coordinates, [1, 1])


def test_power_formula_matches_direct_matrix_power() -> None:
    lesson = DominantEigenvectorLesson()
    x = lesson.example().vector
    for k in (0, 1, 2, 4):
        assert np.allclose(lesson.power_on_example(k), np.linalg.matrix_power(lesson.matrix, k) @ x)


def test_normalized_iterates_approach_dominant_direction() -> None:
    lesson = DominantEigenvectorLesson()
    q1 = lesson.dominant_direction()
    d2 = np.linalg.norm(lesson.normalized_power_direction(2) - q1)
    d8 = np.linalg.norm(lesson.normalized_power_direction(8) - q1)
    assert d8 < d2
