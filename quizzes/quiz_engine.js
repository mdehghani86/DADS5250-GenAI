/* DADS 5250 quiz engine. Reads window.QUIZ = {meta, questions} and window.REVIEW (bool).
   Mechanics: mc, multi, tf, fill, order. Any question may carry a `code` block or `diagram` (SVG).
   typeLabel carries the pedagogical label (Practical insight, Graphic based, Coding, etc.). */
(function () {
  var Q = window.QUIZ || { meta: {}, questions: [] };
  var REVIEW = !!window.REVIEW;
  var questions = Q.questions || [];
  var meta = Q.meta || {};
  var STORAGE_KEY = 'dads_quiz_' + (meta.module || 'x');

  var state = { idx: 0, answers: questions.map(function () { return { answered: false, correct: false }; }) };

  function esc(s) { return String(s == null ? '' : s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
  function norm(s) { return String(s).trim().toLowerCase().replace(/[^a-z0-9.]/g, ''); }
  function root() { return document.getElementById('quiz-root'); }

  function save() { try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch (e) {} }
  function load() { try { var s = JSON.parse(localStorage.getItem(STORAGE_KEY)); if (s && s.answers && s.answers.length === questions.length) state = s; } catch (e) {} }

  function diffLabel(d) { return d ? d.charAt(0).toUpperCase() + d.slice(1) : 'Medium'; }
  function visuals(q) {
    var h = '';
    if (q.diagram) h += '<div class="diagram-area">' + q.diagram + '</div>';
    if (q.code) h += '<div class="code-block">' + esc(q.code) + '</div>';
    return h;
  }
  function score() { return state.answers.filter(function (a) { return a.correct; }).length; }

  /* ---------- STUDENT MODE ---------- */
  function renderStudent() {
    var r = root();
    var done = state.answers.every(function (a) { return a.answered; });
    var dots = questions.map(function (q, i) {
      var c = 'progress-dot' + (i === state.idx ? ' active' : '');
      if (state.answers[i].answered) c += state.answers[i].correct ? ' correct' : ' incorrect';
      return '<span class="' + c + '" data-jump="' + i + '"></span>';
    }).join('');
    var head =
      '<div class="score-bar"><span class="score-text">' + score() + ' / ' + questions.length + ' correct</span>' +
      '<span class="page-indicator">' + (done ? 'Review your answers' : 'Question ' + (state.idx + 1) + ' of ' + questions.length) + '</span></div>' +
      '<div class="progress-dots">' + dots + '</div>';
    r.innerHTML = head + '<div id="card"></div>';
    renderCard();
    Array.prototype.forEach.call(r.querySelectorAll('[data-jump]'), function (d) {
      d.onclick = function () { state.idx = +d.getAttribute('data-jump'); renderStudent(); };
    });
  }

  function renderCard() {
    var q = questions[state.idx], a = state.answers[state.idx], card = document.getElementById('card');
    var body =
      '<div class="qmeta"><span class="question-number">Question ' + (state.idx + 1) + '</span>' +
      '<span class="badge">' + esc(q.typeLabel || 'Multiple choice') + '</span>' +
      '<span class="badge diff-' + (q.difficulty || 'medium') + '">' + diffLabel(q.difficulty) + '</span></div>' +
      '<div class="question-prompt">' + q.prompt + '</div>' + visuals(q);

    if (q.type === 'mc' || q.type === 'multi') {
      body += '<div class="options-list">' + q.options.map(function (o, i) {
        return '<button class="option" data-i="' + i + '"><span class="letter">' + o.letter + '</span><span>' + o.text + '</span><span class="mark"></span></button>';
      }).join('') + '</div>';
      if (q.type === 'multi') body += '<div class="submit-row"><button class="btn primary" id="submit">Submit</button><span class="hint" style="margin:0;align-self:center">Select all that apply.</span></div>';
    } else if (q.type === 'tf') {
      body += '<div class="options-list"><button class="option" data-tf="true"><span class="letter">T</span><span>True</span><span class="mark"></span></button>' +
              '<button class="option" data-tf="false"><span class="letter">F</span><span>False</span><span class="mark"></span></button></div>';
    } else if (q.type === 'fill') {
      body += '<input class="fill-input" id="fill" placeholder="Type your answer" autocomplete="off"><div class="submit-row"><button class="btn primary" id="submit">Submit</button></div>';
    } else if (q.type === 'order') {
      body += '<div class="order-list">' + q.items.map(function (it, i) {
        var opts = q.items.map(function (_, j) { return '<option value="' + j + '">' + (j + 1) + '</option>'; }).join('');
        return '<div class="order-item"><span class="num">' + (i + 1) + '</span><span>' + esc(it) + '</span><select data-oi="' + i + '">' + opts + '</select></div>';
      }).join('') + '</div><div class="submit-row"><button class="btn primary" id="submit">Submit</button></div>';
    }
    body += '<div class="feedback" id="fb"></div>';
    body +=
      '<div class="nav-row"><button class="btn" id="prev"' + (state.idx === 0 ? ' disabled' : '') + '>Previous</button>' +
      '<button class="btn primary" id="next"' + (state.idx === questions.length - 1 ? ' disabled' : '') + '>Next</button></div>';
    card.innerHTML = body;

    wire(q, a);
    document.getElementById('prev').onclick = function () { if (state.idx > 0) { state.idx--; renderStudent(); } };
    document.getElementById('next').onclick = function () { if (state.idx < questions.length - 1) { state.idx++; renderStudent(); } };
    if (a.answered) replay(q, a);
  }

  function wire(q, a) {
    if (a.answered) return;
    if (q.type === 'mc') {
      Array.prototype.forEach.call(document.querySelectorAll('.option'), function (b) {
        b.onclick = function () { gradeMC(q, +b.getAttribute('data-i')); };
      });
    } else if (q.type === 'tf') {
      Array.prototype.forEach.call(document.querySelectorAll('.option'), function (b) {
        b.onclick = function () { gradeTF(q, b.getAttribute('data-tf') === 'true'); };
      });
    } else if (q.type === 'multi') {
      Array.prototype.forEach.call(document.querySelectorAll('.option'), function (b) {
        b.onclick = function () { b.classList.toggle('selected'); };
      });
      document.getElementById('submit').onclick = function () {
        var chosen = []; Array.prototype.forEach.call(document.querySelectorAll('.option.selected'), function (b) { chosen.push(+b.getAttribute('data-i')); });
        gradeMulti(q, chosen);
      };
    } else if (q.type === 'fill') {
      document.getElementById('submit').onclick = function () { gradeFill(q, document.getElementById('fill').value); };
    } else if (q.type === 'order') {
      document.getElementById('submit').onclick = function () {
        var ord = []; Array.prototype.forEach.call(document.querySelectorAll('[data-oi]'), function (s) { ord[+s.getAttribute('data-oi')] = +s.value; });
        gradeOrder(q, ord);
      };
    }
  }

  function lockAndFeedback(correct, answerHTML, exp) {
    Array.prototype.forEach.call(document.querySelectorAll('.option'), function (b) { b.classList.add('locked'); });
    var sub = document.getElementById('submit'); if (sub) sub.disabled = true;
    var fill = document.getElementById('fill'); if (fill) fill.disabled = true;
    var fb = document.getElementById('fb');
    fb.className = 'feedback show ' + (correct ? 'correct' : 'incorrect');
    fb.innerHTML = '<span class="verdict">' + (correct ? 'Correct.' : 'Not quite.') + '</span>' +
      (answerHTML ? '<div class="answer-line">' + answerHTML + '</div>' : '') +
      (exp ? '<div class="answer-line">' + exp + '</div>' : '');
    state.answers[state.idx] = { answered: true, correct: correct };
    save();
    document.getElementById('next').disabled = state.idx === questions.length - 1;
    // refresh dots
    renderStudentDots();
  }
  function renderStudentDots() {
    var dots = document.querySelectorAll('.progress-dot');
    dots.forEach(function (d, i) {
      d.className = 'progress-dot' + (i === state.idx ? ' active' : '') + (state.answers[i].answered ? (state.answers[i].correct ? ' correct' : ' incorrect') : '');
    });
    var st = document.querySelector('.score-text'); if (st) st.textContent = score() + ' / ' + questions.length + ' correct';
  }

  function gradeMC(q, i) {
    var correct = i === q.correctIndex, opts = document.querySelectorAll('.option');
    opts[i].classList.add(correct ? 'correct' : 'incorrect');
    opts[i].querySelector('.mark').textContent = correct ? '✓' : '✗';
    if (!correct) { opts[q.correctIndex].classList.add('correct'); opts[q.correctIndex].querySelector('.mark').textContent = '✓'; }
    var co = q.options[q.correctIndex], chosen = q.options[i];
    var answer = '<strong>Answer:</strong> ' + co.letter + ') ' + co.text;
    var exp = correct
      ? co.explanation
      : '<strong>Why ' + chosen.letter + ' is wrong:</strong> ' + chosen.explanation +
        '<div class="answer-line"><strong>Why ' + co.letter + ' is right:</strong> ' + co.explanation + '</div>';
    lockAndFeedback(correct, answer, exp);
  }
  function gradeMulti(q, chosen) {
    var want = q.correctIndices.slice().sort().join(','), got = chosen.slice().sort().join(',');
    var correct = want === got, opts = document.querySelectorAll('.option');
    q.correctIndices.forEach(function (ci) { opts[ci].classList.add('correct'); opts[ci].querySelector('.mark').textContent = '✓'; });
    chosen.forEach(function (ci) { if (q.correctIndices.indexOf(ci) < 0) { opts[ci].classList.add('incorrect'); opts[ci].querySelector('.mark').textContent = '✗'; } });
    var letters = q.correctIndices.map(function (ci) { return q.options[ci].letter; }).join(', ');
    var exp;
    if (correct) {
      exp = q.explanation || '';
    } else {
      var parts = [];
      chosen.forEach(function (ci) { if (q.correctIndices.indexOf(ci) < 0) parts.push('<div class="answer-line"><strong>' + q.options[ci].letter + ' should NOT be selected:</strong> ' + q.options[ci].explanation + '</div>'); });
      q.correctIndices.forEach(function (ci) { if (chosen.indexOf(ci) < 0) parts.push('<div class="answer-line"><strong>' + q.options[ci].letter + ' should be selected:</strong> ' + q.options[ci].explanation + '</div>'); });
      exp = parts.join('') + (q.explanation ? '<div class="answer-line">' + q.explanation + '</div>' : '');
    }
    lockAndFeedback(correct, '<strong>Correct set:</strong> ' + letters, exp);
  }
  function gradeTF(q, val) {
    var correct = val === q.correctAnswer, opts = document.querySelectorAll('.option');
    var idx = val ? 0 : 1, cidx = q.correctAnswer ? 0 : 1;
    opts[idx].classList.add(correct ? 'correct' : 'incorrect');
    opts[idx].querySelector('.mark').textContent = correct ? '✓' : '✗';
    if (!correct) { opts[cidx].classList.add('correct'); opts[cidx].querySelector('.mark').textContent = '✓'; }
    lockAndFeedback(correct, '<strong>Answer:</strong> ' + (q.correctAnswer ? 'True' : 'False'), q.explanation);
  }
  function gradeFill(q, val) {
    var correct = (q.accept || []).some(function (a) { return norm(a) === norm(val); });
    lockAndFeedback(correct, '<strong>Answer:</strong> ' + esc(q.accept[0]), q.explanation);
  }
  function gradeOrder(q, ord) {
    var correct = ord.join(',') === q.correctOrder.join(',');
    var right = q.correctOrder.map(function (pos, i) { return (i + 1) + '. ' + q.items[q.correctOrder.indexOf(i)]; });
    // simpler: show correct sequence
    var seq = q.correctOrder.map(function (targetPos, itemIdx) { return null; });
    var ordered = q.items.map(function (_, slot) { var itemIdx = q.correctOrder.indexOf(slot); return (slot + 1) + '. ' + q.items[itemIdx]; }).join('<br>');
    lockAndFeedback(correct, '<strong>Correct order:</strong><br>' + ordered, q.explanation);
  }

  function replay(q, a) {
    // re-show a locked, answered card with the correct answer highlighted
    if (q.type === 'mc' || q.type === 'tf') {
      var opts = document.querySelectorAll('.option');
      var cidx = q.type === 'mc' ? q.correctIndex : (q.correctAnswer ? 0 : 1);
      if (opts[cidx]) { opts[cidx].classList.add('correct', 'locked'); opts[cidx].querySelector('.mark').textContent = '✓'; }
      opts.forEach(function (b) { b.classList.add('locked'); });
    }
    var fb = document.getElementById('fb');
    fb.className = 'feedback show ' + (a.correct ? 'correct' : 'incorrect');
    fb.innerHTML = '<span class="verdict">' + (a.correct ? 'Correct.' : 'Not quite.') + '</span> <span class="answer-line">You have already answered this one.</span>';
    var sub = document.getElementById('submit'); if (sub) sub.disabled = true;
    var fill = document.getElementById('fill'); if (fill) fill.disabled = true;
  }

  /* ---------- REVIEW / ANSWER-KEY MODE ---------- */
  function renderReview() {
    var r = root();
    var html = '<div class="review-banner">Colleague review view. Correct answers and explanations are shown. This is not the student view.</div>';
    questions.forEach(function (q, i) {
      html += '<div class="question-card"><div class="qmeta"><span class="question-number">Question ' + (i + 1) + '</span>' +
        '<span class="badge">' + esc(q.typeLabel || 'Multiple choice') + '</span>' +
        '<span class="badge diff-' + (q.difficulty || 'medium') + '">' + diffLabel(q.difficulty) + '</span></div>' +
        '<div class="question-prompt">' + q.prompt + '</div>' + visuals(q);
      if (q.type === 'mc' || q.type === 'multi') {
        var correctSet = q.type === 'mc' ? [q.correctIndex] : q.correctIndices;
        html += '<div class="options-list">' + q.options.map(function (o, j) {
          var isC = correctSet.indexOf(j) >= 0;
          return '<div class="option locked' + (isC ? ' correct' : '') + '"><span class="letter">' + o.letter + '</span><span>' + o.text + '</span><span class="mark">' + (isC ? '✓' : '') + '</span></div>';
        }).join('') + '</div>';
        html += '<div class="rev-exp">' + q.options.map(function (o, j) {
          return '<div class="opt-exp"><span class="ol">' + o.letter + ')</span> ' + (o.explanation || '') + '</div>';
        }).join('') + '</div>';
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
