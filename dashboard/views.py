from django.shortcuts import render
from django.db.models import Avg, Sum
from django.db.models.functions import TruncMonth
from django.contrib.auth.decorators import login_required

from sites.models import Site
from especes.models import Espece
from debarquements.models import Debarquement


def home(request):
    """Page d'accueil publique du système."""
    nombre_sites = Site.objects.filter(actif=True).count()
    nombre_especes = Espece.objects.filter(actif=True).count()
    debarquements = Debarquement.objects.all()
    nombre_debarquements = debarquements.count()
    quantite_totale = debarquements.aggregate(
        total=Sum('quantite')
    )['total'] or 0
    quantite_moyenne = debarquements.aggregate(
        moyenne=Avg('quantite')
    )['moyenne'] or 0

    return render(
        request,
        'home.html',
        {
            'nombre_sites': nombre_sites,
            'nombre_especes': nombre_especes,
            'nombre_debarquements': nombre_debarquements,
            'quantite_totale': quantite_totale,
            'quantite_moyenne': round(quantite_moyenne, 2),
        }
    )


@login_required
def index(request):
    # =========================
    # FILTRES
    # =========================
    annee = request.GET.get('annee')
    site_id = request.GET.get('site')
    espece_id = request.GET.get('espece')

    # =========================
    # SITES ET ANNÉES DISPONIBLES
    # =========================
    sites = Site.objects.filter(actif=True).order_by('nom')
    especes = Espece.objects.filter(actif=True).order_by('nom')

    annees = (
        Debarquement.objects
        .dates('date', 'year', order='DESC')
    )

    # =========================
    # DÉBARQUEMENTS FILTRÉS
    # =========================
    debarquements = Debarquement.objects.all()

    if annee:
        debarquements = debarquements.filter(date__year=annee)

    if site_id:
        debarquements = debarquements.filter(site_id=site_id)

    if espece_id:
        debarquements = debarquements.filter(espece_id=espece_id)

    # =========================
    # INDICATEURS
    # =========================
    nombre_sites_actifs = Site.objects.filter(actif=True).count()
    nombre_especes = Espece.objects.filter(actif=True).count()
    nombre_debarquements = debarquements.count()
    quantite_totale = debarquements.aggregate(total=Sum('quantite'))['total'] or 0
    quantite_moyenne = debarquements.aggregate(moyenne=Avg('quantite'))['moyenne'] or 0

    # =========================
    # QUANTITÉ PAR ESPÈCE
    # =========================
    quantite_par_espece = (
        debarquements
        .values('espece__nom')
        .annotate(total=Sum('quantite'))
        .order_by('-total')
    )

    espece_top = quantite_par_espece.first()

    # =========================
    # QUANTITÉ PAR SITE
    # =========================
    quantite_par_site = (
        debarquements
        .values('site__nom')
        .annotate(total=Sum('quantite'))
        .order_by('-total')
    )

    site_chart_data = [
        {
            'label': ligne['site__nom'],
            'value': float(ligne['total'] or 0),
        }
        for ligne in quantite_par_site
    ]

    site_top = quantite_par_site.first()

    # =========================
    # ÉVOLUTION MENSUELLE
    # =========================
    evolution_mensuelle = (
        debarquements
        .annotate(mois=TruncMonth('date'))
        .values('mois')
        .annotate(total=Sum('quantite'))
        .order_by('mois')
    )

    context = {
        'debarquements': debarquements,
        'nombre_sites': nombre_sites_actifs,
        'nombre_especes': nombre_especes,
        'nombre_debarquements': nombre_debarquements,
        'quantite_totale': quantite_totale,
        'quantite_par_espece': quantite_par_espece,
        'quantite_par_site': quantite_par_site,
        'site_chart_data': site_chart_data,
        'evolution_mensuelle': evolution_mensuelle,
        'sites': sites,
        'annees': annees,
        'annee_selectionnee': annee,
        'site_selectionne': site_id,
        'espece_top': espece_top,
        'site_top': site_top,
        'quantite_moyenne': round(quantite_moyenne, 2),
        'especes': especes,
        'espece_selectionnee': espece_id,
    }

    return render(request, 'dashboard/index.html', context)