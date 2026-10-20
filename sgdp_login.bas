Attribute VB_Name = "SGDPLogin"
Option Explicit

Public CurrentUser As String
Public CurrentRole As String

Public Sub Auto_Open()
    ProtectLoginSheet
End Sub

Public Sub Login()
    Dim wsUsers As Worksheet, wsLogin As Worksheet
    Dim lastRow As Long, row As Long
    Dim username As String, password As String
    Dim storedPassword As String, role As String, activeState As String
    Set wsLogin = ThisWorkbook.Worksheets("Connexion")
    Set wsUsers = ThisWorkbook.Worksheets("Utilisateurs")
    username = Trim(CStr(wsLogin.Range("B5").Value))
    password = CStr(wsLogin.Range("B6").Value)
    If username = "" Or password = "" Then MsgBox "Veuillez saisir le nom utilisateur et le mot de passe.", vbExclamation, "Connexion": Exit Sub
    lastRow = wsUsers.Cells(wsUsers.Rows.Count, "A").End(xlUp).Row
    For row = 5 To lastRow
        If LCase(Trim(CStr(wsUsers.Cells(row, "A").Value))) = LCase(username) Then
            activeState = LCase(Trim(CStr(wsUsers.Cells(row, "G").Value)))
            storedPassword = CStr(wsUsers.Cells(row, "H").Value)
            role = LCase(Trim(CStr(wsUsers.Cells(row, "D").Value)))
            If activeState <> "actif" Then MsgBox "Ce compte est inactif.", vbCritical, "Connexion refusee": Exit Sub
            If storedPassword <> password Then MsgBox "Nom utilisateur ou mot de passe incorrect.", vbCritical, "Connexion refusee": Exit Sub
            CurrentUser = CStr(wsUsers.Cells(row, "A").Value)
            CurrentRole = role
            ApplyRoleVisibility role
            wsLogin.Range("B5:B6").ClearContents
            MsgBox "Connexion reussie. Bienvenue " & CurrentUser & ".", vbInformation, "Connexion"
            Exit Sub
        End If
    Next row
    MsgBox "Nom utilisateur ou mot de passe incorrect.", vbCritical, "Connexion refusee"
End Sub

Public Sub Logout()
    CurrentUser = ""
    CurrentRole = ""
    ProtectLoginSheet
    MsgBox "Vous etes deconnecte.", vbInformation, "Connexion"
End Sub

Public Sub ApplyRoleVisibility(ByVal role As String)
    HideBusinessSheets
    ThisWorkbook.Worksheets("Connexion").Visible = xlSheetVisible
    ThisWorkbook.Worksheets("Accueil").Visible = xlSheetVisible
    ThisWorkbook.Worksheets(9).Visible = xlSheetVisible
    ThisWorkbook.Worksheets(10).Visible = xlSheetVisible
    ThisWorkbook.Worksheets(11).Visible = xlSheetVisible
    If role = "admin" Then
        ThisWorkbook.Worksheets(3).Visible = xlSheetVisible
        ThisWorkbook.Worksheets(4).Visible = xlSheetVisible
        ThisWorkbook.Worksheets(5).Visible = xlSheetVisible
        ThisWorkbook.Worksheets(6).Visible = xlSheetVisible
        ThisWorkbook.Worksheets(7).Visible = xlSheetVisible
        ThisWorkbook.Worksheets(8).Visible = xlSheetVisible
    ElseIf role = "chef" Then
        ThisWorkbook.Worksheets(5).Visible = xlSheetVisible
        ThisWorkbook.Worksheets(6).Visible = xlSheetVisible
        ThisWorkbook.Worksheets(7).Visible = xlSheetVisible
        ThisWorkbook.Worksheets(8).Visible = xlSheetVisible
    End If
    ThisWorkbook.Worksheets("Accueil").Activate
End Sub

Private Sub HideBusinessSheets()
    Dim item As Variant
    Dim sheetNames As Variant
    sheetNames = Array("Accueil", 3, 4, 5, 6, 7, 8, 9, 10, 11)
    For Each item In sheetNames
        ThisWorkbook.Worksheets(item).Visible = xlSheetVeryHidden
    Next item
End Sub

Public Sub ProtectLoginSheet()
    HideBusinessSheets
    ThisWorkbook.Worksheets("Connexion").Visible = xlSheetVisible
    ThisWorkbook.Worksheets("Connexion").Activate
End Sub
