# AP Precalculus Problem Set Generator

A self-contained, client-side web app that generates randomized AP
Precalculus practice problem sets covering Units 1&ndash;4 of the College
Board AP Precalculus Course and Exam Description.

## Usage

Open `index.html` in a browser (double-click it, or serve the folder with
any static file server). No build step, server, or install is required.

1. Choose units/topics from the tree on the left (select all, clear all, or
   pick individual topics/units).
2. Set the number of questions, question type (multiple choice, free
   response, or mixed), and difficulty (Easy/Medium/Hard/Mixed).
3. Toggle between **Student version** (blank answer spaces) and **Teacher
   answer key** (answers + worked solutions, correct choice highlighted).
4. Click **Generate Problem Set** to preview it on the page.
5. Click **Download PDF** to export the currently previewed version
   (student or teacher) as a PDF, generated entirely in the browser via
   [jsPDF](https://github.com/parallax/jsPDF) &mdash; no problem data is sent
   to a server.

## Structure

- `index.html` &mdash; page layout and script includes
- `css/styles.css` &mdash; styling (screen + print)
- `js/curriculum.js` &mdash; AP Precalculus unit/topic list and topic-to-generator mapping
- `js/generators.js` &mdash; randomized problem generators (one per topic family), with difficulty scaling and both MC/free-response output
- `js/app.js` &mdash; UI wiring: topic tree, settings, rendering
- `js/pdf.js` &mdash; client-side PDF export via jsPDF

## Notes

- Math notation is written in plain ASCII (e.g. `x^2`, `sqrt(x)`, `pi`,
  `theta`) rather than Unicode math symbols, since the PDF export uses
  jsPDF's built-in fonts, which only support a Latin-1/WinAnsi character
  set.
- jsPDF is loaded from a CDN (cdnjs) in `index.html`; an internet
  connection is required the first time the page loads for PDF export to
  work.
