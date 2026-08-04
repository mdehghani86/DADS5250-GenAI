const fs = require('fs'), vm = require('vm');
const mods = ["M01","M02","M03","M04","M05","M06","M08","M09","M10","M11","M12","M13"];
const issues = [], codes = [];
const typeCount = {};
for (const m of mods) {
  let q;
  try { const src = fs.readFileSync(`data/${m}_quiz.js`, 'utf8'); const ctx = { window: {} }; vm.runInNewContext(src, ctx); q = ctx.window.QUIZ; }
  catch (e) { issues.push(`${m}: PARSE ERROR ${e.message}`); continue; }
  if (!q || !q.questions) { issues.push(`${m}: no questions`); continue; }
  const qs = q.questions;
  if (qs.length !== 5) issues.push(`${m}: ${qs.length} questions (need 5)`);
  const d = qs.map(x => x.difficulty);
  const de = d.filter(x => x === 'easy').length, dm = d.filter(x => x === 'medium').length, dh = d.filter(x => x === 'hard').length;
  if (de !== 1 || dm !== 3 || dh !== 1) issues.push(`${m}: difficulty ${de}E/${dm}M/${dh}H (need 1/3/1)`);
  const labels = new Set();
  qs.forEach((x, i) => {
    labels.add(x.typeLabel);
    typeCount[x.typeLabel] = (typeCount[x.typeLabel] || 0) + 1;
    if (x.type === 'mc' || x.type === 'multi') {
      if (!x.options || x.options.length < 2) issues.push(`${m} q${i+1}: missing options`);
      else x.options.forEach(o => { if (!o.explanation || !String(o.explanation).trim()) issues.push(`${m} q${i+1} opt ${o.letter}: MISSING explanation`); });
      if (x.type === 'mc' && x.correctIndex == null) issues.push(`${m} q${i+1}: no correctIndex`);
      if (x.type === 'multi' && (!x.correctIndices || !x.correctIndices.length)) issues.push(`${m} q${i+1}: no correctIndices`);
    }
    if ((x.type === 'tf' || x.type === 'fill' || x.type === 'order') && (!x.explanation || !String(x.explanation).trim())) issues.push(`${m} q${i+1}: missing explanation`);
    if (x.type === 'fill' && (!x.accept || !x.accept.length)) issues.push(`${m} q${i+1}: no accept[]`);
    if (x.type === 'order' && (!x.items || !x.correctOrder || x.items.length !== x.correctOrder.length)) issues.push(`${m} q${i+1}: order mismatch`);
    // em dash / emoji scan on visible text
    const blob = JSON.stringify(x);
    if (blob.indexOf('—') >= 0 || blob.indexOf('–') >= 0) issues.push(`${m} q${i+1}: contains an en/em dash`);
    if (x.code) codes.push({ m, q: i + 1, code: x.code, expect: x.options[x.correctIndex].text });
  });
  const distinct = labels.size;
  if (distinct < 3) issues.push(`${m}: only ${distinct} distinct types (want 3-4)`);
}
console.log("=== STRUCTURAL ISSUES ===");
console.log(issues.length ? issues.join("\n") : "none");
console.log("\n=== TYPE LABEL COVERAGE ===");
console.log(JSON.stringify(typeCount, null, 0));
fs.writeFileSync('/tmp/quiz_codes.json', JSON.stringify(codes));
console.log("\ncoding questions found:", codes.length);
