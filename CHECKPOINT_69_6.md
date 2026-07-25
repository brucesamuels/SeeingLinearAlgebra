# Checkpoint 69.6 — Correct Text Staging and Final Layout

## Goal
Preserve the approved 3D camera reveal from CP69.5 while correcting two text-presentation problems.

## Corrections
- Fixed-in-frame text objects now begin fully hidden before being registered with the 3D scene.
- Each title, prompt, readout, discovery statement, definition, and key idea appears only when its animation calls for it.
- The final span definition and key idea now occupy separate bottom rows.
- The definition font is slightly reduced and placed lower.
- The key idea is placed higher with independent edge spacing rather than being attached with `next_to`.

## Preserved
- One-line trace.
- Parallel-line sweep.
- Dense endpoint field.
- Solid span plane.
- Full-field 3D camera tilt without a third axis.
- Renderer-independent mathematics and thin adapters.

## Files updated
- `scenes/two_vector_span_presentation.py`
- `tests/test_two_vector_span_presentation.py`
- `CHECKPOINT_69_6.md`
