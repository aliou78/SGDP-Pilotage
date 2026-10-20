$ErrorActionPreference = 'Stop'
$base = Split-Path -Parent $MyInvocation.MyCommand.Path
$xlsx = Join-Path $base 'sgdp_complet.xlsx'
$xlsm = Join-Path $base 'sgdp_complet_connexion.xlsm'
$bas = Join-Path $base 'sgdp_login.bas'
$referentielsBas = Join-Path $base 'sgdp_referentiels.bas'

if (-not (Test-Path $xlsx)) {
    python (Join-Path $base 'create_excel_full.py')
}
if (Test-Path $xlsm) { Remove-Item $xlsm -Force }

$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false
try {
    Write-Output 'Ouverture du classeur source...'
    $book = $excel.Workbooks.Open($xlsx)
    $connection = $book.Worksheets.Item(1)
    Write-Output 'Connexion creee.'

    $connection.Range('A1:F1').Merge()
    $connection.Range('A1').Value2 = 'SGDP - Connexion'
    $connection.Range('A1').Font.Bold = $true
    $connection.Range('A1').Font.Size = 20
    $connection.Range('A1').Font.Color = 16777215
    $connection.Range('A1').Interior.Color = 5026597
    $connection.Range('A3').Value2 = 'Connexion obligatoire avant acces aux pages du fichier.'
    $connection.Range('A5').Value2 = 'Nom utilisateur'
    $connection.Range('A6').Value2 = 'Mot de passe'
    $connection.Range('B5').Value2 = 'admin'
    $connection.Range('B6').Value2 = 'admin123'
    $connection.Range('A9').Value2 = 'Compte de demonstration : admin / admin123'
    $connection.Range('A10').Value2 = 'Modifiez les mots de passe dans la feuille Utilisateurs apres connexion.'
    $connection.Range('A5:A6').Font.Bold = $true
    $connection.Range('A5:A6').Interior.Color = 15269864
    $connection.Range('B5:B6').Interior.Color = 16777164
    $connection.Range('B5:B6').ColumnWidth = 28
    $connection.Columns.Item('A').ColumnWidth = 32
    $connection.Columns.Item('C').ColumnWidth = 18
    $connection.Range('A3:F3').Merge()
    $connection.Range('A9:F9').Merge()
    $connection.Range('A10:F10').Merge()

    $button = $connection.Buttons().Add(250, 130, 130, 32)
    $button.Caption = 'Se connecter'
    $button.OnAction = 'Login'
    $logout = $connection.Buttons().Add(250, 175, 130, 32)
    $logout.Caption = 'Se deconnecter'
    $logout.OnAction = 'Logout'
    Write-Output 'Page connexion configuree.'

    # Secondary form-control buttons are intentionally omitted here because Excel
    # COM can crash on controls in generated worksheets. The imported macros remain
    # available from Excel's macro menu and the login buttons stay on Connexion.
    if ($false) {
    $siteForm = $book.Worksheets.Item(7)
    $siteButton = $siteForm.Buttons().Add(250, 150, 160, 32)
    $siteButton.Caption = 'Rechercher'
    $siteButton.OnAction = 'RechercherSite'
    $speciesForm = $book.Worksheets.Item(8)
    $speciesButton = $speciesForm.Buttons().Add(250, 125, 175, 32)
    $speciesButton.Caption = 'Rechercher'
    $speciesButton.OnAction = 'RechercherEspece'
    Write-Output 'Formulaires sites/especes configures.'

    $userForm = $book.Worksheets.Item(4)
    $userCreateButton = $userForm.Buttons().Add(250, 330, 155, 32)
    $userCreateButton.Caption = 'Creer utilisateur'
    $userCreateButton.OnAction = 'CreerUtilisateur'
    $userSearchButton = $userForm.Buttons().Add(420, 330, 140, 32)
    $userSearchButton.Caption = 'Rechercher'
    $userSearchButton.OnAction = 'RechercherUtilisateur'
    Write-Output 'Formulaire utilisateurs configure.'

    $usersSheet = $book.Worksheets.Item(3)
    $userToggleButton = $usersSheet.Buttons().Add(20, 35, 155, 28)
    $userToggleButton.Caption = 'Activer / desactiver'
    $userToggleButton.OnAction = 'InverserUtilisateur'
    $userDeleteButton = $usersSheet.Buttons().Add(185, 35, 135, 28)
    $userDeleteButton.Caption = 'Supprimer'
    $userDeleteButton.OnAction = 'SupprimerUtilisateur'

    $sitesSheet = $book.Worksheets.Item(5)
    $siteToggleButton = $sitesSheet.Buttons().Add(20, 35, 155, 28)
    $siteToggleButton.Caption = 'Activer / desactiver'
    $siteToggleButton.OnAction = 'InverserSite'
    $speciesSheet = $book.Worksheets.Item(6)
    $speciesToggleButton = $speciesSheet.Buttons().Add(20, 35, 155, 28)
    $speciesToggleButton.Caption = 'Activer / desactiver'
    $speciesToggleButton.OnAction = 'InverserEspece'

    $landingSheet = $book.Worksheets.Item(9)
    $validateButton = $landingSheet.Buttons().Add(20, 35, 130, 28)
    $validateButton.Caption = 'Valider la ligne'
    $validateButton.OnAction = 'ValiderDebarquement'
    $deleteButton = $landingSheet.Buttons().Add(160, 35, 145, 28)
    $deleteButton.Caption = 'Supprimer la ligne'
    $deleteButton.OnAction = 'SupprimerDebarquement'

    $reportsSheet = $book.Worksheets.Item(10)
    $resetButton = $reportsSheet.Buttons().Add(20, 35, 145, 28)
    $resetButton.Caption = 'Reinitialiser filtres'
    $resetButton.OnAction = 'ReinitialiserFiltres'
    $pdfButton = $reportsSheet.Buttons().Add(175, 35, 125, 28)
    $pdfButton.Caption = 'Exporter PDF'
    $pdfButton.OnAction = 'ExporterRapportPDF'
    }
    Write-Output 'Actions configurees.'

    Write-Output 'Ajout des boutons termine.'
    try {
        $book.VBProject.VBComponents.Import($bas) | Out-Null
        $book.VBProject.VBComponents.Import($referentielsBas) | Out-Null
        Write-Output 'Macros VBA importees.'
    }
    catch {
        Write-Warning 'Import VBA refuse par la securite Excel. Activez la confiance envers le projet VBA puis relancez le script.'
    }

    foreach ($sheet in $book.Worksheets) {
        $sheet.Activate()
        $sheet.Application.ActiveWindow.DisplayGridlines = $false
    }
    foreach ($sheet in $book.Worksheets) {
        if ($sheet.Name -ne 'Connexion' -and $sheet.Name -ne '_Listes') {
            $sheet.Visible = 0
        }
    }
    $book.Worksheets.Item('Connexion').Visible = -1
    $book.Worksheets.Item('Connexion').Activate()
    Write-Output 'Classeur pret pour enregistrement.'
    $book.SaveAs($xlsm, 52)
    Write-Output 'Enregistrement termine.'
    $book.Close($true)
    Write-Output "Fichier cree : $xlsm"
}
catch {
    Write-Error $_
    if ($book) { $book.Close($false) }
    throw
}
finally {
    $excel.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
}
