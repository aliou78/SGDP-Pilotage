from calendar import monthrange

from django.db.models import Sum
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

from accounts.decorators import role_required

from debarquements.models import Debarquement
from especes.models import Espece
from sites.models import Site


# ============================================================
# FILTRES DES RAPPORTS
# ============================================================

class InvalidReportFilter(ValueError):
    pass


def appliquer_filtres(request):

    type_rapport = request.GET.get(
        'type_rapport',
        'journalier'
    )

    date_rapport = request.GET.get(
        'date_rapport',
        ''
    )

    mois = request.GET.get(
        'mois',
        ''
    )

    annee = request.GET.get(
        'annee',
        ''
    )

    date_debut = request.GET.get(
        'date_debut',
        ''
    )

    date_fin = request.GET.get(
        'date_fin',
        ''
    )

    site_id = request.GET.get(
        'site',
        ''
    )

    espece_id = request.GET.get(
        'espece',
        ''
    )

    # Tous les débarquements
    debarquements = Debarquement.objects.select_related(
        'espece',
        'site'
    ).all()

    # --------------------------------------------------------
    # RAPPORT JOURNALIER
    # --------------------------------------------------------

    if type_rapport == 'journalier':

        if date_rapport:
            debarquements = debarquements.filter(
                date=date_rapport
            )

    # --------------------------------------------------------
    # RAPPORT MENSUEL
    # --------------------------------------------------------

    elif type_rapport == 'mensuel':

        if not mois or not annee:
            raise InvalidReportFilter(
                'Un mois et une année valides sont requis pour le rapport mensuel.'
            )

        try:
            mois_int = int(mois)
            annee_int = int(annee)
            if not 1 <= annee_int <= 9999:
                raise ValueError
            dernier_jour_numero = monthrange(annee_int, mois_int)[1]
        except (ValueError, TypeError, OverflowError) as exc:
            raise InvalidReportFilter(
                'Le mois ou l’année du rapport mensuel est invalide.'
            ) from exc

        premier_jour = f'{annee_int:04d}-{mois_int:02d}-01'
        dernier_jour = (
            f'{annee_int:04d}-{mois_int:02d}-{dernier_jour_numero:02d}'
        )

        debarquements = debarquements.filter(
            date__gte=premier_jour,
            date__lte=dernier_jour
        )

    # --------------------------------------------------------
    # RAPPORT ANNUEL
    # --------------------------------------------------------

    elif type_rapport == 'annuel':

        if not annee:
            raise InvalidReportFilter(
                'Une année valide est requise pour le rapport annuel.'
            )

        try:
            annee_int = int(annee)
            if not 1 <= annee_int <= 9999:
                raise ValueError
            premier_jour = f'{annee_int:04d}-01-01'
            dernier_jour = f'{annee_int:04d}-12-31'
            # Validate the year range supported by Python's date implementation.
            monthrange(annee_int, 1)
        except (ValueError, TypeError, OverflowError) as exc:
            raise InvalidReportFilter(
                'L’année du rapport annuel est invalide.'
            ) from exc

        debarquements = debarquements.filter(
            date__gte=premier_jour,
            date__lte=dernier_jour
        )

    # --------------------------------------------------------
    # RAPPORT PERSONNALISÉ
    # --------------------------------------------------------

    elif type_rapport == 'personnalise':

        if date_debut:

            debarquements = debarquements.filter(
                date__gte=date_debut
            )

        if date_fin:

            debarquements = debarquements.filter(
                date__lte=date_fin
            )

    # --------------------------------------------------------
    # FILTRE PAR SITE
    # --------------------------------------------------------

    if site_id:

        debarquements = debarquements.filter(
            site_id=site_id
        )

    if espece_id:

        debarquements = debarquements.filter(
            espece_id=espece_id
        )

    return (
        debarquements,
        type_rapport,
        date_rapport,
        mois,
        annee,
        date_debut,
        date_fin,
        site_id,
        espece_id,
    )


# ============================================================
# CONSTRUCTION DU GRAPHIQUE D'ANALYSE
# ============================================================

def construire_evolution(
    debarquements,
    type_rapport
):

    donnees = (
        debarquements
        .values('date')
        .annotate(total=Sum('quantite'))
        .order_by('date')
    )

    if type_rapport == 'annuel':
        regroupement = {}

        for ligne in donnees:
            periode = ligne['date'].strftime('%m/%Y')
            regroupement[periode] = (
                regroupement.get(periode, 0) + (ligne['total'] or 0)
            )

        return [
            {'label': periode, 'total': total}
            for periode, total in regroupement.items()
        ]

    format_label = '%d/%m/%Y'
    if type_rapport == 'mensuel':
        format_label = '%d/%m'

    return [
        {
            'label': ligne['date'].strftime(format_label),
            'total': ligne['total'] or 0,
        }
        for ligne in donnees
    ]


# ============================================================
# RAPPORT PRINCIPAL
# ============================================================

@role_required('admin', 'chef', 'consultation')
def rapport_list(request):

    try:
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
        ) = appliquer_filtres(request)
    except InvalidReportFilter as exc:
        return HttpResponseBadRequest(str(exc))

    # ========================================================
    # 1. STATISTIQUES PAR SITE ET PAR ESPÈCE
    # ========================================================

    statistiques = (
        debarquements
        .values(
            'site__nom',
            'espece__nom'
        )
        .annotate(
            total=Sum('quantite')
        )
        .order_by('-total')
    )

    # ========================================================
    # 2. QUANTITÉ TOTALE PAR ESPÈCE
    # ========================================================
    # Cette variable alimente :
    # - le tableau "Quantité par espèce"
    # - le graphique "Quantité totale par espèce"
    # ========================================================

    graphique_especes = (
        debarquements
        .values('espece__nom')
        .annotate(
            total=Sum('quantite')
        )
        .order_by('-total')
    )

    # Même donnée pour le tableau
    quantites_par_espece = graphique_especes

    # ========================================================
    # 3. TOTAL GÉNÉRAL
    # ========================================================

    total_general = (
        debarquements
        .aggregate(
            total=Sum('quantite')
        )
        ['total']
        or 0
    )

    # ========================================================
    # 4. ANALYSE / ÉVOLUTION
    # ========================================================

    evolution = construire_evolution(
        debarquements,
        type_rapport
    )

    # ========================================================
    # 5. CONTEXTE
    # ========================================================

    context = {

        # Table principale
        'statistiques': statistiques,

        # Quantités par espèce
        'quantites_par_espece': quantites_par_espece,

        # Graphique par espèce
        'graphique_especes': graphique_especes,

        # Graphique d'analyse
        'evolution': evolution,

        # Total
        'total_general': total_general,

        # Filtres
        'type_rapport': type_rapport,
        'date_rapport': date_rapport,
        'mois': mois,
        'annee': annee,
        'date_debut': date_debut,
        'date_fin': date_fin,
        'site_id': site_id,
        'espece_id': espece_id,
        'site_selectionne': Site.objects.filter(
            pk=site_id
        ).values_list('nom', flat=True).first() if site_id else '',
        'espece_selectionnee': Espece.objects.filter(
            pk=espece_id
        ).values_list('nom', flat=True).first() if espece_id else '',

        # Sites
        'sites': Site.objects.filter(
            actif=True
        ),

        'especes': Espece.objects.filter(
            actif=True
        ),
    }

    return render(
        request,
        'rapports/list.html',
        context
    )


# ============================================================
# EXPORT EXCEL
# ============================================================

@role_required('admin', 'chef', 'consultation')
def rapport_excel(request):
    from .excel_report import generer_rapport_activites_excel

    try:
        filtres = appliquer_filtres(request)
    except InvalidReportFilter as exc:
        return HttpResponseBadRequest(str(exc))
    return generer_rapport_activites_excel(filtres)

# ============================================================
# EXPORT PDF
# ============================================================


@role_required('admin', 'chef')
def rapport_pdf(request):
    from .pdf_report import generer_rapport_activites_pdf

    try:
        filtres = appliquer_filtres(request)
    except InvalidReportFilter as exc:
        return HttpResponseBadRequest(str(exc))
    return generer_rapport_activites_pdf(filtres)