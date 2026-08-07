# Checkpoint 136 — From Permutations to the 3x3 Formula

## Goal

Derive the familiar six-term 3x3 determinant formula directly from the six permutations introduced in CP135.

## Mathematical focus

For a 3x3 matrix, each valid determinant product:

- selects exactly one entry from each row,
- selects exactly one entry from each column,
- therefore corresponds to a permutation of the columns.

The six permutations split into three even permutations and three odd permutations. Their signed products give

\[
\det(A)=
 a_{11}a_{22}a_{33}
+a_{12}a_{23}a_{31}
+a_{13}a_{21}a_{32}
-a_{11}a_{23}a_{32}
-a_{12}a_{21}a_{33}
-a_{13}a_{22}a_{31}.
\]

## Presentation structure

1. **From a permutation to a product**
   - Symbolic 3x3 matrix.
   - One-entry-per-row and one-entry-per-column rule.
   - Example permutation `(2,3,1)` producing `a12 a23 a31`.

2. **Even permutations**
   - Three balanced cards, one for each positive permutation product.
   - Assemble the positive sum.

3. **Odd permutations**
   - Three balanced cards, one for each negative permutation product.
   - Assemble the negative sum.

4. **Assemble the six terms**
   - Positive group.
   - Negative group.
   - Familiar six-term 3x3 determinant formula.

## Files added

- `engine/determinant_big_formula_derivation.py`
- `scenes/determinant_big_formula_derivation_presentation.py`
- `tests/test_determinant_big_formula_derivation.py`
- `tests/test_determinant_big_formula_derivation_presentation.py`
- `scripts/check_cp136_big_formula_derivation.zsh`
- `scripts/render_cp136_big_formula_derivation.zsh`

## Validation

Focused tests cover the six selection patterns, parity split, coordinate/product mapping, formula construction, and presentation structure.


## Final-card font refinement

This refinement rebuilds the final blue determinant formula as two separate MathTex lines, each at font size 33, so its displayed font matches the green and red lines above it more faithfully.


## Negative-sign correction

This refinement corrects the negative-permutation displays so the negative products are shown with explicit minus signs on the negative-products card and in the grouped negative sum. The final assembled determinant formula now concatenates the positive and negative grouped strings directly, since the negative string itself carries the minus signs.


## Blue formula font refinement

This refinement increases both lines of the final blue determinant formula from font size 33 to font size 38 so the blue line is visibly the same scale as, or slightly stronger than, the green and red lines above. The final formula is nudged slightly lower to preserve spacing.


## Display-height correction

The previous font-size changes did not visibly match the blue formula to the green and red lines because those lines are enlarged by `scale_to_fit_width(11.0)`. This revision explicitly scales each blue formula line to the actual rendered height of the green positive-sum line. This makes the visible character size match the lines above rather than relying on nominal font-size values.


## Exact blue-line size matching

The final blue formula now reuses copies of the already-scaled green and red formula objects. This guarantees that the positive and negative product strings in blue have exactly the same displayed size as the corresponding green and red lines. The `det(A)=` prefix is separately scaled to the same height and joined to the copied positive terms.
