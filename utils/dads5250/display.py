"""Display helpers for lab notebooks."""

import json
from IPython.display import display, HTML, Markdown


def pp(data, title: str = None):
    """Pretty-print structured data (dict, list, JSON string, Pydantic model).

    Renders a syntax-highlighted JSON block in a styled box.
    Works with dicts, lists, JSON strings, and Pydantic models.
    """
    # Convert to dict/list if needed
    if hasattr(data, "model_dump"):  # Pydantic v2
        data = data.model_dump()
    elif hasattr(data, "dict"):  # Pydantic v1
        data = data.dict()
    elif isinstance(data, str):
        try:
            data = json.loads(data)
        except (json.JSONDecodeError, TypeError):
            pass  # keep as string

    if isinstance(data, (dict, list)):
        formatted = json.dumps(data, indent=2, default=str)
    else:
        formatted = str(data)

    title_html = ""
    if title:
        title_html = f'<div style="font-size:12px; font-weight:700; color:#0055d4; margin-bottom:6px;">{title}</div>'

    html = f"""
    <div style="background:#f8f9fb; border:1px solid #dde3ec; padding:12px 16px;
                border-radius:8px; margin:8px 0; font-family:monospace; font-size:13px;">
        {title_html}
        <pre style="margin:0; white-space:pre-wrap; color:#1a1a2e;">{formatted}</pre>
    </div>
    """
    display(HTML(html))


def show_response(response, show_usage: bool = True):
    """Pretty-print an OpenAI ChatCompletion response."""
    msg = response.choices[0].message
    content = msg.content or "(no content)"
    role = msg.role

    html = f"""
    <div style="background:#f0f4ff; border-left:4px solid #0055d4; padding:12px 16px;
                border-radius:0 8px 8px 0; margin:8px 0; font-family:system-ui;">
        <div style="font-size:11px; color:#6b7280; margin-bottom:4px;">
            role: {role} &nbsp;|&nbsp; model: {response.model}
        </div>
        <div style="font-size:14px; color:#1a1a2e; white-space:pre-wrap;">{content}</div>
    </div>
    """
    if show_usage and response.usage:
        u = response.usage
        html += f"""
        <div style="font-size:11px; color:#6b7280; padding:4px 16px;">
            tokens — prompt: {u.prompt_tokens} | completion: {u.completion_tokens} | total: {u.total_tokens}
        </div>
        """
    display(HTML(html))


def show_expected(text: str):
    """Show an 'Expected Output' reference box."""
    html = f"""
    <div style="background:#ecfdf5; border:1px solid #a7f3d0; padding:10px 14px;
                border-radius:8px; margin:8px 0; font-family:monospace; font-size:13px;">
        <div style="font-size:11px; font-weight:600; color:#059669; margin-bottom:4px;">
            Expected Output
        </div>
        <div style="color:#1a1a2e; white-space:pre-wrap;">{text}</div>
    </div>
    """
    display(HTML(html))


def show_success(text: str):
    """Show a green success box."""
    html = f"""
    <div style="background:#ecfdf5; border-left:4px solid #059669; padding:10px 14px;
                border-radius:0 8px 8px 0; margin:8px 0;">
        <span style="color:#059669; font-weight:600;">{text}</span>
    </div>
    """
    display(HTML(html))


def show_info(text: str):
    """Show a blue info box."""
    html = f"""
    <div style="background:#f0f4ff; border-left:4px solid #0055d4; padding:10px 14px;
                border-radius:0 8px 8px 0; margin:8px 0;">
        <span style="color:#001a70;">{text}</span>
    </div>
    """
    display(HTML(html))


_PP_THEMES = {
    "blue":   {"color": "#1e4b8f", "background": "#f0f6ff"},
    "red":    {"color": "#c62828", "background": "#ffebee"},
    "yellow": {"color": "#b26a00", "background": "#fff8e1"},
    "green":  {"color": "#1b5e20", "background": "#e8f5e9"},
    "gray":   {"color": "#37474f", "background": "#eceff1"},
}


def pretty_print(text, title="🤖 Model Response", theme="blue", style=None):
    """Display a styled message box for plain-text LLM output.

    Compatibility shim for labs originally authored for the AppliedGenAI
    `utils.py` module — accepts the same `(text, title, theme=...)` /
    `(..., style=...)` signature so reused notebooks keep working
    byte-identically.
    """
    chosen = (style or theme or "blue").lower()
    palette = _PP_THEMES.get(chosen, _PP_THEMES["blue"])
    body = str(text).replace("\n", "<br>")
    display(HTML(f"""
    <div style="border-left: 5px solid {palette['color']};
                padding: 12px 16px;
                background-color: {palette['background']};
                border-radius: 6px;
                font-family: 'Segoe UI', sans-serif;
                line-height: 1.6;
                margin: 10px 0;">
        <strong style="color: {palette['color']}; font-size: 16px;">{title}</strong><br>
        <span style="font-size: 14px; color: #333;">{body}</span>
    </div>
    """))


def lab_pill(title: str, color: str = "#0055d4") -> None:
    """Render a sticky pill at the top of the notebook so the lab name stays
    visible while scrolling."""
    display(HTML(f"""
    <div style="position: sticky; top: 0; z-index: 9999; text-align: center;
                padding: 6px 0; pointer-events: none;">
      <span style="display: inline-block; background: {color}; color: white;
                   padding: 6px 16px; border-radius: 999px;
                   font-family: 'Segoe UI', sans-serif; font-size: 12px;
                   font-weight: 600; letter-spacing: 0.5px;
                   box-shadow: 0 2px 6px rgba(0,0,0,0.15);">
        📘 {title}
      </span>
    </div>
    """))


def compare_responses(responses: dict):
    """Side-by-side comparison of multiple model responses.

    Args:
        responses: dict of {label: response_text}
    """
    cols = len(responses)
    width = int(100 / cols)
    cells = ""
    for label, text in responses.items():
        cells += f"""
        <div style="flex:1; min-width:200px; background:#f0f4ff; border:1px solid #dde3ec;
                    border-radius:8px; padding:12px; margin:4px;">
            <div style="font-size:12px; font-weight:700; color:#0055d4; margin-bottom:6px;">
                {label}
            </div>
            <div style="font-size:13px; color:#1a1a2e; white-space:pre-wrap;">{text}</div>
        </div>
        """
    html = f'<div style="display:flex; gap:8px; flex-wrap:wrap;">{cells}</div>'
    display(HTML(html))
