/**
 * Client-side PDF generation for the generated problem set, using jsPDF
 * (loaded from the vendor CDN script in index.html). Runs entirely in the
 * browser -- no problem data is sent anywhere.
 */

function generateWorksheetPdf(problems, options) {
  const { isTeacher } = options;
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF({ unit: "pt", format: "letter" });

  const pageWidth = doc.internal.pageSize.getWidth();
  const pageHeight = doc.internal.pageSize.getHeight();
  const margin = 54;
  const contentWidth = pageWidth - margin * 2;
  let y = margin;

  function ensureSpace(neededHeight) {
    if (y + neededHeight > pageHeight - margin) {
      doc.addPage();
      y = margin;
    }
  }

  function writeLines(lines, { fontSize = 11, lineGap = 4, indent = 0, style = "normal" } = {}) {
    doc.setFont("helvetica", style);
    doc.setFontSize(fontSize);
    const lineHeight = fontSize + lineGap;
    lines.forEach((line) => {
      ensureSpace(lineHeight);
      doc.text(line, margin + indent, y);
      y += lineHeight;
    });
  }

  function writeWrapped(text, { fontSize = 11, lineGap = 4, indent = 0, style = "normal" } = {}) {
    doc.setFont("helvetica", style);
    doc.setFontSize(fontSize);
    const wrapped = doc.splitTextToSize(text, contentWidth - indent);
    writeLines(wrapped, { fontSize, lineGap, indent, style });
  }

  // Title
  doc.setFont("helvetica", "bold");
  doc.setFontSize(16);
  ensureSpace(24);
  doc.text(`AP Precalculus Practice Problem Set${isTeacher ? " -- Teacher Answer Key" : ""}`, margin, y);
  y += 22;

  doc.setFont("helvetica", "normal");
  doc.setFontSize(10);
  doc.setTextColor(90, 90, 90);
  ensureSpace(14);
  doc.text(`${problems.length} questions  |  generated ${new Date().toLocaleDateString()}`, margin, y);
  y += 18;
  doc.setTextColor(0, 0, 0);

  if (!isTeacher) {
    ensureSpace(20);
    doc.setFontSize(10);
    doc.text("Name: _______________________________", margin, y);
    doc.text("Date: _______________", margin + 300, y);
    y += 24;
  } else {
    y += 6;
  }

  doc.setDrawColor(180, 180, 180);
  doc.line(margin, y, pageWidth - margin, y);
  y += 18;

  const letters = ["A", "B", "C", "D"];
  const diffLabel = { 1: "Easy", 2: "Medium", 3: "Hard" };

  problems.forEach((p, idx) => {
    ensureSpace(30);
    const typeLabel = p.type === "mc" ? "Multiple Choice" : "Free Response";
    const tag = `[${p.topicId} - ${diffLabel[p.difficulty] || ""} - ${typeLabel}]`;

    writeWrapped(`${idx + 1}. ${p.prompt}`, { fontSize: 11, style: "normal" });
    writeWrapped(tag, { fontSize: 8, style: "italic", indent: 14 });
    y += 2;

    if (p.type === "mc") {
      p.choices.forEach((c, i) => {
        const prefix = `${letters[i]}. `;
        const isCorrect = isTeacher && i === p.correctIndex;
        writeWrapped(`${prefix}${c}`, {
          fontSize: 10.5,
          indent: 18,
          style: isCorrect ? "bold" : "normal",
        });
      });
    } else {
      ensureSpace(46);
      doc.setDrawColor(210, 210, 210);
      doc.rect(margin + 14, y, contentWidth - 14, 40);
      y += 50;
    }

    if (isTeacher) {
      ensureSpace(18);
      const answerText = p.type === "mc" ? `Answer: ${letters[p.correctIndex]}. ${p.answer}` : `Answer: ${p.answer}`;
      writeWrapped(answerText, { fontSize: 10.5, style: "bold", indent: 14 });
      if (p.solution && p.solution.length) {
        p.solution.forEach((step, i) => {
          writeWrapped(`${i + 1}. ${step}`, { fontSize: 9.5, indent: 24, style: "normal" });
        });
      }
    }

    y += 10;
    ensureSpace(1);
    doc.setDrawColor(225, 225, 225);
    doc.line(margin, y, pageWidth - margin, y);
    y += 12;
  });

  const pageCount = doc.internal.getNumberOfPages();
  for (let i = 1; i <= pageCount; i++) {
    doc.setPage(i);
    doc.setFont("helvetica", "normal");
    doc.setFontSize(8.5);
    doc.setTextColor(140, 140, 140);
    doc.text(`Page ${i} of ${pageCount}`, pageWidth - margin, pageHeight - 24, { align: "right" });
  }

  const fileSuffix = isTeacher ? "answer-key" : "student";
  const dateStr = new Date().toISOString().slice(0, 10);
  doc.save(`ap-precalc-problem-set-${fileSuffix}-${dateStr}.pdf`);
}
