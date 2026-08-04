from __future__ import annotations

import numpy as np
import pytest

from engine.back_substitution import BackSubstitution


def test_default_solution_is_one_one_one() -> None:
    model = BackSubstitution()
    np.testing.assert_allclose(model.solution(), [1.0, 1.0, 1.0])


def test_steps_match_expected_algebra() -> None:
    steps = BackSubstitution().steps()
    assert [step.variable for step in steps] == ["z", "y", "x"]
    assert [step.equation_tex for step in steps] == [
        r"-7z=-7",
        r"y-2(1)=-1",
        r"x+1+1=3",
    ]
    assert [step.solved_tex for step in steps] == [r"z=1", r"y=1", r"x=1"]


def test_solution_satisfies_original_system() -> None:
    model = BackSubstitution()
    assert model.satisfies_original(model.solution())
    np.testing.assert_allclose(model.residual_in_original([1.0, 1.0, 1.0]), [0.0, 0.0, 0.0])


def test_snapshot_contains_original_equations() -> None:
    snapshot = BackSubstitution().snapshot()
    assert snapshot.original_equations_tex == (
        r"x+y+z=3",
        r"2x-y+z=2",
        r"x+2y-z=2",
    )


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"echelon_augmented": [[1, 2], [3, 4]]}, "shape"),
        ({"original_augmented": [[1, 2], [3, 4]]}, "shape"),
        ({"echelon_augmented": np.zeros((3, 4))}, "full rank"),
        ({"original_augmented": np.zeros((3, 4))}, "full rank"),
    ],
)
def test_invalid_inputs_are_rejected(kwargs, message) -> None:
    with pytest.raises(ValueError, match=message):
        BackSubstitution(**kwargs)


def test_invalid_verification_point_is_rejected() -> None:
    with pytest.raises(ValueError, match="shape"):
        BackSubstitution().residual_in_original([1.0, 2.0])
    with pytest.raises(ValueError, match="atol"):
        BackSubstitution().satisfies_original([1.0, 1.0, 1.0], atol=-1.0)
