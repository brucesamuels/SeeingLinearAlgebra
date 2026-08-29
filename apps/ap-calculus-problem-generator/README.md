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

Every problem is produced by a small, dedicated generator function (see
`generators.js`) rather than pulled from a fixed bank, so numbers and
answers are different each time. Arithmetic uses an exact fraction class
(`Frac` in `core.js`) and polynomial helpers, so answers to algebraic
problems (derivatives, integrals, limits, etc.) are exact — not rounded
approximations — wherever the underlying math is rational. A handful of
generators (population growth/decay) are inherently transcendental and
report a calculator-rounded decimal, matching how those items are scored
on the actual AP exam.

Multiple-choice distractors are generated per problem to reflect
plausible errors (sign mistakes, forgetting the chain rule multiplier,
off-by-one exponents, etc.), not arbitrary numbers.

## Files

- `index.html` — page structure and controls
- `styles.css` — screen and print styles
- `core.js` — random helpers, exact fraction arithmetic, polynomial
  utilities, HTML formatting
- `curriculum.js` — the Unit/Topic list shown in the selector
- `generators.js` — one generator function per topic, plus the registry
  that maps topic codes to generators
- `app.js` — UI wiring: the topics dropdown, generation, rendering, the
  student/teacher toggle, and print/PDF

## Extending

To add a new topic, write a generator function in `generators.js`
following the existing pattern (return `{ unit, topic, topicName,
difficulty, stem, answerHTML, solution, wrongHTML }`), register it in
the `GENERATORS` array, and add the matching `{ code, name }` entry to
the right unit in `curriculum.js`.
