' =====================================================================
'  Excel GPT  --  DADS 5250: Generative AI in Practice
'  Call a large language model DIRECTLY from inside Excel using VBA.
'
'  Instead of the notebook asking the AI for you, here EXCEL is the
'  client: you type =GPT(...) in a cell and the spreadsheet talks to
'  the model itself.
'
'  ---------------------------------------------------------------
'  SETUP (one time)
'  ---------------------------------------------------------------
'    1. In Excel press  Alt + F11  to open the VBA editor
'    2. Insert  >  Module
'    3. Paste this ENTIRE file into the module
'    4. Put your OpenAI API key in API_KEY below
'    5. Close the editor. Now use the functions in any cell.
'
'  ---------------------------------------------------------------
'  SECURITY  (read this)
'  ---------------------------------------------------------------
'    This is a teaching demo. Your API key lives inside the workbook.
'    - Never share a workbook that still has your real key in it.
'    - Never commit your real key to GitHub. Treat it like a password.
'
'  ---------------------------------------------------------------
'  COST NOTE
'  ---------------------------------------------------------------
'    Each cell that uses one of these functions calls the API every
'    time it recalculates. Copy =GPT(...) down 500 rows = 500 calls.
'    Keep an eye on it while experimenting.
' =====================================================================

Private Const API_KEY As String = "sk-REPLACE_WITH_YOUR_KEY"
Private Const API_URL As String = "https://api.openai.com/v1/chat/completions"
Private Const MODEL   As String = "gpt-4.1-mini"


' =====================================================================
'  CORE  --  every function below calls this one helper.
'  It sends a system + user message to the API and returns the reply.
'  (You normally do not need to change this.)
' =====================================================================
Private Function CallOpenAI(systemMsg As String, userMsg As String, _
                            Optional maxTokens As Long = 400, _
                            Optional temperature As Double = 0.2) As String
    Dim http As Object, body As String

    body = "{""model"":""" & MODEL & """," & _
           """temperature"":" & Replace(CStr(temperature), ",", ".") & "," & _
           """max_tokens"":" & maxTokens & "," & _
           """messages"":[" & _
             "{""role"":""system"",""content"":""" & JsonEscape(systemMsg) & """}," & _
             "{""role"":""user"",""content"":""" & JsonEscape(userMsg) & """}]}"

    On Error GoTo Fail
    Set http = CreateObject("MSXML2.ServerXMLHTTP.6.0")   ' WinHttp.WinHttpRequest.5.1 also works
    http.Open "POST", API_URL, False
    http.setRequestHeader "Content-Type", "application/json"
    http.setRequestHeader "Authorization", "Bearer " & API_KEY
    http.send body

    If http.Status <> 200 Then
        CallOpenAI = "ERROR " & http.Status & ": " & Left(http.responseText, 200)
        Exit Function
    End If

    CallOpenAI = ExtractContent(http.responseText)
    Exit Function
Fail:
    CallOpenAI = "ERROR: " & Err.Description
End Function


' =====================================================================
'  THE FUNCTIONS  --  use these in any cell
' =====================================================================

' ---------------------------------------------------------------------
'  1) GPT  --  ask the AI anything
'     =GPT("Write a one-line summary of strong Q4 electronics sales")
'     =GPT("Give me 3 KPIs a sales manager should track")
' ---------------------------------------------------------------------
Public Function GPT(prompt As String) As String
    GPT = CallOpenAI("You are a helpful assistant. Answer concisely.", prompt)
End Function


' ---------------------------------------------------------------------
'  2) GPT_ASK  --  ask a question ABOUT a range of your data
'     =GPT_ASK("Which product category earns the most?", A1:E13)
'     =GPT_ASK("Any months that look like outliers?", A1:E13)
' ---------------------------------------------------------------------
Public Function GPT_ASK(question As String, data As Range) As String
    Dim sys As String
    sys = "You are a data analyst. Use ONLY the table provided to answer. " & _
          "Be specific and concise."
    GPT_ASK = CallOpenAI(sys, "Table:" & vbLf & RangeToText(data) & _
                              vbLf & vbLf & "Question: " & question)
End Function


' ---------------------------------------------------------------------
'  3) GPT_CALC  --  let the AI do the math and return JUST a number
'     =GPT_CALC("total revenue", C2:C13)
'     =GPT_CALC("average units sold for Electronics", A2:E13)
'     =GPT_CALC("percent of months with revenue over 45000", C2:C13)
' ---------------------------------------------------------------------
Public Function GPT_CALC(instruction As String, data As Range) As String
    Dim sys As String
    sys = "You are a calculator. Compute the requested value from the table. " & _
          "Return ONLY the final number -- no words, no units, no formula."
    GPT_CALC = CallOpenAI(sys, "Table:" & vbLf & RangeToText(data) & _
                               vbLf & vbLf & "Compute: " & instruction, 50, 0)
End Function


' ---------------------------------------------------------------------
'  YOUR TURN  --  build your own AI function (this is the fun part)
'  Copy the pattern: pick a "system" personality, pass the user text,
'  return CallOpenAI(...). Ideas to try:
'     - GPT_TRANSLATE(text, "Spanish")
'     - GPT_EMAIL(bulletPoints)      -> polished email
'     - GPT_CLASSIFY(text, "positive/negative/neutral")
'     - GPT_EXPLAIN(formula)         -> plain-English explanation
' ---------------------------------------------------------------------
Public Function GPT_MY_FUNCTION(input As String) As String
    Dim sys As String
    sys = "You are a ______."                 ' <-- describe the AI's job
    GPT_MY_FUNCTION = CallOpenAI(sys, input)
End Function


' =====================================================================
'  BONUS MACRO  --  ask about the cells you have selected.
'  Select a data range, run this macro (or assign it to a button),
'  type your question, and the answer pops up.
' =====================================================================
Public Sub AskSelection()
    Dim q As String, ans As String
    q = InputBox("Ask the AI about the selected cells:", "Excel GPT")
    If q = "" Then Exit Sub
    ans = CallOpenAI("You are a data analyst. Use only the provided table.", _
                     "Table:" & vbLf & RangeToText(Selection) & _
                     vbLf & vbLf & "Question: " & q)
    MsgBox ans, vbInformation, "Excel GPT"
End Sub


' =====================================================================
'  HELPERS  --  you do not need to edit these
' =====================================================================

' Turn a Range into a simple text table for the prompt.
Private Function RangeToText(rng As Range) As String
    Dim row As Range, cell As Range, line As String, out As String
    For Each row In rng.Rows
        line = ""
        For Each cell In row.Cells
            line = line & CStr(cell.Value) & vbTab
        Next cell
        out = out & RTrim(line) & vbLf
    Next row
    RangeToText = out
End Function

' Escape a string so it is safe inside the JSON request body.
Private Function JsonEscape(s As String) As String
    s = Replace(s, "\", "\\")
    s = Replace(s, """", "\""")
    s = Replace(s, vbCrLf, "\n")
    s = Replace(s, vbCr, "\n")
    s = Replace(s, vbLf, "\n")
    s = Replace(s, vbTab, "\t")
    JsonEscape = s
End Function

' Pull the assistant's message text out of the JSON response.
Private Function ExtractContent(json As String) As String
    Dim p As Long, i As Long, ch As String, out As String, esc As Boolean
    p = InStr(json, """content""")
    If p = 0 Then ExtractContent = json: Exit Function
    p = InStr(p, json, ":") + 1
    Do While p <= Len(json) And Mid(json, p, 1) <> """"    ' skip to opening quote
        p = p + 1
    Loop
    p = p + 1
    esc = False
    For i = p To Len(json)
        ch = Mid(json, i, 1)
        If esc Then
            Select Case ch
                Case "n": out = out & vbLf
                Case "t": out = out & vbTab
                Case "r": ' ignore
                Case Else: out = out & ch
            End Select
            esc = False
        ElseIf ch = "\" Then
            esc = True
        ElseIf ch = """" Then
            Exit For
        Else
            out = out & ch
        End If
    Next i
    ExtractContent = out
End Function
