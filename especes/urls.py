from django.urls import path
from . import views

urlpatterns = [
    path('', views.espece_list, name='espece_list'),
    path('ajouter/', views.espece_create, name='espece_create'),
    path('modifier/<int:pk>/', views.espece_update, name='espece_update'),
    path(
    'activer-desactiver/<int:pk>/',
    views.espece_toggle_active,
    name='espece_toggle_active'
),
]