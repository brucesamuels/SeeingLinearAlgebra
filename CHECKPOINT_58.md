# Checkpoint 58 — Add Vector Addition to the Chapter 1 Opening

## Objective

Extend the renderer-independent Chapter 1 opening sequence and its thin
Manim orchestration scene so the approved **Vector Addition** lesson follows
**Placing a Vector at the Origin**.

## Chapter order after this checkpoint

1. Why Vectors?
2. What Is a Vector?
3. Free Vectors and Equality
4. Placing a Vector at the Origin
5. Vector Addition

The sequence now moves directly from the standard-position convention to
the first vector operation.

## Architectural decisions

- `CHAPTER_ONE_OPENING_SEQUENCE` remains the sole ordering authority.
- The combined Manim scene adds one registry entry and delegates to the
  existing `VectorAdditionPresentation.construct` implementation.
- No vector-addition mathematics, arrows, coordinate computation,
  parallelogram construction, labels, or animation code is copied into the
  combined scene.
- The approved 2D Vector Addition scene remains independently renderable.
- The three-vector 3D parallelepiped lesson remains a separate extension and
  is not added to the Chapter 1 opening.
- No new chapter abstraction is introduced.

## Modified files

- `engine/chapter_one_opening_sequence.py`
- `scenes/chapter_one_opening_presentation.py`
- `tests/test_chapter_one_opening_sequence.py`

## Added files

- `tests/test_chapter_one_opening_vector_addition_integration.py`
- `scripts/check_chapter_one_opening_vector_addition.zsh`
- `CHECKPOINT_58.md`

## Verification

```zsh
./scripts/check_chapter_one_opening_vector_addition.zsh
```

## Render

The existing combined-presentation script now renders five lessons:

```zsh
./scripts/render_chapter_one_opening_presentation.zsh
```

## Next architectural step

After visual approval, the next standalone vector-operation lesson should
introduce scalar multiplication before combining the two operations into
general linear combinations.

## Regression-test refinement

The CP55 standard-position test now verifies that `free_vector_equality` is
immediately followed by `placing_vector_at_origin`. It no longer assumes that
those lessons occupy the final two positions, allowing later lessons to be
appended without weakening the original pedagogical invariant.
