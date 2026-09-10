/* Helpers that turn Frac matrices/vectors into real KaTeX-typeset LaTeX
   (rendered via renderMathInElement -- see js/mathify.js and js/app.js)
   instead of hand-aligned ASCII brackets. Each still returns an array of
   lines (now always length 1) so callers that build up multi-matrix blocks
   with `.flat()` and monoLines() keep working unchanged. */

function matToTex(M) {
  return "\\begin{bmatrix} " + M.map(row => row.map(x => x.toString()).join(" & ")).join(" \\\\ ") + " \\end{bmatrix}";
}

function matrixRows(M) {
  return [`\\(${matToTex(M)}\\)`];
}

function labeledMatrix(label, M) {
  return [`${label} = \\(${matToTex(M)}\\)`];
}

function colVectorRows(v) {
  return matrixRows(v.map(x => [x]));
}

function labeledColVector(label, v) {
  return labeledMatrix(label, v.map(x => [x]));
}

function tupleStr(v) {
  return "(" + v.map(x => x.toString()).join(", ") + ")";
}

function sideBySide(blockA, blockB, gap = "    ") {
  const h = Math.max(blockA.length, blockB.length);
  const wa = Math.max(...blockA.map(l => l.length));
  const out = [];
  for (let i = 0; i < h; i++) {
    const a = (blockA[i] || "").padEnd(wa, " ");
    const b = blockB[i] || "";
    out.push(a + gap + b);
  }
  return out;
}

// A "line" in a question is either plain prose (wrapped normally) or a
// preformatted monospace block (rendered verbatim, e.g. a matrix).
function textLine(s) { return { kind: "text", text: s }; }
function monoLines(lines) { return { kind: "mono", text: lines.join("\n") }; }
