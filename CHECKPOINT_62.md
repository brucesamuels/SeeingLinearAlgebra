# Checkpoint 62 — Integrate Commutativity and Vector Subtraction into Chapter 1

## Objective

Insert the approved standalone commutativity and vector-subtraction lessons into the combined Chapter 1 opening while preserving the approved scenes unchanged.

The eight-lesson order is:

1. Why Vectors?
2. What Is a Vector?
3. Free Vectors and Equality
4. Placing a Vector at the Origin
5. Vector Addition
6. Commutativity of Vector Addition
7. Vector Subtraction
8. Three Vectors in 3-Space

## Architecture

`engine/chapter_one_opening_sequence.py` remains the sole source of truth for lesson order.

`scenes/chapter_one_opening_presentation.py` remains a thin renderer-side adapter. It adds registry entries for:

```python
"vector_addition_commutativity": VectorAdditionCommutativityPresentation
"vector_subtraction": VectorSubtractionPresentation
```

The combined scene delegates through the existing generic call:

```python
presentation_class.construct(self)
```

No commutativity mathematics, vector-subtraction mathematics, arrow construction, coordinate calculation, or instructional wording is copied into the combined scene.

## 3D capability

The combined scene continues to inherit from:

```python
class ChapterOneOpeningPresentation(
    ThreeVectorAdditionPresentation,
    WhyVectorsPresentation,
):
```

The three-vector lesson remains the final capstone, and the combined presentation retains Manim's 3D camera and fixed-frame APIs.

## Modified files

- `engine/chapter_one_opening_sequence.py`
- `scenes/chapter_one_opening_presentation.py`
- `tests/test_chapter_one_opening_sequence.py`
- `tests/test_chapter_one_opening_three_vector_addition_integration.py`

## Added files

- `tests/test_chapter_one_opening_commutativity_integration.py`
- `tests/test_chapter_one_opening_vector_subtraction_integration.py`
- `scripts/check_chapter_one_opening_commutativity_and_subtraction.zsh`
- `CHECKPOINT_62.md`

## Test strategy

The focused integration tests verify:

- vector addition is immediately followed by commutativity;
- commutativity is immediately followed by subtraction;
- subtraction is immediately followed by the 3D capstone;
- the 3D capstone remains last;
- both new registry entries reuse the approved standalone scene classes;
- the combined scene contains no copied commutativity or subtraction implementation;
- both standalone scenes remain independently renderable;
- the full registry agrees with the renderer-independent sequence;
- the combined presentation remains 3D-capable.

Older end-of-sequence assumptions are replaced by adjacency and relative-order assertions.

## Verification

```zsh
./scripts/check_chapter_one_opening_commutativity_and_subtraction.zsh
```

## Render

```zsh
./scripts/render_chapter_one_opening_presentation.zsh
```

Do not commit until the combined render is visually approved.
