# Checkpoint 149 - Why Orthogonality?

## Purpose

Open Chapter 6, **Orthogonality and Projection**, as a direct continuation of
the determinant chapter.  The lesson does not yet define orthogonality
algebraically.  Instead, it creates the need for the next lesson by asking
whether some coordinate directions are especially useful.

## Mathematical narrative

1. Reuse determinant-era area geometry and briefly recall
   `|det A| = area scale factor`.
2. Shift the question from *how much area changes* to *how useful the chosen
   coordinate directions are*.
3. Compare a skew basis with a perpendicular basis for the same plane.
4. Decompose the same target vector in both coordinate systems.
5. End with the chapter question:
   “What becomes possible when our directions are orthogonal?”
6. Preview the visual spine: projection, orthogonal decomposition,
   Gram-Schmidt, QR factorization, and least squares.

The dot-product test `u dot v = 0` is intentionally deferred to CP150.
Projection formulas are also intentionally absent.

## Architecture

- `engine/why_orthogonality.py` owns all numerical geometry.
- `scenes/why_orthogonality_presentation.py` is a thin 2D Manim presentation.
- The scene uses a fixed header hierarchy and separates central mathematics from
  explanatory text at the bottom of each card.
- No camera motion or 3D geometry is used.
- All vector arrows have nonzero length.

## Files

- `engine/why_orthogonality.py`
- `scenes/why_orthogonality_presentation.py`
- `tests/test_why_orthogonality.py`
- `tests/test_why_orthogonality_presentation.py`
- `scripts/check_cp149_why_orthogonality.zsh`
- `scripts/render_cp149_why_orthogonality.zsh`
- `CHECKPOINT_149.md`

## Install

From the repository root:

```zsh
unzip -q ~/Downloads/seeing_linear_algebra_cp149.zip -d /tmp/seeing_linear_algebra_cp149
zsh /tmp/seeing_linear_algebra_cp149/apply_checkpoint_149.zsh
```

The installer rejects unrelated repository changes but permits replacement of
CP149 files so a revised CP149 package can be applied before commit.

## Check

```zsh
zsh scripts/check_cp149_why_orthogonality.zsh
```

## Preview render

```zsh
zsh scripts/render_cp149_why_orthogonality.zsh -pql
```

Do not commit until the low-quality render has been visually approved.

## Visual review

- Banner, yellow lesson title, central geometry, and explanatory text occupy
  separate vertical zones.
- The determinant bridge reads as continuity rather than a repeated determinant
  lesson.
- The skew/perpendicular comparison is visually obvious without using the
  dot-product criterion.
- The same target vector is recognizable in both decompositions.
- Right-angle marking is readable and does not collide with arrows or labels.
- No prose approaches the frame edges.
- Final question has generous margins and a deliberate hold.
