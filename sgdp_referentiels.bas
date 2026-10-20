Attribute VB_Name = "SGDPReferentiels"
Option Explicit

Public Sub RechercherSite()
    Dim formSheet As Worksheet
    Dim dataSheet As Worksheet
    Dim row As Long
    Dim found As Boolean

    Set formSheet = ThisWorkbook.Worksheets(7)
    Set dataSheet = ThisWorkbook.Worksheets(5)
    For row = 5 To 104
        dataSheet.Rows(row).Hidden = False
        If Trim(CStr(formSheet.Range("B4").Value)) <> "" Then
            dataSheet.Rows(row).Hidden = InStr(1, CStr(dataSheet.Cells(row, "A").Value) & " " & CStr(dataSheet.Cells(row, "B").Value) & " " & CStr(dataSheet.Cells(row, "C").Value), CStr(formSheet.Range("B4").Value), vbTextCompare) = 0
        End If
        If Not dataSheet.Rows(row).Hidden And dataSheet.Cells(row, "A").Value <> "" Then found = True
    Next row
    dataSheet.Activate
    If Trim(CStr(formSheet.Range("B4").Value)) <> "" And Not found Then MsgBox "Aucun site trouvé.", vbInformation, "Recherche"
End Sub

Public Sub RechercherEspece()
    Dim formSheet As Worksheet
    Dim dataSheet As Worksheet
    Dim row As Long
    Dim found As Boolean

    Set formSheet = ThisWorkbook.Worksheets(8)
    Set dataSheet = ThisWorkbook.Worksheets(6)
    For row = 5 To 104
        dataSheet.Rows(row).Hidden = False
        If Trim(CStr(formSheet.Range("B4").Value)) <> "" Then
            dataSheet.Rows(row).Hidden = InStr(1, CStr(dataSheet.Cells(row, "A").Value) & " " & CStr(dataSheet.Cells(row, "B").Value), CStr(formSheet.Range("B4").Value), vbTextCompare) = 0
        End If
        If Not dataSheet.Rows(row).Hidden And dataSheet.Cells(row, "A").Value <> "" Then found = True
    Next row
    dataSheet.Activate
    If Trim(CStr(formSheet.Range("B4").Value)) <> "" And Not found Then MsgBox "Aucune espèce trouvée.", vbInformation, "Recherche"
End Sub

Public Sub CreerUtilisateur()
    Dim formSheet As Worksheet, dataSheet As Worksheet, nextRow As Long
    Set formSheet = ThisWorkbook.Worksheets("Formulaire Utilisateurs")
    Set dataSheet = ThisWorkbook.Worksheets(3)
    If Trim(CStr(formSheet.Range("B4").Value)) = "" Then
        MsgBox "Le nom utilisateur est obligatoire.", vbExclamation, "Utilisateur"
        Exit Sub
    End If
    If Application.WorksheetFunction.CountIf(dataSheet.Range("A5:A104"), formSheet.Range("B4").Value) > 0 Then
        MsgBox "Ce nom utilisateur existe déjà.", vbExclamation, "Utilisateur"
        Exit Sub
    End If
    nextRow = dataSheet.Cells(dataSheet.Rows.Count, "A").End(xlUp).Row + 1
    If nextRow < 5 Then nextRow = 5
    If nextRow > 104 Then MsgBox "La liste des utilisateurs est pleine.", vbExclamation, "Utilisateur": Exit Sub
    dataSheet.Cells(nextRow, "A").Value = formSheet.Range("B4").Value
    dataSheet.Cells(nextRow, "B").Value = formSheet.Range("B5").Value
    dataSheet.Cells(nextRow, "C").Value = formSheet.Range("B6").Value
    dataSheet.Cells(nextRow, "D").Value = formSheet.Range("B7").Value
    dataSheet.Cells(nextRow, "E").Value = formSheet.Range("B8").Value
    dataSheet.Cells(nextRow, "F").Value = formSheet.Range("B9").Value
    dataSheet.Cells(nextRow, "G").Value = IIf(Trim(CStr(formSheet.Range("B10").Value)) = "", "Actif", formSheet.Range("B10").Value)
    dataSheet.Cells(nextRow, "H").Value = formSheet.Range("B11").Value
    formSheet.Range("B4:B11").ClearContents
    MsgBox "Utilisateur créé.", vbInformation, "Utilisateur"
End Sub

Public Sub RechercherUtilisateur()
    Dim formSheet As Worksheet, dataSheet As Worksheet, row As Long, query As String
    Set formSheet = ThisWorkbook.Worksheets("Formulaire Utilisateurs")
    Set dataSheet = ThisWorkbook.Worksheets(3)
    query = Trim(CStr(formSheet.Range("B4").Value))
    For row = 5 To 104
        dataSheet.Rows(row).Hidden = False
        If query <> "" Then dataSheet.Rows(row).Hidden = InStr(1, CStr(dataSheet.Cells(row, "A").Value) & " " & CStr(dataSheet.Cells(row, "B").Value) & " " & CStr(dataSheet.Cells(row, "C").Value) & " " & CStr(dataSheet.Cells(row, "D").Value), query, vbTextCompare) = 0
    Next row
    dataSheet.Activate
End Sub

Public Sub InverserUtilisateur()
    Dim dataSheet As Worksheet, row As Long
    Set dataSheet = ThisWorkbook.Worksheets("Utilisateurs")
    row = ActiveCell.Row
    If ActiveSheet.Name <> "Utilisateurs" Or row < 5 Or row > 104 Then MsgBox "Sélectionnez une ligne utilisateur.", vbExclamation, "Utilisateur": Exit Sub
    dataSheet.Cells(row, "G").Value = IIf(LCase(CStr(dataSheet.Cells(row, "G").Value)) = "actif", "Inactif", "Actif")
End Sub

Public Sub ValiderDebarquement()
    Dim sheet As Worksheet, row As Long
    Set sheet = ThisWorkbook.Worksheets(9)
    row = ActiveCell.Row
    If ActiveSheet.Name <> sheet.Name Or row < 5 Or row > 1004 Then MsgBox "Sélectionnez une ligne de débarquement.", vbExclamation, "Validation": Exit Sub
    sheet.Cells(row, "G").Value = "Validé"
    sheet.Cells(row, "I").Value = CurrentUser
    sheet.Cells(row, "J").Value = Now
End Sub

Public Sub SupprimerDebarquement()
    Dim sheet As Worksheet, row As Long
    Set sheet = ThisWorkbook.Worksheets(9)
    row = ActiveCell.Row
    If ActiveSheet.Name <> sheet.Name Or row < 5 Or row > 1004 Then MsgBox "Sélectionnez une ligne de débarquement.", vbExclamation, "Suppression": Exit Sub
    If MsgBox("Supprimer le débarquement sélectionné ?", vbYesNo + vbQuestion, "Confirmation") = vbYes Then sheet.Rows(row).Delete
End Sub

Public Sub ReinitialiserFiltres()
    Dim sheet As Worksheet
    For Each sheet In ThisWorkbook.Worksheets
        If sheet.AutoFilterMode Then
            On Error Resume Next
            sheet.ShowAllData
            On Error GoTo 0
        End If
    Next sheet
    ThisWorkbook.Worksheets(5).Rows("5:104").Hidden = False
    ThisWorkbook.Worksheets(6).Rows("5:104").Hidden = False
    ThisWorkbook.Worksheets(3).Rows("5:104").Hidden = False
End Sub

Public Sub InverserSite()
    Dim sheet As Worksheet, row As Long
    Set sheet = ThisWorkbook.Worksheets(5)
    row = ActiveCell.Row
    If ActiveSheet.Name <> sheet.Name Or row < 5 Or row > 104 Then MsgBox "Sélectionnez une ligne de site.", vbExclamation, "Site": Exit Sub
    sheet.Cells(row, "D").Value = IIf(LCase(CStr(sheet.Cells(row, "D").Value)) = "actif", "Inactif", "Actif")
End Sub

Public Sub InverserEspece()
    Dim sheet As Worksheet, row As Long
    Set sheet = ThisWorkbook.Worksheets(6)
    row = ActiveCell.Row
    If ActiveSheet.Name <> sheet.Name Or row < 5 Or row > 104 Then MsgBox "Sélectionnez une ligne d'espèce.", vbExclamation, "Espèce": Exit Sub
    sheet.Cells(row, "D").Value = IIf(LCase(CStr(sheet.Cells(row, "D").Value)) = "actif", "Inactif", "Actif")
End Sub

Public Sub SupprimerUtilisateur()
    Dim sheet As Worksheet, row As Long
    Set sheet = ThisWorkbook.Worksheets(3)
    row = ActiveCell.Row
    If ActiveSheet.Name <> sheet.Name Or row < 5 Or row > 104 Then MsgBox "Sélectionnez une ligne utilisateur.", vbExclamation, "Utilisateur": Exit Sub
    If CStr(sheet.Cells(row, "A").Value) = CurrentUser Then MsgBox "Vous ne pouvez pas supprimer votre propre compte.", vbExclamation, "Utilisateur": Exit Sub
    If MsgBox("Supprimer l'utilisateur sélectionné ?", vbYesNo + vbQuestion, "Confirmation") = vbYes Then sheet.Rows(row).Delete
End Sub

Public Sub ExporterRapportPDF()
    Dim filePath As String
    filePath = ThisWorkbook.Path & Application.PathSeparator & "rapport_sgdp_" & Format(Now, "yyyymmdd_hhnnss") & ".pdf"
    ThisWorkbook.Worksheets("Rapports").ExportAsFixedFormat Type:=xlTypePDF, Filename:=filePath, Quality:=xlQualityStandard, IncludeDocProperties:=True, IgnorePrintAreas:=False, OpenAfterPublish:=True
End Sub