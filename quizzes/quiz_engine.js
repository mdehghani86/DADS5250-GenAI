/* DADS 5250 quiz engine. Reads window.QUIZ = {meta, questions} and window.REVIEW (bool).
   Student mode: ALL questions on one scrolling page, each answered inline with instant feedback.
   Review mode: all questions with correct answers and every explanation shown.
   Mechanics: mc, multi, tf, fill, order. Any question may carry a `code` block or `diagram` (SVG). */
(function () {
  var Q = window.QUIZ || { meta: {}, questions: [] };
  var REVIEW = !!window.REVIEW;
  var questions = Q.questions || [];
  var meta = Q.meta || {};
  var STORAGE_KEY = 'dads_quiz_' + (meta.module || 'x');
  var state = { answers: questions.map(function () { return { answered: false, correct: false }; }) };

  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function norm(s) { return String(s).trim().toLowerCase().replace(/[^a-z0-9.]/g, ''); }
  function root() { return document.getElementById('quiz-root'); }
  function card(i) { return document.getElementById('qc-' + i); }
  function save() { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch (e) {} }
  function load() { try { var s = JSON.parse(localStorage.getItem(STORAGE_KEY)); if (s && s.answers && s.answers.length === questions.length) state = s; } catch (e) {} }
  function diffLabel(d) { return d ? d.charAt(0).toUpperCase() + d.slice(1) : 'Medium'; }
  function score() { return state.answers.filter(function (a) { return a.correct; }).length; }
  function answered() { return state.answers.filter(function (a) { return a.answered; }).length; }
  function visuals(q) {
    var h = '';
    if (q.diagram) h += '<div class="diagram-area">' + q.diagram + '</div>';
    if (q.code) h += '<div class="code-block">' + esc(q.code) + '</div>';
    return h;
  }
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

  /* ---------- one interactive question card (student mode) ---------- */
  function studentCard(q, i) {
    var body = metaRow(q, i) + '<div class="question-prompt">' + q.prompt + '</div>' + visuals(q);
    if (q.type === 'mc' || q.type === 'multi') {
      body += '<div class="options-list">' + q.options.map(function (o, j) {
        return '<button class="option" data-i="' + j + '"><span class="letter">' + o.letter + '</span><span>' + o.text + '</span><span class="mark"></span></button>';
      }).join('') + '</div>';
      if (q.type === 'multi') body += '<div class="submit-row"><button class="btn primary" data-submit>Submit</button><span class="hint" style="margin:0;align-self:center">Select all that apply.</span></div>';
    } else if (q.type === 'tf') {
      body += '<div class="options-list"><button class="option" data-tf="true"><span class="letter">T</span><span>True</span><span class="mark"></span></button>' +
              '<button class="option" data-tf="false"><span class="letter">F</span><span>False</span><span class="mark"></span></button></div>';
    } else if (q.type === 'fill') {
      body += '<input class="fill-input" data-fill placeholder="Type your answer" autocomplete="off"><div class="submit-row"><button class="btn primary" data-submit>Submit</button></div>';
    } else if (q.type === 'order') {
      body += '<div class="order-list">' + q.items.map(function (it, k) {
        var opts = q.items.map(function (_, j) { return '<option value="' + j + '">' + (j + 1) + '</option>'; }).join('');
        return '<div class="order-item"><span class="num">' + (k + 1) + '</span><span>' + esc(it) + '</span><select data-oi="' + k + '">' + opts + '</select></div>';
      }).join('') + '</div><div class="submit-row"><button class="btn primary" data-submit>Submit</button><span class="hint" style="margin:0;align-self:center">Set the correct position for each item.</span></div>';
    }
    body += '<div class="feedback"></div>';
    return body;
  }

  function renderStudent() {
    var r = root();
    var head = '<div class="score-bar"><span class="score-text">' + score() + ' / ' + questions.length + ' correct</span>' +
      '<span class="page-indicator" id="prog">' + answered() + ' of ' + questions.length + ' answered</span></div>';
    r.innerHTML = dlRow() + head + questions.map(function (q, i) { return '<div class="question-card" id="qc-' + i + '">' + studentCard(q, i) + '</div>'; }).join('');
    questions.forEach(function (q, i) { wire(q, i); if (state.answers[i].answered) replay(q, i); });
  }

  function updateBars() {
    var st = document.querySelector('.score-text'); if (st) st.textContent = score() + ' / ' + questions.length + ' correct';
    var pr = document.getElementById('prog'); if (pr) pr.textContent = answered() + ' of ' + questions.length + ' answered';
  }

  function wire(q, i) {
    if (state.answers[i].answered) return;
    var c = card(i);
    if (q.type === 'mc') {
      c.querySelectorAll('.option').forEach(function (b) { b.onclick = function () { gradeMC(q, i, +b.getAttribute('data-i')); }; });
    } else if (q.type === 'tf') {
      c.querySelectorAll('.option').forEach(function (b) { b.onclick = function () { gradeTF(q, i, b.getAttribute('data-tf') === 'true'); }; });
    } else if (q.type === 'multi') {
      c.querySelectorAll('.option').forEach(function (b) { b.onclick = function () { b.classList.toggle('selected'); }; });
      c.querySelector('[data-submit]').onclick = function () {
        var chosen = []; c.querySelectorAll('.option.selected').forEach(function (b) { chosen.push(+b.getAttribute('data-i')); });
        gradeMulti(q, i, chosen);
      };
    } else if (q.type === 'fill') {
      c.querySelector('[data-submit]').onclick = function () { gradeFill(q, i, c.querySelector('[data-fill]').value); };
    } else if (q.type === 'order') {
      c.querySelector('[data-submit]').onclick = function () {
        var ord = []; c.querySelectorAll('[data-oi]').forEach(function (s) { ord[+s.getAttribute('data-oi')] = +s.value; });
        gradeOrder(q, i, ord);
      };
    }
  }

  function lockAndFeedback(q, i, correct, answerHTML, exp) {
    var c = card(i);
    c.querySelectorAll('.option').forEach(function (b) { b.classList.add('locked'); });
    var sub = c.querySelector('[data-submit]'); if (sub) sub.disabled = true;
    var fill = c.querySelector('[data-fill]'); if (fill) fill.disabled = true;
    var fb = c.querySelector('.feedback');
    fb.className = 'feedback show ' + (correct ? 'correct' : 'incorrect');
    fb.innerHTML = '<span class="verdict">' + (correct ? 'Correct.' : 'Not quite.') + '</span>' +
      (answerHTML ? '<div class="answer-line">' + answerHTML + '</div>' : '') +
      (exp ? '<div class="answer-line">' + exp + '</div>' : '');
    state.answers[i] = { answered: true, correct: correct };
    save(); updateBars();
  }

  function gradeMC(q, i, sel) {
    var correct = sel === q.correctIndex, opts = card(i).querySelectorAll('.option');
    opts[sel].classList.add(correct ? 'correct' : 'incorrect');
    opts[sel].querySelector('.mark').textContent = correct ? '✓' : '✗';
    if (!correct) { opts[q.correctIndex].classList.add('correct'); opts[q.correctIndex].querySelector('.mark').textContent = '✓'; }
    var co = q.options[q.correctIndex], ch = q.options[sel];
    var exp = correct ? co.explanation
      : '<strong>Why ' + ch.letter + ' is wrong:</strong> ' + ch.explanation +
        '<div class="answer-line"><strong>Why ' + co.letter + ' is right:</strong> ' + co.explanation + '</div>';
    lockAndFeedback(q, i, correct, '<strong>Answer:</strong> ' + co.letter + ') ' + co.text, exp);
  }
  function gradeMulti(q, i, chosen) {
    var correct = q.correctIndices.slice().sort().join(',') === chosen.slice().sort().join(',');
    var opts = card(i).querySelectorAll('.option');
    q.correctIndices.forEach(function (ci) { opts[ci].classList.add('correct'); opts[ci].querySelector('.mark').textContent = '✓'; });
    chosen.forEach(function (ci) { if (q.correctIndices.indexOf(ci) < 0) { opts[ci].classList.add('incorrect'); opts[ci].querySelector('.mark').textContent = '✗'; } });
    var letters = q.correctIndices.map(function (ci) { return q.options[ci].letter; }).join(', ');
    var exp;
    if (correct) { exp = q.explanation || ''; }
    else {
      var parts = [];
      chosen.forEach(function (ci) { if (q.correctIndices.indexOf(ci) < 0) parts.push('<div class="answer-line"><strong>' + q.options[ci].letter + ' should NOT be selected:</strong> ' + q.options[ci].explanation + '</div>'); });
      q.correctIndices.forEach(function (ci) { if (chosen.indexOf(ci) < 0) parts.push('<div class="answer-line"><strong>' + q.options[ci].letter + ' should be selected:</strong> ' + q.options[ci].explanation + '</div>'); });
      exp = parts.join('') + (q.explanation ? '<div class="answer-line">' + q.explanation + '</div>' : '');
    }
    lockAndFeedback(q, i, correct, '<strong>Correct set:</strong> ' + letters, exp);
  }
  function gradeTF(q, i, val) {
    var correct = val === q.correctAnswer, opts = card(i).querySelectorAll('.option');
    var sidx = val ? 0 : 1, cidx = q.correctAnswer ? 0 : 1;
    opts[sidx].classList.add(correct ? 'correct' : 'incorrect');
    opts[sidx].querySelector('.mark').textContent = correct ? '✓' : '✗';
    if (!correct) { opts[cidx].classList.add('correct'); opts[cidx].querySelector('.mark').textContent = '✓'; }
    lockAndFeedback(q, i, correct, '<strong>Answer:</strong> ' + (q.correctAnswer ? 'True' : 'False'), q.explanation);
  }
  function gradeFill(q, i, val) {
    var correct = (q.accept || []).some(function (a) { return norm(a) === norm(val); });
    lockAndFeedback(q, i, correct, '<strong>Answer:</strong> ' + esc(q.accept[0]), q.explanation);
  }
  function gradeOrder(q, i, ord) {
    var correct = ord.join(',') === q.correctOrder.join(',');
    var ordered = q.items.map(function (_, slot) { var itemIdx = q.correctOrder.indexOf(slot); return (slot + 1) + '. ' + esc(q.items[itemIdx]); }).join('<br>');
    lockAndFeedback(q, i, correct, '<strong>Correct order:</strong><br>' + ordered, q.explanation);
  }

  function replay(q, i) {
    var c = card(i);
    if (q.type === 'mc' || q.type === 'tf') {
      var opts = c.querySelectorAll('.option');
      var cidx = q.type === 'mc' ? q.correctIndex : (q.correctAnswer ? 0 : 1);
      if (opts[cidx]) { opts[cidx].classList.add('correct'); opts[cidx].querySelector('.mark').textContent = '✓'; }
    }
    c.querySelectorAll('.option').forEach(function (b) { b.classList.add('locked'); });
    var sub = c.querySelector('[data-submit]'); if (sub) sub.disabled = true;
    var fill = c.querySelector('[data-fill]'); if (fill) fill.disabled = true;
    var fb = c.querySelector('.feedback');
    fb.className = 'feedback show ' + (state.answers[i].correct ? 'correct' : 'incorrect');
    fb.innerHTML = '<span class="verdict">' + (state.answers[i].correct ? 'Correct.' : 'Not quite.') + '</span> <span class="answer-line">You have already answered this question. Clear your browser storage to retake it.</span>';
  }

  /* ---------- REVIEW / ANSWER-KEY MODE ---------- */
  function renderReview() {
    var r = root();
    var html = dlRow() + '<div class="review-banner">Colleague review view. Correct answers and explanations are shown. This is not the student view.</div>';
    questions.forEach(function (q, i) {
      html += '<div class="question-card">' + metaRow(q, i) + '<div class="question-prompt">' + q.prompt + '</div>' + visuals(q);
      if (q.type === 'mc' || q.type === 'multi') {
        var correctSet = q.type === 'mc' ? [q.correctIndex] : q.correctIndices;
        html += q.options.map(function (o, j) {
          var isC = correctSet.indexOf(j) >= 0;
          var opt = '<div class="option locked' + (isC ? ' correct' : '') + '"><span class="letter">' + o.letter + '</span><span>' + o.text + '</span><span class="mark">' + (isC ? '✓' : '') + '</span></div>';
          var lbl = isC ? 'Shown if selected (correct):' : 'Shown if selected (wrong):';
          var fb = '<div class="rev-optfb ' + (isC ? 'correct' : 'wrong') + '"><span class="lbl">' + lbl + '</span> ' + (o.explanation || '') + '</div>';
          return '<div class="rev-opt">' + opt + fb + '</div>';
        }).join('');
      } else if (q.type === 'tf') {
        html += '<div class="rev-answer"><span class="lbl">Answer:</span> ' + (q.correctAnswer ? 'True' : 'False') + '</div><div class="rev-exp">' + q.explanation + '</div>';
      } else if (q.type === 'fill') {
        html += '<div class="rev-answer"><span class="lbl">Answer:</span> ' + esc(q.accept.join(' / ')) + '</div><div class="rev-exp">' + q.explanation + '</div>';
      } else if (q.type === 'order') {
        var ordered = q.items.map(function (_, slot) { var itemIdx = q.correctOrder.indexOf(slot); return (slot + 1) + '. ' + esc(q.items[itemIdx]); }).join('<br>');
        html += '<div class="rev-answer"><span class="lbl">Correct order:</span><br>' + ordered + '</div><div class="rev-exp">' + q.explanation + '</div>';
      }
      html += '</div>';
    });
    r.innerHTML = html;
  }

  function boot() {
    var hdr = document.getElementById('quiz-header');
    if (hdr) hdr.innerHTML = '<div class="eyebrow">' + esc(meta.module || '') + ' quiz</div><h1>' + esc(meta.title || 'Module quiz') + '</h1><div class="subtitle">' + esc(meta.subtitle || 'DADS 5250 Generative AI in Practice') + '</div>';
    if (REVIEW) renderReview(); else { load(); renderStudent(); }
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
