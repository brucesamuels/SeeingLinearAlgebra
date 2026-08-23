# Checkpoint 191 — Changing Between Two Nonstandard Bases

- Keeps one geometric vector fixed while the B-grid moves explicitly into the C-grid.
- Changes the coordinate readout from `(3,1)_B` to `(2,1)_C`.
- Derives `T_{C<-B}=P_C^{-1}P_B` through the standard-coordinate bridge.
- Includes a complete numerical transition-matrix calculation and reconstruction check.
- The preview script disables Manim caching.

Revision 2 avoids zsh's special `path` parameter inside the installer and
restores a known command search path before performing installation.

Revision 3 separates matrix row breaks from following fraction commands with
`[3pt]`, preventing the invalid LaTeX sequence `\\\frac`.

Revision 4 replaces every raw `bmatrix` string in the calculation cards with
Manim `Matrix` objects, eliminating LaTeX row-break parsing entirely.

Revision 5 uses text-style `\\tfrac{1}{2}` entries and increases the fraction
matrices' vertical row buffer from the default to `1.15`, preventing row collisions.
