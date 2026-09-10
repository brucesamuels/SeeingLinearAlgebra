/* Selection engine: turns a user's (units/topics, question types, difficulty,
   count) choice into a concrete, randomized problem set, mixing exact
   computational generators with the curated conceptual/MC/justify/applied
   question bank. No selection combination is ever a dead end: if a
   requested topic+type+difficulty has nothing available, the engine widens
   the search (difficulty, then type) rather than silently skipping it. */

function findTopicMeta(topicId) {
  for (const unit of CURRICULUM) {
    const topic = unit.topics.find(t => t.id === topicId);
    if (topic) return { unitId: unit.id, unitTitle: unit.title, topicTitle: topic.title };
  }
  return { unitId: null, unitTitle: "", topicTitle: topicId };
}

function bankQuestionToStandard(q, rng) {
  const meta = findTopicMeta(q.topicId);
  const statement = [textLine(q.prompt)];
  if (q.type === "multiplechoice" && q.choices) {
    const letters = "ABCD";
    q.choices.forEach((c, i) => statement.push(textLine(`   ${letters[i]}. ${c}`)));
  }
  const answer = [];
  if (q.type === "multiplechoice" && q.choices) {
    const idx = q.choices.indexOf(q.answer);
    answer.push(textLine(`Answer: ${"ABCD"[idx]}. ${q.answer}`));
  } else {
    answer.push(textLine(`Answer: ${q.answer}`));
  }
  if (q.explanation) answer.push(textLine(q.explanation));
  return {
    unitId: q.unitId, topicId: q.topicId, type: q.type, difficulty: q.difficulty,
    title: meta.topicTitle, statement, answer
  };
}

function pickQuestionForTopic(rng, topicId, allowedTypes, difficulty, usedBankItems) {
  const wantsComputation = allowedTypes.includes("computation");
  const nonCompTypes = allowedTypes.filter(t => t !== "computation");

  // Bank items matching the requested type(s), further narrowed to the
  // requested difficulty when possible. A generator can always hit the
  // exact difficulty, so we only offer bank items as an option here when
  // they *also* match the requested difficulty -- otherwise a mismatched
  // bank item could get picked over an exact-difficulty computation.
  const byType = QUESTION_BANK.filter(q => q.topicId === topicId && nonCompTypes.includes(q.type) && !usedBankItems.has(q));
  let bankCandidates = difficulty === "mixed" ? byType : byType.filter(q => q.difficulty === difficulty);

  const options = [];
  if (wantsComputation && GENERATORS[topicId]) options.push("computation");
  if (bankCandidates.length) options.push("bank");

  let widened = false;
  if (options.length === 0) {
    widened = true;
    // Widen, in order: same type ignoring difficulty; any type/difficulty for this topic; computation.
    if (byType.length) { bankCandidates = byType; options.push("bank"); }
    else if (wantsComputation && GENERATORS[topicId]) options.push("computation");
    else {
      const anyBank = QUESTION_BANK.filter(q => q.topicId === topicId && !usedBankItems.has(q));
      if (anyBank.length) { bankCandidates = anyBank; options.push("bank"); }
      else if (GENERATORS[topicId]) options.push("computation");
      else { bankCandidates = QUESTION_BANK.filter(q => q.topicId === topicId); options.push("bank"); }
    }
  }

  const choice = pick(rng, options);
  let question;
  if (choice === "computation") {
    const diffToUse = difficulty === "mixed" ? randInt(rng, 1, 3) : difficulty;
    question = GENERATORS[topicId](rng, diffToUse);
    question.difficulty = diffToUse;
  } else {
    const q = pick(rng, bankCandidates);
    usedBankItems.add(q);
    question = bankQuestionToStandard(q, rng);
  }
  question.widened = widened;
  return question;
}

// options = { topicIds: string[], typeIds: string[], difficulty: 1|2|3|"mixed", count: number, seed?: number }
function buildProblemSet(options) {
  const rng = makeRng(options.seed ?? Math.floor(Math.random() * 1e9));
  const topicIds = options.topicIds.length ? options.topicIds : CURRICULUM.flatMap(u => u.topics.map(t => t.id));
  const allowedTypes = options.typeIds.length ? options.typeIds : QUESTION_TYPES.map(t => t.id);
  const usedBankItems = new Set();
  const questions = [];
  // Cycle through the selected topics round-robin (shuffled) so a problem
  // set with multiple topics doesn't cluster all its questions on one topic.
  let order = shuffle(rng, topicIds);
  let idx = 0;
  for (let i = 0; i < options.count; i++) {
    if (idx >= order.length) { order = shuffle(rng, topicIds); idx = 0; }
    const topicId = order[idx++];
    questions.push(pickQuestionForTopic(rng, topicId, allowedTypes, options.difficulty, usedBankItems));
  }
  return questions;
}

// Flattens a Question's statement/answer blocks into plain render lines:
// { mono: boolean, text: string }[]
function flattenBlock(block) {
  const lines = [];
  for (const item of block) {
    if (item.kind === "mono") {
      for (const l of item.text.split("\n")) lines.push({ mono: true, text: mathify(l) });
    } else {
      lines.push({ mono: false, text: mathify(item.text) });
    }
  }
  return lines;
}
