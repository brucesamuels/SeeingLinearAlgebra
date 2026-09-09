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
  questions.forEach((q, i) => {
    const card = el("div", { class: "question-card" });
    card.appendChild(el("h3", {}, [
      document.createTextNode(`${i + 1}. ${q.title}`),
      el("span", { class: "diff-badge", text: diffTitle(q.difficulty) })
    ]));
    for (const line of flattenBlock(q.statement)) {
      if (line.mono) card.appendChild(el("pre", { text: line.text || " " }));
      else card.appendChild(el("p", { text: line.text }));
    }
    if (mode === "teacher") {
      const ansBlock = el("div", { class: "answer-block" });
      ansBlock.appendChild(el("div", { class: "answer-label", text: "Teacher key" }));
      for (const line of flattenBlock(q.answer)) {
        if (line.mono) ansBlock.appendChild(el("pre", { text: line.text || " " }));
        else ansBlock.appendChild(el("p", { text: line.text }));
      }
      card.appendChild(ansBlock);
    }
    content.appendChild(card);
  });
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

// Saves the given filename/blob using the host's normal browser download
// when this page is served normally (e.g. a school opening index.html).
// If it's running inside a Claude Artifact preview instead, direct
// downloads are sandboxed, so it hands the file to that host's own
// save API when available, and falls back quietly otherwise.
async function savePdfBlob(filename, blob) {
  if (typeof window.claude?.use === "function") {
    try {
      const downloads = await window.claude.use("downloads");
      if (downloads) {
        await downloads.save({ filename, data: blob });
        return { via: "claude" };
      }
    } catch (err) {
      return { via: "claude", error: err };
    }
  }
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  return { via: "browser" };
}

async function downloadPdf() {
  if (!currentQuestions.length) generateProblemSet();
  if (!currentQuestions.length) return;
  const mode = getSelectedMode();
  const title = document.getElementById("worksheetTitle").value.trim() || "Linear Algebra Problem Set";
  const topicIds = getSelectedTopicIds();
  const typeIds = getSelectedTypeIds();
  const difficulty = getSelectedDifficulty();
  const dateStr = new Date().toLocaleDateString();
  const subtitle = `${summarizeSelection(topicIds, typeIds, difficulty)} - Generated ${dateStr}`;
  const doc = buildPdf(currentQuestions, {
    title: mode === "teacher" ? `${title} -- Teacher Answer Key` : title,
    subtitle,
    mode
  });
  const filenameBase = title.replace(/[^a-z0-9]+/gi, "_").replace(/^_+|_+$/g, "") || "linear_algebra_problem_set";
  const filename = `${filenameBase}_${mode}.pdf`;
  const statusHint = document.getElementById("statusHint");
  const result = await savePdfBlob(filename, doc.output("blob"));
  if (result.error) {
    statusHint.textContent = result.error.code === "declined" ? "PDF save cancelled." : "Couldn't save the PDF here.";
  } else {
    statusHint.textContent = "";
  }
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
