/* UI wiring for the Problem Set Generator. No network calls anywhere in
   this file (or anywhere in this app) -- everything runs from local
   scripts loaded by index.html, so it keeps working even when a school
   network blocks external CDNs. */

let currentQuestions = [];

function el(tag, attrs = {}, children = []) {
  const e = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (k === "text") e.textContent = v;
    else if (k === "html") e.innerHTML = v;
    else e.setAttribute(k, v);
  }
  for (const c of children) e.appendChild(c);
  return e;
}

function buildUnitTree() {
  const container = document.getElementById("unitTree");
  container.innerHTML = "";
  for (const unit of CURRICULUM) {
    const details = el("details", { class: "unit-group", open: "" });
    const summary = el("summary", { text: unit.title });
    details.appendChild(summary);
    for (const topic of unit.topics) {
      const input = el("input", { type: "checkbox", value: topic.id, "data-unit": unit.id });
      input.checked = true;
      const label = el("label", { class: "topic-item" }, [input, document.createTextNode(topic.title)]);
      details.appendChild(label);
    }
    container.appendChild(details);
  }
}

function buildTypeChecks() {
  const container = document.getElementById("typeChecks");
  container.innerHTML = "";
  for (const t of QUESTION_TYPES) {
    const input = el("input", { type: "checkbox", value: t.id, name: "qtype" });
    input.checked = true;
    const label = el("label", {}, [input, document.createTextNode(t.title)]);
    container.appendChild(label);
  }
}

function buildDifficultyRadios() {
  const container = document.getElementById("difficultyRadios");
  container.innerHTML = "";
  const options = [{ id: "mixed", title: "Mixed" }, ...DIFFICULTIES];
  options.forEach((d, i) => {
    const input = el("input", { type: "radio", name: "difficulty", value: String(d.id) });
    if (d.id === 2) input.checked = true;
    const label = el("label", {}, [input, document.createTextNode(d.title)]);
    container.appendChild(label);
  });
}

function getSelectedTopicIds() {
  return Array.from(document.querySelectorAll('#unitTree input[type="checkbox"]:checked')).map(i => i.value);
}
function getSelectedTypeIds() {
  return Array.from(document.querySelectorAll('#typeChecks input[type="checkbox"]:checked')).map(i => i.value);
}
function getSelectedDifficulty() {
  const checked = document.querySelector('input[name="difficulty"]:checked');
  const v = checked ? checked.value : "2";
  return v === "mixed" ? "mixed" : Number(v);
}
function getSelectedMode() {
  return document.querySelector('input[name="mode"]:checked').value;
}

function diffTitle(d) {
  if (d === "mixed") return "Mixed";
  const m = DIFFICULTIES.find(x => x.id === d);
  return m ? m.title : String(d);
}

function renderPreview(questions, mode) {
  const content = document.getElementById("previewContent");
  content.innerHTML = "";
  if (!questions.length) {
    content.appendChild(el("p", { class: "empty-state", text: "No questions matched your selection." }));
    return;
  }
  const title = document.getElementById("worksheetTitle").value.trim() || "Linear Algebra Problem Set";
  const header = el("div", { class: "sheet-header" });
  header.appendChild(el("h2", { class: "sheet-title", text: mode === "teacher" ? `${title} \u2014 Teacher Answer Key` : title }));
  header.appendChild(el("div", { class: "sheet-meta", text: `${questions.length} question${questions.length === 1 ? "" : "s"} \u00b7 Generated ${new Date().toLocaleDateString()}` }));
  if (mode === "student") {
    const fields = el("div", { class: "sheet-fields" });
    fields.appendChild(el("span", { text: "Name: " + "_".repeat(28) }));
    fields.appendChild(el("span", { text: "Date: " + "_".repeat(14) }));
    header.appendChild(fields);
  }
  content.appendChild(header);
  questions.forEach((q, i) => {
    const card = el("div", { class: "question-card" });
    card.appendChild(el("h3", {}, [
      document.createTextNode(`${i + 1}. ${q.title}`),
      el("span", { class: "diff-badge", text: diffTitle(q.difficulty) })
    ]));
    for (const line of flattenBlock(q.statement)) {
      card.appendChild(el("p", { class: line.mono ? "mathline" : "", text: line.text || " " }));
    }
    if (mode === "teacher") {
      const ansBlock = el("div", { class: "answer-block" });
      ansBlock.appendChild(el("div", { class: "answer-label", text: "Teacher key" }));
      for (const line of flattenBlock(q.answer)) {
        ansBlock.appendChild(el("p", { class: line.mono ? "mathline" : "", text: line.text || " " }));
      }
      card.appendChild(ansBlock);
    }
    content.appendChild(card);
  });
  if (window.renderMathInElement) {
    window.renderMathInElement(content, {
      delimiters: [{ left: "\\(", right: "\\)", display: false }],
      throwOnError: false,
    });
  }
}

function summarizeSelection(topicIds, typeIds, difficulty) {
  const totalTopics = CURRICULUM.reduce((s, u) => s + u.topics.length, 0);
  const unitsTouched = new Set();
  for (const id of topicIds) { const m = findTopicMeta(id); if (m.unitId) unitsTouched.add(m.unitId); }
  const typeNames = typeIds.length === QUESTION_TYPES.length ? "all types" : typeIds.map(t => QUESTION_TYPES.find(q => q.id === t)?.title).join(", ");
  return `${topicIds.length}/${totalTopics} topics across ${unitsTouched.size} unit(s) - ${typeNames} - ${diffTitle(difficulty)} difficulty`;
}

function generateProblemSet() {
  const topicIds = getSelectedTopicIds();
  const typeIds = getSelectedTypeIds();
  const difficulty = getSelectedDifficulty();
  const countInput = document.getElementById("questionCount");
  let count = parseInt(countInput.value, 10);
  if (!Number.isFinite(count) || count < 1) count = 1;
  if (count > 50) count = 50;
  countInput.value = count;

  const statusHint = document.getElementById("statusHint");
  if (!topicIds.length) {
    statusHint.textContent = "Select at least one topic first.";
    return;
  }
  if (!typeIds.length) {
    statusHint.textContent = "Select at least one question type first.";
    return;
  }
  statusHint.textContent = "";

  currentQuestions = buildProblemSet({ topicIds, typeIds, difficulty, count });
  const mode = getSelectedMode();
  renderPreview(currentQuestions, mode);
  document.getElementById("previewMeta").textContent = summarizeSelection(topicIds, typeIds, difficulty);
  document.getElementById("downloadBtn").disabled = false;
}

// Opens the browser's own print dialog -- with real KaTeX-typeset math on
// screen, printing (then choosing "Save as PDF" in the dialog) produces a
// PDF with real vector text that matches the on-screen typesetting exactly.
function downloadPdf() {
  if (!currentQuestions.length) generateProblemSet();
  if (!currentQuestions.length) return;
  window.print();
}

function wireEvents() {
  document.getElementById("generateBtn").addEventListener("click", generateProblemSet);
  document.getElementById("downloadBtn").addEventListener("click", downloadPdf);
  document.getElementById("selectAllTopics").addEventListener("click", () => {
    document.querySelectorAll('#unitTree input[type="checkbox"]').forEach(i => i.checked = true);
  });
  document.getElementById("clearAllTopics").addEventListener("click", () => {
    document.querySelectorAll('#unitTree input[type="checkbox"]').forEach(i => i.checked = false);
  });
  document.querySelectorAll('input[name="mode"]').forEach(r => r.addEventListener("change", () => {
    if (currentQuestions.length) renderPreview(currentQuestions, getSelectedMode());
  }));
}

document.addEventListener("DOMContentLoaded", () => {
  buildUnitTree();
  buildTypeChecks();
  buildDifficultyRadios();
  wireEvents();
});
