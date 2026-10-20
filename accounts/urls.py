from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='accounts/login.html'
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    path(
        'utilisateurs/',
        views.user_list,
        name='user_list'
    ),

    path(
        'utilisateurs/creer/',
        views.user_create,
        name='user_create'
    ),
    path(
        'utilisateurs/<int:pk>/modifier/',
        views.user_update,
        name='user_update'
    ),
    path(
        'utilisateurs/<int:pk>/supprimer/',
        views.user_delete,
        name='user_delete'
    ),
    path(
    'utilisateurs/<int:user_id>/activer-desactiver/',
    views.user_toggle_active,
    name='user_toggle_active'
),
]