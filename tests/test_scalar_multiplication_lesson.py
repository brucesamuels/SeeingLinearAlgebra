from engine.scalar_multiplication_lesson import (
    BASE_VECTOR,
    SCALAR_MULTIPLICATION_STAGES,
    scaled_vector,
)


def test_approved_base_vector_is_used() -> None:
    assert BASE_VECTOR == (2.0, 1.0)


def test_stages_cover_stretch_contract_zero_and_reverse() -> None:
    assert tuple(stage.key for stage in SCALAR_MULTIPLICATION_STAGES) == (
        "stretch",
        "contract",
        "zero",
        "reverse",
    )
    assert tuple(stage.scalar for stage in SCALAR_MULTIPLICATION_STAGES) == (
        2.0,
        0.5,
        0.0,
        -1.0,
    )


def test_scaled_vector_values_are_exact() -> None:
    assert scaled_vector(2.0) == (4.0, 2.0)
    assert scaled_vector(0.5) == (1.0, 0.5)
    assert scaled_vector(0.0) == (0.0, 0.0)
    assert scaled_vector(-1.0) == (-2.0, -1.0)
