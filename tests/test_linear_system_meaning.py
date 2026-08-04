import numpy as np
import pytest

from engine.linear_system_meaning import LinearSystemMeaning


def test_default_planar_system_has_expected_unique_solution() -> None:
    snapshot = LinearSystemMeaning().planar_snapshot()

    np.testing.assert_allclose(snapshot.solution, [1.0, 1.0])
    assert snapshot.determinant == pytest.approx(-2.0)
    assert snapshot.equation_tex == (
        "x+y=2",
        "x-y=0",
    )


def test_default_three_dimensional_system_has_expected_unique_solution() -> None:
    snapshot = LinearSystemMeaning().snapshot()

    np.testing.assert_allclose(snapshot.solution, [1.0, 1.0, 1.0])
    assert snapshot.determinant == pytest.approx(7.0)


def test_columns_reconstruct_right_hand_side() -> None:
    snapshot = LinearSystemMeaning().snapshot()

    np.testing.assert_allclose(
        snapshot.reconstructed_right_hand_side,
        snapshot.right_hand_side,
    )
    np.testing.assert_allclose(
        snapshot.weighted_columns.sum(axis=0),
        snapshot.right_hand_side,
    )


def test_solution_lies_on_opening_lines_and_main_planes() -> None:
    system = LinearSystemMeaning()
    planar_solution = system.planar_snapshot().solution
    solution = system.snapshot().solution

    assert system.planar_satisfies(planar_solution)
    assert system.satisfies(solution)
    for row_index in range(2):
        assert system.line_height(
            row_index,
            planar_solution[0],
        ) == pytest.approx(planar_solution[1])
    for row_index in range(3):
        assert system.plane_height(
            row_index,
            solution[0],
            solution[1],
        ) == pytest.approx(solution[2])


def test_public_arrays_are_defensive_copies() -> None:
    system = LinearSystemMeaning()
    matrix = system.matrix
    rhs = system.right_hand_side
    matrix_2d = system.matrix_2d
    rhs_2d = system.right_hand_side_2d

    matrix[0, 0] = 99
    rhs[0] = 99
    matrix_2d[0, 0] = 99
    rhs_2d[0] = 99

    np.testing.assert_allclose(system.matrix, LinearSystemMeaning.DEFAULT_MATRIX)
    np.testing.assert_allclose(
        system.right_hand_side,
        LinearSystemMeaning.DEFAULT_RIGHT_HAND_SIDE,
    )
    np.testing.assert_allclose(system.matrix_2d, LinearSystemMeaning.DEFAULT_2D_MATRIX)
    np.testing.assert_allclose(
        system.right_hand_side_2d,
        LinearSystemMeaning.DEFAULT_2D_RIGHT_HAND_SIDE,
    )


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"matrix": np.eye(2)}, "shape"),
        ({"right_hand_side": [1.0, 2.0]}, "shape"),
        ({"matrix": np.zeros((3, 3))}, "unique solution"),
        ({"matrix_2d": np.zeros((2, 2))}, "matrix_2d"),
        ({"right_hand_side_2d": [1.0]}, "shape"),
    ],
)
def test_invalid_systems_are_rejected(kwargs, message) -> None:
    with pytest.raises(ValueError, match=message):
        LinearSystemMeaning(**kwargs)


def test_invalid_point_and_tolerance_are_rejected() -> None:
    system = LinearSystemMeaning()
    with pytest.raises(ValueError, match="point"):
        system.residual([1.0, 2.0])
    with pytest.raises(ValueError, match="point"):
        system.planar_residual([1.0, 2.0, 3.0])
    with pytest.raises(ValueError, match="tol"):
        system.satisfies([1.0, 1.0, 1.0], tol=-1.0)
    with pytest.raises(ValueError, match="tol"):
        system.planar_satisfies([1.0, 1.0], tol=-1.0)
