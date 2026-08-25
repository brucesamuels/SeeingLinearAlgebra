# Checkpoint 194 — Changing a Transformation Between Two Bases

- Starts with a transformation matrix already expressed in a nonstandard basis B.
- Changes it directly into basis C without using the standard basis as an operational stage.
- Animates the entire B-grid into the C-grid while the geometric input and output vectors remain fixed.
- Constructs the transition matrix conceptually from the linear combinations
  `b_1 = c_1` and `b_2 = -c_1 + c_2`.
- Identifies the columns of `Q_(C<-B)` as `[b_1]_C` and `[b_2]_C`.
- Derives the coordinate-conversion rule by substituting those linear combinations
  into `v = x b_1 + y b_2`.
- Derives `P_C Q_(C<-B) = P_B` before solving for `Q_(C<-B)`.
- Derives `[T]_C = Q_(C<-B) [T]_B Q_(B<-C)` and its similarity form.
- Explains why transition matrices in opposite directions are inverses.
- Introduces the efficient rule `[new basis | old basis] -> [I | old-to-new transition]`.
- Animates all three row operations that compute `Q_(C<-B)` for the lesson bases.
- Uses the same bases and transition matrix introduced in Checkpoint 191.
- Includes a complete numerical verification in both coordinate languages.
- Uses structural Manim `Matrix` objects and disables preview caching.
