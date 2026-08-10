# Checkpoint 145 — Determinant as Signed Area and Volume Scaling

## Central idea

The determinant measures signed area/volume scaling:
\[
|\det(A)|=\text{area/volume scale factor},
\]
while the sign records orientation.

## Lesson structure

1. A matrix sends the unit square to the parallelogram spanned by its columns.
2. The area of that parallelogram is \(|\det(A)|\).
3. Positive determinant preserves orientation; negative determinant reverses it.
4. Zero determinant collapses area to zero.
5. In three dimensions, the unit cube maps to a parallelepiped with volume \(|\det(A)|\).
6. A singular 3D map flattens the cube to a plane or line, so volume vanishes.
7. The product rule \(\det(AB)=\det(A)\det(B)\) is interpreted geometrically as successive volume scaling.
8. Final synthesis: \(\det(A)\) is the signed volume scale factor of the transformation.

## Visual-layout rule

This checkpoint follows fixed non-overlapping vertical zones. Yellow headings stay in a dedicated upper band, diagrams/equations occupy the central band, and explanatory prose stays in a lower band. The largest formula font is reserved for the final takeaway statement.

## Files

- `engine/determinant_geometry.py`
- `scenes/determinant_geometry_presentation.py`
- `tests/test_determinant_geometry.py`
- `tests/test_determinant_geometry_presentation.py`
- `tests/test_cp145_scripts.py`
- `scripts/check_cp145_determinant_geometry.zsh`
- `scripts/render_cp145_determinant_geometry.zsh`
