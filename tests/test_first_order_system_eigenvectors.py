import numpy as np
from engine.first_order_system_eigenvectors import FirstOrderSystemEigenvectorsLesson


def test_eigen_data_are_correct() -> None:
    lesson=FirstOrderSystemEigenvectorsLesson()
    A=lesson.matrix; Q=lesson.eigenvectors; lam=lesson.eigenvalues
    assert np.allclose(A@Q, Q@np.diag(lam))


def test_initial_coordinates_are_sqrt2_sqrt2() -> None:
    lesson=FirstOrderSystemEigenvectorsLesson()
    assert np.allclose(lesson.initial_eigen_coordinates(), [np.sqrt(2),np.sqrt(2)])


def test_closed_form_matches_eigenbasis_solution() -> None:
    lesson=FirstOrderSystemEigenvectorsLesson()
    for t in [0.0,0.2,0.5,1.0]:
        assert np.allclose(lesson.solution(t), lesson.closed_form_solution(t))


def test_initial_condition_is_satisfied() -> None:
    lesson=FirstOrderSystemEigenvectorsLesson()
    assert np.allclose(lesson.solution(0.0), [2.0,0.0])


def test_solution_direction_approaches_dominant_eigenvector() -> None:
    lesson=FirstOrderSystemEigenvectorsLesson()
    d=lesson.normalized_solution_direction(3.0)
    q=lesson.dominant_direction()
    assert np.dot(d,q)>0.999
