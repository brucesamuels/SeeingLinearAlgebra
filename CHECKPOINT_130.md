# Checkpoint 130 - Determinant Sign and Orientation

## Purpose

Separate the determinant's magnitude from its sign. CP129 established that absolute determinant is the area scale factor. CP130 compares two transformations with the same area scale but opposite signs.

## Narrative

The ordered basis pair `(e1, e2)` provides the reference orientation. Two maps are compared:

| Matrix | Determinant | Area scale | Orientation |
|---|---:|---:|---|
| `[[2,1],[0,1]]` | `+2` | `2` | preserved |
| `[[2,1],[0,-1]]` | `-2` | `2` | reversed |

The lesson concludes that determinant magnitude records area change while determinant sign records orientation.

## Files

- `engine/determinant_orientation.py`
- `scenes/determinant_orientation_presentation.py`
- `tests/test_determinant_orientation.py`
- `tests/test_determinant_orientation_presentation.py`
- `scripts/check_cp130_determinant_orientation.zsh`
- `scripts/render_cp130_determinant_orientation.zsh`
- `CHECKPOINT_130.md`

## Check

```zsh
zsh scripts/check_cp130_determinant_orientation.zsh
```

## Render

```zsh
zsh scripts/render_cp130_determinant_orientation.zsh -pql
```

## Visual review

- The positive and negative examples have visibly equal area magnitude.
- The direction marker clearly reverses.
- The original square does not persist behind transformed regions.
- Matrix, captions, and determinant labels do not collide.
- The final statement remains within margins.

Do not commit until the preview is visually approved.
