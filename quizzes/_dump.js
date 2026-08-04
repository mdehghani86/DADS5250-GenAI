const fs = require('fs'), vm = require('vm');
const mods = ["M01","M02","M03","M04","M05","M06","M08","M09","M10","M11","M12","M13"];
const out = {};
for (const m of mods) {
  const src = fs.readFileSync(`data/${m}_quiz.js`, 'utf8');
  const ctx = { window: {} }; vm.runInNewContext(src, ctx); out[m] = ctx.window.QUIZ;
}
fs.writeFileSync('/tmp/quizzes.json', JSON.stringify(out));
console.log('dumped', Object.keys(out).length, 'modules');
