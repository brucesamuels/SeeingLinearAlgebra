# AP Calculus Problem Set Generator

A standalone, client-side web app that generates randomized AP Calculus
AB/BC problem sets. No build step, no server, no external dependencies —
open `index.html` in a browser (or serve the folder with any static file
server) and it runs entirely on the client.

## Features

- **Units & Topics** — a checkbox dropdown covering AP Calculus AB
  (Units 1–8) and BC (Units 1–10), matching the College Board Course and
  Exam Description numbering. Selecting a unit selects all its topics;
  individual topics can also be picked.
- **Course toggle** — AB hides the BC-only units (Parametric/Polar/Vector
  functions and Infinite Series); BC includes all ten units.
- **Number of questions** — 5 to 30 per set.
- **Question type** — Multiple Choice, Free Response, or Mixed.
- **Difficulty** — Easy / Medium / Hard / Mixed, which scales coefficient
  ranges, degrees, and problem complexity per generator.
- **Student / Teacher toggle** — a switch shows or hides the answer key
  and step-by-step solutions (and highlights the correct multiple-choice
  option) without regenerating the set.
- **PDF generation** — the "Print / Save as PDF" button opens the
  browser's native print dialog with a print-tuned stylesheet (controls
  hidden, page-break-safe problems); choosing "Save as PDF" as the
  destination produces a PDF of whatever is currently on screen —
  student worksheet or teacher answer key, depending on the toggle.

## How problems are generated

Problems come from two layers, both registered in the same `GENERATORS`
array (`topic code -> [generator functions]`); `generateProblem()` picks
uniformly at random among whichever are registered for a topic, so a
topic with more than one generator gets that much more variety per
worksheet.

**Hand-written generators** (`generators.js`, one per topic, 31 total)
each build one fixed function shape (e.g. "quadratic times linear,
product rule") with randomized coefficients. Arithmetic uses an exact
fraction class (`Frac` in `core.js`) and polynomial helpers, so answers
are exact — not rounded — wherever the underlying math is rational.

**Compositional generators** (`compositional.js`, covering topics 2.2,
2.3, 2.4, 3.2, 6.1, 6.3, and 8.1 as *additional* variants alongside the
hand-written ones) are built on a small symbolic-expression engine
(`expr.js`) instead of one fixed shape: a random tree is assembled from
primitives (polynomial terms, sin/cos, e^x, ln, integer powers, possibly
nested — e.g. `sin(e^(3x+1))`), and `diff()` differentiates it exactly by
mechanical rule application, so the answer is correct by construction
for whatever shape gets generated. Integration-flavored problems (6.1,
6.3, 8.1) use the same trick the original u-substitution generator used:
build the *antiderivative* first as a random composed expression, then
differentiate it to get the "given" integrand — this sidesteps needing a
general symbolic integrator while still guaranteeing an exact closed
form exists. Numeric evaluation prefers exact fractions and falls back
to a rounded decimal only when the expression is genuinely transcendental
(matching how the AP exam scores calculator-active items).

The engine's correctness doesn't rest on eyeballing sample output: `diff()`
is checked with property-based testing — thousands of randomly composed
expressions, each differentiated symbolically and cross-checked against a
numerical (finite-difference) derivative of the original — which is how
several real bugs were caught during development (a sign-rendering bug,
a degenerate "terms cancel to zero" case, and an `ln` domain crash at
integer bounds).

Multiple-choice distractors are generated per problem to reflect
plausible errors (sign mistakes, forgetting the chain rule multiplier,
off-by-one exponents, dropping the inner derivative, etc.), not
arbitrary numbers.

## Files

- `index.html` — page structure and controls
- `styles.css` — screen and print styles
- `core.js` — random helpers, exact fraction arithmetic, polynomial
  utilities, HTML formatting
- `expr.js` — the symbolic expression engine (node builders, `diff`,
  `simplify`, HTML rendering, exact/decimal evaluation, random
  expression builders) used by the compositional generators
- `curriculum.js` — the Unit/Topic list shown in the selector
- `generators.js` — the hand-written generators (one per topic) and the
  `GENERATORS` registry / `generateProblem()` lookup
- `compositional.js` — engine-based generator variants, pushed onto the
  same `GENERATORS` registry as extra entries for their topics
- `app.js` — UI wiring: the topics dropdown, generation, rendering, the
  student/teacher toggle, and print/PDF

## Extending

**A hand-written generator** — write a function in `generators.js`
following the existing pattern (return `{ unit, topic, topicName,
difficulty, stem, answerHTML, solution, wrongHTML }`), register it in
the `GENERATORS` array, and add a matching `{ code, name }` entry to the
right unit in `curriculum.js` (skip the last step if adding a variant to
an existing topic).

**A compositional generator** — build an expression with `expr.js`'s
node constructors (`cst`, `X_NODE`, `addN`, `mulN`, `powN`, `divN`,
`sinE`, `cosE`, `expE`, `lnE`) or the random builders (`randomExpr`,
`randomComposedSingle`, `randomAntiderivative`), differentiate with
`diff()`, render with `toHTML()`, and return the same shape as above.
Register it in `compositional.js`'s `GENERATORS.push(...)` call. New
primitives (e.g. `sqrt`) would need `diff`, `simplify`, `evalNum`,
`evalExact`, and `renderNode` cases added in `expr.js`.
