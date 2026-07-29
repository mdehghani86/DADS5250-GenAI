![Module 2, Lab 1: Excel GPT](./assets/images/M02_Lab1_banner.png)

# Module 2, Lab 1: Excel GPT

Call an AI model directly from an Excel cell. You use one function,
`=AI_Reply(...)`, to send a prompt to the model and get the answer back in the
cell, right next to your data.

**Difficulty:** 2 of 3 stars &nbsp;·&nbsp; **Time:** about 15 minutes

---

## Platform note (read first)

This lab uses Excel VBA and is built for **Windows Excel (desktop)**, where it
works with no extra setup.

**Mac users:** Mac Excel cannot make the web request from VBA on its own (it
lacks the Windows components this uses), so the function will return an ActiveX
error. To run this lab on a Mac you need an extra one time AppleScript helper
installed, or you can use a Windows machine or lab computer. Ask the instructor
for the Mac setup if you need it.

---

## What you will do

- Put your OpenAI API key into the workbook.
- Use `=AI_Reply(key, prompt)` to get AI answers directly in cells.
- Complete a set of sample prompts (formatting, data analysis, content
  creation, problem solving, data cleaning, translation), then try your own.

---

## Download the file

- **Workbook:**
  [Download M02_Lab1_ExcelGPT.xlsm](https://github.com/mdehghani86/DADS5250-GenAI/raw/main/labs/M02/M02_Lab1_ExcelGPT.xlsm)

This is a macro enabled workbook (`.xlsm`); the AI code is already inside it, so
there is nothing to paste.

---

## Steps

### 1. Open the workbook and enable macros

Open `M02_Lab1_ExcelGPT.xlsm` in Excel. When Excel warns about macros, click
**Enable Content** (or Enable Macros). The code will not run otherwise.

### 2. Add your key and settings on the AI_Reply sheet

Go to the **AI_Reply** sheet and fill in the top cells:

- **B3** — your OpenAI API key (replace `PASTE_YOUR_OPENAI_KEY_HERE`)
- **B4** — the model (default `gpt-4o`)
- **B5** — the temperature (default `0.5`)

### 3. Use the function

In the **Result** column, call the function on the prompt in that row. The
simplest form is:

```
=AI_Reply($B$3, B9)
```

You can also pass the length, model, and temperature:

```
=AI_Reply($B$3, B9, "Short", $B$4, $B$5)
```

`AI_Reply(key, prompt, [length], [model], [temperature])` — length can be
`"Short"`, `"Medium"`, or `"Descriptive"`.

### 4. Complete the samples, then try your own

Fill the Result column for each sample prompt, then add a row with your own
prompt and see what the model returns.

---

## Keep your key safe

Your API key sits inside the workbook. Never share a workbook that still has
your key in it, and never upload your key to GitHub. Treat it like a password.

## A note on cost

Each `=AI_Reply(...)` cell calls the model when it recalculates. When you get an
answer you like, freeze it: copy the cell, then use Paste Special and choose
Values. The cell becomes plain text and will not call the model again.
