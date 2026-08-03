# Checkpoint 96 — Matrix Addition and Subtraction

## Chapter role

This checkpoint begins the **Matrix Operations** chapter.

The lesson intentionally precedes CP94. It establishes that addition and
subtraction are **entrywise operations requiring equal dimensions**, preparing
students to contrast them with the different compatibility rule used in matrix
multiplication.

## Storyboard

1. Ask when two matrices can be added.
2. Establish the equal-dimensions requirement.
3. Animate a 2×2 addition example by pairing corresponding entries.
4. State the general entrywise rule:
   \[
   (A+B)_{ij}=a_{ij}+b_{ij}.
   \]
5. Rewrite subtraction as \(A-B=A+(-B)\).
6. Demonstrate negating every entry before adding.
7. Show why a 2×3 matrix and a 3×2 matrix cannot be added.
8. Summarize familiar algebraic properties.
9. Pause-and-Predict calculation.
10. Reflection and bridge to scalar multiplication.

## Files

- `engine/matrix_addition_subtraction.py`
- `scenes/matrix_addition_subtraction_presentation.py`
- `tests/test_matrix_addition_subtraction.py`
- `tests/test_matrix_addition_subtraction_presentation.py`
- `scripts/check_cp96_matrix_addition_subtraction.zsh`
- `scripts/render_cp96_matrix_addition_subtraction.zsh`
- `apply_checkpoint_96.zsh`

## Installation

From the repository root:

```zsh
chmod +x ~/Downloads/seeing_linear_algebra_cp96/apply_checkpoint_96.zsh
~/Downloads/seeing_linear_algebra_cp96/apply_checkpoint_96.zsh
```

Safari may already have extracted the ZIP into `~/Downloads`.

## Check

```zsh
./scripts/check_cp96_matrix_addition_subtraction.zsh
```

## Render

```zsh
./scripts/render_cp96_matrix_addition_subtraction.zsh
```

Do not commit until the render has been reviewed and approved.
