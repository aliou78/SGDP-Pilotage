from django.urls import path
from . import views


urlpatterns = [
    path(
        '',
        views.debarquement_list,
        name='debarquement_list'
    ),

    path(
        'archives/',
        views.debarquement_archive_list,
        name='debarquement_archive_list'
    ),

    path(
        'restaurer/<int:pk>/',
        views.debarquement_restore,
        name='debarquement_restore'
    ),

    path(
        'ajouter/',
        views.debarquement_create,
        name='debarquement_create'
    ),

    path(
        'modifier/<int:pk>/',
        views.debarquement_update,
        name='debarquement_update'
    ),

    path(
        'supprimer/<int:pk>/',
        views.debarquement_delete,
        name='debarquement_delete'
    ),

    path(
        'valider/<int:pk>/',
        views.debarquement_validate,
        name='debarquement_validate'
    ),

    path(
        '<int:pk>/detail/',
        views.debarquement_detail,
        name='debarquement_detail'
    ),
]