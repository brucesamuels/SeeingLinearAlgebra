/* Client-side PDF generation using the locally vendored jsPDF build
   (vendor/jspdf.umd.min.js) -- no network request of any kind. */

function buildPdf(questions, opts) {
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF({ unit: "pt", format: "letter" });
  const pageW = doc.internal.pageSize.getWidth();
  const pageH = doc.internal.pageSize.getHeight();
  const margin = 54;
  const maxWidth = pageW - margin * 2;
  const lineH = 14;
  let y = margin;

  function ensureSpace(h) {
    if (y + h > pageH - margin) { doc.addPage(); y = margin; }
  }
  function addText(text, { bold = false, size = 11, indent = 0, color = 0 } = {}) {
    doc.setFont("helvetica", bold ? "bold" : "normal");
    doc.setFontSize(size);
    doc.setTextColor(color);
    const wrapped = doc.splitTextToSize(text, maxWidth - indent);
    for (const w of wrapped) {
      ensureSpace(lineH);
      doc.text(w, margin + indent, y);
      y += lineH;
    }
  }
  function addMono(text, indent = 18) {
    doc.setFont("courier", "normal");
    doc.setFontSize(10);
    doc.setTextColor(0);
    ensureSpace(lineH);
    doc.text(text, margin + indent, y);
    y += lineH;
  }
  function rule(color = 220) {
    doc.setDrawColor(color);
    doc.line(margin, y, pageW - margin, y);
    y += 14;
  }

  addText(opts.title, { bold: true, size: 16 });
  y += 2;
  addText(opts.subtitle, { size: 10, color: 90 });
  y += 4;
  if (opts.mode === "student") {
    addText("Name: _______________________________________        Date: ______________", { size: 11 });
  } else {
    addText("TEACHER ANSWER KEY", { bold: true, size: 12, color: 150 });
  }
  y += 6;
  rule(150);

  questions.forEach((q, i) => {
    ensureSpace(lineH * 2);
    addText(`${i + 1}. ${q.title}  (${diffLabel(q.difficulty)})`, { bold: true, size: 12 });
    for (const l of flattenBlock(q.statement)) {
      if (l.mono) addMono(l.text); else addText(l.text, { indent: 14 });
    }
    if (opts.mode === "student") {
      y += 40;
      ensureSpace(0);
    } else {
      y += 4;
      addText("Answer:", { bold: true, size: 11, indent: 14, color: 30 });
      for (const l of flattenBlock(q.answer)) {
        if (l.mono) addMono(l.text, 32); else addText(l.text, { indent: 28, color: 30 });
      }
    }
    y += 10;
    rule(225);
  });

  const totalPages = doc.internal.getNumberOfPages();
  for (let p = 1; p <= totalPages; p++) {
    doc.setPage(p);
    doc.setFont("helvetica", "normal");
    doc.setFontSize(9);
    doc.setTextColor(140);
    doc.text(`Page ${p} of ${totalPages}`, pageW / 2, pageH - 24, { align: "center" });
    doc.text("Seeing Linear Algebra -- Problem Set Generator", margin, pageH - 24);
  }
  return doc;
}

function diffLabel(d) {
  const m = DIFFICULTIES.find(x => x.id === d);
  return m ? m.title : "Standard";
}
