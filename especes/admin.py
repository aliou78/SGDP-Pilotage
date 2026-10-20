from django.contrib import admin
from .models import Espece


@admin.register(Espece)
class EspeceAdmin(admin.ModelAdmin):
    list_display = (
        "nom",
        "categorie",
        "actif",
    )

    search_fields = (
        "nom",
        "nom_scientifique",
    )

    list_filter = (
        "categorie",
        "actif",
    )