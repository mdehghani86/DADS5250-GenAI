' =====================================================================
'  Excel GPT  --  AI_Reply  (DADS 5250, Module 2 Lab 1)
'
'  Exact VBA from the Applied GenAI course workbook (ExcelGPT_v3),
'  combined into one module for easy pasting. The main function is
'  AI_Reply(). Everything else is its plumbing (HTTP + JSON helpers).
'
'  HOW TO USE
'    1. Open your Excel workbook and press Alt + F11 (VBA editor).
'    2. Insert > Module, then paste ALL of this code.
'    3. In any cell:  =AI_Reply("sk-your-key", "Say hello in French")
'       Full form:    =AI_Reply(key, prompt, [length], [model], [temperature])
'
'  PLATFORM: works on Windows Excel with no extra setup. On Mac it also
'  needs the AppleScript helper VBA_HTTP.scpt (see the lab guide).
' =====================================================================

' ===== modCompat.bas =====
Option Explicit

Public Function IsMac() As Boolean
    IsMac = (InStr(1, Application.OperatingSystem, "Mac", vbTextCompare) > 0)
End Function

Public Function PathJoin(ByVal a As String, ByVal b As String) As String
    Dim sep As String: sep = Application.PathSeparator
    If Right$(a, 1) = "\" Or Right$(a, 1) = "/" Or Right$(a, 1) = ":" Then
        PathJoin = a & b
    Else
        PathJoin = a & sep & b
    End If
End Function

' headers can be:
'  - String with lines:  "Name: Value" & vbLf & "Name2: Value2"
'  - Object with .Keys / .Item (Dictionary-like)
Public Function HttpPostJson(ByVal url As String, _
                             ByVal jsonBody As String, _
                             ByVal headers As Variant, _
                             Optional ByVal timeoutSec As Long = 60) As String
    If IsMac() Then
        HttpPostJson = Mac_HttpPostJson(url, jsonBody, headers, timeoutSec)
    Else
        HttpPostJson = Win_HttpPostJson(url, jsonBody, headers, timeoutSec)
    End If
End Function

Private Function Win_HttpPostJson(ByVal url As String, _
                                  ByVal jsonBody As String, _
                                  ByVal headers As Variant, _
                                  ByVal timeoutSec As Long) As String
    Dim http As Object, k As Variant, lines() As String, i As Long, p As Long
    On Error Resume Next
    Set http = CreateObject("WinHttp.WinHttpRequest.5.1")
    If http Is Nothing Then Set http = CreateObject("MSXML2.XMLHTTP")
    On Error GoTo 0
    If http Is Nothing Then
        Win_HttpPostJson = "{""error"":""No HTTP engine (WinHTTP/MSXML) available""}"
        Exit Function
    End If

    On Error GoTo EH
    http.Open "POST", url, False

    ' ---- set headers (string or object) ----
    If IsObject(headers) Then
        For Each k In headers.Keys
            http.setRequestHeader CStr(k), CStr(headers(k))
        Next k
    ElseIf VarType(headers) = vbString Then
        If Len(headers) > 0 Then
            lines = Split(headers, vbLf)
            For i = LBound(lines) To UBound(lines)
                If Len(Trim$(lines(i))) > 0 Then
                    p = InStr(1, lines(i), ":")
                    If p > 0 Then
                        http.setRequestHeader Trim$(Left$(lines(i), p - 1)), Trim$(Mid$(lines(i), p + 1))
                    End If
                End If
            Next i
        End If
    End If

    On Error Resume Next
    http.SetTimeouts 30000, 30000, CLng(timeoutSec) * 1000, CLng(timeoutSec) * 1000
    On Error GoTo EH

    http.send jsonBody

    If TypeName(http.Status) <> "Empty" Then
        If http.Status < 200 Or http.Status >= 300 Then
            Win_HttpPostJson = "{""error"":""HTTP " & http.Status & ": " & Replace(http.responseText, """", "'") & """}"
            Exit Function
        End If
    End If
    Win_HttpPostJson = http.responseText
    Exit Function
EH:
    Win_HttpPostJson = "{""error"":""HTTP error: " & Replace(Err.Description, """", "'") & """}"
End Function

Private Function Mac_HttpPostJson(ByVal url As String, _
                                  ByVal jsonBody As String, _
                                  ByVal headers As Variant, _
                                  ByVal timeoutSec As Long) As String
    Dim headerLines As String, k As Variant
    If IsObject(headers) Then
        For Each k In headers.Keys
            headerLines = headerLines & CStr(k) & ": " & CStr(headers(k)) & vbLf
        Next k
    ElseIf VarType(headers) = vbString Then
        headerLines = CStr(headers)
    End If

    Dim param As String
    param = url & vbLf & "<<<BODY>>>" & jsonBody & vbLf & "<<<HEADERS>>>" & headerLines & vbLf & "<<<TIMEOUT>>>" & CStr(timeoutSec)

    On Error GoTo Fail
    Mac_HttpPostJson = AppleScriptTask("VBA_HTTP.scpt", "httpPostJson", param)
    Exit Function
Fail:
    Mac_HttpPostJson = "{""error"":""AppleScriptTask failed: " & Replace(Err.Description, """", "'") & """}"
End Function


' ===== JsonLite.bas =====

' Extracts the first Chat Completions message content without external refs.
' Returns "" if not found.
Public Function ChatContentFromResponse(ByVal raw As String) As String
    ' Look for: "choices":[{..."message":{"content":"..."}...}]
    Dim iChoices As Long, iMsg As Long, iContent As Long
    Dim startQ As Long, endQ As Long, s As String

    iChoices = InStr(1, raw, """choices""", vbTextCompare)
    If iChoices = 0 Then Exit Function

    iMsg = InStr(iChoices, raw, """message""", vbTextCompare)
    If iMsg = 0 Then Exit Function

    iContent = InStr(iMsg, raw, """content""", vbTextCompare)
    If iContent = 0 Then Exit Function

    ' Find the first quote after "content":
    startQ = InStr(iContent, raw, ":")
    If startQ = 0 Then Exit Function
    startQ = InStr(startQ + 1, raw, """")
    If startQ = 0 Then Exit Function
    ' Now find the matching closing quote accounting for escapes
    endQ = FindJsonStringEnd(raw, startQ + 1)
    If endQ = 0 Then Exit Function

    s = Mid$(raw, startQ + 1, endQ - startQ - 1)
    ChatContentFromResponse = JsonUnescape(s)
End Function

' Finds the end quote of a JSON string, handling backslash escapes
Private Function FindJsonStringEnd(ByVal txt As String, ByVal startPos As Long) As Long
    Dim i As Long, ch As String, esc As Boolean
    For i = startPos To Len(txt)
        ch = Mid$(txt, i, 1)
        If esc Then
            esc = False
        ElseIf ch = "\" Then
            esc = True
        ElseIf ch = """" Then
            FindJsonStringEnd = i
            Exit Function
        End If
    Next i
End Function

' Unescape a subset of JSON escapes
Private Function JsonUnescape(ByVal s As String) As String
    s = Replace(s, "\""", """")
    s = Replace(s, "\\", "\")
    s = Replace(s, "\/", "/")
    s = Replace(s, "\b", vbBack)
    s = Replace(s, "\f", vbFormFeed)
    s = Replace(s, "\n", vbLf)
    s = Replace(s, "\r", vbCr)
    s = Replace(s, "\t", vbTab)
    ' \uXXXX left as-is (Excel cell display normally OK). Add a decoder if needed.
    JsonUnescape = s
End Function

' Simple JSON string wrapper/escaper for request bodies
Public Function JsonString(ByVal s As String) As String
    s = Replace(s, "\", "\\")
    s = Replace(s, """", "\""")
    s = Replace(s, vbCrLf, "\n")
    s = Replace(s, vbCr, "\n")
    s = Replace(s, vbLf, "\n")
    JsonString = """" & s & """"
End Function

' ===== modAI.bas =====

Public Function AI_Reply(ByVal API_key As String, _
                         ByVal Prompt As String, _
                         Optional ByVal Length As String = "Short", _
                         Optional ByVal Model As String = "gpt-4o", _
                         Optional ByVal Temperature As Double = 0.7) As String
    On Error GoTo Fail

    If Len(API_key) = 0 Then
        AI_Reply = "ERROR: Missing API key."
        Exit Function
    End If
    If Len(Prompt) = 0 Then
        AI_Reply = "ERROR: Prompt cannot be empty."
        Exit Function
    End If
    If Temperature < 0 Or Temperature > 1 Then Temperature = 0.7

    Dim systemPrompt As String
    Select Case UCase$(Length)
        Case "SHORT":        systemPrompt = "You are a helpful Excel assistant. Provide very concise answers."
        Case "MEDIUM":       systemPrompt = "You are a helpful Excel assistant. Be concise but explain when useful."
        Case "DESCRIPTIVE":  systemPrompt = "You are a helpful Excel assistant. Provide detailed, example-rich answers."
        Case Else:           systemPrompt = "You are a helpful Excel assistant. Provide very concise answers."
    End Select

    Dim body As String
    body = "{""model"":" & JsonString(Model) & "," & _
           """messages"":[{""role"":""system"",""content"":" & JsonString(systemPrompt) & "}," & _
                          "{""role"":""user"",""content"":" & JsonString(Prompt) & "}]," & _
           """temperature"":" & Replace(CStr(Temperature), ",", ".") & "," & _
           """max_tokens"":1000}"

    ' ---- headers as a simple string (cross-platform) ----
    Dim headerLines As String
    headerLines = "Content-Type: application/json" & vbLf & _
                  "Authorization: Bearer " & API_key

    Dim raw As String
    raw = HttpPostJson("https://api.openai.com/v1/chat/completions", body, headerLines, 60)

    If InStr(1, raw, "{""error"":", vbTextCompare) = 1 Then
        AI_Reply = "ERROR: " & raw
        Exit Function
    End If

    Dim content As String
    content = ChatContentFromResponse(raw)
    If Len(content) = 0 Then
        AI_Reply = "ERROR: Could not parse response. Raw: " & raw
    Else
        AI_Reply = content
    End If
    Exit Function

Fail:
    AI_Reply = "ERROR: " & Err.Description
End Function


Sub Test_PostmanEcho()
    Dim result As String, body As String, headers As String
    body = "{""hello"":""world""}"
    headers = "Content-Type: application/json"
    result = AppleScriptTask("VBA_HTTP.scpt", "httpPostJson", _
              "https://postman-echo.com/post" & vbLf & "<<<BODY>>>" & body & _
              vbLf & "<<<HEADERS>>>" & headers & vbLf & "<<<TIMEOUT>>>10")
    MsgBox Left$(result, 400)
End Sub
