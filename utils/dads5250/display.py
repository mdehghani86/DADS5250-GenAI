"""Display helpers for lab notebooks."""

from IPython.display import display, HTML, Markdown


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
