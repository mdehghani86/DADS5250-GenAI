"""Interactive multiple-choice quiz widget for Colab notebooks."""

from IPython.display import display, HTML
import random
import json


def quiz(questions: list[dict]):
    """Render an interactive HTML/JS multiple-choice quiz inline.

    Args:
        questions: list of dicts with keys:
            - q: question text
            - options: list of answer strings
            - answer: index (0-based) of the correct option
            - explanation: (optional) explanation shown after answering

    Example:
        quiz([
            {
                "q": "What is a token in the context of LLMs?",
                "options": [
                    "A security credential",
                    "A piece of text (word, subword, or character)",
                    "A type of neural network layer",
                    "A billing unit unrelated to text"
                ],
                "answer": 1,
                "explanation": "Tokens are the basic units LLMs process — typically words, subwords, or characters."
            }
        ])
    """
    quiz_id = f"quiz_{random.randint(10000, 99999)}"
    questions_json = json.dumps(questions)

    html = f"""
    <div id="{quiz_id}" style="font-family:system-ui;"></div>
    <script>
    (function() {{
        const questions = {questions_json};
        const container = document.getElementById("{quiz_id}");
        let score = 0;
        let answered = new Set();

        questions.forEach((q, qi) => {{
            const qDiv = document.createElement("div");
            qDiv.style.cssText = "background:#f8fafc; border:1px solid #dde3ec; border-radius:10px; padding:14px 18px; margin:10px 0;";

            let optionsHTML = "";
            q.options.forEach((opt, oi) => {{
                optionsHTML += `
                    <label style="display:block; padding:6px 10px; margin:3px 0; border-radius:6px; cursor:pointer;
                                  border:1px solid #dde3ec; font-size:13px; transition:all .2s;"
                           onmouseover="this.style.background='#e8f0fe'"
                           onmouseout="if(!this.classList.contains('picked'))this.style.background='#fff'"
                           id="{quiz_id}_q${{qi}}_o${{oi}}">
                        <input type="radio" name="{quiz_id}_q${{qi}}" value="${{oi}}"
                               style="margin-right:8px;"
                               onchange="window.{quiz_id}_check(${{qi}}, ${{oi}})">
                        ${{opt}}
                    </label>`;
            }});

            qDiv.innerHTML = `
                <div style="font-size:13px; font-weight:700; color:#001a70; margin-bottom:8px;">
                    Q${{qi + 1}}. ${{q.q}}
                </div>
                ${{optionsHTML}}
                <div id="{quiz_id}_fb${{qi}}" style="margin-top:8px; font-size:12px; display:none;"></div>
            `;
            container.appendChild(qDiv);
        }});

        window["{quiz_id}_check"] = function(qi, oi) {{
            if (answered.has(qi)) return;
            answered.add(qi);
            const q = questions[qi];
            const correct = oi === q.answer;
            if (correct) score++;

            // Disable all radios for this question
            q.options.forEach((_, i) => {{
                const label = document.getElementById("{quiz_id}_q" + qi + "_o" + i);
                label.querySelector("input").disabled = true;
                if (i === q.answer) {{
                    label.style.background = "#ecfdf5";
                    label.style.border = "1px solid #059669";
                    label.classList.add("picked");
                }} else if (i === oi && !correct) {{
                    label.style.background = "#fef2f2";
                    label.style.border = "1px solid #dc2626";
                    label.classList.add("picked");
                }}
            }});

            const fb = document.getElementById("{quiz_id}_fb" + qi);
            fb.style.display = "block";
            if (correct) {{
                fb.innerHTML = '<span style="color:#059669; font-weight:600;">Correct!</span>';
            }} else {{
                fb.innerHTML = '<span style="color:#dc2626; font-weight:600;">Incorrect.</span> The answer is: <b>' + q.options[q.answer] + '</b>';
            }}
            if (q.explanation) {{
                fb.innerHTML += '<div style="color:#6b7280; margin-top:4px;">' + q.explanation + '</div>';
            }}

            // Show score when all answered
            if (answered.size === questions.length) {{
                const scoreDiv = document.createElement("div");
                scoreDiv.style.cssText = "background:#f0f4ff; border:2px solid #0055d4; border-radius:10px; padding:12px 18px; margin:12px 0; text-align:center;";
                scoreDiv.innerHTML = '<span style="font-size:15px; font-weight:700; color:#001a70;">Score: ' + score + ' / ' + questions.length + '</span>';
                container.appendChild(scoreDiv);
            }}
        }};
    }})();
    </script>
    """
    display(HTML(html))
