# Checkpoint 103 — Order, Identity, and Undoing

## Chapter role

This checkpoint is the conceptual capstone of the Matrix Operations chapter.

It follows matrix multiplication as composition, trace, and transposition, and
answers three natural questions:

1. Does order matter?
2. Is there a matrix that changes nothing?
3. Can every transformation be undone?

## Storyboard

1. Compare a shear and reflection in opposite orders.
2. Show that \(BA\mathbf{x}\neq AB\mathbf{x}\).
3. State that matrix multiplication is not commutative in general.
4. Introduce the identity matrix \(I\).
5. Show \(I\mathbf{x}=\mathbf{x}\) and \(IA=AI=A\).
6. Show a shear undone by another shear.
7. Introduce \(A^{-1}A=AA^{-1}=I\).
8. Contrast with a projection that collapses information.
9. Include a Pause-and-Predict prompt about order of action.
10. Defer full inverse theory to the linear-systems chapter.
11. Bridge to Matrix Operations chapter assembly.

## Apply

```zsh
chmod +x ~/Downloads/seeing_linear_algebra_cp103/apply_checkpoint_103.zsh
~/Downloads/seeing_linear_algebra_cp103/apply_checkpoint_103.zsh
```

## Check

```zsh
./scripts/check_cp103_matrix_order_identity_undoing.zsh
```

## Render

```zsh
./scripts/render_cp103_matrix_order_identity_undoing.zsh
```

Do not commit until the render has been reviewed and approved.
