# Checkpoint 148 — Assemble Chapter 5: Determinants

## Goal

Assemble the completed determinant lessons into one reviewable Chapter 5 video.

This checkpoint adds:

- a chapter opening title card,
- an explicit ordered manifest of all determinant lesson videos,
- a robust assembly script that locates the newest render for every scene,
- an ffmpeg concat/re-encode step that produces one chapter MP4,
- focused tests for chapter order and assembly behavior.

## Chapter order

1. Chapter 5 title card
2. Why Do We Need Determinants?
3. Determinant as Area Scale Factor
4. Determinant Sign and Orientation
5. Geometric Derivation of the 2 x 2 Formula
6. Determinant as Signed Area and Volume Scaling
7. Foundational Determinant Properties
8. Derived Determinant Consequences
9. Determinants of Products
10. Determinant of a Transpose
11. Determinants and Elimination
12. The Big Formula
13. From Permutations to the 3 x 3 Formula
14. Cofactor Expansion
15. Using Cofactor Expansion Efficiently
16. Triangular and Block-Triangular Matrices
17. Determinant and Invertibility
18. Cramer's Rule
19. The Adjugate and the Inverse Formula
20. Determinants and Change of Variables / Jacobian Preview
21. Determinant Chapter Synthesis

The revised conceptual arc is:

**geometry -> properties -> algebraic rules -> computation -> structure/applications**

## Assembly strategy

The assembly script renders only the new title card, then uses the newest existing MP4 for every already-approved lesson. It re-encodes the concatenated result with H.264 instead of using stream-copy concatenation, which is more robust if individual previews have small codec/container differences.

The assembled review file is written to:

`media/chapter_five_determinants/Chapter5_Determinants_Assembly.mp4`

## Review before final-quality chapter

The first assembly is for chapter-level review. Check:

- title card readability and duration,
- lesson ordering,
- abrupt or awkward transitions,
- repeated opening language,
- pacing across the chapter as a whole,
- any remaining visual collisions visible only in continuous playback,
- whether the Jacobian preview feels appropriately placed before the synthesis,
- whether the final synthesis provides a satisfying chapter close.

Only after the assembled preview is approved should a final-quality chapter render/assembly be produced.


## R2 — revised ordering and final-resolution workflow

The first full chapter assembly was intentionally a preview built from the newest approved lesson renders. R2 keeps that fast review workflow, but adds a separate final-HD step.

After the revised ordering is visually approved, run:

`scripts/finalize_cp148_determinant_chapter_hd.zsh`

This rerenders every chapter scene with Manim `-qh` (1080p60), then assembles only files from the `1080p60` render directories. This prevents low-resolution preview renders from being mixed into the final chapter.

Final output:

`media/chapter_five_determinants/Chapter5_Determinants_Final_1080p.mp4`


## R3 — computational-section banner consistency

The full-chapter preview exposed one remaining presentation inconsistency: the
CP134 elimination lesson still displayed the banner **Properties of Matrices**.

R3 changes that banner to **Methods of Computation**, matching the Big Formula,
cofactor-expansion, efficiency, and triangular-matrix lessons that now form the
same computational section.

No mathematics, animation timing, or lesson order changes in R3. The installer
also replaces any stale determinant-elimination test assertion that explicitly
expects the former banner.


## R4 — elimination section heading corrected

The assembled preview showed that the CP134 elimination scene still carried
**Properties of the determinant** into the card beginning
**Using elimination to compute the determinant**.

R4 makes the transition to the computational section explicit. Beginning with
that elimination-computation portion, the heading is standardized as:

**Computing the determinant**

The installer also removes stale variants of the old heading from CP134 and
updates any determinant-elimination tests that still assert those older labels.


## R5 — eliminate stale rendered CP134 banner

The preview at approximately 6:43–7:23 still showed **Properties of the Determinant**.
The source patch alone was not enough because the preview assembler intentionally
reused the newest existing lesson render, which was still the older CP134 MP4.

R5 corrects the CP134 section banner to **Methods of Computation** and, during
preview assembly, explicitly rerenders `DeterminantEliminationPresentation`
before concatenation. This guarantees that the rebuilt chapter uses the corrected
banner instead of the stale preview render.


## R6 — direct CP134 source correction

The persistent banner was traced to the actual CP134 source:

`scenes/determinant_elimination_presentation.py`

which still contained:

`banner = Text("Properties of the Determinant", font_size=38)`

R6 rebuilds the installer cleanly, directly replaces that exact source string
with **Methods of Computation**, updates stale elimination-specific tests, and
verifies the corrected source before installation can complete.

The preview assembler also rerenders CP134 before concatenation, so the chapter
cannot reuse the stale 480p15 elimination render.


## R7 — remove stale package-only installer assertion

The R6 repository verification correctly patched and rerendered CP134, but one
focused test still attempted to read `apply_checkpoint_148.zsh` from the
repository root. That installer exists only in the downloaded checkpoint
package and is not copied into the repository.

R7 removes that stale assertion and replaces it with a repository-level test of
the installed banner patch script itself. There are no visual, mathematical,
ordering, or rendering changes in R7.
