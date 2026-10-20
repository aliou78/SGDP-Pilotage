from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from .models import Site
from .forms import SiteForm
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required

@login_required
def site_list(request):
    sites = Site.objects.all().order_by('nom')
    return render(request, 'sites/list.html', {'sites': sites})

@role_required('admin', 'chef')
def site_create(request):
    if request.method == 'POST':
        form = SiteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('site_list')
    else:
        form = SiteForm()

    return render(request, 'sites/form.html', {
        'form': form,
        'title': 'Ajouter un Site',
    })

@role_required('admin', 'chef')
def site_update(request, pk):
    site = get_object_or_404(Site, pk=pk)

    if request.method == 'POST':
        form = SiteForm(request.POST, instance=site)
        if form.is_valid():
            form.save()
            return redirect('site_list')
    else:
        form = SiteForm(instance=site)

    return render(request, 'sites/form.html', {
        'form': form,
        'title': f'Modifier le site : {site.nom}',
    })

@role_required('admin', 'chef')
def site_toggle_active(request, pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    site = get_object_or_404(Site, pk=pk)
    site.actif = not site.actif
    site.save(update_fields=['actif', 'updated_at'])
    return redirect('site_list')