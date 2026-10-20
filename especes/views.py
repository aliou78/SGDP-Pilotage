from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from .models import Espece
from .forms import EspeceForm
from django.contrib.auth.decorators import login_required
from accounts.decorators import role_required


@login_required
def espece_list(request):
    especes = Espece.objects.all().order_by('nom')

    return render(
        request,
        'especes/list.html',
        {'especes': especes}
    )


@role_required('admin', 'chef')
def espece_create(request):
    if request.method == 'POST':
        form = EspeceForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('espece_list')

    else:
        form = EspeceForm()

    return render(
        request,
        'especes/form.html',
        {'form': form}
    )


@role_required('admin', 'chef')
def espece_update(request, pk):
    espece = get_object_or_404(Espece, pk=pk)

    if request.method == 'POST':
        form = EspeceForm(request.POST, instance=espece)

        if form.is_valid():
            form.save()
            return redirect('espece_list')

    else:
        form = EspeceForm(instance=espece)

    return render(
        request,
        'especes/form.html',
        {'form': form}
    )


@role_required('admin', 'chef')
def espece_toggle_active(request, pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    espece = get_object_or_404(Espece, pk=pk)

    espece.actif = not espece.actif
    espece.save(update_fields=['actif'])

    return redirect('espece_list')