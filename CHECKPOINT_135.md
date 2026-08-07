# Checkpoint 135 — The Big Formula

## Goal

Introduce the permutation formula for determinants and show how the familiar six-term formula for a 3x3 determinant comes from it.

## Mathematical focus

The lesson develops

\[
\det(A)=\sum_{\sigma\in S_n}\operatorname{sgn}(\sigma)\,a_{1\sigma(1)}a_{2\sigma(2)}\cdots a_{n\sigma(n)}.
\]

Key ideas:

- each determinant term chooses exactly one entry from each row,
- and exactly one entry from each column,
- so each term corresponds to a permutation of the columns,
- and the sign is determined by the parity of that permutation.

## Presentation structure

1. **Overview**
   - The determinant is a sum of signed products.
   - For a 3x3 matrix there are 3! = 6 permutation products.

2. **General permutation formula**
   - Present the Big Formula.
   - Show a symbolic 3x3 matrix.
   - Explain row choice, column choice, permutation, and sign.

3. **Six terms for the 3x3 case**
   - Split the six permutations into the three positive and three negative terms.
   - Display them in two columns.

4. **Familiar six-term determinant formula**
   - Group the positive and negative contributions.
   - Present the standard six-term 3x3 formula.

## Files added

- `engine/determinant_big_formula.py`
- `scenes/determinant_big_formula_presentation.py`
- `tests/test_determinant_big_formula.py`
- `tests/test_determinant_big_formula_presentation.py`
- `scripts/check_cp135_big_formula.zsh`
- `scripts/render_cp135_big_formula.zsh`

## Validation

- Focused tests for parity, permutation-term enumeration, grouped formula strings, and scene structure.
- Python compilation of engine, scenes, and tests.


## Layout refinement

This refinement moves the explanatory text on the general-formula card farther to the right and nudges the symbolic matrix farther left so the bullets no longer overlap the matrix. It also enlarges the sigma-equation lines on the positive/negative permutation card for better readability.


## Additional layout refinement

This refinement wraps the long sign-explanation line on the general-formula card so it stays on screen, enlarges the positive/negative permutation lists, and reworks the final blue determinant formula into a two-line display so it can keep the same font size as the positive and negative grouped lines.


## Final-card font refinement

This refinement increases the font size of the final blue determinant formula now that it is split across two lines, making the enlargement visibly apparent on screen.


## R4 final-formula size correction

The final blue determinant formula is now explicitly set to font size 40, a substantial increase from 32, while remaining on two lines. The render script also disables Manim caching so the preview cannot reuse a stale cached scene.


## R5 final formula visual-size correction

The final blue determinant formula is now built as two separate MathTex lines. Each line is explicitly scaled to the same 11.4-unit display width used by the green and red grouped formulas. This controls the actual rendered size rather than relying on a source font-size number.
