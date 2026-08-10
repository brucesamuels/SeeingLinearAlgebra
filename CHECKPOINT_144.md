# Checkpoint 144 — Determinant of a Transpose

## Central theorem

For every square matrix,
\[
\det(A^T)=\det(A).
\]

## Proof strategy

This lesson gives an explicit proof from the Big Formula.

### Step 1: start from the permutation formula
\[
\det(A)=\sum_{\sigma\in S_n}\operatorname{sgn}(\sigma)\prod_{i=1}^n a_{i,\sigma(i)}.
\]

### Step 2: apply it to the transpose
\[
\det(A^T)=\sum_{\sigma\in S_n}\operatorname{sgn}(\sigma)\prod_{i=1}^n (A^T)_{i,\sigma(i)}
=\sum_{\sigma\in S_n}\operatorname{sgn}(\sigma)\prod_{i=1}^n a_{\sigma(i),i}.
\]

### Step 3: rewrite the product
\[
\prod_{i=1}^n a_{\sigma(i),i}=\prod_{j=1}^n a_{j,\sigma^{-1}(j)}.
\]
This is only a renaming of indices.

### Step 4: reindex the sum by the inverse permutation
Let \(\tau=\sigma^{-1}\). Then
\[
\det(A^T)=\sum_{\tau\in S_n}\operatorname{sgn}(\tau^{-1})\prod_{j=1}^n a_{j,\tau(j)}.
\]
Since inverse permutations have the same parity,
\[
\operatorname{sgn}(\tau^{-1})=\operatorname{sgn}(\tau).
\]

### Step 5: recognize the Big Formula again
So
\[
\det(A^T)=\sum_{\tau\in S_n}\operatorname{sgn}(\tau)\prod_{j=1}^n a_{j,\tau(j)}=\det(A).
\]

## Pedagogical takeaway

This proof explains why transposing does not affect the determinant and why determinant statements about rows have matching statements about columns.

## Files

- `engine/determinant_transpose_rule.py`
- `scenes/determinant_transpose_rule_presentation.py`
- `tests/test_determinant_transpose_rule.py`
- `tests/test_determinant_transpose_rule_presentation.py`
- `tests/test_cp144_scripts.py`
- `scripts/check_cp144_transpose_rule.zsh`
- `scripts/render_cp144_transpose_rule.zsh`


## Layout refinement R2

This refinement reduces collisions across the transpose-rule lesson by shrinking the heaviest displayed formulas, moving titles slightly higher, and lowering the main equation groups on the most crowded cards. In particular, the cards for applying the formula to $A^T$, rewriting the product, reindexing the sum, and recognizing the Big Formula again all use smaller equation sizes and narrower fit widths. The opening theorem card and closing takeaway also use slightly smaller green theorem lines for better balance.


## Layout refinement R3

This refinement specifically addresses the middle proof cards where large equations were colliding with smaller explainer text. Cards 3 through 6 now use smaller displayed equations, and their explainer notes are pushed farther down so the mathematical lines and the prose occupy clearly separated vertical zones. In contrast, the final takeaway card restores a larger theorem statement because that is the one place where emphasis through size is pedagogically helpful.


## Layout refinement R4

This refinement responds to detailed timestamped feedback on the middle and concluding cards. On card 3, the displayed formulas are raised slightly and the small explanatory note is pushed farther down to create a clearer gap. On card 5, the full reindexed sum is lowered so it no longer collides with the title. On card 6, the key sign-invariance equation is enlarged for emphasis. On card 7, the concluding formula stack is lowered and the heading is slightly reduced so the title no longer runs into the top formula.

## Layout refinement R5

This refinement switches from incremental nudging to explicit vertical-zone layout rules on the crowded proof cards. Card 3 uses a true MathTex heading so \(A^T\) renders as a superscript; the title, equations, and explanatory line are placed in separate upper, central, and lower bands. Card 5 reserves a higher title band for "Reindex the sum" and moves the entire equation stack lower. Card 6 enlarges the sign-invariance equation substantially. Card 7 moves its heading higher and the formula stack lower so the two cannot overlap. The final theorem card retains the largest displayed statement.


## Layout refinement R6

This refinement raises the two remaining crowded headings identified after the R5 redesign. On card 5, the heading "Reindex the sum" is moved higher for better separation from the reindexed formula stack. On card 7, the heading "Now recognize the Big Formula again" is also moved higher so it clears the first displayed equation more comfortably. The mathematical content and overall card structure are unchanged.


## Layout refinement R7

This refinement raises the heading on card 7, "Now recognize the Big Formula again," even further so it clears the displayed formula stack more comfortably. No mathematical or structural changes are made elsewhere in the lesson.
