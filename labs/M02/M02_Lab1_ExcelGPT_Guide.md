![Module 2, Lab 1: Excel GPT](./assets/images/M02_Lab1_banner.png)

# Module 2, Lab 1: Excel GPT

Call an AI model directly from an Excel cell. You paste one block of VBA code
into your workbook and then use `=AI_Reply(...)` to send a prompt to the model
and get the answer back in the cell, right next to your data.

**Difficulty:** 2 of 3 stars &nbsp;·&nbsp; **Time:** about 15 minutes

---

## Platform note (read first)

This lab uses Excel VBA and is built for **Windows Excel (desktop)**, where it
works with no extra setup.

**Mac users:** Mac Excel cannot make the web request from VBA on its own (it
lacks the Windows components this uses), so the function returns an ActiveX
error. To run this on a Mac you need an extra one time AppleScript helper
(`VBA_HTTP.scpt`) installed, or you can use a Windows machine or lab computer.
Ask the instructor for the Mac setup if you need it.

---

## Get the code

- **VBA code:**
  [Open M02_Lab1_ExcelGPT_AI_Reply.bas](https://github.com/mdehghani86/DADS5250-GenAI/blob/main/labs/M02/M02_Lab1_ExcelGPT_AI_Reply.bas)
  Click it, then use the Copy button at the top right of the code box to copy all of it.

That is the only file for this lab. You use your own Excel workbook.

---

## Steps

### 1. Paste the code into your workbook

Open your Excel workbook and press `Alt + F11` to open the VBA editor. Choose
`Insert` then `Module`, and paste all of the code. Close the editor.

### 2. Use the function

`AI_Reply(key, prompt, [length], [model], [temperature])`

The simplest call, with your key and a prompt:

```
=AI_Reply("sk-your-key", "Write a professional thank you email")
```

A cleaner setup is to put your key in a cell (say B3) and reference it, so it is
not repeated in every formula:

```
=AI_Reply($B$3, B9)
=AI_Reply($B$3, B9, "Short", "gpt-4o", 0.5)
```

`length` can be `"Short"`, `"Medium"`, or `"Descriptive"`.

### 3. Try a range of use cases

Use it for formatting, data analysis, content creation, problem solving, data
cleaning, and translation. Fill in the answers, then write your own prompts.

---

## Keep your key safe

Your API key sits inside the workbook. Never share a workbook that still has
your key in it, and never upload your key to GitHub. Treat it like a password.

## A note on cost

Each `=AI_Reply(...)` cell calls the model when it recalculates. When you get an
answer you like, freeze it: copy the cell, then use Paste Special and choose
Values. The cell becomes plain text and will not call the model again.
