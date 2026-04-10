"""
Export All Scripts — reads M00-M14 HTML script files and generates a clean .txt export.
Run: python scripts/export_all_scripts.py
Output: scripts/DADS5250_All_Scripts.txt
"""
import os
import re
from datetime import datetime
from html.parser import HTMLParser

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Module folders in order
MODULE_FOLDERS = [
    ("M00_Course_Intro", "M00", "COURSE INTRODUCTION"),
    ("M01_LLM_APIs", "M01", "GETTING STARTED WITH LLM APIs"),
    ("M02_AI_in_Action", "M02", "AI IN ACTION"),
    ("M03_Prompt_Structured_FunctionCalling", "M03", "PROMPT ENGINEERING, STRUCTURED OUTPUT & FUNCTION CALLING"),
    ("M04_LangChain", "M04", "LANGCHAIN & BEER GAME"),
    ("M05_RAG", "M05", "RETRIEVAL-AUGMENTED GENERATION"),
    ("M06_Agents_OpenAI", "M06", "AGENTS & LANGGRAPH"),
    ("M07_Hackathon", "M07", "HACKATHON"),
    ("M08_MultiAgent", "M08", "MULTI-AGENT SYSTEMS (CREWAI)"),
    ("M09_Frontend", "M09", "FRONTEND FOR AI — GRADIO & STREAMLIT"),
    ("M10_MCP_Guardrails", "M10", "MCP & GUARDRAILS"),
    ("M11_Vision_Eval", "M11", "VISION & EVALUATION"),
    ("M12_SDKs_ClaudeCode", "M12", "AGENT SDKs & CLAUDE CODE"),
    ("M13_Business_n8n", "M13", "BUSINESS GenAI & n8n"),
    ("M14_Final_Project", "M14", "FINAL PROJECT"),
]


class ScriptExtractor(HTMLParser):
    """Parse an M##_Script.html and extract video titles, part titles, and script text."""

    def __init__(self):
        super().__init__()
        self.videos = []  # list of {title, parts: [{title, paragraphs}]}
        self.current_video = None
        self.current_part = None
        self.in_script_col = False
        self.in_p = False
        self.in_h2 = False
        self.in_segment_number = False
        self.in_segment_title = False
        self.skip_video = False
        self.depth_script_col = 0
        self.text_buf = ""
        self.seg_num = ""
        self.seg_title = ""

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        cls = attr_dict.get("class", "")

        # Detect video sections — skip TA-only
        if tag == "div" and "video-section" in cls:
            if attr_dict.get("data-ta-only") == "true" or attr_dict.get("data-script-export") == "false":
                self.skip_video = True
            else:
                self.skip_video = False
                self.current_video = {"title": "", "parts": []}

        # Video title
        if tag == "h2" and not self.skip_video:
            self.in_h2 = True
            self.text_buf = ""

        # Script column
        if tag == "div" and "script-col" in cls and not self.skip_video:
            self.in_script_col = True
            self.depth_script_col = 0

        if self.in_script_col and tag == "div":
            self.depth_script_col += 1

        # Paragraph inside script-col
        if tag == "p" and self.in_script_col:
            self.in_p = True
            self.text_buf = ""

        # Segment number and title
        if tag == "span" and "segment-number" in cls and not self.skip_video:
            self.in_segment_number = True
            self.seg_num = ""

        if tag == "span" and "segment-title" in cls and not self.skip_video:
            self.in_segment_title = True
            self.seg_title = ""

    def handle_endtag(self, tag):
        if tag == "h2" and self.in_h2:
            self.in_h2 = False
            if self.current_video is not None:
                # Clean the title — remove HTML entities and extra whitespace
                title = self.text_buf.strip()
                # Remove any "(TA)" or "Not Part of Script Export" markers
                if "Not Part of Script Export" in title or "(TA)" in title:
                    self.skip_video = True
                    self.current_video = None
                else:
                    self.current_video["title"] = title

        if tag == "p" and self.in_p:
            self.in_p = False
            if self.current_part is not None:
                text = self.text_buf.strip()
                if text:
                    self.current_part["paragraphs"].append(text)

        if tag == "div" and self.in_script_col:
            self.depth_script_col -= 1
            if self.depth_script_col <= 0:
                self.in_script_col = False

        if tag == "span" and self.in_segment_number:
            self.in_segment_number = False
            self.seg_num = self.text_buf.strip() if not hasattr(self, '_seg_num_buf') else self.seg_num

        if tag == "span" and self.in_segment_title:
            self.in_segment_title = False
            # Create a new part
            part_title = f"{self.seg_num}: {self.seg_title.strip()}"
            self.current_part = {"title": part_title, "paragraphs": []}
            if self.current_video is not None:
                self.current_video["parts"].append(self.current_part)

        # End of video section
        if tag == "div" and not self.skip_video and self.current_video is not None:
            # Check if this closes a video-section (heuristic: video has a title)
            pass

    def handle_data(self, data):
        if self.in_h2:
            self.text_buf += data
        if self.in_p and self.in_script_col:
            self.text_buf += data
        if self.in_segment_number:
            self.seg_num = data.strip()
        if self.in_segment_title:
            self.seg_title = data.strip()

    def handle_entityref(self, name):
        char = {"amp": "&", "lt": "<", "gt": ">", "quot": '"', "mdash": "—", "ndash": "–"}.get(name, f"&{name};")
        if self.in_h2:
            self.text_buf += char
        if self.in_p and self.in_script_col:
            self.text_buf += char

    def get_videos(self):
        """Finalize and return videos that have content."""
        # The parser accumulates videos as it encounters video-section divs
        # We need to collect them properly
        return [v for v in self.videos if v["title"] and v["parts"]]


def extract_scripts(html_path):
    """Extract video scripts from an HTML file using regex (more reliable than parser for this HTML)."""
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    videos = []

    # Find all video sections
    video_pattern = re.compile(
        r'<div\s+class="video-section[^"]*"[^>]*id="video-(\d+)"([^>]*)>(.*?)</div><!--\s*end\s+video-\d+',
        re.DOTALL
    )

    for m in video_pattern.finditer(html):
        vid_num = m.group(1)
        vid_attrs = m.group(2)
        vid_content = m.group(3)

        # Skip TA-only videos
        if 'data-ta-only="true"' in vid_attrs or 'data-script-export="false"' in vid_attrs:
            continue

        # Extract video title from h2
        h2_match = re.search(r"<h2>(.*?)</h2>", vid_content, re.DOTALL)
        if not h2_match:
            continue
        video_title = re.sub(r"<[^>]+>", "", h2_match.group(1)).strip()

        # Skip TA videos by title
        if "Not Part of Script Export" in video_title or "(TA)" in video_title:
            continue

        # Clean up title — remove "Video N: " prefix, we'll add our own
        video_title_clean = video_title

        parts = []

        # Find all segments
        seg_pattern = re.compile(
            r'<span\s+class="segment-number">(.*?)</span>\s*<span\s+class="segment-title">(.*?)</span>.*?'
            r'<div\s+class="script-col">(.*?)</div>\s*<div\s+class="media-col',
            re.DOTALL
        )

        for seg_m in seg_pattern.finditer(vid_content):
            part_num = seg_m.group(1).strip()
            part_title = seg_m.group(2).strip()
            script_html = seg_m.group(3)

            # Extract paragraphs from <p> tags
            paragraphs = []
            for p_match in re.finditer(r"<p>(.*?)</p>", script_html, re.DOTALL):
                text = p_match.group(1)
                # Strip HTML tags
                text = re.sub(r"<[^>]+>", "", text)
                # Clean whitespace
                text = re.sub(r"\s+", " ", text).strip()
                if text:
                    paragraphs.append(text)

            if paragraphs:
                parts.append({
                    "title": f"{part_num}: {part_title}",
                    "paragraphs": paragraphs,
                })

        if parts:
            videos.append({"title": video_title_clean, "parts": parts})

    return videos


def main():
    date_str = datetime.now().strftime("%B %d, %Y")
    output_lines = []
    output_lines.append("DADS 5250 \u2014 GENERATIVE AI IN PRACTICE")
    output_lines.append(f"Generated: {date_str}")
    output_lines.append("")

    for folder, mod_id, mod_title in MODULE_FOLDERS:
        script_path = os.path.join(SCRIPT_DIR, folder, f"{mod_id}_Script.html")
        if not os.path.exists(script_path):
            print(f"  Skipping {mod_id} — file not found: {script_path}")
            continue

        videos = extract_scripts(script_path)
        if not videos:
            print(f"  Skipping {mod_id} — no exportable videos found")
            continue

        output_lines.append("")
        output_lines.append("=" * 64)
        output_lines.append(f"MODULE {mod_id}: {mod_title}")
        output_lines.append("=" * 64)

        for video in videos:
            output_lines.append("")
            output_lines.append(video["title"])
            output_lines.append("")

            for i, part in enumerate(video["parts"]):
                output_lines.append(part["title"])
                output_lines.append("")
                for para in part["paragraphs"]:
                    output_lines.append(para)
                    output_lines.append("")
                if i < len(video["parts"]) - 1:
                    output_lines.append("---")
                    output_lines.append("")

        print(f"  {mod_id}: {len(videos)} videos exported")

    # Write output
    out_path = os.path.join(SCRIPT_DIR, "DADS5250_All_Scripts.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    print(f"\nExported to: {out_path}")
    print(f"Total lines: {len(output_lines)}")


if __name__ == "__main__":
    main()
