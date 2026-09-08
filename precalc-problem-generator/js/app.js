/**
 * UI wiring: builds the unit/topic tree, reads settings, generates a
 * problem set, renders it (student or teacher view), and drives the
 * client-side PDF export.
 */

(function () {
  const unitTopicTree = document.getElementById("unitTopicTree");
  const selectAllBtn = document.getElementById("selectAllTopics");
  const clearAllBtn = document.getElementById("clearAllTopics");
  const numQuestionsInput = document.getElementById("numQuestions");
  const questionTypeSelect = document.getElementById("questionType");
  const difficultySelect = document.getElementById("difficulty");
  const generateBtn = document.getElementById("generateBtn");
  const downloadPdfBtn = document.getElementById("downloadPdfBtn");
  const statusMsg = document.getElementById("statusMsg");
  const worksheetEl = document.getElementById("worksheet");

  let currentProblems = [];
  let currentMeta = null;

  /* -------------------------- build topic tree -------------------------- */

  CURRICULUM.forEach((unit) => {
    const group = document.createElement("div");
    group.className = "unit-group";

    const header = document.createElement("label");
    header.className = "unit-group-header";
    const unitCheckbox = document.createElement("input");
    unitCheckbox.type = "checkbox";
    unitCheckbox.dataset.unitId = unit.id;
    unitCheckbox.checked = true;
    const headerText = document.createElement("span");
    headerText.textContent = unit.title;
    header.appendChild(unitCheckbox);
    header.appendChild(headerText);
    group.appendChild(header);

    const list = document.createElement("ul");
    list.className = "topic-list";
    unit.topics.forEach((topic) => {
      const li = document.createElement("li");
      const label = document.createElement("label");
      const cb = document.createElement("input");
      cb.type = "checkbox";
      cb.dataset.topicId = topic.id;
      cb.dataset.unitId = unit.id;
      cb.checked = true;
      const span = document.createElement("span");
      span.textContent = `${topic.id} ${topic.title}`;
      label.appendChild(cb);
      label.appendChild(span);
      li.appendChild(label);
      list.appendChild(li);

      cb.addEventListener("change", () => syncUnitCheckbox(unit.id));
    });
    group.appendChild(list);
    unitTopicTree.appendChild(group);

    unitCheckbox.addEventListener("change", () => {
      list.querySelectorAll('input[type="checkbox"]').forEach((cb) => {
        cb.checked = unitCheckbox.checked;
      });
    });
  });

  function syncUnitCheckbox(unitId) {
    const unitCb = unitTopicTree.querySelector(`input[data-unit-id="${unitId}"]:not([data-topic-id])`);
    const topicCbs = Array.from(unitTopicTree.querySelectorAll(`input[data-topic-id][data-unit-id="${unitId}"]`));
    const checkedCount = topicCbs.filter((cb) => cb.checked).length;
    unitCb.checked = checkedCount === topicCbs.length;
    unitCb.indeterminate = checkedCount > 0 && checkedCount < topicCbs.length;
  }

  selectAllBtn.addEventListener("click", () => {
    unitTopicTree.querySelectorAll('input[type="checkbox"]').forEach((cb) => {
      cb.checked = true;
      cb.indeterminate = false;
    });
  });
  clearAllBtn.addEventListener("click", () => {
    unitTopicTree.querySelectorAll('input[type="checkbox"]').forEach((cb) => {
      cb.checked = false;
      cb.indeterminate = false;
    });
  });

  function getSelectedTopicIds() {
    return Array.from(unitTopicTree.querySelectorAll("input[data-topic-id]"))
      .filter((cb) => cb.checked)
      .map((cb) => cb.dataset.topicId);
  }

  /* ------------------------------ generation ------------------------------ */

  function resolveDifficulty(setting) {
    if (setting === "mixed") return randInt(1, 3);
    return parseInt(setting, 10);
  }

  function setStatus(message, isError) {
    statusMsg.textContent = message;
    statusMsg.classList.toggle("error", !!isError);
  }

  generateBtn.addEventListener("click", () => {
    const topicIds = getSelectedTopicIds();
    if (topicIds.length === 0) {
      setStatus("Select at least one topic before generating a problem set.", true);
      return;
    }
    let count = parseInt(numQuestionsInput.value, 10);
    if (!Number.isFinite(count) || count < 1) count = 1;
    if (count > 60) count = 60;
    numQuestionsInput.value = count;

    const questionTypeSetting = questionTypeSelect.value;
    const difficultySetting = difficultySelect.value;

    const problems = [];
    for (let i = 0; i < count; i++) {
      const topicId = topicIds[i % topicIds.length];
      const difficulty = resolveDifficulty(difficultySetting);
      try {
        const problem = generateProblem(topicId, difficulty, questionTypeSetting);
        problem.difficulty = difficulty;
        problems.push(problem);
      } catch (err) {
        console.error(err);
      }
    }

    if (problems.length === 0) {
      setStatus("Could not generate any problems for the current selection.", true);
      return;
    }

    currentProblems = problems;
    currentMeta = {
      questionTypeSetting,
      difficultySetting,
      generatedAt: new Date(),
    };

    renderWorksheet();
    downloadPdfBtn.disabled = false;
    setStatus(`Generated ${problems.length} question${problems.length === 1 ? "" : "s"}.`, false);
  });

  document.querySelectorAll('input[name="viewMode"]').forEach((radio) => {
    radio.addEventListener("change", () => {
      if (currentProblems.length > 0) renderWorksheet();
    });
  });

  function getViewMode() {
    return document.querySelector('input[name="viewMode"]:checked').value;
  }

  const DIFFICULTY_LABEL = { 1: "Easy", 2: "Medium", 3: "Hard" };

  function renderWorksheet() {
    const isTeacher = getViewMode() === "teacher";
    worksheetEl.innerHTML = "";

    const header = document.createElement("div");
    header.className = "worksheet-header";
    header.innerHTML = `
      <h2>AP Precalculus Practice Problem Set${isTeacher ? '<span class="answer-key-badge">Teacher Answer Key</span>' : ""}</h2>
      <div class="meta">${currentProblems.length} questions &middot; ${new Date().toLocaleDateString()}</div>
      ${
        isTeacher
          ? ""
          : `<div class="name-line"><span>Name:</span><span>Date:</span><span>Period:</span></div>`
      }
    `;
    worksheetEl.appendChild(header);

    currentProblems.forEach((p, idx) => {
      const div = document.createElement("div");
      div.className = "problem";

      const typeLabel = p.type === "mc" ? "Multiple Choice" : "Free Response";
      const diffLabel = DIFFICULTY_LABEL[p.difficulty] || "";

      const promptEl = document.createElement("p");
      promptEl.className = "problem-prompt";
      const numSpan = document.createElement("span");
      numSpan.className = "problem-number";
      numSpan.textContent = `${idx + 1}.`;
      promptEl.appendChild(numSpan);
      promptEl.appendChild(document.createTextNode(p.prompt));
      const tag = document.createElement("span");
      tag.className = "problem-tag";
      tag.textContent = `${p.topicId} · ${diffLabel} · ${typeLabel}`;
      promptEl.appendChild(tag);
      div.appendChild(promptEl);

      if (p.type === "mc") {
        const ul = document.createElement("ul");
        ul.className = "problem-choices";
        const letters = ["A", "B", "C", "D"];
        p.choices.forEach((choiceText, i) => {
          const li = document.createElement("li");
          if (isTeacher && i === p.correctIndex) li.classList.add("correct-choice");
          li.textContent = `${letters[i]}. ${choiceText}`;
          ul.appendChild(li);
        });
        div.appendChild(ul);
      } else {
        const space = document.createElement("div");
        space.className = "fr-answer-space";
        div.appendChild(space);
      }

      if (isTeacher) {
        const answerBlock = document.createElement("div");
        answerBlock.className = "answer-block";
        const letters = ["A", "B", "C", "D"];
        const answerLine = document.createElement("div");
        answerLine.innerHTML = `<strong>Answer:</strong> ${p.type === "mc" ? `${letters[p.correctIndex]}. ${p.answer}` : p.answer}`;
        answerBlock.appendChild(answerLine);
        if (p.solution && p.solution.length) {
          const ol = document.createElement("ol");
          ol.className = "solution-steps";
          p.solution.forEach((step) => {
            const li = document.createElement("li");
            li.textContent = step;
            ol.appendChild(li);
          });
          answerBlock.appendChild(ol);
        }
        div.appendChild(answerBlock);
      }

      worksheetEl.appendChild(div);
    });
  }

  downloadPdfBtn.addEventListener("click", () => {
    if (currentProblems.length === 0) return;
    if (!window.jspdf) {
      setStatus("PDF library failed to load. Check your internet connection and reload the page.", true);
      return;
    }
    try {
      const isTeacher = getViewMode() === "teacher";
      generateWorksheetPdf(currentProblems, { isTeacher });
      setStatus("PDF downloaded.", false);
    } catch (err) {
      console.error(err);
      setStatus("PDF generation failed. See console for details.", true);
    }
  });
})();
