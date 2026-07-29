![Module 2, Lab 1: Excel GPT](./assets/M02_Lab1_banner.png)

# Module 2, Lab 1: Excel GPT

Build an AI assistant that lives inside Excel. Instead of writing code in a
notebook, you paste one VBA module into Excel and then talk to an AI model
directly from your spreadsheet cells.

**Difficulty:** 2 of 3 stars &nbsp;·&nbsp; **Time:** about 15 minutes

---

## What you will build

By the end you can type functions like these into any cell and get answers
back from the AI:

- `=GPT("...")` ask the AI anything
- `=GPT_ASK("question", A1:E13)` ask a question about your data
- `=GPT_CALC("instruction", C2:C13)` let the AI do the math and return a number

---

## What you need

- Microsoft Excel for Windows or Mac, the desktop version. The browser version
  of Excel does not run VBA, so it will not work for this lab.
- Your own OpenAI API key.

---

## Download the files

Grab both files first, then follow the steps below.

- **Starter workbook (Excel):**
  [Download M02_Lab1_ExcelGPT_Starter.xlsx](https://github.com/mdehghani86/DADS5250-GenAI/raw/main/labs/M02/M02_Lab1_ExcelGPT_Starter.xlsx)
  This link downloads the file straight to your computer. Open it in Excel.
- **VBA code:**
  [Open ExcelGPT.bas](https://github.com/mdehghani86/DADS5250-GenAI/blob/main/labs/M02/ExcelGPT.bas)
  Click it, then use the Copy button at the top right of the code box to copy all of it.

Both files also live in the `labs/M02` folder of this repository if you prefer
to browse there.

---

## Steps

### 1. Fill in the Student Info tab

Open `M02_Lab1_ExcelGPT_Starter.xlsx`. It opens on the **Student Info** tab.
Type your first name, last name, and student ID in the highlighted cells, then
read and sign the Declaration of Completion.

### 2. Load the VBA and add your key on the Setup tab

Go to the **Setup** tab and follow the steps there:

1. Press `Alt + F11` to open the VBA editor.
2. Choose `Insert` then `Module`.
3. Open `ExcelGPT.bas`, copy all of it, and paste it into the module.
4. Close the editor and return to the Setup tab.
5. Paste your OpenAI key into the highlighted key cell. The functions read your
   key from that cell automatically, so you do not need to edit the code.

There is also a **Model** cell just below the key. It is set to `gpt-4.1-mini`,
which is fast and cheap. You can change it to a different model whenever you
want, and the functions will use whatever is in that cell. Leave it as is if
you are not sure.

### 3. Run the examples

Go to any use case tab (Sales, Regression, Reviews, Classify, Ask Anything) and
press `Ctrl + Alt + F9` to recalculate. The example cells now return real
answers from the AI. They show `#NAME?` until the VBA is loaded and your key is
in place, which is expected. Change a question and watch the answer change.

### 4. The AskSelection macro (optional)

Select a range of cells, then run the `AskSelection` macro. Type a question in
the box and the answer appears in a pop up. This is a quick way to ask about
data without typing a formula.

---

## Your exercise

Open the VBA editor and find the function called `GPT_MY_FUNCTION`. Turn it into
a new tool of your own by writing a role in the system line and renaming it.
A few ideas:

- `GPT_TRANSLATE(text, "Spanish")` translates text into another language
- `GPT_EMAIL(bulletPoints)` turns notes into a polished email
- `GPT_CLASSIFY(text)` labels text as positive or negative

Test your new function on one of the tabs and note what you changed.

---

## Keep your key safe

Your API key sits inside the workbook. Never share a workbook that still has
your key in it, and never upload your key to GitHub. Treat it like a password.

## A note on cost (important)

Every cell that uses one of these functions calls the AI each time it
recalculates. Two things to keep in mind:

- Pressing `Ctrl + Alt + F9` runs a full recalculation, which re-runs **every**
  AI cell on the sheet at once and charges you for all of them. Copying a
  formula down hundreds of rows means hundreds of calls.
- When you get an answer you like, **freeze it**: copy the cell, then use
  Paste Special and choose Values. The cell becomes plain text and will never
  call the AI again. This is the simplest way to control your cost.

Start small while you are learning.
