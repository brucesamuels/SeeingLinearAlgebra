/* Helpers that turn Frac matrices/vectors into aligned monospace text blocks
   so the same content can be dropped into the HTML preview (<pre>) and into
   the PDF (courier font) without any custom bracket-drawing code. */

function matrixRows(M) {
  const strs = M.map(row => row.map(x => x.toString()));
  const width = Math.max(1, ...strs.flat().map(s => s.length));
  return strs.map(r => "[ " + r.map(s => s.padStart(width)).join("  ") + " ]");
}

function labeledMatrix(label, M) {
  const rows = matrixRows(M);
  const prefix = `${label} = `;
  const pad = " ".repeat(prefix.length);
  return rows.map((r, i) => (i === 0 ? prefix : pad) + r);
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
