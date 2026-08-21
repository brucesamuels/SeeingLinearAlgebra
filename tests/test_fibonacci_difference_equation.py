import numpy as np
from engine.fibonacci_difference_equation import FibonacciDifferenceEquationLesson, PHI, PSI


def test_fibonacci_values() -> None:
    lesson = FibonacciDifferenceEquationLesson()
    assert [lesson.fibonacci(n) for n in range(9)] == [0,1,1,2,3,5,8,13,21]


def test_state_matches_matrix_power() -> None:
    lesson = FibonacciDifferenceEquationLesson()
    for n in range(9):
        assert np.allclose(lesson.state(n), lesson.matrix_power_state(n))


def test_diagonalized_power_matches_matrix_power() -> None:
    lesson = FibonacciDifferenceEquationLesson()
    for n in range(6):
        assert np.allclose(lesson.diagonalized_power(n), np.linalg.matrix_power(lesson.matrix, n))


def test_binet_formula() -> None:
    lesson = FibonacciDifferenceEquationLesson()
    for n in range(12):
        assert abs(lesson.binet(n) - lesson.fibonacci(n)) < 1e-8


def test_eigenvalues_are_golden_ratio_pair() -> None:
    lesson = FibonacciDifferenceEquationLesson()
    phi, psi = lesson.eigenvalues
    assert np.isclose(phi, PHI)
    assert np.isclose(psi, PSI)
    assert np.isclose(phi + psi, 1.0)
    assert np.isclose(phi * psi, -1.0)


def test_ratio_approaches_phi() -> None:
    lesson = FibonacciDifferenceEquationLesson()
    assert abs(lesson.ratio(15) - PHI) < 1e-5
