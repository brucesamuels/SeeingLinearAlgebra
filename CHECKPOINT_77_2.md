# Checkpoint 77.2 — Keep the Echelon Matrix Fixed to the Screen

## Goal
Prevent the displayed echelon matrix \(R\) from being projected and rotated by the 3D camera.

## What changed
- Registered `echelon_tex` with `add_fixed_in_frame_mobjects` before revealing it.
- Preserved the CP77.1 text-collision fix.
- Added a presentation test that requires the echelon matrix to be fixed in frame.

## Files updated
- `scenes/row_space_presentation.py`
- `tests/test_row_space_presentation.py`
- `CHECKPOINT_77_2.md`
