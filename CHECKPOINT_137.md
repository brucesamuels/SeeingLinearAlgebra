# Checkpoint 137 - Cofactor Expansion

## Purpose

CP137 introduces cofactor (Laplace) expansion as a direct reorganization of the six-term 3x3 determinant formula developed in CP136.

## Mathematical narrative

1. Recall the six permutation terms from CP136.
2. Group the terms according to the first-row entries `a_11`, `a_12`, and `a_13`.
3. Recognize each parenthesized pair as a 2x2 determinant.
4. Interpret those 2x2 determinants as minors obtained by deleting the selected entry's row and column.
5. Introduce the checkerboard sign pattern and the cofactor definition `C_ij = (-1)^(i+j) M_ij`.
6. Rewrite the first-row expansion as `det(A) = a_11 C_11 + a_12 C_12 + a_13 C_13`.
7. Generalize cofactor expansion to any row or any column.

## Key message

**Cofactor expansion is not a new determinant formula. It is the Big Formula reorganized so that lower-dimensional determinants appear naturally.**

## Files

- `engine/determinant_cofactor_expansion.py`
- `scenes/determinant_cofactor_expansion_presentation.py`
- `tests/test_determinant_cofactor_expansion.py`
- `tests/test_determinant_cofactor_expansion_presentation.py`
- `scripts/check_cp137_cofactor_expansion.zsh`
- `scripts/render_cp137_cofactor_expansion.zsh`


## Import-path fix

The CP137 check and render scripts now explicitly change to the repository root and export that root on `PYTHONPATH`. This ensures imports such as `from engine.determinant_cofactor_expansion import ...` resolve when Manim loads the scene file directly.


## Minor/sign refinement

This refinement explicitly defines the term **minor** as the determinant obtained by deleting row $i$ and column $j$, and it adds an explicit statement that the negative signs in cofactor expansion come from the factor $(-1)^{i+j}$, which is inherited from the permutation signs in the Big Formula.


## Layout refinement R4

This refinement makes the green and red determinant terms on the opening CP136 bridge card display at the same size by matching the red line height to the green line height. It also enlarges the added minor/sign explanation text, shortens the wording, splits the sign explanation into two readable lines, and shifts the checkerboard/definition layout leftward so the right edge no longer feels crowded.


## Manim 0.20.1 compatibility refinement R5

The R4 layout goal is preserved, but the unsupported `scale_to_match_height` call has been replaced by the Manim-0.20.1-compatible expression `line2.scale(line1.height / line2.height)`. This gives the red CP136 bridge line the same displayed height as the green line without relying on a nonexistent Mobject method.


## Layout refinement R6

This refinement removes explicit references to CP136 from the student-facing narration on the opening card. It now begins simply with the six-term determinant formula. The opening green and red formula lines are equalized by matching their heights, and then both are scaled down together whenever needed so neither line overruns the screen. The render script now disables caching so visual changes are reliably visible in preview renders.


## Opening formula size refinement R7

The opening green and red determinant lines now start at the same explicit MathTex font size and, if needed, are reduced by one shared scale factor. The earlier height-based scaling has been removed because MathTex bounding-box height did not correspond reliably to perceived font size and could make the red line much larger. This keeps both lines visually matched and inside the frame.
