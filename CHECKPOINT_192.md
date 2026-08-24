# Checkpoint 192 — Matrix of a Transformation in Another Basis

- Distinguishes a genuine transformation of a vector from a coordinate change.
- Derives `[A]_B=P_B^{-1}AP_B` through a right-to-left coordinate pipeline.
- Computes a complete numerical example without raw LaTeX matrix environments.
- Verifies the same input/output pair in standard and B-coordinates.
- Uses structural `Matrix` objects with generous row spacing and disables render caching.

Revision 2 adds a second geometry card: the standard grid moves explicitly into
the B-grid while the geometric input and output arrows remain fixed. Their labels
change from `(3,2)_E -> (6,2)_E` to `(1,2)_B -> (4,2)_B`.
