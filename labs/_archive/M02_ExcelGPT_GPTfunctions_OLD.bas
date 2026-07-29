' =====================================================================
'  Excel GPT      DADS 5250: Generative AI in Practice
' =====================================================================
'
'  THE BIG IDEA
'  In the notebook, Python was the one talking to the AI. Here the
'  roles flip. Excel itself becomes the client that talks to the AI.
'  You type a function like =GPT(...) into a cell, and behind the
'  scenes your spreadsheet sends your request over the internet to
'  the model and writes the answer straight back into the cell.
'
'  In other words, you are giving Excel a brain. Any cell can now ask
'  a question in plain English and get an answer.
'
'  HOW IT WORKS IN ONE SENTENCE
'  Every function below builds a small message, sends it to OpenAI
'  over the web, waits for the reply, and returns the text.
'
'  ---------------------------------------------------------------
'  SETUP (you only do this once)
'  ---------------------------------------------------------------
'    1. In Excel, press  Alt + F11  to open the VBA editor.
'    2. From the menu choose  Insert  then  Module.
'    3. Paste this entire file into the empty module window.
'    4. Find the API_KEY line just below and put your own key there.
'    5. Close the editor. You can now use the functions in any cell.
'
'  ---------------------------------------------------------------
'  KEEP YOUR KEY SAFE (please read this)
'  ---------------------------------------------------------------
'    This is a teaching demo, so the key is stored right inside the
'    workbook. Two rules follow from that:
'      - Never send someone a workbook that still has your key in it.
'      - Never commit your real key to GitHub. Treat it like a
'        password, because that is exactly what it is.
'
'  ---------------------------------------------------------------
'  A NOTE ABOUT COST
'  ---------------------------------------------------------------
'    Every cell that uses one of these functions calls the AI again
'    each time the sheet recalculates. If you copy =GPT(...) down
'    500 rows, that is 500 separate calls. Start small while you
'    are learning so the cost stays tiny.
' =====================================================================


' ---------------------------------------------------------------------
'  SETTINGS
'  You have two easy ways to provide your OpenAI key:
'    (a) In the starter workbook, type it into the highlighted cell on
'        the Setup tab. The code reads it from there automatically.
'    (b) Or paste it into the API_KEY line below.
'  Option (a) is used first whenever that cell has a key in it.
' ---------------------------------------------------------------------
Private Const API_KEY As String = "sk-REPLACE_WITH_YOUR_KEY"   ' fallback key, used only if the Setup tab is empty
Private Const API_URL As String = "https://api.openai.com/v1/chat/completions"  ' the address we send requests to
Private Const MODEL   As String = "gpt-4.1-mini"               ' which AI model answers you


' ---------------------------------------------------------------------
'  GetKey
'  Returns your API key. It first looks in the Setup tab (cell C7) of
'  the starter workbook. If that cell is empty, or you are using your
'  own workbook that has no Setup tab, it falls back to the API_KEY
'  constant above.
' ---------------------------------------------------------------------
Private Function GetKey() As String
    Dim k As String
    k = ""
    On Error Resume Next
    k = Trim(CStr(ThisWorkbook.Worksheets("Setup").Range("C7").Value))
    On Error GoTo 0
    If k = "" Then k = API_KEY
    GetKey = k
End Function


' ---------------------------------------------------------------------
'  GetModel
'  Returns which AI model to use. It first looks in the Setup tab
'  (cell C8) so you can switch models without touching the code. For
'  example, type gpt-4.1-mini for speed or a larger model for depth.
'  If that cell is empty, it falls back to the MODEL constant above.
' ---------------------------------------------------------------------
Private Function GetModel() As String
    Dim m As String
    m = ""
    On Error Resume Next
    m = Trim(CStr(ThisWorkbook.Worksheets("Setup").Range("C8").Value))
    On Error GoTo 0
    If m = "" Then m = MODEL
    GetModel = m
End Function


' =====================================================================
'  THE ENGINE
'  This is the single function that actually talks to the AI. Every
'  cell function further down hands its request to this one. You do
'  not normally need to change anything in here, but the comments walk
'  through each step so you can see what is really happening.
'
'  It takes two pieces of text:
'    systemMsg  the AI's job description (its role and rules)
'    userMsg    the actual question or task from the user
'  and it returns the AI's written answer.
' =====================================================================
Private Function CallOpenAI(systemMsg As String, userMsg As String, _
                            Optional maxTokens As Long = 400, _
                            Optional temperature As Double = 0.2) As String
    Dim http As Object, body As String

    ' STEP 1. Build the request as a block of JSON text.
    ' JSON is just the agreed format that OpenAI expects. We are
    ' packing four things into it: the model to use, how creative the
    ' answer may be (temperature), a length limit (max_tokens), and the
    ' two messages (the system role and the user question). The messy
    ' looking double quotes are there because every quote inside JSON
    ' has to be written as "" so Excel keeps it as part of the text.
    body = "{""model"":""" & GetModel() & """," & _
           """temperature"":" & Replace(CStr(temperature), ",", ".") & "," & _
           """max_tokens"":" & maxTokens & "," & _
           """messages"":[" & _
             "{""role"":""system"",""content"":""" & JsonEscape(systemMsg) & """}," & _
             "{""role"":""user"",""content"":""" & JsonEscape(userMsg) & """}]}"

    On Error GoTo Fail

    ' STEP 2. Create the little web browser object that VBA uses to send
    ' requests over the internet. (WinHttp.WinHttpRequest.5.1 would also
    ' work if this line ever gives you trouble.)
    Set http = CreateObject("MSXML2.ServerXMLHTTP.6.0")

    ' STEP 3. Open a connection to OpenAI. "POST" means we are sending
    ' data to them, and False means Excel waits here until the answer
    ' comes back before moving on.
    http.Open "POST", API_URL, False

    ' STEP 4. Attach two headers. The first tells OpenAI we are sending
    ' JSON. The second is your key, which proves the request is really
    ' from you and is allowed to use your account.
    http.setRequestHeader "Content-Type", "application/json"
    http.setRequestHeader "Authorization", "Bearer " & GetKey()

    ' STEP 5. Send the request and wait for the reply.
    http.send body

    ' STEP 6. Check whether it worked. A status of 200 means success.
    ' Anything else is an error (a bad key, no internet, or a typo), so
    ' we return a short message instead of a wrong answer.
    If http.Status <> 200 Then
        CallOpenAI = "ERROR " & http.Status & ": " & Left(http.responseText, 200)
        Exit Function
    End If

    ' STEP 7. The reply is one big block of JSON. Pull the answer text
    ' out of it and hand it back to the cell.
    CallOpenAI = ExtractContent(http.responseText)
    Exit Function

Fail:
    ' If anything above breaks, show the reason instead of crashing.
    CallOpenAI = "ERROR: " & Err.Description
End Function


' =====================================================================
'  THE FUNCTIONS YOU USE IN CELLS
'  Each one is short on purpose. It sets the AI's role in the first
'  line, then passes your text to the engine above. Notice how the only
'  real difference between them is the role we give the AI.
' =====================================================================

' ---------------------------------------------------------------------
'  1) GPT
'  The simplest one. Ask the AI absolutely anything and get a short
'  answer back. Think of it as a chat box that lives in a cell.
'
'    =GPT("Write a one line summary of strong Q4 electronics sales")
'    =GPT("Give me 3 KPIs a sales manager should track")
' ---------------------------------------------------------------------
Public Function GPT(prompt As String) As String
    GPT = CallOpenAI("You are a helpful assistant. Answer concisely.", prompt)
End Function


' ---------------------------------------------------------------------
'  2) GPT_ASK
'  Ask a question about a range of your own data. You give it the
'  question and the cells, and it reads the numbers before answering.
'  The role tells the AI to rely only on the table you handed it, so it
'  does not make things up.
'
'    =GPT_ASK("Which product category earns the most?", A1:E13)
'    =GPT_ASK("Are any months unusual?", A1:E13)
' ---------------------------------------------------------------------
Public Function GPT_ASK(question As String, data As Range) As String
    Dim sys As String
    sys = "You are a data analyst. Use ONLY the table provided to answer. " & _
          "Be specific and concise."
    GPT_ASK = CallOpenAI(sys, "Table:" & vbLf & RangeToText(data) & _
                              vbLf & vbLf & "Question: " & question)
End Function


' ---------------------------------------------------------------------
'  3) GPT_CALC
'  Let the AI do the arithmetic and return only a number, so the result
'  drops cleanly into a cell. The role forces a bare number with no
'  words, no units, and no formula around it.
'
'    =GPT_CALC("total revenue", C2:C13)
'    =GPT_CALC("average units sold for Electronics", A2:E13)
'    =GPT_CALC("percent of months with revenue over 45000", C2:C13)
' ---------------------------------------------------------------------
Public Function GPT_CALC(instruction As String, data As Range) As String
    Dim sys As String
    sys = "You are a calculator. Compute the requested value from the table. " & _
          "Return ONLY the final number, with no words, no units, and no formula."
    GPT_CALC = CallOpenAI(sys, "Table:" & vbLf & RangeToText(data) & _
                               vbLf & vbLf & "Compute: " & instruction, 50, 0)
End Function


' ---------------------------------------------------------------------
'  YOUR TURN
'  This is the fun part and the whole point of the exercise. Copy the
'  same pattern from the functions above: choose a role for the AI in
'  the system line, pass the user text, and return CallOpenAI(...).
'
'  A few ideas to get you started:
'     - GPT_TRANSLATE(text, "Spanish")     turns text into another language
'     - GPT_EMAIL(bulletPoints)            turns notes into a polished email
'     - GPT_CLASSIFY(text)                 labels text positive or negative
'     - GPT_EXPLAIN(formula)               explains a formula in plain English
'
'  Fill in the blank role below, rename the function, and try it.
' ---------------------------------------------------------------------
Public Function GPT_MY_FUNCTION(userText As String) As String
    Dim sys As String
    sys = "You are a ______."              ' describe the AI's job here
    GPT_MY_FUNCTION = CallOpenAI(sys, userText)
End Function


' =====================================================================
'  BONUS MACRO
'  A macro is different from the functions above. Instead of living in
'  a cell, you run it like a button. Select some data first, run this,
'  type a question, and the answer appears in a pop up box. This is a
'  nice way to demo Excel GPT without typing a formula.
' =====================================================================
Public Sub AskSelection()
    Dim q As String, ans As String

    ' Ask the user for their question in a small dialog box.
    q = InputBox("Ask the AI about the selected cells:", "Excel GPT")
    If q = "" Then Exit Sub          ' if they clicked Cancel or typed nothing, stop

    ' Send the highlighted cells plus the question to the AI.
    ans = CallOpenAI("You are a data analyst. Use only the provided table.", _
                     "Table:" & vbLf & RangeToText(Selection) & _
                     vbLf & vbLf & "Question: " & q)

    ' Show the answer in a message box.
    MsgBox ans, vbInformation, "Excel GPT"
End Sub


' =====================================================================
'  HELPERS
'  These three do the plumbing so the functions above can stay short.
'  You do not need to edit them, but here is what each one is for.
' =====================================================================

' RangeToText
' The AI cannot read Excel cells directly, so before we send your data
' we copy it into one plain block of text, one row per line with the
' columns separated by tabs. That is what this function does.
Private Function RangeToText(rng As Range) As String
    Dim r As Range, cell As Range, rowText As String, out As String
    For Each r In rng.Rows
        rowText = ""
        For Each cell In r.Cells
            rowText = rowText & CStr(cell.Value) & vbTab
        Next cell
        out = out & RTrim(rowText) & vbLf
    Next r
    RangeToText = out
End Function

' JsonEscape
' Certain characters (quotes, backslashes, line breaks) have a special
' meaning inside JSON. If we sent them as is, they would break the
' request. This function swaps each one for its safe version so your
' text arrives at OpenAI exactly as you wrote it.
Private Function JsonEscape(s As String) As String
    s = Replace(s, "\", "\\")
    s = Replace(s, """", "\""")
    s = Replace(s, vbCrLf, "\n")
    s = Replace(s, vbCr, "\n")
    s = Replace(s, vbLf, "\n")
    s = Replace(s, vbTab, "\t")
    JsonEscape = s
End Function

' ExtractContent
' OpenAI does not reply with just the answer. It replies with a large
' JSON block, and the answer we want is tucked inside a field called
' "content". VBA has no built in JSON reader, so this function walks
' through the text, finds that field, and copies out the answer while
' turning the escape codes (like \n) back into real line breaks.
Private Function ExtractContent(json As String) As String
    Dim p As Long, i As Long, ch As String, out As String, esc As Boolean

    ' Find where the "content" field begins.
    p = InStr(json, """content""")
    If p = 0 Then ExtractContent = json: Exit Function

    ' Move forward to the opening quote of the answer text.
    p = InStr(p, json, ":") + 1
    Do While p <= Len(json) And Mid(json, p, 1) <> """"
        p = p + 1
    Loop
    p = p + 1

    ' Read the answer one character at a time until the closing quote,
    ' converting the escape codes back into normal characters as we go.
    esc = False
    For i = p To Len(json)
        ch = Mid(json, i, 1)
        If esc Then
            Select Case ch
                Case "n": out = out & vbLf     ' \n becomes a new line
                Case "t": out = out & vbTab    ' \t becomes a tab
                Case "r": ' ignore
                Case Else: out = out & ch
            End Select
            esc = False
        ElseIf ch = "\" Then
            esc = True                          ' the next character is escaped
        ElseIf ch = """" Then
            Exit For                            ' reached the closing quote, done
        Else
            out = out & ch
        End If
    Next i

    ExtractContent = out
End Function
