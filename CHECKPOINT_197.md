# Checkpoint 197 — Change of Basis Preview Assembly

This checkpoint creates the opening title card and assembles the low-quality Change of Basis chapter preview.

## Lesson order

1. Why Change Basis
2. Coordinates Relative to a Basis
3. Coordinates as Linear-Combination Recipes
4. The Basis Matrix
5. Standard to Basis Coordinates
6. Changing Between Two Nonstandard Bases
7. Matrix of a Transformation in Another Basis
8. Changing a Transformation Between Two Bases
9. Why a Good Basis Matters
10. One Object, Many Descriptions

The title card precedes these ten lessons. No chapter number is assigned.

## Build behavior

The render script renders the new title card at low quality, finds the newest `480p15` render for every lesson, and concatenates them in the order above. If any clip is missing, it reports the missing scene instead of assembling an incomplete chapter.

## Commands

```zsh
zsh scripts/check_cp197_change_of_basis_preview.zsh
zsh scripts/render_cp197_change_of_basis_preview.zsh
```

Output:

```text
media/change_of_basis_preview.mp4
```

