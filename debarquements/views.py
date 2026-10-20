from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Debarquement
from .forms import DebarquementForm
from sites.models import Site
from especes.models import Espece
from accounts.decorators import role_required


@login_required
def debarquement_list(request):
    recherche = request.GET.get('recherche', '').strip()
    date = request.GET.get('date', '').strip()
    site_id = request.GET.get('site', '').strip()
    espece_id = request.GET.get('espece', '').strip()

    debarquements = Debarquement.objects.select_related(
        'site',
        'espece',
        'agent',
        'valide_par'
    ).filter(archive=False)

    

    # Recherche par site ou espèce
    if recherche:
        debarquements = debarquements.filter(
            Q(espece__nom__icontains=recherche) |
            Q(site__nom__icontains=recherche)
        )

    # Filtre par date
    if date:
        debarquements = debarquements.filter(
            date=date
        )

    # Filtre par site
    if site_id:
        debarquements = debarquements.filter(
            site_id=site_id
        )

    # Filtre par espèce
    if espece_id:
        debarquements = debarquements.filter(
            espece_id=espece_id
        )

    # Sites actifs disponibles dans le filtre
    sites = Site.objects.filter(
        actif=True
    ).order_by('nom')

    # Espèces actives disponibles dans le filtre
    especes = Espece.objects.filter(
        actif=True
    ).order_by('nom')

    return render(
        request,
        'debarquements/list.html',
        {
            'debarquements': debarquements,
            'recherche': recherche,
            'date': date,
            'site_id': site_id,
            'espece_id': espece_id,
            'sites': sites,
            'especes': especes,
        }
    )


@role_required('admin', 'chef')
def debarquement_archive_list(request):
    debarquements = Debarquement.objects.filter(
        archive=True
    ).select_related(
        'site',
        'espece',
        'agent',
        'archive_par',
    )

    return render(
        request,
        'debarquements/archive_list.html',
        {'debarquements': debarquements},
    )


@role_required('admin', 'chef', 'agent')
def debarquement_create(request):

    if request.method == 'POST':
        form = DebarquementForm(request.POST)

        if form.is_valid():
            debarquement = form.save(commit=False)

            # L'agent connecté est automatiquement enregistré
            if request.user.is_agent():
                debarquement.agent = request.user

            debarquement.save()

            return redirect('debarquement_list')

    else:
        form = DebarquementForm()

    return render(
        request,
        'debarquements/form.html',
        {
            'form': form
        }
    )


@role_required('admin', 'chef', 'agent')
def debarquement_update(request, pk):

    # Un agent peut uniquement modifier ses propres débarquements
    debarquement = get_object_or_404(
        Debarquement,
        archive=False,
        pk=pk,
        **(
            {'agent': request.user}
            if request.user.is_agent()
            else {}
        )
    )

    # Un agent ne peut pas modifier un débarquement validé
    if (
        debarquement.statut == 'valide'
        and request.user.is_agent()
    ):
        return render(
            request,
            'accounts/access_denied.html',
            status=403
        )

    if request.method == 'POST':
        form = DebarquementForm(
            request.POST,
            instance=debarquement
        )

        if form.is_valid():
            form.save()
            return redirect('debarquement_list')

    else:
        form = DebarquementForm(
            instance=debarquement
        )

    return render(
        request,
        'debarquements/form.html',
        {
            'form': form
        }
    )


@role_required('admin', 'chef')
def debarquement_delete(request, pk):

    debarquement = get_object_or_404(
        Debarquement,
        archive=False,
        pk=pk
    )

    if request.method == 'POST':
        debarquement.archive = True
        debarquement.archive_le = timezone.now()
        debarquement.archive_par = request.user
        debarquement.save(
            update_fields=['archive', 'archive_le', 'archive_par', 'updated_at']
        )
        return redirect('debarquement_list')

    return render(
        request,
        'debarquements/delete.html',
        {
            'debarquement': debarquement
        }
    )


@role_required('admin', 'chef')
@require_POST
def debarquement_restore(request, pk):
    debarquement = get_object_or_404(
        Debarquement,
        pk=pk,
        archive=True,
    )
    debarquement.archive = False
    debarquement.save(update_fields=['archive', 'updated_at'])
    return redirect('debarquement_archive_list')


@login_required
def debarquement_detail(request, pk):

    debarquement = get_object_or_404(
    Debarquement.objects.select_related(
        'site',
        'espece',
        'agent',
        'valide_par'
    ),
    pk=pk,
    archive=False
)

    return render(
        request,
        'debarquements/detail.html',
        {
            'debarquement': debarquement
        }
    )


@role_required('admin', 'chef')
def debarquement_validate(request, pk):

    debarquement = get_object_or_404(
        Debarquement,
        archive=False,
        pk=pk
    )

    if request.method == 'POST':
        debarquement.statut = 'valide'
        debarquement.valide_par = request.user
        debarquement.valide_le = timezone.now()

        debarquement.save(
            update_fields=[
                'statut',
                'valide_par',
                'valide_le',
                'updated_at'
            ]
        )

    return redirect('debarquement_list')