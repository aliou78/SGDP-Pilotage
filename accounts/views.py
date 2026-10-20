from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import User
from .forms import UserCreateForm, UserUpdateForm



@login_required
def user_list(request):

    if not request.user.is_admin():
        return render(
            request,
            'accounts/access_denied.html',
            status=403
        )

    recherche = request.GET.get('recherche', '').strip()
    utilisateurs = User.objects.all().order_by('username')
    if recherche:
        utilisateurs = utilisateurs.filter(
            Q(username__icontains=recherche) |
            Q(first_name__icontains=recherche) |
            Q(last_name__icontains=recherche) |
            Q(role__icontains=recherche)
        )

    context = {
        'utilisateurs': utilisateurs,
        'recherche': recherche,
    }

    return render(
        request,
        'accounts/user_list.html',
        context
    )


@login_required
def user_create(request):

    if not request.user.is_admin():
        return render(
            request,
            'accounts/access_denied.html',
            status=403
        )

    if request.method == 'POST':
        form = UserCreateForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('user_list')

    else:
        form = UserCreateForm()

    context = {
        'form': form,
    }

    return render(
        request,
        'accounts/user_form.html',
        context
    )


@login_required
def user_update(request, pk):
    if not request.user.is_admin():
        return render(request, 'accounts/access_denied.html', status=403)

    utilisateur = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=utilisateur)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserUpdateForm(instance=utilisateur)

    return render(request, 'accounts/user_form.html', {
        'form': form,
        'title': f'Modifier l’utilisateur : {utilisateur.username}',
    })


@login_required
def user_delete(request, pk):
    if not request.user.is_admin():
        return render(request, 'accounts/access_denied.html', status=403)

    utilisateur = get_object_or_404(User, pk=pk)
    if utilisateur == request.user:
        return render(request, 'accounts/access_denied.html', status=403)

    if request.method == 'POST':
        utilisateur.delete()
        return redirect('user_list')

    return render(request, 'accounts/user_delete.html', {
        'utilisateur': utilisateur,
    })


@login_required
def user_toggle_active(request, user_id):

    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    if not request.user.is_admin():
        return render(
            request,
            'accounts/access_denied.html',
            status=403
        )

    utilisateur = get_object_or_404(
        User,
        id=user_id
    )

    # Empêcher l'administrateur de désactiver son propre compte
    if utilisateur.id == request.user.id:
        return redirect('user_list')

    utilisateur.actif = not utilisateur.actif
    utilisateur.save(update_fields=['actif', 'is_active', 'updated_at'])

    return redirect('user_list')