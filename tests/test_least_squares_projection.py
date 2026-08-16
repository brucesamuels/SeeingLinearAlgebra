import numpy as np

from engine.least_squares_projection import LeastSquaresProjectionLesson


def test_snapshot_uses_clean_three_by_two_example() -> None:
    snapshot = LeastSquaresProjectionLesson().snapshot()
    assert np.allclose(snapshot.A, np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]]))
    assert np.allclose(snapshot.b, np.array([2.0, 2.0, 1.0]))
    assert np.linalg.matrix_rank(snapshot.A) == 2


def test_least_squares_solution_projection_and_residual_are_exact() -> None:
    snapshot = LeastSquaresProjectionLesson().snapshot()
    assert np.allclose(snapshot.x_hat, np.array([1.0, 1.0]))
    assert np.allclose(snapshot.projection, np.array([1.0, 1.0, 2.0]))
    assert np.allclose(snapshot.residual, np.array([1.0, 1.0, -1.0]))


def test_residual_is_orthogonal_to_column_space() -> None:
    snapshot = LeastSquaresProjectionLesson().snapshot()
    assert np.allclose(snapshot.A.T @ snapshot.residual, np.zeros(2))
    assert np.isclose(np.dot(snapshot.a1, snapshot.residual), 0.0)
    assert np.isclose(np.dot(snapshot.a2, snapshot.residual), 0.0)


def test_normal_equation_data_are_small_integers() -> None:
    snapshot = LeastSquaresProjectionLesson().snapshot()
    assert np.allclose(snapshot.ata, np.array([[2.0, 1.0], [1.0, 2.0]]))
    assert np.allclose(snapshot.atb, np.array([3.0, 3.0]))
    assert np.allclose(snapshot.ata @ snapshot.x_hat, snapshot.atb)


def test_qr_route_gives_same_solution() -> None:
    snapshot = LeastSquaresProjectionLesson().snapshot()
    assert np.allclose(snapshot.Q.T @ snapshot.Q, np.eye(2))
    assert np.allclose(snapshot.Q @ snapshot.R, snapshot.A)
    assert np.allclose(np.linalg.solve(snapshot.R, snapshot.qtb), snapshot.x_hat)
