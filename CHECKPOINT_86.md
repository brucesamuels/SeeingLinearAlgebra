# Checkpoint 86 — Linearity Preserves Linear Combinations

CP86 synthesizes CP84 and CP85.

The lesson compares two routes:

\[
T(a\mathbf u+b\mathbf v)
\]

and

\[
aT(\mathbf u)+bT(\mathbf v).
\]

## Visual sequence

1. Draw \(\mathbf u\) and \(\mathbf v\).
2. Scale them to \(a\mathbf u\) and \(b\mathbf v\).
3. Add them to form \(a\mathbf u+b\mathbf v\).
4. Transform the completed linear combination.
5. Retain the transformed result and clear the first construction.
6. Redraw and transform \(\mathbf u\) and \(\mathbf v\) separately.
7. Scale the images to \(aT(\mathbf u)\) and \(bT(\mathbf v)\).
8. Add the scaled images.
9. Show that both endpoints coincide.

The final card connects:

\[
T(c\mathbf v)=cT(\mathbf v)
\]

and

\[
T(\mathbf u+\mathbf v)
=
T(\mathbf u)+T(\mathbf v)
\]

to the full linearity statement:

\[
T(a\mathbf u+b\mathbf v)
=
aT(\mathbf u)+bT(\mathbf v).
\]

## Check

```zsh
./scripts/check_cp86_linearity_preserves_linear_combinations.zsh
```

## Render

```zsh
./scripts/render_cp86_linearity_preserves_linear_combinations.zsh
```
