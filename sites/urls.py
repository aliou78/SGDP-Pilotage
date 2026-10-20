from django.urls import path
from . import views

urlpatterns = [
    path('', views.site_list, name='site_list'),
    path('ajouter/', views.site_create, name='site_create'),
    path('modifier/<int:pk>/', views.site_update, name='site_update'),
    path('activer-desactiver/<int:pk>/', views.site_toggle_active, name='site_toggle_active'),
]