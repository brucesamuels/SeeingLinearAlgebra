import numpy as np
import pytest
from engine.repeated_eigenvalues import RepeatedEigenvaluesLesson


def test_good_example_has_two_dimensional_eigenspace() -> None:
    example = RepeatedEigenvaluesLesson().good_example()
    assert example.algebraic_multiplicity == 2
    assert example.geometric_multiplicity == 2
    assert example.diagonalizable


def test_bad_example_has_one_dimensional_eigenspace() -> None:
    example = RepeatedEigenvaluesLesson().bad_example()
    assert example.algebraic_multiplicity == 2
    assert example.geometric_multiplicity == 1
    assert not example.diagonalizable


def test_bad_eigenvectors_satisfy_shifted_equation() -> None:
    example = RepeatedEigenvaluesLesson().bad_example()
    shifted = example.matrix - 2 * np.eye(2)
    for vector in example.eigenspace_basis:
        assert np.allclose(shifted @ vector, 0)


def test_same_characteristic_polynomial_is_explicit() -> None:
    assert RepeatedEigenvaluesLesson.same_characteristic_polynomial()


def test_multiplicity_criterion() -> None:
    lesson = RepeatedEigenvaluesLesson()
    assert lesson.diagonalizable_from_multiplicities(2, 2)
    assert not lesson.diagonalizable_from_multiplicities(2, 1)
    with pytest.raises(ValueError):
        lesson.diagonalizable_from_multiplicities(1, 2)
