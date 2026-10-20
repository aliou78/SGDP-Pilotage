from django.urls import path
from . import views

urlpatterns = [
    path('', views.rapport_list, name='rapport_list'),
    path(
        'excel/',
        views.rapport_excel,
        name='rapport_excel'
    ),
    path(
    'pdf/',
    views.rapport_pdf,
    name='rapport_pdf'
),
]