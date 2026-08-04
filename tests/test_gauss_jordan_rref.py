from __future__ import annotations

import numpy as np
import pytest

from engine.gauss_jordan_rref import GaussJordanRREF


def test_default_steps_produce_expected_rref() -> None:
    model = GaussJordanRREF()
    steps = model.steps()
    assert [step.label_tex for step in steps] == [
        r"R_3\leftarrow -\frac{1}{7}R_3",
        r"R_2\leftarrow R_2+2R_3",
        r"R_1\leftarrow R_1-R_3",
        r"R_1\leftarrow R_1-R_2",
    ]
    np.testing.assert_allclose(
        model.rref_augmented(),
        np.array(
            [
                [1.0, 0.0, 0.0, 1.0],
                [0.0, 1.0, 0.0, 1.0],
                [0.0, 0.0, 1.0, 1.0],
            ]
        ),
    )


def test_solution_is_read_directly_as_one_one_one() -> None:
    model = GaussJordanRREF()
    np.testing.assert_allclose(model.solution(), [1.0, 1.0, 1.0])
    assert model.direct_readoff_tex() == (r"x=1", r"y=1", r"z=1")


def test_snapshot_consistency() -> None:
    snapshot = GaussJordanRREF().snapshot()
    np.testing.assert_allclose(snapshot.echelon_augmented, GaussJordanRREF.DEFAULT_ECHELON_AUGMENTED)
    np.testing.assert_allclose(snapshot.rref_augmented[:, -1], [1.0, 1.0, 1.0])


@pytest.mark.parametrize(
    ("matrix", "message"),
    [
        (np.zeros((3, 4)), "full rank"),
        ([[1, 2], [3, 4]], "shape"),
    ],
)
def test_invalid_inputs_are_rejected(matrix, message) -> None:
    with pytest.raises(ValueError, match=message):
        GaussJordanRREF(matrix)
