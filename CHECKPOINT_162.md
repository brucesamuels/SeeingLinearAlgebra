# CP162 - Orthogonal Matrices Preserve Geometry

## Summary

This checkpoint begins the post-QR portion of the orthogonality chapter by making the geometry of orthogonal matrices explicit.  The lesson treats the identity

\[
Q^TQ=I
\]

not merely as an algebraic convenience, but as the reason orthogonal matrices preserve Euclidean geometry.

The lesson is built as a visual continuation of the prior arc

\[
\text{orthogonality}
\to
\text{projection}
\to
\text{Gram-Schmidt}
\to
\text{QR}
\to
\text{least squares}.
\]

Now that the chapter has repeatedly used orthonormal columns and the rule \(Q^{-1}=Q^T\), the natural next question is: **what kind of transformation is an orthogonal matrix?**

## Lesson structure

The presentation contains six cards.

1. **Orthonormal columns give an orthogonal matrix**  
   A concrete orthonormal pair \(\mathbf q_1,\mathbf q_2\) is shown on a coordinate grid and unit circle.  The card introduces
   \[
   Q=\begin{bmatrix}
   \tfrac1{\sqrt2} & -\tfrac1{\sqrt2}\\
   \tfrac1{\sqrt2} & \tfrac1{\sqrt2}
   \end{bmatrix},
   \qquad
   Q^TQ=I,
   \qquad
   Q^{-1}=Q^T.
   \]

2. **Lengths are preserved**  
   A vector \(\mathbf v\) and its image \(Q\mathbf v\) are shown on matched grids with equal-radius circles, emphasizing
   \[
   \|Q\mathbf v\|=\|\mathbf v\|.
   \]

3. **Dot products and angles are preserved**  
   Two vectors \(\mathbf u,\mathbf v\) and their images \(Q\mathbf u,Q\mathbf v\) are compared side by side.  Angle markers and numerical dot products reinforce
   \[
   (Q\mathbf u)^T(Q\mathbf v)=\mathbf u^T\mathbf v.
   \]

4. **Rigid motion viewpoint**  
   A unit square and basis vectors are compared with their images under \(Q\).  The card emphasizes that orthogonal matrices do **not** stretch or shear.

5. **Determinant distinguishes rotation from reflection**  
   A rotation example and a reflection example are shown together to separate the two orthogonal possibilities:
   \[
   \det Q = 1 \quad \text{(rotation)},
   \qquad
   \det Q = -1 \quad \text{(reflection)}.
   \]

6. **Closing synthesis**  
   A final theorem-style card states that orthogonal matrices preserve lengths and angles.

## Files included

- `engine/orthogonal_matrices.py`
- `scenes/orthogonal_matrices_presentation.py`
- `tests/test_orthogonal_matrices.py`
- `tests/test_orthogonal_matrices_presentation.py`
- `scripts/check_cp162_orthogonal_matrices.zsh`
- `scripts/render_cp162_orthogonal_matrices.zsh`
- `CHECKPOINT_162.md`
- `apply_checkpoint_162.zsh`

## Validation performed

The checkpoint was validated with:

```zsh
python -m py_compile \
  engine/orthogonal_matrices.py \
  scenes/orthogonal_matrices_presentation.py \
  tests/test_orthogonal_matrices.py \
  tests/test_orthogonal_matrices_presentation.py

PYTHONPATH=. pytest -q \
  tests/test_orthogonal_matrices.py \
  tests/test_orthogonal_matrices_presentation.py
```

## Notes for review

When previewing, please focus especially on:

- whether the side-by-side geometry reads clearly and comfortably,
- whether the transformed vectors are easy to compare with the originals,
- whether the determinant card is visually balanced,
- and whether the lesson feels like a natural continuation of QR and least squares.

If approved, the next likely checkpoint would be a follow-up lesson devoted specifically to **rotations and reflections as orthogonal transformations**.


## r2 layout refinement

- On Cards 2, 3, and 4, lowered the graph panels slightly and repositioned graph labels to clear collisions with the white explanatory heading region.
- Preserved the mathematical content, timing, and equation placement.


## r4 balanced equation columns

- Rebuilt from the known-working r2 scene flow rather than r3.
- Card 2: reduced and shifted the two graph panels left to create a genuine viewer-right equation column.
- Card 3: moved the equation block only modestly downward.
- Card 5: reduced and shifted the reflection panel left so its equations can sit viewer-right while staying within the frame.
- Added a source-level progression test asserting that all six cards remain called in order.
