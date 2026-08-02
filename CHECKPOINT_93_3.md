# Checkpoint 93.3 — Single Matrix Assembly and Longer Hold

The assembled display now uses one genuine 2 by 2 `Matrix` object rather than
two independently bracketed column matrices inside another pair of brackets.

This removes the matrix collision around 23 seconds.

The symbolic screen now holds for 4.0 seconds, and the stale CP93.1 layout
assertion has been replaced with tests for the current CP93.3 structure.
