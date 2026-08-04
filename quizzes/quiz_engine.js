/* DADS 5250 quiz engine, single DEVELOPMENT / REVIEW view.
   Shows every question fully expanded: prompt, all options with the correct one marked,
   and every per-option feedback comment. Tiny copy button on each field. Optional
   "Download for Canvas" button when window.CANVAS_ZIP is set. Not a student-testing view. */
(function () {
  var Q = window.QUIZ || { meta: {}, questions: [] };
  var questions = Q.questions || [];
  var meta = Q.meta || {};

  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function diffLabel(d) { return d ? d.charAt(0).toUpperCase() + d.slice(1) : 'Medium'; }
  function visuals(q) {
    var h = '';
    if (q.diagram) h += '<div class="diagram-area">' + q.diagram + '</div>';
    if (q.code) h += '<div class="code-block">' + esc(q.code) + '</div>';
    return h;
  }
  var COPY_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>';
  function cb() { return '<button class="copybtn" type="button" title="Copy this field" aria-label="Copy this field">' + COPY_SVG + '</button>'; }
  // wrap arbitrary HTML content as a copyable field followed by a copy button
  function field(html, tag) { tag = tag || 'div'; return '<div class="fieldwrap"><' + tag + ' class="cf">' + html + '</' + tag + '>' + cb() + '</div>'; }
  function metaRow(q, i) {
    return '<div class="qmeta"><span class="question-number">Question ' + (i + 1) + '</span>' +
      '<span class="badge">' + esc(q.typeLabel || 'Multiple choice') + '</span>' +
      '<span class="badge diff-' + (q.difficulty || 'medium') + '">' + diffLabel(q.difficulty) + '</span></div>';
  }
  function dlRow() {
    if (!window.CANVAS_ZIP) return '';
    return '<div class="dl-row"><a class="dl-btn" href="' + window.CANVAS_ZIP + '" download>' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>' +
      'Download for Canvas (QTI .zip)</a></div>';
  }

  function optionRow(o, isCorrect) {
    var opt = '<div class="option locked' + (isCorrect ? ' correct' : '') + '">' +
      '<span class="letter">' + o.letter + '</span><span class="cf">' + o.text + '</span>' +
      '<span class="mark">' + (isCorrect ? '✓' : '') + '</span></div>';
    return '<div class="fieldwrap">' + opt + cb() + '</div>';
  }
  function optionFb(o, isCorrect) {
    var lbl = isCorrect ? 'Shown if selected (correct):' : 'Shown if selected (wrong):';
    return '<div class="rev-optfb ' + (isCorrect ? 'correct' : 'wrong') + '"><span class="lbl">' + lbl + '</span> <span class="cf">' + (o.explanation || '') + '</span>' + cb() + '</div>';
  }

  function render() {
    var r = document.getElementById('quiz-root');
    var html = dlRow() +
      '<div class="review-banner">Development and review view. Every question shows the correct answer and all per-option feedback. This is not the student-facing quiz.</div>';
    questions.forEach(function (q, i) {
      html += '<div class="question-card">' + metaRow(q, i) +
        '<div class="fieldwrap"><div class="question-prompt cf">' + q.prompt + '</div>' + cb() + '</div>' + visuals(q);
      if (q.type === 'mc' || q.type === 'multi') {
        var correctSet = q.type === 'mc' ? [q.correctIndex] : q.correctIndices;
        html += q.options.map(function (o, j) {
          var isC = correctSet.indexOf(j) >= 0;
          return '<div class="rev-opt">' + optionRow(o, isC) + optionFb(o, isC) + '</div>';
        }).join('');
      } else if (q.type === 'tf') {
        html += '<div class="rev-answer"><span class="lbl">Answer:</span> <span class="cf">' + (q.correctAnswer ? 'True' : 'False') + '</span>' + cb() + '</div>' +
          '<div class="rev-optfb correct"><span class="lbl">Feedback:</span> <span class="cf">' + q.explanation + '</span>' + cb() + '</div>';
      } else if (q.type === 'fill') {
        html += '<div class="rev-answer"><span class="lbl">Accepted answer(s):</span> <span class="cf">' + esc(q.accept.join(' / ')) + '</span>' + cb() + '</div>' +
          '<div class="rev-optfb correct"><span class="lbl">Feedback:</span> <span class="cf">' + q.explanation + '</span>' + cb() + '</div>';
      } else if (q.type === 'order') {
        var ordered = q.items.map(function (_, slot) { var itemIdx = q.correctOrder.indexOf(slot); return (slot + 1) + '. ' + esc(q.items[itemIdx]); }).join('<br>');
        html += '<div class="rev-answer"><span class="lbl">Correct order:</span><br><span class="cf">' + ordered + '</span>' + cb() + '</div>' +
          '<div class="rev-optfb correct"><span class="lbl">Feedback:</span> <span class="cf">' + q.explanation + '</span>' + cb() + '</div>';
      }
      html += '</div>';
    });
    r.innerHTML = html;
  }

  // one delegated handler: copy the .cf field paired with the clicked button
  document.addEventListener('click', function (e) {
    var b = e.target.closest ? e.target.closest('.copybtn') : null;
    if (!b) return;
    var cf = b.parentElement.querySelector('.cf');
    if (!cf) return;
    var text = cf.innerText || cf.textContent || '';
    var done = function () { b.classList.add('copied'); setTimeout(function () { b.classList.remove('copied'); }, 1100); };
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done, done);
    else { var ta = document.createElement('textarea'); ta.value = text; document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); } catch (x) {} document.body.removeChild(ta); done(); }
  });

  function boot() {
    var hdr = document.getElementById('quiz-header');
    if (hdr) hdr.innerHTML = '<div class="eyebrow">' + esc(meta.module || '') + ' quiz</div><h1>' + esc(meta.title || 'Module quiz') + '</h1><div class="subtitle">' + esc(meta.subtitle || 'DADS 5250 Generative AI in Practice') + '</div>';
    render();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
