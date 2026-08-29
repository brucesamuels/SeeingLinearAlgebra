/*
 * app.js — wires the controls, the Units & Topics dropdown, worksheet
 * rendering, the student/teacher toggle, and client-side PDF generation
 * (via the browser's native print-to-PDF) for the AP Calculus generator.
 */

const DIFFICULTY_LABELS = { 1: 'Easy', 2: 'Medium', 3: 'Hard' };

function unitsForCourse(course) {
  return AP_CALC_CURRICULUM.filter((u) => (course === 'ab' ? u.course !== 'bc' : true));
}

function buildTopicsPanel(course) {
  const unitListEl = document.getElementById('unitList');
  unitListEl.innerHTML = '';

  for (const unit of unitsForCourse(course)) {
    const block = document.createElement('div');
    block.className = 'unit-block';

    const header = document.createElement('div');
    header.className = 'unit-block-header';
    const unitCb = document.createElement('input');
    unitCb.type = 'checkbox';
    unitCb.checked = true;
    unitCb.id = `unit-${unit.unit}`;
    const unitLabel = document.createElement('label');
    unitLabel.htmlFor = unitCb.id;
    unitLabel.textContent = `Unit ${unit.unit}: ${unit.name}`;
    header.append(unitCb, unitLabel);
    block.appendChild(header);

    const topicEls = [];
    for (const topic of unit.topics) {
      const row = document.createElement('div');
      row.className = 'topic-row';
      const cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.checked = true;
      cb.dataset.topic = topic.code;
      cb.id = `topic-${topic.code}`;
      const label = document.createElement('label');
      label.htmlFor = cb.id;
      label.innerHTML = `<span class="topic-code">${topic.code}</span>${topic.name}`;
      row.append(cb, label);
      block.appendChild(row);
      topicEls.push(cb);
      cb.addEventListener('change', () => {
        unitCb.checked = topicEls.every((t) => t.checked);
        unitCb.indeterminate = !unitCb.checked && topicEls.some((t) => t.checked);
        updateTopicsSummary();
      });
    }
    unitCb.addEventListener('change', () => {
      topicEls.forEach((t) => { t.checked = unitCb.checked; });
      unitCb.indeterminate = false;
      updateTopicsSummary();
    });
    unitListEl.appendChild(block);
  }
  updateTopicsSummary();
}

function updateTopicsSummary() {
  const all = Array.from(document.querySelectorAll('#unitList input[data-topic]'));
  const selected = all.filter((cb) => cb.checked);
  const el = document.getElementById('topicsSummary');
  if (selected.length === all.length) el.textContent = 'All units & topics';
  else if (selected.length === 0) el.textContent = 'No topics selected';
  else el.textContent = `${selected.length} of ${all.length} topics selected`;
}

function getSelectedTopics() {
  return Array.from(document.querySelectorAll('#unitList input[data-topic]:checked')).map((cb) => cb.dataset.topic);
}

/* ---- Dropdown open/close ---- */

function initDropdown() {
  const dropdown = document.getElementById('topicsDropdown');
  const toggle = document.getElementById('topicsToggle');
  const panel = document.getElementById('topicsPanel');
  toggle.addEventListener('click', (e) => {
    e.stopPropagation();
    const willOpen = panel.hidden;
    panel.hidden = !willOpen;
    toggle.setAttribute('aria-expanded', String(willOpen));
  });
  document.addEventListener('click', (e) => {
    if (!dropdown.contains(e.target)) {
      panel.hidden = true;
      toggle.setAttribute('aria-expanded', 'false');
    }
  });
  document.getElementById('selectAllBtn').addEventListener('click', () => {
    document.querySelectorAll('#unitList input[type=checkbox]').forEach((cb) => { cb.checked = true; cb.indeterminate = false; });
    updateTopicsSummary();
  });
  document.getElementById('clearAllBtn').addEventListener('click', () => {
    document.querySelectorAll('#unitList input[type=checkbox]').forEach((cb) => { cb.checked = false; cb.indeterminate = false; });
    updateTopicsSummary();
  });
}

/* ---- Generation ---- */

function pickDifficulty(setting) {
  return setting === 'mixed' ? randInt(1, 3) : parseInt(setting, 10);
}
function pickType(setting) {
  return setting === 'mixed' ? (Math.random() < 0.5 ? 'mc' : 'frq') : setting;
}

function generateSet() {
  const settings = {
    course: document.getElementById('courseSelect').value,
    count: parseInt(document.getElementById('countSelect').value, 10),
    type: document.getElementById('typeSelect').value,
    difficulty: document.getElementById('difficultySelect').value,
  };

  let topics = getSelectedTopics();
  if (topics.length === 0) {
    topics = unitsForCourse(settings.course).flatMap((u) => u.topics.map((t) => t.code));
  }

  const problems = [];
  let guard = 0;
  while (problems.length < settings.count && guard < settings.count * 20) {
    guard++;
    const topicCode = choice(topics);
    const difficulty = pickDifficulty(settings.difficulty);
    const p = generateProblem(topicCode, difficulty);
    if (!p) continue;
    const wantMc = pickType(settings.type) === 'mc';
    p.kind = wantMc && p.wrongHTML && p.wrongHTML.length >= 3 ? 'mc' : 'frq';
    problems.push(p);
  }
  renderWorksheet(problems, settings);
}

function renderProblem(p, index) {
  const letters = ['A', 'B', 'C', 'D'];
  let bodyHTML;
  if (p.kind === 'mc') {
    const options = shuffle([{ html: p.answerHTML, correct: true }, ...p.wrongHTML.slice(0, 3).map((h) => ({ html: h, correct: false }))]);
    bodyHTML = `<div class="choices">${options.map((o, i) => `<div class="choice${o.correct ? ' is-correct' : ''}"><span class="choice-key">${letters[i]}.</span><span class="choice-text">${o.html}</span></div>`).join('')}</div>`;
  } else {
    bodyHTML = `<div class="frq-lines"><div class="line"></div><div class="line"></div><div class="line"></div></div>`;
  }
  const answerBlock = `<div class="answer-block">
      <div class="answer-line">Answer: ${p.answerHTML}</div>
      <ol>${p.solution.map((s) => `<li>${s}</li>`).join('')}</ol>
    </div>`;
  return `<article class="problem">
      <div class="problem-head">
        <span class="qnum">${index + 1}.</span>
        <span class="meta">Unit ${p.unit} (${p.topic}) • ${p.topicName} • ${DIFFICULTY_LABELS[p.difficulty] || 'Mixed'} • ${p.kind === 'mc' ? 'Multiple Choice' : 'Free Response'}</span>
      </div>
      <div class="prompt">${p.stem}</div>
      ${bodyHTML}
      ${answerBlock}
    </article>`;
}

function renderWorksheet(problems, settings) {
  const list = document.getElementById('problemList');
  if (problems.length === 0) {
    list.innerHTML = '<p class="empty-state">No problems could be generated for the selected options. Try selecting more units or topics.</p>';
    document.getElementById('worksheetMeta').textContent = '';
    return;
  }
  list.innerHTML = problems.map((p, i) => renderProblem(p, i)).join('');
  document.getElementById('worksheetTitle').textContent = settings.course === 'bc' ? 'AP Calculus BC Problem Set' : 'AP Calculus AB Problem Set';
  const diffText = settings.difficulty === 'mixed' ? 'Mixed difficulty' : DIFFICULTY_LABELS[parseInt(settings.difficulty, 10)];
  const typeText = { mixed: 'Mixed (MC + FRQ)', mc: 'Multiple Choice', frq: 'Free Response' }[settings.type];
  document.getElementById('worksheetMeta').textContent = `${problems.length} questions • ${diffText} • ${typeText} • Generated ${new Date().toLocaleDateString()}`;
}

/* ---- View toggle (student / teacher) ---- */

function initViewToggle() {
  const toggle = document.getElementById('viewToggle');
  const worksheet = document.getElementById('worksheet');
  const studentLabel = document.getElementById('viewLabelStudent');
  const teacherLabel = document.getElementById('viewLabelTeacher');
  studentLabel.classList.add('active');
  toggle.addEventListener('click', () => {
    const next = toggle.getAttribute('aria-checked') !== 'true';
    toggle.setAttribute('aria-checked', String(next));
    worksheet.classList.toggle('teacher-mode', next);
    studentLabel.classList.toggle('active', !next);
    teacherLabel.classList.toggle('active', next);
  });
}

/* ---- Init ---- */

document.addEventListener('DOMContentLoaded', () => {
  buildTopicsPanel(document.getElementById('courseSelect').value);
  initDropdown();
  initViewToggle();

  document.getElementById('courseSelect').addEventListener('change', (e) => buildTopicsPanel(e.target.value));
  document.getElementById('generateBtn').addEventListener('click', generateSet);
  document.getElementById('printBtn').addEventListener('click', () => window.print());

  generateSet();
});
