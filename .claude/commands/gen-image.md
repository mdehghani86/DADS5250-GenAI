---
description: "Generate image(s) using NanoBanana MCP (Gemini) for DADS 5250 course materials"
---

Generate image(s) using the NanoBanana MCP server (Gemini image models) for the DADS 5250 course.

The user will describe what image they want. Use the NanoBanana MCP tools:

## Steps

1. **Set aspect ratio** first: call `mcp__nanobanana-mcp__set_aspect_ratio` with the appropriate ratio
   - Default for slides/headers: `16:9`
   - Default for lab thumbnails: `4:3`
   - Default for icons/badges: `1:1`
   - Ask user if unclear

2. **Generate the image**: call `mcp__nanobanana-mcp__gemini_generate_image` with:
   - `prompt`: The user's description, enhanced with quality keywords
   - `output_path`: Save to `C:/Users/mdehg/Dropbox/5_Courses/DADS5250-GenAI/images/[descriptive-name].png`

3. **Show the result**: Open the image for the user to review

## Prompt Enhancement Tips

For DADS 5250 course images, enhance prompts with:
- **Slide backgrounds**: "Ultra high resolution 4K, clean modern design, subtle gradient, professional academic aesthetic, no text, no logos"
- **Lab illustrations**: "Clean vector illustration, modern flat design, vibrant yet professional colors, tech/AI theme"
- **Concept diagrams**: "Technical diagram style, clean lines, labeled components, white background, professional"
- **Course branding**: Use Northeastern blue (#001a70) and accent blue (#0055d4) when relevant

## File Naming

Save as: `images/[module]-[description].png`
Examples:
- `images/m05-rag-architecture.png`
- `images/slide-ai-agents-hero.png`
- `images/m09-vision-multimodal.png`

If multiple images requested, add 3s delay between each. Create a picker if user wants to compare options.
