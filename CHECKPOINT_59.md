# Checkpoint 59 — Add 3D Addition to the Chapter 1 Opening

## Objective

Append the approved standalone **Three Vectors in 3-Space** lesson to the
combined Chapter 1 opening presentation.

The six-lesson order is now:

1. Why Vectors?
2. What Is a Vector?
3. Free Vectors and Equality
4. Placing a Vector at the Origin
5. Vector Addition
6. Three Vectors in 3-Space

## Architecture

`CHAPTER_ONE_OPENING_SEQUENCE` remains the sole ordering authority.

The combined scene delegates to the existing
`ThreeVectorAdditionPresentation`; it does not copy any three-vector
mathematics, 3D geometry, parallelepiped construction, labels, or camera
animation.

Because the final lesson requires Manim's `ThreeDScene` API, the combined
scene now inherits from:

```python
class ChapterOneOpeningPresentation(
    ThreeVectorAdditionPresentation,
    WhyVectorsPresentation,
):
```

The first base supplies the 3D camera and fixed-frame methods. The second
preserves the private helper methods required by the approved Why Vectors
lesson. All other lessons continue to delegate through the same registry.

## Modified files

- `engine/chapter_one_opening_sequence.py`
- `scenes/chapter_one_opening_presentation.py`
- `tests/test_chapter_one_opening_sequence.py`
- `tests/test_chapter_one_opening_vector_addition_integration.py`

## Added files

- `tests/test_chapter_one_opening_three_vector_addition_integration.py`
- `scripts/check_chapter_one_opening_with_3d_addition.zsh`
- `CHECKPOINT_59.md`

## Verification

```zsh
./scripts/check_chapter_one_opening_with_3d_addition.zsh
```

## Render

```zsh
./scripts/render_chapter_one_opening_presentation.zsh
```
