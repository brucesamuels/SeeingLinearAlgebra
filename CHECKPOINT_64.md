# Checkpoint 64 — Integrate Scalar Multiplication into Chapter 1

## Purpose

Integrate the approved standalone scalar-multiplication lesson from
Checkpoint 63 into the combined Chapter 1 opening without duplicating
mathematical or Manim scene logic.

## Approved Chapter 1 order

1. Why Vectors?
2. What Is a Vector?
3. Free Vectors and Equality
4. Placing a Vector at the Origin
5. Scalar Multiplication
6. Vector Addition
7. Commutativity of Vector Addition
8. Vector Subtraction
9. Three Vectors in 3-Space

## Architectural guarantees

- `engine/chapter_one_opening_sequence.py` remains the source of truth.
- `ScalarMultiplicationPresentation` is reused unchanged.
- The combined presentation remains a thin delegating adapter.
- The existing 3D capstone remains last.
- The combined scene remains 3D-capable through its existing base class.
- Tests assert adjacency and relative ordering rather than brittle
  end-position assumptions.

## Files changed

- `engine/chapter_one_opening_sequence.py`
- `scenes/chapter_one_opening_presentation.py`
- `tests/test_chapter_one_opening_sequence.py`
- `tests/test_chapter_one_opening_vector_addition_integration.py`
- `tests/test_chapter_one_opening_three_vector_addition_integration.py`

## Files added

- `tests/test_chapter_one_opening_scalar_multiplication_integration.py`
- `scripts/check_chapter_one_opening_scalar_multiplication.zsh`
- `CHECKPOINT_64.md`

## Validation

Run:

```zsh
./scripts/check_chapter_one_opening_scalar_multiplication.zsh
```

Then render:

```zsh
./scripts/render_chapter_one_opening_presentation.zsh
```

Do not commit until the combined render has been visually approved.
