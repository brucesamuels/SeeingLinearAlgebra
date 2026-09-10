# Linear Algebra Problem Set Generator

A self-contained, client-side web app that generates randomized linear
algebra problem sets (with real typeset math and PDF worksheets / answer
keys) for the Seeing Linear Algebra course.

## Opening it

There is no build step and no server required. Either:

- Double-click `index.html` to open it directly in a browser, or
- Serve the folder with any static file server, e.g. `python3 -m http.server`
  from inside `problem_generator/`, then visit `http://localhost:8000`.

## Designed to survive school network filters

Every dependency this app needs ships **inside this folder** -- there are
no `<script src="https://...">` references to any CDN, font host, or API,
anywhere in the app:

- `vendor/katex.min.js`, `vendor/katex-auto-render.min.js`, and
  `vendor/katex.min.css` are a local copy of KaTeX (MIT licensed), used to
  typeset matrices, vectors, and other math notation. `katex.min.css` has
  every font it needs inlined as base64 data URIs, so there's no separate
  font-file request either.
- PDF export uses the browser's own print-to-PDF flow (no vendored PDF
  library needed) -- click **Print / Save as PDF** and choose "Save as
  PDF" in the print dialog.
- All problem generation and rendering logic is plain local JavaScript.

Because nothing is fetched over the network at runtime, a school's web
filter or CDN blocklist (which commonly blocks `cdnjs.cloudflare.com`,
`unpkg.com`, `cdn.jsdelivr.net`, etc.) has nothing to block. The page also
keeps working with no internet connection at all once it has loaded once
(or if it's opened from a local folder / USB drive).

## What it covers

The Units & Topics list (`data/curriculum.js`) mirrors this repository's
own course checkpoints (`CHECKPOINT_1.md` through `CHECKPOINT_239.md`),
which document the full Brooklyn Technical High School Linear Algebra
sequence -- a Strang-style "Introduction to Linear Algebra" course. No
separate syllabus or textbook file was available to build this from, so
the curriculum was derived directly from the project's own chapter
checkpoints. If you have an official syllabus you'd like the topic list
matched to more closely, update `data/curriculum.js` (or ask for it to be
regenerated from that document).

Nine units, ~50 topics total:

1. Vectors & Vector Spaces
2. Linear Transformations & Matrix Algebra
3. Determinants
4. Orthogonality & Least Squares
5. Eigenvalues & Eigenvectors
6. Change of Basis
7. Positive Definite Matrices
8. Singular Value Decomposition
9. Graphs, Networks & Markov Chains

## How problems are generated

Two complementary sources, mixed by `js/engine.js`:

- **Computational generators** (`js/generators.js`) build fresh random
  problem instances with exact fraction arithmetic (`js/math.js` -- no
  floating-point rounding), so answers are always clean. Difficulty
  (Foundational / Standard / Challenge) scales matrix size and number
  ranges.
- **A curated question bank** (`js/questionBank.js`) of true/false,
  multiple-choice, justify/prove, and applied questions, used for
  conceptual understanding and for topics (like the SVD or positive
  definite matrices) where a fully general numeric generator would
  obscure the idea rather than illuminate it.

The engine never leaves a selection empty: if a requested topic + type +
difficulty combination has nothing available, it automatically widens
(first on difficulty, then on type) rather than silently dropping a
question.

## Using the app

1. Pick Units/Topics (checkbox tree, with select-all/clear-all).
2. Pick question type(s): Computation, Conceptual, Multiple choice,
   Justify/prove, Applied.
3. Pick difficulty: Foundational, Standard, Challenge, or Mixed.
4. Pick the number of questions.
5. Toggle **Student worksheet** vs **Teacher answer key**.
6. Click **Generate problem set** to preview it on the page, then
   **Print / Save as PDF** to save a print-ready PDF (blank work space and
   no answers in student mode; full worked solutions in teacher mode) --
   choose "Save as PDF" in your browser's print dialog.

Regenerating with the same options produces a new random problem set each
time (it is not deterministic across generations).
