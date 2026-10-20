from datetime import datetime
from xml.sax.saxutils import escape

from django.contrib.staticfiles import finders
from django.db.models import Sum
from django.http import HttpResponse
from django.utils import timezone

from especes.models import Espece
from sites.models import Site

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Image,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def generer_rapport_activites_pdf(filtres):
    (
        debarquements,
        type_rapport,
        date_rapport,
        mois,
        annee,
        date_debut,
        date_fin,
        site_id,
        espece_id,
    ) = filtres

    mois_noms = {
        '1': 'janvier',
        '2': 'février',
        '3': 'mars',
        '4': 'avril',
        '5': 'mai',
        '6': 'juin',
        '7': 'juillet',
        '8': 'août',
        '9': 'septembre',
        '10': 'octobre',
        '11': 'novembre',
        '12': 'décembre',
    }
    types_rapport = {
        'journalier': 'Rapport journalier',
        'mensuel': 'Rapport d’activités mensuel',
        'annuel': 'Rapport d’activités annuel',
        'personnalise': 'Rapport d’activités',
    }
    periode = types_rapport.get(type_rapport, 'Rapport d’activités')

    if type_rapport == 'journalier' and date_rapport:
        try:
            periode += ' du ' + datetime.strptime(
                date_rapport, '%Y-%m-%d'
            ).strftime('%d/%m/%Y')
        except ValueError:
            periode += ' du ' + date_rapport
    elif type_rapport == 'mensuel':
        if mois and annee:
            periode += f' — {mois_noms.get(str(mois), mois)} {annee}'
        elif annee:
            periode += f' — {annee}'
    elif type_rapport == 'annuel' and annee:
        periode += f' — {annee}'
    elif type_rapport == 'personnalise':
        periode += f' — du {date_debut or "________"} au {date_fin or "________"}'

    site_selectionne = (
        Site.objects.filter(pk=site_id).values_list('nom', flat=True).first()
        if site_id else ''
    )
    espece_selectionnee = (
        Espece.objects.filter(pk=espece_id).values_list('nom', flat=True).first()
        if espece_id else ''
    )

    resume_sites_especes = list(
        debarquements.values('site__nom', 'espece__nom')
        .annotate(total=Sum('quantite'))
        .order_by('site__nom', 'espece__nom')
    )
    total_general = debarquements.aggregate(
        total=Sum('quantite')
    )['total'] or 0

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        'attachment; filename="rapport_activites.pdf"'
    )
    document = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=15 * mm,
        leftMargin=15 * mm,
        topMargin=14 * mm,
        bottomMargin=17 * mm,
        title=f'{periode} — SGDP',
        author='SGDP',
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='Institution',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        alignment=TA_CENTER,
        textColor=colors.black,
        spaceAfter=2,
    ))
    styles.add(ParagraphStyle(
        name='InstitutionDetail',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        alignment=TA_CENTER,
        textColor=colors.black,
    ))
    styles.add(ParagraphStyle(
        name='ReportTitle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        alignment=TA_CENTER,
        textColor=colors.black,
        spaceAfter=5,
    ))
    styles.add(ParagraphStyle(
        name='ReportSection',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        alignment=TA_LEFT,
        textColor=colors.black,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True,
    ))
    styles.add(ParagraphStyle(
        name='ReportBody',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        alignment=TA_LEFT,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name='TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=9,
    ))
    styles.add(ParagraphStyle(
        name='TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=9,
        alignment=TA_CENTER,
    ))

    elements = []

    logo_path = finders.find('images/logo .png')
    institution = [
        Paragraph('RÉPUBLIQUE DU SÉNÉGAL', styles['Institution']),
        Paragraph('Un Peuple - Un But - Une Foi', styles['InstitutionDetail']),
        Spacer(1, 2 * mm),
        Paragraph(
            'MINISTÈRE DES PÊCHES ET DE L’ÉCONOMIE MARITIME',
            styles['Institution'],
        ),
        Paragraph('DIRECTION DE LA PÊCHE CONTINENTALE', styles['Institution']),
        Paragraph(
            'SERVICE RÉGIONAL DES PÊCHES ET DE LA SURVEILLANCE — SÉDHIOU',
            styles['InstitutionDetail'],
        ),
        Paragraph(
            'SERVICE DÉPARTEMENTAL DES PÊCHES ET DE LA SURVEILLANCE — BOUNKILING',
            styles['InstitutionDetail'],
        ),
    ]
    logo = Image(logo_path, width=27 * mm, height=17 * mm) if logo_path else ''
    institution_table = Table(
        [[logo, institution]],
        colWidths=[30 * mm, 150 * mm],
        hAlign='CENTER',
    )
    institution_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (0, 0), 'CENTER'),
        ('LINEBELOW', (0, 0), (-1, -1), 0.7, colors.black),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    elements.extend([institution_table, Spacer(1, 8 * mm)])
    elements.extend([
        Paragraph(escape(periode.upper()), styles['ReportTitle']),
        Paragraph(
            'SUIVI DES ACTIVITÉS ET DE LA PRODUCTION DE LA PÊCHE',
            styles['Institution'],
        ),
        Spacer(1, 4 * mm),
    ])
    if site_selectionne or espece_selectionnee:
        filtres_affiches = []
        if site_selectionne:
            filtres_affiches.append(f'Site : {escape(site_selectionne)}')
        if espece_selectionnee:
            filtres_affiches.append(f'Espèce : {escape(espece_selectionnee)}')
        elements.append(Paragraph(
            ' — '.join(filtres_affiches),
            styles['InstitutionDetail'],
        ))

    def paragraph(value, style='TableCell'):
        return Paragraph(escape(str(value)), styles[style])

    def report_table(rows, widths, header=True):
        formatted_rows = [
            [paragraph(cell, 'TableHeader' if row_index == 0 and header else 'TableCell')
             for cell in row]
            for row_index, row in enumerate(rows)
        ]
        table = Table(
            formatted_rows,
            colWidths=widths,
            repeatRows=1 if header else 0,
            hAlign='LEFT',
        )
        style = [
            ('GRID', (0, 0), (-1, -1), 0.45, colors.HexColor('#555555')),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('LEFTPADDING', (0, 0), (-1, -1), 4),
            ('RIGHTPADDING', (0, 0), (-1, -1), 4),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]
        if header:
            style.extend([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e9efec')),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ])
        table.setStyle(TableStyle(style))
        return table

    def section(title, content):
        elements.append(Paragraph(escape(title), styles['ReportSection']))
        elements.extend(content)

    section('INTRODUCTION', [
        Paragraph(
            'Le présent rapport rend compte des activités du Service '
            'Départemental des Pêches et de la Surveillance de Bounkiling '
            f'pour la période {escape(periode.lower())}. Les données de '
            'débarquement disponibles dans le SGDP sont reprises dans les '
            'tableaux ci-dessous. Les rubriques non gérées par l’application '
            'restent à compléter avant validation du rapport.',
            styles['ReportBody'],
        ),
    ])

    section('1. PERSONNEL', [
        report_table([
            ['N°', 'Prénom(s) et nom', 'Profession', 'Fonction'],
            ['1', '', '', ''],
            ['2', '', '', ''],
            ['3', '', '', ''],
        ], [12 * mm, 48 * mm, 48 * mm, 72 * mm]),
    ])

    section('2. LOGISTIQUE', [
        report_table([
            ['Désignation', 'État', 'Besoins'],
            ['', '', ''],
            ['', '', ''],
        ], [60 * mm, 60 * mm, 60 * mm]),
    ])

    section('3. BESOINS MAJEURS', [
        Paragraph('________________________________________________________________________________',
                  styles['ReportBody']),
        Paragraph('________________________________________________________________________________',
                  styles['ReportBody']),
    ])

    section('4. ÉVÉNEMENT MAJEUR DANS LE MOIS', [
        Paragraph('________________________________________________________________________________',
                  styles['ReportBody']),
    ])

    section('5. ACTIVITÉS RÉALISÉES', [
        report_table([
            ['N°', 'Activité', 'Observations'],
            ['1', '', ''],
            ['2', '', ''],
            ['3', '', ''],
            ['4', '', ''],
        ], [12 * mm, 105 * mm, 63 * mm]),
    ])

    section('6. SITUATION DES CARTES PROFESSIONNELLES ET PERMIS DE PÊCHE', [
        report_table([
            ['Type de permis / carte', 'Catégorie', 'Nombre', 'Total'],
            ['Permis national', 'A', '', ''],
            ['Permis national', 'B', '', ''],
            ['Permis national', 'C', '', ''],
            ['Permis étranger', 'A', '', ''],
            ['Permis étranger', 'B', '', ''],
            ['Permis étranger', 'C', '', ''],
            ['Cartes de mareyeurs', 'À compléter', '', ''],
            ['TOTAL', '', '', ''],
        ], [68 * mm, 42 * mm, 35 * mm, 35 * mm]),
    ])

    section('7. CONTENTIEUX', [
        report_table([
            ['Type d’infraction', 'Nombre', 'Amendes (FCFA)'],
            ['Pêche', '', ''],
            ['Transformation', '', ''],
            ['Mareyage', '', ''],
            ['Transport fluvial', '', ''],
            ['Total', '', ''],
        ], [72 * mm, 45 * mm, 63 * mm]),
    ])

    section('8. BESOIN EN GILETS DE SAUVETAGE', [
        report_table([
            ['Besoin', 'Nombre'],
            ['Gilets de sauvetage', ''],
        ], [120 * mm, 60 * mm]),
    ])

    section('9. SITUATION DU PARC PIROGUIER', [
        report_table([
            ['Désignation', 'Sites', 'Nombre'],
            ['Pirogue de pêche', '', ''],
            ['Pirogue de transport', '', ''],
            ['TOTAL', '', ''],
        ], [75 * mm, 55 * mm, 50 * mm]),
    ])

    section('10. SITUATION DES ORGANISATIONS PROFESSIONNELLES', [
        report_table([
            ['N°', 'Dénomination', 'N° RCCM', 'Membres (H/F)', 'Responsable / contact', 'Adresse'],
            ['1', '', '', '', '', ''],
            ['2', '', '', '', '', ''],
            ['3', '', '', '', '', ''],
        ], [9 * mm, 43 * mm, 30 * mm, 28 * mm, 40 * mm, 30 * mm]),
    ])

    section('11. SÉCURITÉ DE LA PÊCHE ET DU TRANSPORT FLUVIAL', [
        Paragraph('________________________________________________________________________________',
                  styles['ReportBody']),
        Paragraph('________________________________________________________________________________',
                  styles['ReportBody']),
        Paragraph('________________________________________________________________________________',
                  styles['ReportBody']),
    ])

    section('12. PRODUCTION DE LA PÊCHE LOCALE — MISES À TERRE', [
        Paragraph(
            'Les quantités ci-dessous sont calculées à partir des '
            'débarquements enregistrés dans le SGDP. Les prix unitaires et '
            'valeurs commerciales ne sont pas disponibles dans l’application '
            'et sont laissés à compléter.',
            styles['ReportBody'],
        ),
    ])
    data_production = [[
        'Site',
        'Espèce',
        'Poids mis à terre (kg)',
        'Prix unitaire (FCFA/kg)',
        'Valeur commerciale (FCFA)',
    ]]
    for ligne in resume_sites_especes:
        data_production.append([
            ligne['site__nom'] or '',
            ligne['espece__nom'] or '',
            str(ligne['total'] or 0),
            '',
            '',
        ])
    if not resume_sites_especes:
        data_production.append(['', 'Aucun débarquement enregistré', '', '', ''])
    data_production.append(['', 'TOTAL GÉNÉRAL', str(total_general), '', ''])
    elements.append(report_table(
        data_production,
        [36 * mm, 39 * mm, 34 * mm, 35 * mm, 36 * mm],
    ))

    section('13. PHYSIONOMIE GÉNÉRALE DU MAREYAGE', [
        Paragraph('________________________________________________________________________________',
                  styles['ReportBody']),
        Paragraph('________________________________________________________________________________',
                  styles['ReportBody']),
    ])

    section('14. APPORTS EXTÉRIEURS — PRODUITS FRAIS', [
        report_table([
            ['Espèce', 'Quantité (kg)', 'Prix unitaire (FCFA)', 'Nature', 'Valeur estimée (FCFA)'],
            ['', '', '', 'Frais', ''],
            ['', '', '', 'Frais', ''],
            ['TOTAL', '', '', '', ''],
        ], [40 * mm, 30 * mm, 38 * mm, 30 * mm, 42 * mm]),
    ])

    section('15. MAREYAGE DE PRODUITS TRANSFORMÉS', [
        report_table([
            ['Nom vernaculaire', 'Quantité (kg)', 'Prix unitaire (FCFA)', 'Nature', 'Valeur estimée (FCFA)'],
            ['', '', '', 'Transformé', ''],
            ['', '', '', 'Transformé', ''],
            ['TOTAL', '', '', '', ''],
        ], [40 * mm, 30 * mm, 38 * mm, 30 * mm, 42 * mm]),
    ])

    section('16. PROJETS EN COURS D’EXÉCUTION', [
        Paragraph('________________________________________________________________________________',
                  styles['ReportBody']),
    ])

    section('17. PERSPECTIVES', [
        Paragraph('________________________________________________________________________________',
                  styles['ReportBody']),
        Paragraph('________________________________________________________________________________',
                  styles['ReportBody']),
    ])

    section('18. CONTRAINTES LIÉES AU FONCTIONNEMENT DU SERVICE', [
        Paragraph('________________________________________________________________________________',
                  styles['ReportBody']),
        Paragraph('________________________________________________________________________________',
                  styles['ReportBody']),
    ])

    elements.extend([
        Spacer(1, 7 * mm),
        Table([
            [
                Paragraph(
                    f'Fait à Bounkiling, le {timezone.localdate().strftime("%d/%m/%Y")}',
                    styles['InstitutionDetail'],
                ),
                Paragraph('Le Chef de Service', styles['InstitutionDetail']),
            ],
            ['', ''],
            ['', ''],
            ['', ''],
        ], colWidths=[90 * mm, 90 * mm], style=TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('TOPPADDING', (0, 0), (-1, -1), 5),
        ])),
    ])

    def add_page_number(canvas, doc):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor('#777777'))
        canvas.line(15 * mm, 12 * mm, A4[0] - 15 * mm, 12 * mm)
        canvas.setFont('Helvetica', 7)
        canvas.drawString(15 * mm, 7 * mm, 'SGDP — Rapport d’activités')
        canvas.drawRightString(A4[0] - 15 * mm, 7 * mm, f'Page {doc.page}')
        canvas.restoreState()

    document.build(elements, onFirstPage=add_page_number, onLaterPages=add_page_number)
    return response
